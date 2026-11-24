---
title: "BareGroundStep"
slug: "baregroundstep"
domains: ["land_surface"]
component_types: ["model"]
subdomains: ["clm"]
domain: "land_surface"
subdomain: "clm"
component_type: "model"
esm_version: "2.0.0"
esm_path: "components/land_surface/clm/clm_bareground_step.esm"
reference: "10.1029/2018MS001583"
description: "One-step update of the CLM bare-ground stability iteration: a single pass of the do-while of BareGroundFluxes in CTSM ctsm5.4.063 src/biogeophys/BareGroundFluxesMod.F90:342-388 (F90 line numbers below refer to that tag) (the FrictionVelocity call of :344-347 followed by the z0hg update, the stability-parameter update and the Obukhov-length update of :353-387), transcribed exactly and mounted three times by reference in clm_bareground.esm (top-level models.step1..step3, esm-spec section 4.7) so the 17-equation update law is authored once and the unrolled iteration is composed. Inputs are the update-invariant pointwise fields (the wind and temperature measurement heights forc_hgt_u/forc_hgt_t, the momentum roughness z0m = z0mg_patch which is constant across the iteration, the wind speed ur = max(wind_min, |forc_u,forc_v|), the temperature/humidity differences dth/dqh, the forcing specific/potential temperatures forc_q/forc_th, the virtual potential temperature thv, the convective velocity-scale inputs zii/beta, the zetamaxstable stability clamp and the physical constants vkc/grav/zetam/zetat/meier_param3/nu_param/beta_param) and the previous update's state (z0h_prev/obu_prev/um_prev). The iteration height is the step's own momentum profile height zldis_u = forc_hgt_u + z0m, which equals the parent's zldis = forc_hgt_u + z0mg (the redundant coupling is dropped), and the Fortran's stale wc local is computed unconditionally (only read by the unstable um branch; the dead wc threading is dropped). Outputs are the 17 update states (zldis_u = forc_hgt_u + z0m, zldis_t = forc_hgt_t + z0h_prev and zldis_2m = 2 + z0h_prev, the three profile heights of FrictionVelocityMod.F90:850-853, 946-949, 1022-1025; ustar from the four-branch momentum profile F90:857-871; temp1 from the four-branch scalar profile F90:956-970; temp2 = temp1 and temp22m = temp12m by the equality branch F90:997-998 and F90:1051-1052, which holds in the traced run because forc_hgt_q_patch == forc_hgt_t_patch and z0qg == z0hg; temp12m from the 2-m scalar profile F90:1022-1038; tstar = temp1*dth and qstar = temp2*dqh F90:354-355; z0h from the Meier2022 update F90:364; thvstar F90:375 (the virtual_potential_scale law shared with the parent's dthv); zeta_raw F90:376; the sign-preserving stability clamp zeta F90:378-386 (the clamp_zeta law shared with the MoninObukIni initialization); wc F90:383; obu = zldis/zeta F90:387). NaN safety: every branch of an ifelse may be evaluated eagerly by a backend, so the laws the Fortran evaluates only on one branch are written so their unselected branches stay finite - the wc base is clamped at zero (max(base, 0): on the unstable rows where wc is read the base is positive and the value is unchanged; on stable rows the Fortran never evaluates it), and the friction-velocity profile templates clamp the arguments of their unstable-branch logs, fractional powers and stability functions (clm_templates.esm). The expression templates of ./clm_templates.esm are imported by reference."
tags: ["land_surface", "clm", "model", "bare-ground", "monin-obukhov", "stability-iteration", "cesm"]
---

## Description

One-step update of the CLM bare-ground stability iteration: a single pass of the do-while of BareGroundFluxes in CTSM ctsm5.4.063 src/biogeophys/BareGroundFluxesMod.F90:342-388 (F90 line numbers below refer to that tag) (the FrictionVelocity call of :344-347 followed by the z0hg update, the stability-parameter update and the Obukhov-length update of :353-387), transcribed exactly and mounted three times by reference in clm_bareground.esm (top-level models.step1..step3, esm-spec section 4.7) so the 17-equation update law is authored once and the unrolled iteration is composed. Inputs are the update-invariant pointwise fields (the wind and temperature measurement heights forc_hgt_u/forc_hgt_t, the momentum roughness z0m = z0mg_patch which is constant across the iteration, the wind speed ur = max(wind_min, |forc_u,forc_v|), the temperature/humidity differences dth/dqh, the forcing specific/potential temperatures forc_q/forc_th, the virtual potential temperature thv, the convective velocity-scale inputs zii/beta, the zetamaxstable stability clamp and the physical constants vkc/grav/zetam/zetat/meier_param3/nu_param/beta_param) and the previous update's state (z0h_prev/obu_prev/um_prev). The iteration height is the step's own momentum profile height zldis_u = forc_hgt_u + z0m, which equals the parent's zldis = forc_hgt_u + z0mg (the redundant coupling is dropped), and the Fortran's stale wc local is computed unconditionally (only read by the unstable um branch; the dead wc threading is dropped). Outputs are the 17 update states (zldis_u = forc_hgt_u + z0m, zldis_t = forc_hgt_t + z0h_prev and zldis_2m = 2 + z0h_prev, the three profile heights of FrictionVelocityMod.F90:850-853, 946-949, 1022-1025; ustar from the four-branch momentum profile F90:857-871; temp1 from the four-branch scalar profile F90:956-970; temp2 = temp1 and temp22m = temp12m by the equality branch F90:997-998 and F90:1051-1052, which holds in the traced run because forc_hgt_q_patch == forc_hgt_t_patch and z0qg == z0hg; temp12m from the 2-m scalar profile F90:1022-1038; tstar = temp1*dth and qstar = temp2*dqh F90:354-355; z0h from the Meier2022 update F90:364; thvstar F90:375 (the virtual_potential_scale law shared with the parent's dthv); zeta_raw F90:376; the sign-preserving stability clamp zeta F90:378-386 (the clamp_zeta law shared with the MoninObukIni initialization); wc F90:383; obu = zldis/zeta F90:387). NaN safety: every branch of an ifelse may be evaluated eagerly by a backend, so the laws the Fortran evaluates only on one branch are written so their unselected branches stay finite - the wc base is clamped at zero (max(base, 0): on the unstable rows where wc is read the base is positive and the value is unchanged; on stable rows the Fortran never evaluates it), and the friction-velocity profile templates clamp the arguments of their unstable-branch logs, fractional powers and stability functions (clm_templates.esm). The expression templates of ./clm_templates.esm are imported by reference.

## Reference

- Lawrence, D. M., Fisher, R. A., Koven, C. D., Oleson, K. W., Swenson, S. C., Bonan, G., et al. (2019). The Community Land Model Version 5: Description of New Features, Benchmarking, and Impact of Forcing Uncertainty. Journal of Advances in Modeling Earth Systems, 11(12), 4245-4287.
- Meier, R., Davin, E. L., Bonan, G. B., Lawrence, D. M., Hu, X., Duveiller, G., Prigent, C., and Seneviratne, S. I. (2022). Impacts of a revised surface roughness parameterization in the Community Land Model 5.1. Geoscientific Model Development, 15(6), 2365-2393.
- CTSM (Community Terrestrial Systems Model), ESCOMP/CTSM, ctsm5.4.063 (cesm3.0-alphabranch): the CLM land-surface source - BareGroundFluxesMod.F90, FrictionVelocityMod.F90, clm_varcon.F90 (constants) - the reference implementation these components are transcribed from.
- EarthSciModels - the authoritative .esm corpus this component lives in.

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `forc_hgt_u` | `m` | `30.0` | observational height of wind at patch level (BareGroundFluxesMod.F90:370, forc_hgt_u_patch = forc_hgt_u + z0mg + displa with displa = 0), [m] |
| `forc_hgt_t` | `m` | `30.0` | observational height of temperature at patch level (forc_hgt_t_patch = forc_hgt_t + z0hg + displa), [m] |
| `z0m` | `m` | `8.134020505760161e-05` | momentum roughness length over ground z0mg_patch, constant across the stability iteration, [m] |
| `z0h_prev` | `m` | `8.134020505760161e-05` | previous update's scalar roughness z0hg_patch (seeded with z0mg, the initial set of SetRoughnessLengthsAndForcHeightsNonLake FrictionVelocityMod.F90:637), [m] |
| `obu_prev` | `m` | `15.758842` | previous update's Obukhov length obu (seeded by MoninObukIni), [m] |
| `um_prev` | `m/s` | `1.0` | previous update's wind speed um (seeded by MoninObukIni), [m/s] |
| `ur` | `m/s` | `1.0` | wind speed at the forcing height ur = max(wind_min, sqrt(forc_u^2 + forc_v^2)) with wind_min = 1.0 m/s (param file), [m/s] |
| `dth` | `K` | `1.0` | temperature difference dth = thm - t_grnd (BareGroundFluxesMod.F90:319), [K] |
| `dqh` | `kg/kg` | `0.001` | humidity difference dqh = forc_q - qg (BareGroundFluxesMod.F90:320), [kg/kg] |
| `forc_q` | `kg/kg` | `0.003` | atmospheric specific humidity at the forcing height, [kg/kg] |
| `forc_th` | `K` | `290.0` | atmospheric potential temperature at the forcing height forc_th = thv/(1 + 0.61*forc_q) (the traced dump does not carry forc_th; it is recovered from the dumped virtual potential temperature thv), [K] |
| `thv` | `K` | `295.31` | virtual potential temperature at the forcing height (BiogeophysPreFluxCalcsMod, dumped in clm_run_imports preflux), [K] |
| `zii` | `m` | `1000.0` | convective boundary layer height (BiogeophysPreFluxCalcsMod.F90:363, zii = 1000 m in the traced run), [m] |
| `beta` | `1` | `1.0` | coefficient for convective velocity (BiogeophysPreFluxCalcsMod.F90:362, beta = 1 in the traced run), [-] |
| `zetamaxstable` | `1` | `2.0` | maximum zeta in the stable boundary layer (namelist zetamaxstable = 2.0 of the traced run, FrictionVelocityMod.F90:1201), [-] |
| `vkc` | `1` | `0.4` | von Karman constant (clm_varcon.F90:53), [-] |
| `grav` | `m/s^2` | `9.80616` | gravitational acceleration (clm_varcon.F90:51), [m/s^2] |
| `zetam` | `1` | `1.574` | transition point of the flux-gradient relation, wind profile (FrictionVelocityMod.F90:795), [-] |
| `zetat` | `1` | `0.465` | transition point of the flux-gradient relation, temperature profile (FrictionVelocityMod.F90:796), [-] |
| `meier_param3` | `1` | `70.0` | Meier et al. (2022) empirical constant (clm_varcon.F90:171), [-] |
| `nu_param` | `m^2/s` | `1.5e-05` | kinematic viscosity of air (clm_varcon.F90:165), [m^2/s] |
| `beta_param` | `s^0.5/m^0.5/K^0.25` | `7.2` | Meier et al. (2022) empirical constant (clm_varcon.F90:164), [(s/m)^0.5/K^0.25] |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `zldis_u` | `m` |  | momentum profile height zldis = forc_hgt_u_patch - displa with displa = 0 (FrictionVelocityMod.F90:850-853), equal to the pre-iteration zldis = forc_hgt_u + z0mg of BareGroundFluxesMod.F90:322 (z0m = z0mg_patch is constant across the iteration), so it serves as the iteration height in zeta_raw and obu and the redundant parent zldis coupling is dropped, [m] |
| `zldis_t` | `m` |  | scalar profile height zldis = forc_hgt_t_patch - displa (FrictionVelocityMod.F90:946-949), [m] |
| `zldis_2m` | `m` |  | 2-m profile height zldis = 2.0 + z0h (FrictionVelocityMod.F90:1022-1025), [m] |
| `ustar` | `m/s` |  | friction velocity (FrictionVelocityMod.F90:857-871), [m/s] |
| `temp1` | `1` |  | inverse integrated temperature profile at the measurement height (FrictionVelocityMod.F90:956-970), [-] |
| `temp2` | `1` |  | inverse integrated humidity profile at the measurement height, equal to temp1 by the equality branch (FrictionVelocityMod.F90:997-998, forc_hgt_q == forc_hgt_t and z0q == z0h in the traced run), [-] |
| `temp12m` | `1` |  | inverse integrated temperature profile at 2 m (FrictionVelocityMod.F90:1022-1038), [-] |
| `temp22m` | `1` |  | inverse integrated humidity profile at 2 m, equal to temp12m by the equality branch (FrictionVelocityMod.F90:1051-1052, z0q == z0h in the traced run), [-] |
| `tstar` | `K` |  | temperature scale tstar = temp1*dth (BareGroundFluxesMod.F90:354), [K] |
| `qstar` | `kg/kg` |  | humidity scale qstar = temp2*dqh (BareGroundFluxesMod.F90:355), [kg/kg] |
| `z0h` | `m` |  | updated scalar roughness over ground z0hg_patch, Meier2022 branch (BareGroundFluxesMod.F90:364), [m] |
| `thvstar` | `K` |  | virtual potential temperature scale thvstar = tstar*(1 + 0.61*forc_q) + 0.61*forc_th*qstar (BareGroundFluxesMod.F90:375), [K] |
| `zeta_raw` | `1` |  | unclamped stability parameter zeta = zldis_u*vkc*grav*thvstar/(ustar^2*thv) (BareGroundFluxesMod.F90:376, with zldis_u the iteration height), [-] |
| `zeta` | `1` |  | clamped stability parameter: the sign-preserving clamp of clamp_zeta applied to zeta_raw (BareGroundFluxesMod.F90:378-386; the same clamp as the MoninObukIni initialization, FrictionVelocityMod.F90:1200-1204), [-] |
| `wc` | `m/s` |  | convective velocity wc = beta*max(-grav*ustar*thvstar*zii/thv, 0)^0.333 (BareGroundFluxesMod.F90:383, the Fortran's 0.333_r8 exponent), written with the base nondimensionalized by 1 m^3/s^3 so the unit algebra closes (the unit checker only reduces exact rational exponents on dimensional bases). The Fortran evaluates wc only on the unstable branch (zeta < 0, where thvstar < 0 and the base is positive); the esm computes it unconditionally, so the base is clamped at zero to keep the stable rows finite (a negative base to the 0.333 power is NaN) without changing any unstable-branch value. Documented divergence: the Fortran local wc is only read by the unstable um branch and otherwise keeps its MoninObukIni seed 0.5 m/s stale, so computing it unconditionally is observationally identical and the dead wc threading is dropped (on stable rows this wc is 0, never read), [m/s] |
| `um` | `m/s` |  | updated wind speed: stable branch (zeta_raw >= 0) um = max(ur, 0.1 m/s), unstable branch um = sqrt(ur^2 + wc^2) (BareGroundFluxesMod.F90:380,384) - the monin_obukhov_initial_wind law applied to the iteration branch test, [m/s] |
| `obu` | `m` |  | updated Obukhov length obu = zldis/zeta (BareGroundFluxesMod.F90:387), [m] |

## Observed expressions

$$
zldis_{u} = forc_{hgt\,u} + z0m
$$
_momentum profile height zldis = forc_hgt_u_patch - displa with displa = 0 (FrictionVelocityMod.F90:850-853), equal to the pre-iteration zldis = forc_hgt_u + z0mg of BareGroundFluxesMod.F90:322 (z0m = z0mg_patch is constant across the iteration), so it serves as the iteration height in zeta_raw and obu and the redundant parent zldis coupling is dropped, [m]_

$$
zldis_{t} = forc_{hgt\,t} + z0h_{prev}
$$
_scalar profile height zldis = forc_hgt_t_patch - displa (FrictionVelocityMod.F90:946-949), [m]_

$$
zldis_{2m} = \mathrm{const}\left(\right) + z0h_{prev}
$$
_2-m profile height zldis = 2.0 + z0h (FrictionVelocityMod.F90:1022-1025), [m]_

$$
ustar = \mathrm{friction_velocity_momentum}\left(vkc=vkc, um=um_{prev}, zldis=zldis_{u}, z0m=z0m, obu=obu_{prev}, zetam=zetam, zeta=\frac{zldis_{u}}{obu_{prev}}\right)
$$
_friction velocity (FrictionVelocityMod.F90:857-871), [m/s]_

$$
temp1 = \mathrm{friction_velocity_scalar}\left(vkc=vkc, zldis=zldis_{t}, z0=z0h_{prev}, obu=obu_{prev}, zetat=zetat, zeta=\frac{zldis_{t}}{obu_{prev}}\right)
$$
_inverse integrated temperature profile at the measurement height (FrictionVelocityMod.F90:956-970), [-]_

$$
temp2 = temp1
$$
_inverse integrated humidity profile at the measurement height, equal to temp1 by the equality branch (FrictionVelocityMod.F90:997-998, forc_hgt_q == forc_hgt_t and z0q == z0h in the traced run), [-]_

$$
temp12m = \mathrm{friction_velocity_scalar}\left(vkc=vkc, zldis=zldis_{2m}, z0=z0h_{prev}, obu=obu_{prev}, zetat=zetat, zeta=\frac{zldis_{2m}}{obu_{prev}}\right)
$$
_inverse integrated temperature profile at 2 m (FrictionVelocityMod.F90:1022-1038), [-]_

$$
temp22m = temp12m
$$
_inverse integrated humidity profile at 2 m, equal to temp12m by the equality branch (FrictionVelocityMod.F90:1051-1052, z0q == z0h in the traced run), [-]_

$$
tstar = temp1 \cdot dth
$$
_temperature scale tstar = temp1*dth (BareGroundFluxesMod.F90:354), [K]_

$$
qstar = temp2 \cdot dqh
$$
_humidity scale qstar = temp2*dqh (BareGroundFluxesMod.F90:355), [kg/kg]_

$$
z0h = \mathrm{z0hg_meier2022}\left(meier_{param3}=meier_{param3}, nu_{param}=nu_{param}, ustar=ustar, beta_{param}=beta_{param}, tstar=tstar\right)
$$
_updated scalar roughness over ground z0hg_patch, Meier2022 branch (BareGroundFluxesMod.F90:364), [m]_

$$
thvstar = \mathrm{virtual_potential_scale}\left(x=tstar, forc_{q}=forc_{q}, forc_{th}=forc_{th}, y=qstar\right)
$$
_virtual potential temperature scale thvstar = tstar*(1 + 0.61*forc_q) + 0.61*forc_th*qstar (BareGroundFluxesMod.F90:375), [K]_

$$
zeta_{raw} = \frac{zldis_{u} \cdot vkc \cdot grav \cdot thvstar}{ustar^{2} \cdot thv}
$$
_unclamped stability parameter zeta = zldis_u*vkc*grav*thvstar/(ustar^2*thv) (BareGroundFluxesMod.F90:376, with zldis_u the iteration height), [-]_

$$
zeta = \mathrm{clamp_zeta}\left(zeta=zeta_{raw}, zetamaxstable=zetamaxstable\right)
$$
_clamped stability parameter: the sign-preserving clamp of clamp_zeta applied to zeta_raw (BareGroundFluxesMod.F90:378-386; the same clamp as the MoninObukIni initialization, FrictionVelocityMod.F90:1200-1204), [-]_

$$
wc = beta \cdot \mathrm{const}\left(\right) \cdot \mathrm{max}\left(\frac{\left(-grav\right) \cdot ustar \cdot thvstar \cdot zii}{thv \cdot \mathrm{const}\left(\right)}, 0.0\right)^{0.333}
$$
_convective velocity wc = beta*max(-grav*ustar*thvstar*zii/thv, 0)^0.333 (BareGroundFluxesMod.F90:383, the Fortran's 0.333_r8 exponent), written with the base nondimensionalized by 1 m^3/s^3 so the unit algebra closes (the unit checker only reduces exact rational exponents on dimensional bases). The Fortran evaluates wc only on the unstable branch (zeta < 0, where thvstar < 0 and the base is positive); the esm computes it unconditionally, so the base is clamped at zero to keep the stable rows finite (a negative base to the 0.333 power is NaN) without changing any unstable-branch value. Documented divergence: the Fortran local wc is only read by the unstable um branch and otherwise keeps its MoninObukIni seed 0.5 m/s stale, so computing it unconditionally is observationally identical and the dead wc threading is dropped (on stable rows this wc is 0, never read), [m/s]_

$$
um = \mathrm{monin_obukhov_initial_wind}\left(dthv=zeta_{raw}, ur=ur, wc=wc\right)
$$
_updated wind speed: stable branch (zeta_raw >= 0) um = max(ur, 0.1 m/s), unstable branch um = sqrt(ur^2 + wc^2) (BareGroundFluxesMod.F90:380,384) - the monin_obukhov_initial_wind law applied to the iteration branch test, [m/s]_

$$
obu = \frac{zldis_{u}}{zeta}
$$
_updated Obukhov length obu = zldis/zeta (BareGroundFluxesMod.F90:387), [m]_

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "expression_template_imports": [
    {
      "ref": "./clm_templates.esm"
    }
  ],
  "variables": {
    "forc_hgt_u": {
      "type": "parameter",
      "shape": [
        "patch"
      ],
      "units": "m",
      "default": 30.0,
      "description": "observational height of wind at patch level (BareGroundFluxesMod.F90:370, forc_hgt_u_patch = forc_hgt_u + z0mg + displa with displa = 0), [m]"
    },
    "forc_hgt_t": {
      "type": "parameter",
      "shape": [
        "patch"
      ],
      "units": "m",
      "default": 30.0,
      "description": "observational height of temperature at patch level (forc_hgt_t_patch = forc_hgt_t + z0hg + displa), [m]"
    },
    "z0m": {
      "type": "parameter",
      "shape": [
        "patch"
      ],
      "units": "m",
      "default": 8.134020505760161e-05,
      "description": "momentum roughness length over ground z0mg_patch, constant across the stability iteration, [m]"
    },
    "z0h_prev": {
      "type": "parameter",
      "shape": [
        "patch"
      ],
      "units": "m",
      "default": 8.134020505760161e-05,
      "description": "previous update's scalar roughness z0hg_patch (seeded with z0mg, the initial set of SetRoughnessLengthsAndForcHeightsNonLake FrictionVelocityMod.F90:637), [m]"
    },
    "obu_prev": {
      "type": "parameter",
      "shape": [
        "patch"
      ],
      "units": "m",
      "default": 15.758842,
      "description": "previous update's Obukhov length obu (seeded by MoninObukIni), [m]"
    },
    "um_prev": {
      "type": "parameter",
      "shape": [
        "patch"
      ],
      "units": "m/s",
      "default": 1.0,
      "description": "previous update's wind speed um (seeded by MoninObukIni), [m/s]"
    },
    "ur": {
      "type": "parameter",
      "shape": [
        "patch"
      ],
      "units": "m/s",
      "default": 1.0,
      "description": "wind speed at the forcing height ur = max(wind_min, sqrt(forc_u^2 + forc_v^2)) with wind_min = 1.0 m/s (param file), [m/s]"
    },
    "dth": {
      "type": "parameter",
      "shape": [
        "patch"
      ],
      "units": "K",
      "default": 1.0,
      "description": "temperature difference dth = thm - t_grnd (BareGroundFluxesMod.F90:319), [K]"
    },
    "dqh": {
      "type": "parameter",
      "shape": [
        "patch"
      ],
      "units": "kg/kg",
      "default": 0.001,
      "description": "humidity difference dqh = forc_q - qg (BareGroundFluxesMod.F90:320), [kg/kg]"
    },
    "forc_q": {
      "type": "parameter",
      "shape": [
        "patch"
      ],
      "units": "kg/kg",
      "default": 0.003,
      "description": "atmospheric specific humidity at the forcing height, [kg/kg]"
    },
    "forc_th": {
      "type": "parameter",
      "shape": [
        "patch"
      ],
      "units": "K",
      "default": 290.0,
      "description": "atmospheric potential temperature at the forcing height forc_th = thv/(1 + 0.61*forc_q) (the traced dump does not carry forc_th; it is recovered from the dumped virtual potential temperature thv), [K]"
    },
    "thv": {
      "type": "parameter",
      "shape": [
        "patch"
      ],
      "units": "K",
      "default": 295.31,
      "description": "virtual potential temperature at the forcing height (BiogeophysPreFluxCalcsMod, dumped in clm_run_imports preflux), [K]"
    },
    "zii": {
      "type": "parameter",
      "shape": [
        "patch"
      ],
      "units": "m",
      "default": 1000.0,
      "description": "convective boundary layer height (BiogeophysPreFluxCalcsMod.F90:363, zii = 1000 m in the traced run), [m]"
    },
    "beta": {
      "type": "parameter",
      "shape": [
        "patch"
      ],
      "units": "1",
      "default": 1.0,
      "description": "coefficient for convective velocity (BiogeophysPreFluxCalcsMod.F90:362, beta = 1 in the traced run), [-]"
    },
    "zetamaxstable": {
      "type": "parameter",
      "shape": [
        "patch"
      ],
      "units": "1",
      "default": 2.0,
      "description": "maximum zeta in the stable boundary layer (namelist zetamaxstable = 2.0 of the traced run, FrictionVelocityMod.F90:1201), [-]"
    },
    "vkc": {
      "type": "parameter",
      "shape": [
        "patch"
      ],
      "units": "1",
      "default": 0.4,
      "description": "von Karman constant (clm_varcon.F90:53), [-]"
    },
    "grav": {
      "type": "parameter",
      "shape": [
        "patch"
      ],
      "units": "m/s^2",
      "default": 9.80616,
      "description": "gravitational acceleration (clm_varcon.F90:51), [m/s^2]"
    },
    "zetam": {
      "type": "parameter",
      "shape": [
        "patch"
      ],
      "units": "1",
      "default": 1.574,
      "description": "transition point of the flux-gradient relation, wind profile (FrictionVelocityMod.F90:795), [-]"
    },
    "zetat": {
      "type": "parameter",
      "shape": [
        "patch"
      ],
      "units": "1",
      "default": 0.465,
      "description": "transition point of the flux-gradient relation, temperature profile (FrictionVelocityMod.F90:796), [-]"
    },
    "meier_param3": {
      "type": "parameter",
      "shape": [
        "patch"
      ],
      "units": "1",
      "default": 70.0,
      "description": "Meier et al. (2022) empirical constant (clm_varcon.F90:171), [-]"
    },
    "nu_param": {
      "type": "parameter",
      "shape": [
        "patch"
      ],
      "units": "m^2/s",
      "default": 1.5e-05,
      "description": "kinematic viscosity of air (clm_varcon.F90:165), [m^2/s]"
    },
    "beta_param": {
      "type": "parameter",
      "shape": [
        "patch"
      ],
      "units": "s^0.5/m^0.5/K^0.25",
      "default": 7.2,
      "description": "Meier et al. (2022) empirical constant (clm_varcon.F90:164), [(s/m)^0.5/K^0.25]"
    },
    "zldis_u": {
      "type": "unknown",
      "shape": [
        "patch"
      ],
      "units": "m",
      "description": "momentum profile height zldis = forc_hgt_u_patch - displa with displa = 0 (FrictionVelocityMod.F90:850-853), equal to the pre-iteration zldis = forc_hgt_u + z0mg of BareGroundFluxesMod.F90:322 (z0m = z0mg_patch is constant across the iteration), so it serves as the iteration height in zeta_raw and obu and the redundant parent zldis coupling is dropped, [m]"
    },
    "zldis_t": {
      "type": "unknown",
      "shape": [
        "patch"
      ],
      "units": "m",
      "description": "scalar profile height zldis = forc_hgt_t_patch - displa (FrictionVelocityMod.F90:946-949), [m]"
    },
    "zldis_2m": {
      "type": "unknown",
      "shape": [
        "patch"
      ],
      "units": "m",
      "description": "2-m profile height zldis = 2.0 + z0h (FrictionVelocityMod.F90:1022-1025), [m]"
    },
    "ustar": {
      "type": "unknown",
      "shape": [
        "patch"
      ],
      "units": "m/s",
      "description": "friction velocity (FrictionVelocityMod.F90:857-871), [m/s]"
    },
    "temp1": {
      "type": "unknown",
      "shape": [
        "patch"
      ],
      "units": "1",
      "description": "inverse integrated temperature profile at the measurement height (FrictionVelocityMod.F90:956-970), [-]"
    },
    "temp2": {
      "type": "unknown",
      "shape": [
        "patch"
      ],
      "units": "1",
      "description": "inverse integrated humidity profile at the measurement height, equal to temp1 by the equality branch (FrictionVelocityMod.F90:997-998, forc_hgt_q == forc_hgt_t and z0q == z0h in the traced run), [-]"
    },
    "temp12m": {
      "type": "unknown",
      "shape": [
        "patch"
      ],
      "units": "1",
      "description": "inverse integrated temperature profile at 2 m (FrictionVelocityMod.F90:1022-1038), [-]"
    },
    "temp22m": {
      "type": "unknown",
      "shape": [
        "patch"
      ],
      "units": "1",
      "description": "inverse integrated humidity profile at 2 m, equal to temp12m by the equality branch (FrictionVelocityMod.F90:1051-1052, z0q == z0h in the traced run), [-]"
    },
    "tstar": {
      "type": "unknown",
      "shape": [
        "patch"
      ],
      "units": "K",
      "description": "temperature scale tstar = temp1*dth (BareGroundFluxesMod.F90:354), [K]"
    },
    "qstar": {
      "type": "unknown",
      "shape": [
        "patch"
      ],
      "units": "kg/kg",
      "description": "humidity scale qstar = temp2*dqh (BareGroundFluxesMod.F90:355), [kg/kg]"
    },
    "z0h": {
      "type": "unknown",
      "shape": [
        "patch"
      ],
      "units": "m",
      "description": "updated scalar roughness over ground z0hg_patch, Meier2022 branch (BareGroundFluxesMod.F90:364), [m]"
    },
    "thvstar": {
      "type": "unknown",
      "shape": [
        "patch"
      ],
      "units": "K",
      "description": "virtual potential temperature scale thvstar = tstar*(1 + 0.61*forc_q) + 0.61*forc_th*qstar (BareGroundFluxesMod.F90:375), [K]"
    },
    "zeta_raw": {
      "type": "unknown",
      "shape": [
        "patch"
      ],
      "units": "1",
      "description": "unclamped stability parameter zeta = zldis_u*vkc*grav*thvstar/(ustar^2*thv) (BareGroundFluxesMod.F90:376, with zldis_u the iteration height), [-]"
    },
    "zeta": {
      "type": "unknown",
      "shape": [
        "patch"
      ],
      "units": "1",
      "description": "clamped stability parameter: the sign-preserving clamp of clamp_zeta applied to zeta_raw (BareGroundFluxesMod.F90:378-386; the same clamp as the MoninObukIni initialization, FrictionVelocityMod.F90:1200-1204), [-]"
    },
    "wc": {
      "type": "unknown",
      "shape": [
        "patch"
      ],
      "units": "m/s",
      "description": "convective velocity wc = beta*max(-grav*ustar*thvstar*zii/thv, 0)^0.333 (BareGroundFluxesMod.F90:383, the Fortran's 0.333_r8 exponent), written with the base nondimensionalized by 1 m^3/s^3 so the unit algebra closes (the unit checker only reduces exact rational exponents on dimensional bases). The Fortran evaluates wc only on the unstable branch (zeta < 0, where thvstar < 0 and the base is positive); the esm computes it unconditionally, so the base is clamped at zero to keep the stable rows finite (a negative base to the 0.333 power is NaN) without changing any unstable-branch value. Documented divergence: the Fortran local wc is only read by the unstable um branch and otherwise keeps its MoninObukIni seed 0.5 m/s stale, so computing it unconditionally is observationally identical and the dead wc threading is dropped (on stable rows this wc is 0, never read), [m/s]"
    },
    "um": {
      "type": "unknown",
      "shape": [
        "patch"
      ],
      "units": "m/s",
      "description": "updated wind speed: stable branch (zeta_raw >= 0) um = max(ur, 0.1 m/s), unstable branch um = sqrt(ur^2 + wc^2) (BareGroundFluxesMod.F90:380,384) - the monin_obukhov_initial_wind law applied to the iteration branch test, [m/s]"
    },
    "obu": {
      "type": "unknown",
      "shape": [
        "patch"
      ],
      "units": "m",
      "description": "updated Obukhov length obu = zldis/zeta (BareGroundFluxesMod.F90:387), [m]"
    }
  },
  "equations": [
    {
      "lhs": "zldis_u",
      "rhs": {
        "op": "+",
        "args": [
          "forc_hgt_u",
          "z0m"
        ]
      }
    },
    {
      "lhs": "zldis_t",
      "rhs": {
        "op": "+",
        "args": [
          "forc_hgt_t",
          "z0h_prev"
        ]
      }
    },
    {
      "lhs": "zldis_2m",
      "rhs": {
        "op": "+",
        "args": [
          {
            "op": "const",
            "args": [],
            "value": 2.0,
            "units": "m"
          },
          "z0h_prev"
        ]
      }
    },
    {
      "lhs": "ustar",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "friction_velocity_momentum",
        "bindings": {
          "vkc": "vkc",
          "um": "um_prev",
          "zldis": "zldis_u",
          "z0m": "z0m",
          "obu": "obu_prev",
          "zetam": "zetam",
          "zeta": {
            "op": "/",
            "args": [
              "zldis_u",
              "obu_prev"
            ]
          }
        }
      }
    },
    {
      "lhs": "temp1",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "friction_velocity_scalar",
        "bindings": {
          "vkc": "vkc",
          "zldis": "zldis_t",
          "z0": "z0h_prev",
          "obu": "obu_prev",
          "zetat": "zetat",
          "zeta": {
            "op": "/",
            "args": [
              "zldis_t",
              "obu_prev"
            ]
          }
        }
      }
    },
    {
      "lhs": "temp2",
      "rhs": "temp1"
    },
    {
      "lhs": "temp12m",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "friction_velocity_scalar",
        "bindings": {
          "vkc": "vkc",
          "zldis": "zldis_2m",
          "z0": "z0h_prev",
          "obu": "obu_prev",
          "zetat": "zetat",
          "zeta": {
            "op": "/",
            "args": [
              "zldis_2m",
              "obu_prev"
            ]
          }
        }
      }
    },
    {
      "lhs": "temp22m",
      "rhs": "temp12m"
    },
    {
      "lhs": "tstar",
      "rhs": {
        "op": "*",
        "args": [
          "temp1",
          "dth"
        ]
      }
    },
    {
      "lhs": "qstar",
      "rhs": {
        "op": "*",
        "args": [
          "temp2",
          "dqh"
        ]
      }
    },
    {
      "lhs": "z0h",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "z0hg_meier2022",
        "bindings": {
          "meier_param3": "meier_param3",
          "nu_param": "nu_param",
          "ustar": "ustar",
          "beta_param": "beta_param",
          "tstar": "tstar"
        }
      }
    },
    {
      "lhs": "thvstar",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "virtual_potential_scale",
        "bindings": {
          "x": "tstar",
          "forc_q": "forc_q",
          "forc_th": "forc_th",
          "y": "qstar"
        }
      }
    },
    {
      "lhs": "zeta_raw",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "*",
            "args": [
              "zldis_u",
              "vkc",
              "grav",
              "thvstar"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "^",
                "args": [
                  "ustar",
                  2
                ]
              },
              "thv"
            ]
          }
        ]
      }
    },
    {
      "lhs": "zeta",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "clamp_zeta",
        "bindings": {
          "zeta": "zeta_raw",
          "zetamaxstable": "zetamaxstable"
        }
      }
    },
    {
      "lhs": "wc",
      "rhs": {
        "op": "*",
        "args": [
          "beta",
          {
            "op": "const",
            "args": [],
            "value": 1.0,
            "units": "m/s"
          },
          {
            "op": "^",
            "args": [
              {
                "op": "max",
                "args": [
                  {
                    "op": "/",
                    "args": [
                      {
                        "op": "*",
                        "args": [
                          {
                            "op": "-",
                            "args": [
                              "grav"
                            ]
                          },
                          "ustar",
                          "thvstar",
                          "zii"
                        ]
                      },
                      {
                        "op": "*",
                        "args": [
                          "thv",
                          {
                            "op": "const",
                            "args": [],
                            "value": 1.0,
                            "units": "m^3/s^3"
                          }
                        ]
                      }
                    ]
                  },
                  0.0
                ]
              },
              0.333
            ]
          }
        ]
      }
    },
    {
      "lhs": "um",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "monin_obukhov_initial_wind",
        "bindings": {
          "dthv": "zeta_raw",
          "ur": "ur",
          "wc": "wc"
        }
      }
    },
    {
      "lhs": "obu",
      "rhs": {
        "op": "/",
        "args": [
          "zldis_u",
          "zeta"
        ]
      }
    }
  ]
}
```

</details>
