---
title: "GladSmb"
slug: "gladsmb"
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
| `qsmb` | `kg/m^2/s` | `0.0` | surface mass balance from the cap (glad_inputs%qsmb, kg m-2 s-1 = mm s-1; the cism_cap.csv import column, accumulated over the mass-balance window) |
| `tstep_mbal` | `h` | `8760.0` | mass-balance accumulation window (params%tstep_mbal, hours; glad_main.F90:814-816). 8760 h = 1 yr in the reference run |
| `hours2seconds` | `s/h` | `3600.0` | hours-to-seconds conversion factor (glad_constants.F90:44: hours2seconds = 3600) |
| `rhow` | `kg/m^3` | `1000.0` | fresh-water density (glimmer_physcon rhow = SHR_CONST_RHOFW = 1000 kg/m3; glimmer_physcon.F90:43,58) |
| `rhoi` | `kg/m^3` | `917.0` | ice density (glimmer_physcon rhoi = SHR_CONST_RHOICE = 917 kg/m3, glimmer_physcon.F90:41) |
| `scyr` | `s/yr` | `31536000.0` | seconds per year of exactly 365 days (glimmer_physcon.F90:90: scyr = 31536000), the Fortran's year for the acab m/yr convention (glide_set_acab divides the m/yr input by scyr) |
| `thck` | `m` | `0.0` | ice thickness at the time of the glad step (glide_geometry%thck, m; the pre-step thickness used by the glad-level zeroing) |
| `topg` | `m` | `0.0` | bedrock topography elevation (glide_geometry%topg, m) |
| `eus` | `m` | `0.0` | eustatic sea level (model%climate%eus, m; 0 in the reference run) |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `ocean` | `1` | `0.0` | GLIDE_IS_OCEAN: the cism_ocean predicate on the pre-step thickness - bed below sea level and no ice (glide_mask.inc:33-34; the OCEAN bit of the thkmask is set where topg < eus, glide_set_geometry) |
| `window_seconds` | `s` | `0.0` | length of the mass-balance accumulation window in seconds = tstep_mbal*hours2seconds (the Fortran's accumulation factor of glad_main.F90:824) |
| `windows_per_year` | `1/yr` | `0.0` | number of mass-balance windows per year = scyr/(tstep_mbal*hours2seconds), DERIVED from the named glad/glimmer constants (scyr, tstep_mbal, hours2seconds) rather than hand-set: the Fortran accumulates the window's SMB and passes the result to glide_set_acab as an m/yr rate (glad_main.F90:810-824, glad_timestep.F90:200), which is exact only when the window is 1 yr - the reference run has tstep_mbal = 8760 h = 1 yr, so windows_per_year = 1 and the per-window value equals the dump's m/yr ice column |
| `acab_raw` | `m/yr` | `0.0` | unmasked surface mass balance (m/yr ice; glad_main.F90:810-824, glad_timestep.F90:200): the Fortran chain qsmb*tstep_mbal*hours2seconds/rhow*rhow/rhoi*windows_per_year - qsmb*tstep_mbal*hours2seconds is the kg/m2 of water over the window, /rhow is the mm-to-m depth conversion of the Fortran's /1000 (a kg/m2 water column is mm of water), *rhow/rhoi converts water-equivalent to ice (glad_timestep.F90:200), and *windows_per_year turns the per-window accumulation into the per-year rate of the dump column (the rhow factors cancel, which is why the Fortran's own chain reduces to qsmb*tstep_mbal*3600/rhoi in the reference run) |
| `acab` | `m/yr` | `0.0` | the surface mass balance as applied to the ice sheet (m/yr ice; model%climate%acab after the glad-level zeroing of glad_timestep.F90:171-187 and the m/yr conversion of glide_set_acab) |

## Observed expressions

$$
ocean = \mathrm{cism_ocean}\left(thck=thck, topg=topg, eus=eus\right)
$$
_GLIDE_IS_OCEAN: the cism_ocean predicate on the pre-step thickness - bed below sea level and no ice (glide_mask.inc:33-34; the OCEAN bit of the thkmask is set where topg < eus, glide_set_geometry)_

$$
window_{seconds} = tstep_{mbal} \cdot hours2seconds
$$
_length of the mass-balance accumulation window in seconds = tstep_mbal*hours2seconds (the Fortran's accumulation factor of glad_main.F90:824)_

$$
windows_{per\,year} = \frac{scyr}{window_{seconds}}
$$
_number of mass-balance windows per year = scyr/(tstep_mbal*hours2seconds), DERIVED from the named glad/glimmer constants (scyr, tstep_mbal, hours2seconds) rather than hand-set: the Fortran accumulates the window's SMB and passes the result to glide_set_acab as an m/yr rate (glad_main.F90:810-824, glad_timestep.F90:200), which is exact only when the window is 1 yr - the reference run has tstep_mbal = 8760 h = 1 yr, so windows_per_year = 1 and the per-window value equals the dump's m/yr ice column_

$$
acab_{raw} = \frac{qsmb}{rhow} \cdot tstep_{mbal} \cdot hours2seconds \cdot \frac{rhow}{rhoi} \cdot windows_{per\,year}
$$
_unmasked surface mass balance (m/yr ice; glad_main.F90:810-824, glad_timestep.F90:200): the Fortran chain qsmb*tstep_mbal*hours2seconds/rhow*rhow/rhoi*windows_per_year - qsmb*tstep_mbal*hours2seconds is the kg/m2 of water over the window, /rhow is the mm-to-m depth conversion of the Fortran's /1000 (a kg/m2 water column is mm of water), *rhow/rhoi converts water-equivalent to ice (glad_timestep.F90:200), and *windows_per_year turns the per-window accumulation into the per-year rate of the dump column (the rhow factors cancel, which is why the Fortran's own chain reduces to qsmb*tstep_mbal*3600/rhoi in the reference run)_

$$
acab = \mathrm{ifelse}\left(ocean = \mathrm{const}\left(\right), \mathrm{const}\left(\right), \mathrm{ifelse}\left(\mathrm{and}\left(\mathrm{<=}\left(thck, \mathrm{const}\left(\right)\right), \mathrm{<}\left(acab_{raw}, \mathrm{const}\left(\right)\right)\right), \mathrm{const}\left(\right), acab_{raw}\right)\right)
$$
_the surface mass balance as applied to the ice sheet (m/yr ice; model%climate%acab after the glad-level zeroing of glad_timestep.F90:171-187 and the m/yr conversion of glide_set_acab)_

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
    "qsmb": {
      "type": "parameter",
      "units": "kg/m^2/s",
      "default": 0.0,
      "description": "surface mass balance from the cap (glad_inputs%qsmb, kg m-2 s-1 = mm s-1; the cism_cap.csv import column, accumulated over the mass-balance window)"
    },
    "tstep_mbal": {
      "type": "parameter",
      "units": "h",
      "default": 8760.0,
      "description": "mass-balance accumulation window (params%tstep_mbal, hours; glad_main.F90:814-816). 8760 h = 1 yr in the reference run"
    },
    "hours2seconds": {
      "type": "parameter",
      "units": "s/h",
      "default": 3600.0,
      "description": "hours-to-seconds conversion factor (glad_constants.F90:44: hours2seconds = 3600)"
    },
    "rhow": {
      "type": "parameter",
      "units": "kg/m^3",
      "default": 1000.0,
      "description": "fresh-water density (glimmer_physcon rhow = SHR_CONST_RHOFW = 1000 kg/m3; glimmer_physcon.F90:43,58)"
    },
    "rhoi": {
      "type": "parameter",
      "units": "kg/m^3",
      "default": 917.0,
      "description": "ice density (glimmer_physcon rhoi = SHR_CONST_RHOICE = 917 kg/m3, glimmer_physcon.F90:41)"
    },
    "scyr": {
      "type": "parameter",
      "units": "s/yr",
      "default": 31536000.0,
      "description": "seconds per year of exactly 365 days (glimmer_physcon.F90:90: scyr = 31536000), the Fortran's year for the acab m/yr convention (glide_set_acab divides the m/yr input by scyr)"
    },
    "thck": {
      "type": "parameter",
      "units": "m",
      "default": 0.0,
      "description": "ice thickness at the time of the glad step (glide_geometry%thck, m; the pre-step thickness used by the glad-level zeroing)"
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
    "ocean": {
      "type": "unknown",
      "units": "1",
      "default": 0.0,
      "description": "GLIDE_IS_OCEAN: the cism_ocean predicate on the pre-step thickness - bed below sea level and no ice (glide_mask.inc:33-34; the OCEAN bit of the thkmask is set where topg < eus, glide_set_geometry)"
    },
    "window_seconds": {
      "type": "unknown",
      "units": "s",
      "default": 0.0,
      "description": "length of the mass-balance accumulation window in seconds = tstep_mbal*hours2seconds (the Fortran's accumulation factor of glad_main.F90:824)"
    },
    "windows_per_year": {
      "type": "unknown",
      "units": "1/yr",
      "default": 0.0,
      "description": "number of mass-balance windows per year = scyr/(tstep_mbal*hours2seconds), DERIVED from the named glad/glimmer constants (scyr, tstep_mbal, hours2seconds) rather than hand-set: the Fortran accumulates the window's SMB and passes the result to glide_set_acab as an m/yr rate (glad_main.F90:810-824, glad_timestep.F90:200), which is exact only when the window is 1 yr - the reference run has tstep_mbal = 8760 h = 1 yr, so windows_per_year = 1 and the per-window value equals the dump's m/yr ice column"
    },
    "acab_raw": {
      "type": "unknown",
      "units": "m/yr",
      "default": 0.0,
      "description": "unmasked surface mass balance (m/yr ice; glad_main.F90:810-824, glad_timestep.F90:200): the Fortran chain qsmb*tstep_mbal*hours2seconds/rhow*rhow/rhoi*windows_per_year - qsmb*tstep_mbal*hours2seconds is the kg/m2 of water over the window, /rhow is the mm-to-m depth conversion of the Fortran's /1000 (a kg/m2 water column is mm of water), *rhow/rhoi converts water-equivalent to ice (glad_timestep.F90:200), and *windows_per_year turns the per-window accumulation into the per-year rate of the dump column (the rhow factors cancel, which is why the Fortran's own chain reduces to qsmb*tstep_mbal*3600/rhoi in the reference run)"
    },
    "acab": {
      "type": "unknown",
      "units": "m/yr",
      "default": 0.0,
      "description": "the surface mass balance as applied to the ice sheet (m/yr ice; model%climate%acab after the glad-level zeroing of glad_timestep.F90:171-187 and the m/yr conversion of glide_set_acab)"
    }
  },
  "equations": [
    {
      "lhs": "ocean",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "cism_ocean",
        "bindings": {
          "thck": "thck",
          "topg": "topg",
          "eus": "eus"
        }
      }
    },
    {
      "lhs": "window_seconds",
      "rhs": {
        "op": "*",
        "args": [
          "tstep_mbal",
          "hours2seconds"
        ]
      }
    },
    {
      "lhs": "windows_per_year",
      "rhs": {
        "op": "/",
        "args": [
          "scyr",
          "window_seconds"
        ]
      }
    },
    {
      "lhs": "acab_raw",
      "rhs": {
        "op": "*",
        "args": [
          {
            "op": "*",
            "args": [
              {
                "op": "*",
                "args": [
                  {
                    "op": "/",
                    "args": [
                      "qsmb",
                      "rhow"
                    ]
                  },
                  "tstep_mbal"
                ]
              },
              "hours2seconds"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "/",
                "args": [
                  "rhow",
                  "rhoi"
                ]
              },
              "windows_per_year"
            ]
          }
        ]
      }
    },
    {
      "lhs": "acab",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "==",
            "args": [
              "ocean",
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
            "units": "m/yr"
          },
          {
            "op": "ifelse",
            "args": [
              {
                "op": "and",
                "args": [
                  {
                    "op": "<=",
                    "args": [
                      "thck",
                      {
                        "op": "const",
                        "args": [],
                        "value": 0.0,
                        "units": "m"
                      }
                    ]
                  },
                  {
                    "op": "<",
                    "args": [
                      "acab_raw",
                      {
                        "op": "const",
                        "args": [],
                        "value": 0.0,
                        "units": "m/yr"
                      }
                    ]
                  }
                ]
              },
              {
                "op": "const",
                "args": [],
                "value": 0.0,
                "units": "m/yr"
              },
              "acab_raw"
            ]
          }
        ]
      }
    }
  ],
  "tests": [
    {
      "id": "qsmb_to_acab_step1_cell2511",
      "description": "Dump pin, cism_cap.csv import row (cap_step 1, cell 25,11): qsmb = 4.05302216536369290e-06 kg/m2/s, tstep_mbal = 8760 h give the Fortran chain acab_raw = qsmb*8760*3600/1000*1000/917*1 = 0.13938506761931235 m/yr ice (windows_per_year = scyr/(8760*3600) = 1), identical to the cism_transport.csv entry acab of the same cell at step 1 (rel 0.0e+00 on all 64 traced cells, see README.md). thck = 1.30004894733428955 m > 0, so no zeroing fires and acab = acab_raw.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "qsmb": 4.053022165363693e-06,
        "thck": 1.3000489473342896,
        "topg": 1082.0
      },
      "assertions": [
        {
          "variable": "acab_raw",
          "time": 0.0,
          "expected": 0.13938506761931235,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "acab",
          "time": 0.0,
          "expected": 0.13938506761931235,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "ocean",
          "time": 0.0,
          "expected": 0.0
        }
      ]
    },
    {
      "id": "qsmb_to_acab_cap2_cell2511",
      "description": "Dump pin, cism_cap.csv import row (cap_step 2, cell 25,11): qsmb = -1.69074734385490992e-05 kg/m2/s gives acab = -0.58145483354207683 m/yr ice, identical to the cism_transport.csv entry acab of the same cell at step 3 (the ablation year). thck = 1.4394647029325882 m > 0, so the ice-free zeroing does not fire.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "qsmb": -1.69074734385491e-05,
        "thck": 1.4394647029325882,
        "topg": 1082.0
      },
      "assertions": [
        {
          "variable": "acab",
          "time": 0.0,
          "expected": -0.5814548335420768,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "qsmb_to_acab_step1_cell2611",
      "description": "Dump pin, cism_cap.csv import row (cap_step 1, cell 26,11): the largest traced accumulation qsmb = 6.05103156348133181e-05 kg/m2/s gives acab = 2.0809741699667099 m/yr ice, identical to the cism_transport.csv entry acab (step 1).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "qsmb": 6.051031563481332e-05,
        "thck": 14.0,
        "topg": 1752.9000244140625
      },
      "assertions": [
        {
          "variable": "acab",
          "time": 0.0,
          "expected": 2.08097416996671,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "zeroing_icefree_ablation_cell2811_step2",
      "description": "Dump pin of the glad-level ice-free zeroing (glad_timestep.F90:171-175): the cism_transport.csv entry row of cell 28,11 at step 2 has thck = 0 exactly (the step-1 SMB melted the 0.0199585 m column out) and the dump's acab column reads 0 - the raw cap value for cap_step 1 (qsmb = -2.05729925935643034e-05 kg/m2/s, i.e. acab_raw = -0.7075135162820545 m/yr ice) is zeroed because thck <= 0 and acab_raw < 0. The acab_raw assertion pins the raw value; the acab = 0 assertion pins the zeroing.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "qsmb": -2.0572992593564303e-05,
        "thck": 0.0,
        "topg": 921.1400146484375
      },
      "assertions": [
        {
          "variable": "acab_raw",
          "time": 0.0,
          "expected": -0.7075135162820545,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "acab",
          "time": 0.0,
          "expected": 0.0
        }
      ]
    },
    {
      "id": "thin_ice_no_zeroing_cell2811_step3",
      "description": "Dump pin of the zeroing branch boundary: the cism_transport.csv entry row of cell 28,11 at step 3 has thck = 1.6503583323323985e-05 m > 0 (thin ice advected in during step 2) and the dump's acab column reads -1.7674468845051972 m/yr ice - the raw cap_step-2 value (qsmb = -5.13936070868615494e-05 kg/m2/s), NOT zeroed: the glad-level condition thck <= 0 fails for any ice at all, however thin.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "qsmb": -5.139360708686155e-05,
        "thck": 1.6503583323323985e-05,
        "topg": 921.1400146484375
      },
      "assertions": [
        {
          "variable": "acab",
          "time": 0.0,
          "expected": -1.7674468845051972,
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
