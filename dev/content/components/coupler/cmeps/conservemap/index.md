---
title: "ConserveMap"
slug: "conservemap"
domains: ["coupler"]
component_types: ["model"]
subdomains: ["cmeps"]
domain: "coupler"
subdomain: "cmeps"
component_type: "model"
esm_version: "1.3.0"
esm_path: "components/coupler/cmeps/cmeps_map.esm"
reference: "https://github.com/ESCOMP/CESM"
description: "The atm->ocn mapping step of the CMEPS mediator (map_atm2ocn of med_phases_post_atm_mod.F90, the sparse weight apply of med_map_field_packed, med_map_mod.F90:1187-1234) as transcribed from the M8 stage-1 dump (cmeps_map_ocn.csv / cmeps_map_atm.csv of the C_JRA_t62_inst run, fork cmeps 2673bd61). The law is dst_j = (sum_i W_ij x_i)/normOne_j over the source stencil of each destination cell, with the weights W taken AS DATA from the offline ESMF_RegridWeightGen mapping files (atm2ocn_conserve_fracarea.nc, atm2ocn_bilinear.nc - bit-identical to the online routehandle: stage1/analysis/check_cmeps_map.py replays both laws from the file weights at worst rel 0.0 over 1152 (field,step,cell) checks each) and normOne the field_normOne row sums (mapnorm='one': no source fraction factor). Both routehandles express the SAME law through the single EarthSciDiscretizations conservative_overlap_apply template imported by reference (${ESD_ROOT}/regridding/conservative_overlap.esm): ConserveMap binds the ESMF conserve weights as its A_ij data and the dumped normOne_consf as A_j; BilinearMap binds the bilinear weights and normOne_bilnr the same way. The mapnorm='lfrac' source weighting of the M9 lane's lnd->rof map is carried in the field (F_src = lfrac*x) rather than in a second template, so there is exactly one map law for every ESMF routehandle. Both models evaluate on the traced 12-cell window (the first masked cells of PET 0, gids 41583, 41584, 42123-42126, 42662-42667 - the same window as cmeps_merge.csv) with the full ESMF stencils (conserve: 3 distinct T62 source cells, <= 2 terms; bilinear: 8, exactly 4 terms), and the tests pin cmeps_map_ocn.csv cell-wise (coords over the 12 traced cells) at rel 1e-12 at the STEPS_PINNED = (1, 13, 24) steps of the 24-step window (the first, a middle and the last: the steps repeat the same map and the same stencils with smoothly drifting inputs, so three steps spanning the drift suffice): Faxa_snowl (conserve) and Sa_tbot, Sa_pbot (bilinear) - 108 assertions (the stage-1 replay is bit-exact; the engine's own summation order leaves ~1e-16 slack on these short stencils). The remaining dumped fields are configuration facts of the traced window, not law statements, and are unpinned as unfailable: Faxa_rainl/Faxa_rainc/Faxa_snowc are identically 0 on every traced row (the Gulf-of-Guinea window receives snowfall but no rain in this JRA January window), Sa_z is a constant 10 m source (the mapped constant equals itself to 2e-15), and Sa_pslv is bit-identical to Sa_pbot on every traced row (the unfailable-assertion precedent of the prep_ice round)."
tags: ["coupler", "cmeps", "model", "map", "cesm"]
---

## Description

The atm->ocn mapping step of the CMEPS mediator (map_atm2ocn of med_phases_post_atm_mod.F90, the sparse weight apply of med_map_field_packed, med_map_mod.F90:1187-1234) as transcribed from the M8 stage-1 dump (cmeps_map_ocn.csv / cmeps_map_atm.csv of the C_JRA_t62_inst run, fork cmeps 2673bd61). The law is dst_j = (sum_i W_ij x_i)/normOne_j over the source stencil of each destination cell, with the weights W taken AS DATA from the offline ESMF_RegridWeightGen mapping files (atm2ocn_conserve_fracarea.nc, atm2ocn_bilinear.nc - bit-identical to the online routehandle: stage1/analysis/check_cmeps_map.py replays both laws from the file weights at worst rel 0.0 over 1152 (field,step,cell) checks each) and normOne the field_normOne row sums (mapnorm='one': no source fraction factor). Both routehandles express the SAME law through the single EarthSciDiscretizations conservative_overlap_apply template imported by reference (${ESD_ROOT}/regridding/conservative_overlap.esm): ConserveMap binds the ESMF conserve weights as its A_ij data and the dumped normOne_consf as A_j; BilinearMap binds the bilinear weights and normOne_bilnr the same way. The mapnorm='lfrac' source weighting of the M9 lane's lnd->rof map is carried in the field (F_src = lfrac*x) rather than in a second template, so there is exactly one map law for every ESMF routehandle. Both models evaluate on the traced 12-cell window (the first masked cells of PET 0, gids 41583, 41584, 42123-42126, 42662-42667 - the same window as cmeps_merge.csv) with the full ESMF stencils (conserve: 3 distinct T62 source cells, <= 2 terms; bilinear: 8, exactly 4 terms), and the tests pin cmeps_map_ocn.csv cell-wise (coords over the 12 traced cells) at rel 1e-12 at the STEPS_PINNED = (1, 13, 24) steps of the 24-step window (the first, a middle and the last: the steps repeat the same map and the same stencils with smoothly drifting inputs, so three steps spanning the drift suffice): Faxa_snowl (conserve) and Sa_tbot, Sa_pbot (bilinear) - 108 assertions (the stage-1 replay is bit-exact; the engine's own summation order leaves ~1e-16 slack on these short stencils). The remaining dumped fields are configuration facts of the traced window, not law statements, and are unpinned as unfailable: Faxa_rainl/Faxa_rainc/Faxa_snowc are identically 0 on every traced row (the Gulf-of-Guinea window receives snowfall but no rain in this JRA January window), Sa_z is a constant 10 m source (the mapped constant equals itself to 2e-15), and Sa_pslv is bit-identical to Sa_pbot on every traced row (the unfailable-assertion precedent of the prep_ice round).

## Reference

- CESM (Community Earth System Model), ESCOMP/CESM: CMEPS (Coupled Mediator for Earth System Prediction) source (cesm3.0-alphabranch) - flux_atmocn/flux_atmocn_Large.F90, share/src/shr_wv_sat_mod.F90, share/src/shr_orb_mod.F90, mediator/med_phases_aofluxes_mod.F90, mediator/med_phases_ocnalb_mod.F90, mediator/med_phases_prep_ocn_mod.F90, mediator/med_phases_prep_atm_mod.F90, mediator/med_merge_mod.F90, mediator/esmFldsExchange_cesm_mod.F90 - the reference implementation these components are transcribed from.
- EarthSciModels - the authoritative .esm corpus this component lives in.

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `w_ij` | `1` | `[[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.5937491755032698, 0.0, 0.0, 0.0, 0.0, 0.0], [1.0, 1.0, 1.0, 1.0, 0.40625082871365054, 0.0, 0.4062508244967302, 1.0, 1.0, 0.40625082449677163, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.5937491712863495, 1.0, 0.0, 0.0, 0.0, 0.5937491755032284, 1.0, 1.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]]` | the ESMF conservative routehandle weights of the traced subdomain (atm2ocn_conserve_fracarea.nc, S column in file order; the 3 distinct source cells of gids 1960-1962 zero-padded to the NSRC = 8 rows of the bilinear subdomain), [1] |
| `norm_one` | `1` | `[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]` | the field_normOne row sums of the mapconsf routehandle (normOne_consf of cmeps_map_ocn.csv, = the weight-file row sums bit-for-bit; exactly 1.0 on the fully covered ocean cells - the FRACAREA partition of unity), [1] |
| `atol` | `1` | `0.0` | sliver filter of conservative_overlap_apply (w_ij > atol); 0 drops only the zero-padded entries |
| `x_src` | `kg/m^2/s` | `[2.226718622409887e-06, 2.597398944471444e-06, 1.044986737757332e-06, 0.0, 0.0, 0.0, 0.0, 0.0]` | the atm-grid source values of the traced subdomain's source cells (cmeps_map_atm.csv, all-PET gather; the conserve fields are Faxa_rainl/rainc/snowl/snowc, all kg/m^2/s - the model is field-generic and each test overrides x_src with one field's values; only Faxa_snowl is nonzero on the traced window), [kg/m^2/s] |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `dst` | `kg/m^2/s` | `0.0` | the mapped conservative field: dst_j = (sum_i w_ij x_i)/normOne_j of med_map_field_packed (the normOne division of mapnorm='one'), [kg/m^2/s] |

## Observed expressions

$$
dst = \mathrm{conservative_overlap_apply}\left(A_{ij}=w_{ij}, A_{j}=norm_{one}, F_{src}=x_{src}, atol=atol\right)
$$
_the mapped conservative field: dst_j = (sum_i w_ij x_i)/normOne_j of med_map_field_packed (the normOne division of mapnorm='one'), [kg/m^2/s]_

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
      "description": "the ESMF conservative routehandle weights of the traced subdomain (atm2ocn_conserve_fracarea.nc, S column in file order; the 3 distinct source cells of gids 1960-1962 zero-padded to the NSRC = 8 rows of the bilinear subdomain), [1]",
      "default": [
        [
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.5937491755032698,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0
        ],
        [
          1.0,
          1.0,
          1.0,
          1.0,
          0.40625082871365054,
          0.0,
          0.4062508244967302,
          1.0,
          1.0,
          0.40625082449677163,
          0.0,
          0.0
        ],
        [
          0.0,
          0.0,
          0.0,
          0.0,
          0.5937491712863495,
          1.0,
          0.0,
          0.0,
          0.0,
          0.5937491755032284,
          1.0,
          1.0
        ],
        [
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
        [
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
        [
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
        [
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
        [
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
        ]
      ],
      "shape": [
        "src_cells",
        "tgt_cells"
      ]
    },
    "norm_one": {
      "type": "parameter",
      "units": "1",
      "description": "the field_normOne row sums of the mapconsf routehandle (normOne_consf of cmeps_map_ocn.csv, = the weight-file row sums bit-for-bit; exactly 1.0 on the fully covered ocean cells - the FRACAREA partition of unity), [1]",
      "default": [
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0,
        1.0
      ],
      "shape": [
        "tgt_cells"
      ]
    },
    "atol": {
      "type": "parameter",
      "units": "1",
      "description": "sliver filter of conservative_overlap_apply (w_ij > atol); 0 drops only the zero-padded entries",
      "default": 0.0
    },
    "x_src": {
      "type": "parameter",
      "units": "kg/m^2/s",
      "description": "the atm-grid source values of the traced subdomain's source cells (cmeps_map_atm.csv, all-PET gather; the conserve fields are Faxa_rainl/rainc/snowl/snowc, all kg/m^2/s - the model is field-generic and each test overrides x_src with one field's values; only Faxa_snowl is nonzero on the traced window), [kg/m^2/s]",
      "default": [
        2.226718622409887e-06,
        2.597398944471444e-06,
        1.044986737757332e-06,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0
      ],
      "shape": [
        "src_cells"
      ]
    },
    "dst": {
      "type": "unknown",
      "units": "kg/m^2/s",
      "description": "the mapped conservative field: dst_j = (sum_i w_ij x_i)/normOne_j of med_map_field_packed (the normOne division of mapnorm='one'), [kg/m^2/s]",
      "default": 0.0,
      "shape": [
        "tgt_cells"
      ]
    }
  },
  "equations": [
    {
      "lhs": "dst",
      "rhs": {
        "op": "apply_expression_template",
        "name": "conservative_overlap_apply",
        "args": [],
        "bindings": {
          "A_ij": "w_ij",
          "A_j": "norm_one",
          "F_src": "x_src",
          "atol": "atol"
        }
      }
    }
  ],
  "tests": [
    {
      "id": "step1_faxa_snowl",
      "description": "conservative atm->ocn map of Faxa_snowl at coupling step 1: dst_t = (sum_i w_ij x_i)/normOne_t replayed from the offline ESMF weights (cmeps_map_ocn.csv / cmeps_map_atm.csv / atm2ocn_conserve.nc) on the 12 traced cells, pinned cell-wise at rel 1e-12",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "x_src": [
          2.226718622409887e-06,
          2.597398944471444e-06,
          1.044986737757332e-06,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0
        ]
      },
      "assertions": [
        {
          "variable": "dst",
          "time": 0.0,
          "coords": {
            "tgt_cells": 1
          },
          "expected": 2.597398944471444e-06,
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "dst",
          "time": 0.0,
          "coords": {
            "tgt_cells": 2
          },
          "expected": 2.597398944471444e-06,
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "dst",
          "time": 0.0,
          "coords": {
            "tgt_cells": 3
          },
          "expected": 2.597398944471444e-06,
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "dst",
          "time": 0.0,
          "coords": {
            "tgt_cells": 4
          },
          "expected": 2.597398944471444e-06,
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "dst",
          "time": 0.0,
          "coords": {
            "tgt_cells": 5
          },
          "expected": 1.675655483240127e-06,
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "dst",
          "time": 0.0,
          "coords": {
            "tgt_cells": 6
          },
          "expected": 1.044986737757332e-06,
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "dst",
          "time": 0.0,
          "coords": {
            "tgt_cells": 7
          },
          "expected": 2.377307808872108e-06,
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "dst",
          "time": 0.0,
          "coords": {
            "tgt_cells": 8
          },
          "expected": 2.597398944471444e-06,
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "dst",
          "time": 0.0,
          "coords": {
            "tgt_cells": 9
          },
          "expected": 2.597398944471444e-06,
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "dst",
          "time": 0.0,
          "coords": {
            "tgt_cells": 10
          },
          "expected": 1.6756554766937926e-06,
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "dst",
          "time": 0.0,
          "coords": {
            "tgt_cells": 11
          },
          "expected": 1.044986737757332e-06,
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "dst",
          "time": 0.0,
          "coords": {
            "tgt_cells": 12
          },
          "expected": 1.044986737757332e-06,
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        }
      ]
    },
    {
      "id": "step13_faxa_snowl",
      "description": "conservative atm->ocn map of Faxa_snowl at coupling step 13: dst_t = (sum_i w_ij x_i)/normOne_t replayed from the offline ESMF weights (cmeps_map_ocn.csv / cmeps_map_atm.csv / atm2ocn_conserve.nc) on the 12 traced cells, pinned cell-wise at rel 1e-12",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "x_src": [
          2.520915725812504e-06,
          3.849742795486432e-06,
          3.4543534095467123e-07,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0
        ]
      },
      "assertions": [
        {
          "variable": "dst",
          "time": 0.0,
          "coords": {
            "tgt_cells": 1
          },
          "expected": 3.849742795486432e-06,
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "dst",
          "time": 0.0,
          "coords": {
            "tgt_cells": 2
          },
          "expected": 3.849742795486432e-06,
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "dst",
          "time": 0.0,
          "coords": {
            "tgt_cells": 3
          },
          "expected": 3.849742795486432e-06,
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "dst",
          "time": 0.0,
          "coords": {
            "tgt_cells": 4
          },
          "expected": 3.849742795486432e-06,
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "dst",
          "time": 0.0,
          "coords": {
            "tgt_cells": 5
          },
          "expected": 1.769063148425622e-06,
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "dst",
          "time": 0.0,
          "coords": {
            "tgt_cells": 6
          },
          "expected": 3.4543534095467123e-07,
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "dst",
          "time": 0.0,
          "coords": {
            "tgt_cells": 7
          },
          "expected": 3.060752818481111e-06,
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "dst",
          "time": 0.0,
          "coords": {
            "tgt_cells": 8
          },
          "expected": 3.849742795486432e-06,
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "dst",
          "time": 0.0,
          "coords": {
            "tgt_cells": 9
          },
          "expected": 3.849742795486432e-06,
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "dst",
          "time": 0.0,
          "coords": {
            "tgt_cells": 10
          },
          "expected": 1.7690631336483818e-06,
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "dst",
          "time": 0.0,
          "coords": {
            "tgt_cells": 11
          },
          "expected": 3.4543534095467123e-07,
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "dst",
          "time": 0.0,
          "coords": {
            "tgt_cells": 12
          },
          "expected": 3.4543534095467123e-07,
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        }
      ]
    },
    {
      "id": "step24_faxa_snowl",
      "description": "conservative atm->ocn map of Faxa_snowl at coupling step 24: dst_t = (sum_i w_ij x_i)/normOne_t replayed from the offline ESMF weights (cmeps_map_ocn.csv / cmeps_map_atm.csv / atm2ocn_conserve.nc) on the 12 traced cells, pinned cell-wise at rel 1e-12",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "x_src": [
          7.595381597046167e-06,
          1.2233382261728296e-05,
          1.66999474448816e-06,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0
        ]
      },
      "assertions": [
        {
          "variable": "dst",
          "time": 0.0,
          "coords": {
            "tgt_cells": 1
          },
          "expected": 1.2233382261728296e-05,
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "dst",
          "time": 0.0,
          "coords": {
            "tgt_cells": 2
          },
          "expected": 1.2233382261728296e-05,
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "dst",
          "time": 0.0,
          "coords": {
            "tgt_cells": 3
          },
          "expected": 1.2233382261728296e-05,
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "dst",
          "time": 0.0,
          "coords": {
            "tgt_cells": 4
          },
          "expected": 1.2233382261728296e-05,
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "dst",
          "time": 0.0,
          "coords": {
            "tgt_cells": 5
          },
          "expected": 5.961379677390397e-06,
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "dst",
          "time": 0.0,
          "coords": {
            "tgt_cells": 6
          },
          "expected": 1.66999474448816e-06,
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "dst",
          "time": 0.0,
          "coords": {
            "tgt_cells": 7
          },
          "expected": 9.479573191089665e-06,
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "dst",
          "time": 0.0,
          "coords": {
            "tgt_cells": 8
          },
          "expected": 1.2233382261728296e-05,
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "dst",
          "time": 0.0,
          "coords": {
            "tgt_cells": 9
          },
          "expected": 1.2233382261728296e-05,
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "dst",
          "time": 0.0,
          "coords": {
            "tgt_cells": 10
          },
          "expected": 5.961379632845871e-06,
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "dst",
          "time": 0.0,
          "coords": {
            "tgt_cells": 11
          },
          "expected": 1.66999474448816e-06,
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "dst",
          "time": 0.0,
          "coords": {
            "tgt_cells": 12
          },
          "expected": 1.66999474448816e-06,
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        }
      ]
    }
  ]
}
```

</details>
