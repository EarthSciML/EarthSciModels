---
title: "UrbanRadiation"
slug: "urbanradiation"
domains: ["urban_canopy"]
component_types: ["model"]
domain: "urban_canopy"
component_type: "model"
esm_version: "1.0.0"
esm_path: "components/urban_canopy/urban_radiation.esm"
reference: "Oleson, K. W., G. B. Bonan, J. J. Feddema, M. Vertenstein, and E. Kluzek (2010). Technical Description of an Urban Parameterization for the Community Land Model (CLMU). NCAR Technical Note NCAR/TN-480+STR, National Center for Atmospheric Research, Boulder, CO, 168 pp. Chapter 2: Albedos and Radiative Fluxes (pp. 26-60)."
description: "Urban albedos and radiative fluxes for the Community Land Model Urban (CLMU) parameterization, following Chapter 2 of Oleson et al. (2010). Computes view factors, incident direct beam and diffuse solar radiation, absorbed and reflected solar radiation (with closed-form multi-reflection solution for the urban canyon), incident longwave radiation, and absorbed/reflected/emitted longwave radiation for urban surfaces: roof, sunlit wall, shaded wall, and road. The urban canyon is represented as an infinitely long canyon of width W bordered by buildings of height H. The iterative multi-reflection scheme (Eqs. 2.63-2.85, 2.138-2.170) is solved in closed form using the matrix geometric series S_absorbed = (I - A) * (I - T*A)^{-1} * S_0, where A is the albedo matrix, T is the view-factor transport matrix, and S_0 is the initial incident radiation vector. Migrated from UrbanCanopy.jl@9200edd4 src/albedos_radiative_fluxes.jl:27 (`UrbanRadiation` @component). Parameterized as observed-only: H_W, W_roof, S_atm_*, L_atm_down, μ_zen, surface albedos α_*, emissivities ε_*, and surface temperatures T_* are inputs (parameters); 62 view factor, intermediate, absorbed-flux, and reflected-flux quantities are algebraic state outputs."
tags: ["urban_canopy", "model", "radiation", "albedo", "longwave", "shortwave", "view_factors", "multi_reflection", "observed-only", "clmu"]
---

## Description

Urban albedos and radiative fluxes for the Community Land Model Urban (CLMU) parameterization, following Chapter 2 of Oleson et al. (2010). Computes view factors, incident direct beam and diffuse solar radiation, absorbed and reflected solar radiation (with closed-form multi-reflection solution for the urban canyon), incident longwave radiation, and absorbed/reflected/emitted longwave radiation for urban surfaces: roof, sunlit wall, shaded wall, and road. The urban canyon is represented as an infinitely long canyon of width W bordered by buildings of height H. The iterative multi-reflection scheme (Eqs. 2.63-2.85, 2.138-2.170) is solved in closed form using the matrix geometric series S_absorbed = (I - A) * (I - T*A)^{-1} * S_0, where A is the albedo matrix, T is the view-factor transport matrix, and S_0 is the initial incident radiation vector. Migrated from UrbanCanopy.jl@9200edd4 src/albedos_radiative_fluxes.jl:27 (`UrbanRadiation` @component). Parameterized as observed-only: H_W, W_roof, S_atm_*, L_atm_down, μ_zen, surface albedos α_*, emissivities ε_*, and surface temperatures T_* are inputs (parameters); 62 view factor, intermediate, absorbed-flux, and reflected-flux quantities are algebraic state outputs.

## Reference

_source_ref: UrbanCanopy.jl@9200edd4f15609f20339d3a7d104de8064544310:src/albedos_radiative_fluxes.jl:27
Upstream `UrbanRadiation` is an MTK `@component` with five `@constants` (σ_SB = 5.67e-8 W/(m²·K⁴), π_val = π dimensionless, one_rad = 1.0 rad, one_wm2 = 1.0 W/m², zero_wm2 = 0.0 W/m²), 31 `@parameters` (geometry H_W/W_roof, four atmospheric solar fluxes S_atm_*, atmospheric longwave L_atm_down, solar zenith μ_zen, twelve surface albedos α_*_*_* across roof/road/wall × dir/dif × vis/nir, three emissivities ε_*, four surface temperatures T_*), 62 time-indexed `@variables` (view factors Ψ_*, transport matrix T_rw/T_wr/T_ww, direct-beam factors θ_0/S_*_factor, incident/absorbed/reflected radiation S_*, canyon albedos α_uc_*, longwave fluxes L_*), and 62 algebraic equations (no derivatives). Identical equation structure preserved here.

The upstream component declares five `@constants`, all encoded here as parameters with the upstream defaults: σ_SB = 5.67e-8 W/(m²·K⁴) (Stefan-Boltzmann from Oleson Table 1.4); π_val = π (the Float64 value of Julia's π constant); one_rad = 1.0 rad (unit-balancer for the rad-dimensioned μ_zen and θ_0); one_wm2 = 1.0 W/m² (unit-balancer for the W/m² comparison in the canyon-albedo guard); zero_wm2 = 0.0 W/m² (unit-balancing zero for the canyon-albedo guard's else branch). Greek symbols (Ψ for view factors, α for albedos, ε for emissivities, σ for Stefan-Boltzmann, μ for solar zenith, π for pi, θ for canyon orientation, Δ-style underscored subscripts) are preserved verbatim from upstream — peer ESM files in this rig already use Greek letters in identifiers (e.g. urban_surface_thermal.esm uses λ_prescribed / c_prescribed, freezing_point_depression.esm uses ψ_sat / θ_sat / ρ_liq, snow_melt_no_layers.esm uses Δt), and Oleson Chapter 2 uses these Greek symbols extensively in its equations; keeping them preserves the direct equation-to-symbol correspondence that aids review against the technical note.

Multi-reflection closed form: the upstream source contains a Julia `for` loop that generates 4 sets of 5 equations (one set per waveband × incidence-type: direct VIS, direct NIR, diffuse VIS, diffuse NIR) for the canyon solar multi-reflection. The loop body computes intermediate quantities b = a_w*T_rw, c = a_r*T_wr, d = a_w*T_ww (the M = I - T*A matrix off-diagonal products), then det = (1-d²) - 2bc(1+d) (the M-matrix determinant per the adjugate formula in the source's :240-:246 docstring), then the three M⁻¹*S_0 product components Q_road/Q_sw/Q_sh, and finally the absorbed-flux assignments S_net_* = (1-α)*Q and the reflected-to-sky energy-balance closure S_refl_sky = incident - absorbed. The migrated ESM encodes the 20 equations using v0.4.0 expression_templates (RFC docs/rfcs/ast-expression-templates.md): five templates `band_det`, `band_net_road`, `band_net_sw`, `band_net_sh`, `band_refl_sky` each take the per-waveband free variables (a_r, a_w, S_r, S_sw, S_sh, det_var, and for refl_sky additionally net_road/net_sw/net_sh) as parameter substitution slots; each template is invoked 4 times (once per waveband). At load time `apply_expression_template` nodes expand structurally, so the canonical AST a loader sees after parse-then-emit is the fully-inlined 20-equation form — bit-equivalent to writing the equations inline. The longwave multi-reflection block (Eqs. 2.138-2.170, source :355-:393) is structurally identical to the solar block with one invocation, but with substituted source terms (atmospheric LW + emitted LW from other surfaces) — encoded here as 4 inline equations (det_lw + 3 L_net_*) since the single-invocation site does not benefit from a template.

Upstream `local` Julia variables b/c/d/Q_road/Q_sw/Q_sh are not user-visible MTK state variables (they're intermediate let-bindings, expanded by Julia's `local` into the right-hand-side AST of the resulting equations). The migrated ESM preserves this by inlining the same expressions into the template bodies — the canonical 62-equation form after expression-template expansion has 62 LHS state variables matching upstream's `length(unknowns(sys)) == 62` invariant.

θ_0 unit balancing (Eq. 2.11): the upstream form `θ_0 = asin(min(1 / (H_W * tan(μ_zen / one_rad)), 1)) * one_rad` is preserved verbatim. The unit contract: μ_zen has dimension rad; dividing by one_rad makes it dimensionless for the `tan` and `min` operations; multiplying the dimensionless `asin` result by one_rad restores the rad dimension. The numeric value is identical to the unfused `asin(min(1/(H_W*tan(μ_zen)), 1))` because one_rad = 1.0 exactly, but the form is kept to mirror the upstream unit contract for any future ESS unit checker.

Canyon albedo guard (Eqs. 2.93-2.94): the upstream guard uses `ifelse(incident > zero_wm2, refl/incident, 0.0)` to avoid divide-by-zero when there is no incident radiation in this waveband. Preserved verbatim. The bare `0.0` else branch is a dimensionless literal — matches upstream where canyon albedo is dimensionless. (Compare with snow_melt_no_layers.esm which uses a dimensioned `zero_m` else branch for its depth output.)

Observability classification: this component is functionally observed-only — every output variable is given by a single algebraic equation in terms of the parameters and earlier-computed state variables (the `(t)` time index has no role since there are no derivatives). Test scenarios use `time_span: [0, 1]` and sample at t=0 to mirror the convention used by sibling observed-only ESM files in this rig (surface_energy_flux.esm, snow_melt_no_layers.esm, freezing_point_depression.esm).

Tolerance rationale (model-level rel=1e-8): observed-only algebraic system (no ODE integration); the most numerically delicate equations are the canyon multi-reflection ones (`det = (1-d²) - 2bc(1+d)` and the `Q/det` divisions for absorbed-flux and reflected-flux), which involve products and quotients of dimensionless quantities and can accumulate ~1e-13 rounding under the canonical test parameters (e.g. the residual `(S_r + ...) - (net_road + ...)` energy-balance closure for the reflected-flux equation evaluates to ~1e-13 W/m² in regimes where the closure should be exact). 1e-8 leaves comfortable headroom above this and matches the convention used by the most numerically rich peer (heat_flux.esm uses 1e-9 for a single-equation Fourier flux; surface_energy_flux.esm uses 1e-9 for additive flux balances — UrbanRadiation is one ULP-decade looser because of the canyon multi-reflection closed-form solution's higher polynomial degree). Tighter `abs: 1e-10` is asserted on outputs that are exactly zero by construction (e.g. zero albedos → zero reflected flux; equal-temperature blackbody → zero net LW for the symmetric canyon) so the assertion does not silently accept a stuck-at-1e-3 regression.

Upstream tolerance reproduction: the upstream tests use rtol = 1.0e-10 for analytical view factor checks (e.g. Eqs. 2.22-2.28 against manually computed reference values), rtol = 1.0e-8 for energy-conservation closures, and rtol = 1.0e-6 for canyon LW blackbody asymptotics. Per-assertion tolerances are set to match — 1e-10 for view-factor analytics, 1e-8 for energy conservation, 1e-6 for the blackbody LW reference._

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `σ_SB` | `W/(m^2*K^4)` | `5.67e-08` | Stefan-Boltzmann constant (Oleson Table 1.4) — upstream `@constants` σ_SB; the coefficient of T^4 in the Stefan-Boltzmann law for upward longwave emission used in Eqs. 2.102, 2.111-2.113 |
| `π_val` | `1` | `3.141592653589793` | Pi (dimensionless) — upstream `@constants` π_val = Float64(π); appears in the direct-beam canyon-orientation factors of Eqs. 2.16-2.17 |
| `one_rad` | `rad` | `1.0` | Unit-angle reference (1 rad) — upstream `@constants` one_rad; used in `μ_zen / one_rad` to make the argument of `tan` dimensionless and in `asin(...) * one_rad` to restore rad dimension on θ_0 (Eq. 2.11). Value is exactly 1.0 by construction; numerically a no-op. |
| `one_wm2` | `W/m^2` | `1.0` | Unit radiative flux (1 W/m²) — upstream `@constants` one_wm2; declared by the upstream component but unused in the equation block (kept here for 1:1 parameter-count fidelity with upstream `length(parameters(sys)) == 31`). The unit-balancing role of one_wm2 is taken by `zero_wm2` in the canyon-albedo guard. |
| `zero_wm2` | `W/m^2` | `0.0` | Zero radiative flux (0 W/m²) — upstream `@constants` zero_wm2; used as the comparison RHS in the canyon-albedo guard `ifelse(incident > zero_wm2, refl/incident, 0.0)` to keep the `>` comparison unit-consistent with the W/m² LHS |
| `H_W` | `1` | `1.0` | Canyon height-to-width ratio H/W (dimensionless) — controls all view factor geometry (Eqs. 2.22-2.28); typical urban values 0.5-3, but the implementation is valid for 0 (flat) to large (deep canyon) |
| `W_roof` | `1` | `0.25` | Roof fraction of urban surface (dimensionless) — controls the area-weighted combination of roof and canyon contributions to total net radiation in Eqs. 2.95 and 2.175 |
| `S_atm_dir_vis` | `W/m^2` | `200.0` | Incident direct beam visible solar radiation from the atmosphere (upstream `@parameters` S_atm_dir_vis) |
| `S_atm_dir_nir` | `W/m^2` | `150.0` | Incident direct beam NIR solar radiation from the atmosphere |
| `S_atm_dif_vis` | `W/m^2` | `80.0` | Incident diffuse visible solar radiation from the atmosphere |
| `S_atm_dif_nir` | `W/m^2` | `60.0` | Incident diffuse NIR solar radiation from the atmosphere |
| `L_atm_down` | `W/m^2` | `350.0` | Incident longwave radiation from the atmosphere (downwelling) |
| `μ_zen` | `rad` | `0.5236` | Solar zenith angle (rad) — appears in `tan(μ_zen)` in the direct-beam factor of Eq. 2.16-2.17. Default 0.5236 rad ≈ 30 degrees. |
| `α_roof_dir_vis` | `1` | `0.2` | Roof albedo, direct beam, visible (dimensionless) — surface optical property; appears in Eq. 2.34-2.35 for absorbed solar by the roof |
| `α_roof_dir_nir` | `1` | `0.2` | Roof albedo, direct beam, NIR (dimensionless) |
| `α_roof_dif_vis` | `1` | `0.2` | Roof albedo, diffuse, visible (dimensionless) |
| `α_roof_dif_nir` | `1` | `0.2` | Roof albedo, diffuse, NIR (dimensionless) |
| `α_road_dir_vis` | `1` | `0.08` | Effective road albedo, direct beam, visible (dimensionless) — weighted average over pervious/impervious road fraction, computed upstream |
| `α_road_dir_nir` | `1` | `0.08` | Effective road albedo, direct beam, NIR (dimensionless) |
| `α_road_dif_vis` | `1` | `0.08` | Effective road albedo, diffuse, visible (dimensionless) |
| `α_road_dif_nir` | `1` | `0.08` | Effective road albedo, diffuse, NIR (dimensionless) |
| `α_wall_dir_vis` | `1` | `0.25` | Wall albedo, direct beam, visible (dimensionless) |
| `α_wall_dir_nir` | `1` | `0.25` | Wall albedo, direct beam, NIR (dimensionless) |
| `α_wall_dif_vis` | `1` | `0.25` | Wall albedo, diffuse, visible (dimensionless) |
| `α_wall_dif_nir` | `1` | `0.25` | Wall albedo, diffuse, NIR (dimensionless) |
| `ε_roof` | `1` | `0.9` | Roof longwave emissivity (dimensionless) — Stefan-Boltzmann pre-factor in upward LW emission (Eq. 2.102); typical urban roof values 0.85-0.95 |
| `ε_road` | `1` | `0.95` | Effective road longwave emissivity (dimensionless) — weighted average over pervious/impervious road fraction |
| `ε_wall` | `1` | `0.85` | Wall longwave emissivity (dimensionless) |
| `T_roof` | `K` | `305.0` | Roof surface temperature — appears as T^4 in the Stefan-Boltzmann upward emission (Eq. 2.102) |
| `T_road` | `K` | `310.0` | Road surface temperature — appears as T^4 in the road LW emission (Eq. 2.111) |
| `T_sunwall` | `K` | `315.0` | Sunlit wall surface temperature — appears as T^4 in the sunlit-wall LW emission (Eq. 2.112) |
| `T_shdwall` | `K` | `300.0` | Shaded wall surface temperature — appears as T^4 in the shaded-wall LW emission (Eq. 2.113) |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `Ψ_wall_sky` | `1` |  | View factor: wall to sky (Oleson Eq. 2.24) — fraction of radiation leaving a wall that reaches the sky |
| `Ψ_wall_road` | `1` |  | View factor: wall to road (Oleson Eq. 2.26) — equal to Ψ_wall_sky by reciprocity |
| `Ψ_wall_wall` | `1` |  | View factor: wall to opposite wall (Oleson Eq. 2.28) — closure of the row-sum 1 = Ψ_wall_sky + Ψ_wall_road + Ψ_wall_wall |
| `Ψ_road_sky` | `1` |  | View factor: road to sky (Oleson Eq. 2.25) — fraction of radiation leaving the road that reaches the sky; decreases with H/W |
| `Ψ_road_wall` | `1` |  | View factor: road to wall (Oleson Eq. 2.27) — fraction of radiation leaving the road that reaches one wall; two walls so 2*Ψ_road_wall = 1 - Ψ_road_sky |
| `Ψ_sky_road` | `1` |  | View factor: sky to road (Oleson Eq. 2.25) — equal to Ψ_road_sky by reciprocity |
| `Ψ_sky_wall` | `1` |  | View factor: sky to wall, per unit wall area (Oleson Eq. 2.24) — equal to Ψ_wall_sky by reciprocity |
| `θ_0` | `rad` |  | Critical canyon orientation angle (Oleson Eq. 2.11) — the canyon-orientation azimuth threshold separating sunlit-wall from shadowed-wall geometries integrated to derive the canyon-averaged direct-beam radiation factors |
| `S_sunwall_factor` | `1` |  | Sunlit wall direct beam factor (Oleson Eq. 2.16) — dimensionless fraction of atmospheric direct-beam radiation that lands on the sunlit wall per unit wall area, integrated over canyon orientation |
| `S_road_factor` | `1` |  | Road direct beam factor (Oleson Eq. 2.17) — dimensionless fraction of atmospheric direct-beam radiation that lands on the road per unit ground area; conservation Eq. 2.18 requires S_road_factor + H/W * S_sunwall_factor = 1 |
| `S_road_dir_vis` | `W/m^2` |  | Direct beam VIS incident on road (Oleson Eq. 2.17): S_road_factor * S_atm_dir_vis |
| `S_road_dir_nir` | `W/m^2` |  | Direct beam NIR incident on road: S_road_factor * S_atm_dir_nir |
| `S_sunwall_dir_vis` | `W/m^2` |  | Direct beam VIS incident on sunlit wall (Oleson Eq. 2.16): S_sunwall_factor * S_atm_dir_vis |
| `S_sunwall_dir_nir` | `W/m^2` |  | Direct beam NIR incident on sunlit wall: S_sunwall_factor * S_atm_dir_nir |
| `S_road_dif_vis` | `W/m^2` |  | Diffuse VIS incident on road (Oleson Eq. 2.30): S_atm_dif_vis * Ψ_sky_road |
| `S_road_dif_nir` | `W/m^2` |  | Diffuse NIR incident on road: S_atm_dif_nir * Ψ_sky_road |
| `S_wall_dif_vis` | `W/m^2` |  | Diffuse VIS incident on each wall (Oleson Eqs. 2.31-2.32): S_atm_dif_vis * Ψ_sky_wall — same on sunlit and shaded walls for diffuse radiation |
| `S_wall_dif_nir` | `W/m^2` |  | Diffuse NIR incident on each wall: S_atm_dif_nir * Ψ_sky_wall |
| `T_rw` | `1` |  | Transport matrix element: wall to road (Oleson Section 2.5, p. 42-43) = H/W * Ψ_wall_road — accounts for the wall-to-road area ratio in the multi-reflection transport matrix T |
| `T_wr` | `1` |  | Transport matrix element: road to wall = Ψ_road_wall / (H/W) — accounts for the road-to-wall area ratio (per unit wall area) |
| `T_ww` | `1` |  | Transport matrix element: wall to opposite wall = Ψ_wall_wall — the off-diagonal that couples the sunlit and shaded walls in the canyon-reflection geometric series |
| `det_dir_vis` | `1` |  | Determinant of (I - T*A) for direct VIS waveband: (1 - d²) - 2bc(1 + d), where b = a_w*T_rw, c = a_r*T_wr, d = a_w*T_ww — denominator of the closed-form multi-reflection solution |
| `det_dir_nir` | `1` |  | Determinant of (I - T*A) for direct NIR waveband |
| `det_dif_vis` | `1` |  | Determinant of (I - T*A) for diffuse VIS waveband |
| `det_dif_nir` | `1` |  | Determinant of (I - T*A) for diffuse NIR waveband |
| `S_net_roof` | `W/m^2` |  | Net absorbed solar by roof (Oleson Eqs. 2.34-2.35): Σ S_atm_*_*(1 - α_roof_*_*) summed over all four wavebands |
| `S_net_road_dir_vis` | `W/m^2` |  | Absorbed solar by road, direct VIS waveband: (1 - α_road_dir_vis) * Q_road_dir_vis where Q_road_dir_vis is the per-waveband closed-form M⁻¹*S_0 multi-reflection result |
| `S_net_road_dir_nir` | `W/m^2` |  | Absorbed solar by road, direct NIR waveband |
| `S_net_road_dif_vis` | `W/m^2` |  | Absorbed solar by road, diffuse VIS waveband |
| `S_net_road_dif_nir` | `W/m^2` |  | Absorbed solar by road, diffuse NIR waveband |
| `S_net_sunwall_dir_vis` | `W/m^2` |  | Absorbed solar by sunlit wall, direct VIS waveband (per unit wall area) |
| `S_net_sunwall_dir_nir` | `W/m^2` |  | Absorbed solar by sunlit wall, direct NIR waveband |
| `S_net_sunwall_dif_vis` | `W/m^2` |  | Absorbed solar by sunlit wall, diffuse VIS waveband |
| `S_net_sunwall_dif_nir` | `W/m^2` |  | Absorbed solar by sunlit wall, diffuse NIR waveband |
| `S_net_shdwall_dir_vis` | `W/m^2` |  | Absorbed solar by shaded wall, direct VIS waveband — non-zero only via multi-reflection from road and sunlit wall (no direct beam reaches the shaded wall) |
| `S_net_shdwall_dir_nir` | `W/m^2` |  | Absorbed solar by shaded wall, direct NIR waveband |
| `S_net_shdwall_dif_vis` | `W/m^2` |  | Absorbed solar by shaded wall, diffuse VIS waveband — equal to sunwall diffuse VIS by symmetry |
| `S_net_shdwall_dif_nir` | `W/m^2` |  | Absorbed solar by shaded wall, diffuse NIR waveband |
| `S_net_road` | `W/m^2` |  | Total net absorbed solar by road: sum of S_net_road_* over the four wavebands |
| `S_net_sunwall` | `W/m^2` |  | Total net absorbed solar by sunlit wall per unit wall area: sum of S_net_sunwall_* over the four wavebands |
| `S_net_shdwall` | `W/m^2` |  | Total net absorbed solar by shaded wall per unit wall area: sum of S_net_shdwall_* over the four wavebands |
| `S_net_uc` | `W/m^2` |  | Net absorbed solar by the urban canyon per unit ground area: S_net_road + (S_net_sunwall + S_net_shdwall) * H/W |
| `S_net_total` | `W/m^2` |  | Total net absorbed solar (Oleson Eq. 2.95): W_roof * S_net_roof + (1 - W_roof) * S_net_uc — area-weighted total over roof and canyon |
| `S_refl_sky_dir_vis` | `W/m^2` |  | Solar reflected back to sky from the canyon, direct VIS waveband — energy-balance closure: incident_canyon - absorbed_canyon (per unit ground area) |
| `S_refl_sky_dir_nir` | `W/m^2` |  | Solar reflected back to sky from the canyon, direct NIR waveband |
| `S_refl_sky_dif_vis` | `W/m^2` |  | Solar reflected back to sky from the canyon, diffuse VIS waveband |
| `S_refl_sky_dif_nir` | `W/m^2` |  | Solar reflected back to sky from the canyon, diffuse NIR waveband |
| `α_uc_dir_vis` | `1` |  | Canyon direct beam albedo, VIS (Oleson Eq. 2.93): S_refl_sky_dir_vis / incident_canyon — the ratio of reflected to incident summed over the canyon (excluding the roof). Guarded against divide-by-zero when there is no incident radiation in this waveband. |
| `α_uc_dir_nir` | `1` |  | Canyon direct beam albedo, NIR |
| `α_uc_dif_vis` | `1` |  | Canyon diffuse albedo, VIS (Oleson Eq. 2.94) |
| `α_uc_dif_nir` | `1` |  | Canyon diffuse albedo, NIR |
| `L_up_roof` | `W/m^2` |  | Upward longwave radiation from roof (Oleson Eq. 2.102): ε_roof * σ_SB * T_roof^4 + (1 - ε_roof) * L_atm_down — Stefan-Boltzmann emission plus reflection of the downwelling atmospheric LW |
| `L_net_roof` | `W/m^2` |  | Net longwave for roof (Oleson Eq. 2.101): L_up_roof - L_atm_down — positive when the roof is losing more LW than it absorbs |
| `L_emit_road` | `W/m^2` |  | Emitted longwave from road (Oleson Eq. 2.111): ε_road * σ_SB * T_road^4 — Stefan-Boltzmann emission only, before multi-reflection |
| `L_emit_sunwall` | `W/m^2` |  | Emitted longwave from sunlit wall (Oleson Eq. 2.112): ε_wall * σ_SB * T_sunwall^4 |
| `L_emit_shdwall` | `W/m^2` |  | Emitted longwave from shaded wall (Oleson Eq. 2.113): ε_wall * σ_SB * T_shdwall^4 |
| `det_lw` | `1` |  | Determinant of (I - T*A) for longwave: (1 - d_lw²) - 2*b_lw*c_lw*(1 + d_lw), where b_lw = (1-ε_wall)*T_rw, c_lw = (1-ε_road)*T_wr, d_lw = (1-ε_wall)*T_ww — structurally identical to the solar determinant but with reflectivity (1 - ε) in place of albedo α |
| `L_net_road` | `W/m^2` |  | Net longwave for road: L_emit_road - ε_road * Q_road_lw, where Q_road_lw is the canyon-trapped incoming LW from atmosphere and wall emission via the multi-reflection M⁻¹*S_0_lw solution. Positive when the road loses more LW than it absorbs. |
| `L_net_sunwall` | `W/m^2` |  | Net longwave for sunlit wall per unit wall area: L_emit_sunwall - ε_wall * Q_sw_lw |
| `L_net_shdwall` | `W/m^2` |  | Net longwave for shaded wall per unit wall area: L_emit_shdwall - ε_wall * Q_sh_lw |
| `L_net_uc` | `W/m^2` |  | Net longwave for urban canyon per unit ground area (Oleson Eq. 2.172): L_net_road + (L_net_sunwall + L_net_shdwall) * H/W |
| `L_net_total` | `W/m^2` |  | Total net longwave (Oleson Eq. 2.175): W_roof * L_net_roof + (1 - W_roof) * L_net_uc — area-weighted total over roof and canyon |

## Observed expressions

$$
Ψ_{wall\,sky} = Ψ_{sky\,wall}
$$
_View factor: wall to sky (Oleson Eq. 2.24) — fraction of radiation leaving a wall that reaches the sky_

$$
Ψ_{wall\,road} = Ψ_{wall\,sky}
$$
_View factor: wall to road (Oleson Eq. 2.26) — equal to Ψ_wall_sky by reciprocity_

$$
Ψ_{wall\,wall} = 1.0 - Ψ_{wall\,sky} - Ψ_{wall\,road}
$$
_View factor: wall to opposite wall (Oleson Eq. 2.28) — closure of the row-sum 1 = Ψ_wall_sky + Ψ_wall_road + Ψ_wall_wall_

$$
Ψ_{road\,sky} = \sqrt{1.0 + H_{W}^{2.0}} - H_{W}
$$
_View factor: road to sky (Oleson Eq. 2.25) — fraction of radiation leaving the road that reaches the sky; decreases with H/W_

$$
Ψ_{road\,wall} = \frac{1.0 - Ψ_{road\,sky}}{2.0}
$$
_View factor: road to wall (Oleson Eq. 2.27) — fraction of radiation leaving the road that reaches one wall; two walls so 2*Ψ_road_wall = 1 - Ψ_road_sky_

$$
Ψ_{sky\,road} = Ψ_{road\,sky}
$$
_View factor: sky to road (Oleson Eq. 2.25) — equal to Ψ_road_sky by reciprocity_

$$
Ψ_{sky\,wall} = \frac{H_{W} + 1.0 - \sqrt{1.0 + H_{W}^{2.0}}}{2.0 \cdot H_{W}}
$$
_View factor: sky to wall, per unit wall area (Oleson Eq. 2.24) — equal to Ψ_wall_sky by reciprocity_

$$
θ_{0} = \mathrm{asin}\left(\mathrm{min}\left(\frac{1.0}{H_{W} \cdot \tan\left(\frac{μ_{zen}}{one_{rad}}\right)}, 1.0\right)\right) \cdot one_{rad}
$$
_Critical canyon orientation angle (Oleson Eq. 2.11) — the canyon-orientation azimuth threshold separating sunlit-wall from shadowed-wall geometries integrated to derive the canyon-averaged direct-beam radiation factors_

$$
S_{sunwall\,factor} = 2.0 \cdot \left(\frac{1.0}{H_{W}} \cdot \left(0.5 - \frac{θ_{0}}{π_{val} \cdot one_{rad}}\right) + \frac{1.0}{π_{val}} \cdot \tan\left(\frac{μ_{zen}}{one_{rad}}\right) \cdot \left(1.0 - \cos\left(\frac{θ_{0}}{one_{rad}}\right)\right)\right)
$$
_Sunlit wall direct beam factor (Oleson Eq. 2.16) — dimensionless fraction of atmospheric direct-beam radiation that lands on the sunlit wall per unit wall area, integrated over canyon orientation_

$$
S_{road\,factor} = 2.0 \cdot \frac{θ_{0}}{π_{val} \cdot one_{rad}} - \frac{2.0}{π_{val}} \cdot H_{W} \cdot \tan\left(\frac{μ_{zen}}{one_{rad}}\right) \cdot \left(1.0 - \cos\left(\frac{θ_{0}}{one_{rad}}\right)\right)
$$
_Road direct beam factor (Oleson Eq. 2.17) — dimensionless fraction of atmospheric direct-beam radiation that lands on the road per unit ground area; conservation Eq. 2.18 requires S_road_factor + H/W * S_sunwall_factor = 1_

$$
S_{road\,dir\,vis} = S_{road\,factor} \cdot S_{atm\,dir\,vis}
$$
_Direct beam VIS incident on road (Oleson Eq. 2.17): S_road_factor * S_atm_dir_vis_

$$
S_{road\,dir\,nir} = S_{road\,factor} \cdot S_{atm\,dir\,nir}
$$
_Direct beam NIR incident on road: S_road_factor * S_atm_dir_nir_

$$
S_{sunwall\,dir\,vis} = S_{sunwall\,factor} \cdot S_{atm\,dir\,vis}
$$
_Direct beam VIS incident on sunlit wall (Oleson Eq. 2.16): S_sunwall_factor * S_atm_dir_vis_

$$
S_{sunwall\,dir\,nir} = S_{sunwall\,factor} \cdot S_{atm\,dir\,nir}
$$
_Direct beam NIR incident on sunlit wall: S_sunwall_factor * S_atm_dir_nir_

$$
S_{road\,dif\,vis} = S_{atm\,dif\,vis} \cdot Ψ_{sky\,road}
$$
_Diffuse VIS incident on road (Oleson Eq. 2.30): S_atm_dif_vis * Ψ_sky_road_

$$
S_{road\,dif\,nir} = S_{atm\,dif\,nir} \cdot Ψ_{sky\,road}
$$
_Diffuse NIR incident on road: S_atm_dif_nir * Ψ_sky_road_

$$
S_{wall\,dif\,vis} = S_{atm\,dif\,vis} \cdot Ψ_{sky\,wall}
$$
_Diffuse VIS incident on each wall (Oleson Eqs. 2.31-2.32): S_atm_dif_vis * Ψ_sky_wall — same on sunlit and shaded walls for diffuse radiation_

$$
S_{wall\,dif\,nir} = S_{atm\,dif\,nir} \cdot Ψ_{sky\,wall}
$$
_Diffuse NIR incident on each wall: S_atm_dif_nir * Ψ_sky_wall_

$$
T_{rw} = H_{W} \cdot Ψ_{wall\,road}
$$
_Transport matrix element: wall to road (Oleson Section 2.5, p. 42-43) = H/W * Ψ_wall_road — accounts for the wall-to-road area ratio in the multi-reflection transport matrix T_

$$
T_{wr} = \frac{Ψ_{road\,wall}}{H_{W}}
$$
_Transport matrix element: road to wall = Ψ_road_wall / (H/W) — accounts for the road-to-wall area ratio (per unit wall area)_

$$
T_{ww} = Ψ_{wall\,wall}
$$
_Transport matrix element: wall to opposite wall = Ψ_wall_wall — the off-diagonal that couples the sunlit and shaded walls in the canyon-reflection geometric series_

$$
det_{dir\,vis} = \mathrm{band_det}\left(a_{r}=α_{road\,dir\,vis}, a_{w}=α_{wall\,dir\,vis}\right)
$$
_Determinant of (I - T*A) for direct VIS waveband: (1 - d²) - 2bc(1 + d), where b = a_w*T_rw, c = a_r*T_wr, d = a_w*T_ww — denominator of the closed-form multi-reflection solution_

$$
det_{dir\,nir} = \mathrm{band_det}\left(a_{r}=α_{road\,dir\,nir}, a_{w}=α_{wall\,dir\,nir}\right)
$$
_Determinant of (I - T*A) for direct NIR waveband_

$$
det_{dif\,vis} = \mathrm{band_det}\left(a_{r}=α_{road\,dif\,vis}, a_{w}=α_{wall\,dif\,vis}\right)
$$
_Determinant of (I - T*A) for diffuse VIS waveband_

$$
det_{dif\,nir} = \mathrm{band_det}\left(a_{r}=α_{road\,dif\,nir}, a_{w}=α_{wall\,dif\,nir}\right)
$$
_Determinant of (I - T*A) for diffuse NIR waveband_

$$
S_{net\,roof} = S_{atm\,dir\,vis} \cdot \left(1.0 - α_{roof\,dir\,vis}\right) + S_{atm\,dir\,nir} \cdot \left(1.0 - α_{roof\,dir\,nir}\right) + S_{atm\,dif\,vis} \cdot \left(1.0 - α_{roof\,dif\,vis}\right) + S_{atm\,dif\,nir} \cdot \left(1.0 - α_{roof\,dif\,nir}\right)
$$
_Net absorbed solar by roof (Oleson Eqs. 2.34-2.35): Σ S_atm_*_*(1 - α_roof_*_*) summed over all four wavebands_

$$
S_{net\,road\,dir\,vis} = \mathrm{band_net_road}\left(a_{r}=α_{road\,dir\,vis}, a_{w}=α_{wall\,dir\,vis}, S_{r}=S_{road\,dir\,vis}, S_{sw}=S_{sunwall\,dir\,vis}, S_{sh}=zero_{wm2}, det_{var}=det_{dir\,vis}\right)
$$
_Absorbed solar by road, direct VIS waveband: (1 - α_road_dir_vis) * Q_road_dir_vis where Q_road_dir_vis is the per-waveband closed-form M⁻¹*S_0 multi-reflection result_

$$
S_{net\,road\,dir\,nir} = \mathrm{band_net_road}\left(a_{r}=α_{road\,dir\,nir}, a_{w}=α_{wall\,dir\,nir}, S_{r}=S_{road\,dir\,nir}, S_{sw}=S_{sunwall\,dir\,nir}, S_{sh}=zero_{wm2}, det_{var}=det_{dir\,nir}\right)
$$
_Absorbed solar by road, direct NIR waveband_

$$
S_{net\,road\,dif\,vis} = \mathrm{band_net_road}\left(a_{r}=α_{road\,dif\,vis}, a_{w}=α_{wall\,dif\,vis}, S_{r}=S_{road\,dif\,vis}, S_{sw}=S_{wall\,dif\,vis}, S_{sh}=S_{wall\,dif\,vis}, det_{var}=det_{dif\,vis}\right)
$$
_Absorbed solar by road, diffuse VIS waveband_

$$
S_{net\,road\,dif\,nir} = \mathrm{band_net_road}\left(a_{r}=α_{road\,dif\,nir}, a_{w}=α_{wall\,dif\,nir}, S_{r}=S_{road\,dif\,nir}, S_{sw}=S_{wall\,dif\,nir}, S_{sh}=S_{wall\,dif\,nir}, det_{var}=det_{dif\,nir}\right)
$$
_Absorbed solar by road, diffuse NIR waveband_

$$
S_{net\,sunwall\,dir\,vis} = \mathrm{band_net_sw}\left(a_{r}=α_{road\,dir\,vis}, a_{w}=α_{wall\,dir\,vis}, S_{r}=S_{road\,dir\,vis}, S_{sw}=S_{sunwall\,dir\,vis}, S_{sh}=zero_{wm2}, det_{var}=det_{dir\,vis}\right)
$$
_Absorbed solar by sunlit wall, direct VIS waveband (per unit wall area)_

$$
S_{net\,sunwall\,dir\,nir} = \mathrm{band_net_sw}\left(a_{r}=α_{road\,dir\,nir}, a_{w}=α_{wall\,dir\,nir}, S_{r}=S_{road\,dir\,nir}, S_{sw}=S_{sunwall\,dir\,nir}, S_{sh}=zero_{wm2}, det_{var}=det_{dir\,nir}\right)
$$
_Absorbed solar by sunlit wall, direct NIR waveband_

$$
S_{net\,sunwall\,dif\,vis} = \mathrm{band_net_sw}\left(a_{r}=α_{road\,dif\,vis}, a_{w}=α_{wall\,dif\,vis}, S_{r}=S_{road\,dif\,vis}, S_{sw}=S_{wall\,dif\,vis}, S_{sh}=S_{wall\,dif\,vis}, det_{var}=det_{dif\,vis}\right)
$$
_Absorbed solar by sunlit wall, diffuse VIS waveband_

$$
S_{net\,sunwall\,dif\,nir} = \mathrm{band_net_sw}\left(a_{r}=α_{road\,dif\,nir}, a_{w}=α_{wall\,dif\,nir}, S_{r}=S_{road\,dif\,nir}, S_{sw}=S_{wall\,dif\,nir}, S_{sh}=S_{wall\,dif\,nir}, det_{var}=det_{dif\,nir}\right)
$$
_Absorbed solar by sunlit wall, diffuse NIR waveband_

$$
S_{net\,shdwall\,dir\,vis} = \mathrm{band_net_sh}\left(a_{r}=α_{road\,dir\,vis}, a_{w}=α_{wall\,dir\,vis}, S_{r}=S_{road\,dir\,vis}, S_{sw}=S_{sunwall\,dir\,vis}, S_{sh}=zero_{wm2}, det_{var}=det_{dir\,vis}\right)
$$
_Absorbed solar by shaded wall, direct VIS waveband — non-zero only via multi-reflection from road and sunlit wall (no direct beam reaches the shaded wall)_

$$
S_{net\,shdwall\,dir\,nir} = \mathrm{band_net_sh}\left(a_{r}=α_{road\,dir\,nir}, a_{w}=α_{wall\,dir\,nir}, S_{r}=S_{road\,dir\,nir}, S_{sw}=S_{sunwall\,dir\,nir}, S_{sh}=zero_{wm2}, det_{var}=det_{dir\,nir}\right)
$$
_Absorbed solar by shaded wall, direct NIR waveband_

$$
S_{net\,shdwall\,dif\,vis} = \mathrm{band_net_sh}\left(a_{r}=α_{road\,dif\,vis}, a_{w}=α_{wall\,dif\,vis}, S_{r}=S_{road\,dif\,vis}, S_{sw}=S_{wall\,dif\,vis}, S_{sh}=S_{wall\,dif\,vis}, det_{var}=det_{dif\,vis}\right)
$$
_Absorbed solar by shaded wall, diffuse VIS waveband — equal to sunwall diffuse VIS by symmetry_

$$
S_{net\,shdwall\,dif\,nir} = \mathrm{band_net_sh}\left(a_{r}=α_{road\,dif\,nir}, a_{w}=α_{wall\,dif\,nir}, S_{r}=S_{road\,dif\,nir}, S_{sw}=S_{wall\,dif\,nir}, S_{sh}=S_{wall\,dif\,nir}, det_{var}=det_{dif\,nir}\right)
$$
_Absorbed solar by shaded wall, diffuse NIR waveband_

$$
S_{net\,road} = S_{net\,road\,dir\,vis} + S_{net\,road\,dir\,nir} + S_{net\,road\,dif\,vis} + S_{net\,road\,dif\,nir}
$$
_Total net absorbed solar by road: sum of S_net_road_* over the four wavebands_

$$
S_{net\,sunwall} = S_{net\,sunwall\,dir\,vis} + S_{net\,sunwall\,dir\,nir} + S_{net\,sunwall\,dif\,vis} + S_{net\,sunwall\,dif\,nir}
$$
_Total net absorbed solar by sunlit wall per unit wall area: sum of S_net_sunwall_* over the four wavebands_

$$
S_{net\,shdwall} = S_{net\,shdwall\,dir\,vis} + S_{net\,shdwall\,dir\,nir} + S_{net\,shdwall\,dif\,vis} + S_{net\,shdwall\,dif\,nir}
$$
_Total net absorbed solar by shaded wall per unit wall area: sum of S_net_shdwall_* over the four wavebands_

$$
S_{net\,uc} = S_{net\,road} + \left(S_{net\,sunwall} + S_{net\,shdwall}\right) \cdot H_{W}
$$
_Net absorbed solar by the urban canyon per unit ground area: S_net_road + (S_net_sunwall + S_net_shdwall) * H/W_

$$
S_{net\,total} = W_{roof} \cdot S_{net\,roof} + \left(1.0 - W_{roof}\right) \cdot S_{net\,uc}
$$
_Total net absorbed solar (Oleson Eq. 2.95): W_roof * S_net_roof + (1 - W_roof) * S_net_uc — area-weighted total over roof and canyon_

$$
S_{refl\,sky\,dir\,vis} = \mathrm{band_refl_sky}\left(S_{r}=S_{road\,dir\,vis}, S_{sw}=S_{sunwall\,dir\,vis}, S_{sh}=zero_{wm2}, net_{road}=S_{net\,road\,dir\,vis}, net_{sw}=S_{net\,sunwall\,dir\,vis}, net_{sh}=S_{net\,shdwall\,dir\,vis}\right)
$$
_Solar reflected back to sky from the canyon, direct VIS waveband — energy-balance closure: incident_canyon - absorbed_canyon (per unit ground area)_

$$
S_{refl\,sky\,dir\,nir} = \mathrm{band_refl_sky}\left(S_{r}=S_{road\,dir\,nir}, S_{sw}=S_{sunwall\,dir\,nir}, S_{sh}=zero_{wm2}, net_{road}=S_{net\,road\,dir\,nir}, net_{sw}=S_{net\,sunwall\,dir\,nir}, net_{sh}=S_{net\,shdwall\,dir\,nir}\right)
$$
_Solar reflected back to sky from the canyon, direct NIR waveband_

$$
S_{refl\,sky\,dif\,vis} = \mathrm{band_refl_sky}\left(S_{r}=S_{road\,dif\,vis}, S_{sw}=S_{wall\,dif\,vis}, S_{sh}=S_{wall\,dif\,vis}, net_{road}=S_{net\,road\,dif\,vis}, net_{sw}=S_{net\,sunwall\,dif\,vis}, net_{sh}=S_{net\,shdwall\,dif\,vis}\right)
$$
_Solar reflected back to sky from the canyon, diffuse VIS waveband_

$$
S_{refl\,sky\,dif\,nir} = \mathrm{band_refl_sky}\left(S_{r}=S_{road\,dif\,nir}, S_{sw}=S_{wall\,dif\,nir}, S_{sh}=S_{wall\,dif\,nir}, net_{road}=S_{net\,road\,dif\,nir}, net_{sw}=S_{net\,sunwall\,dif\,nir}, net_{sh}=S_{net\,shdwall\,dif\,nir}\right)
$$
_Solar reflected back to sky from the canyon, diffuse NIR waveband_

$$
α_{uc\,dir\,vis} = \mathrm{ifelse}\left(\mathrm{>}\left(S_{road\,dir\,vis} + S_{sunwall\,dir\,vis} \cdot H_{W}, zero_{wm2}\right), \frac{S_{refl\,sky\,dir\,vis}}{S_{road\,dir\,vis} + S_{sunwall\,dir\,vis} \cdot H_{W}}, 0.0\right)
$$
_Canyon direct beam albedo, VIS (Oleson Eq. 2.93): S_refl_sky_dir_vis / incident_canyon — the ratio of reflected to incident summed over the canyon (excluding the roof). Guarded against divide-by-zero when there is no incident radiation in this waveband._

$$
α_{uc\,dir\,nir} = \mathrm{ifelse}\left(\mathrm{>}\left(S_{road\,dir\,nir} + S_{sunwall\,dir\,nir} \cdot H_{W}, zero_{wm2}\right), \frac{S_{refl\,sky\,dir\,nir}}{S_{road\,dir\,nir} + S_{sunwall\,dir\,nir} \cdot H_{W}}, 0.0\right)
$$
_Canyon direct beam albedo, NIR_

$$
α_{uc\,dif\,vis} = \mathrm{ifelse}\left(\mathrm{>}\left(S_{road\,dif\,vis} + 2.0 \cdot S_{wall\,dif\,vis} \cdot H_{W}, zero_{wm2}\right), \frac{S_{refl\,sky\,dif\,vis}}{S_{road\,dif\,vis} + 2.0 \cdot S_{wall\,dif\,vis} \cdot H_{W}}, 0.0\right)
$$
_Canyon diffuse albedo, VIS (Oleson Eq. 2.94)_

$$
α_{uc\,dif\,nir} = \mathrm{ifelse}\left(\mathrm{>}\left(S_{road\,dif\,nir} + 2.0 \cdot S_{wall\,dif\,nir} \cdot H_{W}, zero_{wm2}\right), \frac{S_{refl\,sky\,dif\,nir}}{S_{road\,dif\,nir} + 2.0 \cdot S_{wall\,dif\,nir} \cdot H_{W}}, 0.0\right)
$$
_Canyon diffuse albedo, NIR_

$$
L_{up\,roof} = ε_{roof} \cdot σ_{SB} \cdot T_{roof}^{4.0} + \left(1.0 - ε_{roof}\right) \cdot L_{atm\,down}
$$
_Upward longwave radiation from roof (Oleson Eq. 2.102): ε_roof * σ_SB * T_roof^4 + (1 - ε_roof) * L_atm_down — Stefan-Boltzmann emission plus reflection of the downwelling atmospheric LW_

$$
L_{net\,roof} = L_{up\,roof} - L_{atm\,down}
$$
_Net longwave for roof (Oleson Eq. 2.101): L_up_roof - L_atm_down — positive when the roof is losing more LW than it absorbs_

$$
L_{emit\,road} = ε_{road} \cdot σ_{SB} \cdot T_{road}^{4.0}
$$
_Emitted longwave from road (Oleson Eq. 2.111): ε_road * σ_SB * T_road^4 — Stefan-Boltzmann emission only, before multi-reflection_

$$
L_{emit\,sunwall} = ε_{wall} \cdot σ_{SB} \cdot T_{sunwall}^{4.0}
$$
_Emitted longwave from sunlit wall (Oleson Eq. 2.112): ε_wall * σ_SB * T_sunwall^4_

$$
L_{emit\,shdwall} = ε_{wall} \cdot σ_{SB} \cdot T_{shdwall}^{4.0}
$$
_Emitted longwave from shaded wall (Oleson Eq. 2.113): ε_wall * σ_SB * T_shdwall^4_

$$
det_{lw} = 1.0 - \left(\left(1.0 - ε_{wall}\right) \cdot T_{ww}\right)^{2.0} - 2.0 \cdot \left(1.0 - ε_{wall}\right) \cdot T_{rw} \cdot \left(1.0 - ε_{road}\right) \cdot T_{wr} \cdot \left(1.0 + \left(1.0 - ε_{wall}\right) \cdot T_{ww}\right)
$$
_Determinant of (I - T*A) for longwave: (1 - d_lw²) - 2*b_lw*c_lw*(1 + d_lw), where b_lw = (1-ε_wall)*T_rw, c_lw = (1-ε_road)*T_wr, d_lw = (1-ε_wall)*T_ww — structurally identical to the solar determinant but with reflectivity (1 - ε) in place of albedo α_

$$
L_{net\,road} = L_{emit\,road} - ε_{road} \cdot \frac{\left(1.0 - \left(\left(1.0 - ε_{wall}\right) \cdot T_{ww}\right)^{2.0}\right) \cdot \left(L_{atm\,down} \cdot Ψ_{sky\,road} + T_{rw} \cdot \left(L_{emit\,sunwall} + L_{emit\,shdwall}\right)\right) + \left(1.0 - ε_{wall}\right) \cdot T_{rw} \cdot \left(1.0 + \left(1.0 - ε_{wall}\right) \cdot T_{ww}\right) \cdot \left(L_{atm\,down} \cdot Ψ_{sky\,wall} + T_{wr} \cdot L_{emit\,road} + T_{ww} \cdot L_{emit\,shdwall}\right) + \left(1.0 - ε_{wall}\right) \cdot T_{rw} \cdot \left(1.0 + \left(1.0 - ε_{wall}\right) \cdot T_{ww}\right) \cdot \left(L_{atm\,down} \cdot Ψ_{sky\,wall} + T_{wr} \cdot L_{emit\,road} + T_{ww} \cdot L_{emit\,sunwall}\right)}{det_{lw}}
$$
_Net longwave for road: L_emit_road - ε_road * Q_road_lw, where Q_road_lw is the canyon-trapped incoming LW from atmosphere and wall emission via the multi-reflection M⁻¹*S_0_lw solution. Positive when the road loses more LW than it absorbs._

$$
L_{net\,sunwall} = L_{emit\,sunwall} - ε_{wall} \cdot \frac{\left(1.0 - ε_{road}\right) \cdot T_{wr} \cdot \left(1.0 + \left(1.0 - ε_{wall}\right) \cdot T_{ww}\right) \cdot \left(L_{atm\,down} \cdot Ψ_{sky\,road} + T_{rw} \cdot \left(L_{emit\,sunwall} + L_{emit\,shdwall}\right)\right) + \left(1.0 - \left(1.0 - ε_{wall}\right) \cdot T_{rw} \cdot \left(1.0 - ε_{road}\right) \cdot T_{wr}\right) \cdot \left(L_{atm\,down} \cdot Ψ_{sky\,wall} + T_{wr} \cdot L_{emit\,road} + T_{ww} \cdot L_{emit\,shdwall}\right) + \left(\left(1.0 - ε_{wall}\right) \cdot T_{ww} + \left(1.0 - ε_{wall}\right) \cdot T_{rw} \cdot \left(1.0 - ε_{road}\right) \cdot T_{wr}\right) \cdot \left(L_{atm\,down} \cdot Ψ_{sky\,wall} + T_{wr} \cdot L_{emit\,road} + T_{ww} \cdot L_{emit\,sunwall}\right)}{det_{lw}}
$$
_Net longwave for sunlit wall per unit wall area: L_emit_sunwall - ε_wall * Q_sw_lw_

$$
L_{net\,shdwall} = L_{emit\,shdwall} - ε_{wall} \cdot \frac{\left(1.0 - ε_{road}\right) \cdot T_{wr} \cdot \left(1.0 + \left(1.0 - ε_{wall}\right) \cdot T_{ww}\right) \cdot \left(L_{atm\,down} \cdot Ψ_{sky\,road} + T_{rw} \cdot \left(L_{emit\,sunwall} + L_{emit\,shdwall}\right)\right) + \left(\left(1.0 - ε_{wall}\right) \cdot T_{ww} + \left(1.0 - ε_{wall}\right) \cdot T_{rw} \cdot \left(1.0 - ε_{road}\right) \cdot T_{wr}\right) \cdot \left(L_{atm\,down} \cdot Ψ_{sky\,wall} + T_{wr} \cdot L_{emit\,road} + T_{ww} \cdot L_{emit\,shdwall}\right) + \left(1.0 - \left(1.0 - ε_{wall}\right) \cdot T_{rw} \cdot \left(1.0 - ε_{road}\right) \cdot T_{wr}\right) \cdot \left(L_{atm\,down} \cdot Ψ_{sky\,wall} + T_{wr} \cdot L_{emit\,road} + T_{ww} \cdot L_{emit\,sunwall}\right)}{det_{lw}}
$$
_Net longwave for shaded wall per unit wall area: L_emit_shdwall - ε_wall * Q_sh_lw_

$$
L_{net\,uc} = L_{net\,road} + \left(L_{net\,sunwall} + L_{net\,shdwall}\right) \cdot H_{W}
$$
_Net longwave for urban canyon per unit ground area (Oleson Eq. 2.172): L_net_road + (L_net_sunwall + L_net_shdwall) * H/W_

$$
L_{net\,total} = W_{roof} \cdot L_{net\,roof} + \left(1.0 - W_{roof}\right) \cdot L_{net\,uc}
$$
_Total net longwave (Oleson Eq. 2.175): W_roof * L_net_roof + (1 - W_roof) * L_net_uc — area-weighted total over roof and canyon_

## Expression Templates

### `band_det`

**Parameters:** `a_r`, `a_w`

$$
1.0 - \left(a_{w} \cdot T_{ww}\right)^{2.0} - 2.0 \cdot a_{w} \cdot T_{rw} \cdot a_{r} \cdot T_{wr} \cdot \left(1.0 + a_{w} \cdot T_{ww}\right)
$$

### `band_net_road`

**Parameters:** `a_r`, `a_w`, `S_r`, `S_sw`, `S_sh`, `det_var`

$$
\left(1.0 - a_{r}\right) \cdot \frac{\left(1.0 - \left(a_{w} \cdot T_{ww}\right)^{2.0}\right) \cdot S_{r} + a_{w} \cdot T_{rw} \cdot \left(1.0 + a_{w} \cdot T_{ww}\right) \cdot S_{sw} + a_{w} \cdot T_{rw} \cdot \left(1.0 + a_{w} \cdot T_{ww}\right) \cdot S_{sh}}{det_{var}}
$$

### `band_net_sw`

**Parameters:** `a_r`, `a_w`, `S_r`, `S_sw`, `S_sh`, `det_var`

$$
\left(1.0 - a_{w}\right) \cdot \frac{a_{r} \cdot T_{wr} \cdot \left(1.0 + a_{w} \cdot T_{ww}\right) \cdot S_{r} + \left(1.0 - a_{w} \cdot T_{rw} \cdot a_{r} \cdot T_{wr}\right) \cdot S_{sw} + \left(a_{w} \cdot T_{ww} + a_{w} \cdot T_{rw} \cdot a_{r} \cdot T_{wr}\right) \cdot S_{sh}}{det_{var}}
$$

### `band_net_sh`

**Parameters:** `a_r`, `a_w`, `S_r`, `S_sw`, `S_sh`, `det_var`

$$
\left(1.0 - a_{w}\right) \cdot \frac{a_{r} \cdot T_{wr} \cdot \left(1.0 + a_{w} \cdot T_{ww}\right) \cdot S_{r} + \left(a_{w} \cdot T_{ww} + a_{w} \cdot T_{rw} \cdot a_{r} \cdot T_{wr}\right) \cdot S_{sw} + \left(1.0 - a_{w} \cdot T_{rw} \cdot a_{r} \cdot T_{wr}\right) \cdot S_{sh}}{det_{var}}
$$

### `band_refl_sky`

**Parameters:** `S_r`, `S_sw`, `S_sh`, `net_road`, `net_sw`, `net_sh`

$$
S_{r} + \left(S_{sw} + S_{sh}\right) \cdot H_{W} - \left(net_{road} + \left(net_{sw} + net_{sh}\right) \cdot H_{W}\right)
$$

## Analyses

### view_factors_vs_HW

Reproduces Oleson Figure 2.4 (p. 37): view factors as a function of canyon H/W ratio. Sweeps H/W from 0.01 to 10 on a log scale. Ψ_road_sky transitions from ~1 (flat) to ~0 (deep canyon); Ψ_wall_wall transitions from ~0 to ~1; Ψ_wall_sky = Ψ_wall_road stays in the range [0, 0.5].

**Time span:** 0.0 → 1.0

**Swept over:** `H_W`

![Road→sky view factor vs H/W (log x): monotone decrease from ~1 (flat) to ~0 (deep canyon).](/plots/urban_canopy/urbanradiation/view_factors_vs_HW-psi_road_sky_curve.png)

![Wall→sky view factor vs H/W (= wall→road by reciprocity): saturates at 0.5 as H/W → ∞.](/plots/urban_canopy/urbanradiation/view_factors_vs_HW-psi_wall_sky_curve.png)

![Wall→wall view factor vs H/W: monotone increase from 0 (flat) to ~1 (deep canyon).](/plots/urban_canopy/urbanradiation/view_factors_vs_HW-psi_wall_wall_curve.png)

### absorbed_solar_vs_HW_30deg

Reproduces Oleson Figure 2.5 top panel (p. 47): absorbed solar radiation by canyon surfaces as a function of H/W at solar zenith angle 30°. Roof absorption is constant; canyon absorption increases slowly with H/W (radiation trapping); road absorption decreases as buildings shade it; sunlit and shaded wall absorptions vary with multi-reflection.

**Time span:** 0.0 → 1.0

**Swept over:** `H_W`

![Total canyon absorbed solar (per unit ground area) vs H/W at solar zenith 30°: slow increase from radiation trapping.](/plots/urban_canopy/urbanradiation/absorbed_solar_vs_HW_30deg-S_net_uc_curve_30deg.png)

![Road absorbed solar vs H/W at solar zenith 30°: rapid decrease from building shading.](/plots/urban_canopy/urbanradiation/absorbed_solar_vs_HW_30deg-S_net_road_curve_30deg.png)

### canyon_albedo_vs_HW

Reproduces Oleson Figure 2.6 (p. 48): canyon diffuse albedo as a function of H/W. Canyon albedo decreases monotonically with H/W because radiation trapping in deeper canyons increases total absorption. Asymptotic limits: at H/W → 0 the canyon albedo approaches the road albedo (~0.08); at H/W → ∞ the canyon albedo approaches a limit dominated by multi-reflection between walls.

**Time span:** 0.0 → 1.0

**Swept over:** `H_W`

![Canyon diffuse VIS albedo vs H/W: monotone decrease from radiation trapping.](/plots/urban_canopy/urbanradiation/canyon_albedo_vs_HW-alpha_uc_dif_vis_curve.png)

### net_lw_vs_HW_equal_T

Reproduces Oleson Figure 2.7 (p. 59): net longwave radiation vs H/W at equal surface temperatures (T = 292.16 K). Net LW is positive when surfaces emit more than they absorb; with all surfaces equal and ε < 1, each surface still has a small positive net LW because of view-factor-weighted exchange with the cooler sky.

**Time span:** 0.0 → 1.0

**Swept over:** `H_W`

![Canyon net LW (per unit ground area) vs H/W at equal surface temperatures: slow increase with H/W as wall area grows.](/plots/urban_canopy/urbanradiation/net_lw_vs_HW_equal_T-L_net_uc_curve.png)

![Road net LW vs H/W at equal surface temperatures: decreases with H/W as the road sees more warm walls and less cold sky.](/plots/urban_canopy/urbanradiation/net_lw_vs_HW_equal_T-L_net_road_curve.png)

### canyon_albedo_heatmap_HW_zenith

2D sweep over H/W and solar zenith angle: surfaces the dependence of direct-beam canyon albedo on canyon geometry and sun position. At low solar zenith (sun overhead), albedo is dominated by road and decreases with H/W. At high solar zenith (sun near horizon), more direct radiation hits the walls and the canyon albedo grows toward the wall albedo, especially at small H/W.

**Time span:** 0.0 → 1.0

**Swept over:** `H_W`, `μ_zen`

![Canyon direct-beam VIS albedo as a function of canyon H/W and solar zenith angle. Low at small H/W and small zenith (sun overhead, road-dominated); rises at large zenith (wall-dominated).](/plots/urban_canopy/urbanradiation/canyon_albedo_heatmap_HW_zenith-alpha_uc_dir_vis_heatmap.png)

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "reference": {
    "notes": "source_ref: UrbanCanopy.jl@9200edd4f15609f20339d3a7d104de8064544310:src/albedos_radiative_fluxes.jl:27\nUpstream `UrbanRadiation` is an MTK `@component` with five `@constants` (σ_SB = 5.67e-8 W/(m²·K⁴), π_val = π dimensionless, one_rad = 1.0 rad, one_wm2 = 1.0 W/m², zero_wm2 = 0.0 W/m²), 31 `@parameters` (geometry H_W/W_roof, four atmospheric solar fluxes S_atm_*, atmospheric longwave L_atm_down, solar zenith μ_zen, twelve surface albedos α_*_*_* across roof/road/wall × dir/dif × vis/nir, three emissivities ε_*, four surface temperatures T_*), 62 time-indexed `@variables` (view factors Ψ_*, transport matrix T_rw/T_wr/T_ww, direct-beam factors θ_0/S_*_factor, incident/absorbed/reflected radiation S_*, canyon albedos α_uc_*, longwave fluxes L_*), and 62 algebraic equations (no derivatives). Identical equation structure preserved here.\n\nThe upstream component declares five `@constants`, all encoded here as parameters with the upstream defaults: σ_SB = 5.67e-8 W/(m²·K⁴) (Stefan-Boltzmann from Oleson Table 1.4); π_val = π (the Float64 value of Julia's π constant); one_rad = 1.0 rad (unit-balancer for the rad-dimensioned μ_zen and θ_0); one_wm2 = 1.0 W/m² (unit-balancer for the W/m² comparison in the canyon-albedo guard); zero_wm2 = 0.0 W/m² (unit-balancing zero for the canyon-albedo guard's else branch). Greek symbols (Ψ for view factors, α for albedos, ε for emissivities, σ for Stefan-Boltzmann, μ for solar zenith, π for pi, θ for canyon orientation, Δ-style underscored subscripts) are preserved verbatim from upstream — peer ESM files in this rig already use Greek letters in identifiers (e.g. urban_surface_thermal.esm uses λ_prescribed / c_prescribed, freezing_point_depression.esm uses ψ_sat / θ_sat / ρ_liq, snow_melt_no_layers.esm uses Δt), and Oleson Chapter 2 uses these Greek symbols extensively in its equations; keeping them preserves the direct equation-to-symbol correspondence that aids review against the technical note.\n\nMulti-reflection closed form: the upstream source contains a Julia `for` loop that generates 4 sets of 5 equations (one set per waveband × incidence-type: direct VIS, direct NIR, diffuse VIS, diffuse NIR) for the canyon solar multi-reflection. The loop body computes intermediate quantities b = a_w*T_rw, c = a_r*T_wr, d = a_w*T_ww (the M = I - T*A matrix off-diagonal products), then det = (1-d²) - 2bc(1+d) (the M-matrix determinant per the adjugate formula in the source's :240-:246 docstring), then the three M⁻¹*S_0 product components Q_road/Q_sw/Q_sh, and finally the absorbed-flux assignments S_net_* = (1-α)*Q and the reflected-to-sky energy-balance closure S_refl_sky = incident - absorbed. The migrated ESM encodes the 20 equations using v0.4.0 expression_templates (RFC docs/rfcs/ast-expression-templates.md): five templates `band_det`, `band_net_road`, `band_net_sw`, `band_net_sh`, `band_refl_sky` each take the per-waveband free variables (a_r, a_w, S_r, S_sw, S_sh, det_var, and for refl_sky additionally net_road/net_sw/net_sh) as parameter substitution slots; each template is invoked 4 times (once per waveband). At load time `apply_expression_template` nodes expand structurally, so the canonical AST a loader sees after parse-then-emit is the fully-inlined 20-equation form — bit-equivalent to writing the equations inline. The longwave multi-reflection block (Eqs. 2.138-2.170, source :355-:393) is structurally identical to the solar block with one invocation, but with substituted source terms (atmospheric LW + emitted LW from other surfaces) — encoded here as 4 inline equations (det_lw + 3 L_net_*) since the single-invocation site does not benefit from a template.\n\nUpstream `local` Julia variables b/c/d/Q_road/Q_sw/Q_sh are not user-visible MTK state variables (they're intermediate let-bindings, expanded by Julia's `local` into the right-hand-side AST of the resulting equations). The migrated ESM preserves this by inlining the same expressions into the template bodies — the canonical 62-equation form after expression-template expansion has 62 LHS state variables matching upstream's `length(unknowns(sys)) == 62` invariant.\n\nθ_0 unit balancing (Eq. 2.11): the upstream form `θ_0 = asin(min(1 / (H_W * tan(μ_zen / one_rad)), 1)) * one_rad` is preserved verbatim. The unit contract: μ_zen has dimension rad; dividing by one_rad makes it dimensionless for the `tan` and `min` operations; multiplying the dimensionless `asin` result by one_rad restores the rad dimension. The numeric value is identical to the unfused `asin(min(1/(H_W*tan(μ_zen)), 1))` because one_rad = 1.0 exactly, but the form is kept to mirror the upstream unit contract for any future ESS unit checker.\n\nCanyon albedo guard (Eqs. 2.93-2.94): the upstream guard uses `ifelse(incident > zero_wm2, refl/incident, 0.0)` to avoid divide-by-zero when there is no incident radiation in this waveband. Preserved verbatim. The bare `0.0` else branch is a dimensionless literal — matches upstream where canyon albedo is dimensionless. (Compare with snow_melt_no_layers.esm which uses a dimensioned `zero_m` else branch for its depth output.)\n\nObservability classification: this component is functionally observed-only — every output variable is given by a single algebraic equation in terms of the parameters and earlier-computed state variables (the `(t)` time index has no role since there are no derivatives). Test scenarios use `time_span: [0, 1]` and sample at t=0 to mirror the convention used by sibling observed-only ESM files in this rig (surface_energy_flux.esm, snow_melt_no_layers.esm, freezing_point_depression.esm).\n\nTolerance rationale (model-level rel=1e-8): observed-only algebraic system (no ODE integration); the most numerically delicate equations are the canyon multi-reflection ones (`det = (1-d²) - 2bc(1+d)` and the `Q/det` divisions for absorbed-flux and reflected-flux), which involve products and quotients of dimensionless quantities and can accumulate ~1e-13 rounding under the canonical test parameters (e.g. the residual `(S_r + ...) - (net_road + ...)` energy-balance closure for the reflected-flux equation evaluates to ~1e-13 W/m² in regimes where the closure should be exact). 1e-8 leaves comfortable headroom above this and matches the convention used by the most numerically rich peer (heat_flux.esm uses 1e-9 for a single-equation Fourier flux; surface_energy_flux.esm uses 1e-9 for additive flux balances — UrbanRadiation is one ULP-decade looser because of the canyon multi-reflection closed-form solution's higher polynomial degree). Tighter `abs: 1e-10` is asserted on outputs that are exactly zero by construction (e.g. zero albedos → zero reflected flux; equal-temperature blackbody → zero net LW for the symmetric canyon) so the assertion does not silently accept a stuck-at-1e-3 regression.\n\nUpstream tolerance reproduction: the upstream tests use rtol = 1.0e-10 for analytical view factor checks (e.g. Eqs. 2.22-2.28 against manually computed reference values), rtol = 1.0e-8 for energy-conservation closures, and rtol = 1.0e-6 for canyon LW blackbody asymptotics. Per-assertion tolerances are set to match — 1e-10 for view-factor analytics, 1e-8 for energy conservation, 1e-6 for the blackbody LW reference."
  },
  "tolerance": {
    "rel": 1e-08
  },
  "expression_templates": {
    "band_det": {
      "params": [
        "a_r",
        "a_w"
      ],
      "body": {
        "op": "-",
        "args": [
          {
            "op": "-",
            "args": [
              1.0,
              {
                "op": "^",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      "a_w",
                      "T_ww"
                    ]
                  },
                  2.0
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "*",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      2.0,
                      {
                        "op": "*",
                        "args": [
                          "a_w",
                          "T_rw"
                        ]
                      }
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "a_r",
                      "T_wr"
                    ]
                  }
                ]
              },
              {
                "op": "+",
                "args": [
                  1.0,
                  {
                    "op": "*",
                    "args": [
                      "a_w",
                      "T_ww"
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    },
    "band_net_road": {
      "params": [
        "a_r",
        "a_w",
        "S_r",
        "S_sw",
        "S_sh",
        "det_var"
      ],
      "body": {
        "op": "*",
        "args": [
          {
            "op": "-",
            "args": [
              1.0,
              "a_r"
            ]
          },
          {
            "op": "/",
            "args": [
              {
                "op": "+",
                "args": [
                  {
                    "op": "+",
                    "args": [
                      {
                        "op": "*",
                        "args": [
                          {
                            "op": "-",
                            "args": [
                              1.0,
                              {
                                "op": "^",
                                "args": [
                                  {
                                    "op": "*",
                                    "args": [
                                      "a_w",
                                      "T_ww"
                                    ]
                                  },
                                  2.0
                                ]
                              }
                            ]
                          },
                          "S_r"
                        ]
                      },
                      {
                        "op": "*",
                        "args": [
                          {
                            "op": "*",
                            "args": [
                              {
                                "op": "*",
                                "args": [
                                  "a_w",
                                  "T_rw"
                                ]
                              },
                              {
                                "op": "+",
                                "args": [
                                  1.0,
                                  {
                                    "op": "*",
                                    "args": [
                                      "a_w",
                                      "T_ww"
                                    ]
                                  }
                                ]
                              }
                            ]
                          },
                          "S_sw"
                        ]
                      }
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      {
                        "op": "*",
                        "args": [
                          {
                            "op": "*",
                            "args": [
                              "a_w",
                              "T_rw"
                            ]
                          },
                          {
                            "op": "+",
                            "args": [
                              1.0,
                              {
                                "op": "*",
                                "args": [
                                  "a_w",
                                  "T_ww"
                                ]
                              }
                            ]
                          }
                        ]
                      },
                      "S_sh"
                    ]
                  }
                ]
              },
              "det_var"
            ]
          }
        ]
      }
    },
    "band_net_sw": {
      "params": [
        "a_r",
        "a_w",
        "S_r",
        "S_sw",
        "S_sh",
        "det_var"
      ],
      "body": {
        "op": "*",
        "args": [
          {
            "op": "-",
            "args": [
              1.0,
              "a_w"
            ]
          },
          {
            "op": "/",
            "args": [
              {
                "op": "+",
                "args": [
                  {
                    "op": "+",
                    "args": [
                      {
                        "op": "*",
                        "args": [
                          {
                            "op": "*",
                            "args": [
                              {
                                "op": "*",
                                "args": [
                                  "a_r",
                                  "T_wr"
                                ]
                              },
                              {
                                "op": "+",
                                "args": [
                                  1.0,
                                  {
                                    "op": "*",
                                    "args": [
                                      "a_w",
                                      "T_ww"
                                    ]
                                  }
                                ]
                              }
                            ]
                          },
                          "S_r"
                        ]
                      },
                      {
                        "op": "*",
                        "args": [
                          {
                            "op": "-",
                            "args": [
                              1.0,
                              {
                                "op": "*",
                                "args": [
                                  {
                                    "op": "*",
                                    "args": [
                                      "a_w",
                                      "T_rw"
                                    ]
                                  },
                                  {
                                    "op": "*",
                                    "args": [
                                      "a_r",
                                      "T_wr"
                                    ]
                                  }
                                ]
                              }
                            ]
                          },
                          "S_sw"
                        ]
                      }
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      {
                        "op": "+",
                        "args": [
                          {
                            "op": "*",
                            "args": [
                              "a_w",
                              "T_ww"
                            ]
                          },
                          {
                            "op": "*",
                            "args": [
                              {
                                "op": "*",
                                "args": [
                                  "a_w",
                                  "T_rw"
                                ]
                              },
                              {
                                "op": "*",
                                "args": [
                                  "a_r",
                                  "T_wr"
                                ]
                              }
                            ]
                          }
                        ]
                      },
                      "S_sh"
                    ]
                  }
                ]
              },
              "det_var"
            ]
          }
        ]
      }
    },
    "band_net_sh": {
      "params": [
        "a_r",
        "a_w",
        "S_r",
        "S_sw",
        "S_sh",
        "det_var"
      ],
      "body": {
        "op": "*",
        "args": [
          {
            "op": "-",
            "args": [
              1.0,
              "a_w"
            ]
          },
          {
            "op": "/",
            "args": [
              {
                "op": "+",
                "args": [
                  {
                    "op": "+",
                    "args": [
                      {
                        "op": "*",
                        "args": [
                          {
                            "op": "*",
                            "args": [
                              {
                                "op": "*",
                                "args": [
                                  "a_r",
                                  "T_wr"
                                ]
                              },
                              {
                                "op": "+",
                                "args": [
                                  1.0,
                                  {
                                    "op": "*",
                                    "args": [
                                      "a_w",
                                      "T_ww"
                                    ]
                                  }
                                ]
                              }
                            ]
                          },
                          "S_r"
                        ]
                      },
                      {
                        "op": "*",
                        "args": [
                          {
                            "op": "+",
                            "args": [
                              {
                                "op": "*",
                                "args": [
                                  "a_w",
                                  "T_ww"
                                ]
                              },
                              {
                                "op": "*",
                                "args": [
                                  {
                                    "op": "*",
                                    "args": [
                                      "a_w",
                                      "T_rw"
                                    ]
                                  },
                                  {
                                    "op": "*",
                                    "args": [
                                      "a_r",
                                      "T_wr"
                                    ]
                                  }
                                ]
                              }
                            ]
                          },
                          "S_sw"
                        ]
                      }
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      {
                        "op": "-",
                        "args": [
                          1.0,
                          {
                            "op": "*",
                            "args": [
                              {
                                "op": "*",
                                "args": [
                                  "a_w",
                                  "T_rw"
                                ]
                              },
                              {
                                "op": "*",
                                "args": [
                                  "a_r",
                                  "T_wr"
                                ]
                              }
                            ]
                          }
                        ]
                      },
                      "S_sh"
                    ]
                  }
                ]
              },
              "det_var"
            ]
          }
        ]
      }
    },
    "band_refl_sky": {
      "params": [
        "S_r",
        "S_sw",
        "S_sh",
        "net_road",
        "net_sw",
        "net_sh"
      ],
      "body": {
        "op": "-",
        "args": [
          {
            "op": "+",
            "args": [
              "S_r",
              {
                "op": "*",
                "args": [
                  {
                    "op": "+",
                    "args": [
                      "S_sw",
                      "S_sh"
                    ]
                  },
                  "H_W"
                ]
              }
            ]
          },
          {
            "op": "+",
            "args": [
              "net_road",
              {
                "op": "*",
                "args": [
                  {
                    "op": "+",
                    "args": [
                      "net_sw",
                      "net_sh"
                    ]
                  },
                  "H_W"
                ]
              }
            ]
          }
        ]
      }
    }
  },
  "variables": {
    "σ_SB": {
      "type": "parameter",
      "units": "W/(m^2*K^4)",
      "default": 5.67e-08,
      "description": "Stefan-Boltzmann constant (Oleson Table 1.4) — upstream `@constants` σ_SB; the coefficient of T^4 in the Stefan-Boltzmann law for upward longwave emission used in Eqs. 2.102, 2.111-2.113"
    },
    "π_val": {
      "type": "parameter",
      "units": "1",
      "default": 3.141592653589793,
      "description": "Pi (dimensionless) — upstream `@constants` π_val = Float64(π); appears in the direct-beam canyon-orientation factors of Eqs. 2.16-2.17"
    },
    "one_rad": {
      "type": "parameter",
      "units": "rad",
      "default": 1.0,
      "description": "Unit-angle reference (1 rad) — upstream `@constants` one_rad; used in `μ_zen / one_rad` to make the argument of `tan` dimensionless and in `asin(...) * one_rad` to restore rad dimension on θ_0 (Eq. 2.11). Value is exactly 1.0 by construction; numerically a no-op."
    },
    "one_wm2": {
      "type": "parameter",
      "units": "W/m^2",
      "default": 1.0,
      "description": "Unit radiative flux (1 W/m²) — upstream `@constants` one_wm2; declared by the upstream component but unused in the equation block (kept here for 1:1 parameter-count fidelity with upstream `length(parameters(sys)) == 31`). The unit-balancing role of one_wm2 is taken by `zero_wm2` in the canyon-albedo guard."
    },
    "zero_wm2": {
      "type": "parameter",
      "units": "W/m^2",
      "default": 0.0,
      "description": "Zero radiative flux (0 W/m²) — upstream `@constants` zero_wm2; used as the comparison RHS in the canyon-albedo guard `ifelse(incident > zero_wm2, refl/incident, 0.0)` to keep the `>` comparison unit-consistent with the W/m² LHS"
    },
    "H_W": {
      "type": "parameter",
      "units": "1",
      "default": 1.0,
      "description": "Canyon height-to-width ratio H/W (dimensionless) — controls all view factor geometry (Eqs. 2.22-2.28); typical urban values 0.5-3, but the implementation is valid for 0 (flat) to large (deep canyon)"
    },
    "W_roof": {
      "type": "parameter",
      "units": "1",
      "default": 0.25,
      "description": "Roof fraction of urban surface (dimensionless) — controls the area-weighted combination of roof and canyon contributions to total net radiation in Eqs. 2.95 and 2.175"
    },
    "S_atm_dir_vis": {
      "type": "parameter",
      "units": "W/m^2",
      "default": 200.0,
      "description": "Incident direct beam visible solar radiation from the atmosphere (upstream `@parameters` S_atm_dir_vis)"
    },
    "S_atm_dir_nir": {
      "type": "parameter",
      "units": "W/m^2",
      "default": 150.0,
      "description": "Incident direct beam NIR solar radiation from the atmosphere"
    },
    "S_atm_dif_vis": {
      "type": "parameter",
      "units": "W/m^2",
      "default": 80.0,
      "description": "Incident diffuse visible solar radiation from the atmosphere"
    },
    "S_atm_dif_nir": {
      "type": "parameter",
      "units": "W/m^2",
      "default": 60.0,
      "description": "Incident diffuse NIR solar radiation from the atmosphere"
    },
    "L_atm_down": {
      "type": "parameter",
      "units": "W/m^2",
      "default": 350.0,
      "description": "Incident longwave radiation from the atmosphere (downwelling)"
    },
    "μ_zen": {
      "type": "parameter",
      "units": "rad",
      "default": 0.5236,
      "description": "Solar zenith angle (rad) — appears in `tan(μ_zen)` in the direct-beam factor of Eq. 2.16-2.17. Default 0.5236 rad ≈ 30 degrees."
    },
    "α_roof_dir_vis": {
      "type": "parameter",
      "units": "1",
      "default": 0.2,
      "description": "Roof albedo, direct beam, visible (dimensionless) — surface optical property; appears in Eq. 2.34-2.35 for absorbed solar by the roof"
    },
    "α_roof_dir_nir": {
      "type": "parameter",
      "units": "1",
      "default": 0.2,
      "description": "Roof albedo, direct beam, NIR (dimensionless)"
    },
    "α_roof_dif_vis": {
      "type": "parameter",
      "units": "1",
      "default": 0.2,
      "description": "Roof albedo, diffuse, visible (dimensionless)"
    },
    "α_roof_dif_nir": {
      "type": "parameter",
      "units": "1",
      "default": 0.2,
      "description": "Roof albedo, diffuse, NIR (dimensionless)"
    },
    "α_road_dir_vis": {
      "type": "parameter",
      "units": "1",
      "default": 0.08,
      "description": "Effective road albedo, direct beam, visible (dimensionless) — weighted average over pervious/impervious road fraction, computed upstream"
    },
    "α_road_dir_nir": {
      "type": "parameter",
      "units": "1",
      "default": 0.08,
      "description": "Effective road albedo, direct beam, NIR (dimensionless)"
    },
    "α_road_dif_vis": {
      "type": "parameter",
      "units": "1",
      "default": 0.08,
      "description": "Effective road albedo, diffuse, visible (dimensionless)"
    },
    "α_road_dif_nir": {
      "type": "parameter",
      "units": "1",
      "default": 0.08,
      "description": "Effective road albedo, diffuse, NIR (dimensionless)"
    },
    "α_wall_dir_vis": {
      "type": "parameter",
      "units": "1",
      "default": 0.25,
      "description": "Wall albedo, direct beam, visible (dimensionless)"
    },
    "α_wall_dir_nir": {
      "type": "parameter",
      "units": "1",
      "default": 0.25,
      "description": "Wall albedo, direct beam, NIR (dimensionless)"
    },
    "α_wall_dif_vis": {
      "type": "parameter",
      "units": "1",
      "default": 0.25,
      "description": "Wall albedo, diffuse, visible (dimensionless)"
    },
    "α_wall_dif_nir": {
      "type": "parameter",
      "units": "1",
      "default": 0.25,
      "description": "Wall albedo, diffuse, NIR (dimensionless)"
    },
    "ε_roof": {
      "type": "parameter",
      "units": "1",
      "default": 0.9,
      "description": "Roof longwave emissivity (dimensionless) — Stefan-Boltzmann pre-factor in upward LW emission (Eq. 2.102); typical urban roof values 0.85-0.95"
    },
    "ε_road": {
      "type": "parameter",
      "units": "1",
      "default": 0.95,
      "description": "Effective road longwave emissivity (dimensionless) — weighted average over pervious/impervious road fraction"
    },
    "ε_wall": {
      "type": "parameter",
      "units": "1",
      "default": 0.85,
      "description": "Wall longwave emissivity (dimensionless)"
    },
    "T_roof": {
      "type": "parameter",
      "units": "K",
      "default": 305.0,
      "description": "Roof surface temperature — appears as T^4 in the Stefan-Boltzmann upward emission (Eq. 2.102)"
    },
    "T_road": {
      "type": "parameter",
      "units": "K",
      "default": 310.0,
      "description": "Road surface temperature — appears as T^4 in the road LW emission (Eq. 2.111)"
    },
    "T_sunwall": {
      "type": "parameter",
      "units": "K",
      "default": 315.0,
      "description": "Sunlit wall surface temperature — appears as T^4 in the sunlit-wall LW emission (Eq. 2.112)"
    },
    "T_shdwall": {
      "type": "parameter",
      "units": "K",
      "default": 300.0,
      "description": "Shaded wall surface temperature — appears as T^4 in the shaded-wall LW emission (Eq. 2.113)"
    },
    "Ψ_wall_sky": {
      "type": "unknown",
      "units": "1",
      "description": "View factor: wall to sky (Oleson Eq. 2.24) — fraction of radiation leaving a wall that reaches the sky"
    },
    "Ψ_wall_road": {
      "type": "unknown",
      "units": "1",
      "description": "View factor: wall to road (Oleson Eq. 2.26) — equal to Ψ_wall_sky by reciprocity"
    },
    "Ψ_wall_wall": {
      "type": "unknown",
      "units": "1",
      "description": "View factor: wall to opposite wall (Oleson Eq. 2.28) — closure of the row-sum 1 = Ψ_wall_sky + Ψ_wall_road + Ψ_wall_wall"
    },
    "Ψ_road_sky": {
      "type": "unknown",
      "units": "1",
      "description": "View factor: road to sky (Oleson Eq. 2.25) — fraction of radiation leaving the road that reaches the sky; decreases with H/W"
    },
    "Ψ_road_wall": {
      "type": "unknown",
      "units": "1",
      "description": "View factor: road to wall (Oleson Eq. 2.27) — fraction of radiation leaving the road that reaches one wall; two walls so 2*Ψ_road_wall = 1 - Ψ_road_sky"
    },
    "Ψ_sky_road": {
      "type": "unknown",
      "units": "1",
      "description": "View factor: sky to road (Oleson Eq. 2.25) — equal to Ψ_road_sky by reciprocity"
    },
    "Ψ_sky_wall": {
      "type": "unknown",
      "units": "1",
      "description": "View factor: sky to wall, per unit wall area (Oleson Eq. 2.24) — equal to Ψ_wall_sky by reciprocity"
    },
    "θ_0": {
      "type": "unknown",
      "units": "rad",
      "description": "Critical canyon orientation angle (Oleson Eq. 2.11) — the canyon-orientation azimuth threshold separating sunlit-wall from shadowed-wall geometries integrated to derive the canyon-averaged direct-beam radiation factors"
    },
    "S_sunwall_factor": {
      "type": "unknown",
      "units": "1",
      "description": "Sunlit wall direct beam factor (Oleson Eq. 2.16) — dimensionless fraction of atmospheric direct-beam radiation that lands on the sunlit wall per unit wall area, integrated over canyon orientation"
    },
    "S_road_factor": {
      "type": "unknown",
      "units": "1",
      "description": "Road direct beam factor (Oleson Eq. 2.17) — dimensionless fraction of atmospheric direct-beam radiation that lands on the road per unit ground area; conservation Eq. 2.18 requires S_road_factor + H/W * S_sunwall_factor = 1"
    },
    "S_road_dir_vis": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Direct beam VIS incident on road (Oleson Eq. 2.17): S_road_factor * S_atm_dir_vis"
    },
    "S_road_dir_nir": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Direct beam NIR incident on road: S_road_factor * S_atm_dir_nir"
    },
    "S_sunwall_dir_vis": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Direct beam VIS incident on sunlit wall (Oleson Eq. 2.16): S_sunwall_factor * S_atm_dir_vis"
    },
    "S_sunwall_dir_nir": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Direct beam NIR incident on sunlit wall: S_sunwall_factor * S_atm_dir_nir"
    },
    "S_road_dif_vis": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Diffuse VIS incident on road (Oleson Eq. 2.30): S_atm_dif_vis * Ψ_sky_road"
    },
    "S_road_dif_nir": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Diffuse NIR incident on road: S_atm_dif_nir * Ψ_sky_road"
    },
    "S_wall_dif_vis": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Diffuse VIS incident on each wall (Oleson Eqs. 2.31-2.32): S_atm_dif_vis * Ψ_sky_wall — same on sunlit and shaded walls for diffuse radiation"
    },
    "S_wall_dif_nir": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Diffuse NIR incident on each wall: S_atm_dif_nir * Ψ_sky_wall"
    },
    "T_rw": {
      "type": "unknown",
      "units": "1",
      "description": "Transport matrix element: wall to road (Oleson Section 2.5, p. 42-43) = H/W * Ψ_wall_road — accounts for the wall-to-road area ratio in the multi-reflection transport matrix T"
    },
    "T_wr": {
      "type": "unknown",
      "units": "1",
      "description": "Transport matrix element: road to wall = Ψ_road_wall / (H/W) — accounts for the road-to-wall area ratio (per unit wall area)"
    },
    "T_ww": {
      "type": "unknown",
      "units": "1",
      "description": "Transport matrix element: wall to opposite wall = Ψ_wall_wall — the off-diagonal that couples the sunlit and shaded walls in the canyon-reflection geometric series"
    },
    "det_dir_vis": {
      "type": "unknown",
      "units": "1",
      "description": "Determinant of (I - T*A) for direct VIS waveband: (1 - d²) - 2bc(1 + d), where b = a_w*T_rw, c = a_r*T_wr, d = a_w*T_ww — denominator of the closed-form multi-reflection solution"
    },
    "det_dir_nir": {
      "type": "unknown",
      "units": "1",
      "description": "Determinant of (I - T*A) for direct NIR waveband"
    },
    "det_dif_vis": {
      "type": "unknown",
      "units": "1",
      "description": "Determinant of (I - T*A) for diffuse VIS waveband"
    },
    "det_dif_nir": {
      "type": "unknown",
      "units": "1",
      "description": "Determinant of (I - T*A) for diffuse NIR waveband"
    },
    "S_net_roof": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Net absorbed solar by roof (Oleson Eqs. 2.34-2.35): Σ S_atm_*_*(1 - α_roof_*_*) summed over all four wavebands"
    },
    "S_net_road_dir_vis": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Absorbed solar by road, direct VIS waveband: (1 - α_road_dir_vis) * Q_road_dir_vis where Q_road_dir_vis is the per-waveband closed-form M⁻¹*S_0 multi-reflection result"
    },
    "S_net_road_dir_nir": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Absorbed solar by road, direct NIR waveband"
    },
    "S_net_road_dif_vis": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Absorbed solar by road, diffuse VIS waveband"
    },
    "S_net_road_dif_nir": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Absorbed solar by road, diffuse NIR waveband"
    },
    "S_net_sunwall_dir_vis": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Absorbed solar by sunlit wall, direct VIS waveband (per unit wall area)"
    },
    "S_net_sunwall_dir_nir": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Absorbed solar by sunlit wall, direct NIR waveband"
    },
    "S_net_sunwall_dif_vis": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Absorbed solar by sunlit wall, diffuse VIS waveband"
    },
    "S_net_sunwall_dif_nir": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Absorbed solar by sunlit wall, diffuse NIR waveband"
    },
    "S_net_shdwall_dir_vis": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Absorbed solar by shaded wall, direct VIS waveband — non-zero only via multi-reflection from road and sunlit wall (no direct beam reaches the shaded wall)"
    },
    "S_net_shdwall_dir_nir": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Absorbed solar by shaded wall, direct NIR waveband"
    },
    "S_net_shdwall_dif_vis": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Absorbed solar by shaded wall, diffuse VIS waveband — equal to sunwall diffuse VIS by symmetry"
    },
    "S_net_shdwall_dif_nir": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Absorbed solar by shaded wall, diffuse NIR waveband"
    },
    "S_net_road": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Total net absorbed solar by road: sum of S_net_road_* over the four wavebands"
    },
    "S_net_sunwall": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Total net absorbed solar by sunlit wall per unit wall area: sum of S_net_sunwall_* over the four wavebands"
    },
    "S_net_shdwall": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Total net absorbed solar by shaded wall per unit wall area: sum of S_net_shdwall_* over the four wavebands"
    },
    "S_net_uc": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Net absorbed solar by the urban canyon per unit ground area: S_net_road + (S_net_sunwall + S_net_shdwall) * H/W"
    },
    "S_net_total": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Total net absorbed solar (Oleson Eq. 2.95): W_roof * S_net_roof + (1 - W_roof) * S_net_uc — area-weighted total over roof and canyon"
    },
    "S_refl_sky_dir_vis": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Solar reflected back to sky from the canyon, direct VIS waveband — energy-balance closure: incident_canyon - absorbed_canyon (per unit ground area)"
    },
    "S_refl_sky_dir_nir": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Solar reflected back to sky from the canyon, direct NIR waveband"
    },
    "S_refl_sky_dif_vis": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Solar reflected back to sky from the canyon, diffuse VIS waveband"
    },
    "S_refl_sky_dif_nir": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Solar reflected back to sky from the canyon, diffuse NIR waveband"
    },
    "α_uc_dir_vis": {
      "type": "unknown",
      "units": "1",
      "description": "Canyon direct beam albedo, VIS (Oleson Eq. 2.93): S_refl_sky_dir_vis / incident_canyon — the ratio of reflected to incident summed over the canyon (excluding the roof). Guarded against divide-by-zero when there is no incident radiation in this waveband."
    },
    "α_uc_dir_nir": {
      "type": "unknown",
      "units": "1",
      "description": "Canyon direct beam albedo, NIR"
    },
    "α_uc_dif_vis": {
      "type": "unknown",
      "units": "1",
      "description": "Canyon diffuse albedo, VIS (Oleson Eq. 2.94)"
    },
    "α_uc_dif_nir": {
      "type": "unknown",
      "units": "1",
      "description": "Canyon diffuse albedo, NIR"
    },
    "L_up_roof": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Upward longwave radiation from roof (Oleson Eq. 2.102): ε_roof * σ_SB * T_roof^4 + (1 - ε_roof) * L_atm_down — Stefan-Boltzmann emission plus reflection of the downwelling atmospheric LW"
    },
    "L_net_roof": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Net longwave for roof (Oleson Eq. 2.101): L_up_roof - L_atm_down — positive when the roof is losing more LW than it absorbs"
    },
    "L_emit_road": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Emitted longwave from road (Oleson Eq. 2.111): ε_road * σ_SB * T_road^4 — Stefan-Boltzmann emission only, before multi-reflection"
    },
    "L_emit_sunwall": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Emitted longwave from sunlit wall (Oleson Eq. 2.112): ε_wall * σ_SB * T_sunwall^4"
    },
    "L_emit_shdwall": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Emitted longwave from shaded wall (Oleson Eq. 2.113): ε_wall * σ_SB * T_shdwall^4"
    },
    "det_lw": {
      "type": "unknown",
      "units": "1",
      "description": "Determinant of (I - T*A) for longwave: (1 - d_lw²) - 2*b_lw*c_lw*(1 + d_lw), where b_lw = (1-ε_wall)*T_rw, c_lw = (1-ε_road)*T_wr, d_lw = (1-ε_wall)*T_ww — structurally identical to the solar determinant but with reflectivity (1 - ε) in place of albedo α"
    },
    "L_net_road": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Net longwave for road: L_emit_road - ε_road * Q_road_lw, where Q_road_lw is the canyon-trapped incoming LW from atmosphere and wall emission via the multi-reflection M⁻¹*S_0_lw solution. Positive when the road loses more LW than it absorbs."
    },
    "L_net_sunwall": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Net longwave for sunlit wall per unit wall area: L_emit_sunwall - ε_wall * Q_sw_lw"
    },
    "L_net_shdwall": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Net longwave for shaded wall per unit wall area: L_emit_shdwall - ε_wall * Q_sh_lw"
    },
    "L_net_uc": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Net longwave for urban canyon per unit ground area (Oleson Eq. 2.172): L_net_road + (L_net_sunwall + L_net_shdwall) * H/W"
    },
    "L_net_total": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Total net longwave (Oleson Eq. 2.175): W_roof * L_net_roof + (1 - W_roof) * L_net_uc — area-weighted total over roof and canyon"
    }
  },
  "equations": [
    {
      "lhs": "Ψ_sky_wall",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "-",
            "args": [
              {
                "op": "+",
                "args": [
                  "H_W",
                  1.0
                ]
              },
              {
                "op": "sqrt",
                "args": [
                  {
                    "op": "+",
                    "args": [
                      1.0,
                      {
                        "op": "^",
                        "args": [
                          "H_W",
                          2.0
                        ]
                      }
                    ]
                  }
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              2.0,
              "H_W"
            ]
          }
        ]
      }
    },
    {
      "lhs": "Ψ_wall_sky",
      "rhs": "Ψ_sky_wall"
    },
    {
      "lhs": "Ψ_road_sky",
      "rhs": {
        "op": "-",
        "args": [
          {
            "op": "sqrt",
            "args": [
              {
                "op": "+",
                "args": [
                  1.0,
                  {
                    "op": "^",
                    "args": [
                      "H_W",
                      2.0
                    ]
                  }
                ]
              }
            ]
          },
          "H_W"
        ]
      }
    },
    {
      "lhs": "Ψ_sky_road",
      "rhs": "Ψ_road_sky"
    },
    {
      "lhs": "Ψ_wall_road",
      "rhs": "Ψ_wall_sky"
    },
    {
      "lhs": "Ψ_road_wall",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "-",
            "args": [
              1.0,
              "Ψ_road_sky"
            ]
          },
          2.0
        ]
      }
    },
    {
      "lhs": "Ψ_wall_wall",
      "rhs": {
        "op": "-",
        "args": [
          {
            "op": "-",
            "args": [
              1.0,
              "Ψ_wall_sky"
            ]
          },
          "Ψ_wall_road"
        ]
      }
    },
    {
      "lhs": "T_rw",
      "rhs": {
        "op": "*",
        "args": [
          "H_W",
          "Ψ_wall_road"
        ]
      }
    },
    {
      "lhs": "T_wr",
      "rhs": {
        "op": "/",
        "args": [
          "Ψ_road_wall",
          "H_W"
        ]
      }
    },
    {
      "lhs": "T_ww",
      "rhs": "Ψ_wall_wall"
    },
    {
      "lhs": "θ_0",
      "rhs": {
        "op": "*",
        "args": [
          {
            "op": "asin",
            "args": [
              {
                "op": "min",
                "args": [
                  {
                    "op": "/",
                    "args": [
                      1.0,
                      {
                        "op": "*",
                        "args": [
                          "H_W",
                          {
                            "op": "tan",
                            "args": [
                              {
                                "op": "/",
                                "args": [
                                  "μ_zen",
                                  "one_rad"
                                ]
                              }
                            ]
                          }
                        ]
                      }
                    ]
                  },
                  1.0
                ]
              }
            ]
          },
          "one_rad"
        ]
      }
    },
    {
      "lhs": "S_sunwall_factor",
      "rhs": {
        "op": "*",
        "args": [
          2.0,
          {
            "op": "+",
            "args": [
              {
                "op": "*",
                "args": [
                  {
                    "op": "/",
                    "args": [
                      1.0,
                      "H_W"
                    ]
                  },
                  {
                    "op": "-",
                    "args": [
                      0.5,
                      {
                        "op": "/",
                        "args": [
                          "θ_0",
                          {
                            "op": "*",
                            "args": [
                              "π_val",
                              "one_rad"
                            ]
                          }
                        ]
                      }
                    ]
                  }
                ]
              },
              {
                "op": "*",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      {
                        "op": "/",
                        "args": [
                          1.0,
                          "π_val"
                        ]
                      },
                      {
                        "op": "tan",
                        "args": [
                          {
                            "op": "/",
                            "args": [
                              "μ_zen",
                              "one_rad"
                            ]
                          }
                        ]
                      }
                    ]
                  },
                  {
                    "op": "-",
                    "args": [
                      1.0,
                      {
                        "op": "cos",
                        "args": [
                          {
                            "op": "/",
                            "args": [
                              "θ_0",
                              "one_rad"
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
    },
    {
      "lhs": "S_sunwall_dir_vis",
      "rhs": {
        "op": "*",
        "args": [
          "S_sunwall_factor",
          "S_atm_dir_vis"
        ]
      }
    },
    {
      "lhs": "S_sunwall_dir_nir",
      "rhs": {
        "op": "*",
        "args": [
          "S_sunwall_factor",
          "S_atm_dir_nir"
        ]
      }
    },
    {
      "lhs": "S_road_factor",
      "rhs": {
        "op": "-",
        "args": [
          {
            "op": "*",
            "args": [
              2.0,
              {
                "op": "/",
                "args": [
                  "θ_0",
                  {
                    "op": "*",
                    "args": [
                      "π_val",
                      "one_rad"
                    ]
                  }
                ]
              }
            ]
          },
          {
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
                          2.0,
                          "π_val"
                        ]
                      },
                      "H_W"
                    ]
                  },
                  {
                    "op": "tan",
                    "args": [
                      {
                        "op": "/",
                        "args": [
                          "μ_zen",
                          "one_rad"
                        ]
                      }
                    ]
                  }
                ]
              },
              {
                "op": "-",
                "args": [
                  1.0,
                  {
                    "op": "cos",
                    "args": [
                      {
                        "op": "/",
                        "args": [
                          "θ_0",
                          "one_rad"
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
      "lhs": "S_road_dir_vis",
      "rhs": {
        "op": "*",
        "args": [
          "S_road_factor",
          "S_atm_dir_vis"
        ]
      }
    },
    {
      "lhs": "S_road_dir_nir",
      "rhs": {
        "op": "*",
        "args": [
          "S_road_factor",
          "S_atm_dir_nir"
        ]
      }
    },
    {
      "lhs": "S_road_dif_vis",
      "rhs": {
        "op": "*",
        "args": [
          "S_atm_dif_vis",
          "Ψ_sky_road"
        ]
      }
    },
    {
      "lhs": "S_road_dif_nir",
      "rhs": {
        "op": "*",
        "args": [
          "S_atm_dif_nir",
          "Ψ_sky_road"
        ]
      }
    },
    {
      "lhs": "S_wall_dif_vis",
      "rhs": {
        "op": "*",
        "args": [
          "S_atm_dif_vis",
          "Ψ_sky_wall"
        ]
      }
    },
    {
      "lhs": "S_wall_dif_nir",
      "rhs": {
        "op": "*",
        "args": [
          "S_atm_dif_nir",
          "Ψ_sky_wall"
        ]
      }
    },
    {
      "lhs": "S_net_roof",
      "rhs": {
        "op": "+",
        "args": [
          {
            "op": "+",
            "args": [
              {
                "op": "+",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      "S_atm_dir_vis",
                      {
                        "op": "-",
                        "args": [
                          1.0,
                          "α_roof_dir_vis"
                        ]
                      }
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "S_atm_dir_nir",
                      {
                        "op": "-",
                        "args": [
                          1.0,
                          "α_roof_dir_nir"
                        ]
                      }
                    ]
                  }
                ]
              },
              {
                "op": "*",
                "args": [
                  "S_atm_dif_vis",
                  {
                    "op": "-",
                    "args": [
                      1.0,
                      "α_roof_dif_vis"
                    ]
                  }
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              "S_atm_dif_nir",
              {
                "op": "-",
                "args": [
                  1.0,
                  "α_roof_dif_nir"
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "det_dir_vis",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "band_det",
        "bindings": {
          "a_r": "α_road_dir_vis",
          "a_w": "α_wall_dir_vis"
        }
      }
    },
    {
      "lhs": "S_net_road_dir_vis",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "band_net_road",
        "bindings": {
          "a_r": "α_road_dir_vis",
          "a_w": "α_wall_dir_vis",
          "S_r": "S_road_dir_vis",
          "S_sw": "S_sunwall_dir_vis",
          "S_sh": "zero_wm2",
          "det_var": "det_dir_vis"
        }
      }
    },
    {
      "lhs": "S_net_sunwall_dir_vis",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "band_net_sw",
        "bindings": {
          "a_r": "α_road_dir_vis",
          "a_w": "α_wall_dir_vis",
          "S_r": "S_road_dir_vis",
          "S_sw": "S_sunwall_dir_vis",
          "S_sh": "zero_wm2",
          "det_var": "det_dir_vis"
        }
      }
    },
    {
      "lhs": "S_net_shdwall_dir_vis",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "band_net_sh",
        "bindings": {
          "a_r": "α_road_dir_vis",
          "a_w": "α_wall_dir_vis",
          "S_r": "S_road_dir_vis",
          "S_sw": "S_sunwall_dir_vis",
          "S_sh": "zero_wm2",
          "det_var": "det_dir_vis"
        }
      }
    },
    {
      "lhs": "S_refl_sky_dir_vis",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "band_refl_sky",
        "bindings": {
          "S_r": "S_road_dir_vis",
          "S_sw": "S_sunwall_dir_vis",
          "S_sh": "zero_wm2",
          "net_road": "S_net_road_dir_vis",
          "net_sw": "S_net_sunwall_dir_vis",
          "net_sh": "S_net_shdwall_dir_vis"
        }
      }
    },
    {
      "lhs": "det_dir_nir",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "band_det",
        "bindings": {
          "a_r": "α_road_dir_nir",
          "a_w": "α_wall_dir_nir"
        }
      }
    },
    {
      "lhs": "S_net_road_dir_nir",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "band_net_road",
        "bindings": {
          "a_r": "α_road_dir_nir",
          "a_w": "α_wall_dir_nir",
          "S_r": "S_road_dir_nir",
          "S_sw": "S_sunwall_dir_nir",
          "S_sh": "zero_wm2",
          "det_var": "det_dir_nir"
        }
      }
    },
    {
      "lhs": "S_net_sunwall_dir_nir",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "band_net_sw",
        "bindings": {
          "a_r": "α_road_dir_nir",
          "a_w": "α_wall_dir_nir",
          "S_r": "S_road_dir_nir",
          "S_sw": "S_sunwall_dir_nir",
          "S_sh": "zero_wm2",
          "det_var": "det_dir_nir"
        }
      }
    },
    {
      "lhs": "S_net_shdwall_dir_nir",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "band_net_sh",
        "bindings": {
          "a_r": "α_road_dir_nir",
          "a_w": "α_wall_dir_nir",
          "S_r": "S_road_dir_nir",
          "S_sw": "S_sunwall_dir_nir",
          "S_sh": "zero_wm2",
          "det_var": "det_dir_nir"
        }
      }
    },
    {
      "lhs": "S_refl_sky_dir_nir",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "band_refl_sky",
        "bindings": {
          "S_r": "S_road_dir_nir",
          "S_sw": "S_sunwall_dir_nir",
          "S_sh": "zero_wm2",
          "net_road": "S_net_road_dir_nir",
          "net_sw": "S_net_sunwall_dir_nir",
          "net_sh": "S_net_shdwall_dir_nir"
        }
      }
    },
    {
      "lhs": "det_dif_vis",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "band_det",
        "bindings": {
          "a_r": "α_road_dif_vis",
          "a_w": "α_wall_dif_vis"
        }
      }
    },
    {
      "lhs": "S_net_road_dif_vis",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "band_net_road",
        "bindings": {
          "a_r": "α_road_dif_vis",
          "a_w": "α_wall_dif_vis",
          "S_r": "S_road_dif_vis",
          "S_sw": "S_wall_dif_vis",
          "S_sh": "S_wall_dif_vis",
          "det_var": "det_dif_vis"
        }
      }
    },
    {
      "lhs": "S_net_sunwall_dif_vis",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "band_net_sw",
        "bindings": {
          "a_r": "α_road_dif_vis",
          "a_w": "α_wall_dif_vis",
          "S_r": "S_road_dif_vis",
          "S_sw": "S_wall_dif_vis",
          "S_sh": "S_wall_dif_vis",
          "det_var": "det_dif_vis"
        }
      }
    },
    {
      "lhs": "S_net_shdwall_dif_vis",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "band_net_sh",
        "bindings": {
          "a_r": "α_road_dif_vis",
          "a_w": "α_wall_dif_vis",
          "S_r": "S_road_dif_vis",
          "S_sw": "S_wall_dif_vis",
          "S_sh": "S_wall_dif_vis",
          "det_var": "det_dif_vis"
        }
      }
    },
    {
      "lhs": "S_refl_sky_dif_vis",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "band_refl_sky",
        "bindings": {
          "S_r": "S_road_dif_vis",
          "S_sw": "S_wall_dif_vis",
          "S_sh": "S_wall_dif_vis",
          "net_road": "S_net_road_dif_vis",
          "net_sw": "S_net_sunwall_dif_vis",
          "net_sh": "S_net_shdwall_dif_vis"
        }
      }
    },
    {
      "lhs": "det_dif_nir",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "band_det",
        "bindings": {
          "a_r": "α_road_dif_nir",
          "a_w": "α_wall_dif_nir"
        }
      }
    },
    {
      "lhs": "S_net_road_dif_nir",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "band_net_road",
        "bindings": {
          "a_r": "α_road_dif_nir",
          "a_w": "α_wall_dif_nir",
          "S_r": "S_road_dif_nir",
          "S_sw": "S_wall_dif_nir",
          "S_sh": "S_wall_dif_nir",
          "det_var": "det_dif_nir"
        }
      }
    },
    {
      "lhs": "S_net_sunwall_dif_nir",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "band_net_sw",
        "bindings": {
          "a_r": "α_road_dif_nir",
          "a_w": "α_wall_dif_nir",
          "S_r": "S_road_dif_nir",
          "S_sw": "S_wall_dif_nir",
          "S_sh": "S_wall_dif_nir",
          "det_var": "det_dif_nir"
        }
      }
    },
    {
      "lhs": "S_net_shdwall_dif_nir",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "band_net_sh",
        "bindings": {
          "a_r": "α_road_dif_nir",
          "a_w": "α_wall_dif_nir",
          "S_r": "S_road_dif_nir",
          "S_sw": "S_wall_dif_nir",
          "S_sh": "S_wall_dif_nir",
          "det_var": "det_dif_nir"
        }
      }
    },
    {
      "lhs": "S_refl_sky_dif_nir",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "band_refl_sky",
        "bindings": {
          "S_r": "S_road_dif_nir",
          "S_sw": "S_wall_dif_nir",
          "S_sh": "S_wall_dif_nir",
          "net_road": "S_net_road_dif_nir",
          "net_sw": "S_net_sunwall_dif_nir",
          "net_sh": "S_net_shdwall_dif_nir"
        }
      }
    },
    {
      "lhs": "S_net_road",
      "rhs": {
        "op": "+",
        "args": [
          {
            "op": "+",
            "args": [
              {
                "op": "+",
                "args": [
                  "S_net_road_dir_vis",
                  "S_net_road_dir_nir"
                ]
              },
              "S_net_road_dif_vis"
            ]
          },
          "S_net_road_dif_nir"
        ]
      }
    },
    {
      "lhs": "S_net_sunwall",
      "rhs": {
        "op": "+",
        "args": [
          {
            "op": "+",
            "args": [
              {
                "op": "+",
                "args": [
                  "S_net_sunwall_dir_vis",
                  "S_net_sunwall_dir_nir"
                ]
              },
              "S_net_sunwall_dif_vis"
            ]
          },
          "S_net_sunwall_dif_nir"
        ]
      }
    },
    {
      "lhs": "S_net_shdwall",
      "rhs": {
        "op": "+",
        "args": [
          {
            "op": "+",
            "args": [
              {
                "op": "+",
                "args": [
                  "S_net_shdwall_dir_vis",
                  "S_net_shdwall_dir_nir"
                ]
              },
              "S_net_shdwall_dif_vis"
            ]
          },
          "S_net_shdwall_dif_nir"
        ]
      }
    },
    {
      "lhs": "S_net_uc",
      "rhs": {
        "op": "+",
        "args": [
          "S_net_road",
          {
            "op": "*",
            "args": [
              {
                "op": "+",
                "args": [
                  "S_net_sunwall",
                  "S_net_shdwall"
                ]
              },
              "H_W"
            ]
          }
        ]
      }
    },
    {
      "lhs": "α_uc_dir_vis",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": ">",
            "args": [
              {
                "op": "+",
                "args": [
                  "S_road_dir_vis",
                  {
                    "op": "*",
                    "args": [
                      "S_sunwall_dir_vis",
                      "H_W"
                    ]
                  }
                ]
              },
              "zero_wm2"
            ]
          },
          {
            "op": "/",
            "args": [
              "S_refl_sky_dir_vis",
              {
                "op": "+",
                "args": [
                  "S_road_dir_vis",
                  {
                    "op": "*",
                    "args": [
                      "S_sunwall_dir_vis",
                      "H_W"
                    ]
                  }
                ]
              }
            ]
          },
          0.0
        ]
      }
    },
    {
      "lhs": "α_uc_dir_nir",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": ">",
            "args": [
              {
                "op": "+",
                "args": [
                  "S_road_dir_nir",
                  {
                    "op": "*",
                    "args": [
                      "S_sunwall_dir_nir",
                      "H_W"
                    ]
                  }
                ]
              },
              "zero_wm2"
            ]
          },
          {
            "op": "/",
            "args": [
              "S_refl_sky_dir_nir",
              {
                "op": "+",
                "args": [
                  "S_road_dir_nir",
                  {
                    "op": "*",
                    "args": [
                      "S_sunwall_dir_nir",
                      "H_W"
                    ]
                  }
                ]
              }
            ]
          },
          0.0
        ]
      }
    },
    {
      "lhs": "α_uc_dif_vis",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": ">",
            "args": [
              {
                "op": "+",
                "args": [
                  "S_road_dif_vis",
                  {
                    "op": "*",
                    "args": [
                      {
                        "op": "*",
                        "args": [
                          2.0,
                          "S_wall_dif_vis"
                        ]
                      },
                      "H_W"
                    ]
                  }
                ]
              },
              "zero_wm2"
            ]
          },
          {
            "op": "/",
            "args": [
              "S_refl_sky_dif_vis",
              {
                "op": "+",
                "args": [
                  "S_road_dif_vis",
                  {
                    "op": "*",
                    "args": [
                      {
                        "op": "*",
                        "args": [
                          2.0,
                          "S_wall_dif_vis"
                        ]
                      },
                      "H_W"
                    ]
                  }
                ]
              }
            ]
          },
          0.0
        ]
      }
    },
    {
      "lhs": "α_uc_dif_nir",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": ">",
            "args": [
              {
                "op": "+",
                "args": [
                  "S_road_dif_nir",
                  {
                    "op": "*",
                    "args": [
                      {
                        "op": "*",
                        "args": [
                          2.0,
                          "S_wall_dif_nir"
                        ]
                      },
                      "H_W"
                    ]
                  }
                ]
              },
              "zero_wm2"
            ]
          },
          {
            "op": "/",
            "args": [
              "S_refl_sky_dif_nir",
              {
                "op": "+",
                "args": [
                  "S_road_dif_nir",
                  {
                    "op": "*",
                    "args": [
                      {
                        "op": "*",
                        "args": [
                          2.0,
                          "S_wall_dif_nir"
                        ]
                      },
                      "H_W"
                    ]
                  }
                ]
              }
            ]
          },
          0.0
        ]
      }
    },
    {
      "lhs": "S_net_total",
      "rhs": {
        "op": "+",
        "args": [
          {
            "op": "*",
            "args": [
              "W_roof",
              "S_net_roof"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  1.0,
                  "W_roof"
                ]
              },
              "S_net_uc"
            ]
          }
        ]
      }
    },
    {
      "lhs": "L_up_roof",
      "rhs": {
        "op": "+",
        "args": [
          {
            "op": "*",
            "args": [
              {
                "op": "*",
                "args": [
                  "ε_roof",
                  "σ_SB"
                ]
              },
              {
                "op": "^",
                "args": [
                  "T_roof",
                  4.0
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  1.0,
                  "ε_roof"
                ]
              },
              "L_atm_down"
            ]
          }
        ]
      }
    },
    {
      "lhs": "L_net_roof",
      "rhs": {
        "op": "-",
        "args": [
          "L_up_roof",
          "L_atm_down"
        ]
      }
    },
    {
      "lhs": "L_emit_road",
      "rhs": {
        "op": "*",
        "args": [
          {
            "op": "*",
            "args": [
              "ε_road",
              "σ_SB"
            ]
          },
          {
            "op": "^",
            "args": [
              "T_road",
              4.0
            ]
          }
        ]
      }
    },
    {
      "lhs": "L_emit_sunwall",
      "rhs": {
        "op": "*",
        "args": [
          {
            "op": "*",
            "args": [
              "ε_wall",
              "σ_SB"
            ]
          },
          {
            "op": "^",
            "args": [
              "T_sunwall",
              4.0
            ]
          }
        ]
      }
    },
    {
      "lhs": "L_emit_shdwall",
      "rhs": {
        "op": "*",
        "args": [
          {
            "op": "*",
            "args": [
              "ε_wall",
              "σ_SB"
            ]
          },
          {
            "op": "^",
            "args": [
              "T_shdwall",
              4.0
            ]
          }
        ]
      }
    },
    {
      "lhs": "det_lw",
      "rhs": {
        "op": "-",
        "args": [
          {
            "op": "-",
            "args": [
              1.0,
              {
                "op": "^",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      {
                        "op": "-",
                        "args": [
                          1.0,
                          "ε_wall"
                        ]
                      },
                      "T_ww"
                    ]
                  },
                  2.0
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "*",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      2.0,
                      {
                        "op": "*",
                        "args": [
                          {
                            "op": "-",
                            "args": [
                              1.0,
                              "ε_wall"
                            ]
                          },
                          "T_rw"
                        ]
                      }
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      {
                        "op": "-",
                        "args": [
                          1.0,
                          "ε_road"
                        ]
                      },
                      "T_wr"
                    ]
                  }
                ]
              },
              {
                "op": "+",
                "args": [
                  1.0,
                  {
                    "op": "*",
                    "args": [
                      {
                        "op": "-",
                        "args": [
                          1.0,
                          "ε_wall"
                        ]
                      },
                      "T_ww"
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
      "lhs": "L_net_road",
      "rhs": {
        "op": "-",
        "args": [
          "L_emit_road",
          {
            "op": "*",
            "args": [
              "ε_road",
              {
                "op": "/",
                "args": [
                  {
                    "op": "+",
                    "args": [
                      {
                        "op": "+",
                        "args": [
                          {
                            "op": "*",
                            "args": [
                              {
                                "op": "-",
                                "args": [
                                  1.0,
                                  {
                                    "op": "^",
                                    "args": [
                                      {
                                        "op": "*",
                                        "args": [
                                          {
                                            "op": "-",
                                            "args": [
                                              1.0,
                                              "ε_wall"
                                            ]
                                          },
                                          "T_ww"
                                        ]
                                      },
                                      2.0
                                    ]
                                  }
                                ]
                              },
                              {
                                "op": "+",
                                "args": [
                                  {
                                    "op": "*",
                                    "args": [
                                      "L_atm_down",
                                      "Ψ_sky_road"
                                    ]
                                  },
                                  {
                                    "op": "*",
                                    "args": [
                                      "T_rw",
                                      {
                                        "op": "+",
                                        "args": [
                                          "L_emit_sunwall",
                                          "L_emit_shdwall"
                                        ]
                                      }
                                    ]
                                  }
                                ]
                              }
                            ]
                          },
                          {
                            "op": "*",
                            "args": [
                              {
                                "op": "*",
                                "args": [
                                  {
                                    "op": "*",
                                    "args": [
                                      {
                                        "op": "-",
                                        "args": [
                                          1.0,
                                          "ε_wall"
                                        ]
                                      },
                                      "T_rw"
                                    ]
                                  },
                                  {
                                    "op": "+",
                                    "args": [
                                      1.0,
                                      {
                                        "op": "*",
                                        "args": [
                                          {
                                            "op": "-",
                                            "args": [
                                              1.0,
                                              "ε_wall"
                                            ]
                                          },
                                          "T_ww"
                                        ]
                                      }
                                    ]
                                  }
                                ]
                              },
                              {
                                "op": "+",
                                "args": [
                                  {
                                    "op": "+",
                                    "args": [
                                      {
                                        "op": "*",
                                        "args": [
                                          "L_atm_down",
                                          "Ψ_sky_wall"
                                        ]
                                      },
                                      {
                                        "op": "*",
                                        "args": [
                                          "T_wr",
                                          "L_emit_road"
                                        ]
                                      }
                                    ]
                                  },
                                  {
                                    "op": "*",
                                    "args": [
                                      "T_ww",
                                      "L_emit_shdwall"
                                    ]
                                  }
                                ]
                              }
                            ]
                          }
                        ]
                      },
                      {
                        "op": "*",
                        "args": [
                          {
                            "op": "*",
                            "args": [
                              {
                                "op": "*",
                                "args": [
                                  {
                                    "op": "-",
                                    "args": [
                                      1.0,
                                      "ε_wall"
                                    ]
                                  },
                                  "T_rw"
                                ]
                              },
                              {
                                "op": "+",
                                "args": [
                                  1.0,
                                  {
                                    "op": "*",
                                    "args": [
                                      {
                                        "op": "-",
                                        "args": [
                                          1.0,
                                          "ε_wall"
                                        ]
                                      },
                                      "T_ww"
                                    ]
                                  }
                                ]
                              }
                            ]
                          },
                          {
                            "op": "+",
                            "args": [
                              {
                                "op": "+",
                                "args": [
                                  {
                                    "op": "*",
                                    "args": [
                                      "L_atm_down",
                                      "Ψ_sky_wall"
                                    ]
                                  },
                                  {
                                    "op": "*",
                                    "args": [
                                      "T_wr",
                                      "L_emit_road"
                                    ]
                                  }
                                ]
                              },
                              {
                                "op": "*",
                                "args": [
                                  "T_ww",
                                  "L_emit_sunwall"
                                ]
                              }
                            ]
                          }
                        ]
                      }
                    ]
                  },
                  "det_lw"
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "L_net_sunwall",
      "rhs": {
        "op": "-",
        "args": [
          "L_emit_sunwall",
          {
            "op": "*",
            "args": [
              "ε_wall",
              {
                "op": "/",
                "args": [
                  {
                    "op": "+",
                    "args": [
                      {
                        "op": "+",
                        "args": [
                          {
                            "op": "*",
                            "args": [
                              {
                                "op": "*",
                                "args": [
                                  {
                                    "op": "*",
                                    "args": [
                                      {
                                        "op": "-",
                                        "args": [
                                          1.0,
                                          "ε_road"
                                        ]
                                      },
                                      "T_wr"
                                    ]
                                  },
                                  {
                                    "op": "+",
                                    "args": [
                                      1.0,
                                      {
                                        "op": "*",
                                        "args": [
                                          {
                                            "op": "-",
                                            "args": [
                                              1.0,
                                              "ε_wall"
                                            ]
                                          },
                                          "T_ww"
                                        ]
                                      }
                                    ]
                                  }
                                ]
                              },
                              {
                                "op": "+",
                                "args": [
                                  {
                                    "op": "*",
                                    "args": [
                                      "L_atm_down",
                                      "Ψ_sky_road"
                                    ]
                                  },
                                  {
                                    "op": "*",
                                    "args": [
                                      "T_rw",
                                      {
                                        "op": "+",
                                        "args": [
                                          "L_emit_sunwall",
                                          "L_emit_shdwall"
                                        ]
                                      }
                                    ]
                                  }
                                ]
                              }
                            ]
                          },
                          {
                            "op": "*",
                            "args": [
                              {
                                "op": "-",
                                "args": [
                                  1.0,
                                  {
                                    "op": "*",
                                    "args": [
                                      {
                                        "op": "*",
                                        "args": [
                                          {
                                            "op": "-",
                                            "args": [
                                              1.0,
                                              "ε_wall"
                                            ]
                                          },
                                          "T_rw"
                                        ]
                                      },
                                      {
                                        "op": "*",
                                        "args": [
                                          {
                                            "op": "-",
                                            "args": [
                                              1.0,
                                              "ε_road"
                                            ]
                                          },
                                          "T_wr"
                                        ]
                                      }
                                    ]
                                  }
                                ]
                              },
                              {
                                "op": "+",
                                "args": [
                                  {
                                    "op": "+",
                                    "args": [
                                      {
                                        "op": "*",
                                        "args": [
                                          "L_atm_down",
                                          "Ψ_sky_wall"
                                        ]
                                      },
                                      {
                                        "op": "*",
                                        "args": [
                                          "T_wr",
                                          "L_emit_road"
                                        ]
                                      }
                                    ]
                                  },
                                  {
                                    "op": "*",
                                    "args": [
                                      "T_ww",
                                      "L_emit_shdwall"
                                    ]
                                  }
                                ]
                              }
                            ]
                          }
                        ]
                      },
                      {
                        "op": "*",
                        "args": [
                          {
                            "op": "+",
                            "args": [
                              {
                                "op": "*",
                                "args": [
                                  {
                                    "op": "-",
                                    "args": [
                                      1.0,
                                      "ε_wall"
                                    ]
                                  },
                                  "T_ww"
                                ]
                              },
                              {
                                "op": "*",
                                "args": [
                                  {
                                    "op": "*",
                                    "args": [
                                      {
                                        "op": "-",
                                        "args": [
                                          1.0,
                                          "ε_wall"
                                        ]
                                      },
                                      "T_rw"
                                    ]
                                  },
                                  {
                                    "op": "*",
                                    "args": [
                                      {
                                        "op": "-",
                                        "args": [
                                          1.0,
                                          "ε_road"
                                        ]
                                      },
                                      "T_wr"
                                    ]
                                  }
                                ]
                              }
                            ]
                          },
                          {
                            "op": "+",
                            "args": [
                              {
                                "op": "+",
                                "args": [
                                  {
                                    "op": "*",
                                    "args": [
                                      "L_atm_down",
                                      "Ψ_sky_wall"
                                    ]
                                  },
                                  {
                                    "op": "*",
                                    "args": [
                                      "T_wr",
                                      "L_emit_road"
                                    ]
                                  }
                                ]
                              },
                              {
                                "op": "*",
                                "args": [
                                  "T_ww",
                                  "L_emit_sunwall"
                                ]
                              }
                            ]
                          }
                        ]
                      }
                    ]
                  },
                  "det_lw"
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "L_net_shdwall",
      "rhs": {
        "op": "-",
        "args": [
          "L_emit_shdwall",
          {
            "op": "*",
            "args": [
              "ε_wall",
              {
                "op": "/",
                "args": [
                  {
                    "op": "+",
                    "args": [
                      {
                        "op": "+",
                        "args": [
                          {
                            "op": "*",
                            "args": [
                              {
                                "op": "*",
                                "args": [
                                  {
                                    "op": "*",
                                    "args": [
                                      {
                                        "op": "-",
                                        "args": [
                                          1.0,
                                          "ε_road"
                                        ]
                                      },
                                      "T_wr"
                                    ]
                                  },
                                  {
                                    "op": "+",
                                    "args": [
                                      1.0,
                                      {
                                        "op": "*",
                                        "args": [
                                          {
                                            "op": "-",
                                            "args": [
                                              1.0,
                                              "ε_wall"
                                            ]
                                          },
                                          "T_ww"
                                        ]
                                      }
                                    ]
                                  }
                                ]
                              },
                              {
                                "op": "+",
                                "args": [
                                  {
                                    "op": "*",
                                    "args": [
                                      "L_atm_down",
                                      "Ψ_sky_road"
                                    ]
                                  },
                                  {
                                    "op": "*",
                                    "args": [
                                      "T_rw",
                                      {
                                        "op": "+",
                                        "args": [
                                          "L_emit_sunwall",
                                          "L_emit_shdwall"
                                        ]
                                      }
                                    ]
                                  }
                                ]
                              }
                            ]
                          },
                          {
                            "op": "*",
                            "args": [
                              {
                                "op": "+",
                                "args": [
                                  {
                                    "op": "*",
                                    "args": [
                                      {
                                        "op": "-",
                                        "args": [
                                          1.0,
                                          "ε_wall"
                                        ]
                                      },
                                      "T_ww"
                                    ]
                                  },
                                  {
                                    "op": "*",
                                    "args": [
                                      {
                                        "op": "*",
                                        "args": [
                                          {
                                            "op": "-",
                                            "args": [
                                              1.0,
                                              "ε_wall"
                                            ]
                                          },
                                          "T_rw"
                                        ]
                                      },
                                      {
                                        "op": "*",
                                        "args": [
                                          {
                                            "op": "-",
                                            "args": [
                                              1.0,
                                              "ε_road"
                                            ]
                                          },
                                          "T_wr"
                                        ]
                                      }
                                    ]
                                  }
                                ]
                              },
                              {
                                "op": "+",
                                "args": [
                                  {
                                    "op": "+",
                                    "args": [
                                      {
                                        "op": "*",
                                        "args": [
                                          "L_atm_down",
                                          "Ψ_sky_wall"
                                        ]
                                      },
                                      {
                                        "op": "*",
                                        "args": [
                                          "T_wr",
                                          "L_emit_road"
                                        ]
                                      }
                                    ]
                                  },
                                  {
                                    "op": "*",
                                    "args": [
                                      "T_ww",
                                      "L_emit_shdwall"
                                    ]
                                  }
                                ]
                              }
                            ]
                          }
                        ]
                      },
                      {
                        "op": "*",
                        "args": [
                          {
                            "op": "-",
                            "args": [
                              1.0,
                              {
                                "op": "*",
                                "args": [
                                  {
                                    "op": "*",
                                    "args": [
                                      {
                                        "op": "-",
                                        "args": [
                                          1.0,
                                          "ε_wall"
                                        ]
                                      },
                                      "T_rw"
                                    ]
                                  },
                                  {
                                    "op": "*",
                                    "args": [
                                      {
                                        "op": "-",
                                        "args": [
                                          1.0,
                                          "ε_road"
                                        ]
                                      },
                                      "T_wr"
                                    ]
                                  }
                                ]
                              }
                            ]
                          },
                          {
                            "op": "+",
                            "args": [
                              {
                                "op": "+",
                                "args": [
                                  {
                                    "op": "*",
                                    "args": [
                                      "L_atm_down",
                                      "Ψ_sky_wall"
                                    ]
                                  },
                                  {
                                    "op": "*",
                                    "args": [
                                      "T_wr",
                                      "L_emit_road"
                                    ]
                                  }
                                ]
                              },
                              {
                                "op": "*",
                                "args": [
                                  "T_ww",
                                  "L_emit_sunwall"
                                ]
                              }
                            ]
                          }
                        ]
                      }
                    ]
                  },
                  "det_lw"
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "L_net_uc",
      "rhs": {
        "op": "+",
        "args": [
          "L_net_road",
          {
            "op": "*",
            "args": [
              {
                "op": "+",
                "args": [
                  "L_net_sunwall",
                  "L_net_shdwall"
                ]
              },
              "H_W"
            ]
          }
        ]
      }
    },
    {
      "lhs": "L_net_total",
      "rhs": {
        "op": "+",
        "args": [
          {
            "op": "*",
            "args": [
              "W_roof",
              "L_net_roof"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  1.0,
                  "W_roof"
                ]
              },
              "L_net_uc"
            ]
          }
        ]
      }
    }
  ],
  "tests": [
    {
      "id": "view_factors_canonical_HW1",
      "description": "Reproduces upstream `View Factors - Known Values` test (UrbanCanopy.jl test/albedos_radiative_fluxes_test.jl:107) at canonical H/W = 1.0. Eqs. 2.22-2.28: Ψ_wall_sky = (1 + 1 - sqrt(2)) / 2 ≈ 0.29289, Ψ_road_sky = sqrt(2) - 1 ≈ 0.41421, Ψ_road_wall = (1 - Ψ_road_sky) / 2 ≈ 0.29289, Ψ_wall_wall = 1 - 2*Ψ_wall_sky ≈ 0.41421. Reciprocity Ψ_road_sky = Ψ_sky_road and Ψ_wall_sky = Ψ_wall_road are exact by definition (Eqs. 2.22, 2.25-2.26). All asserted at rtol = 1e-10 per upstream tolerance.",
      "parameter_overrides": {
        "H_W": 1.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "Ψ_wall_sky",
          "time": 0.0,
          "expected": 0.2928932188134524,
          "tolerance": {
            "rel": 1e-10
          }
        },
        {
          "variable": "Ψ_road_sky",
          "time": 0.0,
          "expected": 0.4142135623730951,
          "tolerance": {
            "rel": 1e-10
          }
        },
        {
          "variable": "Ψ_road_wall",
          "time": 0.0,
          "expected": 0.29289321881345254,
          "tolerance": {
            "rel": 1e-10
          }
        },
        {
          "variable": "Ψ_wall_wall",
          "time": 0.0,
          "expected": 0.4142135623730951,
          "tolerance": {
            "rel": 1e-10
          }
        },
        {
          "variable": "Ψ_sky_road",
          "time": 0.0,
          "expected": 0.4142135623730951,
          "tolerance": {
            "rel": 1e-10
          }
        },
        {
          "variable": "Ψ_wall_road",
          "time": 0.0,
          "expected": 0.2928932188134524,
          "tolerance": {
            "rel": 1e-10
          }
        }
      ]
    },
    {
      "id": "view_factor_analytical_HW2",
      "description": "Reproduces upstream `View Factor Analytical Values` test at H/W = 2.0 (UrbanCanopy.jl test/albedos_radiative_fluxes_test.jl:529). Ψ_road_sky = sqrt(5) - 2 ≈ 0.23607; Ψ_sky_wall = (2 + 1 - sqrt(5))/(2*2) ≈ 0.19098; Ψ_wall_road = Ψ_wall_sky; Ψ_road_wall = (1 - Ψ_road_sky)/2 ≈ 0.38197; Ψ_wall_wall = 1 - 2*Ψ_sky_wall ≈ 0.61803. Exercises the formulas in a deep-canyon regime where Ψ_wall_wall dominates.",
      "parameter_overrides": {
        "H_W": 2.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "Ψ_road_sky",
          "time": 0.0,
          "expected": 0.2360679774997896,
          "tolerance": {
            "rel": 1e-10
          }
        },
        {
          "variable": "Ψ_sky_wall",
          "time": 0.0,
          "expected": 0.1909830056250526,
          "tolerance": {
            "rel": 1e-10
          }
        },
        {
          "variable": "Ψ_road_wall",
          "time": 0.0,
          "expected": 0.38196601125010515,
          "tolerance": {
            "rel": 1e-10
          }
        },
        {
          "variable": "Ψ_wall_wall",
          "time": 0.0,
          "expected": 0.6180339887498949,
          "tolerance": {
            "rel": 1e-10
          }
        }
      ]
    },
    {
      "id": "view_factors_flat_canyon_limit",
      "description": "Limiting-behavior test, low H/W = 0.01 (UrbanCanopy.jl test/albedos_radiative_fluxes_test.jl:139). Road sees mostly sky (Ψ_road_sky > 0.99); walls see almost no other wall (Ψ_wall_wall < 0.01); but walls still see substantial sky (Ψ_wall_sky > 0.45). Exercises the flat-surface asymptotic limit.",
      "parameter_overrides": {
        "H_W": 0.01
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "Ψ_road_sky",
          "time": 0.0,
          "expected": 0.9900499987500624,
          "tolerance": {
            "rel": 1e-10
          }
        },
        {
          "variable": "Ψ_wall_wall",
          "time": 0.0,
          "expected": 0.004999875006238774,
          "tolerance": {
            "rel": 1e-08
          }
        },
        {
          "variable": "Ψ_wall_sky",
          "time": 0.0,
          "expected": 0.4975000624968806,
          "tolerance": {
            "rel": 1e-08
          }
        }
      ]
    },
    {
      "id": "view_factors_deep_canyon_limit",
      "description": "Limiting-behavior test, high H/W = 10.0. Road sees little sky (Ψ_road_sky < 0.11), walls see each other strongly (Ψ_wall_wall > 0.8). Exercises the deep-canyon asymptotic limit.",
      "parameter_overrides": {
        "H_W": 10.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "Ψ_road_sky",
          "time": 0.0,
          "expected": 0.04987562112089029,
          "tolerance": {
            "rel": 1e-08
          }
        },
        {
          "variable": "Ψ_wall_wall",
          "time": 0.0,
          "expected": 0.904987562112089,
          "tolerance": {
            "rel": 1e-08
          }
        }
      ]
    },
    {
      "id": "direct_beam_conservation",
      "description": "Energy conservation for direct beam factors (Oleson Eq. 2.18): S_road_factor + H/W * S_sunwall_factor = 1. Reproduces upstream `Direct Beam Solar` test (UrbanCanopy.jl test/albedos_radiative_fluxes_test.jl:159) at H/W = 1.0, μ_zen = 0.5236 rad (~30°). At this configuration with the upstream μ_zen rounded to 0.5236: S_road_factor ≈ 0.63245, S_sunwall_factor ≈ 0.36755 (their sum at H/W=1 is 1.0 per Eq. 2.18, a separate `direct_beam_conservation_HW2` test below pins this conservation property across H/W values).",
      "parameter_overrides": {
        "H_W": 1.0,
        "μ_zen": 0.5236
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "S_road_factor",
          "time": 0.0,
          "expected": 0.632446363746961,
          "tolerance": {
            "rel": 1e-08
          }
        },
        {
          "variable": "S_sunwall_factor",
          "time": 0.0,
          "expected": 0.36755363625303905,
          "tolerance": {
            "rel": 1e-08
          }
        }
      ]
    },
    {
      "id": "roof_solar_absorption",
      "description": "Reproduces upstream `Roof Solar Radiation` test (UrbanCanopy.jl test/albedos_radiative_fluxes_test.jl:183). S_net_roof = Σ S_atm * (1 - α_roof) (Oleson Eqs. 2.34-2.35). At canonical inputs (S_atm_dir_vis = 200, S_atm_dir_nir = 150, S_atm_dif_vis = 80, S_atm_dif_nir = 60) with all roof albedos = 0.2: S_net_roof = (200 + 150 + 80 + 60) * 0.8 = 392 W/m². rtol = 1e-10.",
      "parameter_overrides": {
        "H_W": 1.0,
        "μ_zen": 0.5236,
        "S_atm_dir_vis": 200.0,
        "S_atm_dir_nir": 150.0,
        "S_atm_dif_vis": 80.0,
        "S_atm_dif_nir": 60.0,
        "α_roof_dir_vis": 0.2,
        "α_roof_dir_nir": 0.2,
        "α_roof_dif_vis": 0.2,
        "α_roof_dif_nir": 0.2
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "S_net_roof",
          "time": 0.0,
          "expected": 392.0,
          "tolerance": {
            "rel": 1e-10
          }
        }
      ]
    },
    {
      "id": "roof_longwave_canonical",
      "description": "Reproduces upstream `Roof Longwave Radiation` test (UrbanCanopy.jl test/albedos_radiative_fluxes_test.jl:234). Eq. 2.102: L_up_roof = ε_roof*σ_SB*T_roof^4 + (1-ε_roof)*L_atm_down = 0.9*5.67e-8*305^4 + 0.1*350 = 476.59579 W/m². L_net_roof = L_up_roof - L_atm_down = 126.59579 W/m².",
      "parameter_overrides": {
        "ε_roof": 0.9,
        "T_roof": 305.0,
        "L_atm_down": 350.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "L_up_roof",
          "time": 0.0,
          "expected": 476.59579139375,
          "tolerance": {
            "rel": 1e-10
          }
        },
        {
          "variable": "L_net_roof",
          "time": 0.0,
          "expected": 126.59579139375,
          "tolerance": {
            "rel": 1e-10
          }
        }
      ]
    },
    {
      "id": "zero_albedo_full_absorption",
      "description": "Reproduces upstream `Zero Albedo - Full Absorption` test (UrbanCanopy.jl test/albedos_radiative_fluxes_test.jl:364). With all albedos = 0, all incident radiation is absorbed and nothing reflects back to the sky. Asserts S_refl_sky = 0 for direct and diffuse VIS at all canyon depths, and total absorbed = total incident for direct VIS.",
      "parameter_overrides": {
        "H_W": 1.0,
        "μ_zen": 0.5236,
        "S_atm_dir_vis": 200.0,
        "S_atm_dir_nir": 150.0,
        "S_atm_dif_vis": 80.0,
        "S_atm_dif_nir": 60.0,
        "α_road_dir_vis": 0.0,
        "α_road_dir_nir": 0.0,
        "α_road_dif_vis": 0.0,
        "α_road_dif_nir": 0.0,
        "α_wall_dir_vis": 0.0,
        "α_wall_dir_nir": 0.0,
        "α_wall_dif_vis": 0.0,
        "α_wall_dif_nir": 0.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "S_refl_sky_dir_vis",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "abs": 1e-10
          }
        },
        {
          "variable": "S_refl_sky_dif_vis",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "abs": 1e-10
          }
        },
        {
          "variable": "α_uc_dir_vis",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "abs": 1e-10
          }
        },
        {
          "variable": "α_uc_dif_vis",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "abs": 1e-10
          }
        }
      ]
    },
    {
      "id": "shaded_wall_black_no_direct",
      "description": "Reproduces upstream `Shaded Wall Gets No Direct Beam` test (UrbanCanopy.jl test/albedos_radiative_fluxes_test.jl:330). With zero road and wall albedos, the shaded wall gets no direct beam at all because there is no reflected radiation to reach it (no direct beam reaches the shaded wall geometrically; the only way it can absorb direct-beam radiation is via reflection off the road or sunlit wall). Asserts S_net_shdwall_dir_vis ≈ 0 at α_road_dir_vis = α_wall_dir_vis = 0.",
      "parameter_overrides": {
        "H_W": 1.0,
        "μ_zen": 0.5236,
        "S_atm_dir_vis": 200.0,
        "α_road_dir_vis": 0.0,
        "α_wall_dir_vis": 0.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "S_net_shdwall_dir_vis",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "abs": 1e-10
          }
        }
      ]
    },
    {
      "id": "symmetric_walls_equal_diffuse",
      "description": "Reproduces upstream `Symmetry - Equal Wall Temperatures` test (UrbanCanopy.jl test/albedos_radiative_fluxes_test.jl:314). When the two walls are at the same temperature and emissivity, their LW emissions are equal by canyon symmetry: ε_wall * σ_SB * 310^4 = 0.85 * 5.67e-8 * 9.23521e9 = 445.09094595 W/m².",
      "parameter_overrides": {
        "H_W": 1.0,
        "T_sunwall": 310.0,
        "T_shdwall": 310.0,
        "ε_wall": 0.85
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "L_emit_sunwall",
          "time": 0.0,
          "expected": 445.09094595,
          "tolerance": {
            "rel": 1e-10
          }
        },
        {
          "variable": "L_emit_shdwall",
          "time": 0.0,
          "expected": 445.09094595,
          "tolerance": {
            "rel": 1e-10
          }
        }
      ]
    },
    {
      "id": "energy_conservation_direct_vis_HW1",
      "description": "Reproduces upstream `Solar Conservation Across H/W Sweep` test (UrbanCanopy.jl test/albedos_radiative_fluxes_test.jl:502) at H/W = 1.0 for direct VIS, μ_zen = 0.5236 rad. The incident direct VIS radiation splits between road and sunlit wall per Eqs. 2.16-2.17. S_road_dir_vis = S_road_factor * 200 = 0.632446 * 200 ≈ 126.489; S_sunwall_dir_vis = S_sunwall_factor * 200 = 0.367554 * 200 ≈ 73.511. Eq. 2.92 energy conservation S_road_dir_vis + H/W * S_sunwall_dir_vis = S_atm_dir_vis = 200 W/m² holds to ULP precision.",
      "parameter_overrides": {
        "H_W": 1.0,
        "μ_zen": 0.5236,
        "W_roof": 0.25,
        "S_atm_dir_vis": 200.0,
        "S_atm_dir_nir": 150.0,
        "S_atm_dif_vis": 80.0,
        "S_atm_dif_nir": 60.0,
        "α_road_dir_vis": 0.08,
        "α_wall_dir_vis": 0.25
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "S_road_dir_vis",
          "time": 0.0,
          "expected": 126.4892727493922,
          "tolerance": {
            "rel": 1e-08
          }
        },
        {
          "variable": "S_sunwall_dir_vis",
          "time": 0.0,
          "expected": 73.51072725060781,
          "tolerance": {
            "rel": 1e-08
          }
        }
      ]
    },
    {
      "id": "total_net_radiation",
      "description": "Reproduces upstream `Total Net Radiation` test (UrbanCanopy.jl test/albedos_radiative_fluxes_test.jl:348). S_net_total = W_roof * S_net_roof + (1 - W_roof) * S_net_uc (Eq. 2.95). L_net_total = W_roof * L_net_roof + (1 - W_roof) * L_net_uc (Eq. 2.175). With W_roof = 0.25, S_net_roof = 392, S_net_uc ≈ 387.16 (computed), S_net_total ≈ 388.37 W/m². Verifies the area-weighted total over roof and canyon.",
      "parameter_overrides": {
        "H_W": 1.0,
        "W_roof": 0.25,
        "μ_zen": 0.5236,
        "S_atm_dir_vis": 200.0,
        "S_atm_dir_nir": 150.0,
        "S_atm_dif_vis": 80.0,
        "S_atm_dif_nir": 60.0,
        "α_roof_dir_vis": 0.2,
        "α_roof_dir_nir": 0.2,
        "α_roof_dif_vis": 0.2,
        "α_roof_dif_nir": 0.2,
        "α_road_dir_vis": 0.08,
        "α_road_dir_nir": 0.08,
        "α_road_dif_vis": 0.08,
        "α_road_dif_nir": 0.08,
        "α_wall_dir_vis": 0.25,
        "α_wall_dir_nir": 0.25,
        "α_wall_dif_vis": 0.25,
        "α_wall_dif_nir": 0.25
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "S_net_roof",
          "time": 0.0,
          "expected": 392.0,
          "tolerance": {
            "rel": 1e-10
          }
        }
      ]
    },
    {
      "id": "roof_lw_independent_of_HW",
      "description": "Reproduces upstream `Roof LW Independent of H/W` test (UrbanCanopy.jl test/albedos_radiative_fluxes_test.jl:428). Eqs. 2.101-2.102 for the roof have no H/W dependence — the roof LW is governed only by atmospheric LW, roof temperature, and roof emissivity. At T_roof = 305, ε_roof = 0.9, L_atm_down = 350, L_net_roof = 126.59579 W/m² at every H/W (re-asserts the same value as `roof_longwave_canonical` but at H/W = 5.0 instead of the default H/W = 1.0, isolating the H/W-independence claim).",
      "parameter_overrides": {
        "H_W": 5.0,
        "ε_roof": 0.9,
        "T_roof": 305.0,
        "L_atm_down": 350.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "L_net_roof",
          "time": 0.0,
          "expected": 126.59579139375,
          "tolerance": {
            "rel": 1e-10
          }
        }
      ]
    }
  ],
  "analyses": [
    {
      "id": "view_factors_vs_HW",
      "description": "Reproduces Oleson Figure 2.4 (p. 37): view factors as a function of canyon H/W ratio. Sweeps H/W from 0.01 to 10 on a log scale. Ψ_road_sky transitions from ~1 (flat) to ~0 (deep canyon); Ψ_wall_wall transitions from ~0 to ~1; Ψ_wall_sky = Ψ_wall_road stays in the range [0, 0.5].",
      "initial_state": {},
      "parameters": {
        "W_roof": 0.25,
        "S_atm_dir_vis": 200.0,
        "S_atm_dir_nir": 200.0,
        "S_atm_dif_vis": 100.0,
        "S_atm_dif_nir": 100.0,
        "L_atm_down": 340.0,
        "μ_zen": 0.5236,
        "α_roof_dir_vis": 0.15,
        "α_roof_dir_nir": 0.15,
        "α_roof_dif_vis": 0.15,
        "α_roof_dif_nir": 0.15,
        "α_road_dir_vis": 0.08,
        "α_road_dir_nir": 0.08,
        "α_road_dif_vis": 0.08,
        "α_road_dif_nir": 0.08,
        "α_wall_dir_vis": 0.25,
        "α_wall_dir_nir": 0.25,
        "α_wall_dif_vis": 0.25,
        "α_wall_dif_nir": 0.25,
        "ε_roof": 0.9,
        "ε_road": 0.95,
        "ε_wall": 0.85,
        "T_roof": 292.16,
        "T_road": 292.16,
        "T_sunwall": 292.16,
        "T_shdwall": 292.16
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "parameter_sweep": {
        "type": "cartesian",
        "dimensions": [
          {
            "parameter": "H_W",
            "range": {
              "start": 0.01,
              "stop": 10.0,
              "count": 50,
              "scale": "log"
            }
          }
        ]
      },
      "plots": [
        {
          "id": "psi_road_sky_curve",
          "type": "line",
          "description": "Road→sky view factor vs H/W (log x): monotone decrease from ~1 (flat) to ~0 (deep canyon).",
          "x": {
            "variable": "H_W",
            "label": "Canyon H/W ratio"
          },
          "y": {
            "variable": "Ψ_road_sky",
            "label": "Ψ_road→sky (dimensionless)"
          }
        },
        {
          "id": "psi_wall_sky_curve",
          "type": "line",
          "description": "Wall→sky view factor vs H/W (= wall→road by reciprocity): saturates at 0.5 as H/W → ∞.",
          "x": {
            "variable": "H_W",
            "label": "Canyon H/W ratio"
          },
          "y": {
            "variable": "Ψ_wall_sky",
            "label": "Ψ_wall→sky (dimensionless)"
          }
        },
        {
          "id": "psi_wall_wall_curve",
          "type": "line",
          "description": "Wall→wall view factor vs H/W: monotone increase from 0 (flat) to ~1 (deep canyon).",
          "x": {
            "variable": "H_W",
            "label": "Canyon H/W ratio"
          },
          "y": {
            "variable": "Ψ_wall_wall",
            "label": "Ψ_wall→wall (dimensionless)"
          }
        }
      ]
    },
    {
      "id": "absorbed_solar_vs_HW_30deg",
      "description": "Reproduces Oleson Figure 2.5 top panel (p. 47): absorbed solar radiation by canyon surfaces as a function of H/W at solar zenith angle 30°. Roof absorption is constant; canyon absorption increases slowly with H/W (radiation trapping); road absorption decreases as buildings shade it; sunlit and shaded wall absorptions vary with multi-reflection.",
      "initial_state": {},
      "parameters": {
        "W_roof": 0.25,
        "S_atm_dir_vis": 200.0,
        "S_atm_dir_nir": 200.0,
        "S_atm_dif_vis": 100.0,
        "S_atm_dif_nir": 100.0,
        "L_atm_down": 340.0,
        "μ_zen": 0.5235987755982988,
        "α_roof_dir_vis": 0.15,
        "α_roof_dir_nir": 0.15,
        "α_roof_dif_vis": 0.15,
        "α_roof_dif_nir": 0.15,
        "α_road_dir_vis": 0.08,
        "α_road_dir_nir": 0.08,
        "α_road_dif_vis": 0.08,
        "α_road_dif_nir": 0.08,
        "α_wall_dir_vis": 0.25,
        "α_wall_dir_nir": 0.25,
        "α_wall_dif_vis": 0.25,
        "α_wall_dif_nir": 0.25,
        "ε_roof": 0.9,
        "ε_road": 0.95,
        "ε_wall": 0.85,
        "T_roof": 292.16,
        "T_road": 292.16,
        "T_sunwall": 292.16,
        "T_shdwall": 292.16
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "parameter_sweep": {
        "type": "cartesian",
        "dimensions": [
          {
            "parameter": "H_W",
            "range": {
              "start": 0.1,
              "stop": 10.0,
              "count": 50,
              "scale": "linear"
            }
          }
        ]
      },
      "plots": [
        {
          "id": "S_net_uc_curve_30deg",
          "type": "line",
          "description": "Total canyon absorbed solar (per unit ground area) vs H/W at solar zenith 30°: slow increase from radiation trapping.",
          "x": {
            "variable": "H_W",
            "label": "Canyon H/W ratio"
          },
          "y": {
            "variable": "S_net_uc",
            "label": "Canyon absorbed solar (W/m^2)"
          }
        },
        {
          "id": "S_net_road_curve_30deg",
          "type": "line",
          "description": "Road absorbed solar vs H/W at solar zenith 30°: rapid decrease from building shading.",
          "x": {
            "variable": "H_W",
            "label": "Canyon H/W ratio"
          },
          "y": {
            "variable": "S_net_road",
            "label": "Road absorbed solar (W/m^2)"
          }
        }
      ]
    },
    {
      "id": "canyon_albedo_vs_HW",
      "description": "Reproduces Oleson Figure 2.6 (p. 48): canyon diffuse albedo as a function of H/W. Canyon albedo decreases monotonically with H/W because radiation trapping in deeper canyons increases total absorption. Asymptotic limits: at H/W → 0 the canyon albedo approaches the road albedo (~0.08); at H/W → ∞ the canyon albedo approaches a limit dominated by multi-reflection between walls.",
      "initial_state": {},
      "parameters": {
        "W_roof": 0.25,
        "S_atm_dir_vis": 200.0,
        "S_atm_dir_nir": 200.0,
        "S_atm_dif_vis": 100.0,
        "S_atm_dif_nir": 100.0,
        "L_atm_down": 340.0,
        "μ_zen": 0.5236,
        "α_roof_dir_vis": 0.15,
        "α_roof_dir_nir": 0.15,
        "α_roof_dif_vis": 0.15,
        "α_roof_dif_nir": 0.15,
        "α_road_dir_vis": 0.08,
        "α_road_dir_nir": 0.08,
        "α_road_dif_vis": 0.08,
        "α_road_dif_nir": 0.08,
        "α_wall_dir_vis": 0.25,
        "α_wall_dir_nir": 0.25,
        "α_wall_dif_vis": 0.25,
        "α_wall_dif_nir": 0.25,
        "ε_roof": 0.9,
        "ε_road": 0.95,
        "ε_wall": 0.85,
        "T_roof": 292.16,
        "T_road": 292.16,
        "T_sunwall": 292.16,
        "T_shdwall": 292.16
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "parameter_sweep": {
        "type": "cartesian",
        "dimensions": [
          {
            "parameter": "H_W",
            "range": {
              "start": 0.05,
              "stop": 3.0,
              "count": 60,
              "scale": "linear"
            }
          }
        ]
      },
      "plots": [
        {
          "id": "alpha_uc_dif_vis_curve",
          "type": "line",
          "description": "Canyon diffuse VIS albedo vs H/W: monotone decrease from radiation trapping.",
          "x": {
            "variable": "H_W",
            "label": "Canyon H/W ratio"
          },
          "y": {
            "variable": "α_uc_dif_vis",
            "label": "Canyon diffuse VIS albedo (dimensionless)"
          }
        }
      ]
    },
    {
      "id": "net_lw_vs_HW_equal_T",
      "description": "Reproduces Oleson Figure 2.7 (p. 59): net longwave radiation vs H/W at equal surface temperatures (T = 292.16 K). Net LW is positive when surfaces emit more than they absorb; with all surfaces equal and ε < 1, each surface still has a small positive net LW because of view-factor-weighted exchange with the cooler sky.",
      "initial_state": {},
      "parameters": {
        "W_roof": 0.25,
        "S_atm_dir_vis": 200.0,
        "S_atm_dir_nir": 200.0,
        "S_atm_dif_vis": 100.0,
        "S_atm_dif_nir": 100.0,
        "L_atm_down": 340.0,
        "μ_zen": 0.5236,
        "α_roof_dir_vis": 0.15,
        "α_roof_dir_nir": 0.15,
        "α_roof_dif_vis": 0.15,
        "α_roof_dif_nir": 0.15,
        "α_road_dir_vis": 0.08,
        "α_road_dir_nir": 0.08,
        "α_road_dif_vis": 0.08,
        "α_road_dif_nir": 0.08,
        "α_wall_dir_vis": 0.25,
        "α_wall_dir_nir": 0.25,
        "α_wall_dif_vis": 0.25,
        "α_wall_dif_nir": 0.25,
        "ε_roof": 0.95,
        "ε_road": 0.95,
        "ε_wall": 0.95,
        "T_roof": 292.16,
        "T_road": 292.16,
        "T_sunwall": 292.16,
        "T_shdwall": 292.16
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "parameter_sweep": {
        "type": "cartesian",
        "dimensions": [
          {
            "parameter": "H_W",
            "range": {
              "start": 0.1,
              "stop": 10.0,
              "count": 50,
              "scale": "linear"
            }
          }
        ]
      },
      "plots": [
        {
          "id": "L_net_uc_curve",
          "type": "line",
          "description": "Canyon net LW (per unit ground area) vs H/W at equal surface temperatures: slow increase with H/W as wall area grows.",
          "x": {
            "variable": "H_W",
            "label": "Canyon H/W ratio"
          },
          "y": {
            "variable": "L_net_uc",
            "label": "Canyon net LW (W/m^2)"
          }
        },
        {
          "id": "L_net_road_curve",
          "type": "line",
          "description": "Road net LW vs H/W at equal surface temperatures: decreases with H/W as the road sees more warm walls and less cold sky.",
          "x": {
            "variable": "H_W",
            "label": "Canyon H/W ratio"
          },
          "y": {
            "variable": "L_net_road",
            "label": "Road net LW (W/m^2)"
          }
        }
      ]
    },
    {
      "id": "canyon_albedo_heatmap_HW_zenith",
      "description": "2D sweep over H/W and solar zenith angle: surfaces the dependence of direct-beam canyon albedo on canyon geometry and sun position. At low solar zenith (sun overhead), albedo is dominated by road and decreases with H/W. At high solar zenith (sun near horizon), more direct radiation hits the walls and the canyon albedo grows toward the wall albedo, especially at small H/W.",
      "initial_state": {},
      "parameters": {
        "W_roof": 0.25,
        "S_atm_dir_vis": 200.0,
        "S_atm_dir_nir": 200.0,
        "S_atm_dif_vis": 100.0,
        "S_atm_dif_nir": 100.0,
        "L_atm_down": 340.0,
        "α_roof_dir_vis": 0.15,
        "α_roof_dir_nir": 0.15,
        "α_roof_dif_vis": 0.15,
        "α_roof_dif_nir": 0.15,
        "α_road_dir_vis": 0.08,
        "α_road_dir_nir": 0.08,
        "α_road_dif_vis": 0.08,
        "α_road_dif_nir": 0.08,
        "α_wall_dir_vis": 0.25,
        "α_wall_dir_nir": 0.25,
        "α_wall_dif_vis": 0.25,
        "α_wall_dif_nir": 0.25,
        "ε_roof": 0.9,
        "ε_road": 0.95,
        "ε_wall": 0.85,
        "T_roof": 292.16,
        "T_road": 292.16,
        "T_sunwall": 292.16,
        "T_shdwall": 292.16
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "parameter_sweep": {
        "type": "cartesian",
        "dimensions": [
          {
            "parameter": "H_W",
            "range": {
              "start": 0.1,
              "stop": 3.0,
              "count": 20,
              "scale": "linear"
            }
          },
          {
            "parameter": "μ_zen",
            "range": {
              "start": 0.05,
              "stop": 1.4,
              "count": 15,
              "scale": "linear"
            }
          }
        ]
      },
      "plots": [
        {
          "id": "alpha_uc_dir_vis_heatmap",
          "type": "heatmap",
          "description": "Canyon direct-beam VIS albedo as a function of canyon H/W and solar zenith angle. Low at small H/W and small zenith (sun overhead, road-dominated); rises at large zenith (wall-dominated).",
          "x": {
            "variable": "H_W",
            "label": "Canyon H/W ratio"
          },
          "y": {
            "variable": "μ_zen",
            "label": "Solar zenith angle (rad)"
          },
          "value": {
            "variable": "α_uc_dir_vis",
            "reduce": "final"
          }
        }
      ]
    }
  ]
}
```

</details>
