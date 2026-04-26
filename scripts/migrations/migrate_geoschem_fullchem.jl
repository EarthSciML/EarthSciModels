using Pkg
Pkg.activate("scripts/migrations")
using GasChem
using EarthSciSerialization
using Catalyst
using ModelingToolkit
const MT = ModelingToolkit
using Symbolics
using JSON3
using Serialization

const RS_CACHE = ""

println("[1/7] Loading or building GEOSChemGasPhase ReactionSystem...")
flush(stdout)
local_rs = nothing
if isfile(RS_CACHE)
    println("  loading from cache $RS_CACHE")
    flush(stdout)
    try
        local_rs = deserialize(RS_CACHE)
        println("  loaded.")
    catch e
        println("  cache load failed: $e — rebuilding")
        local_rs = nothing
    end
end
if local_rs === nothing
    @time local_rs = GasChem.GEOSChemGasPhase(; rxn_sys=true)
    try
        serialize(RS_CACHE, local_rs)
        println("  cached to $RS_CACHE")
    catch e
        println("  cache save failed: $e")
    end
end
rs = local_rs
println("  reactions=$(length(Catalyst.reactions(rs))) species=$(length(Catalyst.species(rs))) params=$(length(Catalyst.parameters(rs))) subsys=$(length(MT.get_systems(rs)))")
flush(stdout)

println("[2/7] Building substitution map from sub-system equations...")
flush(stdout)
all_eqs = MT.equations(rs)
println("  total equations: $(length(all_eqs))")
sub_eqs = filter(e -> e isa ModelingToolkit.Equation, all_eqs)
println("  algebraic/observed (Equation type): $(length(sub_eqs))")
sub_map = Dict()
for eq in sub_eqs
    sub_map[eq.lhs] = eq.rhs
end
println("  sub_map size: $(length(sub_map))")
flush(stdout)

println("[3/7] Building numeric-constant substitution map (namespaced params)...")
flush(stdout)
const_map = Dict()
top_params = []
for p in Catalyst.parameters(rs)
    pname = string(Symbolics.getname(Symbolics.unwrap(p)))
    if occursin('₊', pname)
        try
            d = Symbolics.getdefaultval(p)
            if d isa Number
                const_map[p] = d
            end
        catch
        end
    else
        push!(top_params, p)
    end
end
println("  top-level params: $(length(top_params))")
println("  namespaced numeric consts: $(length(const_map))")
flush(stdout)

all_subs = Dict(); for (kk,vv) in const_map; all_subs[kk] = vv; end; for (kk,vv) in sub_map; all_subs[kk] = vv; end
println("  combined substitution map: $(length(all_subs))")
flush(stdout)

println("[4/7] Substituting and rebuilding reactions...")
flush(stdout)
new_rxns = Catalyst.Reaction[]
unresolved_count = 0
unresolved_examples = String[]
for (idx, rxn) in enumerate(Catalyst.reactions(rs))
    rate = rxn.rate
    for round in 1:30
        new_rate = Symbolics.substitute(rate, all_subs)
        if isequal(new_rate, rate)
            break
        end
        rate = new_rate
    end
    rs_str = string(rate)
    if occursin('₊', rs_str)
        unresolved_count += 1
        if length(unresolved_examples) < 5
            push!(unresolved_examples, "rxn[$idx]: $(first(rs_str, 250))")
        end
    end
    new_rxn = Catalyst.Reaction(rate, rxn.substrates, rxn.products,
                                 rxn.substoich, rxn.prodstoich;
                                 only_use_rate=rxn.only_use_rate,
                                 metadata=rxn.metadata)
    push!(new_rxns, new_rxn)
end
println("  rebuilt $(length(new_rxns)) reactions")
println("  unresolved (still has ₊): $unresolved_count")
for ex in unresolved_examples
    println("    $ex")
end
flush(stdout)

println("[5/7] Building flat ReactionSystem with substituted rates and TOP-level params only...")
flush(stdout)
flat_rs = Catalyst.ReactionSystem(new_rxns, MT.get_iv(rs);
    name=:GEOSChemGasPhase,
    combinatoric_ratelaws=false)
println("  flat: rxns=$(length(Catalyst.reactions(flat_rs))) species=$(length(Catalyst.species(flat_rs))) params=$(length(Catalyst.parameters(flat_rs)))")
flush(stdout)

println("[6/7] Calling mtk2esm on flat_rs...")
flush(stdout)
result = EarthSciSerialization.mtk2esm(flat_rs; metadata=(;
    name="GEOSChemGasPhase",
    description="GEOS-Chem fullchem gas-phase mechanism (~819 reactions, ~272 species). Migrated from GasChem.jl GEOSChemGasPhase via mtk2esm with sub-system rate-law inlining.",
    version="0.1.0",
    source_ref="GasChem.jl src/geoschem_fullchem.jl",
    authors=["EarthSciML authors and contributors"],
))
println("  result keys: ", collect(keys(result)))
flush(stdout)

println("[7/7] Inspecting and writing output...")
flush(stdout)
suspect = 0
for (sn, rsd) in result["reaction_systems"]
    println("  RS: $sn  reactions=$(length(rsd["reactions"]))  species=$(length(rsd["species"]))  params=$(length(rsd["parameters"]))")
    flush(stdout)
    for (i, r) in enumerate(rsd["reactions"])
        rate_str = JSON3.write(r["rate"])
        if occursin('₊', rate_str)
            suspect += 1
        end
    end
end
println("  suspect rates with namespaced refs: $suspect")
flush(stdout)

out_path = "/tmp/geoschem_fullchem.esm"
open(out_path, "w") do io
    JSON3.pretty(io, result)
end
println("  wrote $out_path  size=$(stat(out_path).size) bytes")
flush(stdout)
