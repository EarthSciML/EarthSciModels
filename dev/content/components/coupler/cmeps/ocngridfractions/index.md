---
title: "OcnGridFractions"
slug: "ocngridfractions"
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
| `w_ij` | `1` | `[[1.0]]` | the mapfcopy routehandle weights of the traced subdomain (the ice->ocn redistribution of F90:866-881; the ice and ocean grids are the same mesh in the traced C_JRA configuration - tx2_3v2 - so the redist is the identity at the same global element, verified grid-wide from the cpl restart: ocnFrac == iceFrac at 0 diffs over all 259200 cells; the identity matrix is carried as data exactly like the cmeps_map weights), [1] |
| `A_j` | `1` | `[1.0]` | the row-sum normalization of the same routehandle (field_normOne = 1.0 for the mapfcopy redist), [1] |
| `atol` | `1` | `0.0` | sliver filter of conservative_overlap_apply (w_ij > atol); 0 keeps the diagonal weight 1.0 and drops nothing else on the 1x1 subdomain, [1] |
| `ifrac_ice` | `1` | `[0.4692451250438887]` | the ice-grid ice-covered fraction at the traced cell (FBFrac(compice) ifrac, = the ocn-grid value at the same gid through the same-mesh redist identity; the C_JRA ocn dump does not carry the ice-grid columns, so the test overrides are the dump's ocn-grid ifrac values - bit-identical to the ice-grid values, verified grid-wide), [1] |
| `ofrac_ice` | `1` | `[0.5307548749561113]` | the ice-grid open-ocean fraction at the traced cell (FBFrac(compice) ofrac, = the ocn-grid value at the same gid through the same-mesh redist identity; overrides are the dump's ocn-grid ofrac values as for ifrac_ice), [1] |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `ifrac` | `1` | `[0.0]` | the ice-covered fraction of the ocean grid (FBFrac(compocn) ifrac): the mapfcopy redistribution of the ice-grid ifrac (F90:866-881), dst_j = (sum_i w_ij x_i)/A_j over the w_ij > atol set - the identity map in the traced configuration, [1] |
| `ofrac` | `1` | `[0.0]` | the open-ocean fraction of the ocean grid (FBFrac(compocn) ofrac): the mapfcopy redistribution of the ice-grid ofrac (F90:866-881) - the identity map in the traced configuration, [1] |

## Observed expressions

$$
ifrac = \mathrm{conservative_overlap_apply}\left(A_{ij}=w_{ij}, A_{j}=A_{j}, F_{src}=ifrac_{ice}, atol=atol\right)
$$
_the ice-covered fraction of the ocean grid (FBFrac(compocn) ifrac): the mapfcopy redistribution of the ice-grid ifrac (F90:866-881), dst_j = (sum_i w_ij x_i)/A_j over the w_ij > atol set - the identity map in the traced configuration, [1]_

$$
ofrac = \mathrm{conservative_overlap_apply}\left(A_{ij}=w_{ij}, A_{j}=A_{j}, F_{src}=ofrac_{ice}, atol=atol\right)
$$
_the open-ocean fraction of the ocean grid (FBFrac(compocn) ofrac): the mapfcopy redistribution of the ice-grid ofrac (F90:866-881) - the identity map in the traced configuration, [1]_

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "expression_template_imports": [
    {
      "ref": "${ESD_ROOT}/regridding/conservative_overlap.esm",
      "only": [
        "conservative_overlap_apply"
      ],
      "bindings": {
        "NSRC": "NSRC",
        "NTGT": "NTGT",
        "NVERT": "NVERT"
      }
    }
  ],
  "variables": {
    "w_ij": {
      "type": "parameter",
      "units": "1",
      "default": [
        [
          1.0
        ]
      ],
      "description": "the mapfcopy routehandle weights of the traced subdomain (the ice->ocn redistribution of F90:866-881; the ice and ocean grids are the same mesh in the traced C_JRA configuration - tx2_3v2 - so the redist is the identity at the same global element, verified grid-wide from the cpl restart: ocnFrac == iceFrac at 0 diffs over all 259200 cells; the identity matrix is carried as data exactly like the cmeps_map weights), [1]",
      "shape": [
        "src_cells",
        "tgt_cells"
      ]
    },
    "A_j": {
      "type": "parameter",
      "units": "1",
      "default": [
        1.0
      ],
      "description": "the row-sum normalization of the same routehandle (field_normOne = 1.0 for the mapfcopy redist), [1]",
      "shape": [
        "tgt_cells"
      ]
    },
    "atol": {
      "type": "parameter",
      "units": "1",
      "default": 0.0,
      "description": "sliver filter of conservative_overlap_apply (w_ij > atol); 0 keeps the diagonal weight 1.0 and drops nothing else on the 1x1 subdomain, [1]"
    },
    "ifrac_ice": {
      "type": "parameter",
      "units": "1",
      "default": [
        0.4692451250438887
      ],
      "description": "the ice-grid ice-covered fraction at the traced cell (FBFrac(compice) ifrac, = the ocn-grid value at the same gid through the same-mesh redist identity; the C_JRA ocn dump does not carry the ice-grid columns, so the test overrides are the dump's ocn-grid ifrac values - bit-identical to the ice-grid values, verified grid-wide), [1]",
      "shape": [
        "src_cells"
      ]
    },
    "ofrac_ice": {
      "type": "parameter",
      "units": "1",
      "default": [
        0.5307548749561113
      ],
      "description": "the ice-grid open-ocean fraction at the traced cell (FBFrac(compice) ofrac, = the ocn-grid value at the same gid through the same-mesh redist identity; overrides are the dump's ocn-grid ofrac values as for ifrac_ice), [1]",
      "shape": [
        "src_cells"
      ]
    },
    "ifrac": {
      "type": "unknown",
      "units": "1",
      "default": [
        0.0
      ],
      "description": "the ice-covered fraction of the ocean grid (FBFrac(compocn) ifrac): the mapfcopy redistribution of the ice-grid ifrac (F90:866-881), dst_j = (sum_i w_ij x_i)/A_j over the w_ij > atol set - the identity map in the traced configuration, [1]",
      "shape": [
        "tgt_cells"
      ]
    },
    "ofrac": {
      "type": "unknown",
      "units": "1",
      "default": [
        0.0
      ],
      "description": "the open-ocean fraction of the ocean grid (FBFrac(compocn) ofrac): the mapfcopy redistribution of the ice-grid ofrac (F90:866-881) - the identity map in the traced configuration, [1]",
      "shape": [
        "tgt_cells"
      ]
    }
  },
  "equations": [
    {
      "lhs": "ifrac",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "conservative_overlap_apply",
        "bindings": {
          "A_ij": "w_ij",
          "A_j": "A_j",
          "F_src": "ifrac_ice",
          "atol": "atol"
        }
      }
    },
    {
      "lhs": "ofrac",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "conservative_overlap_apply",
        "bindings": {
          "A_ij": "w_ij",
          "A_j": "A_j",
          "F_src": "ofrac_ice",
          "atol": "atol"
        }
      }
    }
  ],
  "tests": [
    {
      "id": "step1_first_cell",
      "description": "Instantaneous pin of the ocn-grid fraction maps (the mapfcopy redistribution of F90:866-881) from stage1/dumps/cmeps/cmeps_fractions_ocn.csv: row (step 1, gid 41583, ocean cell n = 6933, lat -69.504 deg, lon -285.333 deg - the same window as cmeps_merge.csv and cmeps_map_ocn.csv).  The identity map reproduces the ice-grid fractions at the same gid: ifrac = 0.46925, ofrac = 0.53075 (ofrac + ifrac = 1 exactly: the traced cells are fully masked, So_omask = 1, the SICE mask is 1 there).  time_span {0,0} evaluates the map at the dumped inputs; the outputs are asserted at dump precision, rel 1e-12 (abs 0.0).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "ifrac_ice": [
          0.4692451250438887
        ],
        "ofrac_ice": [
          0.5307548749561113
        ]
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 0.0
      },
      "assertions": [
        {
          "variable": "ifrac",
          "time": 0.0,
          "coords": {
            "tgt_cells": 1
          },
          "expected": 0.4692451250438887
        },
        {
          "variable": "ofrac",
          "time": 0.0,
          "coords": {
            "tgt_cells": 1
          },
          "expected": 0.5307548749561113
        }
      ]
    },
    {
      "id": "step2_first_cell",
      "description": "Instantaneous pin of the ocn-grid fraction maps (the mapfcopy redistribution of F90:866-881) from stage1/dumps/cmeps/cmeps_fractions_ocn.csv: row (step 2, gid 41583, ocean cell n = 6933).  The runtime update between steps 1 and 2 (ifrac 0.46925 -> 0.47376; the dump's mapped Si_ifrac column at step 2 equals the step-1 ifrac bit-exactly - the one-step lag of the ice->ocn export map, verified on all 276 (step, n) pairs by the stage-1 validator and documented in the dump header).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "ifrac_ice": [
          0.4737632464673028
        ],
        "ofrac_ice": [
          0.5262367535326973
        ]
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 0.0
      },
      "assertions": [
        {
          "variable": "ifrac",
          "time": 0.0,
          "coords": {
            "tgt_cells": 1
          },
          "expected": 0.4737632464673028
        },
        {
          "variable": "ofrac",
          "time": 0.0,
          "coords": {
            "tgt_cells": 1
          },
          "expected": 0.5262367535326973
        }
      ]
    },
    {
      "id": "step12_mid_cell",
      "description": "Instantaneous pin of the ocn-grid fraction maps (the mapfcopy redistribution of F90:866-881) from stage1/dumps/cmeps/cmeps_fractions_ocn.csv: row (step 12, gid 42662, ocean cell n = 7112, lat -69.032 deg, lon -286.0 deg).  Mid-window near-open cell: ifrac = 0.07441, ofrac = 0.92559 (ofrac + ifrac = 1 exactly).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "ifrac_ice": [
          0.07441152772714216
        ],
        "ofrac_ice": [
          0.9255884722728578
        ]
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 0.0
      },
      "assertions": [
        {
          "variable": "ifrac",
          "time": 0.0,
          "coords": {
            "tgt_cells": 1
          },
          "expected": 0.07441152772714216
        },
        {
          "variable": "ofrac",
          "time": 0.0,
          "coords": {
            "tgt_cells": 1
          },
          "expected": 0.9255884722728578
        }
      ]
    },
    {
      "id": "step24_first_cell",
      "description": "Instantaneous pin of the ocn-grid fraction maps (the mapfcopy redistribution of F90:866-881) from stage1/dumps/cmeps/cmeps_fractions_ocn.csv: row (step 24, gid 41583, ocean cell n = 6933).  The first traced cell of the last step: ifrac = 0.44701, ofrac = 0.55299 (the dump's mapped Si_ifrac column at step 24 = 0.45300 = the step-23 ifrac, the one-step lag).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "ifrac_ice": [
          0.44700692718339563
        ],
        "ofrac_ice": [
          0.5529930728166044
        ]
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 0.0
      },
      "assertions": [
        {
          "variable": "ifrac",
          "time": 0.0,
          "coords": {
            "tgt_cells": 1
          },
          "expected": 0.44700692718339563
        },
        {
          "variable": "ofrac",
          "time": 0.0,
          "coords": {
            "tgt_cells": 1
          },
          "expected": 0.5529930728166044
        }
      ]
    },
    {
      "id": "step24_last_cell",
      "description": "Instantaneous pin of the ocn-grid fraction maps (the mapfcopy redistribution of F90:866-881) from stage1/dumps/cmeps/cmeps_fractions_ocn.csv: row (step 24, gid 42667, ocean cell n = 7117, lat -69.032 deg, lon -282.667 deg).  The last traced cell: ifrac = 0.46845, ofrac = 0.53155.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "ifrac_ice": [
          0.4684479976936625
        ],
        "ofrac_ice": [
          0.5315520023063375
        ]
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 0.0
      },
      "assertions": [
        {
          "variable": "ifrac",
          "time": 0.0,
          "coords": {
            "tgt_cells": 1
          },
          "expected": 0.4684479976936625
        },
        {
          "variable": "ofrac",
          "time": 0.0,
          "coords": {
            "tgt_cells": 1
          },
          "expected": 0.5315520023063375
        }
      ]
    },
    {
      "id": "min_ifrac",
      "description": "Instantaneous pin of the ocn-grid fraction maps (the mapfcopy redistribution of F90:866-881) from stage1/dumps/cmeps/cmeps_fractions_ocn.csv: row (step 24, gid 42662, ocean cell n = 7112).  The lowest ice fraction of the window: ifrac = 0.06772, ofrac = 0.93228.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "ifrac_ice": [
          0.06772403454417536
        ],
        "ofrac_ice": [
          0.9322759654558246
        ]
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 0.0
      },
      "assertions": [
        {
          "variable": "ifrac",
          "time": 0.0,
          "coords": {
            "tgt_cells": 1
          },
          "expected": 0.06772403454417536
        },
        {
          "variable": "ofrac",
          "time": 0.0,
          "coords": {
            "tgt_cells": 1
          },
          "expected": 0.9322759654558246
        }
      ]
    },
    {
      "id": "max_ifrac",
      "description": "Instantaneous pin of the ocn-grid fraction maps (the mapfcopy redistribution of F90:866-881) from stage1/dumps/cmeps/cmeps_fractions_ocn.csv: row (step 24, gid 42126, ocean cell n = 7026, lat -69.270 deg, lon -283.333 deg).  The highest ice fraction of the window: ifrac = 0.61536, ofrac = 0.38464.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "ifrac_ice": [
          0.6153554928858544
        ],
        "ofrac_ice": [
          0.38464450711414555
        ]
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 0.0
      },
      "assertions": [
        {
          "variable": "ifrac",
          "time": 0.0,
          "coords": {
            "tgt_cells": 1
          },
          "expected": 0.6153554928858544
        },
        {
          "variable": "ofrac",
          "time": 0.0,
          "coords": {
            "tgt_cells": 1
          },
          "expected": 0.38464450711414555
        }
      ]
    }
  ]
}
```

</details>
