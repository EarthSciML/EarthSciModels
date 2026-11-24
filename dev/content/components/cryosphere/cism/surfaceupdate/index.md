---
title: "SurfaceUpdate"
slug: "surfaceupdate"
domains: ["cryosphere"]
component_types: ["model"]
subdomains: ["cism"]
domain: "cryosphere"
subdomain: "cism"
component_type: "model"
esm_version: "2.0.0"
esm_path: "components/cryosphere/cism/cism_transport.esm"
reference: "https://github.com/ESCOMP/CESM"
description: "Stage-2 implementation of the pointwise slice of the CISM thickness/tracer solve (stage 2 of the EqESM project; CISM = cismwrap_3_00_002 / cism_main_3.00_002 as built in CESM cesm3.0-alphabranch, reference run T1850Gg/f09_g17_gris20; CISM_LANE.md rows 6/7/14): the parts of glissade_thickness_tracer_solve that are not horizontal/vertical grid operations. (a) GladSmb - the cap qsmb-to-acab conversion and the glad-level zeroing (libglad/glad_main.F90:810-824, libglad/glad_timestep.F90:171-200): the Fortran chain acab = qsmb*tstep_mbal*hours2seconds/rhow*rhow/rhoi*windows_per_year with the named glad/glimmer constants hours2seconds = 3600 s/h (glad_constants.F90:44), rhow = SHR_CONST_RHOFW = 1000 kg/m3 and rhoi = SHR_CONST_RHOICE = 917 kg/m3 (glimmer_physcon.F90:41-43) and scyr = 31536000 s/yr (glimmer_physcon.F90:90) driving the DERIVED windows_per_year = scyr/(tstep_mbal*hours2seconds) [1/yr; = 1 in the reference run, tstep_mbal = 8760 h = 1 yr; the Fortran's per-window accumulation m w.e., converted to m/yr ice], then acab = 0 where thck <= 0 and acab < 0 (ice-free ablation) and where the cell is ice-free ocean (the cism_ocean predicate: topg < eus and no ice, glide_mask.inc:33-34). The further cap 'acab = -thck_temp' of glad_timestep.F90:233-235 is applied AFTER glide_set_acab and only adjusts the glad output variable, not the applied field - it is documented, not transcribed. (b) MassBalance - the surface/basal mass-balance application of add_surface_and_basal_mass_balance (libglissade/glissade_mass_balance.F90:819-1571) as the rate law d(thck)/dt = ifelse(thck <= 0 and net < 0, 0, net) with net = acab - bmlt (m/yr ice; bmlt = bmlt_ground + bmlt_float, 0 everywhere in the reference window): the RATE-LEVEL zeroing reproduces the Fortran's layer-by-layer removal that clips the column at zero (F90:1398-1419) without carrying a deficit into the next step (the Fortran's melt_potential accumulator is zeroed at the top of every mass_balance_driver call, F90:1096). The per-step melt_potential = max(0, -(H_pre + net_applied*dt)) of fully melted columns, the applied-rate bookkeeping acab_applied/bmlt_applied, and the tracer surface/bed handling are per-step ALGEBRAIC MAPS of the dumped entry state (the entry thickness H_pre and the entry tracers T1/Tbar/Tsurf/Tbed/T10), evaluated at the step start (time_span {0,0} in the tests): the layer-1 accumulation blend (H1*T1 + s*Tsurf)/(H1 + s) with H1 = sigma2*H_pre (new snow arrives at the current surface temperature temp(0), glissade_transport.F90:166), the layer-10 freeze-on blend (H10*T10 + b*Tbed)/(H10 + b) with H10 = (1 - sigma10)*H_pre (freeze-on arrives at the bed temperature, F90:172-174), and the column-mean law (H_pre*Tbar + s*T_surf_or_1 + b*Tbed)/(H_pre + s + b) as the nested application of the same cism_tracer_mix law (ablation removes the top layers at their own temperature, the layer-free form at the layer-1 temperature - exact while the ablation stays within layer 1; the Fortran's tracer = 0 of fully removed layers, F90:1411-1413, is the zero of fully melted columns); the ocean mask of glissade_get_masks (glissade_masks.F90:70-96) skips the application entirely in ice-free ocean cells (the same cism_ocean predicate); and the ice-age increment d(age)/dt = 1 where thck > 0 (glissade.F90:1203-1213) with age_usrf = 0 and age_lsrf = age (glissade_transport.F90:204-208) - the Fortran's age reset on ice-free cells is a documented difference for the stage-3 assembly. (c) SurfaceUpdate - the post-transport cleanup calc_lsrf_usrf (glimmer_utils.F90:344-378): the floating test is the shared cism_floating_mask template (the single home of the CISM flotation law, also used by the calving components; bound here with thklim = 0, the exact predicate of the Fortran where-clause for ice-present cells) and lsrf = topg where grounded, lsrf = eus - (rhoi/rhoo)*thck where floating, usrf = lsrf + thck. The horizontal remapping and the first-order vertical remap are grid operations (one traced cell cannot pin them); their fingerprints are the documented advection residuals of the thickness and tracer pins."
tags: ["cryosphere", "cism", "model", "ice-sheet", "transport", "mass-balance", "cesm"]
---

## Description

Stage-2 implementation of the pointwise slice of the CISM thickness/tracer solve (stage 2 of the EqESM project; CISM = cismwrap_3_00_002 / cism_main_3.00_002 as built in CESM cesm3.0-alphabranch, reference run T1850Gg/f09_g17_gris20; CISM_LANE.md rows 6/7/14): the parts of glissade_thickness_tracer_solve that are not horizontal/vertical grid operations. (a) GladSmb - the cap qsmb-to-acab conversion and the glad-level zeroing (libglad/glad_main.F90:810-824, libglad/glad_timestep.F90:171-200): the Fortran chain acab = qsmb*tstep_mbal*hours2seconds/rhow*rhow/rhoi*windows_per_year with the named glad/glimmer constants hours2seconds = 3600 s/h (glad_constants.F90:44), rhow = SHR_CONST_RHOFW = 1000 kg/m3 and rhoi = SHR_CONST_RHOICE = 917 kg/m3 (glimmer_physcon.F90:41-43) and scyr = 31536000 s/yr (glimmer_physcon.F90:90) driving the DERIVED windows_per_year = scyr/(tstep_mbal*hours2seconds) [1/yr; = 1 in the reference run, tstep_mbal = 8760 h = 1 yr; the Fortran's per-window accumulation m w.e., converted to m/yr ice], then acab = 0 where thck <= 0 and acab < 0 (ice-free ablation) and where the cell is ice-free ocean (the cism_ocean predicate: topg < eus and no ice, glide_mask.inc:33-34). The further cap 'acab = -thck_temp' of glad_timestep.F90:233-235 is applied AFTER glide_set_acab and only adjusts the glad output variable, not the applied field - it is documented, not transcribed. (b) MassBalance - the surface/basal mass-balance application of add_surface_and_basal_mass_balance (libglissade/glissade_mass_balance.F90:819-1571) as the rate law d(thck)/dt = ifelse(thck <= 0 and net < 0, 0, net) with net = acab - bmlt (m/yr ice; bmlt = bmlt_ground + bmlt_float, 0 everywhere in the reference window): the RATE-LEVEL zeroing reproduces the Fortran's layer-by-layer removal that clips the column at zero (F90:1398-1419) without carrying a deficit into the next step (the Fortran's melt_potential accumulator is zeroed at the top of every mass_balance_driver call, F90:1096). The per-step melt_potential = max(0, -(H_pre + net_applied*dt)) of fully melted columns, the applied-rate bookkeeping acab_applied/bmlt_applied, and the tracer surface/bed handling are per-step ALGEBRAIC MAPS of the dumped entry state (the entry thickness H_pre and the entry tracers T1/Tbar/Tsurf/Tbed/T10), evaluated at the step start (time_span {0,0} in the tests): the layer-1 accumulation blend (H1*T1 + s*Tsurf)/(H1 + s) with H1 = sigma2*H_pre (new snow arrives at the current surface temperature temp(0), glissade_transport.F90:166), the layer-10 freeze-on blend (H10*T10 + b*Tbed)/(H10 + b) with H10 = (1 - sigma10)*H_pre (freeze-on arrives at the bed temperature, F90:172-174), and the column-mean law (H_pre*Tbar + s*T_surf_or_1 + b*Tbed)/(H_pre + s + b) as the nested application of the same cism_tracer_mix law (ablation removes the top layers at their own temperature, the layer-free form at the layer-1 temperature - exact while the ablation stays within layer 1; the Fortran's tracer = 0 of fully removed layers, F90:1411-1413, is the zero of fully melted columns); the ocean mask of glissade_get_masks (glissade_masks.F90:70-96) skips the application entirely in ice-free ocean cells (the same cism_ocean predicate); and the ice-age increment d(age)/dt = 1 where thck > 0 (glissade.F90:1203-1213) with age_usrf = 0 and age_lsrf = age (glissade_transport.F90:204-208) - the Fortran's age reset on ice-free cells is a documented difference for the stage-3 assembly. (c) SurfaceUpdate - the post-transport cleanup calc_lsrf_usrf (glimmer_utils.F90:344-378): the floating test is the shared cism_floating_mask template (the single home of the CISM flotation law, also used by the calving components; bound here with thklim = 0, the exact predicate of the Fortran where-clause for ice-present cells) and lsrf = topg where grounded, lsrf = eus - (rhoi/rhoo)*thck where floating, usrf = lsrf + thck. The horizontal remapping and the first-order vertical remap are grid operations (one traced cell cannot pin them); their fingerprints are the documented advection residuals of the thickness and tracer pins.

## Reference

- CISM (Community Ice Sheet Model) cismwrap_3_00_002 / cism_main_3.00.002, as built in CESM cesm3.0-alphabranch (checkout stage1/cesm/components/cism, reference run T1850Gg/f09_g17_gris20): libglissade/glissade_basal_traction.F90, libglissade/glissade_therm.F90, libglissade/glissade_grid_operators.F90, libglissade/glissade_velo_higher.F90, libglissade/glissade_mass_balance.F90, libglissade/glissade_calving.F90, libglissade/glissade_masks.F90, libglissade/glissade_utils.F90, libglimmer/glimmer_physcon.F90, libglimmer/glimmer_utils.F90, libglide/glide_types.F90, libglide/glide_setup.F90, libglad/glad_main.F90, libglad/glad_timestep.F90, libglad/glad_output_states.F90, libglad/glad_output_fluxes.F90, drivers/cpl/nuopc/glc_import_export.F90 - the reference implementation these components are transcribed from.
- EarthSciModels - the authoritative .esm corpus this component lives in.

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `thck` | `m` | `0.0` | ice thickness (glide_geometry%thck, m; the post-SMB thickness) |
| `topg` | `m` | `0.0` | bedrock topography elevation (glide_geometry%topg, m) |
| `eus` | `m` | `0.0` | eustatic sea level (model%climate%eus, m; 0 in the reference run) |
| `rhoi` | `kg/m^3` | `917.0` | ice density (glimmer_physcon rhoi = SHR_CONST_RHOICE = 917 kg/m3) |
| `rhoo` | `kg/m^3` | `1026.0` | ocean density (glimmer_physcon rhoo = SHR_CONST_RHOSW = 1026 kg/m3) |
| `thklim` | `m` | `0.0` | Ice-presence threshold (m) for the diagnostic floating-ice mask. |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `floating_mask` | `1` |  | floating-ice mask = 1 where ice is present (thck > thklim) and topg - eus < -(rhoi/rhoo)*thck (the cism_floating_mask template of cism_templates.esm, the single home of the CISM flotation law, also used by the calving components; glissade_masks.F90:179-185) |
| `lsrf` | `m` | `0.0` | Lower surface elevation, max(topg, eus - (rhoi/rhoo)*thck), including sea level over ice-free ocean cells (calc_lsrf_usrf). |
| `usrf` | `m` | `0.0` | upper ice surface elevation (glide_geometry%usrf, m) = lsrf + thck |

## Observed expressions

$$
floating_{mask} = \mathrm{cism_floating_mask}\left(thck=thck, topg=topg, eus=eus, thklim=thklim, rhoi=rhoi, rhoo=rhoo\right)
$$
_floating-ice mask = 1 where ice is present (thck > thklim) and topg - eus < -(rhoi/rhoo)*thck (the cism_floating_mask template of cism_templates.esm, the single home of the CISM flotation law, also used by the calving components; glissade_masks.F90:179-185)_

$$
lsrf = \mathrm{max}\left(topg, eus - \frac{rhoi}{rhoo} \cdot thck\right)
$$
_Lower surface elevation, max(topg, eus - (rhoi/rhoo)*thck), including sea level over ice-free ocean cells (calc_lsrf_usrf)._

$$
usrf = lsrf + thck
$$
_upper ice surface elevation (glide_geometry%usrf, m) = lsrf + thck_

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
      "description": "ice thickness (glide_geometry%thck, m; the post-SMB thickness)"
    },
    "topg": {
      "type": "parameter",
      "units": "m",
      "default": 0.0,
      "description": "bedrock topography elevation (glide_geometry%topg, m)"
    },
    "eus": {
      "type": "parameter",
      "units": "m",
      "default": 0.0,
      "description": "eustatic sea level (model%climate%eus, m; 0 in the reference run)"
    },
    "rhoi": {
      "type": "parameter",
      "units": "kg/m^3",
      "default": 917.0,
      "description": "ice density (glimmer_physcon rhoi = SHR_CONST_RHOICE = 917 kg/m3)"
    },
    "rhoo": {
      "type": "parameter",
      "units": "kg/m^3",
      "default": 1026.0,
      "description": "ocean density (glimmer_physcon rhoo = SHR_CONST_RHOSW = 1026 kg/m3)"
    },
    "thklim": {
      "type": "parameter",
      "units": "m",
      "default": 0.0,
      "description": "Ice-presence threshold (m) for the diagnostic floating-ice mask."
    },
    "floating_mask": {
      "type": "unknown",
      "units": "1",
      "description": "floating-ice mask = 1 where ice is present (thck > thklim) and topg - eus < -(rhoi/rhoo)*thck (the cism_floating_mask template of cism_templates.esm, the single home of the CISM flotation law, also used by the calving components; glissade_masks.F90:179-185)"
    },
    "lsrf": {
      "type": "unknown",
      "units": "m",
      "default": 0.0,
      "description": "Lower surface elevation, max(topg, eus - (rhoi/rhoo)*thck), including sea level over ice-free ocean cells (calc_lsrf_usrf)."
    },
    "usrf": {
      "type": "unknown",
      "units": "m",
      "default": 0.0,
      "description": "upper ice surface elevation (glide_geometry%usrf, m) = lsrf + thck"
    }
  },
  "equations": [
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
      "lhs": "lsrf",
      "rhs": {
        "op": "max",
        "args": [
          "topg",
          {
            "op": "-",
            "args": [
              "eus",
              {
                "op": "*",
                "args": [
                  {
                    "op": "/",
                    "args": [
                      "rhoi",
                      "rhoo"
                    ]
                  },
                  "thck"
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "usrf",
      "rhs": {
        "op": "+",
        "args": [
          "lsrf",
          "thck"
        ]
      }
    }
  ],
  "tests": [
    {
      "id": "grounded_step1_cell2511",
      "description": "Dump pin of the grounded branch of calc_lsrf_usrf (glimmer_utils.F90:344-378): the cism_transport.csv exit row of cell 25,11 at step 1 has thck = 1.3697560650243181 m, topg = 1082 m; topg - eus = 1082 > -(rhoi/rhoo)*thck, so lsrf = topg = 1082 m and usrf = lsrf + thck = 1083.3697560650244 m - identical to the dump's exit lsrf/usrf (rel 0.0e+00; verified on all 256 rows: every traced cell is grounded and lsrf = topg exactly).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "thck": 1.3697560650243181,
        "topg": 1082.0
      },
      "assertions": [
        {
          "variable": "lsrf",
          "time": 0.0,
          "expected": 1082.0,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "usrf",
          "time": 0.0,
          "expected": 1083.3697560650244,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "zero_thickness_cell2811_step3",
      "description": "Dump pin of the ice-free cleanup: the cism_transport.csv exit row of cell 28,11 at step 3 has thck = 0 (fully melted in step 3) with topg = 921.1400146484375 m; usrf = lsrf + thck = topg = 921.1400146484375 m, identical to the dump's exit usrf.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "thck": 0.0,
        "topg": 921.1400146484375
      },
      "assertions": [
        {
          "variable": "lsrf",
          "time": 0.0,
          "expected": 921.1400146484375,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "usrf",
          "time": 0.0,
          "expected": 921.1400146484375,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "thin_ice_cell2913_step4",
      "description": "Dump pin on re-advected thin ice: the cism_transport.csv exit row of cell 29,13 at step 4 has thck = 0.00051154483210166042 m, topg = 980.010009765625 m; usrf = 980.01052131045708 m, identical to the dump's exit usrf.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "thck": 0.0005115448321016604,
        "topg": 980.010009765625
      },
      "assertions": [
        {
          "variable": "usrf",
          "time": 0.0,
          "expected": 980.0105213104571,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "grounded_marine_step4_cell3752",
      "description": "Dump pin of the grounded branch of calc_lsrf_usrf on a marine cell where the two forms of the flotation law disagree (the regression guard for the cism_floating_mask sign, wt/cism-calving3): the cism_velo_marine_exit.csv exit row of cell 37,52 at step 4 has thck = 2758.9811421976005 m, topg = -28.266000747680664 m, eus = 0 m and the dumped floating_mask = 0 (grounded marine ice: topg - eus = -28.266000747680664 m sits between the flotation depth -(rhoi/rhoo)*thck = -2465.8730091571147 m and +0, so the flipped form topg - eus < +(rhoi/rhoo)*thck of the template body as merged from ff0e189 would mark this cell floating); lsrf = topg = -28.266000747680664 m and usrf = lsrf + thck = 2730.7151414499199 m, identical to the dump's usrf column. Rows selected by stage1/analysis/extract_cism_float_mask_pins.py (32 such disagreement rows in the dump, all grounded marine ice with dumped floating_mask = 0).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "thck": 2758.9811421976005,
        "topg": -28.266000747680664,
        "eus": 0.0
      },
      "assertions": [
        {
          "variable": "floating_mask",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "lsrf",
          "time": 0.0,
          "expected": -28.266000747680664,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "usrf",
          "time": 0.0,
          "expected": 2730.71514144992,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "ice_free_ocean_surface",
      "description": "With no ice and a submerged bed, both surfaces are at sea level and the floating-ice mask stays zero.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "thck": 0.0,
        "topg": -100.0,
        "eus": 2.0
      },
      "assertions": [
        {
          "variable": "floating_mask",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "abs": 1e-09,
            "rel": 0.0
          }
        },
        {
          "variable": "lsrf",
          "time": 0.0,
          "expected": 2.0,
          "tolerance": {
            "abs": 1e-09,
            "rel": 0.0
          }
        },
        {
          "variable": "usrf",
          "time": 0.0,
          "expected": 2.0,
          "tolerance": {
            "abs": 1e-09,
            "rel": 0.0
          }
        }
      ]
    }
  ]
}
```

</details>
