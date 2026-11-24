---
title: "DivaGeometry"
slug: "divageometry"
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
| `usrf_sw` | `m` | `0.0` | surface elevation of the SW stencil cell (the traced cell; cism_velo_nbr.csv usrf_sw), m |
| `usrf_se` | `m` | `0.0` | surface elevation of the SE stencil cell (cism_velo_nbr.csv usrf_se), m |
| `usrf_nw` | `m` | `0.0` | surface elevation of the NW stencil cell (cism_velo_nbr.csv usrf_nw), m |
| `usrf_ne` | `m` | `0.0` | surface elevation of the NE stencil cell (cism_velo_nbr.csv usrf_ne), m |
| `thck_sw` | `m` | `0.0` | ice thickness of the SW stencil cell (cism_velo_nbr.csv thck_sw), m |
| `thck_se` | `m` | `0.0` | ice thickness of the SE stencil cell (cism_velo_nbr.csv thck_se), m |
| `thck_nw` | `m` | `0.0` | ice thickness of the NW stencil cell (cism_velo_nbr.csv thck_nw), m |
| `thck_ne` | `m` | `0.0` | ice thickness of the NE stencil cell (cism_velo_nbr.csv thck_ne), m |
| `ice_mask_sw` | `1` | `0.0` | ice mask of the SW stencil cell (cism_velo_nbr.csv ice_mask_sw): 1 where thck > thklim |
| `ice_mask_se` | `1` | `0.0` | ice mask of the SE stencil cell (cism_velo_nbr.csv ice_mask_se) |
| `ice_mask_nw` | `1` | `0.0` | ice mask of the NW stencil cell (cism_velo_nbr.csv ice_mask_nw) |
| `ice_mask_ne` | `1` | `0.0` | ice mask of the NE stencil cell (cism_velo_nbr.csv ice_mask_ne) |
| `land_mask_sw` | `1` | `1.0` | land mask of the SW stencil cell (cism_velo_nbr.csv land_mask_sw): 1 on land, 0 on ocean |
| `land_mask_se` | `1` | `1.0` | land mask of the SE stencil cell (cism_velo_nbr.csv land_mask_se) |
| `land_mask_nw` | `1` | `1.0` | land mask of the NW stencil cell (cism_velo_nbr.csv land_mask_nw) |
| `land_mask_ne` | `1` | `1.0` | land mask of the NE stencil cell (cism_velo_nbr.csv land_mask_ne) |
| `thklim` | `m` | `1.0` | ice thickness limit ice_limit (glide_types.F90 default 1.0 m): cells with thck <= thklim are ice-free; the hybrid-margin ramp starts at this thickness |
| `ramp` | `m` | `50.0` | thck_gradient_ramp (glide_types.F90:2395 default 50.0 m): the distance over which the hybrid-margin edge factor ramps from 0 to 1 |
| `max_slope` | `1` | `0.5` | max_slope (glide_types.F90 default 0.5): the clamp of the driving-stress surface gradient (grid_operators.F90:1234-1252) |
| `dx` | `m` | `20000.0` | grid spacing (gris20 dx = dy = 20 km; the reference run is square, dx = dy) |
| `rhoi` | `kg/m^3` | `917.0` | ice density (glide_types default 917.0 kg/m3) |
| `g` | `m/s^2` | `9.80616` | gravitational acceleration (glide_types default 9.80616 m/s2) |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `z_mean_sw` | `m` |  | z_mean = usrf - thck/2 = 0.5*(usrf + lsrf) of the SW stencil cell, the mid-ice elevation whose gradient feeds the DIVA slope angle (glissade_velo_higher.F90:2160; lsrf = topg - eus and usrf = lsrf + thck, so z_mean = usrf - thck/2) |
| `z_mean_se` | `m` |  | z_mean of the SE stencil cell |
| `z_mean_nw` | `m` |  | z_mean of the NW stencil cell |
| `z_mean_ne` | `m` |  | z_mean of the NE stencil cell |
| `edge_s` | `1` |  | hybrid-margin surface gradient d(usrf)/dx on the SOUTH edge of the vertex (between the SW and SE cells; cism_hybrid_edge_gradient, grid_operators.F90:999-1079) |
| `edge_n` | `1` |  | hybrid-margin surface gradient d(usrf)/dx on the NORTH edge of the vertex (between the NW and NE cells) |
| `edge_w` | `1` |  | hybrid-margin surface gradient d(usrf)/dy on the WEST edge of the vertex (between the SW and NW cells) |
| `edge_e` | `1` |  | hybrid-margin surface gradient d(usrf)/dy on the EAST edge of the vertex (between the SE and NE cells) |
| `dusrf_dx` | `1` |  | surface elevation gradient at the vertex used for the driving stress: the centered average of the south/north hybrid edge gradients, clamped to +/-max_slope (the dumped dusrf_dx column) |
| `dusrf_dy` | `1` |  | surface elevation gradient at the vertex in y: the centered average of the west/east hybrid edge gradients, clamped to +/-max_slope (the dumped dusrf_dy column) |
| `dz_dx` | `1` |  | x-gradient of z_mean at the vertex from the PLAIN centered vertex gradient (no hybrid masking, no clamp: the glissade_gradient construction used by the slope angle, F90:1510, with slope_mask = 1 everywhere) |
| `dz_dy` | `1` |  | y-gradient of z_mean at the vertex (plain centered vertex gradient) |
| `theta_x` | `rad` |  | x-direction surface slope angle of the DIVA slope correction: theta_x = atan(\|dz_dx\|) (cism_theta_slope_x, grid_operators.F90:1510; the dumped stag_theta_slope_x column) |
| `theta_y` | `rad` |  | y-direction surface slope angle of the DIVA slope correction: theta_y = atan(\|dz_dy\|) (the dumped stag_theta_slope_y column) |
| `F_x` | `1` |  | DIVA slope correction factor in x: F_x = cos^2(theta_x) + 4 sin^2(theta_x) (cism_diva_slope_factor, F90:2189-2193; the dumped stag_diva_slope_factor_x column) |
| `F_y` | `1` |  | DIVA slope correction factor in y: F_y = cos^2(theta_y) + 4 sin^2(theta_y) (the dumped stag_diva_slope_factor_y column) |
| `stagthck` | `m` |  | staggered ice thickness at the vertex: the plain 4-cell mean of thck, the stagger_margin = 0 case of glissade_stagger (grid_operators.F90:125-133) applied here as cism_stagger_masked_mean with unit masks (the four-cell stencil of F90:141-143 with mask = 1, so the masked mean collapses to the plain mean; the dumped stagthck column) |
| `taudx` | `Pa` |  | x driving stress at the vertex: taudx = -rhoi*grav*stagthck*dusrf_dx (cism_driving_stress, load_vector_gravity, HO_ASSEMBLE_TAUD_LOCAL, F90:4353-4384; the dumped taudx column) |
| `taudy` | `Pa` |  | y driving stress at the vertex: taudy = -rhoi*grav*stagthck*dusrf_dy (the dumped taudy column) |

## Observed expressions

$$
z_{mean\,sw} = usrf_{sw} - 0.5 \cdot thck_{sw}
$$
_z_mean = usrf - thck/2 = 0.5*(usrf + lsrf) of the SW stencil cell, the mid-ice elevation whose gradient feeds the DIVA slope angle (glissade_velo_higher.F90:2160; lsrf = topg - eus and usrf = lsrf + thck, so z_mean = usrf - thck/2)_

$$
z_{mean\,se} = usrf_{se} - 0.5 \cdot thck_{se}
$$
_z_mean of the SE stencil cell_

$$
z_{mean\,nw} = usrf_{nw} - 0.5 \cdot thck_{nw}
$$
_z_mean of the NW stencil cell_

$$
z_{mean\,ne} = usrf_{ne} - 0.5 \cdot thck_{ne}
$$
_z_mean of the NE stencil cell_

$$
edge_{s} = \mathrm{cism_hybrid_edge_gradient}\left(usrf_{w}=usrf_{sw}, usrf_{e}=usrf_{se}, thck_{w}=thck_{sw}, thck_{e}=thck_{se}, ice_{w}=ice_{mask\,sw}, ice_{e}=ice_{mask\,se}, land_{w}=land_{mask\,sw}, land_{e}=land_{mask\,se}, thklim=thklim, ramp=ramp, dx=dx\right)
$$
_hybrid-margin surface gradient d(usrf)/dx on the SOUTH edge of the vertex (between the SW and SE cells; cism_hybrid_edge_gradient, grid_operators.F90:999-1079)_

$$
edge_{n} = \mathrm{cism_hybrid_edge_gradient}\left(usrf_{w}=usrf_{nw}, usrf_{e}=usrf_{ne}, thck_{w}=thck_{nw}, thck_{e}=thck_{ne}, ice_{w}=ice_{mask\,nw}, ice_{e}=ice_{mask\,ne}, land_{w}=land_{mask\,nw}, land_{e}=land_{mask\,ne}, thklim=thklim, ramp=ramp, dx=dx\right)
$$
_hybrid-margin surface gradient d(usrf)/dx on the NORTH edge of the vertex (between the NW and NE cells)_

$$
edge_{w} = \mathrm{cism_hybrid_edge_gradient}\left(usrf_{w}=usrf_{sw}, usrf_{e}=usrf_{nw}, thck_{w}=thck_{sw}, thck_{e}=thck_{nw}, ice_{w}=ice_{mask\,sw}, ice_{e}=ice_{mask\,nw}, land_{w}=land_{mask\,sw}, land_{e}=land_{mask\,nw}, thklim=thklim, ramp=ramp, dx=dx\right)
$$
_hybrid-margin surface gradient d(usrf)/dy on the WEST edge of the vertex (between the SW and NW cells)_

$$
edge_{e} = \mathrm{cism_hybrid_edge_gradient}\left(usrf_{w}=usrf_{se}, usrf_{e}=usrf_{ne}, thck_{w}=thck_{se}, thck_{e}=thck_{ne}, ice_{w}=ice_{mask\,se}, ice_{e}=ice_{mask\,ne}, land_{w}=land_{mask\,se}, land_{e}=land_{mask\,ne}, thklim=thklim, ramp=ramp, dx=dx\right)
$$
_hybrid-margin surface gradient d(usrf)/dy on the EAST edge of the vertex (between the SE and NE cells)_

$$
dusrf_{dx} = \mathrm{min}\left(\mathrm{max}\left(0.5 \cdot \left(edge_{s} + edge_{n}\right), -max_{slope}\right), max_{slope}\right)
$$
_surface elevation gradient at the vertex used for the driving stress: the centered average of the south/north hybrid edge gradients, clamped to +/-max_slope (the dumped dusrf_dx column)_

$$
dusrf_{dy} = \mathrm{min}\left(\mathrm{max}\left(0.5 \cdot \left(edge_{w} + edge_{e}\right), -max_{slope}\right), max_{slope}\right)
$$
_surface elevation gradient at the vertex in y: the centered average of the west/east hybrid edge gradients, clamped to +/-max_slope (the dumped dusrf_dy column)_

$$
dz_{dx} = 0.5 \cdot \left(\frac{z_{mean\,ne} - z_{mean\,nw}}{dx} + \frac{z_{mean\,se} - z_{mean\,sw}}{dx}\right)
$$
_x-gradient of z_mean at the vertex from the PLAIN centered vertex gradient (no hybrid masking, no clamp: the glissade_gradient construction used by the slope angle, F90:1510, with slope_mask = 1 everywhere)_

$$
dz_{dy} = 0.5 \cdot \left(\frac{z_{mean\,ne} - z_{mean\,se}}{dx} + \frac{z_{mean\,nw} - z_{mean\,sw}}{dx}\right)
$$
_y-gradient of z_mean at the vertex (plain centered vertex gradient)_

$$
theta_{x} = \mathrm{cism_theta_slope_x}\left(dz_{dx}=dz_{dx}\right)
$$
_x-direction surface slope angle of the DIVA slope correction: theta_x = atan(|dz_dx|) (cism_theta_slope_x, grid_operators.F90:1510; the dumped stag_theta_slope_x column)_

$$
theta_{y} = \mathrm{cism_theta_slope_x}\left(dz_{dx}=dz_{dy}\right)
$$
_y-direction surface slope angle of the DIVA slope correction: theta_y = atan(|dz_dy|) (the dumped stag_theta_slope_y column)_

$$
F_{x} = \mathrm{cism_diva_slope_factor}\left(theta=theta_{x}\right)
$$
_DIVA slope correction factor in x: F_x = cos^2(theta_x) + 4 sin^2(theta_x) (cism_diva_slope_factor, F90:2189-2193; the dumped stag_diva_slope_factor_x column)_

$$
F_{y} = \mathrm{cism_diva_slope_factor}\left(theta=theta_{y}\right)
$$
_DIVA slope correction factor in y: F_y = cos^2(theta_y) + 4 sin^2(theta_y) (the dumped stag_diva_slope_factor_y column)_

$$
stagthck = \mathrm{cism_stagger_masked_mean}\left(var_{sw}=thck_{sw}, var_{se}=thck_{se}, var_{nw}=thck_{nw}, var_{ne}=thck_{ne}, mask_{sw}=\mathrm{const}\left(\right), mask_{se}=\mathrm{const}\left(\right), mask_{nw}=\mathrm{const}\left(\right), mask_{ne}=\mathrm{const}\left(\right)\right)
$$
_staggered ice thickness at the vertex: the plain 4-cell mean of thck, the stagger_margin = 0 case of glissade_stagger (grid_operators.F90:125-133) applied here as cism_stagger_masked_mean with unit masks (the four-cell stencil of F90:141-143 with mask = 1, so the masked mean collapses to the plain mean; the dumped stagthck column)_

$$
taudx = \mathrm{cism_driving_stress}\left(rhoi=rhoi, g=g, stagthck=stagthck, dusrf_{dx}=dusrf_{dx}\right)
$$
_x driving stress at the vertex: taudx = -rhoi*grav*stagthck*dusrf_dx (cism_driving_stress, load_vector_gravity, HO_ASSEMBLE_TAUD_LOCAL, F90:4353-4384; the dumped taudx column)_

$$
taudy = \mathrm{cism_driving_stress}\left(rhoi=rhoi, g=g, stagthck=stagthck, dusrf_{dx}=dusrf_{dy}\right)
$$
_y driving stress at the vertex: taudy = -rhoi*grav*stagthck*dusrf_dy (the dumped taudy column)_

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
    "usrf_sw": {
      "type": "parameter",
      "units": "m",
      "default": 0.0,
      "description": "surface elevation of the SW stencil cell (the traced cell; cism_velo_nbr.csv usrf_sw), m"
    },
    "usrf_se": {
      "type": "parameter",
      "units": "m",
      "default": 0.0,
      "description": "surface elevation of the SE stencil cell (cism_velo_nbr.csv usrf_se), m"
    },
    "usrf_nw": {
      "type": "parameter",
      "units": "m",
      "default": 0.0,
      "description": "surface elevation of the NW stencil cell (cism_velo_nbr.csv usrf_nw), m"
    },
    "usrf_ne": {
      "type": "parameter",
      "units": "m",
      "default": 0.0,
      "description": "surface elevation of the NE stencil cell (cism_velo_nbr.csv usrf_ne), m"
    },
    "thck_sw": {
      "type": "parameter",
      "units": "m",
      "default": 0.0,
      "description": "ice thickness of the SW stencil cell (cism_velo_nbr.csv thck_sw), m"
    },
    "thck_se": {
      "type": "parameter",
      "units": "m",
      "default": 0.0,
      "description": "ice thickness of the SE stencil cell (cism_velo_nbr.csv thck_se), m"
    },
    "thck_nw": {
      "type": "parameter",
      "units": "m",
      "default": 0.0,
      "description": "ice thickness of the NW stencil cell (cism_velo_nbr.csv thck_nw), m"
    },
    "thck_ne": {
      "type": "parameter",
      "units": "m",
      "default": 0.0,
      "description": "ice thickness of the NE stencil cell (cism_velo_nbr.csv thck_ne), m"
    },
    "ice_mask_sw": {
      "type": "parameter",
      "units": "1",
      "default": 0.0,
      "description": "ice mask of the SW stencil cell (cism_velo_nbr.csv ice_mask_sw): 1 where thck > thklim"
    },
    "ice_mask_se": {
      "type": "parameter",
      "units": "1",
      "default": 0.0,
      "description": "ice mask of the SE stencil cell (cism_velo_nbr.csv ice_mask_se)"
    },
    "ice_mask_nw": {
      "type": "parameter",
      "units": "1",
      "default": 0.0,
      "description": "ice mask of the NW stencil cell (cism_velo_nbr.csv ice_mask_nw)"
    },
    "ice_mask_ne": {
      "type": "parameter",
      "units": "1",
      "default": 0.0,
      "description": "ice mask of the NE stencil cell (cism_velo_nbr.csv ice_mask_ne)"
    },
    "land_mask_sw": {
      "type": "parameter",
      "units": "1",
      "default": 1.0,
      "description": "land mask of the SW stencil cell (cism_velo_nbr.csv land_mask_sw): 1 on land, 0 on ocean"
    },
    "land_mask_se": {
      "type": "parameter",
      "units": "1",
      "default": 1.0,
      "description": "land mask of the SE stencil cell (cism_velo_nbr.csv land_mask_se)"
    },
    "land_mask_nw": {
      "type": "parameter",
      "units": "1",
      "default": 1.0,
      "description": "land mask of the NW stencil cell (cism_velo_nbr.csv land_mask_nw)"
    },
    "land_mask_ne": {
      "type": "parameter",
      "units": "1",
      "default": 1.0,
      "description": "land mask of the NE stencil cell (cism_velo_nbr.csv land_mask_ne)"
    },
    "thklim": {
      "type": "parameter",
      "units": "m",
      "default": 1.0,
      "description": "ice thickness limit ice_limit (glide_types.F90 default 1.0 m): cells with thck <= thklim are ice-free; the hybrid-margin ramp starts at this thickness"
    },
    "ramp": {
      "type": "parameter",
      "units": "m",
      "default": 50.0,
      "description": "thck_gradient_ramp (glide_types.F90:2395 default 50.0 m): the distance over which the hybrid-margin edge factor ramps from 0 to 1"
    },
    "max_slope": {
      "type": "parameter",
      "units": "1",
      "default": 0.5,
      "description": "max_slope (glide_types.F90 default 0.5): the clamp of the driving-stress surface gradient (grid_operators.F90:1234-1252)"
    },
    "dx": {
      "type": "parameter",
      "units": "m",
      "default": 20000.0,
      "description": "grid spacing (gris20 dx = dy = 20 km; the reference run is square, dx = dy)"
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
    "z_mean_sw": {
      "type": "unknown",
      "units": "m",
      "description": "z_mean = usrf - thck/2 = 0.5*(usrf + lsrf) of the SW stencil cell, the mid-ice elevation whose gradient feeds the DIVA slope angle (glissade_velo_higher.F90:2160; lsrf = topg - eus and usrf = lsrf + thck, so z_mean = usrf - thck/2)"
    },
    "z_mean_se": {
      "type": "unknown",
      "units": "m",
      "description": "z_mean of the SE stencil cell"
    },
    "z_mean_nw": {
      "type": "unknown",
      "units": "m",
      "description": "z_mean of the NW stencil cell"
    },
    "z_mean_ne": {
      "type": "unknown",
      "units": "m",
      "description": "z_mean of the NE stencil cell"
    },
    "edge_s": {
      "type": "unknown",
      "units": "1",
      "description": "hybrid-margin surface gradient d(usrf)/dx on the SOUTH edge of the vertex (between the SW and SE cells; cism_hybrid_edge_gradient, grid_operators.F90:999-1079)"
    },
    "edge_n": {
      "type": "unknown",
      "units": "1",
      "description": "hybrid-margin surface gradient d(usrf)/dx on the NORTH edge of the vertex (between the NW and NE cells)"
    },
    "edge_w": {
      "type": "unknown",
      "units": "1",
      "description": "hybrid-margin surface gradient d(usrf)/dy on the WEST edge of the vertex (between the SW and NW cells)"
    },
    "edge_e": {
      "type": "unknown",
      "units": "1",
      "description": "hybrid-margin surface gradient d(usrf)/dy on the EAST edge of the vertex (between the SE and NE cells)"
    },
    "dusrf_dx": {
      "type": "unknown",
      "units": "1",
      "description": "surface elevation gradient at the vertex used for the driving stress: the centered average of the south/north hybrid edge gradients, clamped to +/-max_slope (the dumped dusrf_dx column)"
    },
    "dusrf_dy": {
      "type": "unknown",
      "units": "1",
      "description": "surface elevation gradient at the vertex in y: the centered average of the west/east hybrid edge gradients, clamped to +/-max_slope (the dumped dusrf_dy column)"
    },
    "dz_dx": {
      "type": "unknown",
      "units": "1",
      "description": "x-gradient of z_mean at the vertex from the PLAIN centered vertex gradient (no hybrid masking, no clamp: the glissade_gradient construction used by the slope angle, F90:1510, with slope_mask = 1 everywhere)"
    },
    "dz_dy": {
      "type": "unknown",
      "units": "1",
      "description": "y-gradient of z_mean at the vertex (plain centered vertex gradient)"
    },
    "theta_x": {
      "type": "unknown",
      "units": "rad",
      "description": "x-direction surface slope angle of the DIVA slope correction: theta_x = atan(|dz_dx|) (cism_theta_slope_x, grid_operators.F90:1510; the dumped stag_theta_slope_x column)"
    },
    "theta_y": {
      "type": "unknown",
      "units": "rad",
      "description": "y-direction surface slope angle of the DIVA slope correction: theta_y = atan(|dz_dy|) (the dumped stag_theta_slope_y column)"
    },
    "F_x": {
      "type": "unknown",
      "units": "1",
      "description": "DIVA slope correction factor in x: F_x = cos^2(theta_x) + 4 sin^2(theta_x) (cism_diva_slope_factor, F90:2189-2193; the dumped stag_diva_slope_factor_x column)"
    },
    "F_y": {
      "type": "unknown",
      "units": "1",
      "description": "DIVA slope correction factor in y: F_y = cos^2(theta_y) + 4 sin^2(theta_y) (the dumped stag_diva_slope_factor_y column)"
    },
    "stagthck": {
      "type": "unknown",
      "units": "m",
      "description": "staggered ice thickness at the vertex: the plain 4-cell mean of thck, the stagger_margin = 0 case of glissade_stagger (grid_operators.F90:125-133) applied here as cism_stagger_masked_mean with unit masks (the four-cell stencil of F90:141-143 with mask = 1, so the masked mean collapses to the plain mean; the dumped stagthck column)"
    },
    "taudx": {
      "type": "unknown",
      "units": "Pa",
      "description": "x driving stress at the vertex: taudx = -rhoi*grav*stagthck*dusrf_dx (cism_driving_stress, load_vector_gravity, HO_ASSEMBLE_TAUD_LOCAL, F90:4353-4384; the dumped taudx column)"
    },
    "taudy": {
      "type": "unknown",
      "units": "Pa",
      "description": "y driving stress at the vertex: taudy = -rhoi*grav*stagthck*dusrf_dy (the dumped taudy column)"
    }
  },
  "equations": [
    {
      "lhs": "z_mean_sw",
      "rhs": {
        "op": "-",
        "args": [
          "usrf_sw",
          {
            "op": "*",
            "args": [
              0.5,
              "thck_sw"
            ]
          }
        ]
      }
    },
    {
      "lhs": "z_mean_se",
      "rhs": {
        "op": "-",
        "args": [
          "usrf_se",
          {
            "op": "*",
            "args": [
              0.5,
              "thck_se"
            ]
          }
        ]
      }
    },
    {
      "lhs": "z_mean_nw",
      "rhs": {
        "op": "-",
        "args": [
          "usrf_nw",
          {
            "op": "*",
            "args": [
              0.5,
              "thck_nw"
            ]
          }
        ]
      }
    },
    {
      "lhs": "z_mean_ne",
      "rhs": {
        "op": "-",
        "args": [
          "usrf_ne",
          {
            "op": "*",
            "args": [
              0.5,
              "thck_ne"
            ]
          }
        ]
      }
    },
    {
      "lhs": "edge_s",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "cism_hybrid_edge_gradient",
        "bindings": {
          "usrf_w": "usrf_sw",
          "usrf_e": "usrf_se",
          "thck_w": "thck_sw",
          "thck_e": "thck_se",
          "ice_w": "ice_mask_sw",
          "ice_e": "ice_mask_se",
          "land_w": "land_mask_sw",
          "land_e": "land_mask_se",
          "thklim": "thklim",
          "ramp": "ramp",
          "dx": "dx"
        }
      }
    },
    {
      "lhs": "edge_n",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "cism_hybrid_edge_gradient",
        "bindings": {
          "usrf_w": "usrf_nw",
          "usrf_e": "usrf_ne",
          "thck_w": "thck_nw",
          "thck_e": "thck_ne",
          "ice_w": "ice_mask_nw",
          "ice_e": "ice_mask_ne",
          "land_w": "land_mask_nw",
          "land_e": "land_mask_ne",
          "thklim": "thklim",
          "ramp": "ramp",
          "dx": "dx"
        }
      }
    },
    {
      "lhs": "edge_w",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "cism_hybrid_edge_gradient",
        "bindings": {
          "usrf_w": "usrf_sw",
          "usrf_e": "usrf_nw",
          "thck_w": "thck_sw",
          "thck_e": "thck_nw",
          "ice_w": "ice_mask_sw",
          "ice_e": "ice_mask_nw",
          "land_w": "land_mask_sw",
          "land_e": "land_mask_nw",
          "thklim": "thklim",
          "ramp": "ramp",
          "dx": "dx"
        }
      }
    },
    {
      "lhs": "edge_e",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "cism_hybrid_edge_gradient",
        "bindings": {
          "usrf_w": "usrf_se",
          "usrf_e": "usrf_ne",
          "thck_w": "thck_se",
          "thck_e": "thck_ne",
          "ice_w": "ice_mask_se",
          "ice_e": "ice_mask_ne",
          "land_w": "land_mask_se",
          "land_e": "land_mask_ne",
          "thklim": "thklim",
          "ramp": "ramp",
          "dx": "dx"
        }
      }
    },
    {
      "lhs": "dusrf_dx",
      "rhs": {
        "op": "min",
        "args": [
          {
            "op": "max",
            "args": [
              {
                "op": "*",
                "args": [
                  0.5,
                  {
                    "op": "+",
                    "args": [
                      "edge_s",
                      "edge_n"
                    ]
                  }
                ]
              },
              {
                "op": "-",
                "args": [
                  "max_slope"
                ]
              }
            ]
          },
          "max_slope"
        ]
      }
    },
    {
      "lhs": "dusrf_dy",
      "rhs": {
        "op": "min",
        "args": [
          {
            "op": "max",
            "args": [
              {
                "op": "*",
                "args": [
                  0.5,
                  {
                    "op": "+",
                    "args": [
                      "edge_w",
                      "edge_e"
                    ]
                  }
                ]
              },
              {
                "op": "-",
                "args": [
                  "max_slope"
                ]
              }
            ]
          },
          "max_slope"
        ]
      }
    },
    {
      "lhs": "dz_dx",
      "rhs": {
        "op": "*",
        "args": [
          0.5,
          {
            "op": "+",
            "args": [
              {
                "op": "/",
                "args": [
                  {
                    "op": "-",
                    "args": [
                      "z_mean_ne",
                      "z_mean_nw"
                    ]
                  },
                  "dx"
                ]
              },
              {
                "op": "/",
                "args": [
                  {
                    "op": "-",
                    "args": [
                      "z_mean_se",
                      "z_mean_sw"
                    ]
                  },
                  "dx"
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "dz_dy",
      "rhs": {
        "op": "*",
        "args": [
          0.5,
          {
            "op": "+",
            "args": [
              {
                "op": "/",
                "args": [
                  {
                    "op": "-",
                    "args": [
                      "z_mean_ne",
                      "z_mean_se"
                    ]
                  },
                  "dx"
                ]
              },
              {
                "op": "/",
                "args": [
                  {
                    "op": "-",
                    "args": [
                      "z_mean_nw",
                      "z_mean_sw"
                    ]
                  },
                  "dx"
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "theta_x",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "cism_theta_slope_x",
        "bindings": {
          "dz_dx": "dz_dx"
        }
      }
    },
    {
      "lhs": "theta_y",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "cism_theta_slope_x",
        "bindings": {
          "dz_dx": "dz_dy"
        }
      }
    },
    {
      "lhs": "F_x",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "cism_diva_slope_factor",
        "bindings": {
          "theta": "theta_x"
        }
      }
    },
    {
      "lhs": "F_y",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "cism_diva_slope_factor",
        "bindings": {
          "theta": "theta_y"
        }
      }
    },
    {
      "lhs": "stagthck",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "cism_stagger_masked_mean",
        "bindings": {
          "var_sw": "thck_sw",
          "var_se": "thck_se",
          "var_nw": "thck_nw",
          "var_ne": "thck_ne",
          "mask_sw": {
            "op": "const",
            "args": [],
            "value": 1.0,
            "units": "1"
          },
          "mask_se": {
            "op": "const",
            "args": [],
            "value": 1.0,
            "units": "1"
          },
          "mask_nw": {
            "op": "const",
            "args": [],
            "value": 1.0,
            "units": "1"
          },
          "mask_ne": {
            "op": "const",
            "args": [],
            "value": 1.0,
            "units": "1"
          }
        }
      }
    },
    {
      "lhs": "taudx",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "cism_driving_stress",
        "bindings": {
          "rhoi": "rhoi",
          "g": "g",
          "stagthck": "stagthck",
          "dusrf_dx": "dusrf_dx"
        }
      }
    },
    {
      "lhs": "taudy",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "cism_driving_stress",
        "bindings": {
          "rhoi": "rhoi",
          "g": "g",
          "stagthck": "stagthck",
          "dusrf_dx": "dusrf_dy"
        }
      }
    }
  ],
  "tests": [
    {
      "id": "geom_step1_cell2511",
      "description": "Dump pin, cism_velo_nbr.csv step 1, cell (25,11) (the NE-corner vertex stencil; SW = the traced cell): thin ice (thck_sw = 1.37 m) on the steepest slope of the traced window (theta_x = 0.0316 rad), all four stencil cells ice-covered land. The hybrid-margin edges are undamped (the upper cell of every edge has thck > thklim + ramp), so dusrf_dx = 0.5*(edge_s + edge_n) = 0.02045 (below the max_slope clamp) and the driving stress taudx = -rhoi*g*stagthck*dusrf_dx = -4890.4 Pa; the slope angle theta_x = atan(|dz_dx|) comes from the PLAIN z_mean gradient (dz_dx = 0.03163, no hybrid masking) and F_x = cos^2 + 4 sin^2 = 1.002997. All assertions at rel 1e-12 except the edge-gradient-derived dusrf_dx/dy/taudx/taudy at 1e-11 (the es26.17 dump round-trip of the ~1800 m surface-elevation differences; worst verified over the 128 exit rows 6.6e-13).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "usrf_sw": 1083.3697560650244,
        "thck_sw": 1.3697560650243181,
        "ice_mask_sw": 1.0,
        "land_mask_sw": 1.0,
        "usrf_se": 1767.9405124627754,
        "thck_se": 15.04048804871283,
        "ice_mask_se": 1.0,
        "land_mask_se": 1.0,
        "usrf_nw": 1243.7076327746151,
        "thck_nw": 6.407583946490077,
        "ice_mask_nw": 1.0,
        "land_mask_nw": 1.0,
        "usrf_ne": 1869.4596555369824,
        "thck_ne": 83.55963112291998,
        "ice_mask_ne": 1.0,
        "land_mask_ne": 1.0
      },
      "assertions": [
        {
          "variable": "dusrf_dx",
          "time": 0.0,
          "expected": 0.020449654330913065,
          "tolerance": {
            "rel": 1e-11
          }
        },
        {
          "variable": "dusrf_dy",
          "time": 0.0,
          "expected": 0.0029714988409105213,
          "tolerance": {
            "rel": 1e-11
          }
        },
        {
          "variable": "stagthck",
          "time": 0.0,
          "expected": 26.594364795786802,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "taudx",
          "time": 0.0,
          "expected": -4890.394605748079,
          "tolerance": {
            "rel": 1e-11
          }
        },
        {
          "variable": "taudy",
          "time": 0.0,
          "expected": -710.6135716244473,
          "tolerance": {
            "rel": 1e-11
          }
        },
        {
          "variable": "theta_x",
          "time": 0.0,
          "expected": 0.03161225012587919,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "theta_y",
          "time": 0.0,
          "expected": 0.005626903970461825,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "F_x",
          "time": 0.0,
          "expected": 1.002997004537962,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "F_y",
          "time": 0.0,
          "expected": 1.0000949851423973,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "geom_step1_cell2713",
      "description": "Dump pin, step 1, cell (27,13): thick ice (thck_sw = 434.5 m) with a negative surface gradient (dusrf_dx = -0.0177, taudx > 0); the y gradient is small and positive. stagthck = 431.9 m (the 4-cell mean), and the bwat = 0 effective-pressure identity effecpress_stag = rhoi*g*stagthck = 3.885e6 Pa is pinned here and on every other row by the same law (the staged N_stag of the basal chain).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "usrf_sw": 2126.804262847162,
        "thck_sw": 434.50421401903714,
        "ice_mask_sw": 1.0,
        "land_mask_sw": 1.0,
        "usrf_se": 1678.37154926737,
        "thck_se": 141.97152485330747,
        "ice_mask_se": 1.0,
        "land_mask_se": 1.0,
        "usrf_nw": 2225.051047853225,
        "thck_nw": 700.35109668135,
        "ice_mask_nw": 1.0,
        "land_mask_nw": 1.0,
        "usrf_ne": 1965.580504027392,
        "thck_ne": 305.2804551992669,
        "ice_mask_ne": 1.0,
        "land_mask_ne": 1.0
      },
      "assertions": [
        {
          "variable": "dusrf_dx",
          "time": 0.0,
          "expected": -0.017697581435140632,
          "tolerance": {
            "rel": 1e-11
          }
        },
        {
          "variable": "dusrf_dy",
          "time": 0.0,
          "expected": 0.009636393494152122,
          "tolerance": {
            "rel": 1e-11
          }
        },
        {
          "variable": "stagthck",
          "time": 0.0,
          "expected": 395.5268226882404,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "taudx",
          "time": 0.0,
          "expected": 62944.55545074094,
          "tolerance": {
            "rel": 1e-11
          }
        },
        {
          "variable": "taudy",
          "time": 0.0,
          "expected": -34273.52527579979,
          "tolerance": {
            "rel": 1e-11
          }
        },
        {
          "variable": "theta_x",
          "time": 0.0,
          "expected": 0.009102288413827259,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "theta_y",
          "time": 0.0,
          "expected": 0.004271919844844606,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "F_x",
          "time": 0.0,
          "expected": 1.0002485480987848,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "F_y",
          "time": 0.0,
          "expected": 1.0000547475644461,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "geom_step3_cell2414",
      "description": "Dump pin, step 3, cell (24,14): the fastest traced column (uvel_2d = 5.02 m/yr) with a strong positive slope (theta_x = 0.0154 rad); the largest |taudx| of the pinned rows (-3.66e5 Pa at stagthck = 224.3 m).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "usrf_sw": 1289.0543401092405,
        "thck_sw": 118.65431569517798,
        "ice_mask_sw": 1.0,
        "land_mask_sw": 1.0,
        "usrf_se": 1693.4477218315672,
        "thck_se": 190.84774624562968,
        "ice_mask_se": 1.0,
        "land_mask_se": 1.0,
        "usrf_nw": 1729.9481148939894,
        "thck_nw": 600.4481148939893,
        "ice_mask_nw": 1.0,
        "land_mask_nw": 1.0,
        "usrf_ne": 2005.3884265448567,
        "thck_ne": 656.6884753729817,
        "ice_mask_ne": 1.0,
        "land_mask_ne": 1.0
      },
      "assertions": [
        {
          "variable": "dusrf_dx",
          "time": 0.0,
          "expected": 0.01699584233432985,
          "tolerance": {
            "rel": 1e-11
          }
        },
        {
          "variable": "dusrf_dy",
          "time": 0.0,
          "expected": 0.018820861987450963,
          "tolerance": {
            "rel": 1e-11
          }
        },
        {
          "variable": "stagthck",
          "time": 0.0,
          "expected": 391.6596630519446,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "taudx",
          "time": 0.0,
          "expected": -59857.67587651341,
          "tolerance": {
            "rel": 1e-11
          }
        },
        {
          "variable": "taudy",
          "time": 0.0,
          "expected": -66285.21460721428,
          "tolerance": {
            "rel": 1e-11
          }
        },
        {
          "variable": "theta_x",
          "time": 0.0,
          "expected": 0.015389204968387698,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "theta_y",
          "time": 0.0,
          "expected": 0.0069753172530337935,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "F_x",
          "time": 0.0,
          "expected": 1.000710426803122,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "F_y",
          "time": 0.0,
          "expected": 1.0001459627850429,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "geom_step3_cell2813",
      "description": "Dump pin, step 3, cell (28,13): the steepest slope of the pinned rows (theta_x = 0.0305 rad, dusrf_dx = -0.0358, taudx = +3.47e5 Pa at stagthck = 253.2 m), a mid-thickness column (143.7 m) on the inland side of the ice sheet; F_y = 1.00218 carries the non-negligible y slope (theta_y = 0.0234 rad).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "usrf_sw": 1680.0585708552715,
        "thck_sw": 143.65854644120898,
        "ice_mask_sw": 1.0,
        "land_mask_sw": 1.0,
        "usrf_se": 980.010009765625,
        "thck_se": 0.0,
        "ice_mask_se": 0.0,
        "land_mask_se": 1.0,
        "usrf_nw": 1967.6980499264253,
        "thck_nw": 307.3980010983003,
        "ice_mask_nw": 1.0,
        "land_mask_nw": 1.0,
        "usrf_ne": 1236.7292065804522,
        "thck_ne": 26.72920658045218,
        "ice_mask_ne": 1.0,
        "land_mask_ne": 1.0
      },
      "assertions": [
        {
          "variable": "dusrf_dx",
          "time": 0.0,
          "expected": -0.035775435110890486,
          "tolerance": {
            "rel": 1e-11
          }
        },
        {
          "variable": "dusrf_dy",
          "time": 0.0,
          "expected": 0.010493577600788354,
          "tolerance": {
            "rel": 1e-11
          }
        },
        {
          "variable": "stagthck",
          "time": 0.0,
          "expected": 119.44643852999036,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "taudx",
          "time": 0.0,
          "expected": 38426.11165354277,
          "tolerance": {
            "rel": 1e-11
          }
        },
        {
          "variable": "taudy",
          "time": 0.0,
          "expected": -11271.068633635188,
          "tolerance": {
            "rel": 1e-11
          }
        },
        {
          "variable": "theta_x",
          "time": 0.0,
          "expected": 0.030461917690539395,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "theta_y",
          "time": 0.0,
          "expected": 0.011227636823231812,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "F_x",
          "time": 0.0,
          "expected": 1.002782924343511,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "F_y",
          "time": 0.0,
          "expected": 1.00037816359509,
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
