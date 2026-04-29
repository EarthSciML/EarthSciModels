"""
    probe_esm_compile.jl

Probe whether components/gaschem/geoschem_fullchem.esm can be loaded and
compiled (mtkcompile) within the bead's time/RAM budget.

This is the CI test path: run_esm_tests calls _compile_reaction_system which
invokes Catalyst.ReactionSystem(rs; name=...) followed by MTK.complete(...).
We mirror that here with explicit timing.

Outputs JSON to stdout with:
  load_seconds, compile_seconds, peak_rss_mib, n_reactions, n_species, n_params

Set environment variable PROBE_BUDGET_SECONDS to abort after that wall time
(default 3600 = 60 min, matching the bead's combined-budget cap).
"""

using Pkg
Pkg.activate("scripts/migrations")
using EarthSciSerialization
using ModelingToolkit
using Catalyst
using JSON3

const ESM_PATH = "components/gaschem/geoschem_fullchem.esm"

println("[probe] loading $(ESM_PATH) ...")
flush(stdout)
GC.gc()
t0 = time()
esm_file = EarthSciSerialization.load(ESM_PATH)
t_load = time() - t0
println("[probe] load done in $(round(t_load, digits=2)) s")
flush(stdout)

rs_dict = esm_file.reaction_systems
@assert rs_dict !== nothing
@assert haskey(rs_dict, "GEOSChemGasPhase")
rs = rs_dict["GEOSChemGasPhase"]

println("[probe] container has tests=$(length(rs.tests))")
flush(stdout)

# Mirror _compile_reaction_system:
println("[probe] building Catalyst ReactionSystem ...")
flush(stdout)
GC.gc()
t1 = time()
catalyst_rs = Catalyst.ReactionSystem(rs; name=:GEOSChemGasPhase)
t_build = time() - t1
println("[probe] Catalyst.ReactionSystem in $(round(t_build, digits=2)) s")
flush(stdout)

println("[probe] complete()ing system ...")
flush(stdout)
GC.gc()
t2 = time()
simp = ModelingToolkit.complete(catalyst_rs)
t_complete = time() - t2
println("[probe] complete() in $(round(t_complete, digits=2)) s")
flush(stdout)

# Read peak RSS
function peak_rss_mib()
    try
        for line in eachline("/proc/self/status")
            if startswith(line, "VmHWM:")
                kib = parse(Int, split(line)[2])
                return kib / 1024
            end
        end
    catch
    end
    return -1.0
end

result = Dict(
    "load_seconds" => t_load,
    "build_seconds" => t_build,
    "complete_seconds" => t_complete,
    "total_seconds" => t_load + t_build + t_complete,
    "peak_rss_mib" => peak_rss_mib(),
    "n_reactions" => length(Catalyst.reactions(catalyst_rs)),
    "n_species" => length(Catalyst.species(catalyst_rs)),
    "n_parameters" => length(Catalyst.parameters(catalyst_rs)),
)
println("[probe] RESULT: ", JSON3.write(result))
flush(stdout)
