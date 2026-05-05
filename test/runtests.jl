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
        # Walk `components/` (all per-science-domain subdirs). An empty tree
        # is OK (Phase 0/1/2 — early migration). Once .esm files land, this
        # gate makes sure they all pass on every push.
        # CI sets ESM_TESTS_JUNIT_XML to collect a junit artifact in the same
        # pass — avoids a second `julia --project=.` invocation which can't
        # see MTK (it's a test-only dep).
        # ESM_TESTS_SKIP_PATTERNS is a comma-separated list of substrings;
        # matching .esm files are skipped from the live-repo walk. The
        # canonical Python inline-test gate (mdl-w1j) is the gate of record
        # for files skipped here. Used in CI to skip files whose Julia/MTK
        # build OOMs the 16 GB GitHub runner (mdl-lvu — geoschem_fullchem.esm
        # peaks at ~13 GB on a single MTK pass).
        junit_xml = get(ENV, "ESM_TESTS_JUNIT_XML", nothing)
        skip_patterns = String.(filter(!isempty,
            strip.(split(get(ENV, "ESM_TESTS_SKIP_PATTERNS", ""), ','))))
        results, exit_code = run_esm_tests(;
            junit_xml=junit_xml, skip_patterns=skip_patterns)
        if !isempty(results)
            failures = filter(r -> r.status != EarthSciModels.PASS, results)
            for f in failures
                println(stderr, "FAIL ", f.file, " :: ", f.container_name,
                        "/", f.test_id, " — ", f.message)
            end
            @test exit_code == 0
        else
            @info "No committed .esm files yet — runner exercised only against fixtures."
        end
    end
end
