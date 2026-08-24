# EarthSciModels

[![test-esm](https://github.com/EarthSciML/EarthSciModels/actions/workflows/test-esm.yml/badge.svg)](https://github.com/EarthSciML/EarthSciModels/actions/workflows/test-esm.yml)

Authoritative `.esm` files for Earth-science model components expressed in the
[EarthSciML Serialization Format](https://github.com/EarthSciML/EarthSciAST)
(`esm-schema.json`, `esm-spec.md`). Each file is a portable, runtime-agnostic
snapshot of an MTK-derived component with inline `tests` and `analyses`.

This repo is a *data* repo with a thin Julia shim for loading. The
authoritative content is the `.esm` files; the shim exists only so Julia users
can `load_esm(...)` a single file and get a ready-to-simulate
`ModelingToolkit.System`.

**How this repo is validated:** every push and PR runs each `.esm` file's
inline `tests` block (ESM spec §6.6) through `tools/run_esm_inline_tests.py`
(the Python gate of record, driving `earthsci_ast.simulation.simulate`).
Each scalar `(variable, time, expected)` assertion is checked by simulating
the model and sampling its solution interpolant. One failed assertion turns
the build red. The Julia equivalent `EarthSciModels.run_esm_tests` runs the
same contract via MTK and is the canonical local walker (see
[`src/run_tests.jl`](src/run_tests.jl)). Workflow definition:
[`.github/workflows/test-esm.yml`](.github/workflows/test-esm.yml).

## Quick links

- [`docs/REPO_LAYOUT.md`](docs/REPO_LAYOUT.md) — directory convention.
- [`docs/migration-tracker.md`](docs/migration-tracker.md) — Phase-0 inventory of
  the ~260 MTK components from 14 earthsciml repos, classified by schema-gap
  blockers.
- [EarthSciAST spec](https://github.com/EarthSciML/EarthSciAST/blob/main/esm-spec.md)
  and [JSON schema](https://github.com/EarthSciML/EarthSciAST/blob/main/esm-schema.json).

## Top-level layout

```
components/        # All .esm files, grouped by science domain (one subdir per
                   # upstream earthsciml repo: gaschem/, aerosol/,
                   # atmospheric_dynamics/, earthsci_data/, ...)
lib/               # Standard-library .esm subsystems (e.g. solar.esm — solar
                   # geometry; included from components via §4.7 reference)
docs/              # Migration tracker + layout convention
src/               # Julia shim (EarthSciModels.jl)
test/              # Shim tests + fixtures
.github/workflows/ # CI
```

`lib/` holds reusable, dependency-light subsystems that other `.esm` files in
`components/` include via §4.7 references — currently `lib/solar.esm` (NOAA
Spencer-Fourier solar declination, equation of time, and zenith angle). Stdlib
files use the same `.esm` schema as components and are validated by the same
inline-test machinery.

Within `components/`, each science-domain subdir holds the `.esm` files for
that domain (e.g. `components/gaschem/superfast.esm`). A single `.esm` file can
contain any mix of models, reaction_systems, coupling and `data_sources` — see
the ESM spec. (`data_sources` is the esm 1.0.0 ingest registry, §8: it is pure
I/O and is *not* a component, so a model consumes one through a parameter whose
`update` names it rather than by mounting it.) One `.esm` file per
paper/chapter of content, not one per source `.jl` file — see
`docs/REPO_LAYOUT.md`.

## Julia shim usage

```julia
using Pkg; Pkg.add(url="https://github.com/EarthSciML/EarthSciModels")
using EarthSciModels
using ModelingToolkit

sys = load_esm(EarthSciModels.esm_path("components", "gaschem", "superfast.esm"))
```

For files with multiple models (or non-`Model` entries like `ReactionSystem`),
use the underlying parser directly:

```julia
using EarthSciAST
esm_file = EarthSciAST.load_path(path)   # returns an EsmFile
# then pick the component you want and build its System / PDESystem / ReactionSystem
```

## Versioning

The top-level `"esm"` field is the **format** version, not a per-component
maturity marker: it says which revision of `esm-schema.json` the file conforms
to, and every file in this repo carries the same value. The corpus is on
**1.0.0**, a clean break with no deprecation path — `earthsci_ast` rejects any
major-0 document outright, so a file cannot be left behind on an older
spelling. Bumping it is a whole-corpus migration, never a per-file edit.

Scientific maturity is judged from a component's `description`, `reference`
and its inline `tests` block, which is what CI actually checks.

## Contributing / migration workflow

Phase-3 per-component migration beads draw from the migration tracker. Each
landing bead adds one `.esm` file plus verification that its inline tests pass
under CI. See the tracker for the current queue.

## Authoring model components (.esm files)

Components declare reactions, parameters, and rate expressions. Rate
laws should be written as ExpressionNode AST trees using existing ops
(`+ - * / ^ exp log10 sqrt max min ifelse` etc.) — see
[EarthSciAST esm-spec.md §4.2](https://github.com/EarthSciML/EarthSciAST/blob/main/esm-spec.md#42-expressionnode-ops)
for the full op enum and
[§9.2](https://github.com/EarthSciML/EarthSciAST/blob/main/esm-spec.md#92-when-a-call-op-is-justified)
for when (rarely) a `call` op is justified.

Do NOT:
- Reach for `{op: "call", fn: "…"}` to hide math that's expressible in AST
- Write a per-binding helper function for a model-specific formula
- Register a function for anything that fits on paper as a finite expression

Legitimate uses of `call`: tabulated photolysis coefficients,
empirical formulas without closed-form (e.g. Wesely canopy resistance),
implicit solvers. See §9.2 for the decision tree.

When in doubt: AST.

## License

See [LICENSE](LICENSE).
