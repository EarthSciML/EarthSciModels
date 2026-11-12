# CICE sea-ice stage-2 components (dynamics/transport lowered on the ESD cice_bgrid rules)

Adds `components/cryosphere/cice/` — the CESM CICE sea-ice component
(`cesm3_cice6_6_3_22`) of the EqESM project's stage-2 corpus as esm 1.3.0
files: component structure, imports/exports, solver block, the pointwise
column/dynamics/transport laws of the default configuration transcribed
exactly, subcomponents, and the top-level assembly, with the `tests` blocks
pinning the stage-1 instrumentation dumps (`stage1/dumps/cice/`).

| File | Contents |
|---|---|
| `cice.esm` | Top-level assembly: mounts IceCap/Thermodynamics/Dynamics/Transport by reference, coupling `variable_map` edges (the 31 shape-mismatched edges carry faq full-map broadcast and single-cell select transforms), enums, solver block, first assembly test (1 test, 17 assertions) |
| `cice_coupling.esm` | `IceCap` — the nuopc cap: import/export unit conversions, the freezing-temperature law, the per-category albedo/heat/salt aggregation, the similarity atmo boundary layer (5-iteration unroll), the Rothrock strength law, the EVP stress pointwise laws and stepu ocean-ice stress partials (40 tests, 69 assertions) |
| `cice_shortwave.esm` | `Shortwave` — the delta-Eddington 3-band radiation scheme (`compute_dEdd_3bd` / `solution_dEdd`, icepack_shortwave.F90:1703-3488): layer geometry, SNICAR snow-IOP table lookup, per-layer tau/w0/g over the snow/bare/pond branches with bulk-aerosol mixing, ocean albedo, the delta-Eddington layer solution with the 8-point Gauss-Legendre diffuse angular integration, the fresnel refraction layer, the downward/upward layer-combination recurrences with the trmin cutoff, the interface flux fractions, and the band-weighted flux/absorption accumulations; the SNICAR and bulk-aerosol tables as `function_tables` (2 tests, 171 assertions) |
| `cice_thermodynamics.esm` | `Thermodynamics` — dEdd shortwave laws, the mushy enthalpy<->temperature inversions, surface energy-block fluxes, radiation rescale, surface-balance residual (17 tests, 30 assertions) |
| `cice_dynamics.esm` | `Dynamics` — the B-grid momentum balance and classic-EVP stress evolution, **lowered onto the ESD `cice_bgrid` rules** (`strain_rates_divu/tension/shear`, `stress_divergence_strintx/strinty`), Hibler strength, ocean-ice stress (1 test, 19 assertions) |
| `cice_transport.esm` | `Transport` — the horizontal continuity system, **lowered onto the ESD `cice_bgrid` `transport_flux_divergence` rule**, integrated over one coupling period (2 tests, 16 assertions) |
| `cice_templates.esm` | Expression-template library shared by the above (119 templates: shortwave, the dEdd family, mushy physics, atmo, mechred, EVP stress) |
| `README.md` | Configuration transcribed, file map, testing table, transcription divergences, the Fortran bugs found |

322 CICE assertions total (171 + 69 + 30 + 19 + 16 + 17). Every expected value is a
real dump row — step / cell / ncat cited in the test description.

## What changed since this PR was opened

- **Refreshed against current EqESM `stage2/`** (commits `7543f57` →
  `3758998`): the 31 shape-mismatched coupling edges (3×5 dynamics/transport →
  single-cell thermodynamics/coupling) now carry faq full-map broadcast and
  single-cell select transforms; `cice.esm` declares the `i/j/N_I/N_J` index
  sets and gained its first **assembly test** (17 assertions pinning the
  step-1 export-time state at the traced cell (3,5)); the assembly metadata
  description and README document both. Equations/tests/values re-verified
  **byte-identical** to `$M/stage2` (STRIP-COMPARE: metadata/descriptions
  stripped, 6/6 IDENTICAL). The stage2 literal-units form (esm-spec §4.8.6)
  is carried verbatim.
- **Merged `origin/main`** (14 commits: `data-fed-no-shape`, `data-param-defaults`,
  docs plot renderer, unit-consistency fixes, ...) — no conflicts.
- **ESD dependency resolved:** the companion EarthSciDiscretizations PR
  (cice_bgrid rules) merged as ESD PR #50; ESD `main` now ships
  `grids/cice_bgrid`, so this PR's CI is no longer blocked on the two lowered
  files.
- **Refreshed again (2026-11-11) against current EqESM `stage2/` and
  `origin/main`:** ported the EqESM cice-dedd work merged since `3758998`
  (`fca81f2` the 39-template dEdd family, `f72ea05` the dEdd template rework,
  `1299614` the new `cice_shortwave.esm` delta-Eddington component,
  `cb21ef3` the dEdd refactor merges/drops, `51bc2fc` the 18 unfailable-pin
  review drops) — `cice_shortwave.esm` is added as a 7th file (2 tests, 171
  assertions against `stage1/dumps/cice/cice_dedd.csv`) and
  `cice_templates.esm` grows 76 → 119 templates (all dEdd laws imported by
  reference by the new component). STRIP-COMPARE re-run on all 7 files:
  **7/7 IDENTICAL** to `$M/stage2` (metadata/descriptions stripped; the
  shortwave metadata keeps stage2's `license: MIT` and adds the port
  tags/created/authors/references block). Merged `origin/main` again (4
  commits: `data-param-defaults-all`, `interp-templates`) — no conflicts,
  nothing touching `components/cryosphere/cice`.
- **Refreshed again (2026-11-12) against current EqESM `stage2/`** (the
  janitor-1110 review round, EqESM `7af940c`, plus the
  `wt/cice-shortwave-cleanup` review follow-ups, EqESM `f6aacc4`):
  `cice_shortwave.esm` and `cice_templates.esm` re-ported from the final
  branch. What changed vs. the previous port: the Sabs/Iabs layer/interface
  absorptions are now written as differences of the already-computed net
  flux profile (`flux[k_top] − flux[k_bottom]`, matching icepack's
  `fthru`/`Sswabs`/`Iswabs`), so the `dEdd_band_absorption` template is
  deleted; the fresnel reflectivity-from-above law is deduplicated into one
  template `dEdd_fresnel_refl_above` applied to both the direct beam and
  diffuse radiation from above (`dEdd_fresnel_rdir` and
  `dEdd_fresnel_rdif_a` deleted; `dEdd_fresnel_rdif_b` kept — its body
  genuinely differs: the layer's own reflectivity is the direct term).
  STRIP-COMPARE on the two re-ported files: **2/2 IDENTICAL** to `$M/stage2`
  (metadata/descriptions stripped per the port conventions); the other five
  files unchanged (6/7 IDENTICAL overall — `cice_transport.esm` is the one
  remaining stale file, its tracer-transport3 rework
  (`tracer_flux_divergence` template form) belongs to the queued
  `cice-transport` lane and will be re-ported with it).

## Cross-runner status (EarthSciAST `main`; ESD_ROOT = ESD `main`, which now has `cice_bgrid`)

| Runner | Result |
|---|---|
| **rust** (`esm test components/cryosphere/cice`, binary 0.7.0 — EqESM main's `./esm`) | **322P / 0F / 0E** (shortwave 171 + assembly 17 + coupling 69 + thermodynamics 30 + dynamics 19 + transport 16) — re-run on the refreshed files |
| **rust** (`esm test components/cryosphere/cice`, release binary 0.10.0) | **322P / 0F / 0E** — `esm validate` also passes on all 7 files under 0.10.0 (its new load-time checks — observed cycles, stdlib template refs — do not affect this component) |
| **python** (inline gate, `earthsci_ast` 0.10.0 + scipy 1.18.1) | 41P / 0F / 282E — identical to the previous port's numbers (the 0.8.0 measurement); every error is the runner bug below (the assembly's 17E are its faq-select forms: `index 3 is out of bounds for axis 1 with size 3`; the shortwave 171E are `Unresolved symbol: 'Shortwave.rsnw'` — the lev/snow-layer-shaped `parameter_overrides` dropped by the runner's scalar `p` channel, same bug). Note: EarthSciAST `main`'s python toolkit (0.2.0/0.3.1) and the CI venv can no longer even **load** the file (`removed_op at /function_tables`: the block was removed at esm 2.0.0), so the gate numbers above come from the 0.10.0 release venv (`esd-rel05-venv-0.10.0` + scipy) |

`esm validate` passes on all 6 files (with `ESD_ROOT` exported).

## Python runner bug (blocking the python gate; not a file issue)

The python gate fails on **all** CICE files, including the three that never
touch ESD, with an internal error class — the document below reproduces it
(1 model, 1 shaped parameter, 1 faq-index equation, 1 test with an array
override):

```json
{"esm": "1.3.0", "metadata": {"name": "p_probe"},
 "index_sets": {"ncat": {"kind": "interval", "size": 5}},
 "models": {"M": {"variables": {
   "aicen": {"type": "parameter", "shape": ["ncat"], "units": "1", "default": 0.0},
   "aice": {"type": "unknown", "units": "1", "default": 0.0}},
  "equations": [{"lhs": "aice", "rhs": {"op": "faq", "output_idx": [], "reduce": "+",
    "ranges": {"ncat": {"from": "ncat"}},
    "expr": {"op": "index", "args": ["aicen", "ncat"]}, "args": ["aicen"]}}],
  "tests": [{"id": "t1", "time_span": {"start": 0.0, "end": 0.0},
    "parameter_overrides": {"aicen": [0.1, 0.2, 0.3, 0.4, 0.5]},
    "assertions": [{"variable": "aice", "time": 0.0, "expected": 1.5}]}]}}}
```

- **rust** (`esm test`): 1/1 PASS (the §6.6.2 shaped override broadcasts).
- **python** (`earthsci_ast` 0.8.0): `solve failed: Unresolved symbol:
  'M.aicen'`.

Root cause: `inline_tests.simulate_states` routes a test's
`parameter_overrides` through `esm_problem(p=...)`, whose `p` channel only
carries scalars — an array value for a shaped parameter (§6.6.2) is dropped
(verified: the build's `param_values`/`input_arrays` never see it; the array
channel is `const_arrays`, which the runner never feeds). Consequences on the
CICE files: every coupling test errors at solve (`Unresolved symbol` /
`index applied to scalar value` — 69E), and every §6.6.5 array-state/observed
assertion errors (`array state 'zTin' has no cells in var_map` — 7E in
thermodynamics; the observed-replay context additionally omits the
`input_arrays` channel, so observeds reading shaped parameters are dropped by
`skip_unresolved`). The new assembly test errors the same way — the
broadcast/select faq forms (`index 3 is out of bounds for axis 1 with size 3`,
17E) are the runner's shaped-index handling on the traced-cell constants. The
new shortwave file's 171E are the same class: its two tests override the
snow-layer/lev-shaped arrays `rsnw`/`dzk`/`frsnw`/`aero_mp` etc. (§6.6.2),
which the runner drops (`Unresolved symbol: 'Shortwave.rsnw'`). The
same constructs are blessed by this repo's own conformance tests
(`shaped_parameter_broadcast`, `shaped_parameter_const_arrays`) and by the
corpus (`slab.esm` uses the identical faq form).

## Notes

- **RangeSpec workaround retained:** the lowered components declare the
  `N_I/N_J/NCAT` metaparameters and `i/j/corner/ncat` index sets locally and
  import the ESD rules by reference **without** bindings. The esm CLI
  0.4.0/0.6.0 rejects a faq range bound to a metaparameter reference when a
  template library is imported with bindings (a RangeSpec round-trip parse
  bug, tracked in the EqESM project). The workaround is transparent to the
  rules' behavior and is what lets the files run on current CLIs; removing it
  is an EarthSciAST-side fix.
- **No Project.toml change in this PR.** Upstream's `[compat] EarthSciAST =
  "0.3"` is stale against the Julia package's current version on `main`, so
  the Julia CI resolve step fails at HEAD for every PR (the same failure mode
  the file's own comment documents). PR #33 carries its own bump; this PR
  avoids the conflict and documents the finding instead.
- The `stage1/...` paths and `bugs.md` citations throughout refer to the
  EqESM project repository (the instrumented CESM checkout and its
  centralized bug list); the README says so in place.
