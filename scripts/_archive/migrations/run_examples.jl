"""
    run_examples.jl

End-to-end examples runner for components/aerosol/aq_eq/water.esm.

Walks every example's parameter_sweep, materializes the model per sweep
point, solves the ODEProblem, and records any run that fails. Closes the
acceptance gate item "examples simulate end-to-end".

Examples live in the raw JSON because EarthSciSerialization.Model does
not yet surface them as a struct field (migration-time note) — we parse
them from the document ourselves.

Exits 0 on success, non-zero if any example run fails.
"""

using ModelingToolkit
using OrdinaryDiffEqTsit5
using EarthSciSerialization
using EarthSciModels
using JSON3

const WATER_PATH = joinpath(@__DIR__, "..", "..", "components", "aerosol", "aq_eq", "water.esm")

function sweep_points(range_spec)
    start = Float64(range_spec[:start])
    stop = Float64(range_spec[:stop])
    count = Int(range_spec[:count])
    scale = get(range_spec, :scale, "linear")
    if scale == "linear"
        return collect(range(start, stop; length = count))
    elseif scale == "log"
        return collect(exp10.(range(log10(start), log10(stop); length = count)))
    else
        error("unknown range scale: $scale")
    end
end

function cartesian_points(sweep)
    dims = sweep[:dimensions]
    per_dim = Pair{String,Vector{Float64}}[]
    for dim in dims
        pname = String(dim[:parameter])
        if haskey(dim, :values)
            push!(per_dim, pname => Float64.(collect(dim[:values])))
        elseif haskey(dim, :range)
            push!(per_dim, pname => sweep_points(dim[:range]))
        else
            error("sweep dim lacks values/range: $dim")
        end
    end
    names = [p.first for p in per_dim]
    values = [p.second for p in per_dim]
    combos = collect(Iterators.product(values...))
    return [Dict(names[i] => c[i] for i in 1:length(names)) for c in combos]
end

function run_example(example, simp)
    ex_id = String(example[:id])
    tspan = (Float64(example[:time_span][:start]), Float64(example[:time_span][:end]))

    base_params = Dict{Symbol,Float64}()
    if haskey(example, :parameters) && example[:parameters] !== nothing
        for (k, v) in pairs(example[:parameters])
            base_params[Symbol(k)] = Float64(v)
        end
    end

    points = if haskey(example, :parameter_sweep) && example[:parameter_sweep] !== nothing
        cartesian_points(example[:parameter_sweep])
    else
        [Dict{String,Float64}()]
    end

    n_runs = length(points)
    n_fail = 0

    # Pre-resolve parameter symbols from the compiled system. The loader
    # prefixes sanitized names with the container ("anonymous_" for
    # unnamed containers, or "<System>_" when named); strip either so the
    # example's parameter names match.
    sym_map = Dict{Symbol,Any}()
    for p in ModelingToolkit.parameters(simp)
        raw = string(ModelingToolkit.getname(p))
        key = raw
        for prefix in ("anonymous_", "WaterEquilibrium_")
            if startswith(raw, prefix)
                key = raw[length(prefix)+1:end]
                break
            end
        end
        sym_map[Symbol(key)] = p
    end

    for (i, pt) in enumerate(points)
        merged_sym = Dict{Any,Float64}()
        for (k, v) in base_params
            haskey(sym_map, k) || error("unknown parameter $k in example $ex_id")
            merged_sym[sym_map[k]] = v
        end
        for (k, v) in pt
            sym = sym_map[Symbol(k)]
            merged_sym[sym] = v
        end
        try
            prob = ModelingToolkit.ODEProblem(simp, merged_sym, tspan)
            sol = solve(prob, Tsit5(); reltol = 1.0e-10, abstol = 1.0e-14)
            if sol.retcode !== ReturnCode.Success && sol.retcode !== ReturnCode.Default
                @warn "example $ex_id run $i non-success retcode" retcode = sol.retcode
                n_fail += 1
            end
        catch e
            @error "example $ex_id run $i errored" exception = (e, catch_backtrace()) params = pt
            n_fail += 1
        end
    end
    return n_runs, n_fail
end

println("── Loading water.esm ──────────────────────────────────────")
esm_file = EarthSciSerialization.load(WATER_PATH)
model = esm_file.models["WaterEquilibrium"]
sys = ModelingToolkit.System(model; name = :WaterEquilibrium)
simp = ModelingToolkit.mtkcompile(sys)

# Parse raw JSON to access examples (ESS Model struct doesn't expose them yet)
raw = JSON3.read(read(WATER_PATH, String))
examples = raw[:models][:WaterEquilibrium][:examples]
println("examples: ", length(examples))

function run_all(examples, simp)
    total_runs = 0
    total_fail = 0
    for example in examples
        println()
        println("── Example $(example[:id]) ────────────────────────────────")
        n_runs, n_fail = run_example(example, simp)
        println("  runs: $n_runs, failures: $n_fail")
        total_runs += n_runs
        total_fail += n_fail
    end
    return total_runs, total_fail
end

total_runs, total_fail = run_all(examples, simp)

println()
println("── Summary ────────────────────────────────────────────────")
println("total runs:    $total_runs")
println("total failures: $total_fail")

exit(total_fail == 0 ? 0 : 1)
