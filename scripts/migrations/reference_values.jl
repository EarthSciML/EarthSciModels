"""
    reference_values.jl

Compute ground-truth K_w, OH_minus, pH values for the WaterEquilibrium
migrated .esm, at a variety of (T, H_plus) parameter settings. Prints as
a JSON dict keyed by scenario id that the component's ESM tests reference.
"""

using ModelingToolkit
using ModelingToolkit: t_nounits as t
using OrdinaryDiffEqTsit5
using JSON3

include(joinpath(@__DIR__, "water_equilibrium.jl"))
simp = ModelingToolkit.mtkcompile(system)

function evaluate(Tval::Float64, Hval::Float64)
    prob = ModelingToolkit.ODEProblem(simp,
        Dict(T => Tval, H_plus => Hval), (0.0, 1.0))
    sol = solve(prob, Tsit5(); reltol = 1.0e-12, abstol = 1.0e-14)
    return (
        K_w = sol(0.5; idxs = K_w),
        OH_minus = sol(0.5; idxs = OH_minus),
        pH = sol(0.5; idxs = pH),
    )
end

scenarios = [
    # (id, T, H_plus)
    ("neutral_298K",         298.0, 1.0e-4),
    ("neutral_273K",         273.15, 1.0e-4),
    ("neutral_280K",         280.0, 1.0e-4),
    ("neutral_310K",         310.0, 1.0e-4),
    ("neutral_318K",         318.0, 1.0e-4),
    ("acidic_pH4_298K",      298.0, 1.0e-1),
    ("acidic_pH2_298K",      298.0, 1.0e1),
    ("basic_pH10_298K",      298.0, 1.0e-7),
    ("basic_pH9_298K",       298.0, 1.0e-6),
    ("cold_acidic_pH4_273K", 273.15, 1.0e-1),
    ("warm_basic_pH9_310K",  310.0, 1.0e-6),
]

results = Dict{String,Any}()
for (id, Tval, Hval) in scenarios
    vals = evaluate(Tval, Hval)
    results[id] = Dict(
        "T" => Tval,
        "H_plus" => Hval,
        "K_w" => vals.K_w,
        "OH_minus" => vals.OH_minus,
        "pH" => vals.pH,
    )
    println("$id (T=$Tval, H_plus=$Hval):")
    @show vals.K_w
    @show vals.OH_minus
    @show vals.pH
    println()
end

open(joinpath(@__DIR__, "reference_values.json"), "w") do io
    write(io, JSON3.write(results; indent = 2))
end
println("wrote reference_values.json")
