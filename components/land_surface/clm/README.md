# CLM soil and bare-ground components — stage 2 `.esm` port

Stage-2 implementation of the CTSM/CLM snow/soil temperature physics and the
bare-ground surface fluxes (ctsm5.4.063, cesm3.0-alphabranch; checkout
`stage1/cesm/components/clm`) as esm 1.3.0 files: the pointwise laws of
`BareGroundFluxesMod.F90` and `FrictionVelocityMod.F90` (MoninObukIni,
FrictionVelocity, StabilityFunc1/2) for the non-exposed-vegetation patches,
the `SoilTemperature` heat-conduction PDE on the EarthSciDiscretizations
`column_nonuniform_1d` grid with the `SoilThermProp` thermal-property laws,
the CLM top-row finite-volume measure in a local discretization rule, and the
`SoilFluxesMod.F90:SoilFluxes` ground energy/moisture flux update. The shared
pointwise laws are factored into the expression-template library
`clm_templates.esm`; the `tests` blocks pin the stage-1 instrumentation dumps
(`stage1/dumps/clm/`) — see [Testing](#testing).

All model logic lives in `.esm` files; this README is the human-readable map.
The `stage1/...` paths cited throughout refer to the EqESM project repository
(the CESM checkout instrumented to produce the dump tuples the tests pin),
where these files were developed and reviewed in `stage2/`. Sources:
`stage1/cesm/components/clm/src/biogeophys/BareGroundFluxesMod.F90`,
`FrictionVelocityMod.F90`, `SoilTemperatureMod.F90`, `SoilFluxesMod.F90`,
`QSatMod.F90`, `clm_varcon.F90` (constants), the parameter file
`ctsm60_params.c260518.nc`, and the traced case namelist
`stage1/cime/cases/I2000Clm60Sp_clm_inst/run/lnd_in`.

## File map

| File | Contents | Fortran source |
|---|---|---|
| `clm_templates.esm` | Expression-template library (36 templates: the subset of the stage-2 library used by these components — the QSat laws, the Monin-Obukhov surface-layer laws of the bare-ground fluxes, the Meier2022 roughness laws, the soil/snow thermal laws and the SoilFluxes laws; see [The template library](#the-template-library)) | `BareGroundFluxesMod.F90`, `FrictionVelocityMod.F90`, `SoilTemperatureMod.F90` (SoilThermProp :604-903), `SoilFluxesMod.F90`, `QSatMod.F90`, `clm_varcon.F90` |
| `clm_bareground_step.esm` | Model `BareGroundStep` — **one** pass of the stability do-while of BareGroundFluxes, authored once and mounted 3× (esm-spec §4.7): the three profile heights zldis_u/zldis_t/zldis_2m, ustar/temp1/temp12m from the four-branch profile templates (zeta passed in), temp2 = temp1 and temp22m = temp12m (equality branches), tstar/qstar, the Meier2022 z0h, thvstar (virtual_potential_scale), zeta_raw, the stability clamp (clamp_zeta), wc (0.333 exponent, base nondimensionalized; unconditional — see divergences), um (monin_obukhov_initial_wind) and obu; 17 equations | `BareGroundFluxesMod.F90:342-388` |
| `clm_bareground.esm` | Model `BareGroundFluxes` — the derived inputs (ur, dth, dqh, dthv, z0mg, zldis), the MoninObukIni initialization (um_ini, rib, zeta_ini, obu_ini), the exit state (= step3 outputs), and the flux laws: ram/rah/raw, raih, forc_esat/forc_e/forc_dewpoint, the raiw selection, ram1, cgrnds/cgrndl/cgrnd, taux/tauy (wind_stress_component), eflx_sh_grnd/soil/snow/h2osfc (sensible_heat_flux), qflx_evap_soi/ev_snow/ev_soil/ev_h2osfc (evaporation_flux), t_ref2m/q_ref2m (ref2m_profile)/qsat_ref2m (qsat_qs)/rh_ref2m, kbm1; 45 equations + top-level mounts step1..step3 and 66 `variable_map` couplings (19 update-invariant fields × 3 steps feed every mount; um/obu/z0h thread the state with 9 chained edges; the zldis and wc chains are dropped as dead) + 5 tests | `BareGroundFluxesMod.F90:325-329,331,342-388,396-499` |
| `clm_soiltemp_discretization.esm` | ESD-format rewrite rule `varcoeff_face_laplacian_lev_flux_bc_capr` (priority 11): the conservative variable-coefficient vertical diffusion `D(K·D(u, lev), lev)` of `varcoeff_face_laplacian_lev_flux_bc` with the CLM top-row measure `M = 0.5·(ze[NLEV+1] − zc[NLEV] + capr·(ze[NLEV+1] − zc[NLEV−1]))` in place of `dz[NLEV]`; imports the two ESD stencils by reference | `SoilTemperatureMod.F90`: ComputeHeatDiffFluxAndFactor :1895, SetMatrix_Snow :2617-2710 |
| `clm_soiltemp.esm` | Model `SoilTemperature` — the heat-conduction PDE `cv·∂T/∂t = dz·D(K·D(T,lev),lev) + sabg` with the state T, the SoilThermProp property laws (consuming `t_entry`, as in CLM), the harmonic-mean interface conductivities on the face axis, the linearized surface flux `kdudz_top = hs + dhsdT·(T[NLEV] − t_entry[NLEV])`, the bottom flux `kdudz_bot = eflx_bot`, the observeds `fn_esd`, `dTdt`, `cn_balance`; 3 tests × 202 pinned/derived assertions | `SoilTemperatureMod.F90`: SoilThermProp :604-903, ComputeGroundHeatFluxAndDeriv :1545-1798, the implicit solve :1825-2859 |
| `clm_soilfluxes.esm` | Model `SoilFluxes` — the full SoilFluxes update, 32 equations (the top-layer water h2osoi_liq+h2osoi_ice is named once as the `h2osoi_top` intermediate, shared by the evaporation limit and the partition); the shared laws imported by reference from `clm_templates.esm`; 4 tests | `SoilFluxesMod.F90`:38-518 |

The parent `clm_bareground.esm` imports `./clm_templates.esm` by reference;
no law is duplicated. The 3-mount composition mirrors the cmeps_aoflux
precedent: top-level mounts are required because the pinned CLI drops
couplings in the single-top-level-model build path.

## The template library

`clm_templates.esm` carries the 36 pointwise laws these components share
(the stage-2 library subset they import):

- **QSat laws** (`qsat_esat`, `qsat_qs`, and the shared ninth-order power-sum
  `poly8`): the Flatau et al. (1992) saturation vapor pressure/specific
  humidity fits of `QSatMod.F90:18-103`.
- **Monin-Obukhov surface-layer laws** (bare-ground fluxes): the Paulson
  (1970) stability functions — the scalar one (`stability_func_scalar`) is
  the CMEPS `psixhu_unstable` law of `flux_atmocn_Large.F90:164`, inlined
  here byte-identical from the stage-2 `cmeps_templates.esm` until the cmeps
  bulk-flux component is ported, at which point this library will import it
  by reference (esm-spec §9.7.3); the momentum one (`stability_func_momentum`)
  is authored fresh because its constant is SHR_CONST_PI·0.5 while the cmeps
  `psimhu_unstable` hard-codes 1.571, with the `chik = sqrt(sqrt(1-16·ζ))`
  intermediate factored as `stability_chik`. The MoninObukIni initialization
  laws (`monin_obukhov_initial_wind`, `bulk_richardson`,
  `monin_obukhov_initial_zeta` through the shared `clamp_zeta`), the
  four-branch friction-velocity profile laws (`friction_velocity_momentum`,
  `friction_velocity_scalar`, taking the stability parameter ζ as a parameter
  and sharing the stable branches as `stable_profile_integral`), the Meier2022
  roughness laws (`z0hg_meier2022`, `z0mg_meier2022_snowmelt`), the Magnus
  dewpoint law, `virtual_potential_scale` (shared by dthv and thvstar) and
  the BareGroundFluxes flux laws (`sensible_heat_flux`, `evaporation_flux`,
  `wind_stress_component`, `ref2m_profile`).
- **Soil/snow thermal laws** (soil temperature): `snow_bulk_density`,
  `snow_thermal_cond_sturm1997` (with the float32-rounded coefficients of
  EqESM bugs.md #33), `snow_heat_capacity` (with the thin-layer floor),
  the Johansen (1975) soil conductivity in named-intermediate form
  (`soil_saturation_water_content`, `kersten_number`, `soil_liquid_fraction`,
  `soil_saturated_thermal_cond`, `soil_thermal_cond`), the de Vries (1963)
  soil heat capacity, and the harmonic-mean interface conductivity
  `clm_interface_conductivity` with the zero bottom boundary.
- **SoilFluxes laws**: `ground_temperature_blend` (the t_grnd0/lw_grnd
  blends), `stefan_boltzmann_emission` (emg·sb·T⁴),
  `flux_temperature_correction` (pre + tinc·deriv, the five flux corrections)
  and `stefan_boltzmann_emission_dT` (4·emg·sb·T³).

The remaining stage-2 shared laws (canopy interception/storage/excess, the
ZengWang2007 vegetation roughness and displacement, the emissivities, the
latent heat of vaporization, the Jordan1991 snow conductivity, the albedo
and shortwave laws, the atmospheric density `rhos`) will be added to this
library as their components (`clm_canopy.esm`, `clm_surfalbedo.esm`,
`clm_atm_forcing.esm`) are ported.

## Components

### Bare-ground turbulent fluxes

The traced configuration (the `I2000Clm60Sp_clm_inst` case): `z0param_method
= 'Meier2022'`, `use_z0m_snowmelt = .true.`, `zetamaxstable = 2.0`,
`soil_resis_method = 1`, `do_soilevap_beta` inactive, GSWP3 forcing heights
30 m, `wind_min = 1.0` m/s, and the Meier2022 constants of
`ctsm60_params.c260518.nc` (`beta_param = 7.2`, `nu_param = 1.5e-5` m²/s,
`b1_param = 1.4`, `b4_param = −0.31`, `meier_param1 = 0.23`,
`meier_param2 = 0.08`, `meier_param3 = 70`; `zetam = 1.574`, `zetat = 0.465`;
`zii = 1000` m, `beta = 1`). The run is the single-clump column experiment of
the EqESM stage-2 plan (16 patches on 16 columns, bare, deep snowpacks,
dtime = 1800 s), `niters = 3`.

The esm has no loop construct, so the stability do-while of
`BareGroundFluxesMod.F90:342-388` is represented compositionally: the
17-equation update law is authored **once** in the one-step model
`BareGroundStep` (`clm_bareground_step.esm`) and mounted three times by
reference as top-level models `step1..step3`, with the chained inputs
coupled by `variable_map` (um_ini/obu_ini/z0mg seed step1; each step's state
feeds the next). The parent keeps the external names of the Fortran locals:
ustar/temp1/temp2/temp12m/temp22m/z0h/um = the step3 outputs (the exit state
of the 3-iteration loop).

### Soil temperature

CLM advances the snow/soil temperatures with the implicit Crank-Nicolson
solve of SetMatrix_Soil/SetMatrix_Snow on the tridiagonal row system
(`cnfac = 0.5`, `capr = 0.34`, `dtime = 1800 s`,
`snow_thermal_cond_method = 'Sturm1997'`, `nlevgrnd = 25`, `snl = −9` on the
traced columns, `use_excess_ice = .true.` with zero excess ice,
`frac_sno_fluxes = 1`, `eflx_bot = 0`, `imelt = 0` on every traced row). The
`.esm` model is a genuine PDE — `cv·∂T/∂t = dz·D(K·D(T, lev), lev) + sabg`
with the state `T` — whose spatial operator, evaluated at the pinned states,
reproduces the CLM row system; it is **not** a transcription of the
tridiagonal matrix rows.

- **Mapping.** ESD lev n = CLM j = 26 − n (lev 1 = deepest soil layer
  j = 25, lev 34 = top snow layer j = −8), with the interface coordinates
  `ze[n] = −zi(26 − n)` and the layer centres `zc = column_cell_center(ze)`.
  The grid's `lev` axis runs bottom → top as the rule requires.
- **Operator.** `D(K·D(T, lev), lev)` is lowered by the local rule
  `varcoeff_face_laplacian_lev_flux_bc_capr` (priority 11, one above the ESD
  `varcoeff_face_laplacian_lev_flux_bc`) to the CLM flux differences:
  interior rows `(G[n+1] − G[n])/dz[n]` with the interface fluxes
  `G[n] = K[n]·(u[n] − u[n−1])/(zc[n] − zc[n−1])` (the ESD stencil
  `interface_flux_K_lev`), the bottom row `(G[2] − kdudz_bot)/dz[1]`, and the
  top row `(kdudz_top − G[NLEV])/M` with the **capr-weighted measure**
  `M = 0.5·(ze[NLEV+1] − zc[NLEV] + capr·(ze[NLEV+1] − zc[NLEV−1]))` of
  ComputeHeatDiffFluxAndFactor :1895 (M = 0.01002979145516516 m in the traced
  column; A ≡ M/dz[NLEV] = 0.643828751513956). The model multiplies the
  lowered divergence by the *dumped* layer thickness `dz` (the top layer's
  dumped dz differs from the grid spacing ze[NLEV+1] − ze[NLEV]; EqESM bugs.md
  #34) and adds `sabg`. The whole RHS `F(u)` is the model-local template
  `soil_heat_tendency(u)`, applied once to the state `T` (the `dTdt`
  observed) and once to the CN mean `t_avg` (the `cn_balance` observed), so
  the operator is authored in one place.
- **Boundary fluxes.** `kdudz_top = hs + dhsdT·(T[NLEV] − t_entry[NLEV])`
  (the surface flux linearized about the entry state) and `kdudz_bot =
  eflx_bot` (0 in the traced run).
- **Properties.** The SoilThermProp laws are plain array equations over `lev`
  consuming the entry state `t_entry`; the layer masks come from
  metaparameters (`is_snow` over N_SNOW_MAX = 9 snow layers, `is_bedrock`
  over the nbedrock = 20 bottom layers). `thk` composes the Sturm1997 snow
  law and the Johansen (1975) soil law with the named intermediates `satw`,
  `dke`, `fl`, `dksat`. The interface conductivities `K` are the harmonic
  mean gathered over the face index set: `K[n] = tk(26−n)` for n = 2..34,
  K[1] = 0 (the zero bottom boundary of :828), K[35] = 0 dummy above the top
  layer.

**Known gap for stage-3 integration.** Because CLM's top row is *fully
implicit* in `dhsdT`, a Crank-Nicolson integration of this PDE by the
stage-3 coupled integrator (earthsciintegrator) will **not reproduce CLM's
top row exactly**: the plain CN average evaluates the linearized surface
flux with the `(1 − cnfac)` weighting CLM does not use at the top. Rows 2..34
match a CN integration exactly; the top-row mismatch is a deliberate
transcription of the F90, so the stage-3 comparison against CLM must tolerate
it on the top snow layer.

**eflx_bot sign.** The F90 comment at the eflx_bot declaration says
"+upward" while the `fn(nlevgrnd) = eflx_bot` slot is +downward
(SetRHSVec_Soil :2379); with eflx_bot = 0 in the dump the sign convention is
unpinned and the model documents the ambiguity rather than guessing.

### Soil fluxes

The `SoilFluxes` update shifts the pre-correction fluxes to the new soil
temperature and completes the surface energy balance:

- **Blends** (F90:175-183, 344-346): `t_grnd0` and `lw_grnd` are the
  frac_sno_fluxes/frac_h2osfc-weighted blends of the previous-time-step
  temperatures/T⁴ (the `ground_temperature_blend` template); `tinc =
  t_grnd − t_grnd0`.
- **Flux corrections** (F90:189-206): all five fluxes are shifted by
  `pre + tinc·deriv` (the `flux_temperature_correction` template, deriv =
  cgrnds for the sensible flux, cgrndl for the four mass fluxes).
- **Liquid/solid partition** (F90:208-274): from the signed `qflx_ev_snow`
  — evaporation split by the top-layer liquid/(liquid+ice) ratio, dew all
  solid when `t_grnd < tfrz` and all liquid otherwise.
- **Snow-evaporation limit** (F90:276-297): `evaporation_limit =
  (h2osoi_liq+h2osoi_ice)/(frac_sno_fluxes·dtime)`; the excess over the
  limit is returned to the soil evaporation and sensible heat
  (energy-conserving), written linearly in
  `qflx_ev_snow_excess = max(qflx_ev_snow_raw − evaporation_limit, 0)` —
  exact because the limiting branch's partition values coincide with the
  general-branch values at the limited flux.
- **Ground heat flux** (F90:341-371): `eflx_soil_grnd = (1−fs)·sabg_soil +
  fs·sabg_snow + dlrad + (1−frac_veg_nosno)·emg·forc_lwrad −
  emg·sb·lw_grnd − 4·emg·sb·t_grnd0³·tinc − (eflx_sh_grnd +
  qflx_evap_soi·htvp)` with the emission terms factored as
  `stefan_boltzmann_emission` and the increment as
  `stefan_boltzmann_emission_dT(emg, sb, t_grnd0)·tinc`.
- **Totals** (F90:373-394): eflx_sh_tot, qflx_evap_tot, eflx_lh_tot (with
  hvap/htvp split), eflx_lh_grnd.
- **Outgoing longwave and skin temperature** (F90:451-495):
  `eflx_lwrad_out`, `eflx_lwrad_net = eflx_lwrad_out − forc_lwrad`, and
  `t_skin = lw_grnd^0.25` for bare ground.

All `qflx_*` moisture fluxes are mass fluxes in `kg/m^2/s` (= mm/s of water):
the esm unit checker enforces dimensional consistency, and only the mass-flux
form makes the latent-heat products qflx·htvp [J/kg] = W/m² consistent. The
values are numerically identical to the Fortran's mm/s. The traced run's
`sb = SHR_CONST_STEBOL = 5.67e-8` exactly (the rounded value, not the CODATA
one) is pinned by the dumps; this is a provenance note (the value follows the
Fortran), not a bug.

## Units

| Quantity | Symbols | Units |
|---|---|---|
| Roughness lengths | `z0mg`, `z0h`, `zlnd`, `zldis`, `zldis_u/t/2m`, `obu*` | m |
| Wind speeds | `ur`, `um*`, `wc*`, `ustar`, `forc_u/v` | m/s |
| Temperatures | `forc_t`, `forc_th`, `thm`, `t_grnd`, `t_soisno_*`, `t_h2osfc`, `thv`, `dth`, `dthv`, `tstar`, `thvstar`, `t_ref2m`, `forc_dewpoint`, `tfrz`, `t_grnd0`, `tinc`, `t_skin`, `t_entry`, `t_exit`, `t_avg` | K |
| Humidities | `forc_q`, `qg*`, `dqh`, `qstar`, `q_ref2m`, `qsat_ref2m` | kg/kg |
| Pressures | `forc_pbot`, `forc_esat`, `forc_e`, `e_ref2m` | Pa |
| Resistances | `ram1`, `ram`, `rah`, `raw`, `soilresis` | s/m |
| Conductances | `raih`, `cgrnds`, `cgrnd` | W/m²/K |
| Latent derivative | `cgrndl` | kg/m²/s/K |
| Stresses | `taux`, `tauy` | kg/m/s² |
| Heat fluxes | `eflx_sh_grnd/soil/snow/h2osfc`, `eflx_soil_grnd`, `eflx_lwrad_out/net`, `eflx_sh_tot/lh_tot/lh_grnd`, `lwrad_emission/increment`, `sabg*` | W/m² |
| Evaporation | `qflx_evap_soi`, `qflx_ev_soil/snow/h2osfc`, `raiw`, `qflx_*_from_top_layer`, `evaporation_limit` | kg/m²/s |
| Soil/snow properties | `thk`, `cv`, `K` | W/m/K, J/m³/K |
| Dimensionless | `zeta*`, `rib`, `zetam`, `zetat`, `zetamaxstable`, `vkc`, `beta*`, `temp1/2`, `temp12m/22m`, `kbm1`, `rh_ref2m`, `frac_sno_albedo`, `snl`, `frac_sno_fluxes`, `frac_h2osfc`, `frac_veg_nosno`, `emg`, `cnfac`, `capr` | 1 |
| Meier2022 constants | `beta_param` | s^0.5/m^0.5/K^0.25 |
| | `nu_param` | m²/s |
| | `meier_param1/2/3`, `b1_param`, `b4_param` | 1 |

The fractional-exponent units of `beta_param` are carried through the unit
checker (verified with a probe). One unit-algebra note: the convective
velocity law `wc = beta·(−grav·ustar·thvstar·zii/thv)^0.333` (F90:372) is
written with the Fortran's exact `0.333_r8` exponent and the base
nondimensionalized by 1 m³/s³ because the unit checker only reduces exact
rational exponents on dimensional bases (the same idiom as the
`log10(snomelt_accum/1 m)` of the z0mg snowmelt law). The
nondimensionalization is exact; wc is only read on the unstable branch
(never pinned — all traced rows are stable).

## Testing

`ESD_ROOT` must point at a checkout of
`github.com/earthsciml/EarthSciDiscretizations` (the soil-temperature model
imports the column grid, the two stencils and the flux-BC rule by reference).
Then, from the EarthSciModels checkout:

```
ESD_ROOT=/path/to/EarthSciDiscretizations esm test components/land_surface/clm
```

(tests of mounted models run when their own file is a target; the
bare-ground run additionally reports its 3 mounts).

| File | Tests | Assertions | What is pinned |
|---|---|---|---|
| `clm_bareground.esm` | 5 | 75 | 5 dump rows of the 192-row `clm_bareground.csv` (one per traced regime), 15 assertions per row (all 14 dumped output columns plus z0mg), rel 1e-12 at `time_span {0,0}` |
| `clm_bareground_step.esm` | 0 | — | (mounted by `clm_bareground.esm`; no tests of its own) |
| `clm_soiltemp.esm` | 3 | 202 | `clm_soiltemp.csv` column 1 step 1: 134 entry-pin + 35 exit-pin + 33 derived CN-identity assertions (see below) |
| `clm_soiltemp_discretization.esm` | 0 | — | (rule file, imported by `clm_soiltemp.esm`) |
| `clm_soilfluxes.esm` | 4 | 58 | `clm_soilfluxes.csv` rows (step 1/p1, step 12/p1 with forc_lwrad from the DATM dump; step 7/p8 and step 6/p16 without) — 17/15/13/13 assertions |
| `clm_templates.esm` | 0 | — | (library, imported by the components) |

Rust CLI (EarthSciAST, esm 0.7.0-era): **335P / 0F / 0E** for the six files,
`esm validate` passes for all six. Python inline-test gate
(`tools/run_esm_inline_tests.py`, earthsci_ast 0.8.0): 78P / 0F / 260E — see
the runner limitation note below.

### Derived values

- **clm_soiltemp**: the `dTdt` and `kdudz_top` expected values are
  *derived* (computed in Python from the dumped quantities by the EqESM
  `stage1/analysis/extract_soiltemp_testdata.py`); the CN-identity residual is
  expected 0 within abs 1e-9 W/m² (the CLM solver's round-off). No fitted
  parameters.
- **clm_soilfluxes**: the assertions on quantities that are not dump columns
  (lw_grnd, qflx_ev_snow, qflx_ev_soil, evaporation_limit,
  qflx_soliddew_to_top_layer, lwrad_emission/increment, eflx_lwrad_out,
  qflx_evap_tot) are labelled "derived (not a dump column)" and produced by
  the EqESM `stage1/analysis/clm_soilfluxes_derived.py`, which evaluates the
  transcribed equations at the pinned dump inputs (f64, cross-checked against
  every dump column they touch, all 192 rows, max rel err 7.9e-15). The
  step-1/step-12 column-1 pins fix `sb = 5.67e-8` exactly.

### Runner limitation (Python gate)

A test `parameter_overrides` with an **ARRAY** value for a shaped parameter
(esm-spec §6.6.2) is routed by the Python runner through `esm_problem(p=...)`
whose `p` channel carries only scalars — the array is silently dropped
(minimal repro `p_probe.esm`: 1 model, 1 patch-shaped parameter, 1 faq-reduce
equation, 1 test with `aicen: [0.5]` — Rust CLI 1/1 PASS, Python gate
`solve failed: Unresolved symbol: 'M.aicen'`; the same failure class was
documented for the CICE port). Consequences for this port:

- `clm_bareground.esm` (75 assertions) passes the Python gate **cleanly** —
  its tests override the patch-shaped parameters with scalars.
- `clm_soilfluxes.esm` (58) and `clm_soiltemp.esm` (202) error at solve in
  the Python gate (`Unresolved symbol: 'SoilFluxes.snl'` /
  `index 34 is out of bounds for axis 0 with size 34` — the dropped arrays
  fall back to wrong-size defaults). The Rust CLI runs all 335 assertions
  green, and the files are byte-identical to the reviewed EqESM stage-2
  sources.

## Coverage gaps

The dumps support exactly the pins above; the following branches are
transcribed or documented but not dump-pinned:

**Bare-ground fluxes** (`README-clm-bareground.md` of the stage-2 repo has
the full census; every traced row is stable with ζ clamped at 2.0 and in the
dew branch): the unstable Monin-Obukhov branches (ζ < 0, incl. the wc/um
unstable update and the 1.14/0.8 free-convection terms of the stability
functions), the liquid dewpoint branch (t ≥ tfrz), the raiw dqh ≤ 0 side
(sl14 and soilbeta sub-branches), the z0mg snowmelt branch
(snomelt_accum ≥ 1e-5, the log10/atan form) and the bare-soil `zlnd` branch,
the ZengWang2007 z0hg branch (not transcribed — the traced run is
Meier2022), and the unpinned outputs qflx_ev_h2osfc (qg_h2osfc not dumped),
cgrnd (htvp not dumped; bound to hvap), rh_ref2m, kbm1. Not transcribed
(dead or undumped in this configuration): the human-stress indices, the www
soil-wetness variable, the rssun/rssha photosynthesis resistances, the u10
diagnostics.

**Soil temperature**: `imelt = 0` everywhere (no phase change — the
Phasechange laws are not transcribed); `frac_sno_fluxes = 1` exactly (the
0 < frac_sno_fluxes < 1 split surface row is untested); Jordan1991 snow
conductivity (transcribed in the stage-2 library, untested — Sturm1997 is
the traced method); h2osno_no_layers = 0; excess_ice = 0 and snow
h2osoi_liq = 0; eflx_bot = 0 (nonzero geothermal-flux branch untested);
frac_h2osfc = 0 (surface-water correction untested); the urban/building
branches of ComputeHeatDiffFluxAndFactor not transcribed. The top row of the
CN identity is not pinned (fully-implicit top row, see above).

**Soil fluxes**: forc_lwrad for columns 6-16 (no DATM longwave identity —
eflx_soil_grnd/eflx_lwrad_out/eflx_lwrad_net unpinned there); qflx_ev_h2osfc
(not dumped; frac_h2osfc = 0 on all rows); the snow-evaporation limit firing
(F90:288-296, never fires on the traced rows — all dew); the evaporation
branch of the partition and the soil solidevap limit (every row is dew); the
liquid-dew branch (all rows t_grnd < tfrz); the urban branch (F90:197-200,
356-371, 490-495) and the `_u`/`_r` aliases (not transcribed); a mixed
snow/soil blend (0 < frac_sno_fluxes < 1) and the no-snow (snl = 0) and
vegetation (frac_veg_nosno = 1) branches; errsoi (F90:399-446, the
soil energy-balance check — not dumped; its conservation content is covered
by the eflx_soil_grnd/eflx_lwrad_net pins for columns 1-5).

## Documented divergences (all annotated in the file metadata)

1. **Bare-ground wc computed unconditionally**: the Fortran's wc local keeps
   its MoninObukIni seed 0.5 m/s stale on the stable branch; the esm step
   computes the update value unconditionally, which is observationally
   identical (stable rows never read it), so the wc_prev threading is
   dropped. Likewise the parent's zldis equals the step's own zldis_u (z0mg
   is iteration-constant), so the zldis couplings are dropped.
2. **forc_th recovered from thv** (exact inversion of the dumped dthv);
   **t_h2osfc = t_soisno(c,1)** (verified on all 192 rows);
   **temp2 = temp1 and temp22m = temp12m** by the equality branches (hold
   because forc_hgt_q_patch == forc_hgt_t_patch and z0qg == z0hg in the
   traced run).
3. **Soil-temperature top row**: the fully-implicit top row of SetMatrix_Snow
   is not expressible in the plain-CN PDE form (see above); the top row of
   `cn_balance` is therefore not pinned.
4. **eflx_bot sign ambiguity** (see above).

## Bugs found in the CESM/CTSM code

Centralized list (per the EqESM project's AGENTS.md): see `bugs.md` in the
EqESM repository root. This port's transcriptions absorb two of them:

- **bugs.md #33** — the Sturm1997 conductivity literals lack `_r8` and
  execute as float32-rounded values; reproduced exactly in
  `snow_thermal_cond_sturm1997` (rel 1.6e-16 pins).
- **bugs.md #34** — the top snow layer's (z, dz) is inconsistent with its zi
  interfaces (suspected DivideSnowLayers/AddNewSnow); absorbed exactly by
  feeding the dumped `zi_bot` through the harmonic-mean template, the dumped
  dz through the PDE rule's measure multiplication, and the capr measure from
  ze/zc (never the dumped dz).

No new CESM defects were found during this transcription.

## Next steps (stage 2.5 / stage 3)

1. The remaining CLM stage-2 components (`clm_canopy.esm`, `clm_surfalbedo.esm`,
   `clm_atm_forcing.esm`) extend this library with their shared laws; the
   stage-2 `clm_templates.esm` is the full library they were reviewed against.
2. When the cmeps bulk-flux component is ported, `clm_templates.esm` drops
   its inlined `psixhu_unstable` and imports `cmeps_templates.esm` by
   reference.
3. `clm_soiltemp_discretization.esm` is a candidate EarthSciDiscretizations
   PR (its rule, priority 11, is a CLM-specific top-row measure over the
   shared `varcoeff_face_laplacian_lev_flux_bc` family).
4. Mount into `eqesm.esm` and integrate with earthsciintegrator; compare
   against full-CESM simulations.
