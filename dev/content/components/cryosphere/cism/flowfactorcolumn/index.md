---
title: "FlowFactorColumn"
slug: "flowfactorcolumn"
domains: ["cryosphere"]
component_types: ["model"]
subdomains: ["cism"]
domain: "cryosphere"
subdomain: "cism"
component_type: "model"
esm_version: "2.0.0"
esm_path: "components/cryosphere/cism/cism_flowlaw.esm"
reference: "https://github.com/ESCOMP/CESM"
description: "Stage-2 implementation of the CISM flow factor (stage 2 of the EqESM project; CISM = cismwrap_3_00_002 / cism_main_3.00_002 as built in CESM cesm3.0-alphabranch, reference run T1850Gg/f09_g17_gris20): the Paterson & Budd (1982) rate factor A(T*) = E * a * exp(-Q/(R*T*)) of glissade_flow_factor (libglissade/glissade_therm.F90:2408-2640) for the reference option FLWA_PATERSON_BUDD (flow_law = 2, F90:2585-2606): T* = tempcor + 273.15 with tempcor = clamp(temp - pmptemp, -50, 0) degC (the CISM-specific T* construction, F90:2596-2598, cism_templates.esm cism_tempcor), the (a, Q/R) pair switching at tempcor >= -10 degC (T* >= 263.15 K): (arrmlh, actenh/gascon) = (1.733e3, 139e3/8.314) above, (arrmll, actenl/gascon) = (3.613e-13, 60e3/8.314) below (glimmer_physcon.F90:94-102, the arrfact table of F90:2502-2506), and the flow enhancement factor E multiplying the rate factor (F90:2579, 2603, 2605; which_ho_flow_enhancement_factor = 0 gives E = flow_factor_ground = 1.0 in the reference config). The softness law itself is the same as PISM's Paterson-Budd law and is imported by reference from the EqIce ice_rheology_templates.esm pb_softness (CISM_LANE.md row 4: 'same law, same constants'; PISM's A_cold = 3.61e-13 differs from CISM's arrmll = 3.613e-13 in the third digit, so the CISM constants are bound at the call site), with the CISM-specific T* construction applied before it. The pressure melting point pmptemp = -rhoi*grav*pmlt*thck*stagsigma (F90:2170) and the layer column geometry (stagsigma) live in the temperature-solve component (a later lane) and are inputs here, exactly as the trace provides them. Tests pin the stage-1 instrumented trace cism_flowlaw.csv (one row per traced cell and layer, nlayers = 10, at each step; E = 1.0 and tempcor > -10 degC on every traced row - the reference window is warm-branch only - so the cold branch and the tempcor clamp bounds are pinned synthetically from the source formula, see README.md). The single model FlowFactorColumn applies the law elementwise over the 10-layer index set lev through the esm-spec 9.6.11 elementwise lift (the applications of the cism_tempcor and pb_softness templates are read per element when their arguments are the shaped temp/pmptemp/T_star, so the column model is the Fortran layer loop of glissade_flow_factor and is the single flow-law mount of the cism subassembly, fed by whole-array edges from the temperature solve); the scalar pointwise form of the law was factored out of the file in the wt/cism-calving3 round (nothing outside this file mounted it), with its single-layer pins re-expressed on the column model at the same dump rows (single-layer coords assertions)."
tags: ["cryosphere", "cism", "model", "ice-sheet", "rheology", "flow-law", "cesm"]
---

## Description

Stage-2 implementation of the CISM flow factor (stage 2 of the EqESM project; CISM = cismwrap_3_00_002 / cism_main_3.00_002 as built in CESM cesm3.0-alphabranch, reference run T1850Gg/f09_g17_gris20): the Paterson & Budd (1982) rate factor A(T*) = E * a * exp(-Q/(R*T*)) of glissade_flow_factor (libglissade/glissade_therm.F90:2408-2640) for the reference option FLWA_PATERSON_BUDD (flow_law = 2, F90:2585-2606): T* = tempcor + 273.15 with tempcor = clamp(temp - pmptemp, -50, 0) degC (the CISM-specific T* construction, F90:2596-2598, cism_templates.esm cism_tempcor), the (a, Q/R) pair switching at tempcor >= -10 degC (T* >= 263.15 K): (arrmlh, actenh/gascon) = (1.733e3, 139e3/8.314) above, (arrmll, actenl/gascon) = (3.613e-13, 60e3/8.314) below (glimmer_physcon.F90:94-102, the arrfact table of F90:2502-2506), and the flow enhancement factor E multiplying the rate factor (F90:2579, 2603, 2605; which_ho_flow_enhancement_factor = 0 gives E = flow_factor_ground = 1.0 in the reference config). The softness law itself is the same as PISM's Paterson-Budd law and is imported by reference from the EqIce ice_rheology_templates.esm pb_softness (CISM_LANE.md row 4: 'same law, same constants'; PISM's A_cold = 3.61e-13 differs from CISM's arrmll = 3.613e-13 in the third digit, so the CISM constants are bound at the call site), with the CISM-specific T* construction applied before it. The pressure melting point pmptemp = -rhoi*grav*pmlt*thck*stagsigma (F90:2170) and the layer column geometry (stagsigma) live in the temperature-solve component (a later lane) and are inputs here, exactly as the trace provides them. Tests pin the stage-1 instrumented trace cism_flowlaw.csv (one row per traced cell and layer, nlayers = 10, at each step; E = 1.0 and tempcor > -10 degC on every traced row - the reference window is warm-branch only - so the cold branch and the tempcor clamp bounds are pinned synthetically from the source formula, see README.md). The single model FlowFactorColumn applies the law elementwise over the 10-layer index set lev through the esm-spec 9.6.11 elementwise lift (the applications of the cism_tempcor and pb_softness templates are read per element when their arguments are the shaped temp/pmptemp/T_star, so the column model is the Fortran layer loop of glissade_flow_factor and is the single flow-law mount of the cism subassembly, fed by whole-array edges from the temperature solve); the scalar pointwise form of the law was factored out of the file in the wt/cism-calving3 round (nothing outside this file mounted it), with its single-layer pins re-expressed on the column model at the same dump rows (single-layer coords assertions).

## Reference

- CISM (Community Ice Sheet Model) cismwrap_3_00_002 / cism_main_3.00.002, as built in CESM cesm3.0-alphabranch (checkout stage1/cesm/components/cism, reference run T1850Gg/f09_g17_gris20): libglissade/glissade_basal_traction.F90, libglissade/glissade_therm.F90, libglissade/glissade_grid_operators.F90, libglissade/glissade_velo_higher.F90, libglissade/glissade_mass_balance.F90, libglissade/glissade_calving.F90, libglissade/glissade_masks.F90, libglissade/glissade_utils.F90, libglimmer/glimmer_physcon.F90, libglimmer/glimmer_utils.F90, libglide/glide_types.F90, libglide/glide_setup.F90, libglad/glad_main.F90, libglad/glad_timestep.F90, libglad/glad_output_states.F90, libglad/glad_output_fluxes.F90, drivers/cpl/nuopc/glc_import_export.F90 - the reference implementation these components are transcribed from.
- EarthSciModels - the authoritative .esm corpus this component lives in.

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `temp` | `degC` | `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]` | ice temperature in each layer (degC; the flowlaw trace's temp column on all 10 layers, equal to the transport-exit temperature profile) |
| `pmptemp` | `degC` | `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]` | pressure melting point temperature in each layer (degC; pmptemp = -rhoi*grav*pmlt*thck*stagsigma, F90:2170; the flowlaw trace's pmptemp column) |
| `E` | `1` | `1.0` | flow enhancement factor (which_ho_flow_enhancement_factor = 0: E = flow_factor_ground = 1.0 everywhere in the reference run; the dumped E column is 1.0 on every row) |
| `A_cold` | `Pa^-3 s^-1` | `3.613e-13` | Paterson-Budd cold-branch proportionality arrmll (glimmer_physcon.F90:99; Pa^-3 s^-1; note PISM's A_cold = 3.61e-13 differs in the third digit - CISM's value is bound here) |
| `Q_cold` | `J/mol` | `60000.0` | cold-branch activation energy actenl = 60.0d3 J/mol (glimmer_physcon.F90:95) |
| `A_warm` | `Pa^-3 s^-1` | `1733.0` | Paterson-Budd warm-branch proportionality arrmlh = 1.733d3 (glimmer_physcon.F90:96) |
| `Q_warm` | `J/mol` | `139000.0` | warm-branch activation energy actenh = 139.0d3 J/mol (glimmer_physcon.F90:94) |
| `T_critical` | `K` | `263.15` | branch switch T* = 263.15 K (tempcor >= -10 degC, F90:2602); the free name of the imported pb_softness template |
| `R_ideal_gas` | `J/mol/K` | `8.314` | universal gas constant gascon = 8.314 J/mol/K (glimmer_physcon.F90:102); the free name of the imported pb_softness template |
| `celsius_to_kelvin` | `K` | `273.15` | the degC -> K offset of the T* construction, celsius_to_kelvin = 273.15 K (glimmer_physcon.F90:89; the Fortran's tempcor + celsius_to_kelvin of F90:2623, 2625); a named parameter so the T* equation carries the constant with its provenance instead of a bare literal |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `tempcor` | `degC` |  | temperature relative to the pressure melting point in each layer, clamp(temp - pmptemp, -50, 0) degC (F90:2596-2598) |
| `T_star` | `K` |  | pressure-corrected absolute temperature tempcor + celsius_to_kelvin (273.15 K, glimmer_physcon.F90:89) in each layer |
| `flwa` | `Pa^-3 s^-1` |  | Glen rate factor in each layer A = E * a * exp(-Q/(R*T*)) with the (a, Q) pair switching at T* = 263.15 K (F90:2602-2606) |

## Observed expressions

$$
tempcor = \mathrm{cism_tempcor}\left(temp=temp, pmptemp=pmptemp\right)
$$
_temperature relative to the pressure melting point in each layer, clamp(temp - pmptemp, -50, 0) degC (F90:2596-2598)_

$$
T_{star} = tempcor + celsius_{to\,kelvin}
$$
_pressure-corrected absolute temperature tempcor + celsius_to_kelvin (273.15 K, glimmer_physcon.F90:89) in each layer_

$$
flwa = E \cdot \mathrm{pb_softness}\left(T_{star}\right)
$$
_Glen rate factor in each layer A = E * a * exp(-Q/(R*T*)) with the (a, Q) pair switching at T* = 263.15 K (F90:2602-2606)_

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "expression_template_imports": [
    {
      "ref": "./cism_templates.esm"
    },
    {
      "ref": "./eqice_ice_rheology_templates.esm"
    }
  ],
  "variables": {
    "temp": {
      "type": "parameter",
      "shape": [
        "lev"
      ],
      "units": "degC",
      "default": [
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
      "description": "ice temperature in each layer (degC; the flowlaw trace's temp column on all 10 layers, equal to the transport-exit temperature profile)"
    },
    "pmptemp": {
      "type": "parameter",
      "shape": [
        "lev"
      ],
      "units": "degC",
      "default": [
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
      "description": "pressure melting point temperature in each layer (degC; pmptemp = -rhoi*grav*pmlt*thck*stagsigma, F90:2170; the flowlaw trace's pmptemp column)"
    },
    "E": {
      "type": "parameter",
      "units": "1",
      "default": 1.0,
      "description": "flow enhancement factor (which_ho_flow_enhancement_factor = 0: E = flow_factor_ground = 1.0 everywhere in the reference run; the dumped E column is 1.0 on every row)"
    },
    "A_cold": {
      "type": "parameter",
      "units": "Pa^-3 s^-1",
      "default": 3.613e-13,
      "description": "Paterson-Budd cold-branch proportionality arrmll (glimmer_physcon.F90:99; Pa^-3 s^-1; note PISM's A_cold = 3.61e-13 differs in the third digit - CISM's value is bound here)"
    },
    "Q_cold": {
      "type": "parameter",
      "units": "J/mol",
      "default": 60000.0,
      "description": "cold-branch activation energy actenl = 60.0d3 J/mol (glimmer_physcon.F90:95)"
    },
    "A_warm": {
      "type": "parameter",
      "units": "Pa^-3 s^-1",
      "default": 1733.0,
      "description": "Paterson-Budd warm-branch proportionality arrmlh = 1.733d3 (glimmer_physcon.F90:96)"
    },
    "Q_warm": {
      "type": "parameter",
      "units": "J/mol",
      "default": 139000.0,
      "description": "warm-branch activation energy actenh = 139.0d3 J/mol (glimmer_physcon.F90:94)"
    },
    "T_critical": {
      "type": "parameter",
      "units": "K",
      "default": 263.15,
      "description": "branch switch T* = 263.15 K (tempcor >= -10 degC, F90:2602); the free name of the imported pb_softness template"
    },
    "R_ideal_gas": {
      "type": "parameter",
      "units": "J/mol/K",
      "default": 8.314,
      "description": "universal gas constant gascon = 8.314 J/mol/K (glimmer_physcon.F90:102); the free name of the imported pb_softness template"
    },
    "celsius_to_kelvin": {
      "type": "parameter",
      "units": "K",
      "default": 273.15,
      "description": "the degC -> K offset of the T* construction, celsius_to_kelvin = 273.15 K (glimmer_physcon.F90:89; the Fortran's tempcor + celsius_to_kelvin of F90:2623, 2625); a named parameter so the T* equation carries the constant with its provenance instead of a bare literal"
    },
    "tempcor": {
      "type": "unknown",
      "shape": [
        "lev"
      ],
      "units": "degC",
      "description": "temperature relative to the pressure melting point in each layer, clamp(temp - pmptemp, -50, 0) degC (F90:2596-2598)"
    },
    "T_star": {
      "type": "unknown",
      "shape": [
        "lev"
      ],
      "units": "K",
      "description": "pressure-corrected absolute temperature tempcor + celsius_to_kelvin (273.15 K, glimmer_physcon.F90:89) in each layer"
    },
    "flwa": {
      "type": "unknown",
      "shape": [
        "lev"
      ],
      "units": "Pa^-3 s^-1",
      "description": "Glen rate factor in each layer A = E * a * exp(-Q/(R*T*)) with the (a, Q) pair switching at T* = 263.15 K (F90:2602-2606)"
    }
  },
  "equations": [
    {
      "lhs": "tempcor",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "cism_tempcor",
        "bindings": {
          "temp": "temp",
          "pmptemp": "pmptemp"
        }
      }
    },
    {
      "lhs": "T_star",
      "rhs": {
        "op": "+",
        "args": [
          "tempcor",
          "celsius_to_kelvin"
        ]
      }
    },
    {
      "lhs": "flwa",
      "rhs": {
        "op": "*",
        "args": [
          "E",
          {
            "op": "pb_softness",
            "args": [
              "T_star"
            ]
          }
        ]
      }
    }
  ],
  "tests": [
    {
      "id": "step1_cell2511_all_layers",
      "description": "cism_flowlaw.csv rows of the full 10-layer column (cism_step 1, cell 25,11, layers 1..10): the elementwise application of the scalar law over the layer axis (esm-spec 9.6.11) reproduces the dump flwa on every layer at rel 1e-12, and the intermediate tempcor = clamp(temp - pmptemp, -50, 0) at the surface and bed layers (the dump's tempcor column).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "temp": [
          -1.7463224232557648,
          -1.7897694178750547,
          -1.8247270848152417,
          -1.8447846601039546,
          -1.8569472376276472,
          -1.8643121036641106,
          -1.8686950101909268,
          -1.8711932597548093,
          -1.8724868984801402,
          -1.8730062714178575
        ],
        "pmptemp": [
          -0.00013888738158086006,
          -0.00038341000708896135,
          -0.000571254310156904,
          -0.0007186937411219001,
          -0.0008365486483060092,
          -0.0009322425097496367,
          -0.0010110066395138066,
          -0.001076614035878038,
          -0.0011318416545665574,
          -0.0011787702392600317
        ]
      },
      "assertions": [
        {
          "variable": "tempcor",
          "time": 0.0,
          "expected": -1.746183535874184,
          "coords": {
            "lev": 1
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "T_star",
          "time": 0.0,
          "expected": 271.4038164641258,
          "coords": {
            "lev": 1
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "flwa",
          "time": 0.0,
          "expected": 3.0602607554030868e-24,
          "coords": {
            "lev": 1
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "flwa",
          "time": 0.0,
          "expected": 3.0303944739507764e-24,
          "coords": {
            "lev": 2
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "flwa",
          "time": 0.0,
          "expected": 3.0065627682278358e-24,
          "coords": {
            "lev": 3
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "flwa",
          "time": 0.0,
          "expected": 2.9929978475766888e-24,
          "coords": {
            "lev": 4
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "flwa",
          "time": 0.0,
          "expected": 2.9848204573577118e-24,
          "coords": {
            "lev": 5
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "flwa",
          "time": 0.0,
          "expected": 2.9798957430697853e-24,
          "coords": {
            "lev": 6
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "flwa",
          "time": 0.0,
          "expected": 2.9769834819219405e-24,
          "coords": {
            "lev": 7
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "flwa",
          "time": 0.0,
          "expected": 2.975338730153917e-24,
          "coords": {
            "lev": 8
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "flwa",
          "time": 0.0,
          "expected": 2.9745017565820985e-24,
          "coords": {
            "lev": 9
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "flwa",
          "time": 0.0,
          "expected": 2.974182517607466e-24,
          "coords": {
            "lev": 10
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "tempcor",
          "time": 0.0,
          "expected": -1.8718275011785974,
          "coords": {
            "lev": 10
          },
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "step1_cell2612_all_layers",
      "description": "cism_flowlaw.csv rows of the full 10-layer column (cism_step 1, cell 26,12): a colder column than 25,11, pinned at the surface and bed layers (the same dump rows the scalar FlowFactor tests of the pre-coupling file pinned): tempcor@lev 1 = -4.665267004926045 degC with flwa = 1.566345909350822e-24 Pa^-3 s^-1, and the deepest layer's flwa = 1.4503883553105943e-24 Pa^-3 s^-1 (tempcor = -4.996477684661026 degC, the largest |pmptemp| traced).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "temp": [
          -4.673739592614364,
          -4.991705620351117,
          -5.031955621084032,
          -5.042595463229652,
          -5.049982034468661,
          -5.055830502219993,
          -5.060537645759002,
          -5.06423914741635,
          -5.066910479437829,
          -5.068386551419353
        ],
        "pmptemp": [
          -0.008472587688318694,
          -0.023389273155451192,
          -0.0348483942892719,
          -0.04384268515535366,
          -0.05103222263709155,
          -0.05686986334344269,
          -0.0616747346609462,
          -0.0656770019106503,
          -0.06904606853736243,
          -0.07190886675832728
        ]
      },
      "assertions": [
        {
          "variable": "tempcor",
          "time": 0.0,
          "expected": -4.665267004926045,
          "coords": {
            "lev": 1
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "flwa",
          "time": 0.0,
          "expected": 1.566345909350822e-24,
          "coords": {
            "lev": 1
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "flwa",
          "time": 0.0,
          "expected": 1.4503883553105943e-24,
          "coords": {
            "lev": 10
          },
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "step4_cell1913_layer5",
      "description": "cism_flowlaw.csv rows of the full 10-layer column (cism_step 4, cell 19,13): a mid-column row of the last step (the same dump row the scalar FlowFactor test pinned): tempcor@lev 5 = -1.7892269700417425 degC, flwa = 3.030503899399558e-24 Pa^-3 s^-1.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "temp": [
          -1.337916875267756,
          -1.5316329630920489,
          -1.6601346509574715,
          -1.7423500683917994,
          -1.7941388838148125,
          -1.8262101193466236,
          -1.8455330805644317,
          -1.85659962434295,
          -1.8623097662041193,
          -1.8645476021719718
        ],
        "pmptemp": [
          -0.0008154969156594573,
          -0.0022512461150546114,
          -0.003354200523385238,
          -0.004219912007250591,
          -0.004911913773069881,
          -0.005473793822694029,
          -0.005936268556943993,
          -0.006321491669155445,
          -0.006645768447845258,
          -0.0069213162739918035
        ]
      },
      "assertions": [
        {
          "variable": "tempcor",
          "time": 0.0,
          "expected": -1.7892269700417425,
          "coords": {
            "lev": 5
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "flwa",
          "time": 0.0,
          "expected": 3.030503899399558e-24,
          "coords": {
            "lev": 5
          },
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "step4_cell2511_layer1",
      "description": "cism_flowlaw.csv rows of the full 10-layer column (cism_step 4, cell 25,11): the step-1 cell four steps later, warmer (the same dump row the scalar FlowFactor test pinned): tempcor@lev 1 = -1.5279796369952778 degC, flwa = 3.215511951544603e-24 Pa^-3 s^-1.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "temp": [
          -1.5280666392064934,
          -1.528143189150328,
          -1.5281904030714353,
          -1.5282195669052396,
          -1.5282386448860363,
          -1.5282487594463532,
          -1.5282548050475209,
          -1.5282583210656902,
          -1.5282602339745843,
          -1.5282611248986624
        ],
        "pmptemp": [
          -8.700221121560043e-05,
          -0.00024017673916264286,
          -0.0003578466782539029,
          -0.00045020608749840905,
          -0.0005240330789134441,
          -0.0005839778877980995,
          -0.0006333175281308367,
          -0.0006744154917529913,
          -0.0007090113268200942,
          -0.0007384084584462942
        ]
      },
      "assertions": [
        {
          "variable": "tempcor",
          "time": 0.0,
          "expected": -1.5279796369952778,
          "coords": {
            "lev": 1
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "flwa",
          "time": 0.0,
          "expected": 3.215511951544603e-24,
          "coords": {
            "lev": 1
          },
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "branch_cold_column",
      "description": "Cold branch (tempcor < -10 degC, F90:2604-2605) pinned from the SOURCE FORMULA on a uniform column (every traced row is warm-branch: tempcor ranges only over [-5.16, -1.13] degC in the reference window). With temp = -15 degC, pmptemp = 0 in every layer: tempcor = -15, T* = 258.15 K < 263.15 K, flwa = 1.0 * 3.613e-13 * exp(-60e3/(8.314 * 258.15)) = 2.611543297913679e-25 Pa^-3 s^-1 (arrmll/actenl pair).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "temp": [
          -15.0,
          -15.0,
          -15.0,
          -15.0,
          -15.0,
          -15.0,
          -15.0,
          -15.0,
          -15.0,
          -15.0
        ],
        "pmptemp": [
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
      },
      "assertions": [
        {
          "variable": "tempcor",
          "time": 0.0,
          "expected": -15.0,
          "coords": {
            "lev": 1
          }
        },
        {
          "variable": "flwa",
          "time": 0.0,
          "expected": 2.611543297913679e-25,
          "coords": {
            "lev": 1
          },
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "branch_boundary_column",
      "description": "Branch boundary pin from the SOURCE FORMULA on a uniform column: at tempcor = -10 degC exactly, T* = 263.15 K and the Fortran's `tempcor >= -10.d0` test (F90:2602) selects the WARM branch (EqIce's pb_softness switches at T_pa < T_critical, so 263.15 K is also warm - the two branch predicates agree). flwa = 1.733e3 * exp(-139e3/(8.314 * 263.15)) = 4.432384868490456e-25 Pa^-3 s^-1.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "temp": [
          -10.0,
          -10.0,
          -10.0,
          -10.0,
          -10.0,
          -10.0,
          -10.0,
          -10.0,
          -10.0,
          -10.0
        ],
        "pmptemp": [
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
      },
      "assertions": [
        {
          "variable": "flwa",
          "time": 0.0,
          "expected": 4.432384868490456e-25,
          "coords": {
            "lev": 1
          },
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "branch_pmp_exceeded_column",
      "description": "tempcor upper clamp pin from the SOURCE FORMULA on a uniform column: with temp - pmptemp > 0 (ice at or above the pressure melting point) the min(0, .) of F90:2597 clamps tempcor to 0 degC (the traced window is entirely cold: temp - pmptemp < 0 on every row). temp = 0.5 degC, pmptemp = 0.1 degC -> tempcor = 0, T* = 273.15 K, flwa = 1.733e3 * exp(-139e3/(8.314 * 273.15)) = 4.5371622457723074e-24 Pa^-3 s^-1.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "temp": [
          0.5,
          0.5,
          0.5,
          0.5,
          0.5,
          0.5,
          0.5,
          0.5,
          0.5,
          0.5
        ],
        "pmptemp": [
          0.1,
          0.1,
          0.1,
          0.1,
          0.1,
          0.1,
          0.1,
          0.1,
          0.1,
          0.1
        ]
      },
      "assertions": [
        {
          "variable": "tempcor",
          "time": 0.0,
          "expected": 0.0,
          "coords": {
            "lev": 1
          }
        },
        {
          "variable": "flwa",
          "time": 0.0,
          "expected": 4.5371622457723074e-24,
          "coords": {
            "lev": 1
          },
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "branch_floor_column",
      "description": "tempcor lower clamp pin from the SOURCE FORMULA on a uniform column: with temp - pmptemp < -50 degC the max(-50, .) of F90:2598 clamps tempcor to -50 degC -> T* = 223.15 K (cold branch): flwa = 3.613e-13 * exp(-60e3/(8.314 * 223.15)) = 3.2557016169108e-27 Pa^-3 s^-1.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "temp": [
          -60.0,
          -60.0,
          -60.0,
          -60.0,
          -60.0,
          -60.0,
          -60.0,
          -60.0,
          -60.0,
          -60.0
        ],
        "pmptemp": [
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
      },
      "assertions": [
        {
          "variable": "tempcor",
          "time": 0.0,
          "expected": -50.0,
          "coords": {
            "lev": 1
          }
        },
        {
          "variable": "flwa",
          "time": 0.0,
          "expected": 3.2557016169108e-27,
          "coords": {
            "lev": 1
          },
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
