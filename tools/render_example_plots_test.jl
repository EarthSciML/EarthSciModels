#=
Tests for tools/render_example_plots.jl.

Run from the repo root:

    julia --project=tools/plots tools/render_example_plots_test.jl

The fixtures are tiny self-contained documents written to a temporary
directory, so the tests exercise the renderer, not the corpus.
=#

using Test
using JSON3

include(joinpath(@__DIR__, "render_example_plots.jl"))
const R = RenderExamplePlots

# y = a^2 * b — algebraic (the built problem has no state).
const ALGEBRAIC = Dict(
    "esm" => "1.0.0",
    "metadata" => Dict("name" => "Square"),
    "models" => Dict("Square" => Dict(
        "variables" => Dict(
            "a" => Dict("type" => "parameter", "units" => "m", "default" => 1.0),
            "b" => Dict("type" => "parameter", "units" => "1", "default" => 2.0),
            "y" => Dict("type" => "unknown", "units" => "m^2"),
        ),
        "equations" => [Dict(
            "lhs" => "y",
            "rhs" => Dict("op" => "*", "args" => [
                Dict("op" => "^", "args" => ["a", 2]), "b"]),
        )],
        "analyses" => [
            Dict("id" => "line_a", "description" => "y vs a",
                "time_span" => Dict("start" => 0, "end" => 1),
                "parameter_sweep" => Dict("type" => "cartesian", "dimensions" => [
                    Dict("parameter" => "a",
                        "range" => Dict("start" => 0.1, "stop" => 10.0, "count" => 5, "scale" => "log"))]),
                "plots" => [
                    Dict("id" => "y_vs_a", "type" => "line", "x" => Dict("variable" => "a"),
                        "y" => Dict("variable" => "y")),
                    Dict("id" => "y_vs_a_pts", "type" => "scatter", "x" => Dict("variable" => "a"),
                        "y" => Dict("variable" => "y")),
                    Dict("id" => "snap", "type" => "field_snapshot", "at_time" => 0.5,
                        "x" => Dict("variable" => "a"), "y" => Dict("variable" => "b"),
                        "value" => Dict("variable" => "y")),
                    Dict("id" => "missing", "type" => "line", "x" => Dict("variable" => "a"),
                        "y" => Dict("variable" => "nope")),
                    Dict("id" => "two_series", "type" => "line", "x" => Dict("variable" => "a"),
                        "y" => [Dict("variable" => "y"), Dict("variable" => "b", "label" => "b")]),
                ]),
            Dict("id" => "heat", "description" => "y over (a, b)",
                "time_span" => Dict("start" => 0, "end" => 1),
                "parameter_sweep" => Dict("type" => "cartesian", "dimensions" => [
                    Dict("parameter" => "a", "values" => [1.0, 2.0, 3.0]),
                    Dict("parameter" => "b", "values" => [1.0, 10.0, 100.0, 1000.0])]),
                "plots" => [Dict("id" => "y_heat", "type" => "heatmap",
                    "x" => Dict("variable" => "b"), "y" => Dict("variable" => "a"),
                    "value" => Dict("variable" => "y"))]),
            Dict("id" => "nothing_to_do", "description" => "no sweep",
                "time_span" => Dict("start" => 0, "end" => 1),
                "plots" => [Dict("id" => "p", "type" => "line", "x" => Dict("variable" => "a"),
                    "y" => Dict("variable" => "y"))]),
        ],
    )),
)

# D(x) = -k x, with observed z = 2 x.
const DECAY = Dict(
    "esm" => "1.0.0",
    "metadata" => Dict("name" => "Decay"),
    "models" => Dict("Decay" => Dict(
        "variables" => Dict(
            "x" => Dict("type" => "unknown", "units" => "1", "default" => 1.0),
            "z" => Dict("type" => "unknown", "units" => "1"),
            "k" => Dict("type" => "parameter", "units" => "s^-1", "default" => 1.0),
        ),
        "equations" => [
            Dict("lhs" => Dict("op" => "D", "wrt" => "t", "args" => ["x"]),
                "rhs" => Dict("op" => "*", "args" => [Dict("op" => "-", "args" => ["k"]), "x"])),
            Dict("lhs" => "z", "rhs" => Dict("op" => "*", "args" => [2, "x"])),
        ],
        "analyses" => [
            Dict("id" => "single", "description" => "one run",
                "time_span" => Dict("start" => 0, "end" => 2),
                "initial_state" => Dict("x" => 3.0),
                "plots" => [
                    Dict("id" => "x_t", "type" => "line", "x" => Dict("variable" => "t"),
                        "y" => Dict("variable" => "x")),
                    Dict("id" => "z_t", "type" => "line", "x" => Dict("variable" => "t"),
                        "y" => Dict("variable" => "z")),
                ]),
            Dict("id" => "k_sweep", "description" => "family",
                "time_span" => Dict("start" => 0, "end" => 1),
                "parameter_sweep" => Dict("type" => "cartesian", "dimensions" => [
                    Dict("parameter" => "k", "values" => [0.5, 1.0, 2.0])]),
                "plots" => [
                    Dict("id" => "family", "type" => "line", "x" => Dict("variable" => "t"),
                        "y" => Dict("variable" => "x")),
                    Dict("id" => "final", "type" => "line", "x" => Dict("variable" => "k"),
                        "y" => Dict("variable" => "x")),
                ]),
            Dict("id" => "two_d", "description" => "2-D sweep of an ODE",
                "time_span" => Dict("start" => 0, "end" => 1),
                "parameter_sweep" => Dict("type" => "cartesian", "dimensions" => [
                    Dict("parameter" => "k", "values" => [0.5, 1.0]),
                    Dict("parameter" => "x", "values" => [1.0, 2.0])]),
                "plots" => [Dict("id" => "h", "type" => "heatmap", "x" => Dict("variable" => "k"),
                    "y" => Dict("variable" => "x"), "value" => Dict("variable" => "z"))]),
        ],
    )),
)

# y = a * c, where `c` has no default: every analysis must supply it.
const NO_DEFAULT = Dict(
    "esm" => "1.0.0",
    "metadata" => Dict("name" => "NoDefault"),
    "models" => Dict("NoDefault" => Dict(
        "variables" => Dict(
            "a" => Dict("type" => "parameter", "units" => "1", "default" => 1.0),
            "c" => Dict("type" => "parameter", "units" => "1"),
            "y" => Dict("type" => "unknown", "units" => "1"),
        ),
        "equations" => [Dict("lhs" => "y", "rhs" => Dict("op" => "*", "args" => ["a", "c"]))],
        "analyses" => [
            Dict("id" => "first", "description" => "sets a",
                "time_span" => Dict("start" => 0, "end" => 1),
                "parameters" => Dict("a" => 5.0),
                "parameter_sweep" => Dict("type" => "cartesian", "dimensions" => [
                    Dict("parameter" => "c", "values" => [1.0, 2.0])]),
                "plots" => [Dict("id" => "y_c", "type" => "line", "x" => Dict("variable" => "c"),
                    "y" => Dict("variable" => "y"))]),
            Dict("id" => "second", "description" => "leaves a at its default",
                "time_span" => Dict("start" => 0, "end" => 1),
                "parameter_sweep" => Dict("type" => "cartesian", "dimensions" => [
                    Dict("parameter" => "c", "values" => [3.0, 4.0])]),
                "plots" => [Dict("id" => "y_c", "type" => "line", "x" => Dict("variable" => "c"),
                    "y" => Dict("variable" => "y"))]),
        ],
    )),
)

function write_fixture(dir, name, doc)
    path = joinpath(dir, name)
    open(io -> JSON3.write(io, doc), path, "w")
    return path
end

@testset "render_example_plots" begin
    @testset "sweep_grid" begin
        names, values, scales = R.sweep_grid(Dict("type" => "cartesian", "dimensions" => [
            Dict("parameter" => "a", "range" => Dict("start" => 1, "stop" => 100, "count" => 3, "scale" => "log")),
            Dict("parameter" => "b", "values" => [1, 2, 3]),
            Dict("parameter" => "c", "values" => [1, 50]),
        ]))
        @test names == ["a", "b", "c"]
        @test values[1] ≈ [1.0, 10.0, 100.0]
        @test scales == [:log, :linear, :log]
        @test_throws R.Unsupported R.sweep_grid(Dict("type" => "latin_hypercube", "dimensions" => []))
        @test_throws R.Unsupported R.sweep_grid(Dict("type" => "cartesian", "dimensions" => []))
    end

    @testset "initial_state_values" begin
        @test R.initial_state_values(Dict("initial_state" => Dict("x" => 1))) ==
            (Dict("x" => 1.0), String[])
        @test R.initial_state_values(Dict("initial_state" =>
            Dict("type" => "per_variable", "values" => Dict("x" => 2.0)))) == (Dict("x" => 2.0), String[])
        _, ev = R.initial_state_values(Dict("initial_state" =>
            Dict("type" => "expression", "values" => Dict("u" => Dict("op" => "sin", "args" => ["x"])))))
        @test ev == ["u"]
        @test R.initial_state_values(Dict()) == (Dict{String, Float64}(), String[])
    end

    @testset "helpers" begin
        @test R.find_key(["M.x", "M.y"], "x") == "M.x"
        @test R.find_key(["M.x", "N.x"], "x") === nothing
        @test R.find_key(["x"], "x") == "x"
        @test R.axis_label(Dict("variable" => "a", "label" => "A!"), Dict("a" => "m")) == "A!"
        @test R.axis_label(Dict("variable" => "a"), Dict("a" => "m")) == "a [m]"
        @test R.axis_label(Dict("variable" => "a"), Dict{String, String}()) == "a"
        @test R.axis_scale("a", ["a"], [:log]) === :log10
        @test R.axis_scale("q", ["a"], [:log]) === :identity
        @test count(==('\n'), R.wrap_title(repeat("word ", 100); width = 20, max_lines = 3)) == 2
    end

    mktempdir() do dir
        alg = write_fixture(dir, "square.esm", ALGEBRAIC)
        ode = write_fixture(dir, "decay.esm", DECAY)

        @testset "numbers come from the runner" begin
            file = R.load_path(ode)
            base = R.esm_problem(file, (0.0, 1.0))
            @test !isempty(base.u0)
            q = R.problem_for(base, file, (0.0, 1.0), Dict("k" => 2.0), Dict("x" => 3.0))
            sol = R.solve_problem(q, (0.0, 1.0))
            env = R.trajectory_env(q, sol, ["x", "z", "k"])
            @test length(env["t"]) == R.N_TIME_POINTS
            @test env["x"][end] ≈ 3.0 * exp(-2.0) rtol = 1e-6
            @test env["z"] ≈ 2 .* env["x"] rtol = 1e-10
            @test all(==(2.0), env["k"])
            # A swept name that is a state goes to u0.
            q2 = R.problem_for(base, file, (0.0, 1.0), Dict("x" => 5.0), Dict{String, Float64}())
            sol2 = R.solve_problem(q2, (0.0, 1.0))
            @test sol2.u[end][1] ≈ 5.0 * exp(-1.0) rtol = 1e-6

            afile = R.load_path(alg)
            abase = R.esm_problem(afile, (0.0, 1.0))
            @test isempty(abase.u0)
            aq = R.problem_for(abase, afile, (0.0, 1.0), Dict("a" => 3.0, "b" => 0.5), Dict{String, Float64}())
            @test R.read_value(aq, "y", nothing, 0.0) ≈ 4.5
            @test R.read_value(aq, "a", nothing, 0.0) == 3.0
        end

        @testset "shared build carries analysis values" begin
            nd = write_fixture(dir, "nodefault.esm", NO_DEFAULT)
            file = R.load_path(nd)
            comp = file.models["NoDefault"]
            @test_throws Exception R.esm_problem(file, (0.0, 1.0))   # c has no value
            p = R.build_overrides(comp.analyses[1])
            @test p == Dict("a" => 5.0, "c" => 1.0)
            base = R.BaseProblem(R.build_problem(file, (0.0, 1.0), p, Dict{String, Float64}()),
                p, Dict{String, Float64}(), R.component_defaults(comp))
            # The second analysis does not name `a`: it gets the default (1), not 5.
            q = R.problem_for(base, file, (0.0, 1.0), Dict("c" => 3.0), Dict{String, Float64}())
            @test R.read_value(q, "y", nothing, 0.0) ≈ 3.0
            q = R.problem_for(base, file, (0.0, 1.0), Dict("a" => 2.0, "c" => 3.0), Dict{String, Float64}())
            @test R.read_value(q, "y", nothing, 0.0) ≈ 6.0
            # A built value with no default that the analysis does not supply
            # forces a rebuild, which fails on its own terms.
            @test_throws Exception R.problem_for(base, file, (0.0, 1.0), Dict("a" => 2.0),
                Dict{String, Float64}())
            stats = R.RenderStats()
            redirect_stdout(devnull) do
                R.render_file(nd, stats)
            end
            @test stats.plots_rendered == 2
            @test stats.plots_skipped == 0
        end

        @testset "end to end" begin
            redirect_stdout(devnull) do
                @test R.main(["--files", alg, ode]) == 0
            end
            pdir = joinpath(dir, "square.plots")
            @test isfile(joinpath(pdir, "line_a-y_vs_a.png"))
            @test isfile(joinpath(pdir, "line_a-y_vs_a_pts.png"))
            @test isfile(joinpath(pdir, "heat-y_heat.png"))
            @test isfile(joinpath(pdir, "line_a-two_series.png"))
            @test !isfile(joinpath(pdir, "line_a-snap.png"))        # unsupported type
            @test !isfile(joinpath(pdir, "line_a-missing.png"))     # unbound variable
            @test !isfile(joinpath(pdir, "nothing_to_do-p.png"))    # nothing to evaluate
            ddir = joinpath(dir, "decay.plots")
            for f in ("single-x_t", "single-z_t", "k_sweep-family", "k_sweep-final")
                @test isfile(joinpath(ddir, f * ".png"))
            end
            @test !isfile(joinpath(ddir, "two_d-h.png"))            # 2-D sweep of an ODE

            stats = R.RenderStats()
            redirect_stdout(devnull) do
                R.render_file(alg, stats)
                R.render_file(ode, stats)
            end
            @test stats.plots_rendered == 8
            @test stats.plots_skipped == 4
        end

        @testset "CLI errors" begin
            redirect_stderr(devnull) do
                @test R.main(["--files", joinpath(dir, "absent.esm")]) == 2
                @test R.main(["--bogus"]) == 2
                @test R.main(["--files", alg, "--components-dir", dir]) == 2
            end
        end
    end
end
