# MOM6 column physics — equation of state, CVMix KPP, penetrating shortwave, frazil, boundary fluxes, and implicit vertical tracer diffusion

Stage-2 implementation of the MOM6 column physics of the EqESM project
(MOM6 `dev/ncar_260909 @301879336`, instrumented fork
`stage1/EqESM-cesm-mom6` branch `instrument/mom6-dumps`), as esm 1.3.0
files with `tests` blocks pinned to the stage-1 instrumentation dumps
(`stage1/dumps/mom6/mom6_eos.csv`, `mom6_kpp_obl.csv`, `mom6_kpp.csv`,
`mom6_kpp_wide.csv`, `mom6_sw_abs.csv`, `mom6_frazil.csv`, `mom6_bflux.csv`,
`mom6_diabatic_tri.csv`).

The ported files (this directory) cover the column physics only: the
equation of state, the CVMix KPP planetary boundary layer, the penetrating
shortwave absorption, frazil formation, the surface boundary fluxes, and
the implicit vertical tracer diffusion.  **Not ported** (still in review in
the EqESM project): the C-grid dynamics (continuity / PGF / Coriolis /
momentum) and `mom6_surface_forcing.esm` (the surface-forcing import lane,
being pruned by the EqESM `pin-lint-prune` work).  The `masked_pair_average`
template of `mom6_templates.esm` is that lane's consumer of this library and
is carried here with the library.

Sources:
`components/mom/MOM6/src/equation_of_state/MOM_EOS_Wright_full.F90`,
`components/mom/MOM6/src/parameterizations/vertical/MOM_CVMix_KPP.F90`,
`components/mom/MOM6/pkg/CVMix-src/src/shared/cvmix_kpp.F90`,
`components/mom/MOM6/pkg/CVMix-src/src/shared/cvmix_math.F90`,
`components/mom/MOM6/src/parameterizations/vertical/MOM_opacity.F90`,
`components/mom/MOM6/src/parameterizations/vertical/MOM_diabatic_aux.F90`,
`components/mom/MOM6/src/parameterizations/vertical/MOM_diabatic_driver.F90`,
`components/mom/MOM6/src/parameterizations/vertical/MOM_tracer_diabatic.F90`,
`components/mom/MOM6/src/ice_shelf/MOM_TFreeze.F90`,
`components/mom/MOM6/src/core/MOM_forcing_type.F90`,
`components/mom/MOM6/config_src/drivers/nuopc_cap/mom_surface_forcing_nuopc.F90`
(`masked_pair_average` only), and
`components/mom/MOM6/src/framework/mom6_dump_mod.F90` (the dump writer).

## File map

| File | Contents | Fortran source |
|---|---|---|
| `mom6_templates.esm` | Expression-template library (27 templates): `wright_alpha0`, `wright_poly` (the shared bivariate polynomial, bound with the b- and c-coefficient sets for the p0 and lambda sub-polynomials), `wright_density`, `wright_drho_dT`, `wright_drho_dS`, the 15 constant fragments `wright_coeff_a0..c5` (the single shared source of the fit coefficients), the `wright_rho` composition (the whole in-situ law in one application, used by KPPBLD), `masked_pair_average` (the AGRID h-point stress average; consumer not ported), `linear_tfreeze`, `interface_entrainment`, `tridiagonal_residual`, `surface_mix`, `layer_content_change` | `MOM_EOS_Wright_full.F90`: density_elem_Wright_full 75-91, calculate_density_derivs_elem_Wright_full 179-204, constants 23-37; `mom_surface_forcing_nuopc.F90`: 943-951; `MOM_TFreeze.F90`: calculate_TFreeze_linear_scalar 51-64; `MOM_diabatic_driver.F90`: 1728-1739; `MOM_tracer_diabatic.F90`: 384-413; `MOM_diabatic_aux.F90`: 1170-1171 |
| `mom6_eos.esm` | Model `WrightEOS` — rho(T, S, p), drho/dT, drho/dS via the templates (imported by reference), with the 15 coefficients bound by reference from the `wright_coeff_a0..c5` fragments, `I_denom2`; 15 dump-pinned tests | `MOM_EOS_Wright_full.F90` as above; the EOS calls themselves are `calculate_density`/`calculate_density_derivs_scalar` in `MOM_CVMix_KPP.F90:1437` |
| `mom6_kpp_templates.esm` | Expression-template library for the KPP laws (16 templates): the LMD94 stability functions phi_m^-1/phi_s^-1 with the Large-et-al.-1994 coefficients (`kpp_phi_coeffs_m_a/c/s_a/s_c`, `kpp_phi_inv_m/s`), the turbulent velocity scales w_m/w_s (`kpp_wm`, `kpp_ws`), the unresolved shear Vt² with the Danabasoglu et al. 2006 Cv (`kpp_unresolved_shear`), the bulk Richardson number (`kpp_bulk_richardson`), the KPP shape function G(σ) (`kpp_shape_cubic`), the OBL-depth quadratic (`kpp_quad_interp_c/b/a`, `kpp_quad_root`), the KPP_IS_ADDITIVE=False replacement (`kpp_override_nonzero`) | `cvmix_kpp.F90`: compute_phi_inv 2910-3005, turbulent_scales_1d_OBL 2416-2604, unresolved_shear 2611-2903, bulk_Richardson 2031-2132, shape_function_coeffs 3079-3112; `cvmix_math.F90`: linear_through_cubic_poly_interp 103-138, cubic_root_find 260-294, evaluate_cubic 300-340 |
| `mom6_column_discretization.esm` | Local EarthSciDiscretizations-format rules: the layer/interface grid of the MOM6 column (index sets `layer`/`iface`, metaparameters `N_LAYER`/`N_IFACE` = 75/76) and the two `column_nonuniform_1d` cumulative-integral rules imported by reference at a 9.7.7 renaming edge (`integral_lev_nodes_cumulative_from_bottom` — the surface-to-interface exclusive prefix; `integral_lev_cumulative_from_bottom` — the surface-to-layer-centre midpoint-rule integral) | `MOM_CVMix_KPP.F90`: the iFaceHeight/cellHeight loops 1237-1243, the pRef hydrostatic accumulation 1282-1283/1452-1456; ESD `grids/column_nonuniform_1d/rules/` |
| `mom6_kpp.esm` | Models `KPPBLD` (KPP_compute_BLD down to the pre-smoothing OBLdepth/kOBL: the surface-layer averages, the Wright EOS as three `wright_rho` applications at the layer-top pressure, the interface/cell heights and hydrostatic `pRef` as ESD `integral`s, deltaBuoy/N2/N, w_s/Vt²/BulkRi, OBL_depth_low with the Monin-Obukhov limit and the MOM6 bounds) and `KPPCoefs` (cvmix_coeffs_kpp_low: the no-match shape G(σ), the 2..floor(kOBL) overwrite, the KPP_IS_ADDITIVE=False replacement via `kpp_override_nonzero` with `Kd_salt = Kd_heat`, the CVMix non-local term, all driven by the *smoothed* OBLdepth/kOBL from the dump); 8 dump-pinned tests (5 BLD rows × 26..31 + 3 coefficient rows × 3..5 = 158 assertions) | `MOM_CVMix_KPP.F90`: KPP_compute_BLD 1195-1575, KPP_calculate 740-1067, KPP_smooth_BLD 1715-1834; `cvmix_kpp.F90`: OBL_depth_low 1585-1814, kOBL 1821-1867, coeffs_kpp_low 701-1298 |
| `mom6_sw_discretization.esm` | Local EarthSciDiscretizations-format rule pair lowering the penetrating-shortwave optical-depth integrals (the Beer-Lambert integral `tau(n,i) = ∫ opacity(n,z') dz'` from the surface to each interface): `sw_optical_depth` (heating path, bounds `z_sfc`, measure `h` = h_after) and `sw_optical_depth_buoy` (buoyancy path, bounds `z_sfc_buoy`, measure `h_buoy` = h_before), sharing the flat `sw_optical_depth_scan` prefix faq | `MOM_opacity.F90`: absorbRemainingSW :748-750, sumSWoverBands :980-982 |
| `mom6_shortwave.esm` | Model `ShortwaveAbsorption` — the penetrating shortwave absorption path written as math: the optical-depth integrals (Beer-Lambert), the per-band surface split `penSW_bnd` (an input here), the decay `dT_k` and the remaining `pen_sw_rem`, `netPen`, `absorbed_total`; 6 dump-pinned tests | `MOM_opacity.F90`: absorbRemainingSW 602-869, sumSWoverBands 894-1041, opacity_from_chl 247-479; `MOM_forcing_type.F90`: extractFluxes1d 619 |
| `mom6_frazil.esm` | Model `FrazilFormation` — per-layer in-situ pressure (the hydrostatic cumulative integral over the layer-thickness measure), the LINEAR freezing-point law (`linear_tfreeze`), the per-layer branch law of the frazil scan and the column heat requirement; 4 dump-pinned tests | `MOM_diabatic_aux.F90`: make_frazil :122-250 (pressure :176,179; law evaluation :187-188, 213-214; heat capacities :190; scan :228-238) |
| `mom6_bflux.esm` | Model `BoundaryFluxes` — surface mass/heat/salt flux application in the surface layer (step A :1039-1071, step B :1109-1146 with `fractionOfForcing = 1` in the surface layer), the penetrating-shortwave heating (step C, absorbRemainingSW), the column budgets (dMass/dSalt/dHeat identities) and the residual pins; 4 dump-pinned tests | `MOM_diabatic_aux.F90`: applyBoundaryFluxesInOut :702-1483 (EnthalpyConst :845-846, :1141) |
| `mom6_vertical_diffusion.esm` | Model `TridiagonalMixing` — the MOM6 implicit vertical tracer diffusion written as the PDE dT/dt = d/dz (Kd_heat dT/dz), dS/dt = d/dz (Kd_salt dS/dz), discretized by the EarthSciDiscretizations rule `varcoeff_face_laplacian_lev_flux_bc` with zero prescribed face fluxes (the rule's lowering is exactly the MOM6 tridiagonal law h_k (u'_k − u_k) = ent_k (u'_{k−1} − u'_k) + ent_{k+1} (u'_{k+1} − u'_k) with ent = dt·Kd/dz_int); T and S are carried separately because Kd_heat ≠ Kd_salt on most dumped interfaces; 3 dump-pinned tests | `MOM_tracer_diabatic.F90`: tracer_vertdiff_Eulerian no-sink branch 384-413; `MOM_diabatic_driver.F90`: 1728-1739 |

## Run configuration pinned by the components

`C_JRA_t62_mom6_inst` (1 day, 0001-01-01; T62_t232, NK=75 z\* ALE,
DT=1800, DT_THERM=3600 s, 72 PEs; solution-neutral — restarts
bit-identical to the reference `C_JRA_t62` run).  13 traced thermo steps
(tods 3600..46800; cpl_step 1 covers two thermo steps), 12 traced cells
(the PET-0 SW corner block) plus — for the KPP widening — the first
`dump_first_cells=32` ocean cells of every PE, restricted to columns that
are unstable (surfBuoyFlux < 0) or warm (T_sfc > 20 °C) at that step
(8164 rows over 33 PEs).  All unit rescale factors are 1.0, so internal ==
MKS and the laws below are evaluated in physical units.

- KPP configuration: `RI_CRIT=0.3`, `VON_KARMAN=0.4`, `SURF_LAYER_EXTENT=0.1`,
  `MINIMUM_OBL_DEPTH=5.0`, `MINIMUM_VT2=1e-10`, `INTERP_TYPE=quadratic`,
  `INTERP_TYPE2=LMD94`, `MATCH_TECHNIQUE=MatchGradient`,
  `ENHANCE_DIFFUSION=False`, `NLT_SHAPE=CVMix`, `N_SMOOTH=3`,
  `COMPUTE_MONIN_OBUKHOV=True`, `COMPUTE_EKMAN=False`,
  `USE_KPP_LT_K/VT2=False`, `KPP_IS_ADDITIVE=False`,
  `KPP_SHORTWAVE_METHOD=MXL_SW`, `l_LMD_ws=false`, `lnoDGat1=true`.
- `EQN_OF_STATE = WRIGHT_FULL` (the MOM6 default), `USE_PSURF_IN_EOS = True`.
- `TFREEZE_FORM=LINEAR` with the Fortran defaults `TFREEZE_S0_P0=0.0 degC`,
  `DTFREEZE_DS=-0.054 degC ppt-1` and `DTFREEZE_DP=-7.75e-8 degC Pa-1`
  from the run's MOM_input; `PRESSURE_DEPENDENT_FRAZIL=True`.
- `RHO_0 = 1035 kg m-3` (MOM6 default, MOM_verticalGrid.F90:135-140),
  `g_Earth = 9.8 m s-2` (MOM6 default, MOM_verticalGrid.F90:130-132 —
  verified against the dump, **not** 9.80665), `C_P = 3992 J kg-1 degC-1`
  from MOM_input.
- `AGGREGATE_FW_FORCING=True` so netMassIn == 0; `EnthalpyConst = 0`
  (the CESM coupler provides heat_content_evap); `OPACITY_SCHEME=OHLMANN_03`
  (chlorophyll-driven opacity), `N_SW_BANDS=2`; `DO_BRINE_PLUME = False`;
  `wind_stagger = AGRID`.

## Units

| Quantity | Symbol | Units |
|---|---|---|
| Potential temperature | `T` | degC |
| Salinity | `S` | ppt (treated as dimensionless, matching the EOS usage) |
| Pressure | `p`, `p0`, `p_surf`, `pRef`, `p_top` | Pa |
| Density | `rho` | kg/m³ |
| Density derivatives | `drho_dT`, `drho_dS` | kg/m³/degC, kg/m³/ppt |
| Specific volume (alpha_0) | `al0` | m³/kg |
| Sound-speed-squared offset | `lam` | m²/s² |
| EOS coefficients | `a0..a2`, `b0..b5`, `c0..c5` | as in the Fortran's units comments (F90:23-37) |
| Layer/interface heights | `z_cell`, `z_inter`, `depth`, `SLdepth`, `delH`, `OBLdepth`, `OBLdepth_s`, `root`, `ze` | m |
| Layer thicknesses | `h`, `h_before`, `h_after`, `dz` | m |
| Velocities | `surfU`, `surfV`, `Uk`, `Vk`, `uStar`, `uStar_s`, `w_s`, `w_m` | m/s |
| Shear | `deltaU2`, `Vt2` | m²/s² |
| Buoyancy | `surfBuoyFlux_s`, `deltaBuoy`, `B0` | m²/s³ (surfBuoyFlux), m/s² (deltaBuoy) |
| Buoyancy frequency | `N2`, `N` | s⁻², s⁻¹ |
| Bulk Richardson number | `BulkRi`, `quad_a2` | 1 |
| Quadratic coefficients | `quad_b2`, `quad_c2`, `slope` | m⁻¹, m⁻², m⁻¹ |
| Fractional OBL index | `kOBL`, `kOBL_s`, `kwup`, `kfirst`, `kwfirst` | 1 |
| Diffusivities/viscosity | `Kd_heat`, `Kd_salt`, `Kv`, `Kt_in`, `Ks_in`, `Kv_in`, `Kt_out`, `Ks_out`, `Kv_out` | m²/s |
| Entrainment | `ent`, `ent_s` | m |
| Non-local transport | `NLT_heat`, `NLT_salt`, `nonlocal_coeff`, `sigma`, `G` | 1 |
| SW penetration | `penSW_bnd`, `pen_sw_rem`, `netPen` | degC·m (pen_sw_rem), degC·m/s (netPen), degC·m (dT·h) |
| KPP constants | `GORHO` = g/ρ₀ (m⁴ s⁻² kg⁻¹), `PRESS_STEP` = g·ρ₀ (Pa/m), `MIN_OBL_DEPTH` (m), `MIN_VTSQR` (m² s⁻²), `RI_CRIT`, `VON_KARMAN`, `SURF_LAYER_EXT`, `ZETA_M` = −0.2, `ZETA_S` = −1.0, `A_M`, `C_M`, `A_S`, `C_S`, `CSTAR` (dimensionless LMD94 constants) | as noted |

`degC` and `ppt` are accepted unit strings in esm 1.3.0; ppt is treated as
dimensionless, matching the model's EOS usage (the a2/b5/c5 coefficients
carry the salinity dimension instead).

## The Wright 1997 full-range EOS (`mom6_templates.esm`, `mom6_eos.esm`)

The law (Wright, JPO 1997, "A new salinity equation of state"; a fit to
UNESCO EOS-80 valid for −2 < θ < 40 degC, 0 < S < 40 PSU, 0 < p < 1e8 Pa)
is rho = (p + p0)/(lambda + al0·(p + p0)) with the three polynomials
al0/p0/lambda (density_elem_Wright_full, MOM_EOS_Wright_full.F90:86-89;
constants a0..c5 at F90:23-37).  The derivatives
(calculate_density_derivs_elem_Wright_full, F90:194-202) are the Fortran's
hand-coded formulas with I_denom2 = 1/(lambda + al0·(p+p0))²; they are
transcribed (not written as symbolic D(rho,T)/D(rho,S)) because in esm
1.3.0 the D operator is a rewrite-target for discretization stencils and
the CLI evaluator rejects it for algebraic expressions.  The `wright_rho`
composition binds the 15 fit coefficients internally from the
`wright_coeff_a0..c5` constant fragments (the single shared source of the
coefficient values, also bound by reference by the WrightEOS model), so a
consuming component applies the whole in-situ law with only its (T, S, p)
triple.  Applied once per state by KPPBLD (surface-layer mean, layer
value, and layer-1 value, all at the layer-top pressure pRef).

## CVMix KPP boundary layer (`mom6_kpp_templates.esm`, `mom6_kpp.esm`, `mom6_column_discretization.esm`)

`KPPBLD` reproduces `KPP_compute_BLD` (MOM_CVMix_KPP.F90:1195-1575) down
to the pre-smoothing OBL depth and kOBL.  The column prefix sums of the
geometry and hydrostatics — the interface depths `depth` (so the heights
`z_inter` and `z_cell`), and the reference pressure `pRef = p_surf +
PRESS_STEP·depth` — are written as **ESD `integral` operators** lowered by
the `column_nonuniform_1d` cumulative-integral rules (imported by
reference at the esm-spec 9.7.7 renaming edge lev → layer, lev_nodes →
iface, with NLEV bound to N_LAYER), per the house rule that integrals are
`integral`, not aggregate sums or `faq` index gathers.  The depth of
interface i is the surface-to-interface exclusive prefix
`depth[i] = Σ_{j<i} f[j]·dz[j]` (the unit integrand is declared by the
component), and the cell heights are the midpoint-rule integrals to the
layer centres.  The rewritten integral forms are bit-identical to the
Fortran's running accumulations (measured residual ~4e-16).  The
surface-layer means (surfHtemp/surfHsalt/surfHu/surfHv) stay `faq` sums:
they are exact integrals over the i-dependent interior depth
`[0, SLdepth(i)]`, and the `column_nonuniform_1d` rules match only the
ground bounds z_sfc/z_top (an ESD generalization to a parameter-valued
interior bound would be the future home — documented in the file).  The
pointwise laws (stability functions, w_m/w_s, Vt², BulkRi, G(σ), the
OBL-depth quadratic) come from `mom6_kpp_templates.esm`.

`KPPCoefs` reproduces `cvmix_coeffs_kpp_low` (cvmix_kpp.F90:701-1298) for
the reference configuration: the no-match shape G(σ) at the surface, the
2..floor(kOBL) overwrite, the `KPP_IS_ADDITIVE=False` replacement via
`kpp_override_nonzero` with `Kd_salt = Kd_heat`, and the CVMix non-local
term — all driven by the *smoothed* OBLdepth/kOBL from the dump.

## Penetrating shortwave absorption (`mom6_shortwave.esm`, `mom6_sw_discretization.esm`)

The component is written as math, not as the Fortran's loop: the optical
depth at interface i is the Beer-Lambert integral
tau(n,i) = ∫₀^{z_i} opacity(n,z') dz' of the surface-to-interface water
column, spelled with the ESD `integral` op and lowered by the local match
rules of `mom6_sw_discretization.esm` (the cumulative-from-bottom integral
of `integral_lev_nodes_cumulative_from_bottom` lifted to the [band, layer]
integrand, because the imported ESD integral rules constrain the integrand
to a bare lev-shaped reference).  The measure is the per-path layer
thickness: `h` = h_after (the post-flux thickness the heating path sees,
absorbRemainingSW :748-750) for OD and `h_buoy` = h_before (the pre-flux
thickness of the sumSWoverBands/KPP path, MOM_forcing_type.F90:1102) for
OD_buoy.  The per-band surface split `penSW_bnd` (extractFluxes1d,
MOM_forcing_type.F90:619) is an input of the component (the
chlorophyll-lookup split law needs chl and downwelling SW, which are not
dumped).  The min_SW_heat clamp region of absorbRemainingSW is a stateful
recurrence (and references the model's `I_Habs = 1e3·GV%H_to_m` length
scale — see bugs.md) and is not expressed as pure math; the pinnable
region is defined exactly by the clamp condition, and `absorbed_total`
pins the conservation identity across the whole column including the
clamped layers.

## Frazil formation (`mom6_frazil.esm`)

`make_frazil` (MOM_diabatic_aux.F90:122-250): the model evaluates the
per-layer in-situ pressure as the hydrostatic cumulative integral of the
constant gradient dpdz = RHO_0·g_Earth over the layer-thickness measure h
(the composite-midpoint form of the F90:176-179 accumulation, lowered by
the shared `mom6_column_discretization.esm` rules — the same import path
mom6_kpp.esm uses; KPP's `PRESS_STEP = g_Earth·H_to_RZ = 9.8·1035` equals
frazil's `g_Earth·RHO_0` under Boussinesq, so the two hydrostatic prefixes
are one law, factored into the shared discretization file), the LINEAR
freezing-point law (the `linear_tfreeze` template, calculate_TFreeze_linear_scalar,
MOM_TFreeze.F90:62), the layer heat capacities hc = RHO_0·C_P·h (F90:190),
and the per-layer branch law of the frazil scan: the supercooling
`supercooling_k = max(0, T_freeze_k − T_before_k)`, the outcome
`T_after_k = T_before_k + supercooling_k`, and the column heat requirement
fraz_col.  The traced window contains no supercooled layer (all 312 rows
`T_before ≥ T_freeze`, frazil_in == 0), so the bottom-up scan, the
thin-layer exception (F90:219-224) and the reclaim are not pinned (a
winter window is required); the freezing-point law and pressure
accumulation they build on **are** pinned on every layer.

## Surface boundary fluxes (`mom6_bflux.esm`)

`applyBoundaryFluxesInOut` (MOM_diabatic_aux.F90:702-1483) with
netMassIn == 0 (AGGREGATE_FW_FORCING=True) and the heat content of the
mass exchange added via dThickness·T·EnthalpyConst (F90:1141; the
reference run has EnthalpyConst = 0 because the CESM coupler provides
heat_content_evap).  Every traced row has `fractionOfForcing = 1` in the
surface layer (h₁ ~ 2.5 m well above minimum_forcing_depth) and the
running remainders vanish exactly, so all forcing is consumed by layer 1
(verified on all 156 rows: h, T and S change only in layer 1, and only by
the fluxes) — the general multi-layer remainder scan (F90:1117-1132) is
not pinned (needs a shallow-column configuration).  The penetrating
shortwave is applied by absorbRemainingSW (step C, F90:1355-1362): the
component consumes the per-layer SW heating dT and the bottom leftover of
the ShortwaveAbsorption component (here sourced from the
mom6_sw_abs.csv dump columns dT_k and pen_sw_rem_n(75)).  The column
budgets are the plain per-layer sums dMass_col = Σ_k (h_after_k −
h_before_k) == netMassIn + netMassOut, dSalt_col = Σ_k (h_after_k·S_k −
h_before_k·S_before_k) == netSalt and dHeat_col == netHeat (the dSalt/dHeat
per-layer terms via the `layer_content_change` template), with the
`heat_residual` pin closing the loop.

## Implicit vertical tracer diffusion (`mom6_vertical_diffusion.esm`)

`TridiagonalMixing` writes the MOM6 operator as the PDE
dT/dt = d/dz (Kd_heat dT/dz), dS/dt = d/dz (Kd_salt dS/dz) for each
tracer, discretized by the EarthSciDiscretizations rule
`varcoeff_face_laplacian_lev_flux_bc` with zero prescribed face fluxes.
The rule's lowering (G[n] = Kd[n]·(u[n] − u[n−1])/(zc[n] − zc[n−1]),
L[ell] = (G[ell+1] − G[ell])/dz[ell]) is exactly the MOM6 tridiagonal law
h_k (u'_k − u_k) = ent_k (u'_{k−1} − u'_k) + ent_{k+1} (u'_{k+1} − u'_k)
with ent = dt·Kd/dz_int (the PDE's h divides out through the cell
measure); the esd column reverses the MOM6 top-down order.  T and S are
carried separately because Kd_heat ≠ Kd_salt on most dumped interfaces
(10-36 of 76 per column, up to ~50%; this corrects a documentation error
in README-mom6-w2.md — the dump contradicts the claim that they are
equal).  An implicit (backward-Euler) solve is not expressible in the esd
inline tests (algebraic self-referential equations are rejected as
observed cycles), so the component carries the operator in ODE form
(D(u,t) = ptend), the dumped after-state as the initial condition, and
the tests assert the operator evaluated on that state (ptend =
(T_after − T_before)/dt, the ent identity, and the tridiagonal-residual
identity at the deep layers the tendencies cannot pin).

## Testing

All `tests` blocks are `time_span {0,0}` instantaneous pins; every
expected value is a real dump row, identified in the test descriptions by
step/cell/layer.  The dump writes `es26.17` and the reference run is r8,
so the transcriptions are pinned to round-off at rel 1e-12 (tolerances
are loosened only where a numerical reason is stated in the test
description — e.g. the deep-layer tendencies limited by the tridiagonal
solve's residual, the OBL-depth quadratic's Newton-vs-closed-form
residual, and the ptend = (T_after − T_before)/dt derived pins).

| File | Tests | Assertions | What is pinned |
|---|---|---|---|
| `mom6_eos.esm` | 15 | 45 | rho/drho_dT/drho_dS at 12 surface/mid/deep states of 4 cells over steps 1, 3, 5, 6, 12: the T/S/p range extremes of the dump (T −1.99..2.04 °C, S 33.25..34.66 ppt, p 9.97e4..7.85e6 Pa), min/max rho, drho_dT (most- and least-negative), drho_dS (min/max) — every template exercised on every row |
| `mom6_kpp.esm` | 8 | 158 | 5 OBL rows: OBLdepth/kOBL, BulkRi/deltaU2/N2 at layers 2..kOBL+3 (layer 1 is 0 by construction), spot z_cell at layers 1..kOBL+3, z_inter at ifaces 2..kOBL+3, the deep z at layer/iface 75, and kfirst (derived, not a dump column); 3 coefficient rows: Kd_heat/Kv at the KPP-active interfaces 2..kwup + one Kv_out pass-through at kwup+1, rel 1e-12 |
| `mom6_shortwave.esm` | 6 | 78 | pen_sw_rem/dT/netPen inside the pinnable region (both bands unclamped, |netPen| > 1e-6), absorbed_total across the whole column, rel 1e-12 (reproduces the dumps at rel 3.6e-15/1e-13/1e-16) |
| `mom6_frazil.esm` | 4 | 52 | p_top/T_freeze at the surface, mid-column and deep layers of the 4 pinned cells (the per-layer in-situ pressure, the LINEAR freezing law, supercooling, the heat requirement); fraz_col and supercooling only in their zero branches (no supercooled layer in the window) |
| `mom6_bflux.esm` | 4 | 28 | h_after/T_after/S_after in the surface layer (the flux application), penSW_total/absorbed_total, the dMass/dSalt/dHeat column budgets and heat_residual on 4 rows spanning the flux ranges |
| `mom6_vertical_diffusion.esm` | 3 | 56 | ptend_T/ptend_S at boundary, mid-column and deep layers; ent/ent_s at the convective spike, a T/S-differing interface and a deep interface; the tri_residual identity at the deep layers, per row (rowA convective, rowB moderate, rowC shallow) |

### Pinned rows and coverage

| Test (BLD) | mom6_kpp_obl.csv row | kfirst (1-based) | OBLdepth [m] | kOBL |
|---|---|---|---|---|
| `cell782_step3600_quad_k3` | (7, 82, 3600) | 4 | 6.613560999075406 | 3.75 |
| `cell883_step3600_quad_k3` | (8, 83, 3600) | 4 | 5.974325344745279 | 3.25 |
| `cell784_step10800_two_point_k2` | (7, 84, 10800) | 3 | 5.0 (floored) | 2.75 |
| `cell1184_step3600_kfirst2` | (11, 84, 3600) | 2 | 5.0 (floored) | 3.25 |
| `cell684_step10800_kfirst2_shallow` | (6, 84, 10800) | 2 | 5.0 (floored) | 2.75 |

| Test (KPPCoefs) | mom6_kpp.csv row | OBLdepth_s [m] | kOBL_s | kwup vs ktup |
|---|---|---|---|---|
| `cell782_step3600_kOBL325` | (7, 82, 3600) | 6.1872106097070425 | 3.25 | kwup = ktup + 1 |
| `cell882_step3600_kOBL375` | (8, 82, 3600) | 6.309964392417778 | 3.75 | kwup = ktup |
| `cell684_step10800_kOBL275` | (6, 84, 10800) | 5.001656526745087 | 2.75 | kwup = 2 |

`kfirst` is not a dump column: it comes from the Python reference
reimplementation of the OBL_depth_low branch selection and is labeled
"derived (not a dump column)" in the test descriptions.  The kfirst = 2
rows exercise the two-point (zero-slope) quadratic through cell centers
1..2; the kfirst = 3 and 4 rows exercise the slope-preserving quadratic.
The kOBL fraction is pinned on both sides of the crossing (.75 and .25),
plus the shallow kfirst = 2 rows.  The vertdiff rows (rowA tod=32400
gi=3 gj=79 convective, rowB tod=10800 gi=5 gj=79 moderate, rowC tod=3600
gi=3 gj=78 shallow) span the ent range 0.02..3.6e6 m and the T/S-differing
diffusivity interfaces; the shortwave rows span 6 cells × steps of
mom6_sw_abs.csv inside the pinnable region; the frazil/bflux rows span
both frazil calls of 4 cells (tod 3600..46800).

### Coverage limitations (this data window)

| Unpinned branch | Why |
|---|---|
| N_SMOOTH=3 horizontal smoothing (KPP) | inherently horizontal; pre-smoothing values pinned, smoothed values consumed as inputs |
| kfirst = N_LAYER+1 (OBL_limit) branch of OBL_depth_low | no traced column has BulkRi ≤ RI_CRIT in every layer |
| kfirst = 2 and 3 interpolated OBL depths | below the MINIMUM_OBL_DEPTH = 5 m floor in every traced column; only the floored OBLdepth can be pinned |
| unstable (surfBuoyFlux < 0) branches (KPP) | all 156 traced columns are stable; the stability functions' convective branch and the nonzero non-local term are unpinned |
| Langmuir paths | l_LMD_ws = false, USE_KPP_LT_K/VT2 = False: the lStokesMOST and Langmuir-entrainment branches are not transcribed |
| MINIMUM_VT2 floor | not reached in the traces (Vt² stays above 1e-10 m² s⁻²) |
| min_SW_heat clamp region (shortwave) | a stateful recurrence (and the I_Habs length scale, see bugs.md); pinned only through absorbed_total; an exact Python simulation of the clamped routine reproduces the dumps to 3e-14 (402 clamp firings across the 156 rows) |
| OHLMANN_03 surface split (shortwave) | chl and downwelling SW are not dumped; sw_pen_band is an input of the component |
| Frazil formation scan, thin-layer exception, reclaim | sequential, data-dependent scans; no supercooled layer and no pending frazil heat in the window (a winter window is required) |
| Multi-layer flux distribution (bflux step B) | fractionOfForcing = 1 in layer 1 on every traced row; the scan degenerates to the layer-1-only law pinned here (a shallow-column configuration is required) |
| Brine plume, heat-content-of-rain/runoff terms | DO_BRINE_PLUME = False; extractFluxes1d outputs are inputs of this component (a separate boundary) |
| Vertdiff surface/bottom face fluxes | the zero-flux boundary conditions are exercised through the operator at the boundary layers, not as separate values |
| EOS range | the dump window only spans −2..2.04 °C, 33.25..34.66 ppt, 9.97e4..7.85e6 Pa; the law's validity range extremes and the density-anomaly/spec-vol variants are not exercised |

## bugs.md

The following `## TBD.` entries are logged in the EqESM project's
`bugs.md` (centralized CESM bug list):

- `sumSWoverBands` hardcodes `I_Habs = 1e3*GV%H_to_m` (MOM_opacity.F90:950)
  while `absorbRemainingSW` uses `optics%PenSW_absorb_Invlen ≈ 1 m-1`
  (:711, 1211): a 1000× inconsistency in the min_SW_heat clamp length
  scale.  Only affects the unpinned clamp region in this window;
  documented, not corrected (the component pins the unclamped law exactly
  as the model computes it).

## ESD dependencies

All four EarthSciDiscretizations imports are on **ESD main** (no unmerged
ESD branch is needed):

- `grids/column_nonuniform_1d/grid.esm` (`column_cell_center`,
  `column_cell_thickness`),
- `grids/column_nonuniform_1d/rules/varcoeff_face_laplacian_lev_flux_bc.esm`,
- `grids/column_nonuniform_1d/rules/integral_lev_cumulative_from_bottom.esm`,
- `grids/column_nonuniform_1d/rules/integral_lev_nodes_cumulative_from_bottom.esm`.

The two local rule files (`mom6_column_discretization.esm`,
`mom6_sw_discretization.esm`) are EarthSciDiscretizations-format and
follow the corpus conventions of the CISM port's
`cism_velo_discretization.esm`.

## Pin-lint (`tools/esm-pin-lint.py` of the EqESM project)

`python3 tools/esm-pin-lint.py` on this directory reports **20 findings
(9 non-warning)** — every one triaged by the EqESM `mom6-prune-esm` slice
(disposition record: `stage2/README-mom6-prune-esm.md` in the EqESM
project).  No assertion was dropped: all 31 flagged assertions are real,
failable tests.  The port's original `wright_lambda` ≡ `wright_p0`
`duplicate-template` finding is gone — the re-port (below) copies the
EqESM stage-2 files after their `wright_poly` refactor, which merged the
pair into one template.

| finding | disposition |
|---|---|
| `override-copy` ×3 — KPPCoefs `Kv_out` pass-through pins at the first restoration interface kwup+1 | **branch-selection pins** of the `kpp_override_nonzero` else-branch (Kv_out = Kv_in where the KPP viscosity is zero): fail on an inverted ifelse condition, a shifted pass-through index, or a kwup off-by-one; the value equals the Kv_in element *because the law's else-branch is a pass-through*; kept one per row by the EqESM review trim (`README-mom6.md`) |
| `override-copy` + `zero-pin` ×4 — bflux `heat_residual` pins | the column heat budget closure `dHeat_col = netHeat + penSW_total − leftover` across four independently computed terms at abs 1e-12; fails if any term is wrong; the conservation pin the EqESM review kept when the mass/salt residual pins were dropped (`README-mom6-frazil-bflux.md`) |
| `zero-pin` ×4 tests — frazil `supercooling` (×2) and `fraz_col` | the **no-formation branch law** of the frazil scan: supercooling = max(0, T_freeze − T_before) pinned on the two closest-to-freezing layers (margins 0.175/0.178 degC), fraz_col = Σ hc·supercooling; fail on a missing max clamp, a wrong freezing point, a wrong heat capacity, or any spurious supercooling (the formation branch is a documented coverage gap — every traced column is warm) |
| `zero-pin` ×3 tests — vertdiff `tri_res_T/S` | the scaled residual of the implicit vertical-diffusion solve (`tridiagonal_residual`), pinned at mixed-layer and bottom layers at abs tolerances scaled to each row's conditioning; the lane's check that the PDE discretization reproduces the MOM6 tridiagonal solve — fails on any operator/solve/ent error; zero-valued on these rows *because the solve is consistent*, the property being asserted |
| `inline-repeat` ×2 — KPPBLD `max(-(i,1),1)` index clamp and KPPCoefs `and(>=(i,2), <=(i,kwup))` guard | **false positives**, documented: the F90's `max(k−1,1)` floor in index position and the `k >= 2 .and. k <= kwup` loop guard in the Kd_heat/Kd_salt/Kv ifelse conditions — index expressions and index-set predicates cannot be named intermediates in esm, and the guard's kwup bound is a test parameter so the faq range cannot express it; both mirror the F90 structure |

## Test results across runners

| runner | result |
|---|---|
| Rust CLI (esm 0.7.0, the EqESM main `./esm` copy) | **417P / 0F / 0E** |
| Rust CLI (release v0.10.0 binary) | **417P / 0F / 0E** |
| Rust CLI (esm 0.12.1, EarthSciAST main — the binary the esm-2.0.0 corpus migration used) | **417P / 0F / 0E** |
| Python inline gate (`tools/run_esm_inline_tests.py`) | **49P / 0F / 372E** — every error is one of the two known python-runner limitation classes (shaped `parameter_overrides` do not resolve in the flattened python system: `Unresolved symbol: '…T_before'/'…h'/'…sw_pen_band'` — bflux 28E, frazil 52E, shortwave 78E; array-state/index-set-size handling: `index 75/76 is out of bounds for axis 0 with size 75/76` — kpp 158E, vertdiff 56E).  The same limitation classes are documented by the CICE and CISM ports; the Rust runner passes every one of these assertions.  Zero FAILs. |

`esm validate` passes on all ten files under all three Rust binaries (with
`ESD_ROOT` pointing at EarthSciDiscretizations main, as the upstream CI
does); `esm units` shows no `units_dimensionless_literal_mismatch` on any
file under either (the informational "consider SI base units" note on the
degC/ppt-carrying files is inherited from stage2 — degC and ppt are
accepted unit strings in esm 1.3.0).

## Next steps

1. A wider stage-1 window (warmer/more saline cells, unstable
   surfBuoyFlux, supercooled winter columns, liquid precipitation,
   shallow columns) to cover the untested branches above.
2. Mount into `eqesm.esm` with `earthsciintegrator` (stage 3) and compare
   against full-CESM runs; in the merged tree `mom6_bflux.esm` should
   consume `dT`, `penSW_bnd` and `leftover` by reference from
   `mom6_shortwave.esm` instead of the dump-sourced parameters.
3. Port the remaining MOM6 lanes (C-grid dynamics, surface forcing) when
   they clear review in the EqESM project.
