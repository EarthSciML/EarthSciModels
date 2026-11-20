#!/usr/bin/env julia
#=
render_example_plots.jl — evaluate `.esm` analyses and emit PNG plots.

Walks `components/**/*.esm` and, for every top-level component (model or
reaction system) carrying `analyses` (esm-spec §6.7) with `plots`, evaluates
the analysis and writes one PNG per plot to

    <esm_dir>/<esm_stem>.plots/<analysis_id>-<plot_id>.png

which is the artifact convention `tools/esm_to_docs.py` inlines on the
rendered component page.

Every number comes from the official Julia runner (AGENTS.md §1, §3):
`EarthSciAST.esm_problem` builds the problem, SciML's `solve` integrates it,
`remake` swaps parameter values between sweep points without rebuilding the
right-hand side, and `observed_field` reads observed quantities. Nothing here
walks the AST, derives classifications or integrates on its own.

Two analysis shapes are rendered:

- **Algebraic components** (the built problem has no state): a
  `parameter_sweep` grid, each point evaluated with `observed_field`. Plot
  types `line` and `scatter` (1-D sweep) and `heatmap` (2-D sweep).
- **ODE components** (the problem has states): one integration over
  `time_span`, or one per point of a 1-D `parameter_sweep`, starting from the
  states' declared defaults overridden by `initial_state`. A `line` plot with
  `x = t` draws the trajectories; one whose `x` is the swept parameter draws
  each trajectory's final value against the sweep.

Anything else is reported as a `[skip]` line and the walk continues.

Usage (from the repo root; the environment lives in tools/plots):

    julia --project=tools/plots tools/render_example_plots.jl
    julia --project=tools/plots tools/render_example_plots.jl --files a.esm b.esm
    julia --project=tools/plots tools/render_example_plots.jl --components-dir <dir>
=#

module RenderExamplePlots

using EarthSciAST
using EarthSciAST: EsmProblem, SimulateError
using SciMLBase
using OrdinaryDiffEqBDF: FBDF
using OrdinaryDiffEqRosenbrock: Rodas5P
using Printf: @sprintf

# GR draws headless with the `100` workstation type (no display in CI).
haskey(ENV, "GKSwstype") || (ENV["GKSwstype"] = "100")
import Plots

const REPO_ROOT = normpath(joinpath(@__DIR__, ".."))

# Number of output samples per trajectory (the time axis of every time-series
# plot, and what final-state plots take their last value from).
const N_TIME_POINTS = 200

# Integration tolerances. Tight enough that no plotted curve is visibly
# coarsened; the solver list is tried in order until one returns Success.
# FBDF is the workhorse — the corpus's large chemistry mechanisms are stiff,
# and on small non-stiff systems it costs little — and Rodas5P backs it up
# where a multistep method stalls (frequent discontinuities, tiny systems).
const RELTOL = 1e-8
const ABSTOL = 1e-12
const SOLVERS = (FBDF, Rodas5P)

const LINE_COLOR = "#1f4d8a"

"""Raised when an analysis or plot cannot be rendered; becomes a `[skip]` line."""
struct Unsupported <: Exception
    msg::String
end
Base.showerror(io::IO, e::Unsupported) = print(io, e.msg)

mutable struct RenderStats
    files_seen::Int
    analyses_seen::Int
    plots_rendered::Int
    plots_skipped::Int
end
RenderStats() = RenderStats(0, 0, 0, 0)

# Every progress line is flushed: in CI stdout is a pipe, and an unflushed
# buffer is what left the old Python job silent for hours at a time.
function say(args...)
    println(stdout, args...)
    flush(stdout)
end

_rel(path) = startswith(path, REPO_ROOT) ? relpath(path, REPO_ROOT) : path

# ---------------------------------------------------------------------------
# Reading the analysis block (raw JSON objects on the typed component)
# ---------------------------------------------------------------------------

_get(d, k, default = nothing) = d isa AbstractDict ? get(d, k, default) : default

_axis_var(axis) = axis isa AbstractDict ? _get(axis, "variable") : nothing

function _float_dict(d)
    out = Dict{String, Float64}()
    d isa AbstractDict || return out
    for (k, v) in d
        v isa Real || throw(Unsupported("parameter $(repr(k)) has a non-numeric value"))
        out[String(k)] = Float64(v)
    end
    return out
end

"""
    initial_state_values(analysis) -> (values, expression_vars)

The analysis's `initial_state`, in either spelling the schema admits
(esm-spec §11.4): a flat `{name: number}` map, or `{type, values}`. A value
that is not a number is an expression-typed (spatial-field) initial
condition; their names come back in `expression_vars`.
"""
function initial_state_values(analysis)
    ic = _get(analysis, "initial_state")
    ic isa AbstractDict || return Dict{String, Float64}(), String[]
    values = Set(keys(ic)) == Set(["type", "values"]) ? ic["values"] : ic
    values isa AbstractDict || return Dict{String, Float64}(), String[]
    expr_vars = sort!([String(k) for (k, v) in values if !(v isa Real)])
    isempty(expr_vars) || return Dict{String, Float64}(), expr_vars
    return Dict{String, Float64}(String(k) => Float64(v) for (k, v) in values), String[]
end

"""
    sweep_grid(sweep) -> (names, values, scales)

The dimensions of a cartesian `parameter_sweep`. `scales` is `:log` for a
log-spaced `range`, and for an explicit `values` list that is all positive and
spans at least a decade; `:linear` otherwise.
"""
function sweep_grid(sweep)
    type = _get(sweep, "type")
    type == "cartesian" || throw(Unsupported("unsupported sweep type: $(repr(type))"))
    dims = _get(sweep, "dimensions", Any[])
    isempty(dims) && throw(Unsupported("parameter_sweep has no dimensions"))
    names = String[]
    values = Vector{Vector{Float64}}()
    scales = Symbol[]
    for d in dims
        name = String(d["parameter"])
        if _get(d, "values") !== nothing
            arr = Float64.(d["values"])
            scale = length(arr) > 1 && all(>(0), arr) &&
                maximum(arr) / minimum(arr) >= 10 ? :log : :linear
        elseif _get(d, "range") !== nothing
            r = d["range"]
            start, stop, n = Float64(r["start"]), Float64(r["stop"]), Int(r["count"])
            scale = _get(r, "scale", "linear") == "log" ? :log : :linear
            arr = scale === :log ?
                exp10.(range(log10(start), log10(stop); length = n)) :
                collect(range(start, stop; length = n))
        else
            throw(Unsupported("dimension $(repr(name)) has neither values nor range"))
        end
        push!(names, name)
        push!(values, arr)
        push!(scales, scale)
    end
    return names, values, scales
end

function axis_scale(var, names, scales)
    i = var === nothing ? nothing : findfirst(==(var), names)
    return i === nothing ? :identity : (scales[i] === :log ? :log10 : :identity)
end

# ---------------------------------------------------------------------------
# Units, for default axis labels
# ---------------------------------------------------------------------------

function component_units(comp::Model)
    Dict{String, String}(k => v.units for (k, v) in comp.variables if v.units !== nothing)
end

function component_units(comp::ReactionSystem)
    out = Dict{String, String}()
    for s in comp.species
        s.units === nothing || (out[s.name] = s.units)
    end
    for p in comp.parameters
        p.units === nothing || (out[p.name] = p.units)
    end
    return out
end

# Declared scalar defaults, by bare name: what a value the shared build was
# given by another analysis falls back to (see `BaseProblem`).
function component_defaults(comp::Model)
    Dict{String, Float64}(k => v.default for (k, v) in comp.variables if v.default isa Float64)
end

function component_defaults(comp::ReactionSystem)
    out = Dict{String, Float64}()
    for s in comp.species
        s.default === nothing || (out[s.name] = s.default)
    end
    for p in comp.parameters
        p.default === nothing || (out[p.name] = p.default)
    end
    return out
end

function axis_label(axis, units)
    axis isa AbstractDict || return ""
    label = _get(axis, "label")
    label isa AbstractString && !isempty(label) && return String(label)
    var = _axis_var(axis)
    var === nothing && return ""
    u = get(units, var, nothing)
    return u === nothing ? String(var) : "$(var) [$(u)]"
end

# ---------------------------------------------------------------------------
# Problem construction and evaluation (the official runner)
# ---------------------------------------------------------------------------

"""
    find_key(keys, name) -> Union{String,Nothing}

Resolve a plot's (bare) variable name against the problem's namespaced names:
an exact hit, else the unique key ending in `.<name>`.
"""
function find_key(ks, name::AbstractString)
    name in ks && return String(name)
    suffix = "." * name
    hits = [String(k) for k in ks if endswith(k, suffix)]
    length(hits) == 1 && return hits[1]
    return nothing
end

"""
    with_overrides(prob, p, u0) -> EsmProblem

`prob` with parameter overrides `p` and initial-state overrides `u0`, by
`remake` (a value swap that shares the compiled right-hand side). A name that
is a state rather than a parameter is moved to `u0`, so a sweep over an
initial concentration works. If a parameter cannot be swapped without a
rebuild (`:structural`), `nothing` is returned and the caller rebuilds.
"""
function with_overrides(prob::EsmProblem, p::AbstractDict, u0::AbstractDict)
    pp = Dict{String, Float64}()
    uu = Dict{String, Float64}(u0)
    states = keys(prob.var_map)
    for (k, v) in p
        if find_key(propertynames(prob.p) .|> String, k) === nothing &&
                find_key(states, k) !== nothing
            uu[k] = v
        else
            pp[k] = v
        end
    end
    try
        return remake(prob; p = pp, u0 = uu)
    catch err
        err isa SimulateError || rethrow()
        return nothing
    end
end

"""Build a fresh problem (when `remake` cannot honour an override)."""
function build_problem(input, tspan, p, u0)
    return esm_problem(input, tspan; p = Dict{String, Any}(p), u0 = Dict{String, Any}(u0))
end

"""
A component's shared build: the problem plus the overrides it was built with.

Many documents leave a parameter or a state without a `default` and rely on
each analysis to supply it, so the build has to carry the first analysis's
values. A later analysis that does not name one of those values gets the
declared default back (`defaults`); where there is none, it is rebuilt with
its own values, which is the build that would have failed (or not) on its
own terms.
"""
struct BaseProblem
    prob::EsmProblem
    p::Dict{String, Float64}
    u0::Dict{String, Float64}
    defaults::Dict{String, Float64}
end

# Overrides for `wanted`, plus the declared default of every key the base was
# built with that `wanted` does not name; `nothing` if one has no default.
function _restore_defaults(wanted, built, defaults)
    out = Dict{String, Float64}(wanted)
    for k in keys(built)
        haskey(out, k) && continue
        d = get(defaults, k, nothing)
        d === nothing && return nothing
        out[k] = d
    end
    return out
end

function problem_for(base::BaseProblem, input, tspan, p, u0)
    pp = _restore_defaults(p, base.p, base.defaults)
    uu = _restore_defaults(u0, base.u0, base.defaults)
    q = (pp === nothing || uu === nothing) ? nothing :
        with_overrides(remake(base.prob; tspan = tspan), pp, uu)
    return q === nothing ? build_problem(input, tspan, p, u0) : q
end

function problem_for(base::EsmProblem, input, tspan, p, u0)
    return problem_for(BaseProblem(base, Dict{String, Float64}(), Dict{String, Float64}(),
        Dict{String, Float64}()), input, tspan, p, u0)
end

function solve_problem(prob::EsmProblem, tspan)
    saveat = collect(range(tspan[1], tspan[2]; length = N_TIME_POINTS))
    last_msg = ""
    for Alg in SOLVERS
        sol = try
            solve(prob, Alg(); reltol = RELTOL, abstol = ABSTOL, saveat = saveat)
        catch err
            err isa InterruptException && rethrow()
            last_msg = "$(nameof(Alg)): $(first(sprint(showerror, err), 300))"
            continue
        end
        SciMLBase.successful_retcode(sol) && return sol
        last_msg = "$(nameof(Alg)): retcode $(sol.retcode)"
    end
    throw(Unsupported("ODE integration failed ($last_msg)"))
end

_scalar(v::Real) = Float64(v)
function _scalar(v::AbstractArray)
    length(v) == 1 || throw(Unsupported("variable is not a scalar (size $(size(v)))"))
    return Float64(first(v))
end

"""Read variable `name` from `prob` at state `u` / time `t` (a parameter or an observed)."""
function read_value(prob::EsmProblem, name::AbstractString, u, t)
    pk = find_key(propertynames(prob.p) .|> String, name)
    pk === nothing || return _scalar(getproperty(prob.p, Symbol(pk)))
    v = try
        observed_field(prob, name; u = u, t = t)
    catch err
        # Out-of-domain arithmetic at one grid point (a `sqrt` of -4e-16 from
        # round-off, say) is a gap in the curve, not a lost analysis.
        err isa DomainError && return NaN
        err isa SimulateError || rethrow()
        throw(Unsupported("cannot evaluate $(repr(name)): $(first(sprint(showerror, err), 300))"))
    end
    x = _scalar(v)
    return isfinite(x) ? x : NaN
end

"""
    trajectory_env(prob, sol, names) -> Dict{String, Vector{Float64}}

`t` plus the trajectory of every name in `names`: states straight from the
solution, parameters as constants, observeds through `observed_field` at each
saved point.
"""
function trajectory_env(prob::EsmProblem, sol, names)
    env = Dict{String, Vector{Float64}}("t" => Float64.(sol.t))
    states = keys(prob.var_map)
    for name in names
        (name === nothing || name == "t" || haskey(env, name)) && continue
        sk = find_key(states, name)
        if sk !== nothing
            idx = prob.var_map[sk]
            env[name] = [Float64(u[idx]) for u in sol.u]
        else
            env[name] = [read_value(prob, name, sol.u[k], sol.t[k]) for k in eachindex(sol.t)]
        end
    end
    return env
end

# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------

# Long descriptions are wrapped onto several title lines rather than running
# off the canvas.
function wrap_title(s::AbstractString; width = 80, max_lines = 4)
    words = split(s)
    lines = String[]
    cur = ""
    for w in words
        if isempty(cur)
            cur = String(w)
        elseif length(cur) + 1 + length(w) <= width
            cur *= " " * w
        else
            push!(lines, cur)
            cur = String(w)
        end
    end
    isempty(cur) || push!(lines, cur)
    if length(lines) > max_lines
        lines = lines[1:max_lines]
        lines[end] *= " …"
    end
    return join(lines, "\n")
end

plot_title(plot) = wrap_title(String(something(_get(plot, "description"), _get(plot, "id"), "")))

function new_figure(plot; size = (720, 480))
    title = plot_title(plot)
    nlines = isempty(title) ? 0 : count(==('\n'), title) + 1
    return Plots.plot(;
        size = (size[1], size[2] + 14 * max(0, nlines - 1)),
        dpi = 100, title = title, titlefontsize = 8, guidefontsize = 9,
        tickfontsize = 8, legendfontsize = 7, gridalpha = 0.3, minorgrid = false,
        framestyle = :box, margin = 4Plots.mm, legend = false,
    )
end

function save_figure(fig, out_path)
    mkpath(dirname(out_path))
    Plots.savefig(fig, out_path)
    return nothing
end

# A plot's `y` is one axis or (esm schema) a list of them: several series on a
# shared x. Returned as a vector either way.
y_axes(plot) = (y = _get(plot, "y"); y isa AbstractVector ? collect(y) : [y])

function render_line_or_scatter(kind, plot, names, values, scales, env, units, out_path)
    length(values) == 1 ||
        throw(Unsupported("$kind plot needs 1D sweep, got $(length(values))D"))
    xv = _axis_var(plot["x"])
    x = get(env, xv, nothing)
    x === nothing && throw(Unsupported("$kind plot x references unbound variable: $(repr(xv))"))
    axes = y_axes(plot)
    multi = length(axes) > 1
    fig = new_figure(plot)
    cmap = Plots.cgrad(:viridis)
    for (i, axis) in enumerate(axes)
        yv = _axis_var(axis)
        y = get(env, yv, nothing)
        y === nothing && throw(Unsupported("$kind plot y references unbound variable: $(repr(yv))"))
        y isa Real && (y = fill(Float64(y), length(x)))
        color = multi ? cmap[(i - 1) / (length(axes) - 1)] : LINE_COLOR
        label = multi ? axis_label(axis, units) : ""
        if kind == "line"
            Plots.plot!(fig, x, y; color = color, linewidth = 2, label = label)
        else
            Plots.scatter!(fig, x, y; color = color, markersize = 4, markeralpha = 0.85,
                markerstrokewidth = 0, label = label)
        end
    end
    multi && Plots.plot!(fig; legend = :best)
    yv1 = _axis_var(axes[1])
    Plots.plot!(fig; xlabel = axis_label(plot["x"], units),
        ylabel = multi ? "" : axis_label(axes[1], units),
        xscale = axis_scale(xv, names, scales), yscale = axis_scale(yv1, names, scales))
    save_figure(fig, out_path)
end

function render_heatmap(plot, names, values, scales, env, units, out_path)
    length(values) == 2 ||
        throw(Unsupported("heatmap plot needs 2D sweep, got $(length(values))D"))
    _get(plot, "value") isa AbstractDict ||
        throw(Unsupported("heatmap plot is missing 'value' axis"))
    xv, yv, vv = _axis_var(plot["x"]), _axis_var(plot["y"]), _axis_var(plot["value"])
    (xv in names && yv in names && haskey(env, vv)) ||
        throw(Unsupported("heatmap references unbound: x=$xv y=$yv value=$vv"))
    xi, yi = findfirst(==(xv), names), findfirst(==(yv), names)
    z = env[vv]
    z isa Real && (z = fill(Float64(z), length(values[1]), length(values[2])))
    # The grid is indexed [dim1, dim2]; Plots wants rows = y, columns = x.
    zyx = xi == 1 ? permutedims(z) : z
    fig = new_figure(plot; size = (720, 540))
    Plots.heatmap!(fig, values[xi], values[yi], zyx; color = :viridis,
        colorbar = true, colorbar_title = axis_label(plot["value"], units),
        xlabel = axis_label(plot["x"], units), ylabel = axis_label(plot["y"], units),
        xscale = axis_scale(xv, names, scales), yscale = axis_scale(yv, names, scales))
    save_figure(fig, out_path)
end

function render_time_series(plot, trajectories, units, out_path)
    type = _get(plot, "type")
    type == "line" || throw(Unsupported(
        "time-series plot type $(repr(type)) not supported (use 'line' with x.variable='t')"))
    xv = _axis_var(plot["x"])
    xv == "t" || throw(Unsupported(
        "time-series line plot requires x.variable='t', got $(repr(xv))"))
    yv = _axis_var(_get(plot, "y"))
    fig = new_figure(plot)
    n = length(trajectories)
    cmap = Plots.cgrad(:viridis)
    for (i, (label, env)) in enumerate(trajectories)
        haskey(env, yv) || throw(Unsupported(
            "time-series line plot y references unbound variable: $(repr(yv))"))
        color = n > 1 ? cmap[(i - 1) / (n - 1)] : LINE_COLOR
        Plots.plot!(fig, env["t"], env[yv]; color = color, linewidth = 2,
            label = label === nothing ? "" : label)
    end
    n > 1 && any(t -> t[1] !== nothing, trajectories) && Plots.plot!(fig; legend = :best)
    Plots.plot!(fig; xlabel = axis_label(plot["x"], units), ylabel = axis_label(plot["y"], units))
    save_figure(fig, out_path)
end

function render_final_state_vs_sweep(plot, sweep_name, sweep_values, sweep_scale,
        trajectories, units, out_path)
    type = _get(plot, "type")
    type == "line" || throw(Unsupported(
        "final-state-vs-sweep plot type $(repr(type)) not supported (use 'line')"))
    yv = _axis_var(_get(plot, "y"))
    yv === nothing && throw(Unsupported("plot y has no variable"))
    finals = map(trajectories) do (_, env)
        haskey(env, yv) || throw(Unsupported(
            "final-state plot y references unbound variable: $(repr(yv))"))
        env[yv][end]
    end
    fig = new_figure(plot)
    Plots.plot!(fig, sweep_values, finals; color = LINE_COLOR, linewidth = 2,
        marker = :circle, markersize = 4, markerstrokewidth = 0,
        xlabel = axis_label(plot["x"], units), ylabel = axis_label(plot["y"], units),
        xscale = sweep_scale === :log ? :log10 : :identity)
    save_figure(fig, out_path)
end

function render_placeholder(plot, expression_vars, out_path)
    fig = new_figure(plot)
    Plots.plot!(fig; axis = false, grid = false, ticks = false, framestyle = :none,
        xlims = (0, 1), ylims = (0, 1))
    Plots.annotate!(fig, 0.5, 0.5, Plots.text(
        "⟨expression IC: $(join(expression_vars, ", "))⟩\n(rendered with state defaults)",
        11, "#555555", :center))
    save_figure(fig, out_path)
end

# ---------------------------------------------------------------------------
# Per-analysis drivers
# ---------------------------------------------------------------------------

struct Ctx
    esm_path::String
    cname::String
    units::Dict{String, String}
    defaults::Dict{String, Float64}
    plots_dir::String
    stats::RenderStats
end

function skip_all(ctx::Ctx, analysis, msg)
    for _ in _get(analysis, "plots", Any[])
        ctx.stats.plots_skipped += 1
        say("[skip] ", basename(ctx.esm_path), "::", ctx.cname, " analysis ",
            repr(String(something(_get(analysis, "id"), "analysis"))), ": ", msg)
    end
end

out_path(ctx::Ctx, aid, plot) =
    joinpath(ctx.plots_dir, "$(aid)-$(something(_get(plot, "id"), "plot")).png")

"""Run `f()` for one plot, turning failures into a `[skip]` line."""
function render_plot(f, ctx::Ctx, aid, plot; note = "")
    pid = something(_get(plot, "id"), "plot")
    path = out_path(ctx, aid, plot)
    try
        f(path)
    catch err
        err isa InterruptException && rethrow()
        ctx.stats.plots_skipped += 1
        msg = err isa Unsupported ? err.msg : first(sprint(showerror, err), 400)
        say("[skip] ", basename(ctx.esm_path), "::", ctx.cname, " analysis ", aid,
            " plot ", pid, ": ", msg)
        return
    end
    ctx.stats.plots_rendered += 1
    say("[ok]   ", _rel(path), note)
end

plot_vars(plots) = unique(filter(!isnothing, vcat(
    [_axis_var(_get(p, ax)) for p in plots for ax in ("x", "value")],
    [_axis_var(a) for p in plots for a in y_axes(p)])))

function render_algebraic(ctx::Ctx, input, base::BaseProblem, analysis, tspan)
    plots = analysis["plots"]
    sweep = _get(analysis, "parameter_sweep")
    if sweep === nothing
        skip_all(ctx, analysis, "no parameter_sweep and no initial_state (nothing to evaluate)")
        return
    end
    ctx.stats.analyses_seen += 1
    aid = String(something(_get(analysis, "id"), "analysis"))
    params = _float_dict(_get(analysis, "parameters"))
    local names, values, scales, env
    try
        names, values, scales = sweep_grid(sweep)
        shape = Tuple(length.(values))
        targets = filter(v -> !(v in names), plot_vars(plots))
        env = Dict{String, Any}(names[i] => values[i] for i in eachindex(names))
        # A swept axis broadcast over the grid, for line/scatter of it vs itself.
        grids = Dict(t => fill(NaN, shape) for t in targets)
        errors = Dict{String, String}()
        t0 = Float64(tspan[1])
        for I in CartesianIndices(shape)
            p = copy(params)
            for (d, name) in enumerate(names)
                p[name] = values[d][I[d]]
            end
            q = problem_for(base, input, tspan, p, Dict{String, Float64}())
            for t in targets
                haskey(errors, t) && continue
                try
                    grids[t][I] = read_value(q, t, nothing, t0)
                catch err
                    err isa Unsupported || rethrow()
                    errors[t] = err.msg
                end
            end
        end
        for t in targets
            haskey(errors, t) || (env[t] = length(shape) == 1 ? vec(grids[t]) : grids[t])
        end
        for (k, v) in params
            haskey(env, k) || (env[k] = v)
        end
        # Unbound plot variables surface below as each plot's own skip line.
    catch err
        err isa Unsupported || rethrow()
        skip_all(ctx, analysis, err.msg)
        return
    end
    for plot in plots
        type = _get(plot, "type")
        render_plot(ctx, aid, plot) do path
            if type == "line" || type == "scatter"
                render_line_or_scatter(type, plot, names, values, scales, env, ctx.units, path)
            elseif type == "heatmap"
                render_heatmap(plot, names, values, scales, env, ctx.units, path)
            else
                throw(Unsupported("unsupported plot type $(repr(type))"))
            end
        end
    end
end

function render_dynamic(ctx::Ctx, input, base::BaseProblem, analysis, tspan, ic)
    plots = analysis["plots"]
    ctx.stats.analyses_seen += 1
    aid = String(something(_get(analysis, "id"), "analysis"))
    params = _float_dict(_get(analysis, "parameters"))
    sweep = _get(analysis, "parameter_sweep")
    sweep_name, sweep_values, sweep_scale = nothing, Float64[], :linear
    runs = Tuple{Union{String, Nothing}, Dict{String, Float64}}[]
    trajectories = Tuple{Union{String, Nothing}, Dict{String, Vector{Float64}}}[]
    try
        if sweep === nothing
            push!(runs, (nothing, params))
        else
            names, values, scales = sweep_grid(sweep)
            length(names) == 1 || throw(Unsupported(
                "time-series + sweep needs 1D sweep, got $(length(names))D"))
            sweep_name, sweep_values, sweep_scale = names[1], values[1], scales[1]
            for v in sweep_values
                p = copy(params)
                p[sweep_name] = v
                push!(runs, (@sprintf("%s=%.3g", sweep_name, v), p))
            end
        end
        wanted = plot_vars(plots)
        for (label, p) in runs
            q = problem_for(base, input, tspan, p, ic)
            sol = solve_problem(q, tspan)
            push!(trajectories, (label, trajectory_env(q, sol, filter(!=(sweep_name), wanted))))
        end
    catch err
        err isa Unsupported || rethrow()
        skip_all(ctx, analysis, err.msg)
        return
    end
    for plot in plots
        render_plot(ctx, aid, plot) do path
            if sweep_name !== nothing && _axis_var(_get(plot, "x")) == sweep_name
                render_final_state_vs_sweep(plot, sweep_name, sweep_values, sweep_scale,
                    trajectories, ctx.units, path)
            else
                render_time_series(plot, trajectories, ctx.units, path)
            end
        end
    end
end

function analysis_tspan(analysis)
    ts = _get(analysis, "time_span")
    ts isa AbstractDict || return (0.0, 1.0)
    start, stop = _get(ts, "start", 0.0), _get(ts, "end", 1.0)
    (start isa Real && stop isa Real) ||
        throw(Unsupported("time_span with non-numeric bounds is not supported"))
    return (Float64(start), Float64(stop))
end

# The values an analysis supplies for the build: its `parameters`, plus the
# first point of its sweep (a swept parameter often has no default).
function build_overrides(analysis)
    p = _float_dict(_get(analysis, "parameters"))
    sweep = _get(analysis, "parameter_sweep")
    if sweep !== nothing
        names, values, _ = sweep_grid(sweep)
        for (n, v) in zip(names, values)
            isempty(v) || (p[n] = v[1])
        end
    end
    return p
end

function render_analysis(ctx::Ctx, input, base_ref::Ref{Any}, analysis)
    plots = _get(analysis, "plots", Any[])
    isempty(plots) && return
    aid = String(something(_get(analysis, "id"), "analysis"))
    ic, expression_vars = initial_state_values(analysis)
    if !isempty(expression_vars)
        # esm-spec §11.4: a renderer that cannot evaluate a spatial-field
        # initial condition must not crash and must make its output visibly
        # different from a scalar-IC plot.
        ctx.stats.analyses_seen += 1
        for plot in plots
            render_plot(ctx, aid, plot;
                note = " (expression IC: $(join(expression_vars, ", ")))") do path
                render_placeholder(plot, expression_vars, path)
            end
        end
        return
    end
    local tspan, base
    try
        tspan = analysis_tspan(analysis)
        # One build per component, shared by every analysis on it (see
        # `BaseProblem`). A failed build is not cached: the next analysis may
        # supply the values this one lacked.
        if base_ref[] === nothing
            p = build_overrides(analysis)
            prob = try
                build_problem(input, tspan, p, ic)
            catch err
                err isa InterruptException && rethrow()
                throw(Unsupported("problem build failed: $(first(sprint(showerror, err), 400))"))
            end
            base_ref[] = BaseProblem(prob, p, ic, ctx.defaults)
        end
        base = base_ref[]
    catch err
        err isa Unsupported || rethrow()
        skip_all(ctx, analysis, err.msg)
        return
    end
    if isempty(base.prob.u0)
        render_algebraic(ctx, input, base, analysis, tspan)
    else
        render_dynamic(ctx, input, base, analysis, tspan, ic)
    end
end

function render_file(esm_path::AbstractString, stats::RenderStats)
    file = try
        load_path(String(esm_path))
    catch err
        err isa InterruptException && rethrow()
        say("[skip] ", basename(esm_path), ": ESS load failed: ",
            first(sprint(showerror, err), 400))
        return
    end
    plots_dir = joinpath(dirname(esm_path), splitext(basename(esm_path))[1] * ".plots")
    comps = Pair{String, Any}[]
    file.models === nothing || append!(comps, collect(file.models))
    file.reaction_systems === nothing || append!(comps, collect(file.reaction_systems))
    for (cname, comp) in comps
        isempty(comp.analyses) && continue
        # A component is rendered on its own, as the analysis describes it.
        input = length(comps) == 1 ? file : EarthSciAST.extract(file, cname)
        ctx = Ctx(esm_path, cname, component_units(comp), component_defaults(comp), plots_dir, stats)
        base_ref = Ref{Any}(nothing)
        for analysis in comp.analyses
            try
                render_analysis(ctx, input, base_ref, analysis)
            catch err
                err isa InterruptException && rethrow()
                skip_all(ctx, analysis, "unexpected error: $(first(sprint(showerror, err), 400))")
            end
        end
    end
end

# ---------------------------------------------------------------------------
# Discovery + CLI
# ---------------------------------------------------------------------------

function discover_esm_files(root::AbstractString)
    files = String[]
    for (dir, _, fs) in walkdir(root)
        for f in fs
            endswith(f, ".esm") && push!(files, joinpath(dir, f))
        end
    end
    return sort!(files)
end

function run_files(files::AbstractVector{<:AbstractString})
    if isempty(files)
        say("warning: no .esm files to render")
        return 0
    end
    stats = RenderStats()
    t0 = time()
    for f in files
        stats.files_seen += 1
        tf = time()
        render_file(f, stats)
        dt = time() - tf
        dt > 10 && say(@sprintf("[time] %s: %.1fs", _rel(f), dt))
    end
    say()
    say(@sprintf(
        "render_example_plots: %d plot(s) rendered, %d skipped, %d analyses seen across %d .esm file(s) in %.2fs",
        stats.plots_rendered, stats.plots_skipped, stats.analyses_seen, stats.files_seen,
        time() - t0))
    return 0
end

const USAGE = """
usage: julia --project=tools/plots tools/render_example_plots.jl [--components-dir DIR | --files F.esm ...]
"""

function main(args::Vector{String} = ARGS)
    components_dir = nothing
    files = String[]
    i = 1
    while i <= length(args)
        a = args[i]
        if a == "--components-dir"
            i += 1
            i <= length(args) || (println(stderr, USAGE); return 2)
            components_dir = args[i]
        elseif a == "--files"
            while i < length(args) && !startswith(args[i + 1], "--")
                i += 1
                push!(files, args[i])
            end
        elseif a in ("-h", "--help")
            print(USAGE)
            return 0
        else
            println(stderr, "unknown argument: $a\n", USAGE)
            return 2
        end
        i += 1
    end
    if !isempty(files) && components_dir !== nothing
        println(stderr, "--files and --components-dir are mutually exclusive")
        return 2
    end
    if !isempty(files)
        resolved = String[]
        for f in files
            p = isabspath(f) ? f : joinpath(REPO_ROOT, f)
            isfile(p) || (println(stderr, "ERROR: --files: not found: $p"); return 2)
            endswith(p, ".esm") || (println(stderr, "ERROR: --files: not a .esm file: $p"); return 2)
            push!(resolved, normpath(abspath(p)))
        end
        return run_files(sort!(unique(resolved)))
    end
    root = normpath(abspath(something(components_dir, joinpath(REPO_ROOT, "components"))))
    if !isdir(root)
        println(stderr, "error: components/ not found at $root")
        return 2
    end
    return run_files(discover_esm_files(root))
end

end # module

if abspath(PROGRAM_FILE) == @__FILE__
    exit(RenderExamplePlots.main())
end
