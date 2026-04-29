# AGENTS.md — EarthSciModels (ESM rig)

This file is the rig-specific addendum to the workspace-level Gas Town agent
guide ([`/CLAUDE.md`](../CLAUDE.md)). Read that first; the rules here apply
only to the EarthSciModels repo.

## 1. The single-pathway rule (absolute)

> **A model is simulated through exactly one pathway: an official ESS runner.**

EarthSciML defines one canonical simulation toolchain — the EarthSciSerialization
(ESS) runners — across every supported language:

| Language | Official runner |
| -------- | --------------- |
| Julia    | `EarthSciModels.load_esm` → `ModelingToolkit` (or a `tree_walk` evaluator over the ESS AST) |
| Python   | `earthsci_toolkit.load` + `earthsci_toolkit.evaluate` (the ESS `numpy_interpreter`) |
| Rust     | `earthsci_toolkit::simulate` (ndarray runtime over the ESS AST) |

Anything that takes a `.esm` file and produces numbers — at runtime, in CI, or
in a docs build — **MUST** go through one of these runners. Building a parallel
solver in this rig (or any other) is the **parallel-evaluator anti-pattern** and
is forbidden.

Concrete things this rule forbids in this repo:

- Calling `sympy.lambdify` on rate expressions and integrating with
  `scipy.integrate.solve_ivp` / `odeint`.
- Hand-rolled RK4 / forward-Euler / Rosenbrock loops that walk the ESS AST.
- Re-implementing `ifelse` / `max` / `min` / `^` / `log10` op semantics outside
  the toolkit. Op semantics are single-sourced in
  [EarthSciSerialization](https://github.com/EarthSciML/EarthSciSerialization)
  and exposed via the runners listed above.
- Hand-translating an `.esm` to a different IR (e.g. emitting raw Julia
  `ODEProblem` code from the AST) for the purpose of simulating it. The
  runners are the IR.

If the official runner is missing a feature you need, file a bead against
EarthSciSerialization or the relevant toolkit — do not work around it locally.

## 2. ESM contract

EarthSciModels is the **model-content rig**. Its job, and only its job, is:

1. Hold authoritative `.esm` files under `components/<domain>/`.
2. Provide a **thin** loader shim per language (today: the Julia shim in
   `src/EarthSciModels.jl`) that calls the canonical ESS parser and returns the
   appropriate runtime object (`ModelingToolkit.System`, etc.).
3. Run each `.esm` file's inline `tests` block (ESS spec §6.6) through the
   canonical runner — `EarthSciModels.run_esm_tests` in CI — to verify the
   model's `(variable, time, expected)` assertions.

What does **not** belong in this rig:

- Application-level workflows or pipelines (those live in downstream consumer
  repos).
- Parallel solvers, custom integrators, or any code that simulates a model
  outside the ESS runners — see §1.
- Schema or op-semantics changes — those belong in EarthSciSerialization.
- New runtime languages — those belong in the corresponding toolkit repo
  (`earthsci_toolkit`, etc.), not here.

If you find yourself adding more than a thin call-through to a canonical runner,
stop and check whether the work belongs upstream (ESS) or downstream (a
consumer repo) instead.

## 3. Documentation / plotting builds

Tooling under `tools/` (e.g. `tools/render_example_plots.py`,
`tools/esm_to_docs.py`) and any future docs-build script is bound by §1.

If a docs build needs simulation output to render plots, it **MUST** drive an
official ESS runner. Specifically:

- Python plot rendering: call `earthsci_toolkit.load` + `evaluate` and, for
  ODE examples, the toolkit's official integration entry point. Do **NOT**
  introduce `sympy.lambdify` + `scipy.solve_ivp` (or any equivalent homebrew
  ODE pipeline) in `tools/`.
- Julia plot rendering: use `EarthSciModels.load_esm` (or
  `EarthSciSerialization.load` for multi-component files) and integrate with
  `ModelingToolkit` / `OrdinaryDiffEq` — not a hand-rolled walker.

CI pipelines that exercise `tools/` count as runtime for the purposes of §1:
the parallel-evaluator anti-pattern is just as forbidden in
`.github/workflows/*` as in `src/`.

`tools/render_example_plots.py` currently still contains a homebrew
`sympy.lambdify` + `scipy.solve_ivp` path. Retiring that path onto the
canonical runner is tracked separately (`mdl-render-plots-canonical`); until
that bead lands, do not extend the homebrew path or copy its pattern into new
tooling.

## 4. `scripts/migrations/*` is historical

Files under `scripts/migrations/` (e.g. `migrate_geoschem_fullchem.jl`,
`gen_fastjx_esm.py`, `inject_tests_into_esm.py`, `rewrite_max_in_esm.py`,
`reference_values*.jl`, `run_*.jl`, `verify_*.jl`, `probe_*.jl`,
`roundtrip_wrapper.jl`, `post_process_*.py`, `extract_fastjx_data.jl`) are
**one-shot legacy bridge tools** that already ran during Phase-0 → Phase-3
migrations. They produced the `.esm` files in `components/`; their job is done.

Rules for `scripts/migrations/`:

- **MAY NOT** be invoked from CI (`.github/workflows/*`).
- **MAY NOT** be invoked from runtime code (`src/`, the Julia shim, the
  `earthsci_toolkit` Python/Rust bindings, or any consumer repo).
- **MAY NOT** be imported by `tools/` or `test/` for ongoing functionality.
- **MAY** be read for archaeological reference (how was this `.esm` produced?).
- **MAY** be re-run by hand by a maintainer if a migration needs to be
  redone — but the output of that re-run goes through normal review like any
  other `.esm` change.

Archiving `scripts/migrations/` out of the active tree is tracked separately
(`mdl-archive-migrations`). Until that lands, treat the directory as read-only
historical material.

## 5. Cross-references

- Workspace agent guide: [`/CLAUDE.md`](../CLAUDE.md)
- Polecat operating contract for this rig: [`./CLAUDE.md`](./CLAUDE.md)
- Repo layout convention: [`docs/REPO_LAYOUT.md`](docs/REPO_LAYOUT.md)
- Migration tracker (Phase-0 inventory): [`docs/migration-tracker.md`](docs/migration-tracker.md)
- ESS spec: <https://github.com/EarthSciML/EarthSciSerialization/blob/main/esm-spec.md>
- ESS schema: <https://github.com/EarthSciML/EarthSciSerialization/blob/main/esm-schema.json>
