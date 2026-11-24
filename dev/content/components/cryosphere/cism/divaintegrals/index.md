---
title: "DivaIntegrals"
slug: "divaintegrals"
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
| `sigma` | `1` | `0.0` | sigma coordinates of the 11 velocity levels (sigma_001 = 0 at the surface .. sigma_011 = 1 at the bed; the dump's sigma_001..011 of cism_velo_nbr.csv) |
| `efvs_q1` | `Pa yr` | `0.0` | effective viscosity at quadrature point 1 of each layer (Pa yr; the dump's efvs_q1_001..010, solver units) |
| `efvs_q2` | `Pa yr` | `0.0` | effective viscosity at quadrature point 2 of each layer (the dump's efvs_q2_001..010) |
| `efvs_q3` | `Pa yr` | `0.0` | effective viscosity at quadrature point 3 of each layer (the dump's efvs_q3_001..010) |
| `efvs_q4` | `Pa yr` | `0.0` | effective viscosity at quadrature point 4 of each layer (the dump's efvs_q4_001..010) |
| `thck` | `m` | `0.0` | ice thickness of the traced cell (m; cism_velo.csv thck) |
| `ice_mask` | `1` | `0.0` | ice mask of the traced cell (cism_velo.csv ice_mask): 1 where thck > thklim; the active_cell guard of the element loop (F90:5091) skips the whole DIVA block on ice-free cells |
| `omega_se` | `m/(Pa yr)` | `0.0` | cell-centered omega of the SE stencil cell (cism_velo_nbr.csv omega_se): the stagger input alongside the model's own omega for the SW cell |
| `omega_nw` | `m/(Pa yr)` | `0.0` | cell-centered omega of the NW stencil cell (cism_velo_nbr.csv omega_nw) |
| `omega_ne` | `m/(Pa yr)` | `0.0` | cell-centered omega of the NE stencil cell (cism_velo_nbr.csv omega_ne) |
| `ipl_mask_sw` | `1` | `1.0` | ice_plus_land_mask of the SW stencil cell (cism_velo_stag.csv ice_plus_land_mask_sw): 1 where ice_mask = 1 or land_mask = 1, the mask array glissade_stagger averages over with stagger_margin_in = 1 (glissade_grid_operators.F90:133-146; computed at glissade_velo_higher.F90:1532-1537) |
| `ipl_mask_se` | `1` | `1.0` | ice_plus_land_mask of the SE stencil cell (cism_velo_stag.csv ice_plus_land_mask_se) |
| `ipl_mask_nw` | `1` | `1.0` | ice_plus_land_mask of the NW stencil cell (cism_velo_stag.csv ice_plus_land_mask_nw) |
| `ipl_mask_ne` | `1` | `1.0` | ice_plus_land_mask of the NE stencil cell (cism_velo_stag.csv ice_plus_land_mask_ne) |
| `omega_k_se` | `m/(Pa yr)` | `0.0` | per-level cell-centered omega_k of the SE stencil cell (cism_velo_stag.csv omega_k_se_001..011): the per-level stagger input alongside the model's own omega_k for the SW cell |
| `omega_k_nw` | `m/(Pa yr)` | `0.0` | per-level cell-centered omega_k of the NW stencil cell (cism_velo_stag.csv omega_k_nw_001..011) |
| `omega_k_ne` | `m/(Pa yr)` | `0.0` | per-level cell-centered omega_k of the NE stencil cell (cism_velo_stag.csv omega_k_ne_001..011) |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `dz` | `1` |  | sigma layer widths dz[l] = sigma[l+1] - sigma[l] (cism_sigma_measure): the dimensionless measure of the imported integral rules (the Fortran dsigma = sigma(k+1) - sigma(k), F90:5636, 5658) |
| `sig_mid` | `1` |  | sigma layer midpoints sig_mid[l] = 0.5*(sigma[l] + sigma[l+1]) (cism_sigma_midpoint; the Fortran depth = 0.5*(sigma(k)+sigma(k+1)), F90:5634) |
| `z_sfc` | `1` |  | surface bound of the integral rules: the sigma surface sigma(1) = 0 |
| `z_top` | `1` |  | bed bound of the integral rules: the sigma bed sigma(11) = 1 (the DIVA integrals run from the surface / each interface to the BED) |
| `efvs` | `Pa yr` |  | cell-centered effective viscosity of the traced cell: the arithmetic mean of the four quad-point viscosities (F90:5266-5272), zeroed on ice-free cells by the active_cell guard (the dumped efvs_001..010 column) |
| `efvs_qp_mean_recip` | `1/(Pa yr)` |  | quad-point mean of the reciprocal viscosities (1/4)*sum_p 1/efvs_qp(p)[l] (the Fortran computes the integral at each quad point and averages, F90:5627-5653; the mean of the reciprocals, NOT the reciprocal of the mean - the harmonic construction, distinct from the arithmetic-mean efvs above) |
| `omega_integrand` | `m/(Pa yr)` |  | DIVA single-integral integrand f[l] = sig_mid[l]*thck*efvs_qp_mean_recip[l]: the layer depth factor (s - z)/H times thck/efvs of Goldberg (2011) eq. 32, with the mean over the quadrature points taken inside the integrand (integral linearity: the four-integral construction of the Fortran averages bit-for-bit) |
| `omega_k` | `m/(Pa yr)` |  | Goldberg (2011) single integral at each velocity level: the interface-to-bed cumulative integral of omega_integrand (the imported integral_lev_nodes_cumulative_to_top rule, the exact suffix scan of F90:5631-5637), zeroed on ice-free cells by the active_cell guard (the dumped omega_k_001..011 column) |
| `omega_layer_avg` | `m/(Pa yr)` |  | layer-averaged single integral g[l] = 0.5*(omega_k[l] + omega_k[l+1]): the trapezoid mean of the interface values, the integrand of the double integral (the Fortran layer_avg, F90:5656) |
| `omega` | `m/(Pa yr)` |  | Goldberg (2011) double integral: the whole-column integral of omega_layer_avg over the sigma measure (the imported integral_lev_whole rule, the exact trapezoid sum of F90:5655-5661, no thck factor - omega here is Goldberg's omega/H; the dumped omega column) |
| `stag_omega` | `m/(Pa yr)` |  | staggered omega at the vertex: the ice-masked 4-cell mean of the cell-centered omegas of the four stencil cells (cism_stagger_masked_mean, glissade_stagger with ice_plus_land_mask and stagger_margin = 1; the dumped stag_omega column). On every traced row of the reference run the four masks are 1, so the masked mean equals the plain 4-cell mean 0.25*(omega + omega_se + omega_nw + omega_ne) exactly |
| `stag_omega_k` | `m/(Pa yr)` |  | the single integral staggered to the vertex at each velocity level: the ice-masked 4-cell mean of the four stencil cells' omega_k per level (cism_stagger_masked_mean; the per-level glissade_stagger call of glissade_velo_higher.F90:2561-2564; the dumped stag_omega_k_001..011 column) |

## Observed expressions

$$
dz = \mathrm{cism_sigma_measure}\left(sigma=sigma\right)
$$
_sigma layer widths dz[l] = sigma[l+1] - sigma[l] (cism_sigma_measure): the dimensionless measure of the imported integral rules (the Fortran dsigma = sigma(k+1) - sigma(k), F90:5636, 5658)_

$$
sig_{mid} = \mathrm{cism_sigma_midpoint}\left(sigma=sigma\right)
$$
_sigma layer midpoints sig_mid[l] = 0.5*(sigma[l] + sigma[l+1]) (cism_sigma_midpoint; the Fortran depth = 0.5*(sigma(k)+sigma(k+1)), F90:5634)_

$$
z_{sfc} = \mathrm{const}\left(\right)
$$
_surface bound of the integral rules: the sigma surface sigma(1) = 0_

$$
z_{top} = \mathrm{const}\left(\right)
$$
_bed bound of the integral rules: the sigma bed sigma(11) = 1 (the DIVA integrals run from the surface / each interface to the BED)_

$$
efvs = \mathrm{faq}\left(efvs_{q1}, efvs_{q2}, efvs_{q3}, efvs_{q4}, ice_{mask}\right)
$$
_cell-centered effective viscosity of the traced cell: the arithmetic mean of the four quad-point viscosities (F90:5266-5272), zeroed on ice-free cells by the active_cell guard (the dumped efvs_001..010 column)_

$$
efvs_{qp\,mean\,recip} = \mathrm{faq}\left(efvs_{q1}, efvs_{q2}, efvs_{q3}, efvs_{q4}\right)
$$
_quad-point mean of the reciprocal viscosities (1/4)*sum_p 1/efvs_qp(p)[l] (the Fortran computes the integral at each quad point and averages, F90:5627-5653; the mean of the reciprocals, NOT the reciprocal of the mean - the harmonic construction, distinct from the arithmetic-mean efvs above)_

$$
omega_{integrand} = \mathrm{faq}\left(sig_{mid}, efvs_{qp\,mean\,recip}, thck\right)
$$
_DIVA single-integral integrand f[l] = sig_mid[l]*thck*efvs_qp_mean_recip[l]: the layer depth factor (s - z)/H times thck/efvs of Goldberg (2011) eq. 32, with the mean over the quadrature points taken inside the integrand (integral linearity: the four-integral construction of the Fortran averages bit-for-bit)_

$$
omega_{k} = \mathrm{ifelse}\left(ice_{mask} = 1.0, \mathrm{integral}\left(omega_{integrand}\right), 0.0\right)
$$
_Goldberg (2011) single integral at each velocity level: the interface-to-bed cumulative integral of omega_integrand (the imported integral_lev_nodes_cumulative_to_top rule, the exact suffix scan of F90:5631-5637), zeroed on ice-free cells by the active_cell guard (the dumped omega_k_001..011 column)_

$$
omega_{layer\,avg} = \mathrm{faq}\left(omega_{k}\right)
$$
_layer-averaged single integral g[l] = 0.5*(omega_k[l] + omega_k[l+1]): the trapezoid mean of the interface values, the integrand of the double integral (the Fortran layer_avg, F90:5656)_

$$
omega = \mathrm{integral}\left(omega_{layer\,avg}\right)
$$
_Goldberg (2011) double integral: the whole-column integral of omega_layer_avg over the sigma measure (the imported integral_lev_whole rule, the exact trapezoid sum of F90:5655-5661, no thck factor - omega here is Goldberg's omega/H; the dumped omega column)_

$$
stag_{omega} = \mathrm{cism_stagger_masked_mean}\left(var_{sw}=omega, var_{se}=omega_{se}, var_{nw}=omega_{nw}, var_{ne}=omega_{ne}, mask_{sw}=ipl_{mask\,sw}, mask_{se}=ipl_{mask\,se}, mask_{nw}=ipl_{mask\,nw}, mask_{ne}=ipl_{mask\,ne}\right)
$$
_staggered omega at the vertex: the ice-masked 4-cell mean of the cell-centered omegas of the four stencil cells (cism_stagger_masked_mean, glissade_stagger with ice_plus_land_mask and stagger_margin = 1; the dumped stag_omega column). On every traced row of the reference run the four masks are 1, so the masked mean equals the plain 4-cell mean 0.25*(omega + omega_se + omega_nw + omega_ne) exactly_

$$
stag_{omega\,k} = \mathrm{faq}\left(omega_{k}, omega_{k\,se}, omega_{k\,nw}, omega_{k\,ne}, ipl_{mask\,sw}, ipl_{mask\,se}, ipl_{mask\,nw}, ipl_{mask\,ne}\right)
$$
_the single integral staggered to the vertex at each velocity level: the ice-masked 4-cell mean of the four stencil cells' omega_k per level (cism_stagger_masked_mean; the per-level glissade_stagger call of glissade_velo_higher.F90:2561-2564; the dumped stag_omega_k_001..011 column)_

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "expression_template_imports": [
    {
      "ref": "./cism_velo_discretization.esm"
    },
    {
      "ref": "./cism_templates.esm"
    }
  ],
  "variables": {
    "sigma": {
      "type": "parameter",
      "units": "1",
      "shape": [
        "lev_nodes"
      ],
      "default": 0.0,
      "description": "sigma coordinates of the 11 velocity levels (sigma_001 = 0 at the surface .. sigma_011 = 1 at the bed; the dump's sigma_001..011 of cism_velo_nbr.csv)"
    },
    "efvs_q1": {
      "type": "parameter",
      "units": "Pa yr",
      "shape": [
        "lev"
      ],
      "default": 0.0,
      "description": "effective viscosity at quadrature point 1 of each layer (Pa yr; the dump's efvs_q1_001..010, solver units)"
    },
    "efvs_q2": {
      "type": "parameter",
      "units": "Pa yr",
      "shape": [
        "lev"
      ],
      "default": 0.0,
      "description": "effective viscosity at quadrature point 2 of each layer (the dump's efvs_q2_001..010)"
    },
    "efvs_q3": {
      "type": "parameter",
      "units": "Pa yr",
      "shape": [
        "lev"
      ],
      "default": 0.0,
      "description": "effective viscosity at quadrature point 3 of each layer (the dump's efvs_q3_001..010)"
    },
    "efvs_q4": {
      "type": "parameter",
      "units": "Pa yr",
      "shape": [
        "lev"
      ],
      "default": 0.0,
      "description": "effective viscosity at quadrature point 4 of each layer (the dump's efvs_q4_001..010)"
    },
    "thck": {
      "type": "parameter",
      "units": "m",
      "default": 0.0,
      "description": "ice thickness of the traced cell (m; cism_velo.csv thck)"
    },
    "ice_mask": {
      "type": "parameter",
      "units": "1",
      "default": 0.0,
      "description": "ice mask of the traced cell (cism_velo.csv ice_mask): 1 where thck > thklim; the active_cell guard of the element loop (F90:5091) skips the whole DIVA block on ice-free cells"
    },
    "omega_se": {
      "type": "parameter",
      "units": "m/(Pa yr)",
      "default": 0.0,
      "description": "cell-centered omega of the SE stencil cell (cism_velo_nbr.csv omega_se): the stagger input alongside the model's own omega for the SW cell"
    },
    "omega_nw": {
      "type": "parameter",
      "units": "m/(Pa yr)",
      "default": 0.0,
      "description": "cell-centered omega of the NW stencil cell (cism_velo_nbr.csv omega_nw)"
    },
    "omega_ne": {
      "type": "parameter",
      "units": "m/(Pa yr)",
      "default": 0.0,
      "description": "cell-centered omega of the NE stencil cell (cism_velo_nbr.csv omega_ne)"
    },
    "ipl_mask_sw": {
      "type": "parameter",
      "units": "1",
      "default": 1.0,
      "description": "ice_plus_land_mask of the SW stencil cell (cism_velo_stag.csv ice_plus_land_mask_sw): 1 where ice_mask = 1 or land_mask = 1, the mask array glissade_stagger averages over with stagger_margin_in = 1 (glissade_grid_operators.F90:133-146; computed at glissade_velo_higher.F90:1532-1537)"
    },
    "ipl_mask_se": {
      "type": "parameter",
      "units": "1",
      "default": 1.0,
      "description": "ice_plus_land_mask of the SE stencil cell (cism_velo_stag.csv ice_plus_land_mask_se)"
    },
    "ipl_mask_nw": {
      "type": "parameter",
      "units": "1",
      "default": 1.0,
      "description": "ice_plus_land_mask of the NW stencil cell (cism_velo_stag.csv ice_plus_land_mask_nw)"
    },
    "ipl_mask_ne": {
      "type": "parameter",
      "units": "1",
      "default": 1.0,
      "description": "ice_plus_land_mask of the NE stencil cell (cism_velo_stag.csv ice_plus_land_mask_ne)"
    },
    "omega_k_se": {
      "type": "parameter",
      "units": "m/(Pa yr)",
      "shape": [
        "lev_nodes"
      ],
      "default": 0.0,
      "description": "per-level cell-centered omega_k of the SE stencil cell (cism_velo_stag.csv omega_k_se_001..011): the per-level stagger input alongside the model's own omega_k for the SW cell"
    },
    "omega_k_nw": {
      "type": "parameter",
      "units": "m/(Pa yr)",
      "shape": [
        "lev_nodes"
      ],
      "default": 0.0,
      "description": "per-level cell-centered omega_k of the NW stencil cell (cism_velo_stag.csv omega_k_nw_001..011)"
    },
    "omega_k_ne": {
      "type": "parameter",
      "units": "m/(Pa yr)",
      "shape": [
        "lev_nodes"
      ],
      "default": 0.0,
      "description": "per-level cell-centered omega_k of the NE stencil cell (cism_velo_stag.csv omega_k_ne_001..011)"
    },
    "dz": {
      "type": "unknown",
      "units": "1",
      "shape": [
        "lev"
      ],
      "description": "sigma layer widths dz[l] = sigma[l+1] - sigma[l] (cism_sigma_measure): the dimensionless measure of the imported integral rules (the Fortran dsigma = sigma(k+1) - sigma(k), F90:5636, 5658)"
    },
    "sig_mid": {
      "type": "unknown",
      "units": "1",
      "shape": [
        "lev"
      ],
      "description": "sigma layer midpoints sig_mid[l] = 0.5*(sigma[l] + sigma[l+1]) (cism_sigma_midpoint; the Fortran depth = 0.5*(sigma(k)+sigma(k+1)), F90:5634)"
    },
    "z_sfc": {
      "type": "unknown",
      "units": "1",
      "description": "surface bound of the integral rules: the sigma surface sigma(1) = 0"
    },
    "z_top": {
      "type": "unknown",
      "units": "1",
      "description": "bed bound of the integral rules: the sigma bed sigma(11) = 1 (the DIVA integrals run from the surface / each interface to the BED)"
    },
    "efvs": {
      "type": "unknown",
      "units": "Pa yr",
      "shape": [
        "lev"
      ],
      "description": "cell-centered effective viscosity of the traced cell: the arithmetic mean of the four quad-point viscosities (F90:5266-5272), zeroed on ice-free cells by the active_cell guard (the dumped efvs_001..010 column)"
    },
    "efvs_qp_mean_recip": {
      "type": "unknown",
      "units": "1/(Pa yr)",
      "shape": [
        "lev"
      ],
      "description": "quad-point mean of the reciprocal viscosities (1/4)*sum_p 1/efvs_qp(p)[l] (the Fortran computes the integral at each quad point and averages, F90:5627-5653; the mean of the reciprocals, NOT the reciprocal of the mean - the harmonic construction, distinct from the arithmetic-mean efvs above)"
    },
    "omega_integrand": {
      "type": "unknown",
      "units": "m/(Pa yr)",
      "shape": [
        "lev"
      ],
      "description": "DIVA single-integral integrand f[l] = sig_mid[l]*thck*efvs_qp_mean_recip[l]: the layer depth factor (s - z)/H times thck/efvs of Goldberg (2011) eq. 32, with the mean over the quadrature points taken inside the integrand (integral linearity: the four-integral construction of the Fortran averages bit-for-bit)"
    },
    "omega_k": {
      "type": "unknown",
      "units": "m/(Pa yr)",
      "shape": [
        "lev_nodes"
      ],
      "description": "Goldberg (2011) single integral at each velocity level: the interface-to-bed cumulative integral of omega_integrand (the imported integral_lev_nodes_cumulative_to_top rule, the exact suffix scan of F90:5631-5637), zeroed on ice-free cells by the active_cell guard (the dumped omega_k_001..011 column)"
    },
    "omega_layer_avg": {
      "type": "unknown",
      "units": "m/(Pa yr)",
      "shape": [
        "lev"
      ],
      "description": "layer-averaged single integral g[l] = 0.5*(omega_k[l] + omega_k[l+1]): the trapezoid mean of the interface values, the integrand of the double integral (the Fortran layer_avg, F90:5656)"
    },
    "omega": {
      "type": "unknown",
      "units": "m/(Pa yr)",
      "description": "Goldberg (2011) double integral: the whole-column integral of omega_layer_avg over the sigma measure (the imported integral_lev_whole rule, the exact trapezoid sum of F90:5655-5661, no thck factor - omega here is Goldberg's omega/H; the dumped omega column)"
    },
    "stag_omega": {
      "type": "unknown",
      "units": "m/(Pa yr)",
      "description": "staggered omega at the vertex: the ice-masked 4-cell mean of the cell-centered omegas of the four stencil cells (cism_stagger_masked_mean, glissade_stagger with ice_plus_land_mask and stagger_margin = 1; the dumped stag_omega column). On every traced row of the reference run the four masks are 1, so the masked mean equals the plain 4-cell mean 0.25*(omega + omega_se + omega_nw + omega_ne) exactly"
    },
    "stag_omega_k": {
      "type": "unknown",
      "units": "m/(Pa yr)",
      "shape": [
        "lev_nodes"
      ],
      "description": "the single integral staggered to the vertex at each velocity level: the ice-masked 4-cell mean of the four stencil cells' omega_k per level (cism_stagger_masked_mean; the per-level glissade_stagger call of glissade_velo_higher.F90:2561-2564; the dumped stag_omega_k_001..011 column)"
    }
  },
  "equations": [
    {
      "lhs": "dz",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "cism_sigma_measure",
        "bindings": {
          "sigma": "sigma"
        }
      }
    },
    {
      "lhs": "sig_mid",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "cism_sigma_midpoint",
        "bindings": {
          "sigma": "sigma"
        }
      }
    },
    {
      "lhs": "z_sfc",
      "rhs": {
        "op": "const",
        "args": [],
        "value": 0.0,
        "units": "1"
      }
    },
    {
      "lhs": "z_top",
      "rhs": {
        "op": "const",
        "args": [],
        "value": 1.0,
        "units": "1"
      }
    },
    {
      "lhs": "efvs",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "l"
        ],
        "args": [
          "efvs_q1",
          "efvs_q2",
          "efvs_q3",
          "efvs_q4",
          "ice_mask"
        ],
        "ranges": {
          "l": {
            "from": "lev"
          }
        },
        "expr": {
          "op": "ifelse",
          "args": [
            {
              "op": "==",
              "args": [
                "ice_mask",
                1.0
              ]
            },
            {
              "op": "*",
              "args": [
                0.25,
                {
                  "op": "+",
                  "args": [
                    {
                      "op": "index",
                      "args": [
                        "efvs_q1",
                        "l"
                      ]
                    },
                    {
                      "op": "+",
                      "args": [
                        {
                          "op": "index",
                          "args": [
                            "efvs_q2",
                            "l"
                          ]
                        },
                        {
                          "op": "+",
                          "args": [
                            {
                              "op": "index",
                              "args": [
                                "efvs_q3",
                                "l"
                              ]
                            },
                            {
                              "op": "index",
                              "args": [
                                "efvs_q4",
                                "l"
                              ]
                            }
                          ]
                        }
                      ]
                    }
                  ]
                }
              ]
            },
            0.0
          ]
        }
      }
    },
    {
      "lhs": "efvs_qp_mean_recip",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "l"
        ],
        "args": [
          "efvs_q1",
          "efvs_q2",
          "efvs_q3",
          "efvs_q4"
        ],
        "ranges": {
          "l": {
            "from": "lev"
          }
        },
        "expr": {
          "op": "*",
          "args": [
            0.25,
            {
              "op": "+",
              "args": [
                {
                  "op": "/",
                  "args": [
                    1.0,
                    {
                      "op": "index",
                      "args": [
                        "efvs_q1",
                        "l"
                      ]
                    }
                  ]
                },
                {
                  "op": "+",
                  "args": [
                    {
                      "op": "/",
                      "args": [
                        1.0,
                        {
                          "op": "index",
                          "args": [
                            "efvs_q2",
                            "l"
                          ]
                        }
                      ]
                    },
                    {
                      "op": "+",
                      "args": [
                        {
                          "op": "/",
                          "args": [
                            1.0,
                            {
                              "op": "index",
                              "args": [
                                "efvs_q3",
                                "l"
                              ]
                            }
                          ]
                        },
                        {
                          "op": "/",
                          "args": [
                            1.0,
                            {
                              "op": "index",
                              "args": [
                                "efvs_q4",
                                "l"
                              ]
                            }
                          ]
                        }
                      ]
                    }
                  ]
                }
              ]
            }
          ]
        }
      }
    },
    {
      "lhs": "omega_integrand",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "l"
        ],
        "args": [
          "sig_mid",
          "efvs_qp_mean_recip",
          "thck"
        ],
        "ranges": {
          "l": {
            "from": "lev"
          }
        },
        "expr": {
          "op": "*",
          "args": [
            {
              "op": "index",
              "args": [
                "sig_mid",
                "l"
              ]
            },
            {
              "op": "*",
              "args": [
                "thck",
                {
                  "op": "index",
                  "args": [
                    "efvs_qp_mean_recip",
                    "l"
                  ]
                }
              ]
            }
          ]
        }
      }
    },
    {
      "lhs": "omega_k",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "==",
            "args": [
              "ice_mask",
              1.0
            ]
          },
          {
            "op": "integral",
            "args": [
              "omega_integrand"
            ],
            "var": "lev",
            "lower": "lev_nodes",
            "upper": "z_top"
          },
          0.0
        ]
      }
    },
    {
      "lhs": "omega_layer_avg",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "l"
        ],
        "args": [
          "omega_k"
        ],
        "ranges": {
          "l": {
            "from": "lev"
          }
        },
        "expr": {
          "op": "*",
          "args": [
            0.5,
            {
              "op": "+",
              "args": [
                {
                  "op": "index",
                  "args": [
                    "omega_k",
                    "l"
                  ]
                },
                {
                  "op": "index",
                  "args": [
                    "omega_k",
                    {
                      "op": "+",
                      "args": [
                        "l",
                        1
                      ]
                    }
                  ]
                }
              ]
            }
          ]
        }
      }
    },
    {
      "lhs": "omega",
      "rhs": {
        "op": "integral",
        "args": [
          "omega_layer_avg"
        ],
        "var": "lev",
        "lower": "z_sfc",
        "upper": "z_top"
      }
    },
    {
      "lhs": "stag_omega",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "cism_stagger_masked_mean",
        "bindings": {
          "var_sw": "omega",
          "var_se": "omega_se",
          "var_nw": "omega_nw",
          "var_ne": "omega_ne",
          "mask_sw": "ipl_mask_sw",
          "mask_se": "ipl_mask_se",
          "mask_nw": "ipl_mask_nw",
          "mask_ne": "ipl_mask_ne"
        }
      }
    },
    {
      "lhs": "stag_omega_k",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "k"
        ],
        "args": [
          "omega_k",
          "omega_k_se",
          "omega_k_nw",
          "omega_k_ne",
          "ipl_mask_sw",
          "ipl_mask_se",
          "ipl_mask_nw",
          "ipl_mask_ne"
        ],
        "ranges": {
          "k": {
            "from": "lev_nodes"
          }
        },
        "expr": {
          "op": "apply_expression_template",
          "args": [],
          "name": "cism_stagger_masked_mean",
          "bindings": {
            "var_sw": {
              "op": "index",
              "args": [
                "omega_k",
                "k"
              ]
            },
            "var_se": {
              "op": "index",
              "args": [
                "omega_k_se",
                "k"
              ]
            },
            "var_nw": {
              "op": "index",
              "args": [
                "omega_k_nw",
                "k"
              ]
            },
            "var_ne": {
              "op": "index",
              "args": [
                "omega_k_ne",
                "k"
              ]
            },
            "mask_sw": "ipl_mask_sw",
            "mask_se": "ipl_mask_se",
            "mask_nw": "ipl_mask_nw",
            "mask_ne": "ipl_mask_ne"
          }
        }
      }
    }
  ],
  "tests": [
    {
      "id": "int_step1_cell2511",
      "description": "Dump pin, cism_velo_nbr.csv / cism_velo_stag.csv step 1, cell (25,11): the thin-ice column (thck = 1.37 m) on the steepest slope; the efvs_q quad-point viscosities (1.1e9, 8.2e8, 5.4e8, 6.0e8 Pa yr at the surface layer) give the arithmetic-mean cell viscosity efvs and the omega_k single integral from the surface (2.63e-6 m/(Pa yr)) to the bed (0 at level 11 - the suffix-scan top), the omega double integral (2.62e-6), and the vertex staggers: stag_omega and stag_omega_k are the ice-masked 4-cell means over the stencil cells (cism_stagger_masked_mean, glissade_grid_operators.F90:135-148) with the model's own omega/omega_k as the SW cell and the cism_velo_stag.csv per-level omega_k_se/nw/ne and ice_plus_land_mask_sw/se/nw/ne as the other inputs (all four masks are 1 on every traced row, so the masked mean equals the plain 4-cell mean). The omega_k law is pinned at levels 1, 6, 11 and the staggers at the same levels; the integral lowering is the exact suffix scan / trapezoid stencil of the Fortran (worst verified 3.9e-16).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "sigma": [
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
        "efvs_q1": [
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
        "efvs_q2": [
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
        "efvs_q3": [
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
        "efvs_q4": [
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
        "thck": 1.3697560650243181,
        "ice_mask": 1.0,
        "omega_se": 5.8532707895434575e-09,
        "omega_nw": 7.336229984236539e-09,
        "omega_ne": 1.6398141089809047e-07,
        "ipl_mask_sw": 1.0,
        "ipl_mask_se": 1.0,
        "ipl_mask_nw": 1.0,
        "ipl_mask_ne": 1.0,
        "omega_k_se": [
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
        "omega_k_nw": [
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
        "omega_k_ne": [
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
          "variable": "efvs",
          "time": 0.0,
          "expected": 766507173.4123569,
          "coords": {
            "lev": 1
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "efvs",
          "time": 0.0,
          "expected": 738336138.5836939,
          "coords": {
            "lev": 6
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "omega_k",
          "time": 0.0,
          "expected": 1.030044712009776e-09,
          "coords": {
            "lev_nodes": 1
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "omega_k",
          "time": 0.0,
          "expected": 4.841814271806598e-10,
          "coords": {
            "lev_nodes": 6
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "omega",
          "time": 0.0,
          "expected": 6.928852082599512e-10,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "stag_omega",
          "time": 0.0,
          "expected": 4.446594922003261e-08,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "stag_omega_k",
          "time": 0.0,
          "expected": 5.8270828530954825e-08,
          "coords": {
            "lev_nodes": 1
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "stag_omega_k",
          "time": 0.0,
          "expected": 3.7358798456499055e-08,
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
      "id": "int_step1_cell2612",
      "description": "Dump pin, step 1, cell (26,12): a mid-thickness column (83.6 m) with a small slope; the layer-to-layer efvs variation (q1 falls from 1.07e9 to 1.05e9 Pa yr) exercises the nonuniform-layer integral over the CISM sigma spacing (dsigma from 0.231 to 0.036).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "sigma": [
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
        "efvs_q1": [
          603453023.9652967,
          577710561.7790526,
          523526069.8630726,
          466997604.14131796,
          416284860.1873542,
          373820332.0396423,
          339471921.67971426,
          312043461.5011166,
          290129618.1981252,
          272479037.89138865
        ],
        "efvs_q2": [
          624080168.6541365,
          598197092.8523568,
          543153016.9782492,
          485609122.43128073,
          433837779.63095164,
          390330096.65138865,
          355006451.0494356,
          326703842.11796296,
          304027413.6843384,
          285720643.3871719
        ],
        "efvs_q3": [
          620347297.4459308,
          415033741.46122414,
          235336454.48025545,
          153498765.53286517,
          114094768.33803779,
          92085211.62390961,
          78370685.8751709,
          69139225.64572169,
          62563892.3468418,
          57672884.74782247
        ],
        "efvs_q4": [
          627172002.0190711,
          486922925.29940367,
          320902547.4379656,
          219871260.18163225,
          165702321.55133536,
          134389306.1186992,
          114616703.20251141,
          101224784.36219819,
          91654380.58254947,
          84521494.66318987
        ],
        "thck": 83.55963112291998,
        "ice_mask": 1.0,
        "omega_se": 1.2634299867709617e-06,
        "omega_nw": 1.8453356764998729e-06,
        "omega_ne": 1.0513968683576465e-05,
        "ipl_mask_sw": 1.0,
        "ipl_mask_se": 1.0,
        "ipl_mask_nw": 1.0,
        "ipl_mask_ne": 1.0,
        "omega_k_se": [
          1.6154887159329762e-06,
          1.598167207891832e-06,
          1.5426304540255906e-06,
          1.435031932851793e-06,
          1.2789947693593789e-06,
          1.0875837672120607e-06,
          8.748560221237803e-07,
          6.52471420100758e-07,
          4.290084219921495e-07,
          2.102977208639311e-07,
          0.0
        ],
        "omega_k_nw": [
          2.3320534310802613e-06,
          2.3131732077817835e-06,
          2.246790661532822e-06,
          2.104871108745498e-06,
          1.8871484553333276e-06,
          1.612105807326085e-06,
          1.3013287866326059e-06,
          9.731445138510666e-07,
          6.41190001862771e-07,
          3.148188401362374e-07,
          0.0
        ],
        "omega_k_ne": [
          1.333855241426739e-05,
          1.3216903363719827e-05,
          1.2808478140481816e-05,
          1.1973013622110484e-05,
          1.0717267669995898e-05,
          9.145208889711902e-06,
          7.3766119579917865e-06,
          5.513248379163223e-06,
          3.6310350560054335e-06,
          1.7822082935198065e-06,
          0.0
        ]
      },
      "assertions": [
        {
          "variable": "efvs",
          "time": 0.0,
          "expected": 618763123.0211089,
          "coords": {
            "lev": 1
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "efvs",
          "time": 0.0,
          "expected": 247656236.60840994,
          "coords": {
            "lev": 6
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "omega_k",
          "time": 0.0,
          "expected": 2.1291725624533777e-07,
          "coords": {
            "lev_nodes": 1
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "omega_k",
          "time": 0.0,
          "expected": 1.392788467430872e-07,
          "coords": {
            "lev_nodes": 6
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "omega",
          "time": 0.0,
          "expected": 1.6398141089809047e-07,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "stag_omega",
          "time": 0.0,
          "expected": 3.4466789394363477e-06,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "stag_omega_k",
          "time": 0.0,
          "expected": 4.374752954381491e-06,
          "coords": {
            "lev_nodes": 1
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "stag_omega_k",
          "time": 0.0,
          "expected": 2.996044327748284e-06,
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
      "id": "int_step1_cell2713",
      "description": "Dump pin, step 1, cell (27,13): the thickest pinned column (434.5 m); its omega (5.9e-5 m/(Pa yr)) is the largest of the pinned rows and the trapezoid double integral runs over the full sigma column with the strongest layer weighting.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "sigma": [
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
        "efvs_q1": [
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
        "efvs_q2": [
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
        "efvs_q3": [
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
        "efvs_q4": [
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
        "thck": 434.50421401903714,
        "ice_mask": 1.0,
        "omega_se": 5.508893261498528e-06,
        "omega_nw": 2.4254396193143267e-05,
        "omega_ne": 2.0727382899639804e-05,
        "ipl_mask_sw": 1.0,
        "ipl_mask_se": 1.0,
        "ipl_mask_nw": 1.0,
        "ipl_mask_ne": 1.0,
        "omega_k_se": [
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
        "omega_k_nw": [
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
        "omega_k_ne": [
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
          "variable": "efvs",
          "time": 0.0,
          "expected": 101799766.89984475,
          "coords": {
            "lev": 1
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "efvs",
          "time": 0.0,
          "expected": 25488732.984231226,
          "coords": {
            "lev": 6
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "omega_k",
          "time": 0.0,
          "expected": 1.333855241426739e-05,
          "coords": {
            "lev_nodes": 1
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "omega_k",
          "time": 0.0,
          "expected": 9.145208889711902e-06,
          "coords": {
            "lev_nodes": 6
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "omega",
          "time": 0.0,
          "expected": 1.0513968683576465e-05,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "stag_omega",
          "time": 0.0,
          "expected": 1.5251160259464516e-05,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "stag_omega_k",
          "time": 0.0,
          "expected": 1.935659415081507e-05,
          "coords": {
            "lev_nodes": 1
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "stag_omega_k",
          "time": 0.0,
          "expected": 1.326622942177941e-05,
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
      "id": "int_step3_cell2414",
      "description": "Dump pin, step 3, cell (24,14): the fastest traced column (uvel_2d = 5.02 m/yr, thck = 118.7 m); the efvs values are an order of magnitude below the slow columns (2.1e8 Pa yr at the surface layer), the regime where the DIVA depth-integrated approximation matters most.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "sigma": [
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
        "efvs_q1": [
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
        "efvs_q2": [
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
        "efvs_q3": [
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
        "efvs_q4": [
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
        "thck": 118.65431569517798,
        "ice_mask": 1.0,
        "omega_se": 1.0113188674798673e-05,
        "omega_nw": 0.0001684390033841888,
        "omega_ne": 0.00014847784194165091,
        "ipl_mask_sw": 1.0,
        "ipl_mask_se": 1.0,
        "ipl_mask_nw": 1.0,
        "ipl_mask_ne": 1.0,
        "omega_k_se": [
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
        "omega_k_nw": [
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
        "omega_k_ne": [
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
          "variable": "efvs",
          "time": 0.0,
          "expected": 25484416.91832387,
          "coords": {
            "lev": 1
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "efvs",
          "time": 0.0,
          "expected": 10604910.06183968,
          "coords": {
            "lev": 6
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "omega_k",
          "time": 0.0,
          "expected": 8.234385852859944e-06,
          "coords": {
            "lev_nodes": 1
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "omega_k",
          "time": 0.0,
          "expected": 5.452576499909037e-06,
          "coords": {
            "lev_nodes": 6
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "omega",
          "time": 0.0,
          "expected": 6.378907868769574e-06,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "stag_omega",
          "time": 0.0,
          "expected": 8.335223546735198e-05,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "stag_omega_k",
          "time": 0.0,
          "expected": 0.00010524493778508243,
          "coords": {
            "lev_nodes": 1
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "stag_omega_k",
          "time": 0.0,
          "expected": 7.286943692579915e-05,
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
      "id": "int_step3_cell1714_inactive",
      "description": "Inactive-cell guard, step 3, cell (17,14): the traced cell lost its ice between steps 2 and 3 (thck 97.3 -> 0.986 m < thklim, ice_mask = 0), so the dumped efvs_q inputs are the STALE previous-step values (5.38e8 Pa yr at every quad point) while the dumped efvs, omega_k and omega are 0 - the active_cell guard of the element loop (F90:5091) skipped the whole DIVA block, and the model reproduces the zeroing with the ice_mask guard on the efvs mean and the omega_k integral (the integral branch is not evaluated, so the reciprocal of the stale viscosities never materializes). The stagger still runs: stag_omega = 0.25*(0 + omega_se + omega_nw + omega_ne) = 1.32e-6 m/(Pa yr) from the three ice-covered stencil neighbors.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "sigma": [
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
        "efvs_q1": [
          538425319.6082127,
          481496266.18696284,
          427910911.5146932,
          391133127.2028214,
          363460925.42411184,
          341836147.94317526,
          324750661.65663254,
          311125260.7124422,
          300136394.9079443,
          291165542.1718296
        ],
        "efvs_q2": [
          538425319.6082127,
          481496266.18696284,
          427910911.5146932,
          391133127.2028214,
          363460925.42411184,
          341836147.94317526,
          324750661.65663254,
          311125260.7124422,
          300136394.9079443,
          291165542.1718296
        ],
        "efvs_q3": [
          538425319.6082127,
          481496266.18696284,
          427910911.5146932,
          391133127.2028214,
          363460925.42411184,
          341836147.94317526,
          324750661.65663254,
          311125260.7124422,
          300136394.9079443,
          291165542.1718296
        ],
        "efvs_q4": [
          538425319.6082127,
          481496266.18696284,
          427910911.5146932,
          391133127.2028214,
          363460925.42411184,
          341836147.94317526,
          324750661.65663254,
          311125260.7124422,
          300136394.9079443,
          291165542.1718296
        ],
        "thck": 0.98647418260486,
        "ice_mask": 0.0,
        "omega_se": 4.369886445331456e-07,
        "omega_nw": 2.8216470233675297e-07,
        "omega_ne": 4.5703364189461865e-06,
        "ipl_mask_sw": 1.0,
        "ipl_mask_se": 1.0,
        "ipl_mask_nw": 1.0,
        "ipl_mask_ne": 1.0,
        "omega_k_se": [
          5.55221472761491e-07,
          5.494624413286405e-07,
          5.320235022596065e-07,
          4.972860756973449e-07,
          4.451991872459179e-07,
          3.799740416186938e-07,
          3.065586777961339e-07,
          2.2917504352900951e-07,
          1.5097334732325885e-07,
          7.411852339887674e-08,
          0.0
        ],
        "omega_k_nw": [
          3.631761571733741e-07,
          3.5829841799331506e-07,
          3.4433474553778786e-07,
          3.1933089436053386e-07,
          2.841824568878698e-07,
          2.4154988884874126e-07,
          1.9433388555640147e-07,
          1.4499736474258887e-07,
          9.538766092060881e-08,
          4.678140189499338e-08,
          0.0
        ],
        "omega_k_ne": [
          5.762675892954696e-06,
          5.720313349671324e-06,
          5.565255145796753e-06,
          5.2193123181549835e-06,
          4.681892378414793e-06,
          4.0006450420975096e-06,
          3.229959675239435e-06,
          2.4156881051183e-06,
          1.5918629175919647e-06,
          7.817610379223547e-07,
          0.0
        ]
      },
      "assertions": [
        {
          "variable": "efvs",
          "time": 0.0,
          "expected": 0.0,
          "coords": {
            "lev": 1
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "omega_k",
          "time": 0.0,
          "expected": 0.0,
          "coords": {
            "lev_nodes": 1
          },
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "omega",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "stag_omega",
          "time": 0.0,
          "expected": 1.3223724414540212e-06,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "stag_omega_k",
          "time": 0.0,
          "expected": 1.6702683807223903e-06,
          "coords": {
            "lev_nodes": 1
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
