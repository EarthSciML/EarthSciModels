---
title: "CalvingLaw"
slug: "calvinglaw"
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
| `thck` | `m` | `0.0` | ice thickness at the calving call, before any removal (m; the calving trace's thck_pre column, equal to the transport-exit thck of the same step) |
| `topg` | `m` | `0.0` | bed topography at the cell (m; the calving trace's topg column) |
| `eus` | `m` | `0.0` | eustatic sea level (m; the calving trace's eus column; 0.0 in the reference run) |
| `rhoi` | `kg/m^3` | `917.0` | ice density (glimmer_physcon rhoi = SHR_CONST_RHOICE = 917 kg/m3, glimmer_physcon.F90:41 - the CCSMCOUPLED pointer association; the standalone default is 910 kg/m3, F90:67) |
| `rhoo` | `kg/m^3` | `1026.0` | ocean density (glimmer_physcon rhoo = SHR_CONST_RHOSW = 1026 kg/m3, glimmer_physcon.F90:42 - the CCSMCOUPLED pointer association; the standalone default is 1028 kg/m3, F90:68) |
| `thklim` | `m` | `0.0` | mask thickness threshold of the calving law, thklim = 0.0 (calve_ice_basic, glissade_calving.F90:1089 - the law removes ice from any cell meeting the criterion, not just dynamically active ice) |
| `whichcalving` | `1` | `1.0` | calving law option whichcalving = 1 = CALVING_FLOAT_ZERO (glide_types.F90:183; the calving trace's whichcalving column is 1 on every row) |
| `calving_domain` | `1` | `1.0` | calving domain option calving_domain = 1 = CALVING_DOMAIN_EVERYWHERE (glide_types.F90:200; the trace's calving_domain column is 1 on every row) |
| `timescale` | `yr` | `0.0` | calving timescale (yr; glide_types.F90:1648; 0 in the reference run - the full column calves at once; the trace's timescale column) |
| `dt` | `yr` | `0.5` | model time step (yr; the reference run's dt = 0.5 yr; used only when timescale > 0) |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `ice_mask` | `1` |  | ice-presence mask ice_mask = 1 where thck > thklim (glissade_masks.F90:165-169; with the law's thklim = 0: thck > 0) |
| `floating_mask` | `1` |  | floating-ice mask floating_mask = 1 where ice is present and topg - eus < -(rhoi/rhoo)*thck (glissade_masks.F90:179-185) |
| `calving_domain_mask` | `1` |  | calving-domain mask: with CALVING_DOMAIN_EVERYWHERE (the reference option) it is identically 1 (calve_ice_basic, glissade_calving.F90:1169-1172); the CALVING_DOMAIN_OCEAN_EDGE alternative (floating with an ocean neighbor, F90:1153-1154) is not used by the reference run and is carried by the trace's margin_mask column as a dumped input |
| `calving_fraction` | `1` |  | fraction of the column removed in a calving cell: 1.0 for timescale = 0, else min(dt/timescale, 1) (calve_ice_basic, F90:1065-1077) |
| `calving_thck` | `m` |  | thickness removed by the calving law: calving_fraction*thck where floating and inside the calving domain, else 0 (F90:1184; with the reference options: thck in full) |
| `thck_after` | `m` |  | thickness after the calving law, thck - calving_thck (F90:1185) |

## Observed expressions

$$
ice_{mask} = \mathrm{ifelse}\left(\mathrm{>}\left(thck, thklim\right), \mathrm{const}\left(\right), \mathrm{const}\left(\right)\right)
$$
_ice-presence mask ice_mask = 1 where thck > thklim (glissade_masks.F90:165-169; with the law's thklim = 0: thck > 0)_

$$
floating_{mask} = \mathrm{cism_floating_mask}\left(thck=thck, topg=topg, eus=eus, thklim=thklim, rhoi=rhoi, rhoo=rhoo\right)
$$
_floating-ice mask floating_mask = 1 where ice is present and topg - eus < -(rhoi/rhoo)*thck (glissade_masks.F90:179-185)_

$$
calving_{domain\,mask} = \mathrm{const}\left(\right)
$$
_calving-domain mask: with CALVING_DOMAIN_EVERYWHERE (the reference option) it is identically 1 (calve_ice_basic, glissade_calving.F90:1169-1172); the CALVING_DOMAIN_OCEAN_EDGE alternative (floating with an ocean neighbor, F90:1153-1154) is not used by the reference run and is carried by the trace's margin_mask column as a dumped input_

$$
calving_{fraction} = \mathrm{ifelse}\left(timescale = \mathrm{const}\left(\right), \mathrm{const}\left(\right), \mathrm{min}\left(\frac{dt}{timescale}, \mathrm{const}\left(\right)\right)\right)
$$
_fraction of the column removed in a calving cell: 1.0 for timescale = 0, else min(dt/timescale, 1) (calve_ice_basic, F90:1065-1077)_

$$
calving_{thck} = \mathrm{cism_calving_float_zero}\left(floating_{mask}=floating_{mask}, calving_{domain\,mask}=calving_{domain\,mask}, calving_{fraction}=calving_{fraction}, thck=thck\right)
$$
_thickness removed by the calving law: calving_fraction*thck where floating and inside the calving domain, else 0 (F90:1184; with the reference options: thck in full)_

$$
thck_{after} = thck - calving_{thck}
$$
_thickness after the calving law, thck - calving_thck (F90:1185)_

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "expression_template_imports": [
    {
      "ref": "./cism_templates.esm"
    }
  ],
  "variables": {
    "thck": {
      "type": "parameter",
      "units": "m",
      "default": 0.0,
      "description": "ice thickness at the calving call, before any removal (m; the calving trace's thck_pre column, equal to the transport-exit thck of the same step)"
    },
    "topg": {
      "type": "parameter",
      "units": "m",
      "default": 0.0,
      "description": "bed topography at the cell (m; the calving trace's topg column)"
    },
    "eus": {
      "type": "parameter",
      "units": "m",
      "default": 0.0,
      "description": "eustatic sea level (m; the calving trace's eus column; 0.0 in the reference run)"
    },
    "rhoi": {
      "type": "parameter",
      "units": "kg/m^3",
      "default": 917.0,
      "description": "ice density (glimmer_physcon rhoi = SHR_CONST_RHOICE = 917 kg/m3, glimmer_physcon.F90:41 - the CCSMCOUPLED pointer association; the standalone default is 910 kg/m3, F90:67)"
    },
    "rhoo": {
      "type": "parameter",
      "units": "kg/m^3",
      "default": 1026.0,
      "description": "ocean density (glimmer_physcon rhoo = SHR_CONST_RHOSW = 1026 kg/m3, glimmer_physcon.F90:42 - the CCSMCOUPLED pointer association; the standalone default is 1028 kg/m3, F90:68)"
    },
    "thklim": {
      "type": "parameter",
      "units": "m",
      "default": 0.0,
      "description": "mask thickness threshold of the calving law, thklim = 0.0 (calve_ice_basic, glissade_calving.F90:1089 - the law removes ice from any cell meeting the criterion, not just dynamically active ice)"
    },
    "whichcalving": {
      "type": "parameter",
      "units": "1",
      "default": 1.0,
      "description": "calving law option whichcalving = 1 = CALVING_FLOAT_ZERO (glide_types.F90:183; the calving trace's whichcalving column is 1 on every row)"
    },
    "calving_domain": {
      "type": "parameter",
      "units": "1",
      "default": 1.0,
      "description": "calving domain option calving_domain = 1 = CALVING_DOMAIN_EVERYWHERE (glide_types.F90:200; the trace's calving_domain column is 1 on every row)"
    },
    "timescale": {
      "type": "parameter",
      "units": "yr",
      "default": 0.0,
      "description": "calving timescale (yr; glide_types.F90:1648; 0 in the reference run - the full column calves at once; the trace's timescale column)"
    },
    "dt": {
      "type": "parameter",
      "units": "yr",
      "default": 0.5,
      "description": "model time step (yr; the reference run's dt = 0.5 yr; used only when timescale > 0)"
    },
    "ice_mask": {
      "type": "unknown",
      "units": "1",
      "description": "ice-presence mask ice_mask = 1 where thck > thklim (glissade_masks.F90:165-169; with the law's thklim = 0: thck > 0)"
    },
    "floating_mask": {
      "type": "unknown",
      "units": "1",
      "description": "floating-ice mask floating_mask = 1 where ice is present and topg - eus < -(rhoi/rhoo)*thck (glissade_masks.F90:179-185)"
    },
    "calving_domain_mask": {
      "type": "unknown",
      "units": "1",
      "description": "calving-domain mask: with CALVING_DOMAIN_EVERYWHERE (the reference option) it is identically 1 (calve_ice_basic, glissade_calving.F90:1169-1172); the CALVING_DOMAIN_OCEAN_EDGE alternative (floating with an ocean neighbor, F90:1153-1154) is not used by the reference run and is carried by the trace's margin_mask column as a dumped input"
    },
    "calving_fraction": {
      "type": "unknown",
      "units": "1",
      "description": "fraction of the column removed in a calving cell: 1.0 for timescale = 0, else min(dt/timescale, 1) (calve_ice_basic, F90:1065-1077)"
    },
    "calving_thck": {
      "type": "unknown",
      "units": "m",
      "description": "thickness removed by the calving law: calving_fraction*thck where floating and inside the calving domain, else 0 (F90:1184; with the reference options: thck in full)"
    },
    "thck_after": {
      "type": "unknown",
      "units": "m",
      "description": "thickness after the calving law, thck - calving_thck (F90:1185)"
    }
  },
  "equations": [
    {
      "lhs": "ice_mask",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": ">",
            "args": [
              "thck",
              "thklim"
            ]
          },
          {
            "op": "const",
            "args": [],
            "value": 1.0,
            "units": "1"
          },
          {
            "op": "const",
            "args": [],
            "value": 0.0,
            "units": "1"
          }
        ]
      }
    },
    {
      "lhs": "floating_mask",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "cism_floating_mask",
        "bindings": {
          "thck": "thck",
          "topg": "topg",
          "eus": "eus",
          "thklim": "thklim",
          "rhoi": "rhoi",
          "rhoo": "rhoo"
        }
      }
    },
    {
      "lhs": "calving_domain_mask",
      "rhs": {
        "op": "const",
        "args": [],
        "value": 1.0,
        "units": "1"
      }
    },
    {
      "lhs": "calving_fraction",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "==",
            "args": [
              "timescale",
              {
                "op": "const",
                "args": [],
                "value": 0.0,
                "units": "yr"
              }
            ]
          },
          {
            "op": "const",
            "args": [],
            "value": 1.0,
            "units": "1"
          },
          {
            "op": "min",
            "args": [
              {
                "op": "/",
                "args": [
                  "dt",
                  "timescale"
                ]
              },
              {
                "op": "const",
                "args": [],
                "value": 1.0,
                "units": "1"
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "calving_thck",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "cism_calving_float_zero",
        "bindings": {
          "floating_mask": "floating_mask",
          "calving_domain_mask": "calving_domain_mask",
          "calving_fraction": "calving_fraction",
          "thck": "thck"
        }
      }
    },
    {
      "lhs": "thck_after",
      "rhs": {
        "op": "-",
        "args": [
          "thck",
          "calving_thck"
        ]
      }
    }
  ],
  "tests": [
    {
      "id": "calving_thin_step1_cell21128",
      "description": "Dump pin, cism_calving.csv row (cism_step 1, cell 21,128), the thinnest active calving cell of step 1: with thck_pre = 1.2836174650601692e-21 m, topg = -395.1099853515625 m and eus = 0 m the cell is floating (flotation depth -(rhoi/rhoo)*thck_pre = -1.14725e-21 m with rhoi/rhoo = 917/1026, glimmer_physcon.F90:41-42), so the CALVING_FLOAT_ZERO law with thklim = 0, calving_domain = CALVING_DOMAIN_EVERYWHERE and timescale = 0 (calve_ice_basic, glissade_calving.F90:1065-1188) removes the whole column: ice_mask = floating_mask = 1, calving_thck = thck_pre and thck_after = 0.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "thck": 1.2836174650601692e-21,
        "topg": -395.1099853515625,
        "eus": 0.0,
        "thklim": 0.0,
        "timescale": 0.0
      },
      "assertions": [
        {
          "variable": "ice_mask",
          "time": 0.0,
          "expected": 1.0,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "floating_mask",
          "time": 0.0,
          "expected": 1.0,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "calving_thck",
          "time": 0.0,
          "expected": 1.2836174650601692e-21,
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
      "id": "calving_thick_step1_cell61111",
      "description": "Dump pin, cism_calving.csv row (cism_step 1, cell 61,111), the thickest active calving cell of step 1: with thck_pre = 0.0015736733963963045 m, topg = -37.31972885131836 m and eus = 0 m the cell is floating (flotation depth -(rhoi/rhoo)*thck_pre = -0.00140649 m), so the CALVING_FLOAT_ZERO law with thklim = 0, calving_domain = CALVING_DOMAIN_EVERYWHERE and timescale = 0 removes the whole column: ice_mask = floating_mask = 1, calving_thck = thck_pre and thck_after = 0.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "thck": 0.0015736733963963045,
        "topg": -37.31972885131836,
        "eus": 0.0,
        "thklim": 0.0,
        "timescale": 0.0
      },
      "assertions": [
        {
          "variable": "ice_mask",
          "time": 0.0,
          "expected": 1.0,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "floating_mask",
          "time": 0.0,
          "expected": 1.0,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "calving_thck",
          "time": 0.0,
          "expected": 0.0015736733963963045,
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
      "id": "calving_thin_step2_cell1396",
      "description": "Dump pin, cism_calving.csv row (cism_step 2, cell 13,96), the thinnest active calving cell of step 2: with thck_pre = 9.372644268114598e-17 m, topg = -215.70689392089844 m and eus = 0 m the cell is floating (flotation depth -(rhoi/rhoo)*thck_pre = -8.37692e-17 m), so the CALVING_FLOAT_ZERO law with thklim = 0, calving_domain = CALVING_DOMAIN_EVERYWHERE and timescale = 0 removes the whole column: ice_mask = floating_mask = 1, calving_thck = thck_pre and thck_after = 0.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "thck": 9.372644268114598e-17,
        "topg": -215.70689392089844,
        "eus": 0.0,
        "thklim": 0.0,
        "timescale": 0.0
      },
      "assertions": [
        {
          "variable": "ice_mask",
          "time": 0.0,
          "expected": 1.0,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "floating_mask",
          "time": 0.0,
          "expected": 1.0,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "calving_thck",
          "time": 0.0,
          "expected": 9.372644268114598e-17,
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
      "id": "calving_thick_step2_cell61111",
      "description": "Dump pin, cism_calving.csv row (cism_step 2, cell 61,111), the thickest active calving cell of step 2: with thck_pre = 0.0015745933506767895 m, topg = -37.31972885131836 m and eus = 0 m the cell is floating (flotation depth -(rhoi/rhoo)*thck_pre = -0.00140731 m), so the CALVING_FLOAT_ZERO law with thklim = 0, calving_domain = CALVING_DOMAIN_EVERYWHERE and timescale = 0 removes the whole column: ice_mask = floating_mask = 1, calving_thck = thck_pre and thck_after = 0.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "thck": 0.0015745933506767895,
        "topg": -37.31972885131836,
        "eus": 0.0,
        "thklim": 0.0,
        "timescale": 0.0
      },
      "assertions": [
        {
          "variable": "ice_mask",
          "time": 0.0,
          "expected": 1.0,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "floating_mask",
          "time": 0.0,
          "expected": 1.0,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "calving_thck",
          "time": 0.0,
          "expected": 0.0015745933506767895,
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
      "id": "calving_thin_step3_cell1393",
      "description": "Dump pin, cism_calving.csv row (cism_step 3, cell 13,93), the thinnest active calving cell of step 3: with thck_pre = 1.5873974488206867e-15 m, topg = -231.77479553222656 m and eus = 0 m the cell is floating (flotation depth -(rhoi/rhoo)*thck_pre = -1.41876e-15 m), so the CALVING_FLOAT_ZERO law with thklim = 0, calving_domain = CALVING_DOMAIN_EVERYWHERE and timescale = 0 removes the whole column: ice_mask = floating_mask = 1, calving_thck = thck_pre and thck_after = 0.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "thck": 1.5873974488206867e-15,
        "topg": -231.77479553222656,
        "eus": 0.0,
        "thklim": 0.0,
        "timescale": 0.0
      },
      "assertions": [
        {
          "variable": "ice_mask",
          "time": 0.0,
          "expected": 1.0,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "floating_mask",
          "time": 0.0,
          "expected": 1.0,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "calving_thck",
          "time": 0.0,
          "expected": 1.5873974488206867e-15,
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
      "id": "calving_thick_step3_cell61111",
      "description": "Dump pin, cism_calving.csv row (cism_step 3, cell 61,111), the thickest active calving cell of step 3: with thck_pre = 0.0015763388587808937 m, topg = -37.31972885131836 m and eus = 0 m the cell is floating (flotation depth -(rhoi/rhoo)*thck_pre = -0.00140887 m), so the CALVING_FLOAT_ZERO law with thklim = 0, calving_domain = CALVING_DOMAIN_EVERYWHERE and timescale = 0 removes the whole column: ice_mask = floating_mask = 1, calving_thck = thck_pre and thck_after = 0.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "thck": 0.0015763388587808937,
        "topg": -37.31972885131836,
        "eus": 0.0,
        "thklim": 0.0,
        "timescale": 0.0
      },
      "assertions": [
        {
          "variable": "ice_mask",
          "time": 0.0,
          "expected": 1.0,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "floating_mask",
          "time": 0.0,
          "expected": 1.0,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "calving_thck",
          "time": 0.0,
          "expected": 0.0015763388587808937,
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
      "id": "calving_thin_step4_cell4034",
      "description": "Dump pin, cism_calving.csv row (cism_step 4, cell 40,34), the thinnest active calving cell of step 4: with thck_pre = 1.7389280455254376e-20 m, topg = -52.79167175292969 m and eus = 0 m the cell is floating (flotation depth -(rhoi/rhoo)*thck_pre = -1.55419e-20 m), so the CALVING_FLOAT_ZERO law with thklim = 0, calving_domain = CALVING_DOMAIN_EVERYWHERE and timescale = 0 removes the whole column: ice_mask = floating_mask = 1, calving_thck = thck_pre and thck_after = 0.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "thck": 1.7389280455254376e-20,
        "topg": -52.79167175292969,
        "eus": 0.0,
        "thklim": 0.0,
        "timescale": 0.0
      },
      "assertions": [
        {
          "variable": "ice_mask",
          "time": 0.0,
          "expected": 1.0,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "floating_mask",
          "time": 0.0,
          "expected": 1.0,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "calving_thck",
          "time": 0.0,
          "expected": 1.7389280455254376e-20,
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
      "id": "calving_thick_step4_cell1494",
      "description": "Dump pin, cism_calving.csv row (cism_step 4, cell 14,94), the thickest active calving cell of step 4: with thck_pre = 11.483261284618747 m, topg = -10.755999565124512 m and eus = 0 m the cell is floating (flotation depth -(rhoi/rhoo)*thck_pre = -10.2633 m), so the CALVING_FLOAT_ZERO law with thklim = 0, calving_domain = CALVING_DOMAIN_EVERYWHERE and timescale = 0 removes the whole column: ice_mask = floating_mask = 1, calving_thck = thck_pre and thck_after = 0.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "thck": 11.483261284618747,
        "topg": -10.755999565124512,
        "eus": 0.0,
        "thklim": 0.0,
        "timescale": 0.0
      },
      "assertions": [
        {
          "variable": "ice_mask",
          "time": 0.0,
          "expected": 1.0,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "floating_mask",
          "time": 0.0,
          "expected": 1.0,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "calving_thck",
          "time": 0.0,
          "expected": 11.483261284618747,
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
      "id": "calving_margin_step4_cell1494",
      "description": "Dump pin, cism_calving.csv row (cism_step 4, cell 14,94), the active cell with the smallest |topg - eus + (rhoi/rhoo)*thck_pre| over the whole dump window (tightest flotation margin, pinning the rhoi/rhoo = 917/1026 flotation ratio most tightly): with thck_pre = 11.483261284618747 m, topg = -10.755999565124512 m and eus = 0 m, the CALVING_FLOAT_ZERO law with thklim = 0, calving_domain = CALVING_DOMAIN_EVERYWHERE and timescale = 0 removes the whole column: ice_mask = floating_mask = 1, calving_thck = thck_pre and thck_after = 0.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "thck": 11.483261284618747,
        "topg": -10.755999565124512,
        "eus": 0.0,
        "thklim": 0.0,
        "timescale": 0.0
      },
      "assertions": [
        {
          "variable": "ice_mask",
          "time": 0.0,
          "expected": 1.0,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "floating_mask",
          "time": 0.0,
          "expected": 1.0,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "calving_thck",
          "time": 0.0,
          "expected": 11.483261284618747,
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
      "id": "calving_grounded_step4_cell2749",
      "description": "Dump pin, cism_velo_marine_exit.csv row (cism_step 4, cell 27,49): grounded marine ice where the two forms of the flotation law disagree (the regression guard for the cism_floating_mask sign, wt/cism-calving3; rows selected by stage1/analysis/extract_cism_float_mask_pins.py - 32 such disagreement rows in the dump, all grounded marine ice with dumped floating_mask = 0, none of which the cism_calving.csv trace covers because the law's active-cell dump only traces cells whose calving-law mask is 1, i.e. floating cells): thck = 2143.8737313863753 m, topg = -6.78439998626709 m, eus = 0 m, dumped floating_mask = 0; topg - eus = -6.78439998626709 m is above the flotation depth -(rhoi/rhoo)*thck = -1916.1132667459124 m but below +0, so the flipped form topg - eus < +(rhoi/rhoo)*thck of the template body as merged from ff0e189 would mark this cell floating. The CALVING_FLOAT_ZERO law with thklim = 0, calving_domain = CALVING_DOMAIN_EVERYWHERE and timescale = 0 (calve_ice_basic, glissade_calving.F90:1065-1188) removes nothing from a grounded cell: ice_mask = 1, floating_mask = 0, calving_thck = 0 and thck_after = thck.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "thck": 2143.8737313863753,
        "topg": -6.78439998626709,
        "eus": 0.0,
        "thklim": 0.0,
        "timescale": 0.0
      },
      "assertions": [
        {
          "variable": "ice_mask",
          "time": 0.0,
          "expected": 1.0,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "floating_mask",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "calving_thck",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "thck_after",
          "time": 0.0,
          "expected": 2143.8737313863753,
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
