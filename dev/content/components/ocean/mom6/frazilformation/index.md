---
title: "FrazilFormation"
slug: "frazilformation"
domains: ["ocean"]
component_types: ["model"]
subdomains: ["mom6"]
domain: "ocean"
subdomain: "mom6"
component_type: "model"
esm_version: "1.3.0"
esm_path: "components/ocean/mom6/mom6_frazil.esm"
reference: "https://github.com/ESCOMP/CESM"
description: "Stage-2 implementation of MOM6 frazil formation in the diabatic column (make_frazil, MOM_diabatic_aux.F90:122-250 of the instrumented fork stage1/EqESM-cesm-mom6; run configuration C_JRA_t62_mom6_inst: TFREEZE_FORM=LINEAR with the Fortran defaults TFREEZE_S0_P0=0.0 degC and DTFREEZE_DS=-0.054 degC ppt-1 and DTFREEZE_DP=-7.75e-8 degC Pa-1 from the run's MOM_input, PRESSURE_DEPENDENT_FRAZIL=True, RHO_0=1035 kg m-3 and G_EARTH=9.8 m s-2 at their MOM6 defaults, C_P=3992 J kg-1 degC-1 from MOM_input, all unit rescale factors 1.0). The model evaluates the per-layer in-situ pressure as the hydrostatic cumulative integral of the constant gradient dpdz = RHO_0*g_Earth over the layer-thickness measure h (the composite-midpoint form of the F90:176-179 accumulation, lowered by the shared ./mom6_column_discretization.esm rules (the integral_lev_cumulative_from_bottom import of grids/column_nonuniform_1d, renamed lev -> layer at the 9.7.7 edge, the same import path mom6_kpp.esm uses)), the LINEAR freezing-point law (the linear_tfreeze expression template of ./mom6_templates.esm, calculate_TFreeze_linear_scalar, MOM_TFreeze.F90:62), the layer heat capacities hc = RHO_0*C_P*h (F90:190), and the per-layer branch law of the frazil scan: the supercooling supercooling_k = max(0, T_freeze_k - T_before_k) (the F90:228 trigger tv%T(k) < T_freeze(k)), the outcome T_after_k = T_before_k + supercooling_k (F90:230 warms a supercooled layer to the freezing point), and the column heat requirement fraz_col = sum_k hc_k*supercooling_k accumulated into tv%frazil (F90:229, 232, 238). In the traced window no layer is supercooled and no frazil heat is pending (all 312 rows of mom6_frazil.csv: T_before >= T_freeze everywhere, frazil_in == 0), so supercooling == 0, T_after == T_before, fraz_col == 0 and frazil_out == frazil_in == 0, and the column heat balance frazil_out - frazil_in == RHO_0*C_P*sum_k h_k*(T_after_k - T_before_k) (== 0) holds: the heat deficit added to tv%frazil equals the heat the column gains by warming to the freezing point. The formation branch's sequential bottom-up scan with its cross-layer partial-warming coupling (F90:207-234), the thin-layer exception (F90:219-224) and the reclaim branch (F90:183-205) are data-dependent and unexercised in the traced window; they are listed as gaps in README.md."
tags: ["ocean", "mom6", "model", "frazil", "sea-ice-formation", "cesm"]
---

## Description

Stage-2 implementation of MOM6 frazil formation in the diabatic column (make_frazil, MOM_diabatic_aux.F90:122-250 of the instrumented fork stage1/EqESM-cesm-mom6; run configuration C_JRA_t62_mom6_inst: TFREEZE_FORM=LINEAR with the Fortran defaults TFREEZE_S0_P0=0.0 degC and DTFREEZE_DS=-0.054 degC ppt-1 and DTFREEZE_DP=-7.75e-8 degC Pa-1 from the run's MOM_input, PRESSURE_DEPENDENT_FRAZIL=True, RHO_0=1035 kg m-3 and G_EARTH=9.8 m s-2 at their MOM6 defaults, C_P=3992 J kg-1 degC-1 from MOM_input, all unit rescale factors 1.0). The model evaluates the per-layer in-situ pressure as the hydrostatic cumulative integral of the constant gradient dpdz = RHO_0*g_Earth over the layer-thickness measure h (the composite-midpoint form of the F90:176-179 accumulation, lowered by the shared ./mom6_column_discretization.esm rules (the integral_lev_cumulative_from_bottom import of grids/column_nonuniform_1d, renamed lev -> layer at the 9.7.7 edge, the same import path mom6_kpp.esm uses)), the LINEAR freezing-point law (the linear_tfreeze expression template of ./mom6_templates.esm, calculate_TFreeze_linear_scalar, MOM_TFreeze.F90:62), the layer heat capacities hc = RHO_0*C_P*h (F90:190), and the per-layer branch law of the frazil scan: the supercooling supercooling_k = max(0, T_freeze_k - T_before_k) (the F90:228 trigger tv%T(k) < T_freeze(k)), the outcome T_after_k = T_before_k + supercooling_k (F90:230 warms a supercooled layer to the freezing point), and the column heat requirement fraz_col = sum_k hc_k*supercooling_k accumulated into tv%frazil (F90:229, 232, 238). In the traced window no layer is supercooled and no frazil heat is pending (all 312 rows of mom6_frazil.csv: T_before >= T_freeze everywhere, frazil_in == 0), so supercooling == 0, T_after == T_before, fraz_col == 0 and frazil_out == frazil_in == 0, and the column heat balance frazil_out - frazil_in == RHO_0*C_P*sum_k h_k*(T_after_k - T_before_k) (== 0) holds: the heat deficit added to tv%frazil equals the heat the column gains by warming to the freezing point. The formation branch's sequential bottom-up scan with its cross-layer partial-warming coupling (F90:207-234), the thin-layer exception (F90:219-224) and the reclaim branch (F90:183-205) are data-dependent and unexercised in the traced window; they are listed as gaps in README.md.

## Reference

- MOM6 (Modular Ocean Model 6), ESCOMP/CESM components/mom (dev/ncar_260909 @301879336; instrumented fork stage1/EqESM-cesm-mom6 branch instrument/mom6-dumps, reference run C_JRA_t62_mom6_inst): src/parameterizations/vertical/MOM_diabatic_aux.F90 (make_frazil 122-250) and src/ice_shelf/MOM_TFreeze.F90 (calculate_TFreeze_linear_scalar 51-64) - the reference implementation these components are transcribed from.
- EarthSciModels - the authoritative .esm corpus this component lives in.

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `h` | `m` | `0.0` | Layer thicknesses as consumed by the pressure accumulation and the layer heat capacities (F90:176-179, 190), [m] |
| `S` | `ppt` | `0.0` | Layer salinities at which the freezing point is evaluated (F90:187-188, 213-214), [ppt] |
| `T_before` | `degC` | `0.0` | Layer temperatures at make_frazil entry (the dump column T_before_k), [degC] |
| `p_surf` | `Pa` | `0.0` | Surface pressure ps passed to make_frazil (fluxes%p_surf_full; the dump column p_surf), [Pa] |
| `frazil_in` | `J/m^2` | `0.0` | Pending frazil heat deficit tv%frazil at make_frazil entry (the dump column frazil_in), [J m-2] |
| `RHO_0` | `kg/m^3` | `1035.0` | GV%Rho0, the mean seawater density of the Boussinesq reference state (MOM_verticalGrid.F90:135-140; default 1035.0, not overridden in the reference run's MOM_input), [kg m-3] |
| `C_P` | `J/kg/degC` | `3992.0` | tv%C_p, the seawater heat capacity (MOM_input C_P = 3992.0 in the reference run), [J kg-1 degC-1] |
| `g_Earth` | `m/s^2` | `9.8` | GV%g_Earth, the gravitational acceleration of the Earth (MOM_verticalGrid.F90:130-132; default 9.80 m s-2, not overridden in the reference run), [m s-2] |
| `TFREEZE_S0_P0` | `degC` | `0.0` | The LINEAR freezing-point law's reference temperature TFREEZE_S0_P0 (MOM_TFreeze.F90:74-77; default 0.0 degC), [degC] |
| `DTFREEZE_DS` | `degC/ppt` | `-0.054` | The LINEAR freezing-point law's salinity coefficient DTFREEZE_DS (MOM_TFreeze.F90:78-83; default -0.054 degC ppt-1), [degC ppt-1] |
| `DTFREEZE_DP` | `degC/Pa` | `-7.75e-08` | The LINEAR freezing-point law's pressure coefficient DTFREEZE_DP (MOM_TFreeze.F90:85-91; -7.75e-8 degC Pa-1 in the reference run's MOM_input), [degC Pa-1] |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `dz` | `m` |  | The layer-thickness measure of the column integrals (the free-name dz of the imported integral rule), dz_k = h_k, [m] |
| `z_sfc` | `m` |  | The surface bound of the integral rules: the ocean surface, coordinate 0 of the depth axis (carries no numeric weight in the lowering, esm-spec 4.2), [m] |
| `dpdz` | `Pa/m` |  | The hydrostatic pressure gradient of the Boussinesq reference state, dpdz = g_Earth*RHO_0, constant over the column (F90:176 H_to_RL2_T2 = GV%H_to_RZ*GV%g_Earth with H_to_RZ = RHO_0 under Boussinesq and unit rescaling), [Pa m-1] |
| `pressure` | `Pa` |  | In-situ pressure at a layer's mid-depth, pressure_k = p_surf + integral(dpdz, z_sfc -> layer)_k, the cumulative hydrostatic integral of F90:176,179 (the composite midpoint sum sum_{j<k} dpdz*h_j + dpdz*h_k/2), the dump column p_k, [Pa] |
| `T_freeze` | `degC` |  | The LINEAR freezing-point law evaluated at (S_k, pressure_k) via calculate_TFreeze (F90:187-188, 213-214; the dump column T_freeze_k), [degC] |
| `hc` | `J/m^2/degC` |  | A layer's heat capacity hc = (tv%C_p*GV%H_to_RZ)*h_k (F90:190), [J m-2 degC-1] |
| `supercooling` | `degC` |  | A layer's supercooling supercooling_k = max(0, T_freeze_k - T_before_k), the heat-deficit branch condition of the frazil scan (F90:228 triggers on tv%T(k) < T_freeze(k)); 0 on every traced layer (no layer is supercooled in the window), [degC] |
| `T_after` | `degC` |  | Layer temperatures at make_frazil exit, T_after_k = T_before_k + supercooling_k: a supercooled layer warms to the freezing point (F90:230), a non-supercooled layer is unchanged (the dump column T_after_k; == T_before_k bitwise on all 312 traced rows), [degC] |
| `fraz_col` | `J/m^2` |  | The column frazil heat requirement fraz_col = sum_k hc_k*supercooling_k accumulated by the formation scan (F90:229, 232; the dump column fraz_col; 0.0 on all traced rows), [J m-2] |
| `frazil_out` | `J/m^2` |  | tv%frazil at make_frazil exit, frazil_in + fraz_col (F90:238; the dump column frazil_out), [J m-2] |

## Observed expressions

$$
dz = h
$$
_The layer-thickness measure of the column integrals (the free-name dz of the imported integral rule), dz_k = h_k, [m]_

$$
z_{sfc} = \mathrm{const}\left(\right)
$$
_The surface bound of the integral rules: the ocean surface, coordinate 0 of the depth axis (carries no numeric weight in the lowering, esm-spec 4.2), [m]_

$$
dpdz = \mathrm{faq}\left(g_{Earth}, RHO_{0}\right)
$$
_The hydrostatic pressure gradient of the Boussinesq reference state, dpdz = g_Earth*RHO_0, constant over the column (F90:176 H_to_RL2_T2 = GV%H_to_RZ*GV%g_Earth with H_to_RZ = RHO_0 under Boussinesq and unit rescaling), [Pa m-1]_

$$
pressure = p_{surf} + \mathrm{integral}\left(dpdz\right)
$$
_In-situ pressure at a layer's mid-depth, pressure_k = p_surf + integral(dpdz, z_sfc -> layer)_k, the cumulative hydrostatic integral of F90:176,179 (the composite midpoint sum sum_{j<k} dpdz*h_j + dpdz*h_k/2), the dump column p_k, [Pa]_

$$
T_{freeze} = \mathrm{faq}\left(S, pressure\right)
$$
_The LINEAR freezing-point law evaluated at (S_k, pressure_k) via calculate_TFreeze (F90:187-188, 213-214; the dump column T_freeze_k), [degC]_

$$
hc = \mathrm{faq}\left(h\right)
$$
_A layer's heat capacity hc = (tv%C_p*GV%H_to_RZ)*h_k (F90:190), [J m-2 degC-1]_

$$
supercooling = \mathrm{faq}\left(T_{freeze}, T_{before}\right)
$$
_A layer's supercooling supercooling_k = max(0, T_freeze_k - T_before_k), the heat-deficit branch condition of the frazil scan (F90:228 triggers on tv%T(k) < T_freeze(k)); 0 on every traced layer (no layer is supercooled in the window), [degC]_

$$
T_{after} = \mathrm{faq}\left(T_{before}, supercooling\right)
$$
_Layer temperatures at make_frazil exit, T_after_k = T_before_k + supercooling_k: a supercooled layer warms to the freezing point (F90:230), a non-supercooled layer is unchanged (the dump column T_after_k; == T_before_k bitwise on all 312 traced rows), [degC]_

$$
fraz_{col} = \mathrm{faq}\left(hc, supercooling\right)
$$
_The column frazil heat requirement fraz_col = sum_k hc_k*supercooling_k accumulated by the formation scan (F90:229, 232; the dump column fraz_col; 0.0 on all traced rows), [J m-2]_

$$
frazil_{out} = frazil_{in} + fraz_{col}
$$
_tv%frazil at make_frazil exit, frazil_in + fraz_col (F90:238; the dump column frazil_out), [J m-2]_

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "expression_template_imports": [
    {
      "ref": "./mom6_templates.esm"
    },
    {
      "ref": "./mom6_column_discretization.esm"
    }
  ],
  "variables": {
    "h": {
      "type": "parameter",
      "shape": [
        "layer"
      ],
      "units": "m",
      "default": 0.0,
      "description": "Layer thicknesses as consumed by the pressure accumulation and the layer heat capacities (F90:176-179, 190), [m]"
    },
    "S": {
      "type": "parameter",
      "shape": [
        "layer"
      ],
      "units": "ppt",
      "default": 0.0,
      "description": "Layer salinities at which the freezing point is evaluated (F90:187-188, 213-214), [ppt]"
    },
    "T_before": {
      "type": "parameter",
      "shape": [
        "layer"
      ],
      "units": "degC",
      "default": 0.0,
      "description": "Layer temperatures at make_frazil entry (the dump column T_before_k), [degC]"
    },
    "p_surf": {
      "type": "parameter",
      "units": "Pa",
      "default": 0.0,
      "description": "Surface pressure ps passed to make_frazil (fluxes%p_surf_full; the dump column p_surf), [Pa]"
    },
    "frazil_in": {
      "type": "parameter",
      "units": "J/m^2",
      "default": 0.0,
      "description": "Pending frazil heat deficit tv%frazil at make_frazil entry (the dump column frazil_in), [J m-2]"
    },
    "RHO_0": {
      "type": "parameter",
      "units": "kg/m^3",
      "default": 1035.0,
      "description": "GV%Rho0, the mean seawater density of the Boussinesq reference state (MOM_verticalGrid.F90:135-140; default 1035.0, not overridden in the reference run's MOM_input), [kg m-3]"
    },
    "C_P": {
      "type": "parameter",
      "units": "J/kg/degC",
      "default": 3992.0,
      "description": "tv%C_p, the seawater heat capacity (MOM_input C_P = 3992.0 in the reference run), [J kg-1 degC-1]"
    },
    "g_Earth": {
      "type": "parameter",
      "units": "m/s^2",
      "default": 9.8,
      "description": "GV%g_Earth, the gravitational acceleration of the Earth (MOM_verticalGrid.F90:130-132; default 9.80 m s-2, not overridden in the reference run), [m s-2]"
    },
    "TFREEZE_S0_P0": {
      "type": "parameter",
      "units": "degC",
      "default": 0.0,
      "description": "The LINEAR freezing-point law's reference temperature TFREEZE_S0_P0 (MOM_TFreeze.F90:74-77; default 0.0 degC), [degC]"
    },
    "DTFREEZE_DS": {
      "type": "parameter",
      "units": "degC/ppt",
      "default": -0.054,
      "description": "The LINEAR freezing-point law's salinity coefficient DTFREEZE_DS (MOM_TFreeze.F90:78-83; default -0.054 degC ppt-1), [degC ppt-1]"
    },
    "DTFREEZE_DP": {
      "type": "parameter",
      "units": "degC/Pa",
      "default": -7.75e-08,
      "description": "The LINEAR freezing-point law's pressure coefficient DTFREEZE_DP (MOM_TFreeze.F90:85-91; -7.75e-8 degC Pa-1 in the reference run's MOM_input), [degC Pa-1]"
    },
    "dz": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "m",
      "description": "The layer-thickness measure of the column integrals (the free-name dz of the imported integral rule), dz_k = h_k, [m]"
    },
    "z_sfc": {
      "type": "unknown",
      "units": "m",
      "description": "The surface bound of the integral rules: the ocean surface, coordinate 0 of the depth axis (carries no numeric weight in the lowering, esm-spec 4.2), [m]"
    },
    "dpdz": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "Pa/m",
      "description": "The hydrostatic pressure gradient of the Boussinesq reference state, dpdz = g_Earth*RHO_0, constant over the column (F90:176 H_to_RL2_T2 = GV%H_to_RZ*GV%g_Earth with H_to_RZ = RHO_0 under Boussinesq and unit rescaling), [Pa m-1]"
    },
    "pressure": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "Pa",
      "description": "In-situ pressure at a layer's mid-depth, pressure_k = p_surf + integral(dpdz, z_sfc -> layer)_k, the cumulative hydrostatic integral of F90:176,179 (the composite midpoint sum sum_{j<k} dpdz*h_j + dpdz*h_k/2), the dump column p_k, [Pa]"
    },
    "T_freeze": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "degC",
      "description": "The LINEAR freezing-point law evaluated at (S_k, pressure_k) via calculate_TFreeze (F90:187-188, 213-214; the dump column T_freeze_k), [degC]"
    },
    "hc": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "J/m^2/degC",
      "description": "A layer's heat capacity hc = (tv%C_p*GV%H_to_RZ)*h_k (F90:190), [J m-2 degC-1]"
    },
    "supercooling": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "degC",
      "description": "A layer's supercooling supercooling_k = max(0, T_freeze_k - T_before_k), the heat-deficit branch condition of the frazil scan (F90:228 triggers on tv%T(k) < T_freeze(k)); 0 on every traced layer (no layer is supercooled in the window), [degC]"
    },
    "T_after": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "degC",
      "description": "Layer temperatures at make_frazil exit, T_after_k = T_before_k + supercooling_k: a supercooled layer warms to the freezing point (F90:230), a non-supercooled layer is unchanged (the dump column T_after_k; == T_before_k bitwise on all 312 traced rows), [degC]"
    },
    "fraz_col": {
      "type": "unknown",
      "units": "J/m^2",
      "description": "The column frazil heat requirement fraz_col = sum_k hc_k*supercooling_k accumulated by the formation scan (F90:229, 232; the dump column fraz_col; 0.0 on all traced rows), [J m-2]"
    },
    "frazil_out": {
      "type": "unknown",
      "units": "J/m^2",
      "description": "tv%frazil at make_frazil exit, frazil_in + fraz_col (F90:238; the dump column frazil_out), [J m-2]"
    }
  },
  "equations": [
    {
      "lhs": "dz",
      "rhs": "h"
    },
    {
      "lhs": "z_sfc",
      "rhs": {
        "op": "const",
        "args": [],
        "value": 0.0,
        "units": "m"
      }
    },
    {
      "lhs": "dpdz",
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
          "op": "*",
          "args": [
            "g_Earth",
            "RHO_0"
          ]
        },
        "args": [
          "g_Earth",
          "RHO_0"
        ]
      }
    },
    {
      "lhs": "pressure",
      "rhs": {
        "op": "+",
        "args": [
          "p_surf",
          {
            "op": "integral",
            "args": [
              "dpdz"
            ],
            "var": "layer",
            "lower": "z_sfc",
            "upper": "layer"
          }
        ]
      }
    },
    {
      "lhs": "T_freeze",
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
          "name": "linear_tfreeze",
          "bindings": {
            "TFREEZE_S0_P0": "TFREEZE_S0_P0",
            "DTFREEZE_DS": "DTFREEZE_DS",
            "DTFREEZE_DP": "DTFREEZE_DP",
            "S": {
              "op": "index",
              "args": [
                "S",
                "i"
              ]
            },
            "p": {
              "op": "index",
              "args": [
                "pressure",
                "i"
              ]
            }
          }
        },
        "args": [
          "S",
          "pressure"
        ]
      }
    },
    {
      "lhs": "hc",
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
          "op": "*",
          "args": [
            {
              "op": "*",
              "args": [
                "RHO_0",
                "C_P"
              ]
            },
            {
              "op": "index",
              "args": [
                "h",
                "i"
              ]
            }
          ]
        },
        "args": [
          "h"
        ]
      }
    },
    {
      "lhs": "supercooling",
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
          "op": "max",
          "args": [
            {
              "op": "const",
              "args": [],
              "value": 0.0,
              "units": "degC"
            },
            {
              "op": "-",
              "args": [
                {
                  "op": "index",
                  "args": [
                    "T_freeze",
                    "i"
                  ]
                },
                {
                  "op": "index",
                  "args": [
                    "T_before",
                    "i"
                  ]
                }
              ]
            }
          ]
        },
        "args": [
          "T_freeze",
          "T_before"
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
                "T_before",
                "i"
              ]
            },
            {
              "op": "index",
              "args": [
                "supercooling",
                "i"
              ]
            }
          ]
        },
        "args": [
          "T_before",
          "supercooling"
        ]
      }
    },
    {
      "lhs": "fraz_col",
      "rhs": {
        "op": "faq",
        "output_idx": [],
        "reduce": "+",
        "ranges": {
          "j": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "*",
          "args": [
            {
              "op": "index",
              "args": [
                "hc",
                "j"
              ]
            },
            {
              "op": "index",
              "args": [
                "supercooling",
                "j"
              ]
            }
          ]
        },
        "args": [
          "hc",
          "supercooling"
        ]
      }
    },
    {
      "lhs": "frazil_out",
      "rhs": {
        "op": "+",
        "args": [
          "frazil_in",
          "fraz_col"
        ]
      }
    }
  ],
  "tests": [
    {
      "id": "frazil_t3600_g3j78_c1",
      "description": "mom6_frazil.csv row (tod, gi, gj, call) = (3600, 3, 78, 1): the pre-diabatic make_frazil call of the first thermo step of the traced column (3, 78). Pins the hydrostatic cumulative integral (pressure at layers 1, 20, 47, 60, 75), the LINEAR freezing-point law (T_freeze at the same layers), and the no-formation branch law: the branch-condition supercooling == 0 at layers 47 and 48 (layer 47 is the layer closest to freezing, T_before - T_freeze = 0.1753 degC, layer 48 the second-closest at 0.1780 degC) and the column heat requirement fraz_col == 0. Values are dump columns (mom6_frazil.csv) except supercooling (derived, not a dump column: max(0, T_freeze - T_before)) and fraz_col (the dump column, reproduced by the branch-law sum sum_k hc_k*supercooling_k).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "h": [
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
        "S": [
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
          -1.9368465097462928,
          -1.1068531682136094,
          -0.6951833259707765,
          -0.6951334044311067,
          -0.6951243465133399,
          -0.6951243459722233,
          -0.6951243459884608,
          -0.6951243460031444,
          -0.695124346016283,
          -0.6951243460279016,
          -0.6951243460380736,
          -0.6951243460470161,
          -0.6951243460553768,
          -0.6951243460650647,
          -0.6951243460816838,
          -0.6951243461216231,
          -0.695124346232723,
          -0.6951243465544502,
          -0.6951243474930505,
          -0.6951243502311716
        ],
        "p_surf": 99753.85917574639,
        "frazil_in": 0.0
      },
      "tolerance": {
        "rel": 1e-12
      },
      "assertions": [
        {
          "variable": "pressure",
          "time": 0.0,
          "expected": 112462.7909604987,
          "coords": {
            "layer": 1
          }
        },
        {
          "variable": "T_freeze",
          "time": 0.0,
          "expected": -1.822743643366657,
          "coords": {
            "layer": 1
          }
        },
        {
          "variable": "pressure",
          "time": 0.0,
          "expected": 936825.5485584434,
          "coords": {
            "layer": 20
          }
        },
        {
          "variable": "T_freeze",
          "time": 0.0,
          "expected": -1.9289419612473826,
          "coords": {
            "layer": 20
          }
        },
        {
          "variable": "pressure",
          "time": 0.0,
          "expected": 2739332.300009568,
          "coords": {
            "layer": 47
          }
        },
        {
          "variable": "T_freeze",
          "time": 0.0,
          "expected": -2.072416708990133,
          "coords": {
            "layer": 47
          }
        },
        {
          "variable": "pressure",
          "time": 0.0,
          "expected": 5729439.790250093,
          "coords": {
            "layer": 60
          }
        },
        {
          "variable": "T_freeze",
          "time": 0.0,
          "expected": -2.315439560677971,
          "coords": {
            "layer": 60
          }
        },
        {
          "variable": "pressure",
          "time": 0.0,
          "expected": 5729591.929505189,
          "coords": {
            "layer": 75
          }
        },
        {
          "variable": "T_freeze",
          "time": 0.0,
          "expected": -2.3154513514662884,
          "coords": {
            "layer": 75
          }
        },
        {
          "variable": "supercooling",
          "time": 0.0,
          "expected": 0.0,
          "coords": {
            "layer": 47
          }
        },
        {
          "variable": "supercooling",
          "time": 0.0,
          "expected": 0.0,
          "coords": {
            "layer": 48
          }
        },
        {
          "variable": "fraz_col",
          "time": 0.0,
          "expected": 0.0
        }
      ]
    },
    {
      "id": "frazil_t3600_g3j78_c2",
      "description": "mom6_frazil.csv row (tod, gi, gj, call) = (3600, 3, 78, 2): the post-diabatic make_frazil call of the first thermo step (the state after the tracer vertical-diffusion solve). Pins the hydrostatic cumulative integral and the LINEAR freezing-point law at layers 1, 20, 47, 60, 75, and the no-formation branch law: supercooling == 0 at layers 47 and 48 (the two layers closest to freezing, margins T_before - T_freeze = 0.1661 and 0.1779 degC) and fraz_col == 0. Values are dump columns (mom6_frazil.csv) except supercooling (derived, not a dump column) and fraz_col (the dump column, reproduced by the branch-law sum).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "h": [
          2.505937959830134,
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
        "S": [
          33.592821497054686,
          33.59016757987681,
          33.590579562535936,
          33.7820127499342,
          33.9041186691469,
          33.96573892486835,
          34.00792163542461,
          34.07055811490504,
          34.148351994266115,
          34.21088248839258,
          34.244727937951836,
          34.25234141242352,
          34.26230151749832,
          34.27100171938577,
          34.30332945582841,
          34.33954264049526,
          34.34303351771804,
          34.34967383853876,
          34.36551576783358,
          34.37661771319154,
          34.383047201672646,
          34.38845791924443,
          34.39104144190381,
          34.39104187144943,
          34.3912652122478,
          34.396396851396545,
          34.40919774618177,
          34.417967673874074,
          34.424377950340435,
          34.42839971404339,
          34.43010958650064,
          34.43086652251297,
          34.431794242543546,
          34.432976820841766,
          34.434449505961624,
          34.43611134357104,
          34.4379828249702,
          34.43994139828235,
          34.442028216398356,
          34.44430373575145,
          34.44610954845737,
          34.44726183030929,
          34.4476374210173,
          34.44764589593479,
          34.44746696357514,
          34.446873033589945,
          34.4459985697631,
          34.445956465016806,
          34.44591312978192,
          34.450896653160136,
          34.455128471350555,
          34.45887855626845,
          34.46460325479459,
          34.47257833672675,
          34.47697582645556,
          34.47696461715757,
          34.61927444142477,
          34.61928480331004,
          34.61929183516097,
          34.61929653464631,
          34.619297874234356,
          34.619304430327446,
          34.61931041838488,
          34.61931584233179,
          34.619320706820105,
          34.61932501744165,
          34.619328781024514,
          34.61933200605497,
          34.619334703294776,
          34.61933688671342,
          34.6193385749499,
          34.619339793711575,
          34.619340579936605,
          34.61934091610266,
          34.61934108418691
        ],
        "T_before": [
          1.8967950667787645,
          1.872433367631375,
          1.8586110174180326,
          1.8888746535370076,
          1.8444025217565576,
          1.4333248389996531,
          1.1840260204057733,
          0.4551287096236492,
          -0.25315006045438687,
          -0.49118856691698687,
          -0.7744781884655084,
          -1.010739652435143,
          -1.2172285564058611,
          -1.4041456345691687,
          -1.5239304210250129,
          -1.5632017175724653,
          -1.5827284631789595,
          -1.5952696859656361,
          -1.6234308816962604,
          -1.6357523732933843,
          -1.6466763650749372,
          -1.6561385823397161,
          -1.6516538710936968,
          -1.6516332619017597,
          -1.6488560152420948,
          -1.6483709504470598,
          -1.6483278476358747,
          -1.648346822000947,
          -1.648351534084377,
          -1.6487562038365202,
          -1.7240744823596046,
          -1.7789238484082701,
          -1.7792971333726786,
          -1.7792933277673846,
          -1.7785591624219075,
          -1.752973304026943,
          -1.7492821807120429,
          -1.7492475583431648,
          -1.749373488089697,
          -1.7732838484479705,
          -1.8026847110689328,
          -1.823675416301705,
          -1.8369205468318144,
          -1.8485383208330488,
          -1.865436868632705,
          -1.8823281420682163,
          -1.9062947925989122,
          -1.9069118933211193,
          -1.9076319149956191,
          -1.9148075783276317,
          -1.912448819122959,
          -1.8815038097979733,
          -1.872423279869306,
          -1.8563092549262374,
          -1.8708096676527546,
          -1.9366773077454842,
          -0.994530569758493,
          -0.9944841024175344,
          -0.9944530536166883,
          -0.9944313725804529,
          -0.994420338723266,
          -0.994366337797397,
          -0.9943170156415817,
          -0.9942723399253677,
          -0.9942322723319338,
          -0.9941967668028063,
          -0.9941657670967691,
          -0.9941392033144334,
          -0.9941169868137648,
          -0.994099002531668,
          -0.9940850969431738,
          -0.9940750583030997,
          -0.994068582360976,
          -0.994065813443892,
          -0.9940644289753425
        ],
        "p_surf": 99753.85917574639,
        "frazil_in": 0.0
      },
      "tolerance": {
        "rel": 1e-12
      },
      "assertions": [
        {
          "variable": "pressure",
          "time": 0.0,
          "expected": 112462.72353902491,
          "coords": {
            "layer": 1
          }
        },
        {
          "variable": "T_freeze",
          "time": 0.0,
          "expected": -1.8227282219152274,
          "coords": {
            "layer": 1
          }
        },
        {
          "variable": "pressure",
          "time": 0.0,
          "expected": 936825.4137154958,
          "coords": {
            "layer": 20
          }
        },
        {
          "variable": "T_freeze",
          "time": 0.0,
          "expected": -1.9289413260752943,
          "coords": {
            "layer": 20
          }
        },
        {
          "variable": "pressure",
          "time": 0.0,
          "expected": 2739332.1651666206,
          "coords": {
            "layer": 47
          }
        },
        {
          "variable": "T_freeze",
          "time": 0.0,
          "expected": -2.0723821655676202,
          "coords": {
            "layer": 47
          }
        },
        {
          "variable": "pressure",
          "time": 0.0,
          "expected": 5729439.655407145,
          "coords": {
            "layer": 60
          }
        },
        {
          "variable": "T_freeze",
          "time": 0.0,
          "expected": -2.3134735861649545,
          "coords": {
            "layer": 60
          }
        },
        {
          "variable": "pressure",
          "time": 0.0,
          "expected": 5729591.794662241,
          "coords": {
            "layer": 75
          }
        },
        {
          "variable": "T_freeze",
          "time": 0.0,
          "expected": -2.3134877826324165,
          "coords": {
            "layer": 75
          }
        },
        {
          "variable": "supercooling",
          "time": 0.0,
          "expected": 0.0,
          "coords": {
            "layer": 47
          }
        },
        {
          "variable": "supercooling",
          "time": 0.0,
          "expected": 0.0,
          "coords": {
            "layer": 48
          }
        },
        {
          "variable": "fraz_col",
          "time": 0.0,
          "expected": 0.0
        }
      ]
    },
    {
      "id": "frazil_t3600_g7j80_c1",
      "description": "mom6_frazil.csv row (tod, gi, gj, call) = (3600, 7, 80, 1): the pre-diabatic call of the first thermo step of the second traced column (7, 80), a different column (shallower than (3, 78), layer 52 closest to freezing with T_before - T_freeze = 0.2906 degC). Pins the hydrostatic cumulative integral and the LINEAR freezing-point law at layers 1, 20, 52, 60, 75, and the no-formation branch law: supercooling == 0 at layers 52 and 53 (the two layers closest to freezing, margins 0.2906 and 0.2920 degC) and fraz_col == 0. Values are dump columns (mom6_frazil.csv) except supercooling (derived, not a dump column) and fraz_col (the dump column, reproduced by the branch-law sum).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "h": [
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
        "S": [
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
          -1.8907871589017267,
          -1.1930270087851709,
          -0.687572050541072,
          -0.6875672121267258,
          -0.6875605688029478,
          -0.6875605688154112,
          -0.6875605688362363,
          -0.6875605688566457,
          -0.6875605688766397,
          -0.6875605688962166,
          -0.687560568915374,
          -0.6875605689341069,
          -0.6875605689524066,
          -0.6875605689702579,
          -0.6875605689876311,
          -0.6875605690044672,
          -0.6875605690206295,
          -0.6875605690357489,
          -0.6875605690485359,
          -0.687560569055496,
          -0.6875605693684661
        ],
        "p_surf": 99843.79217433969,
        "frazil_in": 0.0
      },
      "tolerance": {
        "rel": 1e-12
      },
      "assertions": [
        {
          "variable": "pressure",
          "time": 0.0,
          "expected": 112457.1380540935,
          "coords": {
            "layer": 1
          }
        },
        {
          "variable": "T_freeze",
          "time": 0.0,
          "expected": -1.8159589590835858,
          "coords": {
            "layer": 1
          }
        },
        {
          "variable": "pressure",
          "time": 0.0,
          "expected": 936122.0336878779,
          "coords": {
            "layer": 20
          }
        },
        {
          "variable": "T_freeze",
          "time": 0.0,
          "expected": -1.925183019513806,
          "coords": {
            "layer": 20
          }
        },
        {
          "variable": "pressure",
          "time": 0.0,
          "expected": 3824113.985223228,
          "coords": {
            "layer": 52
          }
        },
        {
          "variable": "T_freeze",
          "time": 0.0,
          "expected": -2.1565884117358043,
          "coords": {
            "layer": 52
          }
        },
        {
          "variable": "pressure",
          "time": 0.0,
          "expected": 5189420.098657977,
          "coords": {
            "layer": 60
          }
        },
        {
          "variable": "T_freeze",
          "time": 0.0,
          "expected": -2.2735953168061522,
          "coords": {
            "layer": 60
          }
        },
        {
          "variable": "pressure",
          "time": 0.0,
          "expected": 5189572.256069808,
          "coords": {
            "layer": 75
          }
        },
        {
          "variable": "T_freeze",
          "time": 0.0,
          "expected": -2.273607109004936,
          "coords": {
            "layer": 75
          }
        },
        {
          "variable": "supercooling",
          "time": 0.0,
          "expected": 0.0,
          "coords": {
            "layer": 52
          }
        },
        {
          "variable": "supercooling",
          "time": 0.0,
          "expected": 0.0,
          "coords": {
            "layer": 53
          }
        },
        {
          "variable": "fraz_col",
          "time": 0.0,
          "expected": 0.0
        }
      ]
    },
    {
      "id": "frazil_t46800_g3j78_c1",
      "description": "mom6_frazil.csv row (tod, gi, gj, call) = (46800, 3, 78, 1): the pre-diabatic make_frazil call of the last traced thermo step (13 hours into the run). Pins the hydrostatic cumulative integral and the LINEAR freezing-point law at layers 1, 20, 47, 60, 75, and the no-formation branch law: supercooling == 0 at layers 47 and 46 (the two layers closest to freezing, margins T_before - T_freeze = 0.1763 and 0.1780 degC) and fraz_col == 0. Values are dump columns (mom6_frazil.csv) except supercooling (derived, not a dump column) and fraz_col (the dump column, reproduced by the branch-law sum).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "h": [
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
        "S": [
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
          -1.9349983502513706,
          -1.9197289254414085,
          -1.8521866831079816,
          -1.9197068031937863,
          -1.919718096110613,
          -1.919717696782256,
          -1.9197174913382609,
          -1.9197173193644077,
          -1.9197174294582067,
          -1.9197175246290026,
          -1.9197176048733646,
          -1.9197176707808292,
          -1.9197177233628484,
          -1.9197177639313816,
          -1.9197177939904708,
          -1.9197178151469834,
          -1.919717823392188,
          -1.9197178233709304,
          -1.919717823356777,
          -1.9197178233474523
        ],
        "p_surf": 99831.7513959237,
        "frazil_in": 0.0
      },
      "tolerance": {
        "rel": 1e-12
      },
      "assertions": [
        {
          "variable": "pressure",
          "time": 0.0,
          "expected": 112618.3676829421,
          "coords": {
            "layer": 1
          }
        },
        {
          "variable": "T_freeze",
          "time": 0.0,
          "expected": -1.8145785462895172,
          "coords": {
            "layer": 1
          }
        },
        {
          "variable": "pressure",
          "time": 0.0,
          "expected": 937287.7060779035,
          "coords": {
            "layer": 20
          }
        },
        {
          "variable": "T_freeze",
          "time": 0.0,
          "expected": -1.9287280058491745,
          "coords": {
            "layer": 20
          }
        },
        {
          "variable": "pressure",
          "time": 0.0,
          "expected": 2738278.396985214,
          "coords": {
            "layer": 47
          }
        },
        {
          "variable": "T_freeze",
          "time": 0.0,
          "expected": -2.0723192727258377,
          "coords": {
            "layer": 47
          }
        },
        {
          "variable": "pressure",
          "time": 0.0,
          "expected": 5719174.518015607,
          "coords": {
            "layer": 60
          }
        },
        {
          "variable": "T_freeze",
          "time": 0.0,
          "expected": -2.305171050561407,
          "coords": {
            "layer": 60
          }
        },
        {
          "variable": "pressure",
          "time": 0.0,
          "expected": 5719326.656845438,
          "coords": {
            "layer": 75
          }
        },
        {
          "variable": "T_freeze",
          "time": 0.0,
          "expected": -2.3051828435601185,
          "coords": {
            "layer": 75
          }
        },
        {
          "variable": "supercooling",
          "time": 0.0,
          "expected": 0.0,
          "coords": {
            "layer": 47
          }
        },
        {
          "variable": "supercooling",
          "time": 0.0,
          "expected": 0.0,
          "coords": {
            "layer": 46
          }
        },
        {
          "variable": "fraz_col",
          "time": 0.0,
          "expected": 0.0
        }
      ]
    }
  ]
}
```

</details>
