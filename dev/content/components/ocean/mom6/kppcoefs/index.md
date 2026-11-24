---
title: "KPPCoefs"
slug: "kppcoefs"
domains: ["ocean"]
component_types: ["model"]
subdomains: ["mom6"]
domain: "ocean"
subdomain: "mom6"
component_type: "model"
esm_version: "1.3.0"
esm_path: "components/ocean/mom6/mom6_kpp.esm"
reference: "https://github.com/ESCOMP/CESM"
description: "Stage-2 implementation of the MOM6 CVMix KPP planetary boundary layer parameterization (MOM6 dev/ncar_260909 @301879336, fork stage1/EqESM-cesm-mom6 branch instrument/mom6-dumps; run configuration C_JRA_t62_mom6_inst: RI_CRIT=0.3, VON_KARMAN=0.4, SURF_LAYER_EXTENT=0.1, MINIMUM_OBL_DEPTH=5.0, MINIMUM_VT2=1e-10, INTERP_TYPE=quadratic, INTERP_TYPE2=LMD94, MATCH_TECHNIQUE=MatchGradient, ENHANCE_DIFFUSION=False, NLT_SHAPE=CVMix, N_SMOOTH=3, COMPUTE_MONIN_OBUKHOV=True, COMPUTE_EKMAN=False, USE_KPP_LT_K/VT2=False, KPP_IS_ADDITIVE=False, KPP_SHORTWAVE_METHOD=MXL_SW, l_LMD_ws=false, lnoDGat1=true, all unit rescale factors 1.0). Two models: KPPBLD reproduces KPP_compute_BLD (MOM_CVMix_KPP.F90:1195-1575) down to the pre-smoothing OBL depth and kOBL — the surface-layer averages (F90:1342-1405), the per-assumed-OBL hydrostatic pressure for the Wright 1997 EOS (F90:1428-1440, the shared wright_rho composition of ./mom6_templates.esm, whose 15 coefficients are the wright_coeff_* constant fragments shared with mom6_eos.esm), deltaBuoy/N2/N (F90:1444-1457), w_s/Vt^2/BulkRi (F90:1509-1550 via the ./mom6_kpp_templates.esm laws), and OBL_depth_low/kOBL (cvmix_kpp.F90:1585-1814, 1821-1867) with the quadratic interpolation, the Monin-Obukhov limit, the minOBLdepth floor and the MOM6 top/bottom bounds. The column prefix sums of the geometry and hydrostatics — the interface depths depth (and so the heights z_inter = -depth and z_cell), and the reference pressure pRef = p_surf + PRESS_STEP*depth — are ESD integral operators lowered by the local ./mom6_column_discretization.esm rules (the EarthSciDiscretizations column_nonuniform_1d integral_lev_nodes_cumulative_from_bottom and integral_lev_cumulative_from_bottom imports, the exact exclusive-prefix and midpoint stencils of the Fortran iFaceHeight/cellHeight/pRef loops, F90:1237-1243 and F90:1452-1456; see README.md for the summation-order notes). KPPCoefs reproduces cvmix_coeffs_kpp_low (cvmix_kpp.F90:701-1298, not lStokesMOST, MatchGradient, ENHANCE_DIFFUSION=False: the no-match shape G(sigma) = sigma*(1-sigma)^2, the diffusivity/viscosity overwrite at interfaces 2..floor(kOBL), the KPP_IS_ADDITIVE=False replacement of nonzero entries via the kpp_override_nonzero template (Kd_salt = Kd_heat), and the CVMix non-local term) driven by the SMOOTHED OBLdepth/kOBL, z_inter, uStar, surfBuoyFlux (MXL_SW) and the incoming Kt/Ks/Kv from mom6_kpp.csv. Pins: mom6_kpp_obl.csv rows for BulkRi/deltaU2/N2 at layers 2..kOBL+3 (layer 1 is 0 by construction), spot z_cell at layers 1..kOBL+3 and z_inter at ifaces 2..kOBL+3 (iface 1 is the surface) plus the deep z_cell/z_inter at layer/iface 75, and OBLdepth/kOBL (rel 1e-12; the N_SMOOTH=3 Laplacian smoothing of KPP_smooth_BLD is inherently horizontal and is NOT reproduced — the pre-smoothing values are pinned and the smoothed values are consumed as inputs), and mom6_kpp.csv rows for Kd_heat/Kv at interfaces 2..kwup plus one pass-through Kv_out at kwup+1 (the kpp_override_nonzero else-branch). Unpinned (never exercised by the 156 traced columns; see README.md): the OBL_limit branch (no traced column has BulkRi <= 0.3 everywhere, kfirst = N_LAYER+1), the interpolated OBL depth of the kfirst = 2 and 3 rows (always floored to MINIMUM_OBL_DEPTH in the traces), the unstable (surfBuoyFlux < 0) branches of the stability functions and of the non-local term, the Langmuir enhancement paths, and the MINIMUM_VT2 floor."
tags: ["ocean", "mom6", "model", "kpp", "boundary-layer", "mixing", "cesm"]
---

## Description

Stage-2 implementation of the MOM6 CVMix KPP planetary boundary layer parameterization (MOM6 dev/ncar_260909 @301879336, fork stage1/EqESM-cesm-mom6 branch instrument/mom6-dumps; run configuration C_JRA_t62_mom6_inst: RI_CRIT=0.3, VON_KARMAN=0.4, SURF_LAYER_EXTENT=0.1, MINIMUM_OBL_DEPTH=5.0, MINIMUM_VT2=1e-10, INTERP_TYPE=quadratic, INTERP_TYPE2=LMD94, MATCH_TECHNIQUE=MatchGradient, ENHANCE_DIFFUSION=False, NLT_SHAPE=CVMix, N_SMOOTH=3, COMPUTE_MONIN_OBUKHOV=True, COMPUTE_EKMAN=False, USE_KPP_LT_K/VT2=False, KPP_IS_ADDITIVE=False, KPP_SHORTWAVE_METHOD=MXL_SW, l_LMD_ws=false, lnoDGat1=true, all unit rescale factors 1.0). Two models: KPPBLD reproduces KPP_compute_BLD (MOM_CVMix_KPP.F90:1195-1575) down to the pre-smoothing OBL depth and kOBL — the surface-layer averages (F90:1342-1405), the per-assumed-OBL hydrostatic pressure for the Wright 1997 EOS (F90:1428-1440, the shared wright_rho composition of ./mom6_templates.esm, whose 15 coefficients are the wright_coeff_* constant fragments shared with mom6_eos.esm), deltaBuoy/N2/N (F90:1444-1457), w_s/Vt^2/BulkRi (F90:1509-1550 via the ./mom6_kpp_templates.esm laws), and OBL_depth_low/kOBL (cvmix_kpp.F90:1585-1814, 1821-1867) with the quadratic interpolation, the Monin-Obukhov limit, the minOBLdepth floor and the MOM6 top/bottom bounds. The column prefix sums of the geometry and hydrostatics — the interface depths depth (and so the heights z_inter = -depth and z_cell), and the reference pressure pRef = p_surf + PRESS_STEP*depth — are ESD integral operators lowered by the local ./mom6_column_discretization.esm rules (the EarthSciDiscretizations column_nonuniform_1d integral_lev_nodes_cumulative_from_bottom and integral_lev_cumulative_from_bottom imports, the exact exclusive-prefix and midpoint stencils of the Fortran iFaceHeight/cellHeight/pRef loops, F90:1237-1243 and F90:1452-1456; see README.md for the summation-order notes). KPPCoefs reproduces cvmix_coeffs_kpp_low (cvmix_kpp.F90:701-1298, not lStokesMOST, MatchGradient, ENHANCE_DIFFUSION=False: the no-match shape G(sigma) = sigma*(1-sigma)^2, the diffusivity/viscosity overwrite at interfaces 2..floor(kOBL), the KPP_IS_ADDITIVE=False replacement of nonzero entries via the kpp_override_nonzero template (Kd_salt = Kd_heat), and the CVMix non-local term) driven by the SMOOTHED OBLdepth/kOBL, z_inter, uStar, surfBuoyFlux (MXL_SW) and the incoming Kt/Ks/Kv from mom6_kpp.csv. Pins: mom6_kpp_obl.csv rows for BulkRi/deltaU2/N2 at layers 2..kOBL+3 (layer 1 is 0 by construction), spot z_cell at layers 1..kOBL+3 and z_inter at ifaces 2..kOBL+3 (iface 1 is the surface) plus the deep z_cell/z_inter at layer/iface 75, and OBLdepth/kOBL (rel 1e-12; the N_SMOOTH=3 Laplacian smoothing of KPP_smooth_BLD is inherently horizontal and is NOT reproduced — the pre-smoothing values are pinned and the smoothed values are consumed as inputs), and mom6_kpp.csv rows for Kd_heat/Kv at interfaces 2..kwup plus one pass-through Kv_out at kwup+1 (the kpp_override_nonzero else-branch). Unpinned (never exercised by the 156 traced columns; see README.md): the OBL_limit branch (no traced column has BulkRi <= 0.3 everywhere, kfirst = N_LAYER+1), the interpolated OBL depth of the kfirst = 2 and 3 rows (always floored to MINIMUM_OBL_DEPTH in the traces), the unstable (surfBuoyFlux < 0) branches of the stability functions and of the non-local term, the Langmuir enhancement paths, and the MINIMUM_VT2 floor.

KPPBLD: The boundary-layer depth computation of KPP_compute_BLD (MOM_CVMix_KPP.F90:1195-1575) with the CVMix OBL_depth_low interpolation and the kOBL fraction (cvmix_kpp.F90:1585-1867). Inputs are the per-column traced state: layer thicknesses h and heights dz (equal in the instrumented run: no thickness inflation, min_thickness=0), temperature/salinity/velocity T, S, U_H, V_H, the surface buoyancy flux profile buoyFlux(1..76) (from calculateBuoyancyFlux2d, buoyFlux(N_IFACE) = 0), the surface friction velocity uStar and the surface pressure p_surf; outputs include the per-layer bulk Richardson numbers, the squared resolved shear and buoyancy frequency, the OBL depth and its fractional index. The EOS is applied as the wright_rho composition of ./mom6_templates.esm (one application per state: the surface-layer mean, the layer value and the layer-1 value, all at the layer-top pressure pRef), whose 15 Wright coefficients are the shared wright_coeff_* constant fragments (bound by reference, also in mom6_eos.esm's WrightEOS); the pointwise KPP laws come from ./mom6_kpp_templates.esm. The N_SMOOTH=3 horizontal Laplacian smoothing of KPP_smooth_BLD is not reproduced (single-column law); OBLdepth/kOBL here are the PRE-smoothing values (mom6_kpp_obl.csv).

KPPCoefs: The KPP diffusivity/viscosity/non-local coefficient computation of cvmix_coeffs_kpp_low (cvmix_kpp.F90:701-1298, not lStokesMOST) with the MOM6 wrappers of KPP_calculate (MOM_CVMix_KPP.F90:740-1067): inputs are the SMOOTHED OBLdepth/kOBL (after the N_SMOOTH=3 Laplacian of KPP_smooth_BLD, which is not reproduced here), the interface heights z_inter, uStar, the MXL_SW surface buoyancy flux surfBuoyFlux = buoyFlux(1) - buoyFlux(floor(kOBL)+1) (F90:848-853) and the incoming diffusivities Kt_in/Ks_in/Kv_in. With MATCH_TECHNIQUE=MatchGradient and ENHANCE_DIFFUSION=False, MOM6 zeroes the interior diffusivities before the CVMix call (F90:903-906), so the shape function is the no-match cubic G(sigma) = sigma*(1-sigma)^2 (G(1) = G'(1) = 0), and the overwrite loop 2..floor(kOBL) with the kwup==ktup zero restoration gives nonzero coefficients exactly on interfaces 2..floor(kOBL). KPP_IS_ADDITIVE=False: an output interface keeps the incoming value unless the KPP value is nonzero (F90:1023-1038). The non-local term is the CVMix law Tnonlocal = nonlocal_coeff*G(sigma) on interfaces 2..kwup when surfBuoyFlux < 0 (NLT_SHAPE=CVMix: MOM6 does not override), with nonlocal_coeff = Cstar*kappa*(kappa*eps*c_s)^(1/3), Cstar = 10; all traced columns are stable (surfBuoyFlux >= 0), so NLT is pinned at zero and the unstable branch is unpinned.

## Reference

- MOM6 (Modular Ocean Model 6), ESCOMP/CESM components/mom (dev/ncar_260909 @301879336; instrumented fork stage1/EqESM-cesm-mom6 branch instrument/mom6-dumps, reference run C_JRA_t62_mom6_inst): src/parameterizations/vertical/MOM_CVMix_KPP.F90 (KPP_compute_BLD 1195-1575, KPP_calculate 740-1067, KPP_smooth_BLD 1715-1834) and pkg/CVMix-src/src/shared/cvmix_kpp.F90 (OBL_depth_low 1585-1814, kOBL 1821-1867, coeffs_kpp_low 701-1298) - the reference implementation these components are transcribed from.
- EarthSciModels - the authoritative .esm corpus this component lives in.

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `OBLdepth_s` | `m` | `0.0` | The smoothed boundary-layer depth from mom6_kpp.csv (after KPP_smooth_BLD), [m] |
| `kOBL_s` | `dimensionless` | `0.0` | The smoothed fractional OBL index from mom6_kpp.csv, [-] |
| `uStar_s` | `m s^-1` | `0.0` | Surface friction velocity in MKS, [m s-1] |
| `surfBuoyFlux_s` | `m^2 s^-3` | `0.0` | The MXL_SW surface buoyancy flux buoy_scale*(buoyFlux(1) - buoyFlux(int(kOBL)+1)) from mom6_kpp.csv, [m2 s-3] |
| `z_inter_s` | `m` | `0.0` | Interface heights from mom6_kpp.csv (recomputed identically to the BLD step), [m] |
| `Kt_in` | `m^2 s^-1` | `0.0` | Incoming heat diffusivity (before KPP), [m2 s-1] |
| `Ks_in` | `m^2 s^-1` | `0.0` | Incoming salt diffusivity, [m2 s-1] |
| `Kv_in` | `m^2 s^-1` | `0.0` | Incoming viscosity, [m2 s-1] |
| `VON_KARMAN` | `dimensionless` | `0.4` |  |
| `SURF_LAYER_EXT` | `dimensionless` | `0.1` |  |
| `ZETA_M` | `dimensionless` | `-0.2` |  |
| `ZETA_S` | `dimensionless` | `-1.0` |  |
| `A_M` | `dimensionless` | `1.2573615701844176` |  |
| `C_M` | `dimensionless` | `8.382410467896117` |  |
| `A_S` | `dimensionless` | `-28.861739379323623` |  |
| `C_S` | `dimensionless` | `98.95453501482385` |  |
| `CSTAR` | `dimensionless` | `10.0` | The Cstar constant of the non-local coefficient (cvmix_kpp.F90:576-584, default 10), [-] |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `kwup` | `dimensionless` | `0.0` | The interface index above the OBL: floor(kOBL) (cvmix_kpp.F90:836-837), [-] |
| `sigma` | `dimensionless` | `0.0` | sigma = -z_inter/OBLdepth at interfaces (cvmix_kpp.F90:1224), [-] |
| `w_s` | `m s^-1` | `0.0` | Scalar turbulent velocity scale at the interfaces (turbulent_scales_1d_OBL with the scalar surface flux), [m s-1] |
| `w_m` | `m s^-1` | `0.0` | Momentum turbulent velocity scale at the interfaces, [m s-1] |
| `G` | `dimensionless` | `0.0` | The no-match shape function G(sigma) = sigma*(1-sigma)^2 (evaluate_cubic order), [-] |
| `Kd_heat` | `m^2 s^-1` | `0.0` | The KPP heat diffusivity on interfaces 2..kwup, zero elsewhere (OBL_Tdiff), [m2 s-1] |
| `Kd_salt` | `m^2 s^-1` | `0.0` | The KPP salt diffusivity (OBL_Sdiff), [m2 s-1] |
| `Kv` | `m^2 s^-1` | `0.0` | The KPP viscosity (OBL_Mdiff), [m2 s-1] |
| `nonlocal_coeff` | `dimensionless` | `0.0` | Cstar*kappa*(kappa*eps*c_s)^(1/3) = 6.327399015078757 (cvmix_kpp.F90:576-584), [-] |
| `Kt_out` | `m^2 s^-1` | `0.0` | Heat diffusivity after KPP: the KPP value where nonzero, else the incoming value (F90:1023-1038), [m2 s-1] |
| `Ks_out` | `m^2 s^-1` | `0.0` | Salt diffusivity after KPP, [m2 s-1] |
| `Kv_out` | `m^2 s^-1` | `0.0` | Viscosity after KPP, [m2 s-1] |
| `NLT_heat` | `dimensionless` | `0.0` | The CVMix non-local heat transport nonlocal_coeff*G(sigma) on interfaces 2..kwup when surfBuoyFlux < 0 (all traced columns are stable: pinned at zero; NLT_SHAPE=CVMix, so MOM6's override block at MOM_CVMix_KPP.F90:960-1001 is inactive), [-] |
| `NLT_salt` | `dimensionless` | `0.0` | The CVMix non-local salt transport, equal to the heat term (nonLocalTrans(:,2) = nonLocalTrans(:,1), MOM_CVMix_KPP.F90:1002-1003), [-] |

## Observed expressions

$$
kwup = \mathrm{floor}\left(kOBL_{s}\right)
$$
_The interface index above the OBL: floor(kOBL) (cvmix_kpp.F90:836-837), [-]_

$$
sigma = \mathrm{faq}\left(z_{inter\,s}\right)
$$
_sigma = -z_inter/OBLdepth at interfaces (cvmix_kpp.F90:1224), [-]_

$$
w_{s} = \mathrm{faq}\left(sigma\right)
$$
_Scalar turbulent velocity scale at the interfaces (turbulent_scales_1d_OBL with the scalar surface flux), [m s-1]_

$$
w_{m} = \mathrm{faq}\left(sigma\right)
$$
_Momentum turbulent velocity scale at the interfaces, [m s-1]_

$$
G = \mathrm{faq}\left(sigma\right)
$$
_The no-match shape function G(sigma) = sigma*(1-sigma)^2 (evaluate_cubic order), [-]_

$$
Kd_{heat} = \mathrm{faq}\left(w_{s}, G\right)
$$
_The KPP heat diffusivity on interfaces 2..kwup, zero elsewhere (OBL_Tdiff), [m2 s-1]_

$$
Kd_{salt} = Kd_{heat}
$$
_The KPP salt diffusivity (OBL_Sdiff), [m2 s-1]_

$$
Kv = \mathrm{faq}\left(w_{m}, G\right)
$$
_The KPP viscosity (OBL_Mdiff), [m2 s-1]_

$$
nonlocal_{coeff} = CSTAR \cdot VON_{KARMAN} \cdot \left(VON_{KARMAN} \cdot SURF_{LAYER\,EXT} \cdot C_{S}\right)^{\frac{1.0}{3.0}}
$$
_Cstar*kappa*(kappa*eps*c_s)^(1/3) = 6.327399015078757 (cvmix_kpp.F90:576-584), [-]_

$$
Kt_{out} = \mathrm{faq}\left(Kd_{heat}, Kt_{in}\right)
$$
_Heat diffusivity after KPP: the KPP value where nonzero, else the incoming value (F90:1023-1038), [m2 s-1]_

$$
Ks_{out} = \mathrm{faq}\left(Kd_{salt}, Ks_{in}\right)
$$
_Salt diffusivity after KPP, [m2 s-1]_

$$
Kv_{out} = \mathrm{faq}\left(Kv, Kv_{in}\right)
$$
_Viscosity after KPP, [m2 s-1]_

$$
NLT_{heat} = \mathrm{faq}\left(G\right)
$$
_The CVMix non-local heat transport nonlocal_coeff*G(sigma) on interfaces 2..kwup when surfBuoyFlux < 0 (all traced columns are stable: pinned at zero; NLT_SHAPE=CVMix, so MOM6's override block at MOM_CVMix_KPP.F90:960-1001 is inactive), [-]_

$$
NLT_{salt} = NLT_{heat}
$$
_The CVMix non-local salt transport, equal to the heat term (nonLocalTrans(:,2) = nonLocalTrans(:,1), MOM_CVMix_KPP.F90:1002-1003), [-]_

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "expression_template_imports": [
    {
      "ref": "./mom6_column_discretization.esm"
    },
    {
      "ref": "./mom6_kpp_templates.esm"
    }
  ],
  "variables": {
    "OBLdepth_s": {
      "type": "parameter",
      "units": "m",
      "default": 0.0,
      "description": "The smoothed boundary-layer depth from mom6_kpp.csv (after KPP_smooth_BLD), [m]"
    },
    "kOBL_s": {
      "type": "parameter",
      "units": "dimensionless",
      "default": 0.0,
      "description": "The smoothed fractional OBL index from mom6_kpp.csv, [-]"
    },
    "uStar_s": {
      "type": "parameter",
      "units": "m s^-1",
      "default": 0.0,
      "description": "Surface friction velocity in MKS, [m s-1]"
    },
    "surfBuoyFlux_s": {
      "type": "parameter",
      "units": "m^2 s^-3",
      "default": 0.0,
      "description": "The MXL_SW surface buoyancy flux buoy_scale*(buoyFlux(1) - buoyFlux(int(kOBL)+1)) from mom6_kpp.csv, [m2 s-3]"
    },
    "z_inter_s": {
      "type": "parameter",
      "shape": [
        "iface"
      ],
      "units": "m",
      "default": 0.0,
      "description": "Interface heights from mom6_kpp.csv (recomputed identically to the BLD step), [m]"
    },
    "Kt_in": {
      "type": "parameter",
      "shape": [
        "iface"
      ],
      "units": "m^2 s^-1",
      "default": 0.0,
      "description": "Incoming heat diffusivity (before KPP), [m2 s-1]"
    },
    "Ks_in": {
      "type": "parameter",
      "shape": [
        "iface"
      ],
      "units": "m^2 s^-1",
      "default": 0.0,
      "description": "Incoming salt diffusivity, [m2 s-1]"
    },
    "Kv_in": {
      "type": "parameter",
      "shape": [
        "iface"
      ],
      "units": "m^2 s^-1",
      "default": 0.0,
      "description": "Incoming viscosity, [m2 s-1]"
    },
    "VON_KARMAN": {
      "type": "parameter",
      "units": "dimensionless",
      "default": 0.4
    },
    "SURF_LAYER_EXT": {
      "type": "parameter",
      "units": "dimensionless",
      "default": 0.1
    },
    "ZETA_M": {
      "type": "parameter",
      "units": "dimensionless",
      "default": -0.2
    },
    "ZETA_S": {
      "type": "parameter",
      "units": "dimensionless",
      "default": -1.0
    },
    "A_M": {
      "type": "parameter",
      "units": "dimensionless",
      "default": 1.2573615701844176
    },
    "C_M": {
      "type": "parameter",
      "units": "dimensionless",
      "default": 8.382410467896117
    },
    "A_S": {
      "type": "parameter",
      "units": "dimensionless",
      "default": -28.861739379323623
    },
    "C_S": {
      "type": "parameter",
      "units": "dimensionless",
      "default": 98.95453501482385
    },
    "CSTAR": {
      "type": "parameter",
      "units": "dimensionless",
      "default": 10.0,
      "description": "The Cstar constant of the non-local coefficient (cvmix_kpp.F90:576-584, default 10), [-]"
    },
    "kwup": {
      "type": "unknown",
      "units": "dimensionless",
      "default": 0.0,
      "description": "The interface index above the OBL: floor(kOBL) (cvmix_kpp.F90:836-837), [-]"
    },
    "sigma": {
      "type": "unknown",
      "shape": [
        "iface"
      ],
      "units": "dimensionless",
      "default": 0.0,
      "description": "sigma = -z_inter/OBLdepth at interfaces (cvmix_kpp.F90:1224), [-]"
    },
    "w_s": {
      "type": "unknown",
      "shape": [
        "iface"
      ],
      "units": "m s^-1",
      "default": 0.0,
      "description": "Scalar turbulent velocity scale at the interfaces (turbulent_scales_1d_OBL with the scalar surface flux), [m s-1]"
    },
    "w_m": {
      "type": "unknown",
      "shape": [
        "iface"
      ],
      "units": "m s^-1",
      "default": 0.0,
      "description": "Momentum turbulent velocity scale at the interfaces, [m s-1]"
    },
    "G": {
      "type": "unknown",
      "shape": [
        "iface"
      ],
      "units": "dimensionless",
      "default": 0.0,
      "description": "The no-match shape function G(sigma) = sigma*(1-sigma)^2 (evaluate_cubic order), [-]"
    },
    "Kd_heat": {
      "type": "unknown",
      "shape": [
        "iface"
      ],
      "units": "m^2 s^-1",
      "default": 0.0,
      "description": "The KPP heat diffusivity on interfaces 2..kwup, zero elsewhere (OBL_Tdiff), [m2 s-1]"
    },
    "Kd_salt": {
      "type": "unknown",
      "shape": [
        "iface"
      ],
      "units": "m^2 s^-1",
      "default": 0.0,
      "description": "The KPP salt diffusivity (OBL_Sdiff), [m2 s-1]"
    },
    "Kv": {
      "type": "unknown",
      "shape": [
        "iface"
      ],
      "units": "m^2 s^-1",
      "default": 0.0,
      "description": "The KPP viscosity (OBL_Mdiff), [m2 s-1]"
    },
    "nonlocal_coeff": {
      "type": "unknown",
      "units": "dimensionless",
      "default": 0.0,
      "description": "Cstar*kappa*(kappa*eps*c_s)^(1/3) = 6.327399015078757 (cvmix_kpp.F90:576-584), [-]"
    },
    "Kt_out": {
      "type": "unknown",
      "shape": [
        "iface"
      ],
      "units": "m^2 s^-1",
      "default": 0.0,
      "description": "Heat diffusivity after KPP: the KPP value where nonzero, else the incoming value (F90:1023-1038), [m2 s-1]"
    },
    "Ks_out": {
      "type": "unknown",
      "shape": [
        "iface"
      ],
      "units": "m^2 s^-1",
      "default": 0.0,
      "description": "Salt diffusivity after KPP, [m2 s-1]"
    },
    "Kv_out": {
      "type": "unknown",
      "shape": [
        "iface"
      ],
      "units": "m^2 s^-1",
      "default": 0.0,
      "description": "Viscosity after KPP, [m2 s-1]"
    },
    "NLT_heat": {
      "type": "unknown",
      "shape": [
        "iface"
      ],
      "units": "dimensionless",
      "default": 0.0,
      "description": "The CVMix non-local heat transport nonlocal_coeff*G(sigma) on interfaces 2..kwup when surfBuoyFlux < 0 (all traced columns are stable: pinned at zero; NLT_SHAPE=CVMix, so MOM6's override block at MOM_CVMix_KPP.F90:960-1001 is inactive), [-]"
    },
    "NLT_salt": {
      "type": "unknown",
      "shape": [
        "iface"
      ],
      "units": "dimensionless",
      "default": 0.0,
      "description": "The CVMix non-local salt transport, equal to the heat term (nonLocalTrans(:,2) = nonLocalTrans(:,1), MOM_CVMix_KPP.F90:1002-1003), [-]"
    }
  },
  "equations": [
    {
      "lhs": "kwup",
      "rhs": {
        "op": "floor",
        "args": [
          "kOBL_s"
        ]
      }
    },
    {
      "lhs": "sigma",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "iface"
          }
        },
        "expr": {
          "op": "/",
          "args": [
            {
              "op": "-",
              "args": [
                {
                  "op": "index",
                  "args": [
                    "z_inter_s",
                    "i"
                  ]
                }
              ]
            },
            "OBLdepth_s"
          ]
        },
        "args": [
          "z_inter_s"
        ]
      }
    },
    {
      "lhs": "w_s",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "iface"
          }
        },
        "expr": {
          "op": "apply_expression_template",
          "args": [],
          "name": "kpp_ws",
          "bindings": {
            "sigma": {
              "op": "index",
              "args": [
                "sigma",
                "i"
              ]
            },
            "OBL": "OBLdepth_s",
            "B0": "surfBuoyFlux_s",
            "uStar": "uStar_s",
            "eps": "SURF_LAYER_EXT",
            "kappa": "VON_KARMAN",
            "zs": "ZETA_S",
            "as": "A_S",
            "cs": "C_S"
          }
        },
        "args": [
          "sigma"
        ]
      }
    },
    {
      "lhs": "w_m",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "iface"
          }
        },
        "expr": {
          "op": "apply_expression_template",
          "args": [],
          "name": "kpp_wm",
          "bindings": {
            "sigma": {
              "op": "index",
              "args": [
                "sigma",
                "i"
              ]
            },
            "OBL": "OBLdepth_s",
            "B0": "surfBuoyFlux_s",
            "uStar": "uStar_s",
            "eps": "SURF_LAYER_EXT",
            "kappa": "VON_KARMAN",
            "zm": "ZETA_M",
            "am": "A_M",
            "cm": "C_M"
          }
        },
        "args": [
          "sigma"
        ]
      }
    },
    {
      "lhs": "G",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "iface"
          }
        },
        "expr": {
          "op": "apply_expression_template",
          "args": [],
          "name": "kpp_shape_cubic",
          "bindings": {
            "sigma": {
              "op": "index",
              "args": [
                "sigma",
                "i"
              ]
            },
            "G1": 0.0,
            "dG1": 0.0
          }
        },
        "args": [
          "sigma"
        ]
      }
    },
    {
      "lhs": "nonlocal_coeff",
      "rhs": {
        "op": "*",
        "args": [
          "CSTAR",
          {
            "op": "*",
            "args": [
              "VON_KARMAN",
              {
                "op": "^",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      "VON_KARMAN",
                      {
                        "op": "*",
                        "args": [
                          "SURF_LAYER_EXT",
                          "C_S"
                        ]
                      }
                    ]
                  },
                  {
                    "op": "/",
                    "args": [
                      1.0,
                      3.0
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "Kd_heat",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "iface"
          }
        },
        "expr": {
          "op": "ifelse",
          "args": [
            {
              "op": "and",
              "args": [
                {
                  "op": ">=",
                  "args": [
                    "i",
                    2
                  ]
                },
                {
                  "op": "<=",
                  "args": [
                    "i",
                    "kwup"
                  ]
                }
              ]
            },
            {
              "op": "*",
              "args": [
                "OBLdepth_s",
                {
                  "op": "*",
                  "args": [
                    {
                      "op": "index",
                      "args": [
                        "w_s",
                        "i"
                      ]
                    },
                    {
                      "op": "index",
                      "args": [
                        "G",
                        "i"
                      ]
                    }
                  ]
                }
              ]
            },
            {
              "op": "const",
              "args": [],
              "value": 0.0,
              "units": "m^2 s^-1"
            }
          ]
        },
        "args": [
          "w_s",
          "G"
        ]
      }
    },
    {
      "lhs": "Kd_salt",
      "rhs": "Kd_heat"
    },
    {
      "lhs": "Kv",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "iface"
          }
        },
        "expr": {
          "op": "ifelse",
          "args": [
            {
              "op": "and",
              "args": [
                {
                  "op": ">=",
                  "args": [
                    "i",
                    2
                  ]
                },
                {
                  "op": "<=",
                  "args": [
                    "i",
                    "kwup"
                  ]
                }
              ]
            },
            {
              "op": "*",
              "args": [
                "OBLdepth_s",
                {
                  "op": "*",
                  "args": [
                    {
                      "op": "index",
                      "args": [
                        "w_m",
                        "i"
                      ]
                    },
                    {
                      "op": "index",
                      "args": [
                        "G",
                        "i"
                      ]
                    }
                  ]
                }
              ]
            },
            {
              "op": "const",
              "args": [],
              "value": 0.0,
              "units": "m^2 s^-1"
            }
          ]
        },
        "args": [
          "w_m",
          "G"
        ]
      }
    },
    {
      "lhs": "NLT_heat",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "iface"
          }
        },
        "expr": {
          "op": "ifelse",
          "args": [
            {
              "op": "and",
              "args": [
                {
                  "op": "<=",
                  "args": [
                    "surfBuoyFlux_s",
                    {
                      "op": "const",
                      "args": [],
                      "value": 0.0,
                      "units": "m^2 s^-3"
                    }
                  ]
                },
                {
                  "op": "and",
                  "args": [
                    {
                      "op": ">=",
                      "args": [
                        "i",
                        2
                      ]
                    },
                    {
                      "op": "<=",
                      "args": [
                        "i",
                        "kwup"
                      ]
                    }
                  ]
                }
              ]
            },
            {
              "op": "*",
              "args": [
                "nonlocal_coeff",
                {
                  "op": "index",
                  "args": [
                    "G",
                    "i"
                  ]
                }
              ]
            },
            {
              "op": "const",
              "args": [],
              "value": 0.0,
              "units": "dimensionless"
            }
          ]
        },
        "args": [
          "G"
        ]
      }
    },
    {
      "lhs": "Kt_out",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "iface"
          }
        },
        "expr": {
          "op": "apply_expression_template",
          "args": [],
          "name": "kpp_override_nonzero",
          "bindings": {
            "K_kpp": {
              "op": "index",
              "args": [
                "Kd_heat",
                "i"
              ]
            },
            "K_in": {
              "op": "index",
              "args": [
                "Kt_in",
                "i"
              ]
            }
          }
        },
        "args": [
          "Kd_heat",
          "Kt_in"
        ]
      }
    },
    {
      "lhs": "Ks_out",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "iface"
          }
        },
        "expr": {
          "op": "apply_expression_template",
          "args": [],
          "name": "kpp_override_nonzero",
          "bindings": {
            "K_kpp": {
              "op": "index",
              "args": [
                "Kd_salt",
                "i"
              ]
            },
            "K_in": {
              "op": "index",
              "args": [
                "Ks_in",
                "i"
              ]
            }
          }
        },
        "args": [
          "Kd_salt",
          "Ks_in"
        ]
      }
    },
    {
      "lhs": "Kv_out",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "iface"
          }
        },
        "expr": {
          "op": "apply_expression_template",
          "args": [],
          "name": "kpp_override_nonzero",
          "bindings": {
            "K_kpp": {
              "op": "index",
              "args": [
                "Kv",
                "i"
              ]
            },
            "K_in": {
              "op": "index",
              "args": [
                "Kv_in",
                "i"
              ]
            }
          }
        },
        "args": [
          "Kv",
          "Kv_in"
        ]
      }
    },
    {
      "lhs": "NLT_salt",
      "rhs": "NLT_heat"
    }
  ],
  "tests": [
    {
      "id": "cell782_step3600_kOBL325",
      "description": "mom6_kpp.csv row (i, j, tod) = (7, 82, 3600): smoothed OBLdepth = 6.1872106097070425 m, kOBL = 3.25 (ktup = nint(kOBL)-1 = 2 = kwup-1: the kw loop computes interfaces 2..3, no restoration). Pins Kd_heat and Kv at interfaces 2..kwup = 2..3 (the KPP-active region; Kv pins the w_m momentum branch, numerically equal to Kd_heat in this stable column) and one pass-through pin Kv_out at the first restoration interface kwup+1 = 4 (Kv_out = Kv_in, the kpp_override_nonzero else-branch), at rel 1e-12.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "OBLdepth_s": 6.1872106097070425,
        "kOBL_s": 3.25,
        "uStar_s": 0.00312023723466675,
        "surfBuoyFlux_s": 5.051434844118651e-09,
        "z_inter_s": [
          0.0,
          -2.505951254018008,
          -5.007844232182665,
          -7.509571486709462,
          -10.011140868126144,
          -13.012867385263757,
          -16.014426744296664,
          -20.016233864336883,
          -25.018120866772726,
          -30.01961304442029,
          -35.02074145348367,
          -40.021580761558695,
          -45.02220917941755,
          -50.022697808247905,
          -55.023099657572764,
          -60.023496524654384,
          -65.02396447708895,
          -70.02453667723405,
          -75.02527182809051,
          -80.02628076985721,
          -85.02778398074857,
          -90.03014932623928,
          -95.03393942449411,
          -100.04001045817427,
          -105.0496402263123,
          -110.06471430238129,
          -115.0878748970654,
          -120.1228003045011,
          -125.17453221509601,
          -130.24990010651914,
          -135.35800374296502,
          -140.5108011614997,
          -145.72380844728917,
          -151.0169384593951,
          -156.41548389543,
          -161.951186257771,
          -167.6640935356069,
          -173.60311638643464,
          -179.82887029070238,
          -186.41524969688493,
          -193.45188146283354,
          -201.04683073575148,
          -209.3296325730296,
          -218.45516348267034,
          -228.6069037330521,
          -240.0012385311366,
          -252.89273096864673,
          -267.5801943658347,
          -284.4131017553315,
          -303.79441943761805,
          -326.19113940187503,
          -352.14736167279847,
          -382.28260595968806,
          -417.30797525485764,
          -458.03705571096924,
          -505.3959341333475,
          -555.0276268683139,
          -555.029140695571,
          -555.0301407041239,
          -555.0311406662098,
          -555.0321406261787,
          -555.0331405865783,
          -555.0341405470646,
          -555.0351405076314,
          -555.0361404682731,
          -555.0371404289849,
          -555.0381403897641,
          -555.039140350612,
          -555.0401403115399,
          -555.0411402725807,
          -555.0421402338175,
          -555.043140195446,
          -555.0441401579188,
          -555.0451401222674,
          -555.046140090821,
          -555.0471400687849
        ],
        "Kt_in": [
          0.0025,
          0.002721836876278671,
          0.0003398625744625902,
          1.857838163433473e-05,
          1.7360478390697586e-05,
          1.7505337709233038e-05,
          1.792833662550946e-05,
          1.7635796320659048e-05,
          1.7680830040176887e-05,
          1.8116736000660893e-05,
          1.8752785005349037e-05,
          2.1519731158762565e-05,
          2.1509374517162607e-05,
          2.2320747640994768e-05,
          1.939529709855298e-05,
          1.9377084085639223e-05,
          3.880354661675348e-05,
          2.990095024280806e-05,
          2.2461296622243756e-05,
          2.5084891508815605e-05,
          3.081643048291811e-05,
          3.351945424814085e-05,
          5.738156759960706e-05,
          1.7310110208442285e-05,
          0.0006233019003005899,
          3.788391634598068e-05,
          2.6236397244887122e-05,
          2.86682217778737e-05,
          3.31851612089607e-05,
          4.4509580919559e-05,
          3.964501280180045e-05,
          5.4642492644260296e-05,
          0.00013791773057460986,
          0.00011589758289739704,
          0.00010073803747919772,
          0.0002516121732462597,
          9.36638941838649e-05,
          8.85210049417561e-05,
          8.705134083877552e-05,
          6.542161187709182e-05,
          7.412710330186976e-05,
          0.00011129972094269331,
          0.0002474861247112089,
          0.0005082217397658594,
          0.0005410734568146919,
          0.0029375945027996174,
          0.000986719506358274,
          1.7276598896187788e-05,
          1.7335400094469503e-05,
          0.00013125717755870222,
          0.00019802226120328462,
          0.00041458376866069504,
          0.00022967936648102342,
          0.00021269693634595274,
          0.00035997306887592897,
          0.0006396456373816936,
          3.822717290835148e-05,
          4.052730320887429e-05,
          4.557171233303339e-05,
          6.141853054200718e-05,
          2.1263528727468247e-05,
          2.157438148833046e-05,
          2.1932600834962637e-05,
          2.235002578227098e-05,
          2.2842800607429218e-05,
          2.3433527521443913e-05,
          2.4154854363796886e-05,
          2.5055753146421876e-05,
          2.621318009620815e-05,
          2.775539579441163e-05,
          2.991326930393077e-05,
          3.31485386025548e-05,
          3.853859071500859e-05,
          6.0089489506441004e-05,
          6.0089607811646595e-05,
          0.0
        ],
        "Ks_in": [
          0.0025,
          0.0027487634139227155,
          0.0003398625744625902,
          1.721826231278331e-05,
          1.7360478390697586e-05,
          1.7505337709233038e-05,
          1.792833662550946e-05,
          1.7635796320659048e-05,
          1.7680830040176887e-05,
          1.8116736000660893e-05,
          1.8752785005349037e-05,
          2.1519731158762565e-05,
          2.1509374517162607e-05,
          2.2320747640994768e-05,
          1.939529709855298e-05,
          1.9377084085639223e-05,
          3.880354661675348e-05,
          2.990095024280806e-05,
          2.2461296622243756e-05,
          2.5084891508815605e-05,
          3.081643048291811e-05,
          3.351945424814085e-05,
          5.60232123808245e-05,
          1.7310110208442285e-05,
          0.0006219477662418,
          3.652079934754307e-05,
          2.4872923200898634e-05,
          2.86682217778737e-05,
          3.31851612089607e-05,
          4.3146082013739885e-05,
          3.964501280180045e-05,
          5.4642492644260296e-05,
          0.00013655433732196872,
          0.00011453409348116199,
          9.937457954199687e-05,
          0.0002250204677213541,
          9.231082252495806e-05,
          8.715750595319372e-05,
          8.705134083877552e-05,
          6.542161187709182e-05,
          7.412710330186976e-05,
          0.00011129972094269331,
          0.0002474861247112089,
          0.0005082217397658594,
          0.0005410734568146919,
          0.002958995025302821,
          0.000986719506358274,
          1.7276598896187788e-05,
          1.7335400094469503e-05,
          0.00012989399089076897,
          0.00019666371497711462,
          0.0004060065814332485,
          0.00022832332345933798,
          0.0002113065145480539,
          0.00035997306887592897,
          0.0006396456373816936,
          3.0110582095805928e-05,
          2.2065054468296467e-05,
          2.4429574554628585e-05,
          3.440115818778687e-05,
          2.1263528727468247e-05,
          2.157438148833046e-05,
          2.1932600834962637e-05,
          2.235002578227098e-05,
          2.2842800607429218e-05,
          2.3433527521443913e-05,
          2.4154854363796886e-05,
          2.5055753146421876e-05,
          2.621318009620815e-05,
          2.775539579441163e-05,
          2.991326930393077e-05,
          3.31485386025548e-05,
          3.853859071500859e-05,
          6.0089489506441004e-05,
          6.0089607811646595e-05,
          0.0
        ],
        "Kv_in": [
          0.002671,
          0.0028129663727710207,
          0.0004937920866790544,
          0.00017121484016164538,
          0.00017136041333529932,
          0.00017150526566451517,
          0.00017192821848364395,
          0.00017163573794686738,
          0.00017168078784573056,
          0.00017211668509236453,
          0.00017275272551027347,
          0.00017551961304046687,
          0.00017550928111762242,
          0.0001763206582456426,
          0.00017339526229974788,
          0.00017337705123254713,
          0.00019280325014584354,
          0.00018390077898481602,
          0.00017646122731255294,
          0.00017908479252901736,
          0.00018481626371253957,
          0.00018751925823266833,
          0.0002100176194342515,
          0.000171,
          0.0007759268064638658,
          0.00019052021703847374,
          0.00017887282456109684,
          0.00018266813032983062,
          0.00018718505817683878,
          0.000197145949812533,
          0.00019364492416488316,
          0.00020864237648024952,
          0.0002905539347505512,
          0.0002685338873366081,
          0.0002533744035471519,
          0.0003667766678102544,
          0.00024629711583687463,
          0.00024115745253446106,
          0.00024105130007527061,
          0.0002194215865716013,
          0.0002281270678877557,
          0.0002652996321702831,
          0.0004014857691966603,
          0.0006622205334782455,
          0.000695071561615089,
          0.0030416462304197396,
          0.0011407137819232401,
          0.000171,
          0.000171,
          0.0002838926179737853,
          0.0003506577672412396,
          0.0005594884004202307,
          0.0003823074678147825,
          0.0003652853271727235,
          0.0005139730335728409,
          0.0007936456345962831,
          0.000183632333020285,
          0.0001745364977222552,
          0.00017475052683008132,
          0.00017499116351356726,
          0.0001752635287274638,
          0.00017557438148832626,
          0.0001759326008349587,
          0.0001763500257822673,
          0.0001768428006074258,
          0.00017743352752144082,
          0.00017815485436379412,
          0.00017905575314641946,
          0.00018021318009620607,
          0.00018175539579440994,
          0.00018391326930392948,
          0.00018714853860255388,
          0.00019253859071500804,
          0.0002140894895064407,
          0.0002140895756855059,
          0.000171
        ]
      },
      "tolerance": {
        "rel": 1e-12
      },
      "assertions": [
        {
          "variable": "Kd_heat",
          "time": 0.0,
          "expected": 0.000918247342468442,
          "coords": {
            "iface": 2
          }
        },
        {
          "variable": "Kv",
          "time": 0.0,
          "expected": 0.000918247342468442,
          "coords": {
            "iface": 2
          }
        },
        {
          "variable": "Kd_heat",
          "time": 0.0,
          "expected": 0.00018833998264060838,
          "coords": {
            "iface": 3
          }
        },
        {
          "variable": "Kv",
          "time": 0.0,
          "expected": 0.00018833998264060838,
          "coords": {
            "iface": 3
          }
        },
        {
          "variable": "Kv_out",
          "time": 0.0,
          "expected": 0.00017121484016164538,
          "coords": {
            "iface": 4
          }
        }
      ]
    },
    {
      "id": "cell882_step3600_kOBL375",
      "description": "mom6_kpp.csv row (i, j, tod) = (8, 82, 3600): smoothed OBLdepth = 6.309964392417778 m, kOBL = 3.75 (ktup = nint(kOBL)-1 = 3 = kwup: interface 4 is restored to the incoming value). Pins Kd_heat and Kv at interfaces 2..kwup = 2..3 (the KPP-active region; Kv pins the w_m momentum branch, numerically equal to Kd_heat in this stable column) and one pass-through pin Kv_out at the first restoration interface kwup+1 = 4 (Kv_out = Kv_in, the kpp_override_nonzero else-branch), at rel 1e-12.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "OBLdepth_s": 6.309964392417778,
        "kOBL_s": 3.75,
        "uStar_s": 0.003961113528183046,
        "surfBuoyFlux_s": 9.467561478743733e-09,
        "z_inter_s": [
          0.0,
          -2.49310163037841,
          -4.991225880004249,
          -7.489505530859266,
          -9.987909979620143,
          -12.986119640718492,
          -15.984468124889936,
          -19.98250027648157,
          -24.980346364212327,
          -29.978487773795216,
          -34.976918743449254,
          -39.97560341713998,
          -44.97449885948381,
          -49.97356346781151,
          -54.97276514459516,
          -59.97203655177731,
          -64.97133146364585,
          -69.97069171411833,
          -74.97019118122725,
          -79.9699568971618,
          -84.97020134601703,
          -89.97127688031166,
          -94.97375633123048,
          -99.97854419681421,
          -104.98686769734823,
          -110.00062199856563,
          -115.02250030935659,
          -120.05620993335195,
          -125.10685489277836,
          -130.18129607528147,
          -135.28864224698654,
          -140.44083908274587,
          -145.6533835923243,
          -150.9461653578588,
          -156.34446576455866,
          -161.880219727713,
          -167.59286398388176,
          -173.53195009172632,
          -179.75791188528692,
          -186.34466717705206,
          -193.3819235950065,
          -200.97788756045614,
          -209.26237260114223,
          -218.38985071658664,
          -228.54398752398802,
          -239.94206529456818,
          -252.83944916910391,
          -267.5344170748938,
          -284.3738003285332,
          -303.7634002315543,
          -326.17270485186214,
          -330.7198294171211,
          -330.72437993277606,
          -330.7287802969353,
          -330.7322857767858,
          -330.73469642024503,
          -330.73588544709907,
          -330.7368854936398,
          -330.73788554854633,
          -330.73888560312537,
          -330.739885657316,
          -330.7408857111447,
          -330.74188576463774,
          -330.74288581782105,
          -330.74388587072,
          -330.74488592335905,
          -330.7458859757601,
          -330.74688602794015,
          -330.74788607990473,
          -330.74888613163336,
          -330.7498861830455,
          -330.75088623392213,
          -330.7518862837239,
          -330.7528863311685,
          -330.7538863732501,
          -330.7548864029628
        ],
        "Kt_in": [
          0.0025,
          0.0025227251732353904,
          2.0036715211925057e-05,
          1.7089289753087235e-05,
          1.7145998898496764e-05,
          1.7266899196074866e-05,
          1.7356142552429928e-05,
          1.726039052256498e-05,
          1.7302643583436975e-05,
          1.7425983116020924e-05,
          1.7568734208965606e-05,
          1.806889666486146e-05,
          1.8220065250539352e-05,
          1.8439135778094125e-05,
          1.7703154258956072e-05,
          1.7799523190768473e-05,
          2.751722064522938e-05,
          3.292233929291327e-05,
          1.989585183037992e-05,
          1.963025022784304e-05,
          2.1931699495036242e-05,
          2.9570140536220786e-05,
          6.038068335311306e-05,
          1.7287522492841608e-05,
          0.005112427395659121,
          9.170910817430927e-05,
          3.397292252805613e-05,
          3.0394068973913102e-05,
          3.0266919975546783e-05,
          2.9090417470008647e-05,
          2.348397032818334e-05,
          2.451682869373701e-05,
          2.951449551042915e-05,
          3.2759279710810045e-05,
          3.826718011450976e-05,
          1.702991108865438e-05,
          6.570155797179328e-05,
          6.159316840650137e-05,
          6.997816353400422e-05,
          5.517269190462204e-05,
          8.535443134633559e-05,
          0.00011453028746391688,
          0.00020074946343804186,
          0.00015728882085436623,
          6.161714125056499e-05,
          5.808909372496008e-05,
          0.00013602333758074952,
          0.00030879849050657367,
          0.0005446004316829369,
          5.786271915392415e-05,
          6.250262066261212e-05,
          1.9604222699949584e-05,
          1.861919239797489e-05,
          2.0119396508452975e-05,
          2.149900988374544e-05,
          2.5385371522242514e-05,
          3.1403493201054586e-05,
          1.706867229530832e-05,
          3.8927074772221016e-05,
          1.7077548151960047e-05,
          1.7082860424282184e-05,
          1.7088922041887235e-05,
          1.7095905872475656e-05,
          1.7104042410636114e-05,
          1.711364597203542e-05,
          1.7125156604141028e-05,
          1.713920993758891e-05,
          1.7156759426195906e-05,
          1.7179303364512167e-05,
          1.7209338923837326e-05,
          0.0019141396354517021,
          0.0025290945762531957,
          0.0025144928469926177,
          0.002517655936411309,
          0.0025178274756368006,
          0.0
        ],
        "Ks_in": [
          0.0025,
          0.0025227251732353904,
          2.0036715211925057e-05,
          1.7089289753087235e-05,
          1.7145998898496764e-05,
          1.7266899196074866e-05,
          1.7356142552429928e-05,
          1.726039052256498e-05,
          1.7302643583436975e-05,
          1.7425983116020924e-05,
          1.7568734208965606e-05,
          1.806889666486146e-05,
          1.8220065250539352e-05,
          1.8439135778094125e-05,
          1.7703154258956072e-05,
          1.7799523190768473e-05,
          2.751722064522938e-05,
          3.156507414108543e-05,
          1.989585183037992e-05,
          1.963025022784304e-05,
          2.1931699495036242e-05,
          2.9570140536220786e-05,
          6.038068335311306e-05,
          1.7287522492841608e-05,
          0.005089657618327649,
          8.604449225705104e-05,
          3.25953072572457e-05,
          3.0394068973913102e-05,
          2.8903424670087257e-05,
          2.7726923459470434e-05,
          2.348397032818334e-05,
          2.451682869373701e-05,
          2.951449551042915e-05,
          3.2759279710810045e-05,
          3.826718011450976e-05,
          1.702991108865438e-05,
          6.380438308806366e-05,
          6.159316840650137e-05,
          6.997816353400422e-05,
          5.517269190462204e-05,
          8.535443134633559e-05,
          0.00011316680557501587,
          0.00019443719441151943,
          0.0001450151325360581,
          6.0183565091705074e-05,
          5.6735174152407005e-05,
          0.00013602333758074952,
          0.00030879849050657367,
          0.0005303322066758129,
          5.650201515007662e-05,
          6.250262066261212e-05,
          1.7387998745167428e-05,
          1.7184235433068796e-05,
          1.720122541808478e-05,
          1.7259091783964078e-05,
          1.7520026348953738e-05,
          1.8024454373714288e-05,
          1.706867229530832e-05,
          1.9376120734757948e-05,
          1.7077548151960047e-05,
          1.7082860424282184e-05,
          1.7088922041887235e-05,
          1.7095905872475656e-05,
          1.7104042410636114e-05,
          1.711364597203542e-05,
          1.7125156604141028e-05,
          1.713920993758891e-05,
          1.7156759426195906e-05,
          1.7179303364512167e-05,
          1.7209338923837326e-05,
          0.001915961970265107,
          0.002554093139308113,
          0.0025144928469926177,
          0.002517655936411309,
          0.0025178274756368006,
          0.0
        ],
        "Kv_in": [
          0.002671,
          0.002671,
          0.00017403524202679456,
          0.00017108925147423028,
          0.000171145940433404,
          0.00017126681490593028,
          0.00017135604251589443,
          0.00017126033814748997,
          0.00017130260314159314,
          0.00017142594230099326,
          0.00017156869496253384,
          0.00017206884182509866,
          0.00017222001715409317,
          0.00017243909084271148,
          0.0001717031353608733,
          0.00017179950239058097,
          0.00018151694585888744,
          0.0001855584621250386,
          0.00017389577971917193,
          0.0001736301866340306,
          0.00017593158064597143,
          0.00018356983938311753,
          0.00021437966755862887,
          0.000171,
          0.005171,
          0.00023975576781692573,
          0.00018657542079806842,
          0.00018439385059013504,
          0.00018290326487405836,
          0.00018172681014222764,
          0.00017748392135789073,
          0.0001785167856339552,
          0.0001835144401685925,
          0.00018675922512744402,
          0.00019226712210997882,
          0.000171,
          0.0002177533516505869,
          0.00021559311790789816,
          0.00022397811731628635,
          0.00020917266033476816,
          0.0002393543560834794,
          0.0002671666094989796,
          0.00034810134392254297,
          0.0002981630763470716,
          0.00021415843187454103,
          0.00021072505172266758,
          0.00029002178294398163,
          0.00046279391621901274,
          0.0006832737763515512,
          0.00021049839743374966,
          0.0002164994060663246,
          0.00017132000325049813,
          0.00017112597870709624,
          0.0001710811155018013,
          0.00017106663696795046,
          0.00017106244478869032,
          0.00017106492364001288,
          0.00017106867229530783,
          0.0001710728530349034,
          0.00017107754815195953,
          0.00017108286042428168,
          0.00017108892204188676,
          0.0001710959058724752,
          0.00017110404241063565,
          0.00017111364597203498,
          0.00017112515660414062,
          0.00017113920993758856,
          0.0001711567594261956,
          0.00017117930336451188,
          0.0001712093389238371,
          0.0020638875208870903,
          0.002624764595791722,
          0.0026684928469926177,
          0.002671655936411309,
          0.0026718274730987888,
          0.0026709885640536966
        ]
      },
      "tolerance": {
        "rel": 1e-12
      },
      "assertions": [
        {
          "variable": "Kd_heat",
          "time": 0.0,
          "expected": 0.0012123079218295501,
          "coords": {
            "iface": 2
          }
        },
        {
          "variable": "Kv",
          "time": 0.0,
          "expected": 0.0012123079218295501,
          "coords": {
            "iface": 2
          }
        },
        {
          "variable": "Kd_heat",
          "time": 0.0,
          "expected": 0.00028972400103798013,
          "coords": {
            "iface": 3
          }
        },
        {
          "variable": "Kv",
          "time": 0.0,
          "expected": 0.00028972400103798013,
          "coords": {
            "iface": 3
          }
        },
        {
          "variable": "Kv_out",
          "time": 0.0,
          "expected": 0.00017108925147423028,
          "coords": {
            "iface": 4
          }
        }
      ]
    },
    {
      "id": "cell684_step10800_kOBL275",
      "description": "mom6_kpp.csv row (i, j, tod) = (6, 84, 10800): smoothed OBLdepth = 5.001656526745087 m, kOBL = 2.75 (kwup = 2: the KPP coefficients are nonzero only on interface 2). Pins Kd_heat and Kv at interface 2 (the KPP-active region; Kv pins the w_m momentum branch, numerically equal to Kd_heat in this stable column) and one pass-through pin Kv_out at the first restoration interface kwup+1 = 3 (Kv_out = Kv_in, the kpp_override_nonzero else-branch), at rel 1e-12.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "OBLdepth_s": 5.001656526745087,
        "kOBL_s": 2.75,
        "uStar_s": 0.0020634389900162525,
        "surfBuoyFlux_s": 2.838077120606359e-08,
        "z_inter_s": [
          0.0,
          -2.5041168640077416,
          -5.007492257423143,
          -7.510344496641718,
          -10.013223793880123,
          -13.016597338152812,
          -16.019836783575833,
          -20.023914024067018,
          -25.02858188202471,
          -30.03271674012516,
          -35.036323729954745,
          -40.039477357455,
          -45.04222600160183,
          -50.044586639207566,
          -55.046570006201236,
          -60.04827205724097,
          -65.04984539888224,
          -70.05134480218577,
          -75.05281564093154,
          -80.05438219926764,
          -85.05629984128487,
          -90.05895337391499,
          -95.06292160303362,
          -100.06906196222174,
          -105.07867192066054,
          -110.09360996606613,
          -115.11652323131679,
          -120.15110315327482,
          -125.20240398269202,
          -130.27725922151868,
          -135.38476741180583,
          -140.53688463283996,
          -145.74913210631132,
          -151.04142127054604,
          -156.4390383094349,
          -161.97381509761496,
          -167.68547588117286,
          -173.62322261920718,
          -179.847544807403,
          -186.43230333122983,
          -193.4670989871858,
          -201.0599808669453,
          -209.3405049399085,
          -218.46316282661624,
          -228.61134391085113,
          -240.00156835369094,
          -252.888142098045,
          -267.57015360481967,
          -284.39568878849,
          -303.76724911585256,
          -326.15227662652364,
          -352.09030322565746,
          -382.2009956593474,
          -417.1938109938508,
          -457.8801721724934,
          -505.18267448866027,
          -560.15000101285,
          -623.9683289679033,
          -697.9750253810764,
          -715.7938959770581,
          -715.7948959431153,
          -715.7958959093544,
          -715.7968958755984,
          -715.7978958419658,
          -715.7988958084585,
          -715.799895775079,
          -715.8008957417132,
          -715.8018957083654,
          -715.8028956750411,
          -715.8038956418543,
          -715.8048956087854,
          -715.8058955757676,
          -715.8068955427827,
          -715.8078955095672,
          -715.8088954725572,
          -715.8098954430486
        ],
        "Kt_in": [
          0.0025,
          0.0010765510198860575,
          2.1472515897521995e-05,
          1.7141491204374394e-05,
          1.7200936139797708e-05,
          1.73073334515345e-05,
          1.749445528762281e-05,
          1.742868986611344e-05,
          1.743349489446823e-05,
          1.7643949360437452e-05,
          1.8060724015282057e-05,
          1.890191806611367e-05,
          1.902769459294655e-05,
          2.0064115540024505e-05,
          1.9338640452941393e-05,
          1.9335310903898608e-05,
          2.9574040790625413e-05,
          2.7128371653518292e-05,
          2.2531845976741176e-05,
          2.42640593272207e-05,
          2.787051079599439e-05,
          2.8724718805315442e-05,
          3.405142440857557e-05,
          0.0001469361853351942,
          9.812120471603148e-05,
          3.112219633514566e-05,
          2.350369616977226e-05,
          2.614190071640832e-05,
          2.915613628465587e-05,
          3.48622920562101e-05,
          3.860930277868919e-05,
          6.17222255264867e-05,
          0.0001060668345840937,
          8.593118102724678e-05,
          7.421705351067312e-05,
          8.17629111719072e-05,
          6.993273407251928e-05,
          7.357084160849085e-05,
          7.893492837296097e-05,
          6.226893240534211e-05,
          6.649198474517781e-05,
          8.395201853961063e-05,
          9.660589988457579e-05,
          0.00024979018302941303,
          0.0003398784324564862,
          0.0004609240869360228,
          0.005084019926882657,
          0.0050840157661994935,
          0.0011601494070891999,
          0.00013830571763045593,
          0.00011357441728740719,
          0.00013277103459294017,
          0.00017013771900881166,
          0.000381258581535038,
          0.0010927416315086563,
          0.0007086154756599824,
          0.00042195976188019876,
          0.00033345819695023907,
          0.00012380477515722504,
          3.88910100855474e-05,
          4.6498505688657155e-05,
          6.193354419027713e-05,
          4.692890566621143e-05,
          5.6465887298447196e-05,
          0.00012162410493315632,
          4.9334863878905936e-05,
          5.091622357426776e-05,
          5.313047835458436e-05,
          6.647238037033459e-05,
          6.073071422772047e-05,
          6.738144284320502e-05,
          7.783357874516724e-05,
          9.797390420489557e-05,
          0.0001786338036106701,
          0.0001700034022355891,
          0.0
        ],
        "Ks_in": [
          0.0025,
          0.0010765510198860575,
          2.1472515897521995e-05,
          1.7141491204374394e-05,
          1.7200936139797708e-05,
          1.73073334515345e-05,
          1.749445528762281e-05,
          1.742868986611344e-05,
          1.743349489446823e-05,
          1.7643949360437452e-05,
          1.8060724015282057e-05,
          1.890191806611367e-05,
          1.902769459294655e-05,
          2.0064115540024505e-05,
          1.9338640452941393e-05,
          1.9335310903898608e-05,
          2.9574040790625413e-05,
          2.7128371653518292e-05,
          2.2531845976741176e-05,
          2.42640593272207e-05,
          2.787051079599439e-05,
          2.8724718805315442e-05,
          3.405142440857557e-05,
          0.0001469361853351942,
          9.812120471603148e-05,
          3.112219633514566e-05,
          2.350369616977226e-05,
          2.614190071640832e-05,
          2.915613628465587e-05,
          3.48622920562101e-05,
          3.860930277868919e-05,
          6.17222255264867e-05,
          0.0001060668345840937,
          8.593118102724678e-05,
          7.285440196473802e-05,
          7.920046955841018e-05,
          6.857627752183868e-05,
          7.22074577612204e-05,
          7.893492837296097e-05,
          6.226893240534211e-05,
          6.649198474517781e-05,
          8.395201853961063e-05,
          9.660589988457579e-05,
          0.00024979018302941303,
          0.0003398784324564862,
          0.0004616527872630438,
          0.005111968200569117,
          0.005111149418863505,
          0.0011601494070891999,
          0.00013830571763045593,
          0.00011221668345598763,
          0.0001310274930547544,
          0.0001687805108488009,
          0.0003787701630885563,
          0.0010927416315086563,
          0.0007086154756599824,
          0.000398827150366832,
          0.0003320034480654315,
          0.00012380477515722504,
          3.166304990756197e-05,
          4.6498505688657155e-05,
          4.767834158468714e-05,
          4.692890566621143e-05,
          4.794882433165769e-05,
          9.314806486176003e-05,
          4.9334863878905936e-05,
          5.091622357426776e-05,
          5.313047835458436e-05,
          5.685671736061572e-05,
          6.073071422772047e-05,
          6.738144284320502e-05,
          7.783357874516724e-05,
          9.59464922058236e-05,
          0.00018191979316612458,
          0.0001700034022355891,
          0.0
        ],
        "Kv_in": [
          0.002671,
          0.001230518557633713,
          0.00017546744610281016,
          0.00017114133372481016,
          0.00017120070260005416,
          0.00017130701305675985,
          0.00017149391687335702,
          0.0001714282795055701,
          0.00017143313851418344,
          0.0001716434444495823,
          0.00017205992921500443,
          0.0001729005582422842,
          0.0001730263189770306,
          0.0001740621498175815,
          0.0001733372135824418,
          0.0001733339381840939,
          0.0001835668833605271,
          0.0001811227890019575,
          0.0001765288881495715,
          0.0001782602755030033,
          0.00018186498212490547,
          0.00018271889097309308,
          0.0001880431501798292,
          0.00030087465715275313,
          0.0002520837789589712,
          0.00018511585800868284,
          0.00017750085367262736,
          0.00018013800366069966,
          0.0001831510776887062,
          0.0001888550334106303,
          0.00019260072565617574,
          0.00021570487027104278,
          0.00026003304606629147,
          0.00023990564898990904,
          0.00022683338190266473,
          0.00023309197948371988,
          0.00022255168160621025,
          0.00022618918872480896,
          0.00023291533360426402,
          0.0002162552200949034,
          0.00022047771454383467,
          0.00023793377943926353,
          0.00025058560054370493,
          0.00040373531160465723,
          0.0004938092892576875,
          0.0006131396047918459,
          0.005171,
          0.005171,
          0.0013140147359133822,
          0.0002922942346656005,
          0.00026620393136831603,
          0.00028497845029173843,
          0.0003227684309370267,
          0.0005326782280939657,
          0.0012467230716235315,
          0.0008626072422119267,
          0.0005468976936888392,
          0.00048597109324499677,
          0.0002778040175042189,
          0.0001848047935571768,
          0.0001860577861831126,
          0.0001871518562111624,
          0.00018841213045868742,
          0.0001898825207921792,
          0.00019162062209836751,
          0.00019370486158394088,
          0.00019624870733026345,
          0.00019942556235159477,
          0.00020350824838217323,
          0.00020895134148460126,
          0.00021656501325033456,
          0.00022798020660606323,
          0.00024699849127431236,
          0.0003230395801013126,
          0.00032303988418077683,
          0.000171
        ]
      },
      "tolerance": {
        "rel": 1e-12
      },
      "assertions": [
        {
          "variable": "Kd_heat",
          "time": 0.0,
          "expected": 0.00012179159960576173,
          "coords": {
            "iface": 2
          }
        },
        {
          "variable": "Kv",
          "time": 0.0,
          "expected": 0.00012179159960576173,
          "coords": {
            "iface": 2
          }
        },
        {
          "variable": "Kv_out",
          "time": 0.0,
          "expected": 0.00017546744610281016,
          "coords": {
            "iface": 3
          }
        }
      ]
    }
  ]
}
```

</details>
