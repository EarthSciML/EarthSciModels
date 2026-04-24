"""
    roundtrip_wrapper.jl

Thin wrapper around the ESS roundtrip CLI. Preloads `Printf` so the
script's top-level `@sprintf` call resolves (upstream places
`using Printf` below the function that uses the macro), then invokes
`main(ARGS)` so the validator runs as if called directly.

Usage (positional args mirror scripts/roundtrip.jl):

    julia --project=scripts/migrations \\
        scripts/migrations/roundtrip_wrapper.jl \\
        scripts/migrations/water_equilibrium.jl \\
        --tol rel=1e-6 --atol 1e-9 --tspan 0.0,1.0 --samples 10 \\
        --name WaterEquilibrium
"""

using Printf
const ESS_DIR = "/home/ctessum/esmlgt/EarthSciSerialization/refinery/rig/packages/EarthSciSerialization.jl"
include(joinpath(ESS_DIR, "scripts", "roundtrip.jl"))
main(ARGS)
