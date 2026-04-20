# EarthSciModels

[![test-esm](https://github.com/EarthSciML/EarthSciModels/actions/workflows/test-esm.yml/badge.svg)](https://github.com/EarthSciML/EarthSciModels/actions/workflows/test-esm.yml)

Authoritative `.esm` files for Earth-science model components expressed in the
[EarthSciML Serialization Format](https://github.com/EarthSciML/EarthSciSerialization)
(`esm-schema.json`, `esm-spec.md`). Each file is a portable, runtime-agnostic
snapshot of an MTK-derived component with inline tests and examples.

This repo is a *data* repo with a thin Julia shim for loading. The
authoritative content is the `.esm` files; the shim exists only so Julia users
can `load_esm(...)` a single file and get a ready-to-simulate
`ModelingToolkit.System`.

**How this repo is validated:** every push and PR runs each `.esm` file's
inline `tests` block (ESM spec §6.6) through `EarthSciModels.run_esm_tests` —
each scalar `(variable, time, expected)` assertion is checked by simulating
the model and sampling its solution interpolant. One failed assertion turns
the build red. See [`src/run_tests.jl`](src/run_tests.jl) and
[`.github/workflows/test-esm.yml`](.github/workflows/test-esm.yml).

## Quick links

- [`docs/REPO_LAYOUT.md`](docs/REPO_LAYOUT.md) — directory convention.
- [`docs/migration-tracker.md`](docs/migration-tracker.md) — Phase-0 inventory of
  the ~260 MTK components from 14 earthsciml repos, classified by schema-gap
  blockers.
- [EarthSciSerialization spec](https://github.com/EarthSciML/EarthSciSerialization/blob/main/esm-spec.md)
  and [JSON schema](https://github.com/EarthSciML/EarthSciSerialization/blob/main/esm-schema.json).

## Top-level layout

```
components/        # All .esm files, grouped by science domain (one subdir per
                   # upstream earthsciml repo: gaschem/, aerosol/,
                   # atmospheric_dynamics/, earthsci_data/, ...)
docs/              # Migration tracker + layout convention
src/               # Julia shim (EarthSciModels.jl)
test/              # Shim tests + fixtures
.github/workflows/ # CI
```

Within `components/`, each science-domain subdir holds the `.esm` files for
that domain (e.g. `components/gaschem/superfast.esm`). A single `.esm` file can
contain any mix of models, reaction_systems, operators, data_loaders, coupling,
and interfaces — see the ESM spec. One `.esm` file per paper/chapter of
content, not one per source `.jl` file — see `docs/REPO_LAYOUT.md`.

## Julia shim usage

```julia
using Pkg; Pkg.add(url="https://github.com/EarthSciML/EarthSciModels")
using EarthSciModels
using ModelingToolkit

sys = load_esm(EarthSciModels.esm_path("components", "gaschem", "superfast.esm"))
```

For files with multiple models (or non-`Model` entries like `ReactionSystem` or
`DataLoader`), use the underlying parser directly:

```julia
using EarthSciSerialization
esm_file = EarthSciSerialization.load(path)   # returns an EsmFile
# then pick the component you want and build its System / PDESystem / ReactionSystem
```

## Versioning

Each component starts at `version 0.1.0` in its `.esm` file and bumps to
`1.0.0` only when a human maintainer is confident it is scientifically correct
(see each component's `description` / `reference` / inline tests).

## Contributing / migration workflow

Phase-3 per-component migration beads draw from the migration tracker. Each
landing bead adds one `.esm` file plus verification that its inline tests pass
under CI. See the tracker for the current queue.

## License

See [LICENSE](LICENSE).
