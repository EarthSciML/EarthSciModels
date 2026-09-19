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
   A document declares a higher minor version when, and only when, it uses a
   construct that arrives there: `components/gaschem/pollu.esm` is on **1.1.0**
   because the top-level `solver` block (esm-spec §2.2) does, and a 1.0.0
   document carrying one is rejected with `solver_version_too_old`.
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

   - **Python (`tools/run_esm_inline_tests.py`):** drives the public
     `earthsci_ast.inline_tests.run_inline_tests` per §1. The gate itself
     owns only discovery, the per-file subprocess (so it is the only
     runner with OOM isolation), the junit report and the summary —
     §6.6 semantics, the integrator and its tolerances are the toolkit's.
     It is the runner the corpus was migrated against. Walks
     `components/**`, `lib/**` and `registered_functions/**`.

     No per-file knob tables live in this rig, with one measured
     exception. A document that needs a stiff integrator says so ITSELF
     with `solver.stiffness: "high"` (esm-spec §2.2), which every binding
     maps to its own solver; a basename table in one gate cannot travel
     to the other two. One document in the corpus declares it —
     `components/gaschem/pollu.esm`, the POLLU stiff benchmark, whose
     rate constants span ~8e-7 to ~7e9 1/s: with the declaration each
     binding picks an implicit method and all 61 of its assertions pass,
     and without it Julia's explicit default gives every one of them back
     as `retcode MaxIters`. `cse` is the exception, because the spec keeps it
     out of the document (it is a SymPy-lowering knob, not a fact about
     the model) and the corpus contains one document the library default
     cannot build in usable time: `geoschem_fullchem.esm` does not finish
     in 50 minutes under `cse=True` and passes 81/81 in 506 s under
     `cse=False`, while `urban_canopy_model.esm` is the mirror image
     (2.3 min / >50 min). `CSE_FALSE_FILENAMES` in the gate names the one
     document, and goes away when the toolkit picks CSE from system size.
   - **Julia (`EarthSciModels.run_esm_tests`):** drives
     `EarthSciAST.run_inline_tests` — the TREE-WALK runner, the same
     pathway the Python gate uses — one document at a time. It runs by
     default under `pkg test` for local development, and in CI as the
     `julia-inline-tests` matrix, one shard per job
     (`ESM_TESTS_SHARD="i/n"`, see `shard_esm_files`); the shards are a
     partition of the corpus, so sharding splits the cost without
     dropping a file. `ESM_TESTS_SKIP_LIVE_REPO=1` short-circuits the
     walk locally for a fast shim-only `pkg test`.

     Deliberately NOT `EarthSciAST.run_esm_tests`, the MTK walker: its
     lowering has no arm for a long tail of ops this corpus uses (`and`,
     `or`, `floor`, `atan2`, `datetime.hour`, an unexpanded
     `apply_expression_template` in a reaction rate), so documents that
     integrate fine fail there at compile time — over a sample of the
     files the job used to report red, the MTK walker passed 0 of 276
     assertions and the tree-walk runner 190. Materializing a document
     as an MTK `System` is `load_esm`, and the package's own tests cover
     it; it is not how the corpus gate runs.
   - **Rust (`esm test`):** the `earthsci-ast` crate's CLI, built from
     EarthSciAST main by the `rust-cli-inline-tests` job.

   No binding clears the corpus today, and the jobs say so rather than
   hiding it. The Python gate — the one that reported 22 assertions while
   running nothing — passes 8,181 of the 8,198 rows it emits over the whole
   corpus (a count that includes one load-only row per document declaring
   no inline tests). The seventeen exceptions are of two kinds.

   Seven are numeric misses of a declared tolerance, in three documents:
   `aerosol/transport/droplet_mass_balance.esm` (4, worst ~4e-8 against a
   declared 1e-8), `gaschem/stratospheric/brox_cycle.esm` (2, worst 1.4e-4
   against 1e-5) and `gaschem/stratospheric/chapman.esm` (1, 2.6e-6 against
   1e-6). All three bindings reproduce those seven, agreeing with each
   other to ~10 significant digits and disagreeing with the stored
   `expected` — so the question is the recorded value or the tolerance, not
   a binding.

   The other ten are `environmental_transport/puff.esm`, the corpus's
   sharpest cross-binding divergence: 12.0 minutes under the Python runner,
   ten of its 28 assertions coming back as `solve failed` from scipy's
   LSODA callback, against 86 s and 28/28 under the Julia runner and 0.02 s
   and 28/28 under the Rust CLI.

   The Julia sweep is further behind, and until this branch nobody had
   counted by how much. A single-process walk of 343 documents (the corpus
   less the four slowest) through `EarthSciAST.run_inline_tests` takes
   about 40 minutes and returns 7,562 passes, 30 failures and 457 errors,
   with 17 documents carrying at least one non-pass row. Measured with
   `${ESD_ROOT}` unset, which also errors the two `surface_runoff`
   documents that need it; CI sets it, so those are not in these figures.

   Two documents dominate. `stratospheric_ozone_system.esm` errors all 176
   of its assertions after 19.5 minutes, where the Python gate passes all
   176 in 5.9 s; `gaschem/methane/methane_ode.esm` errors all 107 after
   3.7 minutes, against 107 passes in 2.9 s. A third is diagnosed:
   `gaschem/stratospheric/chapman.esm`'s `dense_M_perturbation` errors with
   `maxiters` under the non-stiff default, and a stiff integrator clears it
   at no cost elsewhere (66/67 in 5.6 s against 61/67 in 94.7 s) — that
   document declares no `solver.stiffness`, and whether it should is a
   question about the model rather than about the gate.

   The Rust path does not clear it either, and that job says so too:
   measured when it landed, the Rust sweep leaves
   96 of the 322 files with inline tests carrying at least one non-pass
   row (diffsol failing the first step, algebraic unknowns with no
   `D(x,t)` equation, unexpanded §4.7 `${VAR}` refs, a few numeric
   divergences). Closing that is upstream work on EarthSciAST, not corpus
   work here — but it is upstream work with a red job attached to it,
   which is the point.

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

Do not put "Co-Authored-By: Claude ..." in any commit messages. Claude is an LLM and LLMs cannot take responsibility for outputs, therefore they cannot be authors.
