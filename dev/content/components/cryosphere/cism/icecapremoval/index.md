---
title: "IceCapRemoval"
slug: "icecapremoval"
domains: ["cryosphere"]
component_types: ["model"]
subdomains: ["cism"]
domain: "cryosphere"
subdomain: "cism"
component_type: "model"
esm_version: "2.0.0"
esm_path: "components/cryosphere/cism/cism_calving.esm"
reference: "https://github.com/ESCOMP/CESM"
description: "Stage-2 implementation of the CISM calving physics (stage 2 of the EqESM project; CISM = cismwrap_3_00_002 / cism_main_3.00_002 as built in CESM cesm3.0-alphabranch, reference run T1850Gg/f09_g17_gris20): (a) CalvingLaw - the CALVING_FLOAT_ZERO threshold/margin criterion and removal law of glissade_calving_solve (libglissade/glissade_calving.F90:618-963) for the reference options whichcalving = 1 = CALVING_FLOAT_ZERO, calving_domain = 1 = CALVING_DOMAIN_EVERYWHERE and calving timescale = 0 (glide_types.F90:183,200,1648): the basic ice/floating masks of glissade_get_masks with the law's mask threshold thklim = 0.0 (calve_ice_basic, F90:1085-1092; ice_mask = thck > 0, floating_mask = ice & (topg - eus < -(rhoi/rhoo)*thck), glissade_masks.F90:165-193, rhoi/rhoo = 917/1026 - glimmer_physcon.F90:41-42, the CCSMCOUPLED pointer associations rhoi => SHR_CONST_RHOICE, rhoo => SHR_CONST_RHOSW that override the standalone 910/1028 defaults of F90:67-68 - the cism_templates.esm cism_floating_mask template), the calving fraction (F90:1065-1077: 1.0 for timescale = 0, else min(dt/timescale, 1)), and the removal law (F90:1175-1188, the cism_calving_float_zero template): calving_thck = calving_fraction*thck where the cell is floating and inside the calving domain (with CALVING_DOMAIN_EVERYWHERE the domain mask is identically 1, F90:1171), then thck -= calving_thck (F90:1185). (b) IcebergRemoval - the remove_icebergs pass (F90:875-922, 4110-4324) as a PER-CELL LAW GIVEN THE DUMPED CONNECTIVITY MASK: iceberg removal is a flood fill (firmly grounded cells with f_ground_cell >= f_ground_threshold seed a fill; the initial color is thck > 0 and the fill spreads through the law's ice_mask cells, F90:4216-4225; floating cells still holding the initial color with land_mask = 0 are removed, F90:4310-4318), which the .esm spec cannot express as an equation - the stage-1 dump carries the per-cell result (calving_thck_iceberg, the amount the pass removed) and the model applies the per-cell law removal = thck where iceberg_mask = 1. In the reference window the mask is 0 on every row (the CALVING_FLOAT_ZERO law has already removed every floating cell within the same solve, and remove_icebergs only removes floating cells), so only the no-op branch is pinned (hollow boundary pins); the flood fill itself has no operator in the esm spec or EarthSciDiscretizations and is a documented stage-3 gap (README.md). (c) IceCapRemoval - the ice-cap removal of glissade_handle_ice_caps (glissade_utils.F90:1141-1235) as a PER-CELL LAW GIVEN THE DUMPED CONNECTIVITY MASK: the ice_cap_mask of glissade_ice_sheet_mask (cells with thck > thklim = 1.0 m, the run's ice_limit, not connected by edge neighbors to any cell with thck >= minthck_ice_sheet = 2000 m, glissade_masks.F90:701-889) is likewise a flood-fill result the spec cannot express; the model applies the per-cell removal law (F90:1228-1233): removal_thck += thck and thck = 0 where ice_cap_mask = 1. The mask is exercised in the reference run (the gland20 initial state has ice caps removed at initialization, cism_step = 0, and a cap forms and is removed in year 2). Tests pin the stage-1 instrumented traces cism_calving.csv and cism_calving_icecap.csv (one row per active cell and solve call; the law fires at the marine margins from step 3 on, and the caps fire at init and in year 2) and the h0i whole-domain flux."
tags: ["cryosphere", "cism", "model", "ice-sheet", "calving", "iceberg", "ice-cap", "cesm"]
---

## Description

Stage-2 implementation of the CISM calving physics (stage 2 of the EqESM project; CISM = cismwrap_3_00_002 / cism_main_3.00_002 as built in CESM cesm3.0-alphabranch, reference run T1850Gg/f09_g17_gris20): (a) CalvingLaw - the CALVING_FLOAT_ZERO threshold/margin criterion and removal law of glissade_calving_solve (libglissade/glissade_calving.F90:618-963) for the reference options whichcalving = 1 = CALVING_FLOAT_ZERO, calving_domain = 1 = CALVING_DOMAIN_EVERYWHERE and calving timescale = 0 (glide_types.F90:183,200,1648): the basic ice/floating masks of glissade_get_masks with the law's mask threshold thklim = 0.0 (calve_ice_basic, F90:1085-1092; ice_mask = thck > 0, floating_mask = ice & (topg - eus < -(rhoi/rhoo)*thck), glissade_masks.F90:165-193, rhoi/rhoo = 917/1026 - glimmer_physcon.F90:41-42, the CCSMCOUPLED pointer associations rhoi => SHR_CONST_RHOICE, rhoo => SHR_CONST_RHOSW that override the standalone 910/1028 defaults of F90:67-68 - the cism_templates.esm cism_floating_mask template), the calving fraction (F90:1065-1077: 1.0 for timescale = 0, else min(dt/timescale, 1)), and the removal law (F90:1175-1188, the cism_calving_float_zero template): calving_thck = calving_fraction*thck where the cell is floating and inside the calving domain (with CALVING_DOMAIN_EVERYWHERE the domain mask is identically 1, F90:1171), then thck -= calving_thck (F90:1185). (b) IcebergRemoval - the remove_icebergs pass (F90:875-922, 4110-4324) as a PER-CELL LAW GIVEN THE DUMPED CONNECTIVITY MASK: iceberg removal is a flood fill (firmly grounded cells with f_ground_cell >= f_ground_threshold seed a fill; the initial color is thck > 0 and the fill spreads through the law's ice_mask cells, F90:4216-4225; floating cells still holding the initial color with land_mask = 0 are removed, F90:4310-4318), which the .esm spec cannot express as an equation - the stage-1 dump carries the per-cell result (calving_thck_iceberg, the amount the pass removed) and the model applies the per-cell law removal = thck where iceberg_mask = 1. In the reference window the mask is 0 on every row (the CALVING_FLOAT_ZERO law has already removed every floating cell within the same solve, and remove_icebergs only removes floating cells), so only the no-op branch is pinned (hollow boundary pins); the flood fill itself has no operator in the esm spec or EarthSciDiscretizations and is a documented stage-3 gap (README.md). (c) IceCapRemoval - the ice-cap removal of glissade_handle_ice_caps (glissade_utils.F90:1141-1235) as a PER-CELL LAW GIVEN THE DUMPED CONNECTIVITY MASK: the ice_cap_mask of glissade_ice_sheet_mask (cells with thck > thklim = 1.0 m, the run's ice_limit, not connected by edge neighbors to any cell with thck >= minthck_ice_sheet = 2000 m, glissade_masks.F90:701-889) is likewise a flood-fill result the spec cannot express; the model applies the per-cell removal law (F90:1228-1233): removal_thck += thck and thck = 0 where ice_cap_mask = 1. The mask is exercised in the reference run (the gland20 initial state has ice caps removed at initialization, cism_step = 0, and a cap forms and is removed in year 2). Tests pin the stage-1 instrumented traces cism_calving.csv and cism_calving_icecap.csv (one row per active cell and solve call; the law fires at the marine margins from step 3 on, and the caps fire at init and in year 2) and the h0i whole-domain flux.

## Reference

- CISM (Community Ice Sheet Model) cismwrap_3_00_002 / cism_main_3.00.002, as built in CESM cesm3.0-alphabranch (checkout stage1/cesm/components/cism, reference run T1850Gg/f09_g17_gris20): libglissade/glissade_basal_traction.F90, libglissade/glissade_therm.F90, libglissade/glissade_grid_operators.F90, libglissade/glissade_velo_higher.F90, libglissade/glissade_mass_balance.F90, libglissade/glissade_calving.F90, libglissade/glissade_masks.F90, libglissade/glissade_utils.F90, libglimmer/glimmer_physcon.F90, libglimmer/glimmer_utils.F90, libglide/glide_types.F90, libglide/glide_setup.F90, libglad/glad_main.F90, libglad/glad_timestep.F90, libglad/glad_output_states.F90, libglad/glad_output_fluxes.F90, drivers/cpl/nuopc/glc_import_export.F90 - the reference implementation these components are transcribed from.
- CISM (Community Ice Sheet Model) cism_main_3.00.002: libglissade/glissade_calving.F90, libglissade/glissade_masks.F90, libglissade/glissade_utils.F90, libglide/glide_types.F90, libglimmer/glimmer_physcon.F90.
- EarthSciModels - the authoritative .esm corpus this component lives in.

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `thck` | `m` | `0.0` | thickness at the glissade_handle_ice_caps call (m; the ice-cap trace's thck_before column) |
| `removal_thck_in` | `m` | `0.0` | accumulated removal flux entering the call (m; the trace's removal_thck_before column; 0 in the reference run - the flux is reset right after the calving solve, glissade.F90:1341) |
| `ice_cap_mask` | `1` | `0.0` | ice-cap connectivity mask of glissade_ice_sheet_mask (cells with thck > thklim = 1.0 m - the run's ice_limit, glc.log 'thickness limit for dynamically active ice (m): 1.0'; glide_setup.F90:2278 reads 'ice_limit' into model%numerics%thklim - not connected by edge neighbors to any cell with thck >= minthck_ice_sheet = 2000 m, glissade_masks.F90:701-889; a flood fill the .esm spec cannot express - dumped per cell, 1 on every trace row) |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `removal_thck` | `m` |  | removal flux after the call: removal_thck_in + thck where ice_cap_mask = 1, else removal_thck_in (glissade_utils.F90:1230; the trace's removal_thck_after column) |
| `thck_after` | `m` |  | thickness after the removal: 0 where ice_cap_mask = 1, else thck (glissade_utils.F90:1231; the trace's thck_after column) |

## Observed expressions

$$
removal_{thck} = removal_{thck\,in} + \mathrm{ifelse}\left(ice_{cap\,mask} = \mathrm{const}\left(\right), thck, \mathrm{const}\left(\right)\right)
$$
_removal flux after the call: removal_thck_in + thck where ice_cap_mask = 1, else removal_thck_in (glissade_utils.F90:1230; the trace's removal_thck_after column)_

$$
thck_{after} = \mathrm{ifelse}\left(ice_{cap\,mask} = \mathrm{const}\left(\right), \mathrm{const}\left(\right), thck\right)
$$
_thickness after the removal: 0 where ice_cap_mask = 1, else thck (glissade_utils.F90:1231; the trace's thck_after column)_

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "variables": {
    "thck": {
      "type": "parameter",
      "units": "m",
      "default": 0.0,
      "description": "thickness at the glissade_handle_ice_caps call (m; the ice-cap trace's thck_before column)"
    },
    "removal_thck_in": {
      "type": "parameter",
      "units": "m",
      "default": 0.0,
      "description": "accumulated removal flux entering the call (m; the trace's removal_thck_before column; 0 in the reference run - the flux is reset right after the calving solve, glissade.F90:1341)"
    },
    "ice_cap_mask": {
      "type": "parameter",
      "units": "1",
      "default": 0.0,
      "description": "ice-cap connectivity mask of glissade_ice_sheet_mask (cells with thck > thklim = 1.0 m - the run's ice_limit, glc.log 'thickness limit for dynamically active ice (m): 1.0'; glide_setup.F90:2278 reads 'ice_limit' into model%numerics%thklim - not connected by edge neighbors to any cell with thck >= minthck_ice_sheet = 2000 m, glissade_masks.F90:701-889; a flood fill the .esm spec cannot express - dumped per cell, 1 on every trace row)"
    },
    "removal_thck": {
      "type": "unknown",
      "units": "m",
      "description": "removal flux after the call: removal_thck_in + thck where ice_cap_mask = 1, else removal_thck_in (glissade_utils.F90:1230; the trace's removal_thck_after column)"
    },
    "thck_after": {
      "type": "unknown",
      "units": "m",
      "description": "thickness after the removal: 0 where ice_cap_mask = 1, else thck (glissade_utils.F90:1231; the trace's thck_after column)"
    }
  },
  "equations": [
    {
      "lhs": "removal_thck",
      "rhs": {
        "op": "+",
        "args": [
          "removal_thck_in",
          {
            "op": "ifelse",
            "args": [
              {
                "op": "==",
                "args": [
                  "ice_cap_mask",
                  {
                    "op": "const",
                    "args": [],
                    "value": 1.0,
                    "units": "1"
                  }
                ]
              },
              "thck",
              {
                "op": "const",
                "args": [],
                "value": 0.0,
                "units": "m"
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "thck_after",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "==",
            "args": [
              "ice_cap_mask",
              {
                "op": "const",
                "args": [],
                "value": 1.0,
                "units": "1"
              }
            ]
          },
          {
            "op": "const",
            "args": [],
            "value": 0.0,
            "units": "m"
          },
          "thck"
        ]
      }
    }
  ],
  "tests": [
    {
      "id": "icecap_step0_cell58123",
      "description": "Dump pin, cism_calving_icecap.csv row (cism_step 0, cell 58,123): the ice-cap removal of glissade_handle_ice_caps (glissade_utils.F90:1228-1233) removes the full column of every cell with ice_cap_mask = 1 - the mask comes from the glissade_ice_sheet_mask flood fill (thck > thklim = 1.0 m cells not connected by edge neighbors to any thck >= 2000 m cell, glissade_masks.F90:701-889), dumped per cell: with thck_before = 7.729979991912842 m and removal_thck_before = 0 m, removal_thck = 7.729979991912842 m and thck_after = 0.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "thck": 7.729979991912842,
        "removal_thck_in": 0.0,
        "ice_cap_mask": 1.0
      },
      "assertions": [
        {
          "variable": "removal_thck",
          "time": 0.0,
          "expected": 7.729979991912842,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "thck_after",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "icecap_init_thin_cell59124",
      "description": "Dump pin, cism_calving_icecap.csv row (cism_step 0, cell 59,124), the thinnest init-time ice cap: with thck_before = 4.87994384765625 m and removal_thck_before = 0 m, the removal (glissade_utils.F90:1228-1233) gives removal_thck = 4.87994384765625 m and thck_after = 0.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "thck": 4.87994384765625,
        "removal_thck_in": 0.0,
        "ice_cap_mask": 1.0
      },
      "assertions": [
        {
          "variable": "removal_thck",
          "time": 0.0,
          "expected": 4.87994384765625,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "thck_after",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "icecap_init_thick_cell60128",
      "description": "Dump pin, cism_calving_icecap.csv row (cism_step 0, cell 60,128), the thickest init-time ice cap: with thck_before = 123.94999694824219 m and removal_thck_before = 0 m, the removal (glissade_utils.F90:1228-1233) gives removal_thck = 123.94999694824219 m and thck_after = 0.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "thck": 123.94999694824219,
        "removal_thck_in": 0.0,
        "ice_cap_mask": 1.0
      },
      "assertions": [
        {
          "variable": "removal_thck",
          "time": 0.0,
          "expected": 123.94999694824219,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "thck_after",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "icecap_step4_cell3627",
      "description": "Dump pin, cism_calving_icecap.csv row (cism_step 4, cell 36,27): the single ice cap that forms during year 2 and is removed at the end of it (the same cell appears as the only nz cell of the year-3 h0i ice_cap_mask, and the h0i calving_rate checks show the calving-law cells of step 4 all calved): with thck_before = 1.2239353984099954 m and removal_thck_before = 0 m, the removal (glissade_utils.F90:1228-1233) gives removal_thck = 1.2239353984099954 m and thck_after = 0.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "thck": 1.2239353984099954,
        "removal_thck_in": 0.0,
        "ice_cap_mask": 1.0
      },
      "assertions": [
        {
          "variable": "removal_thck",
          "time": 0.0,
          "expected": 1.2239353984099954,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "thck_after",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    }
  ]
}
```

</details>
