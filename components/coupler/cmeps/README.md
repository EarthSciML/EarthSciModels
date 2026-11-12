# CMEPS stage 2 — bulk flux, ocean albedo, and fraction-weighted merge laws

Stage-2 implementation of the CMEPS (Coupled Mediator for Earth System
Prediction) pointwise laws as esm 1.3.0 files: the expression-template
library, the `AoFlux` component transcribing the atmosphere–ocean bulk flux
computation (the Large & Pond / Large & Yeager scheme of
`flux_atmocn/flux_atmocn_Large.F90` in the cesm3.0-alphabranch checkout
`stage1/cesm/components/cmeps/cesm/`), the `OcnAlb` ocean-albedo component
(`mediator/med_phases_ocnalb_mod.F90` with `share/src/shr_orb_mod.F90`), and
the `OcnMerge`/`AtmMerge` fraction-weighted export-merge components
(`mediator/med_phases_prep_ocn_mod.F90` / `med_phases_prep_atm_mod.F90` with
`med_merge_mod.F90` and `esmFldsExchange_cesm_mod.F90`). The `tests` blocks
pin the stage-1 instrumentation dumps: `stage1/dumps/cmeps/cmeps_aoflux.csv`
(288 rows = 12 PET-0 ocean cells × 24 coupling steps of the `C_JRA_t62`
DATM+MOM6 run) and `cmeps_aoflux_wide.csv` (192 rows, dynamic wind-ranked
selection), `cmeps_ocnalb.csv` / `cmeps_merge.csv` (288 rows each, same 12
cells × 24 steps), and `cmeps_prep_atm.csv` (432 rows = 36 traced atm cells ×
12 coupling steps of the `F2000climo_f19_inst` CAM6+CLM+CICE+DOCN+MOSART
run). See [Testing](#testing).

All model logic lives in `.esm` files; this README is the human-readable map.
Sources: `stage1/cesm/components/cmeps/cesm/flux_atmocn/flux_atmocn_Large.F90`
(the traced scheme), `stage1/cesm/share/src/shr_wv_sat_mod.F90`
(`shr_wv_sat_qsat_liquid` / `shr_wv_sat_svp_to_qsat` / `GoffGratch_svp_liquid`),
`stage1/cesm/components/cmeps/mediator/med_phases_aofluxes_mod.F90` (the
`add_gusts` / `minwind` / `seq_flux_atmocn_minwind` configuration), the run
records in `stage1/runs/cmeps_instrument.json` / `stage1/runs/CMEPS_LANE.md`,
and the two lane READMEs this document merges (the atmosphere–ocean flux
lane and the ocnalb/merge + prep_atm lanes).

Configuration transcribed (the `C_JRA_t62` run's `nuopc.runconfig`):
`ocn_surface_flux_scheme = 0` (flux_atmOcn_large), `add_gusts = .false.`,
`coldair_outbreak_mod = .false.`, `aofluxes_use_shr_wv_sat = .true.` (the
shr_wv_sat Goff & Gratch path; `wv_sat_use_tables = .false.` in the traced run,
so the analytic form is used, not the lookup table), `flux_convergence = 0.01`,
`flux_max_iteration = 5`, `minwind = 0.5` m/s.

## File map

| File | Contents | Fortran source |
|---|---|---|
| `cmeps_templates.esm` | Expression-template library (14 templates): the Goff & Gratch (1946) liquid-water saturation vapor pressure (`shr_wv_sat_mod.F90:942-956`) and the epsilo·es/(p−omeps·es) saturation-humidity conversion with the p ≤ es guard (`F90:351-363`), the Large & Yeager (2009) neutral 10-m drag coefficient cdn(U) = 0.0027/min(33,U) + 0.000142 + 0.0000764·min(33,U) − 3.14807e-13·min(33,U)⁶ (`flux_atmocn_Large.F90:153-154`), the Paulson (1970) unstable psimhu/psixhu (`F90:163-164`), the shared stable-flag blend `stable_blend(stable, stable_value, unstable_value) = stable·stable_value + (1−stable)·unstable_value` (`F90:238, 258-259`) used by the combined stable/unstable psi_m/psi_h (`F90:258-259`) and the neutral heat coefficient (`F90:238`), the Monin-Obukhov stability parameter (unclamped, with karman/g/zvir as named parameters, `F90:252-253`) and its sign-preserving |hol| ≤ 10 clamp `stability_parameter_clamp` (`F90:254`), the exchange-coefficient height shift c/(1 + c/karman·(alz − psi)) (`F90:282-284`) and its clamped variant with max(..., −0.5) used for the wind-speed shift (`F90:272`) — both with karman as a named parameter, and the frozen-state selection (input-state pinning for the composed iteration) | `flux_atmocn_Large.F90`, `shr_wv_sat_mod.F90` |
| `cmeps_aoflux_step.esm` | Model `AoFluxStep` — ONE pass of the stability do-while (`F90:242-290`), authored once and mounted 6× by reference (models.step1..step5 + exit of `cmeps_aoflux.esm`): 22 equations = the 17 update states (hol_raw, the unclamped Monin-Obukhov parameter of `F90:252-253`; hol = stability_parameter_clamp(hol_raw), the |hol| ≤ 10 clamp of `F90:254`; stable, xsq, xqq, psimh, psixh, the clamped wind-shift rdw, u10n, rdn, rhn, rd, rh, re, ustar, tstar, qstar), the per-update convergence flag conv = |(ustar − ustar_prev)/ustar| ≤ 0.01, and 4 frozen-state fields pinning the INPUT state of the first-converged update (ustar_prev/tstar_prev/qstar_prev/rdn_prev, via the `frozen_state_select` template); 20 parameters = the 7 fixed pointwise fields (vmag, delt, delq, alz, zbot, thbot, qbot) + ren, the CESM constants karman/g/zvir (defaults, not coupled — the ren precedent), the previous state (ustar_prev, tstar_prev, qstar_prev, rdn_prev), conv_prev, and the 4 frozen threading inputs | `flux_atmocn_Large.F90` |
| `cmeps_aoflux.esm` | Model `AoFlux` — the full pointwise chain, composed: 59 equations = the 12 raw inputs; the derived inputs du/dv (the relative-wind components), vmag (minwind-clamped relative wind), wind0 = vmag (the resolved wind of `F90:204`; with add_gusts = .false. the Fortran computes it identically to vmag, so the alias is exact), esat_raw/esat (the min(es, pslv) cap), qsat (from the RAW es, as shr_wv_sat_qsat_liquid calls svp_to_qsat before the cap), ssq = 0.98·qsat, delt, delq, alz, al2, cp (with the CESM constants cpdair/cpvir/latvap/stebol/karman declared once as named parameters); the neutral first estimates stable0/rdn0/rhn0/ren0/ustar0/tstar0/qstar0 (`F90:236-244`); the convergence representation conv_1..4 = step1..4.conv and iter = first converged k, else 5; the 16 exit-state fields = the 15 exit.* fields + ren (the iteration of `F90:242-290` is reproduced by the 6 top-level mounts of `./cmeps_aoflux_step.esm` chained by 86 variable_map couplings: ustar0/tstar0/qstar0/rdn0 seed step1, each step's state/conv/frozen-input fields feed the next, the 7 fixed fields feed every step; the 6th mount exit is fed step5's 4 pinned input-state fields + the 7 fixed fields and recomputes the 15 exit-state fields — the exit state of the first-converged update k is a deterministic function of the pre-converged state (update k−1 outputs) plus the fixed fields); the 7 fluxes (`F90:299-311`); the 10 diagnostics (`F90:316-333`) | `flux_atmocn_Large.F90` |
| `cmeps_ocnalb.esm` | Model `OcnAlb` — the solar geometry of the ocean-albedo phase (`med_phases_ocnalb_run`): earth_true_longitude / solar_declination / earth_sun_distance_factor (the Berger 1978 mean-longitude series of `shr_orb_decl`, `shr_orb_mod.F90:736-814`, ve = 80.5, dayspy = 365) and solar_zenith_cosine (`shr_orb_cosz` F90:110-159, the no-dt_avg branch), plus the Briegleb et al. (1986) direct-albedo law with its cubic correction term and the `ocean_albedo_scheme` selection / `ocean_albedo_visible` / `ocean_albedo_nearinfrared` laws of F90:453-518 (the flux_albav, use_min_albedo, Taylor-scheme and dark-side branches transcribed but unpinned) — 7 equations, 9 tests / 36 assertions | `mediator/med_phases_ocnalb_mod.F90`, `share/src/shr_orb_mod.F90` |
| `cmeps_merge.esm` | Model `OcnMerge` — the ocn-export merges of `med_phases_prep_ocn_run` (`med_phases_prep_ocn_mod.F90`): the four scaled fractions (F90:800-813, `scaled_fraction`), the fraction-weighted merges of the rain/snow/lwdn/shortwave/aoflux/ice/runoff fields onto the ocean grid (`fraction_weighted_sum` of `med_merge_mod.F90:405-412` with the `esmFldsExchange_cesm_mod.F90` weights, `open_ocean_weighted_sum` for the two-source merges sharing the open-ocean weight), the absorbed-shortwave computation `ocean_absorbed_shortwave` (shared by fswabsv/fswabsi) and the c1..c4 `shortwave_band` split (F90:830-834; the float32-promoted literals 0.2849999964237213 / 0.2150000035762787 pinned by every traced row) — 23 equations, 9 tests / 135 assertions | `mediator/med_phases_prep_ocn_mod.F90`, `med_merge_mod.F90`, `esmFldsExchange_cesm_mod.F90` |
| `cmeps_prep_atm.esm` | Model `AtmMerge` — the atm-export merges of `med_phases_prep_atm_mod.F90:156-166` (`med_merge_mod.F90:405-412` with the `esmFldsExchange_cesm_mod.F90` weights): all 14 three-source exports as `fraction_weighted_sum` composed twice in the Fortran term order `((Sl·lfrac + Si·ifrac) + So·ofrac)`, plus the `So_t` copy export — 15 equations, 5 tests / 70 assertions | `mediator/med_phases_prep_atm_mod.F90`, `med_merge_mod.F90`, `esmFldsExchange_cesm_mod.F90` |

The `ren = 0.0346` water coefficient is constant across the iteration and is
carried once (`ren0`, the final `ren`, and each AoFluxStep mount's `ren`
parameter bind the same 0.0346 value; the parameter is not coupled). The same
"declare once, not coupled" pattern carries the other CESM constants:
`AoFlux` declares karman = 0.4, cpdair = 1004.64 J/kg/K, cpvir = 1810/1004.64 − 1,
latvap = 2.501e6 J/kg and stebol = 5.67e-8 W/m²/K⁴ as named parameters used by
the cp/lat/lwup/evap/fac_t/fac_q equations, and each AoFluxStep mount declares
karman/g/zvir (the stability-parameter constants) as parameters with the same
defaults; none are coupled (shr_const_mod.F90:22, 32, 46, 48, 52, 21, 31).

## Units

All fields are SI; temperatures are Kelvin; humidity kg/kg (the unit checker's
algebra treats kg/kg as dimensionless, which is how qsat/ssq/delt/… close);
stresses N/m²; fluxes W/m²; water flux kg/m²/s.

| Quantity | Symbols | Units |
|---|---|---|
| Heights / pressures | `zbot`, `ztref`/`zref`, `pslv`, `esat`, `esat_raw` | m; Pa |
| Atmosphere state | `ubot`, `vbot`, `us`, `vs`, `vmag`, `wind0`, `ugust`, `u10n`, `u10res`, `duu10n` | m/s; m²/s² |
| Temperatures | `thbot`, `tbot`, `ts`, `delt`, `tstar`, `tref` | K |
| Humidity | `qbot`, `qsat`, `ssq`, `delq`, `qstar`, `qref` | kg/kg (dimensionless in the checker) |
| Coefficients | `rdn`, `rhn`, `ren`, `rd`, `rh`, `re`, `rdw`, `stable`, `stable0` | 1 |
| Stability | `hol`, `hol2`, `xsq`, `xqq`, `xsq2`, `xqq2`, `psimh`, `psixh`, `psix2`, `fac_t`, `fac_q` | 1 |
| Fluxes | `tau`, `taux`, `tauy`; `sen`, `lat`, `lwup`; `evap` | N/m²; W/m²; kg/m²/s |
| Constants | `minwind = 0.5` m/s, `zref = 10` m, `ztref = 2` m, `karman = 0.4`, `grav = 9.80616` m/s², `cpdair = 1004.64` J/kg/K, `cpvir = 1810/1004.64 − 1`, `latvap = 2.501e6` J/kg, `stebol = 5.67e-8` W/m²/K⁴, `zvir = 28.966/18.016 − 1`, `epsilo = 18.016/28.966`, `omeps = 1 − epsilo`, `tboil = 373.16` K (Goff & Gratch) | (shr_const_mod.F90; the nuopc-cap values the run uses) |

**Unit notes**

- The `tref` potential-to-actual correction `0.01·ztref` (F90:323) is a lapse
  rate: the 0.01 is declared `K/m`, so `0.01 [K/m]·2 [m] = 0.02 K` closes.
- The Goff & Gratch formula evaluates in hPa and the trailing `×100` converts
  to Pa; in the unit algebra the 100 is declared `Pa` (the dimensionless 10^()
  factor multiplies it), per the template description.
- The empirical cdn coefficients carry the SI dimensions that make each term
  dimensionless (0.0027 [m/s], 0.0000764 [s/m], 3.14807e-13 [s⁶/m⁶]) — the
  template closes as a dimensionless coefficient.
- `sign(0.5, x)` (the Fortran two-argument sign) is emulated as the 0/1
  selection `ifelse(x >= 0, 1, 0)` for both `stable0` (F90:237, on delt) and
  the per-iteration `stable` (F90:255, on hol); the sign-preserving |hol| ≤ 10
  clamp of F90:254 is transcribed as `stability_parameter_clamp` =
  `sign(hol_raw)·min(|hol_raw|,10)` (the unary esm sign returns ±1, and 0 at
  hol_raw = 0 where 0·min = 0 anyway), which coincides bit-identically with the
  conditional `ifelse(hol_raw >= 0, min(|hol_raw|,10), −min(|hol_raw|,10))` on
  every value.

## Pointwise laws — Fortran vs esm transcription notes

| Law | Fortran | esm |
|---|---|---|
| Relative wind | `du = ubot−us`, `dv = vbot−vs` (F90:193) | `du`/`dv` equations |
| Wind magnitude | `vmag = max(minwind, sqrt(du² + dv²))` (F90:193-196; no gusts) | `max(sqrt(du² + dv²), 0.5 m/s)` |
| Saturation vapor pressure | `es = 10^(−7.90298·(tboil/t−1) + 5.02808·log10(tboil/t) − 1.3816e-7·(10^(11.344·(1−t/tboil))−1) + 8.1328e-3·(10^(−3.49149·(tboil/t−1))−1) + log10(1013.246))·100` (shr_wv_sat_mod.F90:942-956) | `goff_gratch_liquid_svp(ts)` template; `esat = min(esat_raw, pslv)` at the call site |
| Saturation humidity | `qs = epsilo·es/(p − omeps·es)`, `qs = 1` when `p ≤ es` (F90:351-363) | `svp_to_qsat(esat_raw, pslv)` — bound to the RAW es (the Fortran caps es AFTER computing qsat, F90:439-441) |
| Stability parameter | `hol = karman·g·zbot·(tstar/thbot + qstar/(1/zvir + qbot))/ustar²`, then `hol = sign(min(|hol|,10), hol)` (F90:252-254) | `stability_parameter(ustar, tstar, qstar, thbot, qbot, zbot, karman, g, zvir)` (unclamped) + `stability_parameter_clamp(hol_raw)` templates |
| Stability functions | `psimh = −5·hol·stable + (1−stable)·psimhu(xqq)`, xqq = sqrt(sqrt(|1−16·hol|)) (F90:256-259) | `psi_momentum` / `psi_scalar` templates over the shared `stable_blend(stable, −5·hol, psi_unstable)` template (also used by `neutral_heat_coefficient`) |
| Wind-speed shift | `rd = rdn/(1 + max(rdn/karman·(alz−psimh), −0.5))`; `u10n = vmag·rd/rdn` (F90:272-273) | `exchange_coefficient_shift_clamped` (momentum only, wind-shift step only) |
| Coefficient shift | `rd/rh/re = c/(1 + c/karman·(alz−psi))` (F90:282-284) | `exchange_coefficient_shift` |
| Fluxes | `tau = rbot·ustar²`; `taux/tauy = tau·du/vmag` etc.; `sen = cp·tau·tstar/ustar`; `lat = latvap·tau·qstar/ustar`; `lwup = −stebol·ts⁴`; `evap = lat/latvap` (F90:299-311) | identical |
| 2-m diagnostics | `hol2 = hol·ztref/zbot`; `psix2` at (hol2, stable, xqq2); `tref = thbot − delt·(rh/karman)·(alz+al2−psixh+psix2) − 0.01·ztref`; `qref = qbot − delq·(re/karman)·(…)`; `duu10n = u10n²`; `u10res = u10n·wind0/vmag` (F90:316-333) | identical (`al2 = ln(zref/ztref)` as its own equation, consumed by `fac_t`/`fac_q`); the diagnostics consume the exit-state rh/re/psimh/psixh/stable, exactly as the Fortran leaves them after the do-while |

## Documented divergences (all annotated in file metadata)

1. **Iteration unrolled and exit-selected, composed by reference.** The
   Fortran do-while of F90:242-290 runs until |(ustar − ustar_prev)/ustar| ≤
   flux_convergence (checked after each update, at most flux_max_iteration =
   5). esm 1.3.0 has no loop construct, so the 16-equation update law is
   authored ONCE in the one-step model `AoFluxStep` (`cmeps_aoflux_step.esm`)
   and mounted six times by reference in `AoFlux` as top-level models
   step1..step5 + exit (esm-spec §4.7), chained by 86 variable_map couplings.
   Each mount threads the previous state (ustar/tstar/qstar/rdn), the previous
   convergence flag, and 4 frozen-state fields that pin the INPUT state of the
   FIRST-converged update (ustar_prev/tstar_prev/qstar_prev/rdn_prev, via
   `frozen_state_select` in `cmeps_templates.esm`): the Fortran exits at the
   first passing update k, leaving the update-k exit-state fields, which are
   deterministic functions of the PRE-converged state (the update k−1 outputs)
   plus the fixed fields — and the iteration states do not repeat after
   convergence (ustar_2 differs from ustar_4 at the 1.8e-4 level on the pinned
   rows), so the input state must be carried forward through the remaining
   mounts. The 6th mount `exit` is fed step5's 4 pinned fields + the 7 fixed
   fields (conv_prev stays at its 0 default, so the frozen selection inside it
   is the identity) and its 16 fresh unknowns ARE the exit state; the parent
   aliases the 15 exit-state fields from `exit.*` (all except the intermediates
   hol_raw/rdw and the unused conv), which coincide bit-identically with the
   values the Fortran leaves in the iteration variables. The parent exposes
   the same external names as the pre-refactor unrolled model, so the pinned
   tests are unchanged: `conv_1..4 = step1..4.conv`, `iter` = the first
   converged k, else 5, and the 16 exit-state fields = the 15 `exit.*` fields
   + ren. The all-5-iterations case keeps conv_prev = 0 throughout, so the
   frozen inputs are the fresh 4th-update values, which the exit mount passes
   through the update law to produce the 5th-update values — exactly what the
   do-while leaves in the iteration variables after its final pass. The
   stage-1 replay (`stage1/analysis/validate_cmeps_dump.py`) mirrors this
   exact structure and reproduces the dumped `iter` and exit state on all 288
   rows, so the representation is pinned, not just the laws.
   - **Why top-level mounts and not subsystems.** The pinned CLI (esm 0.7.0)
     silently drops variable_map couplings whose targets live under
     `subsystems` in the single-top-level-model build path
     (`build_array_compiled` builds via `from_file` when the document has one
     top-level model and applies couplings only when flattening documents
     with several top-level models). Probes in `scratch/` confirmed the §4.7
     top-level form works (`probe_toplevel.esm`, 8/8) while the subsystem form
     leaves values at their defaults.
   - **Why not a coupled recurrence.** A direct coupled-recurrence formulation
     (each update referencing the previous update through the mount boundary)
     trips the §4.9.6 cycle rule; the CLI reports: `Observed dependency cycle:
     x -> y -> x. Each of these observed variables is defined in terms of the
     next, so no evaluation order satisfies every definition (esm-spec
     §4.9.6). Break the cycle by splitting one observed into a pre-value and a
     post-value.` The step model therefore splits every chained state into a
     pre-value parameter (x_prev) and a post-value unknown (x) — precisely the
     split the rule prescribes. `scratch/recur_probe2.esm` is the minimal
     failing probe (a single-variable recurrence, `scratch/recur_probe.esm`,
     passes 4/4, but the coupled multi-variable form does not).
2. **rainc unused.** With `add_gusts = .false.` the physics never reads rainc;
   the stage-1 dump sanitizes it to 0 after the mediator's 1-element dummy
   allocation was exposed as an out-of-bounds read (bugs.md #28). The
   gustiness law `ugust(min(rainc, 6.94444e-4))` of F90:197-202 is not
   transcribed (no dump coverage); `ugust = 0` is a plain equation.
3. **Coverage limits.** The fixed-window dump (288 rows) is entirely unstable
   Antarctic-coast cells with low-to-moderate wind, so the stable branch
   (stable0 = 1, the `rhn = 0.018` ratio, the −5·hol stable psi of F90:258-259)
   and the cdn 33 m/s wind cap carried no dump pins. The wide dump
   (`cmeps_aoflux_wide.csv`, dynamic selection: the per-step top-8 strongest
   wind cells and top-8 delt > 0 cells of ALL masked PET-0 cells) then
   PROVABLY exhausts the run's domain: its 192 rows are the strongest-wind rows
   the run offers (vmag max 4.81 m/s, still far below the cap; iter 2/3/4) and
   the stable selection is empty every step — no cell of PET 0 has delt > 0 in
   this January window. So the stable-branch and cdn laws remain transcribed
   but unpinned (they are exercised by construction only in the
   psi_momentum/psi_scalar and neutral_heat_coefficient branches); closing the
   gap needs a different window (a PET slice or season with warm-air-over-
   cold-water cells and/or storm-force winds), and the gustiness and
   cold-air-outbreak paths are namelist-off in this case (not run, documented).
   The minwind = 0.5 m/s floor and the |hol| ≤ 10 clamp ARE pinned (rows with
   vmag = 0.5 and hol = −10).
4. **esat vs qsat ordering.** The dump's `esat` column is the capped
   min(es_raw, pslv) while `qsat` is computed from the uncapped es_raw — the
   model carries both (`esat_raw` internal, `esat` capped output); the two
   coincide in the traced rows (es ≈ 700 Pa ≪ pslv ≈ 99.8 kPa), so the cap is
   not exercised.

## Testing

The stage-2 `tests` block pins the stage-1 instrumentation dumps
(`stage1/dumps/cmeps/cmeps_aoflux.csv` fixed window and
`cmeps_aoflux_wide.csv` dynamic window) with instantaneous laws
(`time_span {0,0}`, MOSART pattern): 9 tests × 52 assertions = 468 assertions,
all `rel 1e-12`, byte-identical to the pre-refactor unrolled model (the
composition keeps the same external variable names). The full stage-2 suite —
`./esm test stage2/` — reports 1327P/0F/0E (468 aoflux + 859 CICE/MOSART/other
files); this component needs no `ESD_ROOT`.

| test | dump row (step, gid) | what is pinned |
|---|---|---|
| `iter2_typical_unstable` | (1, 41583) | the full chain at the typical traced state: convergence at iteration 2 (145/288 rows), vmag 2.72 m/s, hol −1.84; all 47 dumped columns + conv_1..4 + iter |
| `iter3_cold_cell` | (1, 42662) | the coldest traced cell: convergence at iteration 3, vmag 1.33 m/s, hol −4.12 |
| `iter4_cold_cell` | (3, 42662) | convergence at iteration 4, vmag 0.80 m/s, hol −7.20 (approaching the clamp) |
| `iter5_hol_clamp` | (8, 42662) | all 5 iterations run (no convergence) with hol pinned at the |hol| ≤ 10 clamp (−10.0 exactly), vmag 0.52 m/s near the minwind floor |
| `iter5_minwind_clamp` | (22, 42662) | all 5 iterations run with vmag pinned at the minwind = 0.5 m/s floor while hol = −9.76 stays just off the clamp |
| `iter2_late_step` | (24, 41583) | the same cell as the first test 23 coupling steps later (convergence at iteration 2 again, vmag 2.22 m/s, hol −2.58) |
| `wide_maxwind_cell` | (4, 42667) | the wide dump's strongest-wind row: the wind-ranked selection's domain maximum vmag 4.81 m/s (the strongest wind this run's PET-0 slice offers; the cdn 33 m/s cap is not reached), converged at iteration 2, hol −1.16 |
| `wide_iter3_coldest_cell` | (13, 42126) | wide-dump convergence at iteration 3 at one of the domain's coldest cells (delt −4.54 K at this row, −5.86 K over the run), vmag 1.75 m/s, hol −4.21 |
| `wide_iter4_holclamp_adj` | (19, 41583) | wide-dump convergence at iteration 4 with hol −9.901, a tenth off the |hol| ≤ 10 clamp, at the weakest-wind step of the wind-ranked selection (vmag 0.64 m/s; same cell as `iter2_typical_unstable`) |

Every test overrides the 12 raw inputs at full dump precision and asserts the
11 derived inputs, the 4 neutral first estimates, the 16-field exit state, the
7 fluxes, the 10 diagnostics, and the convergence representation
(`conv_1..4` from the replay, `iter` from both). The replay
(`stage1/analysis/validate_cmeps_dump.py`) reproduces all 288 fixed-window rows
to ≤ 4.4e-15 and all 192 wide-window rows to ≤ 3.4e-15 relative on every
computed column, so `rel 1e-12` pins the dump to round-off. Row identity
(step, gid, local n, lat, lon — the true cell latitude, ~69 S for both
windows) and the exercised laws are cited in each test description.

### Coverage summary

| branch | traced rows | pinned |
|---|---|---|
| unstable psi (Paulson psimhu/psixhu, stable = 0) | 288 (fixed) + 192 (wide) | ✓ |
| |hol| ≤ 10 clamp | 21 rows at hol = −10 (fixed); wide hol ≥ −9.90 | ✓ |
| minwind = 0.5 m/s floor | 17 rows at vmag = 0.5 (fixed) | ✓ |
| iteration convergence 2 / 3 / 4 / 5 | 145 / 85 / 37 / 21 (fixed); 126 / 57 / 9 / 0 (wide) | ✓ |
| nonzero ocean currents (us/vs) | all rows (|u| ≤ 0.13 m/s) | ✓ |
| wind-ranked selection (dynamic, per-step top-8 of all masked PET-0 cells) | 192 rows, 9 cells | ✓ |
| strongest-wind rows of the domain | wide vmag 0.63–4.81 m/s (max 4.81) | ✓ |
| stable psi (−5·hol branch), rhn = 0.018 | 0 — delt > 0 nowhere on PET 0 (selection exhaustive, proven) | ✗ gap |
| cdn 33 m/s cap | 0 — domain wind max 4.81 m/s (selection exhaustive, proven) | ✗ gap |
| gustiness (rainc → ugust), cold-air outbreak | 0 (namelist-off in this case, not run) | ✗ gap |

### Transcription fixes found while writing the tests

1. **Exit state vs last unrolled update.** The first draft of the replay/selector
   returned the state after the final unrolled update; the dump carries the
   state at the CONVERGED iteration (the Fortran leaves the last-update values
   in the variables when the do-while exits), which for the iter-2 rows differs
   at the 1e-2 level (hol −3.683 vs −3.626 at the traced (11, 42124) row). The
   component selects the exit state by `iter`, and the validator replay mirrors
   the selection; with the fix all 288 rows reproduce to ≤ 4.4e-15.
2. **svp_to_qsat guard units.** The template's `(p − es) <= 0` guard declared
   the zero dimensionless, which only fails dimensional analysis once the
   template is bound to typed variables (p = pslv Pa, es = esat_raw Pa); the
   zero is declared Pa.
## Ocean albedo and ocean-export merges (`cmeps_ocnalb.esm`, `cmeps_merge.esm`)

This lane extends the CMEPS stage-2 work (the atmosphere–ocean flux lane above) with two more
pointwise components transcribed from the instrumented C_JRA_t62 run:

| File | Model | Laws | Source |
|---|---|---|---|
| `cmeps_ocnalb.esm` | `OcnAlb` | solar geometry + ocean albedo | `mediator/med_phases_ocnalb_mod.F90` (with `share/src/shr_orb_mod.F90`) |
| `cmeps_merge.esm` | `OcnMerge` | fraction-weighted ocn-export merges + custom shortwave | `mediator/med_phases_prep_ocn_mod.F90` (with `med_merge_mod.F90`, `esmFldsExchange_cesm_mod.F90`) |

Both import their shared math from `./cmeps_templates.esm` by reference (the
library now carries, in addition to the aoflux templates, the Berger 1978
solar-geometry templates `earth_mean_anomaly` / `earth_true_longitude_series` /
`earth_true_longitude` / `solar_declination` / `earth_sun_distance_factor` /
`solar_zenith_cosine`, the albedo templates `briegleb_direct_albedo` /
`taylor_direct_albedo` / `ocean_albedo_scheme` / `ocean_albedo_visible` /
`ocean_albedo_nearinfrared`, and the merge templates `scaled_fraction` /
`fraction_weighted_sum` / `open_ocean_weighted_sum` /
`ocean_absorbed_shortwave` / `shortwave_band`). The mean anomaly
`lambm0 + (calday−80.5)·2π/365 − mvelpp` is factored into `earth_mean_anomaly`
and bound once by `earth_true_longitude` (which passes it to the
equation-of-center series `earth_true_longitude_series`); `fswabsv` and
`fswabsi` share the single `ocean_absorbed_shortwave` law
`sw_dr·(1−α_dr) + sw_df·(1−α_df)` (the same law as the CLM `absorbed_shortwave`
of clm_templates.esm, named distinctly because both template libraries are
imported together and the esm-spec deep-equality rule rejects same-name
non-deep-equal definitions); the two-source merges whose sources share the
open-ocean weight (Faxa_rain/Faxa_snow/Foxx_lwnet) use
`open_ocean_weighted_sum` = `(a + b)·ofrac` rather than `fraction_weighted_sum`
(which is kept for the different-weight Foxx_taux/Foxx_tauy merges).

### The dumps

`stage1/dumps/cmeps/cmeps_ocnalb.csv` (288 rows = 12 traced cells × 24 steps)
pins the albedo phase; `stage1/dumps/cmeps/cmeps_merge.csv` (same 12 cells × 24
steps) pins the merges and the custom shortwave computation. Both come from the
definitive instrumented run **12134714** (fork commits
`cb613113`/`43ccf07` on `instrument/cmeps-dumps`), which is solution-neutral:
its restarts are md5-identical to the reference C_JRA_t62 run and to the two
earlier instrumented runs (12126699, 12127523 — three independent runs, same
restart md5s), and `ocean.stats.nc` is byte-identical. The traced cells are the
fixed `dump_first_cells = 12` window of PET 0 (local ogrid indices n
6933..7117, all ~69 S, January); all 12 are partial-ice cells
(ifrac 0.0683..0.6246), so the traced set is the same 12 cells every step.

Row contents:

- **ocnalb** (31 columns): nextsw_cday (1.0417..2.0 day), the orbital inputs
  eccen/obliqr/lambm0/mvelpp and outputs delta/eccf, the albedo settings
  albdif/albdir/min_albedo/use_min_albedo/use_briegleb/flux_albav, rlat/rlon,
  cosz, the FBFrac fractions ifrac/ofrac/ifrad/ofrad, and the four albedos
  anidr/avsdr/anidf/avsdf.
- **merge** (60 columns): the 4 fractions, the 9 atm inputs (rain/snow
  convective+large-scale, lwdn, 4 shortwave bands), the 5 aoflux inputs
  (lwup/sen/taux/tauy/evap), the 6 ice imports (taux/tauy/melth/meltw/salt/
  swpen), the 2 runoff inputs, the 4 ocean albedos (So_*, the `FBMed_ocnalb_o`
  link to the ocnalb phase), the 6 derived columns (fswabsv/fswabsi, the four
  scaled fractions), the 13 merged outputs and the 4 shortwave bands.

### Validation (stage1/analysis/validate_cmeps_ocnalb_merge_dumps.py)

The validator replays both phases from the dumped inputs in the Fortran term
order and compares every dumped output column:

- **ocnalb**: all 7 columns (delta, eccf, cosz, anidr, avsdr, anidf, avsdf)
  reproduce **bit-identically** (0.000e+00 relative error over all 288 rows).
  The Berger 1978 declination series (ve = 80.5, dayspy = 365), the cosz chain
  and the Briegleb et al. (1986) law with its cubic correction term
  `0.026/(cosz^1.7 + 0.065) + 0.15·(cosz−0.1)(cosz−0.5)(cosz−1.0)` are exact.
- **merge**: all 23 columns reproduce **bit-identically** (0.000e+00), including
  the swnet chain with the scaled fractions and the band split.

Two findings surfaced during validation, both pinned by the dumps:

1. **The band coefficients are single-precision literals.** The Fortran
   `c1 = 0.285` (med_phases_prep_ocn_mod.F90:830-834) carries no `_r8` suffix,
   so it is a float32 literal promoted to r8: every dumped row has
   `Foxx_swnet_vdr/Foxx_swnet = 0.28499999642372131` (= float32 0.285), not
   0.285. The `shortwave_band` template documents this and the components bind
   the exact promoted values (0.2849999964237213 / 0.2150000035762787).
2. **The radiation fractions lag by one coupling step.** The ocnalb phase
   copies ifrac/ofrac into ifrad/ofrad *after* its albedo loop, so at the
   merge phase's dump point (which runs after ocnalb in the next step's prep)
   the ifrad/ofrad used by the swnet computation are the *previous* step's
   fractions: ifrad(k) = ifrac(k−1), verified for all 288 rows. The merge
   component treats ifrad/ofrad as inputs (that is what the Fortran does); the
   lag is documented in both components.

### Transcription notes

- The ocnalb phase skips the whole computation when `flux_albav`; the traced
  run has `flux_albav = .false.`, so that branch is transcribed but unpinned,
  as are the Taylor scheme (`ocean_albedo_scheme = 0` in the run), the
  `use_min_albedo` clamp (`min_albedo = 0` unset) and the dark-side branch
  (all 288 rows are day-side, cosz 0.036..0.695). The `nextsw_cday >= -0.5`
  guard is always true here.
- `Foxx_swnet` weights the *open-ocean absorbed* shortwave by the lagged
  radiation fraction `ofracr_scaled` and the ice-penetrating shortwave by the
  current `ifrac_scaled` — the asymmetry is the Fortran's (F90:814), not a
  transcription artifact.
- The `Fioi_*_ice` dump labels map to `FBImp(compice,compocn)` fields whose
  names drop the `_ice` suffix; the components use the dump labels.
- The `import_swpen_by_bands` per-band branch (F90:824-827) is not exercised
  (SICE exports no `Fioi_swpen_vdr/vdf/idr/idf`) and is documented, not
  transcribed as a separate template.
- The enthalpy merges (Foxx_hlat etc.) are not dumped (documented gap); the
  Sx_*/Faxx_* atmosphere merges of prep_atm need a CAM case (no prep_atm phase
  in this run sequence).

### Bugs found in the CESM code (this lane)

- bugs.md #34: `med_phases_ocnalb_mod.F90` init: the `ocean_albedo_limit` else
  branch sets the dead local `use_min_ocnalb` instead of the module
  `use_min_albedo` (benign — the namelist default leaves the limit unset in
  the traced run, and the albedo loop reads the module variable).
- Instrumentation bugs fixed during this lane (not CESM bugs): the ocnalb
  writer initially shared the merge writer's selection cursor and wrote
  headers only (fixed with a dedicated `inext2o`), and both new writers
  emitted a trailing empty CSV field (fixed in run 12134714).

### Tests

9 tests × 4 assertions (ocnalb) and 9 tests × 15 assertions (merge), 18 tests
total, all green under `./esm test stage2/` (whole suite 2297P/0F/0E) at
`rel 1e-12`, `time_span {0,0}`. The rows are the four (step, cell) corners
plus step 2 cell 6933 (fraction-lag context), mid-run step 12 cell 7024, and
the min/max/median cosz (ocnalb) and ifrac (merge) rows; the informative
outputs are asserted per test. Pins that cannot fail are dropped: the ocnalb
anidf/avsdf (copies of the overridden albdif) and avsdr (duplicate of anidr),
the merge scaled fractions (equal to their inputs in every row), the
Foxx_rofl/Foxx_rofi copies of Forr_rofl/Forr_rofi, and the identically-zero
Faxa_rain and Fioi_salt (see Gaps). Full 288-row coverage is the validator's
job (bit-identical replay).

### Gaps

- Taylor scheme, flux_albav branch, use_min_albedo clamp, dark side (ocnalb);
  import_swpen_by_bands branch, enthalpy merges, prep_atm atmosphere merges
  (merge). All documented in the component descriptions.
- Faxa_rain and Fioi_salt (merge): both are identically zero in all 288 traced
  rows — the traced DATM forcing has no rain (Faxa_rainc/Faxa_rainl = 0) and
  the SICE data-ice exports no salt (Fioi_salt_ice = 0) — so their merge laws
  `(Faxa_rainc + Faxa_rainl)·ofrac` and `Fioi_salt_ice·ifrac` are transcribed
  but unpinned; a rain-bearing or salt-exporting case would pin them.
## Atmosphere-export merges (`cmeps_prep_atm.esm`)

This lane closes the last documented gap of `README-cmeps-ocnalb.md` ("the
Sx_*/Faxx_* atmosphere merges of prep_atm need a CAM case"): a second
instrumented CMEPS case, `F2000climo_f19_inst` (CAM6 + CLM + CICE + DOCN +
MOSART, f19 grid, 6 h run, 12 coupling steps at 1800 s), traced with a new
prep_atm phase dump.

| File | Model | Laws | Source |
|---|---|---|---|
| `cmeps_prep_atm.esm` | `AtmMerge` | the fraction-weighted lnd/ice/ocn -> atm merges | `mediator/med_phases_prep_atm_mod.F90:156-166` (with `med_merge_mod.F90:405-412`, `esmFldsExchange_cesm_mod.F90`) |

The model imports `fraction_weighted_sum` from `./cmeps_templates.esm` by
reference. Every atm export is a three-source merge accumulated in the Fortran
term order `dp = 0 + Sl*lfrac, dp = dp + Si*ifrac, dp = dp + So*ofrac`
(`med_merge_mod.F90:405-412`), so the .esm composes `fraction_weighted_sum`
twice: the land+ice pair weighted by `lfrac`/`ifrac` first (the inner
application), then the open-ocean source weighted by `ofrac` added on top (the
outer application with the identity `ice_frac = 1.0`, which multiplies
exactly). The 14 merged exports are `Sx_avsdr`/`Sx_avsdf`/`Sx_anidr`/
`Sx_anidf` (L875-887, 902-914, 929-941, 956-968), `Sx_tref`/`Sx_u10`/
`Sx_qref` (L988-1002, 1015-1029, 1046-1062), `Faxx_taux`/`Faxx_tauy`/
`Faxx_lat`/`Faxx_sen`/`Faxx_evap`/`Faxx_lwup` (L1085-1099, 1112-1126,
1139-1153, 1166-1180, 1197-1211, 1236-1250) and `Sx_t` (L1267-1279); the
15th export `So_t_export` is the unweighted `So_t` copy of L1282-1285
(`mrg_type = 'copy'`). The weights are the `FBFrac(compatm)` fractions:
`lfrac` for the land source (`mrg_fracname_lnd2atm_state/flux = 'lfrac'`,
`med_internalstate_mod.F90:289-290`), `ifrac` for the ice source, `ofrac` for
the ocean source (the traced case has `samegrid_atmlnd = .true.` and
`component_computes_enthalpy_flux = none`).

### The instrumentation fix

`med_dump_prep_atm_active` was originally gated on the *ogrid* aoflux init
flag (`is_init`) and the ogrid traced-cell counter (`step`). On this case
PET 0's f19 ogrid block is all-land (the Antarctica rows come first in the
local element order; `So_omask = 0` everywhere on PET 0), so the ogrid init
bails ("WARNING: no masked cells traced" in ocn.log), `is_init` stays
`.false.` and the prep_atm dump was permanently gated off — a silent
instrumentation failure that produced no rows. The fork fix (cmeps submodule
commit `17eef08f`, pointer `ea48423`):

- the atm-export dump gets its own counters `step3`/`ymd3`/`tod3`;
  `med_dump_prep_atm_tick` advances them from the mediator clock and is
  called by `med_phases_prep_atm_dump`, and `med_dump_prep_atm_active` gates
  on `is_init3`/`step3` instead of the ogrid flags;
- `med_dump_init_agrid` (the atm-grid dump init, first exercised by this
  dump) called `ESMF_MeshGet` on unallocated `elementIDs`/`elementCoords`
  (the ogrid path allocates first) — a latent segfault on the first
  execution; it now queries `elementCount` first and allocates.

The ogrid aoflux dump (`cmeps_aoflux_f2000.csv`) still produces nothing for
this case by design: PET 0 has no masked ogrid cells, and a cross-PE redesign
of the traced-cell selection is out of scope (the C_JRA_t62 lane already
pins the aoflux laws).

### The dump

`stage1/dumps/cmeps/cmeps_prep_atm.csv` (741708 B, 432 rows = 36 traced atm
cells x 12 coupling steps), written by `med_phases_prep_atm_dump` after the
merges, one row per traced atm-grid cell per step: `step,ymd,tod,n,gid,lat,lon`
(metadata; n is the PET-0 local atm index, gid the global element sequence
id), the fractions `lfrac,ifrac,ofrac`, then per field the three mapped
sources and the merged export: `Sl_/Si_/So_/Sx_avsdr`, `avsdf`, `anidr`,
`anidf`, `tref`, `u10`, `qref`, `Fall_/Faii_/Faox_/Faxx_taux`, `tauy`, `lat`,
`sen`, `evap`, `lwup`, `Sl_/Si_/So_/Sx_t`, and the `So_t` copy export
(duplicated column; the extractor/validator rename the second `So_t` to
`So_t_export`). 67 columns; floats `es26.17e3`, subnormals flushed.

Traced cells: the `dump_first_cells = 12` base window of PET 0 (n = 1..12,
present in every step) unioned with the per-step partial-ice (0 < ifrac < 1)
and partial-land (0 < lfrac < 1) extras, capped at 12 each; on PET 0's f19
slice the extras are also the same cells every step, so the traced set is the
fixed 36 cells n = 1..12, 18, 20, 22, 34, 36, 38, 40, 50, 52, 54, 66, 68, 70,
72, 88, 95, 102, 109, 111, 118, 120, 123, 136, 139 (all coastal Antarctica
cells of PET 0's slice; the stable (n, gid) pairing holds across all 12
steps). The pinned fraction regimes: fully-land
(lfrac = 1, n = 1), open-ocean (ofrac = 1, n = 5), partial-ice (ifrac =
0.99875, n = 2), the mixed three-fraction cell (n = 6: lfrac 0.0753, ifrac
0.6206, ofrac 0.3041), and partial-land (n = 95, 102). Sources on
zero-fraction cells carry the CMEPS spval 1e30 (the 13 land-source columns
`Sl_*`/`Fall_*` on the 20 lfrac = 0 cells: 240 spval-like values per column)
or 0.0 (the `Si_*` columns of the ice-free Antarctica rows) — both inert at
weight 0 (0.0 x 1e30 = 0.0 exactly, no NaN), and the tests pin the resulting
values implicitly.

### Validation (stage1/analysis/validate_cmeps_prep_atm_dump.py)

The validator replays the merge law per group (all 14 merged exports plus the
`So_t` copy) in the Fortran term order and checks every row:

- all 14 merge groups reproduce to **worst relative error <= 2.9e-16** over
  all 432 rows (bit-identical modulo the last ulp), with the spval-like
  sources checked as spval, not NaN (0 NaN anywhere);
- `lfrac + ifrac + ofrac == 1` (tol 1e-12) on every row;
- `So_t_export == So_t` everywhere (the copy law);
- fraction-regime counts: 252 partial-ice / 180 open-ocean / 0 fully-iced /
  168 partial-land rows; distinct ifrac values 80 (0.0000..0.9988);
- every step traces the base window (n = 1..12 present in every step, 36
  cells/step), and the stable (n, gid) pairing holds across all 12 steps.

`RESULT: prep_atm PASS`. Neutrality: the instrumented run's `cpl.r`, `cice.r`
and `docn.r` restarts are md5-identical to the reference `F2000climo_f19`
case (b9a9f0e2... / dc5e4704... / 0e5c3203...); `cam.r`/`clm2.r`/`mosart.r`
differ only in the filename variables (`cpath`, `hrestpath`, `nhfil`,
`op_field1/2`, `locfnh`, `locfnhr`) and the `caseid`/`case_title`/`history`
attributes, as expected.

### Transcription notes

- The 15 exports are `fraction_weighted_sum` composed twice (no dedicated
  three-source template): `((Sl*lfrac + Si*ifrac) + So*ofrac)` reproduces the
  `med_merge` accumulation order exactly, including the spval-at-zero-weight
  rows.
- `Sx_qref`/`Faxx_evap` are the bulk blank-suffix branch of the
  `water_bulk_or_tracers` split (the traced run is bulk).
- The `Faox_*` ocean sources come from the aoflux phase output
  (`FBMed_aoflux_a`; on this case's `aoflux_grid = ogrid` they are the ogrid
  values mapped to the atm grid by `med_aofluxes_map_ogrid2agrid_output`,
  called at the top of `med_phases_prep_atm`, F90:143-145); the `So_*` albedo
  sources come from the ocnalb phase output (`FBMed_ocnalb_a`, `addmap_ocnalb`).
- The `So_t` copy export is named `So_t_export` in the model because the
  dump carries both the `So_t` source and the copy export columns.

### Bugs found in the CESM code (this lane)

- bugs.md #38: the prep_atm dump gating bug (fork instrumentation; see "The
  instrumentation fix" above) and the latent `ESMF_MeshGet` crash in
  `med_dump_init_agrid`.

### Tests

5 tests x 15 assertions = 75 assertions, all green under `./esm test stage2/`
(whole suite **2737P/0F/0E**; the worktree's starting commit 5726a2d ran
2662P/0F/0E, so this lane adds exactly its 75) at `rel 1e-12`, `time_span
{0,0}`, plus `./esm validate` clean. The pinned rows exercise the fraction
regimes: `step1_fully_land` (merge reduces to the land source), `step1_open_ocean`
(reduces to the ocean source), `step1_partial_ice` (two-source ice + ocean),
`step1_mixed` (full three-way merge, every source valid) and `step12_mixed`
(the same cell at the last step, where the 05:30 local-time albedo sources
are the dark-side 1.0 from all three sources and the merge still sums to
1.0). Every merged export is asserted at full dump precision, so a wrong
weight, a wrong source, a wrong association or a wrong fraction all fail.
Full 432-row coverage is the validator's job (bit-identical replay).

### Gaps

- The ogrid aoflux dump for this case produces no rows (PET 0 all-land; a
  cross-PE traced-cell selection would be needed — out of scope; the aoflux
  laws are pinned by the C_JRA_t62 lane).
- No fully-iced rows in this window (ifrac max 0.9988); the lfrac = 1 rows
  pin the land-only reduction instead. The dark side is pinned only through
  the albedo = 1.0 sources of `step12_mixed`.
- The `lnd2atm` merges on grids with `samegrid_atmlnd = .false.` (the
  `lfrin` fallback of the `Sl_lfrac` custom copy, med_phases_prep_atm_mod.F90)
  are not exercised (the traced case is same-grid).

## Test results across runners

The Rust CLI runs the whole ported lane (see the per-file tables above; the
lane total is **709 assertions**: 468 aoflux + 135 merge + 36 ocnalb + 70
prep_atm, all `rel 1e-12`, `time_span {0,0}`) with **709P / 0F / 0E** on both
the EqESM main `./esm` binary (0.7.0) and the EarthSciAST 0.10.0 release
binary; `esm validate` and `esm units` are clean on all six files under both
binaries. The python inline gate
(`tools/run_esm_inline_tests.py`) reports the same 709 assertions plus the
two no-test library/build rows (1 pass each for `cmeps_aoflux_step.esm` and
`cmeps_templates.esm`, the runner's per-file convention) as **711P / 0F / 0E**
— zero FAILs and zero ERRORs, unlike the CICE/CISM lanes whose shaped
parameter and mount-edge constructs hit python-runner limitations; none of
those constructs appear in this lane.
