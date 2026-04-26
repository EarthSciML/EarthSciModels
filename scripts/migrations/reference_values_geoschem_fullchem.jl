"""
    reference_values_geoschem_fullchem.jl

Build GasChem.GEOSChemGasPhase upstream and integrate it from each of three
reference initial states defined in mdl-ode. Sample a small set of
key species at chosen times and emit JSON the .esm tests block can copy.

Strategy mirrors GasChem.jl's own test/geoschem_test.jl:
  sys  = GEOSChemGasPhase()                       # ODESystem path
  sys  = mtkcompile(sys)                          # structural_simplify
  prob = ODEProblem(sys, ic_overrides, tspan)
  sol  = solve(prob, Rosenbrock23())

Time/RAM budget (mdl-ode): 60 min wall, 32 GiB RAM combined for build +
mtkcompile. If exceeded, abort and let the caller record FINDING.

Output: scripts/migrations/reference_values_geoschem_fullchem.json
"""

using Pkg
Pkg.activate("scripts/migrations")
using GasChem
using ModelingToolkit
using OrdinaryDiffEqRosenbrock
using JSON3
using Serialization

println("[ref] building GEOSChemGasPhase ...")
flush(stdout)
GC.gc()
t0 = time()
sys_raw = GasChem.GEOSChemGasPhase()
println("[ref] build done in $(round(time() - t0, digits=2)) s")
flush(stdout)

println("[ref] mtkcompile ...")
flush(stdout)
GC.gc()
t1 = time()
sys = ModelingToolkit.mtkcompile(sys_raw)
println("[ref] mtkcompile done in $(round(time() - t1, digits=2)) s")
flush(stdout)

# Save the simplified system for the verify step
try
    serialize("/tmp/geoschem_fullchem_sys.jls", sys)
    println("[ref] cached simplified sys to /tmp/geoschem_fullchem_sys.jls")
catch e
    println("[ref] cache save failed: $e")
end

# Reference states (per mdl-ode bead — do not redesign):
#  (1) CLEAN TROPOSPHERE: T=285 K, P=101325 Pa
#  (2) POLLUTED URBAN:    T=298 K, P=101325 Pa
#  (3) UPPER TROPOSPHERE: T=220 K, P=20000 Pa
#
# The mechanism uses `num_density` (mol/m³ ≈ P/(R·T)) as the @parameter that
# carries pressure, not P directly — the migration script kept num_density as
# a top-level parameter but did not retain P. Compute num_density from (T,P)
# using the ideal-gas form upstream uses (see GasChem.jl/src/geoschem_fullchem.jl
# L1054: num_density = 2.7e19 / N_A * 1e6, i.e. mol/m³).
#
# Concentrations in ppb. j_11 = j_NO2 in the GEOS-Chem j-table (verified against
# /home/ctessum/.julia/dev/GasChem/src/geoschem_fullchem.jl L3014: `j_11, NO2 --> NO + O`).

const R_GAS_CONST = 8.314  # J/(mol·K)
nd(T::Real, P::Real) = P / (R_GAS_CONST * T)  # mol/m³

const STATES = [
    (
        id  = "clean_troposphere",
        T = 285.0, P = 101325.0,
        # NO=50 ppt=0.05, NO2=200 ppt=0.2, ISOP=200 ppt=0.2, O3=30 ppb
        ic = Dict("NO" => 0.05, "NO2" => 0.2, "ISOP" => 0.2, "O3" => 30.0,
                  "OH" => 4.0e-6, "HO2" => 4.0e-6),
        # j_NO2 ≈ 0.005 1/s
        j_no2 = 0.005,
        tspan  = (0.0, 600.0),
        sample_times = [60.0, 300.0, 600.0],
    ),
    (
        id  = "polluted_urban",
        T = 298.0, P = 101325.0,
        ic = Dict("NO" => 10.0, "NO2" => 20.0, "ISOP" => 2.0, "O3" => 70.0,
                  "OH" => 4.0e-6, "HO2" => 4.0e-6),
        j_no2 = 0.0149,
        tspan  = (0.0, 600.0),
        sample_times = [60.0, 300.0, 600.0],
    ),
    (
        id  = "upper_troposphere",
        T = 220.0, P = 20000.0,
        ic = Dict("NO" => 0.05, "NO2" => 0.1, "ISOP" => 0.0, "O3" => 100.0,
                  "OH" => 4.0e-6, "HO2" => 4.0e-6),
        j_no2 = 0.002,
        tspan  = (0.0, 600.0),
        sample_times = [60.0, 300.0, 600.0],
    ),
]

# Species we sample — chosen to span O3/NOx/HOx/VOC chemistry.
const SAMPLE_VARS = ["O3", "NO", "NO2", "OH", "HO2", "HNO3", "CO", "ISOP", "CH2O"]

function _resolve(simp, name::String)
    qual = Symbol("GEOSChemGasPhase_" * replace(name, "." => "_"))
    if hasproperty(simp, qual); return getproperty(simp, qual); end
    bare = Symbol(replace(name, "." => "_"))
    if hasproperty(simp, bare); return getproperty(simp, bare); end
    return nothing
end

results = Dict{String,Any}()
for state in STATES
    println("[ref] integrating $(state.id) ...")
    flush(stdout)
    nd_value = nd(state.T, state.P)
    # Build the parameter override map. `num_density` is the .esm's
    # pressure-equivalent parameter (mol/m³, see migration notes); upstream
    # has both P and num_density, but only num_density carries through to
    # the rate expressions after migration so we set it directly.
    params = Dict(
        "T" => state.T,
        "P" => state.P,
        "num_density" => nd_value,
        "j_11" => state.j_no2,
    )
    ic_pairs = Pair[]
    for (n, v) in state.ic
        h = _resolve(sys, n)
        h === nothing && continue
        push!(ic_pairs, h => Float64(v))
    end
    for (n, v) in params
        h = _resolve(sys, n)
        h === nothing && continue
        push!(ic_pairs, h => Float64(v))
    end
    prob = ModelingToolkit.ODEProblem(sys, ic_pairs, state.tspan)
    sol = ModelingToolkit.SciMLBase.solve(prob, Rosenbrock23();
                                          reltol=1e-10, abstol=1e-12)
    samples = Vector{Dict{String,Any}}()
    for var in SAMPLE_VARS
        h = _resolve(sys, var)
        h === nothing && continue
        for tt in state.sample_times
            try
                val = Float64(sol(tt; idxs=h))
                push!(samples, Dict(
                    "variable" => var,
                    "time" => tt,
                    "expected" => val,
                ))
            catch e
                println("[ref]   sample $var @ $tt failed: $e")
            end
        end
    end
    results[state.id] = Dict(
        "initial_conditions" => state.ic,
        # num_density is the pressure-carrying override on the .esm side;
        # we expose it (and j_11) explicitly so inject_tests_into_esm.py can
        # build the parameter_overrides block without re-deriving the value.
        "parameter_overrides" => Dict(
            "T" => state.T,
            "num_density" => nd_value,
            "j_11" => state.j_no2,
        ),
        "tspan_seconds" => [state.tspan[1], state.tspan[2]],
        "samples" => samples,
    )
end

open("scripts/migrations/reference_values_geoschem_fullchem.json", "w") do io
    JSON3.pretty(io, results)
end
println("[ref] wrote scripts/migrations/reference_values_geoschem_fullchem.json")
