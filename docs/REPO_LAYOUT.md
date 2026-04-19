# EarthSciModels repository layout

This repository holds authoritative `.esm` (EarthSciML Serialization Format) files
for MTK-derived Earth-science model components. It is a *data* repo: the files
here are the canonical serialized models, and CI validates that each one's inline
tests pass.

## Top-level directories

Each top-level directory corresponds to one kind of ESM schema entity, matching
the type enum used by the migration tracker (`docs/migration-tracker.md`) and the
ESM spec (EarthSciSerialization/esm-spec.md):

| Directory | Contains | ESM type(s) | Example path |
|---|---|---|---|
| `models/` | `.esm` files whose top-level entity is a `Model` (ODE/PDE/nonlinear/algebraic). One file per model or per paper/chapter. | `models:` | `models/gaschem/superfast.esm`, `models/aerosol/isorropia/isorropia.esm` |
| `reaction_systems/` | `.esm` files for Catalyst / `@reaction_network` systems | `reaction_systems:` | `reaction_systems/gaschem/geoschem_fullchem.esm` |
| `operators/` | `.esm` files for standalone `Operator` entries (e.g. advection stencils, PBL callback) | `operators:` | `operators/environmental_transport/advection.esm` |
| `data_loaders/` | `.esm` files for `DataLoader` entries (ERA5, GEOSFP, NEI, ...) | `data_loaders:` | `data_loaders/era5.esm` |
| `coupling/` | `.esm` files for standalone `CouplingEntry` entries (cross-model param-to-var / operator_compose / couple). Optional — couplings are often embedded inside a parent Model's `coupling:` block per ESM spec §10. | `coupling:` | `coupling/fastjx_superfast.esm` |
| `interfaces/` | `.esm` files for reusable `Interface` entries (registered functions, coordinate transforms, callback handler contracts). | `interfaces:` | `interfaces/registered_functions/flux_interp.esm` |
| `docs/` | Markdown documentation. | n/a | `docs/migration-tracker.md`, `docs/REPO_LAYOUT.md` |

Additional top-level items:

- `src/EarthSciModels.jl` — thin Julia shim exporting `load_esm(path) → System`.
- `test/runtests.jl` — package tests (CI runs these).
- `.github/workflows/test-esm.yml` — CI entry point.

## Per-source-repo subdirectory convention

Within each top-level kind directory, use one subdirectory per source repo,
matching the lowercase-with-underscores form of the source repo name (dropping
`.jl`):

```
models/
  aerosol/
    aerosol_dynamics.esm
    cloud_physics/
      cloud_physics.esm
      droplet_growth.esm
    isorropia/
      isorropia.esm
    ...
  atmospheric_dynamics/
    clark1977/
      clark1977_anelastic_system.esm
      anelastic_momentum.esm
    ...
  gaschem/
    superfast.esm
    geoschem_fullchem.esm
    stratospheric/
      stratospheric_ozone_system.esm
    ...
  urban_canopy/
    urban_canopy_model.esm
    hydro/
    temps/
  vegetation/
  wildland_fire/
  environmental_transport/
  ...
```

## One file per model, not one per source-file

**Rule (from `README.md`):** each `.esm` file holds approximately one paper or
chapter of content — a self-contained set of components that together describe
one scientific mechanism, with inline tests and examples. This is *finer* than
"one file per `src/<name>.jl`" in the upstream repo.

For example, `Aerosol.jl/src/aqueous_equilibria.jl` contains 9 `@component`
functions. These all describe the same aqueous-phase equilibria mechanism from
Seinfeld & Pandis, so they can live in a single `.esm` file. In contrast,
`Aerosol.jl/src/cloud_physics.jl` covers 9 distinct mechanisms (water
properties, Kohler theory, droplet growth, ice physics, rain formation, ...)
and should be split into separate `.esm` files in `models/aerosol/cloud_physics/`.

The migration tracker (`docs/migration-tracker.md`) lists suggested
`target_path`s — these are suggestions only; Phase-3 migrators may reorganize.

## File naming

- Use lowercase snake_case matching the ESM component name: `.../superfast.esm`,
  `.../cloud_physics.esm`.
- One-component files: the file name matches the component name.
- Multi-component files: the file name reflects the bundle (e.g.
  `aqueous_equilibria.esm` holds `WaterEquilibrium`, `CO2Equilibria`, ...).

## What is NOT in this repo

- MTK Julia source (lives in `Aerosol.jl`, `GasChem.jl`, etc. under
  github.com/EarthSciML).
- The ESM parser / schema / MTK-conversion code (lives in
  `EarthSciSerialization.jl`).
- Runtime simulation drivers (each model's inline tests + examples are
  self-contained; end-to-end drivers go in the consumer's code).

## Empty-directory policy

Each top-level directory holds a `.gitkeep` until real content lands. Remove
`.gitkeep` when the first real `.esm` file is added.
