---
title: "IceGridFractions"
slug: "icegridfractions"
domains: ["coupler"]
component_types: ["model"]
subdomains: ["cmeps"]
domain: "coupler"
subdomain: "cmeps"
component_type: "model"
esm_version: "1.3.0"
esm_path: "components/coupler/cmeps/cmeps_fractions.esm"
reference: "https://github.com/ESCOMP/CESM"
description: "The surface fractions of the CMEPS mediator (med_fraction_set of mediator/med_fraction_mod.F90:774-954 plus the init-time fields of med_fraction_init, called from med_phases_post_ice) as transcribed from the M8 stage-1 dump (cmeps_fractions_*.csv of the C_JRA_t62_inst run 12446243 and the F2000climo_f19_inst rerun of 2026-11-17, fork cmeps 5e41b8ee/b548fa7c/17545715).  The per-grid laws: on the ICE grid (F90:851-856) ifrac = Si_ifrac*Si_imask and ofrac = Si_imask - ifrac with Si_ifrac the time-evolving ice export and Si_imask the constant ice domain mask (the gx1v7 ocean mask mapped onto the f19 grid in the F2000climo case takes PARTIAL values on coastal cells, so the product law is exercised non-degenerately there); the OCN grid bundle is the mapfcopy redistribution of the ice-grid fractions (F90:866-881) - in the traced configurations the ice and ocean grids are the same mesh (tx2_3v2 in C_JRA, fv1.9x2.5 in F2000), so every same-mesh map is the identity at the same global element (verified grid-wide from the cpl restarts, 0 diffs), and the two fraction maps are modeled through the single EarthSciDiscretizations conservative_overlap_apply template imported by reference (${ESD_ROOT}/regridding/conservative_overlap.esm) with the identity weights carried as data - the same map law as the cmeps_map component, one template for every ESMF routehandle; the ATM grid bundle (F90:900-929) is the ice->atm mapped ifrac, the ice->atm mapped ofrac (gated on the ocn->atm coupling; the source is the ice-grid ofrac) and aofrac = Sa_ofrac of FBImp(compatm,compatm) (F90:928), plus the init-time lfrac (the truncated residual 1 - ofrac of F90:455-481 with the |x| < 1.0e-3 truncation - NOT dumped, so lfrac is carried as DATA from the dump column, a documented gap: the init-time ofrac is not traced) and lfrin (the lnd->atm mapped lfrin of F90:421-448, = the lnd-grid Sl_lfrin at the same gid in the traced configuration); the LND grid bundle is the pure copy lfrac = lfrin = Sl_lfrin of F90:294-309 (the land model's own mask export, pinned by the stage-1 validator only: a copy law admits no failable stage-2 pin).  The models: IceGridFractions evaluates the product laws pointwise; OcnGridFractions and AtmGridFractions evaluate the identity maps on the 1x1 traced subdomain (NSRC = NTGT = 1, the single traced cell of each test; the weights-as-data treatment is the cmeps_map precedent); LndGridFractions carries the copy equations.  The fail-able cross-check of the component is the partition of unity on the ATM grid, pou = lfrac + ifrac + ofrac == 1 (asserted in every atm test; it fails if the data lfrac, pinned from the dump, does not tile with the mapped fractions - the traced F2000 rows sum to 1.0 exactly).  Configuration facts (verified by stage1/analysis/check_cmeps_fractions.py and asserted by stage1/analysis/extract_cmeps_fraction_test_rows.py on ALL dumped rows): the C_JRA atm bundle is identically zero (DATM run sequence: no MED->ATM connector, the atm fraction maps of F90:900-921 are gated off by the med_coupling_active checks); the C_JRA ocn traced cells are fully masked (So_omask = 1, the SICE mask is 1 there, so ofrac + ifrac = 1 on every row) and the mapped ice export Si_ifrac(step k) == ifrac(step k-1) bit-exactly (the mapfcopy redist maps PET-0-local index n of the ice grid to the same n of the ocn grid; the mapped Si_imask column holds the bundle reset 0.0 because Si_imask is not in the ice->ocn packed map list of this configuration); the F2000 atm lfrac/lfrin/aofrac/Sa_ofrac are constant across steps (init-time) with lfrin == lfrac on every traced cell and aofrac == Sa_ofrac == 0 (CAM does not export Sa_ofrac here); the F2000 ice Si_imask takes 5 distinct values 0.114..1.0 on the traced window (the non-degenerate product law).  The pinned rows: the F2000 ice rows (5 tests, partial mask everywhere: ifrac = Si_ifrac*Si_imask is never a copy of an input, and the step-6/step-12 rows cover the cells that enter the traced set as the ice edge moves and the time evolution of Si_ifrac), the C_JRA ocn rows (7 tests: first/mid/last traced cells at steps 1, 2, 12, 24 plus the min/max ifrac rows; the identity-map pins fail on any wrong map law or weight), and the F2000 atm rows (4 tests: the partial-land AND partial-ice cell n = 6 at steps 1 and 6 - the only cell of the window where lfrac, ifrac and ofrac are all partial, so every pin can fail and the partition-of-unity pin cross-checks the data lfrac - plus the north-pole cell gid 13753 at step 12, whose ifrac 0.99875 the wrong 0edaae42 recorder read as 0 (the bug the recorder fix removed), and the smallest partial-ice ocean cell of step 12).  The lfrin pin is dropped on the pure-ocean rows (lfrin = Sl_lfrin = 0 there: a copy of a zero input cannot fail) and the aofrac pin is dropped everywhere (aofrac = Sa_ofrac = 0 in this configuration; the equation is the law, the pin would be unfailable).  All overrides and expected values are raw dump columns at rel 1e-12 (abs 0.0); the stage-1 replay is bit-exact and the engine's summation slack on the 1-term maps is zero, so the pins hold exactly."
tags: ["coupler", "cmeps", "model", "fractions", "cesm"]
---

## Description

The surface fractions of the CMEPS mediator (med_fraction_set of mediator/med_fraction_mod.F90:774-954 plus the init-time fields of med_fraction_init, called from med_phases_post_ice) as transcribed from the M8 stage-1 dump (cmeps_fractions_*.csv of the C_JRA_t62_inst run 12446243 and the F2000climo_f19_inst rerun of 2026-11-17, fork cmeps 5e41b8ee/b548fa7c/17545715).  The per-grid laws: on the ICE grid (F90:851-856) ifrac = Si_ifrac*Si_imask and ofrac = Si_imask - ifrac with Si_ifrac the time-evolving ice export and Si_imask the constant ice domain mask (the gx1v7 ocean mask mapped onto the f19 grid in the F2000climo case takes PARTIAL values on coastal cells, so the product law is exercised non-degenerately there); the OCN grid bundle is the mapfcopy redistribution of the ice-grid fractions (F90:866-881) - in the traced configurations the ice and ocean grids are the same mesh (tx2_3v2 in C_JRA, fv1.9x2.5 in F2000), so every same-mesh map is the identity at the same global element (verified grid-wide from the cpl restarts, 0 diffs), and the two fraction maps are modeled through the single EarthSciDiscretizations conservative_overlap_apply template imported by reference (${ESD_ROOT}/regridding/conservative_overlap.esm) with the identity weights carried as data - the same map law as the cmeps_map component, one template for every ESMF routehandle; the ATM grid bundle (F90:900-929) is the ice->atm mapped ifrac, the ice->atm mapped ofrac (gated on the ocn->atm coupling; the source is the ice-grid ofrac) and aofrac = Sa_ofrac of FBImp(compatm,compatm) (F90:928), plus the init-time lfrac (the truncated residual 1 - ofrac of F90:455-481 with the |x| < 1.0e-3 truncation - NOT dumped, so lfrac is carried as DATA from the dump column, a documented gap: the init-time ofrac is not traced) and lfrin (the lnd->atm mapped lfrin of F90:421-448, = the lnd-grid Sl_lfrin at the same gid in the traced configuration); the LND grid bundle is the pure copy lfrac = lfrin = Sl_lfrin of F90:294-309 (the land model's own mask export, pinned by the stage-1 validator only: a copy law admits no failable stage-2 pin).  The models: IceGridFractions evaluates the product laws pointwise; OcnGridFractions and AtmGridFractions evaluate the identity maps on the 1x1 traced subdomain (NSRC = NTGT = 1, the single traced cell of each test; the weights-as-data treatment is the cmeps_map precedent); LndGridFractions carries the copy equations.  The fail-able cross-check of the component is the partition of unity on the ATM grid, pou = lfrac + ifrac + ofrac == 1 (asserted in every atm test; it fails if the data lfrac, pinned from the dump, does not tile with the mapped fractions - the traced F2000 rows sum to 1.0 exactly).  Configuration facts (verified by stage1/analysis/check_cmeps_fractions.py and asserted by stage1/analysis/extract_cmeps_fraction_test_rows.py on ALL dumped rows): the C_JRA atm bundle is identically zero (DATM run sequence: no MED->ATM connector, the atm fraction maps of F90:900-921 are gated off by the med_coupling_active checks); the C_JRA ocn traced cells are fully masked (So_omask = 1, the SICE mask is 1 there, so ofrac + ifrac = 1 on every row) and the mapped ice export Si_ifrac(step k) == ifrac(step k-1) bit-exactly (the mapfcopy redist maps PET-0-local index n of the ice grid to the same n of the ocn grid; the mapped Si_imask column holds the bundle reset 0.0 because Si_imask is not in the ice->ocn packed map list of this configuration); the F2000 atm lfrac/lfrin/aofrac/Sa_ofrac are constant across steps (init-time) with lfrin == lfrac on every traced cell and aofrac == Sa_ofrac == 0 (CAM does not export Sa_ofrac here); the F2000 ice Si_imask takes 5 distinct values 0.114..1.0 on the traced window (the non-degenerate product law).  The pinned rows: the F2000 ice rows (5 tests, partial mask everywhere: ifrac = Si_ifrac*Si_imask is never a copy of an input, and the step-6/step-12 rows cover the cells that enter the traced set as the ice edge moves and the time evolution of Si_ifrac), the C_JRA ocn rows (7 tests: first/mid/last traced cells at steps 1, 2, 12, 24 plus the min/max ifrac rows; the identity-map pins fail on any wrong map law or weight), and the F2000 atm rows (4 tests: the partial-land AND partial-ice cell n = 6 at steps 1 and 6 - the only cell of the window where lfrac, ifrac and ofrac are all partial, so every pin can fail and the partition-of-unity pin cross-checks the data lfrac - plus the north-pole cell gid 13753 at step 12, whose ifrac 0.99875 the wrong 0edaae42 recorder read as 0 (the bug the recorder fix removed), and the smallest partial-ice ocean cell of step 12).  The lfrin pin is dropped on the pure-ocean rows (lfrin = Sl_lfrin = 0 there: a copy of a zero input cannot fail) and the aofrac pin is dropped everywhere (aofrac = Sa_ofrac = 0 in this configuration; the equation is the law, the pin would be unfailable).  All overrides and expected values are raw dump columns at rel 1e-12 (abs 0.0); the stage-1 replay is bit-exact and the engine's summation slack on the 1-term maps is zero, so the pins hold exactly.

## Reference

- CESM (Community Earth System Model), ESCOMP/CESM: CMEPS (Coupled Mediator for Earth System Prediction) source (cesm3.0-alphabranch) - flux_atmocn/flux_atmocn_Large.F90, share/src/shr_wv_sat_mod.F90, share/src/shr_orb_mod.F90, mediator/med_phases_aofluxes_mod.F90, mediator/med_phases_ocnalb_mod.F90, mediator/med_phases_prep_ocn_mod.F90, mediator/med_phases_prep_atm_mod.F90, mediator/med_merge_mod.F90, mediator/esmFldsExchange_cesm_mod.F90 - the reference implementation these components are transcribed from.
- EarthSciModels - the authoritative .esm corpus this component lives in.

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `Si_ifrac` | `1` | `0.053999547086316865` | the time-evolving ice fraction export of the ice model (FBImp(compice,compice) Si_ifrac; the F2000 rerun's CICE value on the traced ice-grid cell, dump column Si_ifrac; the default is the step-1 value of the first test, overridden per test), [-] |
| `Si_imask` | `1` | `0.4818725776652769` | the constant ice domain mask (FBImp(compice,compice) Si_imask, the gx1v7 ocean mask mapped onto the f19 grid: 0 on land, 1 on the open ocean, PARTIAL on coastal cells - the dump's traced window holds 5 distinct values 0.114..1.0, so the product law below is exercised non-degenerately; the default is the step-1 value of the first test, overridden per test), [-] |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `ifrac` | `1` | `0.0` | the ice-covered fraction of the ice grid (FBFrac(compice) ifrac, F90:851): ifrac = Si_ifrac*Si_imask, [-] |
| `ofrac` | `1` | `0.0` | the open-ocean fraction of the ice grid (FBFrac(compice) ofrac, F90:856): ofrac = Si_imask - ifrac, the complement of ifrac within the ice domain mask, [-] |

## Observed expressions

$$
ifrac = Si_{ifrac} \cdot Si_{imask}
$$
_the ice-covered fraction of the ice grid (FBFrac(compice) ifrac, F90:851): ifrac = Si_ifrac*Si_imask, [-]_

$$
ofrac = Si_{imask} - ifrac
$$
_the open-ocean fraction of the ice grid (FBFrac(compice) ofrac, F90:856): ofrac = Si_imask - ifrac, the complement of ifrac within the ice domain mask, [-]_

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "variables": {
    "Si_ifrac": {
      "type": "parameter",
      "units": "1",
      "default": 0.053999547086316865,
      "description": "the time-evolving ice fraction export of the ice model (FBImp(compice,compice) Si_ifrac; the F2000 rerun's CICE value on the traced ice-grid cell, dump column Si_ifrac; the default is the step-1 value of the first test, overridden per test), [-]"
    },
    "Si_imask": {
      "type": "parameter",
      "units": "1",
      "default": 0.4818725776652769,
      "description": "the constant ice domain mask (FBImp(compice,compice) Si_imask, the gx1v7 ocean mask mapped onto the f19 grid: 0 on land, 1 on the open ocean, PARTIAL on coastal cells - the dump's traced window holds 5 distinct values 0.114..1.0, so the product law below is exercised non-degenerately; the default is the step-1 value of the first test, overridden per test), [-]"
    },
    "ifrac": {
      "type": "unknown",
      "units": "1",
      "default": 0.0,
      "description": "the ice-covered fraction of the ice grid (FBFrac(compice) ifrac, F90:851): ifrac = Si_ifrac*Si_imask, [-]"
    },
    "ofrac": {
      "type": "unknown",
      "units": "1",
      "default": 0.0,
      "description": "the open-ocean fraction of the ice grid (FBFrac(compice) ofrac, F90:856): ofrac = Si_imask - ifrac, the complement of ifrac within the ice domain mask, [-]"
    }
  },
  "equations": [
    {
      "lhs": "ifrac",
      "rhs": {
        "op": "*",
        "args": [
          "Si_ifrac",
          "Si_imask"
        ]
      }
    },
    {
      "lhs": "ofrac",
      "rhs": {
        "op": "-",
        "args": [
          "Si_imask",
          "ifrac"
        ]
      }
    }
  ],
  "tests": [
    {
      "id": "step1_first_cell",
      "description": "Instantaneous pin of the ice-grid fraction laws (med_fraction_mod.F90:851-856) from stage1/dumps/cmeps/cmeps_fractions_f2000_ice.csv: row (step 1, gid 11528, ice cell n = 328, lat 61.579 deg, lon 17.5 deg).  Partial mask: Si_imask = 0.48187 (a coastal cell of the gx1v7 mask mapped onto f19), Si_ifrac = 0.05400, so ifrac = 0.02602 = Si_ifrac*Si_imask is a NON-degenerate product (a pin on a fully-masked row would be a copy of the Si_ifrac input and could not fail).  time_span {0,0} evaluates the pointwise laws at the dumped inputs; the outputs are asserted at dump precision, rel 1e-12 (abs 0.0).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "Si_ifrac": 0.053999547086316865,
        "Si_imask": 0.4818725776652769
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 0.0
      },
      "assertions": [
        {
          "variable": "ifrac",
          "time": 0.0,
          "expected": 0.026020900947241
        },
        {
          "variable": "ofrac",
          "time": 0.0,
          "expected": 0.4558516767180359
        }
      ]
    },
    {
      "id": "step1_min_mask",
      "description": "Instantaneous pin of the ice-grid fraction laws (med_fraction_mod.F90:851-856) from stage1/dumps/cmeps/cmeps_fractions_f2000_ice.csv: row (step 1, gid 11672, ice cell n = 336, lat 63.474 deg, lon 17.5 deg).  The smallest partial mask of the window: Si_imask = 0.11447, Si_ifrac = 0.08604, ifrac = 0.00985 - the strongest-teeth product-law pin (both factors partial, the product differs from both inputs).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "Si_ifrac": 0.08603887930600053,
        "Si_imask": 0.11446510269413157
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 0.0
      },
      "assertions": [
        {
          "variable": "ifrac",
          "time": 0.0,
          "expected": 0.009848449155449343
        },
        {
          "variable": "ofrac",
          "time": 0.0,
          "expected": 0.10461665353868223
        }
      ]
    },
    {
      "id": "step6_cell360",
      "description": "Instantaneous pin of the ice-grid fraction laws (med_fraction_mod.F90:851-856) from stage1/dumps/cmeps/cmeps_fractions_f2000_ice.csv: row (step 6, gid 12104, ice cell n = 360, lat 69.158 deg, lon 17.5 deg).  This cell ENTERS the traced set at step 6 (the per-step partial-ice selection changes as the ice edge moves - the same 25-cell count, with cells 360/384 swapping; the dynamic selection is a documented dump property, verified by the stage-1 validator).  Tiny partial ice: Si_ifrac = 1.1521e-4, Si_imask = 0.40149, ifrac = 4.6255e-5.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "Si_ifrac": 0.00011520786961961155,
        "Si_imask": 0.40149481043130375
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 0.0
      },
      "assertions": [
        {
          "variable": "ifrac",
          "time": 0.0,
          "expected": 4.6255361773120294e-05
        },
        {
          "variable": "ofrac",
          "time": 0.0,
          "expected": 0.40144855506953064
        }
      ]
    },
    {
      "id": "step12_max_ifrac",
      "description": "Instantaneous pin of the ice-grid fraction laws (med_fraction_mod.F90:851-856) from stage1/dumps/cmeps/cmeps_fractions_f2000_ice.csv: row (step 12, gid 11528, ice cell n = 328, lat 61.579 deg, lon 17.5 deg).  The same cell as step1_first_cell at the last step - the time evolution of the runtime input: Si_ifrac grew 0.05400 -> 0.05484 over the window (Si_imask constant), ifrac = 0.02642.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "Si_ifrac": 0.05483728282025925,
        "Si_imask": 0.4818725776652769
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 0.0
      },
      "assertions": [
        {
          "variable": "ifrac",
          "time": 0.0,
          "expected": 0.026424582824758132
        },
        {
          "variable": "ofrac",
          "time": 0.0,
          "expected": 0.4554479948405188
        }
      ]
    },
    {
      "id": "step12_last_cell",
      "description": "Instantaneous pin of the ice-grid fraction laws (med_fraction_mod.F90:851-856) from stage1/dumps/cmeps/cmeps_fractions_f2000_ice.csv: row (step 12, gid 12104, ice cell n = 360, lat 69.158 deg, lon 17.5 deg).  Cell 360 at the last step: Si_ifrac doubled since step 6 (1.1521e-4 -> 2.3042e-4), ifrac = 9.2511e-5.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "Si_ifrac": 0.0002304157392392231,
        "Si_imask": 0.40149481043130375
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 0.0
      },
      "assertions": [
        {
          "variable": "ifrac",
          "time": 0.0,
          "expected": 9.251072354624059e-05
        },
        {
          "variable": "ofrac",
          "time": 0.0,
          "expected": 0.40140229970775754
        }
      ]
    }
  ]
}
```

</details>
