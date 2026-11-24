---
title: "BasalWater"
slug: "basalwater"
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

## Variables

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `bwat` | `m` | `0.0` | basal water thickness (m of water, glide_basal_hydro%bwat): the ODE state of the local till balance (HO_BWAT_LOCAL_TILL, glissade_basal_water.F90:146-166); the reference initial state is bwat = 0 everywhere |

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `bmlt` | `m/s` | `0.0` | grounded basal melt rate (m/s of ice) as consumed by glissade_calcbwat: model%basal_melt%bmlt_ground of the thermal solve just above the call (glissade_basal_water.F90:112, 158); positive = melting, negative = freeze-on |
| `dt` | `s` | `0.0` | time step (s): the glide timestep passed into glissade_calcbwat (glissade.F90:1619; dttem = 1.5768e7 s = 0.5 yr in the reference run) |
| `c_drainage` | `m/yr` | `0.001` | uniform drainage rate (glide_types.F90:2298 default 1.0e-3 m/yr; the local till model's constant sink, converted to m/s by /scyr) |
| `W_till_max` | `m` | `2.0` | maximum water depth in till bwat_till_max (glide_types.F90:2297 default 2.0 m); the upper bound of the post-step clamp (F90:162) |
| `rhoi` | `kg/m^3` | `917.0` | ice density (glimmer_physcon rhoi, 917.0 kg/m3 in the CESM build; the ratio rhoi/rhow converts the melt rate from ice to water equivalent, F90:158) |
| `rhow` | `kg/m^3` | `1000.0` | fresh water density (glimmer_physcon rhow = 1000.0 kg/m3) |
| `scyr` | `s/yr` | `31536000.0` | seconds per 365-day year (glimmer_physcon scyr = 31536000.0 s); converts the drainage rate and the dumped m/yr columns |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `dbwat_dt` | `m/s` |  | rate of change of basal water (m/s of water): dbwat_dt = bmlt*rhoi/rhow - c_drainage/scyr (F90:158), the RHS of the ODE |
| `bwat_next` | `m` |  | basal water after the Fortran's discrete step: bwat_next = max(0, min(bwat + dbwat_dt*dt, W_till_max)) - the explicit Euler step with the post-step clamp applied in the Fortran's order (min at F90:162, then max at F90:163). The clamp is a BOUND on the stepped state, not a clamp on the rate: the Fortran computes bwat = bwat + dbwat_dt*dt first and only then clips to [0, bwat_till_max] (the excess/deficit is discarded, not fed back into the rate). The DSL has no bounds mechanism for ODE states, so the exact step map is written out and pinned from the dump; the stage-3 integrator must apply the same projection at each step |

## Observed expressions

$$
dbwat_{dt} = bmlt \cdot \frac{rhoi}{rhow} - \frac{c_{drainage}}{scyr}
$$
_rate of change of basal water (m/s of water): dbwat_dt = bmlt*rhoi/rhow - c_drainage/scyr (F90:158), the RHS of the ODE_

$$
bwat_{next} = \mathrm{max}\left(\mathrm{const}\left(\right), \mathrm{min}\left(bwat + dbwat_{dt} \cdot dt, W_{till\,max}\right)\right)
$$
_basal water after the Fortran's discrete step: bwat_next = max(0, min(bwat + dbwat_dt*dt, W_till_max)) - the explicit Euler step with the post-step clamp applied in the Fortran's order (min at F90:162, then max at F90:163). The clamp is a BOUND on the stepped state, not a clamp on the rate: the Fortran computes bwat = bwat + dbwat_dt*dt first and only then clips to [0, bwat_till_max] (the excess/deficit is discarded, not fed back into the rate). The DSL has no bounds mechanism for ODE states, so the exact step map is written out and pinned from the dump; the stage-3 integrator must apply the same projection at each step_

## Equations

$$
\mathrm{D}\left(bwat\right) = dbwat_{dt}
$$

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "variables": {
    "bmlt": {
      "type": "parameter",
      "units": "m/s",
      "default": 0.0,
      "description": "grounded basal melt rate (m/s of ice) as consumed by glissade_calcbwat: model%basal_melt%bmlt_ground of the thermal solve just above the call (glissade_basal_water.F90:112, 158); positive = melting, negative = freeze-on"
    },
    "dt": {
      "type": "parameter",
      "units": "s",
      "default": 0.0,
      "description": "time step (s): the glide timestep passed into glissade_calcbwat (glissade.F90:1619; dttem = 1.5768e7 s = 0.5 yr in the reference run)"
    },
    "c_drainage": {
      "type": "parameter",
      "units": "m/yr",
      "default": 0.001,
      "description": "uniform drainage rate (glide_types.F90:2298 default 1.0e-3 m/yr; the local till model's constant sink, converted to m/s by /scyr)"
    },
    "W_till_max": {
      "type": "parameter",
      "units": "m",
      "default": 2.0,
      "description": "maximum water depth in till bwat_till_max (glide_types.F90:2297 default 2.0 m); the upper bound of the post-step clamp (F90:162)"
    },
    "rhoi": {
      "type": "parameter",
      "units": "kg/m^3",
      "default": 917.0,
      "description": "ice density (glimmer_physcon rhoi, 917.0 kg/m3 in the CESM build; the ratio rhoi/rhow converts the melt rate from ice to water equivalent, F90:158)"
    },
    "rhow": {
      "type": "parameter",
      "units": "kg/m^3",
      "default": 1000.0,
      "description": "fresh water density (glimmer_physcon rhow = 1000.0 kg/m3)"
    },
    "scyr": {
      "type": "parameter",
      "units": "s/yr",
      "default": 31536000.0,
      "description": "seconds per 365-day year (glimmer_physcon scyr = 31536000.0 s); converts the drainage rate and the dumped m/yr columns"
    },
    "bwat": {
      "type": "unknown",
      "units": "m",
      "default": 0.0,
      "description": "basal water thickness (m of water, glide_basal_hydro%bwat): the ODE state of the local till balance (HO_BWAT_LOCAL_TILL, glissade_basal_water.F90:146-166); the reference initial state is bwat = 0 everywhere"
    },
    "dbwat_dt": {
      "type": "unknown",
      "units": "m/s",
      "description": "rate of change of basal water (m/s of water): dbwat_dt = bmlt*rhoi/rhow - c_drainage/scyr (F90:158), the RHS of the ODE"
    },
    "bwat_next": {
      "type": "unknown",
      "units": "m",
      "description": "basal water after the Fortran's discrete step: bwat_next = max(0, min(bwat + dbwat_dt*dt, W_till_max)) - the explicit Euler step with the post-step clamp applied in the Fortran's order (min at F90:162, then max at F90:163). The clamp is a BOUND on the stepped state, not a clamp on the rate: the Fortran computes bwat = bwat + dbwat_dt*dt first and only then clips to [0, bwat_till_max] (the excess/deficit is discarded, not fed back into the rate). The DSL has no bounds mechanism for ODE states, so the exact step map is written out and pinned from the dump; the stage-3 integrator must apply the same projection at each step"
    }
  },
  "equations": [
    {
      "lhs": {
        "op": "D",
        "args": [
          "bwat"
        ],
        "wrt": "t"
      },
      "rhs": "dbwat_dt"
    },
    {
      "lhs": "dbwat_dt",
      "rhs": {
        "op": "-",
        "args": [
          {
            "op": "*",
            "args": [
              "bmlt",
              {
                "op": "/",
                "args": [
                  "rhoi",
                  "rhow"
                ]
              }
            ]
          },
          {
            "op": "/",
            "args": [
              "c_drainage",
              "scyr"
            ]
          }
        ]
      }
    },
    {
      "lhs": "bwat_next",
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
              {
                "op": "+",
                "args": [
                  "bwat",
                  {
                    "op": "*",
                    "args": [
                      "dbwat_dt",
                      "dt"
                    ]
                  }
                ]
              },
              "W_till_max"
            ]
          }
        ]
      }
    }
  ],
  "tests": [
    {
      "id": "step5_cell5117_lower_clamp",
      "description": "cism_calcbwat.csv row (cism_step 5, cell 5,117, the first step with bmlt > 0 in the 12-year window): the thin coastal cell (thck = 3.3928887429507637 m) has warmed to the pressure melting point and melts at bmlt = 2.434181218057683e-15 m/s of ice (7.676433889266709e-08 m/yr), so dbwat_dt = bmlt*rhoi/rhow - c_drainage/scyr = -3.170755983958763e-11 m/s of water (melt 2.23e-15 < drainage 3.17e-11): the balance is negative, bwat + dbwat_dt*dt = -4.999648035506177e-4 m (dt = 1.5768e7 s = 0.5 yr), and the post-step clamp (min at F90:162, then max at F90:163) pins bwat_next to 0 (the lower branch). bwat stays 0 on every step of the run - the reference configuration is cold-based by construction (geothermal_flux = 0) and the maximum sustainable melt (2.4e-4 m/yr of ice at cell 26,9) is far below c_drainage = 1e-3 m/yr of water, so the till never accumulates water (see README.md). rhoi = 917, rhow = 1000, scyr = 31536000, c_drainage = 1e-3 m/yr, W_till_max = 2.0 m are the dumped constants.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "bmlt": 2.434181218057683e-15,
        "dt": 15768000.0
      },
      "assertions": [
        {
          "variable": "dbwat_dt",
          "time": 0.0,
          "expected": -3.170755983958763e-11,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "bwat_next",
          "time": 0.0,
          "expected": 0.0
        }
      ]
    },
    {
      "id": "step16_cell5117_lower_clamp",
      "description": "cism_calcbwat.csv row (cism_step 16, cell 5,117, mid-window): the melt has grown to bmlt = 5.953783583469358e-12 m/s of ice (1.8775851908828966e-4 m/yr) but is still far below the drainage: dbwat_dt = -2.6250172437723183e-11 m/s of water, bwat + dbwat_dt*dt = -4.1391271899801917e-4 m, bwat_next = 0 (lower clamp). thck = 3.400052662808923 m (the cell has thinned slightly).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "bmlt": 5.953783583469358e-12,
        "dt": 15768000.0
      },
      "assertions": [
        {
          "variable": "dbwat_dt",
          "time": 0.0,
          "expected": -2.6250172437723183e-11,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "bwat_next",
          "time": 0.0,
          "expected": 0.0
        }
      ]
    },
    {
      "id": "step24_cell269_lower_clamp",
      "description": "cism_calcbwat.csv row (cism_step 24, cell 26,9, the last step of the 12-year window and the largest melt of the run): bmlt = 7.542954105813634e-12 m/s of ice (2.3787460068093875e-4 m/yr) at thck = 8.814431634311582 m; dbwat_dt = -2.4792903068733482e-11 m/s of water, bwat + dbwat_dt*dt = -3.9093449558778956e-4 m, bwat_next = 0 (lower clamp). Cell 26,9 starts melting at step 9 (its thck = 8.8 m warms more slowly than the 3.4-m cell 5,117). The upper-clamp branch (bwat + dbwat_dt*dt > W_till_max) is not reachable in this cold-based window and is not pinned (bwat_next's min at F90:162); the interior branch is not reachable either - the melt never exceeds the drainage (the balance is negative on every row).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "bmlt": 7.542954105813634e-12,
        "dt": 15768000.0
      },
      "assertions": [
        {
          "variable": "dbwat_dt",
          "time": 0.0,
          "expected": -2.4792903068733482e-11,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "bwat_next",
          "time": 0.0,
          "expected": 0.0
        }
      ]
    }
  ]
}
```

</details>
