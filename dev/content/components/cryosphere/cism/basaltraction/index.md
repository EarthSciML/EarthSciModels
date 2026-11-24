---
title: "BasalTraction"
slug: "basaltraction"
domains: ["cryosphere"]
component_types: ["model"]
subdomains: ["cism"]
domain: "cryosphere"
subdomain: "cism"
component_type: "model"
esm_version: "2.0.0"
esm_path: "components/cryosphere/cism/cism_basal.esm"
reference: "https://github.com/ESCOMP/CESM"
description: "Stage-2 implementation of the CISM basal physics (stage 2 of the EqESM project; CISM = cismwrap_3_00_002 / cism_main_3.00_002 as built in CESM cesm3.0-alphabranch, reference run T1850Gg/f09_g17_gris20): (a) Effecpress - the cell-centered effective pressure of glissade_calc_effecpress (libglissade/glissade_basal_traction.F90:668-1114) for the reference option HO_EFFECPRESS_BWAT_BVP (which_ho_effecpress = 4, F90:944-985): the Bueler & van Pelt (2015) Eq. 23 law N = N0*(delta*P/N0)^s * 10^((e0/Cc)*(1-s)) with s = clamp(bwat/bwat_till_max, 0, 1), imported by reference from the EqIce basal_templates.esm mohr_coulomb_N_interior (the identical functional form, CISM_LANE.md row 9), plus the two CISM-specific branches: the min(., overburden) cap and the bwat = 0 initialization (N = overburden when the bwat > 0 branch does not fire, F90:784), and the floating-cell zeroing (F90:982-985). The final 0..overburden capping of F90:1082-1086 is a no-op on this construction (N is already in [0, P]) and is documented, not transcribed. The cell-to-vertex stagger (effecpress_stag = 4-cell average of effecpress with stagger_margin = 0, F90:1096-1098; the plain average over all four neighboring cells, glissade_grid_operators.F90:125-133) is a grid discretization step and lives in the stage-3 assembly, not here; the traced N column of cism_basal_traction.csv is that staggered value and is carried into the drag law as the input N_stag. (b) BasalTraction - the pseudo-plastic drag of glissade_calcbeta (F90:69-664) for the reference option HO_BABC_PSEUDO_PLASTIC_OLD (which_ho_babc = 3, F90:250-292): phi(bed) from the bed-elevation ramp (cism_templates.esm cism_phi_ramp, with the CELL-CENTER topg quirk, F90:261-263, bugs.md #23), tanphi = tan(phi*pi/180), yield stress tau_c = tanphi * N_stag, regularized speed = sqrt(u^2 + v^2 + 0.01^2) (the Fortran smallnum = 1.0d-2 m/yr of F90:136,189), and beta = tau_c / (u0^q * speed^(1-q)) - the identical formula to EqIce's pseudo-plastic drag beta = tauc*(eps^2+vx^2+vy^2)^((q-1)/2)*u_threshold^(-q) with eps = 0.01 m/yr (CISM_LANE.md row 8: 'same drag law'), imported by reference from ../../eqice/stage2/basal_templates.esm. Not transcribed (documented coverage gaps): the beta_grounded_min floor and f_ground weighting of F90:597-633 (which_ho_beta_limit = 0 in the reference run; f_ground = 1 at every traced vertex so the floor at 100 Pa yr/m never fires on the traced rows) and the speed cap of F90:196-198 (beta_powerlaw_umax = 0 in the reference config). Tests pin the stage-1 instrumented trace cism_basal_traction.csv (one row per traced vertex and Picard iteration of the velocity solve; q = 0.5, u0 = 100 m/yr, phimin = 5 deg, phimax = 40 deg, bedmin = -300 m, bedmax = 700 m on every row) and the velo-trace overburden chain (the effecpress trace is empty in this run - gland20 starts with bwat = 0 everywhere and the 2-year cold-base run melts nothing, so N is pinned via N = rhoi*g*thck with thck from cism_velo.csv and the source formula for the bwat > 0 branches, see README.md)."
tags: ["cryosphere", "cism", "model", "ice-sheet", "basal", "traction", "effective-pressure", "till-water", "hydrology", "cesm"]
---

## Description

Stage-2 implementation of the CISM basal physics (stage 2 of the EqESM project; CISM = cismwrap_3_00_002 / cism_main_3.00_002 as built in CESM cesm3.0-alphabranch, reference run T1850Gg/f09_g17_gris20): (a) Effecpress - the cell-centered effective pressure of glissade_calc_effecpress (libglissade/glissade_basal_traction.F90:668-1114) for the reference option HO_EFFECPRESS_BWAT_BVP (which_ho_effecpress = 4, F90:944-985): the Bueler & van Pelt (2015) Eq. 23 law N = N0*(delta*P/N0)^s * 10^((e0/Cc)*(1-s)) with s = clamp(bwat/bwat_till_max, 0, 1), imported by reference from the EqIce basal_templates.esm mohr_coulomb_N_interior (the identical functional form, CISM_LANE.md row 9), plus the two CISM-specific branches: the min(., overburden) cap and the bwat = 0 initialization (N = overburden when the bwat > 0 branch does not fire, F90:784), and the floating-cell zeroing (F90:982-985). The final 0..overburden capping of F90:1082-1086 is a no-op on this construction (N is already in [0, P]) and is documented, not transcribed. The cell-to-vertex stagger (effecpress_stag = 4-cell average of effecpress with stagger_margin = 0, F90:1096-1098; the plain average over all four neighboring cells, glissade_grid_operators.F90:125-133) is a grid discretization step and lives in the stage-3 assembly, not here; the traced N column of cism_basal_traction.csv is that staggered value and is carried into the drag law as the input N_stag. (b) BasalTraction - the pseudo-plastic drag of glissade_calcbeta (F90:69-664) for the reference option HO_BABC_PSEUDO_PLASTIC_OLD (which_ho_babc = 3, F90:250-292): phi(bed) from the bed-elevation ramp (cism_templates.esm cism_phi_ramp, with the CELL-CENTER topg quirk, F90:261-263, bugs.md #23), tanphi = tan(phi*pi/180), yield stress tau_c = tanphi * N_stag, regularized speed = sqrt(u^2 + v^2 + 0.01^2) (the Fortran smallnum = 1.0d-2 m/yr of F90:136,189), and beta = tau_c / (u0^q * speed^(1-q)) - the identical formula to EqIce's pseudo-plastic drag beta = tauc*(eps^2+vx^2+vy^2)^((q-1)/2)*u_threshold^(-q) with eps = 0.01 m/yr (CISM_LANE.md row 8: 'same drag law'), imported by reference from ../../eqice/stage2/basal_templates.esm. Not transcribed (documented coverage gaps): the beta_grounded_min floor and f_ground weighting of F90:597-633 (which_ho_beta_limit = 0 in the reference run; f_ground = 1 at every traced vertex so the floor at 100 Pa yr/m never fires on the traced rows) and the speed cap of F90:196-198 (beta_powerlaw_umax = 0 in the reference config). Tests pin the stage-1 instrumented trace cism_basal_traction.csv (one row per traced vertex and Picard iteration of the velocity solve; q = 0.5, u0 = 100 m/yr, phimin = 5 deg, phimax = 40 deg, bedmin = -300 m, bedmax = 700 m on every row) and the velo-trace overburden chain (the effecpress trace is empty in this run - gland20 starts with bwat = 0 everywhere and the 2-year cold-base run melts nothing, so N is pinned via N = rhoi*g*thck with thck from cism_velo.csv and the source formula for the bwat > 0 branches, see README.md).

## Reference

- CISM (Community Ice Sheet Model) cismwrap_3_00_002 / cism_main_3.00.002, as built in CESM cesm3.0-alphabranch (checkout stage1/cesm/components/cism, reference run T1850Gg/f09_g17_gris20): libglissade/glissade_basal_traction.F90, libglissade/glissade_therm.F90, libglissade/glissade_grid_operators.F90, libglissade/glissade_velo_higher.F90, libglissade/glissade_mass_balance.F90, libglissade/glissade_calving.F90, libglissade/glissade_masks.F90, libglissade/glissade_utils.F90, libglimmer/glimmer_physcon.F90, libglimmer/glimmer_utils.F90, libglide/glide_types.F90, libglide/glide_setup.F90, libglad/glad_main.F90, libglad/glad_timestep.F90, libglad/glad_output_states.F90, libglad/glad_output_fluxes.F90, drivers/cpl/nuopc/glc_import_export.F90 - the reference implementation these components are transcribed from.
- EarthSciModels - the authoritative .esm corpus this component lives in.

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `u` | `m/yr` | `0.0` | basal velocity x-component at the vertex (m/yr), the current Picard iterate |
| `v` | `m/yr` | `0.0` | basal velocity y-component at the vertex (m/yr) |
| `bed` | `m` | `0.0` | bed elevation topg - eus at the CELL CENTER (the PSEUDO_PLASTIC_OLD quirk: beta is computed from the cell-center topg, not the staggered stagtopg, F90:261-263, bugs.md #23) |
| `N_stag` | `Pa` | `0.0` | effective pressure at the vertex (the staggered effecpress_stag of the velocity solve, F90:1096-1098; the traced N column of cism_basal_traction.csv) |
| `q` | `1` | `0.5` | pseudo-plastic exponent pseudo_plastic_q (glide_types.F90:2373 default 0.5; the dumped q column is 0.5 on every row) |
| `u0` | `m/yr` | `100.0` | threshold velocity pseudo_plastic_u0 (glide_types.F90:2375 default 100 m/yr; the dumped u0 column is 100 on every row) |
| `eps` | `m/yr` | `0.01` | speed regularization smallnum = 1.0d-2 m/yr (F90:136): speed = sqrt(u^2 + v^2 + smallnum^2), F90:189; this is the same Schoof epsilon of EqIce's pseudo_plastic_drag |
| `phimin` | `degrees` | `5.0` | min friction angle pseudo_plastic_phimin (glide_types.F90:2380 default 5 deg) |
| `phimax` | `degrees` | `40.0` | max friction angle pseudo_plastic_phimax (glide_types.F90:2381 default 40 deg) |
| `bedmin` | `m` | `-300.0` | bed elevation below which phi = phimin, pseudo_plastic_bedmin (glide_types.F90:2382 default -300 m) |
| `bedmax` | `m` | `700.0` | bed elevation above which phi = phimax, pseudo_plastic_bedmax (glide_types.F90:2383 default 700 m) |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `phi` | `degrees` |  | friction angle from the bed-elevation ramp (F90:268-276) |
| `tanphi` | `1` |  | tan(phi) with phi in degrees (F90:277) |
| `speed` | `m/yr` |  | regularized ice speed sqrt(u^2 + v^2 + 0.01^2) (F90:189) |
| `tau_c` | `Pa` |  | yield stress tau_c = tanphi * N_stag (F90:280) |
| `beta` | `Pa yr/m` |  | basal traction coefficient beta = tau_c / (u0^q * speed^(1-q)) (F90:281), the same pseudo-plastic drag as EqIce's pseudo_plastic_drag with eps = 0.01 m/yr |

## Observed expressions

$$
phi = \mathrm{cism_phi_ramp}\left(bed=bed, phimin=phimin, phimax=phimax, bedmin=bedmin, bedmax=bedmax\right)
$$
_friction angle from the bed-elevation ramp (F90:268-276)_

$$
tanphi = \tan\left(phi \cdot \frac{3.141592653589793}{180.0}\right)
$$
_tan(phi) with phi in degrees (F90:277)_

$$
speed = \mathrm{basal_speed}\left(eps, u, v\right)
$$
_regularized ice speed sqrt(u^2 + v^2 + 0.01^2) (F90:189)_

$$
tau_{c} = tanphi \cdot N_{stag}
$$
_yield stress tau_c = tanphi * N_stag (F90:280)_

$$
beta = \mathrm{pseudo_plastic_drag}\left(tau_{c}, q, u0, eps, u, v\right)
$$
_basal traction coefficient beta = tau_c / (u0^q * speed^(1-q)) (F90:281), the same pseudo-plastic drag as EqIce's pseudo_plastic_drag with eps = 0.01 m/yr_

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "expression_template_imports": [
    {
      "ref": "./cism_templates.esm"
    },
    {
      "ref": "./eqice_basal_templates.esm"
    }
  ],
  "variables": {
    "u": {
      "type": "parameter",
      "units": "m/yr",
      "default": 0.0,
      "description": "basal velocity x-component at the vertex (m/yr), the current Picard iterate"
    },
    "v": {
      "type": "parameter",
      "units": "m/yr",
      "default": 0.0,
      "description": "basal velocity y-component at the vertex (m/yr)"
    },
    "bed": {
      "type": "parameter",
      "units": "m",
      "default": 0.0,
      "description": "bed elevation topg - eus at the CELL CENTER (the PSEUDO_PLASTIC_OLD quirk: beta is computed from the cell-center topg, not the staggered stagtopg, F90:261-263, bugs.md #23)"
    },
    "N_stag": {
      "type": "parameter",
      "units": "Pa",
      "default": 0.0,
      "description": "effective pressure at the vertex (the staggered effecpress_stag of the velocity solve, F90:1096-1098; the traced N column of cism_basal_traction.csv)"
    },
    "q": {
      "type": "parameter",
      "units": "1",
      "default": 0.5,
      "description": "pseudo-plastic exponent pseudo_plastic_q (glide_types.F90:2373 default 0.5; the dumped q column is 0.5 on every row)"
    },
    "u0": {
      "type": "parameter",
      "units": "m/yr",
      "default": 100.0,
      "description": "threshold velocity pseudo_plastic_u0 (glide_types.F90:2375 default 100 m/yr; the dumped u0 column is 100 on every row)"
    },
    "eps": {
      "type": "parameter",
      "units": "m/yr",
      "default": 0.01,
      "description": "speed regularization smallnum = 1.0d-2 m/yr (F90:136): speed = sqrt(u^2 + v^2 + smallnum^2), F90:189; this is the same Schoof epsilon of EqIce's pseudo_plastic_drag"
    },
    "phimin": {
      "type": "parameter",
      "units": "degrees",
      "default": 5.0,
      "description": "min friction angle pseudo_plastic_phimin (glide_types.F90:2380 default 5 deg)"
    },
    "phimax": {
      "type": "parameter",
      "units": "degrees",
      "default": 40.0,
      "description": "max friction angle pseudo_plastic_phimax (glide_types.F90:2381 default 40 deg)"
    },
    "bedmin": {
      "type": "parameter",
      "units": "m",
      "default": -300.0,
      "description": "bed elevation below which phi = phimin, pseudo_plastic_bedmin (glide_types.F90:2382 default -300 m)"
    },
    "bedmax": {
      "type": "parameter",
      "units": "m",
      "default": 700.0,
      "description": "bed elevation above which phi = phimax, pseudo_plastic_bedmax (glide_types.F90:2383 default 700 m)"
    },
    "phi": {
      "type": "unknown",
      "units": "degrees",
      "description": "friction angle from the bed-elevation ramp (F90:268-276)"
    },
    "tanphi": {
      "type": "unknown",
      "units": "1",
      "description": "tan(phi) with phi in degrees (F90:277)"
    },
    "speed": {
      "type": "unknown",
      "units": "m/yr",
      "description": "regularized ice speed sqrt(u^2 + v^2 + 0.01^2) (F90:189)"
    },
    "tau_c": {
      "type": "unknown",
      "units": "Pa",
      "description": "yield stress tau_c = tanphi * N_stag (F90:280)"
    },
    "beta": {
      "type": "unknown",
      "units": "Pa yr/m",
      "description": "basal traction coefficient beta = tau_c / (u0^q * speed^(1-q)) (F90:281), the same pseudo-plastic drag as EqIce's pseudo_plastic_drag with eps = 0.01 m/yr"
    }
  },
  "equations": [
    {
      "lhs": "phi",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "cism_phi_ramp",
        "bindings": {
          "bed": "bed",
          "phimin": "phimin",
          "phimax": "phimax",
          "bedmin": "bedmin",
          "bedmax": "bedmax"
        }
      }
    },
    {
      "lhs": "tanphi",
      "rhs": {
        "op": "tan",
        "args": [
          {
            "op": "*",
            "args": [
              "phi",
              {
                "op": "/",
                "args": [
                  3.141592653589793,
                  180.0
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "speed",
      "rhs": {
        "op": "basal_speed",
        "args": [
          "eps",
          "u",
          "v"
        ]
      }
    },
    {
      "lhs": "tau_c",
      "rhs": {
        "op": "*",
        "args": [
          "tanphi",
          "N_stag"
        ]
      }
    },
    {
      "lhs": "beta",
      "rhs": {
        "op": "pseudo_plastic_drag",
        "args": [
          "tau_c",
          "q",
          "u0",
          "eps",
          "u",
          "v"
        ]
      }
    }
  ],
  "tests": [
    {
      "id": "step1_cell2213_iter1_ramp",
      "description": "cism_basal_traction.csv row (cism_step 1, cell 22,13, velo_iter 1): bed = 538.0499877929688 m is inside the ramp (between bedmin = -300 and bedmax = 700), so phi = 5 + (bed + 300)/1000 * 35 = 34.33174957275391 deg and tanphi = 0.6829660486015453; N_stag = 452193.46653451095 Pa (the velo-entry effecpress_stag of the same vertex) gives tau_c = 308832.7850425101 Pa, and speed = sqrt(u^2 + v^2 + 0.01^2) = 0.1985937339061685 m/yr gives beta = tau_c/(u0^q * speed^(1-q)) = 69301.17964177231 Pa yr/m. q = 0.5, u0 = 100 m/yr are the run values (the dumped q/u0 columns).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "u": 0.03649814617456908,
        "v": -0.1949547549371747,
        "bed": 538.0499877929688,
        "N_stag": 452193.46653451095
      },
      "assertions": [
        {
          "variable": "phi",
          "time": 0.0,
          "expected": 34.33174957275391,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "tanphi",
          "time": 0.0,
          "expected": 0.6829660486015453,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "speed",
          "time": 0.0,
          "expected": 0.1985937339061685,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "tau_c",
          "time": 0.0,
          "expected": 308832.7850425101,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "beta",
          "time": 0.0,
          "expected": 69301.17964177231,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "step1_cell2213_iter2",
      "description": "cism_basal_traction.csv row (cism_step 1, cell 22,13, velo_iter 2): the Picard iterate u, v has moved (u = 0.036574094731719, v = -0.19500952167451643) so speed and beta change (beta = 69289.36483789686 Pa yr/m) while N_stag, phi, tanphi and tau_c are iteration-invariant (N is recomputed once per solve, before the Picard loop).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "u": 0.036574094731719,
        "v": -0.19500952167451643,
        "bed": 538.0499877929688,
        "N_stag": 452193.46653451095
      },
      "assertions": [
        {
          "variable": "phi",
          "time": 0.0,
          "expected": 34.33174957275391,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "speed",
          "time": 0.0,
          "expected": 0.19866146568765786,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "beta",
          "time": 0.0,
          "expected": 69289.36483789686,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "step1_cell2213_iter3",
      "description": "cism_basal_traction.csv row (cism_step 1, cell 22,13, velo_iter 3): third Picard iterate, u = 0.03551339129282068, v = -0.18922188498396986 -> speed = 0.19278517245370222 m/yr, beta = 70337.44422256357 Pa yr/m.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "u": 0.03551339129282068,
        "v": -0.18922188498396986,
        "bed": 538.0499877929688,
        "N_stag": 452193.46653451095
      },
      "assertions": [
        {
          "variable": "speed",
          "time": 0.0,
          "expected": 0.19278517245370222,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "beta",
          "time": 0.0,
          "expected": 70337.44422256357,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "step1_cell2511_iter1_phimax",
      "description": "cism_basal_traction.csv row (cism_step 1, cell 25,11, velo_iter 1): bed = 1082.0 m >= bedmax = 700 m -> phi = phimax = 40 deg, tanphi = tan(40 deg) = 0.8390996311772799; N_stag = 239143.1427941269 Pa (the velo-entry effecpress_stag = rhoi*g*stagthck of the same vertex) -> tau_c = 200664.92291712746 Pa; speed = 0.05970704267801483 m/yr -> beta = 82121.8420169373 Pa yr/m. The phimax branch pin.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "u": -0.058233403771395534,
        "v": -0.008590787539678785,
        "bed": 1082.0,
        "N_stag": 239143.1427941269
      },
      "assertions": [
        {
          "variable": "phi",
          "time": 0.0,
          "expected": 40.0
        },
        {
          "variable": "tanphi",
          "time": 0.0,
          "expected": 0.8390996311772799,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "speed",
          "time": 0.0,
          "expected": 0.05970704267801483,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "tau_c",
          "time": 0.0,
          "expected": 200664.92291712746,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "beta",
          "time": 0.0,
          "expected": 82121.8420169373,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "step1_cell2612_iter1_largeN",
      "description": "cism_basal_traction.csv row (cism_step 1, cell 26,12, velo_iter 1): the highest-N traced vertex, N_stag = 1792132.1941786127 Pa (velo entry effecpress_stag = rhoi*g*stagthck with stagthck = 199.2974449419603 m) at bed = 1785.9 m -> tau_c = 1503777.4631562033 Pa, beta = 1060770.9491729552 Pa yr/m at the near-frozen speed 0.020096661101139186 m/yr.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "u": -0.016714798113099248,
        "v": -0.004948869714629256,
        "bed": 1785.9000244140625,
        "N_stag": 1792132.1941786127
      },
      "assertions": [
        {
          "variable": "phi",
          "time": 0.0,
          "expected": 40.0
        },
        {
          "variable": "tau_c",
          "time": 0.0,
          "expected": 1503777.4631562033,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "beta",
          "time": 0.0,
          "expected": 1060770.9491729552,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "step2_cell2811_iter1",
      "description": "cism_basal_traction.csv row (cism_step 2, cell 28,11, velo_iter 1): a step-2 row; the cell is ice-free at solve time (velo entry ice_mask = 0, thck = 1.65e-5 m) but the traced vertex still carries N_stag = 78357.35970008482 Pa from its neighbors (effecpress is the overburden of all cells, F90:784) -> tau_c = 65749.63162436664 Pa, beta = 47725.541361728465 Pa yr/m.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "u": 0.013052192685070345,
        "v": -0.00947955388395866,
        "bed": 921.1400146484375,
        "N_stag": 78357.35970008482
      },
      "assertions": [
        {
          "variable": "phi",
          "time": 0.0,
          "expected": 40.0
        },
        {
          "variable": "tau_c",
          "time": 0.0,
          "expected": 65749.63162436664,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "beta",
          "time": 0.0,
          "expected": 47725.541361728465,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "step4_cell1913_iter39",
      "description": "cism_basal_traction.csv row (cism_step 4, cell 19,13, velo_iter 39, the last traced Picard iteration of the last solve): converged state u = 0.004696179028551737, v = -0.04407246548412945, N_stag = 1168699.017599082 Pa -> tau_c = 980654.9146246392 Pa, beta = 460061.44255729334 Pa yr/m.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "u": 0.004696179028551737,
        "v": -0.04407246548412945,
        "bed": 1107.9000244140625,
        "N_stag": 1168699.017599082
      },
      "assertions": [
        {
          "variable": "phi",
          "time": 0.0,
          "expected": 40.0
        },
        {
          "variable": "speed",
          "time": 0.0,
          "expected": 0.04543606839635215,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "tau_c",
          "time": 0.0,
          "expected": 980654.9146246392,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "beta",
          "time": 0.0,
          "expected": 460061.44255729334,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "step4_cell2511_iter39",
      "description": "cism_basal_traction.csv row (cism_step 4, cell 25,11, velo_iter 39): the same cell as the step-1 phimax pin, four steps later: N_stag has grown to 250317.3236931863 Pa (thicker ice) -> tau_c = 210041.17398823643 Pa, beta = 80777.44843505582 Pa yr/m at speed 0.06761275191976918 m/yr; the bed (1082 m) and phi (40 deg) are unchanged (topg is fixed).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "u": -0.06621956605320506,
        "v": -0.009298026343771191,
        "bed": 1082.0,
        "N_stag": 250317.3236931863
      },
      "assertions": [
        {
          "variable": "phi",
          "time": 0.0,
          "expected": 40.0
        },
        {
          "variable": "speed",
          "time": 0.0,
          "expected": 0.06761275191976918,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "tau_c",
          "time": 0.0,
          "expected": 210041.17398823643,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "beta",
          "time": 0.0,
          "expected": 80777.44843505582,
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
