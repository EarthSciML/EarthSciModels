# AGENTS.md — EarthSciModels

## 1. The single-pathway rule (absolute)

> **A model is simulated through exactly one pathway: an official EarthSciAST runner.**

EarthSciML defines one canonical simulation toolchain — the EarthSciAST
(ESS) runners — across every supported language:

| Language | Official runner |
| -------- | --------------- |
| Julia    | `EarthSciModels.load_esm` → `ModelingToolkit` (or a `tree_walk` evaluator over the ESS AST) |
| Python   | `earthsci_ast.load` + `earthsci_ast.evaluate` (the ESS `numpy_interpreter`) |
| Rust     | `earthsci_ast::simulate` (ndarray runtime over the ESS AST) |

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
  [EarthSciAST](https://github.com/EarthSciML/EarthSciAST)
  and exposed via the runners listed above.
- Hand-translating an `.esm` to a different IR (e.g. emitting raw Julia
  `ODEProblem` code from the AST) for the purpose of simulating it. The
  runners are the IR.
- Re-deriving **variable classification** from a model's equations. From esm
  1.0.0 a document declares exactly two variable types, `unknown` and
  `parameter`. Whether an unknown is an ODE state, an observed quantity or an
  algebraic one, and whether a parameter is Brownian / discrete / sampled /
  constant, are DERIVED (esm-spec §6.3.1) and single-sourced in
  `earthsci_ast.classification` — `ode_states`, `observed_definitions`,
  `algebraic_unknowns`, `parameters`, `brownian_parameters`, … Code that used
  to branch on `variable.type == "state"` / `"observed"` / `"brownian"` /
  `"discrete"` calls those instead. Walking the equations locally to answer
  the same question is the shadow-logic form of this anti-pattern: it drifts
  from the spec and from the other four bindings.

If the official runner is missing a feature you need, file a bead against
EarthSciAST or the relevant toolkit — do not work around it locally.

## 2. ESM contract

EarthSciModels is the **model-content rig**. Its job, and only its job, is:

1. Hold authoritative `.esm` files under `components/<domain>/`, at the
   **current** format version. The corpus is on esm **1.0.0**, which is a
   clean break with no deprecation path — `earthsci_ast` rejects every major-0
   document outright, so there is no such thing as a file left behind on 0.x.
2. Provide a **thin** loader shim per language (today: the Julia shim in
   `src/EarthSciModels.jl`) that calls the canonical ESS parser and returns the
   appropriate runtime object (`ModelingToolkit.System`, etc.).
3. Run each `.esm` file's inline `tests` block (ESS spec §6.6) through a
   canonical runner to verify the model's `(variable, time, expected)`
   assertions. All three canonical runners sweep the corpus in CI
   (`.github/workflows/test-esm.yml`), because a single-runner sweep cannot
   see a cross-binding divergence.

   Every runner walks the WHOLE corpus and every runner blocks. There is
   no allowlist, no deferred set and no per-runner exclusion: where one
   binding cannot yet run what another already does, that is reported as
   a failing job. A green CI therefore means all three bindings agree on
   every assertion, and a red one names which binding does not.

   - **Python (`tools/run_esm_inline_tests.py`):** drives
     `earthsci_ast.solve(cse=False)` per §1 (mdl-w1j → mdl-lvu).
     Per-file subprocess, so it is the only runner with OOM isolation,
     and the one the corpus was migrated against. Walks
     `components/**`, `lib/**` and `registered_functions/**`.
   - **Julia (`EarthSciModels.run_esm_tests`):** the canonical Julia
     walker; runs by default under `pkg test` for local development and
     exercises the same `.esm` files via MTK directly. In CI it runs as
     the `julia-inline-tests` matrix, one shard per job
     (`ESM_TESTS_SHARD="i/n"`, see `shard_esm_files`): the walk builds
     every system in-process, so its cost scales with the corpus — ~4
     s/file measured, ~25 min for the whole walk — which is what blew the
     single-job budget in esm-g97l / esm-m0r2. Sharding splits the cost
     across runners; it does not drop a file — the shards are a partition
     of the corpus. `ESM_TESTS_SKIP_LIVE_REPO=1` still
     short-circuits the walk locally for a fast shim-only `pkg test`.
   - **Rust (`esm test`):** the `earthsci-ast` crate's CLI, built from
     EarthSciAST main by the `rust-cli-inline-tests` job.

   The Rust and Julia paths do not clear the corpus today, and the jobs
   say so rather than hiding it. Measured when they landed: the Rust
   sweep leaves 96 of the 322 files with inline tests carrying at least
   one non-pass row (diffsol failing the first step, algebraic unknowns
   with no `D(x,t)` equation, unexpanded §4.7 `${VAR}` refs, a few
   numeric divergences), and the in-process Julia walk is not expected to
   survive geoschem_fullchem.esm's 819-reaction Catalyst → MTK build on a
   16 GB runner. Closing those is upstream work on EarthSciAST, not
   corpus work here — but it is upstream work with a red job attached to
   it, which is the point.

What does **not** belong in this rig:

- Application-level workflows or pipelines (those live in downstream consumer
  repos).
- Parallel solvers, custom integrators, or any code that simulates a model
  outside the ESS runners — see §1.
- Schema or op-semantics changes — those belong in EarthSciAST.
- New runtime languages — those belong in the corresponding toolkit repo
  (`earthsci_ast`, etc.), not here.

If you find yourself adding more than a thin call-through to a canonical runner,
stop and check whether the work belongs upstream (ESS) or downstream (a
consumer repo) instead.

## 3. Documentation / plotting builds

Tooling under `tools/` (e.g. `tools/render_example_plots.py`,
`tools/esm_to_docs.py`) and any future docs-build script is bound by §1.

If a docs build needs simulation output to render plots, it **MUST** drive an
official ESS runner. Specifically:

- Python plot rendering: call `earthsci_ast.load` + `evaluate` and, for
  ODE analyses, the toolkit's official integration entry point. Do **NOT**
  introduce `sympy.lambdify` + `scipy.solve_ivp` (or any equivalent homebrew
  ODE pipeline) in `tools/`.
- Julia plot rendering: use `EarthSciModels.load_esm` (or
  `EarthSciAST.load` for multi-component files) and integrate with
  `ModelingToolkit` / `OrdinaryDiffEq` — not a hand-rolled walker.

CI pipelines that exercise `tools/` count as runtime for the purposes of §1:
the parallel-evaluator anti-pattern is just as forbidden in
`.github/workflows/*` as in `src/`.

`tools/render_example_plots.py`'s time-series path now drives
`earthsci_ast.simulation.simulate` — the canonical Python ESS runner —
for every ODE integration (mdl-5xp). The renderer keeps its own resolution
plan only to recover *observed* variables from the integrated state via
`earthsci_ast.evaluate` (the canonical AST evaluator). Do not add a
homebrew `sympy.lambdify` / `scipy.solve_ivp` branch back in; if simulate
lacks a feature the doc-build needs, file a bead to extend simulate rather
than re-introducing a side channel.

Both generators read the **esm 1.0.0** vocabulary, and both take their
variable classification from `earthsci_ast.classification` per §1:

- The illustrative-run block on a Model / ReactionSystem is `analyses`
  (esm-spec §6.7), not `examples`. The `Analysis` `$def` is
  `additionalProperties: false`, so the 0.4-era `title` / `code` / `language`
  keys cannot appear and nothing reads them. Plot artifacts still land at
  `<esm_dir>/<esm_stem>.plots/<analysis_id>-<plot_id>.png`; the two modules
  keep their `*_example_*` filenames so the CI job and this convention keep
  resolving.
- The document-scoped ingest registry is `data_sources` (esm-spec §8), not
  `data_loaders`. A source is pure I/O: it is **not** a component, not a
  coupling endpoint, not a subsystem, and it exposes no variables. A model
  consumes one by declaring a **parameter** whose `update` is
  `{kind: "data", source: "<registry key>", from: {file_variable, …}}` — so
  units live on the parameter, and a `data`-updated parameter must declare a
  `shape`. `esm_to_docs.py` still emits a page per source, carrying its I/O
  descriptor rather than a variables table.
- There is no `variables[v].expression`. An observed quantity is defined by a
  bare-variable-LHS equation in the model's `equations`, and both generators
  recover it through `classification.observed_definitions`.

## 4. `scripts/_archive/*` is historical

Files under `scripts/_archive/` (currently `scripts/_archive/migrations/`,
e.g. `migrate_geoschem_fullchem.jl`, `gen_fastjx_esm.py`,
`inject_tests_into_esm.py`, `rewrite_max_in_esm.py`, `reference_values*.jl`,
`run_*.jl`, `verify_*.jl`, `probe_*.jl`, `roundtrip_wrapper.jl`,
`post_process_*.py`, `extract_fastjx_data.jl`) are **one-shot legacy bridge
tools** that already ran during Phase-0 → Phase-3 migrations. They produced
the `.esm` files in `components/`; their job is done. See
[`scripts/_archive/README.md`](scripts/_archive/README.md) for the canonical
archive policy.

Rules for `scripts/_archive/`:

- **MAY NOT** be invoked from CI (`.github/workflows/*`).
- **MAY NOT** be invoked from runtime code (`src/`, the Julia shim, the
  `earthsci_ast` Python/Rust bindings, or any consumer repo).
- **MAY NOT** be imported by `tools/` or `test/` for ongoing functionality.
- **MAY NOT** be added to `Project.toml`, `runtests.jl`, or any other
  active build/test manifest.
- **MAY** be read for archaeological reference (how was this `.esm` produced?).
- **MAY** be re-run by hand by a maintainer if a migration needs to be
  redone — but in that case move the script back out of `_archive/` first,
  so the archive stays a clean "no live code" boundary, and the output of
  that re-run goes through normal review like any other `.esm` change.

## 5. Cross-references

- Workspace agent guide: [`/CLAUDE.md`](../CLAUDE.md)
- Polecat operating contract for this rig: [`./CLAUDE.md`](./CLAUDE.md)
- Repo layout convention: [`docs/REPO_LAYOUT.md`](docs/REPO_LAYOUT.md)
- Migration tracker (Phase-0 inventory): [`docs/migration-tracker.md`](docs/migration-tracker.md)
- ESS spec: <https://github.com/EarthSciML/EarthSciAST/blob/main/esm-spec.md>
- ESS schema: <https://github.com/EarthSciML/EarthSciAST/blob/main/esm-schema.json>
