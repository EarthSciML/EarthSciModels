"""
    run_tests.jl

The Julia inline-test gate over this repo's `.esm` corpus: `EarthSciAST`'s
tree-walk runner, sharded for CI.

The run itself — discovery, `EarthSciAST.load_path`, the `esm_problem` build,
integration of each esm-spec §6.6 test, §6.6.4 tolerance resolution, the §6.6.3
pass predicate and the junit report — belongs to `EarthSciAST` and is not
restated here. This file adds the two things that are facts about this REPO
rather than about the ESM format: where its `.esm` files live, and that the
corpus does not fit one GitHub Actions job, so the walk is split across a
matrix.

The runner is `EarthSciAST.run_inline_tests` — the tree-walk pathway, the same
one the Python gate drives — NOT `EarthSciAST.run_esm_tests`, which lowers each
document to ModelingToolkit first. The two are not equivalent over this corpus:
the MTK lowering has no arm for a long tail of ops the corpus uses (`and`,
`or`, `floor`, `atan2`, `datetime.hour`, an unexpanded `apply_expression_template`
in a reaction rate), and every document reaching one of them errors at compile
time under that runner while the tree-walk runner integrates it. Loading a
document as an MTK `System` is still what `load_esm` is for, and it is covered
by this package's own tests; it is just not how the corpus gate runs.

Public surface:
- `shard_esm_files(files; shard="i/n")` — select shard `i` of `n` (defaults to
  the `ESM_TESTS_SHARD` env var)
- `run_esm_tests(roots; shard, junit_xml, …)` — run the inline tests of this
  repo's corpus (or of one shard of it)
- `discover_esm_files(roots)` — `EarthSciAST.discover_esm_files` rooted here
"""

# Sweep roots, kept in parity with the Python gate's DEFAULT_ROOTS in
# `tools/run_esm_inline_tests.py`. `components/` holds the per-science-domain
# corpus; `lib/` and `registered_functions/` hold the shared leaves the
# components `ref`-include. The two runners walking different corpora is how a
# cross-runner divergence hides, so they walk the same three.
const DEFAULT_ROOTS = ["components", "lib", "registered_functions"]

"""
    discover_esm_files(roots=DEFAULT_ROOTS; exclude=nothing) -> Vector{String}

[`EarthSciAST.discover_esm_files`](@ref) rooted at this repo: `roots` that are
not absolute resolve against [`esm_root`](@ref) rather than against the
toolkit's own package directory.

`exclude` (or the `ESM_TESTS_EXCLUDE` env var) is passed straight through.
"""
discover_esm_files(roots::AbstractVector{<:AbstractString}=DEFAULT_ROOTS;
                   exclude::Union{Nothing,AbstractVector{<:AbstractString}}=nothing) =
    EarthSciAST.discover_esm_files(roots; root=esm_root(), exclude=exclude)

"""
    shard_esm_files(files; shard=nothing) -> Vector{String}

Select one shard of `files`. `shard` is an `"i/n"` string (1-based `i` of `n`
shards) and defaults to the `ESM_TESTS_SHARD` env var; when neither is set,
`files` is returned unchanged.

Selection is by **stride** (`files[i:n:end]`), not by contiguous block: the
sorted corpus is grouped by science domain, and per-file cost is dominated by
whichever domain a file belongs to, so contiguous blocks would hand one shard
every large chemistry mechanism and another only the cheap leaves. Striding
interleaves the domains and keeps shard wall-times close.

The shards are a partition — every discovered `.esm` is walked by exactly one
of them — so splitting the walk across CI jobs costs no coverage.
"""
function shard_esm_files(files::AbstractVector{<:AbstractString};
                         shard::Union{Nothing,AbstractString}=nothing)
    spec = shard === nothing ? get(ENV, "ESM_TESTS_SHARD", "") : String(shard)
    spec = String(strip(spec))
    isempty(spec) && return collect(String, files)

    parts = split(spec, "/"; keepempty=false)
    length(parts) == 2 || throw(ArgumentError(
        "ESM_TESTS_SHARD must be \"i/n\" (1-based shard i of n); got \"$(spec)\"."))
    i = tryparse(Int, strip(parts[1]))
    n = tryparse(Int, strip(parts[2]))
    (i === nothing || n === nothing) && throw(ArgumentError(
        "ESM_TESTS_SHARD must be \"i/n\" with integer i and n; got \"$(spec)\"."))
    n >= 1 || throw(ArgumentError("ESM_TESTS_SHARD shard count must be >= 1; got $(n)."))
    1 <= i <= n || throw(ArgumentError(
        "ESM_TESTS_SHARD index $(i) is out of range for $(n) shard(s)."))

    return collect(String, files[i:n:end])
end

"""
    run_esm_tests(roots=DEFAULT_ROOTS; shard=nothing, exclude=nothing,
                  junit_xml=nothing, verbose=true, io=stdout, kwargs...)
        -> (results, exit_code)

Run every inline test of every `.esm` file under `roots` through
[`EarthSciAST.run_inline_tests`](@ref), and return
`(results::Vector{EarthSciAST.AssertionResult}, exit_code::Int)` where
`exit_code == 0` iff every assertion passed.

`kwargs` go straight to the toolkit runner. In particular `alg` is NOT passed
by default, which is deliberate: left unset, each document gets the algorithm
its own `solver.stiffness` declaration asks for (esm-spec §2.2), and a single
corpus-wide algorithm named here would override that for every document —
which a stiff member of the corpus does not survive.

Documents are run ONE AT A TIME, each passed as its own one-element VECTOR:
that selects the runner's batch semantics, where a document that fails to LOAD
contributes an ERROR row naming it instead of throwing and ending the walk on
the first unreadable file. Rows are attributed to their file by the runner, so
a single batch call would summarize identically; what the loop does NOT buy is
isolation from a throw raised past the loader — that still ends the walk, and
the per-file subprocess of the Python gate is what this side does not have.

`shard` is `nothing` by default rather than deferring to `ESM_TESTS_SHARD`: the
CI matrix sets that variable for the WHOLE job, so an ambient fallback would
also shard a run rooted at a fixture directory and silently find nothing there.
The live-repo walk names the shard it wants; every other call gets the whole of
what it asked for.
"""
function run_esm_tests(roots::AbstractVector{<:AbstractString}=DEFAULT_ROOTS;
                       shard::Union{Nothing,AbstractString}=nothing,
                       exclude::Union{Nothing,AbstractVector{<:AbstractString}}=nothing,
                       junit_xml::Union{AbstractString,Nothing}=nothing,
                       verbose::Bool=true,
                       io::IO=stdout,
                       kwargs...)
    files = discover_esm_files(roots; exclude=exclude)
    shard === nothing || (files = shard_esm_files(files; shard=shard))

    results = EarthSciAST.AssertionResult[]
    if isempty(files)
        verbose && println(io, "No .esm files discovered under: ", join(roots, ", "))
    else
        base = esm_root()
        verbose && println(io, "Walking ", length(files), " .esm file(s) ...")
        for (i, f) in enumerate(files)
            t0 = time()
            # A one-element VECTOR, not the path itself: that selects the
            # runner's batch semantics, where a document that fails to LOAD
            # contributes an ERROR row naming it instead of throwing and
            # ending the walk on its first unreadable file.
            rows = EarthSciAST.run_inline_tests([f]; kwargs...)
            append!(results, rows)
            # Printed per document, and FLUSHED, because the alternative is
            # what a 60-minute job cap taught: a shard killed mid-walk had
            # emitted nothing at all, so the log could not say which document
            # it was on, how far it had got, or whether it was stuck. A
            # summary that only exists at the end does not survive the run
            # being cut short — which is exactly when it is most wanted.
            if verbose
                bad = count(r -> r.status != EarthSciAST.PASS, rows)
                @printf(io, "  [%s] %4d/%d %s  (%d rows, %.1fs)\n",
                        bad == 0 ? "OK " : "FAIL", i, length(files),
                        startswith(f, base) ? relpath(f, base) : f,
                        length(rows), time() - t0)
                flush(io)
            end
        end
    end

    verbose && _print_summary(io, files, results)
    junit_xml === nothing || EarthSciAST.write_junit_xml(results, String(junit_xml))

    n_bad = count(r -> r.status != EarthSciAST.PASS, results)
    return results, n_bad == 0 ? 0 : 1
end

run_esm_tests(roots::AbstractString...; kwargs...) =
    run_esm_tests(collect(String, roots); kwargs...)

# Per-file pass/fail table plus the failure list. Deliberately the only
# reporting this file owns: the junit report is the toolkit's, and this is what
# a human reads in the CI log.
function _print_summary(io::IO, files::Vector{String},
                        results::Vector{EarthSciAST.AssertionResult})
    base = esm_root()
    rel(p) = isempty(p) ? "(unattributed)" :
             (startswith(p, base) ? relpath(p, base) : p)

    by_file = Dict{String,Vector{EarthSciAST.AssertionResult}}()
    for r in results
        push!(get!(by_file, r.file, EarthSciAST.AssertionResult[]), r)
    end

    println(io)
    println(io, "================ ESM inline-test summary ================")
    println(io, "Files discovered: ", length(files))
    println(io, "Assertions:       ", length(results))

    counts(rows) = (count(r -> r.status == EarthSciAST.PASS, rows),
                    count(r -> r.status == EarthSciAST.FAIL, rows),
                    count(r -> r.status == EarthSciAST.ERROR, rows))

    for f in sort!(collect(keys(by_file)))
        p, fa, e = counts(by_file[f])
        println(io, "  [", (fa + e == 0 ? "OK " : "FAIL"), "] ", rel(f),
                ": ", p, "P / ", fa, "F / ", e, "E")
    end

    p, fa, e = counts(results)
    println(io, "  TOTAL: ", p, "P / ", fa, "F / ", e, "E")

    if fa + e > 0
        println(io)
        println(io, "Failures / errors:")
        for r in results
            r.status == EarthSciAST.PASS && continue
            println(io, "  - [", r.status, "] ", rel(r.file), " :: ",
                    r.container_name, "/", r.test_id, "[", r.assertion_idx,
                    "] (", r.variable, "@t=", r.time, ") — ", r.message)
        end
    end
    println(io, "=========================================================")
end
