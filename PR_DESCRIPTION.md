# PR: `components/ocean/mom6` — the MOM6 stage-2 column physics

## Summary

Ports the MOM6 (Modular Ocean Model 6, `dev/ncar_260909 @301879336` as
built in CESM cesm3.0-alphabranch; reference run `C_JRA_t62_mom6_inst`)
stage-2 **column physics** from the EqESM project's `stage2/` lane into
the corpus, following the merged CICE port's conventions
(`components/cryosphere/cice/`, PR #37), the CISM port
(`components/cryosphere/cism/`), and the CMEPS port
(`components/coupler/cmeps/`): equations, tests, and every numeric value
are byte-identical to the EqESM sources (STRIP-COMPARE IDENTICAL —
metadata/descriptions stripped, import paths normalized; see the identity
check below). Files:

| file | contents |
|---|---|
| `mom6_eos.esm` | `WrightEOS` — the Wright 1997 full-range in-situ density rho(T,S,p) and its analytic first derivatives drho/dT, drho/dS (`MOM_EOS_Wright_full.F90`, as called by `KPP_compute_BLD`), the 15 fit coefficients bound by reference from the shared constant fragments — 15 tests / 45 assertions |
| `mom6_templates.esm` | the 27 MOM6 expression templates: the Wright EOS family (`wright_alpha0`, the shared `wright_poly` bivariate polynomial bound with the b- and c-coefficient sets for the p0/lambda sub-polynomials, `wright_density`, `wright_drho_dT/dS`, the 15 `wright_coeff_*` constant fragments, the `wright_rho` composition), `masked_pair_average` (the AGRID stress average; its consumer `mom6_surface_forcing.esm` is NOT part of this port), `linear_tfreeze`, `interface_entrainment`, `tridiagonal_residual`, `surface_mix`, `layer_content_change` |
| `mom6_kpp.esm` | `KPPBLD` (KPP_compute_BLD down to the pre-smoothing OBLdepth/kOBL: surface-layer means, the Wright EOS as three `wright_rho` applications, the interface/cell heights and hydrostatic `pRef` as ESD `integral`s, deltaBuoy/N2/N, w_s/Vt²/BulkRi, OBL_depth_low with the Monin-Obukhov limit) and `KPPCoefs` (cvmix_coeffs_kpp_low for the reference configuration) — 8 tests / 158 assertions |
| `mom6_kpp_templates.esm` | the 16 CVMix KPP law templates (LMD94 stability functions and coefficients, w_m/w_s, unresolved shear Vt² with the Danabasoglu Cv, bulk Richardson, shape function G(σ), the OBL-depth quadratic, the KPP_IS_ADDITIVE=False override) |
| `mom6_column_discretization.esm` | local ESD-format rules: the MOM6 layer/interface grid (layer/iface, N_LAYER=75/N_IFACE=76) and the two `column_nonuniform_1d` cumulative-integral rules imported by reference at a 9.7.7 renaming edge |
| `mom6_frazil.esm` | `FrazilFormation` — the per-layer in-situ pressure (a hydrostatic cumulative integral over the shared column rules), the LINEAR freezing-point law, the frazil scan branch law and the column heat requirement — 4 tests / 52 assertions |
| `mom6_bflux.esm` | `BoundaryFluxes` — the surface mass/heat/salt flux application in the surface layer, the penetrating-shortwave heating, the column budgets and residual — 4 tests / 28 assertions |
| `mom6_shortwave.esm` | `ShortwaveAbsorption` — the Beer-Lambert optical-depth integrals as ESD `integral`s, the per-band decay dT_k/pen_sw_rem, netPen, absorbed_total — 6 tests / 78 assertions |
| `mom6_sw_discretization.esm` | local ESD-format rule pair lowering the [band, layer]-integrand optical-depth integrals (heating and buoyancy paths) |
| `mom6_vertical_diffusion.esm` | `TridiagonalMixing` — the implicit vertical tracer diffusion as the PDE dT/dt = d/dz(Kd dT/dz), discretized by the ESD rule `varcoeff_face_laplacian_lev_flux_bc` (its lowering is exactly the MOM6 tridiagonal law), T and S carried separately — 3 tests / 56 assertions |
| `README.md` | the merged human-readable map (from the six stage2 lane READMEs: `README-mom6.md`, `README-mom6-kpp-integrals.md`, `README-mom6-frazil-bflux.md`, `README-mom6-shortwave.md`, `README-mom6-vertdiff.md`, `README-mom6-w2.md`) |

417 assertions total (45 + 158 + 52 + 28 + 78 + 56), 40 tests.  Every
expected value is a real dump row — step/cell/layer cited in the test
description (`stage1/dumps/mom6/mom6_eos.csv`, `mom6_kpp_obl.csv`,
`mom6_kpp.csv`, `mom6_kpp_wide.csv`, `mom6_sw_abs.csv`, `mom6_frazil.csv`,
`mom6_bflux.csv`, `mom6_diabatic_tri.csv` of the EqESM project).  The
`stage1/...` paths and `bugs.md` citations throughout refer to the EqESM
project repository (the instrumented CESM checkout and its centralized bug
list); the component README says so in place, as in the CICE/CISM/CMEPS
ports.

## Exclusions (per the task)

- **C-grid dynamics** (continuity / PGF / Coriolis / momentum) — still in
  review in the EqESM project; no ported file imports any of it.
- **`mom6_surface_forcing.esm`** (the surface-forcing import lane) — being
  pruned by the EqESM `pin-lint-prune` work.  No ported file imports it
  (its *reverse* dependency is the only link: it consumes
  `masked_pair_average` from `mom6_templates.esm`, which is carried here
  with the library; the template's description says its consumer is not
  part of this port).

## Placement

`components/ocean/mom6/` — the `<domain>/<component>` corpus pattern, in a
**new `ocean` domain**.  MOM6 is the CESM ocean component
(`components/mom/MOM6` in the CESM source tree); all ten files transcribe
column physics (equation of state, KPP boundary layer, shortwave
absorption, frazil, boundary fluxes, vertical tracer diffusion — none of
the existing science domains fit the lane as a whole), the direct analogue
of the CICE port keeping `cice_templates.esm` with its consumers, the CISM
port keeping its lane's files and ESD rules in one directory, and the
CMEPS port opening the `coupler` domain.  Splitting the files across
hypothetical atmosphere/cryosphere domains would duplicate the shared
template libraries.  The `components/` README and `couplings/` are not
touched (matching the CICE/CISM/CMEPS ports).

## Law reuse

Per the task rule, every law already upstream should be imported from
there, not duplicated.  A corpus-wide check found **no MOM6/ocean
components upstream** (`git ls-tree origin/main` has no mom6/ocean files
in `components/` or `lib/`), and a grep of all 47 template names and their
distinctive bodies against the whole corpus found no overlap (the Wright
EOS, the CVMix KPP laws, and the MOM6 tridiagonal/entrainment laws have no
upstream counterparts).  All 47 templates therefore ship in the two
template libraries and are imported by reference by the components;
nothing is duplicated between the ported files themselves.  The EOS
coefficient fragments are the single shared source of the fit values
(bound by reference by both `WrightEOS` and the `wright_rho` composition).

## Identity check (equations / tests / numbers byte-identical)

`tools/esm_strip_compare.py` (committed on the EqESM branch,
`wt/esm-pr-mom6` @ 251fc1a, from EqESM main) strips the top-level metadata
block and every nested `description`, normalizes import paths, and
compares the remaining JSON documents.  The only import-path change in
this lane: the bare `mom6_templates.esm` ref of
`mom6_vertical_diffusion.esm` became `./mom6_templates.esm` (corpus
relative-ref style; normalized with `--normalize`):

```
STRIP-COMPARE mom6_bflux.esm: IDENTICAL              STRIP-COMPARE mom6_kpp_templates.esm: IDENTICAL
STRIP-COMPARE mom6_column_discretization.esm: IDENTICAL  STRIP-COMPARE mom6_shortwave.esm: IDENTICAL
STRIP-COMPARE mom6_eos.esm: IDENTICAL                STRIP-COMPARE mom6_sw_discretization.esm: IDENTICAL
STRIP-COMPARE mom6_frazil.esm: IDENTICAL             STRIP-COMPARE mom6_templates.esm: IDENTICAL
STRIP-COMPARE mom6_kpp.esm: IDENTICAL                STRIP-COMPARE mom6_vertical_diffusion.esm: IDENTICAL
ALL IDENTICAL
```

The raw diffs vs `stage2/` are confined to: the metadata blocks (corpus
key order tags/created/authors/references, `created: 2026-11-12T00:00:00Z`,
authors ["EqESM project contributors"], the CESM + EarthSciModels
reference pair; the ESD-format files keep their `license: MIT` and their
stage2 specific references, per the CISM discretization-file precedent),
the description re-points of the stage2 README citations at `README.md`
(8 occurrences across 6 files, plus the `masked_pair_average` consumer
note), and the one ref normalization above.

## ESD dependencies

**None unmerged.**  All four `${ESD_ROOT}` imports are on
EarthSciDiscretizations **main**:

- `grids/column_nonuniform_1d/grid.esm` (only `column_cell_center`,
  `column_cell_thickness`),
- `grids/column_nonuniform_1d/rules/varcoeff_face_laplacian_lev_flux_bc.esm`,
- `grids/column_nonuniform_1d/rules/integral_lev_cumulative_from_bottom.esm`,
- `grids/column_nonuniform_1d/rules/integral_lev_nodes_cumulative_from_bottom.esm`.

The two local rule files are EarthSciDiscretizations-format and follow the
CISM port's `cism_velo_discretization.esm` conventions.  (One future ESD
generalization is documented in the files: the KPP surface-layer means are
integrals over an i-dependent interior depth bound `SLdepth(i)`, which the
`column_nonuniform_1d` rules do not match — they stay `faq` sums, exactly
as in the EqESM sources.)

## Pin-lint (refresh 2026-11-15)

`python3 tools/esm-pin-lint.py` (the EqESM project's current lint, with
the coord-window/ifelse false-positive fixes) on the ported directory
reports **20 findings (9 non-warning)** — down from the 35 (24 non-warning)
of the original port (the old count included lint false positives since
fixed, and the port's stale `wright_lambda` ≡ `wright_p0`
`duplicate-template`).  Every finding was triaged by the EqESM
`mom6-prune-esm` slice (disposition record: `stage2/README-mom6-prune-esm.md`
in the EqESM project); **no assertion was dropped** — all 31 flagged
assertions are real, failable tests:

- `override-copy` ×3 — the KPPCoefs pass-through `Kv_out = Kv_in` pins at
  the first restoration interface kwup+1: **branch-selection pins** of the
  `kpp_override_nonzero` else-branch.  They fail on an inverted ifelse
  condition, a shifted pass-through index, or a kwup off-by-one; the
  expected value equals the Kv_in element *because the law's else-branch
  is a pass-through*.  Kept one per row by the EqESM review trim
  (`21c28ad`), documented in `README-mom6.md`.
- `override-copy` + `zero-pin` ×4 — the bflux `heat_residual` pins: the
  column heat budget closure `dHeat_col = netHeat + penSW_total − leftover`
  across four independently computed terms at abs 1e-12 (the terms are
  O(0.01..0.1) degC·m, so any wrong law in the chain fails the pin).  The
  conservation pin the EqESM review kept when it dropped the
  `mass_residual`/`salt_residual`/`dMass_col`/`dSalt_col` pins (algebraic
  identities — `README-mom6-frazil-bflux.md`).  The lint flags it because
  the dumped `leftover` override (0.0) coincides with the expected value —
  a residual's reference value *is* zero.
- `zero-pin` ×4 tests — the frazil `supercooling` (×2 per test) and
  `fraz_col` pins: the **no-formation branch law** of the frazil scan.
  `supercooling = max(0, T_freeze − T_before)` is pinned on the two
  closest-to-freezing layers (T_before − T_freeze = 0.1753/0.1780 degC on
  the pinned layers) and `fraz_col = Σ hc·supercooling` at 0; they fail on
  a missing max clamp (the raw difference is −0.175), a freezing-point
  error beyond the margin, a wrong heat capacity, or any spurious
  supercooling.  The formation branch itself is a documented coverage gap
  (no traced column forms frazil).
- `zero-pin` ×3 tests — the vertdiff `tri_res_T/S` pins: the scaled
  residual of the implicit vertical-diffusion solve, pinned at the
  mixed-layer and bottom layers at abs tolerances scaled to each row's
  conditioning (1e-13..1e-8; measured residuals ≤ 1.4e-16).  The lane's
  check that the PDE discretization (the ESD
  `varcoeff_face_laplacian_lev_flux_bc` lowering) reproduces the MOM6
  tridiagonal solve — any operator/solve/ent error makes the residual
  nonzero (the convective row's terms are O(1) against abs 6e-9).  They
  are zero-valued *because the solve is consistent*, the property being
  asserted.
- `inline-repeat` ×2 — the KPPBLD `max(-(i,1),1)` index clamp and the
  KPPCoefs `and(>=(i,2), <=(i,kwup))` guard: documented false positives.
  The former is the F90's `max(k−1,1)` floor in index position, the latter
  the F90's `k >= 2 .and. k <= kwup` loop guard in the Kd_heat/Kd_salt/Kv
  ifelse conditions; index expressions and index-set predicates cannot be
  named intermediates in esm (and kwup is a test parameter, so the faq
  range cannot express the guard), and both mirror the F90 structure.
- `duplicate-template` ×1 — resolved by this refresh: the re-port copies
  the current EqESM stage-2 files, whose `wright_poly` refactor
  (`7cde108`) merged `wright_p0`/`wright_lambda` into the single shared
  polynomial template.  Same law, same numbers — 28 → 27 templates, no
  assertion changed.

## Runner results

### Rust CLI (`esm test components/ocean/mom6`, ESD_ROOT = ESD main content)

| binary | result |
|---|---|
| `$M/esm` (0.7.0) | **417P / 0F / 0E** |
| release v0.10.0 (`/scratch.local/ctessum/cism-upstream-prep/esm-cli-0.10.0-linux-x64/esm`; the `../EarthSciAST-v0.10.0` directory holds the release source, not a binary) | **417P / 0F / 0E** |
| esm 0.12.1 (EarthSciAST main — the binary the corpus's esm-2.0.0 migration used; re-verified on this refresh) | **417P / 0F / 0E** |

All three with `ESD_ROOT` = EarthSciDiscretizations main (fresh clone, as
the upstream CI sets it up).  The files declare esm 1.3.0 exactly as in
stage2; the esm-2.0.0 CLI accepts them (the removed ops — `fn
interp.*`/`datetime.*`, `aggregate` — do not occur in these files, so no
codemod was needed; the identity check preserves the version field).

`esm validate` passes on all ten files under both binaries; `esm units`
shows no `units_dimensionless_literal_mismatch` on any file under either
(the degC/ppt-carrying files inherit the informational "consider SI base
units" note from stage2 — degC and ppt are accepted unit strings in esm
1.3.0, documented in the README).

### Python inline gate (`tools/run_esm_inline_tests.py`)

**49P / 0F / 372E** — the 45 EOS assertions plus one per-file build pass
for the four no-test files (the same 1P-per-template-file convention the
CICE/CISM/CMEPS ports record).  Every E falls into one of the **two known
python-runner limitation classes** documented by the CICE and CISM ports
(all passing in the Rust runner):

| file | result | error class |
|---|---|---|
| mom6_eos.esm | 45P/0F/0E | — |
| mom6_column_discretization.esm, mom6_kpp_templates.esm, mom6_sw_discretization.esm, mom6_templates.esm | 1P/0F/0E each | — |
| mom6_bflux.esm | 0P/0F/28E | shaped `parameter_overrides` do not resolve in the flattened python system (`Unresolved symbol: 'BoundaryFluxes.T_before'`) |
| mom6_frazil.esm | 0P/0F/52E | same class (`Unresolved symbol: 'FrazilFormation.h'`) |
| mom6_shortwave.esm | 0P/0F/78E | same class (`Unresolved symbol: 'ShortwaveAbsorption.sw_pen_band'`) |
| mom6_kpp.esm | 0P/0F/158E | array-state handling: index-set size expressions / array indexing (`index 75 is out of bounds for axis 0 with size 75`) |
| mom6_vertical_diffusion.esm | 0P/0F/56E | same class (`index 76 is out of bounds for axis 0 with size 76`) |

Zero FAILs: unlike the CICE/CISM lanes there are no mounted-component
`variable_map` endpoints in this lane, so that limitation class does not
apply; the two classes above are exactly the ones the CICE PR
(`UPSTREAM-cice-pr.md`) documents.

## Notes

- `mom6_sw_discretization.esm` carries `"esm": "1.2.0"` exactly as in
  stage2 (the identity check does not strip the version field); 65
  upstream corpus files are at 1.2.0, so this is consistent with the
  corpus.
- The stage2 lane records the frazil/bflux cross-file consistency
  observation (the bflux `T_after` equals the vertdiff lane's `T_before`
  bitwise on all 156 rows, so the lanes compose without a gap), the
  `bugs.md` entry for the 1000× `I_Habs` inconsistency in
  `sumSWoverBands`' min_SW_heat clamp, and the documentation correction
  (Kd_heat ≠ Kd_salt on most interfaces — a README error in the EqESM
  project, not a CESM bug); all carried into the component README.
- No `Project.toml` change (nothing to declare; the Julia CI resolve
  staleness at HEAD is a pre-existing upstream issue documented by the
  CICE PR).
- Branch `mom6` was created from `origin/main` (`fc40c8c`); this PR is not
  pushed — the reviewer can pull the worktree branch or apply the two
  commits `d654eaa` + the refresh commit below.
- **Refresh 2026-11-15** (this commit): merged `origin/main`
  (through `d3cc087`, the esm-2.0.0 corpus migration and the Rust-CLI CI
  change) into `mom6`; re-ported the ten files from the EqESM stage-2 lane
  after its pin-lint triage and the `wright_poly` refactor (see Pin-lint);
  `tools/esm_strip_compare.py --normalize 'mom6_templates.esm=./mom6_templates.esm'`
  reports every file IDENTICAL.  The port remains byte-identical to the
  EqESM sources modulo metadata/descriptions/refs; no esm-2.0.0 codemod
  was needed for these files (verified: validate + 417P/0F/0E under the
  0.12.1 CLI with a fresh EarthSciDiscretizations-main `ESD_ROOT`, as the
  upstream CI runs).
