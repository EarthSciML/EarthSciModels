# Migration Guide — `mtk2esm` and the Round-Trip Validator

This guide is for polecats migrating an existing ModelingToolkit
(MTK) / Catalyst component into an `.esm` file under this repo. It covers:

1. Wiring `EarthSciSerialization.jl` (the `mtk2esm` provider) into your
   polecat's Julia environment.
2. Invoking `mtk2esm` to scaffold an `.esm` from an MTK `System` /
   `ReactionSystem`.
3. Running the round-trip validator (`scripts/roundtrip.jl` in the
   `EarthSciSerialization.jl` package) to confirm the migration preserves
   trajectories within tolerance.
4. Handling the `TODO_GAP` markers the scaffolder emits when it hits a
   schema gap.

The companion tool — `mtk2esm` and the round-trip CLI — was landed in
[`gt-dod2`](https://github.com/EarthSciML/EarthSciSerialization). This
guide pairs with that tool's reference docs, not replaces them.

---

## 1. Wire `EarthSciSerialization` into your env

`EarthSciSerialization.jl` is **not** in the Julia General registry. ESM's
`Project.toml` declares it as a dep, but `Pkg.instantiate` cannot resolve
it on its own. Run the setup script once per fresh worktree before any
other Julia work:

```bash
scripts/setup_polecat_env.sh
```

Resolution order (the script picks the first that works):

1. `$EARTHSCI_SERIALIZATION_PATH` — explicit override.
2. A Gas Town workspace checkout, in priority order:
   - `../../../../EarthSciSerialization/refinery/rig/packages/EarthSciSerialization.jl`
   - `../../../../EarthSciSerialization/mayor/rig/packages/EarthSciSerialization.jl`
3. Fallback: `Pkg.add(url="https://github.com/EarthSciML/EarthSciSerialization.git", rev="main", subdir="packages/EarthSciSerialization.jl")`
   (override the rev with `EARTHSCI_SERIALIZATION_REV=<sha>`). The `subdir` is
   required because the Julia package lives at `packages/EarthSciSerialization.jl/`
   in the upstream repo, not at repo root.

The script is idempotent — re-running it on an already-resolved env is a
no-op aside from `Pkg.instantiate`.

After it succeeds, this works:

```bash
julia --project=. -e 'using EarthSciSerialization; println(pathof(EarthSciSerialization))'
```

If you see a `pathof` printed, you're set. If you get
`ArgumentError: Package EarthSciSerialization not found`, the script
either didn't run or none of its resolution paths existed — re-run with
`EARTHSCI_SERIALIZATION_PATH` pointing at a valid checkout.

---

## 2. Scaffold an `.esm` from your MTK system

`mtk2esm` walks an MTK system and produces a schema-valid `Dict` shaped
like a full ESM file (top-level `models.<name>` or
`reaction_systems.<name>`).

```julia
using EarthSciSerialization
using ModelingToolkit            # required: loads the MTK extension
# using Catalyst                 # also load this if your system is a ReactionSystem

# `sys` is whatever your migration source produces — a System,
# ReactionSystem, ODESystem, NonlinearSystem, or PDESystem.
esm_dict = EarthSciSerialization.mtk2esm(sys; metadata=(;
    name        = "SuperFast",
    description = "Gas-phase chemistry — SuperFast subset",
    tags        = ["chemistry", "gas-phase"],
    source_ref  = "GasChem.jl/superfast.jl",
))

# Serialize to disk under the appropriate component dir:
open("components/gaschem/superfast.esm", "w") do io
    JSON3.pretty(io, esm_dict)
end
```

`mtk2esm` populates the IR-derived fields (`variables`, `equations`,
`continuous_events`, `discrete_events`). The `metadata` keyword is the
hand-curated overlay — `name`, `description`, `tags`, `source_ref`,
`authors`, `version`. `name` overrides `nameof(sys)`.

The Catalyst extension provides a `ReactionSystem` overload that emits
under `reaction_systems.<name>` instead of `models.<name>` (this is the
schema field, not a directory — both kinds of file live under
`components/<domain>/`).

### The `EarthSciModels` shim

Once an `.esm` exists, the consuming side is one line:

```julia
using EarthSciModels
using ModelingToolkit   # so the ESS MTK extension activates

sys = load_esm(esm_path("components", "gaschem", "superfast.esm"))
```

`load_esm` delegates to `EarthSciSerialization.load(...)` and asserts the
file contains exactly one model. For multi-component files, drop down
to `EarthSciSerialization.load(path)` and pick the entry yourself.

---

## 3. Run the round-trip validator

The validator confirms `mtk → mtk2esm → file → load → mtk` preserves
trajectories within tolerance. It lives in the `EarthSciSerialization.jl`
package at `scripts/roundtrip.jl`. Resolve the path via the env var the
setup script honors, or invoke it from the workspace checkout:

```bash
ESS_DIR=$(julia --project=. -e 'using EarthSciSerialization; print(dirname(dirname(pathof(EarthSciSerialization))))')

julia --project=. "$ESS_DIR/scripts/roundtrip.jl" \
    path/to/MyModel.jl \
    --tol rel=1e-6 \
    --atol 1e-9 \
    --tspan 0.0,10.0 \
    --samples 50 \
    --name MyModel
```

The CLI:

1. `include`s the MTK module file you point it at.
2. Picks a `ModelingToolkit.AbstractSystem` binding (defaults to a binding
   named `system` or `default_system`; override with `--name`).
3. Calls `mtk2esm(sys)` → tempfile `.esm`.
4. Loads the tempfile back through `esm2mtk` (i.e.
   `ModelingToolkit.System(load(tempfile).models[name])`).
5. Simulates both originals over the declared timespan and compares
   trajectories at a dense sample of points.

Exit codes:

| Code | Meaning                                                 |
|------|---------------------------------------------------------|
| 0    | Round-trip passed within tolerance                      |
| 1    | Trajectory diff exceeded tolerance — the scaffold drifts|
| 2    | Usage / loading error (bad CLI args, missing system)    |
| 3    | Simulation failed (one side blew up; usually a gap)     |

A failure prints a per-variable diff summary; use it to identify which
state(s) drifted and look upstream for unsupported constructs.

---

## 4. Handle `TODO_GAP` markers

`mtk2esm` is not lossless yet — some MTK constructs don't have an `.esm`
spec slot. When the scaffolder hits one, it emits a `TODO_GAP` marker
into the component's `metadata.notes` and logs an `@warn` listing the
unresolved gap IDs.

Each gap carries:

- `bead_id`: the upstream bead tracking the missing schema feature
  (or the literal `"unknown"` if it's something the scaffolder couldn't
  classify).
- `description`: a human-readable one-liner.
- `where`: a location hint (variable name, observed expression index,
  equation index).

How to handle them:

1. **Don't ignore the warning.** Open the emitted `.esm`, search for
   `TODO_GAP`, and read the `notes` block. Each gap is a thing your
   migration is silently dropping.
2. **If the gap is tracked** (`bead_id` is a real bead id like `gt-kuxo`
   for SDE noise, etc.), reference it in your migration commit message
   and on the bead you're working. Mark the migration as partial and
   open a follow-up bead that depends on the upstream tracker.
3. **If the gap is `"unknown"`,** open a new bead under
   `EarthSciSerialization` describing the construct. The scaffolder hit
   something it couldn't even classify — that's a serializer bug, not
   just a missing feature.
4. **Never hand-edit a `TODO_GAP` away** without resolving the
   underlying construct. The marker exists so reviewers and the
   round-trip validator know not to trust the migration end-to-end. A
   round-trip pass on a gap-bearing `.esm` does not mean the model is
   complete — it means the parts that *did* round-trip drift within
   tolerance.

---

## 5. CI integration

The `.github/workflows/test-esm.yml` job invokes `setup_polecat_env.sh`
before `Pkg.instantiate`, so the same resolution path used locally runs
in CI. The `mdl-08t` inline-test walker that runs after instantiate
exercises every committed `.esm`. If your migration adds a new `.esm`,
it gets picked up automatically — no workflow changes needed.

---

## 6. Fleshing out `tests` and `examples`

`mtk2esm` scaffolds the structural parts of the `.esm` (variables,
equations, events) but leaves the `tests` and `examples` blocks thin
or empty. Those blocks are how downstream users and conformance
harnesses verify the migrated component behaves correctly — they are
**not optional**, and a migration with a thin `tests`/`examples` block
is an incomplete migration even if the round-trip validator passes.

### 6.1 `tests` — thorough behavioral coverage

The `tests` block should **thoroughly exercise the behavior of the
model component**, not just smoke-test that it runs. Build it by
reading the upstream Julia test suite of the component you're
migrating and translating those tests into `.esm` form.

Minimum coverage:

- Every scenario covered by the upstream Julia package's `test/`
  directory should have a counterpart entry in the `tests` list.
  If the Julia tests assert a decay curve for `OH`, check the same
  variable at the same time points with comparable tolerances.
- Exercise the full range of species / variables the model tracks,
  not just one or two representative ones.
- Sample at multiple time points spanning short, medium, and long
  dynamics so stiff and slow modes are both covered.
- Include parameter-sweep tests wherever the upstream tests vary
  inputs (temperature, pressure, boundary conditions, etc.).
- Reproduce any regression-test fixtures the upstream package keeps
  (reference trajectories pinned from a trusted run).

Practical workflow:

1. Open the upstream package's `test/runtests.jl` (or equivalent)
   alongside the migrated `.esm`.
2. For each Julia test case, add a matching entry to the `tests`
   list with `assertions` capturing the same numeric checks.
3. Re-run the round-trip validator (section 3) with a tolerance at
   least as tight as the upstream tests used.

`tests` is the physics-level trust signal. Round-trip passing tells
you the *trajectory* matches; dense `tests` tells a reviewer the
migration actually captures the model's scientific behavior.

### 6.2 `examples` — reproduce the paper's figures

The `examples` block should surface the **scientific behavior** of
the component the way a paper or documentation page would. For any
component migrated from a published model, the target is to include
versions of **as many of the figures from the original paper as
possible**.

Draw from two upstream sources:

- **The original paper** (cited in `reference`): each figure showing
  a canonical run, parameter sweep, regime comparison, or sensitivity
  analysis is a candidate example. Reproduce it via an `examples`
  entry with the appropriate `initial_state`, `time_span`, parameter
  overrides, and `Plot` block(s).
- **The upstream Julia package's documentation pages** (typically
  under `docs/src/` or the rendered Documenter.jl site). Doc pages
  are already distilled, often with runnable scripts that map almost
  one-to-one to `.esm` examples. They may also cover runs the paper
  did not include (updated parameters, extended time horizons, etc.).

Practical workflow:

1. Catalog figures from the paper and the doc pages. Each one is a
   candidate `examples[*]` entry.
2. For plots run at specific conditions, reproduce those conditions
   as `initial_state` + parameter overrides.
3. For plots showing a parameter sweep, use `sweep` in the example
   spec rather than producing one entry per sweep point.
4. Pick plot types that match the data: `line` for trajectories,
   `heatmap` for 2-param sweeps, `field_slice` / `field_snapshot`
   for PDE components (see esm-spec.md §6.7).
5. Where the paper or docs provide reference values, include
   `expected` markers in any supporting `tests` entry so CI can
   catch regressions in the figure-reproducing runs.

The bar: someone reading the `.esm` should be able to reproduce the
headline visualizations of the upstream publication without
touching the Julia source. An `examples` block that only runs the
model once with defaults is a migration gap even if everything else
about the file is correct.

---

## 7. Done checklist

Before you run `gt done`, you **must** locally verify every one of the
following. A round-trip-only pass is **not** sufficient — `tests` and
`examples` are part of the behavioral contract, not optional decoration.
The merge queue will re-run the same gates, but the point of this
checklist is to catch failures at the polecat, not at the refinery.

> **The walker is the gate.** The `mdl-08t` inline-test walker
> (`run_esm_tests`) is the only code path that determines whether a
> migration lands. Round-trip passing is *necessary* but not
> *sufficient*; "all examples simulated" claims via `scripts/roundtrip.jl`
> or ad-hoc Julia scripts do **not** clear the gate. The walker uses a
> distinct compile + solve path — see §7.3 — and CI runs the walker, not
> roundtrip. If the walker fails, the migration fails, regardless of
> what other scripts say.

### 7.1 Run the walker locally — exact invocation

CI invokes the walker via `julia-actions/julia-runtest@v1`, which is
equivalent to `Pkg.test()`. Run the **same** command locally before
`gt done`:

```bash
scripts/setup_polecat_env.sh                       # idempotent; once per worktree
julia --project=. -e 'using Pkg; Pkg.test()'       # this IS the walker
```

This loads `test/runtests.jl`, which calls
`run_esm_tests()` over `components/` — the same call CI makes. Do not
substitute `julia --project=. test/runtests.jl` (it bypasses `Pkg.test`'s
test environment), and do not paraphrase the command — copy it.

### 7.2 Report the assertion count

The walker's summary block ends with a line of the form:

```
================ ESM inline-test summary ================
Files discovered: <N>
Assertions:       <M>
...
TOTAL                              <pass>      <fail>      <err>
```

The polecat **must** report the `Assertions:` count and the per-file
TOTAL row in:

- the migration commit message (one line: `walker: M assertions, all pass`), and
- a `bd update <id> --notes "..."` on the assigned bead, before `gt done`.

This lets the witness/mayor sanity-check the count against the new
`.esm`'s declared `tests:` block. A migration that adds 40 assertions
to the file but reports a delta of 0 is suspicious by construction.

A zero-assertion run is **not** acceptable — it means either no test
file is present or your `.esm` was not picked up by
`discover_esm_files`. See §6.1 for the coverage bar.

### 7.3 Walker ≠ `scripts/roundtrip.jl` — they are different code paths

These are commonly confused. They are not interchangeable:

| | `scripts/roundtrip.jl` | Walker (`run_esm_tests`) |
|---|---|---|
| **Lives in** | `EarthSciSerialization.jl` | `EarthSciModels` (`src/run_tests.jl`) |
| **Input** | An upstream MTK `.jl` file | Every committed `.esm` under `components/` |
| **What it checks** | `mtk → esm → mtk` trajectory drift on the upstream system | The committed `.esm`'s `tests:` assertions, sample-by-sample |
| **Solve path** | Whatever `roundtrip.jl` configures (Tsit5, default reltol/abstol) | `run_esm_tests` solver pick (Tsit5 → Rosenbrock23 fallback), `reltol=1e-10`, `abstol=1e-12`, `combinatoric_ratelaws=false` for ReactionSystems |
| **CI runs it?** | No (one-shot polecat-side validation) | **Yes** — this is the gate |

A roundtrip pass tells you the scaffolder didn't drift the trajectory.
The walker tells you the assertions a reviewer actually reads pass on
the committed file with the solver tolerances CI enforces. **Never
substitute one for the other.** Past incident: `mdl-drx` reported "all
4 examples simulate cleanly" via `roundtrip.jl` and was contradicted
by 4 walker assertion failures on CI.

### 7.4 Every `examples:` entry actually runs

Load the `.esm` and simulate each example with its declared
`initial_state`, parameter overrides, and `time_span`. Confirm no
simulation errors. If an example has `expected` markers, they must
satisfy. A syntactically valid `examples` block whose entries fail
to simulate is a regression, not a migration.

### 7.5 No `TODO_GAP` markers remain

Grep the committed `.esm` for `TODO_GAP` — there should be none.
The only exception is when the bead's `blocking_gap` field explicitly
tolerates a gap; in that case, cite the tracked upstream bead id in
your commit message and leave the marker in place. See §4 for the
full gap-handling protocol.

### 7.6 Hard gate

If any one of §7.1–§7.5 fails, do **not** run `gt done`. Fix the
underlying issue (or escalate per §4 / the stuck-polecat protocol)
and re-verify from the top. "All my other scripts pass" is not a
substitute for §7.1. The checklist is a hard gate, not a suggestion.

---

## References

- **Tool**: [`gt-dod2`](https://github.com/EarthSciML/EarthSciSerialization)
  — `mtk2esm` scaffolder + round-trip CLI source of truth.
- **Friction report**: `mdl-uao` — slit's pilot-time notes that
  surfaced the wiring gap this guide addresses.
- **Pilots**: `mdl-dkw` (SuperFast, hand-written), `mdl-qba`
  (CarbonCycle, in flight). Both are useful prior art for how
  `mtk2esm`-scaffolded `.esm` files differ from hand-written ones.
- **Spec**: `EarthSciSerialization/refinery/rig/esm-spec.md` and
  `esm-schema.json` for the canonical `.esm` shape.
