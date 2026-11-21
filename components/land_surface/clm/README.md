# CLM soil and bare-ground components

A port of three pieces of the CTSM/CLM land model (CTSM tag `ctsm5.4.063`, the
CESM3.0 alpha-branch land model) to esm 2.0.0 files:

- the bare-ground turbulent fluxes of `BareGroundFluxesMod.F90` with the
  Monin-Obukhov surface-layer laws of `FrictionVelocityMod.F90` (MoninObukIni,
  FrictionVelocity, StabilityFunc1/2), for the non-exposed-vegetation patches;
- the snow/soil heat-conduction step of `SoilTemperatureMod.F90`
  (SoilTemperature with the SoilThermProp thermal-property laws), written as a
  PDE on the EarthSciDiscretizations `column_nonuniform_1d` grid plus a local
  discretization rule for CLM's top-row finite-volume measure;
- the ground energy/moisture flux update `SoilFluxesMod.F90:SoilFluxes`.

The shared pointwise laws are factored into the expression-template library
`clm_templates.esm`. All model logic lives in the `.esm` files; this README is
the human-readable map. Every Fortran citation (`File.F90:line`) refers to the
upstream source at the `ctsm5.4.063` tag of
[ESCOMP/CTSM](https://github.com/ESCOMP/CTSM) (`src/biogeophys/` and
`src/main/clm_varcon.F90`); constants come from `clm_varcon.F90`, the
parameter file `ctsm60_params.c260518.nc` and the case's `lnd_in` namelist.

## Scope and validity — read first

- **`clm_soiltemp.esm` is a single-time-step model.** It reproduces one CLM
  soil-temperature step from a supplied entry state; it is **not** a
  free-running soil-temperature model and must not be integrated over more
  than one step on its own:
  - the thermal properties (`thk`, `cv`, `K`) are computed from the
    *parameter* `t_entry` (the start-of-step temperatures, as SoilThermProp
    does once per CLM step), not from the evolving state `T`;
  - the top boundary flux `kdudz_top = hs + dhsdT·(T[NLEV] − t_entry[NLEV])`
    is linearized about `t_entry`, with `hs`, `dhsdT`, `sabg` and `eflx_bot`
    given as parameters for that step;
  - the column structure is fixed at compile time (`N_SNOW_MAX = 9` snow
    layers, `nbedrock = 20`); there is no phase change, no snow-layer
    combination/division and no change of layer water content;
  - every test uses `time_span {0, 0}`: it checks the instantaneous tendency
    `cv·∂T/∂t = F(T)` at the entry and exit states and the Crank-Nicolson
    identity of the one step.

  What it *is* valid for: evaluating the CLM heat-conduction operator, the
  thermal-property laws and one step's energy balance for a given entry
  state. Integrated past one step it does not reproduce CLM (the properties
  and surface linearization go stale, and CLM's top row is fully implicit —
  see [Soil temperature](#soil-temperature)). A multi-step use needs a driver
  that recomputes `t_entry`, `hs`, `dhsdT` and `sabg` every step from a coupled
  surface energy balance, which is not part of this directory.
- **`clm_bareground.esm` and `clm_soilfluxes.esm`** are algebraic
  (pointwise) models; all their tests evaluate them at `time_span {0, 0}`.
- **One tested regime.** The reference data (below) contain a single physical
  regime — stable, dew-depositing, frozen, fully snow-covered — so every
  other branch of the transcribed laws is untested. See
  [Tested regimes and gaps](#tested-regimes-and-gaps).

## Reference data

The tests pin values recorded from an instrumented CESM run: a CESM3 /
CTSM `ctsm5.4.063` `I2000Clm60Sp` land-only case (GSWP3 atmospheric forcing,
starting 2000-01-01, `dtime = 1800 s`) to which write statements were added
at the exits of `BiogeophysPreFluxCalcs`/`CalculateSurfaceHumidity`,
`BareGroundFluxes`, `ComputeGroundHeatFluxAndDeriv`, `SoilTemperature` (before
SoilThermProp and after the band-diagonal solve), `SurfaceRadiation` and
`SoilFluxes`. Each record holds the subroutine's inputs and outputs in full
double precision for the first 16 traced patches (16 bare-soil columns,
`p == c`, each under a 9-layer snowpack, `t_grnd` 234–248 K) over the first
12 time steps — 192 rows per dump (34 layers per column for the
soil-temperature dump). The only CESM change was the added output; the
physics is the unmodified `ctsm5.4.063` source. Test values that are not
recorded columns are labelled *derived* in the test descriptions and were
computed offline by evaluating the transcribed equations in double precision
at the recorded inputs.

## File map

| File | Contents | Fortran source |
|---|---|---|
| `clm_templates.esm` | Expression-template library (the QSat laws, the Monin-Obukhov surface-layer laws of the bare-ground fluxes, the Meier2022 roughness laws, the soil/snow thermal laws and the SoilFluxes laws; see [The template library](#the-template-library)) | `BareGroundFluxesMod.F90`, `FrictionVelocityMod.F90`, `SoilTemperatureMod.F90` (SoilThermProp :604-903), `SoilFluxesMod.F90`, `QSatMod.F90`, `clm_varcon.F90` |
| `clm_bareground_step.esm` | Model `BareGroundStep` — **one** pass of the stability do-while of BareGroundFluxes, authored once and mounted 3× (esm-spec §4.7): the profile heights zldis_u/zldis_t/zldis_2m, ustar/temp1/temp12m from the four-branch profile templates, temp2 = temp1 and temp22m = temp12m (equality branches), tstar/qstar, the Meier2022 z0h, thvstar, zeta_raw, the stability clamp, wc, um and obu; 17 equations | `BareGroundFluxesMod.F90:342-388` |
| `clm_bareground.esm` | Model `BareGroundFluxes` — the derived inputs (ur, dth, dqh, dthv, z0mg, zldis), the MoninObukIni initialization (um_ini, rib, zeta_ini, obu_ini), the exit state (= step3 outputs) and the flux laws: ram/rah/raw, raih, forc_esat/forc_e/forc_dewpoint, the raiw selection, ram1, cgrnds/cgrndl/cgrnd, taux/tauy, eflx_sh_grnd/soil/snow/h2osfc and qflx_evap_soi/ev_snow/ev_soil/ev_h2osfc (one law: `aerodynamic_surface_flux`), t_ref2m/q_ref2m/qsat_ref2m/rh_ref2m, kbm1; 45 equations + top-level mounts step1..step3 wired by `clm_bareground_steps_coupling.esm`; 5 tests | `BareGroundFluxesMod.F90:318-322,331,342-388,400-495` |
| `clm_bareground_steps_coupling.esm` | Coupling library (esm-spec §10.9): the single source of the 66 `variable_map` `param_to_var` edges wiring `BareGroundFluxes` to its three `BareGroundStep` mounts — the 19 iteration-invariant fields feed every step and the iteration state chains step1 → step2 → step3 (um, obu, z0h). Imported by `coupling_import` (with bind) in `clm_bareground.esm`; no tests of its own | `BareGroundFluxesMod.F90:342-388` |
| `clm_soiltemp_discretization.esm` | ESD-format rewrite rule `varcoeff_face_laplacian_lev_flux_bc_capr` (priority 11): the conservative variable-coefficient vertical diffusion `D(K·D(u, lev), lev)` of the EarthSciDiscretizations `varcoeff_face_laplacian_lev_flux_bc` rule with CLM's top-row measure `M = 0.5·(ze[NLEV+1] − zc[NLEV] + capr·(ze[NLEV+1] − zc[NLEV−1]))` in place of `dz[NLEV]`; imports the two ESD stencils by reference. Kept with this component because the measure is CLM-specific | `SoilTemperatureMod.F90`: ComputeHeatDiffFluxAndFactor :1895, SetMatrix_Snow :2593-2686 |
| `clm_soiltemp.esm` | Model `SoilTemperature` — the **single-step** heat-conduction PDE `cv·∂T/∂t = dz·D(K·D(T,lev),lev) + sabg` (see [Scope and validity](#scope-and-validity--read-first)) with the SoilThermProp property laws (from `t_entry`), the harmonic-mean interface conductivities, the linearized surface flux, the bottom flux `eflx_bot`, the observeds `fn_esd`, `dTdt`, `cn_balance`; 3 tests | `SoilTemperatureMod.F90`: SoilThermProp :604-903, ComputeGroundHeatFluxAndDeriv :1545-1798, the implicit solve :1801-2686 |
| `clm_soilfluxes.esm` | Model `SoilFluxes` — the full SoilFluxes update, 32 equations; the shared laws imported by reference from `clm_templates.esm`; 4 tests | `SoilFluxesMod.F90:38-518` |

`clm_bareground.esm` imports `./clm_templates.esm` by reference; no law is
duplicated. The 3-mount composition uses top-level mounts because the Rust
CLI drops couplings in the single-top-level-model build path.

## The template library

`clm_templates.esm` carries the pointwise laws these components share:

- **QSat laws** (`qsat_esat`, `qsat_qs`, and the shared ninth-order power-sum
  `poly8`): the Flatau et al. (1992) saturation vapor pressure/specific
  humidity fits of `QSatMod.F90:18-103`.
- **Monin-Obukhov surface-layer laws** (bare-ground fluxes): the Paulson
  (1970) stability functions — the scalar one (`stability_func_scalar`) is
  the CMEPS `psixhu_unstable` law (`flux_atmocn_Large.F90:164`), transcribed
  here until a CMEPS bulk-flux component carrying it is in this repository,
  at which point this library can import it by reference (esm-spec §9.7.3);
  the momentum one (`stability_func_momentum`) is authored separately because
  its constant is SHR_CONST_PI·0.5 while the CMEPS `psimhu_unstable`
  hard-codes 1.571, with the `chik = sqrt(sqrt(1-16·ζ))` intermediate factored
  as `stability_chik`. The MoninObukIni initialization laws
  (`monin_obukhov_initial_wind`, `bulk_richardson`,
  `monin_obukhov_initial_zeta` through the shared `clamp_zeta`), the
  four-branch friction-velocity profile laws (`friction_velocity_momentum`,
  `friction_velocity_scalar`, taking ζ as a parameter and sharing the stable
  branches as `stable_profile_integral`), the Meier2022 roughness laws
  (`z0hg_meier2022`, `z0mg_meier2022_snowmelt`), the Magnus dewpoint law,
  `virtual_potential_scale` (shared by dthv and thvstar) and the
  BareGroundFluxes flux laws (`aerodynamic_surface_flux` — one merged
  sensible-heat/evaporation law, `wind_stress_component`, `ref2m_profile`).
- **Soil/snow thermal laws** (soil temperature): `snow_bulk_density`,
  `snow_thermal_cond_sturm1997` (with the float32-rounded coefficients — see
  [Defects in the CTSM source](#defects-in-the-ctsm-source)),
  `snow_heat_capacity` (with the thin-layer floor), the Johansen (1975) soil
  conductivity in named-intermediate form (`soil_saturation_water_content`,
  `kersten_number`, `soil_liquid_fraction`, `soil_saturated_thermal_cond`,
  `soil_thermal_cond`), the de Vries (1963) soil heat capacity, and the
  harmonic-mean interface conductivity `clm_interface_conductivity` with the
  zero bottom boundary.
- **SoilFluxes laws**: `ground_temperature_blend` (the t_grnd0/lw_grnd
  blends), `stefan_boltzmann_emission` (emg·sb·T⁴),
  `flux_temperature_correction` (pre + tinc·deriv, the five flux corrections)
  and `stefan_boltzmann_emission_dT` (4·emg·sb·T³).

The other CLM shared laws (canopy interception/storage, the ZengWang2007
vegetation roughness, emissivities, the Jordan1991 snow conductivity, the
albedo and shortwave laws, …) will be added as the components that use them
are ported.

### NaN safety of unselected branches

A backend may evaluate every `ifelse` branch eagerly, so the laws the Fortran
evaluates on only one branch are written to stay finite on the others,
without changing any selected-branch value:

- `wc = beta·max(−grav·ustar·thvstar·zii/thv, 0)^0.333`
  (`BareGroundFluxesMod.F90:383`): the Fortran evaluates wc only when
  ζ < 0, where the base is positive; the esm computes it unconditionally, so
  the base is clamped at 0 for the stable rows (a negative base to a
  fractional power is NaN).
- In `friction_velocity_momentum`/`friction_velocity_scalar` the
  unstable-branch terms are written `log(abs(−ζm·obu/z0))`,
  `abs(ζ)^±0.333` (for `(−ζ)^±0.333`) and `stability_func_*(min(x, 0))`; in
  `stable_profile_integral` the ζ > 1 branch is written `log(abs(obu/z0))`
  and `log(abs(ζ))`. Each clamp is the identity on the branch that selects it
  (ζ < 0 with obu < 0, resp. ζ > 1 with obu > 0).

## Components

### Bare-ground turbulent fluxes

The configuration of the reference case: `z0param_method = 'Meier2022'`,
`use_z0m_snowmelt = .true.`, `zetamaxstable = 2.0`, `soil_resis_method = 1`,
`do_soilevap_beta` inactive, forcing heights 30 m, `wind_min = 1.0` m/s, and
the Meier2022 constants of `ctsm60_params.c260518.nc` (`beta_param = 7.2`,
`nu_param = 1.5e-5` m²/s, `b1_param = 1.4`, `b4_param = −0.31`,
`meier_param1 = 0.23`, `meier_param2 = 0.08`, `meier_param3 = 70`;
`zetam = 1.574`, `zetat = 0.465`; `zii = 1000` m, `beta = 1`), `niters = 3`.

The esm has no loop construct, so the stability do-while of
`BareGroundFluxesMod.F90:342-388` is represented compositionally: the
17-equation update law is authored **once** in `BareGroundStep`
(`clm_bareground_step.esm`) and mounted three times by reference as
top-level models `step1..step3`, chained by the coupling library
(um_ini/obu_ini/z0mg seed step1; each step's state feeds the next). The
parent keeps the external names of the Fortran locals: ustar/temp1/temp2/
temp12m/temp22m/z0h/um = the step3 outputs (the exit state of the
3-iteration loop).

**Latent heat `htvp`.** `cgrnd = cgrnds + htvp·cgrndl`
(`BareGroundFluxesMod.F90:450`) uses the column latent heat chosen in
`BiogeophysPreFluxCalcsMod.F90:353-357`: `hsub = SHR_CONST_LATSUB =
2.8347e6 J/kg` (LATICE + LATVAP) when the top layer `snl+1` holds ice and no
liquid, else `hvap = 2.501e6 J/kg`. Every reference row has a dry snow top
layer, so `htvp = hsub` (the recorded value on all 192 rows); it is the
model's default and every test's override, and `cgrnd` is asserted against
the recorded `cgrnd` of the same run.

**`rh_ref2m`** is the 2-m relative humidity in percent (units `%`,
`min(100 %, 100 %·q_ref2m/qsat_ref2m)`, `BareGroundFluxesMod.F90:488`).

### Soil temperature

*Single-step model — see [Scope and validity](#scope-and-validity--read-first).*

CLM advances the snow/soil temperatures with the implicit Crank-Nicolson
solve of SetMatrix_Soil/SetMatrix_Snow on the tridiagonal row system
(`cnfac = 0.5`, `capr = 0.34`, `dtime = 1800 s`,
`snow_thermal_cond_method = 'Sturm1997'`, `nlevgrnd = 25`, `snl = −9` on the
reference columns, `use_excess_ice = .true.` with zero excess ice,
`frac_sno_fluxes = 1`, `eflx_bot = 0`, `imelt = 0` on every recorded row).
The `.esm` model is a PDE — `cv·∂T/∂t = dz·D(K·D(T, lev), lev) + sabg` with
the state `T` — whose spatial operator, evaluated at the recorded states,
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
  `SoilTemperatureMod.F90:1895` (M = 0.01002979145516516 m in the reference
  column). The model multiplies the lowered divergence by the *recorded*
  layer thickness `dz` (the top layer's dz differs from the grid spacing
  ze[NLEV+1] − ze[NLEV] — see [Defects](#defects-in-the-ctsm-source)) and
  adds `sabg`. The whole RHS `F(u)` is the model-local template
  `soil_heat_tendency(u)`, applied once to `T` (the `dTdt` observed) and once
  to the CN mean `t_avg` (the `cn_balance` observed).
- **Boundary fluxes.** `kdudz_top = hs + dhsdT·(T[NLEV] − t_entry[NLEV])`
  (the surface flux linearized about the entry state) and `kdudz_bot =
  eflx_bot` (0 in the reference run).
- **Properties.** The SoilThermProp laws are array equations over `lev`
  consuming `t_entry`; the layer masks come from metaparameters (`is_snow`
  over N_SNOW_MAX = 9 snow layers, `is_bedrock` over the nbedrock = 20 bottom
  layers). `thk` composes the Sturm1997 snow law and the Johansen (1975) soil
  law with the named intermediates `satw`, `dke`, `fl`, `dksat`. The interface
  conductivities `K` are the harmonic mean over the face index set:
  `K[n] = tk(26−n)` for n = 2..34, K[1] = 0 (the zero bottom boundary of
  :828), K[35] = 0 dummy above the top layer.

**Top row is fully implicit in CLM.** CLM's top row is fully implicit in
`dhsdT`, so a Crank-Nicolson integration of this PDE would **not reproduce
CLM's top row exactly**: the plain CN average evaluates the linearized surface
flux with the `(1 − cnfac)` weighting CLM does not use at the top. Rows 1..33
match a CN step exactly; the top row of `cn_balance` is therefore not pinned.

**eflx_bot sign.** The F90 comment at the eflx_bot declaration says
"+upward" while the `fn(nlevgrnd) = eflx_bot` slot is +downward
(SetRHSVec_Soil); with eflx_bot = 0 in the reference run the sign
convention is unpinned and the model documents the ambiguity rather than
guessing.

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
only the mass-flux form makes the latent-heat products qflx·htvp [J/kg] =
W/m² dimensionally consistent. The values are numerically identical to the
Fortran's mm/s. The run's `sb = SHR_CONST_STEBOL = 5.67e-8` exactly (the
rounded value, not the CODATA one) is pinned by the recorded ground heat
flux.

## Units

| Quantity | Symbols | Units |
|---|---|---|
| Roughness lengths | `z0mg`, `z0h`, `zlnd`, `zldis`, `zldis_u/t/2m`, `obu*` | m |
| Wind speeds | `ur`, `um*`, `wc*`, `ustar`, `forc_u/v` | m/s |
| Temperatures | `forc_t`, `forc_th`, `thm`, `t_grnd`, `t_soisno_*`, `t_h2osfc`, `thv`, `dth`, `dthv`, `tstar`, `thvstar`, `t_ref2m`, `forc_dewpoint`, `tfrz`, `t_grnd0`, `tinc`, `t_skin`, `t_entry`, `t_exit`, `t_avg` | K |
| Humidities | `forc_q`, `qg*`, `dqh`, `qstar`, `q_ref2m`, `qsat_ref2m` | kg/kg |
| Relative humidity | `rh_ref2m` | % |
| Pressures | `forc_pbot`, `forc_esat`, `forc_e`, `e_ref2m` | Pa |
| Resistances | `ram1`, `ram`, `rah`, `raw`, `soilresis` | s/m |
| Conductances | `raih`, `cgrnds`, `cgrnd` | W/m²/K |
| Latent derivative | `cgrndl` | kg/m²/s/K |
| Latent heat | `htvp` | J/kg |
| Stresses | `taux`, `tauy` | kg/m/s² |
| Heat fluxes | `eflx_sh_grnd/soil/snow/h2osfc`, `eflx_soil_grnd`, `eflx_lwrad_out/net`, `eflx_sh_tot/lh_tot/lh_grnd`, `lwrad_emission/increment`, `sabg*` | W/m² |
| Evaporation | `qflx_evap_soi`, `qflx_ev_soil/snow/h2osfc`, `raiw`, `qflx_*_from_top_layer`, `evaporation_limit` | kg/m²/s |
| Soil/snow properties | `thk`, `cv`, `K` | W/m/K, J/m³/K |
| Dimensionless | `zeta*`, `rib`, `zetam`, `zetat`, `zetamaxstable`, `vkc`, `beta*`, `temp1/2`, `temp12m/22m`, `kbm1`, `frac_sno_albedo`, `snl`, `frac_sno_fluxes`, `frac_h2osfc`, `frac_veg_nosno`, `emg`, `cnfac`, `capr` | 1 |
| Meier2022 constants | `beta_param` | s^0.5/m^0.5/K^0.25 |
| | `nu_param` | m²/s |
| | `meier_param1/2/3`, `b1_param`, `b4_param` | 1 |

The convective velocity law `wc` (`BareGroundFluxesMod.F90:383`) is written
with the Fortran's exact `0.333_r8` exponent and the base nondimensionalized
by 1 m³/s³, because the unit checker only reduces exact rational exponents on
dimensional bases (the same idiom as the `log10(snomelt_accum/1 m)` of the
z0mg snowmelt law).

## Testing

`ESD_ROOT` must point at a checkout of
[EarthSciML/EarthSciDiscretizations](https://github.com/EarthSciML/EarthSciDiscretizations)
(the soil-temperature model imports the column grid, the two stencils and the
flux-BC rule by reference). Then, from the EarthSciModels checkout:

```
ESD_ROOT=/path/to/EarthSciDiscretizations esm test components/land_surface/clm
```

| File | Tests | Assertions | What is pinned |
|---|---|---|---|
| `clm_bareground.esm` | 5 | 80 | 5 of the 192 recorded bare-ground rows, 16 assertions per row (the 14 recorded output columns, z0mg, and cgrnd against the recorded ground-heat-flux `cgrnd`), rel 1e-12 |
| `clm_bareground_step.esm` | 0 | — | (mounted by `clm_bareground.esm`; no tests of its own) |
| `clm_bareground_steps_coupling.esm` | 0 | — | (coupling library, imported by `clm_bareground.esm`) |
| `clm_soiltemp.esm` | 3 | 202 | column 1, step 1: 134 entry-state + 35 exit-state + 33 derived Crank-Nicolson-identity assertions |
| `clm_soiltemp_discretization.esm` | 0 | — | (rule file, imported by `clm_soiltemp.esm`) |
| `clm_soilfluxes.esm` | 4 | 62 | step 1/p1, step 12/p1, step 7/p8, step 6/p16 — 17/15/15/15 assertions; the recorded column longwave `forc_lwrad` drives `eflx_soil_grnd`/`eflx_lwrad_net` pins on all four |
| `clm_templates.esm` | 0 | — | (library, imported by the components) |

The bare-ground rows: `row_1_1` (step 1, column 1 — one of the few rows on
which the MoninObukIni initial ζ is below the 2.0 clamp), `row_2_1` (steady
stable state), `row_6_8` (mid-run, warm column), `row_9_4` (low wind,
ur = 1.78 m/s, above `wind_min`), `row_12_16` (last step, cold column). The
same input construction, applied to all 192 recorded rows with the same
assertions and tolerance, passes on every row (3,072 assertions, checked
when these tests were written; not committed as tests because all rows are in
the same regime and add no branch coverage).

### Derived values

- **clm_soiltemp**: the `dTdt` and `kdudz_top` expected values are
  *derived* (computed offline in double precision from the recorded
  quantities); the CN-identity residual is expected 0 within abs 1e-9 W/m²
  (the CLM solver's round-off, max 6.3e-10 W/m²). No fitted parameters.
- **clm_soilfluxes**: the assertions on quantities that are not recorded
  columns (lw_grnd, qflx_ev_snow, qflx_ev_soil, evaporation_limit,
  qflx_soliddew_to_top_layer, lwrad_emission/increment, eflx_lwrad_out,
  qflx_evap_tot) are labelled "derived (not a dump column)", computed by
  evaluating the transcribed equations at the recorded inputs (double
  precision, cross-checked against every recorded column they touch on all
  192 rows, max rel err 7.9e-15).

### Runner limitation (Python gate)

A test `parameter_overrides` with an **array** value for a shaped parameter
(esm-spec §6.6.2) is routed by the Python runner through a `p` channel that
carries only scalars, so the array is dropped. `clm_bareground.esm` overrides
only scalars and is unaffected; `clm_soilfluxes.esm` and `clm_soiltemp.esm`
error at solve in the Python runner (the dropped arrays fall back to
wrong-size defaults). The Rust CLI runs all of them.

## Tested regimes and gaps

Every recorded row comes from one physical regime. Checked over all rows of
the bare-ground (192), soil-fluxes (192) and soil-temperature (13,056
layer-rows) records:

| Property | All recorded rows | Consequence |
|---|---|---|
| Stability | stable: `thm > t_grnd` and `forc_q > qg` on every row, so dthv > 0; iteration ζ clamped at `zetamaxstable = 2.0` | momentum/heat profiles only in the ζ > 1 branch, 2-m profiles only in 0 < ζ ≤ 1; **no unstable row** (ζ < 0, ζ < −ζm, ζ < −ζt, the wc/um unstable update, the StabilityFunc1/2 unstable forms) |
| Moisture flux | dew on every row (`qflx_evap_soi < 0`, dqh > 0, `t_grnd ≤ forc_dewpoint`) | raiw = forc_rho/raw only; **no evaporating row** (the dqh ≤ 0 side with the sl14 soil resistance and the soilbeta branch); in SoilFluxes no evaporation partition, no firing snow-evaporation limit |
| Temperature | `t_grnd` 234–248 K, all soil layers ≤ 226 K | ice dewpoint coefficients only; **no liquid dew**; Kersten number only on the frozen branch (`dke = satw`), **no unfrozen soil** |
| Snow | `snl = −9`, `frac_sno_fluxes = 1`, `frac_sno_albedo = 1`, `snomelt_accum = 0`, `htvp = hsub` | **no snow-free or partially snow-covered column**; z0mg only in the snomelt_accum < 1e-5 branch; the bare-soil `zlnd` and snowmelt z0mg branches and `htvp = hvap` untested |
| Wind | `forc_u == forc_v` on every row, `ur > wind_min` | taux/tauy pinned with equal components only |
| Soil temperature | `imelt = 0`, `eflx_bot = 0`, `frac_h2osfc = 0`, excess ice 0, snow liquid 0, Sturm1997 only | no phase change, geothermal flux, surface water, or Jordan1991 snow conductivity |

These branches are transcribed from the Fortran but **not exercised by any
test**: the reference run contains no rows in those regimes, and no other
recorded data were available, so no test values were invented for them.
Additional untested items: qflx_ev_h2osfc (qg_h2osfc not recorded),
rh_ref2m and kbm1 (not recorded); in SoilFluxes the urban branch (not
transcribed), mixed snow/soil blends, the `frac_veg_nosno = 1` branch and the
errsoi energy-balance check (not recorded); in SoilTemperature the
0 < frac_sno_fluxes < 1 split surface row, h2osno_no_layers > 0, the urban
branches of ComputeHeatDiffFluxAndFactor (not transcribed), and the top row
of the CN identity (fully implicit in CLM). Not transcribed (dead or
unrecorded in this configuration): the human-stress indices, the www
soil-wetness variable, the rssun/rssha photosynthesis resistances, the u10
diagnostics, and the ZengWang2007 z0hg branch.

## Documented divergences (all annotated in the file metadata)

1. **Bare-ground wc computed unconditionally**: the Fortran's wc local keeps
   its MoninObukIni seed 0.5 m/s stale on the stable branch; the esm step
   computes the update value unconditionally (base clamped at 0, see
   [NaN safety](#nan-safety-of-unselected-branches)), which is
   observationally identical (stable rows never read it), so the wc_prev
   threading is dropped. Likewise the parent's zldis equals the step's own
   zldis_u (z0mg is iteration-constant), so the zldis couplings are dropped.
2. **forc_th recovered from thv** (exact inversion of the recorded dthv);
   **t_h2osfc = t_soisno(c,1)** (verified on all 192 rows);
   **temp2 = temp1 and temp22m = temp12m** by the equality branches (they
   hold because forc_hgt_q_patch == forc_hgt_t_patch and z0qg == z0hg in this
   configuration).
3. **Soil-temperature top row**: the fully-implicit top row of SetMatrix_Snow
   is not expressible in the plain-CN PDE form (see above).
4. **eflx_bot sign ambiguity** (see above).

## Defects in the CTSM source

Two defects of `ctsm5.4.063` are reproduced exactly by this port:

- **Sturm1997 snow conductivity literals are single precision.**
  `SoilTemperatureMod.F90:775` and `:777` write the five coefficients
  (0.023, 0.234, 0.138, 1.01, 3.233) without the `_r8` kind suffix, so they
  execute as float32-rounded values promoted to double;
  `snow_thermal_cond_sturm1997` carries those values (rel 1.6e-16 against
  the recorded conductivities).
- **Top snow layer thickness inconsistent with its interfaces.** In the
  recorded state the top snow layer's `dz` (0.015578352833079012 m) differs
  from `zi(snl) − zi(snl+1)` (0.015517897173545236 m) — apparently from
  DivideSnowLayers/AddNewSnow. The port absorbs it exactly by feeding the
  recorded `zi` interfaces through the harmonic-mean template and grid, the
  recorded `dz` through the measure multiplication, and building the capr
  measure from `ze`/`zc` (never from `dz`).
