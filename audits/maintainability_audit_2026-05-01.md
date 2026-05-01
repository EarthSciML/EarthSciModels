# EarthSciModels maintainability audit — 2026-05-01

- **Bead:** mdl-nip (review-only)
- **Auditor:** EarthSciModels/polecats/capable
- **Branch:** polecat/capable-momzfcif (worktree only — not committed)
- **Method:** depth-first on load-bearing areas, breadth across the surface.
  Audit-only; no commits.
- **Scope corpus:** 8 `.esm` files (3 gaschem, 5 aerosol), 1 `lib/solar.esm`,
  Julia shim (`src/`, ~600 LoC), Python tooling (`tools/`, ~4500 LoC),
  CI workflows (2 files), 2 doc pages, 46 open beads.

---

## Findings

Severity legend: P0 (block) · P1 (must fix this cycle) · P2 (next cycle) ·
P3 (backlog). Effort: S (≤½ day) · M (1–3 days) · L (>3 days).

### F1 — `.esm` schema-version drift across the corpus
- **Severity:** P2 · **Effort:** M (per-file bump + regression run)
- **Files:**
  - `components/gaschem/geoschem_fullchem.esm` → `"esm": "0.4.0"`
  - `components/gaschem/fastjx.esm` → `"esm": "0.3.0"`
  - `lib/solar.esm` → `"esm": "0.3.0"`
  - 6 others (`superfast`, all aerosol/*) → `"esm": "0.1.0"`
- **Current state:** versions span three minor releases. The Python and Julia
  ESS parsers both load all of them, so the drift is invisible at runtime, but
  any spec field added at `0.2`–`0.4` (e.g. `expression_templates`,
  `function_tables`) is silently unavailable in the `0.1.0` files even though
  some — `superfast.esm` (Arrhenius rates) — would benefit (see F2).
- **Recommendation:** standardize on the highest version we currently emit
  (`0.4.0`), bump in-place across all 9 files, run the inline-test gate, and
  open follow-up beads for each file that *gains* expressive capability at
  the new level (so the bump isn't no-op rewriting).

### F2 — Expression-template adoption is incomplete past `geoschem_fullchem`
- **Severity:** P2 · **Effort:** M (mostly mechanical per-file)
- **Files:** `components/gaschem/superfast.esm` (27 reactions, 0 templates),
  `geoschem_fullchem.esm` (819 reactions, 10 templates — landed in mdl-mzp).
- **Current state:** `superfast.esm`'s rate ASTs are 19 copies of the same
  shape (`A·P·exp(-Ea/T) / (R·T)` and minor variants); each rate is a fresh
  inline tree. mdl-mzp covered Troe/JPL forms only on the GEOS-Chem
  mechanism — no follow-up bead yet exists for SuperFast or other reaction
  systems.
- **Recommendation:** factor a 2–3-template family
  (`arrhenius_PoverRT`, `arrhenius_PoverRT_clamp`, …) and rewrite the 19
  matches; gives `tools/esm_to_docs` something to render in the Expression
  Templates section (mdl-jaf already supports it) and removes ~25 lines of
  cut-and-paste rate AST.

### F3 — Inline-test tolerance variance is unrationalized
- **Severity:** P2 · **Effort:** S (one-pass annotation pass)
- **Spread observed (rel tolerances per file):**

  | file | rel range |
  |---|---|
  | `geoschem_fullchem.esm` | 1e-3 |
  | `fastjx.esm` | 5e-3 |
  | `superfast.esm` | 1e-10 → 1e-2 |
  | `cloud_albedo.esm` | 1e-8 |
  | `water.esm` | 1e-6 |
  | `droplet_growth.esm` | 1e-4 |
  | `aerosol_scavenging.esm` | 1e-8 |
  | `diameter_growth.esm` | 1e-4 → 1e-3 |

- **Current state:** mdl-1k5 loosened `superfast.esm` for the Python ESS
  runner; the broader pattern is undocumented. `geoschem_fullchem.esm` at
  `rel=1e-3` is two orders of magnitude looser than `superfast.esm`'s
  tightest bands, and `fastjx.esm` sits at `5e-3` with no commentary.
- **Recommendation:** add a one-line `rel_rationale` (or `description`) to
  each `tolerance` block — what numerical artifact justifies the rel/atol
  pair (LSODA truncation, lambdify CSE precision, MTK structural ordering,
  reference-value precision). Avoids drift via "loosen until green".

### F4 — Inline-test gate uses private `earthsci_toolkit` internals
- **Severity:** P2 · **Effort:** S in this rig (M upstream)
- **Files:** `tools/run_esm_inline_tests.py:166-233`
  (`_build_cse_false_cache`).
- **Current state:** the gate pre-populates
  `flat._simulate_compile_cache` with a hand-built `_CompiledRhs` to flip
  `cse=False` on the lambdify call (mdl-w1j workaround for the lambdify
  memory cliff on `geoschem_fullchem`). The names imported —
  `_CompiledRhs`, `_flat_to_sympy_rhs`, `_LAMBDIFY_MODULES`,
  `_simulate_compile_cache` — all begin with `_` and are private
  implementation details of the upstream package. The pattern is endorsed
  upstream (mirrors `test_simulation_csefalse_geoschem.py` per esm-5gk),
  but we still ship CI behavior coupled to a private surface that can move
  without notice.
- **Recommendation:** file an ESS bead asking `earthsci_toolkit.simulate`
  to expose a public `cse: bool = True` kwarg, then reduce
  `_build_cse_false_cache` to a single `simulate(..., cse=False)` call
  here. Single-pathway-rule compliance ✓ (the canonical runner is what
  walks the AST), but the `_-prefixed` import surface is brittle.

### F5 — Python `earthsci_toolkit` is unpinned in both CI legs
- **Severity:** P2 · **Effort:** S
- **Files:**
  - `.github/workflows/test-esm.yml:90` —
    `earthsci_toolkit @ git+...EarthSciSerialization.git@main#subdirectory=...`
  - `.github/workflows/docs.yml:55-60` —
    `git clone --depth=1 ... main` then `pip install`.
- **Current state:** both Python jobs install whatever is at
  `EarthSciSerialization main` HEAD when CI runs. The Julia leg pins
  `EarthSciSerialization = "0.0.3"` in `Project.toml [compat]`, so the two
  legs can disagree on parser/runner behavior across the same workflow run.
  Combined with F4 (private-name coupling), an upstream rename is a CI
  outage.
- **Recommendation:** pin `earthsci_toolkit` to a commit SHA, refreshed in
  step with the Julia compat bump. Mirror the resolution-order story in
  `scripts/setup_polecat_env.sh` (workspace checkout > pinned URL).

### F6 — `AGENTS.md §4` references `scripts/migrations/*` which no longer exists
- **Severity:** P2 · **Effort:** S
- **Files:** `AGENTS.md:96-118` (rules for `scripts/migrations/`); actual
  location is `scripts/_archive/migrations/`. `mdl-archive-migrations` (the
  tracking bead noted in §4) appears to have landed but the doc rewriting
  was not part of it.
- **Current state:** every CI/runtime ban in `AGENTS.md §4` keys off the
  wrong path; an enforcement check that grepped for
  `scripts/migrations/` would silently miss anything that survived the
  archive move. The file `scripts/_archive/README.md` already states the
  policy correctly, so two sources of truth now disagree.
- **Recommendation:** rewrite §4 to point at `scripts/_archive/`, link to
  its README, drop the "Archiving … is tracked separately" sentence.

### F7 — `docs/README.md` claims the renderer uses `scipy.solve_ivp` (stale post-mdl-5xp)
- **Severity:** P2 · **Effort:** S
- **Files:** `docs/README.md:13` (table row for
  `tools/render_example_plots.py`). Says "evaluates each example via the
  `parameter_sweep` path … or via `scipy.integrate.solve_ivp` (ODE
  models …)".
- **Current state:** mdl-5xp (commit `41fb39c`) routed every ODE
  integration through `earthsci_toolkit.simulation.simulate` and updated
  `AGENTS.md §3` accordingly. `docs/README.md` was not updated. Reads as
  the single-pathway-rule violation it no longer is.
- **Recommendation:** replace the offending phrase with
  "via the canonical Python ESS runner
  (`earthsci_toolkit.simulation.simulate`)". One-line fix.

### F8 — `lib/solar.esm` standard library is undocumented
- **Severity:** P3 · **Effort:** S
- **Files:** `lib/solar.esm` (205 LoC, `esm = "0.3.0"`); `README.md:34-37`,
  `docs/REPO_LAYOUT.md:7-15` (top-level layouts listing).
- **Current state:** neither the README nor the layout doc mention `lib/`;
  `lib/solar.esm` markets itself as "Standard-library solar-geometry
  subsystem … Includable via §4.7 reference; see
  docs/standard_library.md", but `docs/standard_library.md` does not
  exist. A user landing in this repo cold has no path to discover that the
  stdlib exists.
- **Recommendation:** (a) add `lib/` to the README and `REPO_LAYOUT.md`
  top-level listings with a one-line description; (b) either land
  `docs/standard_library.md` as a short index or fix the in-file pointer
  to the README.

### F9 — `lib/solar.esm` structural validation bug (mdl-pk3) still open
- **Severity:** P3 · **Effort:** S
- **Files:** referenced bead `mdl-pk3` (the only P3-priority bead currently
  open in this rig).
- **Current state:** validation fails on the `true_solar_time`
  addition/subtraction units check. Bead is unowned.
- **Recommendation:** dispatch to a polecat alongside any work that
  touches the stdlib (F8 is a natural pairing).

### F10 — Julia full-chemistry inline test still on the workflow (mdl-lvu pending soak)
- **Severity:** P2 · **Effort:** S (when soak window passes)
- **Files:** `.github/workflows/test-esm.yml:42-58` (Julia
  `julia-actions/julia-runtest@v1` runs `Pkg.test`, which walks
  `components/` including `geoschem_fullchem.esm`).
- **Current state:** documented as transitional — the Python gate is
  `continue-on-error: true` for ~7 days while the Julia full-chem leg
  remains the gate of record. mdl-lvu tracks the retirement (option
  (a) — env-var skip — preferred).
- **Recommendation:** track the soak end date (likely 2026-05-08); when
  reached, dispatch mdl-lvu and pair the Julia `continue-on-error` removal
  with the Python `continue-on-error: false` flip in the same PR.

### F11 — `mdl-jm8` deferred (fastjx 18-wavelength × 220-σ → function tables)
- **Severity:** P3 · **Effort:** L
- **Current state:** the only `deferred`-status bead in the rig. Blocks
  fastjx from evolving past its committed snapshot of σ rows; mdl-1yv
  (LSODA fullchem 24h) shares the same root cause class (tabular data
  inlined as constants, not function tables).
- **Recommendation:** hold deferred until ESS exposes the function-table
  schema that bead `esm-hid` is tracking; revisit on ESS bump (F1).

### F12 — `tools/diagnose_geoschem_oom.jl` lacks an exit policy
- **Severity:** P3 · **Effort:** S
- **Files:** `tools/diagnose_geoschem_oom.jl` (141 LoC, mdl-i5j diagnostic).
- **Current state:** documented as "DIAGNOSIS ONLY" but lives under
  `tools/` next to actively-invoked Python scripts. There is no `[ci]
  skip` or path-filter exclusion in `.github/workflows/*`. Would not run
  by default but a careless `julia tools/*.jl` from a developer would
  spin it up. The bead it was filed for (mdl-i5j root-cause) closed; the
  archaeology value is the comment block at the top, not the script
  itself.
- **Recommendation:** either (a) move into
  `scripts/_archive/diagnostics/` per the
  `scripts/_archive/README.md` policy or (b) demote to a docstring
  excerpt under `docs/` and delete. Avoids future "what is this for"
  drag.

### F13 — `Project.toml` test-extras pull a heavy MTK + Catalyst + ODEsolver stack into every Julia env
- **Severity:** P3 · **Effort:** M
- **Files:** `Project.toml:14-22` (extras), `:24` (test target).
- **Current state:** `Pkg.test` requires Tsit5, Rosenbrock, NonlinearSolve
  + MTK + Symbolics + DomainSets + Catalyst before it can compile. The
  shim itself only depends on ESS. Polecats running `julia --project=.`
  for a quick `load_esm` smoke test cold-precompile every one of those
  for no return.
- **Recommendation:** consider a `[targets.test]`-versus-fully-loaded
  split, or a `test/Project.toml` sub-environment so the shim's
  precompile path stays cheap. Low-leverage; only worth doing if the
  cold-start friction is biting other polecats.

### F14 — Workflow churn beads (`mdl-wfs-*`) account for 41/46 open issues
- **Severity:** P3 · **Effort:** N/A (process)
- **Current state:** the rig's open bead list is dominated by
  formula-step beads (`Scan merge queue`, `Mechanical rebase`,
  `Burn and respawn or loop`, …). These are workflow molecules — they
  are creating noise during routine listing and complicate "what is
  outstanding model work?" queries.
- **Recommendation:** filter convention. Either tag them
  `kind=workflow` (so `bd list --status=open --not-tag=workflow` is the
  default rig view) or close on completion via the formula
  runtime. Mayor- or witness-side concern, not a code change here.

### F15 — Inline-test count vs. equation count is shallow on the largest mechanism
- **Severity:** P3 · **Effort:** M (test-design effort, not code)
- **Coverage table:**

  | file | tests | assertions | scale |
  |---|---|---|---|
  | `geoschem_fullchem.esm` | 3 | 81 | 819 reactions / 272 species |
  | `superfast.esm` | 6 | 49 | 27 reactions |
  | `fastjx.esm` | 3 | 45 | 1 equation, 18 wavelengths |
  | `cloud_albedo.esm` | 10 | 15 | 4 vars |
  | `water.esm` | 11 | 30 | 3 eqs |
  | `droplet_growth.esm` | 7 | 38 | 9 eqs |
  | `aerosol_scavenging.esm` | 7 | 28 | 3 eqs |
  | `diameter_growth.esm` | 7 | 28 | 3 eqs |

- **Current state:** the largest mechanism is the most under-tested per
  reaction (3 tests / 819 reactions ≈ 0.4 %; superfast 6/27 ≈ 22 %).
  Aerosol files cover 9–10× more assertions per equation than the gas-phase
  ones.
- **Recommendation:** file a follow-up bead to mdl-mzp / mdl-1yv:
  add per-family canary tests (one per Troe/JPL/Arrhenius template) so a
  template regression surfaces immediately. Not urgent — mdl-1yv shows
  the integrator side is the current gate, not the assertion coverage.

---

## Top 10 priorities (ordered)

1. **F7** — fix `docs/README.md` stale claim (lies about the simulation
   pathway). One-line edit; high signal-to-noise. **P2 · S**
2. **F6** — rewrite `AGENTS.md §4` for `scripts/_archive/migrations/`.
   Two sources of truth disagree today. **P2 · S**
3. **F5** — pin `earthsci_toolkit` to a commit SHA in both workflows.
   Removes a class of "CI broke overnight, no commit landed" outages.
   **P2 · S**
4. **F4** — request a public `cse=False` kwarg on
   `earthsci_toolkit.simulate`; reduce the inline-test gate's
   `_build_cse_false_cache` to a single line. **P2 · S** (here) /
   **M** (upstream).
5. **F1** — sweep `.esm` files onto schema `0.4.0` so newer expressive
   sections are even available. **P2 · M**
6. **F10** — when soak window closes (~2026-05-08), dispatch mdl-lvu
   alongside the `continue-on-error` flip. **P2 · S**
7. **F3** — annotate every tolerance block with a rationale. Cheap,
   prevents drift. **P2 · S**
8. **F2** — extract Arrhenius templates from `superfast.esm`; gives
   esm_to_docs more to render and shrinks the file. **P2 · M**
9. **F8 + F9** — pair the `lib/` documentation surface fix with the
   mdl-pk3 unit-validation bug. Close two P3s in one polecat dispatch.
   **P3 · S**
10. **F12** — relocate `tools/diagnose_geoschem_oom.jl` into
    `scripts/_archive/diagnostics/`. Keeps `tools/` exclusively for
    actively-invoked tooling. **P3 · S**

F11/F13/F14/F15 are accepted backlog — surface again when their unblocking
preconditions land (ESS function-table schema, polecat cold-start
friction, mayor workflow-bead policy, integrator side of mdl-1yv).
