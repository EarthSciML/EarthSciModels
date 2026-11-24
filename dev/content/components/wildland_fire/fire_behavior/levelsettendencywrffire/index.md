---
title: "LevelSetTendencyWRFFire"
slug: "levelsettendencywrffire"
domains: ["wildland_fire"]
component_types: ["model"]
subdomains: ["fire_behavior"]
domain: "wildland_fire"
subdomain: "fire_behavior"
component_type: "model"
esm_version: "1.2.0"
esm_path: "components/wildland_fire/fire_behavior/level_set_tendency_wrffire.esm"
reference: "NCAR Community Fire Behavior Model (fire_behavior), develop @ eb77580; instrumented fork ctessum-claude/fire_behavior branch earthsciml-instrumented (c9dda02)."
description: "The level-set propagation equation of fire_behavior (physics/level_set_mod.F90 Calc_tend_ls; Munoz-Esparza et al. 2018) as a PDE on a uniform 2-D grid: d psi/dt = -R |grad psi| + nu |R| (dx d2psi/dx2 + dy d2psi/dy2), the Hamilton-Jacobi front propagation with the rate of spread R normal to the front plus a grid-scaled artificial viscosity, together with the per-axis upwind derivatives diff2x, diff2y and the front normal (nvx, nvy) = (diff2x, diff2y)/sqrt(|grad psi|^2 + eps) that ROSWRFFire consumes. |grad psi| is written as the compound sqrt(D(psi,x)^2 + D(psi,y)^2) and the per-axis derivatives as D(psi,x), D(psi,y); THIS MODEL IMPORTS NO DISCRETISATION OF ITS OWN (only the grid geometry): its consumer -- an inline test, a subsystem-ref edge or a coupling entry (esm-spec 6.6.6, 9.7.10) -- MUST import the complete rule set of one fire_upwinding scheme, and the model cannot be lowered without one (unlowered_operator). It deliberately has no model-level default, because a consumer's imports are APPENDED to the model's own (9.7.10 merge order) and equal-priority matches go to the first declared (9.6.3), so a model-level rule would shadow every consumer's choice for the same match (checked: with the fire_upwinding = 9 rules at model level, 171 of the Godunov, blend and WENO3 tests' assertions fail). The rule sets, from EarthSciDiscretizations grids/cartesian_uniform_2d/rules unless marked ./ (local discretisation files next to this one, for the two schemes ESD lacks a matching rule for), each completed by central_D2x_extrapolate_bc and central_D2y_extrapolate_bc for the viscosity term's second differences (fire_behavior's (diffrx - difflx) with the same halo): fire_upwinding = 9 (fire_behavior's namelist default, hybrid WENO5/ENO1) = weno5_eno1_norm_D2_extrapolate_bc + weno5_eno1_D1x_extrapolate_bc + weno5_eno1_D1y_extrapolate_bc; fire_upwinding = 7 (pure WENO5) = the same three with weno_band_cells past the domain diagonal; fire_upwinding = 10 (WENO5/ENO1 with a cosine blending zone) = weno5_eno1_blend_norm_D2_extrapolate_bc + ./weno5_eno1_blend_D1x_extrapolate_bc + ./weno5_eno1_blend_D1y_extrapolate_bc (the per-axis derivatives must be the blended ones, because fire_behavior blends diff2x, diff2y themselves and builds both |grad psi| and the normal from them); fire_upwinding = 8 (hybrid WENO3/ENO1) = weno3_eno1_norm_D2_extrapolate_bc + weno3_eno1_D1x_extrapolate_bc + weno3_eno1_D1y_extrapolate_bc; fire_upwinding = 4 (classical Godunov) = ./godunov_eno1_norm_D2_extrapolate_bc + godunov_upwind_D1x_extrapolate_bc + godunov_upwind_D1y_extrapolate_bc (max(D-,0) - min(D+,0)). Every one of these closes the walls as fire_behavior does: the first-order ENO1 minmod within bdy_eno1_cells (BDY_ENO1 = 10) of any wall WHATEVER the scheme (Calc_tend_ls tests the wall band before its select case), and at the wall cells a one-cell guarded linear-extrapolation ghost (Extrapol_var_at_bdys), so the domain edge carries no prescribed level-set value. The rules' free names wind_u, wind_v (the mid-flame wind that selects the WENO upwind side), bdy_eno1_cells, weno_band_cells (fire_lsm_band_ngp = 4) and pi_blend are this model's inputs and parameters. R is supplied as an input field (it depends on the normal, tested in ROSWRFFire); the propagation term, the viscosity, the per-axis derivatives and the normal are what this component asserts. Tests: the ls_tend dumps of Runge-Kutta stage 1 of step 20 (t = 10 s) of test7 under five schemes, each test importing its scheme's rule set: fire_upwinding = 9 twice (weno5_step20_stage1, 90 assertions, and weno5_eno1_step20_stage1, 112), 4 (godunov_step20_stage1, 189, including 14 wall-strip and wall cells), 7 (weno5_pure_step20_stage1, 54), 10 (weno5_blend_step20_stage1, 79) and 8 (weno3_eno1_step20_stage1, 71); every scheme's test asserts the per-axis derivatives psi_x, psi_y and the normal nvx, nvy besides |grad psi| and the tendency except weno5_step20_stage1, which predates them (the same scheme's weno5_eno1_step20_stage1 covers them); real32, rel 1e-5 to 2e-5. Coupling hook (added 2026-09-21): the rate-of-spread field the PDE uses is `ros`, which equals the consumer-supplied `ros_supplied` everywhere except the single cell (i_coupled, j_coupled), where it is the coupling-target parameter ros_in; i_coupled = 0 by default, so nothing changes unless a coupling document sets it. couplings/wildlandfire_behavior.esm uses it to drive one cell's spread rate from the mounted Anderson13FuelTable -> FuelMoistureWRFFire -> RothermelWRFFire -> ROSWRFFire chain. fire_upwinding = 7 (pure WENO5) added 2026-09-21 as a third regime: it is case (9) with the band test removed, so it needs no new rule -- only weno_band_cells past the domain diagonal. fire_upwinding = 10 (WENO5/ENO1 with a cosine blending zone) added 2026-09-21 as a fourth regime, lowered by a new ESD norm rule and local per-axis rules; it is the first smooth partition-of-unity operator in that library. fire_upwinding = 8 (hybrid WENO3/ENO1) added 2026-09-21 as a fifth regime, lowered by a new ESD rule family weno3_eno1_norm_D2_extrapolate_bc + weno3_eno1_D1x/D1y_extrapolate_bc: case (8) is case (9) with Select_weno5 replaced by Select_weno3, but there was no WENO3 on cartesian_uniform_2d at all and the library's only WENO3 elsewhere is a 1-D WENO-Z reconstruction with different nonlinear weights, so the classical Jiang-Shu pair had to be transcribed fresh."
tags: ["wildland_fire", "fire_behavior", "model", "wrf-fire", "level-set", "pde"]
---

## Description

The level-set propagation equation of fire_behavior (physics/level_set_mod.F90 Calc_tend_ls; Munoz-Esparza et al. 2018) as a PDE on a uniform 2-D grid: d psi/dt = -R |grad psi| + nu |R| (dx d2psi/dx2 + dy d2psi/dy2), the Hamilton-Jacobi front propagation with the rate of spread R normal to the front plus a grid-scaled artificial viscosity, together with the per-axis upwind derivatives diff2x, diff2y and the front normal (nvx, nvy) = (diff2x, diff2y)/sqrt(|grad psi|^2 + eps) that ROSWRFFire consumes. |grad psi| is written as the compound sqrt(D(psi,x)^2 + D(psi,y)^2) and the per-axis derivatives as D(psi,x), D(psi,y); THIS MODEL IMPORTS NO DISCRETISATION OF ITS OWN (only the grid geometry): its consumer -- an inline test, a subsystem-ref edge or a coupling entry (esm-spec 6.6.6, 9.7.10) -- MUST import the complete rule set of one fire_upwinding scheme, and the model cannot be lowered without one (unlowered_operator). It deliberately has no model-level default, because a consumer's imports are APPENDED to the model's own (9.7.10 merge order) and equal-priority matches go to the first declared (9.6.3), so a model-level rule would shadow every consumer's choice for the same match (checked: with the fire_upwinding = 9 rules at model level, 171 of the Godunov, blend and WENO3 tests' assertions fail). The rule sets, from EarthSciDiscretizations grids/cartesian_uniform_2d/rules unless marked ./ (local discretisation files next to this one, for the two schemes ESD lacks a matching rule for), each completed by central_D2x_extrapolate_bc and central_D2y_extrapolate_bc for the viscosity term's second differences (fire_behavior's (diffrx - difflx) with the same halo): fire_upwinding = 9 (fire_behavior's namelist default, hybrid WENO5/ENO1) = weno5_eno1_norm_D2_extrapolate_bc + weno5_eno1_D1x_extrapolate_bc + weno5_eno1_D1y_extrapolate_bc; fire_upwinding = 7 (pure WENO5) = the same three with weno_band_cells past the domain diagonal; fire_upwinding = 10 (WENO5/ENO1 with a cosine blending zone) = weno5_eno1_blend_norm_D2_extrapolate_bc + ./weno5_eno1_blend_D1x_extrapolate_bc + ./weno5_eno1_blend_D1y_extrapolate_bc (the per-axis derivatives must be the blended ones, because fire_behavior blends diff2x, diff2y themselves and builds both |grad psi| and the normal from them); fire_upwinding = 8 (hybrid WENO3/ENO1) = weno3_eno1_norm_D2_extrapolate_bc + weno3_eno1_D1x_extrapolate_bc + weno3_eno1_D1y_extrapolate_bc; fire_upwinding = 4 (classical Godunov) = ./godunov_eno1_norm_D2_extrapolate_bc + godunov_upwind_D1x_extrapolate_bc + godunov_upwind_D1y_extrapolate_bc (max(D-,0) - min(D+,0)). Every one of these closes the walls as fire_behavior does: the first-order ENO1 minmod within bdy_eno1_cells (BDY_ENO1 = 10) of any wall WHATEVER the scheme (Calc_tend_ls tests the wall band before its select case), and at the wall cells a one-cell guarded linear-extrapolation ghost (Extrapol_var_at_bdys), so the domain edge carries no prescribed level-set value. The rules' free names wind_u, wind_v (the mid-flame wind that selects the WENO upwind side), bdy_eno1_cells, weno_band_cells (fire_lsm_band_ngp = 4) and pi_blend are this model's inputs and parameters. R is supplied as an input field (it depends on the normal, tested in ROSWRFFire); the propagation term, the viscosity, the per-axis derivatives and the normal are what this component asserts. Tests: the ls_tend dumps of Runge-Kutta stage 1 of step 20 (t = 10 s) of test7 under five schemes, each test importing its scheme's rule set: fire_upwinding = 9 twice (weno5_step20_stage1, 90 assertions, and weno5_eno1_step20_stage1, 112), 4 (godunov_step20_stage1, 189, including 14 wall-strip and wall cells), 7 (weno5_pure_step20_stage1, 54), 10 (weno5_blend_step20_stage1, 79) and 8 (weno3_eno1_step20_stage1, 71); every scheme's test asserts the per-axis derivatives psi_x, psi_y and the normal nvx, nvy besides |grad psi| and the tendency except weno5_step20_stage1, which predates them (the same scheme's weno5_eno1_step20_stage1 covers them); real32, rel 1e-5 to 2e-5. Coupling hook (added 2026-09-21): the rate-of-spread field the PDE uses is `ros`, which equals the consumer-supplied `ros_supplied` everywhere except the single cell (i_coupled, j_coupled), where it is the coupling-target parameter ros_in; i_coupled = 0 by default, so nothing changes unless a coupling document sets it. couplings/wildlandfire_behavior.esm uses it to drive one cell's spread rate from the mounted Anderson13FuelTable -> FuelMoistureWRFFire -> RothermelWRFFire -> ROSWRFFire chain. fire_upwinding = 7 (pure WENO5) added 2026-09-21 as a third regime: it is case (9) with the band test removed, so it needs no new rule -- only weno_band_cells past the domain diagonal. fire_upwinding = 10 (WENO5/ENO1 with a cosine blending zone) added 2026-09-21 as a fourth regime, lowered by a new ESD norm rule and local per-axis rules; it is the first smooth partition-of-unity operator in that library. fire_upwinding = 8 (hybrid WENO3/ENO1) added 2026-09-21 as a fifth regime, lowered by a new ESD rule family weno3_eno1_norm_D2_extrapolate_bc + weno3_eno1_D1x/D1y_extrapolate_bc: case (8) is case (9) with Select_weno5 replaced by Select_weno3, but there was no WENO3 on cartesian_uniform_2d at all and the library's only WENO3 elsewhere is a 1-D WENO-Z reconstruction with different nonlinear weights, so the classical Jiang-Shu pair had to be transcribed fresh.

## Reference

- NCAR Community Fire Behavior Model (fire_behavior), develop @ eb77580; instrumented fork ctessum-claude/fire_behavior branch earthsciml-instrumented (c9dda02).
- Munoz-Esparza, D., Kosovic, B., Jimenez, P.A., Coen, J.L. (2018). An accurate fire-spread algorithm in the Weather Research and Forecasting model using the level-set method. J. Adv. Model. Earth Syst. 10, 908-926.
- Osher, S., Sethian, J.A. (1988). Fronts propagating with curvature-dependent speed. J. Comput. Phys. 79, 12-49.

## Variables

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `psi` | `m` |  | Level-set function over the [x, y] fire grid (fire_behavior lfn; negative inside the burnt area, a signed distance after reinitialisation). |

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `x0` | `m` | `0.0` | Left domain edge (grid free name). |
| `y0` | `m` | `0.0` | Bottom domain edge (grid free name). |
| `Lx` | `m` | `2000.0` | Domain width NX dx (test7: 80 x 25 m). |
| `Ly` | `m` | `2000.0` | Domain height NY dy. |
| `fire_viscosity` | `1` | `0.4` | Artificial viscosity coefficient nu (namelist fire_viscosity = fire_viscosity_bg = 0.4 in test7, so the near-front band has the same value and the coefficient is uniform). |
| `bdy_eno1_cells` | `1` | `10` | Width in cells of the wall band where fire_behavior always uses first-order ENO1 (BDY_ENO1 = 10, a compile-time constant of level_set_mod.F90); free name of the hybrid rules. |
| `weno_band_cells` | `1` | `4` | Half-width in cells of the band \|psi\| < weno_band_cells dx around the front where the hybrid scheme uses WENO5 (namelist fire_lsm_band_ngp = 4); free name of the hybrid rules. |
| `nv_eps` | `1` | `1.1920928955078125e-07` | Regularisation of the normal's denominator sqrt(\|grad psi\|^2 + eps): fire_behavior's EPS = epsilon(0.0) of its default real32 kind. |
| `i_coupled` | `1` | `0.0` | x index (1-based) of the cell whose rate of spread is taken from ros_in; 0 disables the replacement. |
| `j_coupled` | `1` | `0.0` | y index (1-based) of the cell whose rate of spread is taken from ros_in; 0 disables the replacement. |
| `ros_in` | `m/s` | `0.0` | Coupling target: rate of spread of cell (i_coupled, j_coupled), supplied by a mounted ROSWRFFire through a variable_map param_to_var edge. |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `ros` | `m/s` |  | Effective rate-of-spread field entering the PDE: ros_supplied everywhere except the single cell (i_coupled, j_coupled), where it is the coupling target ros_in. With the default i_coupled = 0 no cell matches and ros is ros_supplied, so a standalone run is unchanged; a coupling document that mounts ROSWRFFire beside this component sets i_coupled/j_coupled and drives ros_in, which makes d psi/dt at that cell depend on the whole fuel -> moisture -> Rothermel -> ROS chain. Same idiom as s_coupled in fire_flux_to_atmosphere_wrffire.esm. |
| `wind_u` | `m/s` |  | Mid-flame wind x-component uf on the fire grid (input field; free name wind_u of the hybrid WENO5/ENO1 rules, whose WENO upwind side is selected by the sign of (grad4 psi . U) d4 psi). Not read by the Godunov rules. |
| `wind_v` | `m/s` |  | Mid-flame wind y-component vf on the fire grid (input field; free name wind_v of the hybrid rules). |
| `dx` | `m` |  | x spacing Lx/NX (grid free name). |
| `dy` | `m` |  | y spacing Ly/NY (grid free name). |
| `grad_mag` | `1` |  | \|grad psi\| of the selected scheme (fire_behavior grad / grad_norm_ls): with the Godunov rule (fire_upwinding = 4) sqrt(max(D-x,0)^2 + min(D+x,0)^2 + max(D-y,0)^2 + min(D+y,0)^2); with the hybrid rules (fire_upwinding = 7, 8, 9, 10) sqrt(diff2x^2 + diff2y^2) of the per-axis derivatives; for every scheme sqrt(diff2x^2 + diff2y^2) of the ENO1 minmod derivatives within bdy_eno1_cells of a wall. Written as the compound sqrt(D(psi,x)^2 + D(psi,y)^2); the norm rule the consumer imports selects the scheme (the model imports none). |
| `psi_xx` | `1/m` |  | d2 psi/dx2 by the centred second-difference rule; fire_behavior's (diffrx - difflx) = dx psi_xx. |
| `psi_yy` | `1/m` |  | d2 psi/dy2 by the centred second-difference rule. |
| `tend_adv` | `m/s` |  | Hamilton-Jacobi propagation term -ros \|grad psi\|. |
| `tend_visc` | `m/s` |  | Artificial viscosity nu \|ros\| (dx psi_xx + dy psi_yy): fire_behavior adds fire_viscosity \|ros\| ((diffrx - difflx) + (diffry - diffly)), a grid-scaled Laplacian that vanishes with the mesh. |
| `tend` | `m/s` |  | Level-set tendency d psi/dt = tend_adv + tend_visc (Calc_tend_ls tend). |
| `psi_x` | `1` |  | Per-axis upwind derivative diff2x of the selected scheme: for fire_upwinding = 4 the Godunov-upwind quantity max(D-x psi, 0) - min(D+x psi, 0) (godunov_upwind_D1x_extrapolate_bc; a magnitude for negative slopes, N44), for fire_upwinding = 7 and 9 the hybrid WENO5/ENO1 derivative (weno5_eno1_D1x_extrapolate_bc), for 10 the blended mask diff2x_weno + (1 - mask) diff2x_eno (./weno5_eno1_blend_D1x_extrapolate_bc), for 8 the WENO3/ENO1 derivative (weno3_eno1_D1x_extrapolate_bc); ENO1 within bdy_eno1_cells of a wall for all of them. Written as D(psi, x); the rule the consumer imports selects the scheme (the model imports none). |
| `psi_y` | `1` |  | Per-axis upwind derivative diff2y of the selected scheme (see psi_x); D(psi, y). |
| `nvx` | `1` |  | x-component of the front normal, psi_x / sqrt(\|grad psi\|^2 + eps) (Calc_tend_ls nvx); the input ROSWRFFire takes for the wind and slope projections. |
| `nvy` | `1` |  | y-component of the front normal, psi_y / sqrt(\|grad psi\|^2 + eps) (nvy). |
| `ros_supplied` | `m/s` |  | Rate of spread normal to the front at each cell as supplied by the consumer (ROSWRFFire ros, itself a function of the upwind normal); the operator assembly is tested independently of the normal computation. |
| `pi_blend` | `1` |  | fire_behavior's pi, taken from the fire constants library. It is a free name the fire_upwinding = 10 blending rules read; the hard-edged fire_upwinding = 9 and Godunov rules never reference it, so it is inert in those regimes. |

## Observed expressions

$$
ros = \mathrm{faq}\left(\right)
$$
_Effective rate-of-spread field entering the PDE: ros_supplied everywhere except the single cell (i_coupled, j_coupled), where it is the coupling target ros_in. With the default i_coupled = 0 no cell matches and ros is ros_supplied, so a standalone run is unchanged; a coupling document that mounts ROSWRFFire beside this component sets i_coupled/j_coupled and drives ros_in, which makes d psi/dt at that cell depend on the whole fuel -> moisture -> Rothermel -> ROS chain. Same idiom as s_coupled in fire_flux_to_atmosphere_wrffire.esm._

$$
wind_{u} = \mathrm{input_wind_u}\left(\right)
$$
_Mid-flame wind x-component uf on the fire grid (input field; free name wind_u of the hybrid WENO5/ENO1 rules, whose WENO upwind side is selected by the sign of (grad4 psi . U) d4 psi). Not read by the Godunov rules._

$$
wind_{v} = \mathrm{input_wind_v}\left(\right)
$$
_Mid-flame wind y-component vf on the fire grid (input field; free name wind_v of the hybrid rules)._

$$
dx = \frac{Lx}{NX}
$$
_x spacing Lx/NX (grid free name)._

$$
dy = \frac{Ly}{NY}
$$
_y spacing Ly/NY (grid free name)._

$$
grad_{mag} = \sqrt{\mathrm{D}\left(psi\right)^{2} + \mathrm{D}\left(psi\right)^{2}}
$$
_|grad psi| of the selected scheme (fire_behavior grad / grad_norm_ls): with the Godunov rule (fire_upwinding = 4) sqrt(max(D-x,0)^2 + min(D+x,0)^2 + max(D-y,0)^2 + min(D+y,0)^2); with the hybrid rules (fire_upwinding = 7, 8, 9, 10) sqrt(diff2x^2 + diff2y^2) of the per-axis derivatives; for every scheme sqrt(diff2x^2 + diff2y^2) of the ENO1 minmod derivatives within bdy_eno1_cells of a wall. Written as the compound sqrt(D(psi,x)^2 + D(psi,y)^2); the norm rule the consumer imports selects the scheme (the model imports none)._

$$
psi_{xx} = \mathrm{D}\left(\mathrm{D}\left(psi\right)\right)
$$
_d2 psi/dx2 by the centred second-difference rule; fire_behavior's (diffrx - difflx) = dx psi_xx._

$$
psi_{yy} = \mathrm{D}\left(\mathrm{D}\left(psi\right)\right)
$$
_d2 psi/dy2 by the centred second-difference rule._

$$
tend_{adv} = \left(-ros\right) \cdot grad_{mag}
$$
_Hamilton-Jacobi propagation term -ros |grad psi|._

$$
tend_{visc} = fire_{viscosity} \cdot \left|ros\right| \cdot \left(dx \cdot psi_{xx} + dy \cdot psi_{yy}\right)
$$
_Artificial viscosity nu |ros| (dx psi_xx + dy psi_yy): fire_behavior adds fire_viscosity |ros| ((diffrx - difflx) + (diffry - diffly)), a grid-scaled Laplacian that vanishes with the mesh._

$$
tend = tend_{adv} + tend_{visc}
$$
_Level-set tendency d psi/dt = tend_adv + tend_visc (Calc_tend_ls tend)._

$$
psi_{x} = \mathrm{D}\left(psi\right)
$$
_Per-axis upwind derivative diff2x of the selected scheme: for fire_upwinding = 4 the Godunov-upwind quantity max(D-x psi, 0) - min(D+x psi, 0) (godunov_upwind_D1x_extrapolate_bc; a magnitude for negative slopes, N44), for fire_upwinding = 7 and 9 the hybrid WENO5/ENO1 derivative (weno5_eno1_D1x_extrapolate_bc), for 10 the blended mask diff2x_weno + (1 - mask) diff2x_eno (./weno5_eno1_blend_D1x_extrapolate_bc), for 8 the WENO3/ENO1 derivative (weno3_eno1_D1x_extrapolate_bc); ENO1 within bdy_eno1_cells of a wall for all of them. Written as D(psi, x); the rule the consumer imports selects the scheme (the model imports none)._

$$
psi_{y} = \mathrm{D}\left(psi\right)
$$
_Per-axis upwind derivative diff2y of the selected scheme (see psi_x); D(psi, y)._

$$
nvx = \frac{psi_{x}}{\sqrt{grad_{mag}^{2} + nv_{eps}}}
$$
_x-component of the front normal, psi_x / sqrt(|grad psi|^2 + eps) (Calc_tend_ls nvx); the input ROSWRFFire takes for the wind and slope projections._

$$
nvy = \frac{psi_{y}}{\sqrt{grad_{mag}^{2} + nv_{eps}}}
$$
_y-component of the front normal, psi_y / sqrt(|grad psi|^2 + eps) (nvy)._

$$
ros_{supplied} = \mathrm{input_ros}\left(\right)
$$
_Rate of spread normal to the front at each cell as supplied by the consumer (ROSWRFFire ros, itself a function of the upwind normal); the operator assembly is tested independently of the normal computation._

$$
pi_{blend} = par.pi
$$
_fire_behavior's pi, taken from the fire constants library. It is a free name the fire_upwinding = 10 blending rules read; the hard-edged fire_upwinding = 9 and Godunov rules never reference it, so it is inert in those regimes._

## Equations

$$
\mathrm{ic}\left(psi\right) = \mathrm{input_psi}\left(\right)
$$

$$
\mathrm{D}\left(psi\right) = tend
$$

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "expression_template_imports": [
    {
      "ref": "${ESD_ROOT}/grids/cartesian_uniform_2d/grid.esm",
      "bindings": {
        "NX": "NX",
        "NY": "NY"
      }
    }
  ],
  "variables": {
    "psi": {
      "type": "unknown",
      "units": "m",
      "shape": [
        "x",
        "y"
      ],
      "description": "Level-set function over the [x, y] fire grid (fire_behavior lfn; negative inside the burnt area, a signed distance after reinitialisation)."
    },
    "ros": {
      "type": "unknown",
      "units": "m/s",
      "shape": [
        "x",
        "y"
      ],
      "description": "Effective rate-of-spread field entering the PDE: ros_supplied everywhere except the single cell (i_coupled, j_coupled), where it is the coupling target ros_in. With the default i_coupled = 0 no cell matches and ros is ros_supplied, so a standalone run is unchanged; a coupling document that mounts ROSWRFFire beside this component sets i_coupled/j_coupled and drives ros_in, which makes d psi/dt at that cell depend on the whole fuel -> moisture -> Rothermel -> ROS chain. Same idiom as s_coupled in fire_flux_to_atmosphere_wrffire.esm."
    },
    "wind_u": {
      "type": "unknown",
      "units": "m/s",
      "shape": [
        "x",
        "y"
      ],
      "description": "Mid-flame wind x-component uf on the fire grid (input field; free name wind_u of the hybrid WENO5/ENO1 rules, whose WENO upwind side is selected by the sign of (grad4 psi . U) d4 psi). Not read by the Godunov rules."
    },
    "wind_v": {
      "type": "unknown",
      "units": "m/s",
      "shape": [
        "x",
        "y"
      ],
      "description": "Mid-flame wind y-component vf on the fire grid (input field; free name wind_v of the hybrid rules)."
    },
    "x0": {
      "type": "parameter",
      "units": "m",
      "default": 0.0,
      "description": "Left domain edge (grid free name)."
    },
    "y0": {
      "type": "parameter",
      "units": "m",
      "default": 0.0,
      "description": "Bottom domain edge (grid free name)."
    },
    "Lx": {
      "type": "parameter",
      "units": "m",
      "default": 2000.0,
      "description": "Domain width NX dx (test7: 80 x 25 m)."
    },
    "Ly": {
      "type": "parameter",
      "units": "m",
      "default": 2000.0,
      "description": "Domain height NY dy."
    },
    "dx": {
      "type": "unknown",
      "units": "m",
      "description": "x spacing Lx/NX (grid free name)."
    },
    "dy": {
      "type": "unknown",
      "units": "m",
      "description": "y spacing Ly/NY (grid free name)."
    },
    "fire_viscosity": {
      "type": "parameter",
      "units": "1",
      "default": 0.4,
      "description": "Artificial viscosity coefficient nu (namelist fire_viscosity = fire_viscosity_bg = 0.4 in test7, so the near-front band has the same value and the coefficient is uniform)."
    },
    "grad_mag": {
      "type": "unknown",
      "units": "1",
      "shape": [
        "x",
        "y"
      ],
      "description": "|grad psi| of the selected scheme (fire_behavior grad / grad_norm_ls): with the Godunov rule (fire_upwinding = 4) sqrt(max(D-x,0)^2 + min(D+x,0)^2 + max(D-y,0)^2 + min(D+y,0)^2); with the hybrid rules (fire_upwinding = 7, 8, 9, 10) sqrt(diff2x^2 + diff2y^2) of the per-axis derivatives; for every scheme sqrt(diff2x^2 + diff2y^2) of the ENO1 minmod derivatives within bdy_eno1_cells of a wall. Written as the compound sqrt(D(psi,x)^2 + D(psi,y)^2); the norm rule the consumer imports selects the scheme (the model imports none)."
    },
    "psi_xx": {
      "type": "unknown",
      "units": "1/m",
      "shape": [
        "x",
        "y"
      ],
      "description": "d2 psi/dx2 by the centred second-difference rule; fire_behavior's (diffrx - difflx) = dx psi_xx."
    },
    "psi_yy": {
      "type": "unknown",
      "units": "1/m",
      "shape": [
        "x",
        "y"
      ],
      "description": "d2 psi/dy2 by the centred second-difference rule."
    },
    "tend_adv": {
      "type": "unknown",
      "units": "m/s",
      "shape": [
        "x",
        "y"
      ],
      "description": "Hamilton-Jacobi propagation term -ros |grad psi|."
    },
    "tend_visc": {
      "type": "unknown",
      "units": "m/s",
      "shape": [
        "x",
        "y"
      ],
      "description": "Artificial viscosity nu |ros| (dx psi_xx + dy psi_yy): fire_behavior adds fire_viscosity |ros| ((diffrx - difflx) + (diffry - diffly)), a grid-scaled Laplacian that vanishes with the mesh."
    },
    "tend": {
      "type": "unknown",
      "units": "m/s",
      "shape": [
        "x",
        "y"
      ],
      "description": "Level-set tendency d psi/dt = tend_adv + tend_visc (Calc_tend_ls tend)."
    },
    "bdy_eno1_cells": {
      "type": "parameter",
      "units": "1",
      "default": 10,
      "description": "Width in cells of the wall band where fire_behavior always uses first-order ENO1 (BDY_ENO1 = 10, a compile-time constant of level_set_mod.F90); free name of the hybrid rules."
    },
    "weno_band_cells": {
      "type": "parameter",
      "units": "1",
      "default": 4,
      "description": "Half-width in cells of the band |psi| < weno_band_cells dx around the front where the hybrid scheme uses WENO5 (namelist fire_lsm_band_ngp = 4); free name of the hybrid rules."
    },
    "nv_eps": {
      "type": "parameter",
      "units": "1",
      "default": 1.1920928955078125e-07,
      "description": "Regularisation of the normal's denominator sqrt(|grad psi|^2 + eps): fire_behavior's EPS = epsilon(0.0) of its default real32 kind."
    },
    "psi_x": {
      "type": "unknown",
      "units": "1",
      "shape": [
        "x",
        "y"
      ],
      "description": "Per-axis upwind derivative diff2x of the selected scheme: for fire_upwinding = 4 the Godunov-upwind quantity max(D-x psi, 0) - min(D+x psi, 0) (godunov_upwind_D1x_extrapolate_bc; a magnitude for negative slopes, N44), for fire_upwinding = 7 and 9 the hybrid WENO5/ENO1 derivative (weno5_eno1_D1x_extrapolate_bc), for 10 the blended mask diff2x_weno + (1 - mask) diff2x_eno (./weno5_eno1_blend_D1x_extrapolate_bc), for 8 the WENO3/ENO1 derivative (weno3_eno1_D1x_extrapolate_bc); ENO1 within bdy_eno1_cells of a wall for all of them. Written as D(psi, x); the rule the consumer imports selects the scheme (the model imports none)."
    },
    "psi_y": {
      "type": "unknown",
      "units": "1",
      "shape": [
        "x",
        "y"
      ],
      "description": "Per-axis upwind derivative diff2y of the selected scheme (see psi_x); D(psi, y)."
    },
    "nvx": {
      "type": "unknown",
      "units": "1",
      "shape": [
        "x",
        "y"
      ],
      "description": "x-component of the front normal, psi_x / sqrt(|grad psi|^2 + eps) (Calc_tend_ls nvx); the input ROSWRFFire takes for the wind and slope projections."
    },
    "nvy": {
      "type": "unknown",
      "units": "1",
      "shape": [
        "x",
        "y"
      ],
      "description": "y-component of the front normal, psi_y / sqrt(|grad psi|^2 + eps) (nvy)."
    },
    "ros_supplied": {
      "type": "unknown",
      "units": "m/s",
      "shape": [
        "x",
        "y"
      ],
      "description": "Rate of spread normal to the front at each cell as supplied by the consumer (ROSWRFFire ros, itself a function of the upwind normal); the operator assembly is tested independently of the normal computation."
    },
    "i_coupled": {
      "type": "parameter",
      "units": "1",
      "default": 0.0,
      "description": "x index (1-based) of the cell whose rate of spread is taken from ros_in; 0 disables the replacement."
    },
    "j_coupled": {
      "type": "parameter",
      "units": "1",
      "default": 0.0,
      "description": "y index (1-based) of the cell whose rate of spread is taken from ros_in; 0 disables the replacement."
    },
    "ros_in": {
      "type": "parameter",
      "units": "m/s",
      "default": 0.0,
      "description": "Coupling target: rate of spread of cell (i_coupled, j_coupled), supplied by a mounted ROSWRFFire through a variable_map param_to_var edge."
    },
    "pi_blend": {
      "type": "unknown",
      "units": "1",
      "description": "fire_behavior's pi, taken from the fire constants library. It is a free name the fire_upwinding = 10 blending rules read; the hard-edged fire_upwinding = 9 and Godunov rules never reference it, so it is inert in those regimes."
    }
  },
  "equations": [
    {
      "lhs": "dx",
      "rhs": {
        "op": "/",
        "args": [
          "Lx",
          "NX"
        ]
      }
    },
    {
      "lhs": "dy",
      "rhs": {
        "op": "/",
        "args": [
          "Ly",
          "NY"
        ]
      }
    },
    {
      "lhs": {
        "op": "ic",
        "args": [
          "psi"
        ]
      },
      "rhs": {
        "op": "input_psi",
        "args": []
      }
    },
    {
      "lhs": "ros_supplied",
      "rhs": {
        "op": "input_ros",
        "args": []
      }
    },
    {
      "lhs": "ros",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i",
          "j"
        ],
        "args": [],
        "ranges": {
          "i": {
            "from": "x"
          },
          "j": {
            "from": "y"
          }
        },
        "expr": {
          "op": "ifelse",
          "args": [
            {
              "op": "==",
              "args": [
                "i",
                "i_coupled"
              ]
            },
            {
              "op": "ifelse",
              "args": [
                {
                  "op": "==",
                  "args": [
                    "j",
                    "j_coupled"
                  ]
                },
                "ros_in",
                {
                  "op": "index",
                  "args": [
                    "ros_supplied",
                    "i",
                    "j"
                  ]
                }
              ]
            },
            {
              "op": "index",
              "args": [
                "ros_supplied",
                "i",
                "j"
              ]
            }
          ]
        }
      }
    },
    {
      "lhs": "wind_u",
      "rhs": {
        "op": "input_wind_u",
        "args": []
      }
    },
    {
      "lhs": "wind_v",
      "rhs": {
        "op": "input_wind_v",
        "args": []
      }
    },
    {
      "lhs": "grad_mag",
      "rhs": {
        "op": "sqrt",
        "args": [
          {
            "op": "+",
            "args": [
              {
                "op": "^",
                "args": [
                  {
                    "op": "D",
                    "args": [
                      "psi"
                    ],
                    "wrt": "x"
                  },
                  2
                ]
              },
              {
                "op": "^",
                "args": [
                  {
                    "op": "D",
                    "args": [
                      "psi"
                    ],
                    "wrt": "y"
                  },
                  2
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "psi_x",
      "rhs": {
        "op": "D",
        "args": [
          "psi"
        ],
        "wrt": "x"
      }
    },
    {
      "lhs": "psi_y",
      "rhs": {
        "op": "D",
        "args": [
          "psi"
        ],
        "wrt": "y"
      }
    },
    {
      "lhs": "nvx",
      "rhs": {
        "op": "/",
        "args": [
          "psi_x",
          {
            "op": "sqrt",
            "args": [
              {
                "op": "+",
                "args": [
                  {
                    "op": "^",
                    "args": [
                      "grad_mag",
                      2
                    ]
                  },
                  "nv_eps"
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "nvy",
      "rhs": {
        "op": "/",
        "args": [
          "psi_y",
          {
            "op": "sqrt",
            "args": [
              {
                "op": "+",
                "args": [
                  {
                    "op": "^",
                    "args": [
                      "grad_mag",
                      2
                    ]
                  },
                  "nv_eps"
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "psi_xx",
      "rhs": {
        "op": "D",
        "args": [
          {
            "op": "D",
            "args": [
              "psi"
            ],
            "wrt": "x"
          }
        ],
        "wrt": "x"
      }
    },
    {
      "lhs": "psi_yy",
      "rhs": {
        "op": "D",
        "args": [
          {
            "op": "D",
            "args": [
              "psi"
            ],
            "wrt": "y"
          }
        ],
        "wrt": "y"
      }
    },
    {
      "lhs": "tend_adv",
      "rhs": {
        "op": "*",
        "args": [
          {
            "op": "-",
            "args": [
              "ros"
            ]
          },
          "grad_mag"
        ]
      }
    },
    {
      "lhs": "tend_visc",
      "rhs": {
        "op": "*",
        "args": [
          "fire_viscosity",
          {
            "op": "abs",
            "args": [
              "ros"
            ]
          },
          {
            "op": "+",
            "args": [
              {
                "op": "*",
                "args": [
                  "dx",
                  "psi_xx"
                ]
              },
              {
                "op": "*",
                "args": [
                  "dy",
                  "psi_yy"
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "tend",
      "rhs": {
        "op": "+",
        "args": [
          "tend_adv",
          "tend_visc"
        ]
      }
    },
    {
      "lhs": {
        "op": "D",
        "args": [
          "psi"
        ],
        "wrt": "t"
      },
      "rhs": "tend"
    },
    {
      "lhs": "pi_blend",
      "rhs": "par.pi"
    }
  ],
  "tests": [
    {
      "id": "weno5_step20_stage1",
      "description": "Reference: NCAR fire_behavior test7 (80x80 fire cells of 25 m, dt = 0.5 s, num_tiles = 1) with its default level-set scheme (fire_upwinding = 9), default real32 build, dumped in-model by the ctessum-claude/fire_behavior fork (branch earthsciml-instrumented, commit c9dda02, based on NCAR fire_behavior eb77580, three commits before v1.0.0; -DESM_DUMP=ON): ls_tend dump call 58 = Runge-Kutta stage 1 of step 20 (t = 10 s). The inputs psi, ros, wind_u and wind_v are the full 80x80 dumped lfn, ros, uf and vf fields injected as [x, y] const fields. grad_mag, tend_adv and tend are checked at all four corners, cells on each wall, cells inside the 10-cell ENO1 wall band, cells within the WENO band of the front (|psi| < 100 m) and far-field ENO1 cells. The rules reproduce the dump over the whole field to the tolerances used here (checked offline). fire_viscosity = fire_viscosity_bg = 0.4 in test7, so the viscosity coefficient is uniform. Single precision: rel 1e-5 on grad_mag and the propagation term, 2e-5 on the total tendency (a sum of the two). (The model imports no discretisation of its own, see its description, so this test imports the fire_upwinding = 9 rule set: weno5_eno1_norm_D2_extrapolate_bc, the matching per-axis weno5_eno1_D1x/D1y_extrapolate_bc for psi_x/psi_y, and central_D2x/D2y_extrapolate_bc.)",
      "parameter_overrides": {
        "Lx": 2000.0,
        "Ly": 2000.0,
        "fire_viscosity": 0.4,
        "bdy_eno1_cells": 10,
        "weno_band_cells": 4
      },
      "expression_template_imports": [
        {
          "ref": "${ESD_ROOT}/grids/cartesian_uniform_2d/rules/weno5_eno1_norm_D2_extrapolate_bc.esm",
          "bindings": {
            "NX": 80,
            "NY": 80
          }
        },
        {
          "ref": "${ESD_ROOT}/grids/cartesian_uniform_2d/rules/weno5_eno1_D1x_extrapolate_bc.esm",
          "bindings": {
            "NX": 80,
            "NY": 80
          }
        },
        {
          "ref": "${ESD_ROOT}/grids/cartesian_uniform_2d/rules/weno5_eno1_D1y_extrapolate_bc.esm",
          "bindings": {
            "NX": 80,
            "NY": 80
          }
        },
        {
          "ref": "${ESD_ROOT}/grids/cartesian_uniform_2d/rules/central_D2x_extrapolate_bc.esm",
          "bindings": {
            "NX": 80,
            "NY": 80
          }
        },
        {
          "ref": "${ESD_ROOT}/grids/cartesian_uniform_2d/rules/central_D2y_extrapolate_bc.esm",
          "bindings": {
            "NX": 80,
            "NY": 80
          }
        },
        {
          "ref": "./tests/weno5_step20_stage1_inputs.esm"
        }
      ],
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 1,
            "y": 1
          },
          "expected": 0.9607469439506531,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 1,
            "y": 1
          },
          "expected": -0.01707698591053486,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 1,
            "y": 1
          },
          "expected": -0.01707698591053486,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 1,
            "y": 80
          },
          "expected": 0.956847608089447,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 1,
            "y": 80
          },
          "expected": -0.4924148619174957,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 1,
            "y": 80
          },
          "expected": -0.4924148619174957,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 80,
            "y": 1
          },
          "expected": 0.949800431728363,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 80,
            "y": 1
          },
          "expected": -0.017183275893330574,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 80,
            "y": 1
          },
          "expected": -0.017183275893330574,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 80,
            "y": 80
          },
          "expected": 1.0361480712890625,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 80,
            "y": 80
          },
          "expected": -0.5494412183761597,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 80,
            "y": 80
          },
          "expected": -0.5494412183761597,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 1,
            "y": 60
          },
          "expected": 0.9394055604934692,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 1,
            "y": 60
          },
          "expected": -0.016697648912668228,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 1,
            "y": 60
          },
          "expected": -0.016350295394659042,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 80,
            "y": 40
          },
          "expected": 0.9431357979774475,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 80,
            "y": 40
          },
          "expected": -0.018146438524127007,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 80,
            "y": 40
          },
          "expected": -0.01807500049471855,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 1
          },
          "expected": 0.9623169302940369,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 1
          },
          "expected": -0.01810791902244091,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 1
          },
          "expected": -0.01777046173810959,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 80
          },
          "expected": 0.9592926502227783,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 80
          },
          "expected": -0.8218752145767212,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 80
          },
          "expected": -0.7904891967773438,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 2,
            "y": 60
          },
          "expected": 0.9394165873527527,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 2,
            "y": 60
          },
          "expected": -0.016697846353054047,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 2,
            "y": 60
          },
          "expected": -0.017075246199965477,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 3,
            "y": 60
          },
          "expected": 1.0435833930969238,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 3,
            "y": 60
          },
          "expected": -0.019534800201654434,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 3,
            "y": 60
          },
          "expected": -0.019129078835248947,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 10,
            "y": 60
          },
          "expected": 0.938305139541626,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 10,
            "y": 60
          },
          "expected": -0.016678089275956154,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 10,
            "y": 60
          },
          "expected": -0.016800178214907646,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 11,
            "y": 60
          },
          "expected": 0.9374631643295288,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 11,
            "y": 60
          },
          "expected": -0.016663124784827232,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 11,
            "y": 60
          },
          "expected": -0.015242619439959526,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 70,
            "y": 40
          },
          "expected": 0.946587085723877,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 70,
            "y": 40
          },
          "expected": -0.016825299710035324,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 70,
            "y": 40
          },
          "expected": -0.01742207072675228,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 71,
            "y": 40
          },
          "expected": 0.9442129731178284,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 71,
            "y": 40
          },
          "expected": -0.016783099621534348,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 71,
            "y": 40
          },
          "expected": -0.0160024706274271,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 40
          },
          "expected": 0.9608290195465088,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 40
          },
          "expected": -0.017078444361686707,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 40
          },
          "expected": -0.01639811135828495,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 60,
            "y": 20
          },
          "expected": 1.0064423084259033,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 60,
            "y": 20
          },
          "expected": -0.01788920722901821,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 60,
            "y": 20
          },
          "expected": -0.01775367558002472,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 13,
            "y": 62
          },
          "expected": 1.0745012760162354,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 13,
            "y": 62
          },
          "expected": -0.019098935648798943,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 13,
            "y": 62
          },
          "expected": -0.018266914412379265,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 15,
            "y": 60
          },
          "expected": 0.9177594184875488,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 15,
            "y": 60
          },
          "expected": -0.016312895342707634,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 15,
            "y": 60
          },
          "expected": -0.01522440742701292,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 16,
            "y": 61
          },
          "expected": 0.9846597909927368,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 16,
            "y": 61
          },
          "expected": -0.017502030357718468,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 16,
            "y": 61
          },
          "expected": -0.0169366467744112,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 17,
            "y": 58
          },
          "expected": 1.2361421585083008,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 17,
            "y": 58
          },
          "expected": -0.02197205275297165,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 17,
            "y": 58
          },
          "expected": -0.005636632442474365,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 17,
            "y": 62
          },
          "expected": 1.0679022073745728,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 17,
            "y": 62
          },
          "expected": -0.035334110260009766,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 17,
            "y": 62
          },
          "expected": -0.032472554594278336,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 18,
            "y": 62
          },
          "expected": 0.9711326360702515,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 18,
            "y": 62
          },
          "expected": -0.09294385462999344,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 18,
            "y": 62
          },
          "expected": -0.07872790843248367,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 19,
            "y": 65
          },
          "expected": 0.9979144930839539,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 19,
            "y": 65
          },
          "expected": -0.6892843842506409,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 19,
            "y": 65
          },
          "expected": -0.6468188166618347,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 20,
            "y": 64
          },
          "expected": 1.004002332687378,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 20,
            "y": 64
          },
          "expected": -0.549563467502594,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 20,
            "y": 64
          },
          "expected": -0.4792269468307495,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 21,
            "y": 58
          },
          "expected": 0.7880091667175293,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 21,
            "y": 58
          },
          "expected": -0.014409762807190418,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 21,
            "y": 58
          },
          "expected": -0.03751404583454132,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 22,
            "y": 66
          },
          "expected": 1.0010517835617065,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 22,
            "y": 66
          },
          "expected": -0.940845787525177,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 22,
            "y": 66
          },
          "expected": -0.8635289669036865,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 23,
            "y": 60
          },
          "expected": 2.4502270221710205,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 23,
            "y": 60
          },
          "expected": -0.04739733040332794,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 23,
            "y": 60
          },
          "expected": -0.05745498090982437,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 24,
            "y": 62
          },
          "expected": 2.600867986679077,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 24,
            "y": 62
          },
          "expected": -0.04929045960307121,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 24,
            "y": 62
          },
          "expected": -0.03891885280609131,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 25,
            "y": 64
          },
          "expected": 0.8732550740242004,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 25,
            "y": 64
          },
          "expected": -0.5849319696426392,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 25,
            "y": 64
          },
          "expected": -0.38170430064201355,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 26,
            "y": 64
          },
          "expected": 1.531110405921936,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-06
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 26,
            "y": 64
          },
          "expected": -0.028976095840334892,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 26,
            "y": 64
          },
          "expected": -0.0016478244215250015,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-06
          }
        }
      ]
    },
    {
      "id": "godunov_step20_stage1",
      "description": "Reference: NCAR fire_behavior test7 (80x80 fire cells of 25 m, dt = 0.5 s, num_tiles = 1) rerun with fire_upwinding = 4 (classical Godunov discretisation of the Hamiltonian), default real32 build, dumped in-model by the ctessum-claude/fire_behavior fork (c9dda02, -DESM_DUMP=ON): ls_tend dump call 58 = Runge-Kutta stage 1 of step 20 (t = 10 s) (data/eqwefic/dumps/fire/run_godunov/esm_dump_ls_tend_58.json). The inputs psi and ros are the full 80x80 dumped lfn and ros fields injected as [x, y] const fields. fire_behavior's case (4) is an INTERIOR scheme only: Calc_tend_ls tests the BDY_ENO1 = 10 wall band before its select case, so within 10 cells of any wall grad = sqrt(eno1x^2 + eno1y^2) and diff2 = the ENO1 minmod, with the guarded linear-extrapolation halo (Extrapol_var_at_bdys) at the wall cells, and the Rouy-Tourin Hamiltonian sqrt(max(D-x,0)^2 + min(D+x,0)^2 + max(D-y,0)^2 + min(D+y,0)^2) and diff2 = max(D-,0) - min(D+,0) only on 11 <= i, j <= 70. The test imports the rules that do exactly that: ./godunov_eno1_norm_D2_extrapolate_bc (local: ESD's shared WENO5/ENO1 boundary frames, which carry the ENO1 strips and the extrapolation ghosts, around a per-axis Godunov magnitude with the ENO1 wall-band switch, combined as sqrt(Gx^2 + Gy^2)), EarthSciDiscretizations' godunov_upwind_D1x/D1y_extrapolate_bc for the normal's per-axis quantities (already with the wall band and halo), and central_D2x/D2y_extrapolate_bc for the viscosity, with bdy_eno1_cells = 10. ESD's godunov_norm_D2_dirichlet_bc, which applies the Hamiltonian up to the wall against prescribed wall values, does not: with zero wall values its wall-cell |grad psi| is ~60 against fire_behavior's ~1, and swapping it back in fails 55 of these assertions. Asserted, per cell grad_mag, tend_adv, tend, psi_x, psi_y (the dumped diff2x, diff2y) and nvx, nvy = diff2/sqrt(grad^2 + eps): 13 interior cells (10 within 150 m of the front where the level set is moving, plus three far-field cells), and 14 cells inside the 10-cell wall strip -- the four corners' neighbourhood (1,1), (80,80), (5,5), the wall cells (1,40), (80,40), (40,1), (40,80) where the extrapolation ghost enters, (75,40), (40,75), (71,30), (2,62), and (8,58), (10,60), (10,64) in the strip next to the front. fire_viscosity = fire_viscosity_bg = 0.4 in test7, so the viscosity coefficient is uniform. Single precision: rel 1e-5 on grad_mag and the propagation term, 2e-5 on the total tendency, the per-axis quantities and the normal, with absolute floors for values near zero. SIGN CAVEAT (fire_behavior note N44, reproduced): for a field decreasing along an axis, the interior Godunov diff2 is a magnitude while the wall-strip ENO1 diff2 is signed.",
      "parameter_overrides": {
        "Lx": 2000.0,
        "Ly": 2000.0,
        "fire_viscosity": 0.4,
        "bdy_eno1_cells": 10
      },
      "expression_template_imports": [
        {
          "ref": "./godunov_eno1_norm_D2_extrapolate_bc.esm",
          "bindings": {
            "NX": 80,
            "NY": 80
          }
        },
        {
          "ref": "${ESD_ROOT}/grids/cartesian_uniform_2d/rules/godunov_upwind_D1x_extrapolate_bc.esm",
          "bindings": {
            "NX": 80,
            "NY": 80
          }
        },
        {
          "ref": "${ESD_ROOT}/grids/cartesian_uniform_2d/rules/godunov_upwind_D1y_extrapolate_bc.esm",
          "bindings": {
            "NX": 80,
            "NY": 80
          }
        },
        {
          "ref": "${ESD_ROOT}/grids/cartesian_uniform_2d/rules/central_D2x_extrapolate_bc.esm",
          "bindings": {
            "NX": 80,
            "NY": 80
          }
        },
        {
          "ref": "${ESD_ROOT}/grids/cartesian_uniform_2d/rules/central_D2y_extrapolate_bc.esm",
          "bindings": {
            "NX": 80,
            "NY": 80
          }
        },
        {
          "ref": "./tests/godunov_step20_stage1_inputs.esm"
        }
      ],
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 12,
            "y": 56
          },
          "expected": 1.008783221244812,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 12,
            "y": 56
          },
          "expected": -0.5785404443740845,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 12,
            "y": 56
          },
          "expected": -0.5823176503181458,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 14,
            "y": 55
          },
          "expected": 1.7142146825790405,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 14,
            "y": 55
          },
          "expected": -1.5782140493392944,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 14,
            "y": 55
          },
          "expected": -1.1295781135559082,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 15,
            "y": 66
          },
          "expected": 0.921559751033783,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 15,
            "y": 66
          },
          "expected": -0.7018488645553589,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 15,
            "y": 66
          },
          "expected": -0.6666386127471924,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 17,
            "y": 62
          },
          "expected": 1.009670376777649,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 17,
            "y": 62
          },
          "expected": -0.2751450538635254,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 17,
            "y": 62
          },
          "expected": -0.25157710909843445,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 19,
            "y": 57
          },
          "expected": 2.699244976043701,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 19,
            "y": 57
          },
          "expected": -2.392396926879883,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 19,
            "y": 57
          },
          "expected": -3.0914411544799805,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 20,
            "y": 65
          },
          "expected": 0.9558852910995483,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 20,
            "y": 65
          },
          "expected": -0.9046502113342285,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 20,
            "y": 65
          },
          "expected": -0.8088884353637695,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 22,
            "y": 58
          },
          "expected": 1.2604304552078247,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 22,
            "y": 58
          },
          "expected": -1.1193839311599731,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 22,
            "y": 58
          },
          "expected": -1.0631152391433716,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 23,
            "y": 66
          },
          "expected": 0.9706542491912842,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 23,
            "y": 66
          },
          "expected": -0.9187670946121216,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 23,
            "y": 66
          },
          "expected": -0.8613925576210022,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 25,
            "y": 58
          },
          "expected": 0.921127438545227,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 25,
            "y": 58
          },
          "expected": -0.4448780119419098,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 25,
            "y": 58
          },
          "expected": -0.38935917615890503,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 26,
            "y": 67
          },
          "expected": 0.9370625019073486,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 26,
            "y": 67
          },
          "expected": -0.8462659120559692,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 26,
            "y": 67
          },
          "expected": -0.7776193618774414,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 30,
            "y": 30
          },
          "expected": 0.9772482514381409,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 30,
            "y": 30
          },
          "expected": -0.9715944528579712,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 30,
            "y": 30
          },
          "expected": -0.9418787360191345,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 60,
            "y": 20
          },
          "expected": 1.0064423084259033,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 60,
            "y": 20
          },
          "expected": -0.8580030202865601,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 60,
            "y": 20
          },
          "expected": -0.8515026569366455,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 50,
            "y": 50
          },
          "expected": 1.0322295427322388,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 50,
            "y": 50
          },
          "expected": -0.4822290539741516,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 50,
            "y": 50
          },
          "expected": -0.4736826419830322,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 12,
            "y": 56
          },
          "expected": 0.920306384563446,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 12,
            "y": 56
          },
          "expected": 0.4131341576576233,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 12,
            "y": 56
          },
          "expected": 0.9122934937477112,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 12,
            "y": 56
          },
          "expected": 0.40953710675239563,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 14,
            "y": 55
          },
          "expected": 0.28484436869621277,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 14,
            "y": 55
          },
          "expected": 1.6903833150863647,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 14,
            "y": 55
          },
          "expected": 0.16616609692573547,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 14,
            "y": 55
          },
          "expected": 0.9860978126525879,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 15,
            "y": 66
          },
          "expected": 0.7073400616645813,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 15,
            "y": 66
          },
          "expected": 0.5907135009765625,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 15,
            "y": 66
          },
          "expected": 0.767546534538269,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 15,
            "y": 66
          },
          "expected": 0.6409931182861328,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 17,
            "y": 62
          },
          "expected": 0.997007429599762,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 17,
            "y": 62
          },
          "expected": 0.15940673649311066,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 17,
            "y": 62
          },
          "expected": 0.987458348274231,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 17,
            "y": 62
          },
          "expected": 0.15787997841835022,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 19,
            "y": 57
          },
          "expected": 0.7066952586174011,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 19,
            "y": 57
          },
          "expected": 2.6298205852508545,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 19,
            "y": 57
          },
          "expected": 0.2618122100830078,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 19,
            "y": 57
          },
          "expected": 0.974280059337616,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 20,
            "y": 65
          },
          "expected": 0.20843414962291718,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 20,
            "y": 65
          },
          "expected": 0.932883620262146,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 20,
            "y": 65
          },
          "expected": 0.21805350482463837,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 20,
            "y": 65
          },
          "expected": 0.9759367108345032,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 22,
            "y": 58
          },
          "expected": 0.06373664736747742,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 22,
            "y": 58
          },
          "expected": 1.2588179111480713,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 22,
            "y": 58
          },
          "expected": 0.05056736618280411,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 22,
            "y": 58
          },
          "expected": 0.998720645904541,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 23,
            "y": 66
          },
          "expected": 0.20870117843151093,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 23,
            "y": 66
          },
          "expected": 0.9479522705078125,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 23,
            "y": 66
          },
          "expected": 0.21501082181930542,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 23,
            "y": 66
          },
          "expected": 0.9766116142272949,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 25,
            "y": 58
          },
          "expected": 0.8832383751869202,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 25,
            "y": 58
          },
          "expected": 0.2614684998989105,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 25,
            "y": 58
          },
          "expected": 0.9588665962219238,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 25,
            "y": 58
          },
          "expected": 0.2838570177555084,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 26,
            "y": 67
          },
          "expected": 0.511641263961792,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 26,
            "y": 67
          },
          "expected": 0.7850537300109863,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 26,
            "y": 67
          },
          "expected": 0.5460054278373718,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 26,
            "y": 67
          },
          "expected": 0.837781548500061,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 30,
            "y": 30
          },
          "expected": 0.21545898914337158,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 30,
            "y": 30
          },
          "expected": 0.9532006978988647,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 30,
            "y": 30
          },
          "expected": 0.22047516703605652,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 30,
            "y": 30
          },
          "expected": 0.9753925204277039,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 50,
            "y": 50
          },
          "expected": 0.9887866377830505,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 50,
            "y": 50
          },
          "expected": 0.29630860686302185,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 50,
            "y": 50
          },
          "expected": 0.9579133987426758,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 50,
            "y": 50
          },
          "expected": 0.2870568633079529,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 60,
            "y": 20
          },
          "expected": 0.7161474823951721,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 60,
            "y": 20
          },
          "expected": 0.7071484327316284,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 60,
            "y": 20
          },
          "expected": 0.7115633487701416,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 60,
            "y": 20
          },
          "expected": 0.7026219367980957,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 1,
            "y": 1
          },
          "expected": 0.9607469439506531,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 1,
            "y": 1
          },
          "expected": -0.01707698591053486,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 1,
            "y": 1
          },
          "expected": -0.01707698591053486,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 1,
            "y": 1
          },
          "expected": -0.32111817598342896,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 1,
            "y": 1
          },
          "expected": -0.9054931402206421,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 1,
            "y": 1
          },
          "expected": -0.3342380225658417,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 1,
            "y": 1
          },
          "expected": -0.9424886703491211,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 1,
            "y": 40
          },
          "expected": 0.9565963745117188,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 1,
            "y": 40
          },
          "expected": -0.01700321026146412,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 1,
            "y": 40
          },
          "expected": -0.016959069296717644,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 1,
            "y": 40
          },
          "expected": -0.6963794231414795,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 1,
            "y": 40
          },
          "expected": -0.6558447480201721,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 1,
            "y": 40
          },
          "expected": -0.7279762029647827,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 1,
            "y": 40
          },
          "expected": -0.6856023073196411,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 80,
            "y": 40
          },
          "expected": 0.9431357979774475,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 80,
            "y": 40
          },
          "expected": -0.018146438524127007,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 80,
            "y": 40
          },
          "expected": -0.01807500049471855,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 80,
            "y": 40
          },
          "expected": 0.890917956829071,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 80,
            "y": 40
          },
          "expected": -0.30946776270866394,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 80,
            "y": 40
          },
          "expected": 0.9446337223052979,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 80,
            "y": 40
          },
          "expected": -0.3281264007091522,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 1
          },
          "expected": 0.9623169302940369,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 1
          },
          "expected": -0.01810791902244091,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 1
          },
          "expected": -0.01777046173810959,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 1
          },
          "expected": 0.2623876929283142,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 1
          },
          "expected": -0.925854504108429,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 1
          },
          "expected": 0.2726624310016632,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 1
          },
          "expected": -0.9621096849441528,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 80
          },
          "expected": 0.9592926502227783,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 80
          },
          "expected": -0.8218752145767212,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 80
          },
          "expected": -0.7904891967773438,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 80
          },
          "expected": 0.6433374285697937,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 80
          },
          "expected": 0.7115893363952637,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 80
          },
          "expected": 0.6706372499465942,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 80
          },
          "expected": 0.7417854070663452,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 80,
            "y": 80
          },
          "expected": 1.0361480712890625,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 80,
            "y": 80
          },
          "expected": -0.5494412183761597,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 80,
            "y": 80
          },
          "expected": -0.5494412183761597,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 80,
            "y": 80
          },
          "expected": 0.9808251857757568,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 80,
            "y": 80
          },
          "expected": 0.3340429663658142,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 80,
            "y": 80
          },
          "expected": 0.9466071724891663,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 80,
            "y": 80
          },
          "expected": 0.3223892152309418,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 5,
            "y": 5
          },
          "expected": 0.9672893285751343,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 5,
            "y": 5
          },
          "expected": -0.017193274572491646,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 5,
            "y": 5
          },
          "expected": -0.017758211120963097,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 5,
            "y": 5
          },
          "expected": -0.2978564500808716,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 5,
            "y": 5
          },
          "expected": -0.9202880859375,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 5,
            "y": 5
          },
          "expected": -0.30792900919914246,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 5,
            "y": 5
          },
          "expected": -0.9514092803001404,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 75,
            "y": 40
          },
          "expected": 0.9454014897346497,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 75,
            "y": 40
          },
          "expected": -0.016804225742816925,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 75,
            "y": 40
          },
          "expected": -0.017417730763554573,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 75,
            "y": 40
          },
          "expected": 0.8839452862739563,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 75,
            "y": 40
          },
          "expected": -0.3352978527545929,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 75,
            "y": 40
          },
          "expected": 0.9349945187568665,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 75,
            "y": 40
          },
          "expected": -0.35466185212135315,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 75
          },
          "expected": 0.948695957660675,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 75
          },
          "expected": -0.7353954315185547,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 75
          },
          "expected": -0.6964895725250244,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 75
          },
          "expected": 0.7383349537849426,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 75
          },
          "expected": 0.5957226753234863,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 75
          },
          "expected": 0.7782629132270813,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 75
          },
          "expected": 0.6279383897781372,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 10,
            "y": 60
          },
          "expected": 0.938305139541626,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 10,
            "y": 60
          },
          "expected": -0.016678089275956154,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 10,
            "y": 60
          },
          "expected": -0.016800178214907646,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 10,
            "y": 60
          },
          "expected": -0.9379479885101318,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 10,
            "y": 60
          },
          "expected": -0.02588745206594467,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 10,
            "y": 60
          },
          "expected": -0.9996193051338196,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 10,
            "y": 60
          },
          "expected": -0.0275895856320858,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 8,
            "y": 58
          },
          "expected": 1.0346107482910156,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 8,
            "y": 58
          },
          "expected": -0.02420082502067089,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 8,
            "y": 58
          },
          "expected": -0.023516448214650154,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 8,
            "y": 58
          },
          "expected": -1.0207922458648682,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 8,
            "y": 58
          },
          "expected": -0.16853027045726776,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 8,
            "y": 58
          },
          "expected": -0.9866436719894409,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 8,
            "y": 58
          },
          "expected": -0.1628924161195755,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 10,
            "y": 64
          },
          "expected": 0.9364401698112488,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 10,
            "y": 64
          },
          "expected": -0.033993758261203766,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 10,
            "y": 64
          },
          "expected": -0.03423306345939636,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 10,
            "y": 64
          },
          "expected": -0.9074755907058716,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 10,
            "y": 64
          },
          "expected": 0.23110228776931763,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 10,
            "y": 64
          },
          "expected": -0.9690694212913513,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 10,
            "y": 64
          },
          "expected": 0.24678808450698853,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 71,
            "y": 30
          },
          "expected": 0.9467691779136658,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 71,
            "y": 30
          },
          "expected": -0.016936220228672028,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 71,
            "y": 30
          },
          "expected": -0.016108671203255653,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 71,
            "y": 30
          },
          "expected": 0.8030078411102295,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 71,
            "y": 30
          },
          "expected": -0.5015478730201721,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 71,
            "y": 30
          },
          "expected": 0.8481557965278625,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 71,
            "y": 30
          },
          "expected": -0.5297467112541199,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 2,
            "y": 62
          },
          "expected": 0.9390222430229187,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 2,
            "y": 62
          },
          "expected": -0.01715197041630745,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 2,
            "y": 62
          },
          "expected": -0.0175407063215971,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 2,
            "y": 62
          },
          "expected": -0.9382873773574829,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 2,
            "y": 62
          },
          "expected": 0.03714233264327049,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 2,
            "y": 62
          },
          "expected": -0.9992173314094543,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 2,
            "y": 62
          },
          "expected": 0.03955426067113876,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        }
      ]
    },
    {
      "id": "weno5_eno1_step20_stage1",
      "description": "Reference: NCAR fire_behavior test7 (80x80 fire cells of 25 m, dt = 0.5 s, num_tiles = 1) with the shipped namelist, i.e. fire_behavior's namelist-default scheme fire_upwinding = 9 (hybrid: 5th-order Jiang-Shu WENO5 within fire_lsm_band_ngp = 4 cells of the front, upwind side selected by the wind-relative propagation sign, first-order ENO1 minmod elsewhere and within BDY_ENO1 = 10 cells of the walls, one-cell guarded linear-extrapolation halo), default real32 build, dumped in-model by the ctessum-claude/fire_behavior fork (c9dda02, -DESM_DUMP=ON): ls_tend dump call 58 = Runge-Kutta stage 1 of step 20 (t = 10 s). The inputs psi, ros and the mid-flame wind uf, vf are the full 80x80 dumped fields injected as [x, y] const fields; this test imports EarthSciDiscretizations' weno5_eno1_norm_D2_extrapolate_bc (|grad psi|) and weno5_eno1_D1x/D1y_extrapolate_bc (the per-axis derivatives diff2x, diff2y that also give the normal), with bdy_eno1_cells = 10 and weno_band_cells = 4 (the rules' free names), and central_D2x/D2y_extrapolate_bc for the viscosity term's second differences (fire_behavior's (diffrx - difflx) with the same extrapolated ghost, which makes the wall-cell second difference vanish when the ghost is the linear one). Asserted at 16 cells: 8 cells inside the WENO band around the front (|lfn| < 100 m, 11 <= i, j <= 70; the band spans i 13-28, j 56-69 at this step and the selector signo = (grad4 psi . U) d4 psi changes sign across it, so both upwind orientations are exercised), 3 ENO1 far-field cells, 2 cells inside the 10-cell wall strip (ENO1 by the index rule) and 3 wall cells (i = 1, j = 1, and the corner (80, 80)), where the guarded extrapolation ghost enters; per cell psi_x, psi_y (the dumped diff2x, diff2y), grad_mag (grad), nvx, nvy, tend_adv and tend. fire_viscosity = fire_viscosity_bg = 0.4, so the viscosity coefficient is uniform (viscosity_var = 0.4 on every cell of the dump). Single precision: rel 1e-5 on grad_mag and the propagation term, 2e-5 on the per-axis derivatives, the normal and the total tendency, with absolute floors for values near zero. The whole-field agreement of the transcribed scheme with the dump was checked offline in a NumPy replica: grad <= 7.4e-7 relative, diff2x/y <= 1.3e-5 relative on values above 1e-3, tend <= 1.1e-5, i.e. real32 roundoff.",
      "parameter_overrides": {
        "Lx": 2000.0,
        "Ly": 2000.0,
        "fire_viscosity": 0.4,
        "bdy_eno1_cells": 10,
        "weno_band_cells": 4
      },
      "expression_template_imports": [
        {
          "ref": "${ESD_ROOT}/grids/cartesian_uniform_2d/rules/weno5_eno1_norm_D2_extrapolate_bc.esm",
          "bindings": {
            "NX": 80,
            "NY": 80
          }
        },
        {
          "ref": "${ESD_ROOT}/grids/cartesian_uniform_2d/rules/weno5_eno1_D1x_extrapolate_bc.esm",
          "bindings": {
            "NX": 80,
            "NY": 80
          }
        },
        {
          "ref": "${ESD_ROOT}/grids/cartesian_uniform_2d/rules/weno5_eno1_D1y_extrapolate_bc.esm",
          "bindings": {
            "NX": 80,
            "NY": 80
          }
        },
        {
          "ref": "${ESD_ROOT}/grids/cartesian_uniform_2d/rules/central_D2x_extrapolate_bc.esm",
          "bindings": {
            "NX": 80,
            "NY": 80
          }
        },
        {
          "ref": "${ESD_ROOT}/grids/cartesian_uniform_2d/rules/central_D2y_extrapolate_bc.esm",
          "bindings": {
            "NX": 80,
            "NY": 80
          }
        },
        {
          "ref": "./tests/weno5_eno1_step20_stage1_inputs.esm"
        }
      ],
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 17,
            "y": 57
          },
          "expected": 2.545614004135132,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 17,
            "y": 57
          },
          "expected": 0.6075868010520935,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 17,
            "y": 57
          },
          "expected": -2.472041368484497,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 17,
            "y": 57
          },
          "expected": 0.23867985606193542,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 17,
            "y": 57
          },
          "expected": -0.9710983037948608,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 17,
            "y": 57
          },
          "expected": -0.045981667935848236,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 17,
            "y": 57
          },
          "expected": -0.039460472762584686,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 21,
            "y": 66
          },
          "expected": 1.0003001689910889,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 21,
            "y": 66
          },
          "expected": -0.08848945796489716,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 21,
            "y": 66
          },
          "expected": 0.996378481388092,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 21,
            "y": 66
          },
          "expected": -0.08846289664506912,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 21,
            "y": 66
          },
          "expected": 0.9960793852806091,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 21,
            "y": 66
          },
          "expected": -0.9031526446342468,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 21,
            "y": 66
          },
          "expected": -0.8391401767730713,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 22,
            "y": 58
          },
          "expected": 1.405798077583313,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 22,
            "y": 58
          },
          "expected": -0.9745906591415405,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 22,
            "y": 58
          },
          "expected": -1.0131343603134155,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 22,
            "y": 58
          },
          "expected": -0.6932649612426758,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 22,
            "y": 58
          },
          "expected": -0.7206826210021973,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 22,
            "y": 58
          },
          "expected": -0.024987636134028435,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 22,
            "y": 58
          },
          "expected": -0.02279062196612358,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 23,
            "y": 56
          },
          "expected": 0.9756455421447754,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 23,
            "y": 56
          },
          "expected": 0.11277984827756882,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 23,
            "y": 56
          },
          "expected": -0.9691052436828613,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 23,
            "y": 56
          },
          "expected": 0.11559509485960007,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 23,
            "y": 56
          },
          "expected": -0.9932963848114014,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 23,
            "y": 56
          },
          "expected": -0.01734180375933647,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 23,
            "y": 56
          },
          "expected": -0.015520437620580196,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 24,
            "y": 60
          },
          "expected": 1.1697722673416138,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 24,
            "y": 60
          },
          "expected": 1.1671230792999268,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 24,
            "y": 60
          },
          "expected": 0.07868194580078125,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 24,
            "y": 60
          },
          "expected": 0.9977352023124695,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 24,
            "y": 60
          },
          "expected": 0.06726261228322983,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 24,
            "y": 60
          },
          "expected": -0.3580305576324463,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 24,
            "y": 60
          },
          "expected": -0.6409715414047241,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 25,
            "y": 57
          },
          "expected": 0.9737127423286438,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 25,
            "y": 57
          },
          "expected": 0.7053143382072449,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 25,
            "y": 57
          },
          "expected": -0.671303391456604,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 25,
            "y": 57
          },
          "expected": 0.7243556380271912,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 25,
            "y": 57
          },
          "expected": -0.6894264817237854,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 25,
            "y": 57
          },
          "expected": -0.01854361779987812,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 25,
            "y": 57
          },
          "expected": -0.01669306494295597,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 25,
            "y": 65
          },
          "expected": 1.0395927429199219,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 25,
            "y": 65
          },
          "expected": 0.6479994058609009,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 25,
            "y": 65
          },
          "expected": 0.8129266500473022,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 25,
            "y": 65
          },
          "expected": 0.6233203411102295,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 25,
            "y": 65
          },
          "expected": 0.7819663882255554,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 25,
            "y": 65
          },
          "expected": -0.8968417048454285,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 25,
            "y": 65
          },
          "expected": -0.8568363785743713,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 26,
            "y": 58
          },
          "expected": 0.9949598908424377,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 26,
            "y": 58
          },
          "expected": 0.9392926096916199,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 26,
            "y": 58
          },
          "expected": -0.3281381130218506,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 26,
            "y": 58
          },
          "expected": 0.944050669670105,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 26,
            "y": 58
          },
          "expected": -0.3298003375530243,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 26,
            "y": 58
          },
          "expected": -0.020028969272971153,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 26,
            "y": 58
          },
          "expected": -0.01698843389749527,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 30,
            "y": 30
          },
          "expected": 0.9772482514381409,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 30,
            "y": 30
          },
          "expected": 0.21545898914337158,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 30,
            "y": 30
          },
          "expected": -0.9532006978988647,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 30,
            "y": 30
          },
          "expected": 0.22047516703605652,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 30,
            "y": 30
          },
          "expected": -0.9753925204277039,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 30,
            "y": 30
          },
          "expected": -0.01737029105424881,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 30,
            "y": 30
          },
          "expected": -0.016839029267430305,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 50,
            "y": 50
          },
          "expected": 1.0322295427322388,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 50,
            "y": 50
          },
          "expected": 0.9887866377830505,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 50,
            "y": 50
          },
          "expected": -0.29630860686302185,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 50,
            "y": 50
          },
          "expected": 0.9579133987426758,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 50,
            "y": 50
          },
          "expected": -0.2870568633079529,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 50,
            "y": 50
          },
          "expected": -0.018347566947340965,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 50,
            "y": 50
          },
          "expected": -0.01802239753305912,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 60,
            "y": 20
          },
          "expected": 1.0064423084259033,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 60,
            "y": 20
          },
          "expected": 0.7161474823951721,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 60,
            "y": 20
          },
          "expected": -0.7071484327316284,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 60,
            "y": 20
          },
          "expected": 0.7115633487701416,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 60,
            "y": 20
          },
          "expected": -0.7026219367980957,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 60,
            "y": 20
          },
          "expected": -0.01788920722901821,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 60,
            "y": 20
          },
          "expected": -0.01775367558002472,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 5,
            "y": 60
          },
          "expected": 0.9391743540763855,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 5,
            "y": 60
          },
          "expected": -0.9390014410018921,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 5,
            "y": 60
          },
          "expected": -0.018022460862994194,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 5,
            "y": 60
          },
          "expected": -0.999815821647644,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 5,
            "y": 60
          },
          "expected": -0.019189685583114624,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 5,
            "y": 60
          },
          "expected": -0.01968720741569996,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 5,
            "y": 60
          },
          "expected": -0.02005324885249138,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 75,
            "y": 40
          },
          "expected": 0.9454014897346497,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 75,
            "y": 40
          },
          "expected": 0.8839452862739563,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 75,
            "y": 40
          },
          "expected": -0.3352978527545929,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 75,
            "y": 40
          },
          "expected": 0.9349945187568665,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 75,
            "y": 40
          },
          "expected": -0.35466185212135315,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 75,
            "y": 40
          },
          "expected": -0.016804225742816925,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 75,
            "y": 40
          },
          "expected": -0.017417730763554573,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 1,
            "y": 60
          },
          "expected": 0.9394055604934692,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 1,
            "y": 60
          },
          "expected": -0.9392932057380676,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 1,
            "y": 60
          },
          "expected": -0.014527588151395321,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 1,
            "y": 60
          },
          "expected": -0.999880313873291,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 1,
            "y": 60
          },
          "expected": -0.0154646597802639,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 1,
            "y": 60
          },
          "expected": -0.016697648912668228,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 1,
            "y": 60
          },
          "expected": -0.016350295394659042,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 1
          },
          "expected": 0.9623169302940369,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 1
          },
          "expected": 0.2623876929283142,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 1
          },
          "expected": -0.925854504108429,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 1
          },
          "expected": 0.2726624310016632,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 1
          },
          "expected": -0.9621096849441528,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 1
          },
          "expected": -0.01810791902244091,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 1
          },
          "expected": -0.01777046173810959,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 80,
            "y": 80
          },
          "expected": 1.0361480712890625,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 80,
            "y": 80
          },
          "expected": 0.9808251857757568,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 80,
            "y": 80
          },
          "expected": 0.3340429663658142,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 80,
            "y": 80
          },
          "expected": 0.9466071724891663,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 80,
            "y": 80
          },
          "expected": 0.3223892152309418,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 80,
            "y": 80
          },
          "expected": -0.5494412183761597,
          "tolerance": {
            "rel": 1e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 80,
            "y": 80
          },
          "expected": -0.5494412183761597,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        }
      ]
    },
    {
      "id": "weno5_pure_step20_stage1",
      "description": "fire_upwinding = 7, PURE 5th-order WENO -- the third of the eleven upwinding options to be covered, after 9 (fire_behavior's namelist-default hybrid) and 4 (classical Godunov). Option 7 is not a separate discretization: physics/level_set_mod.F90 case (7) is byte-for-byte case (9)'s in-band branch with the `abs(lfn) < threshold_hlu` test removed, so the SAME EarthSciDiscretizations weno5_eno1 rules reproduce it once weno_band_cells is set past the domain diagonal (1e6 cells x 25 m here, against the 2828 m diagonal). The ENO1 strip within bdy_eno1_cells = 10 of the wall is NOT part of the case statement and still applies, which is why the wall cells (5,40), (75,40) and (11,11) are asserted too. Besides tend and grad_mag, the per-axis derivatives psi_x, psi_y (the dumped diff2x, diff2y) and the normal nvx, nvy are asserted at all ten cells (rel 2e-5, abs 1e-7). Reference: the test7 standalone rerun with fire_upwinding = 7 (data/eqwefic/dumps/fire/run_weno5/esm_dump_ls_tend_58.json, real32, gfortran 13.3 -O2 in the EqWeFiC container), Runge-Kutta stage 1 of step 20. The option is genuinely discriminating: against the fire_upwinding = 9 run of the same case, 3480 of the 6400 interior cells have a different tendency and the largest difference is 1.30 m/s, e.g. -0.02769 against -0.02686 at (40,40) where |lfn| = 646 m, five times the 100 m hybrid band. Near the front, where both schemes are in band, the two runs still agree to the last real32 digit at step 20. rel 2e-5, the same tolerance as the hybrid test, because the WENO5 smoothness weights amplify real32 rounding. Note: the five rule imports bind NX/NY to the literal 80, not to the metaparameter names -- a TEST-level import is injected after the model's index sets are resolved, so binding a symbol there raises template_import_index_set_conflict. The MODEL-level grid import binds the names, which is where the metaparameter has to be honoured.",
      "expression_template_imports": [
        {
          "ref": "${ESD_ROOT}/grids/cartesian_uniform_2d/rules/weno5_eno1_norm_D2_extrapolate_bc.esm",
          "bindings": {
            "NX": 80,
            "NY": 80
          }
        },
        {
          "ref": "${ESD_ROOT}/grids/cartesian_uniform_2d/rules/weno5_eno1_D1x_extrapolate_bc.esm",
          "bindings": {
            "NX": 80,
            "NY": 80
          }
        },
        {
          "ref": "${ESD_ROOT}/grids/cartesian_uniform_2d/rules/weno5_eno1_D1y_extrapolate_bc.esm",
          "bindings": {
            "NX": 80,
            "NY": 80
          }
        },
        {
          "ref": "${ESD_ROOT}/grids/cartesian_uniform_2d/rules/central_D2x_extrapolate_bc.esm",
          "bindings": {
            "NX": 80,
            "NY": 80
          }
        },
        {
          "ref": "${ESD_ROOT}/grids/cartesian_uniform_2d/rules/central_D2y_extrapolate_bc.esm",
          "bindings": {
            "NX": 80,
            "NY": 80
          }
        },
        {
          "ref": "./tests/weno5_pure_step20_stage1_inputs.esm"
        }
      ],
      "parameter_overrides": {
        "Lx": 2000.0,
        "Ly": 2000.0,
        "fire_viscosity": 0.4,
        "bdy_eno1_cells": 10,
        "weno_band_cells": 1000000.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 18,
            "y": 64
          },
          "expected": -0.3517639935016632,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 17,
            "y": 57
          },
          "expected": -0.06454001367092133,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 40
          },
          "expected": -0.027688151225447655,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 30,
            "y": 50
          },
          "expected": -0.030216578394174576,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 12,
            "y": 12
          },
          "expected": -0.028674522414803505,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 20,
            "y": 66
          },
          "expected": -1.2457104921340942,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 5,
            "y": 40
          },
          "expected": -0.028804698958992958,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 75,
            "y": 40
          },
          "expected": -0.028540227562189102,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 11,
            "y": 11
          },
          "expected": -0.028880592435598373,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 70,
            "y": 70
          },
          "expected": -0.7183499336242676,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 18,
            "y": 64
          },
          "expected": 0.987514078617096,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 40
          },
          "expected": 0.9892694354057312,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 12,
            "y": 12
          },
          "expected": 0.9773737192153931,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 70,
            "y": 70
          },
          "expected": 0.9917244911193848,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 5,
            "y": 40
          },
          "expected": -0.6455346941947937,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 5,
            "y": 40
          },
          "expected": -0.7274096608161926,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 5,
            "y": 40
          },
          "expected": -0.6637594699859619,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 5,
            "y": 40
          },
          "expected": -0.7479459643363953,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 11,
            "y": 11
          },
          "expected": -0.24007324874401093,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 11,
            "y": 11
          },
          "expected": -1.001254916191101,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 11,
            "y": 11
          },
          "expected": -0.23316359519958496,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 11,
            "y": 11
          },
          "expected": -0.9724373817443848,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 12,
            "y": 12
          },
          "expected": -0.21013671159744263,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 12,
            "y": 12
          },
          "expected": -0.954516589641571,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 12,
            "y": 12
          },
          "expected": -0.21500137448310852,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 12,
            "y": 12
          },
          "expected": -0.9766136407852173,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 17,
            "y": 57
          },
          "expected": 0.6075868010520935,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 17,
            "y": 57
          },
          "expected": -2.472165584564209,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 17,
            "y": 57
          },
          "expected": 0.2386685460805893,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 17,
            "y": 57
          },
          "expected": -0.9711010456085205,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 18,
            "y": 64
          },
          "expected": -0.7092993855476379,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 18,
            "y": 64
          },
          "expected": 0.6870796084403992,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 18,
            "y": 64
          },
          "expected": -0.718267560005188,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 18,
            "y": 64
          },
          "expected": 0.6957668662071228,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 20,
            "y": 66
          },
          "expected": -0.2688955068588257,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 20,
            "y": 66
          },
          "expected": 0.9649879932403564,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 20,
            "y": 66
          },
          "expected": -0.26842525601387024,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 20,
            "y": 66
          },
          "expected": 0.9633004069328308,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 30,
            "y": 50
          },
          "expected": 0.6263269186019897,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 30,
            "y": 50
          },
          "expected": -0.7855163812637329,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 30,
            "y": 50
          },
          "expected": 0.6234280467033386,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 30,
            "y": 50
          },
          "expected": -0.7818807363510132,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 40
          },
          "expected": 0.6660107374191284,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 40
          },
          "expected": -0.731494128704071,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 40
          },
          "expected": 0.6732348799705505,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 40
          },
          "expected": -0.7394285798072815,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 70,
            "y": 70
          },
          "expected": 0.9656640887260437,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 70,
            "y": 70
          },
          "expected": 0.22585448622703552,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 70,
            "y": 70
          },
          "expected": 0.9737221002578735,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 70,
            "y": 70
          },
          "expected": 0.2277391254901886,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 75,
            "y": 40
          },
          "expected": 0.8839452862739563,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 75,
            "y": 40
          },
          "expected": -0.3352978527545929,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 75,
            "y": 40
          },
          "expected": 0.9349945187568665,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 75,
            "y": 40
          },
          "expected": -0.35466185212135315,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        }
      ]
    },
    {
      "id": "weno5_blend_step20_stage1",
      "description": "fire_upwinding = 10, the WENO5/ENO1 scheme with a cosine BLENDING ZONE -- the fourth of the eleven upwinding options covered, after 9 (fire_behavior's namelist-default hard-edged hybrid), 4 (classical Godunov) and 7 (pure WENO5). Where option 9 switches abruptly from WENO5 to ENO1 at |psi| = B = weno_band_cells dx = 100 m, option 10 keeps WENO5 out to B, tapers with mask = 0.5 (1 + cos(pi (|psi| - B)/B)) over B < |psi| <= 2B, and is pure ENO1 beyond -- diff2 = mask diff2_weno + (1 - mask) diff2_eno. The blend is applied to the PER-AXIS derivatives (diff2x = mask diff2x_weno + (1 - mask) diff2x_eno, likewise diff2y) and both |grad psi| = sqrt(diff2x^2 + diff2y^2) and the normal nvx = diff2x/sqrt(grad^2 + eps) are built from them, so the test imports the blend for the norm AND for the bare derivatives: EarthSciDiscretizations' weno5_eno1_blend_norm_D2_extrapolate_bc (whose stencils write the mask as one clamped expression rather than three branches) and the local per-axis rules ./weno5_eno1_blend_D1x_extrapolate_bc and ./weno5_eno1_blend_D1y_extrapolate_bc (ESD's per-axis frame around ESD's blend interior stencil; ESD has no per-axis blend rule). Lowering psi_x, psi_y with the hard-edged fire_upwinding = 9 per-axis rules instead leaves |grad psi| and the tendency right but the derivatives and the normal wrong throughout the zone: it fails 32 of these assertions, e.g. nvy = 0.0697 against the reference 0.1031 at (11,62) and -0.688 against -0.963 at (17,56). IT IS GENUINELY DISCRIMINATING, and in exactly the place the physics says it should be: against the fire_upwinding = 9 run of the same case, 185 interior cells have a different tendency and 173 of them lie inside the blending zone, which holds 233 cells; the largest difference is 0.468 m/s and the largest anywhere OUTSIDE the zone is 2.0e-3. The four cells (11,57), (11,58), (11,59) and (11,62) are in the zone (|psi| = 137 to 152 m, mask 0.47 to 0.70); (21,60) at |psi| = 81 m and (17,57) at |psi| = 54 m are inside B and therefore pure WENO5 (mask = 1); (18,64), (20,66), (40,40) and (12,12) are unchanged from the option-9 run to the last real32 digit, which is the check that the blend does not disturb cells it should not touch. psi_x, psi_y (the dumped diff2x, diff2y) and nvx, nvy are asserted at those four zone cells, at four more zone cells spanning the taper -- (22,61) mask 0.999, (17,56) 0.905, (28,64) 0.795, (12,54) 0.225, where tend and grad_mag are asserted too -- at the in-band cells (17,57), (21,60), (18,64), and at the ENO1 cells (40,40), (12,12) and (5,5) (far field and wall strip). Reference: data/eqwefic/dumps/fire/run_blend/esm_dump_ls_tend_58.json, real32, rel 2e-5. The rule reads a free name pi_blend, which this component now takes from the fire constants library (fire_behavior's own truncated PI = 3.1415926, share/constants_mod.F90:18).",
      "expression_template_imports": [
        {
          "ref": "${ESD_ROOT}/grids/cartesian_uniform_2d/rules/weno5_eno1_blend_norm_D2_extrapolate_bc.esm",
          "bindings": {
            "NX": 80,
            "NY": 80
          }
        },
        {
          "ref": "./weno5_eno1_blend_D1x_extrapolate_bc.esm",
          "bindings": {
            "NX": 80,
            "NY": 80
          }
        },
        {
          "ref": "./weno5_eno1_blend_D1y_extrapolate_bc.esm",
          "bindings": {
            "NX": 80,
            "NY": 80
          }
        },
        {
          "ref": "${ESD_ROOT}/grids/cartesian_uniform_2d/rules/central_D2x_extrapolate_bc.esm",
          "bindings": {
            "NX": 80,
            "NY": 80
          }
        },
        {
          "ref": "${ESD_ROOT}/grids/cartesian_uniform_2d/rules/central_D2y_extrapolate_bc.esm",
          "bindings": {
            "NX": 80,
            "NY": 80
          }
        },
        {
          "ref": "./tests/weno5_blend_step20_stage1_inputs.esm"
        }
      ],
      "parameter_overrides": {
        "Lx": 2000.0,
        "Ly": 2000.0,
        "fire_viscosity": 0.4,
        "bdy_eno1_cells": 10,
        "weno_band_cells": 4
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 11,
            "y": 57
          },
          "expected": -0.026899786666035652,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 11,
            "y": 58
          },
          "expected": -0.026327010244131088,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 11,
            "y": 59
          },
          "expected": -0.02653227001428604,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 11,
            "y": 62
          },
          "expected": -0.026615459471940994,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 21,
            "y": 60
          },
          "expected": -0.0424681156873703,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 18,
            "y": 64
          },
          "expected": -0.3517639935016632,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 20,
            "y": 66
          },
          "expected": -1.2457104921340942,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 40
          },
          "expected": -0.026860108599066734,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 12,
            "y": 12
          },
          "expected": -0.02887246385216713,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 17,
            "y": 57
          },
          "expected": -0.0645393654704094,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 11,
            "y": 57
          },
          "expected": 0.9719451069831848,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 17,
            "y": 57
          },
          "expected": 2.5457119941711426,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 40
          },
          "expected": 0.9608290195465088,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 21,
            "y": 60
          },
          "expected": 2.225917339324951,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "pi_blend",
          "time": 0.0,
          "expected": 3.1415926,
          "tolerance": {
            "rel": 1e-09
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 11,
            "y": 57
          },
          "expected": -0.9167547821998596,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 11,
            "y": 57
          },
          "expected": -0.3228590190410614,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 11,
            "y": 57
          },
          "expected": -0.9432165622711182,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 11,
            "y": 57
          },
          "expected": -0.3321782350540161,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 11,
            "y": 58
          },
          "expected": -0.9530215263366699,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 11,
            "y": 58
          },
          "expected": -0.2412606030702591,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 11,
            "y": 58
          },
          "expected": -0.9694189429283142,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 11,
            "y": 58
          },
          "expected": -0.24541166424751282,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 11,
            "y": 59
          },
          "expected": -0.9795873761177063,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 11,
            "y": 59
          },
          "expected": -0.1549353301525116,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 11,
            "y": 59
          },
          "expected": -0.9877219200134277,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 11,
            "y": 59
          },
          "expected": -0.1562219113111496,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 11,
            "y": 62
          },
          "expected": -0.9898958206176758,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 11,
            "y": 62
          },
          "expected": 0.1026533767580986,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 11,
            "y": 62
          },
          "expected": -0.9946659207344055,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 11,
            "y": 62
          },
          "expected": 0.10314804315567017,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 22,
            "y": 61
          },
          "expected": 1.7308987379074097,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 22,
            "y": 61
          },
          "expected": -0.4177160859107971,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 22,
            "y": 61
          },
          "expected": 0.9720932841300964,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 22,
            "y": 61
          },
          "expected": -0.23459431529045105,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 17,
            "y": 56
          },
          "expected": 0.8480704426765442,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 17,
            "y": 56
          },
          "expected": -3.0299766063690186,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 17,
            "y": 56
          },
          "expected": 0.269534707069397,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 17,
            "y": 56
          },
          "expected": -0.9629906415939331,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 28,
            "y": 64
          },
          "expected": 2.3064472675323486,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 28,
            "y": 64
          },
          "expected": -2.1426939964294434,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 28,
            "y": 64
          },
          "expected": 0.7326362133026123,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 28,
            "y": 64
          },
          "expected": -0.6806204915046692,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 12,
            "y": 54
          },
          "expected": 0.03358006477355957,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 12,
            "y": 54
          },
          "expected": -0.8947361707687378,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 12,
            "y": 54
          },
          "expected": 0.03750428184866905,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 12,
            "y": 54
          },
          "expected": -0.9992964267730713,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 17,
            "y": 57
          },
          "expected": 0.6075868010520935,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 17,
            "y": 57
          },
          "expected": -2.472142219543457,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 17,
            "y": 57
          },
          "expected": 0.23867067694664001,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 17,
            "y": 57
          },
          "expected": -0.9711005091667175,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 21,
            "y": 60
          },
          "expected": 0.37594878673553467,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 21,
            "y": 60
          },
          "expected": -2.193939447402954,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 21,
            "y": 60
          },
          "expected": 0.16889610886573792,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 21,
            "y": 60
          },
          "expected": -0.9856338500976562,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 18,
            "y": 64
          },
          "expected": -0.7092993855476379,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 18,
            "y": 64
          },
          "expected": 0.6870796084403992,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 18,
            "y": 64
          },
          "expected": -0.718267560005188,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 18,
            "y": 64
          },
          "expected": 0.6957668662071228,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 40
          },
          "expected": 0.6217920184135437,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 40
          },
          "expected": -0.7325073480606079,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 40
          },
          "expected": 0.64714115858078,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 40
          },
          "expected": -0.7623701095581055,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 12,
            "y": 12
          },
          "expected": -0.21531249582767487,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 12,
            "y": 12
          },
          "expected": -0.9603320360183716,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 12,
            "y": 12
          },
          "expected": -0.2187749743461609,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 12,
            "y": 12
          },
          "expected": -0.9757753014564514,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 5,
            "y": 5
          },
          "expected": -0.2978564500808716,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 5,
            "y": 5
          },
          "expected": -0.9202880859375,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 5,
            "y": 5
          },
          "expected": -0.30792900919914246,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 5,
            "y": 5
          },
          "expected": -0.9514092803001404,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 22,
            "y": 61
          },
          "expected": 1.780588984489441,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 22,
            "y": 61
          },
          "expected": -0.015869662165641785,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 17,
            "y": 56
          },
          "expected": 3.146423816680908,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 17,
            "y": 56
          },
          "expected": -0.09727403521537781,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 28,
            "y": 64
          },
          "expected": 3.1481480598449707,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 28,
            "y": 64
          },
          "expected": -0.1057797521352768,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 12,
            "y": 54
          },
          "expected": 0.8953660726547241,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 12,
            "y": 54
          },
          "expected": 0.01442580483853817,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        }
      ]
    },
    {
      "id": "weno3_eno1_step20_stage1",
      "description": "fire_upwinding = 8, the hybrid WENO3/ENO1 scheme -- the fifth of the eleven upwinding options covered, after 9 (fire_behavior's namelist-default hard-edged WENO5/ENO1 hybrid), 4 (classical Godunov), 7 (pure WENO5) and 10 (WENO5/ENO1 with a cosine blending zone). physics/level_set_mod.F90 case (8) is case (9) with Select_weno5 replaced by Select_weno3: same band test |psi| < weno_band_cells*dx, same ENO1 wall band, same fourth-order wind-relative upwind selector, a two-stencil third-order Jiang-Shu reconstruction instead of a three-stencil fifth-order one. It needed a NEW EarthSciDiscretizations rule family (weno3_eno1_norm_D2_extrapolate_bc and the two per-axis rules, over the new stencils weno3_js_face_recon, weno3_js_upwind_D1 and weno3_eno1_D1x/D1y_interior): there was no WENO3 at all on cartesian_uniform_2d, and the only WENO3 anywhere in that library is the 1-D weno3_recon, which is WENO-Z (weights gamma_k(1 + (tau3/(eps+beta_k))^2), tau3 = |beta0 - beta1|) rather than the classical gamma_k/(beta_k + eps)^2 this code computes, so it could not be reused. IT IS DISCRIMINATING, and maximally so: applied to this run's own psi field, options 8 and 9 give a different tendency in 175 of the 6400 cells -- which is EVERY cell the WENO branch touches on this state (175 cells are both inside the band and outside the 10-cell ENO1 wall strip) -- and agree to exactly zero difference in all 6225 others. The largest difference is 0.550 m/s in the tendency at (22,62) and 0.377 in |grad psi|. The ten asserted in-band cells are the ten largest of those differences (0.067 to 0.550 m/s); (40,40) and (12,12) are ENO1 cells outside the band and (5,5) is inside the ENO1 wall strip, all three identical under both schemes, which is the check that the third-order reconstruction does not leak outside the band. psi_x, psi_y (the dumped diff2x, diff2y) and nvx, nvy are asserted at all thirteen cells; the ones added at the ten cells beyond the original three carry abs 2e-6, because the small component at (22,63), psi_x = 0.0119 beside psi_y = 1.22, differs from the real32 dump by 6e-7 (5e-7 of |grad psi|), WENO-amplified real32 rounding. Swapping weno5_eno1_norm_D2_extrapolate_bc and its two per-axis rules back in, with this run's own psi still bound, fails 55 of these 71 assertions and leaves exactly the 16 control-cell ones green. Reference: data/eqwefic/dumps/fire/run_weno3/esm_dump_ls_tend_58.json -- NCAR fire_behavior test7 (80x80 fire cells of 25 m, dt = 0.5 s, num_tiles = 1) rerun with fire_upwinding = 8, otherwise the namelist of the option-10 rerun, default real32 build, fork ctessum-claude/fire_behavior c9dda02 with -DESM_DUMP=ON; ls_tend dump call 58 = Runge-Kutta stage 1 of step 20 (t = 10 s). rel 2e-5.",
      "expression_template_imports": [
        {
          "ref": "${ESD_ROOT}/grids/cartesian_uniform_2d/rules/weno3_eno1_norm_D2_extrapolate_bc.esm",
          "bindings": {
            "NX": 80,
            "NY": 80
          }
        },
        {
          "ref": "${ESD_ROOT}/grids/cartesian_uniform_2d/rules/weno3_eno1_D1x_extrapolate_bc.esm",
          "bindings": {
            "NX": 80,
            "NY": 80
          }
        },
        {
          "ref": "${ESD_ROOT}/grids/cartesian_uniform_2d/rules/weno3_eno1_D1y_extrapolate_bc.esm",
          "bindings": {
            "NX": 80,
            "NY": 80
          }
        },
        {
          "ref": "${ESD_ROOT}/grids/cartesian_uniform_2d/rules/central_D2x_extrapolate_bc.esm",
          "bindings": {
            "NX": 80,
            "NY": 80
          }
        },
        {
          "ref": "${ESD_ROOT}/grids/cartesian_uniform_2d/rules/central_D2y_extrapolate_bc.esm",
          "bindings": {
            "NX": 80,
            "NY": 80
          }
        },
        {
          "ref": "./tests/weno3_eno1_step20_stage1_inputs.esm"
        }
      ],
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "parameter_overrides": {
        "Lx": 2000.0,
        "Ly": 2000.0,
        "fire_viscosity": 0.4,
        "bdy_eno1_cells": 10,
        "weno_band_cells": 4
      },
      "assertions": [
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 22,
            "y": 62
          },
          "expected": 0.10618841648101807,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 25,
            "y": 65
          },
          "expected": -1.843404769897461,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 24,
            "y": 64
          },
          "expected": -1.7087421417236328,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 22,
            "y": 63
          },
          "expected": -1.5113365650177002,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 20,
            "y": 62
          },
          "expected": -0.6013855338096619,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 27,
            "y": 65
          },
          "expected": 0.03338557481765747,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 25,
            "y": 61
          },
          "expected": -1.687272310256958,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 23,
            "y": 62
          },
          "expected": 0.17289280891418457,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 19,
            "y": 63
          },
          "expected": -0.7044859528541565,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 21,
            "y": 62
          },
          "expected": -0.8534263372421265,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 40
          },
          "expected": -0.026860108599066734,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 12,
            "y": 12
          },
          "expected": -0.02887246385216713,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend",
          "time": 0.0,
          "coords": {
            "x": 5,
            "y": 5
          },
          "expected": -0.029080096632242203,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 22,
            "y": 62
          },
          "expected": 0.40974128246307373,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 25,
            "y": 65
          },
          "expected": 1.3102424144744873,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 24,
            "y": 64
          },
          "expected": 1.2807655334472656,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "grad_mag",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 40
          },
          "expected": 0.9608290195465088,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 22,
            "y": 62
          },
          "expected": -0.598097026348114,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "tend_adv",
          "time": 0.0,
          "coords": {
            "x": 25,
            "y": 65
          },
          "expected": -1.9110417366027832,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-09
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 22,
            "y": 62
          },
          "expected": 0.020528869703412056,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 25,
            "y": 65
          },
          "expected": 0.6926230788230896,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 24,
            "y": 64
          },
          "expected": 0.605000913143158,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 22,
            "y": 62
          },
          "expected": 0.4092266857624054,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 25,
            "y": 65
          },
          "expected": 1.1122088432312012,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 24,
            "y": 64
          },
          "expected": 1.1288641691207886,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 22,
            "y": 62
          },
          "expected": 0.05010201036930084,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 25,
            "y": 65
          },
          "expected": 0.528622031211853,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 24,
            "y": 64
          },
          "expected": 0.47237443923950195,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 22,
            "y": 62
          },
          "expected": 0.9987437129020691,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 25,
            "y": 65
          },
          "expected": 0.8488572239875793,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 24,
            "y": 64
          },
          "expected": 0.8813979625701904,
          "tolerance": {
            "rel": 2e-05,
            "abs": 1e-07
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 5,
            "y": 5
          },
          "expected": -0.2978564500808716,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 5,
            "y": 5
          },
          "expected": -0.9202880859375,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 5,
            "y": 5
          },
          "expected": -0.30792900919914246,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 5,
            "y": 5
          },
          "expected": -0.9514092803001404,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 12,
            "y": 12
          },
          "expected": -0.21531249582767487,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 12,
            "y": 12
          },
          "expected": -0.9603320360183716,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 12,
            "y": 12
          },
          "expected": -0.2187749743461609,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 12,
            "y": 12
          },
          "expected": -0.9757753014564514,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 19,
            "y": 63
          },
          "expected": -0.8382159471511841,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 19,
            "y": 63
          },
          "expected": 0.73048996925354,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 19,
            "y": 63
          },
          "expected": -0.7538896203041077,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 19,
            "y": 63
          },
          "expected": 0.6570010781288147,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 20,
            "y": 62
          },
          "expected": -0.9008617997169495,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 20,
            "y": 62
          },
          "expected": 0.7547332644462585,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 20,
            "y": 62
          },
          "expected": -0.7665383219718933,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 20,
            "y": 62
          },
          "expected": 0.642198383808136,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 21,
            "y": 62
          },
          "expected": 0.020527038723230362,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 21,
            "y": 62
          },
          "expected": 0.8969372510910034,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 21,
            "y": 62
          },
          "expected": 0.02287971042096615,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 21,
            "y": 62
          },
          "expected": 0.9997381567955017,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 22,
            "y": 63
          },
          "expected": 0.011946410872042179,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 22,
            "y": 63
          },
          "expected": 1.2237520217895508,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 22,
            "y": 63
          },
          "expected": 0.00976165197789669,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 22,
            "y": 63
          },
          "expected": 0.9999523758888245,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 23,
            "y": 62
          },
          "expected": 1.009889841079712,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 23,
            "y": 62
          },
          "expected": 0.5457788109779358,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 23,
            "y": 62
          },
          "expected": 0.8797456622123718,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 23,
            "y": 62
          },
          "expected": 0.475444495677948,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 25,
            "y": 61
          },
          "expected": 1.0973526239395142,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 25,
            "y": 61
          },
          "expected": 0.2580801248550415,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 25,
            "y": 61
          },
          "expected": 0.9734408855438232,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 25,
            "y": 61
          },
          "expected": 0.228938028216362,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 27,
            "y": 65
          },
          "expected": 0.8779510259628296,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 27,
            "y": 65
          },
          "expected": 0.3421687185764313,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 27,
            "y": 65
          },
          "expected": 0.9317378997802734,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 27,
            "y": 65
          },
          "expected": 0.3631313741207123,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "psi_x",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 40
          },
          "expected": 0.6217920184135437,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "psi_y",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 40
          },
          "expected": -0.7325073480606079,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "nvx",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 40
          },
          "expected": 0.64714115858078,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        },
        {
          "variable": "nvy",
          "time": 0.0,
          "coords": {
            "x": 40,
            "y": 40
          },
          "expected": -0.7623701095581055,
          "tolerance": {
            "rel": 2e-05,
            "abs": 2e-06
          }
        }
      ]
    }
  ],
  "subsystems": {
    "par": {
      "ref": "./fire_behavior_parameters.esm"
    }
  }
}
```

</details>
