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
