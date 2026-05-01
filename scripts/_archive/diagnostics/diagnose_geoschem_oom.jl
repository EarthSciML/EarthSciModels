#!/usr/bin/env julia
# scripts/_archive/diagnostics/diagnose_geoschem_oom.jl  (mdl-i5j)
#
# ARCHIVED — kept for git-log archeology only (see scripts/_archive/README.md).
# Do not invoke from CI, runtime, or test runners. mdl-i5j is closed; the
# diagnostic value here is the phase breakdown documented below.
#
# Localize the memory peak of compiling
# components/gaschem/geoschem_fullchem.esm (275 species x 819 reactions) by
# instrumenting the canonical pipeline with phase-wise Sys.maxrss() +
# time_ns() markers. Hard-aborts above an 8 GB safety budget so the host
# does not OOM. DIAGNOSIS ONLY -- the script does not solve the ODE, run
# any inline tests, or touch any other .esm file.
#
# Pipeline phases instrumented (all via the canonical pathway):
#   1. deps_loaded         -- using ModelingToolkit, Catalyst, EarthSciSerialization
#   2. esm_loaded          -- EarthSciSerialization.load(geoschem_fullchem.esm)
#   3a. catalyst_rs_built  -- Catalyst.ReactionSystem(rs; name=...)
#   3b. mtk_complete       -- ModelingToolkit.complete(catalyst_rs)
#   4. odeproblem_built    -- ModelingToolkit.ODEProblem(simp, merged, tspan;
#                              combinatoric_ratelaws=false)
#
# Invocation (uses the @esm-test-env env, which has MTK + Catalyst + ESS):
#   julia --threads=1,1 --check-bounds=no --project=@esm-test-env \
#       scripts/_archive/diagnostics/diagnose_geoschem_oom.jl
#
# Exit codes:
#   0  pipeline ran end-to-end
#   2  Sys.maxrss() exceeded MAX_RSS_BYTES; partial phase output is the answer

# Capture process-baseline RSS + clock BEFORE loading anything else so the
# first phase delta reflects real cost of `using ModelingToolkit ...`.
const _BASELINE_RSS = Sys.maxrss()
const _BASELINE_NS = time_ns()

using Printf

const MAX_RSS_BYTES = 8_000_000_000

const ESM_PATH = normpath(joinpath(@__DIR__, "..", "components", "gaschem",
                                   "geoschem_fullchem.esm"))

mutable struct PhaseTracker
    last_rss::Int
    last_time_ns::UInt64
end
const PT = PhaseTracker(_BASELINE_RSS, _BASELINE_NS)

function phase!(name::AbstractString)
    rss = Sys.maxrss()
    now = time_ns()
    delta_b = Int(rss) - PT.last_rss
    dt = (now - PT.last_time_ns) / 1e9
    rss_mb = rss / 1024 / 1024
    delta_mb = delta_b / 1024 / 1024
    @printf("PHASE %-22s rss=%6.0f MB   delta=%+7.0f MB   t=%6.2f s\n",
            name, rss_mb, delta_mb, dt)
    flush(stdout)
    PT.last_rss = Int(rss)
    PT.last_time_ns = now
    if rss > MAX_RSS_BYTES
        @printf("ABORT: peak RSS %.0f MB exceeded %.0f MB budget after phase '%s'\n",
                rss_mb, MAX_RSS_BYTES / 1024 / 1024, name)
        flush(stdout)
        exit(2)
    end
end

# ----- 1. deps_loaded ------------------------------------------------------
using ModelingToolkit
using Catalyst
using EarthSciSerialization
phase!("deps_loaded")

# ----- 2. esm_loaded -------------------------------------------------------
esm_file = EarthSciSerialization.load(ESM_PATH)
phase!("esm_loaded")

const RS_NAME = "GEOSChemGasPhase"
rs = esm_file.reaction_systems[RS_NAME]
sys_name = Symbol(RS_NAME)

# ----- 3a. catalyst_rs_built ----------------------------------------------
catalyst_rs = Catalyst.ReactionSystem(rs; name=sys_name)
phase!("catalyst_rs_built")

# ----- 3b. mtk_complete ----------------------------------------------------
# Mirrors src/run_tests.jl::_compile_reaction_system.
simp = ModelingToolkit.complete(catalyst_rs)
phase!("mtk_complete")

# Resolve a species/parameter handle on the compiled system the same way
# src/run_tests.jl::_resolve_handle does. Returns nothing if not found
# (diagnostic-tolerant; we just skip rather than abort).
function resolve_handle(simp, sys_name::Symbol, var_spec::AbstractString)
    sanitized = replace(String(var_spec), "." => "_")
    qualified = Symbol(String(sys_name) * "_" * sanitized)
    if hasproperty(simp, qualified)
        return getproperty(simp, qualified)
    end
    bare = Symbol(sanitized)
    if hasproperty(simp, bare)
        return getproperty(simp, bare)
    end
    return nothing
end

# Seed u0 / p maps from ESM defaults (the Catalyst extension does not
# propagate sp.default through @species metadata), then overlay the
# first inline test's explicit overrides -- mirrors run_tests.jl.
defaults_u0 = Dict{Any,Float64}()
defaults_p  = Dict{Any,Float64}()
for sp in rs.species
    sp.default === nothing && continue
    h = resolve_handle(simp, sys_name, sp.name); h === nothing && continue
    defaults_u0[h] = Float64(sp.default)
end
for pr in rs.parameters
    pr.default === nothing && continue
    h = resolve_handle(simp, sys_name, pr.name); h === nothing && continue
    defaults_p[h] = Float64(pr.default)
end

isempty(rs.tests) && error("geoschem_fullchem.esm has no inline tests; bead expected at least one for ODEProblem build.")
t = first(rs.tests)
u0_map = copy(defaults_u0)
for (spec, val) in t.initial_conditions
    h = resolve_handle(simp, sys_name, spec); h === nothing && continue
    u0_map[h] = Float64(val)
end
p_map = copy(defaults_p)
for (spec, val) in t.parameter_overrides
    h = resolve_handle(simp, sys_name, spec); h === nothing && continue
    p_map[h] = Float64(val)
end
tspan = (t.time_span.start, t.time_span.stop)
merged = isempty(p_map) ? u0_map : Base.merge(u0_map, p_map)

# ----- 4. odeproblem_built -------------------------------------------------
# combinatoric_ratelaws=false matches the inline-test runner's call shape.
prob = ModelingToolkit.ODEProblem(simp, merged, tspan; combinatoric_ratelaws=false)
phase!("odeproblem_built")

@printf("\nDONE: final peak RSS %.0f MB across %d phases (test='%s')\n",
        Sys.maxrss() / 1024 / 1024, 5, t.id)
