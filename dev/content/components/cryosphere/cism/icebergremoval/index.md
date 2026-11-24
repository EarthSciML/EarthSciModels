---
title: "IcebergRemoval"
slug: "icebergremoval"
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
| `thck` | `m` | `0.0` | thickness at the remove_icebergs call (m; the calving trace's thck_iceberg column - after the calving law; 0 for the law's active cells) |
| `iceberg_mask` | `1` | `0.0` | iceberg-removal connectivity mask, dumped per cell as the calving trace's calving_thck_iceberg column > 0 indicator: 1 where remove_icebergs removed the cell (floating cells not connected by a path through cells with thck > 0 to grounded ice - the initial color of the fill, glissade_calving.F90:4216-4225, with removal of the initial-colored floating cells at F90:4310-4318; a flood fill the .esm spec cannot express). 0 on every row of the reference window - the CALVING_FLOAT_ZERO law has already removed every floating cell in the same solve, so the pass is a no-op by construction |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `iceberg_removal` | `m` |  | thickness removed by the iceberg pass: thck where iceberg_mask = 1, else 0 (F90:4313-4314) |
| `thck_after` | `m` |  | thickness after the iceberg pass, thck - iceberg_removal (F90:4314) |

## Observed expressions

$$
iceberg_{removal} = \mathrm{ifelse}\left(iceberg_{mask} = \mathrm{const}\left(\right), thck, \mathrm{const}\left(\right)\right)
$$
_thickness removed by the iceberg pass: thck where iceberg_mask = 1, else 0 (F90:4313-4314)_

$$
thck_{after} = thck - iceberg_{removal}
$$
_thickness after the iceberg pass, thck - iceberg_removal (F90:4314)_

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "variables": {
    "thck": {
      "type": "parameter",
      "units": "m",
      "default": 0.0,
      "description": "thickness at the remove_icebergs call (m; the calving trace's thck_iceberg column - after the calving law; 0 for the law's active cells)"
    },
    "iceberg_mask": {
      "type": "parameter",
      "units": "1",
      "default": 0.0,
      "description": "iceberg-removal connectivity mask, dumped per cell as the calving trace's calving_thck_iceberg column > 0 indicator: 1 where remove_icebergs removed the cell (floating cells not connected by a path through cells with thck > 0 to grounded ice - the initial color of the fill, glissade_calving.F90:4216-4225, with removal of the initial-colored floating cells at F90:4310-4318; a flood fill the .esm spec cannot express). 0 on every row of the reference window - the CALVING_FLOAT_ZERO law has already removed every floating cell in the same solve, so the pass is a no-op by construction"
    },
    "iceberg_removal": {
      "type": "unknown",
      "units": "m",
      "description": "thickness removed by the iceberg pass: thck where iceberg_mask = 1, else 0 (F90:4313-4314)"
    },
    "thck_after": {
      "type": "unknown",
      "units": "m",
      "description": "thickness after the iceberg pass, thck - iceberg_removal (F90:4314)"
    }
  },
  "equations": [
    {
      "lhs": "iceberg_removal",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "==",
            "args": [
              "iceberg_mask",
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
    },
    {
      "lhs": "thck_after",
      "rhs": {
        "op": "-",
        "args": [
          "thck",
          "iceberg_removal"
        ]
      }
    }
  ],
  "tests": [
    {
      "id": "iceberg_dump_step1_cell3104",
      "description": "Dump pin, cism_calving.csv row (cism_step 1, cell 3,104): the remove_icebergs pass with the dumped connectivity mask. In the reference window iceberg_mask = 0 on every row (the CALVING_FLOAT_ZERO law has already removed every floating cell in the same solve, and remove_icebergs only removes floating cells, glissade_calving.F90:4310-4318), and the incoming thck (the trace's thck_iceberg column) is 0, so the pass is a no-op: iceberg_removal = 0 and thck_after = 0.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "thck": 0.0,
        "iceberg_mask": 0.0
      },
      "assertions": [
        {
          "variable": "iceberg_removal",
          "time": 0.0,
          "expected": 0.0,
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
      "id": "iceberg_dump_step1_cell3105",
      "description": "Dump pin, cism_calving.csv row (cism_step 1, cell 3,105): as iceberg_dump_step1_cell3104 - a second no-op row (iceberg_mask = 0, thck_iceberg = 0): iceberg_removal = 0 and thck_after = 0.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "thck": 0.0,
        "iceberg_mask": 0.0
      },
      "assertions": [
        {
          "variable": "iceberg_removal",
          "time": 0.0,
          "expected": 0.0,
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
