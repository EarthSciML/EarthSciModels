---
title: "MassBalance"
slug: "massbalance"
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

## Variables

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `thck` | `m` | `0.0` | Ice thickness (m). Start the ODE state at H_pre and integrate for dt. The applied rates distribute the CISM step's net change over the interval; H_post is the same update as an algebraic step map. |
| `age` | `yr` | `0.0` | ice age (yr; model%geometry%ice_age, seconds internally, converted to years on output). Incremented d(age)/dt = 1 where thck > 0 (glissade.F90:1203-1213). The Fortran additionally RESETS the age to 0 on ice-free cells (F90:1209-1213); the ODE form only stops the increment - the reset is unobservable in the reference window (no traced cell refreezes) and is a documented difference for the stage-3 assembly. Unpinned (no age column in the dump, and the reference window never refreezes - see README.md) |

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `acab` | `m/yr` | `0.0` | surface mass balance (m/yr ice), as zeroed by GladSmb (model%climate%acab, m/s in the Fortran; glad_timestep.F90:171-187) |
| `bmlt` | `m/yr` | `0.0` | basal melt rate bmlt_ground + bmlt_float (m/yr ice; positive melting, negative freeze-on; model%basal_melt%bmlt, glissade_apply_smb F90:842-850). 0 everywhere in the reference window (cold base, no shelf melt), so the bmlt branches are unpinned source formulas (see README.md) |
| `topg` | `m` | `0.0` | bedrock topography elevation (m), for the ocean mask |
| `eus` | `m` | `0.0` | eustatic sea level (m; 0 in the reference run) |
| `dt` | `yr` | `0.5` | Positive dynamics time step (yr), 0.5 yr in the reference run. |
| `x_sigma2` | `1` | `0.1` | normalized level of the layer-1 interface: x = (up-1)/(upn-1) = 1/10 for upn = 11 (glide_setup.F90:303-308) |
| `x_sigma10` | `1` | `0.9` | normalized level of the layer-10 interface: x = 9/10 for upn = 11 |
| `n_sigma` | `1` | `2.0` | SIGMA_COMPUTE_GLIDE stretch exponent n = 2 (glide_setup.F90:303-308) |
| `H_pre` | `m` | `0.0` | pre-step ice thickness (m; the dumped entry thck of the step, the thickness the Fortran's layer loops start from, F90:1330-1332: thck_layer = thck*(sigma(k+1)-sigma(k))). The tracer blends, the applied-rate bookkeeping and melt_potential are per-step algebraic maps of this entry state, evaluated at the step start |
| `T1` | `degC` | `0.0` | pre-step layer-1 temperature (model%temper%temp(1,:,:), degC) |
| `Tbar` | `degC` | `0.0` | pre-step column-mean temperature over layers 1..10 (the layer-free representation of the temperature tracer column; not a Fortran state - the dump's exit mean is derived) |
| `Tsurf` | `degC` | `0.0` | upper-surface temperature temp(0), the temperature of new accumulation (tracers_usrf of the temperature tracer, glissade_transport.F90:166) |
| `Tbed` | `degC` | `0.0` | lower-surface temperature temp(upn), the temperature of basal freeze-on (tracers_lsrf, glissade_transport.F90:172-174) |
| `T10` | `degC` | `0.0` | pre-step layer-10 temperature (model%temper%temp(10,:,:), degC) |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `sigma2` | `1` | `0.0` | glide sigma level 2 = glide_calc_sigma(0.1, 2) = 0.23140495867768607 (glide_setup.F90:380-387); the layer-1 thickness fraction |
| `sigma10` | `1` | `0.0` | glide sigma level 10 = glide_calc_sigma(0.9, 2) = 0.96398891966759004; the layer-10 thickness fraction is 1 - sigma10 |
| `ocean_mask` | `1` | `0.0` | ocean mask of the mass-balance driver: the cism_ocean predicate on the ENTRY thickness (topg < eus and H_pre <= 0; glissade_get_masks, glissade_masks.F90:70-96, computed from the pre-step state). The SMB and BMB are not applied to ocean cells (glissade_mass_balance.F90:1333-1341) and their applied rates and melt_potential stay 0 (the effective_areafrac = 0 of ocean cells, F90:893-901). No traced cell is ocean (all 32 cells have topg >= 921 m): source formula, unpinned |
| `net` | `m/yr` | `0.0` | unmasked net mass balance acab - bmlt (m/yr ice) |
| `net_applied` | `m/yr` | `0.0` | Applied surface mass balance minus applied basal melt (m/yr), after clipping the two stages in order. |
| `H_post` | `m` | `0.0` | End-of-step thickness after applying the clipped surface and basal changes in order. |
| `melt_potential` | `m` | `0.0` | Unused surface and basal ablation summed over the step (m), evaluated against the ice available at each stage. Zero in open ocean. |
| `s` | `m` | `0.0` | signed surface thickness change per step (m): acab*dt; positive accumulation, negative ablation |
| `b` | `m` | `0.0` | freeze-on thickness per step (m): -bmlt*dt for bmlt < 0, else 0 (bed_accum, F90:1455-1456) |
| `H1` | `m` | `0.0` | pre-step layer-1 thickness = sigma2*H_pre (thck_layer(:,:,1), F90:1330-1332) |
| `H10` | `m` | `0.0` | pre-step layer-10 thickness = (1 - sigma10)*H_pre |
| `acab_applied` | `m/yr` | `0.0` | surface mass balance actually applied (m/yr ice; model%climate%acab_applied, m/s in the Fortran): the full acab while the column survives, -H_pre/dt when the ablation removes the whole column (F90:1385-1422; the Fortran accumulates the applied amount in m per step and converts back to m/s at F90:1567). Derived (not a dump column) - the dump carries the input acab, not the applied value; pinned from the source formula at the full-melt pins |
| `bmlt_applied` | `m/yr` | `0.0` | Actual basal melt rate: limited by H_after_surface for basal melt, equal to bmlt for freeze-on, and zero in open ocean. |
| `T1_out` | `degC` | `0.0` | Layer-1 tracer after surface accumulation or ablation. It is zero if surface ablation exhausts the column or if basal melt removes all remaining ice. |
| `Tbar_blend` | `degC` | `0.0` | Column-mean tracer after the surface stage. The layer-free blend removes ablated ice at T1 and assigns zero when no ice remains. |
| `Tbar_out` | `degC` | `0.0` | Column-mean tracer after the step. Basal freeze-on adds ice at Tbed to the surface-stage tracer mass. Basal melting that removes the entire column gives zero. |
| `T10_out` | `degC` | `0.0` | Layer-10 tracer after the step. Basal freeze-on mixes with the remaining layer-10 ice at Tbed. A fully melted column gives zero. |
| `age_usrf` | `yr` | `0.0` | ice age of new surface accumulation = 0 (tracers_usrf of the age tracer, glissade_transport.F90:204-206). Unpinned |
| `age_lsrf` | `yr` | `0.0` | ice age of basal freeze-on = the bottom-layer age (tracers_lsrf, glissade_transport.F90:207-208); the layer-free model's bottom-layer age is the age state. Unpinned |
| `H_after_surface` | `m` | `0.0` | Thickness after surface accumulation or ablation, before basal melt or freeze-on. |

## Observed expressions

$$
sigma2 = \mathrm{cism_sigma}\left(x=x_{sigma2}, n=n_{sigma}\right)
$$
_glide sigma level 2 = glide_calc_sigma(0.1, 2) = 0.23140495867768607 (glide_setup.F90:380-387); the layer-1 thickness fraction_

$$
sigma10 = \mathrm{cism_sigma}\left(x=x_{sigma10}, n=n_{sigma}\right)
$$
_glide sigma level 10 = glide_calc_sigma(0.9, 2) = 0.96398891966759004; the layer-10 thickness fraction is 1 - sigma10_

$$
ocean_{mask} = \mathrm{cism_ocean}\left(thck=H_{pre}, topg=topg, eus=eus\right)
$$
_ocean mask of the mass-balance driver: the cism_ocean predicate on the ENTRY thickness (topg < eus and H_pre <= 0; glissade_get_masks, glissade_masks.F90:70-96, computed from the pre-step state). The SMB and BMB are not applied to ocean cells (glissade_mass_balance.F90:1333-1341) and their applied rates and melt_potential stay 0 (the effective_areafrac = 0 of ocean cells, F90:893-901). No traced cell is ocean (all 32 cells have topg >= 921 m): source formula, unpinned_

$$
net = acab - bmlt
$$
_unmasked net mass balance acab - bmlt (m/yr ice)_

$$
net_{applied} = acab_{applied} - bmlt_{applied}
$$
_Applied surface mass balance minus applied basal melt (m/yr), after clipping the two stages in order._

$$
H_{post} = \mathrm{max}\left(\mathrm{const}\left(\right), H_{after\,surface} - bmlt_{applied} \cdot dt\right)
$$
_End-of-step thickness after applying the clipped surface and basal changes in order._

$$
melt_{potential} = \mathrm{ifelse}\left(ocean_{mask} = 1.0, \mathrm{const}\left(\right), \mathrm{max}\left(\mathrm{const}\left(\right), -\left(H_{pre} + s\right)\right) + \mathrm{max}\left(\mathrm{const}\left(\right), bmlt \cdot dt - H_{after\,surface}\right)\right)
$$
_Unused surface and basal ablation summed over the step (m), evaluated against the ice available at each stage. Zero in open ocean._

$$
s = acab \cdot dt
$$
_signed surface thickness change per step (m): acab*dt; positive accumulation, negative ablation_

$$
b = \mathrm{max}\left(\mathrm{const}\left(\right), -bmlt_{applied} \cdot dt\right)
$$
_freeze-on thickness per step (m): -bmlt*dt for bmlt < 0, else 0 (bed_accum, F90:1455-1456)_

$$
H1 = sigma2 \cdot H_{pre}
$$
_pre-step layer-1 thickness = sigma2*H_pre (thck_layer(:,:,1), F90:1330-1332)_

$$
H10 = \left(\mathrm{const}\left(\right) - sigma10\right) \cdot H_{pre}
$$
_pre-step layer-10 thickness = (1 - sigma10)*H_pre_

$$
acab_{applied} = \mathrm{ifelse}\left(ocean_{mask} = 1.0, \mathrm{const}\left(\right), \mathrm{ifelse}\left(\mathrm{<=}\left(dt, \mathrm{const}\left(\right)\right), acab, \mathrm{max}\left(acab, -\frac{H_{pre}}{dt}\right)\right)\right)
$$
_surface mass balance actually applied (m/yr ice; model%climate%acab_applied, m/s in the Fortran): the full acab while the column survives, -H_pre/dt when the ablation removes the whole column (F90:1385-1422; the Fortran accumulates the applied amount in m per step and converts back to m/s at F90:1567). Derived (not a dump column) - the dump carries the input acab, not the applied value; pinned from the source formula at the full-melt pins_

$$
bmlt_{applied} = \mathrm{ifelse}\left(ocean_{mask} = 1.0, \mathrm{const}\left(\right), \mathrm{ifelse}\left(\mathrm{<=}\left(dt, \mathrm{const}\left(\right)\right), bmlt, \mathrm{min}\left(bmlt, \frac{H_{after\,surface}}{dt}\right)\right)\right)
$$
_Actual basal melt rate: limited by H_after_surface for basal melt, equal to bmlt for freeze-on, and zero in open ocean._

$$
T1_{out} = \mathrm{ifelse}\left(\mathrm{or}\left(\mathrm{<=}\left(H_{post}, \mathrm{const}\left(\right)\right), \mathrm{<=}\left(H_{after\,surface}, \mathrm{const}\left(\right)\right)\right), \mathrm{const}\left(\right), \mathrm{ifelse}\left(\mathrm{>}\left(s, \mathrm{const}\left(\right)\right), \mathrm{cism_tracer_mix}\left(H=H1, T=T1, s=s, Tp=Tsurf\right), T1\right)\right)
$$
_Layer-1 tracer after surface accumulation or ablation. It is zero if surface ablation exhausts the column or if basal melt removes all remaining ice._

$$
Tbar_{blend} = \mathrm{ifelse}\left(\mathrm{>}\left(H_{after\,surface}, \mathrm{const}\left(\right)\right), \mathrm{cism_tracer_mix}\left(H=H_{pre}, T=Tbar, s=s, Tp=\mathrm{ifelse}\left(\mathrm{>}\left(s, \mathrm{const}\left(\right)\right), Tsurf, T1\right)\right), \mathrm{const}\left(\right)\right)
$$
_Column-mean tracer after the surface stage. The layer-free blend removes ablated ice at T1 and assigns zero when no ice remains._

$$
Tbar_{out} = \mathrm{ifelse}\left(\mathrm{<=}\left(H_{post}, \mathrm{const}\left(\right)\right), \mathrm{const}\left(\right), \mathrm{cism_tracer_mix}\left(H=H_{after\,surface}, T=Tbar_{blend}, s=b, Tp=Tbed\right)\right)
$$
_Column-mean tracer after the step. Basal freeze-on adds ice at Tbed to the surface-stage tracer mass. Basal melting that removes the entire column gives zero._

$$
T10_{out} = \mathrm{ifelse}\left(\mathrm{<=}\left(H_{post}, \mathrm{const}\left(\right)\right), \mathrm{const}\left(\right), \mathrm{ifelse}\left(\mathrm{<}\left(bmlt, \mathrm{const}\left(\right)\right), \mathrm{cism_tracer_mix}\left(H=\mathrm{min}\left(H10, H_{after\,surface}\right), T=T10, s=b, Tp=Tbed\right), T10\right)\right)
$$
_Layer-10 tracer after the step. Basal freeze-on mixes with the remaining layer-10 ice at Tbed. A fully melted column gives zero._

$$
age_{usrf} = \mathrm{const}\left(\right)
$$
_ice age of new surface accumulation = 0 (tracers_usrf of the age tracer, glissade_transport.F90:204-206). Unpinned_

$$
age_{lsrf} = age
$$
_ice age of basal freeze-on = the bottom-layer age (tracers_lsrf, glissade_transport.F90:207-208); the layer-free model's bottom-layer age is the age state. Unpinned_

$$
H_{after\,surface} = \mathrm{max}\left(\mathrm{const}\left(\right), H_{pre} + acab_{applied} \cdot dt\right)
$$
_Thickness after surface accumulation or ablation, before basal melt or freeze-on._

## Equations

$$
\mathrm{D}\left(thck\right) = \mathrm{ifelse}\left(\mathrm{and}\left(\mathrm{<=}\left(thck, \mathrm{const}\left(\right)\right), \mathrm{<}\left(net_{applied}, \mathrm{const}\left(\right)\right)\right), \mathrm{const}\left(\right), net_{applied}\right)
$$

$$
\mathrm{D}\left(age\right) = \mathrm{ifelse}\left(\mathrm{>}\left(thck, \mathrm{const}\left(\right)\right), \mathrm{const}\left(\right), \mathrm{const}\left(\right)\right)
$$

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
    "acab": {
      "type": "parameter",
      "units": "m/yr",
      "default": 0.0,
      "description": "surface mass balance (m/yr ice), as zeroed by GladSmb (model%climate%acab, m/s in the Fortran; glad_timestep.F90:171-187)"
    },
    "bmlt": {
      "type": "parameter",
      "units": "m/yr",
      "default": 0.0,
      "description": "basal melt rate bmlt_ground + bmlt_float (m/yr ice; positive melting, negative freeze-on; model%basal_melt%bmlt, glissade_apply_smb F90:842-850). 0 everywhere in the reference window (cold base, no shelf melt), so the bmlt branches are unpinned source formulas (see README.md)"
    },
    "topg": {
      "type": "parameter",
      "units": "m",
      "default": 0.0,
      "description": "bedrock topography elevation (m), for the ocean mask"
    },
    "eus": {
      "type": "parameter",
      "units": "m",
      "default": 0.0,
      "description": "eustatic sea level (m; 0 in the reference run)"
    },
    "dt": {
      "type": "parameter",
      "units": "yr",
      "default": 0.5,
      "description": "Positive dynamics time step (yr), 0.5 yr in the reference run."
    },
    "x_sigma2": {
      "type": "parameter",
      "units": "1",
      "default": 0.1,
      "description": "normalized level of the layer-1 interface: x = (up-1)/(upn-1) = 1/10 for upn = 11 (glide_setup.F90:303-308)"
    },
    "x_sigma10": {
      "type": "parameter",
      "units": "1",
      "default": 0.9,
      "description": "normalized level of the layer-10 interface: x = 9/10 for upn = 11"
    },
    "n_sigma": {
      "type": "parameter",
      "units": "1",
      "default": 2.0,
      "description": "SIGMA_COMPUTE_GLIDE stretch exponent n = 2 (glide_setup.F90:303-308)"
    },
    "H_pre": {
      "type": "parameter",
      "units": "m",
      "default": 0.0,
      "description": "pre-step ice thickness (m; the dumped entry thck of the step, the thickness the Fortran's layer loops start from, F90:1330-1332: thck_layer = thck*(sigma(k+1)-sigma(k))). The tracer blends, the applied-rate bookkeeping and melt_potential are per-step algebraic maps of this entry state, evaluated at the step start"
    },
    "T1": {
      "type": "parameter",
      "units": "degC",
      "default": 0.0,
      "description": "pre-step layer-1 temperature (model%temper%temp(1,:,:), degC)"
    },
    "Tbar": {
      "type": "parameter",
      "units": "degC",
      "default": 0.0,
      "description": "pre-step column-mean temperature over layers 1..10 (the layer-free representation of the temperature tracer column; not a Fortran state - the dump's exit mean is derived)"
    },
    "Tsurf": {
      "type": "parameter",
      "units": "degC",
      "default": 0.0,
      "description": "upper-surface temperature temp(0), the temperature of new accumulation (tracers_usrf of the temperature tracer, glissade_transport.F90:166)"
    },
    "Tbed": {
      "type": "parameter",
      "units": "degC",
      "default": 0.0,
      "description": "lower-surface temperature temp(upn), the temperature of basal freeze-on (tracers_lsrf, glissade_transport.F90:172-174)"
    },
    "T10": {
      "type": "parameter",
      "units": "degC",
      "default": 0.0,
      "description": "pre-step layer-10 temperature (model%temper%temp(10,:,:), degC)"
    },
    "sigma2": {
      "type": "unknown",
      "units": "1",
      "default": 0.0,
      "description": "glide sigma level 2 = glide_calc_sigma(0.1, 2) = 0.23140495867768607 (glide_setup.F90:380-387); the layer-1 thickness fraction"
    },
    "sigma10": {
      "type": "unknown",
      "units": "1",
      "default": 0.0,
      "description": "glide sigma level 10 = glide_calc_sigma(0.9, 2) = 0.96398891966759004; the layer-10 thickness fraction is 1 - sigma10"
    },
    "ocean_mask": {
      "type": "unknown",
      "units": "1",
      "default": 0.0,
      "description": "ocean mask of the mass-balance driver: the cism_ocean predicate on the ENTRY thickness (topg < eus and H_pre <= 0; glissade_get_masks, glissade_masks.F90:70-96, computed from the pre-step state). The SMB and BMB are not applied to ocean cells (glissade_mass_balance.F90:1333-1341) and their applied rates and melt_potential stay 0 (the effective_areafrac = 0 of ocean cells, F90:893-901). No traced cell is ocean (all 32 cells have topg >= 921 m): source formula, unpinned"
    },
    "net": {
      "type": "unknown",
      "units": "m/yr",
      "default": 0.0,
      "description": "unmasked net mass balance acab - bmlt (m/yr ice)"
    },
    "net_applied": {
      "type": "unknown",
      "units": "m/yr",
      "default": 0.0,
      "description": "Applied surface mass balance minus applied basal melt (m/yr), after clipping the two stages in order."
    },
    "thck": {
      "type": "unknown",
      "units": "m",
      "default": 0.0,
      "description": "Ice thickness (m). Start the ODE state at H_pre and integrate for dt. The applied rates distribute the CISM step's net change over the interval; H_post is the same update as an algebraic step map."
    },
    "H_post": {
      "type": "unknown",
      "units": "m",
      "default": 0.0,
      "description": "End-of-step thickness after applying the clipped surface and basal changes in order."
    },
    "melt_potential": {
      "type": "unknown",
      "units": "m",
      "default": 0.0,
      "description": "Unused surface and basal ablation summed over the step (m), evaluated against the ice available at each stage. Zero in open ocean."
    },
    "s": {
      "type": "unknown",
      "units": "m",
      "default": 0.0,
      "description": "signed surface thickness change per step (m): acab*dt; positive accumulation, negative ablation"
    },
    "b": {
      "type": "unknown",
      "units": "m",
      "default": 0.0,
      "description": "freeze-on thickness per step (m): -bmlt*dt for bmlt < 0, else 0 (bed_accum, F90:1455-1456)"
    },
    "H1": {
      "type": "unknown",
      "units": "m",
      "default": 0.0,
      "description": "pre-step layer-1 thickness = sigma2*H_pre (thck_layer(:,:,1), F90:1330-1332)"
    },
    "H10": {
      "type": "unknown",
      "units": "m",
      "default": 0.0,
      "description": "pre-step layer-10 thickness = (1 - sigma10)*H_pre"
    },
    "acab_applied": {
      "type": "unknown",
      "units": "m/yr",
      "default": 0.0,
      "description": "surface mass balance actually applied (m/yr ice; model%climate%acab_applied, m/s in the Fortran): the full acab while the column survives, -H_pre/dt when the ablation removes the whole column (F90:1385-1422; the Fortran accumulates the applied amount in m per step and converts back to m/s at F90:1567). Derived (not a dump column) - the dump carries the input acab, not the applied value; pinned from the source formula at the full-melt pins"
    },
    "bmlt_applied": {
      "type": "unknown",
      "units": "m/yr",
      "default": 0.0,
      "description": "Actual basal melt rate: limited by H_after_surface for basal melt, equal to bmlt for freeze-on, and zero in open ocean."
    },
    "T1_out": {
      "type": "unknown",
      "units": "degC",
      "default": 0.0,
      "description": "Layer-1 tracer after surface accumulation or ablation. It is zero if surface ablation exhausts the column or if basal melt removes all remaining ice."
    },
    "Tbar_blend": {
      "type": "unknown",
      "units": "degC",
      "default": 0.0,
      "description": "Column-mean tracer after the surface stage. The layer-free blend removes ablated ice at T1 and assigns zero when no ice remains."
    },
    "Tbar_out": {
      "type": "unknown",
      "units": "degC",
      "default": 0.0,
      "description": "Column-mean tracer after the step. Basal freeze-on adds ice at Tbed to the surface-stage tracer mass. Basal melting that removes the entire column gives zero."
    },
    "T10_out": {
      "type": "unknown",
      "units": "degC",
      "default": 0.0,
      "description": "Layer-10 tracer after the step. Basal freeze-on mixes with the remaining layer-10 ice at Tbed. A fully melted column gives zero."
    },
    "age": {
      "type": "unknown",
      "units": "yr",
      "default": 0.0,
      "description": "ice age (yr; model%geometry%ice_age, seconds internally, converted to years on output). Incremented d(age)/dt = 1 where thck > 0 (glissade.F90:1203-1213). The Fortran additionally RESETS the age to 0 on ice-free cells (F90:1209-1213); the ODE form only stops the increment - the reset is unobservable in the reference window (no traced cell refreezes) and is a documented difference for the stage-3 assembly. Unpinned (no age column in the dump, and the reference window never refreezes - see README.md)"
    },
    "age_usrf": {
      "type": "unknown",
      "units": "yr",
      "default": 0.0,
      "description": "ice age of new surface accumulation = 0 (tracers_usrf of the age tracer, glissade_transport.F90:204-206). Unpinned"
    },
    "age_lsrf": {
      "type": "unknown",
      "units": "yr",
      "default": 0.0,
      "description": "ice age of basal freeze-on = the bottom-layer age (tracers_lsrf, glissade_transport.F90:207-208); the layer-free model's bottom-layer age is the age state. Unpinned"
    },
    "H_after_surface": {
      "type": "unknown",
      "units": "m",
      "default": 0.0,
      "description": "Thickness after surface accumulation or ablation, before basal melt or freeze-on."
    }
  },
  "equations": [
    {
      "lhs": "sigma2",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "cism_sigma",
        "bindings": {
          "x": "x_sigma2",
          "n": "n_sigma"
        }
      }
    },
    {
      "lhs": "sigma10",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "cism_sigma",
        "bindings": {
          "x": "x_sigma10",
          "n": "n_sigma"
        }
      }
    },
    {
      "lhs": "ocean_mask",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "cism_ocean",
        "bindings": {
          "thck": "H_pre",
          "topg": "topg",
          "eus": "eus"
        }
      }
    },
    {
      "lhs": "net",
      "rhs": {
        "op": "-",
        "args": [
          "acab",
          "bmlt"
        ]
      }
    },
    {
      "lhs": "net_applied",
      "rhs": {
        "op": "-",
        "args": [
          "acab_applied",
          "bmlt_applied"
        ]
      }
    },
    {
      "lhs": {
        "op": "D",
        "args": [
          "thck"
        ],
        "wrt": "t"
      },
      "rhs": {
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
                  "net_applied",
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
          "net_applied"
        ]
      }
    },
    {
      "lhs": "H_after_surface",
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
            "op": "+",
            "args": [
              "H_pre",
              {
                "op": "*",
                "args": [
                  "acab_applied",
                  "dt"
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "H_post",
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
            "op": "-",
            "args": [
              "H_after_surface",
              {
                "op": "*",
                "args": [
                  "bmlt_applied",
                  "dt"
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "melt_potential",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "==",
            "args": [
              "ocean_mask",
              1.0
            ]
          },
          {
            "op": "const",
            "args": [],
            "value": 0.0,
            "units": "m"
          },
          {
            "op": "+",
            "args": [
              {
                "op": "max",
                "args": [
                  {
                    "op": "const",
                    "args": [],
                    "value": 0.0,
                    "units": "m"
                  },
                  {
                    "op": "-",
                    "args": [
                      {
                        "op": "+",
                        "args": [
                          "H_pre",
                          "s"
                        ]
                      }
                    ]
                  }
                ]
              },
              {
                "op": "max",
                "args": [
                  {
                    "op": "const",
                    "args": [],
                    "value": 0.0,
                    "units": "m"
                  },
                  {
                    "op": "-",
                    "args": [
                      {
                        "op": "*",
                        "args": [
                          "bmlt",
                          "dt"
                        ]
                      },
                      "H_after_surface"
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "s",
      "rhs": {
        "op": "*",
        "args": [
          "acab",
          "dt"
        ]
      }
    },
    {
      "lhs": "b",
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
            "op": "-",
            "args": [
              {
                "op": "*",
                "args": [
                  "bmlt_applied",
                  "dt"
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "acab_applied",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "==",
            "args": [
              "ocean_mask",
              1.0
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
                "op": "<=",
                "args": [
                  "dt",
                  {
                    "op": "const",
                    "args": [],
                    "value": 0.0,
                    "units": "yr"
                  }
                ]
              },
              "acab",
              {
                "op": "max",
                "args": [
                  "acab",
                  {
                    "op": "-",
                    "args": [
                      {
                        "op": "/",
                        "args": [
                          "H_pre",
                          "dt"
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
    },
    {
      "lhs": "bmlt_applied",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "==",
            "args": [
              "ocean_mask",
              1.0
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
                "op": "<=",
                "args": [
                  "dt",
                  {
                    "op": "const",
                    "args": [],
                    "value": 0.0,
                    "units": "yr"
                  }
                ]
              },
              "bmlt",
              {
                "op": "min",
                "args": [
                  "bmlt",
                  {
                    "op": "/",
                    "args": [
                      "H_after_surface",
                      "dt"
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "H1",
      "rhs": {
        "op": "*",
        "args": [
          "sigma2",
          "H_pre"
        ]
      }
    },
    {
      "lhs": "H10",
      "rhs": {
        "op": "*",
        "args": [
          {
            "op": "-",
            "args": [
              {
                "op": "const",
                "args": [],
                "value": 1.0,
                "units": "1"
              },
              "sigma10"
            ]
          },
          "H_pre"
        ]
      }
    },
    {
      "lhs": "T1_out",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "or",
            "args": [
              {
                "op": "<=",
                "args": [
                  "H_post",
                  {
                    "op": "const",
                    "args": [],
                    "value": 0.0,
                    "units": "m"
                  }
                ]
              },
              {
                "op": "<=",
                "args": [
                  "H_after_surface",
                  {
                    "op": "const",
                    "args": [],
                    "value": 0.0,
                    "units": "m"
                  }
                ]
              }
            ]
          },
          {
            "op": "const",
            "args": [],
            "value": 0.0,
            "units": "degC"
          },
          {
            "op": "ifelse",
            "args": [
              {
                "op": ">",
                "args": [
                  "s",
                  {
                    "op": "const",
                    "args": [],
                    "value": 0.0,
                    "units": "m"
                  }
                ]
              },
              {
                "op": "apply_expression_template",
                "args": [],
                "name": "cism_tracer_mix",
                "bindings": {
                  "H": "H1",
                  "T": "T1",
                  "s": "s",
                  "Tp": "Tsurf"
                }
              },
              "T1"
            ]
          }
        ]
      }
    },
    {
      "lhs": "Tbar_blend",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": ">",
            "args": [
              "H_after_surface",
              {
                "op": "const",
                "args": [],
                "value": 0.0,
                "units": "m"
              }
            ]
          },
          {
            "op": "apply_expression_template",
            "args": [],
            "name": "cism_tracer_mix",
            "bindings": {
              "H": "H_pre",
              "T": "Tbar",
              "s": "s",
              "Tp": {
                "op": "ifelse",
                "args": [
                  {
                    "op": ">",
                    "args": [
                      "s",
                      {
                        "op": "const",
                        "args": [],
                        "value": 0.0,
                        "units": "m"
                      }
                    ]
                  },
                  "Tsurf",
                  "T1"
                ]
              }
            }
          },
          {
            "op": "const",
            "args": [],
            "value": 0.0,
            "units": "degC"
          }
        ]
      }
    },
    {
      "lhs": "Tbar_out",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "<=",
            "args": [
              "H_post",
              {
                "op": "const",
                "args": [],
                "value": 0.0,
                "units": "m"
              }
            ]
          },
          {
            "op": "const",
            "args": [],
            "value": 0.0,
            "units": "degC"
          },
          {
            "op": "apply_expression_template",
            "args": [],
            "name": "cism_tracer_mix",
            "bindings": {
              "H": "H_after_surface",
              "T": "Tbar_blend",
              "s": "b",
              "Tp": "Tbed"
            }
          }
        ]
      }
    },
    {
      "lhs": "T10_out",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "<=",
            "args": [
              "H_post",
              {
                "op": "const",
                "args": [],
                "value": 0.0,
                "units": "m"
              }
            ]
          },
          {
            "op": "const",
            "args": [],
            "value": 0.0,
            "units": "degC"
          },
          {
            "op": "ifelse",
            "args": [
              {
                "op": "<",
                "args": [
                  "bmlt",
                  {
                    "op": "const",
                    "args": [],
                    "value": 0.0,
                    "units": "m/yr"
                  }
                ]
              },
              {
                "op": "apply_expression_template",
                "args": [],
                "name": "cism_tracer_mix",
                "bindings": {
                  "H": {
                    "op": "min",
                    "args": [
                      "H10",
                      "H_after_surface"
                    ]
                  },
                  "T": "T10",
                  "s": "b",
                  "Tp": "Tbed"
                }
              },
              "T10"
            ]
          }
        ]
      }
    },
    {
      "lhs": {
        "op": "D",
        "args": [
          "age"
        ],
        "wrt": "t"
      },
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": ">",
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
            "op": "const",
            "args": [],
            "value": 1.0,
            "units": "yr/yr"
          },
          {
            "op": "const",
            "args": [],
            "value": 0.0,
            "units": "yr/yr"
          }
        ]
      }
    },
    {
      "lhs": "age_usrf",
      "rhs": {
        "op": "const",
        "args": [],
        "value": 0.0,
        "units": "yr"
      }
    },
    {
      "lhs": "age_lsrf",
      "rhs": "age"
    }
  ],
  "tests": [
    {
      "id": "accumulate_thickness_step1_cell2611",
      "description": "Dump pin of the thickness rate law d(thck)/dt = acab - bmlt with bmlt = 0: the cism_transport.csv entry row of cell 26,11 at step 1 has thck = 14 m and acab = 2.0809741699667099 m/yr; the SMB-only prediction after one 0.5-yr step is 14 + 0.5*2.0809741699667099 = 15.040487084983354 m, and the dump exit thck is 15.040488048712829 m. The +9.64e-07 m residual is the horizontal advection of the step (the transport happens between the entry and exit phases of the dump; the same cell's step-2 residual drops to +9.6e-10 m, see README.md): tolerance rel 1e-6 is ~10x the residual.",
      "time_span": {
        "start": 0.0,
        "end": 0.5
      },
      "parameter_overrides": {
        "acab": 2.08097416996671,
        "topg": 1752.9000244140625,
        "H_pre": 14.0
      },
      "initial_conditions": {
        "thck": 14.0,
        "age": 0.0
      },
      "assertions": [
        {
          "variable": "thck",
          "time": 0.5,
          "expected": 15.04048804871283,
          "tolerance": {
            "rel": 1e-06
          }
        }
      ]
    },
    {
      "id": "accumulate_thickness_step2_cell2611",
      "description": "Dump pin, same cell, step 2: entry thck = 15.040488048712829 m (the step-1 exit), same acab; prediction 16.080975133696185 m vs dump exit 16.080975134653887 m - the advection residual is +9.58e-10 m (rel 6e-11), near round-off: tolerance rel 1e-9.",
      "time_span": {
        "start": 0.0,
        "end": 0.5
      },
      "parameter_overrides": {
        "acab": 2.08097416996671,
        "topg": 1752.9000244140625,
        "H_pre": 15.04048804871283
      },
      "initial_conditions": {
        "thck": 15.04048804871283,
        "age": 0.0
      },
      "assertions": [
        {
          "variable": "thck",
          "time": 0.5,
          "expected": 16.080975134653887,
          "tolerance": {
            "rel": 1e-09
          }
        }
      ]
    },
    {
      "id": "accumulate_thickness_step4_cell2611",
      "description": "Dump pin, same cell, step 4 (the second cap year's ablation-free second step): entry thck = 16.85918996861492 m with acab = 1.5564316967068248 m/yr (cap_step 2 qsmb of this cell); prediction 17.637405816968332 m vs dump exit 17.637404090581274 m - residual -1.73e-06 m: tolerance rel 1e-6.",
      "time_span": {
        "start": 0.0,
        "end": 0.5
      },
      "parameter_overrides": {
        "acab": 1.5564316967068248,
        "topg": 1752.9000244140625,
        "H_pre": 16.85918996861492
      },
      "initial_conditions": {
        "thck": 16.85918996861492,
        "age": 0.0
      },
      "assertions": [
        {
          "variable": "thck",
          "time": 0.5,
          "expected": 17.637404090581274,
          "tolerance": {
            "rel": 1e-06
          }
        }
      ]
    },
    {
      "id": "ablate_thickness_step3_cell2511",
      "description": "Dump pin of the ablation year: cell 25,11 at step 3 has entry thck = 1.4394647029325882 m and acab = -0.58145483354207683 m/yr; prediction 1.1487372861615497 m vs dump exit 1.1487549741605207 m - residual +1.77e-05 m (rel 1.5e-5): tolerance rel 2e-4.",
      "time_span": {
        "start": 0.0,
        "end": 0.5
      },
      "parameter_overrides": {
        "acab": -0.5814548335420768,
        "topg": 1082.0,
        "H_pre": 1.4394647029325882
      },
      "initial_conditions": {
        "thck": 1.4394647029325882,
        "age": 0.0
      },
      "assertions": [
        {
          "variable": "thck",
          "time": 0.5,
          "expected": 1.1487549741605207,
          "tolerance": {
            "rel": 0.0002
          }
        }
      ]
    },
    {
      "id": "ablate_thickness_step4_cell2511",
      "description": "Dump pin, same cell, step 4: entry thck = 1.1487549741605207 m; prediction 0.8580275573894823 m vs dump exit 0.85804631872704562 m - residual +1.88e-05 m (rel 2.2e-5): tolerance rel 3e-4.",
      "time_span": {
        "start": 0.0,
        "end": 0.5
      },
      "parameter_overrides": {
        "acab": -0.5814548335420768,
        "topg": 1082.0,
        "H_pre": 1.1487549741605207
      },
      "initial_conditions": {
        "thck": 1.1487549741605207,
        "age": 0.0
      },
      "assertions": [
        {
          "variable": "thck",
          "time": 0.5,
          "expected": 0.8580463187270456,
          "tolerance": {
            "rel": 0.0003
          }
        }
      ]
    },
    {
      "id": "full_melt_step1_cell2811",
      "description": "Dump pin for full melt. Surface ablation at -0.7075135162820545 m/yr exhausts the 0.0199584998190403 m entry column during the step. The applied surface rate removes the available thickness, giving the dumped exit thickness of zero.",
      "time_span": {
        "start": 0.0,
        "end": 0.5
      },
      "parameter_overrides": {
        "acab": -0.7075135162820545,
        "topg": 921.1400146484375,
        "H_pre": 0.0199584998190403
      },
      "initial_conditions": {
        "thck": 0.0199584998190403,
        "age": 0.0
      },
      "assertions": [
        {
          "variable": "thck",
          "time": 0.5,
          "expected": 0.0,
          "tolerance": {
            "rel": 1e-12,
            "abs": 1e-08
          }
        }
      ]
    },
    {
      "id": "full_melt_step3_cell2811",
      "description": "Dump pin for full melt. Surface ablation at -1.7674468845051972 m/yr exhausts the 1.6503583323323985e-05 m entry column during the step. The applied surface rate removes the available thickness, giving the dumped exit thickness of zero.",
      "time_span": {
        "start": 0.0,
        "end": 0.5
      },
      "parameter_overrides": {
        "acab": -1.7674468845051972,
        "topg": 921.1400146484375,
        "H_pre": 1.6503583323323985e-05
      },
      "initial_conditions": {
        "thck": 1.6503583323323985e-05,
        "age": 0.0
      },
      "assertions": [
        {
          "variable": "thck",
          "time": 0.5,
          "expected": 0.0,
          "tolerance": {
            "rel": 1e-12,
            "abs": 1e-08
          }
        }
      ]
    },
    {
      "id": "full_melt_step1_cell2913",
      "description": "Dump pin for full melt. Surface ablation at -0.5325515248149018 m/yr exhausts the 0.0399780310690403 m entry column during the step. The applied surface rate removes the available thickness, giving the dumped exit thickness of zero.",
      "time_span": {
        "start": 0.0,
        "end": 0.5
      },
      "parameter_overrides": {
        "acab": -0.5325515248149018,
        "topg": 980.010009765625,
        "H_pre": 0.0399780310690403
      },
      "initial_conditions": {
        "thck": 0.0399780310690403,
        "age": 0.0
      },
      "assertions": [
        {
          "variable": "thck",
          "time": 0.5,
          "expected": 0.0,
          "tolerance": {
            "rel": 1e-12,
            "abs": 1e-08
          }
        }
      ]
    },
    {
      "id": "layer1_blend_step1_cell2611",
      "description": "Dump pin of the layer-1 accumulation blend T1' = (H1*T1 + s*Tsurf)/(H1 + s) with H1 = sigma2*H_pre, s = acab*dt (F90:1380-1386), as the per-step algebraic map of the dumped entry state: cell 26,11 at step 1 has entry thck = 14 m (H_pre), T1 = temp_001 = -2.4958552232280957 degC, Tsurf = temp_000 = -1.041416074241738 degC (the surface temperature, = artm on this cell) and acab = 2.0809741699667099 m/yr; s = 1.040487084983355 m, H1 = 0.23140495867768607*14 = 3.239669421487605 m, blend = -2.142287509494599 degC. The dump's exit temp_001 is -2.1422892285376252 degC - the residual -1.72e-06 degC is the horizontal advection and vertical remap of the step (the new surface layer lies within the blended layer 1, so the blend itself is the Fortran's exact pre-remap value): tolerance rel 1e-5. The law's effect (0.354 degC) exceeds the residual by five orders of magnitude, so the assertion fails without the blend.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "acab": 2.08097416996671,
        "topg": 1752.9000244140625,
        "H_pre": 14.0,
        "T1": -2.4958552232280957,
        "Tsurf": -1.041416074241738
      },
      "assertions": [
        {
          "variable": "T1_out",
          "time": 0.0,
          "expected": -2.142289228537625,
          "tolerance": {
            "rel": 1e-05
          }
        }
      ]
    },
    {
      "id": "layer1_blend_step1_cell2711",
      "description": "Dump pin of the accumulation blend with the new snow layer deeper than layer 1 (s = 1.065497900516611 m > H1 = 1.0413223140495873 m): cell 27,11 at step 1 has entry thck = 4.5 m, T1 = -1.8315649780451615 degC, Tsurf = -1.4796403057549128 degC, acab = 2.1309958010332219 m/yr; blend = -1.6535834887501839 degC vs dump exit temp_001 = -1.6535950045502839 degC (residual -1.15e-05 degC; the blend formula is still exact pre-remap because the new layer 1 of thickness sigma2*(thck + s) lies inside the blended layer of thickness H1 + s): tolerance rel 7e-5.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "acab": 2.130995801033222,
        "topg": 1752.9000244140625,
        "H_pre": 4.5,
        "T1": -1.8315649780451615,
        "Tsurf": -1.4796403057549128
      },
      "assertions": [
        {
          "variable": "T1_out",
          "time": 0.0,
          "expected": -1.6535950045502839,
          "tolerance": {
            "rel": 7e-05
          }
        }
      ]
    },
    {
      "id": "layer1_blend_step1_cell2512",
      "description": "Dump pin of the accumulation blend at a third cell: cell 25,12 at step 1 has entry thck = 6.0999760627746582 m, T1 = -1.8445613381693202 degC, Tsurf = -1.2769386424540698 degC, acab = 0.61503345382937313 m/yr; blend = -1.743022533847207 degC vs dump exit temp_001 = -1.7430587941782636 degC (residual -3.63e-05 degC, the largest of the three blend pins - this cell sits in the stronger-advection zone of the traced window): tolerance rel 2.5e-4.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "acab": 0.6150334538293731,
        "topg": 1237.300048828125,
        "H_pre": 6.099976062774658,
        "T1": -1.8445613381693202,
        "Tsurf": -1.2769386424540698
      },
      "assertions": [
        {
          "variable": "T1_out",
          "time": 0.0,
          "expected": -1.7430587941782636,
          "tolerance": {
            "rel": 0.00025
          }
        }
      ]
    },
    {
      "id": "full_melt_step1_cell2811_rates",
      "description": "Per-step algebraic maps of the dumped entry state of cell 28,11 step 1 (entry thck = 0.019958499819040298 m, acab = -0.7075135162820545 m/yr): melt_potential = max(0, -(H_pre + net*dt)) = 0.35375675814102725 - 0.019958499819040298 = 0.33379825832198695 m (derived, not a dump column - the per-step value follows from the same conservation check the Fortran itself runs, F90:1523-1538); acab_applied = -H_pre/dt = -0.039916999638080596 m/yr (derived, not a dump column - the surface ablation applied to the 0.0199585 m that existed; the Fortran accumulates the applied amount per step, F90:1385-1422). The dump's exit temp_001..010 are all 0 (the tracer = 0 of the removed layers, F90:1411-1413), pinning T1_out = 0 (the H_post <= 0 zeroing; Tbar_out has no Fortran counterpart and is left unpinned).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "acab": -0.7075135162820545,
        "topg": 921.1400146484375,
        "H_pre": 0.0199584998190403,
        "T1": -2.389185071557904,
        "Tbar": -2.389185071557904,
        "Tsurf": -2.389185071557904,
        "Tbed": -2.389185071557904
      },
      "assertions": [
        {
          "variable": "melt_potential",
          "time": 0.0,
          "expected": 0.33379825832198695,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "acab_applied",
          "time": 0.0,
          "expected": -0.0399169996380806,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "T1_out",
          "time": 0.0,
          "expected": 0.0
        }
      ]
    },
    {
      "id": "full_melt_step3_cell2811_rates",
      "description": "Per-step algebraic map of the dumped entry state of cell 28,11 step 3 (entry thck = 1.6503583323323985e-05 m, acab = -1.7674468845051972 m/yr): melt_potential = 0.8837234422525986 - 1.6503583323323985e-05 = 0.8837069386692753 m (derived, not a dump column - the per-step excess of the fully melted column).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "acab": -1.7674468845051972,
        "topg": 921.1400146484375,
        "H_pre": 1.6503583323323985e-05
      },
      "assertions": [
        {
          "variable": "melt_potential",
          "time": 0.0,
          "expected": 0.8837069386692753,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "full_melt_step1_cell2913_rates",
      "description": "Per-step algebraic map of the dumped entry state of cell 29,13 step 1 (entry thck = 0.039978031069040298 m, acab = -0.53255152481490176 m/yr): melt_potential = 0.26627576240745088 - 0.039978031069040298 = 0.22629773133841058 m (derived, not a dump column - the per-step excess of the fully melted column).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "acab": -0.5325515248149018,
        "topg": 980.010009765625,
        "H_pre": 0.0399780310690403
      },
      "assertions": [
        {
          "variable": "melt_potential",
          "time": 0.0,
          "expected": 0.22629773133841058,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "surface_exhaustion_before_basal_freeze_on",
      "description": "CISM clips surface ablation first, records unused melt potential, then adds ice at the bed temperature.",
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "initial_conditions": {
        "thck": 1.0
      },
      "parameter_overrides": {
        "dt": 1.0,
        "H_pre": 1.0,
        "acab": -2.0,
        "bmlt": -2.0,
        "T1": -5.0,
        "Tbar": -5.0,
        "T10": -5.0,
        "Tbed": -1.0
      },
      "assertions": [
        {
          "variable": "thck",
          "time": 1.0,
          "expected": 2.0,
          "tolerance": {
            "abs": 1e-09,
            "rel": 0.0
          }
        },
        {
          "variable": "H_after_surface",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "abs": 1e-09,
            "rel": 0.0
          }
        },
        {
          "variable": "H_post",
          "time": 0.0,
          "expected": 2.0,
          "tolerance": {
            "abs": 1e-09,
            "rel": 0.0
          }
        },
        {
          "variable": "melt_potential",
          "time": 0.0,
          "expected": 1.0,
          "tolerance": {
            "abs": 1e-09,
            "rel": 0.0
          }
        },
        {
          "variable": "acab_applied",
          "time": 0.0,
          "expected": -1.0,
          "tolerance": {
            "abs": 1e-09,
            "rel": 0.0
          }
        },
        {
          "variable": "bmlt_applied",
          "time": 0.0,
          "expected": -2.0,
          "tolerance": {
            "abs": 1e-09,
            "rel": 0.0
          }
        },
        {
          "variable": "T1_out",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "abs": 1e-09,
            "rel": 0.0
          }
        },
        {
          "variable": "Tbar_out",
          "time": 0.0,
          "expected": -1.0,
          "tolerance": {
            "abs": 1e-09,
            "rel": 0.0
          }
        },
        {
          "variable": "T10_out",
          "time": 0.0,
          "expected": -1.0,
          "tolerance": {
            "abs": 1e-09,
            "rel": 0.0
          }
        }
      ]
    },
    {
      "id": "basal_melt_uses_surface_accumulation",
      "description": "Basal melt can consume ice accumulated during the same surface step.",
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "initial_conditions": {
        "thck": 1.0
      },
      "parameter_overrides": {
        "dt": 1.0,
        "H_pre": 1.0,
        "acab": 2.0,
        "bmlt": 4.0
      },
      "assertions": [
        {
          "variable": "thck",
          "time": 1.0,
          "expected": 0.0,
          "tolerance": {
            "abs": 1e-08,
            "rel": 0.0
          }
        },
        {
          "variable": "H_post",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "abs": 1e-09,
            "rel": 0.0
          }
        },
        {
          "variable": "bmlt_applied",
          "time": 0.0,
          "expected": 3.0,
          "tolerance": {
            "abs": 1e-09,
            "rel": 0.0
          }
        },
        {
          "variable": "melt_potential",
          "time": 0.0,
          "expected": 1.0,
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
