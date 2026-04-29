"""
    verify_water_esm.jl

Exercises components/aerosol/aq_eq/water.esm locally:
1. Load the .esm and verify it parses.
2. Materialize the `WaterEquilibrium` MTK System.
3. Run the inline-test walker on the full `components/` tree.

Prints pass/fail and exits non-zero on any assertion failure.
"""

using ModelingToolkit
using Catalyst
using OrdinaryDiffEqTsit5
using OrdinaryDiffEqRosenbrock
using EarthSciSerialization
using EarthSciModels

const WATER_PATH = joinpath(@__DIR__, "..", "..", "components", "aerosol", "aq_eq", "water.esm")

println("── Loading water.esm ──────────────────────────────────────")
esm_file = EarthSciSerialization.load(WATER_PATH)
model = esm_file.models["WaterEquilibrium"]
println("variables: ", collect(keys(model.variables)))
println("equations: ", length(model.equations))
println("tests:     ", length(model.tests))

println()
println("── Materializing as MTK System ────────────────────────────")
sys = load_esm(WATER_PATH)
simp = ModelingToolkit.mtkcompile(sys)
println("simp unknowns:   ", ModelingToolkit.unknowns(simp))
println("simp parameters: ", ModelingToolkit.parameters(simp))

println()
println("── Running inline-test walker on components/ ──────────────")
results, exit_code = EarthSciModels.run_esm_tests(["components"]; verbose = true)

n_fail = count(r -> r.status != EarthSciModels.PASS, results)
println()
println("── Summary ────────────────────────────────────────────────")
println("total:  $(length(results))")
println("passed: $(count(r -> r.status == EarthSciModels.PASS, results))")
println("failed: $n_fail")
println("exit_code: $exit_code")

exit(exit_code)
