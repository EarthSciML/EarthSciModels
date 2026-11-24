---
title: "DivaVelocity"
slug: "divavelocity"
domains: ["cryosphere"]
component_types: ["model"]
subdomains: ["cism"]
domain: "cryosphere"
subdomain: "cism"
component_type: "model"
esm_version: "2.0.0"
esm_path: "components/cryosphere/cism/cism_velo.esm"
reference: "https://github.com/ESCOMP/CESM"
description: "Stage-2 implementation of the pointwise laws of the CISM DIVA velocity solve (stage 2 of the EqESM project; CISM = cismwrap_3_00_002 / cism_main_3.00.002 as built in CESM cesm3.0-alphabranch, reference run T1850Gg/f09_g17_gris20, which_ho_approx = HO_APPROX_DIVA = 4, which_ho_gradient = 0, margin = 1, assemble_taud = 1, diva_slope_correction = .true., which_ho_babc = 3, max_slope = 0.5, thck_gradient_ramp = 50 m, thklim = 1 m, upn = 11, nquad = 4): three pointwise components covering the DIVA column laws of glissade_velo_higher_solve, leaving the 2-D finite-element matrix solve, the vertex staggers, and the Picard iteration itself to the stage-3 assembly (README.md): (a) DivaGeometry - the vertex geometry of the driving stress and the slope correction: the hybrid-margin surface gradient dusrf_dx/dy of the NE-corner vertex from the four-cell stencil (glissade_grid_operators.F90 surface_elevation_gradient, HO_GRADIENT_MARGIN_HYBRID, F90:999-1079, with the max_slope clamp F90:1234-1252), the staggered thickness stagthck (the stagger_margin = 0 plain 4-cell mean, cism_stagger_masked_mean with unit masks), the driving stress taudx = -rhoi*grav*stagthck*dusrf_dx (load_vector_gravity, HO_ASSEMBLE_TAUD_LOCAL, F90:4353-4384), the slope angle of the DIVA correction theta_x = atan(|dz_dx|) from the PLAIN vertex gradient of z_mean = usrf - thck/2 (glissade_slope_angle_staggered, F90:1510, with slope_mask = 1 everywhere) and the slope factor F = cos^2(theta) + 4 sin^2(theta) (F90:2189-2193), plus the bwat = 0 effective-pressure identity effecpress_stag = rhoi*g*stagthck pinned at the same stencil; (b) DivaIntegrals - the Goldberg (2011) vertical integrals of the sigma column (compute_integrals_diva, F90:5570-5696): omega_k as the interface-to-bed cumulative integral of sig_mid*thck*(mean over the nquad quadrature points of 1/efvs_qp) and omega as the trapezoid sigma integral of omega_k (no thck factor), both written as ESD integral operators lowered by the local EarthSciDiscretizations-format rules of ./cism_velo_discretization.esm (the imported column_nonuniform_1d rules integral_lev_nodes_cumulative_to_top and integral_lev_whole, the exact stencil of the Fortran loops), with the cell-centered efvs (the arithmetic mean of the quad-point viscosities, F90:5266-5272; the Fortran computes the integral at each quad point and averages, NOT the integral of the averaged viscosity, F90:5578-5583), the staggered stag_omega (the 4-cell mean of omega with stagger_margin = 1; the other three cells' omega enter as inputs because only the traced cell's efvs_q is dumped), and the active-cell guard (the whole block sits inside the active_cell test of the element loop, F90:5091: ice-free cells keep efvs = omega_k = omega = 0 even when the dumped efvs_q inputs are stale nonzero values from a previous step); (c) DivaVelocity - the basal friction, traction and 3-D recovery chain: the pseudo-plastic beta of the mounted BasalTraction (./cism_basal.esm, which_ho_babc = 3) evaluated at the basal velocity, beta_internal = f_ground*beta (the calcbeta f_ground weighting, glissade_basal_traction.F90:595-630; f_ground = 1 on every traced row), the effective basal friction beta_eff = F*beta/(F + beta*omega*cos(theta)) (F90:2589-2601, Goldberg 2011 eq. 40-41 with the May 2025 slope correction), the basal traction btractx = beta_internal*uvel_basal (= beta_eff*uvel_2d, F90:3874, 5780), the basal-velocity recovery uvel_basal = uvel_2d*beta_eff/beta_internal (Goldberg eq. 34, F90:5800-5801) and the 3-D velocity profile uvel[k] = uvel_basal + btractx*stag_omega_k[k]*cos(theta)/F (Goldberg eq. 32 with the slope correction, F90:5935-5936). Deferred to stage 3 (documented in README.md): the 2-D finite-element assembly and the Picard iteration of the solve itself, the effective-pressure cell-to-vertex stagger (N_stag enters as a dumped input; the effecpress_stag = rhoi*g*stagthck identity of the bwat = 0 run is pinned in the DivaGeometry tests). The dumped beta_internal is the last ACCEPTED calcbeta pass of accel_picard (the cism_basal_traction.csv row whose beta equals beta_internal); the tests feed BasalTraction that pass's u/v/bed/N, which makes the beta chain exact, so every law is pinned at rel 1e-12 (dusrf/taud at 1e-11, the ~1800 m elevation dump round-trip). Tests pin the laws against the cism_velo.csv / cism_velo_nbr.csv exit rows (4 steps x 32 traced cells, solver-internal m/yr and Pa yr units; scale_output has not yet run). The seven wiring edges of the velocity block (BasalTraction.beta -> DivaVelocity.beta_raw and the four geometry / two integral staggers) are authored once in the EqESM stage2 coupling library ./cism_velo_coupling.esm (esm-spec 10.9-10.10), an EqESM-only coupling library that is not ported to the corpus; this port inlines those edges so its standalone tests consume exactly the wiring the EqESM cism subassembly reaches through its own coupling_import of the library."
tags: ["cryosphere", "cism", "model", "ice-sheet", "velocity", "diva", "cesm"]
---

## Description

Stage-2 implementation of the pointwise laws of the CISM DIVA velocity solve (stage 2 of the EqESM project; CISM = cismwrap_3_00_002 / cism_main_3.00.002 as built in CESM cesm3.0-alphabranch, reference run T1850Gg/f09_g17_gris20, which_ho_approx = HO_APPROX_DIVA = 4, which_ho_gradient = 0, margin = 1, assemble_taud = 1, diva_slope_correction = .true., which_ho_babc = 3, max_slope = 0.5, thck_gradient_ramp = 50 m, thklim = 1 m, upn = 11, nquad = 4): three pointwise components covering the DIVA column laws of glissade_velo_higher_solve, leaving the 2-D finite-element matrix solve, the vertex staggers, and the Picard iteration itself to the stage-3 assembly (README.md): (a) DivaGeometry - the vertex geometry of the driving stress and the slope correction: the hybrid-margin surface gradient dusrf_dx/dy of the NE-corner vertex from the four-cell stencil (glissade_grid_operators.F90 surface_elevation_gradient, HO_GRADIENT_MARGIN_HYBRID, F90:999-1079, with the max_slope clamp F90:1234-1252), the staggered thickness stagthck (the stagger_margin = 0 plain 4-cell mean, cism_stagger_masked_mean with unit masks), the driving stress taudx = -rhoi*grav*stagthck*dusrf_dx (load_vector_gravity, HO_ASSEMBLE_TAUD_LOCAL, F90:4353-4384), the slope angle of the DIVA correction theta_x = atan(|dz_dx|) from the PLAIN vertex gradient of z_mean = usrf - thck/2 (glissade_slope_angle_staggered, F90:1510, with slope_mask = 1 everywhere) and the slope factor F = cos^2(theta) + 4 sin^2(theta) (F90:2189-2193), plus the bwat = 0 effective-pressure identity effecpress_stag = rhoi*g*stagthck pinned at the same stencil; (b) DivaIntegrals - the Goldberg (2011) vertical integrals of the sigma column (compute_integrals_diva, F90:5570-5696): omega_k as the interface-to-bed cumulative integral of sig_mid*thck*(mean over the nquad quadrature points of 1/efvs_qp) and omega as the trapezoid sigma integral of omega_k (no thck factor), both written as ESD integral operators lowered by the local EarthSciDiscretizations-format rules of ./cism_velo_discretization.esm (the imported column_nonuniform_1d rules integral_lev_nodes_cumulative_to_top and integral_lev_whole, the exact stencil of the Fortran loops), with the cell-centered efvs (the arithmetic mean of the quad-point viscosities, F90:5266-5272; the Fortran computes the integral at each quad point and averages, NOT the integral of the averaged viscosity, F90:5578-5583), the staggered stag_omega (the 4-cell mean of omega with stagger_margin = 1; the other three cells' omega enter as inputs because only the traced cell's efvs_q is dumped), and the active-cell guard (the whole block sits inside the active_cell test of the element loop, F90:5091: ice-free cells keep efvs = omega_k = omega = 0 even when the dumped efvs_q inputs are stale nonzero values from a previous step); (c) DivaVelocity - the basal friction, traction and 3-D recovery chain: the pseudo-plastic beta of the mounted BasalTraction (./cism_basal.esm, which_ho_babc = 3) evaluated at the basal velocity, beta_internal = f_ground*beta (the calcbeta f_ground weighting, glissade_basal_traction.F90:595-630; f_ground = 1 on every traced row), the effective basal friction beta_eff = F*beta/(F + beta*omega*cos(theta)) (F90:2589-2601, Goldberg 2011 eq. 40-41 with the May 2025 slope correction), the basal traction btractx = beta_internal*uvel_basal (= beta_eff*uvel_2d, F90:3874, 5780), the basal-velocity recovery uvel_basal = uvel_2d*beta_eff/beta_internal (Goldberg eq. 34, F90:5800-5801) and the 3-D velocity profile uvel[k] = uvel_basal + btractx*stag_omega_k[k]*cos(theta)/F (Goldberg eq. 32 with the slope correction, F90:5935-5936). Deferred to stage 3 (documented in README.md): the 2-D finite-element assembly and the Picard iteration of the solve itself, the effective-pressure cell-to-vertex stagger (N_stag enters as a dumped input; the effecpress_stag = rhoi*g*stagthck identity of the bwat = 0 run is pinned in the DivaGeometry tests). The dumped beta_internal is the last ACCEPTED calcbeta pass of accel_picard (the cism_basal_traction.csv row whose beta equals beta_internal); the tests feed BasalTraction that pass's u/v/bed/N, which makes the beta chain exact, so every law is pinned at rel 1e-12 (dusrf/taud at 1e-11, the ~1800 m elevation dump round-trip). Tests pin the laws against the cism_velo.csv / cism_velo_nbr.csv exit rows (4 steps x 32 traced cells, solver-internal m/yr and Pa yr units; scale_output has not yet run). The seven wiring edges of the velocity block (BasalTraction.beta -> DivaVelocity.beta_raw and the four geometry / two integral staggers) are authored once in the EqESM stage2 coupling library ./cism_velo_coupling.esm (esm-spec 10.9-10.10), an EqESM-only coupling library that is not ported to the corpus; this port inlines those edges so its standalone tests consume exactly the wiring the EqESM cism subassembly reaches through its own coupling_import of the library.

## Reference

- CISM (Community Ice Sheet Model) cismwrap_3_00_002 / cism_main_3.00.002, as built in CESM cesm3.0-alphabranch (checkout stage1/cesm/components/cism, reference run T1850Gg/f09_g17_gris20): libglissade/glissade_basal_traction.F90, libglissade/glissade_therm.F90, libglissade/glissade_grid_operators.F90, libglissade/glissade_velo_higher.F90, libglissade/glissade_mass_balance.F90, libglissade/glissade_calving.F90, libglissade/glissade_masks.F90, libglissade/glissade_utils.F90, libglimmer/glimmer_physcon.F90, libglimmer/glimmer_utils.F90, libglide/glide_types.F90, libglide/glide_setup.F90, libglad/glad_main.F90, libglad/glad_timestep.F90, libglad/glad_output_states.F90, libglad/glad_output_fluxes.F90, drivers/cpl/nuopc/glc_import_export.F90 - the reference implementation these components are transcribed from.
- CISM (Community Ice Sheet Model) cism_main_3.00.002, libglissade/glissade_velo_higher.F90 (glissade_velo_higher_solve, compute_integrals_diva, compute_3d_velocity_diva, load_vector_gravity) and libglissade/glissade_grid_operators.F90 (surface_elevation_gradient, glissade_slope_angle_staggered).
- Goldberg, D. N. (2011). A variationally derived, depth-integrated approximation for a full-Stokes ice sheet model. Journal of Glaciology, 57(204), 717-728.
- EarthSciModels - the authoritative .esm corpus this component lives in.

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `uvel_2d` | `m/yr` | `0.0` | depth-integrated (DIVA) x velocity at the vertex, the solution of the 2-D solve (cism_velo.csv uvel_2d, solver units; the recovery law uvel_basal = uvel_2d*beta_eff/beta_internal is pinned against it) |
| `vvel_2d` | `m/yr` | `0.0` | depth-integrated (DIVA) y velocity at the vertex (cism_velo.csv vvel_2d) |
| `uvel_basal` | `m/yr` | `0.0` | basal x velocity at the vertex, uvel(11) (cism_velo.csv uvel_011, the last accepted solve result; the input to the mounted BasalTraction - the Fortran's calcbeta argument ubas/vbas, F90:844, and the anchor of the 3-D profile) |
| `vvel_basal` | `m/yr` | `0.0` | basal y velocity at the vertex, vvel(11) (cism_velo.csv vvel_011) |
| `f_ground` | `1` | `1.0` | grounded ice fraction at the vertex (cism_velo.csv f_ground; 1 on every traced row of the reference run): beta_internal = f_ground*beta, the calcbeta weighting of glissade_basal_traction.F90:595-630 |
| `beta_raw` | `Pa yr/m` | `0.0` | basal friction coefficient of the mounted BasalTraction (the pseudo-plastic beta of glissade_calcbeta, which_ho_babc = 3), driven by the coupling edge from BasalTraction.beta (param_to_var); evaluated at the basal velocity uvel_basal/vvel_basal and the bed/N_stag of the vertex |
| `omega` | `m/(Pa yr)` | `0.0` | staggered double integral at the vertex (the dumped stag_omega column): the ice-masked 4-cell mean computed by DivaIntegrals, fed by the variable_map edge DivaIntegrals.stag_omega -> DivaVelocity.omega (declared as a parameter with a default so the edge overrides it at runtime, the same pattern as beta_raw); the omega of the beta_eff law |
| `stag_omega_k` | `m/(Pa yr)` | `0.0` | single integral staggered to the vertex at each velocity level (the dumped stag_omega_k_001..011 column): the per-level ice-masked 4-cell mean computed by DivaIntegrals, fed by the variable_map edge DivaIntegrals.stag_omega_k -> DivaVelocity.stag_omega_k; level 11 (the bed) is 0 on every traced row, which makes the profile formula reduce to uvel(11) = uvel_basal at the bed |
| `theta_x` | `rad` | `0.0` | x-direction slope angle at the vertex (the dumped stag_theta_slope_x column): DivaGeometry's atan(\|dz_dx\|) law, fed by the variable_map edge DivaGeometry.theta_x -> DivaVelocity.theta_x |
| `theta_y` | `rad` | `0.0` | y-direction slope angle at the vertex (the dumped stag_theta_slope_y column): DivaGeometry's atan(\|dz_dy\|) law, fed by the edge DivaGeometry.theta_y -> DivaVelocity.theta_y |
| `F_x` | `1` | `1.0` | DIVA slope correction factor in x at the vertex (the dumped stag_diva_slope_factor_x column): DivaGeometry's cos^2(theta_x) + 4 sin^2(theta_x) law, fed by the edge DivaGeometry.F_x -> DivaVelocity.F_x |
| `F_y` | `1` | `1.0` | DIVA slope correction factor in y at the vertex (the dumped stag_diva_slope_factor_y column): DivaGeometry's law, fed by the edge DivaGeometry.F_y -> DivaVelocity.F_y |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `beta_internal` | `Pa yr/m` |  | basal friction coefficient as consumed by the solve: beta_internal = f_ground*beta_raw (the calcbeta f_ground weighting, F90:595-630; the dumped beta_internal column holds the last ACCEPTED calcbeta pass of the Picard loop, so the chain is pinned at rel 1e-5) |
| `beta_eff_x` | `Pa yr/m` |  | effective basal friction in x: beta_eff_x = F_x*beta_internal/(F_x + beta_internal*omega*cos(theta_x)) (cism_beta_eff, F90:2589-2601, Goldberg 2011 eq. 40-41 with the May 2025 slope correction; the dumped beta_eff_x column) |
| `beta_eff_y` | `Pa yr/m` |  | effective basal friction in y: beta_eff_y = F_y*beta_internal/(F_y + beta_internal*omega*cos(theta_y)) (the dumped beta_eff_y column) |
| `uvel_basal_recovered` | `m/yr` |  | the 3-D recovery law of Goldberg (2011) eq. 34: uvel(nz) = uvel_2d*beta_eff_x/beta_internal (F90:5800-5801); equals the input uvel_basal to within the Picard chain error When basal drag is zero, CISM uses the depth-averaged velocity. |
| `vvel_basal_recovered` | `m/yr` |  | the y recovery law: vvel(nz) = vvel_2d*beta_eff_y/beta_internal (F90:5801) When basal drag is zero, CISM uses the depth-averaged velocity. |
| `btractx` | `Pa` |  | basal traction in x: btractx = beta_internal*uvel_basal = beta_eff_x*uvel_2d (F90:3874 and F90:5780, Goldberg 2011 eq. 38-39; the dumped btractx column) |
| `btracty` | `Pa` |  | basal traction in y: btracty = beta_internal*vvel_basal = beta_eff_y*vvel_2d (the dumped btracty column) |
| `slope_corr_x` | `1` |  | x slope correction of the vertical shear: cos(theta_x)/F_x (the Fortran slope_correction_x, F90:5935) |
| `slope_corr_y` | `1` |  | y slope correction of the vertical shear: cos(theta_y)/F_y (F90:5936) |
| `uvel` | `m/yr` |  | 3-D x velocity profile: uvel[k] = uvel_basal + btractx*stag_omega_k[k]*slope_corr_x (Goldberg 2011 eq. 32 with the slope correction, F90:5804-5815; the dumped uvel_001..011 columns; at the bed level 11 the formula reduces to uvel_basal since stag_omega_k(11) = 0) |
| `vvel` | `m/yr` |  | 3-D y velocity profile: vvel[k] = vvel_basal + btracty*stag_omega_k[k]*slope_corr_y (the dumped vvel_001..011 columns) |

## Observed expressions

$$
beta_{internal} = f_{ground} \cdot beta_{raw}
$$
_basal friction coefficient as consumed by the solve: beta_internal = f_ground*beta_raw (the calcbeta f_ground weighting, F90:595-630; the dumped beta_internal column holds the last ACCEPTED calcbeta pass of the Picard loop, so the chain is pinned at rel 1e-5)_

$$
beta_{eff\,x} = \mathrm{cism_beta_eff}\left(F=F_{x}, beta=beta_{internal}, omega=omega, theta=theta_{x}\right)
$$
_effective basal friction in x: beta_eff_x = F_x*beta_internal/(F_x + beta_internal*omega*cos(theta_x)) (cism_beta_eff, F90:2589-2601, Goldberg 2011 eq. 40-41 with the May 2025 slope correction; the dumped beta_eff_x column)_

$$
beta_{eff\,y} = \mathrm{cism_beta_eff}\left(F=F_{y}, beta=beta_{internal}, omega=omega, theta=theta_{y}\right)
$$
_effective basal friction in y: beta_eff_y = F_y*beta_internal/(F_y + beta_internal*omega*cos(theta_y)) (the dumped beta_eff_y column)_

$$
uvel_{basal\,recovered} = \mathrm{ifelse}\left(\mathrm{>}\left(beta_{internal}, \mathrm{const}\left(\right)\right), \frac{uvel_{2d} \cdot beta_{eff\,x}}{beta_{internal}}, uvel_{2d}\right)
$$
_the 3-D recovery law of Goldberg (2011) eq. 34: uvel(nz) = uvel_2d*beta_eff_x/beta_internal (F90:5800-5801); equals the input uvel_basal to within the Picard chain error When basal drag is zero, CISM uses the depth-averaged velocity._

$$
vvel_{basal\,recovered} = \mathrm{ifelse}\left(\mathrm{>}\left(beta_{internal}, \mathrm{const}\left(\right)\right), \frac{vvel_{2d} \cdot beta_{eff\,y}}{beta_{internal}}, vvel_{2d}\right)
$$
_the y recovery law: vvel(nz) = vvel_2d*beta_eff_y/beta_internal (F90:5801) When basal drag is zero, CISM uses the depth-averaged velocity._

$$
btractx = beta_{internal} \cdot uvel_{basal}
$$
_basal traction in x: btractx = beta_internal*uvel_basal = beta_eff_x*uvel_2d (F90:3874 and F90:5780, Goldberg 2011 eq. 38-39; the dumped btractx column)_

$$
btracty = beta_{internal} \cdot vvel_{basal}
$$
_basal traction in y: btracty = beta_internal*vvel_basal = beta_eff_y*vvel_2d (the dumped btracty column)_

$$
slope_{corr\,x} = \frac{\cos\left(theta_{x}\right)}{F_{x}}
$$
_x slope correction of the vertical shear: cos(theta_x)/F_x (the Fortran slope_correction_x, F90:5935)_

$$
slope_{corr\,y} = \frac{\cos\left(theta_{y}\right)}{F_{y}}
$$
_y slope correction of the vertical shear: cos(theta_y)/F_y (F90:5936)_

$$
uvel = \mathrm{faq}\left(stag_{omega\,k}\right)
$$
_3-D x velocity profile: uvel[k] = uvel_basal + btractx*stag_omega_k[k]*slope_corr_x (Goldberg 2011 eq. 32 with the slope correction, F90:5804-5815; the dumped uvel_001..011 columns; at the bed level 11 the formula reduces to uvel_basal since stag_omega_k(11) = 0)_

$$
vvel = \mathrm{faq}\left(stag_{omega\,k}\right)
$$
_3-D y velocity profile: vvel[k] = vvel_basal + btracty*stag_omega_k[k]*slope_corr_y (the dumped vvel_001..011 columns)_

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
    "uvel_2d": {
      "type": "parameter",
      "units": "m/yr",
      "default": 0.0,
      "description": "depth-integrated (DIVA) x velocity at the vertex, the solution of the 2-D solve (cism_velo.csv uvel_2d, solver units; the recovery law uvel_basal = uvel_2d*beta_eff/beta_internal is pinned against it)"
    },
    "vvel_2d": {
      "type": "parameter",
      "units": "m/yr",
      "default": 0.0,
      "description": "depth-integrated (DIVA) y velocity at the vertex (cism_velo.csv vvel_2d)"
    },
    "uvel_basal": {
      "type": "parameter",
      "units": "m/yr",
      "default": 0.0,
      "description": "basal x velocity at the vertex, uvel(11) (cism_velo.csv uvel_011, the last accepted solve result; the input to the mounted BasalTraction - the Fortran's calcbeta argument ubas/vbas, F90:844, and the anchor of the 3-D profile)"
    },
    "vvel_basal": {
      "type": "parameter",
      "units": "m/yr",
      "default": 0.0,
      "description": "basal y velocity at the vertex, vvel(11) (cism_velo.csv vvel_011)"
    },
    "f_ground": {
      "type": "parameter",
      "units": "1",
      "default": 1.0,
      "description": "grounded ice fraction at the vertex (cism_velo.csv f_ground; 1 on every traced row of the reference run): beta_internal = f_ground*beta, the calcbeta weighting of glissade_basal_traction.F90:595-630"
    },
    "beta_raw": {
      "type": "parameter",
      "units": "Pa yr/m",
      "default": 0.0,
      "description": "basal friction coefficient of the mounted BasalTraction (the pseudo-plastic beta of glissade_calcbeta, which_ho_babc = 3), driven by the coupling edge from BasalTraction.beta (param_to_var); evaluated at the basal velocity uvel_basal/vvel_basal and the bed/N_stag of the vertex"
    },
    "omega": {
      "type": "parameter",
      "units": "m/(Pa yr)",
      "default": 0.0,
      "description": "staggered double integral at the vertex (the dumped stag_omega column): the ice-masked 4-cell mean computed by DivaIntegrals, fed by the variable_map edge DivaIntegrals.stag_omega -> DivaVelocity.omega (declared as a parameter with a default so the edge overrides it at runtime, the same pattern as beta_raw); the omega of the beta_eff law"
    },
    "stag_omega_k": {
      "type": "parameter",
      "units": "m/(Pa yr)",
      "shape": [
        "lev_nodes"
      ],
      "default": 0.0,
      "description": "single integral staggered to the vertex at each velocity level (the dumped stag_omega_k_001..011 column): the per-level ice-masked 4-cell mean computed by DivaIntegrals, fed by the variable_map edge DivaIntegrals.stag_omega_k -> DivaVelocity.stag_omega_k; level 11 (the bed) is 0 on every traced row, which makes the profile formula reduce to uvel(11) = uvel_basal at the bed"
    },
    "theta_x": {
      "type": "parameter",
      "units": "rad",
      "default": 0.0,
      "description": "x-direction slope angle at the vertex (the dumped stag_theta_slope_x column): DivaGeometry's atan(|dz_dx|) law, fed by the variable_map edge DivaGeometry.theta_x -> DivaVelocity.theta_x"
    },
    "theta_y": {
      "type": "parameter",
      "units": "rad",
      "default": 0.0,
      "description": "y-direction slope angle at the vertex (the dumped stag_theta_slope_y column): DivaGeometry's atan(|dz_dy|) law, fed by the edge DivaGeometry.theta_y -> DivaVelocity.theta_y"
    },
    "F_x": {
      "type": "parameter",
      "units": "1",
      "default": 1.0,
      "description": "DIVA slope correction factor in x at the vertex (the dumped stag_diva_slope_factor_x column): DivaGeometry's cos^2(theta_x) + 4 sin^2(theta_x) law, fed by the edge DivaGeometry.F_x -> DivaVelocity.F_x"
    },
    "F_y": {
      "type": "parameter",
      "units": "1",
      "default": 1.0,
      "description": "DIVA slope correction factor in y at the vertex (the dumped stag_diva_slope_factor_y column): DivaGeometry's law, fed by the edge DivaGeometry.F_y -> DivaVelocity.F_y"
    },
    "beta_internal": {
      "type": "unknown",
      "units": "Pa yr/m",
      "description": "basal friction coefficient as consumed by the solve: beta_internal = f_ground*beta_raw (the calcbeta f_ground weighting, F90:595-630; the dumped beta_internal column holds the last ACCEPTED calcbeta pass of the Picard loop, so the chain is pinned at rel 1e-5)"
    },
    "beta_eff_x": {
      "type": "unknown",
      "units": "Pa yr/m",
      "description": "effective basal friction in x: beta_eff_x = F_x*beta_internal/(F_x + beta_internal*omega*cos(theta_x)) (cism_beta_eff, F90:2589-2601, Goldberg 2011 eq. 40-41 with the May 2025 slope correction; the dumped beta_eff_x column)"
    },
    "beta_eff_y": {
      "type": "unknown",
      "units": "Pa yr/m",
      "description": "effective basal friction in y: beta_eff_y = F_y*beta_internal/(F_y + beta_internal*omega*cos(theta_y)) (the dumped beta_eff_y column)"
    },
    "uvel_basal_recovered": {
      "type": "unknown",
      "units": "m/yr",
      "description": "the 3-D recovery law of Goldberg (2011) eq. 34: uvel(nz) = uvel_2d*beta_eff_x/beta_internal (F90:5800-5801); equals the input uvel_basal to within the Picard chain error When basal drag is zero, CISM uses the depth-averaged velocity."
    },
    "vvel_basal_recovered": {
      "type": "unknown",
      "units": "m/yr",
      "description": "the y recovery law: vvel(nz) = vvel_2d*beta_eff_y/beta_internal (F90:5801) When basal drag is zero, CISM uses the depth-averaged velocity."
    },
    "btractx": {
      "type": "unknown",
      "units": "Pa",
      "description": "basal traction in x: btractx = beta_internal*uvel_basal = beta_eff_x*uvel_2d (F90:3874 and F90:5780, Goldberg 2011 eq. 38-39; the dumped btractx column)"
    },
    "btracty": {
      "type": "unknown",
      "units": "Pa",
      "description": "basal traction in y: btracty = beta_internal*vvel_basal = beta_eff_y*vvel_2d (the dumped btracty column)"
    },
    "slope_corr_x": {
      "type": "unknown",
      "units": "1",
      "description": "x slope correction of the vertical shear: cos(theta_x)/F_x (the Fortran slope_correction_x, F90:5935)"
    },
    "slope_corr_y": {
      "type": "unknown",
      "units": "1",
      "description": "y slope correction of the vertical shear: cos(theta_y)/F_y (F90:5936)"
    },
    "uvel": {
      "type": "unknown",
      "units": "m/yr",
      "shape": [
        "lev_nodes"
      ],
      "description": "3-D x velocity profile: uvel[k] = uvel_basal + btractx*stag_omega_k[k]*slope_corr_x (Goldberg 2011 eq. 32 with the slope correction, F90:5804-5815; the dumped uvel_001..011 columns; at the bed level 11 the formula reduces to uvel_basal since stag_omega_k(11) = 0)"
    },
    "vvel": {
      "type": "unknown",
      "units": "m/yr",
      "shape": [
        "lev_nodes"
      ],
      "description": "3-D y velocity profile: vvel[k] = vvel_basal + btracty*stag_omega_k[k]*slope_corr_y (the dumped vvel_001..011 columns)"
    }
  },
  "equations": [
    {
      "lhs": "beta_internal",
      "rhs": {
        "op": "*",
        "args": [
          "f_ground",
          "beta_raw"
        ]
      }
    },
    {
      "lhs": "beta_eff_x",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "cism_beta_eff",
        "bindings": {
          "F": "F_x",
          "beta": "beta_internal",
          "omega": "omega",
          "theta": "theta_x"
        }
      }
    },
    {
      "lhs": "beta_eff_y",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "cism_beta_eff",
        "bindings": {
          "F": "F_y",
          "beta": "beta_internal",
          "omega": "omega",
          "theta": "theta_y"
        }
      }
    },
    {
      "lhs": "uvel_basal_recovered",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": ">",
            "args": [
              "beta_internal",
              {
                "op": "const",
                "args": [],
                "value": 0.0,
                "units": "Pa yr/m"
              }
            ]
          },
          {
            "op": "/",
            "args": [
              {
                "op": "*",
                "args": [
                  "uvel_2d",
                  "beta_eff_x"
                ]
              },
              "beta_internal"
            ]
          },
          "uvel_2d"
        ]
      }
    },
    {
      "lhs": "vvel_basal_recovered",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": ">",
            "args": [
              "beta_internal",
              {
                "op": "const",
                "args": [],
                "value": 0.0,
                "units": "Pa yr/m"
              }
            ]
          },
          {
            "op": "/",
            "args": [
              {
                "op": "*",
                "args": [
                  "vvel_2d",
                  "beta_eff_y"
                ]
              },
              "beta_internal"
            ]
          },
          "vvel_2d"
        ]
      }
    },
    {
      "lhs": "btractx",
      "rhs": {
        "op": "*",
        "args": [
          "beta_internal",
          "uvel_basal"
        ]
      }
    },
    {
      "lhs": "btracty",
      "rhs": {
        "op": "*",
        "args": [
          "beta_internal",
          "vvel_basal"
        ]
      }
    },
    {
      "lhs": "slope_corr_x",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "cos",
            "args": [
              "theta_x"
            ]
          },
          "F_x"
        ]
      }
    },
    {
      "lhs": "slope_corr_y",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "cos",
            "args": [
              "theta_y"
            ]
          },
          "F_y"
        ]
      }
    },
    {
      "lhs": "uvel",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "k"
        ],
        "args": [
          "stag_omega_k"
        ],
        "ranges": {
          "k": {
            "from": "lev_nodes"
          }
        },
        "expr": {
          "op": "+",
          "args": [
            "uvel_basal",
            {
              "op": "*",
              "args": [
                "btractx",
                {
                  "op": "*",
                  "args": [
                    {
                      "op": "index",
                      "args": [
                        "stag_omega_k",
                        "k"
                      ]
                    },
                    "slope_corr_x"
                  ]
                }
              ]
            }
          ]
        }
      }
    },
    {
      "lhs": "vvel",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "k"
        ],
        "args": [
          "stag_omega_k"
        ],
        "ranges": {
          "k": {
            "from": "lev_nodes"
          }
        },
        "expr": {
          "op": "+",
          "args": [
            "vvel_basal",
            {
              "op": "*",
              "args": [
                "btracty",
                {
                  "op": "*",
                  "args": [
                    {
                      "op": "index",
                      "args": [
                        "stag_omega_k",
                        "k"
                      ]
                    },
                    "slope_corr_y"
                  ]
                }
              ]
            }
          ]
        }
      }
    }
  ],
  "tests": [
    {
      "id": "velo_step1_cell2511",
      "description": "Dump pin, cism_velo.csv / cism_velo_nbr.csv / cism_velo_stag.csv step 1, cell (25,11): the thin-ice vertex (thck_sw = 1.37 m) on the steepest slope (theta_x = 0.0316 rad, F_x = 1.003). The coupled chain: the mounted BasalTraction at the ACCEPTED calcbeta pass (u = -0.0604383, v = -0.0088207 m/yr, bed = 1082.0 m, N_stag = 2.3914e5 Pa; the cism_basal_traction.csv row velo_iter 38 of 39 whose beta equals the dumped beta_internal) gives beta_raw = 8.07e4 Pa yr/m and beta_internal = f_ground*beta_raw = 8.07e4 (rel 0.0 on all 128 exit rows - the pass velocity iterate differs from the exit basal velocity by the final Picard correction, so feeding the exit velocity instead would leave a ~6e-7 residual); theta_x/y and F_x/y come from DivaGeometry and omega/stag_omega_k from DivaIntegrals through the variable_map edges; beta_eff_x = F*beta/(F + beta*omega*cos(theta)) = 7.72e4; the recovery uvel_basal = uvel_2d*beta_eff/beta_internal returns the input basal velocity; btractx = beta_internal*uvel_basal = 4.89e3 Pa; and the 3-D profile uvel[k] = uvel_basal + btractx*stag_omega_k[k]*cos(theta)/F spans 0.0610 (surface) down to the basal value. All assertions at rel 1e-12 (the whole chain is exact to machine precision given the accepted-pass inputs).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "BasalTraction.u": -0.06043830506966366,
        "BasalTraction.v": -0.008820742902389414,
        "BasalTraction.bed": 1082.0,
        "BasalTraction.N_stag": 239143.1427941269,
        "uvel_2d": -0.060654317079365465,
        "vvel_2d": -0.008852375837850536,
        "uvel_basal": -0.06043830497199017,
        "vvel_basal": -0.008820742899733815,
        "f_ground": 1.0,
        "DivaGeometry.usrf_sw": 1083.3697560650244,
        "DivaGeometry.thck_sw": 1.3697560650243181,
        "DivaGeometry.ice_mask_sw": 1.0,
        "DivaGeometry.land_mask_sw": 1.0,
        "DivaGeometry.usrf_se": 1767.9405124627754,
        "DivaGeometry.thck_se": 15.04048804871283,
        "DivaGeometry.ice_mask_se": 1.0,
        "DivaGeometry.land_mask_se": 1.0,
        "DivaGeometry.usrf_nw": 1243.7076327746151,
        "DivaGeometry.thck_nw": 6.407583946490077,
        "DivaGeometry.ice_mask_nw": 1.0,
        "DivaGeometry.land_mask_nw": 1.0,
        "DivaGeometry.usrf_ne": 1869.4596555369824,
        "DivaGeometry.thck_ne": 83.55963112291998,
        "DivaGeometry.ice_mask_ne": 1.0,
        "DivaGeometry.land_mask_ne": 1.0,
        "DivaIntegrals.sigma": [
          0.0,
          0.23140495867768607,
          0.4074074074074073,
          0.5443786982248522,
          0.6530612244897959,
          0.7407407407407408,
          0.8125,
          0.8719723183391004,
          0.9218106995884773,
          0.96398891966759,
          1.0
        ],
        "DivaIntegrals.efvs_q1": [
          1108636349.955666,
          1111811478.7223725,
          1114106210.3268867,
          1115114768.0464818,
          1115485090.131957,
          1115501667.4248939,
          1115324638.016571,
          1115045936.3715098,
          1114718966.9368856,
          1114374844.8687665
        ],
        "DivaIntegrals.efvs_q2": [
          815791790.8115213,
          815178610.6327991,
          812742655.3981028,
          809118941.1479666,
          805188301.4629989,
          801321015.9404694,
          797683334.0481234,
          794339748.5576909,
          791304105.1001412,
          788565737.627963
        ],
        "DivaIntegrals.efvs_q3": [
          543213426.5808085,
          528795621.1490218,
          507648401.7377518,
          484743044.94889224,
          462678027.5376662,
          442499337.1030386,
          424529700.50131905,
          408746824.0989182,
          394976261.7971264,
          382989568.72511727
        ],
        "DivaIntegrals.efvs_q4": [
          598387126.3014317,
          598881817.3986205,
          598415650.3881472,
          597155378.8896582,
          595617656.049436,
          594022533.8663735,
          592476475.7142807,
          591027838.3691171,
          589694973.551225,
          588480848.2114793
        ],
        "DivaIntegrals.thck": 1.3697560650243181,
        "DivaIntegrals.ice_mask": 1.0,
        "DivaIntegrals.omega_se": 5.8532707895434575e-09,
        "DivaIntegrals.omega_nw": 7.336229984236539e-09,
        "DivaIntegrals.omega_ne": 1.6398141089809047e-07,
        "DivaIntegrals.ipl_mask_sw": 1.0,
        "DivaIntegrals.ipl_mask_se": 1.0,
        "DivaIntegrals.ipl_mask_nw": 1.0,
        "DivaIntegrals.ipl_mask_ne": 1.0,
        "DivaIntegrals.omega_k_se": [
          8.803688685520676e-09,
          8.301098040840841e-09,
          7.310078741071078e-09,
          6.206338677335351e-09,
          5.104946285519024e-09,
          4.058390197721767e-09,
          3.0878662842739247e-09,
          2.1995192929746455e-09,
          1.3921317421518294e-09,
          6.61009030580591e-10,
          0.0
        ],
        "DivaIntegrals.omega_k_nw": [
          1.033232448095105e-08,
          9.928703151504055e-09,
          9.064362851999841e-09,
          7.996516106446116e-09,
          6.826418748067522e-09,
          5.613775458006621e-09,
          4.400840765538931e-09,
          3.2173290272839886e-09,
          2.082661332121814e-09,
          1.0083118938563594e-09,
          0.0
        ],
        "DivaIntegrals.omega_k_ne": [
          2.1291725624533777e-07,
          2.0930079341510503e-07,
          2.0006355087818551e-07,
          1.8492618692321907e-07,
          1.6417837753525697e-07,
          1.392788467430872e-07,
          1.1187665727917449e-07,
          8.336599786921322e-08,
          5.4785013984371086e-08,
          2.6845502224168177e-08,
          0.0
        ]
      },
      "assertions": [
        {
          "variable": "beta_internal",
          "time": 0.0,
          "expected": 80659.3885029248,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "beta_eff_x",
          "time": 0.0,
          "expected": 80372.1310523575,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "beta_eff_y",
          "time": 0.0,
          "expected": 80371.161535184,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "btractx",
          "time": 0.0,
          "expected": -4874.916721194007,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "btracty",
          "time": 0.0,
          "expected": -711.4757284340452,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "uvel_basal_recovered",
          "time": 0.0,
          "expected": -0.06043830497199017,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "vvel_basal_recovered",
          "time": 0.0,
          "expected": -0.008820742899733815,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "uvel",
          "time": 0.0,
          "expected": -0.06072138010454138,
          "coords": {
            "lev_nodes": 1
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "vvel",
          "time": 0.0,
          "expected": -0.008862196586099725,
          "coords": {
            "lev_nodes": 1
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "uvel",
          "time": 0.0,
          "expected": -0.0606197910962077,
          "coords": {
            "lev_nodes": 6
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "vvel",
          "time": 0.0,
          "expected": -0.008847319832879707,
          "coords": {
            "lev_nodes": 6
          },
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "velo_step1_cell2213",
      "description": "Dump pin, step 1, cell (22,13): the traced cell is ice-FREE (thck = 0, ice_mask = 0) but its NE-corner vertex is an active solve vertex (ice in the stencil neighbors: stagthck = 50.3 m), so the full basal chain runs: the mounted BasalTraction at the accepted calcbeta pass (velo_iter 38 of 39) gives beta_internal = 6.93e4 Pa yr/m and the largest btracty of the pinned rows (-1.35e4 Pa, the strong y flow along the margin); the FULL 3-D profile is pinned at all 11 levels (the shear spans 0.0445 m/yr at the surface down to 0.0366 at the bed in x; stag_omega_k(11) = 0 makes uvel(11) = uvel_basal exactly). All at rel 1e-12 (accepted-pass chain reason, as above).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "BasalTraction.u": 0.03659068802100858,
        "BasalTraction.v": -0.1952271652727915,
        "BasalTraction.bed": 538.0499877929688,
        "BasalTraction.N_stag": 452193.46653451095,
        "uvel_2d": 0.04275089681717399,
        "vvel_2d": -0.228011086639162,
        "uvel_basal": 0.03659068435187166,
        "vvel_basal": -0.19522714548482892,
        "f_ground": 1.0,
        "DivaGeometry.usrf_sw": 538.0499877929688,
        "DivaGeometry.thck_sw": 0.0,
        "DivaGeometry.ice_mask_sw": 0.0,
        "DivaGeometry.land_mask_sw": 1.0,
        "DivaGeometry.usrf_se": 707.1500244140625,
        "DivaGeometry.thck_se": 0.0,
        "DivaGeometry.ice_mask_se": 0.0,
        "DivaGeometry.land_mask_se": 1.0,
        "DivaGeometry.usrf_nw": 1326.3389184143132,
        "DivaGeometry.thck_nw": 102.93889400025078,
        "DivaGeometry.ice_mask_nw": 1.0,
        "DivaGeometry.land_mask_nw": 1.0,
        "DivaGeometry.usrf_ne": 1099.8091950842693,
        "DivaGeometry.thck_ne": 98.20921949833179,
        "DivaGeometry.ice_mask_ne": 1.0,
        "DivaGeometry.land_mask_ne": 1.0,
        "DivaIntegrals.sigma": [
          0.0,
          0.23140495867768607,
          0.4074074074074073,
          0.5443786982248522,
          0.6530612244897959,
          0.7407407407407408,
          0.8125,
          0.8719723183391004,
          0.9218106995884773,
          0.96398891966759,
          1.0
        ],
        "DivaIntegrals.efvs_q1": [
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
        "DivaIntegrals.efvs_q2": [
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
        "DivaIntegrals.efvs_q3": [
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
        "DivaIntegrals.efvs_q4": [
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
        "DivaIntegrals.thck": 0.0,
        "DivaIntegrals.ice_mask": 0.0,
        "DivaIntegrals.omega_se": 0.0,
        "DivaIntegrals.omega_nw": 4.747188139225804e-06,
        "DivaIntegrals.omega_ne": 4.977108201269624e-06,
        "DivaIntegrals.ipl_mask_sw": 1.0,
        "DivaIntegrals.ipl_mask_se": 1.0,
        "DivaIntegrals.ipl_mask_nw": 1.0,
        "DivaIntegrals.ipl_mask_ne": 1.0,
        "DivaIntegrals.omega_k_se": [
          0.0,
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
        "DivaIntegrals.omega_k_nw": [
          6.063958815401146e-06,
          5.993117224207654e-06,
          5.784629125862847e-06,
          5.389843426130012e-06,
          4.813915248304584e-06,
          4.102053729264714e-06,
          3.3058383211464547e-06,
          2.4693831898731397e-06,
          1.6257687420552882e-06,
          7.977871291384221e-07,
          0.0
        ],
        "DivaIntegrals.omega_k_ne": [
          6.417312948381128e-06,
          6.324122415411599e-06,
          6.071207321536375e-06,
          5.631056211249157e-06,
          5.010433133908156e-06,
          4.256662175340079e-06,
          3.422431597413289e-06,
          2.5518997117052705e-06,
          1.6777789853319526e-06,
          8.224230949078171e-07,
          0.0
        ]
      },
      "assertions": [
        {
          "variable": "beta_internal",
          "time": 0.0,
          "expected": 69251.60541507347,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "beta_eff_x",
          "time": 0.0,
          "expected": 59272.759714022424,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "beta_eff_y",
          "time": 0.0,
          "expected": 59294.45556663745,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "btractx",
          "time": 0.0,
          "expected": 2533.96363460332,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "btracty",
          "time": 0.0,
          "expected": -13519.793245426514,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "uvel_basal_recovered",
          "time": 0.0,
          "expected": 0.03659068435187166,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "vvel_basal_recovered",
          "time": 0.0,
          "expected": -0.19522714548482892,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "uvel",
          "time": 0.0,
          "expected": 0.04449740409897475,
          "coords": {
            "lev_nodes": 1
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "vvel",
          "time": 0.0,
          "expected": -0.2373057972152461,
          "coords": {
            "lev_nodes": 1
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "uvel",
          "time": 0.0,
          "expected": 0.04439349192881894,
          "coords": {
            "lev_nodes": 2
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "vvel",
          "time": 0.0,
          "expected": -0.23675278861517018,
          "coords": {
            "lev_nodes": 2
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "uvel",
          "time": 0.0,
          "expected": 0.044101199140043304,
          "coords": {
            "lev_nodes": 3
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "vvel",
          "time": 0.0,
          "expected": -0.2351972400620918,
          "coords": {
            "lev_nodes": 3
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "uvel",
          "time": 0.0,
          "expected": 0.043572277769824835,
          "coords": {
            "lev_nodes": 4
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "vvel",
          "time": 0.0,
          "expected": -0.23238238145548035,
          "coords": {
            "lev_nodes": 4
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "uvel",
          "time": 0.0,
          "expected": 0.042814278455596426,
          "coords": {
            "lev_nodes": 5
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "vvel",
          "time": 0.0,
          "expected": -0.22834839641800656,
          "coords": {
            "lev_nodes": 5
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "uvel",
          "time": 0.0,
          "expected": 0.041885819763884814,
          "coords": {
            "lev_nodes": 6
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "vvel",
          "time": 0.0,
          "expected": -0.2234072462085375,
          "coords": {
            "lev_nodes": 6
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "uvel",
          "time": 0.0,
          "expected": 0.04085295390546681,
          "coords": {
            "lev_nodes": 7
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "vvel",
          "time": 0.0,
          "expected": -0.21791045308436824,
          "coords": {
            "lev_nodes": 7
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "uvel",
          "time": 0.0,
          "expected": 0.03977160032142107,
          "coords": {
            "lev_nodes": 8
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "vvel",
          "time": 0.0,
          "expected": -0.21215561386963944,
          "coords": {
            "lev_nodes": 8
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "uvel",
          "time": 0.0,
          "expected": 0.038683437922659616,
          "coords": {
            "lev_nodes": 9
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "vvel",
          "time": 0.0,
          "expected": -0.20636453892729123,
          "coords": {
            "lev_nodes": 9
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "uvel",
          "time": 0.0,
          "expected": 0.0376170659911288,
          "coords": {
            "lev_nodes": 10
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "vvel",
          "time": 0.0,
          "expected": -0.20068943034153194,
          "coords": {
            "lev_nodes": 10
          },
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "velo_step1_cell2713",
      "description": "Dump pin, step 1, cell (27,13): the thickest pinned column (thck = 434.5 m, omega = 5.9e-5 m/(Pa yr)) with a high-friction bed (beta_internal = 1.23e6 Pa yr/m): the beta_eff correction is the strongest of the pinned rows (beta_eff_x/beta_internal = 0.955), and the deep column shows the smallest surface-to-bed shear (uvel spans 1.0085 down to 1.0064 m/yr). All at rel 1e-12 (accepted-pass chain reason).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "BasalTraction.u": 0.05094957451754119,
        "BasalTraction.v": -0.027760467674301847,
        "BasalTraction.bed": 1692.300048828125,
        "BasalTraction.N_stag": 3556675.565043996,
        "uvel_2d": 1.0063872203321913,
        "vvel_2d": -0.5484594737080144,
        "uvel_basal": 0.05094956654534079,
        "vvel_basal": -0.027760463359866833,
        "f_ground": 1.0,
        "DivaGeometry.usrf_sw": 2126.804262847162,
        "DivaGeometry.thck_sw": 434.50421401903714,
        "DivaGeometry.ice_mask_sw": 1.0,
        "DivaGeometry.land_mask_sw": 1.0,
        "DivaGeometry.usrf_se": 1678.37154926737,
        "DivaGeometry.thck_se": 141.97152485330747,
        "DivaGeometry.ice_mask_se": 1.0,
        "DivaGeometry.land_mask_se": 1.0,
        "DivaGeometry.usrf_nw": 2225.051047853225,
        "DivaGeometry.thck_nw": 700.35109668135,
        "DivaGeometry.ice_mask_nw": 1.0,
        "DivaGeometry.land_mask_nw": 1.0,
        "DivaGeometry.usrf_ne": 1965.580504027392,
        "DivaGeometry.thck_ne": 305.2804551992669,
        "DivaGeometry.ice_mask_ne": 1.0,
        "DivaGeometry.land_mask_ne": 1.0,
        "DivaIntegrals.sigma": [
          0.0,
          0.23140495867768607,
          0.4074074074074073,
          0.5443786982248522,
          0.6530612244897959,
          0.7407407407407408,
          0.8125,
          0.8719723183391004,
          0.9218106995884773,
          0.96398891966759,
          1.0
        ],
        "DivaIntegrals.efvs_q1": [
          127575475.80982167,
          116550358.03507909,
          102087709.8930134,
          87826528.568235,
          75687599.0223082,
          66127517.950745285,
          58833838.04207159,
          53289177.8759403,
          49029549.26545312,
          45696741.959086746
        ],
        "DivaIntegrals.efvs_q2": [
          126136129.13561843,
          54879782.718396455,
          26123655.905649934,
          16584598.876416741,
          12252982.631154658,
          9869760.720818885,
          8392978.268310219,
          7401745.194067882,
          6697234.482130702,
          6173440.79552777
        ],
        "DivaIntegrals.efvs_q3": [
          76629442.04398118,
          42831867.74060151,
          22034029.88012886,
          14122082.256920334,
          10454862.494814748,
          8426953.306219777,
          7168060.149007513,
          6322382.219974159,
          5721062.845489742,
          5273876.127396688
        ],
        "DivaIntegrals.efvs_q4": [
          76858020.60995768,
          59757186.23873286,
          40760818.660430565,
          28438383.340502568,
          21564984.044689834,
          17530699.959140975,
          14967383.467839181,
          13226617.707026154,
          11981609.296751522,
          11052512.315654451
        ],
        "DivaIntegrals.thck": 434.50421401903714,
        "DivaIntegrals.ice_mask": 1.0,
        "DivaIntegrals.omega_se": 5.508893261498528e-06,
        "DivaIntegrals.omega_nw": 2.4254396193143267e-05,
        "DivaIntegrals.omega_ne": 2.0727382899639804e-05,
        "DivaIntegrals.ipl_mask_sw": 1.0,
        "DivaIntegrals.ipl_mask_se": 1.0,
        "DivaIntegrals.ipl_mask_nw": 1.0,
        "DivaIntegrals.ipl_mask_ne": 1.0,
        "DivaIntegrals.omega_k_se": [
          6.917088510191423e-06,
          6.8843753205440805e-06,
          6.714376541467536e-06,
          6.302048965478592e-06,
          5.6549236045440115e-06,
          4.832815842229762e-06,
          3.90211147798462e-06,
          2.9184690884992105e-06,
          1.923128704543543e-06,
          9.443238694086973e-07,
          0.0
        ],
        "DivaIntegrals.omega_k_nw": [
          3.1174626399567155e-05,
          3.071943838139048e-05,
          2.9496944337137618e-05,
          2.7433566261136264e-05,
          2.4503764066238927e-05,
          2.0889792658044365e-05,
          1.6842084827191792e-05,
          1.258442335346978e-05,
          8.286727964523265e-06,
          4.066785490451196e-06,
          0.0
        ],
        "DivaIntegrals.omega_k_ne": [
          2.5996109279234316e-05,
          2.5887639943119815e-05,
          2.526858982249929e-05,
          2.372456199747502e-05,
          2.1291271646139458e-05,
          1.8197100297131605e-05,
          1.4693092214204161e-05,
          1.0989278089584608e-05,
          7.241229931226304e-06,
          3.555588499998292e-06,
          0.0
        ]
      },
      "assertions": [
        {
          "variable": "beta_internal",
          "time": 0.0,
          "expected": 1229942.7460914883,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "beta_eff_x",
          "time": 0.0,
          "expected": 62267.33460333767,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "beta_eff_y",
          "time": 0.0,
          "expected": 62253.971668623264,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "btractx",
          "time": 0.0,
          "expected": 62665.04978894747,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "btracty",
          "time": 0.0,
          "expected": -34143.780537606755,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "uvel_basal_recovered",
          "time": 0.0,
          "expected": 0.05094956654534079,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "vvel_basal_recovered",
          "time": 0.0,
          "expected": -0.027760463359866833,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "uvel",
          "time": 0.0,
          "expected": 1.26357985736417,
          "coords": {
            "lev_nodes": 1
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "vvel",
          "time": 0.0,
          "expected": -0.6886255547082697,
          "coords": {
            "lev_nodes": 1
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "uvel",
          "time": 0.0,
          "expected": 0.8820374901987009,
          "coords": {
            "lev_nodes": 6
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "vvel",
          "time": 0.0,
          "expected": -0.4806907593801484,
          "coords": {
            "lev_nodes": 6
          },
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "velo_step3_cell2414",
      "description": "Dump pin, step 3, cell (24,14): the fastest traced column (uvel_2d = 5.02 m/yr) on a moderate slope (theta_x = 0.0154 rad): beta_internal = 9.70e5 Pa yr/m with the largest basal traction of the pinned rows (btractx = 3.72e4 Pa) and the strongest profile shear (uvel spans 5.13 down to 4.92 m/yr). All at rel 1e-12 (accepted-pass chain reason).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "BasalTraction.u": -0.061353276116788,
        "BasalTraction.v": -0.06876027735165609,
        "BasalTraction.bed": 1170.4000244140625,
        "BasalTraction.N_stag": 3521901.1037544804,
        "uvel_2d": -5.0211015462978335,
        "vvel_2d": -5.630944873896263,
        "uvel_basal": -0.06135326057407625,
        "vvel_basal": -0.06876025989913012,
        "f_ground": 1.0,
        "DivaGeometry.usrf_sw": 1289.0543401092405,
        "DivaGeometry.thck_sw": 118.65431569517798,
        "DivaGeometry.ice_mask_sw": 1.0,
        "DivaGeometry.land_mask_sw": 1.0,
        "DivaGeometry.usrf_se": 1693.4477218315672,
        "DivaGeometry.thck_se": 190.84774624562968,
        "DivaGeometry.ice_mask_se": 1.0,
        "DivaGeometry.land_mask_se": 1.0,
        "DivaGeometry.usrf_nw": 1729.9481148939894,
        "DivaGeometry.thck_nw": 600.4481148939893,
        "DivaGeometry.ice_mask_nw": 1.0,
        "DivaGeometry.land_mask_nw": 1.0,
        "DivaGeometry.usrf_ne": 2005.3884265448567,
        "DivaGeometry.thck_ne": 656.6884753729817,
        "DivaGeometry.ice_mask_ne": 1.0,
        "DivaGeometry.land_mask_ne": 1.0,
        "DivaIntegrals.sigma": [
          0.0,
          0.23140495867768607,
          0.4074074074074073,
          0.5443786982248522,
          0.6530612244897959,
          0.7407407407407408,
          0.8125,
          0.8719723183391004,
          0.9218106995884773,
          0.96398891966759,
          1.0
        ],
        "DivaIntegrals.efvs_q1": [
          27204222.270195074,
          26429966.505905874,
          24349254.17409404,
          22154135.88088036,
          20138101.920219637,
          18398657.435496002,
          16945807.336416315,
          15749630.525729988,
          14767440.48609012,
          13957656.410028402
        ],
        "DivaIntegrals.efvs_q2": [
          28280730.924030997,
          26952469.815480452,
          24085014.035801973,
          21151513.414980415,
          18573584.758513164,
          16469599.817743286,
          14810439.8045167,
          13513989.96485717,
          12495523.040432045,
          11685602.673093408
        ],
        "DivaIntegrals.efvs_q3": [
          23595949.964201137,
          16035436.616285693,
          9164824.376810016,
          5990288.461791572,
          4454668.806634897,
          3595787.652441714,
          3060245.22279873,
          2699479.9441044047,
          2442193.6700120657,
          2250538.4118048
        ],
        "DivaIntegrals.efvs_q4": [
          22856764.51486827,
          16447401.641958266,
          9896517.141890028,
          6558504.591362735,
          4894503.08994623,
          3955595.3416777197,
          3368215.007761929,
          2971926.204156804,
          2689076.206916499,
          2478277.0163590824
        ],
        "DivaIntegrals.thck": 118.65431569517798,
        "DivaIntegrals.ice_mask": 1.0,
        "DivaIntegrals.omega_se": 1.0113188674798673e-05,
        "DivaIntegrals.omega_nw": 0.0001684390033841888,
        "DivaIntegrals.omega_ne": 0.00014847784194165091,
        "DivaIntegrals.ipl_mask_sw": 1.0,
        "DivaIntegrals.ipl_mask_se": 1.0,
        "DivaIntegrals.ipl_mask_nw": 1.0,
        "DivaIntegrals.ipl_mask_ne": 1.0,
        "DivaIntegrals.omega_k_se": [
          1.2910388197254002e-05,
          1.276134022261245e-05,
          1.2322878022626229e-05,
          1.1485223332473326e-05,
          1.0260224111974054e-05,
          8.744596332160335e-06,
          7.048386222893679e-06,
          5.265783756339049e-06,
          3.467443999811232e-06,
          1.7019303311490003e-06,
          0.0
        ],
        "DivaIntegrals.omega_k_nw": [
          0.00021294879459276883,
          0.00021113418683995134,
          0.0002050087079633802,
          0.00019207718693654694,
          0.0001722417794655061,
          0.0001471713814403996,
          0.00011882862350826739,
          8.88826002482524e-05,
          5.8577776855887045e-05,
          2.8770491628245327e-05,
          0.0
        ],
        "DivaIntegrals.omega_k_ne": [
          0.00018688618249744694,
          0.00018570262005309415,
          0.0001808506820899046,
          0.00016967408865108474,
          0.0001522373632571439,
          0.00013010919343072765,
          0.00010506151779839757,
          7.858592340365684e-05,
          5.179017434051772e-05,
          2.5435102300096016e-05,
          0.0
        ]
      },
      "assertions": [
        {
          "variable": "beta_internal",
          "time": 0.0,
          "expected": 970654.3150698128,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "beta_eff_x",
          "time": 0.0,
          "expected": 11860.5064189031,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "beta_eff_y",
          "time": 0.0,
          "expected": 11852.796372739278,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "btractx",
          "time": 0.0,
          "expected": -59552.80711982973,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "btracty",
          "time": 0.0,
          "expected": -66742.44297641247,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "uvel_basal_recovered",
          "time": 0.0,
          "expected": -0.06135326057407625,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "vvel_basal_recovered",
          "time": 0.0,
          "expected": -0.06876025989913012,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "uvel",
          "time": 0.0,
          "expected": -6.323793575868588,
          "coords": {
            "lev_nodes": 1
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "vvel",
          "time": 0.0,
          "expected": -7.09186852288701,
          "coords": {
            "lev_nodes": 1
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "uvel",
          "time": 0.0,
          "expected": -4.397338526571521,
          "coords": {
            "lev_nodes": 6
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "vvel",
          "time": 0.0,
          "expected": -4.931416415750771,
          "coords": {
            "lev_nodes": 6
          },
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "marine_step1_cell2749",
      "description": "Dump pin, cism_velo_marine_exit.csv / cism_velo_marine_pass.csv step 1, cell (27,49): the first marine-margin cell (initial ice over a marine bed, topg = -6.8 m < eus = 0) with thck = 2143 m, fully grounded (f_ground = 1.0 - the reference run has no partially grounded vertices, so the f_ground < 1 branch of beta_internal = f_ground*beta_raw is documented in the README, not exercised). The accepted calcbeta pass (the marine pass row whose f_ground*beta equals the dumped beta_internal, velo_iter 38 of 39) feeds the mounted BasalTraction: beta_internal = 3.19e6 Pa yr/m with the largest omega of the pinned rows (2.36e-4 m/(Pa yr), the deep marine column), so the beta_eff correction is the strongest of all pinned rows (beta_eff_x/beta_internal = 1.35e-3) and the basal velocity is strongly reduced below uvel_2d (uvel_basal = -0.0232 vs uvel_2d = -17.14 m/yr). All assertions at rel 1e-12.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "BasalTraction.u": -0.02316379173631204,
        "BasalTraction.v": 0.007073409984318888,
        "BasalTraction.bed": -6.78439998626709,
        "BasalTraction.N_stag": 18951759.88798822,
        "uvel_2d": -17.137045483112377,
        "vvel_2d": 5.233347053051022,
        "uvel_basal": -0.02316379172088001,
        "vvel_basal": 0.00707340997927847,
        "f_ground": 1.0,
        "DivaGeometry.usrf_sw": 2136.393486247367,
        "DivaGeometry.thck_sw": 2143.177886233634,
        "DivaGeometry.ice_mask_sw": 1.0,
        "DivaGeometry.land_mask_sw": 0.0,
        "DivaGeometry.usrf_se": 2214.131280710165,
        "DivaGeometry.thck_se": 2087.3712785739344,
        "DivaGeometry.ice_mask_se": 1.0,
        "DivaGeometry.land_mask_se": 1.0,
        "DivaGeometry.usrf_nw": 2112.0647941064885,
        "DivaGeometry.thck_nw": 2079.489793343549,
        "DivaGeometry.ice_mask_nw": 1.0,
        "DivaGeometry.land_mask_nw": 1.0,
        "DivaGeometry.usrf_ne": 2190.4640292949316,
        "DivaGeometry.thck_ne": 2120.2260303325293,
        "DivaGeometry.ice_mask_ne": 1.0,
        "DivaGeometry.land_mask_ne": 1.0,
        "DivaIntegrals.sigma": [
          0.0,
          0.23140495867768607,
          0.4074074074074073,
          0.5443786982248522,
          0.6530612244897959,
          0.7407407407407408,
          0.8125,
          0.8719723183391004,
          0.9218106995884773,
          0.96398891966759,
          1.0
        ],
        "DivaIntegrals.efvs_q1": [
          85168039.3705319,
          17219489.533911932,
          7777516.376759191,
          4914666.518037892,
          3627509.333751026,
          2920978.866283367,
          2483528.3610214335,
          2190011.288225249,
          1981453.1742331404,
          1826693.683825694
        ],
        "DivaIntegrals.efvs_q2": [
          88723860.24655117,
          17868398.77565617,
          8070203.980714114,
          5099598.323276967,
          3764004.3639305737,
          3030887.9887314104,
          2576977.04655566,
          2272415.5738035,
          2056009.9130658417,
          1895427.205674019
        ],
        "DivaIntegrals.efvs_q3": [
          100855196.01378764,
          17875387.929022443,
          8062993.192877823,
          5094544.00872194,
          3760199.6398153575,
          3027805.122711569,
          2574349.0066930065,
          2270095.0936842933,
          2053908.861327935,
          1893489.368713958
        ],
        "DivaIntegrals.efvs_q4": [
          88699507.63144803,
          17633180.36426459,
          7962684.493321312,
          5031594.406779306,
          3713801.577538055,
          2990460.8298217454,
          2542603.473684265,
          2242104.083296494,
          2028584.8395420017,
          1870144.0314012168
        ],
        "DivaIntegrals.thck": 2143.177886233634,
        "DivaIntegrals.ice_mask": 1.0,
        "DivaIntegrals.omega_se": 0.00022645328154437274,
        "DivaIntegrals.omega_nw": 0.00022609887289801224,
        "DivaIntegrals.omega_ne": 0.00023659612866137173,
        "DivaIntegrals.ipl_mask_sw": 1.0,
        "DivaIntegrals.ipl_mask_se": 1.0,
        "DivaIntegrals.ipl_mask_nw": 1.0,
        "DivaIntegrals.ipl_mask_ne": 1.0,
        "DivaIntegrals.omega_k_se": [
          0.00028337921686380756,
          0.00028275540628027503,
          0.0002762009125304221,
          0.0002593724265036362,
          0.00023278721373911555,
          0.00019896421682310785,
          0.00016065441539661645,
          0.00012015662712335751,
          7.917310871128502e-05,
          3.8871551858578015e-05,
          0.0
        ],
        "DivaIntegrals.omega_k_nw": [
          0.00028289427333913426,
          0.00028231669789491337,
          0.0002757758038697495,
          0.0002589740494320133,
          0.00023243005809257865,
          0.00019865920605193697,
          0.0001604083146275971,
          0.00011997269207326765,
          7.905199393065904e-05,
          3.881213161545013e-05,
          0.0
        ],
        "DivaIntegrals.omega_k_ne": [
          0.0002961026780344589,
          0.00029541997227000577,
          0.0002885657294356172,
          0.0002709826490752391,
          0.0002432071194560407,
          0.00020787014025183367,
          0.00016784560502191377,
          0.00012553513662645304,
          8.2717147937712e-05,
          4.0611585563861845e-05,
          0.0
        ]
      },
      "assertions": [
        {
          "variable": "beta_internal",
          "time": 0.0,
          "expected": 3194661.040226113,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "beta_eff_x",
          "time": 0.0,
          "expected": 4318.157586004599,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "beta_eff_y",
          "time": 0.0,
          "expected": 4317.914912440877,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "btractx",
          "time": 0.0,
          "expected": -74000.46295460756,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "btracty",
          "time": 0.0,
          "expected": 22597.147282347527,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "uvel_basal_recovered",
          "time": 0.0,
          "expected": -0.02316379172088001,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "vvel_basal_recovered",
          "time": 0.0,
          "expected": 0.00707340997927847,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "uvel",
          "time": 0.0,
          "expected": -21.438665775384326,
          "coords": {
            "lev_nodes": 1
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "vvel",
          "time": 0.0,
          "expected": 6.546985020252344,
          "coords": {
            "lev_nodes": 1
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "uvel",
          "time": 0.0,
          "expected": -15.059658886783614,
          "coords": {
            "lev_nodes": 6
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "vvel",
          "time": 0.0,
          "expected": 4.598950309480875,
          "coords": {
            "lev_nodes": 6
          },
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "marine_step3_cell3951",
      "description": "Dump pin, step 3, cell (39,51): the deep-bed marine cell (topg = -56.7 m, the deepest marine bed of the pinned rows) with thck = 2788 m, fully grounded (f_ground = 1.0); the accepted-pass chain gives beta_internal = 4.43e6 Pa yr/m with the strong beta_eff correction of the marine columns (beta_eff_x/beta_internal = 1.2e-3). All at rel 1e-12.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "BasalTraction.u": -0.004097627365390254,
        "BasalTraction.v": -0.013884201080792235,
        "BasalTraction.bed": -56.68000030517578,
        "BasalTraction.N_stag": 24434635.111505523,
        "uvel_2d": -3.4169918332703304,
        "vvel_2d": -11.57927555762732,
        "uvel_basal": -0.004097627350853731,
        "vvel_basal": -0.01388420101238741,
        "f_ground": 1.0,
        "DivaGeometry.usrf_sw": 2731.638168957832,
        "DivaGeometry.thck_sw": 2788.318169263008,
        "DivaGeometry.ice_mask_sw": 1.0,
        "DivaGeometry.land_mask_sw": 0.0,
        "DivaGeometry.usrf_se": 2743.8897497243092,
        "DivaGeometry.thck_se": 2574.5397436207936,
        "DivaGeometry.ice_mask_se": 1.0,
        "DivaGeometry.land_mask_se": 1.0,
        "DivaGeometry.usrf_nw": 2779.8389433012903,
        "DivaGeometry.thck_nw": 2845.5499418364466,
        "DivaGeometry.ice_mask_nw": 1.0,
        "DivaGeometry.land_mask_nw": 0.0,
        "DivaGeometry.usrf_ne": 2797.601104010106,
        "DivaGeometry.thck_ne": 2660.7911064515124,
        "DivaGeometry.ice_mask_ne": 1.0,
        "DivaGeometry.land_mask_ne": 1.0,
        "DivaIntegrals.sigma": [
          0.0,
          0.23140495867768607,
          0.4074074074074073,
          0.5443786982248522,
          0.6530612244897959,
          0.7407407407407408,
          0.8125,
          0.8719723183391004,
          0.9218106995884773,
          0.96398891966759,
          1.0
        ],
        "DivaIntegrals.efvs_q1": [
          37079171.12331992,
          22583547.010268785,
          12156192.043736732,
          7849296.832880841,
          5820600.220099149,
          4694049.920151845,
          3993620.080686037,
          3522754.8572412343,
          3187841.801032386,
          2938999.642986678
        ],
        "DivaIntegrals.efvs_q2": [
          37476765.221424796,
          20909409.74171123,
          10738823.906741265,
          6880935.40105849,
          5093714.760091926,
          4105512.889023377,
          3492058.3886574684,
          3079954.796923133,
          2786947.117501243,
          2569288.982559246
        ],
        "DivaIntegrals.efvs_q3": [
          37532142.0043102,
          22302909.516159385,
          11830213.223302448,
          7619031.856503702,
          5646513.757672004,
          4552767.8040245455,
          3873097.8607036336,
          3416299.8232022165,
          3091434.2461707043,
          2850075.7649238226
        ],
        "DivaIntegrals.efvs_q4": [
          37197579.77844654,
          24473776.310724374,
          13918484.578418985,
          9090778.45003157,
          6759568.013121214,
          5456243.648720222,
          4643884.381609179,
          4097152.4992883666,
          3708042.9227468427,
          3418829.49876402
        ],
        "DivaIntegrals.thck": 2788.318169263008,
        "DivaIntegrals.ice_mask": 1.0,
        "DivaIntegrals.omega_se": 0.00021530023108383322,
        "DivaIntegrals.omega_nw": 0.0001583128315591433,
        "DivaIntegrals.omega_ne": 0.000180720854196388,
        "DivaIntegrals.ipl_mask_sw": 1.0,
        "DivaIntegrals.ipl_mask_se": 1.0,
        "DivaIntegrals.ipl_mask_nw": 1.0,
        "DivaIntegrals.ipl_mask_ne": 1.0,
        "DivaIntegrals.omega_k_se": [
          0.00027091562530804774,
          0.0002692119877507113,
          0.0002622714124574342,
          0.0002461066456731526,
          0.0002208171016867634,
          0.0001887074071878481,
          0.00015236161563041332,
          0.00011395004735578087,
          7.508246394161987e-05,
          3.686387621431409e-05,
          0.0
        ],
        "DivaIntegrals.omega_k_nw": [
          0.00020072207899511199,
          0.0001987550991921841,
          0.00019260621296650118,
          0.00018030660635640598,
          0.00016161298082666823,
          0.0001380399959182333,
          0.00011141865829530853,
          8.331246252681584e-05,
          5.48874167339142e-05,
          2.6945629009976755e-05,
          0.0
        ],
        "DivaIntegrals.omega_k_ne": [
          0.00022802091513407415,
          0.00022627265667654123,
          0.00022002885831804401,
          0.00020632143167519893,
          0.00018506561585113982,
          0.00015813068107640155,
          0.0001276624698356378,
          9.547192637883673e-05,
          6.290430455016191e-05,
          3.0883567135472505e-05,
          0.0
        ]
      },
      "assertions": [
        {
          "variable": "beta_internal",
          "time": 0.0,
          "expected": 4428059.845582935,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "beta_eff_x",
          "time": 0.0,
          "expected": 5310.091454655901,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "beta_eff_y",
          "time": 0.0,
          "expected": 5309.492177207703,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "btractx",
          "time": 0.0,
          "expected": -18144.53913447778,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "btracty",
          "time": 0.0,
          "expected": -61480.07299095462,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "uvel_basal_recovered",
          "time": 0.0,
          "expected": -0.004097627350853731,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "vvel_basal_recovered",
          "time": 0.0,
          "expected": -0.01388420101238741,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "uvel",
          "time": 0.0,
          "expected": -4.312128670186737,
          "coords": {
            "lev_nodes": 1
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "vvel",
          "time": 0.0,
          "expected": -14.612656381065854,
          "coords": {
            "lev_nodes": 1
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "uvel",
          "time": 0.0,
          "expected": -2.989264450957046,
          "coords": {
            "lev_nodes": 6
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "vvel",
          "time": 0.0,
          "expected": -10.12982114388851,
          "coords": {
            "lev_nodes": 6
          },
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "floating_vertex_basal_recovery",
      "description": "A fully floating vertex with nonzero raw basal drag and nonzero depth-averaged flow. The drag weighting is zero and recovery uses the depth-averaged velocity in both directions.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "BasalTraction.N_stag": 200000.0,
        "uvel_2d": 2.0,
        "vvel_2d": -3.0,
        "f_ground": 0.0
      },
      "assertions": [
        {
          "variable": "beta_internal",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "abs": 1e-09,
            "rel": 0.0
          }
        },
        {
          "variable": "uvel_basal_recovered",
          "time": 0.0,
          "expected": 2.0,
          "tolerance": {
            "abs": 1e-09,
            "rel": 0.0
          }
        },
        {
          "variable": "vvel_basal_recovered",
          "time": 0.0,
          "expected": -3.0,
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
