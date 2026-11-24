---
title: "Effecpress"
slug: "effecpress"
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
| `bwat` | `m` | `0.0` | basal water thickness (glide_basal_hydro%bwat, m); 0 everywhere in the reference run |
| `thck` | `m` | `0.0` | ice thickness (m) |
| `rhoi` | `kg/m^3` | `917.0` | ice density (glide_types default 917.0 kg/m3) |
| `g` | `m/s^2` | `9.80616` | gravitational acceleration (glide_types default 9.80616 m/s2) |
| `floating_mask` | `1` | `0.0` | 1 where the cell is floating (topg - eus < 0 and thck > 0); the reference window has no floating traced cells |
| `W_till_max` | `m` | `2.0` | maximum water depth in till, bwat_till_max (glide_types.F90:2297 default 2.0 m); free name of the imported mohr_coulomb_N_interior template |
| `N0` | `Pa` | `1000.0` | reference effective pressure N_0 (glide_types.F90:2302 default 1000 Pa); free name of the imported mohr_coulomb_N_interior template |
| `e0` | `1` | `0.69` | reference void ratio e_0 (glide_types.F90:2303 default 0.69); free name of the imported mohr_coulomb_N_interior template |
| `Cc` | `1` | `0.12` | till compressibility C_c (glide_types.F90:2304 default 0.12); free name of the imported mohr_coulomb_N_interior template |
| `delta` | `1` | `0.02` | minimum N relative to overburden, effecpress_delta (glide_types.F90:2330 default 0.02) |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `P` | `Pa` |  | overburden pressure P = rhoi*g*thck (glissade_calc_effecpress, F90:777-783) |
| `s_bwat` | `m` |  | clamped basal water thickness max(0, min(bwat, W_till_max)): the Fortran clamps the ratio s = bwat/bwat_till_max to [0, 1] (F90:960); clamping the water thickness itself is algebraically identical since W_till_max > 0 |
| `N_interior` | `Pa` |  | un-capped Bueler & van Pelt (2015) Eq. 23 value N0*(delta*P/N0)^s * 10^((e0/Cc)*(1-s)) with s = s_bwat/W_till_max (the EqIce mohr_coulomb_N_interior rule, the identical functional form) |
| `N` | `Pa` |  | cell-centered effective pressure: overburden when bwat = 0 (the F90:784 initialization, unchanged because the bwat > 0 branch does not fire), min(N_interior, P) when bwat > 0 (the F90:974-975 cap), and 0 for floating ice (the F90:982-985 zeroing) |

## Observed expressions

$$
P = \mathrm{overburden_pressure}\left(rhoi, g, thck\right)
$$
_overburden pressure P = rhoi*g*thck (glissade_calc_effecpress, F90:777-783)_

$$
s_{bwat} = \mathrm{max}\left(\mathrm{const}\left(\right), \mathrm{min}\left(bwat, W_{till\,max}\right)\right)
$$
_clamped basal water thickness max(0, min(bwat, W_till_max)): the Fortran clamps the ratio s = bwat/bwat_till_max to [0, 1] (F90:960); clamping the water thickness itself is algebraically identical since W_till_max > 0_

$$
N_{interior} = \mathrm{mohr_coulomb_N_interior}\left(delta, P, s_{bwat}\right)
$$
_un-capped Bueler & van Pelt (2015) Eq. 23 value N0*(delta*P/N0)^s * 10^((e0/Cc)*(1-s)) with s = s_bwat/W_till_max (the EqIce mohr_coulomb_N_interior rule, the identical functional form)_

$$
N = \mathrm{ifelse}\left(floating_{mask} = 1.0, 0.0, \mathrm{ifelse}\left(\mathrm{>}\left(bwat, \mathrm{const}\left(\right)\right), \mathrm{min}\left(N_{interior}, P\right), P\right)\right)
$$
_cell-centered effective pressure: overburden when bwat = 0 (the F90:784 initialization, unchanged because the bwat > 0 branch does not fire), min(N_interior, P) when bwat > 0 (the F90:974-975 cap), and 0 for floating ice (the F90:982-985 zeroing)_

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "expression_template_imports": [
    {
      "ref": "./eqice_basal_templates.esm"
    }
  ],
  "variables": {
    "bwat": {
      "type": "parameter",
      "units": "m",
      "default": 0.0,
      "description": "basal water thickness (glide_basal_hydro%bwat, m); 0 everywhere in the reference run"
    },
    "thck": {
      "type": "parameter",
      "units": "m",
      "default": 0.0,
      "description": "ice thickness (m)"
    },
    "rhoi": {
      "type": "parameter",
      "units": "kg/m^3",
      "default": 917.0,
      "description": "ice density (glide_types default 917.0 kg/m3)"
    },
    "g": {
      "type": "parameter",
      "units": "m/s^2",
      "default": 9.80616,
      "description": "gravitational acceleration (glide_types default 9.80616 m/s2)"
    },
    "floating_mask": {
      "type": "parameter",
      "units": "1",
      "default": 0.0,
      "description": "1 where the cell is floating (topg - eus < 0 and thck > 0); the reference window has no floating traced cells"
    },
    "W_till_max": {
      "type": "parameter",
      "units": "m",
      "default": 2.0,
      "description": "maximum water depth in till, bwat_till_max (glide_types.F90:2297 default 2.0 m); free name of the imported mohr_coulomb_N_interior template"
    },
    "N0": {
      "type": "parameter",
      "units": "Pa",
      "default": 1000.0,
      "description": "reference effective pressure N_0 (glide_types.F90:2302 default 1000 Pa); free name of the imported mohr_coulomb_N_interior template"
    },
    "e0": {
      "type": "parameter",
      "units": "1",
      "default": 0.69,
      "description": "reference void ratio e_0 (glide_types.F90:2303 default 0.69); free name of the imported mohr_coulomb_N_interior template"
    },
    "Cc": {
      "type": "parameter",
      "units": "1",
      "default": 0.12,
      "description": "till compressibility C_c (glide_types.F90:2304 default 0.12); free name of the imported mohr_coulomb_N_interior template"
    },
    "delta": {
      "type": "parameter",
      "units": "1",
      "default": 0.02,
      "description": "minimum N relative to overburden, effecpress_delta (glide_types.F90:2330 default 0.02)"
    },
    "P": {
      "type": "unknown",
      "units": "Pa",
      "description": "overburden pressure P = rhoi*g*thck (glissade_calc_effecpress, F90:777-783)"
    },
    "s_bwat": {
      "type": "unknown",
      "units": "m",
      "description": "clamped basal water thickness max(0, min(bwat, W_till_max)): the Fortran clamps the ratio s = bwat/bwat_till_max to [0, 1] (F90:960); clamping the water thickness itself is algebraically identical since W_till_max > 0"
    },
    "N_interior": {
      "type": "unknown",
      "units": "Pa",
      "description": "un-capped Bueler & van Pelt (2015) Eq. 23 value N0*(delta*P/N0)^s * 10^((e0/Cc)*(1-s)) with s = s_bwat/W_till_max (the EqIce mohr_coulomb_N_interior rule, the identical functional form)"
    },
    "N": {
      "type": "unknown",
      "units": "Pa",
      "description": "cell-centered effective pressure: overburden when bwat = 0 (the F90:784 initialization, unchanged because the bwat > 0 branch does not fire), min(N_interior, P) when bwat > 0 (the F90:974-975 cap), and 0 for floating ice (the F90:982-985 zeroing)"
    }
  },
  "equations": [
    {
      "lhs": "P",
      "rhs": {
        "op": "overburden_pressure",
        "args": [
          "rhoi",
          "g",
          "thck"
        ]
      }
    },
    {
      "lhs": "s_bwat",
      "rhs": {
        "op": "max",
        "args": [
          {
            "op": "const",
            "args": [],
            "value": 0.0,
            "units": "m"
          },
          {
            "op": "min",
            "args": [
              "bwat",
              "W_till_max"
            ]
          }
        ]
      }
    },
    {
      "lhs": "N_interior",
      "rhs": {
        "op": "mohr_coulomb_N_interior",
        "args": [
          "delta",
          "P",
          "s_bwat"
        ]
      }
    },
    {
      "lhs": "N",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "==",
            "args": [
              "floating_mask",
              1.0
            ]
          },
          0.0,
          {
            "op": "ifelse",
            "args": [
              {
                "op": ">",
                "args": [
                  "bwat",
                  {
                    "op": "const",
                    "args": [],
                    "value": 0.0,
                    "units": "m"
                  }
                ]
              },
              {
                "op": "min",
                "args": [
                  "N_interior",
                  "P"
                ]
              },
              "P"
            ]
          }
        ]
      }
    }
  ],
  "tests": [
    {
      "id": "bwat0_overburden_step1_cell2511",
      "description": "bwat = 0 branch pinned from the dump: velo entry row (cism_step 1, cell 25,11) of cism_velo.csv has thck = 1.36975606502431813 m, and with bwat = 0 the BWAT_BVP branch does not fire, so N = P = rhoi*g*thck = 12317.187222427161 Pa (the F90:784 overburden initialization). The same vertex's staggered N (the 4-cell average used by the drag law) is the basal row's N column = effecpress_stag = 239143.1427941269 Pa = rhoi*g*stagthck (stagthck = 26.594364795786802 m in the velo row, the plain all-cells average of glissade_stagger, F90:1096-1098) - the stagger itself is a stage-3 grid operation, documented in README.md.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "thck": 1.3697560650243181
      },
      "assertions": [
        {
          "variable": "P",
          "time": 0.0,
          "expected": 12317.187222427161,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "N",
          "time": 0.0,
          "expected": 12317.187222427161,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "bwat0_overburden_step1_cell2612",
      "description": "bwat = 0 branch, thick-cell pin: velo entry row (cism_step 1, cell 26,12) thck = 83.55963112291998 m -> N = P = 751388.9860087493 Pa.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "thck": 83.55963112291998
      },
      "assertions": [
        {
          "variable": "N",
          "time": 0.0,
          "expected": 751388.9860087493,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "bwat0_overburden_step4_cell1913",
      "description": "bwat = 0 branch, last-step pin: velo entry row (cism_step 4, cell 19,13) thck = 8.042716577407948 m -> N = P = 72322.1078485194 Pa (the overburden grows as the thickness evolves).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "thck": 8.042716577407948
      },
      "assertions": [
        {
          "variable": "N",
          "time": 0.0,
          "expected": 72322.1078485194,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "bwat0_overburden_calcbwat_cell5117_step5",
      "description": "bwat = 0 branch at the first melting cell of the hydrology lane: the cism_calcbwat.csv row (cism_step 5, cell 5,117) carries thck = 3.3928887429507637 m for the cell whose bmlt first exceeds 0; with bwat = 0 the BWAT_BVP branch does not fire, so N = P = rhoi*g*thck = 30509.699455901413 Pa (the F90:784 overburden initialization, same cell whose BasalWater step-5 row pins dbwat_dt).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "thck": 3.3928887429507637
      },
      "assertions": [
        {
          "variable": "N",
          "time": 0.0,
          "expected": 30509.699455901413,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "bwat0_overburden_calcbwat_cell269_step24",
      "description": "bwat = 0 branch at the strongest-melting cell of the hydrology lane: the cism_calcbwat.csv row (cism_step 24, cell 26,9) carries thck = 8.814431634311582 m -> N = P = 79261.56158116582 Pa (same cell whose BasalWater step-24 row pins the largest |dbwat_dt| of the run).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "thck": 8.814431634311582
      },
      "assertions": [
        {
          "variable": "N",
          "time": 0.0,
          "expected": 79261.56158116582,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "bwat_partial_plateau",
      "description": "bwat > 0 branch, mid-range pin from the SOURCE FORMULA (the effecpress trace is empty in this run - gland20 starts with bwat = 0 everywhere and the cold base melts nothing, cism_thermo.csv bwat = bmlt_ground = 0 on every row; see README.md 'how N is pinned'): with bwat = 0.5 m at the cell overburden P = rhoi*g*thck = 12317.187222427161 Pa (thck = 1.3697560650243181 m from the velo entry row of cell 25,11, step 1; the same cell's VERTEX N_stag is 239143.14 Pa, the 4-cell average, not a cell value), s = 0.25, N_interior = N0*(delta*P/N0)^s * 10^((e0/Cc)*(1-s)) = 1000*(0.02*P/1000)^0.25 * 10^(5.75*0.75) = 14467229.956136435 Pa - far above overburden, so the min(., P) cap of F90:974-975 holds N at P: this is the Bueler & van Pelt (2015) plateau where N stays at overburden for bwat up to ~0.6*bwat_till_max (F90:952-953). N0 = 1000 Pa, e0 = 0.69, Cc = 0.12, delta = 0.02, W_till_max = 2.0 m are the glide_types defaults (F90:2297-2330).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "bwat": 0.5,
        "thck": 1.3697560650243181
      },
      "assertions": [
        {
          "variable": "s_bwat",
          "time": 0.0,
          "expected": 0.5
        },
        {
          "variable": "N_interior",
          "time": 0.0,
          "expected": 14467229.956136435,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "N",
          "time": 0.0,
          "expected": 12317.187222427161,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "bwat_saturated",
      "description": "bwat > 0 branch, saturated pin from the SOURCE FORMULA: with bwat = bwat_till_max = 2.0 m (s = 1) at the same overburden P = 12317.187222427161 Pa, N_interior = N0*(delta*P/N0) = delta*P = 246.34374444854322 Pa - now below overburden, so N = N_interior (the reduced-N branch of F90:962-975; N = delta*P = 0.02*P at full saturation).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "bwat": 2.0,
        "thck": 1.3697560650243181
      },
      "assertions": [
        {
          "variable": "s_bwat",
          "time": 0.0,
          "expected": 2.0
        },
        {
          "variable": "N",
          "time": 0.0,
          "expected": 246.34374444854322,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "bwat_clamped",
      "description": "bwat > 0 branch, clamp pin from the SOURCE FORMULA: with bwat = 3.0 m > bwat_till_max = 2.0 m the Fortran clamps s to 1 (F90:960), so the saturated value N = 246.34374444854322 Pa is unchanged (s_bwat = 2.0 m after the clamp).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "bwat": 3.0,
        "thck": 1.3697560650243181
      },
      "assertions": [
        {
          "variable": "s_bwat",
          "time": 0.0,
          "expected": 2.0
        },
        {
          "variable": "N",
          "time": 0.0,
          "expected": 246.34374444854322,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "floating_zero",
      "description": "Floating-cell zeroing (F90:982-985) pinned from the SOURCE FORMULA: with floating_mask = 1 the effective pressure is zeroed regardless of bwat (here bwat = 2.0 m would otherwise give N = 246.34 Pa) - the reference window has no floating traced cells (all 256 velo rows have floating_mask = 0), so this branch is not dump-covered.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "bwat": 2.0,
        "thck": 1.3697560650243181,
        "floating_mask": 1.0
      },
      "assertions": [
        {
          "variable": "N",
          "time": 0.0,
          "expected": 0.0
        }
      ]
    }
  ]
}
```

</details>
