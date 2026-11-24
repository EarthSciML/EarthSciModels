---
title: "BoundaryFluxes"
slug: "boundaryfluxes"
domains: ["ocean"]
component_types: ["model"]
subdomains: ["mom6"]
domain: "ocean"
subdomain: "mom6"
component_type: "model"
esm_version: "1.3.0"
esm_path: "components/ocean/mom6/mom6_bflux.esm"
reference: "https://github.com/ESCOMP/CESM"
description: "Stage-2 implementation of the MOM6 surface boundary fluxes applied in the diabatic column (applyBoundaryFluxesInOut, MOM_diabatic_aux.F90:702-1483 of the instrumented fork stage1/EqESM-cesm-mom6; run configuration C_JRA_t62_mom6_inst: AGGREGATE_FW_FORCING=True so netMassIn == 0 (the net mass change of the column is netMassOut alone), all unit rescale factors 1.0, dt = 3600 s). The component applies the net surface mass, heat and salt fluxes of a step to the surface layer (step A, F90:1039-1071 with netMassIn = 0, and step B, F90:1109-1146 with fractionOfForcing = 1 in the surface layer and the running remainders vanishing exactly -- every traced row has h_1 ~ 2.5 m well above minimum_forcing_depth, so all forcing is consumed by layer 1, verified on all 156 rows: h, T and S change only in layer 1, and only by the fluxes), with the heat content of the mass exchange added via dThickness*T*EnthalpyConst (F90:1141); the reference run has EnthalpyConst = 0 (F90:845-846) because the CESM coupler provides heat_content_evap. The penetrating shortwave is applied by absorbRemainingSW (step C, F90:1355-1362, MOM_opacity.F90:602-885): the component consumes the per-layer SW heating dT and the bottom leftover of the ShortwaveAbsorption component (mom6_shortwave.esm; here sourced from the mom6_sw_abs.csv dump columns dT_k and pen_sw_rem_n(75)). The column budgets are the plain per-layer sums dMass_col = sum_k (h_after_k - h_before_k) == netMassIn + netMassOut, dSalt_col = sum_k (h_after_k*S_after_k - h_before_k*S_before_k) == netSalt, and dHeat_col = sum_k (h_after_k*T_after_k - h_before_k*T_before_k) == netHeat + sum_n penSW_bnd(n) - leftover (netHeat already contains the non-penetrating SW and excludes the heat content of the outgoing mass; the dump rows satisfy these to rel 1e-9, the tolerance of the stage-1 validator stage1/analysis/validate_mom6_w2.py, because the guarded per-layer updates below the surface layer round T/S by ~1 ulp on ~10 of 74 layers per row). The heat_residual variable pins the consistency of the two dumps against the EnthalpyConst = 0 configuration: with EnthalpyConst = 0 it reduces to sum_k h_after_k*dT_k - (penSW_total - leftover) == 0, i.e. the shortwave dump's per-layer heating dT (mom6_sw_abs.csv) must reproduce the bflux dump's per-band totals penSW_bnd and leftover (mom6_bflux.csv) once the layer-1 flux law holds; the dThickness*T_before_1*EnthalpyConst term it also carries (F90:1141) pins EnthalpyConst = 0. The general multi-layer distribution of the fluxes (fractionOfForcing = min(1, h_k/max(H_subroundoff, minimum_forcing_depth - netMassOut_rem)), the evap_CFL_limit branch and the dSalt_frac_max floor, F90:1117-1132) is a sequential data-dependent scan that no traced row exercises (fractionOfForcing = 1 in layer 1, 0 below) and that is not expressible as an algebraic law; it is listed as a gap in README.md, as are the brine-plume insertion (DO_BRINE_PLUME=False in this run) and the heat-content-of-rain/runoff terms of extractFluxes1d (MOM_forcing_type.F90:464-961), which is not part of this component (its outputs netMassIn/netMassOut/netHeat/netSalt/penSW_bnd are the component's inputs)."
tags: ["ocean", "mom6", "model", "boundary-fluxes", "surface-forcing", "cesm"]
---

## Description

Stage-2 implementation of the MOM6 surface boundary fluxes applied in the diabatic column (applyBoundaryFluxesInOut, MOM_diabatic_aux.F90:702-1483 of the instrumented fork stage1/EqESM-cesm-mom6; run configuration C_JRA_t62_mom6_inst: AGGREGATE_FW_FORCING=True so netMassIn == 0 (the net mass change of the column is netMassOut alone), all unit rescale factors 1.0, dt = 3600 s). The component applies the net surface mass, heat and salt fluxes of a step to the surface layer (step A, F90:1039-1071 with netMassIn = 0, and step B, F90:1109-1146 with fractionOfForcing = 1 in the surface layer and the running remainders vanishing exactly -- every traced row has h_1 ~ 2.5 m well above minimum_forcing_depth, so all forcing is consumed by layer 1, verified on all 156 rows: h, T and S change only in layer 1, and only by the fluxes), with the heat content of the mass exchange added via dThickness*T*EnthalpyConst (F90:1141); the reference run has EnthalpyConst = 0 (F90:845-846) because the CESM coupler provides heat_content_evap. The penetrating shortwave is applied by absorbRemainingSW (step C, F90:1355-1362, MOM_opacity.F90:602-885): the component consumes the per-layer SW heating dT and the bottom leftover of the ShortwaveAbsorption component (mom6_shortwave.esm; here sourced from the mom6_sw_abs.csv dump columns dT_k and pen_sw_rem_n(75)). The column budgets are the plain per-layer sums dMass_col = sum_k (h_after_k - h_before_k) == netMassIn + netMassOut, dSalt_col = sum_k (h_after_k*S_after_k - h_before_k*S_before_k) == netSalt, and dHeat_col = sum_k (h_after_k*T_after_k - h_before_k*T_before_k) == netHeat + sum_n penSW_bnd(n) - leftover (netHeat already contains the non-penetrating SW and excludes the heat content of the outgoing mass; the dump rows satisfy these to rel 1e-9, the tolerance of the stage-1 validator stage1/analysis/validate_mom6_w2.py, because the guarded per-layer updates below the surface layer round T/S by ~1 ulp on ~10 of 74 layers per row). The heat_residual variable pins the consistency of the two dumps against the EnthalpyConst = 0 configuration: with EnthalpyConst = 0 it reduces to sum_k h_after_k*dT_k - (penSW_total - leftover) == 0, i.e. the shortwave dump's per-layer heating dT (mom6_sw_abs.csv) must reproduce the bflux dump's per-band totals penSW_bnd and leftover (mom6_bflux.csv) once the layer-1 flux law holds; the dThickness*T_before_1*EnthalpyConst term it also carries (F90:1141) pins EnthalpyConst = 0. The general multi-layer distribution of the fluxes (fractionOfForcing = min(1, h_k/max(H_subroundoff, minimum_forcing_depth - netMassOut_rem)), the evap_CFL_limit branch and the dSalt_frac_max floor, F90:1117-1132) is a sequential data-dependent scan that no traced row exercises (fractionOfForcing = 1 in layer 1, 0 below) and that is not expressible as an algebraic law; it is listed as a gap in README.md, as are the brine-plume insertion (DO_BRINE_PLUME=False in this run) and the heat-content-of-rain/runoff terms of extractFluxes1d (MOM_forcing_type.F90:464-961), which is not part of this component (its outputs netMassIn/netMassOut/netHeat/netSalt/penSW_bnd are the component's inputs).

## Reference

- MOM6 (Modular Ocean Model 6), ESCOMP/CESM components/mom (dev/ncar_260909 @301879336; instrumented fork stage1/EqESM-cesm-mom6 branch instrument/mom6-dumps, reference run C_JRA_t62_mom6_inst): src/parameterizations/vertical/MOM_diabatic_aux.F90 (applyBoundaryFluxesInOut 702-1483) and src/parameterizations/vertical/MOM_opacity.F90 (absorbRemainingSW 602-869) - the reference implementation these components are transcribed from.
- EarthSciModels - the authoritative .esm corpus this component lives in.

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `h_before` | `m` | `0.0` | Layer thicknesses at applyBoundaryFluxesInOut entry (the dump column h_before_k), [m] |
| `T_before` | `degC` | `0.0` | Layer temperatures at applyBoundaryFluxesInOut entry (the dump column T_before_k), [degC] |
| `S_before` | `ppt` | `0.0` | Layer salinities at applyBoundaryFluxesInOut entry (the dump column S_before_k), [ppt] |
| `dT` | `degC` | `0.0` | Per-layer temperature change from the penetrating shortwave absorption of absorbRemainingSW (step C; the dump column dT_k of mom6_sw_abs.csv; in the merged tree this is the dT output of the ShortwaveAbsorption component, mom6_shortwave.esm), [degC] |
| `netMassIn` | `m` | `0.0` | Net surface mass flux into the ocean over the step (step A; == 0 on every traced row under AGGREGATE_FW_FORCING=True; the dump column netMassIn), [m] |
| `netMassOut` | `m` | `0.0` | Net surface mass flux out of the ocean over the step, == the dump's net column mass change netMassInOut on every traced row (the dump column netMassOut; range -1.6e-5..2.0e-3 m), [m] |
| `netHeat` | `degC m` | `0.0` | Net surface heat flux over the step excluding the penetrating shortwave (which enters per band) and excluding the heat content of the outgoing mass (the dump column netHeat; the non-penetrating SW nonpenSW is a diagnostic part of it), [degC m] |
| `netSalt` | `ppt m` | `0.0` | Net surface salt flux over the step (the dump column netSalt), [ppt m] |
| `penSW_bnd` | `degC m` | `0.0` | Penetrating shortwave heat at the surface, per spectral band, over the step (the dump columns penSW_bnd_n; nsw = 2 active bands (OHLMANN_03) with bands 3..10 zero in the dump, the MAX_SW_BANDS padding), [degC m] |
| `leftover` | `degC m` | `0.0` | Penetrating shortwave reaching the column bottom, sum_n pen_sw_rem(n,75) of the ShortwaveAbsorption component (0.0 on every traced row: all traced columns absorb all SW), [degC m] |
| `EnthalpyConst` | `dimensionless` | `0.0` | The heat-content switch of the mass exchange: dTemp includes dThickness*T*EnthalpyConst (F90:1141); EnthalpyConst = 1.0 by default, 0.0 when fluxes%heat_content_evap is associated (F90:845-846) -- the CESM coupler provides it, so the reference run has EnthalpyConst = 0.0, [-] |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `dThickness_1` | `m` |  | The surface layer's thickness change over the step, netMassIn + netMassOut (steps A+B with fractionOfForcing = 1 in the surface layer), [m] |
| `dTemp_1` | `degC m` |  | The heat added to the surface layer over the step, netHeat plus the heat content of the mass exchange dThickness_1*T_before_1*EnthalpyConst (F90:1141; the latter vanishes with EnthalpyConst = 0 in this run), [degC m] |
| `dSalt_1` | `ppt m` | `0.0` | The salt added to the surface layer over the step, netSalt (the dSalt_frac_max floor of F90:1132 never binds on the traced rows: \|netSalt\| ~ 1e-3 ppt m vs 0.8*h*S ~ 66 ppt m), [ppt m] |
| `h_after` | `m` |  | Layer thicknesses after the fluxes: the surface layer gains dThickness_1, deeper layers are unchanged (the dump column h_after_k; h_after_k == h_before_k bitwise for k >= 2 on all 156 traced rows), [m] |
| `T_mass` | `degC` |  | Layer temperatures after the mass/heat/salt steps A+B (the surface layer updated by (h*T + dTemp)/h_after per F90:1143-1144, deeper layers unchanged), before the shortwave heating of step C, [degC] |
| `T_after` | `degC` |  | Layer temperatures after all flux applications, T_mass + dT (the dump column T_after_k; for k >= 2 the dump reproduces T_before_k + dT_k to ~1 ulp of T, the roundoff of the guarded update path), [degC] |
| `S_after` | `ppt` |  | Layer salinities after the salt update (the surface layer updated by (h*S + dSalt)/h_after per F90:1145, deeper layers unchanged; the dump column S_after_k), [ppt] |
| `penSW_total` | `degC m` |  | The column's total penetrating shortwave heat, penSW_total = sum over n in band of penSW_bnd(n) (bands 3..10 zero in the dump), [degC m] |
| `dMass_k` | `m` |  | Per-layer thickness change h_after_k - h_before_k, [m] |
| `dSalt_k` | `ppt m` |  | Per-layer salt content change h_after_k*S_after_k - h_before_k*S_before_k, [ppt m] |
| `dHeat_k` | `degC m` |  | Per-layer heat content change h_after_k*T_after_k - h_before_k*T_before_k, [degC m] |
| `dMass_col` | `m` |  | The column mass change, dMass_col = sum over k in layer of dMass_k == netMassIn + netMassOut (the dump identity sum_k (h_after - h_before) == netMassInOut), [m] |
| `dSalt_col` | `ppt m` |  | The column salt content change, dSalt_col = sum over k in layer of dSalt_k == netSalt (the dump identity), [ppt m] |
| `dHeat_col` | `degC m` |  | The column heat content change, dHeat_col = sum over k in layer of dHeat_k == netHeat + sum_n penSW_bnd(n) - leftover (the dump heat identity; netHeat includes the non-penetrating SW), [degC m] |
| `mass_residual` | `m` |  | The mass balance residual dMass_col - (netMassIn + netMassOut) == 0 by construction of h_after (the surface-layer update consumes the whole net mass flux), [m] |
| `salt_residual` | `ppt m` |  | The salt balance residual dSalt_col - netSalt == 0 by construction of S_after_1, [ppt m] |
| `heat_residual` | `degC m` |  | The heat balance residual dHeat_col - (netHeat + penSW_total - leftover), which checks the consistency of the two dumps plus EnthalpyConst: substituting the layer-1 law and T_after_k = T_before_k + dT_k it reduces to EnthalpyConst*dThickness_1*T_before_1 + sum_k h_after_k*dT_k - (penSW_total - leftover), i.e. the shortwave dump's per-layer heating dT (mom6_sw_abs.csv) must reproduce the bflux dump's per-band totals penSW_bnd and leftover (mom6_bflux.csv), and the EnthalpyConst term (F90:1141, 845-846) pins the EnthalpyConst = 0 configuration, [degC m] |

## Observed expressions

$$
dThickness_{1} = netMassIn + netMassOut
$$
_The surface layer's thickness change over the step, netMassIn + netMassOut (steps A+B with fractionOfForcing = 1 in the surface layer), [m]_

$$
dTemp_{1} = netHeat + dThickness_{1} \cdot \mathrm{index}\left(T_{before}, 1\right) \cdot EnthalpyConst
$$
_The heat added to the surface layer over the step, netHeat plus the heat content of the mass exchange dThickness_1*T_before_1*EnthalpyConst (F90:1141; the latter vanishes with EnthalpyConst = 0 in this run), [degC m]_

$$
dSalt_{1} = netSalt
$$
_The salt added to the surface layer over the step, netSalt (the dSalt_frac_max floor of F90:1132 never binds on the traced rows: |netSalt| ~ 1e-3 ppt m vs 0.8*h*S ~ 66 ppt m), [ppt m]_

$$
h_{after} = \mathrm{faq}\left(h_{before}, dThickness_{1}\right)
$$
_Layer thicknesses after the fluxes: the surface layer gains dThickness_1, deeper layers are unchanged (the dump column h_after_k; h_after_k == h_before_k bitwise for k >= 2 on all 156 traced rows), [m]_

$$
T_{mass} = \mathrm{faq}\left(T_{before}, dTemp_{1}, h_{before}, h_{after}\right)
$$
_Layer temperatures after the mass/heat/salt steps A+B (the surface layer updated by (h*T + dTemp)/h_after per F90:1143-1144, deeper layers unchanged), before the shortwave heating of step C, [degC]_

$$
T_{after} = \mathrm{faq}\left(T_{mass}, dT\right)
$$
_Layer temperatures after all flux applications, T_mass + dT (the dump column T_after_k; for k >= 2 the dump reproduces T_before_k + dT_k to ~1 ulp of T, the roundoff of the guarded update path), [degC]_

$$
S_{after} = \mathrm{faq}\left(S_{before}, dSalt_{1}, h_{before}, h_{after}\right)
$$
_Layer salinities after the salt update (the surface layer updated by (h*S + dSalt)/h_after per F90:1145, deeper layers unchanged; the dump column S_after_k), [ppt]_

$$
penSW_{total} = \mathrm{faq}\left(penSW_{bnd}\right)
$$
_The column's total penetrating shortwave heat, penSW_total = sum over n in band of penSW_bnd(n) (bands 3..10 zero in the dump), [degC m]_

$$
dMass_{k} = \mathrm{faq}\left(h_{after}, h_{before}\right)
$$
_Per-layer thickness change h_after_k - h_before_k, [m]_

$$
dSalt_{k} = \mathrm{faq}\left(S_{after}, S_{before}, h_{after}, h_{before}\right)
$$
_Per-layer salt content change h_after_k*S_after_k - h_before_k*S_before_k, [ppt m]_

$$
dHeat_{k} = \mathrm{faq}\left(T_{after}, T_{before}, h_{after}, h_{before}\right)
$$
_Per-layer heat content change h_after_k*T_after_k - h_before_k*T_before_k, [degC m]_

$$
dMass_{col} = \mathrm{faq}\left(dMass_{k}\right)
$$
_The column mass change, dMass_col = sum over k in layer of dMass_k == netMassIn + netMassOut (the dump identity sum_k (h_after - h_before) == netMassInOut), [m]_

$$
dSalt_{col} = \mathrm{faq}\left(dSalt_{k}\right)
$$
_The column salt content change, dSalt_col = sum over k in layer of dSalt_k == netSalt (the dump identity), [ppt m]_

$$
dHeat_{col} = \mathrm{faq}\left(dHeat_{k}\right)
$$
_The column heat content change, dHeat_col = sum over k in layer of dHeat_k == netHeat + sum_n penSW_bnd(n) - leftover (the dump heat identity; netHeat includes the non-penetrating SW), [degC m]_

$$
mass_{residual} = dMass_{col} - \left(netMassIn + netMassOut\right)
$$
_The mass balance residual dMass_col - (netMassIn + netMassOut) == 0 by construction of h_after (the surface-layer update consumes the whole net mass flux), [m]_

$$
salt_{residual} = dSalt_{col} - netSalt
$$
_The salt balance residual dSalt_col - netSalt == 0 by construction of S_after_1, [ppt m]_

$$
heat_{residual} = dHeat_{col} - netHeat - penSW_{total} + leftover
$$
_The heat balance residual dHeat_col - (netHeat + penSW_total - leftover), which checks the consistency of the two dumps plus EnthalpyConst: substituting the layer-1 law and T_after_k = T_before_k + dT_k it reduces to EnthalpyConst*dThickness_1*T_before_1 + sum_k h_after_k*dT_k - (penSW_total - leftover), i.e. the shortwave dump's per-layer heating dT (mom6_sw_abs.csv) must reproduce the bflux dump's per-band totals penSW_bnd and leftover (mom6_bflux.csv), and the EnthalpyConst term (F90:1141, 845-846) pins the EnthalpyConst = 0 configuration, [degC m]_

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "expression_template_imports": [
    {
      "ref": "./mom6_templates.esm"
    }
  ],
  "variables": {
    "h_before": {
      "type": "parameter",
      "shape": [
        "layer"
      ],
      "units": "m",
      "default": 0.0,
      "description": "Layer thicknesses at applyBoundaryFluxesInOut entry (the dump column h_before_k), [m]"
    },
    "T_before": {
      "type": "parameter",
      "shape": [
        "layer"
      ],
      "units": "degC",
      "default": 0.0,
      "description": "Layer temperatures at applyBoundaryFluxesInOut entry (the dump column T_before_k), [degC]"
    },
    "S_before": {
      "type": "parameter",
      "shape": [
        "layer"
      ],
      "units": "ppt",
      "default": 0.0,
      "description": "Layer salinities at applyBoundaryFluxesInOut entry (the dump column S_before_k), [ppt]"
    },
    "dT": {
      "type": "parameter",
      "shape": [
        "layer"
      ],
      "units": "degC",
      "default": 0.0,
      "description": "Per-layer temperature change from the penetrating shortwave absorption of absorbRemainingSW (step C; the dump column dT_k of mom6_sw_abs.csv; in the merged tree this is the dT output of the ShortwaveAbsorption component, mom6_shortwave.esm), [degC]"
    },
    "netMassIn": {
      "type": "parameter",
      "units": "m",
      "default": 0.0,
      "description": "Net surface mass flux into the ocean over the step (step A; == 0 on every traced row under AGGREGATE_FW_FORCING=True; the dump column netMassIn), [m]"
    },
    "netMassOut": {
      "type": "parameter",
      "units": "m",
      "default": 0.0,
      "description": "Net surface mass flux out of the ocean over the step, == the dump's net column mass change netMassInOut on every traced row (the dump column netMassOut; range -1.6e-5..2.0e-3 m), [m]"
    },
    "netHeat": {
      "type": "parameter",
      "units": "degC m",
      "default": 0.0,
      "description": "Net surface heat flux over the step excluding the penetrating shortwave (which enters per band) and excluding the heat content of the outgoing mass (the dump column netHeat; the non-penetrating SW nonpenSW is a diagnostic part of it), [degC m]"
    },
    "netSalt": {
      "type": "parameter",
      "units": "ppt m",
      "default": 0.0,
      "description": "Net surface salt flux over the step (the dump column netSalt), [ppt m]"
    },
    "penSW_bnd": {
      "type": "parameter",
      "shape": [
        "band"
      ],
      "units": "degC m",
      "default": 0.0,
      "description": "Penetrating shortwave heat at the surface, per spectral band, over the step (the dump columns penSW_bnd_n; nsw = 2 active bands (OHLMANN_03) with bands 3..10 zero in the dump, the MAX_SW_BANDS padding), [degC m]"
    },
    "leftover": {
      "type": "parameter",
      "units": "degC m",
      "default": 0.0,
      "description": "Penetrating shortwave reaching the column bottom, sum_n pen_sw_rem(n,75) of the ShortwaveAbsorption component (0.0 on every traced row: all traced columns absorb all SW), [degC m]"
    },
    "EnthalpyConst": {
      "type": "parameter",
      "units": "dimensionless",
      "default": 0.0,
      "description": "The heat-content switch of the mass exchange: dTemp includes dThickness*T*EnthalpyConst (F90:1141); EnthalpyConst = 1.0 by default, 0.0 when fluxes%heat_content_evap is associated (F90:845-846) -- the CESM coupler provides it, so the reference run has EnthalpyConst = 0.0, [-]"
    },
    "dThickness_1": {
      "type": "unknown",
      "units": "m",
      "description": "The surface layer's thickness change over the step, netMassIn + netMassOut (steps A+B with fractionOfForcing = 1 in the surface layer), [m]"
    },
    "dTemp_1": {
      "type": "unknown",
      "units": "degC m",
      "description": "The heat added to the surface layer over the step, netHeat plus the heat content of the mass exchange dThickness_1*T_before_1*EnthalpyConst (F90:1141; the latter vanishes with EnthalpyConst = 0 in this run), [degC m]"
    },
    "dSalt_1": {
      "type": "unknown",
      "units": "ppt m",
      "default": 0.0,
      "description": "The salt added to the surface layer over the step, netSalt (the dSalt_frac_max floor of F90:1132 never binds on the traced rows: |netSalt| ~ 1e-3 ppt m vs 0.8*h*S ~ 66 ppt m), [ppt m]"
    },
    "h_after": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "m",
      "description": "Layer thicknesses after the fluxes: the surface layer gains dThickness_1, deeper layers are unchanged (the dump column h_after_k; h_after_k == h_before_k bitwise for k >= 2 on all 156 traced rows), [m]"
    },
    "T_mass": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "degC",
      "description": "Layer temperatures after the mass/heat/salt steps A+B (the surface layer updated by (h*T + dTemp)/h_after per F90:1143-1144, deeper layers unchanged), before the shortwave heating of step C, [degC]"
    },
    "T_after": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "degC",
      "description": "Layer temperatures after all flux applications, T_mass + dT (the dump column T_after_k; for k >= 2 the dump reproduces T_before_k + dT_k to ~1 ulp of T, the roundoff of the guarded update path), [degC]"
    },
    "S_after": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "ppt",
      "description": "Layer salinities after the salt update (the surface layer updated by (h*S + dSalt)/h_after per F90:1145, deeper layers unchanged; the dump column S_after_k), [ppt]"
    },
    "penSW_total": {
      "type": "unknown",
      "units": "degC m",
      "description": "The column's total penetrating shortwave heat, penSW_total = sum over n in band of penSW_bnd(n) (bands 3..10 zero in the dump), [degC m]"
    },
    "dMass_k": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "m",
      "description": "Per-layer thickness change h_after_k - h_before_k, [m]"
    },
    "dSalt_k": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "ppt m",
      "description": "Per-layer salt content change h_after_k*S_after_k - h_before_k*S_before_k, [ppt m]"
    },
    "dHeat_k": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "degC m",
      "description": "Per-layer heat content change h_after_k*T_after_k - h_before_k*T_before_k, [degC m]"
    },
    "dMass_col": {
      "type": "unknown",
      "units": "m",
      "description": "The column mass change, dMass_col = sum over k in layer of dMass_k == netMassIn + netMassOut (the dump identity sum_k (h_after - h_before) == netMassInOut), [m]"
    },
    "dSalt_col": {
      "type": "unknown",
      "units": "ppt m",
      "description": "The column salt content change, dSalt_col = sum over k in layer of dSalt_k == netSalt (the dump identity), [ppt m]"
    },
    "dHeat_col": {
      "type": "unknown",
      "units": "degC m",
      "description": "The column heat content change, dHeat_col = sum over k in layer of dHeat_k == netHeat + sum_n penSW_bnd(n) - leftover (the dump heat identity; netHeat includes the non-penetrating SW), [degC m]"
    },
    "mass_residual": {
      "type": "unknown",
      "units": "m",
      "description": "The mass balance residual dMass_col - (netMassIn + netMassOut) == 0 by construction of h_after (the surface-layer update consumes the whole net mass flux), [m]"
    },
    "salt_residual": {
      "type": "unknown",
      "units": "ppt m",
      "description": "The salt balance residual dSalt_col - netSalt == 0 by construction of S_after_1, [ppt m]"
    },
    "heat_residual": {
      "type": "unknown",
      "units": "degC m",
      "description": "The heat balance residual dHeat_col - (netHeat + penSW_total - leftover), which checks the consistency of the two dumps plus EnthalpyConst: substituting the layer-1 law and T_after_k = T_before_k + dT_k it reduces to EnthalpyConst*dThickness_1*T_before_1 + sum_k h_after_k*dT_k - (penSW_total - leftover), i.e. the shortwave dump's per-layer heating dT (mom6_sw_abs.csv) must reproduce the bflux dump's per-band totals penSW_bnd and leftover (mom6_bflux.csv), and the EnthalpyConst term (F90:1141, 845-846) pins the EnthalpyConst = 0 configuration, [degC m]"
    }
  },
  "equations": [
    {
      "lhs": "dThickness_1",
      "rhs": {
        "op": "+",
        "args": [
          "netMassIn",
          "netMassOut"
        ]
      }
    },
    {
      "lhs": "dTemp_1",
      "rhs": {
        "op": "+",
        "args": [
          "netHeat",
          {
            "op": "*",
            "args": [
              {
                "op": "*",
                "args": [
                  "dThickness_1",
                  {
                    "op": "index",
                    "args": [
                      "T_before",
                      1
                    ]
                  }
                ]
              },
              "EnthalpyConst"
            ]
          }
        ]
      }
    },
    {
      "lhs": "dSalt_1",
      "rhs": "netSalt"
    },
    {
      "lhs": "h_after",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "ifelse",
          "args": [
            {
              "op": "==",
              "args": [
                "i",
                1
              ]
            },
            {
              "op": "+",
              "args": [
                {
                  "op": "index",
                  "args": [
                    "h_before",
                    "i"
                  ]
                },
                "dThickness_1"
              ]
            },
            {
              "op": "index",
              "args": [
                "h_before",
                "i"
              ]
            }
          ]
        },
        "args": [
          "h_before",
          "dThickness_1"
        ]
      }
    },
    {
      "lhs": "T_mass",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "apply_expression_template",
          "args": [],
          "name": "surface_mix",
          "bindings": {
            "X_before": "T_before",
            "dX": "dTemp_1",
            "h_before": "h_before",
            "h_after": "h_after"
          }
        },
        "args": [
          "T_before",
          "dTemp_1",
          "h_before",
          "h_after"
        ]
      }
    },
    {
      "lhs": "S_after",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "apply_expression_template",
          "args": [],
          "name": "surface_mix",
          "bindings": {
            "X_before": "S_before",
            "dX": "dSalt_1",
            "h_before": "h_before",
            "h_after": "h_after"
          }
        },
        "args": [
          "S_before",
          "dSalt_1",
          "h_before",
          "h_after"
        ]
      }
    },
    {
      "lhs": "T_after",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "+",
          "args": [
            {
              "op": "index",
              "args": [
                "T_mass",
                "i"
              ]
            },
            {
              "op": "index",
              "args": [
                "dT",
                "i"
              ]
            }
          ]
        },
        "args": [
          "T_mass",
          "dT"
        ]
      }
    },
    {
      "lhs": "penSW_total",
      "rhs": {
        "op": "faq",
        "output_idx": [],
        "reduce": "+",
        "ranges": {
          "n": {
            "from": "band"
          }
        },
        "expr": {
          "op": "index",
          "args": [
            "penSW_bnd",
            "n"
          ]
        },
        "args": [
          "penSW_bnd"
        ]
      }
    },
    {
      "lhs": "dMass_k",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "-",
          "args": [
            {
              "op": "index",
              "args": [
                "h_after",
                "i"
              ]
            },
            {
              "op": "index",
              "args": [
                "h_before",
                "i"
              ]
            }
          ]
        },
        "args": [
          "h_after",
          "h_before"
        ]
      }
    },
    {
      "lhs": "dSalt_k",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "apply_expression_template",
          "args": [],
          "name": "layer_content_change",
          "bindings": {
            "X_after": "S_after",
            "X_before": "S_before",
            "h_after": "h_after",
            "h_before": "h_before"
          }
        },
        "args": [
          "S_after",
          "S_before",
          "h_after",
          "h_before"
        ]
      }
    },
    {
      "lhs": "dHeat_k",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "apply_expression_template",
          "args": [],
          "name": "layer_content_change",
          "bindings": {
            "X_after": "T_after",
            "X_before": "T_before",
            "h_after": "h_after",
            "h_before": "h_before"
          }
        },
        "args": [
          "T_after",
          "T_before",
          "h_after",
          "h_before"
        ]
      }
    },
    {
      "lhs": "dMass_col",
      "rhs": {
        "op": "faq",
        "output_idx": [],
        "reduce": "+",
        "ranges": {
          "k": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "index",
          "args": [
            "dMass_k",
            "k"
          ]
        },
        "args": [
          "dMass_k"
        ]
      }
    },
    {
      "lhs": "dSalt_col",
      "rhs": {
        "op": "faq",
        "output_idx": [],
        "reduce": "+",
        "ranges": {
          "k": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "index",
          "args": [
            "dSalt_k",
            "k"
          ]
        },
        "args": [
          "dSalt_k"
        ]
      }
    },
    {
      "lhs": "dHeat_col",
      "rhs": {
        "op": "faq",
        "output_idx": [],
        "reduce": "+",
        "ranges": {
          "k": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "index",
          "args": [
            "dHeat_k",
            "k"
          ]
        },
        "args": [
          "dHeat_k"
        ]
      }
    },
    {
      "lhs": "mass_residual",
      "rhs": {
        "op": "-",
        "args": [
          "dMass_col",
          {
            "op": "+",
            "args": [
              "netMassIn",
              "netMassOut"
            ]
          }
        ]
      }
    },
    {
      "lhs": "salt_residual",
      "rhs": {
        "op": "-",
        "args": [
          "dSalt_col",
          "netSalt"
        ]
      }
    },
    {
      "lhs": "heat_residual",
      "rhs": {
        "op": "+",
        "args": [
          {
            "op": "-",
            "args": [
              {
                "op": "-",
                "args": [
                  "dHeat_col",
                  "netHeat"
                ]
              },
              "penSW_total"
            ]
          },
          "leftover"
        ]
      }
    }
  ],
  "tests": [
    {
      "id": "bflux_t3600_g3j78",
      "description": "mom6_bflux.csv row (tod, gi, gj) = (3600, 3, 78) with dT and leftover from mom6_sw_abs.csv for the same cell/step: the first thermo step, netMassInOut = -1.3294e-5 m (net mass leaves the ocean), netHeat = -0.0330 degC m, netSalt = +2.34e-3 ppt m, penSW_bnd = (0.08330, 0.03043) degC m with bands 3..10 zero, leftover = 0. Pins the full flux application in the surface layer (h_after_1 = h_before_1 + netMassOut; T_after_1 = (h*T + netHeat)/h_after_1 + dT_1 with EnthalpyConst = 0; S_after_1 = (h*S + netSalt)/h_after_1), one shortwave-law point below the surface (T_after_2 = T_before_2 + dT_2), the total penetrating shortwave penSW_total, the column heat budget dHeat_col, and the heat_residual (the two-dump consistency check: with EnthalpyConst = 0 it reduces to sum_k h_after_k*dT_k - (penSW_total - leftover) == 0). The mass and salt column budgets are not pinned: dMass_col == netMassIn + netMassOut and dSalt_col == netSalt are algebraic identities of the already-pinned layer-1 laws (h_after_1, S_after_1), so they cannot fail. Values are dump columns (mom6_bflux.csv, mom6_sw_abs.csv) except penSW_total (derived: the sum of the input penSW_bnd bands), dHeat_col and heat_residual, which are derived (the budget identities, validated at rel 1e-9 by stage1/analysis/validate_mom6_w2.py because the guarded updates below the surface layer round S/T by ~1 ulp; heat_residual at abs 1e-12).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "h_before": [
          2.505951254018008,
          2.501892978164657,
          2.5017272545267977,
          2.5015693814166826,
          3.001726517137612,
          3.0015593590329077,
          4.001807120040217,
          5.0018870024358435,
          5.001492177647564,
          5.0011284090633845,
          5.00083930807502,
          5.000628417858856,
          5.000488628830354,
          5.000401849324857,
          5.000396867081619,
          5.000467952434573,
          5.000572200145099,
          5.000735150856453,
          5.001008941766694,
          5.001503210891359,
          5.0023653454907215,
          5.003790098254819,
          5.006071033680151,
          5.009629768138034,
          5.015074076068978,
          5.023160594684109,
          5.034925407435693,
          5.051731910594908,
          5.075367891423117,
          5.108103636445879,
          5.1527974185346865,
          5.213007285789468,
          5.293130012105934,
          5.398545436034885,
          5.535702362341015,
          5.71290727783589,
          5.93902285082774,
          6.225753904267744,
          6.586379406182547,
          7.036631765948616,
          7.594949272917944,
          8.282801837278132,
          9.125530909640725,
          10.151740250381746,
          11.394334798084529,
          12.891492437510122,
          14.687463397187956,
          16.832907389496818,
          19.381317682286536,
          22.396719964256963,
          25.95622227092345,
          30.135244286889563,
          35.02536929516961,
          40.729080456111625,
          47.358878422378254,
          49.631692734966386,
          0.001513827257149827,
          0.0010000085529628421,
          0.000999962085871611,
          0.0009999599688644196,
          0.0009999603995984824,
          0.0009999604862692374,
          0.0009999605668350338,
          0.0009999606417310767,
          0.0009999607118574131,
          0.0009999607791579305,
          0.0009999608479388797,
          0.0009999609278773275,
          0.000999961040885174,
          0.0009999612367414307,
          0.0009999616285651701,
          0.000999962472857992,
          0.0009999643486363742,
          0.0009999685535890417,
          0.0009999779638633285
        ],
        "T_before": [
          1.9019792708374321,
          1.8515253625554617,
          1.8514055607269526,
          1.8862508282108714,
          1.8448579551802922,
          1.430724547487314,
          1.184740754822769,
          0.4545384997307825,
          -0.25447828091116215,
          -0.49110845069930276,
          -0.7745387986640418,
          -1.0108442754100886,
          -1.2172725851525845,
          -1.4044141170351905,
          -1.5241563554760427,
          -1.5632026230407188,
          -1.5827837524498456,
          -1.595232696516834,
          -1.623477480795172,
          -1.6357484297227263,
          -1.6466791888181294,
          -1.656221184292802,
          -1.654576424760375,
          -1.6489240159200447,
          -1.6486107320064047,
          -1.648368487671491,
          -1.6483276097363904,
          -1.648346876856009,
          -1.6483490468578914,
          -1.6483485152219775,
          -1.7240770995793384,
          -1.779316420795108,
          -1.779303855059408,
          -1.7793022937387388,
          -1.7792947412824167,
          -1.7522894115497871,
          -1.749246515320854,
          -1.7492462774605688,
          -1.7492489013831836,
          -1.7732489287041933,
          -1.8026864282434933,
          -1.8236396376574981,
          -1.8368274543826035,
          -1.8484545779130355,
          -1.8644139652470242,
          -1.882990351789187,
          -1.897117644563898,
          -1.906781666944587,
          -1.9150097745832726,
          -1.9148179312139284,
          -1.912509584509385,
          -1.8814568103622398,
          -1.8724260008079083,
          -1.8562907816743524,
          -1.870752635490293,
          -1.9368455913068205,
          -1.1062868181803074,
          -0.6946169759566972,
          -0.6945670544170301,
          -0.6945579964992634,
          -0.6945579959581468,
          -0.6945579959743844,
          -0.694557995989068,
          -0.6945579960022066,
          -0.6945579960138252,
          -0.6945579960239971,
          -0.6945579960329397,
          -0.6945579960413003,
          -0.6945579960509881,
          -0.6945579960676073,
          -0.6945579961075465,
          -0.6945579962186464,
          -0.6945579965403735,
          -0.6945579974789736,
          -0.6945580002170941
        ],
        "S_before": [
          33.59310698272627,
          33.588722523356644,
          33.588728173167695,
          33.782800236630365,
          33.90461160541478,
          33.965910906160445,
          34.00789518405837,
          34.070536794122596,
          34.148386895795504,
          34.21095418134514,
          34.24479571539441,
          34.25233415633717,
          34.26230440210986,
          34.27093940432499,
          34.303318701427465,
          34.33962416579716,
          34.34302443500428,
          34.34965119897978,
          34.365526903564955,
          34.37662928211302,
          34.38304962038136,
          34.38846319400944,
          34.39100055450505,
          34.39108359654662,
          34.39125830182479,
          34.39637823789326,
          34.40920736997063,
          34.417973261151076,
          34.42438357645966,
          34.428414420006455,
          34.43011324225855,
          34.430855379327674,
          34.431793412511745,
          34.43297586591467,
          34.4344236756591,
          34.43613455500456,
          34.43798378740711,
          34.43994122932394,
          34.44203177035942,
          34.44430555607114,
          34.44611056416715,
          34.44726421007603,
          34.4476414576481,
          34.44764924130422,
          34.447509850940904,
          34.44685009113937,
          34.44663806924799,
          34.44589694101489,
          34.445462825680195,
          34.450896101063485,
          34.455125716217445,
          34.45888024899668,
          34.464602805430374,
          34.47257909244512,
          34.476978569749,
          34.47695208208595,
          34.59731571231767,
          34.65569524651118,
          34.65570220934429,
          34.655703276547946,
          34.6557032765586,
          34.655703276558285,
          34.655703276557986,
          34.65570327655773,
          34.655703276557496,
          34.65570327655731,
          34.65570327655714,
          34.65570327655696,
          34.65570327655678,
          34.655703276556444,
          34.65570327655567,
          34.655703276553474,
          34.65570327654714,
          34.655703276528655,
          34.655703276474746
        ],
        "dT": [
          0.020810465965843017,
          0.009550013104703936,
          0.005384655860658727,
          0.0033510463218076048,
          0.0020832554734739883,
          0.001255812269909562,
          0.0007057549926394735,
          0.00033709633947343054,
          0.000146711018099821,
          6.386184089174352e-05,
          2.7799954323226572e-05,
          1.2102223645671373e-05,
          5.2686491871511976e-06,
          2.2937275665491086e-06,
          9.985920508270851e-07,
          4.3474276623101105e-07,
          1.892650642876248e-07,
          8.23946835204481e-08,
          3.586845753744683e-08,
          1.5613474735332034e-08,
          1.2032516316651254e-08,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0
        ],
        "netMassIn": 0.0,
        "netMassOut": -1.3294187874021135e-05,
        "netHeat": -0.03300379386004522,
        "netSalt": 0.0023417215038853043,
        "penSW_bnd": [
          0.08330292343473028,
          0.03042626642391491,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0
        ],
        "leftover": 0.0
      },
      "tolerance": {
        "rel": 1e-12
      },
      "assertions": [
        {
          "variable": "h_after",
          "time": 0.0,
          "expected": 2.505937959830134,
          "coords": {
            "layer": 1
          }
        },
        {
          "variable": "T_after",
          "time": 0.0,
          "expected": 1.9096295911336987,
          "coords": {
            "layer": 1
          }
        },
        {
          "variable": "S_after",
          "time": 0.0,
          "expected": 33.59421966573123,
          "coords": {
            "layer": 1
          }
        },
        {
          "variable": "T_after",
          "time": 0.0,
          "expected": 1.8610753756601657,
          "coords": {
            "layer": 2
          }
        },
        {
          "variable": "penSW_total",
          "time": 0.0,
          "expected": 0.11372918985864519
        },
        {
          "variable": "dHeat_col",
          "time": 0.0,
          "expected": 0.08072539599859563
        },
        {
          "variable": "heat_residual",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "abs": 1e-12
          }
        }
      ]
    },
    {
      "id": "bflux_t3600_g7j80",
      "description": "mom6_bflux.csv row (tod, gi, gj) = (3600, 7, 80) with dT and leftover from mom6_sw_abs.csv: the first thermo step of the second traced column, netMassInOut = +1.7668e-5 m (net mass enters the ocean; the surface layer thickens), netHeat = -0.0561 degC m, netSalt = +2.74e-3 ppt m, penSW_bnd = (0.09514, 0.03467) degC m, leftover = 0. Pins the surface-layer flux application, one shortwave-law point below the surface (T_after_2 = T_before_2 + dT_2), penSW_total (derived: the sum of the input penSW_bnd bands), the column heat budget dHeat_col and the heat_residual (the two-dump consistency check; the mass and salt column budgets are not pinned, being algebraic identities of the already-pinned layer-1 laws). All derived from the dump identities.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "h_before": [
          2.4871035945487163,
          2.498413302371859,
          2.4984636163347167,
          2.4984896065497355,
          2.9981379217849966,
          2.9980966879360187,
          3.9974456603890887,
          4.996834980969886,
          4.996925641759502,
          4.997076363758009,
          4.997261460140166,
          4.997451603550523,
          4.9976392161912875,
          4.997827909665866,
          4.997961819453403,
          4.99812590238134,
          4.998287502046111,
          4.9985712926683235,
          4.99893991619021,
          4.999504447368247,
          5.000421886054464,
          5.001902035388606,
          5.004310446986138,
          5.0078732437830205,
          5.013355512422344,
          5.021566357896912,
          5.033436801037826,
          5.050373503629741,
          5.074152828013639,
          5.10703361298613,
          5.151861609331785,
          5.212194490720269,
          5.29242817529179,
          5.397950222359949,
          5.535354252486961,
          5.712371007997995,
          5.9387543377285406,
          6.225626131417505,
          6.586407155810753,
          7.036883631868407,
          7.59551415304259,
          8.283847892086692,
          9.126871367179508,
          10.153565885245879,
          11.397161234956846,
          12.895816146652148,
          14.693145091585757,
          16.838789046558368,
          19.38924076886001,
          22.408121074455998,
          25.967525204431027,
          30.147966551781987,
          35.03959585681851,
          40.7440775198378,
          43.74283280420597,
          0.0017593870036773354,
          0.0010000823957908604,
          0.0010000820517989154,
          0.0010000818070983201,
          0.0010000817826533019,
          0.0010000817582120562,
          0.0010000817337736264,
          0.0010000817093365605,
          0.001000081684898762,
          0.0010000816604571403,
          0.0010000816360069532,
          0.0010000816115405726,
          0.0010000815870450247,
          0.0010000815624966947,
          0.001000081537848709,
          0.0010000815129965815,
          0.0010000814876650955,
          0.001000081460873459,
          0.0010000814230470088,
          0.0010000808539779441
        ],
        "T_before": [
          1.6607833811937347,
          1.4928867785164637,
          1.4684280117808186,
          1.4457699507020516,
          1.3065067248204203,
          0.9858443513494252,
          0.7456835312514202,
          0.3296138517526932,
          0.02530065685166574,
          -0.20007147386219362,
          -0.5398081417257311,
          -0.7593826008918697,
          -0.8557235048236405,
          -1.1855228608000106,
          -1.3828957801737443,
          -1.4116866134188633,
          -1.4120319995795054,
          -1.4123103561933346,
          -1.4660242085361896,
          -1.512935264387252,
          -1.5565086084156623,
          -1.5682686222457247,
          -1.5756683301289272,
          -1.5802175633278004,
          -1.5802170555779347,
          -1.5676065745323686,
          -1.555469445366853,
          -1.5554701723088882,
          -1.5554788027980506,
          -1.5554787184955639,
          -1.6219238672791183,
          -1.670419375498139,
          -1.6704259308522633,
          -1.6704268079440694,
          -1.6704358270286706,
          -1.6357788350599085,
          -1.6318597737775915,
          -1.631859150478132,
          -1.6318689720231978,
          -1.6863621026159057,
          -1.6966502716726843,
          -1.69665205434674,
          -1.6945279925292953,
          -1.6933730447769857,
          -1.6957142386058823,
          -1.7196940094939872,
          -1.7465535073562757,
          -1.7666010607949465,
          -1.771353612785282,
          -1.7731994924051775,
          -1.8008021232833415,
          -1.866036353384365,
          -1.8906334228228723,
          -1.864272040983561,
          -1.890786131639456,
          -1.1924599228419959,
          -0.6870049646223689,
          -0.6870001262080228,
          -0.6869934828842448,
          -0.6869934828967081,
          -0.6869934829175333,
          -0.6869934829379427,
          -0.6869934829579367,
          -0.6869934829775136,
          -0.686993482996671,
          -0.6869934830154039,
          -0.6869934830337036,
          -0.6869934830515548,
          -0.686993483068928,
          -0.6869934830857641,
          -0.6869934831019264,
          -0.6869934831170459,
          -0.6869934831298329,
          -0.686993483136793,
          -0.6869934834497631
        ],
        "S_before": [
          33.467472794155434,
          33.45868278951647,
          33.45868315762573,
          33.647646473624114,
          33.74085385026331,
          33.76095785510792,
          33.801681874783725,
          33.85930100009265,
          33.921469810946896,
          33.98568540986409,
          34.033001577669936,
          34.07275873735322,
          34.107414420007956,
          34.124444949432046,
          34.20785598002516,
          34.255129991119475,
          34.25670744894207,
          34.26185903307561,
          34.282960586179016,
          34.308028924129545,
          34.32069171865757,
          34.3309234736942,
          34.3377133502802,
          34.33811339665909,
          34.338655790197464,
          34.342113225850994,
          34.35047943576404,
          34.35720324588949,
          34.36302379535271,
          34.3679378846917,
          34.37195942148805,
          34.375423652203565,
          34.378613011669856,
          34.38153519552919,
          34.38418605765033,
          34.38659228639152,
          34.38894145062746,
          34.39130829135094,
          34.39370601333748,
          34.3961264245905,
          34.3984222892823,
          34.40049135843291,
          34.40237558765785,
          34.40565348565611,
          34.412022487397934,
          34.420343579922445,
          34.42588014062876,
          34.42917063319703,
          34.43340031823423,
          34.437050048704755,
          34.44124652597061,
          34.448510701500076,
          34.45656176705909,
          34.46710372104415,
          34.46652746721304,
          34.57282815214046,
          34.65583635103022,
          34.655837165797884,
          34.65583813259517,
          34.65583813259554,
          34.65583813259512,
          34.6558381325947,
          34.65583813259429,
          34.655838132593885,
          34.655838132593495,
          34.65583813259311,
          34.65583813259274,
          34.65583813259235,
          34.655838132591995,
          34.65583813259164,
          34.65583813259131,
          34.655838132590986,
          34.6558381325907,
          34.65583813259052,
          34.65583813258381
        ],
        "dT": [
          0.024042049907795127,
          0.011017538037460861,
          0.006169153292364449,
          0.0038091656902479176,
          0.002347315104543446,
          0.0014012225641993892,
          0.000778779859042178,
          0.0003666902763789781,
          0.00015699294843318778,
          6.721957987024241e-05,
          2.8780560013319523e-05,
          1.2322217807336777e-05,
          5.275511628766161e-06,
          2.258532908916422e-06,
          9.668878164781347e-07,
          4.1391858229822276e-07,
          1.7719103384550294e-07,
          7.584950889594211e-08,
          3.246685276181438e-08,
          1.3896141348723745e-08,
          1.0395341254465507e-08,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0
        ],
        "netMassIn": 0.0,
        "netMassOut": 1.7668341626516095e-05,
        "netHeat": -0.05614858126133704,
        "netSalt": 0.0027381930275717672,
        "penSW_bnd": [
          0.09513932741670972,
          0.034668981589810605,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0
        ],
        "leftover": 0.0
      },
      "tolerance": {
        "rel": 1e-12
      },
      "assertions": [
        {
          "variable": "h_after",
          "time": 0.0,
          "expected": 2.487121262890343,
          "coords": {
            "layer": 1
          }
        },
        {
          "variable": "T_after",
          "time": 0.0,
          "expected": 1.6622379017406983,
          "coords": {
            "layer": 1
          }
        },
        {
          "variable": "S_after",
          "time": 0.0,
          "expected": 33.468335992229804,
          "coords": {
            "layer": 1
          }
        },
        {
          "variable": "T_after",
          "time": 0.0,
          "expected": 1.5039043165539245,
          "coords": {
            "layer": 2
          }
        },
        {
          "variable": "penSW_total",
          "time": 0.0,
          "expected": 0.12980830900652032
        },
        {
          "variable": "dHeat_col",
          "time": 0.0,
          "expected": 0.07365972774518234
        },
        {
          "variable": "heat_residual",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "abs": 1e-12
          }
        }
      ]
    },
    {
      "id": "bflux_t46800_g3j78",
      "description": "mom6_bflux.csv row (tod, gi, gj) = (46800, 3, 78) with dT and leftover from mom6_sw_abs.csv: the last traced thermo step of column (3, 78), with a strong net mass input netMassInOut = +1.5503e-3 m (h_after_1 ~ 2.523 m), netHeat = -0.1566 degC m, netSalt = +3.43e-3 ppt m, penSW_bnd = (0.07209, 0.02633) degC m, leftover = 0. Pins the surface-layer flux application, one shortwave-law point below the surface (T_after_2 = T_before_2 + dT_2), penSW_total (derived: the sum of the input penSW_bnd bands), the column heat budget dHeat_col and the heat_residual (the two-dump consistency check; the mass and salt column budgets are not pinned, being algebraic identities of the already-pinned layer-1 laws). All derived from the dump identities.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "h_before": [
          2.5212691091429376,
          2.506700628535699,
          2.5046447111833876,
          2.5062768937861706,
          3.006714012018839,
          3.005829484927918,
          4.006308557851199,
          5.005954025222019,
          5.00422688721181,
          5.002569118557452,
          5.001060738807335,
          4.9998171530698166,
          4.99889248728744,
          4.998317384717849,
          4.998350008357129,
          4.998800996943278,
          4.999198452985638,
          4.999556613895338,
          5.000043717602154,
          5.00077234161589,
          5.001859178441709,
          5.003443385402806,
          5.005766060782743,
          5.00934589161691,
          5.014745217021541,
          5.022823788353105,
          5.034507099912024,
          5.051050558092689,
          5.074271921263283,
          5.106522495311029,
          5.150749656578001,
          5.210532818270677,
          5.290260398737687,
          5.395322216370895,
          5.53207303229955,
          5.7088647863919855,
          5.934525764154643,
          6.2206181970101815,
          6.580480036040717,
          7.02977105037616,
          7.586813238238306,
          8.27294820521278,
          9.113201707865802,
          10.13641205428381,
          11.37510852623199,
          12.86796064059754,
          14.659195087245665,
          16.797181057329897,
          19.33724481136997,
          22.340686639031993,
          25.878169347630546,
          30.03274814033474,
          34.905408449476255,
          40.59342080037187,
          47.20548249364946,
          49.46149593735911,
          0.0013925914841605887,
          0.0026997827605034106,
          0.001000033343022122,
          0.0009999609543178039,
          0.0009999636045222348,
          0.0009999628365999845,
          0.0009999621644223662,
          0.00099996160050321,
          0.0009999611589517673,
          0.0009999608441156158,
          0.000999960655452339,
          0.0009999605840044449,
          0.0009999606004607606,
          0.0009999606151065352,
          0.0009999603163430841,
          0.0009999578826198222,
          0.0009999386386523898,
          0.000999943884349607,
          0.0009999916377655014
        ],
        "T_before": [
          1.762542514555966,
          1.950263143461382,
          1.9466089448562778,
          1.9234658809823886,
          1.8694442892857475,
          1.5732223155503646,
          1.2873324488201308,
          0.6604962170677864,
          -0.09916467604449415,
          -0.42312128070924787,
          -0.6932362898680426,
          -0.9361546336442522,
          -1.146275668423427,
          -1.3401475760393913,
          -1.4880647940114433,
          -1.552776823337305,
          -1.5787031973274055,
          -1.589775484370231,
          -1.6145369905987672,
          -1.6324171519781834,
          -1.6434016535930243,
          -1.65600296915712,
          -1.6550512370544674,
          -1.6535016123030344,
          -1.6530813521669763,
          -1.6518297474560586,
          -1.6511809966769586,
          -1.6512295787580595,
          -1.651321695475054,
          -1.6526087766759574,
          -1.6785740736771881,
          -1.7550012526414267,
          -1.7783678734011208,
          -1.7802961360720488,
          -1.778745215268448,
          -1.7680735173027706,
          -1.7542619235502708,
          -1.750822986374503,
          -1.7511436052159672,
          -1.7612463023182712,
          -1.790660758693119,
          -1.8166729325431163,
          -1.833802598290831,
          -1.845043689424842,
          -1.8675865135135434,
          -1.8835485185228709,
          -1.8960575536322544,
          -1.9034947557316493,
          -1.9058796767058308,
          -1.9138964590338479,
          -1.9123081294876825,
          -1.884077288833876,
          -1.8728790760839862,
          -1.8568597237155866,
          -1.871535467008316,
          -1.9349974467267457,
          -1.9191625754113635,
          -1.8516203330582455,
          -1.9191404531797056,
          -1.9191517460965366,
          -1.9191513467681793,
          -1.9191511413241842,
          -1.919150969350331,
          -1.9191510794441302,
          -1.9191511746149261,
          -1.9191512548592882,
          -1.9191513207667528,
          -1.919151373348772,
          -1.9191514139173051,
          -1.9191514439763944,
          -1.919151465132907,
          -1.9191514733781119,
          -1.919151473356855,
          -1.9191514733427015,
          -1.919151473333374
        ],
        "S_before": [
          33.44167819989054,
          33.54063928640922,
          33.58634588412475,
          33.71358126232299,
          33.85911492632293,
          33.94154343396582,
          33.989936981881335,
          34.04848947336631,
          34.12403894836091,
          34.191228526495,
          34.23540743894015,
          34.248470776225396,
          34.25873934879455,
          34.265601876106345,
          34.287818069129926,
          34.32967651374999,
          34.34123021573931,
          34.34573197936246,
          34.35867348673091,
          34.37200386348402,
          34.380084187372105,
          34.38596142912377,
          34.39024248569589,
          34.39091189751434,
          34.39105139531139,
          34.39252974645674,
          34.402087301963476,
          34.412863539336655,
          34.420669406837256,
          34.42598491593632,
          34.42891231923602,
          34.430264392510544,
          34.43114180601676,
          34.432106288583185,
          34.43361676213762,
          34.43498845679914,
          34.436764008646946,
          34.43877269169668,
          34.440790035978225,
          34.44312388043725,
          34.44526758621323,
          34.4467801951212,
          34.44748104576954,
          34.44754076538563,
          34.44725892854526,
          34.44678491039535,
          34.44634623999044,
          34.446084505153074,
          34.44603283177568,
          34.450146442583126,
          34.454826928839026,
          34.458619030408315,
          34.464359455535956,
          34.472431070386776,
          34.47692053375624,
          34.47711358308868,
          34.48065950133954,
          34.49278249624165,
          34.48028100348453,
          34.480278248429585,
          34.48027834586178,
          34.48027838258718,
          34.48027841289698,
          34.48027838602874,
          34.48027836280376,
          34.48027834322112,
          34.480278327136986,
          34.48027831430458,
          34.480278304403775,
          34.480278297067564,
          34.480278291903886,
          34.48027828989087,
          34.48027828989519,
          34.48027828989805,
          34.48027828989995
        ],
        "dT": [
          0.017964190388767287,
          0.008223441170839285,
          0.00463795119340471,
          0.002885987862598194,
          0.001793095004443357,
          0.0010801579890651336,
          0.0006066211874449223,
          0.00028954372481260204,
          0.00012594224821553535,
          5.480156383252943e-05,
          2.3852260367163147e-05,
          1.0384051266409955e-05,
          4.5215151032174106e-06,
          1.9690513330949955e-06,
          8.575366439167453e-07,
          3.7345041059566597e-07,
          1.6262312074744045e-07,
          7.081155950494633e-08,
          3.083160549088859e-08,
          1.3422871036894435e-08,
          1.0346090428825505e-08,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0
        ],
        "netMassIn": 0.0,
        "netMassOut": 0.001550287719108293,
        "netHeat": -0.15655216496106295,
        "netSalt": 0.003427970462530352,
        "penSW_bnd": [
          0.07208731785815417,
          0.02632978349980929,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0
        ],
        "leftover": 0.0
      },
      "tolerance": {
        "rel": 1e-12
      },
      "assertions": [
        {
          "variable": "h_after",
          "time": 0.0,
          "expected": 2.522819396862046,
          "coords": {
            "layer": 1
          }
        },
        {
          "variable": "T_after",
          "time": 0.0,
          "expected": 1.7173691639959405,
          "coords": {
            "layer": 1
          }
        },
        {
          "variable": "S_after",
          "time": 0.0,
          "expected": 33.42248687267252,
          "coords": {
            "layer": 1
          }
        },
        {
          "variable": "T_after",
          "time": 0.0,
          "expected": 1.9584865846322213,
          "coords": {
            "layer": 2
          }
        },
        {
          "variable": "penSW_total",
          "time": 0.0,
          "expected": 0.09841710135796346
        },
        {
          "variable": "dHeat_col",
          "time": 0.0,
          "expected": -0.058135063603091675
        },
        {
          "variable": "heat_residual",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "abs": 1e-12
          }
        }
      ]
    },
    {
      "id": "bflux_t46800_g4j78",
      "description": "mom6_bflux.csv row (tod, gi, gj) = (46800, 4, 78) with dT and leftover from mom6_sw_abs.csv: the last traced thermo step of column (4, 78), the strongest traced mass input netMassInOut = +1.9698e-3 m, netHeat = -0.1831 degC m, netSalt = +3.48e-3 ppt m, penSW_bnd = (0.05782, 0.02105) degC m, leftover = 0. Pins the surface-layer flux application, one shortwave-law point below the surface (T_after_2 = T_before_2 + dT_2), penSW_total (derived: the sum of the input penSW_bnd bands), the column heat budget dHeat_col and the heat_residual (the two-dump consistency check; the mass and salt column budgets are not pinned, being algebraic identities of the already-pinned layer-1 laws). All derived from the dump identities.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "h_before": [
          2.5019417642335613,
          2.4959742794121995,
          2.495670324545963,
          2.4929609142619484,
          2.9915809853577056,
          2.9916293745703997,
          3.9889421834882697,
          4.986133195151644,
          4.985847108080284,
          4.985584360227782,
          4.98541032909137,
          4.985315237801663,
          4.985260339936663,
          4.9851642170242565,
          4.984916665864474,
          4.984688555878565,
          4.9846570054608454,
          4.984730620099254,
          4.984848618889171,
          4.9851476995873965,
          4.985846280359379,
          4.987161664536952,
          4.989377101319105,
          4.992936160008591,
          4.998365789765222,
          5.006381722409909,
          5.018095225262815,
          5.034881983964966,
          5.058510902444875,
          5.0912223371630425,
          5.135835958557184,
          5.1959054862736505,
          5.275823600394229,
          5.380936665613926,
          5.517828546354955,
          5.694295155392619,
          5.919868830149706,
          6.2057589980052255,
          6.5653239376780865,
          7.014278479247179,
          7.57106088692975,
          8.257184873673523,
          9.097441207297274,
          10.120620293788088,
          11.360187886992614,
          12.854024563103364,
          14.644082340691918,
          16.782032773745943,
          19.322734606112558,
          22.331600461903513,
          4.5162119703716606,
          0.003339111253604374,
          0.003655049034751263,
          0.0037046227593623567,
          0.0025214456126846346,
          0.0019475231077281008,
          0.0010000570271603835,
          0.0010000483442089072,
          0.001000048387182655,
          0.0010000483820025979,
          0.0010000482771033152,
          0.0010000481533284145,
          0.001000048008496809,
          0.00100004783950971,
          0.001000047639021993,
          0.0010000474009517536,
          0.0010000471202540667,
          0.001000046797441448,
          0.0010000464520942532,
          0.001000046167369912,
          0.0010000462616018518,
          0.0010000486391828524,
          0.0010000690956889014,
          0.0010000671799731062,
          0.0010000104313717096
        ],
        "T_before": [
          1.331002337113528,
          1.565354399426177,
          1.539959824602991,
          1.4129620429514536,
          1.1929438024709074,
          0.8957328800953109,
          0.6676493637069735,
          0.015641446665296502,
          -0.5550456243354069,
          -0.7613432471918238,
          -1.0627736566343295,
          -1.2764137352688196,
          -1.4282865394513924,
          -1.592946578678669,
          -1.7011514788373152,
          -1.7217231326176599,
          -1.7284810266895159,
          -1.7275520111222071,
          -1.745169614620584,
          -1.77506365674107,
          -1.7970464817999279,
          -1.8055521803568186,
          -1.8186335687060442,
          -1.8188982532161955,
          -1.8188854168131312,
          -1.8129522788507348,
          -1.8059874597702437,
          -1.80577614385602,
          -1.8060051441175946,
          -1.8120973016911028,
          -1.8833760605742462,
          -1.9219175677346083,
          -1.9232395615903883,
          -1.9172789084958561,
          -1.8905573082804397,
          -1.8900154113892436,
          -1.8595466419732694,
          -1.8568370774373237,
          -1.8592833374539057,
          -1.8765072695642173,
          -1.8796387805628152,
          -1.8788794730056506,
          -1.8716524701421664,
          -1.8568652358814381,
          -1.8481091916260637,
          -1.8447579673743284,
          -1.8502906574162787,
          -1.8569106377284792,
          -1.849652371299967,
          -1.8473411735256375,
          -1.8495120162343597,
          -1.8760932114896174,
          -1.868595958337488,
          -1.856951055065126,
          -1.866099815191199,
          -1.8955500053012408,
          -1.8587173574206248,
          -1.8587162602012104,
          -1.8587156143358103,
          -1.8587168709722321,
          -1.8587168648428685,
          -1.8587168576046214,
          -1.858716849126621,
          -1.8587168392414914,
          -1.858716827507692,
          -1.8587168135787266,
          -1.8587167971759817,
          -1.858716778356314,
          -1.858716758316845,
          -1.8587167420386133,
          -1.8587167485604907,
          -1.858716891884446,
          -1.858718113461187,
          -1.8587180490376722,
          -1.8587147235465304
        ],
        "S_before": [
          33.25068021800728,
          33.36136529813153,
          33.42552572121672,
          33.599578936252485,
          33.72508261808859,
          33.790242078770014,
          33.85112415791008,
          33.93626173904326,
          34.02775611814323,
          34.10685291327242,
          34.159224595984696,
          34.18651413862956,
          34.2123903815066,
          34.23549366108862,
          34.28917854201348,
          34.3342510906401,
          34.33900274623079,
          34.34265681879174,
          34.35672403795307,
          34.371170748678246,
          34.37858778730896,
          34.38148358119862,
          34.381890742573,
          34.38190726621457,
          34.38193761298996,
          34.38302135606971,
          34.38634358905126,
          34.38982316258889,
          34.39382263670373,
          34.39831031697109,
          34.40327088349123,
          34.407945933457654,
          34.41187884960678,
          34.41537877325846,
          34.418182153280625,
          34.41821702602994,
          34.42072071933806,
          34.42205613697008,
          34.42327346496727,
          34.42439100024259,
          34.425352439435166,
          34.42624610657877,
          34.4270606288018,
          34.42863904600305,
          34.43195362325228,
          34.435526022149006,
          34.43656339183549,
          34.43689230813761,
          34.43792498083835,
          34.44490827249451,
          34.453553942506126,
          34.45810579205951,
          34.46232057028396,
          34.46824112418593,
          34.46898531721965,
          34.46674046744665,
          34.456912605806096,
          34.45691265048851,
          34.45691284632632,
          34.456912423027504,
          34.45691242083383,
          34.45691241823189,
          34.45691241518245,
          34.45691241162417,
          34.45691240740457,
          34.45691240240223,
          34.45691239652431,
          34.45691238981049,
          34.45691238273761,
          34.45691237720553,
          34.45691238040464,
          34.45691243547691,
          34.45691289506276,
          34.45691283760106,
          34.45691164210969
        ],
        "dT": [
          0.014641412874602855,
          0.0066840445288529615,
          0.0037354977731316463,
          0.002299533758622241,
          0.0014119602676823106,
          0.0008393467307045155,
          0.00046425901794955315,
          0.00021724704434111092,
          9.235788508210607e-05,
          3.9269793800422725e-05,
          1.6697828523870584e-05,
          7.100220090539011e-06,
          3.01918289880021e-06,
          1.2838445555551914e-06,
          5.459432130816566e-07,
          2.3216690858696154e-07,
          9.873334905208253e-08,
          4.1988117427393945e-08,
          1.7855911860209517e-08,
          1.3210895932758149e-08,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0
        ],
        "netMassIn": 0.0,
        "netMassOut": 0.001969816806741289,
        "netHeat": -0.18312218837928051,
        "netSalt": 0.0034810525892703986,
        "penSW_bnd": [
          0.057824396189544075,
          0.021046056116244414,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0
        ],
        "leftover": 0.0
      },
      "tolerance": {
        "rel": 1e-12
      },
      "assertions": [
        {
          "variable": "h_after",
          "time": 0.0,
          "expected": 2.5039115810403025,
          "coords": {
            "layer": 1
          }
        },
        {
          "variable": "T_after",
          "time": 0.0,
          "expected": 1.2714622091704764,
          "coords": {
            "layer": 1
          }
        },
        {
          "variable": "S_after",
          "time": 0.0,
          "expected": 33.2259122922509,
          "coords": {
            "layer": 1
          }
        },
        {
          "variable": "T_after",
          "time": 0.0,
          "expected": 1.5720384439550297,
          "coords": {
            "layer": 2
          }
        },
        {
          "variable": "penSW_total",
          "time": 0.0,
          "expected": 0.07887045230578849
        },
        {
          "variable": "dHeat_col",
          "time": 0.0,
          "expected": -0.10425173607349271
        },
        {
          "variable": "heat_residual",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "abs": 1e-12
          }
        }
      ]
    }
  ]
}
```

</details>
