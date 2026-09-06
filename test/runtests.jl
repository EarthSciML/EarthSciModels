using Test
using EarthSciModels
using ModelingToolkit
using Catalyst
using OrdinaryDiffEqTsit5
using OrdinaryDiffEqNonlinearSolve

# Placeholder .esm fixture — replaced once real .esm files land. The fixture
# exists so the shim's parse → System → materialize path is exercised in CI
# before any real component is migrated.
const FIXTURE = joinpath(@__DIR__, "fixtures", "minimal_model.esm")

@testset "EarthSciModels shim" begin
    @testset "exports" begin
        @test isdefined(EarthSciModels, :load_esm)
        @test isdefined(EarthSciModels, :esm_root)
        @test isdefined(EarthSciModels, :esm_path)
        @test isdefined(EarthSciModels, :run_esm_tests)
        @test isdefined(EarthSciModels, :discover_esm_files)
        @test isdefined(EarthSciModels, :shard_esm_files)
    end

    @testset "esm_root / esm_path" begin
        root = EarthSciModels.esm_root()
        @test root !== nothing
        @test isdir(root)
        @test EarthSciModels.esm_path("components") == joinpath(root, "components")
    end

    @testset "load_esm on minimal fixture" begin
        sys = load_esm(FIXTURE)
        @test sys isa ModelingToolkit.System
    end

    @testset "load_esm errors on missing file" begin
        @test_throws Exception load_esm(joinpath(@__DIR__, "does_not_exist.esm"))
    end
end

@testset "Inline-test runner (mdl-08t)" begin
    inline_dir = joinpath(@__DIR__, "fixtures", "inline_tests")

    @testset "discover_esm_files" begin
        found = discover_esm_files([inline_dir])
        @test length(found) == 2
        @test all(endswith(f, ".esm") for f in found)
    end

    @testset "discover_esm_files honours exclude (mdl-lvu)" begin
        kw = discover_esm_files([inline_dir]; exclude=["failing_decay"])
        @test length(kw) == 1
        @test endswith(kw[1], "passing_decay.esm")

        prev = get(ENV, "ESM_TESTS_EXCLUDE", nothing)
        try
            ENV["ESM_TESTS_EXCLUDE"] = "failing_decay.esm"
            envf = discover_esm_files([inline_dir])
            @test length(envf) == 1
            @test endswith(envf[1], "passing_decay.esm")
        finally
            if prev === nothing
                delete!(ENV, "ESM_TESTS_EXCLUDE")
            else
                ENV["ESM_TESTS_EXCLUDE"] = prev
            end
        end
    end

    @testset "discover_esm_files accepts file paths, and de-duplicates" begin
        one = joinpath(inline_dir, "passing_decay.esm")
        @test discover_esm_files([one]) == [one]
        # A file named alongside the directory that already contains it is
        # listed once, not twice.
        @test discover_esm_files([inline_dir, one]) == discover_esm_files([inline_dir])
        # A non-.esm file is not a root.
        @test isempty(discover_esm_files([@__FILE__]))
    end

    @testset "shard_esm_files strides, and covers the corpus exactly once" begin
        files = ["a", "b", "c", "d", "e", "f", "g"]

        # This testset asserts what `shard_esm_files` does for a GIVEN spec, so
        # it has to own the env var the function falls back to. Under CI it does
        # not: the julia-inline-tests matrix sets ESM_TESTS_SHARD for the whole
        # job, and an ambient "1/40" silently turned the no-shard case below into
        # shard 1 of 40. Clear it for the duration and put it back after.
        prev = get(ENV, "ESM_TESTS_SHARD", nothing)
        delete!(ENV, "ESM_TESTS_SHARD")
        try
            @test shard_esm_files(files) == files                 # no shard → all
            @test shard_esm_files(files; shard="1/3") == ["a", "d", "g"]
            @test shard_esm_files(files; shard="2/3") == ["b", "e"]
            @test shard_esm_files(files; shard="3/3") == ["c", "f"]
            # Union of every shard is a partition of the input.
            union3 = vcat((shard_esm_files(files; shard="$i/3") for i in 1:3)...)
            @test sort(union3) == sort(files)
            @test length(union3) == length(files)
            # More shards than files: the tail shards are empty, not an error.
            @test shard_esm_files(["a"]; shard="2/4") == String[]

            # The env var is the fallback, and an explicit `shard=` overrides it.
            ENV["ESM_TESTS_SHARD"] = "2/3"
            @test shard_esm_files(files) == ["b", "e"]
            @test shard_esm_files(files; shard="1/3") == ["a", "d", "g"]
            ENV["ESM_TESTS_SHARD"] = ""
            @test shard_esm_files(files) == files
            delete!(ENV, "ESM_TESTS_SHARD")

            @test_throws ArgumentError shard_esm_files(files; shard="1")
            @test_throws ArgumentError shard_esm_files(files; shard="x/3")
            @test_throws ArgumentError shard_esm_files(files; shard="0/3")
            @test_throws ArgumentError shard_esm_files(files; shard="4/3")
        finally
            if prev === nothing
                delete!(ENV, "ESM_TESTS_SHARD")
            else
                ENV["ESM_TESTS_SHARD"] = prev
            end
        end
    end

    @testset "passing fixture → all PASS" begin
        passing = joinpath(inline_dir, "passing_decay.esm")
        results, exit_code = run_esm_tests([dirname(passing)]; verbose=false)
        # Both fixture files in the same dir; filter to just the passing one.
        passing_results = filter(r -> r.file == passing, results)
        @test !isempty(passing_results)
        @test all(r -> r.status == EarthSciModels.PASS, passing_results)
    end

    @testset "failing fixture → reports FAIL, exit_code != 0" begin
        failing = joinpath(inline_dir, "failing_decay.esm")
        results, exit_code = run_esm_tests([dirname(failing)]; verbose=false)
        failing_results = filter(r -> r.file == failing, results)
        @test !isempty(failing_results)
        @test any(r -> r.status == EarthSciModels.FAIL, failing_results)
        @test exit_code != 0
    end

    @testset "junit XML emission" begin
        mktempdir() do tmp
            xml_path = joinpath(tmp, "report.xml")
            results, _ = run_esm_tests([inline_dir];
                                        verbose=false, junit_xml=xml_path)
            @test isfile(xml_path)
            content = read(xml_path, String)
            @test occursin("<testsuites", content)
            @test occursin("FailingDecay", content)
            @test occursin("<failure", content)
        end
    end

    @testset "live repo: every committed .esm passes" begin
        # Walk the DEFAULT_ROOTS corpus (`components/` and its per-science-domain
        # subdirs, plus `lib/` and `registered_functions/`). An empty tree is OK
        # (Phase 0/1/2 — early migration). Once .esm files land, this gate makes
        # sure they all pass on every push.
        # CI sets ESM_TESTS_JUNIT_XML to collect a junit artifact in the same
        # pass — avoids a second `julia --project=.` invocation which can't
        # see MTK (it's a test-only dep).
        #
        # ESM_TESTS_SHARD="i/n" walks only shard i of n (see `shard_esm_files`).
        # This is how the walk fits CI: it builds every system IN-PROCESS at
        # ~a minute-plus per file, which scales linearly with component count
        # and blew past the 30-minute job budget once the migration burst pushed
        # the repo past ~25 components (esm-g97l, esm-m0r2). The
        # `julia-inline-tests` matrix in .github/workflows/test-esm.yml runs one
        # shard per job, and the shards partition the corpus, so the sweep is
        # whole. Unset (the local default) walks everything in one process.
        #
        # ESM_TESTS_SKIP_LIVE_REPO=1 still short-circuits the walk entirely, for
        # a fast shim-only `pkg test`.
        if get(ENV, "ESM_TESTS_SKIP_LIVE_REPO", "") in ("1", "true", "yes")
            @info "ESM_TESTS_SKIP_LIVE_REPO set — skipping the live-repo walk."
        else
            junit_xml = get(ENV, "ESM_TESTS_JUNIT_XML", nothing)
            shard = get(ENV, "ESM_TESTS_SHARD", "")
            discovered = discover_esm_files()
            files = shard_esm_files(discovered)
            isempty(shard) || @info "ESM_TESTS_SHARD=$(shard) — walking $(length(files)) of $(length(discovered)) discovered .esm file(s)."
            results, exit_code = run_esm_tests(files; junit_xml=junit_xml)
            if !isempty(results)
                failures = filter(r -> r.status != EarthSciModels.PASS, results)
                for f in failures
                    println(stderr, "FAIL ", f.file, " :: ", f.container_name,
                            "/", f.test_id, " — ", f.message)
                end
                @test exit_code == 0
            elseif isempty(files)
                @info "No .esm files in this shard — runner exercised only against fixtures."
            else
                @info "No inline tests in this shard's .esm files."
            end
        end
    end
end
