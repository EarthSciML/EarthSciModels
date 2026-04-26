# `scripts/migrations/`

Scripts that translate upstream MTK / Catalyst components into committed `.esm`
files under `components/`. One script per migrated mechanism, plus shared
helpers.

See `docs/migration-guide.md` for the end-to-end migration workflow. This
README covers only the **per-environment setup** that polecats must do once
before running any GasChem-based migration.

## GasChem.jl Catalyst / MTK compat

**Symptom (you'll see this if you skip the setup below):**

```
Unsatisfiable requirements detected for package Catalyst
  GasChem [...] requires Catalyst = 15
  EarthSciSerialization [...] requires Catalyst = 16
```

or, if you fall back to the registry:

```
Unsatisfiable requirements detected for package ModelingToolkit
  GasChem 0.11.0 requires ModelingToolkit = 10
  EarthSciSerialization 0.0.3 requires ModelingToolkit = 11
```

**Why:** GasChem.jl 0.12.0 (the unreleased dev version polecats need) declares
`Catalyst = "15"` in `[compat]` but its `[sources]` entry pulls Catalyst master
(v16+). EarthSciSerialization 0.0.3 requires `Catalyst = "16"` and
`ModelingToolkit = "11"`. The published GasChem 0.11.0 pins MTK 10, so the
registry version cannot resolve against ESS either. The only resolvable shape
today is "GasChem dev checkout, with `Catalyst = "15"` bumped to `"16"` in
its compat block."

**Fix (run once per polecat sandbox):**

```bash
# Make sure GasChem is dev'd locally.
julia -e 'using Pkg; Pkg.develop("GasChem")'

# Bootstrap the migrations env (patches GasChem compat + Pkg.develops the
# three local packages it depends on).
scripts/migrations/setup_gaschem_env.sh
```

The script:

1. Locates the GasChem dev checkout (`$GASCHEM_DEV_PATH` or `~/.julia/dev/GasChem`)
   and rewrites `Catalyst = "15"` → `Catalyst = "16"` in its `Project.toml`. The
   sed is idempotent — re-running on an already-patched checkout is a no-op
   and does not error. Unfamiliar compat shapes are left alone with a warning.
2. Locates the EarthSciSerialization checkout (`$EARTHSCI_SERIALIZATION_PATH`
   or the Gas Town workspace defaults — same rules as `scripts/setup_polecat_env.sh`).
3. `Pkg.develop`s **EarthSciModels** (this repo), **EarthSciSerialization**, and
   the patched **GasChem** into `scripts/migrations/`'s env in a single resolve,
   then instantiates. Developing all three at once is required: the migrations
   env's `Project.toml` lists EarthSciModels + EarthSciSerialization as deps
   but neither is registered, so they have to come from local paths.

After this, `julia --project=scripts/migrations -e 'using GasChem, EarthSciSerialization, Catalyst'` works.

## When this can be retired

When GasChem.jl ships a release (or `master` tag) with both:

- `Catalyst = "16"` in `[compat]`
- `ModelingToolkit = "11"` in `[compat]`

the patch step in `setup_gaschem_env.sh` becomes a no-op for new checkouts
and can be deleted. Track via the upstream repo:
<https://github.com/EarthSciML/GasChem.jl>.

If a polecat picks up another GasChem migration before that lands, they should
either (a) use this script as-is or (b) open the upstream PR themselves and
remove this workaround in the same change. Filing the upstream PR is the
preferred long-term fix; this script is the bridge until it lands.
