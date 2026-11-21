# CICE stage 2 — `.esm` skeleton

Stage-2 implementation of the CESM CICE sea-ice component (cesm3_cice6_6_3_22,
checkout `stage1/cesm/components/cice`) as esm 2.0.0 files: component structure,
imports/exports, solver block, the pointwise column/dynamics/transport laws of
the default configuration transcribed exactly, subcomponents, and top-level
assembly. The `tests` blocks pin the stage-1 instrumentation dumps
(`stage1/dumps/cice/`) — see [Testing](#testing).

All model logic lives in `.esm` files; this README is the human-readable map.

The `stage1/...` paths and `bugs.md` citations throughout refer to the EqESM
project repository (the CESM checkout instrumented to produce the dump tuples
the tests pin, and the project's centralized bug list).
Sources: `stage1/cesm/components/cice/src/cicecore/drivers/nuopc/cmeps/`
(`ice_import_export.F90`, `CICE_RunMod.F90`),
`stage1/cesm/components/cice/src/cicecore/cicedyn/general/`
(`ice_step_mod.F90`, `ice_forcing.F90`, `ice_flux.F90`),
`stage1/cesm/components/cice/src/cicecore/cicedyn/dynamics/`
(`ice_dyn_evp.F90`, `ice_dyn_shared.F90`),
`stage1/cesm/components/cice/src/cicecore/cicedyn/analysis/`
(`ice_transport_driver.F90`, `ice_transport_remap.F90`),
`stage1/cesm/components/cice/src/icepack/columnphysics/`
(`icepack_shortwave.F90`, `icepack_therm_shared.F90`, `icepack_therm_bl99.F90`,
`icepack_therm_vertical.F90`, `icepack_meltpond_lvl.F90`, `icepack_atmo.F90`,
`icepack_mechred.F90`, `icepack_mushy_physics.F90`, `icepack_flux.F90`,
`icepack_parameters.F90`), and the boundary plan in `stage1/boundaries.md` (§1.3).

Default configuration transcribed (the D-class reference run's namelist,
`stage1/cime/cases/D_cice_inst/CaseDocs/ice_in`, unless noted): `shortwave = 'dEdd'`
(the delta-Eddington 3-band solver and the albedo/shortwave laws, ported as
`cice_shortwave.esm` plus the dEdd template family of `cice_templates.esm`),
`kdyn = 1` (EVP), `grid_ice = 'B'`, `ndtd = 1`, `ndte = 120`,
`revised_evp = .false.`, `elasticDamp = 0.36`, `Ktens = 0`,
`e_yieldcurve = e_plasticpot = 2`, `capping = 1`, `u0 = 5e-5`, `cosw = 1`,
`sinw = 0`, `kstrength = 1` (the Rothrock potential-energy strength is
transcribed and dump-pinned both in the lowered `Dynamics` model, where it
feeds the viscosities, and as a single-cell probe in the coupling cap; the
ridge redistribution itself is a stage-3 dynamics concern), `atmbndy = 'similarity'` (the
Monin-Obukhov iteration is transcribed and dump-pinned in the coupling cap;
the constant scheme remains for the assembly Control), `ktherm = 2` (mushy), `conduct = 'MU71'`,
`tfrz_option = 'mushy'`, `saltflux_option = 'constant'`, `frzpnd = 'hlid'`
(sea-level ponds, `tr_pond_sealvl`), `snwredist = 'none'`, `hs0 = 0.0`,
`phi_i_mushy = 0.45`, `congel_freeze = 'one-step'`, `emissivity = 0.95`
(forcing_nml), `natmiter = 5`, `ncat = 5`, `nilyr = 8`, `nslyr = 3`,
`l_brine = .true.`, `dt = 3600 s`.

## File map

| File | Contents | Fortran source |
|---|---|---|
| `cice_templates.esm` | Expression-template library (119 templates): snow cover / albedo / absorbed-penetrating shortwave, the dEdd snow fraction and effective pond area, the full delta-Eddington law family (scaled IOPs taus/omgs/asys, delta-Eddington layer solution, fresnel refraction amplitudes, snow grain adjust + mass extinction, aerosol mixing, band weights, interface flux fractions, band absorption) | `icepack_shortwave.F90`: compute_albedos 466-597, absorbed_solar 701-896, shortwave_dEdd_set_snow 3448-3454, shortwave_dEdd_set_eff 3495-3637, compute_dEdd_3bd 1703-3013, solution_dEdd 3022-3488 |
| | saturation humidity, surface heat flux, liquidus (linear + mushy), enthalpy↔temperature (BL99 brine quadratic, mushy quadratic, fresh, snow) | `icepack_therm_shared.F90`: surface_heat_flux 147-165, liquidus 383-418; `icepack_mushy_physics.F90`: liquidus_temperature_mush 227-261, icepack_mushy_temperature_mush 348-452, enthalpy_of_melting 264-286, liquid_fraction_mush 288-310; calculate_Tin_from_qin 68-101; snow temperature 470-484 |
| | conductivity (bubbly Pringle 2007 / MU71 / mushy) and interface conductances, congelation enthalpy, ocean heat flux, melt-pond volume change (cesm and sea-level schemes) | `icepack_therm_bl99.F90`: conductivity 874-961 (MU71 911-916); `icepack_mushy_physics.F90`: conductivity_mush 455-485; `icepack_therm_vertical.F90`: qbot 1432-1443, fbot 662-678; `icepack_meltpond_lvl.F90`: 154-174; `icepack_meltpond_sealvl.F90`: 76, 157 |
| | constant atmo boundary layer (tau, shcoef, lhcoef) and the similarity scheme (neutral drag, relative wind, stability parameter, stable/unstable psi, exchange coefficients, 2-m psix2, Tref/Qref/Uref) | `icepack_atmo.F90`: atmo_boundary_const 398-496 (460-464, 493-494); atmo_boundary_layer 52-389 (215, 176-210, 985-989, 1015-1075, 289-291, 364-378) |
| | Hibler and Rothrock strength (cumulative distribution, exponential participation, ridge redistribution hrmin/hrexp/krdg, aksum, strength term), Delta invariant, viscosities/replacement pressure, classic-EVP stress maps, ocean-ice stress, seabed stress | `icepack_mechred.F90`: 1720, ridge_itd 848-1036, icepack_ice_strength 1660-1712; `ice_dyn_shared.F90`: strain_rates 2081-2161, visc_replpress 2444-2473, set_evp_parameters 451-484; stepu 923-964 |
| `cice_shortwave.esm` | Model `Shortwave` — the delta-Eddington 3-band radiation scheme `compute_dEdd_3bd` / `solution_dEdd` (icepack_shortwave.F90:1703-3488): layer geometry, SNICAR snow-IOP table lookup and mass extinction, per-layer tau/w0/g over the snow/bare/pond branches with bulk-aerosol mixing, ocean albedo, the delta-Eddington layer solution (8-point Gauss-Legendre diffuse angular integration), the fresnel refraction layer, the downward/upward layer-combination recurrences with the trmin activity cutoff, the interface flux fractions, and the band-weighted flux/absorption accumulations; 125 equations over the layer/iface/band/gauss axes; the SNICAR and bulk-aerosol tables as `function_tables`; the pond branch (srftyp = 2) transcribed but untested (the instrumented run has no pond rows) | `icepack_shortwave.F90`: compute_dEdd_3bd 1703-3013, solution_dEdd 3022-3488; `icepack_shortwave_data.F90`: 107-263, 331-353 |
| `cice_thermodynamics.esm` | Model `Thermodynamics` — the D-class column physics: prep_radiation dEdd shortwave/albedo, the mushy (ktherm = 2) vertical heat conduction and surface energy balance, growth/melt/ponds (frzpnd = hlid sea-level) and ocean heat/fresh/salt fluxes, plus the cell-level merged aggregates of icepack_flux.F90:196-257 (aice, fsurf, fcondtop, fhocn, fresh, fsalt, flwout, fsens, flat, evap, fswabs, fswthru, fswint, congel, meltb, meltt, melts, dsnow); 85 equations over ncat × nilyr/nslyr (83 algebraic pointwise laws + 2 enthalpy PDEs) | `icepack_shortwave.F90` (step_radiation, prep_radiation 3893-3922, dEdd set_eff/set_snow), `icepack_therm_mushy.F90` (two-stage mushy tridiagonal 1800-1985, semi-discrete flux-divergence ODEs), `icepack_mushy_physics.F90` (temperature/enthalpy inversions), `icepack_therm_vertical.F90` (thickness changes, freshn/fsaltn 510-522, fhocnn 1625-1630, sublimation 1355-1403, 1502-1559), `icepack_flux.F90` (merge_fluxes 180-260), `icepack_meltpond_sealvl.F90` (compute_ponds_sealvl, dvn) |
| `cice_dynamics.esm` | Model `Dynamics` — B-grid momentum balance (continuous limit of stepu) and classic-EVP stress relaxation ODEs, the kstrength = 1 Rothrock strength (aice0, Gsum, exponential participation apartic, hrmin/hrexp/krdg, aksum per T cell), viscosities; 48 equations over the traced 3×5 subdomain (N_I = 3 T cells × N_J = 5), the spatial-D targets lowered by the EarthSciDiscretizations B-grid rules (`strain_rates_divu/tension/shear`, `stress_divergence_strintx/strinty`); the four-corner staggered stresses carried per corner on a `corner` axis (no corner collapse) | `ice_dyn_shared.F90`: stepu 923-964, dyn_prep2 815-833, dyn_finish 1345-1348, Tmass 540, strain_rates 2094-2175; `ice_dyn_evp.F90`: stress 1584-1609, 1667-1765; `icepack_mechred.F90`: icepack_ice_strength 1660-1712, ridge_itd 848-1036 |
| `cice_transport.esm` | Model `Transport` — per-category conservative advection of the area aicen, the volumes vicen/vsnon, and the tracer products aTsfcn = aicen·Tsfcn, vqicen = vicen·qicen (8 ice layers) and vsqsnon = vsnon·qsnon (3 snow layers), with the tracers recovered by division (Tsfcn, qicen_adv, qsnon_adv); lowered by the EarthSciDiscretizations `transport_flux_divergence` rule and its layered companion `transport_flux_divergence_layered` (passive layer axis) to a **centered** conservative cell flux divergence — not CICE's incremental remapping, and without its positivity/monotonicity guarantees (see [Transport scheme](#transport-scheme)); 16 equations over the 3×5 subdomain | `ice_transport_driver.F90`: 251-700, state_to_tracers/tracers_to_state 889-1114; `ice_transport_remap.F90`: 317-831, 658-666, 3556-3690 |
| `cice_coupling.esm` | Model `IceCap` — med↔ice cap renames, areacor scaling, Sa_pbot potT/rhoa branch, export aggregation (ailohi, Tsrf, merge_fluxes sums), Faii_lwup fix; the similarity atmo boundary layer (5-iteration unroll) with the aicen_init-weighted reference-height exports, the Rothrock strength law, and the dynamics pointwise-law probes (EVP stress maps, strain invariant, viscosities/replacement pressure, stepu ocean-ice stress) as algebraic probes of the dynamics physics; 166 equations | `ice_import_export.F90`: ice_import 414-700, ice_export 1030-1317; `icepack_flux.F90`: merge_fluxes 180-260; `icepack_atmo.F90`: atmo_boundary_layer 52-389; `icepack_mechred.F90`: ridge_itd 848-1036, icepack_ice_strength 1660-1712 |
| `cice.esm` | Top-level assembly: mounts the four subcomponents by reference + inline `Control` (dt_dyn subcycling, constant atmo boundary layer), 57 `variable_map` coupling entries, solver block | `CICE_RunMod.F90`: ice_step 109-369; `ice_step_mod.F90`: step_dyn_horiz 990-1074; `ice_forcing.F90`: prepare_forcing 1606-1825; `icepack_atmo.F90`: 398-496 |

The PDEs are written as spatial-D rewrite targets
(`div(c·u) = D(c·uvel, x) + D(c·vvel, y)`), lowered onto the traced 3×5
subdomain by the CICE B-grid discretization rules of
`github.com/earthsciml/EarthSciDiscretizations` (`grids/cice_bgrid`, on
ESD `main` since EarthSciDiscretizations PR #50, with the layered transport
rule of PR #59): the strain-rate rules lower `D(uvel,x)+D(vvel,y)`,
`D(uvel,x)−D(vvel,y)`, `D(uvel,y)+D(vvel,x)` to the four-corner staggered
combinations of `strain_rates` (ice_dyn_shared.F90:2094-2175), the
stress-divergence rules lower `D(sigma11,x)+D(sigma12,y)` and
`D(sigma12,x)+D(sigma22,y)` to the stepu stress integrals strintx/strinty
(ice_dyn_evp.F90:1698-1765), and the transport rule lowers
`D(c·uvel,x)+D(c·vvel,y)` to the conservative cell flux divergence of the
mass update `mm − w1·tarear` (ice_transport_remap.F90:3586-3590) with the
centered edge reconstruction of the edgearea_e/n linear branch (F90:658-666)
— the continuous flux form that the incremental-remapping scheme replaces
with the departure-cell integrals of the Fortran (the scheme difference is
quantified by the transport pin tolerances, see [Testing](#testing), and
the consequences are listed under [Transport scheme](#transport-scheme)). The
momentum equation is the continuous limit of the Fortran's implicit stepu
solve (the cca/ccb/ab2 algebra is solver machinery, documented rather than
transcribed); the classic-EVP stress maps become relaxation ODEs
d(σ)/dt = (σ_target − σ)/Td with Td = 2·elasticDamp·dt.

## Units

All fields are SI; temperatures are °C internally (`degC` ≡ K in the unit
checker's algebra) with `Tffresh = 273.15` added where Kelvin is needed;
salinity is ppt; the CMEPS flux imports are W/m² and kg/m²/s (the latter equals
mm/s of water).

| Quantity | Symbols | Units |
|---|---|---|
| Thicknesses / volumes / depths | `hi`, `hs`, `hilyr`, `hslyr`, `vicen`, `vsnon`, `hpnd`, `vice`, `vsno`, `Si_snowh` | m (volumes per unit grid-cell area) |
| Enthalpies | `qicen`, `qsnon`, `qbot` | J/m³ |
| Temperatures | `zTin`, `zTsn`, `Tmlts`, `Tbot`, `Tsfc`, `Tf`, `sst` | degC; `potT`, `Tair`, `Si_t` in K |
| Conductivities / conductances | `kilyr`, `kslyr`; `kh_top`, `kh_snowice`, `kh_bot` | W/m/K; W/m²/K |
| Fluxes | `fswsfc`, `fswpen`, `fswthru`, `fsurfn`, `fsensn`, `flatn`, `flwoutn`, `fbot`, `fhocnn`, `frzmlt`, sw bands, Faii_*/Fioi_* | W/m² |
| Water fluxes | `evapn`, `freshn`, `fsaltn`, `fsnow`, `frain` | kg/m²/s |
| Stresses | `strength`, `stressp/m/12`, `sigma*`, `rep_prs` | N/m; `tau`, `strairx/y`, `taux/y`, `strintx/y`, `strtltx/y`, `Cb` | N/m² |
| Strain rates | `divu`, `tension`, `shear`, `Delta`, `deltaminEVP` | 1/s (T-point rates); m²/s in the lowered B-grid dynamics — the corner strain rates of `strain_rates` are area-weighted ("NOTE these are actually strain rates * area (m^2/s)", ice_dyn_shared.F90:2119-2120), and `DminTarea = deltaminEVP·dxT·dyT` |
| Mass | `m` (Tmass) | kg/m² |
| Viscosities | `zetax2`, `etax2`, `tmpcalc` | kg/s (T point); kg/(m² s) in the lowered B-grid dynamics (the area factors cancel in the stress update, so `zetax2·divu − rep_prs` closes as N/m) |
| Dynamics | `uvel`, `vvel`, `uocn`, `vocn`, `uatm`, `vatm`, `wind`, `u0` | m/s |
| Air | `rhoa` | kg/m³; `Qa`, `Qsfc` kg/kg; `Sa_z`/`zlvl` m; `Sa_pbot` Pa |
| Time | `dt`, `dt_dyn`, `Td` | s |
| Constants | `puny = 1e-11`, `Tffresh = 273.15`, `rhoi = 917`, `rhos = 330`, `rhow = 1026`, `cp_ice = 2106`, `cp_ocn = 4218`, `cp_air = 1005`, `Lfresh = 3.34e5`, `Lsub = 2.835e6`, `Lvap = 2.501e6`, `depressT = 0.054`, `emissivity = 0.95` (D-class forcing_nml), `stefan_boltzmann = 5.67e-8`, `gravit = 9.80616`, `vonkar = 0.4`, `zref = 10`, `iceruf = 5e-4`, `zvir = 0.606`, `cp_wv = 1810`, `Cf = 17`, `Gstar = 0.15`, `astar = 0.05`, `maxraft = 1`, `mu_rdg = 4` (D-class namelist) | (icepack_parameters.F90:36, 82, 62, 61, 65, 74-75, 281, 83-84, 77, 159, 56, 190, 284-285, 283, 282, 261, 269; icepack_mechred.F90:70-72, 74; icepack_parameters.F90:2814) |

**Unit notes**

- `"C"` parses as Coulomb in the esm unit checker, so all Celsius fields use
  `degC` (identical to K in the checker's algebra).
- `lhcoef` is W/m² (per specific-humidity difference, not per K): the Fortran
  `lhcoef = latncoef·Lheat·rhoa·wind` (icepack_atmo.F90:494) carries the latent
  heat inside the coefficient.
- `evapn` requires the ρ in the numerator: the Fortran
  `evapn += dhs·rhos` (icepack_therm_vertical.F90:1502-1521) is transcribed as
  the continuous rate `evapn = (esub + econ)·rhos/((qsn − rhos·Lvap)·dt)` (the
  condensation closure `dhs = econ/qsub` accumulates into the same evapn,
  F90:1355-1399, so the net is `−flatn·dt/qsub`; transcription fix #9);
  `fsaltn` is
  the rate form `fsaltn = −rhoi·dhi·ice_ref_salinity·0.001` with the same net
  thickness change `dhi = congeln + meltbn + melttn + evapin/rhoi` as freshn
  (F90:513, 521; the per-step dt divides out of both rate forms).
- `freshn` in rate form: the Fortran's `freshn = evapn − (rhoi·dhi +
  rhos·dhs)/dt` (F90:510-513, per-step) cancels the sublimation/condensation
  and new-snowfall terms exactly — `evapn = evapin + evapsn` and
  `dhs = −meltsn − evapsn/rhos` with `hsn_new` added back to dzs(1) before
  hin/hsn are summed (F90:1641-1672) — leaving
  `freshn = −(rhoi·(congeln + meltbn + melttn) + rhos·meltsn)`; the rain is
  added at the cell level (`fresh = fresh + frain·aice`,
  icepack_therm_itd.F90:2179, frain in kg/m²/s).
- The dumped volume tendencies (dsnow, congel, meltb, meltt, melts) are per
  step [m] — the instrumented dump column carries the accumulated step
  change — while the .esm laws are continuous rates [m/s]; the assertion
  expected values are `dump/dt` (dt = 3600 s). Flux columns (fsurf, fcondtop,
  fhocn, flwout, fsens, flat) are [W/m²] and water fluxes (fresh, fsalt,
  evap) [kg/m²/s] as dumped (transcription fix #11).
- All icepack module constants are inlined as bare literals inside the
  templates; the unit checker treats bare literals as dimension-Unknown and
  skips products/comparisons containing them, which is how the many
  Fortran-sloppy unit mixes (e.g. `meltt·rhoi + frain·dt` in the melt-pond
  law) validate.
- `sign()` preserves its argument's dimension, so the Fortran's
  `sign(1, fm)` of the ocean-stress rotation is carried as the `hemis`
  parameter (+1/−1).

## §1.3 mapping, as implemented

| Boundary (boundaries.md §1.3) | Proposed | Implemented |
|---|---|---|
| Import (med→ice): atm state, rad/precip, ocn state, Fioo_q | `cice_coupling.esm` | ✓ `IceCap`: renames + areacor + Sa_pbot potT/rhoa branch; uocn/vocn/ss_tltx/ss_tlty wired to Dynamics; potT/Qa/rhoa/sw*/flw/sst/sss/frzmlt/frain/fsnow wired to Thermodynamics; uatm/vatm/rhoa wired to the assembly `Control` atmo scheme |
| Export (ice→med): Si_* state, Faii_* atm/ice fluxes, Fioi_* ice/ocn fluxes | `cice_coupling.esm` | ✓ `IceCap`: ailohi, Tsrf, aggregate albedos, vice/vsno/snowh, merge_fluxes sums, areacor; Fioi_taux/tauy sign flip from the Dynamics full ocean stress |
| Wave exports (Si_thick, Si_floediam), aerosols (Fioi_bcpho/bcphi, Fioi_flxdst), isotopes, per-band Fioi_swpen_* | `cice_coupling.esm` | ◐ deferred — carried as zero parameters with file:line notes (wave/aerosol/isotope tracers off; per-band fswthru_* not in the stage-2 column skeleton) |
| EVP dynamics + icepack column thermodynamics (the run step) | `cice_dynamics.esm` + `cice_thermodynamics.esm` | ✓ mounted in `cice.esm` with the ice_step ordering documented (step_prep → prep_radiation → step_therm1 → step_therm2 → update_state → ndtd loop step_dyn_horiz(evp → transport_remap) → step_dyn_ridge → update_state) |
| Transport (advection) | `cice_transport.esm` | ◐ continuity system and the Tsfc/qice/qsno tracer-product transport as spatial-D rewrite targets, lowered to a centered flux divergence; CICE's incremental remapping (and its positivity/monotonicity) is a stage-3 discretization |
| Ridging (kstrength = 1 Rothrock) | `cice_dynamics.esm` + `cice_coupling.esm` (probe) | ◐ the Rothrock strength law (icepack_mechred.F90:1660-1712 with the ridge_itd state, krdg_partic = krdg_redist = 1, mu_rdg = 4) is transcribed per T cell in `Dynamics`, where it feeds the viscosities (pinned at all 15 traced cells against `cice_ice_strength.csv`), and as a single-cell probe in `IceCap`; the ridge redistribution of area/volume/enthalpy (ridge_shift, F90:1068+) is a stage-3 dynamics concern |
| Tsfc implicit surface energy balance | `cice_thermodynamics.esm` | ◐ the balance fsurfn(Tsfc) − fcondtopn = 0 (the fcondtop − fsurfn < ferrmax consistency checks of the mushy two-stage solver, icepack_therm_mushy.F90:535/588/834/892, with the etop_mlt = max((fsurfn − fcondtopn)·dt, 0) closure of icepack_therm_vertical.F90:1337-1338) is transcendental in Tsfc (saturation-humidity exponential); the Rust runner cannot solve implicit equations (divergence 2), so Tsfc is a parameter fed by the coupled solve in stage 3 — the algebraic residual `fsurf_bal = fsurfn − fcondtopn` is carried as a diagnostic (eq 85) and pinned at the dumped exit state (test `thermo_surface_balance_step2_cell2_4`) |

## Pointwise laws — Fortran vs esm transcription notes

All templates are match-less, invoked by name (`apply_expression_template`
with bindings), and transcribed exactly with file:line citations in the
descriptions. Representative transcriptions:

| Template | Fortran | esm |
|---|---|---|
| `snow_cover_fraction` | `asnow = hs/(hs+snowpatch)` for `hs > puny` (icepack_shortwave.F90:574-579) | `ifelse(hs > 1e-11, hs/(hs+0.02), 0)` |
| `thickness_albedo_factor` | `fh = min(atan(hi·4)/atan(ahmax·4), 1)` (F90:541-542) | `min(atan(hi·4)/atan(0.3·4), 1)` |
| `layer_absorbed_shortwave` | `Iswabs = fswpen·(exp(−kappav·ztop) − exp(−kappav·zbot))` (F90:862-880) | `fswpen·(transmittance(ztop) − transmittance(zbot))`, calling `shortwave_transmittance` by reference |
| `surface_heat_flux` | `fsurfn = fswsfc + ε·flw − ε·σ·TsfK⁴ + shcoef·(potT−TsfK) + lhcoef·(Qa−Qsfc)` (icepack_therm_shared.F90:147-165) | same, with `Qsfc` from `saturation_specific_humidity_ice` |
| `ice_temperature_from_enthalpy` | brine quadratic `cp_ice·T² + ((cp_ocn−cp_ice)·Tmltk − qin/ρi − L)·T + L·Tmltk = 0` solved by the negative root (F90:68-101) | `ifelse(l_brine > 0.5, min((−bb1−√(bb1²−4·cp_ice·cc1))/(2·cp_ice), Tmltk), (L+qin/ρi)/cp_ice)`; the Fortran abort on a negative discriminant is a noted guard; the D-class run uses the mushy inversion instead (`icepack_mushy_temperature_mush`) |
| `ice_conductivity_bubbly` | `k = max((2.11 − 0.011·T + 0.09·S/min(−puny,T))·ρi/917, kimin)` (icepack_therm_bl99.F90:918-924) | same with `min(−1e-11, T)` |
| `ice_conductivity_mu71` | `k = max(rhoi·(1.88 + 0.0102·T) − 0.9e-3·T², kimin)` (icepack_therm_bl99.F90:911-916) | same; the D-class `conduct = 'MU71'` law |
| `ice_conductivity_mush` | mushy two-stage `k = max(k1, k2)` with the solid-fraction weighted law (icepack_mushy_physics.F90:455-485) | same; used by the ktherm = 2 solver |
| `congelation_enthalpy` | `qbot = −ρi·(cp_ice·(Tmlts−Tbot) + L·(1−Tmlts/Tbot) − cp_ocn·Tmlts)`, capped at `−0.5·ρi·L` (icepack_therm_vertical.F90:1432-1443) | same, `ifelse` brine/fresh, `min` cap |
| `ocean_heat_flux` | `fbot = max(−cp_ocn·rhow·0.006·max(sst−Tf,0)·ustar, frzmlt)` (F90:662-678) | same; ustar floored at 0.005 in the model |
| `meltpond_cesm_dvn` | `dvn = rfrac/rhofresh·(meltt·ρi + melts·ρs + frain·dt)·aicen − volpn·(1−exp(rexp·dTs/Tp))` (icepack_meltpond_lvl.F90:154-174) | same with `Tp = −2`, `rexp = 0.01`, `dTs = max(−2−Tsfcn, 0)`; the D-class run uses the sea-level scheme instead (`meltpond_sealvl_dvn`) |
| `atmo_constant_tau/shcoef/lhcoef` | `tau = ρa·0.0012·wind`; `shcoef = 0.0012·1005·ρa·wind`; `lhcoef = 0.0015·Lheat·ρa·wind` (icepack_atmo.F90:460, 493-494) | identical, `Lheat = Lsub = 2.835e6` for ice |
| `atmo_neutral_drag` | `rdn = vonkar/log(zref/iceruf)` (icepack_atmo.F90:215) | identical (`vonkar = 0.4`, `zref = 10`, `iceruf = 5e-4`) |
| `atmo_stability_parameter` | `hol = vonkar·gravit·zlvl·(tstar/thva + qstar/(1/zvir+Qa))/ustar²`, clamped to |hol| ≤ 10 (F90:985-989) | identical (sign-preserving clamp via min/max) |
| `atmo_psi_momentum_unstable` / `atmo_psi_scalar_unstable` | Paulson-1970 forms with `capital_X = sqrt(max(sqrt(|1−16·hol|), 1))` (F90:1040-1075) | identical, `pih = π/2`; the stable branch `psi_stable = −(0.7·hol + 0.75·(hol−14.3)·exp(−0.35·hol) + 10.7)` (F90:1017-1019) |
| `atmo_reference_temperature/humidity/wind` | `Tref = potT − delt·(rh/vonkar)·(alzs+al2−psixh+psix2) − 0.01·zTrf`; `Qref = Qa − delq·(re/vonkar)·(…)`; `Uref = vmag_rel·rd/rdn` (F90:366-378) | identical; psix2 = −5·hols·stable + (1−stable)·ψ_scalar_unstable(hols) at hols = hol·2/zlvl (F90:364-365) |
| `ice_strength_hibler` | `strength = Pstar·vice·exp(−Cstar·(1−aice))` (icepack_mechred.F90:1720) | identical (`Pstar = 2.75e4`, `Cstar = 20`); the kstrength ≠ 1 branch, kept in the library but not used — the run is kstrength = 1 (Rothrock) |
| `ridge_cumulative_area` | `Gsum(n) = Gsum(n−1) + aicen(n)` for `aicen(n) > puny`, `Gsum(0) = aice0` for `aice0 > puny` (F90:850-879) | nested prefix sum over m ≤ n with the aicen/aice0 masks |
| `ridge_participation_exponential` | `apartic = [exp(−G(n−1)/astar) − exp(−G(n)/astar)]/(1 − exp(−astari))`, `astari = 20` (F90:919-934) | identical (`astar = 0.05`) |
| `ridge_hrmin/hrexp/krdg` | `hrmin = min(2·hi, hi+maxraft)`; `hrexp = mu_rdg·√hi`; `krdg = (hrmin+hrexp)/hi` for `aicen > puny`, else `krdg = 1` (F90:1004-1010) | identical (`maxraft = 1`, `mu_rdg = 4`), `hi = max(vicen/aicen, puny)` |
| `ridge_strength_term` | `apartic·(h2rdg/krdg − hi²)` with `h2rdg = hrmin² + 2·hrmin·hrexp + 2·hrexp²` (F90:1697-1706) | identical; the cap sums it into `strength = Cf·Cp·Σ/aksum` (F90:1710) |
| `viscosity_scale` | `tmpcalc = capping·P/max(Δ,Dmin) + (1−capping)·P/(Δ+Dmin)` (ice_dyn_shared.F90:2467-2468) | identical; `Dmin = deltaminEVP = 1e-11` |
| `evp_stressp_update` | `stressp_new = (stressp·(1−arlx1i·revp) + arlx1i·(zetax2·divu − rep_prs))·denom1` (ice_dyn_evp.F90:1584-1591) | transcribed as the relaxation ODE `D(stressp)/t = (stressp_target − stressp)/Td` with `Td = 2·elasticDamp·dt` (see divergences) |

## Documented divergences (all annotated in file metadata)

1. **Heat conduction as semi-discrete ODEs.** The Fortran assembles and solves
   an implicit backward-Euler tridiagonal for Tsfc and the layer temperatures —
   the mushy two-stage solver (icepack_therm_mushy.F90:1800-1985) under the
   D-class ktherm = 2, with the kh conductances of the conductivity
   subroutines (icepack_mushy_physics.F90:455-485) and the per-layer absorbed
   shortwave of absorbed_solar (icepack_shortwave.F90:862-880). The .esm writes
   the equivalent energy-conserving method-of-lines form
   `d(q_k)/dt = (kh_up·(T_up−T_k) + kh_dn·(T_dn−T_k) + Iswabs_k)/hilyr`
   (volumetric-enthalpy balance, no ρ·cp factor). The stage-3 integrator
   reproduces the backward-Euler trajectory; the layer-energy and growth/melt
   rates are pinned at stage 3 once the Tsfc implicit solve is coupled.
2. **Tsfc is a parameter.** The implicit surface energy balance
   `fsurfn(Tsfc) − fcondtopn = 0` (the converged solve has fsurfn = fcondtopn,
   same sign: the `fcondtop − fsurfn < ferrmax` consistency checks of the
   mushy two-stage solver, icepack_therm_mushy.F90:535/588/834/892 with
   ferrmax = 1e-3 W m-2, icepack_therm_shared.F90:42, and the top-melt closure
   `etop_mlt = max((fsurfn − fcondtopn)·dt, 0)` of icepack_therm_vertical.F90:
   1337-1338) is transcendental in Tsfc. The esm spec does express
   implicit algebraic constraints (an expression on the equation LHS makes its
   leading unknown an algebraic unknown, src/classification.rs), but the Rust
   `esm test` runner refuses them at compile: any implicit equation hits
   `implicit_equation_refusal` ("this runtime has no algebraic solve" →
   `unsupported_construct`, src/simulate_array/compile.rs:908-912), and the DAE
   classifier only eliminates trivial algebraics `var ~ expr` (var absent from
   expr) before raising `E_NONTRIVIAL_DAE` (src/dae.rs) — so Tsfc is a free
   parameter of the thermodynamics model fed by the coupled solve. The
   algebraic residual is carried as the diagnostic equation
   `fsurf_bal = fsurfn − fcondtopn` (eq 85), pinned by the balance test at the
   dumped exit state (see the testing table).
3. **Momentum equation as continuous limit.** stepu's implicit-solve algebra
   (cca/ccb/ab2/cc1/cc2, ice_dyn_shared.F90:949-959) is solver machinery; the
   skeleton writes `m·du/dt = τa + τtilt + τo + ∇·σ − Cb·u + m·f·k̂×u` with the
   full ocean stress of dyn_finish (F90:1345-1348) and the tilt stress
   `strtltx = −gravit·m·ss_tltx` (F90:826).
4. **EVP stress evolution as relaxation ODEs.** The classic-EVP under-relaxed
   subcycle maps (ice_dyn_evp.F90:1584-1609, `arlx = 2·elasticDamp·ndte = 86.4`,
   `brlx = ndte`) are written as `d(σ)/dt = (σ_target − σ)/Td` with
   `Td = 2·elasticDamp·dt`. The four-corner (NE/NW/SW/SE) staggered stresses
   are carried per corner on the `corner` axis of the lowered 3×5 dynamics
   (the stressp/stressm/stress12 unknowns ARE the dump's newp/newm/new12
   ksub1 four-corner fields, so no corner collapse is needed).
5. **Similarity iteration unrolled to 5 fixed updates.** The Monin-Obukhov
   do-while (icepack_atmo.F90:269) is unrolled for the D-class `natmiter = 5`
   and `atmiter_conv = 0` (unset), which always runs the full 5 updates; the
   always-5 unroll reproduces the dumped reference-height exports to machine
   precision for Tref/Qref. The assembly `Control` still uses the constant
   scheme for the stresses (strairxT/strairyT stay parameters; the similarity
   stress wiring is a stage-3 concern).
6. **Dynamics physics in the coupling cap (probes) and in the dynamics file
   (lowered pins).** The kstrength = 1 Rothrock strength law
   (icepack_mechred.F90:1660-1712) and the dynamics pointwise laws — the EVP
   stress maps (`evp_stressp/m/12_update`, ice_dyn_evp.F90:1584-1609), the
   strain invariant and viscosities/replacement pressure
   (`strain_invariant_delta`, `viscosity_scale`, `bulk_viscosity`,
   `shear_viscosity`, `replacement_pressure`, ice_dyn_shared.F90:2156-2159,
   2467-2471), and the stepu ocean-ice stress (`ocean_ice_stress_magnitude`,
   `seabed_stress_coefficient` plus the waterx/watery projections, F90:817-818,
   931-937) — remain transcribed and dump-pinned in `IceCap` as algebraic
   probes (the `cice_evp_stress.csv` / `cice_evp_momentum.csv` /
   `cice_ice_strength.csv` rows reproduce to rel 1e-12 / 1e-9). The dumped
   taux/tauy there are the stepu partials `vrel·waterx/y`; the lowered
   `cice_dynamics.esm` pins the FULL dyn_finish ocean stress
   `vrel·((uocn−uvel)·cosw − …)` (F90:1345-1348) instead. The lowered
   dynamics evaluates the run's kstrength = 1 Rothrock strength per T cell
   (the same law as the cap probe, over `[i, j, ncat]`, with aice0 = 1 − aice)
   and pins it at all 15 traced cells (P = 321248.8660482337 at global
   (2,4)); an earlier revision used the Hibler kstrength ≠ 1 form there,
   which overstated P by 70% at the thick-ice cell (546804.85) and so the
   viscosities and plastic stress targets.
7. **Tracers transported as products.** The conservative forms
   `d(vicen·qicen)/dt + div(vicen·qicen·u) = 0` are the Fortran's type-2
   tracer transport (ice_transport_driver.F90:98-102; update_fields conserves
   mass·tracer, ice_transport_remap.F90:3556-3571). A product-form LHS cannot
   define an unknown under the esm equation-balance rule, so `Transport`
   carries the products themselves as states — `aTsfcn` (type 1, area
   tracer), `vqicen[i,j,ncat,ice_layer]` (type 2) and
   `vsqsnon[i,j,ncat,snow_layer]` (type 3) — advected by the same flux
   divergence as the masses (the layered ESD rule tiles the stencil over the
   passive layer axis), and recovers `Tsfcn`, `qicen_adv`, `qsnon_adv` by
   division with the update_fields floors (0, 0, −rhos·Lfresh where the
   transported mass is zero). The Thermodynamics → Transport enthalpy
   hand-off (state_to_tracers at the start of each transport step) is an
   operator-splitting sequencing step the single-period assembly cannot
   express, so `cice.esm` no longer carries the dangling
   `Thermodynamics.qicen/qsnon → Transport.qicen/qsnon` param_to_var edges;
   the transport tests set the product states through `initial_conditions`.
8. **Grid and stagger collapse.** The single-cell skeleton collapses the B-grid
   staggering (T/U points), the ANGLET POP-grid rotations of the export
   stresses (ice_import_export.F90:962-968), the `aiU` division of the
   T-point ocean-stress average (ice_step_mod.F90:1051-1072), and the tmask
   ocean-mask guards; each collapse is annotated at the affected variable.
9. **`frain` in kg/m²/s.** The cap stores `frain = Faxa_rain·med2mod_areacor`
   in kg/m²/s with no rhofresh conversion (ice_import_export.F90:556-557): the
   melt-pond volume change divides the water equivalent `meltt·ρi + melts·ρs +
   frain·dt` by rhofresh inside the pond law (icepack_meltpond_lvl.F90:158-160),
   and the ocean rain drain adds `frain·aice` directly
   (icepack_therm_itd.F90:2179). An earlier revision divided by rhofresh in the
   cap and multiplied by 1000 in `fresh`, which left the rain into the pond
   laws 1000× too small; the frain pin's Faxa_rain was inverted through that
   wrong law, so it passed circularly (ported from EqESM 7b32882).

## Bugs found in the Fortran code

| # | Location | Bug / quirk |
|---|---|---|
| 1 | `icepack_atmo.F90:463-464` (atmo_boundary_const) | `strx = tau·uatm` omits the `/wind` direction-cosine normalization — the vmag division is commented out at F90:328-329 and the active stress is dimensionally `kg/s³` (a 10 m/s wind gives a 10× stress). Transcribed as written (the stage-3 tests must pin the active code); the esm skeleton declares the honest `kg/s^3` dimension at Control.strairx/strairy and the dynamics consumes the same value with its N/m² momentum balance annotated. |
| 2 | `icepack_therm_shared.F90:90-94` (calculate_Tin_from_qin) | The Fortran aborts on a negative discriminant of the brine quadratic; the .esm skeleton cannot express the abort and carries it as a documented guard for the stage-2 tests (a negative discriminant in a dump would expose a thermodynamics inconsistency upstream). |
| 3 | `icepack_shortwave.F90:3587-3588` (shortwave_dEdd_set_eff) | `dhs = hsnlvl − fsnow·dt` subtracts the snowfall **mass flux** (kg/m²/s, F90:3511) from a snow **depth** (m) — the `/rhos` conversion is missing (bugs.md #10). The .esm reproduces the Fortran numerics by carrying the coupled flux in an m/s parameter (`fsnow_dEdd`); the branch fires in 92/1920 dumped rows but is usually masked by the `ipn·spn < puny` reset at F90:3590. |
| 4 | `ice_dyn_shared.F90:2170-2171` (strain_rates, shear corner 2) | `shear2 = −cyp·v(i−1,j) + dyT·v(i,j) − cxm·u(i−1,j) − dxT·u(i−1,j−1)` — the `+dyT·v(i,j)` term flips sign vs corner 1's all-negative `−cym·v(i,j) − dyT·v(i−1,j) − cxm·u(i,j) − dxT·u(i,j−1)` (F90:2168-2169); the corner combinations are mutually inconsistent under a uniform B-grid pattern. Transcribed exactly (the ESD `strain_shear_corner2` atom); a symmetric guess fails the dump pins. |
| 5 | `ice_dyn_shared.F90:2172-2173` (strain_rates, shear corner 3) | `shear3 = −cyp·v(i−1,j−1) + dyT·v(i,j−1) − cxp·u(i−1,j−1) + dxT·u(i−1,j)` — two sign flips vs the corner-1 pattern (the `+dyT·v(i,j−1)` and `+dxT·u(i−1,j)` terms). Reproduced exactly in the ESD `strain_shear_corner3` atom. |
| 6 | `ice_dyn_shared.F90:2174-2175` (strain_rates, shear corner 4) | `shear4 = −cym·v(i,j−1) − dyT·v(i−1,j−1) − cxp·u(i,j−1) + dxT·u(i,j)` — the `+dxT·u(i,j)` term flips sign vs corner 1's `−dxT·u(i,j−1)`. Reproduced exactly in the ESD `strain_shear_corner4` atom. |
| 7 | `ice_dyn_evp.F90:1760-1761` (stress, str_dy k7) | The NW-corner y-divergence atom weights the p/m pair sums west-dominant: `strp_tmp = p25·dxT·(p333·ssigpw + p166·ssigpe)` (F90:1754-1755) while the NE/SE atoms k5/k6 use the east-dominant `p333·ssigpe + p166·ssigpw` (F90:1748-1749) — the corner weighting is not symmetric under reflection. Reproduced exactly in the ESD `str_dy_cell_k7` atom. |
| 8 | `ice_dyn_evp.F90:1764-1765` (stress, str_dy k8) | The SW-corner atom carries the same west-dominant `p333·ssigpw + p166·ssigpe` weighting as k7 (F90:1754-1755), again inconsistent with k5/k6. Reproduced exactly in the ESD `str_dy_cell_k8` atom. |

## Delta-Eddington shortwave (`cice_shortwave.esm`) — transcription notes

The `Shortwave` model transcribes `compute_dEdd_3bd` (icepack_shortwave.F90:
1703-3013) and the per-layer solver `solution_dEdd` (F90:3022-3488) of the
`shortwave = 'dEdd'` 3-band scheme, built entirely from templates imported by
reference from `./cice_templates.esm` (the dEdd family appended at the end of
that library). Conventions:

- **Layer axis:** model layer `k` = Fortran layer `k−1`; the sea-ice surface
  scattering layer (SSL) is model layer `N_SLYR+2`, the delta layer
  `N_SLYR+3`, the fresnel layer `kfrsnl = N_SLYR+3`. All layer-branch
  conditions use `N_SLYR+2`/`N_SLYR+3` (a stage-2 Class-A fix: the first
  transcription used `N_ILYR+1/2`, which coincided with the truth only for
  the ice layers).
- **Downward interface arrays** are top-down (model iface 1 = the top,
  Fortran iface 0); **`rupdir`/`rupdif` are ocean-up** (model iface 1 = the
  ocean base `albodr`, iface `klevp = N_SLYR+N_ILYR+3` = the surface). The
  `dfdir`/`dfdif` flux fractions index `rupdir/rupdif` at `klevp+1−k`.
- **Aerosol mass path** `aero_mp` is species-major (`aero_mp(sp, slot)`,
  slots snow-SSL, snow interior, ice SSL, ice interior — the Fortran's
  `aero_mp(1:12)` with `na` stepping 4); the stage-1 dump columns are
  likewise species-major (`aero_mp_{(sp−1)*4+slot}`).
- **`ksrf`** = 2 for snow, `N_SLYR+3` otherwise; **`mu0n`** is `mu0nij`
  below the fresnel level and `mu0` above it for `srftyp < 2`.
- **Bit-level arithmetic:** `smr/smt` accumulate `mu·(rdr·gwt)` (the gwt
  multiplies rdr before the mu scaling, F90:3347-3348); the `alpha`/`agamm`
  denominators are `1 − (e·e)·(mu·mu)` (squared pair, F90:3321-3322,
  3343-3344 — the run's gfortran -O2 association; the near-pole snow band-3
  layers amplify a flat-vs-squared-pair difference to ~2e-10 relative);
  `exp(−min(10, x))` clamps extinction/transmission arguments at
  `exp_argmax = 10` (F90:3307-3308, 3317-3318, 3339-3340).
- **No ESD quadrature for the Gauss angle axis:** the 8-point Gauss-Legendre
  diffuse angular integration is an explicit sum over the 8 abscissas (an
  esm `integral` reaches evaluation only when a discretization rule lowers
  it); the downward/upward recurrences are explicit unrolled
  `faq`/`ifelse` chains over the 13 layer levels.
- **`trmin` activity cutoff** (F90:3285-3287): the Fortran skips the layer
  solution below the cutoff; here the full solution is computed and the
  outputs masked with the same condition (`active = trntdr_f > trmin`),
  which reproduces the Fortran bit-for-bit (the guard condition is a
  property of the full solution).

Transcription bugs caught by the tests (all errors in the stage-2 .esm
files, not in CICE — no `bugs.md` entries): the `tdr_g` sign in
`dEdd_direct_transmissivity` (F90:3346 is `−apg·trn + trn`); `ksrf` made
`fsfc` identically zero for snow; the `aerosol_3bd` table transposed
(species-major data under (band, aero) axes — masked by the pin curation,
surfacing as ~1e-8 residuals and localized by pinning `taer/waer/gaer`);
the `aero_mp` dump layout (species-major, not slot-major); and the
`rupdir` top-down-vs-ocean-up index convention (`dfdir(1,1) = 0.9687` vs
`0.0313`).

Coverage and gaps: pinned against `cice_dedd.csv` are the layer geometry,
snow-table IOPs, mixed `tau/w0/g`, the guard-zeroed `m_*` (incl. zero pins
below the cutoff), the downward/upward chains, `dfdir`/`dfdif`, the scalar
band sums, `fsfc/fint/fthru`, the `fthruvdr/fthruvdf` and band-3
`fthruidr/fthruidf` rows, and `Sabs`/`Iabs`/`fthrul` (tolerances rel 1e-12,
rel 1e-9 on the interface quantities — the 13-layer recurrence round-off
amplification; the band-3 near-snow-SSL algebra is the worst case, `ne`
amplifying relative error by ~1e4). Not pinned: the **pond branch**
(`srftyp = 2` — transcribed but untested, the instrumented run has no pond
rows), `fthruuvdr/fthruuvdf` and `pardr/pardf` (UV scheme and pond-area
adjustments, out of scope), the bare-group snow IOPs and `Sabs`
(identically zero), and aerosol species 4-6 (the run carries only
species 1-3; the table holds only those).

## Testing

The stage-2 `tests` blocks pin the stage-1 instrumentation dumps
(`stage1/dumps/cice/`) with instantaneous laws (`time_span {0,0}`, MOSART
pattern) plus one integrated transport trace. Run `esm test components/cryosphere/cice` for
the full suite (485 CICE assertions). The two lowered
components import the B-grid rules by reference from the
EarthSciDiscretizations checkout, so the tests (and `esm validate` of those
two files) need `export ESD_ROOT=/path/to/EarthSciDiscretizations` (the
`${ESD_ROOT}` ref expansion; without it the imports fail as
`template_import_unresolved`). ESD `main` carries every rule used (verified
at `4ea6f83`).

| file | tests | assertions | what is pinned |
|---|---|---|---|
| `cice_coupling.esm` | 40 | 69 | the import laws (areacor scaling, potT/rhoa branch wiring), the freezing-temperature law, the export state fields, the per-category albedo aggregation, the scale_fluxes `/aice` flux aggregation, the air-ice stress exports, the similarity reference-height exports Si_tref/Si_qref/Si_u10 (4 cells × 2 steps), the Rothrock strength law (2 dump rows), the EVP stress pointwise laws Delta/zetax2/etax2/rep_prs and the newp/newm/new12 subcycle maps (2 dump rows, different cells/corners/ksub), and the stepu ocean-ice stress laws vrel/taux/tauy/Cb (2 dump rows) |
| `cice_thermodynamics.esm` | 17 | 30 | the dEdd shortwave laws against `cice_albedo.csv`: the snow fraction on bare ice and snow (vsnon = 0 / > 0), the effective pond area apeffn through the infiltration, hypsometry, hpmin and taper branches, the ice/snow broadband albedos, and the shortwave conservation fswintn = swabs − fswsfc − fswthrun; the mushy enthalpy↔temperature inversions zTin/zTsn (eqs 1-2) against the `cice_thermo_state.csv` zTin_1..8/zTsn_1..3 columns (all `rel 1e-12`); the step-1 surface energy-block aggregates flwout/fsens against `cice_thermo_flux.csv` (the similarity-driven shcoef/lhcoef at the entry Tsfcn, fluxes at the exit Tsfcn, ε = 0.95; `rel 1e-9`, cells (3,5) and (2,4)); the step-1 latent-heat and sublimation/condensation aggregates flat/evap/dsnow (cell (2,4), `rel 1e-6`; the evapn `esub + econ` closure and the dsnow [m/step]→[m/s] rate convention, transcription fixes #9-#11); the step-2 radiation aggregates fswabs/fswthru testing the prep_radiation rescale `albedo_dump(1) × netsw(2)/netsw(1)` (icepack_shortwave.F90:3893-3922; `rel 1e-12`, cells (3,5) and (4,5)); and the per-category surface energy balance residual fsurf_bal = fsurfn − fcondtopn at the step-2 exit state (cell (2,4), cats 2-5, `abs 1e-2` ≈ 1.5× the largest measured residual 6.7e-3; the implicit solve's own convergence, see the balance test description) |
| `cice_shortwave.esm` | 2 | 171 | the delta-Eddington column against `stage1/dumps/cice/cice_dedd.csv` (step 1, cell (2,4), snow group ncat 2 srftyp 1 with hs = 0.15364 m, frsnw = 290.36 µm and aerosols in all four slots; bare group ncat 1 srftyp 0 with hs = 0; both at `coszen = 0.21184`, `rel 1e-12`): the layer geometry `dzk`/`frsnw`, the SNICAR-table IOPs `Qs/ws_snw/gs_snw/ks_snw`, the mixed `tau/w0/g`, the guard-zeroed layer props `m_*` (incl. pins below the trmin cutoff), the downward chain `trndir/trntdr/rdndif/trndif` at the top/bottom of band 1 and the first guarded interface of bands 2/3, the upward chain `rupdir/rupdif`, the flux fractions `dfdir/dfdif`, the scalar band sums `avdr/avdf/aidr/aidf`, `fsfc/fint/fthru`, `fthruvdr/fthruvdf` and the band-3 `fthruidr/fthruidf`, and `Sabs`/`Iabs`/`fthrul` (interface quantities at `rel 1e-9` — the 13-layer recurrence round-off amplification; see the file's README notes below) |
| `cice_dynamics.esm` | 2 | 89 | `cice_dynamics_bgrid_pins` (53, `time_span {0,0}`, `rel 1e-12`, full-domain overrides so m > 0 and DminTarea > 0 everywhere) — the lowered B-grid laws at the step-1 first-subcycle state: the four-corner strain rates divu/tension/shear at T cell (3,5) (12 values; the `strain_rates` corner combinations, ice_dyn_shared.F90:2148-2175, area-weighted m²/s), the stress integrals strintx/strinty at U(2,4) (the stepu `uarear·(str1 − str2 + str3 − str4)` sums, ice_dyn_evp.F90:1698-1765), the kstrength = 1 Rothrock strength at all 15 T cells against `cice_ice_strength.csv` (P(2,4) = 321248.8660482337; thin-ice cells 65.6–257.3 N/m), the viscosity chain Delta/zetax2/etax2/rep_prs and the plastic target stressp_target at (3,5) corners 1-4 against the ksub-1 `cice_evp_stress.csv` rows, and the full dyn_finish ocean-ice stress vrel/taux/tauy/Cb at U(2,4) with the dump's aiX/uocn/vocn (F90:1345-1348); `cice_dynamics_evp_subcycle_integrated` (36) — the coupled momentum + stress ODEs integrated over one EVP subcycle [0, 30] s (one subcycle = one backward-Euler step of dte = Td·arlx1i of the relaxation ODE) from the ksub-1 oldp/oldm/old12 and velocity, with strairx/strairy = the momentum dump's forcex/forcey and fcor = fm/umass, asserting stressp/stressm/stress12 at the three interior T cells (global (3,5..7)), corners 1-4, against the dumped newp/newm/new12 with per-assertion abs tolerance 0.6·\|newp − oldp\| (a frozen model fails every assertion; measured residuals 0.001–0.46 of the increment — the Fortran freezes the velocity during the stress update and uses the U-cell umass, the model integrates both continuously with the T-cell Tmass). Not asserted: boundary cells (halo-copy closure, residuals 1–21× the increment) and velocities (the continuous momentum ODE is not stepu's semi-implicit pseudo-time update; at (3,5) the dumped uvel increment is not reproduced even in sign) |
| `cice_transport.esm` | 4 | 109 | `cice_transport_centered_flux_35_integrated` (15) — the continuity system integrated over [0, 3600] s from the dump's t_entr state with the dump's velocity/grid parameters, compared with the exit aicen/vicen/vsnon at cell (3,7): a **scheme-difference check, not a remap pin** — the residuals ≤ 3.04e-5/3.33e-5/1.78e-4 are ~10% of the transported change (3e-4..5.5e-4 relative), and the tolerances rel 1e-4/1e-4/2e-4 are that residual rounded up (loose relative to the change; they still reject a no-transport model by 3–5×); `cice_transport_uniform_field` (1) — div_flux with a uniform aicen = 1 field = the discrete velocity divergence 1.1240071614720283e-07 1/s (rel 1e-12, integrator-independent); `cice_transport_tracers_divergence_pins` (45) — the 15 lowered divergences (masses, aTsfcn, the 4-D vqicen/vsqsnon) of the dumped step-1 t_entr state (`cice_transport_tracers.csv`) against the rule formula at an interior, an edge and a corner cell (rel 1e-12; the edge/corner pins verify the rule's halo-copy closure, not CICE behavior); `cice_transport_tracers_uniform_preservation` (48) — uniform tracers advected with the dumped masses for 3600 s stay exactly uniform (rel 1e-12; an operator-consistency test of the product/recovery formulation, which a zero-velocity model would also pass), including the snow-free qsnon floor −rhos·Lfresh |
| `cice.esm` | 1 | 17 | the coupled assembly at the step-1 export-time state (test `assembly_exports_dynamics_step1_cell3_5`, `time_span {0,0}`, `rel 1e-12`): the export chain through the coupling — the Transport→Thermodynamics/IceCap single-cell selects (faq full-map over ncat of the traced cell (2,2) = global (3,5)) and the Thermodynamics→IceCap Tsfc/albedo edges — pinned exactly against `cice_run_exports.csv` step-1 (3,5): Si_ifrac/Si_vice/Si_vsno/Si_snowh/Si_t and the albedo aggregation Si_avsdr/Si_anidr/Si_avsdf/Si_anidf (the state is `cice_thermo_state.csv` entry(2): exports(S) = entry(S+1) to round-off; Tsfc = the entry Tsfc tracer, not the solve Tsfcn — see coverage limits); the constant-scheme Control chain through the cap aggregation (Faii_taux/Faii_tauy formulation pins = strairxT/aice·areacor with strairx = tau·uatm from the step-1 (3,5) imports; the run's similarity-scheme export differs); the broadcast ocean stress and the tilt stress (Dynamics.taux/tauy at U(1,1) and U(2,2) — formulation pins vrel = aiX·rhow·Cw·\|u_ocn−u\| with the momentum-dump aiX and the broadcast step-1 uocn/vocn; strtltx/strtlty wiring pins with the run's identically-zero So_dhdx/dhdy imports) |

All 47 pre-probe coupling assertions reproduce the dumped values at the
tolerances documented per test: the imports/exports/aggregations at round-off
(`rel 1e-12`, every expected value tracing to a specific dump row (step, cell,
ncat) cited in the test description), the similarity exports (Si_tref/Si_qref
at `rel 1e-9`, machine precision) and the Rothrock strength (two dump rows at
`rel 1e-9`); Si_u10 carries a documented `rel 1e-4` gap: the uvelT_icep
reconstruction (ice_step_mod.F90:114-128, the uarea-weighted average of the
U-point uvel) reproduces the run's T-point velocity only to ~1e-4 m/s, and
Uref = |Uatm−U|·rd/rdn amplifies that difference by rd/rdn ≈ 8. The source of
the residual is unidentified (the run-side value is consumed inside
step_therm1, not dumped); the pin is kept at the observed precision rather
than tightening past it. The 22 dynamics-probe assertions (4 tests) reproduce
`cice_evp_stress.csv` and `cice_evp_momentum.csv` to round-off (`rel 1e-12`):
all probe inputs are bound from the dump rows, and a Python transcription of
the templates' laws reproduces every asserted column over all 184,320 stress
rows and 40,320 momentum rows (see "Transcription fixes found while writing
the tests" for the e_factor/epp2i/capping/Ktens fit results). The 30
thermodynamics assertions (17 tests) likewise reproduce `cice_albedo.csv`,
the `cice_thermo_state.csv` zTin/zTsn columns, and the `cice_thermo_flux.csv`
flwout/fsens (step 1, cells (3,5) and (2,4), `rel 1e-9`/`1e-6`), the step-1
flat/evap/dsnow latent and sublimation/condensation aggregates (cell (2,4),
`rel 1e-6`), fswabs/fswthru (step 2, cells (3,5) and (4,5), `rel 1e-12`),
and the per-category surface energy balance residual fsurf_bal = fsurfn −
fcondtopn (step 2, cell (2,4), cats 2-5, `abs 1e-2`; the model's diagnostic
reproduces the measured solve closure, see the balance test description) to
the documented tolerances. The 198 dynamics/transport assertions (2 + 4
tests) exercise the lowered B-grid laws: 53 dynamics instant pins reproduce
the corner strain rates, stress integrals, Rothrock strength, viscosities
and full dyn_finish ocean-ice stress at rel 1e-12 (the rules transcribe the
Fortran grid algebra exactly on the traced subdomain), 36 integrated
dynamics pins check one EVP subcycle of the stress/momentum ODEs at
scheme-difference tolerances, and the 109 transport assertions cover the
integrated continuity trace (scheme-difference tolerances), the exact
rule-formula pins of all 15 divergences, and the uniform-field and
uniform-tracer operator checks (see the table).

### Derived inputs (the raw CMEPS fields are not dumped)

The run dumps the fields *after* the import mapping (`cice_run_imports.csv`).
The raw CMEPS inputs are reconstructed by inverting the same law, and the .esm
must reproduce the dumped value:

- `Faxa_*` / `Fioo_q` = dumped import / `med2mod_areacor`. The mesh areacor ≈
  1.00033 (not 1), so the scaling genuinely bites (e.g. `flw = Faxa_lwdn·areacor`).
- `Faxa_rain` = dumped frain / areacor (frain is dumped in kg/m²/s; pinned
  with the nonzero step-2 rain rows — step 1 is rain-free).
- `Sa_ptem` / `Sa_dens` = the dumped potT / rhoa. The dump rows have
  `potT = Tair` exactly, so the run used the Sa_ptem/Sa_dens branch; the
  Sa_pbot fallback is not exercised (inverting the dumped rhoa gives
  pbot = 99250.47 Pa, which would yield potT = 270.92 K, not the dumped
  270.34 K) and carries no dump-based pin.
- Per-category flux inputs for the export aggregation (fsensn, flatn, evapn,
  swabs, flwoutn, fhocnn, freshn, fsaltn, fswthrun) are not dumped — only the
  merged `cice_flux.csv` values are. The tests use the uniform per-category
  value that makes the aicen-weighted sum reproduce the dumped `exit` value
  (`flwoutn = exit flwout + (1−emissivity)·flw` for the outgoing-longwave
  emissivity correction). The albedo and state pins use real per-category data:
  `cice_albedo.csv` outputs × the coupling-time state of `cice_thermo_state.csv`
  entry(S+1) — in the nuopc driver the export at the end of step S runs after
  step S's dynamics (step_radiation at CICE_RunMod.F90:353, coupling_prep at
  :363), so exports(S) = entry(S+1) to round-off.
- `strairxT` / `strairyT` = dumped `Faii_taux` / `Faii_tauy` × aice / areacor
  (inversion of the scale_fluxes + export chain; the pre-scale T-point stress
  is not dumped).
- Similarity-test inputs: `Sa_u`/`Sa_v`/`Sa_ptem`/`Sa_shum`/`Sa_dens`/`Sa_z`
  are the dumped imports of `cice_run_imports.csv`; `uvelT`/`vvelT` are the
  uarea-weighted averages of the four surrounding U-point uvel/vvel of
  `cice_dyn_state.csv` (phase `d_entr`, the uvelT_icep reconstruction of
  ice_step_mod.F90:114-128 with the gx1v7 HTN/HTE cell-edge lengths);
  `Tsfcn`/`aicen_init` are the entry(S) per-category states of
  `cice_thermo_state.csv` (the surface temperature and the aicen saved before
  the thermodynamics, which merge_fluxes weights Trefn/Qrefn/Urefn by) and
  `aicen` is entry(S+1) (the aice of the scale_fluxes division).

### Transcription fixes found while writing the tests

1. **scale_fluxes `/aice` division missing.** `scale_fluxes`
   (cicecore/cicedyn/general/ice_flux.F90:1565-1592) divides the aggregated
   albedos, stresses, and fluxes by the ice area aice, so the coupled exports
   are per unit ice area; the skeleton's aggregation equations omitted the
   division. Dump-proven: Si_avsdr = 0.97303 = sum(albedo·aicen)/ailohi =
   0.967465/0.994260. Fixed in `cice_coupling.esm`: the 13 aggregation
   equations and Faii_taux/tauy now divide by `aice`, with the ice_flux.F90
   line citations.
2. **Faii_lwup ifelse arity.** The outgoing-longwave fix
   (ice_import_export.F90:1149-1164) was transcribed with a malformed
   3-argument `>` (only caught at test-compile time:
   `invalid_operator_arity: operator '>' takes exactly 2 argument(s)`); rebuilt
   as `ifelse(flwout > -1e-11, -stefan_boltzmann·(Tf+Tffresh)^4/ailohi, flwout)
   · mod2med_areacor`.
3. **Tf law.** The `sea_freezing_temperature` template transcribed the icepack
   mushy liquidus, but the coupled import path (CESMCOUPLED) computes
   `Tf = shr_frz_freezetemp(sss) = max(sss/(-18.48+0.01848·sss), -2.0)`
   (share/shr_frz_mod.F90.in:94-105, ice_import_export.F90:818-821; bugs.md
   #6). Updated the template; all 384 dumped rows match the coupled law to
   round-off (the −2 °C clamp is not exercised: the run's sss < 35.64 psu).
4. **Nuopc-cap constant overrides (bugs.md #11).** The CESM nuopc cap
   (`ice_comp_nuopc.F90:415-450`) overwrites ~20 icepack parameters with
   SHR_CONST values at init: cp_ice = 2117.27 (SHR_CONST_CPICE), cp_ocn =
   3996 (SHR_CONST_CPSW), cp_air = 1004.64 (SHR_CONST_CPDAIR), zvir =
   0.6077930728241565, Lsub = 2,834,700, Lfresh = 333,700, snowpatch =
   0.005, Tocnfrz = −1.836 (rhoi/rhow/rhos/gravit/vonkar/stefan/cp_wv/
   Tffresh unchanged). The first zTin transcription used the icepack
   defaults (cp_ice = 2106, Lfresh = 334000, …) and was off by 0.3–0.4%
   against the new dump columns; with the run's constants all 8 mushy layers
   reproduce the dumped zTin to round-off. The 16 affected templates, the
   coupling model's inline zvir/cp_air (eqs 68, 69, 75), and the `Control`
   Lheat binding (`cice.esm` eq 6, Lsub) now carry the run values, with the
   cap override cited in the template descriptions.
5. **Dynamics probe pins — findings.** (a) The `cice_evp_stress.csv` corner
   quantities are area-weighted (strain rate × corner area, m²/s); the dump
   header's `zetax2 [kg/s]` is the Fortran variable's nominal unit — the
   corner value is strength/max(Delta, DminTarea) = kg/(m²·s), and the area
   factors cancel in the stress update so `zetax2·divu − rep_prs` closes as
   N/m (the probe declares the honest kg/m²/s dimension, annotated). The
   D-class constants were verified by fitting, not assumed: e_factor =
   e_yieldcurve²/e_plasticpot⁴ = 0.25 reproduces the dumped Delta from
   divu/tension/shear on all 184,320 rows, epp2i = 1/e_plasticpot² = 0.25
   reproduces etax2/zetax2, and capping = 1/Ktens = 0 reproduces
   zetax2/rep_prs — no constant mismatch found. (b) The
   `cice_evp_momentum.csv` taux/tauy columns carry the **stepu partial
   stresses** `taux = vrel·waterx`, `tauy = vrel·watery` (ice_dyn_shared.F90:
   933-935, "NOTE this is not the entire ocn stress term"), not the
   dyn_finish full form `vrel·((uocn−uvel)·cosw − …)` of F90:1345-1348 that
   `cice_dynamics.esm` eqs 26-27 transcribe (the difference is the
   −vrel·uvel term); the probe transposes the stepu form, with the
   dyn_prep2 waterx/watery rotation (F90:817-818) and `sign(1,fm)` carried
   as the `ocn_hemis` parameter (bound from the dumped fm; unobservable in
   this run since sinw = 0). (c) `TbU = 0` in every traced row (no landfast
   grounding in the traced region), so the Cb pins check the wiring with a
   zero numerator; a nonzero-Cb pin needs a landfast cell from a later run.
6. **emissivity 0.985 → 0.95.** The `surface_heat_flux` template body (both
   the `ε·flw` absorption and the `ε·σ·TsfK⁴` emission terms) and the model's
   `flwoutn` equation transcribed the icepack default emissivity = 0.985
   (icepack_parameters.F90:156), but the D-class forcing_nml overrides it to
   0.95 — the value the coupling aggregation already assumed (the cap's
   flwout sum uses `(1−ε)·flw` = 0.05·flw, icepack_flux.F90:209-211).
   Dump-proven: with ε = 0.985 the step-1 (3,5) flwout aggregate misses the
   dump by rel 3.3e-3; with ε = 0.95 it reproduces it to 6e-11. Fixed in the
   template body and description, the model's flwoutn, and the model
   metadata (the template library's constants note already recorded the
   D-class 0.95 override).
7. **freshn/fsaltn corrected rate forms.** The skeleton's `freshn` carried
   the ktherm = 1 form `2·evapn − ρi·(congel+meltb−meltt) − fsnow − ρs·melts`
   (per-step, with /dt), but the F90:510-513 law cancels the sublimation and
   new-snowfall terms exactly: `freshn = evapn − (ρi·dhi + ρs·dhs)/dt` with
   `dhi = hin − worki` (which includes −evapin/ρi) and `dhs = hsn − works −
   hsn_new` (the hsn_new snowfall cancels), leaving the rate form
   `freshn = −(ρi·(congeln + meltbn + melttn) + ρs·meltsn)`, and
   `fsaltn = −ρi·dhi·ice_ref_salinity·0.001` with the same dhi (F90:513, 521;
   no separate /dt — the per-step dt divides out). Dump-proven: at step-1
   (3,5), `Σ aicen·freshn + frain·aice` reproduces the dumped fresh to
   3e-17 (the rain term is the "let rain drain through to the ocean" line of
   icepack_therm_itd.F90:2179, frain in kg/m²/s), and
   `Σ aicen·fsaltn` reproduces the dumped fsalt exactly (ratio 1.0;
   evapin = 0 at step 1, all sublimation from snow). The per-category
   `dsnown = fsnow/ρs − meltsn + evapsn/ρs` rate law is added alongside.
8. **prep_radiation scale factor.** The step-S (S ≥ 2) thermo consumes the
   STORED step-S−1 dEdd outputs rescaled by
   `scale_factor = netsw(S)/netsw(S−1)` (icepack_shortwave.F90:3893-3922),
   with `netsw = Σ sw·(1 − al_band_ai)` computed from the grid-box-mean
   albedos `al_band_ai = Σ aicen·al_bandn` **per unit grid area** (the quirky
   aggregation of F90:3902-3922 — NOT divided by aice) and with netsw(S−1)
   the step's coupling_prep "Save net shortwave" value (the cice_flux exit
   scale_factor of CICE_RunMod.F90:618-624). Only the fswsfcn/fswintn/
   fswthrun (+ fswthrun_*) outputs are rescaled — the incoming bands and the
   albedos are not. The step-2 radiation pins reproduce the merged
   fswabs/fswthru to 1.5e-16 by feeding the model the step-1 bands × ratio
   with the unchanged step-1 albedos (the dEdd solve is linear in the input
   bands) and aggregating with the entry aicen(2) = albedo_dump(1) aicen.
9. **evapn condensation branch missing.** The skeleton's `evapn` closure used
   `esub` only, but the Fortran adds the condensation to the SAME evapn
   accumulator: the condensation closure `dhs = econ/(zqsn(1) − rhos·Lvap)`
   (icepack_therm_vertical.F90:1355-1375, econ = −flatn·dt < 0) does
   `evapn = evapn + dhs·rhos` (F90:1398-1399) exactly like the sublimation
   closure `dhs = esub/(zqsn(1) − rhos·Lvap)` (F90:1502-1521), so the net
   per-category closure is `evapn = (esub + econ)/qsub = −flatn·dt/qsub`
   (the `econ` law existed but was dead code). Dump-proven: at step-1 (2,4)
   the dump evap = +2.04e-7 kg/m²/s (net condensation over cats 2-5, flatn =
   +0.71..+0.87 W/m²) while the esub-only model gave −5.6e-8; with
   `esub + econ` the evap matches all cells (3,5) to 1.4e-3 and (2,4) to
   1.2e-7 (exit state). Fixed in `evapn` (both the snow and ice branches)
   and its variable description.
10. **Flux-merge weighting is the ENTRY aicen.** The merged `cice_thermo_flux`
    values are the icepack_flux.F90 sums evaluated at the flux merge with the
    entry aicen: merge_fluxes sums `aicen_init*xn` (icepack_therm_vertical.F90:
    3169) where aicen_init is saved before the thermo (save_init,
    ice_step_mod.F90:80) — equal to the ENTRY dump aicen, not the exit. The
    earlier (3,5) flwout/fsens pin assumed exit-weighting (the aicen remap is
    ≤ 1.8e-5 there, so exit-weighting still approximates the merge to ~1e-10);
    the (2,4) pins use the entry aicen explicitly. Dump-proven at (2,4) (aicen
    remaps up to 3.7e-4 relative): flwout with entry weights is off the dump
    by 2.6e-9 vs 4e-6 with exit weights; flat 1.0e-7 vs 9.9e-5; fsens 3.7e-8
    vs 1.9e-6. The remaining residual mechanism for the surface-flux columns:
    the merged values are evaluated at the converged-solve Tsfc, and the
    exit-dump Tsfc differs from it by ~1e-7..3e-6 K (the linear_itd tracer
    remap, icepack_therm_itd.F90:94-719), which is what the `rel 1e-6`
    tolerances cover.
11. **dsnow dump units are [m/step], not [m/s].** The volume tendencies
    (dsnow, and by extension congel/meltb/meltt/melts) are accumulated over
    the step in the dump, while the .esm laws are continuous rates, so the
    expected value is `dump/dt` (dt = 3600 s). Without the division the (2,4)
    dsnow pin misses by factor 3600. Documented in the test description and
    the "Units" section.
12. **meltsn bare-ice guard.** The skeleton's `meltsn = etop_mlt/(qsnon_top·dt)`
    divides by the top snow-layer enthalpy even for categories with no snow:
    at (2,4) cat 1 (bare ice, vsnon = 2.8e-15) the model's kh_top =
    2·kslyr/hslyr diverges as hslyr → 0 and the model's (unconverged)
    etop_mlt becomes huge, poisoning dsnown. The Fortran clamps the snow
    melt to the existing snow: `dhs = max(−dzs(k), etop_mlt/zqsn(k))`
    (F90:1530), which pins the melt of a bare-ice category to ~0; the .esm
    mirrors the branch with the hs > puny guard (the same condition as the
    condensation/sublimation snow-first cascade, F90:1338-1340). Dump-proven:
    at (2,4) the solve converged (dump fsurf − fcondtop = −6.9e-9) so the
    top-melt energy etop_mlt = 0 and the dump dsnow = 2.8361604414965248e-06
    m/step equals the accumulated evapsn/rhos exactly (melts has no dump
    column); the guarded dsnow reproduces the dump to 1.1e-7.
13. **Tsfc balance sign in the descriptions.** The model equations always
    carried the correct surface balance — the etop_mlt closure was
    `max((fsurfn − fcondtopn)·dt, 0)` (icepack_therm_vertical.F90:1337-1338)
    — but the file description and the Tsfc parameter description stated the
    balance as `fsurfn + fcondtopn = 0`. The converged implicit solve has
    fsurfn = fcondtopn with the SAME sign (the downward-positive conductive
    flux enters the surface heat budget as −fcondtopn; the two-stage
    consistency checks are `fcondtop − fsurfn < ferrmax`,
    icepack_therm_mushy.F90:535/588/834/892). Dump-proven: the merged dump
    fsurf/fcondtop at (2,4) steps 1-3 are equal to round-off (−2.1211666
    both at step 1, −4.020587 both at step 2, −4.241307 both at step 3),
    and the per-category balance fsurfn − fcondtopn computed from the
    step-2 exit state closes to 6.8e-4..6.7e-3 W m-2 while the sum would
    read 2×fcondtopn ≈ −29 W m-2. Fixed in the two description texts; the
    new diagnostic equation `fsurf_bal = fsurfn − fcondtopn` (eq 85) and
    its balance pin (test `thermo_surface_balance_step2_cell2_4`) carry the
    corrected convention.

### Coverage limits (why the other files have no tests)

- **Thermodynamics re-transcribed to the D-class configuration.** The first
   stage-2 skeleton transcribed the icepack namelist defaults (BL99 7/1,
   bubbly, ccsm3 albedos, cesm pond), which the run does not exercise: the
   D-class run (stage1/cime/cases/D_cice_inst/run/ice_in) used ktherm = 2
   (mushy) with nilyr = 8/nslyr = 3, conduct = MU71, shortwave = dEdd,
   frzpnd = hlid, kstrength = 1 (Rothrock), and atmbndy = similarity. The
   thermodynamics model and templates now transcribe the D-class laws, and the
   dEdd surface laws are dump-pinned. Pinned in this file: the dEdd surface
   laws (snow fraction, effective pond area, broadband albedos, radiation
   conservation), the mushy enthalpy↔temperature inversions `zTin =
   icepack_mushy_temperature_mush(qicen, zSin)` (eq 1) and `zTsn =
   snow_temperature_from_enthalpy(qsnon)` (eq 2) against the dumped
   `cice_thermo_state.csv` zTin_1..8/zTsn_1..3 columns, the step-1 surface
   energy-block aggregates flwout/fsens (tests
   `thermo_surface_fluxes_step1_cell3_5`, `thermo_surface_fluxes_step1_cell2_4`),
   the step-1 latent-heat and sublimation/condensation aggregates
   flat/evap/dsnow (test `thermo_sublimation_condensation_step1_cell2_4` —
   the `esub + econ` evapn closure of thickness_changes, the exit-state
   qsub evaluation, and the [m/step]→[m/s] dsnow convention, transcription
   fixes #9-#12), the step-2 radiation aggregates fswabs/fswthru
   through the prep_radiation rescale (tests
   `thermo_radiation_scale_step2_cell3_5`, `..._cell4_5`), and the
   per-category surface energy balance residual fsurf_bal = fsurfn −
   fcondtopn at the step-2 exit state (test
   `thermo_surface_balance_step2_cell2_4`: cats 2-5, `abs 1e-2`; cat 1 is
   bare at step 2, vsnon = 0, where the .esm kh_top diverges while the
   Fortran switches to the bare-ice branch kcstar(1) = km(1),
   calc_intercell_conductivity F90:2038-2051). Remaining unpinnable from
   the stage-1 dumps: the vertical
   conduction ODE trajectories (blocked: the per-layer Iswabs/Sswabs are
   never dumped and every traced row is daytime — coszen 0.158..0.572,
   fswintn 2..106 W/m² (cice_albedo.csv) comparable to the conduction
   fluxes — so no step has a zero-shortwave conduction-only trajectory to
   compare; the growth/melt
   rates likewise depend on the solve-internal zTin(8)), the merged ocean
   flux aggregates fhocn/fresh/fsalt (the step-2 cells are contaminated by
   lateral melt, icepack_therm_itd.F90:1016-1127, and congel/meltbn depend
   on the solve-internal zTin(8) — every dumped zTin variant exceeds Tbot so
   the melt/basal closures are not exercised in the dump; meltt = the solver
   residual 3.35e-20 at (2,4); melts has no dump column), the step-1 balance
   (the step-1 thermo consumed the init-time dEdd solve, init_shortwave
   CICE_InitMod.F90:192-201, which the dumps do not contain — the step-1
   albedo-dump shortwave leaves the residual at ~−15 W/m²), the step-2 flat
   (the history-file uvel differs from the actual dynamics velocity by rel
   17%), and dsnow at cells (2,6)-(2,8) where the surface-energy solve did
   NOT converge (dump fsurf − fcondtop ≈ +0.3 W/m² → top melt; needs the
   solver residual). The fresh rain term of icepack_therm_itd.F90:2043 is
   verified numerically to 3e-17 but the freshn/fsaltn laws are pinned only
   as documented rate forms — their dump agreement at step 1 is exact by
   construction of the cancellation, see transcription-fix 7.
- **Tsfc tracer (dump bug, now fixed).** The first instrumented run read
   the `nt_Tsfc`/`nt_qice`/`nt_qsno` tracers with the j and tracer indices
   swapped (`trcrn(i,nt,j,n,blk)` vs the declared `(i,j,nt,n,blk)`), so
   Tsfc/Tsfcn/qice/qsno read 0 in every `cice_thermo_state.csv` row and
   Tsfcn/alvl/apnd/hpnd/ipnd read 0 in `cice_albedo.csv`. Fixed in the
   instrumented fork (`ced43eb`, superproject `c8a3bef`; rerun job
   11864874) — the columns now carry physical values (Tsfc ≈ −14.7 °C,
   qice_1 ≈ −3.03e8 J/m3) and the Si_t export is pinned against them
   (test `icecap_export_sit_step1_cell2_4`).
- **Spatial-D lowering landed; what remains deferred.** The dynamics and
   transport rewrite targets are now lowered by the EarthSciDiscretizations
   CICE B-grid rules (`grids/cice_bgrid`, ESD `main`) and carry
   their own dump pins (89 + 109 assertions, see the testing table). The
   **assembly** now couples them and runs a 17-assertion instant pin of the
   step-1 export-time state (see the testing table): the 31 shape-mismatched
   `variable_map` edges (3×5 dynamics/transport → single-cell
   thermodynamics/coupling) carry faq full-map broadcast and single-cell
   select transforms — `param_to_var` breaks the receiving var_map
   ("array state has no cells in var_map") for any scalar→shaped edge, and
   the native compiler additionally requires the select as a full-rank index
   inside the faq (a bare partial `index` yields a sub-array and is refused,
   esm-libraries-spec §2.5.10), so each select edge is
   `faq(output_idx: [ncat], expr: index(From.var, 2, 2, ncat), ranges: {ncat})`
   with the traced-cell constants (2,2) = global (3,5). What stays deferred:
   a whole-coupling-period trace from a cold start (stage 3), a
   velocity pin of the momentum ODE (the one-subcycle integrated test pins
   the stresses only: the continuous m·du/dt is not the Fortran's stepu
   semi-implicit pseudo-time update, whose cca/ccb/ab2/cc1/cc2 machinery is
   documented rather than transcribed), the aiX
   derivation (the ocean-ice stress consumes the dump's aiX = the cap's
   aice_init-based concentration, ice_dyn_shared.F90:928-930 — the 4-cell
   U-point average of the model aicen misses the cap value by up to 2.6e-3,
   so aiX stays a dump parameter), the ridge redistribution (the Rothrock
   strength is now evaluated and pinned in the dynamics file), and the
   incremental-remap departure-cell
   discretization of the transport (the rule's centered edge reconstruction
   is the continuous flux form; the scheme difference is quantified by the
   transport pin tolerances). The dynamics pointwise laws additionally
   remain pinned in the coupling cap (see divergence 6).
   `cice_dyn_state.csv` continues to feed the similarity tests through the
   uvelT/vvelT reconstruction.
- **Assembly pins: what the single-cell skeleton cannot reproduce.** The
   assembly test pins the export-state chain, the ocean/tilt stress, and the
   constant-scheme Control chain (see the testing table). Deliberately
   excluded: the flux exports (Faii_lwup/sen/lat/evap, Fioi_swpen/melth/
   meltw/salt) — the run's merged fluxes are evaluated at the converged-solve
   Tsfcn (the exit Tsfcn is ~0.7 K warmer than the entry Tsfc tracer the Si_t
   export aggregates), and the skeleton carries a single Tsfc parameter, so
   the two chains cannot both be exact; the flux chains stay pinned at the
   component level (thermo merged aggregates, cap constructed-input exports);
   Faii_swnet at step 1 (the init-time dEdd solve of CICE_InitMod.F90:192-201
   is not dumped); Fioi_taux/tauy (the collapsed T-point average of
   strocnxU/aiU of ice_step_mod.F90:1051-1072 does not reproduce the dumped
   export); and the similarity exports (uvelT reconstruction, a stage-3
   concern). The dynamics Control→Dynamics strairx/strairy and
   shcoef/lhcoef broadcast edges enter only the momentum/energy ODE rates, so
   they are compile-exercised but not instant-pinned.
- **fswthru merge timing.** `merge_fluxes` weights fswthrun by the mid-thermo
   aicen (icepack_therm_vertical.F90:3169), which is not a dumped state; a
   per-category fswthru pin misses the dump by 0.1-18%, so Fioi_swpen uses the
   uniform construction. The per-category fswthrun of `cice_albedo.csv` stays
   available for the stage-3 dEdd tests.
- **Si_t, the Sa_pbot branch, and the lwup fix branch** are unpinned (Tsfc
   tracer not dumped; pbot branch not exercised by the run; flwout < −puny on
   the ice-covered cell so the outgoing-longwave substitution never fires).
- **Per-band Fioi_swpen_vdr/vdf/idr/idf** are dumped, but the stage-2 skeleton
   carries them as deferred zero parameters; `cice_budget.csv` has a single
   diagnostics row (hemispheric budgets are a stage-3 assembly concern).

`esm validate` passes on every file (with `ESD_ROOT` exported for the two
lowered files); `esm test components/cryosphere/cice` (Rust CLI 0.12.1, ESD
`main`) runs the 485 CICE assertions (69 coupling + 30 thermodynamics +
171 shortwave + 89 dynamics + 109 transport + 17 assembly) with 0 failures
and 0 errors — 485P/0F/0E.

## Transport scheme

`cice_transport.esm` is **not** CICE's incremental remapping. CICE advects
the area, volumes and tracers with the incremental-remapping scheme of
Dukowicz & Baumgardner (2000) / Lipscomb & Hunke (2004)
(`horizontal_remap`, ice_transport_remap.F90:317-831: a limited linear
reconstruction in each cell, departure regions traced back along the corner
velocities, and the transport integrals over those regions). That scheme is
upwind-biased, keeps the masses non-negative, and keeps the tracers within
the range of their neighbors.

What the `.esm` carries is the continuous flux form of the same
conservation laws, lowered by the ESD `cice_bgrid` rules to a **centered**
conservative flux divergence: each face flux is the face-average velocity
times the face-average of the two adjacent cell values. It conserves mass
and tracer·mass exactly, but:

- **No positivity guarantee.** A centered flux can pull more out of a cell
  than it holds, so an integration can drive aicen/vicen/vsnon (and the
  tracer products) negative near sharp ice edges or with large Courant
  numbers. The tracer recovery `ifelse(mass > 0, product/mass, floor)` only
  covers the exactly-zero-mass case; it does not repair negative masses.
- **No monotonicity.** Centered fluxes are dispersive and can create new
  tracer extrema (over/undershoots of Tsfcn, qicen, qsnon).
- **Scheme difference against the dump.** At the traced interior cell the
  centered result misses the dumped remap exit state by ~10% of the
  transported change (test `cice_transport_centered_flux_35_integrated`);
  over the whole traced domain the worst-case relative residuals are aicen
  4.0e-4, vicen 3.7e-4, vsnon 4.8e-4, Tsfcn 2.2e-3, qicen 2.1e-4, qsnon
  9.9e-6, each larger than a tenth of the field's transported change. So
  the other transport tests pin the **operator** (exact rule-formula pins,
  uniform-field and uniform-tracer checks), not the remap trajectory.

EarthSciDiscretizations has upwind, flux-limited, PPM and WENO rules only
for the 1-D Cartesian grids; there is no upwind or limited face rule for
`cice_bgrid` to swap in. Writing the incremental remap (or a limited
upwind face rule) is ESD work, and it is listed under
[Next steps](#next-steps-stage-25--stage-3). Until then this component is
fine for the short, smooth-field pins here, but it is not safe for long
integrations or sharp ice edges without a positivity fix.

## Cross-runner status

Measured on 2026-11-20 with `ESD_ROOT` set to EarthSciDiscretizations `main`
(`4ea6f83`):

| file | Rust `esm test` (0.12.1) | Julia tree-walk (`EarthSciAST.run_inline_tests`, EarthSciAST.jl 0.12.1, OrdinaryDiffEqRosenbrock) |
|---|---|---|
| `cice.esm` | 17/17 | 17/17 |
| `cice_coupling.esm` | 69/69 | not run here; known not to finish within a 40-min CI shard (algebraic, 166 observeds: 16e9 allocations, 5.6 GB) |
| `cice_thermodynamics.esm` | 30/30 | 30/30 |
| `cice_shortwave.esm` | 171/171 | does not finish: killed after RSS passed 40 GB at ~6.5 min |
| `cice_dynamics.esm` | 89/89 | 0/89 — `E_TREEWALK_GEOMETRY_SETUP` (see below) |
| `cice_transport.esm` | 109/109 | 109/109 |

Two cheap fixes in this revision got two files past the Julia walker without
changing their meaning or their Rust results:

- `Thermodynamics.kslyr` (`[ncat]`) used to be set to a bare scalar const,
  which the walker stored as a 0-D const array (`E_TREEWALK_CONSTARRAY_NDIM`
  on `index(kslyr, ncat)`). It is now an explicit full-map `faq` broadcast of
  the same constant. Thermodynamics went from 30 errors to 30/30.
- `Dynamics.sigma12 = stress12` was a bare alias of a shaped state, which the
  walker refuses (`E_TREEWALK_UNSUPPORTED_SHAPE: sigma12`). It is now
  `1.0·stress12`. With only this change the pre-Rothrock dynamics passes
  19/19 in Julia.

**Still blocked: the Rothrock chain in the Julia walker.** The per-cell
Rothrock chain (aice0, Gsum, participation, …) depends only on parameters,
so the walker classifies it as setup-time geometry. Its geometry evaluator
then refuses the chain's `ifelse`/full-map `faq` operands
(`E_TREEWALK_GEOMETRY_SETUP: operand must be a build-time array …`; the whole
file reports `MethodError: no method matching iterate(::IndexSetRef)`). The
same constructs evaluate fine in the walker when they are not
parameter-only. This is an EarthSciAST.jl walker gap, not a defect in the
file, so the Rust runner remains the reference for `cice_dynamics.esm`. The
coupling and shortwave files are walker scalability limits.

## Scheme gaps (continuous ODE vs Fortran discrete)

- The Fortran's backward-Euler tridiagonal, the stepu implicit solve, and the
  EVP subcycle iteration become ODEs; the discrete-equivalent trajectories are
  matched at stage 3 through the integrator and the discretization templates.
- The incremental-remapping advection (departure points, transport integrals,
  the category-0 open-water mass) is a discretization, not a pointwise law;
  the skeleton carries its continuous continuity system lowered to a
  centered flux divergence, with no positivity guarantee (see
  [Transport scheme](#transport-scheme)).
- The ridge redistribution (ridge_shift, icepack_mechred.F90:1068+), the
  salinity-profile module (zSin is a prescribed parameter with the 'constant'
  profile), the melt-pond tracers hpnd/apnd/alvl (prescribed parameters), and
  the wave/aerosol/isotope tracers are deferred. (The delta-Eddington
  shortwave solver is ported in `cice_shortwave.esm`; the Rothrock strength
  law is transcribed in `Dynamics` and the coupling cap, the similarity atmo
  boundary layer in the coupling cap; the assembly `Control` atmo scheme
  remains the constant branch.)
- The `Si_imask` ocean mask is a grid field (deferred on the single-cell
  skeleton).

## Next steps (stage 2.5 / stage 3)

1. Reconcile any transcription mismatches the assembly pins expose; the
   assembly instant pins cover the export, ocean-stress, tilt-stress, and
   constant-scheme Control chains at the step-1 export-time state, and the
   deferred assembly items are: the single-cell selects' traced-cell choice
   (2,2) = global (3,5) is a skeleton constant, the momentum-ODE rate
   (strairx/strairy enter only the ODE, not an instant pin), and the
   whole-coupling-period trace from a cold start (stage 3).
2. Write the incremental-remap discretization (limited linear
   reconstruction, departure cells, transport integrals) — or at least an
   upwind/limited face rule for the `cice_bgrid` grid — in
   EarthSciDiscretizations, so the transport recovers CICE's positivity and
   monotonicity (the B-grid strain-rate, stress-divergence and centered
   transport rules this component uses have merged: EarthSciDiscretizations
   PRs #50 and #59).
3. Wire the Tsfc implicit solve; mount the full B-grid on the real grid;
   derive aiX from the model aicen; wire the Thermodynamics → Transport
   enthalpy hand-off once the assembly can express operator splitting.
4. Couple CICE with the other components in the top-level `eqesm.esm` model
   and integrate with `github.com/earthsciml/earthsciintegrator`.
