using Test
using EarthSciModels
using ModelingToolkit

# Placeholder .esm fixture — replaced once real .esm files land. The fixture
# exists so the shim's parse → System → materialize path is exercised in CI
# before any real component is migrated.
const FIXTURE = joinpath(@__DIR__, "fixtures", "minimal_model.esm")

@testset "EarthSciModels shim" begin
    @testset "exports" begin
        @test isdefined(EarthSciModels, :load_esm)
        @test isdefined(EarthSciModels, :esm_root)
        @test isdefined(EarthSciModels, :esm_path)
    end

    @testset "esm_root / esm_path" begin
        root = EarthSciModels.esm_root()
        @test root !== nothing
        @test isdir(root)
        @test EarthSciModels.esm_path("models") == joinpath(root, "models")
    end

    @testset "load_esm on minimal fixture" begin
        sys = load_esm(FIXTURE)
        @test sys isa ModelingToolkit.System
    end

    @testset "load_esm errors on missing file" begin
        @test_throws Exception load_esm(joinpath(@__DIR__, "does_not_exist.esm"))
    end
end
