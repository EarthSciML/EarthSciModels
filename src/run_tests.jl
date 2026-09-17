"""
    run_tests.jl

Discovery + inline-test runner for `.esm` files in this repo.

Each `Model` and `ReactionSystem` may carry a `tests` block (ESM spec §6.6) of
scalar `(variable, time, expected, [tolerance])` assertions. This module walks
`components/` (organized by science domain), parses every `.esm` file via
`EarthSciAST.load_path`, simulates each Test on the resulting MTK system,
samples each Assertion via the solution interpolant, and compares to the
declared expected value with the tolerance resolved per spec §6.6.4 (assertion
> test > model > default `rel=1e-6`).

The runner requires `ModelingToolkit`, `OrdinaryDiffEqTsit5` /
`OrdinaryDiffEqRosenbrock`, and (for `ReactionSystem` tests) `Catalyst` to be
loaded at the call site so the EarthSciAST MTK / Catalyst extensions
are active.

Public surface:
- `discover_esm_files(roots)` — recursive `.esm` walk over directories and/or
  explicit `.esm` files
- `shard_esm_files(files; shard="i/n")` — select shard `i` of `n` (defaults to
  the `ESM_TESTS_SHARD` env var), so the walk can be split across CI jobs
- `run_esm_tests(roots; junit_xml=nothing, verbose=true)` — returns
  `(results, exit_code)` where `exit_code == 0` iff every assertion passed
- `write_junit_xml(results, path)` — emit a junit-compatible report
"""

# Sweep roots, kept in parity with the Python gate's DEFAULT_ROOTS in
# `tools/run_esm_inline_tests.py`. `components/` holds the per-science-domain
# corpus; `lib/` and `registered_functions/` hold the shared leaves the
# components `ref`-include. The two runners walking different corpora is how a
# cross-runner divergence hides, so they walk the same three.
const DEFAULT_ROOTS = ["components", "lib", "registered_functions"]

@enum AssertionStatus PASS FAIL ERROR SKIP

"""
    AssertionResult

Outcome of one `(file, container, test, assertion_idx)` evaluation.
`message` carries the diff or error text for non-`PASS` results.
"""
struct AssertionResult
    file::String
    container_kind::Symbol   # :model or :reaction_system
    container_name::String
    test_id::String
    assertion_idx::Int
    variable::String
    time::Float64
    expected::Float64
    actual::Union{Float64,Nothing}
    status::AssertionStatus
    message::String
    duration_s::Float64
end

# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------

# Resolve exclude patterns: either an explicit kwarg vector, or the
# ESM_TESTS_EXCLUDE env var (";" or ":" separated). Patterns are matched as
# substrings against the absolute discovered path AND the path relative to
# `esm_root()`, so users can write either "components/gaschem/geoschem_fullchem.esm"
# or just "geoschem_fullchem.esm".
function _resolve_exclude(exclude::Union{Nothing,AbstractVector{<:AbstractString}})
    if exclude !== nothing
        return collect(String, exclude)
    end
    raw = get(ENV, "ESM_TESTS_EXCLUDE", "")
    isempty(raw) && return String[]
    parts = split(raw, r"[;:]"; keepempty=false)
    return String[String(strip(p)) for p in parts if !isempty(strip(p))]
end

function _is_excluded(path::AbstractString, base::AbstractString,
                     patterns::Vector{String})
    isempty(patterns) && return false
    rel = startswith(path, base) ? relpath(path, base) : path
    for pat in patterns
        (occursin(pat, path) || occursin(pat, rel)) && return true
    end
    return false
end

"""
    discover_esm_files(roots; exclude=nothing) -> Vector{String}

Resolve `roots` (each relative to `esm_root()` when not absolute) to a
deterministic, sorted, de-duplicated list of `*.esm` paths. A root that names a
directory is walked recursively; a root that names a `.esm` file is taken as
itself, so a caller can hand the runner an explicit file list — the same
"files and/or directories" surface the Rust CLI's `esm test PATH...` and the
Python gate's `--files` offer. Missing roots are skipped silently — empty
top-level dirs are normal in the migration window.

`exclude` (or the `ESM_TESTS_EXCLUDE` env var, ";"- or ":"-separated) is a list
of substring patterns; any discovered file whose absolute or repo-relative
path contains a pattern is dropped. This is the supported way to skip the
OOM-prone full-chemistry inline test on memory-constrained CI runners
(see bead mdl-lvu).
"""
function discover_esm_files(roots::AbstractVector{<:AbstractString};
                            exclude::Union{Nothing,AbstractVector{<:AbstractString}}=nothing)
    base = esm_root()
    patterns = _resolve_exclude(exclude)
    found = String[]
    for r in roots
        path = isabspath(r) ? r : joinpath(base, r)
        if isfile(path)
            endswith(path, ".esm") || continue
            _is_excluded(path, base, patterns) && continue
            push!(found, path)
            continue
        end
        isdir(path) || continue
        for (root, _dirs, files) in walkdir(path)
            for f in files
                endswith(f, ".esm") || continue
                full = joinpath(root, f)
                _is_excluded(full, base, patterns) && continue
                push!(found, full)
            end
        end
    end
    sort!(found)
    unique!(found)
    return found
end

"""
    shard_esm_files(files; shard=nothing) -> Vector{String}

Select one shard of `files`. `shard` is an `"i/n"` string (1-based `i` of `n`
shards) and defaults to the `ESM_TESTS_SHARD` env var; when neither is set,
`files` is returned unchanged.

Selection is by **stride** (`files[i:n:end]`), not by contiguous block: the
sorted corpus is grouped by science domain, and per-file cost is dominated by
the MTK build of whichever domain a file belongs to, so contiguous blocks would
hand one shard every large chemistry mechanism and another only the cheap
leaves. Striding interleaves the domains and keeps shard wall-times close.

This exists because the Julia walk builds every system IN-PROCESS, so its cost
scales linearly with the corpus — measured at ~4 s/file, which puts the whole
walk near 25 minutes in one process and growing. Sharding is what lets the walk
back into CI (esm-g97l, esm-m0r2 removed it) without either raising the per-job
budget or dropping coverage.
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

discover_esm_files(; kwargs...) = discover_esm_files(DEFAULT_ROOTS; kwargs...)

# ---------------------------------------------------------------------------
# Tolerance resolution (spec §6.6.4)
# ---------------------------------------------------------------------------


# Returns (rtol, atol) — the most-specific declared tolerance wins.

# ---------------------------------------------------------------------------
# Symbol lookup on a compiled MTK system
# ---------------------------------------------------------------------------

# Variable names in flattened ESM systems are dotted ("Sub.x"); the MTK
# extension's `_san` rewrites dots to underscores when constructing symbolic
# names. After mtkcompile, `getproperty(simp, Symbol(name))` returns the
# symbolic handle for either form, prefixed by the wrapper system's name.

# Lazy module lookup so this file can `include` without a hard dep on MTK
# being loaded at module-init time. Mirrors the pattern used by `_to_system`
# in EarthSciModels.jl.


# Per-file stiff-solver override (esm-4sxf). .esm basenames listed here are
# integrated with the stiff Rosenbrock23 solver instead of the default
# non-stiff Tsit5. Mirrors SOLVER_METHOD_OVERRIDE_FILENAMES in
# tools/run_esm_inline_tests.py — see that file and the pollu.esm reference
# notes for the rationale: the POLLU stiff-ODE benchmark (rate constants
# spanning ~8e-7 to ~7e9 1/s) cannot be integrated by an explicit non-stiff
# method, and Rosenbrock23 is the solver the upstream GasChem.jl reference
# values were generated with.
const STIFF_SOLVER_OVERRIDE_FILENAMES = Set(["pollu.esm"])

# Pick a solver: prefer Tsit5 (non-stiff, fast); fall back to Rosenbrock23.
# `.esm` files in `STIFF_SOLVER_OVERRIDE_FILENAMES` force Rosenbrock23.

# ---------------------------------------------------------------------------
# Per-container test execution
# ---------------------------------------------------------------------------





# ---------------------------------------------------------------------------
# Per-file driver
# ---------------------------------------------------------------------------

function run_file_tests!(results::Vector{AssertionResult}, path::AbstractString)
    upstream = EarthSciAST.AssertionResult[]
    EarthSciAST.run_file_tests!(upstream, String(path);
                                stiff_files=STIFF_SOLVER_OVERRIDE_FILENAMES)
    for r in upstream
        push!(results, AssertionResult(
            r.file, r.container_kind, r.container_name, r.test_id,
            r.assertion_idx, r.variable, r.time, r.expected, r.actual,
            _status_from_upstream(r.status), r.message, r.duration_s))
    end
    return results
end

"""Map the upstream `AssertionStatus` onto this package's own enum. The two are
declared identically; the conversion goes through the symbol so that a new
status added upstream fails loudly here rather than silently mapping to PASS."""
function _status_from_upstream(status)::AssertionStatus
    sym = Symbol(status)
    sym === :PASS && return PASS
    sym === :FAIL && return FAIL
    sym === :ERROR && return ERROR
    sym === :SKIP && return SKIP
    throw(ArgumentError("unknown upstream AssertionStatus: $(status)"))
end

"""
    run_esm_tests(roots=DEFAULT_ROOTS; junit_xml=nothing, verbose=true,
                  exclude=nothing, io::IO=stdout) -> (results, exit_code)

Walk each directory in `roots` (default: `components/`, which holds all
per-science-domain subdirs), run every inline test in every `.esm` file,
and return `(results::Vector{AssertionResult}, exit_code::Int)` where
`exit_code == 0` iff every assertion passed.

Prints a per-file summary table to `io` when `verbose=true`. When
`junit_xml` is a path, emits a junit-compatible XML report there.

`exclude` (or the `ESM_TESTS_EXCLUDE` env var) drops any `.esm` file whose
path contains one of the listed substrings. See `discover_esm_files`.
"""
function run_esm_tests(roots::AbstractVector{<:AbstractString}=DEFAULT_ROOTS;
                       junit_xml::Union{AbstractString,Nothing}=nothing,
                       verbose::Bool=true,
                       exclude::Union{Nothing,AbstractVector{<:AbstractString}}=nothing,
                       io::IO=stdout)
    files = discover_esm_files(roots; exclude=exclude)
    results = AssertionResult[]
    if isempty(files)
        verbose && println(io, "No .esm files discovered under: ",
                            join(roots, ", "))
    else
        for f in files
            run_file_tests!(results, f)
        end
    end

    verbose && _print_summary(io, files, results)
    junit_xml !== nothing && write_junit_xml(results, String(junit_xml))

    n_fail = count(r -> r.status == FAIL || r.status == ERROR, results)
    exit_code = n_fail == 0 ? 0 : 1
    return results, exit_code
end

run_esm_tests(roots::AbstractString...; kwargs...) =
    run_esm_tests(collect(String, roots); kwargs...)

function _print_summary(io::IO, files::Vector{String},
                        results::Vector{AssertionResult})
    base = esm_root()
    rel(p) = startswith(p, base) ? relpath(p, base) : p

    println(io)
    println(io, "================ ESM inline-test summary ================")
    println(io, "Files discovered: ", length(files))
    println(io, "Assertions:       ", length(results))

    by_file = Dict{String,Vector{AssertionResult}}()
    for r in results
        push!(get!(by_file, r.file, AssertionResult[]), r)
    end

    if isempty(results)
        println(io, "(no inline tests found)")
        println(io, "=========================================================")
        return
    end

    namepad = max(20, maximum(length(rel(p)) for p in keys(by_file); init=20))
    @printf(io, "  %-*s  %5s  %5s  %5s\n", namepad, "file", "pass", "fail", "err")
    println(io, "  ", repeat("-", namepad + 25))
    for f in sort!(collect(keys(by_file)))
        rows = by_file[f]
        np = count(r -> r.status == PASS, rows)
        nf = count(r -> r.status == FAIL, rows)
        ne = count(r -> r.status == ERROR, rows)
        @printf(io, "  %-*s  %5d  %5d  %5d\n", namepad, rel(f), np, nf, ne)
    end
    println(io, "  ", repeat("-", namepad + 25))

    total_pass = count(r -> r.status == PASS, results)
    total_fail = count(r -> r.status == FAIL, results)
    total_err = count(r -> r.status == ERROR, results)
    @printf(io, "  %-*s  %5d  %5d  %5d\n", namepad, "TOTAL", total_pass,
             total_fail, total_err)

    if total_fail + total_err > 0
        println(io)
        println(io, "Failures:")
        for r in results
            (r.status == PASS) && continue
            println(io, "  - ", rel(r.file), " :: ", r.container_name, "/",
                     r.test_id, "[", r.assertion_idx, "] (",
                     r.variable, "@t=", r.time, ") — ",
                     r.status == ERROR ? "ERROR" : "FAIL")
            isempty(r.message) || println(io, "      ", r.message)
        end
    end
    println(io, "=========================================================")
end

# ---------------------------------------------------------------------------
# JUnit XML emission
# ---------------------------------------------------------------------------

function _xml_escape(s::AbstractString)
    s = replace(String(s), '&' => "&amp;")
    s = replace(s, '<' => "&lt;")
    s = replace(s, '>' => "&gt;")
    s = replace(s, '"' => "&quot;")
    return s
end

"""
    write_junit_xml(results, path)

Emit a junit-compatible XML report covering every `AssertionResult`.

Each unique `(file, container, test_id)` becomes a `<testcase>`; one or more
failing assertions inside it produce `<failure>` / `<error>` children.
"""
function write_junit_xml(results::Vector{AssertionResult}, path::AbstractString)
    by_test = Dict{Tuple{String,String,String},Vector{AssertionResult}}()
    order = Tuple{String,String,String}[]
    for r in results
        key = (r.file, r.container_name, r.test_id)
        if !haskey(by_test, key)
            push!(order, key)
            by_test[key] = AssertionResult[]
        end
        push!(by_test[key], r)
    end

    n_tests = length(order)
    n_fail = sum(any(r -> r.status == FAIL, rs) for rs in values(by_test); init=0)
    n_err = sum(any(r -> r.status == ERROR, rs) for rs in values(by_test); init=0)

    open(path, "w") do io
        println(io, "<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
        println(io, "<testsuites tests=\"", n_tests,
                 "\" failures=\"", n_fail,
                 "\" errors=\"", n_err, "\">")
        println(io, "  <testsuite name=\"esm-inline-tests\" tests=\"",
                 n_tests, "\" failures=\"", n_fail,
                 "\" errors=\"", n_err, "\">")
        for key in order
            file, container, test_id = key
            rs = by_test[key]
            classname = _xml_escape(string(file, "::", container))
            casename = _xml_escape(test_id)
            duration = sum(r.duration_s for r in rs; init=0.0)
            println(io, "    <testcase classname=\"", classname,
                     "\" name=\"", casename,
                     "\" time=\"", duration, "\">")
            for r in rs
                if r.status == FAIL
                    println(io, "      <failure type=\"AssertionFailure\" ",
                             "message=\"", _xml_escape(r.message), "\">",
                             _xml_escape(string(r.variable, "@t=", r.time,
                                                 " expected=", r.expected,
                                                 " actual=", r.actual)),
                             "</failure>")
                elseif r.status == ERROR
                    println(io, "      <error type=\"RunnerError\" ",
                             "message=\"", _xml_escape(r.message), "\"/>")
                end
            end
            println(io, "    </testcase>")
        end
        println(io, "  </testsuite>")
        println(io, "</testsuites>")
    end
    return path
end
