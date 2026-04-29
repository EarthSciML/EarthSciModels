"""
    run_water_equilibrium.jl

One-shot migration driver for WaterEquilibrium → components/aerosol/aq_eq/water.esm.

Steps:
1. Load the standalone MTK module (water_equilibrium.jl).
2. Compile with mtkcompile and print unknowns / parameters / observed.
3. Simulate at two reference temperatures to produce ground-truth values.
4. Write a bare `mtk2esm` scaffold (structural) to a tempfile for inspection.
"""

using ModelingToolkit
using ModelingToolkit: t_nounits as t
using Symbolics
using EarthSciSerialization
using JSON3
using OrdinaryDiffEqTsit5
using Unitful

include(joinpath(@__DIR__, "water_equilibrium.jl"))

println("── Compiling WaterEquilibrium ──────────────────────────────")
simp = ModelingToolkit.mtkcompile(system)

println("unknowns:   ", ModelingToolkit.unknowns(simp))
println("parameters: ", ModelingToolkit.parameters(simp))
println("observed equations:")
for obs in ModelingToolkit.observed(simp)
    println("  ", obs)
end

println()
println("── mtk2esm scaffold ────────────────────────────────────────")
esm_dict = EarthSciSerialization.mtk2esm(
    system;
    metadata = (;
        name = "WaterEquilibrium",
        description = "Water autoionization equilibrium with van't Hoff temperature dependence (Seinfeld & Pandis Ch 7, Eq 7.10–7.13, Table 7.4). Parameterized as observed-only: T and H_plus are inputs; K_w, OH_minus, pH are computed.",
        tags = ["aerosol", "aqueous_equilibria", "observed-only"],
        source_ref = "Aerosol.jl@c8c640bb:src/aqueous_equilibria.jl:76",
    ),
)

out_path = joinpath(@__DIR__, "scaffold_water.esm")
open(out_path, "w") do io
    write(io, JSON3.write(esm_dict; indent = 2))
end
println("Scaffold written: ", out_path)

# Quick structural summary
esm_file = EarthSciSerialization.load(out_path)
model = esm_file.models["WaterEquilibrium"]
println("Variables declared: ", length(model.variables))
println("Equations: ", length(model.equations))

# Smoke-simulate the compiled system at two parameter settings
println()
println("── Reference evaluations ───────────────────────────────────")
for (Tval, Hval) in [(298.0, 1.0e-4), (280.0, 1.0e-4), (298.0, 1.0e-3)]
    prob = ModelingToolkit.ODEProblem(simp,
        Dict(T => Tval, H_plus => Hval), (0.0, 1.0))
    sol = solve(prob, Tsit5(); reltol = 1e-12, abstol = 1e-14)
    println("T=$Tval K, H_plus=$Hval mol/m³")
    println("  K_w      = ", sol(0.5; idxs = K_w))
    println("  OH_minus = ", sol(0.5; idxs = OH_minus))
    println("  pH       = ", sol(0.5; idxs = pH))
end

println()
println("── Done ────────────────────────────────────────────────────")
