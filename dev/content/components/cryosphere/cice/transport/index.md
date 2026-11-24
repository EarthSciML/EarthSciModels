---
title: "Transport"
slug: "transport"
domains: ["cryosphere"]
component_types: ["model"]
subdomains: ["cice"]
domain: "cryosphere"
subdomain: "cice"
component_type: "model"
esm_version: "2.0.0"
esm_path: "components/cryosphere/cice/cice_transport.esm"
reference: "Hunke, E. C., Allard, R., Bailey, D. A., Blain, P., Craig, A., Dupont, F., ... & Roberts, A. F. (2023). CICE-Consortium Icepack v1.2.4 and CICE v6.3.22: documentation and user's guide. Los Alamos National Laboratory (LA-UR-23-31851)."
description: "CICE horizontal transport (stage 2 of the EqESM project): the per-category conservative advection of the area, volume and enthalpy/surface-temperature tracer states of the default configuration of cesm3_cice6_6_3_22, lowered onto the traced 3x5 subdomain (N_I = 3 T cells along x, N_J = 5 along y, global cells (2..4, 4..8) of the stage-1 dump) with the EarthSciDiscretizations CICE B-grid flux-divergence rules (grids/cice_bgrid/rules/transport_flux_divergence.esm and its layered companion transport_flux_divergence_layered.esm). The conservative statement per category n is the continuity system d(aicen)/dt + div(aicen*u) = 0, d(vicen)/dt + div(vicen*u) = 0, d(vsnon)/dt + div(vsnon*u) = 0, plus the tracer-product forms the Fortran conserves (update_fields, ice_transport_remap.F90:3556-3571; tracer types of ice_init.F90:3061-3067): d(aTsfcn)/dt + div(aTsfcn*u) = 0 for the area tracer Tsfcn (trcr_depend = 0), d(vqicen)/dt + div(vqicen*u) = 0 for the volume tracer qicen over the 8 ice layers (trcr_depend = 1, vqicen = vicen*qicen), and d(vsqsnon)/dt + div(vsqsnon*u) = 0 for the snow-volume tracer qsnon over the 3 snow layers (trcr_depend = 2, vsqsnon = vsnon*qsnon). The tracers are recovered by tracer_from_product (cice_templates.esm): Tsfcn = aTsfcn/aicen, qicen_adv = vqicen/vicen, qsnon_adv = vsqsnon/vsnon, floored where the transported mass vanishes exactly as the Fortran's update_fields/tracers_to_state (0 for Tsfc and qice, -rhos*Lfresh for qsno; ice_transport_remap.F90:3631-3658, ice_transport_driver.F90:990-1114). Every divergence is the spatial-D rewrite target D(c*uvel, x) + D(c*vvel, y) (the tracer_flux_divergence template), lowered by the rule to the conservative cell flux divergence (F_e(i,j) - F_e(i-1,j) + F_n(i,j) - F_n(i,j-1))/tarea of the Fortran's mass update (ice_transport_remap.F90:3586-3590) with the CENTERED face reconstruction F_e = HTE*((uS+uN)/2)*((cL+cR)/2), F_n = HTN*((vW+vE)/2)*((cS+cN)/2); the layered rule applies the same stencil on the passive layer axis (imported twice, layer renamed to ice_layer / snow_layer with N_LAYER bound to N_ILYR / N_SLYR). THIS IS NOT CICE'S INCREMENTAL REMAPPING. The Fortran advects with the incremental-remapping scheme of Dukowicz & Baumgardner (2000) / Lipscomb & Hunke (2004) (horizontal_remap, ice_transport_remap.F90:317-831: limited linear reconstruction construct_fields F90:1009-1283, departure_points F90:1449-1623, departure-region integrals transport_integrals F90:3188-3472), which is upwind-biased, monotone for the tracers and positivity-preserving for the masses. The centered flux divergence here is the continuous flux form of the same conservation law: it is conservative but neither upwind nor limited, so it carries NO positivity or monotonicity guarantee -- an integration can drive aicen/vicen/vsnon negative or create tracer extrema near sharp ice edges, and the tracer recovery floors only the exactly-zero-mass case. No upwind or limited face rule exists for the cice_bgrid grid in EarthSciDiscretizations (the upwind/limiter rules there are for the 1-D Cartesian grids only), and incremental remapping itself is a stage-3 discretization (see README.md 'Transport scheme'). The integrated test cice_transport_centered_flux_35_integrated quantifies the scheme difference against the dump at a single interior cell (residuals ~10% of the transported change, tolerances rel 1e-4/1e-4/2e-4); the measured worst-case scheme residuals of the model against the dump t_exit over the whole traced domain are aicen 4.0e-4, vicen 3.7e-4, vsnon 4.8e-4, Tsfcn 2.2e-3, qicen 2.1e-4, qsnon 9.9e-6 relative (each above one tenth of the field's transported change, so the other tests pin the operator itself, not the trajectory: the uniform-field and divergence pins evaluate the lowered rule exactly, rel 1e-12, and the uniform-tracer preservation test checks the advection-consistency property of the product/recovery formulation). The velocity and grid fields are parameters overridden from the dumps in the tests: uvel/vvel are the transport dump's t_entr step-1 ncat-1 rows (the cell (i,j) row carries the U(i,j) NE-corner velocity = the post-dynamics field), HTE/HTN/tarea are derived from the stress-dump metrics (HTE = (3*cyp - cym)/4, HTN = (3*cxp - cxm)/4, tarea = dxT*dyT; ice_dyn_shared.F90:432-436). Import contract: the model declares the N_I/N_J/NCAT/N_ILYR/N_SLYR metaparameters and the i/j/ncat/ice_layer/snow_layer index sets locally (a workaround for the esm CLI RangeSpec round-trip bug with faq-range metaparameter references under template-import bindings), and imports the rules by reference from ${ESD_ROOT} (an EarthSciDiscretizations checkout at main, which carries both cice_bgrid transport rules since PR #50 / #59). Assembly: the recovered states are named qicen_adv/qsnon_adv because the esm CLI's initial-conditions shape check resolves an override key's trailing local name against the first declaring model, so a Transport state named qicen would shadow Thermodynamics.qicen in the cice.esm assembly test. The thermodynamics -> transport enthalpy hand-off (initializing vqicen = vicen*qicen from the post-thermodynamics state each step, the Fortran's state_to_tracers) is an operator-splitting sequencing step the single-period assembly cannot express, so cice.esm does not wire Thermodynamics.qicen/qsnon into this model; the tests set the product states by initial_conditions."
tags: ["cryosphere", "cice", "model", "sea-ice", "transport", "advection", "cesm", "tracers"]
---

## Description

CICE horizontal transport (stage 2 of the EqESM project): the per-category conservative advection of the area, volume and enthalpy/surface-temperature tracer states of the default configuration of cesm3_cice6_6_3_22, lowered onto the traced 3x5 subdomain (N_I = 3 T cells along x, N_J = 5 along y, global cells (2..4, 4..8) of the stage-1 dump) with the EarthSciDiscretizations CICE B-grid flux-divergence rules (grids/cice_bgrid/rules/transport_flux_divergence.esm and its layered companion transport_flux_divergence_layered.esm). The conservative statement per category n is the continuity system d(aicen)/dt + div(aicen*u) = 0, d(vicen)/dt + div(vicen*u) = 0, d(vsnon)/dt + div(vsnon*u) = 0, plus the tracer-product forms the Fortran conserves (update_fields, ice_transport_remap.F90:3556-3571; tracer types of ice_init.F90:3061-3067): d(aTsfcn)/dt + div(aTsfcn*u) = 0 for the area tracer Tsfcn (trcr_depend = 0), d(vqicen)/dt + div(vqicen*u) = 0 for the volume tracer qicen over the 8 ice layers (trcr_depend = 1, vqicen = vicen*qicen), and d(vsqsnon)/dt + div(vsqsnon*u) = 0 for the snow-volume tracer qsnon over the 3 snow layers (trcr_depend = 2, vsqsnon = vsnon*qsnon). The tracers are recovered by tracer_from_product (cice_templates.esm): Tsfcn = aTsfcn/aicen, qicen_adv = vqicen/vicen, qsnon_adv = vsqsnon/vsnon, floored where the transported mass vanishes exactly as the Fortran's update_fields/tracers_to_state (0 for Tsfc and qice, -rhos*Lfresh for qsno; ice_transport_remap.F90:3631-3658, ice_transport_driver.F90:990-1114). Every divergence is the spatial-D rewrite target D(c*uvel, x) + D(c*vvel, y) (the tracer_flux_divergence template), lowered by the rule to the conservative cell flux divergence (F_e(i,j) - F_e(i-1,j) + F_n(i,j) - F_n(i,j-1))/tarea of the Fortran's mass update (ice_transport_remap.F90:3586-3590) with the CENTERED face reconstruction F_e = HTE*((uS+uN)/2)*((cL+cR)/2), F_n = HTN*((vW+vE)/2)*((cS+cN)/2); the layered rule applies the same stencil on the passive layer axis (imported twice, layer renamed to ice_layer / snow_layer with N_LAYER bound to N_ILYR / N_SLYR). THIS IS NOT CICE'S INCREMENTAL REMAPPING. The Fortran advects with the incremental-remapping scheme of Dukowicz & Baumgardner (2000) / Lipscomb & Hunke (2004) (horizontal_remap, ice_transport_remap.F90:317-831: limited linear reconstruction construct_fields F90:1009-1283, departure_points F90:1449-1623, departure-region integrals transport_integrals F90:3188-3472), which is upwind-biased, monotone for the tracers and positivity-preserving for the masses. The centered flux divergence here is the continuous flux form of the same conservation law: it is conservative but neither upwind nor limited, so it carries NO positivity or monotonicity guarantee -- an integration can drive aicen/vicen/vsnon negative or create tracer extrema near sharp ice edges, and the tracer recovery floors only the exactly-zero-mass case. No upwind or limited face rule exists for the cice_bgrid grid in EarthSciDiscretizations (the upwind/limiter rules there are for the 1-D Cartesian grids only), and incremental remapping itself is a stage-3 discretization (see README.md 'Transport scheme'). The integrated test cice_transport_centered_flux_35_integrated quantifies the scheme difference against the dump at a single interior cell (residuals ~10% of the transported change, tolerances rel 1e-4/1e-4/2e-4); the measured worst-case scheme residuals of the model against the dump t_exit over the whole traced domain are aicen 4.0e-4, vicen 3.7e-4, vsnon 4.8e-4, Tsfcn 2.2e-3, qicen 2.1e-4, qsnon 9.9e-6 relative (each above one tenth of the field's transported change, so the other tests pin the operator itself, not the trajectory: the uniform-field and divergence pins evaluate the lowered rule exactly, rel 1e-12, and the uniform-tracer preservation test checks the advection-consistency property of the product/recovery formulation). The velocity and grid fields are parameters overridden from the dumps in the tests: uvel/vvel are the transport dump's t_entr step-1 ncat-1 rows (the cell (i,j) row carries the U(i,j) NE-corner velocity = the post-dynamics field), HTE/HTN/tarea are derived from the stress-dump metrics (HTE = (3*cyp - cym)/4, HTN = (3*cxp - cxm)/4, tarea = dxT*dyT; ice_dyn_shared.F90:432-436). Import contract: the model declares the N_I/N_J/NCAT/N_ILYR/N_SLYR metaparameters and the i/j/ncat/ice_layer/snow_layer index sets locally (a workaround for the esm CLI RangeSpec round-trip bug with faq-range metaparameter references under template-import bindings), and imports the rules by reference from ${ESD_ROOT} (an EarthSciDiscretizations checkout at main, which carries both cice_bgrid transport rules since PR #50 / #59). Assembly: the recovered states are named qicen_adv/qsnon_adv because the esm CLI's initial-conditions shape check resolves an override key's trailing local name against the first declaring model, so a Transport state named qicen would shadow Thermodynamics.qicen in the cice.esm assembly test. The thermodynamics -> transport enthalpy hand-off (initializing vqicen = vicen*qicen from the post-thermodynamics state each step, the Fortran's state_to_tracers) is an operator-splitting sequencing step the single-period assembly cannot express, so cice.esm does not wire Thermodynamics.qicen/qsnon into this model; the tests set the product states by initial_conditions.

## Reference

- Hunke, E. C., Allard, R., Bailey, D. A., Blain, P., Craig, A., Dupont, F., ... & Roberts, A. F. (2023). CICE-Consortium Icepack v1.2.4 and CICE v6.3.22: documentation and user's guide. Los Alamos National Laboratory (LA-UR-23-31851).
- Dukowicz, J. K., & Baumgardner, J. R. (2000). Incremental remapping as a transport/advection algorithm. Journal of Computational Physics, 160(1), 318-335.
- Lipscomb, W. H., & Hunke, E. C. (2004). Modeling sea ice transport using incremental remapping. Monthly Weather Review, 132(6), 1341-1354.
- CESM (Community Earth System Model), ESCOMP/CESM: CICE sea-ice source (cesm3_cice6_6_3_22) - ice_transport_driver.F90, ice_transport_remap.F90 - the reference implementation these components are transcribed from.
- EarthSciModels - the authoritative .esm corpus this component lives in.

## Variables

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `aicen` | `1` | `0.0` | ice area fraction per category, the transported area state: d(aicen)/dt + div(aicen*u) = 0 (the Fortran 'mass' field mm of horizontal_remap, ice_transport_remap.F90:279-280, including category 0 open water), [-] |
| `vicen` | `m` | `0.0` | ice volume per unit grid-cell area per category vicen = aicen*hin, the transported volume state: d(vicen)/dt + div(vicen*u) = 0, [m] |
| `vsnon` | `m` | `0.0` | snow volume per unit grid-cell area per category vsnon = aicen*hsn, the transported snow-volume state: d(vsnon)/dt + div(vsnon*u) = 0, [m] |
| `aTsfcn` | `degC` | `0.0` | the transported area-tracer product aicen*Tsfcn: the works-array entry of the Tsfc tracer (trcr_depend = 0, ice_transport_driver.F90:1579-1583), advected by the conservative form d(aTsfcn)/dt + div(aTsfcn*u) = 0 (the Fortran's type-1 tracer transport conserves mass*tracer with mass = aicen, update_fields ice_transport_remap.F90:3636-3644), [degC] |
| `vqicen` | `J/m^2` | `0.0` | the transported ice-layer enthalpy product vicen*qicen over the passive layer axis (the works-array entries of the enthalpy tracer, trcr_depend = 1, ice_transport_driver.F90:1585-1589; the per-layer formulation carried the 8 unknowns vqicen_1..8, the layered transport rule transport_flux_divergence_layered collapses them to this one 4-D unknown), advected by d(vqicen)/dt + div(vqicen*u) = 0 (the Fortran's type-2 tracer transport conserves mass*tracer with mass = vicen = aicen*hice, update_fields ice_transport_remap.F90:3645-3653), [J/m2] |
| `vsqsnon` | `J/m^2` | `0.0` | the transported snow-layer enthalpy product vsnon*qsnon over the passive layer axis (trcr_depend = 2, ice_transport_driver.F90:1590-1594; the Fortran transports qsnon + rhos*Lfresh, state_to_tracers F90:990-995, a constant offset that exactly cancels in the conservation law; the per-layer formulation's vsqsnon_1..3), advected by d(vsqsnon)/dt + div(vsqsnon*u) = 0, [J/m2] |

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `uvel` | `m/s` | `0.0` | x-component of the ice velocity at the B-grid corner points (the transport dump's t_entr step-1 ncat-1 rows: the cell (i,j) row carries the U(i,j) NE-corner velocity = the post-dynamics field, wired from the dynamics component in the assembly), [m/s] |
| `vvel` | `m/s` | `0.0` | y-component of the ice velocity at the B-grid corner points (wired from the dynamics component), [m/s] |
| `HTE` | `m` | `0.0` | east edge length of the T cell, derived from the stress-dump metrics as HTE = (3*cyp - cym)/4 (the free-name metric of the transport_flux_divergence rule; the tests override it from the dump), [m] |
| `HTN` | `m` | `0.0` | north edge length of the T cell, HTN = (3*cxp - cxm)/4, [m] |
| `tarea` | `m^2` | `0.0` | area of the T cell, tarea = dxT*dyT (ice_grid.F90:682; the tests override it from the dump), [m2] |
| `rhos` | `kg/m^3` | `330.0` | snow density (icepack_parameters.F90:61; the nuopc cap does not override it, bugs.md #11), the density of the snow-enthalpy reference rhos*Lfresh of the qsnon tracer, [kg/m3] |
| `Lfresh` | `J/kg` | `333700.0` | latent heat of fusion of fresh water (Lfresh = Lsub - Lvap with the nuopc-cap overridden Lsub = 2834700 and Lvap = 2501000 J/kg, ice_comp_nuopc.F90:415-450; bugs.md #11), the reference-enthalpy factor of the snow tracer, [J/kg] |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `div_flux` | `1/s` | `0.0` | the conservative per-category flux divergence div_flux = D(c*uvel,x) + D(c*vvel,y) lowered by the transport_flux_divergence rule (the continuous flux form the incremental-remapping scheme replaces; ice_transport_remap.F90:658-666, 3586-3590), the algebraic rewrite target the continuity equations consume, [1/s] |
| `div_flux_v` | `m/s` | `0.0` | the conservative ice-volume-flux divergence D(vicen*uvel,x) + D(vicen*vvel,y) (the rule target of the vicen continuity equation), [m/s] |
| `div_flux_s` | `m/s` | `0.0` | the conservative snow-volume-flux divergence D(vsnon*uvel,x) + D(vsnon*vvel,y) (the rule target of the vsnon continuity equation), [m/s] |
| `Tsfcn` | `degC` | `0.0` | the ice surface temperature tracer recovered from the transported product by the tracers_to_state division Tsfcn = aTsfcn/aicen (the Fortran's trcrn after the remap, tracers_to_state F90:1060-1070), [degC] |
| `qsno_ref_enthalpy` | `J/m^3` | `0.0` | the snow-enthalpy reference rhos*Lfresh of the qsnon tracer, the constant offset the Fortran adds when loading the qsno tracers for transport (state_to_tracers, ice_transport_driver.F90:990-995) and the floor of the qsnon recovery where the transported snow volume vanishes (the qsnon fallback of update_fields, ice_transport_remap.F90:3655-3658; the dump column qsno_k reads exactly -rhos*Lfresh = -110121000 J/m3 at snow-free cells), the named intermediate of the tracer_from_product applications, [J/m3] |
| `div_aTsfcn` | `degC/s` | `0.0` | the per-category flux divergence of the transported area-tracer product aTsfcn = aicen*Tsfcn, D(aTsfcn*uvel,x) + D(aTsfcn*vvel,y) lowered by the tracer_flux_divergence template, the algebraic rewrite target of d(aTsfcn)/dt = -div_aTsfcn; the cice_transport_tracers_divergence_pins test asserts it at time 0 against the rule formula of the dumped state, [degC/s] |
| `div_vqicen` | `J/m^2/s` | `0.0` | the per-category per-layer flux divergence of the transported volume-tracer product vqicen = vicen*qicen over the passive layer axis, D(vqicen*uvel,x) + D(vqicen*vvel,y) lowered by the layered transport rule transport_flux_divergence_layered (the same edge fluxes/areas apply at every layer, so the rule tiles the per-layer stencil of the per-layer formulation's div_vqicen_k), the algebraic rewrite target of d(vqicen)/dt = -div_vqicen; the cice_transport_tracers_divergence_pins test asserts it at time 0 against the rule formula of the dumped state, [J/m2/s] |
| `div_vsqsnon` | `J/m^2/s` | `0.0` | the per-category per-layer flux divergence of the transported snow-volume-tracer product vsqsnon = vsnon*qsnon over the passive layer axis, D(vsqsnon*uvel,x) + D(vsqsnon*vvel,y) lowered by the layered transport rule transport_flux_divergence_layered (the per-layer formulation's div_vsqsnon_k), the algebraic rewrite target of d(vsqsnon)/dt = -div_vsqsnon; the cice_transport_tracers_divergence_pins test asserts it at time 0 against the rule formula of the dumped state, [J/m2/s] |
| `qicen_adv` | `J/m^3` | `0.0` | the advected mushy ice-layer enthalpy tracer recovered from the transported product by qicen_adv = vqicen/vicen over the passive layer axis (tracers_to_state F90:1060-1070; the dump column qice_k of the per-layer formulation; the _adv suffix avoids shadowing Thermodynamics.qicen in the cice.esm assembly test, whose initial-conditions shape check resolves an override key's trailing local name against the first declaring model), [J/m3] |
| `qsnon_adv` | `J/m^3` | `0.0` | the advected snow-layer enthalpy tracer recovered from the transported product by qsnon_adv = vsqsnon/vsnon over the passive layer axis, floored at the reference enthalpy -rhos*Lfresh where the transported snow volume vanishes (tracers_to_state F90:1060-1070 with the rhos*Lfresh reference of F90:994; the Fortran leaves the tracer stale where vsnon = 0, update_fields F90:3655-3658; the dump column qsno_k reads exactly -rhos*Lfresh at snow-free cells), [J/m3] |

## Observed expressions

$$
div_{flux} = \mathrm{tracer_flux_divergence}\left(c=aicen, u=uvel, v=vvel\right)
$$
_the conservative per-category flux divergence div_flux = D(c*uvel,x) + D(c*vvel,y) lowered by the transport_flux_divergence rule (the continuous flux form the incremental-remapping scheme replaces; ice_transport_remap.F90:658-666, 3586-3590), the algebraic rewrite target the continuity equations consume, [1/s]_

$$
div_{flux\,v} = \mathrm{tracer_flux_divergence}\left(c=vicen, u=uvel, v=vvel\right)
$$
_the conservative ice-volume-flux divergence D(vicen*uvel,x) + D(vicen*vvel,y) (the rule target of the vicen continuity equation), [m/s]_

$$
div_{flux\,s} = \mathrm{tracer_flux_divergence}\left(c=vsnon, u=uvel, v=vvel\right)
$$
_the conservative snow-volume-flux divergence D(vsnon*uvel,x) + D(vsnon*vvel,y) (the rule target of the vsnon continuity equation), [m/s]_

$$
Tsfcn = \mathrm{tracer_from_product}\left(product=aTsfcn, mass=aicen, floor=\mathrm{const}\left(\right)\right)
$$
_the ice surface temperature tracer recovered from the transported product by the tracers_to_state division Tsfcn = aTsfcn/aicen (the Fortran's trcrn after the remap, tracers_to_state F90:1060-1070), [degC]_

$$
qsno_{ref\,enthalpy} = -rhos \cdot Lfresh
$$
_the snow-enthalpy reference rhos*Lfresh of the qsnon tracer, the constant offset the Fortran adds when loading the qsno tracers for transport (state_to_tracers, ice_transport_driver.F90:990-995) and the floor of the qsnon recovery where the transported snow volume vanishes (the qsnon fallback of update_fields, ice_transport_remap.F90:3655-3658; the dump column qsno_k reads exactly -rhos*Lfresh = -110121000 J/m3 at snow-free cells), the named intermediate of the tracer_from_product applications, [J/m3]_

$$
div_{aTsfcn} = \mathrm{tracer_flux_divergence}\left(c=aTsfcn, u=uvel, v=vvel\right)
$$
_the per-category flux divergence of the transported area-tracer product aTsfcn = aicen*Tsfcn, D(aTsfcn*uvel,x) + D(aTsfcn*vvel,y) lowered by the tracer_flux_divergence template, the algebraic rewrite target of d(aTsfcn)/dt = -div_aTsfcn; the cice_transport_tracers_divergence_pins test asserts it at time 0 against the rule formula of the dumped state, [degC/s]_

$$
div_{vqicen} = \mathrm{tracer_flux_divergence}\left(c=vqicen, u=uvel, v=vvel\right)
$$
_the per-category per-layer flux divergence of the transported volume-tracer product vqicen = vicen*qicen over the passive layer axis, D(vqicen*uvel,x) + D(vqicen*vvel,y) lowered by the layered transport rule transport_flux_divergence_layered (the same edge fluxes/areas apply at every layer, so the rule tiles the per-layer stencil of the per-layer formulation's div_vqicen_k), the algebraic rewrite target of d(vqicen)/dt = -div_vqicen; the cice_transport_tracers_divergence_pins test asserts it at time 0 against the rule formula of the dumped state, [J/m2/s]_

$$
div_{vsqsnon} = \mathrm{tracer_flux_divergence}\left(c=vsqsnon, u=uvel, v=vvel\right)
$$
_the per-category per-layer flux divergence of the transported snow-volume-tracer product vsqsnon = vsnon*qsnon over the passive layer axis, D(vsqsnon*uvel,x) + D(vsqsnon*vvel,y) lowered by the layered transport rule transport_flux_divergence_layered (the per-layer formulation's div_vsqsnon_k), the algebraic rewrite target of d(vsqsnon)/dt = -div_vsqsnon; the cice_transport_tracers_divergence_pins test asserts it at time 0 against the rule formula of the dumped state, [J/m2/s]_

$$
qicen_{adv} = \mathrm{tracer_from_product}\left(product=vqicen, mass=vicen, floor=\mathrm{const}\left(\right)\right)
$$
_the advected mushy ice-layer enthalpy tracer recovered from the transported product by qicen_adv = vqicen/vicen over the passive layer axis (tracers_to_state F90:1060-1070; the dump column qice_k of the per-layer formulation; the _adv suffix avoids shadowing Thermodynamics.qicen in the cice.esm assembly test, whose initial-conditions shape check resolves an override key's trailing local name against the first declaring model), [J/m3]_

$$
qsnon_{adv} = \mathrm{tracer_from_product}\left(product=vsqsnon, mass=vsnon, floor=qsno_{ref\,enthalpy}\right)
$$
_the advected snow-layer enthalpy tracer recovered from the transported product by qsnon_adv = vsqsnon/vsnon over the passive layer axis, floored at the reference enthalpy -rhos*Lfresh where the transported snow volume vanishes (tracers_to_state F90:1060-1070 with the rhos*Lfresh reference of F90:994; the Fortran leaves the tracer stale where vsnon = 0, update_fields F90:3655-3658; the dump column qsno_k reads exactly -rhos*Lfresh at snow-free cells), [J/m3]_

## Equations

$$
\mathrm{D}\left(aicen\right) = -div_{flux}
$$

$$
\mathrm{D}\left(vicen\right) = -div_{flux\,v}
$$

$$
\mathrm{D}\left(vsnon\right) = -div_{flux\,s}
$$

$$
\mathrm{D}\left(aTsfcn\right) = -div_{aTsfcn}
$$

$$
\mathrm{D}\left(vqicen\right) = -div_{vqicen}
$$

$$
\mathrm{D}\left(vsqsnon\right) = -div_{vsqsnon}
$$

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "expression_template_imports": [
    {
      "ref": "${ESD_ROOT}/grids/cice_bgrid/rules/transport_flux_divergence.esm"
    },
    {
      "ref": "${ESD_ROOT}/grids/cice_bgrid/rules/transport_flux_divergence_layered.esm",
      "bindings": {
        "N_LAYER": "N_ILYR"
      },
      "rename": {
        "layer": "ice_layer",
        "transport_flux_divergence_layered": "transport_flux_divergence_layered_ice"
      }
    },
    {
      "ref": "${ESD_ROOT}/grids/cice_bgrid/rules/transport_flux_divergence_layered.esm",
      "bindings": {
        "N_LAYER": "N_SLYR"
      },
      "rename": {
        "layer": "snow_layer",
        "transport_flux_divergence_layered": "transport_flux_divergence_layered_snow"
      }
    },
    {
      "ref": "./cice_templates.esm"
    }
  ],
  "variables": {
    "aicen": {
      "type": "unknown",
      "shape": [
        "i",
        "j",
        "ncat"
      ],
      "units": "1",
      "default": 0.0,
      "description": "ice area fraction per category, the transported area state: d(aicen)/dt + div(aicen*u) = 0 (the Fortran 'mass' field mm of horizontal_remap, ice_transport_remap.F90:279-280, including category 0 open water), [-]"
    },
    "vicen": {
      "type": "unknown",
      "shape": [
        "i",
        "j",
        "ncat"
      ],
      "units": "m",
      "default": 0.0,
      "description": "ice volume per unit grid-cell area per category vicen = aicen*hin, the transported volume state: d(vicen)/dt + div(vicen*u) = 0, [m]"
    },
    "vsnon": {
      "type": "unknown",
      "shape": [
        "i",
        "j",
        "ncat"
      ],
      "units": "m",
      "default": 0.0,
      "description": "snow volume per unit grid-cell area per category vsnon = aicen*hsn, the transported snow-volume state: d(vsnon)/dt + div(vsnon*u) = 0, [m]"
    },
    "div_flux": {
      "type": "unknown",
      "shape": [
        "i",
        "j",
        "ncat"
      ],
      "units": "1/s",
      "default": 0.0,
      "description": "the conservative per-category flux divergence div_flux = D(c*uvel,x) + D(c*vvel,y) lowered by the transport_flux_divergence rule (the continuous flux form the incremental-remapping scheme replaces; ice_transport_remap.F90:658-666, 3586-3590), the algebraic rewrite target the continuity equations consume, [1/s]"
    },
    "div_flux_v": {
      "type": "unknown",
      "shape": [
        "i",
        "j",
        "ncat"
      ],
      "units": "m/s",
      "default": 0.0,
      "description": "the conservative ice-volume-flux divergence D(vicen*uvel,x) + D(vicen*vvel,y) (the rule target of the vicen continuity equation), [m/s]"
    },
    "div_flux_s": {
      "type": "unknown",
      "shape": [
        "i",
        "j",
        "ncat"
      ],
      "units": "m/s",
      "default": 0.0,
      "description": "the conservative snow-volume-flux divergence D(vsnon*uvel,x) + D(vsnon*vvel,y) (the rule target of the vsnon continuity equation), [m/s]"
    },
    "uvel": {
      "type": "parameter",
      "shape": [
        "i",
        "j"
      ],
      "units": "m/s",
      "default": 0.0,
      "description": "x-component of the ice velocity at the B-grid corner points (the transport dump's t_entr step-1 ncat-1 rows: the cell (i,j) row carries the U(i,j) NE-corner velocity = the post-dynamics field, wired from the dynamics component in the assembly), [m/s]"
    },
    "vvel": {
      "type": "parameter",
      "shape": [
        "i",
        "j"
      ],
      "units": "m/s",
      "default": 0.0,
      "description": "y-component of the ice velocity at the B-grid corner points (wired from the dynamics component), [m/s]"
    },
    "HTE": {
      "type": "parameter",
      "shape": [
        "i",
        "j"
      ],
      "units": "m",
      "default": 0.0,
      "description": "east edge length of the T cell, derived from the stress-dump metrics as HTE = (3*cyp - cym)/4 (the free-name metric of the transport_flux_divergence rule; the tests override it from the dump), [m]"
    },
    "HTN": {
      "type": "parameter",
      "shape": [
        "i",
        "j"
      ],
      "units": "m",
      "default": 0.0,
      "description": "north edge length of the T cell, HTN = (3*cxp - cxm)/4, [m]"
    },
    "tarea": {
      "type": "parameter",
      "shape": [
        "i",
        "j"
      ],
      "units": "m^2",
      "default": 0.0,
      "description": "area of the T cell, tarea = dxT*dyT (ice_grid.F90:682; the tests override it from the dump), [m2]"
    },
    "rhos": {
      "type": "parameter",
      "units": "kg/m^3",
      "default": 330.0,
      "description": "snow density (icepack_parameters.F90:61; the nuopc cap does not override it, bugs.md #11), the density of the snow-enthalpy reference rhos*Lfresh of the qsnon tracer, [kg/m3]"
    },
    "Lfresh": {
      "type": "parameter",
      "units": "J/kg",
      "default": 333700.0,
      "description": "latent heat of fusion of fresh water (Lfresh = Lsub - Lvap with the nuopc-cap overridden Lsub = 2834700 and Lvap = 2501000 J/kg, ice_comp_nuopc.F90:415-450; bugs.md #11), the reference-enthalpy factor of the snow tracer, [J/kg]"
    },
    "aTsfcn": {
      "type": "unknown",
      "shape": [
        "i",
        "j",
        "ncat"
      ],
      "units": "degC",
      "default": 0.0,
      "description": "the transported area-tracer product aicen*Tsfcn: the works-array entry of the Tsfc tracer (trcr_depend = 0, ice_transport_driver.F90:1579-1583), advected by the conservative form d(aTsfcn)/dt + div(aTsfcn*u) = 0 (the Fortran's type-1 tracer transport conserves mass*tracer with mass = aicen, update_fields ice_transport_remap.F90:3636-3644), [degC]"
    },
    "vqicen": {
      "type": "unknown",
      "shape": [
        "i",
        "j",
        "ncat",
        "ice_layer"
      ],
      "units": "J/m^2",
      "default": 0.0,
      "description": "the transported ice-layer enthalpy product vicen*qicen over the passive layer axis (the works-array entries of the enthalpy tracer, trcr_depend = 1, ice_transport_driver.F90:1585-1589; the per-layer formulation carried the 8 unknowns vqicen_1..8, the layered transport rule transport_flux_divergence_layered collapses them to this one 4-D unknown), advected by d(vqicen)/dt + div(vqicen*u) = 0 (the Fortran's type-2 tracer transport conserves mass*tracer with mass = vicen = aicen*hice, update_fields ice_transport_remap.F90:3645-3653), [J/m2]"
    },
    "vsqsnon": {
      "type": "unknown",
      "shape": [
        "i",
        "j",
        "ncat",
        "snow_layer"
      ],
      "units": "J/m^2",
      "default": 0.0,
      "description": "the transported snow-layer enthalpy product vsnon*qsnon over the passive layer axis (trcr_depend = 2, ice_transport_driver.F90:1590-1594; the Fortran transports qsnon + rhos*Lfresh, state_to_tracers F90:990-995, a constant offset that exactly cancels in the conservation law; the per-layer formulation's vsqsnon_1..3), advected by d(vsqsnon)/dt + div(vsqsnon*u) = 0, [J/m2]"
    },
    "Tsfcn": {
      "type": "unknown",
      "shape": [
        "i",
        "j",
        "ncat"
      ],
      "units": "degC",
      "default": 0.0,
      "description": "the ice surface temperature tracer recovered from the transported product by the tracers_to_state division Tsfcn = aTsfcn/aicen (the Fortran's trcrn after the remap, tracers_to_state F90:1060-1070), [degC]"
    },
    "qsno_ref_enthalpy": {
      "type": "unknown",
      "units": "J/m^3",
      "default": 0.0,
      "description": "the snow-enthalpy reference rhos*Lfresh of the qsnon tracer, the constant offset the Fortran adds when loading the qsno tracers for transport (state_to_tracers, ice_transport_driver.F90:990-995) and the floor of the qsnon recovery where the transported snow volume vanishes (the qsnon fallback of update_fields, ice_transport_remap.F90:3655-3658; the dump column qsno_k reads exactly -rhos*Lfresh = -110121000 J/m3 at snow-free cells), the named intermediate of the tracer_from_product applications, [J/m3]"
    },
    "div_aTsfcn": {
      "type": "unknown",
      "shape": [
        "i",
        "j",
        "ncat"
      ],
      "units": "degC/s",
      "default": 0.0,
      "description": "the per-category flux divergence of the transported area-tracer product aTsfcn = aicen*Tsfcn, D(aTsfcn*uvel,x) + D(aTsfcn*vvel,y) lowered by the tracer_flux_divergence template, the algebraic rewrite target of d(aTsfcn)/dt = -div_aTsfcn; the cice_transport_tracers_divergence_pins test asserts it at time 0 against the rule formula of the dumped state, [degC/s]"
    },
    "div_vqicen": {
      "type": "unknown",
      "shape": [
        "i",
        "j",
        "ncat",
        "ice_layer"
      ],
      "units": "J/m^2/s",
      "default": 0.0,
      "description": "the per-category per-layer flux divergence of the transported volume-tracer product vqicen = vicen*qicen over the passive layer axis, D(vqicen*uvel,x) + D(vqicen*vvel,y) lowered by the layered transport rule transport_flux_divergence_layered (the same edge fluxes/areas apply at every layer, so the rule tiles the per-layer stencil of the per-layer formulation's div_vqicen_k), the algebraic rewrite target of d(vqicen)/dt = -div_vqicen; the cice_transport_tracers_divergence_pins test asserts it at time 0 against the rule formula of the dumped state, [J/m2/s]"
    },
    "div_vsqsnon": {
      "type": "unknown",
      "shape": [
        "i",
        "j",
        "ncat",
        "snow_layer"
      ],
      "units": "J/m^2/s",
      "default": 0.0,
      "description": "the per-category per-layer flux divergence of the transported snow-volume-tracer product vsqsnon = vsnon*qsnon over the passive layer axis, D(vsqsnon*uvel,x) + D(vsqsnon*vvel,y) lowered by the layered transport rule transport_flux_divergence_layered (the per-layer formulation's div_vsqsnon_k), the algebraic rewrite target of d(vsqsnon)/dt = -div_vsqsnon; the cice_transport_tracers_divergence_pins test asserts it at time 0 against the rule formula of the dumped state, [J/m2/s]"
    },
    "qicen_adv": {
      "type": "unknown",
      "shape": [
        "i",
        "j",
        "ncat",
        "ice_layer"
      ],
      "units": "J/m^3",
      "default": 0.0,
      "description": "the advected mushy ice-layer enthalpy tracer recovered from the transported product by qicen_adv = vqicen/vicen over the passive layer axis (tracers_to_state F90:1060-1070; the dump column qice_k of the per-layer formulation; the _adv suffix avoids shadowing Thermodynamics.qicen in the cice.esm assembly test, whose initial-conditions shape check resolves an override key's trailing local name against the first declaring model), [J/m3]"
    },
    "qsnon_adv": {
      "type": "unknown",
      "shape": [
        "i",
        "j",
        "ncat",
        "snow_layer"
      ],
      "units": "J/m^3",
      "default": 0.0,
      "description": "the advected snow-layer enthalpy tracer recovered from the transported product by qsnon_adv = vsqsnon/vsnon over the passive layer axis, floored at the reference enthalpy -rhos*Lfresh where the transported snow volume vanishes (tracers_to_state F90:1060-1070 with the rhos*Lfresh reference of F90:994; the Fortran leaves the tracer stale where vsnon = 0, update_fields F90:3655-3658; the dump column qsno_k reads exactly -rhos*Lfresh at snow-free cells), [J/m3]"
    }
  },
  "equations": [
    {
      "lhs": "div_flux",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "tracer_flux_divergence",
        "bindings": {
          "c": "aicen",
          "u": "uvel",
          "v": "vvel"
        }
      }
    },
    {
      "lhs": "div_flux_v",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "tracer_flux_divergence",
        "bindings": {
          "c": "vicen",
          "u": "uvel",
          "v": "vvel"
        }
      }
    },
    {
      "lhs": "div_flux_s",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "tracer_flux_divergence",
        "bindings": {
          "c": "vsnon",
          "u": "uvel",
          "v": "vvel"
        }
      }
    },
    {
      "lhs": {
        "op": "D",
        "args": [
          "aicen"
        ],
        "wrt": "t"
      },
      "rhs": {
        "op": "-",
        "args": [
          "div_flux"
        ]
      }
    },
    {
      "lhs": {
        "op": "D",
        "args": [
          "vicen"
        ],
        "wrt": "t"
      },
      "rhs": {
        "op": "-",
        "args": [
          "div_flux_v"
        ]
      }
    },
    {
      "lhs": {
        "op": "D",
        "args": [
          "vsnon"
        ],
        "wrt": "t"
      },
      "rhs": {
        "op": "-",
        "args": [
          "div_flux_s"
        ]
      }
    },
    {
      "lhs": "div_aTsfcn",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "tracer_flux_divergence",
        "bindings": {
          "c": "aTsfcn",
          "u": "uvel",
          "v": "vvel"
        }
      }
    },
    {
      "lhs": {
        "op": "D",
        "args": [
          "aTsfcn"
        ],
        "wrt": "t"
      },
      "rhs": {
        "op": "-",
        "args": [
          "div_aTsfcn"
        ]
      }
    },
    {
      "lhs": "Tsfcn",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "tracer_from_product",
        "bindings": {
          "product": "aTsfcn",
          "mass": "aicen",
          "floor": {
            "op": "const",
            "args": [],
            "value": 0.0,
            "units": "degC"
          }
        }
      }
    },
    {
      "lhs": "div_vqicen",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "tracer_flux_divergence",
        "bindings": {
          "c": "vqicen",
          "u": "uvel",
          "v": "vvel"
        }
      }
    },
    {
      "lhs": {
        "op": "D",
        "args": [
          "vqicen"
        ],
        "wrt": "t"
      },
      "rhs": {
        "op": "-",
        "args": [
          "div_vqicen"
        ]
      }
    },
    {
      "lhs": "qicen_adv",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "tracer_from_product",
        "bindings": {
          "product": "vqicen",
          "mass": "vicen",
          "floor": {
            "op": "const",
            "args": [],
            "value": 0.0,
            "units": "J/m^3"
          }
        }
      }
    },
    {
      "lhs": "div_vsqsnon",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "tracer_flux_divergence",
        "bindings": {
          "c": "vsqsnon",
          "u": "uvel",
          "v": "vvel"
        }
      }
    },
    {
      "lhs": {
        "op": "D",
        "args": [
          "vsqsnon"
        ],
        "wrt": "t"
      },
      "rhs": {
        "op": "-",
        "args": [
          "div_vsqsnon"
        ]
      }
    },
    {
      "lhs": "qsnon_adv",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "tracer_from_product",
        "bindings": {
          "product": "vsqsnon",
          "mass": "vsnon",
          "floor": "qsno_ref_enthalpy"
        }
      }
    },
    {
      "lhs": "qsno_ref_enthalpy",
      "rhs": {
        "op": "-",
        "args": [
          {
            "op": "*",
            "args": [
              "rhos",
              "Lfresh"
            ]
          }
        ]
      }
    }
  ],
  "tests": [
    {
      "assertions": [
        {
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 1
          },
          "expected": 1.1240071614720283e-07,
          "time": 0.0,
          "tolerance": {
            "abs": 0.0,
            "rel": 1e-12
          },
          "variable": "div_flux"
        }
      ],
      "description": "Instantaneous pin of the lowered flux divergence at global (3,7) = local (2,4) with a uniform field: with the initial aicen = 1 everywhere (full 3x5x5 array of ones; the CLI rejects scalar initial_conditions on shaped states) and the dump's velocity/grid parameters, the algebraic rewrite target div_flux = D(aicen*uvel,x) + D(aicen*vvel,y) reduces to the discrete velocity divergence D_vel = 1.1240071614720283e-07 1/s of the rule's centered reconstruction (the flux-form operator is linear in aicen, so the c = 1 field evaluates the velocity divergence exactly; asserted at time 0 with rel 1e-12, independent of the integrator). The dump's t_exit aicen at (3,7) differs from the continuous-limit 1 - D_vel*3600 = 0.99959535742187011 by the incremental-remap scheme difference (documented in README.md); this pin locks the lowered operator itself, independent of the remap scheme and of the integration solver (the earlier integrated form of this pin was solver-sensitive: the bdf integrator converges to the exponential exp(-D_vel*3600) = 0.9995954392786368, whose (D*dt)^2/2 = 8.2e-8 difference from the Euler form exceeds rel 1e-12).",
      "id": "cice_transport_uniform_field",
      "initial_conditions": {
        "aicen": [
          [
            [
              1.0,
              1.0,
              1.0,
              1.0,
              1.0
            ],
            [
              1.0,
              1.0,
              1.0,
              1.0,
              1.0
            ],
            [
              1.0,
              1.0,
              1.0,
              1.0,
              1.0
            ],
            [
              1.0,
              1.0,
              1.0,
              1.0,
              1.0
            ],
            [
              1.0,
              1.0,
              1.0,
              1.0,
              1.0
            ]
          ],
          [
            [
              1.0,
              1.0,
              1.0,
              1.0,
              1.0
            ],
            [
              1.0,
              1.0,
              1.0,
              1.0,
              1.0
            ],
            [
              1.0,
              1.0,
              1.0,
              1.0,
              1.0
            ],
            [
              1.0,
              1.0,
              1.0,
              1.0,
              1.0
            ],
            [
              1.0,
              1.0,
              1.0,
              1.0,
              1.0
            ]
          ],
          [
            [
              1.0,
              1.0,
              1.0,
              1.0,
              1.0
            ],
            [
              1.0,
              1.0,
              1.0,
              1.0,
              1.0
            ],
            [
              1.0,
              1.0,
              1.0,
              1.0,
              1.0
            ],
            [
              1.0,
              1.0,
              1.0,
              1.0,
              1.0
            ],
            [
              1.0,
              1.0,
              1.0,
              1.0,
              1.0
            ]
          ]
        ]
      },
      "parameter_overrides": {
        "HTE": [
          [
            59395.455016421605,
            59395.455016421605,
            59395.455016421605,
            59395.455016421605,
            59395.455016421605
          ],
          [
            59395.455016421605,
            59395.455016421605,
            59395.455016421605,
            59395.455016421605,
            59395.455016421605
          ],
          [
            59395.455016421605,
            59395.455016421605,
            59395.455016421605,
            59395.455016421605,
            59395.455016421605
          ]
        ],
        "HTN": [
          [
            26251.235254161526,
            27390.328313754686,
            28527.04003199235,
            29661.271582069905,
            30792.92435281096
          ],
          [
            26251.235254161526,
            27390.328313754686,
            28527.04003199235,
            29661.271582069905,
            30792.92435281096
          ],
          [
            26251.235254161526,
            27390.328313754686,
            28527.04003199235,
            29661.271582069905,
            30792.92435281096
          ]
        ],
        "tarea": [
          [
            1525307808.0270946,
            1593032537.954344,
            1660618768.108248,
            1728060622.4772792,
            1795352237.6020775
          ],
          [
            1525307808.0270946,
            1593032537.954344,
            1660618768.108248,
            1728060622.4772792,
            1795352237.6020775
          ],
          [
            1525307808.0270946,
            1593032537.954344,
            1660618768.108248,
            1728060622.4772792,
            1795352237.6020775
          ]
        ],
        "uvel": [
          [
            0.00012200831259922484,
            -0.00430503734325033,
            -0.006404552971129575,
            -0.0029079564379971357,
            -0.0037366886985347827
          ],
          [
            1.349728123413932e-05,
            -0.0049893802525858445,
            -0.006556908183432414,
            -0.004013004944111566,
            -0.0042590499452267415
          ],
          [
            0.0,
            -0.006049027918925767,
            -0.0058923320164812176,
            -0.0045391275967812655,
            -0.004738980872614332
          ]
        ],
        "vvel": [
          [
            0.0007204892821085377,
            0.0007865942006418693,
            0.0037168927343423233,
            0.013900356415145056,
            0.015928611364519916
          ],
          [
            0.0009977387642852074,
            0.001620845665338858,
            0.00661497866621736,
            0.011651221033965178,
            0.012191539845748306
          ],
          [
            0.0,
            0.003975027437344815,
            0.009118244672511678,
            0.01094051866825294,
            0.010805999470988786
          ]
        ]
      },
      "time_span": {
        "end": 0.0,
        "start": 0.0
      }
    },
    {
      "id": "cice_transport_tracers_uniform_preservation",
      "description": "Uniform-tracer preservation over [0, 3600] s: the mass fields of the dump's t_entr step-1 state are advected together with the product fields aTsfcn = T0*aicen (T0 = -2.0 degC), vqicen = q0*vicen and vsqsnon = s0*vsnon with the uniform per-layer tracer constants q0[ice_layer] = -(3.0e8 + (ice_layer-1)*1e7) J/m3 and s0[snow_layer] = -(1.1e8 + (snow_layer-1)*1e6) J/m3 stacked over the passive layer axis ('derived (not a dump column)' products of the uniform fields). Because every operator of the model is linear, the products stay exactly proportional to the masses along the whole trajectory, and the tracer_from_product recoveries Tsfcn = aTsfcn/aicen, qicen_adv = vqicen/vicen, qsnon_adv = vsqsnon/vsnon equal the constants to machine precision -- the assertions pin the recovered constants at t = 3600 with rel 1e-12 (independent of the integrator: the difference (product - s0*mass) has a zero initial condition and a zero right-hand side, so it stays zero along any trajectory; the constants are exactly representable doubles and the initial proportionality holds exactly). The 48 assertions are the few informative points of the review rule, not every index: the interior cell (2,4), the edge cell (2,5), the corner cell (1,1) and the snow-free floor cell (2,1), one category each -- the most-advected category of the cell (the largest |t_exit - t_entr| of aicen, from the state dump; at (2,1) category 1, the snow-free category). This is an operator-consistency test, not a comparison to CICE: because the expected values are constants, a model that transports nothing (e.g. zero velocities) also passes every assertion, so the test verifies that the advective transport operator preserves uniform tracer fields -- the discrete form of the advection-consistency requirement that a constant tracer advected by any velocity field stays constant. The qsnon assertions cover exactly the cells whose entry snow volume is nonzero (every cell except the snow-free (i,1) category-1 column, where vsnon = 0 and the recovery falls back to the reference enthalpy floor qsno_ref_enthalpy = -rhos*Lfresh instead of s0_k); the (2,1) category-1 qsnon pins assert that floor value -110121000 J/m3.",
      "time_span": {
        "start": 0.0,
        "end": 3600.0
      },
      "initial_conditions": {
        "aicen": [
          [
            [
              0.009853548870050664,
              0.012856324595003365,
              0.029676941490770437,
              0.16811440592585572,
              0.7737911360216866
            ],
            [
              0.19517590526067544,
              0.17517092814581073,
              0.20299967624466317,
              0.09250674814792506,
              0.12164352345239411
            ],
            [
              0.24010745627023652,
              0.2634716864755195,
              0.17913714386260754,
              0.06250924884224413,
              0.055099641785219235
            ],
            [
              0.24279805104338764,
              0.3006214819690576,
              0.16436715629707735,
              0.05921139667196378,
              0.051256324337174905
            ],
            [
              0.21446261957461704,
              0.3380275433857241,
              0.16112887904267895,
              0.06074578363509802,
              0.05272893334174682
            ]
          ],
          [
            [
              0.020000787893919705,
              0.018691298764765496,
              0.02123405723287625,
              0.2325823474953262,
              0.7062726776408558
            ],
            [
              0.1951085551827879,
              0.19103150780464098,
              0.19874511294878222,
              0.0852676614296998,
              0.10443105537326039
            ],
            [
              0.2665650105082223,
              0.2729606621507003,
              0.16782172397858613,
              0.05190504256475333,
              0.04559080814091524
            ],
            [
              0.2711227454925614,
              0.3055903706996223,
              0.1412717592470561,
              0.04939762562994809,
              0.040677317264858584
            ],
            [
              0.25048328256606534,
              0.3314283920301694,
              0.13476490615446873,
              0.05200182928019541,
              0.042383130922557063
            ]
          ],
          [
            [
              0.014548532518963476,
              0.014380833122369022,
              0.02220597912138724,
              0.1984707738728337,
              0.7493379585660391
            ],
            [
              0.19336284155326217,
              0.2162321165560872,
              0.2086988498366698,
              0.07229635067222134,
              0.08562040148508959
            ],
            [
              0.293731361151834,
              0.2767298787967303,
              0.15421663268947136,
              0.04716294309980759,
              0.04080758394240371
            ],
            [
              0.29902010258623624,
              0.297339158557214,
              0.11593803015640608,
              0.04344629470278152,
              0.035326077885262035
            ],
            [
              0.29693728359561494,
              0.3099293559893525,
              0.10537286140183962,
              0.044948070262977986,
              0.03608739625384745
            ]
          ]
        ],
        "vicen": [
          [
            [
              0.0033680184834617927,
              0.015542052227473355,
              0.06637765750622569,
              0.590810760871143,
              21.61213381468219
            ],
            [
              0.03492051855887914,
              0.1881462069722783,
              0.3803456398502473,
              0.32465543818502113,
              1.449938023658202
            ],
            [
              0.043483558783242754,
              0.27351867543189595,
              0.3192183512775029,
              0.21711473196953432,
              0.4267481976542756
            ],
            [
              0.04744904191254742,
              0.30927223432872736,
              0.28851115698570634,
              0.20480394767022725,
              0.3826462618653526
            ],
            [
              0.05151143940340013,
              0.3462557318196647,
              0.27725715110715127,
              0.2089216567907939,
              0.38686182855482437
            ]
          ],
          [
            [
              0.005398374149404335,
              0.02394414626491763,
              0.039941722338436514,
              0.9742070459848247,
              19.818005707722715
            ],
            [
              0.034089423501091495,
              0.20815847329100748,
              0.35599580221040084,
              0.3057541297880248,
              1.1667404164975148
            ],
            [
              0.049043930583768804,
              0.2794514836874194,
              0.2938193131598404,
              0.17852188658136484,
              0.34522466795247597
            ],
            [
              0.05587368765282823,
              0.3046830908131356,
              0.24501371039941883,
              0.16882628186138604,
              0.29618372127005743
            ],
            [
              0.06560408395072942,
              0.32609147007145284,
              0.23103593019886898,
              0.17724136576899244,
              0.30663221048100014
            ]
          ],
          [
            [
              0.003501282429120844,
              0.01786491306444554,
              0.04490947585209308,
              0.7286779809238466,
              18.89132406691435
            ],
            [
              0.03649673531868588,
              0.23309953928407742,
              0.3695943628273455,
              0.25387709158198946,
              0.8301563230719655
            ],
            [
              0.05636266355870376,
              0.27807881312680083,
              0.267696453134157,
              0.16166773031800252,
              0.3080507749868207
            ],
            [
              0.06850917717924364,
              0.28674649365747185,
              0.20070170993414216,
              0.14766212029151474,
              0.25643875495901225
            ],
            [
              0.08541943356949086,
              0.29183452966561274,
              0.18211636343675705,
              0.1525079186388313,
              0.26034930198917733
            ]
          ]
        ],
        "vsnon": [
          [
            [
              0.0,
              0.0019752994781107257,
              0.020421161467932235,
              0.18231500761877956,
              3.417817070425085
            ],
            [
              0.002558829070170628,
              0.04642591804295368,
              0.08453430208038736,
              0.053011609212643265,
              0.16052798613321836
            ],
            [
              0.005537052333306855,
              0.07730053090743055,
              0.06981963949185285,
              0.036078876638408676,
              0.05587080548511934
            ],
            [
              0.007358258103351589,
              0.09280017199343121,
              0.0685369544362089,
              0.03715553051049877,
              0.05313362931543603
            ],
            [
              0.01413057165211172,
              0.10680389967046192,
              0.0720580210125999,
              0.04204769642589584,
              0.05728570969849854
            ]
          ],
          [
            [
              0.0,
              0.0027949531841832964,
              0.007229022287709656,
              0.2822000858375975,
              3.004847428368811
            ],
            [
              0.0021453037964992293,
              0.05120365121132793,
              0.07438873060098469,
              0.04896831880001137,
              0.1384948923056299
            ],
            [
              0.006341674700852336,
              0.07948317298760875,
              0.06587530420013424,
              0.03022621513166698,
              0.045065380693348964
            ],
            [
              0.009790021264114329,
              0.09067365685552146,
              0.05976966142045742,
              0.03104546605099247,
              0.04118793098173599
            ],
            [
              0.018987800137287264,
              0.09718454331707943,
              0.060941236218567583,
              0.035454220890101966,
              0.044936863252113435
            ]
          ],
          [
            [
              0.0,
              0.0028994981145980024,
              0.013945776317644876,
              0.22736282514148398,
              3.516254903372643
            ],
            [
              0.00321822271152046,
              0.059757732239091546,
              0.08167056070309638,
              0.04051320512716417,
              0.10489156378478834
            ],
            [
              0.008168142483340798,
              0.07720906990349308,
              0.058888232679579024,
              0.027111166918299907,
              0.039413148002080206
            ],
            [
              0.013560169735333477,
              0.0804038925380842,
              0.04867200453862066,
              0.0265540148118653,
              0.034638293156888475
            ],
            [
              0.023917843356799032,
              0.07889303175975235,
              0.04792495336362836,
              0.02943973746304848,
              0.03689645590603434
            ]
          ]
        ],
        "aTsfcn": [
          [
            [
              -0.019707097740101327,
              -0.02571264919000673,
              -0.05935388298154087,
              -0.33622881185171144,
              -1.5475822720433732
            ],
            [
              -0.3903518105213509,
              -0.35034185629162146,
              -0.40599935248932634,
              -0.18501349629585012,
              -0.24328704690478822
            ],
            [
              -0.48021491254047305,
              -0.526943372951039,
              -0.3582742877252151,
              -0.12501849768448825,
              -0.11019928357043847
            ],
            [
              -0.4855961020867753,
              -0.6012429639381152,
              -0.3287343125941547,
              -0.11842279334392757,
              -0.10251264867434981
            ],
            [
              -0.4289252391492341,
              -0.6760550867714482,
              -0.3222577580853579,
              -0.12149156727019604,
              -0.10545786668349363
            ]
          ],
          [
            [
              -0.04000157578783941,
              -0.03738259752953099,
              -0.0424681144657525,
              -0.4651646949906524,
              -1.4125453552817115
            ],
            [
              -0.3902171103655758,
              -0.38206301560928196,
              -0.39749022589756444,
              -0.1705353228593996,
              -0.20886211074652078
            ],
            [
              -0.5331300210164446,
              -0.5459213243014006,
              -0.33564344795717227,
              -0.10381008512950667,
              -0.09118161628183048
            ],
            [
              -0.5422454909851228,
              -0.6111807413992446,
              -0.2825435184941122,
              -0.09879525125989617,
              -0.08135463452971717
            ],
            [
              -0.5009665651321307,
              -0.6628567840603388,
              -0.26952981230893747,
              -0.10400365856039082,
              -0.08476626184511413
            ]
          ],
          [
            [
              -0.02909706503792695,
              -0.028761666244738044,
              -0.04441195824277448,
              -0.3969415477456674,
              -1.4986759171320783
            ],
            [
              -0.38672568310652433,
              -0.4324642331121744,
              -0.4173976996733396,
              -0.1445927013444427,
              -0.17124080297017918
            ],
            [
              -0.587462722303668,
              -0.5534597575934606,
              -0.3084332653789427,
              -0.09432588619961518,
              -0.08161516788480742
            ],
            [
              -0.5980402051724725,
              -0.594678317114428,
              -0.23187606031281216,
              -0.08689258940556303,
              -0.07065215577052407
            ],
            [
              -0.5938745671912299,
              -0.619858711978705,
              -0.21074572280367923,
              -0.08989614052595597,
              -0.0721747925076949
            ]
          ]
        ],
        "vqicen": [
          [
            [
              [
                -1010405.5450385378,
                -1044085.7298731557,
                -1077765.9147077736,
                -1111446.0995423915,
                -1145126.2843770096,
                -1178806.4692116275,
                -1212486.6540462454,
                -1246166.8388808633
              ],
              [
                -4662615.668242007,
                -4818036.19051674,
                -4973456.712791474,
                -5128877.235066207,
                -5284297.757340941,
                -5439718.279615674,
                -5595138.801890408,
                -5750559.324165141
              ],
              [
                -19913297.251867708,
                -20577073.826929964,
                -21240850.40199222,
                -21904626.97705448,
                -22568403.552116737,
                -23232180.127178993,
                -23895956.70224125,
                -24559733.277303506
              ],
              [
                -177243228.2613429,
                -183151335.87005433,
                -189059443.4787658,
                -194967551.0874772,
                -200875658.69618863,
                -206783766.30490005,
                -212691873.9136115,
                -218599981.52232292
              ],
              [
                -6483640144.404656,
                -6699761482.551478,
                -6915882820.6983,
                -7132004158.845122,
                -7348125496.991944,
                -7564246835.138766,
                -7780368173.285588,
                -7996489511.432409
              ]
            ],
            [
              [
                -10476155.567663742,
                -10825360.753252534,
                -11174565.938841326,
                -11523771.124430116,
                -11872976.310018908,
                -12222181.4956077,
                -12571386.68119649,
                -12920591.866785282
              ],
              [
                -56443862.09168349,
                -58325324.16140627,
                -60206786.23112906,
                -62088248.30085184,
                -63969710.37057462,
                -65851172.4402974,
                -67732634.51002018,
                -69614096.57974297
              ],
              [
                -114103691.95507418,
                -117907148.35357666,
                -121710604.75207913,
                -125514061.1505816,
                -129317517.54908407,
                -133120973.94758655,
                -136924430.346089,
                -140727886.7445915
              ],
              [
                -97396631.45550634,
                -100643185.83735655,
                -103889740.21920677,
                -107136294.60105698,
                -110382848.98290719,
                -113629403.36475739,
                -116875957.7466076,
                -120122512.12845781
              ],
              [
                -434981407.0974606,
                -449480787.3340426,
                -463980167.57062465,
                -478479547.8072067,
                -492978928.0437887,
                -507478308.2803707,
                -521977688.51695275,
                -536477068.75353473
              ]
            ],
            [
              [
                -13045067.634972826,
                -13479903.222805254,
                -13914738.81063768,
                -14349574.39847011,
                -14784409.986302536,
                -15219245.574134964,
                -15654081.161967391,
                -16088916.74979982
              ],
              [
                -82055602.62956879,
                -84790789.38388774,
                -87525976.1382067,
                -90261162.89252566,
                -92996349.64684463,
                -95731536.40116358,
                -98466723.15548255,
                -101201909.9098015
              ],
              [
                -95765505.38325088,
                -98957688.89602591,
                -102149872.40880093,
                -105342055.92157596,
                -108534239.434351,
                -111726422.94712602,
                -114918606.45990105,
                -118110789.97267608
              ],
              [
                -65134419.59086029,
                -67305566.91055565,
                -69476714.23025098,
                -71647861.54994632,
                -73819008.86964166,
                -75990156.18933702,
                -78161303.50903235,
                -80332450.82872769
              ],
              [
                -128024459.29628268,
                -132291941.27282543,
                -136559423.2493682,
                -140826905.22591093,
                -145094387.2024537,
                -149361869.17899644,
                -153629351.1555392,
                -157896833.13208196
              ]
            ],
            [
              [
                -14234712.573764225,
                -14709202.992889699,
                -15183693.412015174,
                -15658183.831140647,
                -16132674.250266122,
                -16607164.669391597,
                -17081655.08851707,
                -17556145.507642545
              ],
              [
                -92781670.29861821,
                -95874392.64190549,
                -98967114.98519276,
                -102059837.32848004,
                -105152559.6717673,
                -108245282.01505457,
                -111338004.35834184,
                -114430726.70162912
              ],
              [
                -86553347.0957119,
                -89438458.66556896,
                -92323570.23542602,
                -95208681.8052831,
                -98093793.37514016,
                -100978904.94499722,
                -103864016.51485428,
                -106749128.08471134
              ],
              [
                -61441184.30106817,
                -63489223.777770445,
                -65537263.25447272,
                -67585302.73117499,
                -69633342.20787726,
                -71681381.68457954,
                -73729421.16128181,
                -75777460.63798408
              ],
              [
                -114793878.55960578,
                -118620341.17825931,
                -122446803.79691283,
                -126273266.41556635,
                -130099729.03421989,
                -133926191.65287341,
                -137752654.27152693,
                -141579116.89018047
              ]
            ],
            [
              [
                -15453431.821020039,
                -15968546.21505404,
                -16483660.609088043,
                -16998775.003122043,
                -17513889.397156045,
                -18029003.791190047,
                -18544118.18522405,
                -19059232.579258047
              ],
              [
                -103876719.5458994,
                -107339276.86409605,
                -110801834.1822927,
                -114264391.50048934,
                -117726948.818686,
                -121189506.13688263,
                -124652063.45507929,
                -128114620.77327593
              ],
              [
                -83177145.33214538,
                -85949716.8432169,
                -88722288.3542884,
                -91494859.86535992,
                -94267431.37643144,
                -97040002.88750294,
                -99812574.39857446,
                -102585145.90964597
              ],
              [
                -62676497.03723817,
                -64765713.60514611,
                -66854930.173054054,
                -68944146.740962,
                -71033363.30886993,
                -73122579.87677787,
                -75211796.4446858,
                -77301013.01259375
              ],
              [
                -116058548.56644732,
                -119927166.85199556,
                -123795785.1375438,
                -127664403.42309204,
                -131533021.70864029,
                -135401639.99418852,
                -139270258.2797368,
                -143138876.56528503
              ]
            ]
          ],
          [
            [
              [
                -1619512.2448213005,
                -1673495.986315344,
                -1727479.7278093873,
                -1781463.4693034308,
                -1835447.210797474,
                -1889430.9522915173,
                -1943414.6937855608,
                -1997398.435279604
              ],
              [
                -7183243.879475289,
                -7422685.342124465,
                -7662126.804773641,
                -7901568.267422818,
                -8141009.730071994,
                -8380451.19272117,
                -8619892.655370347,
                -8859334.118019523
              ],
              [
                -11982516.701530954,
                -12381933.92491532,
                -12781351.148299685,
                -13180768.37168405,
                -13580185.595068416,
                -13979602.81845278,
                -14379020.041837145,
                -14778437.26522151
              ],
              [
                -292262113.7954474,
                -302004184.25529563,
                -311746254.7151439,
                -321488325.17499214,
                -331230395.63484037,
                -340972466.09468865,
                -350714536.5545369,
                -360456607.0143851
              ],
              [
                -5945401712.316814,
                -6143581769.394042,
                -6341761826.471269,
                -6539941883.548496,
                -6738121940.625723,
                -6936301997.7029505,
                -7134482054.780177,
                -7332662111.857405
              ]
            ],
            [
              [
                -10226827.050327448,
                -10567721.285338363,
                -10908615.520349279,
                -11249509.755360194,
                -11590403.990371108,
                -11931298.225382023,
                -12272192.460392939,
                -12613086.695403853
              ],
              [
                -62447541.98730224,
                -64529126.72021232,
                -66610711.45312239,
                -68692296.18603247,
                -70773880.91894254,
                -72855465.65185262,
                -74937050.38476269,
                -77018635.11767277
              ],
              [
                -106798740.66312025,
                -110358698.68522426,
                -113918656.70732827,
                -117478614.72943227,
                -121038572.75153628,
                -124598530.77364029,
                -128158488.7957443,
                -131718446.81784831
              ],
              [
                -91726238.93640743,
                -94783780.2342877,
                -97841321.53216794,
                -100898862.83004819,
                -103956404.12792844,
                -107013945.42580868,
                -110071486.72368893,
                -113129028.02156918
              ],
              [
                -350022124.94925445,
                -361689529.1142296,
                -373356933.2792047,
                -385024337.4441799,
                -396691741.60915506,
                -408359145.77413017,
                -420026549.93910533,
                -431693954.1040805
              ]
            ],
            [
              [
                -14713179.175130641,
                -15203618.480968328,
                -15694057.786806017,
                -16184497.092643704,
                -16674936.398481393,
                -17165375.704319082,
                -17655815.01015677,
                -18146254.315994456
              ],
              [
                -83835445.10622582,
                -86629959.94310002,
                -89424474.7799742,
                -92218989.61684841,
                -95013504.4537226,
                -97808019.29059678,
                -100602534.12747099,
                -103397048.96434517
              ],
              [
                -88145793.94795212,
                -91083987.07955052,
                -94022180.21114892,
                -96960373.34274733,
                -99898566.47434573,
                -102836759.60594414,
                -105774952.73754254,
                -108713145.86914094
              ],
              [
                -53556565.97440945,
                -55341784.8402231,
                -57127003.70603675,
                -58912222.5718504,
                -60697441.43766405,
                -62482660.30347769,
                -64267879.16929134,
                -66053098.03510499
              ],
              [
                -103567400.3857428,
                -107019647.06526755,
                -110471893.74479231,
                -113924140.42431708,
                -117376387.10384183,
                -120828633.78336659,
                -124280880.46289136,
                -127733127.1424161
              ]
            ],
            [
              [
                -16762106.295848468,
                -17320843.172376752,
                -17879580.048905034,
                -18438316.925433315,
                -18997053.801961597,
                -19555790.67848988,
                -20114527.55501816,
                -20673264.431546446
              ],
              [
                -91404927.24394068,
                -94451758.15207204,
                -97498589.06020339,
                -100545419.96833475,
                -103592250.87646611,
                -106639081.78459746,
                -109685912.69272882,
                -112732743.60086018
              ],
              [
                -73504113.11982565,
                -75954250.22381984,
                -78404387.32781403,
                -80854524.43180822,
                -83304661.5358024,
                -85754798.63979658,
                -88204935.74379078,
                -90655072.84778497
              ],
              [
                -50647884.558415815,
                -52336147.37702967,
                -54024410.19564353,
                -55712673.014257394,
                -57400935.83287125,
                -59089198.651485115,
                -60777461.47009897,
                -62465724.28871284
              ],
              [
                -88855116.38101722,
                -91816953.5937178,
                -94778790.80641837,
                -97740628.01911895,
                -100702465.23181953,
                -103664302.4445201,
                -106626139.65722068,
                -109587976.86992125
              ]
            ],
            [
              [
                -19681225.185218826,
                -20337266.02472612,
                -20993306.864233416,
                -21649347.70374071,
                -22305388.543248,
                -22961429.3827553,
                -23617470.22226259,
                -24273511.061769884
              ],
              [
                -97827441.02143586,
                -101088355.72215039,
                -104349270.42286491,
                -107610185.12357944,
                -110871099.82429397,
                -114132014.5250085,
                -117392929.22572303,
                -120653843.92643756
              ],
              [
                -69310779.05966069,
                -71621138.36164938,
                -73931497.66363807,
                -76241856.96562676,
                -78552216.26761545,
                -80862575.56960414,
                -83172934.87159283,
                -85483294.17358153
              ],
              [
                -53172409.73069773,
                -54944823.38838766,
                -56717237.04607758,
                -58489650.7037675,
                -60262064.36145743,
                -62034478.01914735,
                -63806891.67683728,
                -65579305.3345272
              ],
              [
                -91989663.14430004,
                -95055985.24911004,
                -98122307.35392004,
                -101188629.45873004,
                -104254951.56354006,
                -107321273.66835006,
                -110387595.77316006,
                -113453917.87797005
              ]
            ]
          ],
          [
            [
              [
                -1050384.7287362532,
                -1085397.5530274617,
                -1120410.37731867,
                -1155423.2016098786,
                -1190436.0259010869,
                -1225448.8501922954,
                -1260461.674483504,
                -1295474.4987747122
              ],
              [
                -5359473.919333662,
                -5538123.049978117,
                -5716772.180622572,
                -5895421.311267028,
                -6074070.441911483,
                -6252719.572555939,
                -6431368.703200394,
                -6610017.833844849
              ],
              [
                -13472842.755627925,
                -13921937.514148856,
                -14371032.272669787,
                -14820127.031190718,
                -15269221.789711647,
                -15718316.548232578,
                -16167411.306753509,
                -16616506.06527444
              ],
              [
                -218603394.277154,
                -225890174.08639246,
                -233176953.89563093,
                -240463733.7048694,
                -247750513.51410785,
                -255037293.32334632,
                -262324073.13258478,
                -269610852.94182324
              ],
              [
                -5667397220.074306,
                -5856310460.743448,
                -6045223701.412592,
                -6234136942.081736,
                -6423050182.750879,
                -6611963423.420023,
                -6800876664.089167,
                -6989789904.758309
              ]
            ],
            [
              [
                -10949020.595605763,
                -11313987.948792621,
                -11678955.30197948,
                -12043922.65516634,
                -12408890.008353198,
                -12773857.361540057,
                -13138824.714726916,
                -13503792.067913774
              ],
              [
                -69929861.78522323,
                -72260857.178064,
                -74591852.57090478,
                -76922847.96374555,
                -79253843.35658632,
                -81584838.7494271,
                -83915834.14226787,
                -86246829.53510864
              ],
              [
                -110878308.84820364,
                -114574252.4764771,
                -118270196.10475056,
                -121966139.733024,
                -125662083.36129746,
                -129358026.98957092,
                -133053970.61784437,
                -136749914.24611783
              ],
              [
                -76163127.47459684,
                -78701898.39041673,
                -81240669.30623662,
                -83779440.22205652,
                -86318211.13787642,
                -88856982.0536963,
                -91395752.9695162,
                -93934523.8853361
              ],
              [
                -249046896.92158964,
                -257348460.1523093,
                -265650023.38302895,
                -273951586.6137486,
                -282253149.8444683,
                -290554713.0751879,
                -298856276.3059076,
                -307157839.53662723
              ]
            ],
            [
              [
                -16908799.067611128,
                -17472425.703198165,
                -18036052.3387852,
                -18599678.97437224,
                -19163305.60995928,
                -19726932.245546315,
                -20290558.88113335,
                -20854185.51672039
              ],
              [
                -83423643.93804024,
                -86204432.06930825,
                -88985220.20057626,
                -91766008.33184427,
                -94546796.46311228,
                -97327584.59438029,
                -100108372.7256483,
                -102889160.85691631
              ],
              [
                -80308935.9402471,
                -82985900.47158867,
                -85662865.00293025,
                -88339829.53427182,
                -91016794.06561339,
                -93693758.59695496,
                -96370723.12829652,
                -99047687.65963809
              ],
              [
                -48500319.09540076,
                -50116996.39858078,
                -51733673.701760806,
                -53350351.00494083,
                -54967028.308120854,
                -56583705.611300886,
                -58200382.91448091,
                -59817060.217660934
              ],
              [
                -92415232.49604622,
                -95495740.24591441,
                -98576247.99578263,
                -101656755.74565083,
                -104737263.49551904,
                -107817771.24538724,
                -110898278.99525546,
                -113978786.74512365
              ]
            ],
            [
              [
                -20552753.15377309,
                -21237844.92556553,
                -21922936.697357964,
                -22608028.4691504,
                -23293120.240942836,
                -23978212.012735274,
                -24663303.78452771,
                -25348395.556320146
              ],
              [
                -86023948.09724155,
                -88891413.03381628,
                -91758877.97039099,
                -94626342.9069657,
                -97493807.84354043,
                -100361272.78011514,
                -103228737.71668987,
                -106096202.65326458
              ],
              [
                -60210512.98024265,
                -62217530.07958407,
                -64224547.17892549,
                -66231564.278266914,
                -68238581.37760833,
                -70245598.47694975,
                -72252615.57629117,
                -74259632.6756326
              ],
              [
                -44298636.08745442,
                -45775257.29036957,
                -47251878.49328472,
                -48728499.696199864,
                -50205120.89911501,
                -51681742.10203016,
                -53158363.304945305,
                -54634984.50786045
              ],
              [
                -76931626.48770368,
                -79496014.03729379,
                -82060401.58688392,
                -84624789.13647404,
                -87189176.68606417,
                -89753564.2356543,
                -92317951.7852444,
                -94882339.33483453
              ]
            ],
            [
              [
                -25625830.070847258,
                -26480024.406542167,
                -27334218.742237076,
                -28188413.077931985,
                -29042607.41362689,
                -29896801.7493218,
                -30750996.08501671,
                -31605190.420711618
              ],
              [
                -87550358.89968382,
                -90468704.19633995,
                -93387049.49299608,
                -96305394.7896522,
                -99223740.08630833,
                -102142085.38296446,
                -105060430.6796206,
                -107978775.97627671
              ],
              [
                -54634909.031027116,
                -56456072.665394686,
                -58277236.29976226,
                -60098399.93412983,
                -61919563.5684974,
                -63740727.20286497,
                -65561890.83723254,
                -67383054.47160012
              ],
              [
                -45752375.59164939,
                -47277454.778037705,
                -48802533.96442602,
                -50327613.15081433,
                -51852692.337202646,
                -53377771.52359096,
                -54902850.70997927,
                -56427929.89636759
              ],
              [
                -78104790.5967532,
                -80708283.61664498,
                -83311776.63653675,
                -85915269.65642852,
                -88518762.67632028,
                -91122255.69621207,
                -93725748.71610384,
                -96329241.7359956
              ]
            ]
          ]
        ],
        "vsqsnon": [
          [
            [
              [
                -0.0,
                -0.0,
                -0.0
              ],
              [
                -217282.94259217984,
                -219258.24207029055,
                -221233.5415484013
              ],
              [
                -2246327.761472546,
                -2266748.922940478,
                -2287170.0844084104
              ],
              [
                -20054650.83806575,
                -20236965.845684532,
                -20419280.85330331
              ],
              [
                -375959877.74675936,
                -379377694.81718445,
                -382795511.88760954
              ]
            ],
            [
              [
                -281471.1977187691,
                -284030.0267889397,
                -286588.8558591103
              ],
              [
                -5106850.984724904,
                -5153276.9027678585,
                -5199702.820810812
              ],
              [
                -9298773.228842609,
                -9383307.530922996,
                -9467841.833003383
              ],
              [
                -5831277.013390759,
                -5884288.6226034025,
                -5937300.231816046
              ],
              [
                -17658078.47465402,
                -17818606.460787237,
                -17979134.44692046
              ]
            ],
            [
              [
                -609075.756663754,
                -614612.8089970609,
                -620149.8613303677
              ],
              [
                -8503058.39981736,
                -8580358.930724792,
                -8657659.461632222
              ],
              [
                -7680160.344103814,
                -7749979.9835956665,
                -7819799.62308752
              ],
              [
                -3968676.430224954,
                -4004755.306863363,
                -4040834.1835017717
              ],
              [
                -6145788.603363127,
                -6201659.4088482475,
                -6257530.214333367
              ]
            ],
            [
              [
                -809408.3913686748,
                -816766.6494720264,
                -824124.907575378
              ],
              [
                -10208018.919277433,
                -10300819.091270864,
                -10393619.263264297
              ],
              [
                -7539064.987982979,
                -7607601.942419188,
                -7676138.896855397
              ],
              [
                -4087108.356154864,
                -4124263.8866653633,
                -4161419.417175862
              ],
              [
                -5844699.224697963,
                -5897832.854013399,
                -5950966.483328836
              ]
            ],
            [
              [
                -1554362.8817322892,
                -1568493.453384401,
                -1582624.0250365126
              ],
              [
                -11748428.963750811,
                -11855232.863421272,
                -11962036.763091734
              ],
              [
                -7926382.311385988,
                -7998440.332398588,
                -8070498.353411188
              ],
              [
                -4625246.606848543,
                -4667294.303274439,
                -4709341.999700334
              ],
              [
                -6301428.066834839,
                -6358713.776533338,
                -6415999.4862318365
              ]
            ]
          ],
          [
            [
              [
                -0.0,
                -0.0,
                -0.0
              ],
              [
                -307444.8502601626,
                -310239.8034443459,
                -313034.7566285292
              ],
              [
                -795192.4516480622,
                -802421.4739357718,
                -809650.4962234815
              ],
              [
                -31042009.44213572,
                -31324209.52797332,
                -31606409.61381092
              ],
              [
                -330533217.1205692,
                -333538064.54893804,
                -336542911.97730684
              ]
            ],
            [
              [
                -235983.41761491523,
                -238128.72141141444,
                -240274.02520791368
              ],
              [
                -5632401.633246073,
                -5683605.2844574,
                -5734808.935668728
              ],
              [
                -8182760.366108316,
                -8257149.096709301,
                -8331537.8273102855
              ],
              [
                -5386515.068001251,
                -5435483.386801262,
                -5484451.705601274
              ],
              [
                -15234438.153619288,
                -15372933.045924919,
                -15511427.938230548
              ]
            ],
            [
              [
                -697584.2170937569,
                -703925.8917946093,
                -710267.5664954616
              ],
              [
                -8743149.028636962,
                -8822632.20162457,
                -8902115.37461218
              ],
              [
                -7246283.462014766,
                -7312158.766214901,
                -7378034.070415035
              ],
              [
                -3324883.664483368,
                -3355109.879615035,
                -3385336.094746702
              ],
              [
                -4957191.876268386,
                -5002257.256961735,
                -5047322.637655084
              ]
            ],
            [
              [
                -1076902.339052576,
                -1086692.3603166905,
                -1096482.381580805
              ],
              [
                -9974102.254107362,
                -10064775.910962883,
                -10155449.567818403
              ],
              [
                -6574662.756250316,
                -6634432.417670773,
                -6694202.079091231
              ],
              [
                -3415001.2656091717,
                -3446046.7316601644,
                -3477092.1977111567
              ],
              [
                -4530672.407990959,
                -4571860.338972695,
                -4613048.269954431
              ]
            ],
            [
              [
                -2088658.015101599,
                -2107645.8152388865,
                -2126633.6153761735
              ],
              [
                -10690299.764878737,
                -10787484.308195816,
                -10884668.851512896
              ],
              [
                -6703535.984042434,
                -6764477.220261002,
                -6825418.456479569
              ],
              [
                -3899964.297911216,
                -3935418.518801318,
                -3970872.73969142
              ],
              [
                -4943054.957732478,
                -4987991.820984591,
                -5032928.684236704
              ]
            ]
          ],
          [
            [
              [
                -0.0,
                -0.0,
                -0.0
              ],
              [
                -318944.7926057803,
                -321844.2907203783,
                -324743.78883497627
              ],
              [
                -1534035.3949409362,
                -1547981.171258581,
                -1561926.947576226
              ],
              [
                -25009910.76556324,
                -25237273.59070472,
                -25464636.415846206
              ],
              [
                -386788039.3709907,
                -390304294.27436334,
                -393820549.177736
              ]
            ],
            [
              [
                -354004.4982672506,
                -357222.72097877105,
                -360440.9436902915
              ],
              [
                -6573350.54630007,
                -6633108.278539161,
                -6692866.010778253
              ],
              [
                -8983761.6773406,
                -9065432.238043698,
                -9147102.798746794
              ],
              [
                -4456452.563988059,
                -4496965.769115223,
                -4537478.974242387
              ],
              [
                -11538072.016326718,
                -11642963.580111505,
                -11747855.143896295
              ]
            ],
            [
              [
                -898495.6731674877,
                -906663.8156508285,
                -914831.9581341693
              ],
              [
                -8492997.689384239,
                -8570206.759287732,
                -8647415.829191225
              ],
              [
                -6477705.594753693,
                -6536593.827433271,
                -6595482.060112851
              ],
              [
                -2982228.3610129897,
                -3009339.5279312897,
                -3036450.69484959
              ],
              [
                -4335446.2802288225,
                -4374859.428230903,
                -4414272.576232983
              ]
            ],
            [
              [
                -1491618.6708866823,
                -1505178.840622016,
                -1518739.0103573494
              ],
              [
                -8844428.179189263,
                -8924832.071727347,
                -9005235.96426543
              ],
              [
                -5353920.499248273,
                -5402592.503786894,
                -5451264.508325513
              ],
              [
                -2920941.629305183,
                -2947495.6441170485,
                -2974049.658928914
              ],
              [
                -3810212.2472577323,
                -3844850.5404146207,
                -3879488.833571509
              ]
            ],
            [
              [
                -2630962.7692478937,
                -2654880.6126046926,
                -2678798.4559614914
              ],
              [
                -8678233.493572759,
                -8757126.52533251,
                -8836019.557092262
              ],
              [
                -5271744.86999912,
                -5319669.823362748,
                -5367594.776726376
              ],
              [
                -3238371.1209353325,
                -3267810.858398381,
                -3297250.59586143
              ],
              [
                -4058610.1496637776,
                -4095506.6055698115,
                -4132403.061475846
              ]
            ]
          ]
        ]
      },
      "parameter_overrides": {
        "uvel": [
          [
            0.00012200831259922484,
            -0.00430503734325033,
            -0.006404552971129575,
            -0.0029079564379971357,
            -0.0037366886985347827
          ],
          [
            1.349728123413932e-05,
            -0.0049893802525858445,
            -0.006556908183432414,
            -0.004013004944111566,
            -0.0042590499452267415
          ],
          [
            0.0,
            -0.006049027918925767,
            -0.0058923320164812176,
            -0.0045391275967812655,
            -0.004738980872614332
          ]
        ],
        "vvel": [
          [
            0.0007204892821085377,
            0.0007865942006418693,
            0.0037168927343423233,
            0.013900356415145056,
            0.015928611364519916
          ],
          [
            0.0009977387642852074,
            0.001620845665338858,
            0.00661497866621736,
            0.011651221033965178,
            0.012191539845748306
          ],
          [
            0.0,
            0.003975027437344815,
            0.009118244672511678,
            0.01094051866825294,
            0.010805999470988786
          ]
        ],
        "HTE": [
          [
            59395.455016421605,
            59395.455016421605,
            59395.455016421605,
            59395.455016421605,
            59395.455016421605
          ],
          [
            59395.455016421605,
            59395.455016421605,
            59395.455016421605,
            59395.455016421605,
            59395.455016421605
          ],
          [
            59395.455016421605,
            59395.455016421605,
            59395.455016421605,
            59395.455016421605,
            59395.455016421605
          ]
        ],
        "HTN": [
          [
            26251.235254161526,
            27390.328313754686,
            28527.04003199235,
            29661.271582069905,
            30792.92435281096
          ],
          [
            26251.235254161526,
            27390.328313754686,
            28527.04003199235,
            29661.271582069905,
            30792.92435281096
          ],
          [
            26251.235254161526,
            27390.328313754686,
            28527.04003199235,
            29661.271582069905,
            30792.92435281096
          ]
        ],
        "tarea": [
          [
            1525307808.0270946,
            1593032537.954344,
            1660618768.108248,
            1728060622.4772792,
            1795352237.6020775
          ],
          [
            1525307808.0270946,
            1593032537.954344,
            1660618768.108248,
            1728060622.4772792,
            1795352237.6020775
          ],
          [
            1525307808.0270946,
            1593032537.954344,
            1660618768.108248,
            1728060622.4772792,
            1795352237.6020775
          ]
        ]
      },
      "assertions": [
        {
          "variable": "Tsfcn",
          "time": 3600.0,
          "expected": -2.0,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 2
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qicen_adv",
          "time": 3600.0,
          "expected": -300000000.0,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 2,
            "ice_layer": 1
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qicen_adv",
          "time": 3600.0,
          "expected": -310000000.0,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 2,
            "ice_layer": 2
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qicen_adv",
          "time": 3600.0,
          "expected": -320000000.0,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 2,
            "ice_layer": 3
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qicen_adv",
          "time": 3600.0,
          "expected": -330000000.0,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 2,
            "ice_layer": 4
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qicen_adv",
          "time": 3600.0,
          "expected": -340000000.0,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 2,
            "ice_layer": 5
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qicen_adv",
          "time": 3600.0,
          "expected": -350000000.0,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 2,
            "ice_layer": 6
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qicen_adv",
          "time": 3600.0,
          "expected": -360000000.0,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 2,
            "ice_layer": 7
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qicen_adv",
          "time": 3600.0,
          "expected": -370000000.0,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 2,
            "ice_layer": 8
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qsnon_adv",
          "time": 3600.0,
          "expected": -110000000.0,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 2,
            "snow_layer": 1
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qsnon_adv",
          "time": 3600.0,
          "expected": -111000000.0,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 2,
            "snow_layer": 2
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qsnon_adv",
          "time": 3600.0,
          "expected": -112000000.0,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 2,
            "snow_layer": 3
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "Tsfcn",
          "time": 3600.0,
          "expected": -2.0,
          "coords": {
            "i": 2,
            "j": 5,
            "ncat": 1
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qicen_adv",
          "time": 3600.0,
          "expected": -300000000.0,
          "coords": {
            "i": 2,
            "j": 5,
            "ncat": 1,
            "ice_layer": 1
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qicen_adv",
          "time": 3600.0,
          "expected": -310000000.0,
          "coords": {
            "i": 2,
            "j": 5,
            "ncat": 1,
            "ice_layer": 2
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qicen_adv",
          "time": 3600.0,
          "expected": -320000000.0,
          "coords": {
            "i": 2,
            "j": 5,
            "ncat": 1,
            "ice_layer": 3
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qicen_adv",
          "time": 3600.0,
          "expected": -330000000.0,
          "coords": {
            "i": 2,
            "j": 5,
            "ncat": 1,
            "ice_layer": 4
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qicen_adv",
          "time": 3600.0,
          "expected": -340000000.0,
          "coords": {
            "i": 2,
            "j": 5,
            "ncat": 1,
            "ice_layer": 5
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qicen_adv",
          "time": 3600.0,
          "expected": -350000000.0,
          "coords": {
            "i": 2,
            "j": 5,
            "ncat": 1,
            "ice_layer": 6
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qicen_adv",
          "time": 3600.0,
          "expected": -360000000.0,
          "coords": {
            "i": 2,
            "j": 5,
            "ncat": 1,
            "ice_layer": 7
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qicen_adv",
          "time": 3600.0,
          "expected": -370000000.0,
          "coords": {
            "i": 2,
            "j": 5,
            "ncat": 1,
            "ice_layer": 8
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qsnon_adv",
          "time": 3600.0,
          "expected": -110000000.0,
          "coords": {
            "i": 2,
            "j": 5,
            "ncat": 1,
            "snow_layer": 1
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qsnon_adv",
          "time": 3600.0,
          "expected": -111000000.0,
          "coords": {
            "i": 2,
            "j": 5,
            "ncat": 1,
            "snow_layer": 2
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qsnon_adv",
          "time": 3600.0,
          "expected": -112000000.0,
          "coords": {
            "i": 2,
            "j": 5,
            "ncat": 1,
            "snow_layer": 3
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "Tsfcn",
          "time": 3600.0,
          "expected": -2.0,
          "coords": {
            "i": 1,
            "j": 1,
            "ncat": 5
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qicen_adv",
          "time": 3600.0,
          "expected": -300000000.0,
          "coords": {
            "i": 1,
            "j": 1,
            "ncat": 5,
            "ice_layer": 1
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qicen_adv",
          "time": 3600.0,
          "expected": -310000000.0,
          "coords": {
            "i": 1,
            "j": 1,
            "ncat": 5,
            "ice_layer": 2
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qicen_adv",
          "time": 3600.0,
          "expected": -320000000.0,
          "coords": {
            "i": 1,
            "j": 1,
            "ncat": 5,
            "ice_layer": 3
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qicen_adv",
          "time": 3600.0,
          "expected": -330000000.0,
          "coords": {
            "i": 1,
            "j": 1,
            "ncat": 5,
            "ice_layer": 4
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qicen_adv",
          "time": 3600.0,
          "expected": -340000000.0,
          "coords": {
            "i": 1,
            "j": 1,
            "ncat": 5,
            "ice_layer": 5
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qicen_adv",
          "time": 3600.0,
          "expected": -350000000.0,
          "coords": {
            "i": 1,
            "j": 1,
            "ncat": 5,
            "ice_layer": 6
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qicen_adv",
          "time": 3600.0,
          "expected": -360000000.0,
          "coords": {
            "i": 1,
            "j": 1,
            "ncat": 5,
            "ice_layer": 7
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qicen_adv",
          "time": 3600.0,
          "expected": -370000000.0,
          "coords": {
            "i": 1,
            "j": 1,
            "ncat": 5,
            "ice_layer": 8
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qsnon_adv",
          "time": 3600.0,
          "expected": -110000000.0,
          "coords": {
            "i": 1,
            "j": 1,
            "ncat": 5,
            "snow_layer": 1
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qsnon_adv",
          "time": 3600.0,
          "expected": -111000000.0,
          "coords": {
            "i": 1,
            "j": 1,
            "ncat": 5,
            "snow_layer": 2
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qsnon_adv",
          "time": 3600.0,
          "expected": -112000000.0,
          "coords": {
            "i": 1,
            "j": 1,
            "ncat": 5,
            "snow_layer": 3
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "Tsfcn",
          "time": 3600.0,
          "expected": -2.0,
          "coords": {
            "i": 2,
            "j": 1,
            "ncat": 1
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qicen_adv",
          "time": 3600.0,
          "expected": -300000000.0,
          "coords": {
            "i": 2,
            "j": 1,
            "ncat": 1,
            "ice_layer": 1
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qicen_adv",
          "time": 3600.0,
          "expected": -310000000.0,
          "coords": {
            "i": 2,
            "j": 1,
            "ncat": 1,
            "ice_layer": 2
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qicen_adv",
          "time": 3600.0,
          "expected": -320000000.0,
          "coords": {
            "i": 2,
            "j": 1,
            "ncat": 1,
            "ice_layer": 3
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qicen_adv",
          "time": 3600.0,
          "expected": -330000000.0,
          "coords": {
            "i": 2,
            "j": 1,
            "ncat": 1,
            "ice_layer": 4
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qicen_adv",
          "time": 3600.0,
          "expected": -340000000.0,
          "coords": {
            "i": 2,
            "j": 1,
            "ncat": 1,
            "ice_layer": 5
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qicen_adv",
          "time": 3600.0,
          "expected": -350000000.0,
          "coords": {
            "i": 2,
            "j": 1,
            "ncat": 1,
            "ice_layer": 6
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qicen_adv",
          "time": 3600.0,
          "expected": -360000000.0,
          "coords": {
            "i": 2,
            "j": 1,
            "ncat": 1,
            "ice_layer": 7
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qicen_adv",
          "time": 3600.0,
          "expected": -370000000.0,
          "coords": {
            "i": 2,
            "j": 1,
            "ncat": 1,
            "ice_layer": 8
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qsnon_adv",
          "time": 3600.0,
          "expected": -110121000.0,
          "coords": {
            "i": 2,
            "j": 1,
            "ncat": 1,
            "snow_layer": 1
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qsnon_adv",
          "time": 3600.0,
          "expected": -110121000.0,
          "coords": {
            "i": 2,
            "j": 1,
            "ncat": 1,
            "snow_layer": 2
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "qsnon_adv",
          "time": 3600.0,
          "expected": -110121000.0,
          "coords": {
            "i": 2,
            "j": 1,
            "ncat": 1,
            "snow_layer": 3
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        }
      ]
    },
    {
      "id": "cice_transport_tracers_divergence_pins",
      "description": "Instantaneous pins of the lowered flux divergences of the dumped step-1 t_entr state at time 0 (time_span {0, 0}, independent of the integrator): the fifteen algebraic rewrite targets div_flux/div_flux_v/div_flux_s/div_aTsfcn/div_vqicen/div_vsqsnon are evaluated from the dumped products aTsfcn = aicen*Tsfcn, vqicen = vicen*qice_k, vsqsnon = vsnon*qsno_k stacked over the passive layer axis (the initial_conditions of this test; 'derived (not a dump column)') and the dump's velocity/grid parameters, and asserted against the rule formula of the transport_flux_divergence / transport_flux_divergence_layered lowering computed by stage1/analysis/extract_cice_transport_tracers_pins.py: div(c) = (F_e(i,j) - F_e(i-1,j) + F_n(i,j) - F_n(i,j-1))/tarea with F_e = HTE*((uS+uN)/2)*((cL+cR)/2) and F_n = HTN*((vW+vE)/2)*((cS+cN)/2), the centered face-average reconstruction of the rule's scalar atoms transport_flux_e/n, with the halo-copy closures of the rule's nine position classes (every neighbor index leaving the domain bound to the nearest interior value). Each pin asserts D(product)/dt = -div at time 0 for the dumped state with rel 1e-12, at the few informative points of the review rule rather than every index: 45 pins = 3 cells (the interior cell (2,4), the edge cell (2,5) and the corner cell (1,1)) x 15 fields, at each (cell, field) the single category with the largest |div| (the strongest signal; the divergence operator is linear in the product field and identical for every category). At the interior cell the pin verifies the centered face-average reconstruction against the dumped state; at the edge and corner cells the pins verify the rule's halo-copy closure -- a property of the discretization rule, not of CICE behaviour (the halo-copied neighbor values are the rule's construction; the Fortran's own halo update would supply physical boundary values instead). The uniform-field c = 1 pin of cice_transport_uniform_field cross-checks the same operator: div_flux = 1.1240071614720283e-07 1/s at local (2,4).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "initial_conditions": {
        "aicen": [
          [
            [
              0.009853548870050664,
              0.012856324595003365,
              0.029676941490770437,
              0.16811440592585572,
              0.7737911360216866
            ],
            [
              0.19517590526067544,
              0.17517092814581073,
              0.20299967624466317,
              0.09250674814792506,
              0.12164352345239411
            ],
            [
              0.24010745627023652,
              0.2634716864755195,
              0.17913714386260754,
              0.06250924884224413,
              0.055099641785219235
            ],
            [
              0.24279805104338764,
              0.3006214819690576,
              0.16436715629707735,
              0.05921139667196378,
              0.051256324337174905
            ],
            [
              0.21446261957461704,
              0.3380275433857241,
              0.16112887904267895,
              0.06074578363509802,
              0.05272893334174682
            ]
          ],
          [
            [
              0.020000787893919705,
              0.018691298764765496,
              0.02123405723287625,
              0.2325823474953262,
              0.7062726776408558
            ],
            [
              0.1951085551827879,
              0.19103150780464098,
              0.19874511294878222,
              0.0852676614296998,
              0.10443105537326039
            ],
            [
              0.2665650105082223,
              0.2729606621507003,
              0.16782172397858613,
              0.05190504256475333,
              0.04559080814091524
            ],
            [
              0.2711227454925614,
              0.3055903706996223,
              0.1412717592470561,
              0.04939762562994809,
              0.040677317264858584
            ],
            [
              0.25048328256606534,
              0.3314283920301694,
              0.13476490615446873,
              0.05200182928019541,
              0.042383130922557063
            ]
          ],
          [
            [
              0.014548532518963476,
              0.014380833122369022,
              0.02220597912138724,
              0.1984707738728337,
              0.7493379585660391
            ],
            [
              0.19336284155326217,
              0.2162321165560872,
              0.2086988498366698,
              0.07229635067222134,
              0.08562040148508959
            ],
            [
              0.293731361151834,
              0.2767298787967303,
              0.15421663268947136,
              0.04716294309980759,
              0.04080758394240371
            ],
            [
              0.29902010258623624,
              0.297339158557214,
              0.11593803015640608,
              0.04344629470278152,
              0.035326077885262035
            ],
            [
              0.29693728359561494,
              0.3099293559893525,
              0.10537286140183962,
              0.044948070262977986,
              0.03608739625384745
            ]
          ]
        ],
        "vicen": [
          [
            [
              0.0033680184834617927,
              0.015542052227473355,
              0.06637765750622569,
              0.590810760871143,
              21.61213381468219
            ],
            [
              0.03492051855887914,
              0.1881462069722783,
              0.3803456398502473,
              0.32465543818502113,
              1.449938023658202
            ],
            [
              0.043483558783242754,
              0.27351867543189595,
              0.3192183512775029,
              0.21711473196953432,
              0.4267481976542756
            ],
            [
              0.04744904191254742,
              0.30927223432872736,
              0.28851115698570634,
              0.20480394767022725,
              0.3826462618653526
            ],
            [
              0.05151143940340013,
              0.3462557318196647,
              0.27725715110715127,
              0.2089216567907939,
              0.38686182855482437
            ]
          ],
          [
            [
              0.005398374149404335,
              0.02394414626491763,
              0.039941722338436514,
              0.9742070459848247,
              19.818005707722715
            ],
            [
              0.034089423501091495,
              0.20815847329100748,
              0.35599580221040084,
              0.3057541297880248,
              1.1667404164975148
            ],
            [
              0.049043930583768804,
              0.2794514836874194,
              0.2938193131598404,
              0.17852188658136484,
              0.34522466795247597
            ],
            [
              0.05587368765282823,
              0.3046830908131356,
              0.24501371039941883,
              0.16882628186138604,
              0.29618372127005743
            ],
            [
              0.06560408395072942,
              0.32609147007145284,
              0.23103593019886898,
              0.17724136576899244,
              0.30663221048100014
            ]
          ],
          [
            [
              0.003501282429120844,
              0.01786491306444554,
              0.04490947585209308,
              0.7286779809238466,
              18.89132406691435
            ],
            [
              0.03649673531868588,
              0.23309953928407742,
              0.3695943628273455,
              0.25387709158198946,
              0.8301563230719655
            ],
            [
              0.05636266355870376,
              0.27807881312680083,
              0.267696453134157,
              0.16166773031800252,
              0.3080507749868207
            ],
            [
              0.06850917717924364,
              0.28674649365747185,
              0.20070170993414216,
              0.14766212029151474,
              0.25643875495901225
            ],
            [
              0.08541943356949086,
              0.29183452966561274,
              0.18211636343675705,
              0.1525079186388313,
              0.26034930198917733
            ]
          ]
        ],
        "vsnon": [
          [
            [
              0.0,
              0.0019752994781107257,
              0.020421161467932235,
              0.18231500761877956,
              3.417817070425085
            ],
            [
              0.002558829070170628,
              0.04642591804295368,
              0.08453430208038736,
              0.053011609212643265,
              0.16052798613321836
            ],
            [
              0.005537052333306855,
              0.07730053090743055,
              0.06981963949185285,
              0.036078876638408676,
              0.05587080548511934
            ],
            [
              0.007358258103351589,
              0.09280017199343121,
              0.0685369544362089,
              0.03715553051049877,
              0.05313362931543603
            ],
            [
              0.01413057165211172,
              0.10680389967046192,
              0.0720580210125999,
              0.04204769642589584,
              0.05728570969849854
            ]
          ],
          [
            [
              0.0,
              0.0027949531841832964,
              0.007229022287709656,
              0.2822000858375975,
              3.004847428368811
            ],
            [
              0.0021453037964992293,
              0.05120365121132793,
              0.07438873060098469,
              0.04896831880001137,
              0.1384948923056299
            ],
            [
              0.006341674700852336,
              0.07948317298760875,
              0.06587530420013424,
              0.03022621513166698,
              0.045065380693348964
            ],
            [
              0.009790021264114329,
              0.09067365685552146,
              0.05976966142045742,
              0.03104546605099247,
              0.04118793098173599
            ],
            [
              0.018987800137287264,
              0.09718454331707943,
              0.060941236218567583,
              0.035454220890101966,
              0.044936863252113435
            ]
          ],
          [
            [
              0.0,
              0.0028994981145980024,
              0.013945776317644876,
              0.22736282514148398,
              3.516254903372643
            ],
            [
              0.00321822271152046,
              0.059757732239091546,
              0.08167056070309638,
              0.04051320512716417,
              0.10489156378478834
            ],
            [
              0.008168142483340798,
              0.07720906990349308,
              0.058888232679579024,
              0.027111166918299907,
              0.039413148002080206
            ],
            [
              0.013560169735333477,
              0.0804038925380842,
              0.04867200453862066,
              0.0265540148118653,
              0.034638293156888475
            ],
            [
              0.023917843356799032,
              0.07889303175975235,
              0.04792495336362836,
              0.02943973746304848,
              0.03689645590603434
            ]
          ]
        ],
        "aTsfcn": [
          [
            [
              -0.021717976711802672,
              -0.10161998246404125,
              -0.22615154049618766,
              -1.2773916555727602,
              -5.995220144299218
            ],
            [
              -0.6112586253800723,
              -0.7380755949537842,
              -0.7619201642094927,
              -0.3223570639825835,
              -0.3050900711419732
            ],
            [
              -0.4191903956932166,
              -0.4062771105630224,
              -0.19062987174644344,
              -0.024237175517468703,
              0.0
            ],
            [
              -0.4327556455678789,
              -0.40479374747051095,
              -0.13075718117425605,
              -0.003100409556771286,
              0.0
            ],
            [
              -0.48145157475841677,
              -0.4425000866762686,
              -0.11529506986992388,
              -0.002593505108219058,
              0.0
            ]
          ],
          [
            [
              -0.04421250198130248,
              -0.15086201124089435,
              -0.1642343721697706,
              -1.728859504987689,
              -5.29270409354885
            ],
            [
              -0.6471595338273431,
              -0.9062475714115071,
              -0.8791522094022818,
              -0.34259725336308916,
              -0.31684028818980076
            ],
            [
              -0.5830670413481303,
              -0.63056342994429,
              -0.3086837344503088,
              -0.0627957620068571,
              -0.010866260040682323
            ],
            [
              -0.6340051237841907,
              -0.6722328743540146,
              -0.22714886111854865,
              -0.048113118400194124,
              -0.003365716406747907
            ],
            [
              -0.646026322436363,
              -0.6530921388208052,
              -0.19463876856292406,
              -0.052425143558409354,
              -0.01725439249773359
            ]
          ],
          [
            [
              -0.030570054919879453,
              -0.11547327851935596,
              -0.16880127008867948,
              -1.4682624775581257,
              -5.544385654745628
            ],
            [
              -0.7009780725054917,
              -1.0665635728684424,
              -0.9489533626867465,
              -0.30329885708416,
              -0.2733245872308772
            ],
            [
              -0.6844113813556131,
              -0.7119800415307307,
              -0.317344037279371,
              -0.06405446616483149,
              -0.014891202246941335
            ],
            [
              -0.7978885265217482,
              -0.7709150190377596,
              -0.2131626917456124,
              -0.05318675453357558,
              -0.011406037492379048
            ],
            [
              -0.8435015666921907,
              -0.7476837969951196,
              -0.18245927374821838,
              -0.060703564824524145,
              -0.02492392613734129
            ]
          ]
        ],
        "vqicen": [
          [
            [
              [
                -840401.8897171413,
                -799775.9468094613,
                -789401.4257972003,
                -801575.0555082781,
                -818608.835845186,
                -828929.3592756338,
                -831369.3374686403,
                -830982.5557329424
              ],
              [
                -4595254.905698941,
                -4579694.031538033,
                -4560734.256277191,
                -4543230.41897954,
                -4521448.35522569,
                -4465616.211125757,
                -4257282.545320706,
                -3732656.7533798395
              ],
              [
                -18782335.89763199,
                -19396942.138504583,
                -19535845.825863633,
                -19738213.994789016,
                -19849584.726707295,
                -19798761.23551538,
                -19082184.490645878,
                -15849981.736432116
              ],
              [
                -164783239.1116205,
                -172173622.81431934,
                -174612907.07348624,
                -175362374.07206678,
                -174938483.38441056,
                -175252412.76641506,
                -168985157.59316164,
                -137125992.00612515
              ],
              [
                -6503995163.779266,
                -4309857487.151828,
                -3130081182.6977587,
                -2683410830.280102,
                -2422528527.499523,
                -2265531562.379854,
                -2173657612.678788,
                -2107143606.2630897
              ]
            ],
            [
              [
                -10432852.176223237,
                -10396280.84455276,
                -10368798.140593432,
                -10341173.996935349,
                -10286159.688450526,
                -10147694.839006647,
                -9675283.135626536,
                -7911287.375100073
              ],
              [
                -55593691.22209769,
                -55423567.54928301,
                -55277499.45468859,
                -55184391.013173774,
                -55149090.64474186,
                -55106984.869100645,
                -54974522.46023473,
                -54065055.451245606
              ],
              [
                -112106010.45634194,
                -111847516.26217063,
                -111750244.98120944,
                -111834128.6642829,
                -112139108.28922832,
                -112205032.31916174,
                -111601874.38872486,
                -108479496.96117604
              ],
              [
                -95860557.34722549,
                -95771350.24626794,
                -95757050.69730073,
                -95748435.02812539,
                -95875433.25612058,
                -96488054.3296963,
                -96839459.18757285,
                -93775479.2264672
              ],
              [
                -431230576.5243692,
                -416990186.14373094,
                -390923547.83883506,
                -367504501.69061244,
                -350968263.26532245,
                -331552536.66320753,
                -293319326.5330899,
                -240967535.29341614
              ]
            ],
            [
              [
                -12947163.344208345,
                -12913041.98696485,
                -12889818.985169359,
                -12868100.335489998,
                -12837415.294962378,
                -12748143.442787986,
                -12390364.122475103,
                -10695359.790903026
              ],
              [
                -80697579.70351961,
                -80408834.3991963,
                -80233231.42364275,
                -80122225.85541499,
                -80080074.79659633,
                -80069790.29613377,
                -79903073.46384016,
                -78419163.1755414
              ],
              [
                -93944868.75762008,
                -93622843.62389532,
                -93519313.76645103,
                -93523977.87625988,
                -93615710.29306142,
                -93619660.82894121,
                -93260514.36962542,
                -90285498.26053497
              ],
              [
                -64370683.08921774,
                -64367464.988550514,
                -64421009.626408696,
                -64482028.35077438,
                -64608591.988935545,
                -64746063.39236251,
                -64631366.77134034,
                -62037570.229927234
              ],
              [
                -128049076.88446994,
                -128025668.29438265,
                -127477903.97349656,
                -126403209.65573843,
                -125025241.76552911,
                -123015356.61112702,
                -116163402.16217194,
                -102392393.5193769
              ]
            ],
            [
              [
                -14130220.356388772,
                -14089572.732046898,
                -14065913.691253014,
                -14045052.574955037,
                -14022595.708179247,
                -13977717.727709055,
                -13783881.188285086,
                -12434863.138225224
              ],
              [
                -91176608.79355465,
                -90818425.55683665,
                -90632177.61725813,
                -90526881.4980869,
                -90499770.33846986,
                -90510164.96384205,
                -90323721.31180046,
                -88475099.63463548
              ],
              [
                -84716848.61498407,
                -84366382.7082614,
                -84293378.59235992,
                -84315239.18667527,
                -84389181.98039854,
                -84425074.21778283,
                -84135291.58772172,
                -81234424.84796469
              ],
              [
                -60722252.4389009,
                -60764559.53426441,
                -60861833.54599863,
                -60962389.45200599,
                -61108098.01813494,
                -61172659.89864085,
                -60841985.724615335,
                -57785848.831375316
              ],
              [
                -114859113.79211964,
                -114983501.13725543,
                -114650187.97022133,
                -113928655.35714968,
                -112965002.29370572,
                -111659969.43018313,
                -107964372.4563222,
                -99781339.86381593
              ]
            ],
            [
              [
                -15273638.149726547,
                -15230768.106261387,
                -15207320.215595169,
                -15192661.830910148,
                -15178707.588698141,
                -15162475.715619612,
                -15130582.246126361,
                -14929387.01237744
              ],
              [
                -101567531.87785995,
                -101246213.40712583,
                -101123833.48882905,
                -101074128.1156927,
                -101093789.54191393,
                -101164496.85310848,
                -101104295.63711335,
                -99363167.00204925
              ],
              [
                -81120848.20088048,
                -80707756.36959437,
                -80683053.00141492,
                -80764356.58648114,
                -80889325.1829233,
                -80985043.35743222,
                -80849559.54401535,
                -78565921.77263717
              ],
              [
                -61842115.58693066,
                -61955379.65456735,
                -62111038.1940656,
                -62276109.22645538,
                -62453855.0447177,
                -62490001.42170706,
                -62080632.85010451,
                -59165817.52036856
              ],
              [
                -115952358.81565422,
                -116293305.61316969,
                -116061288.26521473,
                -115431790.47936249,
                -114607832.28009972,
                -113552174.23836803,
                -110793678.43805721,
                -106289538.36305742
              ]
            ]
          ],
          [
            [
              [
                -1199170.401961563,
                -1085528.182716798,
                -1019660.3789913444,
                -1003091.0600540647,
                -1015226.1130401453,
                -1037204.8627315939,
                -1060781.940312357,
                -1050358.5120354495
              ],
              [
                -7098622.26307887,
                -7073298.199690244,
                -7045846.194490644,
                -7019110.583027952,
                -6980712.290185307,
                -6883156.275007456,
                -6532697.569073759,
                -5567392.361789796
              ],
              [
                -11805023.753168318,
                -11778066.205410775,
                -11797497.334251408,
                -11855625.570461981,
                -11882102.019818248,
                -11719951.66522943,
                -11204058.425458577,
                -9117649.014923206
              ],
              [
                -270892996.09454507,
                -284509675.9568004,
                -288065236.8727332,
                -288024017.0351815,
                -286660469.96556866,
                -228458601.42049795,
                -192465171.3766238,
                -180984258.61059192
              ],
              [
                -5908795584.59633,
                -3919538636.3374753,
                -2865408064.436459,
                -2454228267.717346,
                -2203636040.3337216,
                -2046927082.2421014,
                -1954771794.6842866,
                -1891743909.9156578
              ]
            ],
            [
              [
                -10218178.686780633,
                -10183538.583008615,
                -10151338.256760377,
                -10108290.410850914,
                -10020758.41755388,
                -9837173.595887935,
                -9256346.289303774,
                -7306670.697551327
              ],
              [
                -61587365.55448884,
                -61397671.208748005,
                -61230695.40727668,
                -61119578.03306166,
                -61067243.86965092,
                -61009770.18216971,
                -60890576.75825761,
                -59748767.06645529
              ],
              [
                -105170270.75149637,
                -104838026.83215012,
                -104673022.80625026,
                -104692897.50207904,
                -104921861.48053183,
                -104869245.85092363,
                -104375325.02887894,
                -101723337.8144425
              ],
              [
                -90452102.80885424,
                -90350710.29127291,
                -90322077.39067963,
                -90290201.89872384,
                -90363926.3837383,
                -90955648.44140805,
                -91347293.49499328,
                -89246486.6704281
              ],
              [
                -347048365.0414372,
                -332997644.89005613,
                -314719249.1264372,
                -300541270.8297463,
                -289941962.50490403,
                -277748160.1170192,
                -244390952.79442272,
                -202143881.85728422
              ]
            ],
            [
              [
                -14647809.764187986,
                -14609589.876055261,
                -14581024.583379453,
                -14551394.616920259,
                -14504165.429110127,
                -14373552.969599027,
                -13876010.070293108,
                -11542968.167996675
              ],
              [
                -82596908.89133522,
                -82291250.03154168,
                -82091449.16208865,
                -81957214.15254311,
                -81896760.65356404,
                -81881344.22654615,
                -81748873.9914063,
                -80137279.65486026
              ],
              [
                -86510912.21057266,
                -86180332.61989687,
                -86055999.34532349,
                -86044555.12337816,
                -86113260.96768565,
                -86131150.75119625,
                -85946566.84830809,
                -83527718.8823641
              ],
              [
                -52976674.94680014,
                -52963270.74177946,
                -53007885.409884386,
                -53062060.8970684,
                -53171366.708010666,
                -53268925.910473175,
                -53196606.55345878,
                -51406101.48594145
              ],
              [
                -103690794.29679528,
                -103755104.62708916,
                -103369938.91228688,
                -102618775.8536445,
                -101656363.57857254,
                -100251431.80496264,
                -96125688.6942631,
                -87528748.22365694
              ]
            ],
            [
              [
                -16675181.38681465,
                -16628744.850558283,
                -16598746.505807387,
                -16571580.318925686,
                -16541309.994898139,
                -16490657.092490261,
                -16293272.308126545,
                -14850357.576350395
              ],
              [
                -90042548.65196298,
                -89701831.7126996,
                -89493913.05979949,
                -89358193.47417109,
                -89289116.3881598,
                -89271061.39250286,
                -89135341.71326347,
                -87283269.56166248
              ],
              [
                -72002743.04070368,
                -71672691.18576287,
                -71588858.05804485,
                -71586371.50654794,
                -71630702.71991329,
                -71670552.29908851,
                -71556582.87148294,
                -69538443.51635951
              ],
              [
                -50100397.1120298,
                -50116778.47025126,
                -50184227.01105341,
                -50254293.71263427,
                -50348759.82466129,
                -50366877.36832833,
                -50107711.22995313,
                -47972363.074878916
              ],
              [
                -88973720.74542566,
                -89071063.39470844,
                -88846405.67833,
                -88369138.3886079,
                -87742792.99303815,
                -86890435.48004295,
                -84776904.59833507,
                -81208075.76703653
              ]
            ],
            [
              [
                -19477862.579419736,
                -19420437.314199932,
                -19392875.230987,
                -19374112.200728092,
                -19354570.84200634,
                -19331020.48522411,
                -19289994.49734759,
                -19058025.31322311
              ],
              [
                -96089269.8178392,
                -95571630.50022957,
                -95387925.69261575,
                -95279293.28435771,
                -95247022.49139887,
                -95289228.18171395,
                -95264221.30908692,
                -93521666.22099723
              ],
              [
                -67648939.59471054,
                -67237942.3568092,
                -67199843.15647447,
                -67258443.34573455,
                -67360481.97713985,
                -67453005.0175906,
                -67429369.716663,
                -65853534.84343378
              ],
              [
                -52474535.55507591,
                -52553490.82962919,
                -52670826.51155451,
                -52785414.80518407,
                -52890862.36238682,
                -52896063.768226765,
                -52573215.58542915,
                -50413833.526289314
              ],
              [
                -91900368.91106378,
                -92160742.62411153,
                -91983306.3987007,
                -91528231.74565685,
                -90935656.68059166,
                -90175086.37131187,
                -88362280.49961849,
                -86834511.77370697
              ]
            ]
          ],
          [
            [
              [
                -781941.0402300645,
                -698351.5252179785,
                -642192.5463421101,
                -621039.0378407734,
                -628355.9919354127,
                -651097.0201143615,
                -676718.2201830432,
                -667058.038609974
              ],
              [
                -5295455.400934453,
                -5276153.277599973,
                -5256981.484535906,
                -5241579.23564081,
                -5225759.569012416,
                -5195869.969069285,
                -5064891.3559957035,
                -4492769.688973042
              ],
              [
                -13065045.616318801,
                -13200717.637207404,
                -13273438.816140627,
                -13377630.589092517,
                -13434721.959323991,
                -13422636.950439297,
                -13084286.886307519,
                -11486967.936607689
              ],
              [
                -202356140.89851356,
                -211661283.18359053,
                -214874947.9250611,
                -215537235.99285567,
                -214611717.54745317,
                -216382179.89645138,
                -213411899.815907,
                -186190974.67547882
              ],
              [
                -5702874788.593353,
                -4666496124.478456,
                -3106358045.9191513,
                -2595748952.9532747,
                -2323858831.4628954,
                -2159881196.417767,
                -2065751943.6574538,
                -2002916620.172001
              ]
            ],
            [
              [
                -10967048.983863253,
                -10932735.365572821,
                -10900678.369906323,
                -10863181.31410115,
                -10794670.021016235,
                -10650686.223160876,
                -10171080.395380756,
                -8304690.127443275
              ],
              [
                -69018792.7472379,
                -68799543.4834947,
                -68602014.11187638,
                -68464473.26495071,
                -68396258.66883378,
                -68336387.14736478,
                -68215093.51891415,
                -66794973.919219665
              ],
              [
                -109187179.55717012,
                -108847811.48504616,
                -108657343.87194774,
                -108645904.71505557,
                -108835197.544752,
                -108774415.46998997,
                -108404127.05731107,
                -105358940.22241463
              ],
              [
                -75305398.62655127,
                -75220297.19662912,
                -75241742.24703382,
                -75278697.2791563,
                -75400605.50633653,
                -75963790.82563043,
                -76342227.18004753,
                -74440752.83927129
              ],
              [
                -249141464.2762127,
                -245366463.3214187,
                -238343499.68315682,
                -231291377.5432473,
                -225234967.05836195,
                -218471099.92200783,
                -197751107.92463017,
                -163550728.14496914
              ]
            ],
            [
              [
                -16854028.164683573,
                -16808120.460921504,
                -16773535.044670694,
                -16739463.634994423,
                -16694677.256191796,
                -16582598.040377332,
                -16132958.25104308,
                -13563626.815968588
              ],
              [
                -82323042.88192779,
                -82018385.28493148,
                -81810568.90859401,
                -81664925.56867452,
                -81585026.4568064,
                -81547115.49009703,
                -81417483.7819728,
                -79824862.24338788
              ],
              [
                -78868293.08442569,
                -78519270.38537394,
                -78382636.6252982,
                -78345807.46409012,
                -78392563.23955092,
                -78393458.2994331,
                -78274533.27570257,
                -76313156.26034339
              ],
              [
                -47998554.65475757,
                -47974759.26863289,
                -48015730.72745879,
                -48065601.303556874,
                -48158834.08000024,
                -48255740.022520125,
                -48168839.16411424,
                -46712654.07557465
              ],
              [
                -92644821.12905303,
                -92651770.97735141,
                -92336262.10667807,
                -91713309.32774077,
                -90897570.77905652,
                -89672066.6926041,
                -86186763.74970923,
                -79520128.31824566
              ]
            ],
            [
              [
                -20469180.132931445,
                -20409737.54985665,
                -20370118.00501146,
                -20333783.686539076,
                -20295981.70841096,
                -20245782.31323518,
                -20147430.55470873,
                -19286303.403257325
              ],
              [
                -84984700.69694574,
                -84625720.3180103,
                -84403794.80043086,
                -84247699.5152962,
                -84154254.84741487,
                -84106716.89582352,
                -83942039.41012502,
                -82144981.10615684
              ],
              [
                -59023711.706624895,
                -58702831.892666675,
                -58614204.149872445,
                -58597579.68812508,
                -58625908.63055971,
                -58660221.0574355,
                -58606546.92486155,
                -57051570.83726285
              ],
              [
                -43820429.54098628,
                -43819860.1542376,
                -43868162.47140647,
                -43915086.04226908,
                -43975378.63661345,
                -43980559.17194212,
                -43758573.33973983,
                -42106411.39701003
              ],
              [
                -77046678.06934498,
                -77131262.56047592,
                -76930428.207685,
                -76536316.2516436,
                -76004663.22418858,
                -75253822.73802224,
                -73509315.06211056,
                -70914528.8987754
              ]
            ],
            [
              [
                -25512906.26486944,
                -25380863.56394043,
                -25338539.92635494,
                -25303793.264674146,
                -25263140.722454395,
                -25217597.34254719,
                -25154670.348306447,
                -24915373.59556101
              ],
              [
                -86526194.25619057,
                -85848569.90105335,
                -85558483.85114418,
                -85384595.67116667,
                -85302202.15538557,
                -85300463.12699011,
                -85219800.73534927,
                -83496964.73566929
              ],
              [
                -53393179.149768226,
                -52970585.05732317,
                -52924449.180576034,
                -52966846.23689584,
                -53046128.49220404,
                -53128032.28421795,
                -53130060.07842586,
                -51852941.2445752
              ],
              [
                -45129548.96910632,
                -45177891.73492565,
                -45266839.209436774,
                -45340471.897512846,
                -45399676.19962007,
                -45394633.550057165,
                -45142601.067390524,
                -43421693.79640455
              ],
              [
                -78023329.72604473,
                -78240164.59269425,
                -78096149.84544067,
                -77724166.09514564,
                -77230509.91265643,
                -76581642.60638927,
                -75098540.49867648,
                -73897369.71329607
              ]
            ]
          ]
        ],
        "vsqsnon": [
          [
            [
              [
                -0.0,
                -0.0,
                -0.0
              ],
              [
                -228077.60741710462,
                -225741.11591776772,
                -223825.43340397565
              ],
              [
                -2345682.672652044,
                -2323827.6654540505,
                -2299054.5692239273
              ],
              [
                -20867327.21285367,
                -20654914.209202327,
                -20464766.02556566
              ],
              [
                -386807284.8800406,
                -398429968.83311826,
                -389899685.46096516
              ]
            ],
            [
              [
                -287267.0615271591,
                -287114.2372761386,
                -287002.6406234271
              ],
              [
                -5324522.270618363,
                -5277782.539257822,
                -5239742.409845638
              ],
              [
                -9708062.775313621,
                -9644837.481897773,
                -9579959.196080929
              ],
              [
                -6100432.376668138,
                -6078873.206623548,
                -6040886.509033151
              ],
              [
                -18395012.873921648,
                -18313427.935073864,
                -18251630.161397282
              ]
            ],
            [
              [
                -617303.0000742907,
                -618530.6183858671,
                -619490.4064006031
              ],
              [
                -8826224.81723915,
                -8768154.088848503,
                -8707677.159283541
              ],
              [
                -7987567.542615335,
                -7944923.710410383,
                -7896953.950933213
              ],
              [
                -4139606.3487960435,
                -4131593.004429046,
                -4112190.4280268033
              ],
              [
                -6409546.701187743,
                -6401000.762793098,
                -6389744.251738962
              ]
            ],
            [
              [
                -821091.6642013096,
                -823098.3855680078,
                -824307.9483846753
              ],
              [
                -10594015.326807007,
                -10522042.899548996,
                -10445299.435327353
              ],
              [
                -7838155.453928616,
                -7793908.686064599,
                -7741956.002830214
              ],
              [
                -4261368.82719202,
                -4251756.486962299,
                -4232405.656195697
              ],
              [
                -6089080.061578252,
                -6080397.59008385,
                -6074557.855534459
              ]
            ],
            [
              [
                -1586218.7980916982,
                -1589375.0436127195,
                -1586806.5657917701
              ],
              [
                -12146860.51756698,
                -12068649.390174203,
                -11992460.171315292
              ],
              [
                -8201748.510666547,
                -8156103.445447415,
                -8113481.931349336
              ],
              [
                -4794243.226053641,
                -4790382.801840557,
                -4780280.461079522
              ],
              [
                -6520908.1773999175,
                -6527163.15969073,
                -6534639.376093925
              ]
            ]
          ],
          [
            [
              [
                -0.0,
                -0.0,
                -0.0
              ],
              [
                -323399.6475467407,
                -320245.13036540314,
                -317422.77829419816
              ],
              [
                -835175.8030104431,
                -825687.5563267942,
                -819614.4188737138
              ],
              [
                -32302741.92872612,
                -31948005.521941956,
                -31650122.799200375
              ],
              [
                -339546565.63310844,
                -348987155.93675673,
                -342109971.61108863
              ]
            ],
            [
              [
                -241114.51443624694,
                -240957.85114545128,
                -240841.66597850958
              ],
              [
                -5889572.740137445,
                -5831708.594572166,
                -5784292.407360352
              ],
              [
                -8566019.912051119,
                -8494644.969985977,
                -8433459.574194666
              ],
              [
                -5649343.300510429,
                -5623114.762978723,
                -5585176.956278848
              ],
              [
                -15903622.592251947,
                -15822633.520843772,
                -15760223.967801431
              ]
            ],
            [
              [
                -708826.2533758713,
                -709889.5441244569,
                -710629.6745273214
              ],
              [
                -9098774.403663661,
                -9029420.903458597,
                -8959235.737673098
              ],
              [
                -7554973.816088107,
                -7505844.257790536,
                -7453263.7187585095
              ],
              [
                -3476253.357477517,
                -3465654.1293410333,
                -3446914.9977460774
              ],
              [
                -5181147.018295876,
                -5171058.375510745,
                -5159963.862605571
              ]
            ],
            [
              [
                -1096359.2208451058,
                -1098361.9802233083,
                -1098877.2547983103
              ],
              [
                -10371011.434390577,
                -10293322.335617997,
                -10212625.914134786
              ],
              [
                -6848668.2920579715,
                -6804360.480392354,
                -6753827.453363523
              ],
              [
                -3567185.6396542536,
                -3556316.9864835762,
                -3538044.268155279
              ],
              [
                -4729179.712153855,
                -4720663.2608271595,
                -4713285.776564051
              ]
            ],
            [
              [
                -2134222.3887466094,
                -2136456.4884830466,
                -2132377.238394453
              ],
              [
                -11030067.159767956,
                -10977949.042640068,
                -10914475.96974234
              ],
              [
                -6927923.395083754,
                -6899841.221077107,
                -6862848.210943824
              ],
              [
                -4042030.1458532354,
                -4042356.064790249,
                -4031979.635984267
              ],
              [
                -5119111.397218351,
                -5125210.3404622665,
                -5127744.780362084
              ]
            ]
          ],
          [
            [
              [
                -0.0,
                -0.0,
                -0.0
              ],
              [
                -335920.76803162135,
                -331801.93190180324,
                -328646.21473450994
              ],
              [
                -1610191.4727239832,
                -1593556.6112918074,
                -1576129.8753829931
              ],
              [
                -26101972.013085306,
                -25791201.983447198,
                -25522962.66133886
              ],
              [
                -398424042.49155974,
                -411137338.88533336,
                -401927138.7417277
              ]
            ],
            [
              [
                -362423.9673484103,
                -362188.86192519777,
                -361975.466602061
              ],
              [
                -6889810.078799112,
                -6816214.965681335,
                -6754004.329958486
              ],
              [
                -9425696.840948634,
                -9338273.141627274,
                -9261507.219462924
              ],
              [
                -4684917.2390225865,
                -4658106.615322498,
                -4625172.412449993
              ],
              [
                -12088679.809961205,
                -12034827.27703668,
                -11995054.958128754
              ]
            ],
            [
              [
                -914083.1904760957,
                -915572.9464241395,
                -916366.0994463159
              ],
              [
                -8852822.28153452,
                -8782242.273344183,
                -8708125.85923766
              ],
              [
                -6764953.466571036,
                -6715213.677342338,
                -6663952.344498958
              ],
              [
                -3122500.5281349355,
                -3110150.2054641335,
                -3092333.503417192
              ],
              [
                -4537351.54269973,
                -4526855.888706123,
                -4517011.434271229
              ]
            ],
            [
              [
                -1523025.5747026852,
                -1525735.1994540999,
                -1525082.2940737298
              ],
              [
                -9209271.602907386,
                -9139479.418482045,
                -9062841.677769154
              ],
              [
                -5586143.659063802,
                -5545720.870469813,
                -5501094.017370067
              ],
              [
                -3055437.6785676563,
                -3043567.9362639883,
                -3026586.3061724147
              ],
              [
                -3982779.4899062477,
                -3973414.355581403,
                -3965625.1610290166
              ]
            ],
            [
              [
                -2694097.4942548363,
                -2696753.0095462087,
                -2690431.5593282473
              ],
              [
                -8970024.026465353,
                -8928557.768142305,
                -8871474.963828566
              ],
              [
                -5465104.048570452,
                -5440365.19236393,
                -5403064.3928901795
              ],
              [
                -3368183.60400094,
                -3363982.8971396536,
                -3349980.6609438662
              ],
              [
                -4218466.6696170475,
                -4214967.121804694,
                -4212472.108673653
              ]
            ]
          ]
        ]
      },
      "parameter_overrides": {
        "uvel": [
          [
            0.00012200831259922484,
            -0.00430503734325033,
            -0.006404552971129575,
            -0.0029079564379971357,
            -0.0037366886985347827
          ],
          [
            1.349728123413932e-05,
            -0.0049893802525858445,
            -0.006556908183432414,
            -0.004013004944111566,
            -0.0042590499452267415
          ],
          [
            0.0,
            -0.006049027918925767,
            -0.0058923320164812176,
            -0.0045391275967812655,
            -0.004738980872614332
          ]
        ],
        "vvel": [
          [
            0.0007204892821085377,
            0.0007865942006418693,
            0.0037168927343423233,
            0.013900356415145056,
            0.015928611364519916
          ],
          [
            0.0009977387642852074,
            0.001620845665338858,
            0.00661497866621736,
            0.011651221033965178,
            0.012191539845748306
          ],
          [
            0.0,
            0.003975027437344815,
            0.009118244672511678,
            0.01094051866825294,
            0.010805999470988786
          ]
        ],
        "HTE": [
          [
            59395.455016421605,
            59395.455016421605,
            59395.455016421605,
            59395.455016421605,
            59395.455016421605
          ],
          [
            59395.455016421605,
            59395.455016421605,
            59395.455016421605,
            59395.455016421605,
            59395.455016421605
          ],
          [
            59395.455016421605,
            59395.455016421605,
            59395.455016421605,
            59395.455016421605,
            59395.455016421605
          ]
        ],
        "HTN": [
          [
            26251.235254161526,
            27390.328313754686,
            28527.04003199235,
            29661.271582069905,
            30792.92435281096
          ],
          [
            26251.235254161526,
            27390.328313754686,
            28527.04003199235,
            29661.271582069905,
            30792.92435281096
          ],
          [
            26251.235254161526,
            27390.328313754686,
            28527.04003199235,
            29661.271582069905,
            30792.92435281096
          ]
        ],
        "tarea": [
          [
            1525307808.0270946,
            1593032537.954344,
            1660618768.108248,
            1728060622.4772792,
            1795352237.6020775
          ],
          [
            1525307808.0270946,
            1593032537.954344,
            1660618768.108248,
            1728060622.4772792,
            1795352237.6020775
          ],
          [
            1525307808.0270946,
            1593032537.954344,
            1660618768.108248,
            1728060622.4772792,
            1795352237.6020775
          ]
        ]
      },
      "assertions": [
        {
          "variable": "div_flux",
          "time": 0.0,
          "expected": 3.892471770783875e-08,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 2
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_flux",
          "time": 0.0,
          "expected": -6.544266967290097e-09,
          "coords": {
            "i": 2,
            "j": 5,
            "ncat": 1
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_flux",
          "time": 0.0,
          "expected": -4.2036875555027334e-09,
          "coords": {
            "i": 1,
            "j": 1,
            "ncat": 5
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_flux_v",
          "time": 0.0,
          "expected": 4.287439225874571e-08,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 5
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_flux_v",
          "time": 0.0,
          "expected": 9.64740429045927e-09,
          "coords": {
            "i": 2,
            "j": 5,
            "ncat": 5
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_flux_v",
          "time": 0.0,
          "expected": -1.292670165745469e-07,
          "coords": {
            "i": 1,
            "j": 1,
            "ncat": 5
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_flux_s",
          "time": 0.0,
          "expected": 1.2485747917546644e-08,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 2
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_flux_s",
          "time": 0.0,
          "expected": 2.7743585198569155e-09,
          "coords": {
            "i": 2,
            "j": 5,
            "ncat": 2
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_flux_s",
          "time": 0.0,
          "expected": -2.1176113145429363e-08,
          "coords": {
            "i": 1,
            "j": 1,
            "ncat": 5
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_aTsfcn",
          "time": 0.0,
          "expected": -4.48741456798781e-08,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 2
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_aTsfcn",
          "time": 0.0,
          "expected": 1.9244347090878233e-08,
          "coords": {
            "i": 2,
            "j": 5,
            "ncat": 1
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_aTsfcn",
          "time": 0.0,
          "expected": 3.6947478612703936e-08,
          "coords": {
            "i": 1,
            "j": 1,
            "ncat": 5
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_vqicen",
          "time": 0.0,
          "expected": -12.848701701761971,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 5,
            "ice_layer": 1
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_vqicen",
          "time": 0.0,
          "expected": -2.8705339849361082,
          "coords": {
            "i": 2,
            "j": 5,
            "ncat": 5,
            "ice_layer": 1
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_vqicen",
          "time": 0.0,
          "expected": 39.06487182418549,
          "coords": {
            "i": 1,
            "j": 1,
            "ncat": 5,
            "ice_layer": 1
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_vqicen",
          "time": 0.0,
          "expected": -12.882249998928307,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 5,
            "ice_layer": 2
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_vqicen",
          "time": 0.0,
          "expected": -2.895969174718097,
          "coords": {
            "i": 2,
            "j": 5,
            "ncat": 5,
            "ice_layer": 2
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_vqicen",
          "time": 0.0,
          "expected": 25.062873791354782,
          "coords": {
            "i": 1,
            "j": 1,
            "ncat": 5,
            "ice_layer": 2
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_vqicen",
          "time": 0.0,
          "expected": -12.858161545157724,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 5,
            "ice_layer": 3
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_vqicen",
          "time": 0.0,
          "expected": -2.8951057885576623,
          "coords": {
            "i": 2,
            "j": 5,
            "ncat": 5,
            "ice_layer": 3
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_vqicen",
          "time": 0.0,
          "expected": 17.611433804053608,
          "coords": {
            "i": 1,
            "j": 1,
            "ncat": 5,
            "ice_layer": 3
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_vqicen",
          "time": 0.0,
          "expected": -12.791529765101025,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 5,
            "ice_layer": 4
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_vqicen",
          "time": 0.0,
          "expected": -2.8807392601901554,
          "coords": {
            "i": 2,
            "j": 5,
            "ncat": 5,
            "ice_layer": 4
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_vqicen",
          "time": 0.0,
          "expected": 14.902979408829298,
          "coords": {
            "i": 1,
            "j": 1,
            "ncat": 5,
            "ice_layer": 4
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_vqicen",
          "time": 0.0,
          "expected": -12.703568766087946,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 5,
            "ice_layer": 5
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_vqicen",
          "time": 0.0,
          "expected": -2.862946827133984,
          "coords": {
            "i": 2,
            "j": 5,
            "ncat": 5,
            "ice_layer": 5
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_vqicen",
          "time": 0.0,
          "expected": 13.363596391729038,
          "coords": {
            "i": 1,
            "j": 1,
            "ncat": 5,
            "ice_layer": 5
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_vqicen",
          "time": 0.0,
          "expected": -12.59594534013368,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 5,
            "ice_layer": 6
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_vqicen",
          "time": 0.0,
          "expected": -2.8463706740231296,
          "coords": {
            "i": 2,
            "j": 5,
            "ncat": 5,
            "ice_layer": 6
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_vqicen",
          "time": 0.0,
          "expected": 12.509912303282936,
          "coords": {
            "i": 1,
            "j": 1,
            "ncat": 5,
            "ice_layer": 6
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_vqicen",
          "time": 0.0,
          "expected": -12.317042375660279,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 5,
            "ice_layer": 7
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_vqicen",
          "time": 0.0,
          "expected": -2.7978499471187406,
          "coords": {
            "i": 2,
            "j": 5,
            "ncat": 5,
            "ice_layer": 7
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_vqicen",
          "time": 0.0,
          "expected": 12.178009498737927,
          "coords": {
            "i": 1,
            "j": 1,
            "ncat": 5,
            "ice_layer": 7
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_vqicen",
          "time": 0.0,
          "expected": -11.89639566073597,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 5,
            "ice_layer": 8
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_vqicen",
          "time": 0.0,
          "expected": -2.8225112174565834,
          "coords": {
            "i": 2,
            "j": 5,
            "ncat": 5,
            "ice_layer": 8
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_vqicen",
          "time": 0.0,
          "expected": 12.081922866704648,
          "coords": {
            "i": 1,
            "j": 1,
            "ncat": 5,
            "ice_layer": 8
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_vsqsnon",
          "time": 0.0,
          "expected": -1.415579309253335,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 2,
            "snow_layer": 1
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_vsqsnon",
          "time": 0.0,
          "expected": -0.30672914769492526,
          "coords": {
            "i": 2,
            "j": 5,
            "ncat": 2,
            "snow_layer": 1
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_vsqsnon",
          "time": 0.0,
          "expected": 2.3964139086440306,
          "coords": {
            "i": 1,
            "j": 1,
            "ncat": 5,
            "snow_layer": 1
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_vsqsnon",
          "time": 0.0,
          "expected": -1.4090355105502164,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 2,
            "snow_layer": 2
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_vsqsnon",
          "time": 0.0,
          "expected": -0.30710034187913215,
          "coords": {
            "i": 2,
            "j": 5,
            "ncat": 2,
            "snow_layer": 2
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_vsqsnon",
          "time": 0.0,
          "expected": 2.474163621435436,
          "coords": {
            "i": 1,
            "j": 1,
            "ncat": 5,
            "snow_layer": 2
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_vsqsnon",
          "time": 0.0,
          "expected": -1.4013531157059052,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 2,
            "snow_layer": 3
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_vsqsnon",
          "time": 0.0,
          "expected": -0.30758137765840593,
          "coords": {
            "i": 2,
            "j": 5,
            "ncat": 2,
            "snow_layer": 3
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        },
        {
          "variable": "div_vsqsnon",
          "time": 0.0,
          "expected": 2.4177323038374254,
          "coords": {
            "i": 1,
            "j": 1,
            "ncat": 5,
            "snow_layer": 3
          },
          "tolerance": {
            "rel": 1e-12,
            "abs": 0.0
          }
        }
      ]
    },
    {
      "id": "cice_transport_centered_flux_35_integrated",
      "description": "Integrated scheme-difference check of the traced step-1 transport over [0, 3600] s at one interior cell -- NOT a pin of CICE's incremental remapping. The continuity system is integrated from the transport dump's t_entr state (the initial_conditions aicen/vicen/vsnon) with the dump's velocity and grid parameters (uvel/vvel = the t_entr step-1 ncat-1 rows; HTE/HTN/tarea from the stress-dump metrics) using the rule's CENTERED face-average flux divergence, and the state at local cell (2,4) = global (3,7), t = 3600 s, is compared against the dump's t_exit state, which the Fortran produced with the incremental-remapping departure-cell integrals (transport_integrals, ice_transport_remap.F90:3188-3472). The two schemes differ at O(C*Delta c): the measured residuals are aicen rel <= 3.04e-5, vicen rel <= 3.33e-5, vsnon rel <= 1.78e-4 over the five categories, while the entry-to-exit change at this cell is only ~3e-4..5.5e-4 relative -- i.e. the residual is ~10% of the transported change, and the tolerances rel 1e-4 / 1e-4 / 2e-4 are loose relative to that change (they are the observed scheme residual rounded up, not a numerical-accuracy statement: a model that transported nothing would miss the aicen/vicen exit values by ~3e-4..5.5e-4, i.e. 3-5x the tolerance, so the test still discriminates transport from no transport, but it cannot distinguish the centered scheme from a ~10%-different one). The centered scheme carries no positivity or monotonicity guarantee (see the file description and README.md 'Transport scheme'); this interior cell has smooth fields, so no negative values arise here. The expected values are the dump's t_exit rows for cell (3,7).",
      "time_span": {
        "start": 0.0,
        "end": 3600.0
      },
      "initial_conditions": {
        "aicen": [
          [
            [
              0.009853548870050664,
              0.012856324595003365,
              0.029676941490770437,
              0.16811440592585572,
              0.7737911360216866
            ],
            [
              0.19517590526067544,
              0.17517092814581073,
              0.20299967624466317,
              0.09250674814792506,
              0.12164352345239411
            ],
            [
              0.24010745627023652,
              0.2634716864755195,
              0.17913714386260754,
              0.06250924884224413,
              0.055099641785219235
            ],
            [
              0.24279805104338764,
              0.3006214819690576,
              0.16436715629707735,
              0.05921139667196378,
              0.051256324337174905
            ],
            [
              0.21446261957461704,
              0.3380275433857241,
              0.16112887904267895,
              0.06074578363509802,
              0.05272893334174682
            ]
          ],
          [
            [
              0.020000787893919705,
              0.018691298764765496,
              0.02123405723287625,
              0.2325823474953262,
              0.7062726776408558
            ],
            [
              0.1951085551827879,
              0.19103150780464098,
              0.19874511294878222,
              0.0852676614296998,
              0.10443105537326039
            ],
            [
              0.2665650105082223,
              0.2729606621507003,
              0.16782172397858613,
              0.05190504256475333,
              0.04559080814091524
            ],
            [
              0.2711227454925614,
              0.3055903706996223,
              0.1412717592470561,
              0.04939762562994809,
              0.040677317264858584
            ],
            [
              0.25048328256606534,
              0.3314283920301694,
              0.13476490615446873,
              0.05200182928019541,
              0.042383130922557063
            ]
          ],
          [
            [
              0.014548532518963476,
              0.014380833122369022,
              0.02220597912138724,
              0.1984707738728337,
              0.7493379585660391
            ],
            [
              0.19336284155326217,
              0.2162321165560872,
              0.2086988498366698,
              0.07229635067222134,
              0.08562040148508959
            ],
            [
              0.293731361151834,
              0.2767298787967303,
              0.15421663268947136,
              0.04716294309980759,
              0.04080758394240371
            ],
            [
              0.29902010258623624,
              0.297339158557214,
              0.11593803015640608,
              0.04344629470278152,
              0.035326077885262035
            ],
            [
              0.29693728359561494,
              0.3099293559893525,
              0.10537286140183962,
              0.044948070262977986,
              0.03608739625384745
            ]
          ]
        ],
        "vicen": [
          [
            [
              0.0033680184834617927,
              0.015542052227473355,
              0.06637765750622569,
              0.590810760871143,
              21.61213381468219
            ],
            [
              0.03492051855887914,
              0.1881462069722783,
              0.3803456398502473,
              0.32465543818502113,
              1.449938023658202
            ],
            [
              0.043483558783242754,
              0.27351867543189595,
              0.3192183512775029,
              0.21711473196953432,
              0.4267481976542756
            ],
            [
              0.04744904191254742,
              0.30927223432872736,
              0.28851115698570634,
              0.20480394767022725,
              0.3826462618653526
            ],
            [
              0.05151143940340013,
              0.3462557318196647,
              0.27725715110715127,
              0.2089216567907939,
              0.38686182855482437
            ]
          ],
          [
            [
              0.005398374149404335,
              0.02394414626491763,
              0.039941722338436514,
              0.9742070459848247,
              19.818005707722715
            ],
            [
              0.034089423501091495,
              0.20815847329100748,
              0.35599580221040084,
              0.3057541297880248,
              1.1667404164975148
            ],
            [
              0.049043930583768804,
              0.2794514836874194,
              0.2938193131598404,
              0.17852188658136484,
              0.34522466795247597
            ],
            [
              0.05587368765282823,
              0.3046830908131356,
              0.24501371039941883,
              0.16882628186138604,
              0.29618372127005743
            ],
            [
              0.06560408395072942,
              0.32609147007145284,
              0.23103593019886898,
              0.17724136576899244,
              0.30663221048100014
            ]
          ],
          [
            [
              0.003501282429120844,
              0.01786491306444554,
              0.04490947585209308,
              0.7286779809238466,
              18.89132406691435
            ],
            [
              0.03649673531868588,
              0.23309953928407742,
              0.3695943628273455,
              0.25387709158198946,
              0.8301563230719655
            ],
            [
              0.05636266355870376,
              0.27807881312680083,
              0.267696453134157,
              0.16166773031800252,
              0.3080507749868207
            ],
            [
              0.06850917717924364,
              0.28674649365747185,
              0.20070170993414216,
              0.14766212029151474,
              0.25643875495901225
            ],
            [
              0.08541943356949086,
              0.29183452966561274,
              0.18211636343675705,
              0.1525079186388313,
              0.26034930198917733
            ]
          ]
        ],
        "vsnon": [
          [
            [
              0.0,
              0.0019752994781107257,
              0.020421161467932235,
              0.18231500761877956,
              3.417817070425085
            ],
            [
              0.002558829070170628,
              0.04642591804295368,
              0.08453430208038736,
              0.053011609212643265,
              0.16052798613321836
            ],
            [
              0.005537052333306855,
              0.07730053090743055,
              0.06981963949185285,
              0.036078876638408676,
              0.05587080548511934
            ],
            [
              0.007358258103351589,
              0.09280017199343121,
              0.0685369544362089,
              0.03715553051049877,
              0.05313362931543603
            ],
            [
              0.01413057165211172,
              0.10680389967046192,
              0.0720580210125999,
              0.04204769642589584,
              0.05728570969849854
            ]
          ],
          [
            [
              0.0,
              0.0027949531841832964,
              0.007229022287709656,
              0.2822000858375975,
              3.004847428368811
            ],
            [
              0.0021453037964992293,
              0.05120365121132793,
              0.07438873060098469,
              0.04896831880001137,
              0.1384948923056299
            ],
            [
              0.006341674700852336,
              0.07948317298760875,
              0.06587530420013424,
              0.03022621513166698,
              0.045065380693348964
            ],
            [
              0.009790021264114329,
              0.09067365685552146,
              0.05976966142045742,
              0.03104546605099247,
              0.04118793098173599
            ],
            [
              0.018987800137287264,
              0.09718454331707943,
              0.060941236218567583,
              0.035454220890101966,
              0.044936863252113435
            ]
          ],
          [
            [
              0.0,
              0.0028994981145980024,
              0.013945776317644876,
              0.22736282514148398,
              3.516254903372643
            ],
            [
              0.00321822271152046,
              0.059757732239091546,
              0.08167056070309638,
              0.04051320512716417,
              0.10489156378478834
            ],
            [
              0.008168142483340798,
              0.07720906990349308,
              0.058888232679579024,
              0.027111166918299907,
              0.039413148002080206
            ],
            [
              0.013560169735333477,
              0.0804038925380842,
              0.04867200453862066,
              0.0265540148118653,
              0.034638293156888475
            ],
            [
              0.023917843356799032,
              0.07889303175975235,
              0.04792495336362836,
              0.02943973746304848,
              0.03689645590603434
            ]
          ]
        ]
      },
      "parameter_overrides": {
        "uvel": [
          [
            0.00012200831259922484,
            -0.00430503734325033,
            -0.006404552971129575,
            -0.0029079564379971357,
            -0.0037366886985347827
          ],
          [
            1.349728123413932e-05,
            -0.0049893802525858445,
            -0.006556908183432414,
            -0.004013004944111566,
            -0.0042590499452267415
          ],
          [
            0.0,
            -0.006049027918925767,
            -0.0058923320164812176,
            -0.0045391275967812655,
            -0.004738980872614332
          ]
        ],
        "vvel": [
          [
            0.0007204892821085377,
            0.0007865942006418693,
            0.0037168927343423233,
            0.013900356415145056,
            0.015928611364519916
          ],
          [
            0.0009977387642852074,
            0.001620845665338858,
            0.00661497866621736,
            0.011651221033965178,
            0.012191539845748306
          ],
          [
            0.0,
            0.003975027437344815,
            0.009118244672511678,
            0.01094051866825294,
            0.010805999470988786
          ]
        ],
        "HTE": [
          [
            59395.455016421605,
            59395.455016421605,
            59395.455016421605,
            59395.455016421605,
            59395.455016421605
          ],
          [
            59395.455016421605,
            59395.455016421605,
            59395.455016421605,
            59395.455016421605,
            59395.455016421605
          ],
          [
            59395.455016421605,
            59395.455016421605,
            59395.455016421605,
            59395.455016421605,
            59395.455016421605
          ]
        ],
        "HTN": [
          [
            26251.235254161526,
            27390.328313754686,
            28527.04003199235,
            29661.271582069905,
            30792.92435281096
          ],
          [
            26251.235254161526,
            27390.328313754686,
            28527.04003199235,
            29661.271582069905,
            30792.92435281096
          ],
          [
            26251.235254161526,
            27390.328313754686,
            28527.04003199235,
            29661.271582069905,
            30792.92435281096
          ]
        ],
        "tarea": [
          [
            1525307808.0270946,
            1593032537.954344,
            1660618768.108248,
            1728060622.4772792,
            1795352237.6020775
          ],
          [
            1525307808.0270946,
            1593032537.954344,
            1660618768.108248,
            1728060622.4772792,
            1795352237.6020775
          ],
          [
            1525307808.0270946,
            1593032537.954344,
            1660618768.108248,
            1728060622.4772792,
            1795352237.6020775
          ]
        ]
      },
      "assertions": [
        {
          "variable": "aicen",
          "time": 3600.0,
          "expected": 0.27103919783438446,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 1
          },
          "tolerance": {
            "rel": 0.0001,
            "abs": 0.0
          }
        },
        {
          "variable": "vicen",
          "time": 3600.0,
          "expected": 0.05585460978663387,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 1
          },
          "tolerance": {
            "rel": 0.0001,
            "abs": 0.0
          }
        },
        {
          "variable": "vsnon",
          "time": 3600.0,
          "expected": 0.00978557361247467,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 1
          },
          "tolerance": {
            "rel": 0.0002,
            "abs": 0.0
          }
        },
        {
          "variable": "aicen",
          "time": 3600.0,
          "expected": 0.30545282276515473,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 2
          },
          "tolerance": {
            "rel": 0.0001,
            "abs": 0.0
          }
        },
        {
          "variable": "vicen",
          "time": 3600.0,
          "expected": 0.30454205614243457,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 2
          },
          "tolerance": {
            "rel": 0.0001,
            "abs": 0.0
          }
        },
        {
          "variable": "vsnon",
          "time": 3600.0,
          "expected": 0.0906286232646995,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 2
          },
          "tolerance": {
            "rel": 0.0002,
            "abs": 0.0
          }
        },
        {
          "variable": "aicen",
          "time": 3600.0,
          "expected": 0.14120832691372256,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 3
          },
          "tolerance": {
            "rel": 0.0001,
            "abs": 0.0
          }
        },
        {
          "variable": "vicen",
          "time": 3600.0,
          "expected": 0.2449038936723979,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 3
          },
          "tolerance": {
            "rel": 0.0001,
            "abs": 0.0
          }
        },
        {
          "variable": "vsnon",
          "time": 3600.0,
          "expected": 0.0597403722840652,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 3
          },
          "tolerance": {
            "rel": 0.0002,
            "abs": 0.0
          }
        },
        {
          "variable": "aicen",
          "time": 3600.0,
          "expected": 0.04937153685077105,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 4
          },
          "tolerance": {
            "rel": 0.0001,
            "abs": 0.0
          }
        },
        {
          "variable": "vicen",
          "time": 3600.0,
          "expected": 0.16873638490628676,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 4
          },
          "tolerance": {
            "rel": 0.0001,
            "abs": 0.0
          }
        },
        {
          "variable": "vsnon",
          "time": 3600.0,
          "expected": 0.031027368491591805,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 4
          },
          "tolerance": {
            "rel": 0.0002,
            "abs": 0.0
          }
        },
        {
          "variable": "aicen",
          "time": 3600.0,
          "expected": 0.04065491064383748,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 5
          },
          "tolerance": {
            "rel": 0.0001,
            "abs": 0.0
          }
        },
        {
          "variable": "vicen",
          "time": 3600.0,
          "expected": 0.2960204973191455,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 5
          },
          "tolerance": {
            "rel": 0.0001,
            "abs": 0.0
          }
        },
        {
          "variable": "vsnon",
          "time": 3600.0,
          "expected": 0.041163425997390694,
          "coords": {
            "i": 2,
            "j": 4,
            "ncat": 5
          },
          "tolerance": {
            "rel": 0.0002,
            "abs": 0.0
          }
        }
      ]
    }
  ]
}
```

</details>
