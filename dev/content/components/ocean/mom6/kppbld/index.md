---
title: "KPPBLD"
slug: "kppbld"
domains: ["ocean"]
component_types: ["model"]
subdomains: ["mom6"]
domain: "ocean"
subdomain: "mom6"
component_type: "model"
esm_version: "1.3.0"
esm_path: "components/ocean/mom6/mom6_kpp.esm"
reference: "https://github.com/ESCOMP/CESM"
description: "Stage-2 implementation of the MOM6 CVMix KPP planetary boundary layer parameterization (MOM6 dev/ncar_260909 @301879336, fork stage1/EqESM-cesm-mom6 branch instrument/mom6-dumps; run configuration C_JRA_t62_mom6_inst: RI_CRIT=0.3, VON_KARMAN=0.4, SURF_LAYER_EXTENT=0.1, MINIMUM_OBL_DEPTH=5.0, MINIMUM_VT2=1e-10, INTERP_TYPE=quadratic, INTERP_TYPE2=LMD94, MATCH_TECHNIQUE=MatchGradient, ENHANCE_DIFFUSION=False, NLT_SHAPE=CVMix, N_SMOOTH=3, COMPUTE_MONIN_OBUKHOV=True, COMPUTE_EKMAN=False, USE_KPP_LT_K/VT2=False, KPP_IS_ADDITIVE=False, KPP_SHORTWAVE_METHOD=MXL_SW, l_LMD_ws=false, lnoDGat1=true, all unit rescale factors 1.0). Two models: KPPBLD reproduces KPP_compute_BLD (MOM_CVMix_KPP.F90:1195-1575) down to the pre-smoothing OBL depth and kOBL — the surface-layer averages (F90:1342-1405), the per-assumed-OBL hydrostatic pressure for the Wright 1997 EOS (F90:1428-1440, the shared wright_rho composition of ./mom6_templates.esm, whose 15 coefficients are the wright_coeff_* constant fragments shared with mom6_eos.esm), deltaBuoy/N2/N (F90:1444-1457), w_s/Vt^2/BulkRi (F90:1509-1550 via the ./mom6_kpp_templates.esm laws), and OBL_depth_low/kOBL (cvmix_kpp.F90:1585-1814, 1821-1867) with the quadratic interpolation, the Monin-Obukhov limit, the minOBLdepth floor and the MOM6 top/bottom bounds. The column prefix sums of the geometry and hydrostatics — the interface depths depth (and so the heights z_inter = -depth and z_cell), and the reference pressure pRef = p_surf + PRESS_STEP*depth — are ESD integral operators lowered by the local ./mom6_column_discretization.esm rules (the EarthSciDiscretizations column_nonuniform_1d integral_lev_nodes_cumulative_from_bottom and integral_lev_cumulative_from_bottom imports, the exact exclusive-prefix and midpoint stencils of the Fortran iFaceHeight/cellHeight/pRef loops, F90:1237-1243 and F90:1452-1456; see README.md for the summation-order notes). KPPCoefs reproduces cvmix_coeffs_kpp_low (cvmix_kpp.F90:701-1298, not lStokesMOST, MatchGradient, ENHANCE_DIFFUSION=False: the no-match shape G(sigma) = sigma*(1-sigma)^2, the diffusivity/viscosity overwrite at interfaces 2..floor(kOBL), the KPP_IS_ADDITIVE=False replacement of nonzero entries via the kpp_override_nonzero template (Kd_salt = Kd_heat), and the CVMix non-local term) driven by the SMOOTHED OBLdepth/kOBL, z_inter, uStar, surfBuoyFlux (MXL_SW) and the incoming Kt/Ks/Kv from mom6_kpp.csv. Pins: mom6_kpp_obl.csv rows for BulkRi/deltaU2/N2 at layers 2..kOBL+3 (layer 1 is 0 by construction), spot z_cell at layers 1..kOBL+3 and z_inter at ifaces 2..kOBL+3 (iface 1 is the surface) plus the deep z_cell/z_inter at layer/iface 75, and OBLdepth/kOBL (rel 1e-12; the N_SMOOTH=3 Laplacian smoothing of KPP_smooth_BLD is inherently horizontal and is NOT reproduced — the pre-smoothing values are pinned and the smoothed values are consumed as inputs), and mom6_kpp.csv rows for Kd_heat/Kv at interfaces 2..kwup plus one pass-through Kv_out at kwup+1 (the kpp_override_nonzero else-branch). Unpinned (never exercised by the 156 traced columns; see README.md): the OBL_limit branch (no traced column has BulkRi <= 0.3 everywhere, kfirst = N_LAYER+1), the interpolated OBL depth of the kfirst = 2 and 3 rows (always floored to MINIMUM_OBL_DEPTH in the traces), the unstable (surfBuoyFlux < 0) branches of the stability functions and of the non-local term, the Langmuir enhancement paths, and the MINIMUM_VT2 floor."
tags: ["ocean", "mom6", "model", "kpp", "boundary-layer", "mixing", "cesm"]
---

## Description

Stage-2 implementation of the MOM6 CVMix KPP planetary boundary layer parameterization (MOM6 dev/ncar_260909 @301879336, fork stage1/EqESM-cesm-mom6 branch instrument/mom6-dumps; run configuration C_JRA_t62_mom6_inst: RI_CRIT=0.3, VON_KARMAN=0.4, SURF_LAYER_EXTENT=0.1, MINIMUM_OBL_DEPTH=5.0, MINIMUM_VT2=1e-10, INTERP_TYPE=quadratic, INTERP_TYPE2=LMD94, MATCH_TECHNIQUE=MatchGradient, ENHANCE_DIFFUSION=False, NLT_SHAPE=CVMix, N_SMOOTH=3, COMPUTE_MONIN_OBUKHOV=True, COMPUTE_EKMAN=False, USE_KPP_LT_K/VT2=False, KPP_IS_ADDITIVE=False, KPP_SHORTWAVE_METHOD=MXL_SW, l_LMD_ws=false, lnoDGat1=true, all unit rescale factors 1.0). Two models: KPPBLD reproduces KPP_compute_BLD (MOM_CVMix_KPP.F90:1195-1575) down to the pre-smoothing OBL depth and kOBL — the surface-layer averages (F90:1342-1405), the per-assumed-OBL hydrostatic pressure for the Wright 1997 EOS (F90:1428-1440, the shared wright_rho composition of ./mom6_templates.esm, whose 15 coefficients are the wright_coeff_* constant fragments shared with mom6_eos.esm), deltaBuoy/N2/N (F90:1444-1457), w_s/Vt^2/BulkRi (F90:1509-1550 via the ./mom6_kpp_templates.esm laws), and OBL_depth_low/kOBL (cvmix_kpp.F90:1585-1814, 1821-1867) with the quadratic interpolation, the Monin-Obukhov limit, the minOBLdepth floor and the MOM6 top/bottom bounds. The column prefix sums of the geometry and hydrostatics — the interface depths depth (and so the heights z_inter = -depth and z_cell), and the reference pressure pRef = p_surf + PRESS_STEP*depth — are ESD integral operators lowered by the local ./mom6_column_discretization.esm rules (the EarthSciDiscretizations column_nonuniform_1d integral_lev_nodes_cumulative_from_bottom and integral_lev_cumulative_from_bottom imports, the exact exclusive-prefix and midpoint stencils of the Fortran iFaceHeight/cellHeight/pRef loops, F90:1237-1243 and F90:1452-1456; see README.md for the summation-order notes). KPPCoefs reproduces cvmix_coeffs_kpp_low (cvmix_kpp.F90:701-1298, not lStokesMOST, MatchGradient, ENHANCE_DIFFUSION=False: the no-match shape G(sigma) = sigma*(1-sigma)^2, the diffusivity/viscosity overwrite at interfaces 2..floor(kOBL), the KPP_IS_ADDITIVE=False replacement of nonzero entries via the kpp_override_nonzero template (Kd_salt = Kd_heat), and the CVMix non-local term) driven by the SMOOTHED OBLdepth/kOBL, z_inter, uStar, surfBuoyFlux (MXL_SW) and the incoming Kt/Ks/Kv from mom6_kpp.csv. Pins: mom6_kpp_obl.csv rows for BulkRi/deltaU2/N2 at layers 2..kOBL+3 (layer 1 is 0 by construction), spot z_cell at layers 1..kOBL+3 and z_inter at ifaces 2..kOBL+3 (iface 1 is the surface) plus the deep z_cell/z_inter at layer/iface 75, and OBLdepth/kOBL (rel 1e-12; the N_SMOOTH=3 Laplacian smoothing of KPP_smooth_BLD is inherently horizontal and is NOT reproduced — the pre-smoothing values are pinned and the smoothed values are consumed as inputs), and mom6_kpp.csv rows for Kd_heat/Kv at interfaces 2..kwup plus one pass-through Kv_out at kwup+1 (the kpp_override_nonzero else-branch). Unpinned (never exercised by the 156 traced columns; see README.md): the OBL_limit branch (no traced column has BulkRi <= 0.3 everywhere, kfirst = N_LAYER+1), the interpolated OBL depth of the kfirst = 2 and 3 rows (always floored to MINIMUM_OBL_DEPTH in the traces), the unstable (surfBuoyFlux < 0) branches of the stability functions and of the non-local term, the Langmuir enhancement paths, and the MINIMUM_VT2 floor.

KPPBLD: The boundary-layer depth computation of KPP_compute_BLD (MOM_CVMix_KPP.F90:1195-1575) with the CVMix OBL_depth_low interpolation and the kOBL fraction (cvmix_kpp.F90:1585-1867). Inputs are the per-column traced state: layer thicknesses h and heights dz (equal in the instrumented run: no thickness inflation, min_thickness=0), temperature/salinity/velocity T, S, U_H, V_H, the surface buoyancy flux profile buoyFlux(1..76) (from calculateBuoyancyFlux2d, buoyFlux(N_IFACE) = 0), the surface friction velocity uStar and the surface pressure p_surf; outputs include the per-layer bulk Richardson numbers, the squared resolved shear and buoyancy frequency, the OBL depth and its fractional index. The EOS is applied as the wright_rho composition of ./mom6_templates.esm (one application per state: the surface-layer mean, the layer value and the layer-1 value, all at the layer-top pressure pRef), whose 15 Wright coefficients are the shared wright_coeff_* constant fragments (bound by reference, also in mom6_eos.esm's WrightEOS); the pointwise KPP laws come from ./mom6_kpp_templates.esm. The N_SMOOTH=3 horizontal Laplacian smoothing of KPP_smooth_BLD is not reproduced (single-column law); OBLdepth/kOBL here are the PRE-smoothing values (mom6_kpp_obl.csv).

KPPCoefs: The KPP diffusivity/viscosity/non-local coefficient computation of cvmix_coeffs_kpp_low (cvmix_kpp.F90:701-1298, not lStokesMOST) with the MOM6 wrappers of KPP_calculate (MOM_CVMix_KPP.F90:740-1067): inputs are the SMOOTHED OBLdepth/kOBL (after the N_SMOOTH=3 Laplacian of KPP_smooth_BLD, which is not reproduced here), the interface heights z_inter, uStar, the MXL_SW surface buoyancy flux surfBuoyFlux = buoyFlux(1) - buoyFlux(floor(kOBL)+1) (F90:848-853) and the incoming diffusivities Kt_in/Ks_in/Kv_in. With MATCH_TECHNIQUE=MatchGradient and ENHANCE_DIFFUSION=False, MOM6 zeroes the interior diffusivities before the CVMix call (F90:903-906), so the shape function is the no-match cubic G(sigma) = sigma*(1-sigma)^2 (G(1) = G'(1) = 0), and the overwrite loop 2..floor(kOBL) with the kwup==ktup zero restoration gives nonzero coefficients exactly on interfaces 2..floor(kOBL). KPP_IS_ADDITIVE=False: an output interface keeps the incoming value unless the KPP value is nonzero (F90:1023-1038). The non-local term is the CVMix law Tnonlocal = nonlocal_coeff*G(sigma) on interfaces 2..kwup when surfBuoyFlux < 0 (NLT_SHAPE=CVMix: MOM6 does not override), with nonlocal_coeff = Cstar*kappa*(kappa*eps*c_s)^(1/3), Cstar = 10; all traced columns are stable (surfBuoyFlux >= 0), so NLT is pinned at zero and the unstable branch is unpinned.

## Reference

- MOM6 (Modular Ocean Model 6), ESCOMP/CESM components/mom (dev/ncar_260909 @301879336; instrumented fork stage1/EqESM-cesm-mom6 branch instrument/mom6-dumps, reference run C_JRA_t62_mom6_inst): src/parameterizations/vertical/MOM_CVMix_KPP.F90 (KPP_compute_BLD 1195-1575, KPP_calculate 740-1067, KPP_smooth_BLD 1715-1834) and pkg/CVMix-src/src/shared/cvmix_kpp.F90 (OBL_depth_low 1585-1814, kOBL 1821-1867, coeffs_kpp_low 701-1298) - the reference implementation these components are transcribed from.
- EarthSciModels - the authoritative .esm corpus this component lives in.

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `h` | `m` | `0.0` | Layer thicknesses as consumed by the pRef hydrostatic sum (F90:1439-1440), [m] |
| `dz` | `m` | `0.0` | Layer heights used for the interface/cell geometry and the surface-layer delH (thickness_to_dz; equal to h in the instrumented run), [m] |
| `T` | `degC` | `0.0` |  |
| `S` | `ppt` | `0.0` |  |
| `U_H` | `m s^-1` | `0.0` | C-grid-averaged zonal velocity at T points (F90:1228-1229), [m s-1] |
| `V_H` | `m s^-1` | `0.0` |  |
| `buoyFlux` | `m^2 s^-3` | `0.0` | Surface buoyancy flux profile on interfaces, buoyFlux(N_IFACE) = 0 (calculateBuoyancyFlux2d), [m2 s-3] |
| `uStar` | `m s^-1` | `0.0` | Surface friction velocity (surfFricVel in MKS), [m s-1] |
| `p_surf` | `Pa` | `0.0` | Surface pressure tv%p_surf, [Pa] |
| `RI_CRIT` | `dimensionless` | `0.3` |  |
| `VON_KARMAN` | `dimensionless` | `0.4` |  |
| `SURF_LAYER_EXT` | `dimensionless` | `0.1` |  |
| `MIN_OBL_DEPTH` | `m` | `5.0` |  |
| `MIN_VTSQR` | `m^2 s^-2` | `1e-10` |  |
| `GORHO` | `m^4 s^-2 kg^-1` | `0.009468599033816427` | GoRho = g/rho0 with g = 9.8 m s-2 and rho0 = 1035 kg m-3 (GV%GoRho in MKS, Boussinesq), [m4 s-2 kg-1] |
| `PRESS_STEP` | `Pa m^-1` | `10143.0` | g_Earth*H_to_RZ = 9.8*1035 in MKS, the hydrostatic pressure increment per metre of layer thickness (F90:1439), [Pa m-1] |
| `ZETA_M` | `dimensionless` | `-0.2` | CVMix init zeta_m (cvmix_kpp.F90:369-371), [-] |
| `ZETA_S` | `dimensionless` | `-1.0` | CVMix init zeta_s (cvmix_kpp.F90:374-377), [-] |
| `A_M` | `dimensionless` | `1.2573615701844176` | a_m = (1-16*zeta_m)^(-1/4)*(1-4*zeta_m) at zeta_m = -0.2 (cvmix_kpp.F90:370), [-] |
| `C_M` | `dimensionless` | `8.382410467896117` | c_m = (1-16*zeta_m)^(-1/4)*12 (cvmix_kpp.F90:372), [-] |
| `A_S` | `dimensionless` | `-28.861739379323623` | a_s = sqrt(1-16*zeta_s)*(1+8*zeta_s) at zeta_s = -1 (cvmix_kpp.F90:374), [-] |
| `C_S` | `dimensionless` | `98.95453501482385` | c_s = 24*sqrt(1-16*zeta_s) (cvmix_kpp.F90:376), [-] |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `unit_layer` | `1` | `1.0` | The unit layer field, identically 1 on every layer: the dimensionless integrand of the column depth integrals depth(i) = integral(unit_layer, var: layer, lower: z_sfc, upper: iface) and their layer-centre form — the depth IS the integral of the layer-thickness measure dz, and the imported rules' where clause requires a layer-shaped integrand name (the ESD idiom for integral(1, dz)), [1] |
| `depth` | `m` | `0.0` | Interface depths below the surface, positive: depth(i) = integral_{z_sfc}^{iface i} dz = sum_{j<i} dz(j), the cumulative integral of the layer heights from the surface, lowered by the imported integral_lev_nodes_cumulative_from_bottom rule (the exact exclusive-prefix stencil of the Fortran iFaceHeight loop, F90:1238-1243; the shared integrand of z_inter = -depth and pRef = p_surf + PRESS_STEP*depth), [m] |
| `z_sfc` | `m` | `0.0` | Surface bound of the imported integral rules: the ocean surface coordinate ze(1) = 0 (the bound is a bare name in the integral node and carries no numeric weight in the lowering, esm-spec 4.2; declared for the free-name contract, as in cism_velo.esm), [m] |
| `z_top` | `m` | `0.0` | Bottom bound of the imported integral rules: the last-interface coordinate ze(N_IFACE) = depth(N_IFACE), the total column depth (measure-free bound of the integral node, esm-spec 4.2), [m] |
| `z_inter` | `m` | `0.0` | Interface heights referenced to the surface, negative in the ocean: z_inter(i) = -depth(i) with depth the cumulative integral of the layer heights (iFaceHeight in MKS, F90:1238-1243; the lowered rule reproduces the Fortran loop bit-for-bit), [m] |
| `z_cell` | `m` | `0.0` | Cell-center heights, negative in the ocean: z_cell(k) = -integral_{z_sfc}^{zc(k)} dz = -(sum_{j<k} dz(j) + dz(k)/2), the midpoint-rule cumulative integral from the surface to the layer centre, lowered by the imported integral_lev_cumulative_from_bottom rule (the exact stencil of cellHeight(k) = iFaceHeight(k) - 0.5*dh, F90:1237), [m] |
| `SLdepth` | `m` | `0.0` | Surface-layer depth for each assumed OBL depth: SLdepth_0d = surf_layer_ext*max(max(-z_cell(k), -z_inter(2)), minOBLdepth) (F90:1346), [m] |
| `delH` | `m` | `0.0` | Surface-layer thickness measure delH(k, kp) = min(max(SLdepth(k) + z_inter(kp), 0), dz(kp)); z_inter(kp) is the top interface of layer kp, so SLdepth + z_inter(kp) = SLdepth - (cumulative thickness above kp) and the closed form is bit-identical to the Fortran's running hTot accumulation (F90:1359-1375, Sterbenz: the crossing-layer sum reaches SLdepth exactly), [m] |
| `surfHtemp` | `degC m` | `0.0` |  |
| `surfHsalt` | `ppt m` | `0.0` |  |
| `surfHu` | `m^2 s^-1` | `0.0` |  |
| `surfHv` | `m^2 s^-1` | `0.0` |  |
| `surfT` | `degC` | `0.0` | Surface-layer-mean temperature for the assumed OBL depth at layer k (F90:1379; the sum runs over all 75 layers, delH = 0 beyond ksfc), [degC] |
| `surfS` | `ppt` | `0.0` |  |
| `surfU` | `m s^-1` | `0.0` |  |
| `surfV` | `m s^-1` | `0.0` |  |
| `pRef` | `Pa` | `0.0` | Hydrostatic pressure at the top of each layer (the running pRef of the KPP loop: pRef = p_surf, then per layer pRef = pRef + PRESS_STEP*h(k), F90:1282-1283 init and F90:1452-1456 update): pRef(i) = p_surf + PRESS_STEP*depth(i), the Boussinesq pressure at the interface depth, with depth the cumulative integral of the layer heights (PRESS_STEP = g_Earth*H_to_RZ = rho0*g under Boussinesq; the Fortran accumulates the per-layer products PRESS_STEP*h(k) onto p_surf in the k loop, while the integral form accumulates the layer heights first and then applies PRESS_STEP and adds p_surf — both factored out of the per-layer additions, so the rounding differs from the Fortran's summation order at ~1e-15 relative, measured on the pinned rows, see README.md), [Pa] |
| `rho_surf` | `kg m^-3` | `0.0` | In-situ density of the surface-layer mean (surfT, surfS) at the pressure at the top of layer k (rho_1D(kk+1), F90:1433-1436, 1442), via the wright_rho composition of the shared mom6_templates EOS (the al0/p0/lambda intermediates are internal to the template), [kg m-3] |
| `rho_k` | `kg m^-3` | `0.0` | In-situ density of layer k at the pressure at its top (rho_1D(kk), F90:1442), via wright_rho, [kg m-3] |
| `rho_km1` | `kg m^-3` | `0.0` | In-situ density of layer k-1 (clamped at layer 1) at the pressure at the top of layer k (rho_1D(kk-1), F90:1442), via wright_rho, [kg m-3] |
| `deltaBuoy` | `m s^-2` | `0.0` | Bulk buoyancy difference Br - B(z) = GoRho*(rho_k - rho_surf) (F90:1445-1448, Boussinesq), [m s-2] |
| `N2` | `s^-2` | `0.0` | Buoyancy frequency squared on interfaces 1..N_LAYER (N2_1d(k), F90:1449-1451). The N equation sets the bottom interface separately and caps the N2 gather at the last layer for eager evaluation. [s-2] |
| `N` | `s^-1` | `0.0` | Non-negative buoyancy frequency on interfaces, N(N_IFACE) = 0 (CS%N, F90:1452-1456), [s-1] |
| `B0` | `m^2 s^-3` | `0.0` | Surface buoyancy flux for the assumed OBL depth at layer k: B0(k) = buoyFlux(1) - buoyFlux(k+1) (surfBuoyFlux2(k), F90:1426-1427), [m2 s-3] |
| `Ws_1d` | `m s^-1` | `0.0` | Scalar turbulent velocity scale at sigma = 1 with OBL = -z_cell(k) and B0(k) (Ws_1d from CVMix_kpp_compute_turbulent_scales, F90:1509-1516), [m s-1] |
| `Uk` | `m s^-1` | `0.0` |  |
| `Vk` | `m s^-1` | `0.0` |  |
| `deltaU2` | `m^2 s^-2` | `0.0` | Square of the resolved surface-layer shear Uk^2 + Vk^2 (F90:1414), [m2 s-2] |
| `Vt2` | `m^2 s^-2` | `0.0` | Square of the unresolved shear (cvmix_kpp_compute_unresolved_shear, the NO_LANGMUIR_ENTRAINMENT branch), [m2 s-2] |
| `BulkRi` | `dimensionless` | `0.0` | Bulk Richardson number (cvmix_kpp_compute_bulk_Richardson), dimensionless |
| `OBL_limit` | `m` | `0.0` | The OBL limit: min(-z_cell(N_LAYER), Monin-Obukhov) with Monin-Obukhov = u*^3/(B0(N_LAYER)*kappa) when B0(N_LAYER) > 0 (cvmix_kpp.F90:1743-1761), [m] |
| `kfirst` | `dimensionless` | `0.0` | First layer (1-based) with BulkRi > RI_CRIT, or N_LAYER+1 when none (cvmix_kpp.F90:1765-1771), [-] |
| `slope` | `m^-1` | `0.0` | Slope of the OBL quadratic at x1 for the crossing layer k: (BulkRi(k-1)-BulkRi(k-2))/(z_cell(k-1)-z_cell(k-2)), zero for k <= 2 (the two-point case, cvmix_kpp.F90:1772-1779), [m-1] |
| `root` | `m` | `0.0` | Root of the OBL quadratic for crossing layer k (negative height), [m] |
| `OBLdepth_interp` | `m` | `0.0` | OBL depth from the CVMix interpolation before the minOBLdepth floor and the MOM6 top/bottom bounds (cvmix_kpp.F90:1765-1810), [m] |
| `OBLdepth` | `m` | `0.0` | The pre-smoothing boundary-layer depth: the CVMix value floored by minOBLdepth, bounded below by the top-layer interface and above by the bottom interface (F90:1557-1572), [m] |
| `kwfirst` | `dimensionless` | `0.0` | First interface (1-based) below the OBL depth, or N_LAYER+1 when none (cvmix_kpp.F90:1833-1841), [-] |
| `kOBL` | `dimensionless` | `0.0` | The fractional index of the OBL depth: kw + 0.25 when the OBL is above the cell center, kw + 0.75 below, N_LAYER + 0.75 when the OBL reaches the bottom (cvmix_kpp_compute_kOBL_depth, F90:1558), [-] |
| `quad_a2` | `dimensionless` | `0.0` | The constant coefficient a of the OBL-depth interpolation quadratic, already offset by -RI_CRIT (the CVMIX_MATH_INTERP_QUAD case of linear_through_cubic_poly_interp, cvmix_math.F90:103-138, with coeffs(1) = coeffs(1) - ri_crit, cvmix_kpp.F90:1799-1800): a = y1 - slope*x1 + c*x1^2 - RI_CRIT, from f(x1) = y1; dimensionless (Ri units), zero at k = 1 |
| `quad_b2` | `m^-1` | `0.0` | The linear coefficient b of the OBL-depth interpolation quadratic: b = slope - 2*c*x1, from f'(x1) = slope; [m-1] for the bulk-Richardson use, zero at k = 1 |
| `quad_c2` | `m^-2` | `0.0` | The quadratic coefficient c of the OBL-depth interpolation quadratic through (x1, y1), (x2, y2) with slope at x1 (the CVMIX_MATH_INTERP_QUAD case of linear_through_cubic_poly_interp, cvmix_math.F90:103-138): c = (y2 - y1 - slope*(x2 - x1))/(x2 - x1)^2; [m-2] for the bulk-Richardson use, zero at k = 1 |

## Observed expressions

$$
unit_{layer} = \mathrm{const}\left(\right)
$$
_The unit layer field, identically 1 on every layer: the dimensionless integrand of the column depth integrals depth(i) = integral(unit_layer, var: layer, lower: z_sfc, upper: iface) and their layer-centre form — the depth IS the integral of the layer-thickness measure dz, and the imported rules' where clause requires a layer-shaped integrand name (the ESD idiom for integral(1, dz)), [1]_

$$
depth = \mathrm{integral}\left(unit_{layer}\right)
$$
_Interface depths below the surface, positive: depth(i) = integral_{z_sfc}^{iface i} dz = sum_{j<i} dz(j), the cumulative integral of the layer heights from the surface, lowered by the imported integral_lev_nodes_cumulative_from_bottom rule (the exact exclusive-prefix stencil of the Fortran iFaceHeight loop, F90:1238-1243; the shared integrand of z_inter = -depth and pRef = p_surf + PRESS_STEP*depth), [m]_

$$
z_{sfc} = \mathrm{const}\left(\right)
$$
_Surface bound of the imported integral rules: the ocean surface coordinate ze(1) = 0 (the bound is a bare name in the integral node and carries no numeric weight in the lowering, esm-spec 4.2; declared for the free-name contract, as in cism_velo.esm), [m]_

$$
z_{top} = \mathrm{index}\left(depth, N_{IFACE}\right)
$$
_Bottom bound of the imported integral rules: the last-interface coordinate ze(N_IFACE) = depth(N_IFACE), the total column depth (measure-free bound of the integral node, esm-spec 4.2), [m]_

$$
z_{inter} = -depth
$$
_Interface heights referenced to the surface, negative in the ocean: z_inter(i) = -depth(i) with depth the cumulative integral of the layer heights (iFaceHeight in MKS, F90:1238-1243; the lowered rule reproduces the Fortran loop bit-for-bit), [m]_

$$
z_{cell} = -\mathrm{integral}\left(unit_{layer}\right)
$$
_Cell-center heights, negative in the ocean: z_cell(k) = -integral_{z_sfc}^{zc(k)} dz = -(sum_{j<k} dz(j) + dz(k)/2), the midpoint-rule cumulative integral from the surface to the layer centre, lowered by the imported integral_lev_cumulative_from_bottom rule (the exact stencil of cellHeight(k) = iFaceHeight(k) - 0.5*dh, F90:1237), [m]_

$$
SLdepth = \mathrm{faq}\left(z_{cell}, z_{inter}\right)
$$
_Surface-layer depth for each assumed OBL depth: SLdepth_0d = surf_layer_ext*max(max(-z_cell(k), -z_inter(2)), minOBLdepth) (F90:1346), [m]_

$$
delH = \mathrm{faq}\left(SLdepth, z_{inter}, dz\right)
$$
_Surface-layer thickness measure delH(k, kp) = min(max(SLdepth(k) + z_inter(kp), 0), dz(kp)); z_inter(kp) is the top interface of layer kp, so SLdepth + z_inter(kp) = SLdepth - (cumulative thickness above kp) and the closed form is bit-identical to the Fortran's running hTot accumulation (F90:1359-1375, Sterbenz: the crossing-layer sum reaches SLdepth exactly), [m]_

$$
surfHtemp = \mathrm{faq}\left(delH, T\right)
$$

$$
surfHsalt = \mathrm{faq}\left(delH, S\right)
$$

$$
surfHu = \mathrm{faq}\left(delH, U_{H}\right)
$$

$$
surfHv = \mathrm{faq}\left(delH, V_{H}\right)
$$

$$
surfT = \mathrm{faq}\left(surfHtemp, SLdepth\right)
$$
_Surface-layer-mean temperature for the assumed OBL depth at layer k (F90:1379; the sum runs over all 75 layers, delH = 0 beyond ksfc), [degC]_

$$
surfS = \mathrm{faq}\left(surfHsalt, SLdepth\right)
$$

$$
surfU = \mathrm{faq}\left(surfHu, SLdepth\right)
$$

$$
surfV = \mathrm{faq}\left(surfHv, SLdepth\right)
$$

$$
pRef = \mathrm{faq}\left(depth\right)
$$
_Hydrostatic pressure at the top of each layer (the running pRef of the KPP loop: pRef = p_surf, then per layer pRef = pRef + PRESS_STEP*h(k), F90:1282-1283 init and F90:1452-1456 update): pRef(i) = p_surf + PRESS_STEP*depth(i), the Boussinesq pressure at the interface depth, with depth the cumulative integral of the layer heights (PRESS_STEP = g_Earth*H_to_RZ = rho0*g under Boussinesq; the Fortran accumulates the per-layer products PRESS_STEP*h(k) onto p_surf in the k loop, while the integral form accumulates the layer heights first and then applies PRESS_STEP and adds p_surf — both factored out of the per-layer additions, so the rounding differs from the Fortran's summation order at ~1e-15 relative, measured on the pinned rows, see README.md), [Pa]_

$$
rho_{surf} = \mathrm{faq}\left(surfT, surfS, pRef\right)
$$
_In-situ density of the surface-layer mean (surfT, surfS) at the pressure at the top of layer k (rho_1D(kk+1), F90:1433-1436, 1442), via the wright_rho composition of the shared mom6_templates EOS (the al0/p0/lambda intermediates are internal to the template), [kg m-3]_

$$
rho_{k} = \mathrm{faq}\left(T, S, pRef\right)
$$
_In-situ density of layer k at the pressure at its top (rho_1D(kk), F90:1442), via wright_rho, [kg m-3]_

$$
rho_{km1} = \mathrm{faq}\left(T, S, pRef\right)
$$
_In-situ density of layer k-1 (clamped at layer 1) at the pressure at the top of layer k (rho_1D(kk-1), F90:1442), via wright_rho, [kg m-3]_

$$
deltaBuoy = \mathrm{faq}\left(rho_{k}, rho_{surf}\right)
$$
_Bulk buoyancy difference Br - B(z) = GoRho*(rho_k - rho_surf) (F90:1445-1448, Boussinesq), [m s-2]_

$$
N2 = \mathrm{faq}\left(rho_{k}, rho_{km1}, h\right)
$$
_Buoyancy frequency squared on interfaces 1..N_LAYER (N2_1d(k), F90:1449-1451). The N equation sets the bottom interface separately and caps the N2 gather at the last layer for eager evaluation. [s-2]_

$$
N = \mathrm{faq}\left(N2\right)
$$
_Non-negative buoyancy frequency on interfaces, N(N_IFACE) = 0 (CS%N, F90:1452-1456), [s-1]_

$$
B0 = \mathrm{faq}\left(buoyFlux\right)
$$
_Surface buoyancy flux for the assumed OBL depth at layer k: B0(k) = buoyFlux(1) - buoyFlux(k+1) (surfBuoyFlux2(k), F90:1426-1427), [m2 s-3]_

$$
Ws_{1d} = \mathrm{faq}\left(z_{cell}, B0\right)
$$
_Scalar turbulent velocity scale at sigma = 1 with OBL = -z_cell(k) and B0(k) (Ws_1d from CVMix_kpp_compute_turbulent_scales, F90:1509-1516), [m s-1]_

$$
Uk = \mathrm{faq}\left(U_{H}, surfU\right)
$$

$$
Vk = \mathrm{faq}\left(V_{H}, surfV\right)
$$

$$
deltaU2 = \mathrm{faq}\left(Uk, Vk\right)
$$
_Square of the resolved surface-layer shear Uk^2 + Vk^2 (F90:1414), [m2 s-2]_

$$
Vt2 = \mathrm{faq}\left(z_{cell}, N, Ws_{1d}\right)
$$
_Square of the unresolved shear (cvmix_kpp_compute_unresolved_shear, the NO_LANGMUIR_ENTRAINMENT branch), [m2 s-2]_

$$
BulkRi = \mathrm{faq}\left(z_{cell}, deltaBuoy, deltaU2, Vt2\right)
$$
_Bulk Richardson number (cvmix_kpp_compute_bulk_Richardson), dimensionless_

$$
OBL_{limit} = \mathrm{ifelse}\left(\mathrm{>}\left(\mathrm{index}\left(B0, N_{LAYER}\right), \mathrm{const}\left(\right)\right), \mathrm{min}\left(-\mathrm{index}\left(z_{cell}, N_{LAYER}\right), \frac{uStar \cdot uStar \cdot uStar}{\mathrm{index}\left(B0, N_{LAYER}\right) \cdot VON_{KARMAN}}\right), -\mathrm{index}\left(z_{cell}, N_{LAYER}\right)\right)
$$
_The OBL limit: min(-z_cell(N_LAYER), Monin-Obukhov) with Monin-Obukhov = u*^3/(B0(N_LAYER)*kappa) when B0(N_LAYER) > 0 (cvmix_kpp.F90:1743-1761), [m]_

$$
kfirst = \mathrm{faq}\left(BulkRi\right)
$$
_First layer (1-based) with BulkRi > RI_CRIT, or N_LAYER+1 when none (cvmix_kpp.F90:1765-1771), [-]_

$$
slope = \mathrm{faq}\left(BulkRi, z_{cell}\right)
$$
_Slope of the OBL quadratic at x1 for the crossing layer k: (BulkRi(k-1)-BulkRi(k-2))/(z_cell(k-1)-z_cell(k-2)), zero for k <= 2 (the two-point case, cvmix_kpp.F90:1772-1779), [m-1]_

$$
root = \mathrm{faq}\left(quad_{a2}, quad_{b2}, quad_{c2}, z_{cell}\right)
$$
_Root of the OBL quadratic for crossing layer k (negative height), [m]_

$$
OBLdepth_{interp} = \mathrm{ifelse}\left(kfirst = N_{IFACE}, OBL_{limit}, \mathrm{ifelse}\left(kfirst = 1.0, -\mathrm{index}\left(z_{cell}, 1\right), \mathrm{min}\left(\mathrm{ifelse}\left(kfirst = 2.0, \mathrm{max}\left(-\mathrm{index}\left(root, \mathrm{min}\left(kfirst, N_{LAYER}\right)\right), -\mathrm{index}\left(z_{cell}, 1\right)\right), -\mathrm{index}\left(root, \mathrm{min}\left(kfirst, N_{LAYER}\right)\right)\right), OBL_{limit}\right)\right)\right)
$$
_OBL depth from the CVMix interpolation before the minOBLdepth floor and the MOM6 top/bottom bounds (cvmix_kpp.F90:1765-1810), [m]_

$$
OBLdepth = \mathrm{min}\left(-\mathrm{index}\left(z_{inter}, N_{IFACE}\right), \mathrm{max}\left(-\mathrm{index}\left(z_{inter}, 2\right), \mathrm{max}\left(MIN_{OBL\,DEPTH}, OBLdepth_{interp}\right)\right)\right)
$$
_The pre-smoothing boundary-layer depth: the CVMix value floored by minOBLdepth, bounded below by the top-layer interface and above by the bottom interface (F90:1557-1572), [m]_

$$
kwfirst = \mathrm{faq}\left(z_{inter}\right)
$$
_First interface (1-based) below the OBL depth, or N_LAYER+1 when none (cvmix_kpp.F90:1833-1841), [-]_

$$
kOBL = \mathrm{ifelse}\left(kwfirst = N_{IFACE}, N_{LAYER} + 0.75, kwfirst + \mathrm{ifelse}\left(\mathrm{<}\left(OBLdepth, -\mathrm{index}\left(z_{cell}, \mathrm{min}\left(kwfirst, N_{LAYER}\right)\right)\right), 0.25, 0.75\right)\right)
$$
_The fractional index of the OBL depth: kw + 0.25 when the OBL is above the cell center, kw + 0.75 below, N_LAYER + 0.75 when the OBL reaches the bottom (cvmix_kpp_compute_kOBL_depth, F90:1558), [-]_

$$
quad_{a2} = \mathrm{faq}\left(z_{cell}, BulkRi, slope, quad_{c2}\right)
$$
_The constant coefficient a of the OBL-depth interpolation quadratic, already offset by -RI_CRIT (the CVMIX_MATH_INTERP_QUAD case of linear_through_cubic_poly_interp, cvmix_math.F90:103-138, with coeffs(1) = coeffs(1) - ri_crit, cvmix_kpp.F90:1799-1800): a = y1 - slope*x1 + c*x1^2 - RI_CRIT, from f(x1) = y1; dimensionless (Ri units), zero at k = 1_

$$
quad_{b2} = \mathrm{faq}\left(z_{cell}, slope, quad_{c2}\right)
$$
_The linear coefficient b of the OBL-depth interpolation quadratic: b = slope - 2*c*x1, from f'(x1) = slope; [m-1] for the bulk-Richardson use, zero at k = 1_

$$
quad_{c2} = \mathrm{faq}\left(z_{cell}, BulkRi, slope\right)
$$
_The quadratic coefficient c of the OBL-depth interpolation quadratic through (x1, y1), (x2, y2) with slope at x1 (the CVMIX_MATH_INTERP_QUAD case of linear_through_cubic_poly_interp, cvmix_math.F90:103-138): c = (y2 - y1 - slope*(x2 - x1))/(x2 - x1)^2; [m-2] for the bulk-Richardson use, zero at k = 1_

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "expression_template_imports": [
    {
      "ref": "./mom6_column_discretization.esm"
    },
    {
      "ref": "./mom6_kpp_templates.esm"
    },
    {
      "ref": "./mom6_templates.esm"
    }
  ],
  "variables": {
    "h": {
      "type": "parameter",
      "shape": [
        "layer"
      ],
      "units": "m",
      "default": 0.0,
      "description": "Layer thicknesses as consumed by the pRef hydrostatic sum (F90:1439-1440), [m]"
    },
    "dz": {
      "type": "parameter",
      "shape": [
        "layer"
      ],
      "units": "m",
      "default": 0.0,
      "description": "Layer heights used for the interface/cell geometry and the surface-layer delH (thickness_to_dz; equal to h in the instrumented run), [m]"
    },
    "T": {
      "type": "parameter",
      "shape": [
        "layer"
      ],
      "units": "degC",
      "default": 0.0
    },
    "S": {
      "type": "parameter",
      "shape": [
        "layer"
      ],
      "units": "ppt",
      "default": 0.0
    },
    "U_H": {
      "type": "parameter",
      "shape": [
        "layer"
      ],
      "units": "m s^-1",
      "default": 0.0,
      "description": "C-grid-averaged zonal velocity at T points (F90:1228-1229), [m s-1]"
    },
    "V_H": {
      "type": "parameter",
      "shape": [
        "layer"
      ],
      "units": "m s^-1",
      "default": 0.0
    },
    "buoyFlux": {
      "type": "parameter",
      "shape": [
        "iface"
      ],
      "units": "m^2 s^-3",
      "default": 0.0,
      "description": "Surface buoyancy flux profile on interfaces, buoyFlux(N_IFACE) = 0 (calculateBuoyancyFlux2d), [m2 s-3]"
    },
    "uStar": {
      "type": "parameter",
      "units": "m s^-1",
      "default": 0.0,
      "description": "Surface friction velocity (surfFricVel in MKS), [m s-1]"
    },
    "p_surf": {
      "type": "parameter",
      "units": "Pa",
      "default": 0.0,
      "description": "Surface pressure tv%p_surf, [Pa]"
    },
    "RI_CRIT": {
      "type": "parameter",
      "units": "dimensionless",
      "default": 0.3
    },
    "VON_KARMAN": {
      "type": "parameter",
      "units": "dimensionless",
      "default": 0.4
    },
    "SURF_LAYER_EXT": {
      "type": "parameter",
      "units": "dimensionless",
      "default": 0.1
    },
    "MIN_OBL_DEPTH": {
      "type": "parameter",
      "units": "m",
      "default": 5.0
    },
    "MIN_VTSQR": {
      "type": "parameter",
      "units": "m^2 s^-2",
      "default": 1e-10
    },
    "GORHO": {
      "type": "parameter",
      "units": "m^4 s^-2 kg^-1",
      "default": 0.009468599033816427,
      "description": "GoRho = g/rho0 with g = 9.8 m s-2 and rho0 = 1035 kg m-3 (GV%GoRho in MKS, Boussinesq), [m4 s-2 kg-1]"
    },
    "PRESS_STEP": {
      "type": "parameter",
      "units": "Pa m^-1",
      "default": 10143.0,
      "description": "g_Earth*H_to_RZ = 9.8*1035 in MKS, the hydrostatic pressure increment per metre of layer thickness (F90:1439), [Pa m-1]"
    },
    "ZETA_M": {
      "type": "parameter",
      "units": "dimensionless",
      "default": -0.2,
      "description": "CVMix init zeta_m (cvmix_kpp.F90:369-371), [-]"
    },
    "ZETA_S": {
      "type": "parameter",
      "units": "dimensionless",
      "default": -1.0,
      "description": "CVMix init zeta_s (cvmix_kpp.F90:374-377), [-]"
    },
    "A_M": {
      "type": "parameter",
      "units": "dimensionless",
      "default": 1.2573615701844176,
      "description": "a_m = (1-16*zeta_m)^(-1/4)*(1-4*zeta_m) at zeta_m = -0.2 (cvmix_kpp.F90:370), [-]"
    },
    "C_M": {
      "type": "parameter",
      "units": "dimensionless",
      "default": 8.382410467896117,
      "description": "c_m = (1-16*zeta_m)^(-1/4)*12 (cvmix_kpp.F90:372), [-]"
    },
    "A_S": {
      "type": "parameter",
      "units": "dimensionless",
      "default": -28.861739379323623,
      "description": "a_s = sqrt(1-16*zeta_s)*(1+8*zeta_s) at zeta_s = -1 (cvmix_kpp.F90:374), [-]"
    },
    "C_S": {
      "type": "parameter",
      "units": "dimensionless",
      "default": 98.95453501482385,
      "description": "c_s = 24*sqrt(1-16*zeta_s) (cvmix_kpp.F90:376), [-]"
    },
    "unit_layer": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "1",
      "default": 1.0,
      "description": "The unit layer field, identically 1 on every layer: the dimensionless integrand of the column depth integrals depth(i) = integral(unit_layer, var: layer, lower: z_sfc, upper: iface) and their layer-centre form — the depth IS the integral of the layer-thickness measure dz, and the imported rules' where clause requires a layer-shaped integrand name (the ESD idiom for integral(1, dz)), [1]"
    },
    "depth": {
      "type": "unknown",
      "shape": [
        "iface"
      ],
      "units": "m",
      "default": 0.0,
      "description": "Interface depths below the surface, positive: depth(i) = integral_{z_sfc}^{iface i} dz = sum_{j<i} dz(j), the cumulative integral of the layer heights from the surface, lowered by the imported integral_lev_nodes_cumulative_from_bottom rule (the exact exclusive-prefix stencil of the Fortran iFaceHeight loop, F90:1238-1243; the shared integrand of z_inter = -depth and pRef = p_surf + PRESS_STEP*depth), [m]"
    },
    "z_sfc": {
      "type": "unknown",
      "units": "m",
      "default": 0.0,
      "description": "Surface bound of the imported integral rules: the ocean surface coordinate ze(1) = 0 (the bound is a bare name in the integral node and carries no numeric weight in the lowering, esm-spec 4.2; declared for the free-name contract, as in cism_velo.esm), [m]"
    },
    "z_top": {
      "type": "unknown",
      "units": "m",
      "default": 0.0,
      "description": "Bottom bound of the imported integral rules: the last-interface coordinate ze(N_IFACE) = depth(N_IFACE), the total column depth (measure-free bound of the integral node, esm-spec 4.2), [m]"
    },
    "z_inter": {
      "type": "unknown",
      "shape": [
        "iface"
      ],
      "units": "m",
      "default": 0.0,
      "description": "Interface heights referenced to the surface, negative in the ocean: z_inter(i) = -depth(i) with depth the cumulative integral of the layer heights (iFaceHeight in MKS, F90:1238-1243; the lowered rule reproduces the Fortran loop bit-for-bit), [m]"
    },
    "z_cell": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "m",
      "default": 0.0,
      "description": "Cell-center heights, negative in the ocean: z_cell(k) = -integral_{z_sfc}^{zc(k)} dz = -(sum_{j<k} dz(j) + dz(k)/2), the midpoint-rule cumulative integral from the surface to the layer centre, lowered by the imported integral_lev_cumulative_from_bottom rule (the exact stencil of cellHeight(k) = iFaceHeight(k) - 0.5*dh, F90:1237), [m]"
    },
    "SLdepth": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "m",
      "default": 0.0,
      "description": "Surface-layer depth for each assumed OBL depth: SLdepth_0d = surf_layer_ext*max(max(-z_cell(k), -z_inter(2)), minOBLdepth) (F90:1346), [m]"
    },
    "delH": {
      "type": "unknown",
      "shape": [
        "layer",
        "layer"
      ],
      "units": "m",
      "default": 0.0,
      "description": "Surface-layer thickness measure delH(k, kp) = min(max(SLdepth(k) + z_inter(kp), 0), dz(kp)); z_inter(kp) is the top interface of layer kp, so SLdepth + z_inter(kp) = SLdepth - (cumulative thickness above kp) and the closed form is bit-identical to the Fortran's running hTot accumulation (F90:1359-1375, Sterbenz: the crossing-layer sum reaches SLdepth exactly), [m]"
    },
    "surfHtemp": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "degC m",
      "default": 0.0
    },
    "surfHsalt": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "ppt m",
      "default": 0.0
    },
    "surfHu": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "m^2 s^-1",
      "default": 0.0
    },
    "surfHv": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "m^2 s^-1",
      "default": 0.0
    },
    "surfT": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "degC",
      "default": 0.0,
      "description": "Surface-layer-mean temperature for the assumed OBL depth at layer k (F90:1379; the sum runs over all 75 layers, delH = 0 beyond ksfc), [degC]"
    },
    "surfS": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "ppt",
      "default": 0.0
    },
    "surfU": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "m s^-1",
      "default": 0.0
    },
    "surfV": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "m s^-1",
      "default": 0.0
    },
    "pRef": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "Pa",
      "default": 0.0,
      "description": "Hydrostatic pressure at the top of each layer (the running pRef of the KPP loop: pRef = p_surf, then per layer pRef = pRef + PRESS_STEP*h(k), F90:1282-1283 init and F90:1452-1456 update): pRef(i) = p_surf + PRESS_STEP*depth(i), the Boussinesq pressure at the interface depth, with depth the cumulative integral of the layer heights (PRESS_STEP = g_Earth*H_to_RZ = rho0*g under Boussinesq; the Fortran accumulates the per-layer products PRESS_STEP*h(k) onto p_surf in the k loop, while the integral form accumulates the layer heights first and then applies PRESS_STEP and adds p_surf — both factored out of the per-layer additions, so the rounding differs from the Fortran's summation order at ~1e-15 relative, measured on the pinned rows, see README.md), [Pa]"
    },
    "rho_surf": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "kg m^-3",
      "default": 0.0,
      "description": "In-situ density of the surface-layer mean (surfT, surfS) at the pressure at the top of layer k (rho_1D(kk+1), F90:1433-1436, 1442), via the wright_rho composition of the shared mom6_templates EOS (the al0/p0/lambda intermediates are internal to the template), [kg m-3]"
    },
    "rho_k": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "kg m^-3",
      "default": 0.0,
      "description": "In-situ density of layer k at the pressure at its top (rho_1D(kk), F90:1442), via wright_rho, [kg m-3]"
    },
    "rho_km1": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "kg m^-3",
      "default": 0.0,
      "description": "In-situ density of layer k-1 (clamped at layer 1) at the pressure at the top of layer k (rho_1D(kk-1), F90:1442), via wright_rho, [kg m-3]"
    },
    "deltaBuoy": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "m s^-2",
      "default": 0.0,
      "description": "Bulk buoyancy difference Br - B(z) = GoRho*(rho_k - rho_surf) (F90:1445-1448, Boussinesq), [m s-2]"
    },
    "N2": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "s^-2",
      "default": 0.0,
      "description": "Buoyancy frequency squared on interfaces 1..N_LAYER (N2_1d(k), F90:1449-1451). The N equation sets the bottom interface separately and caps the N2 gather at the last layer for eager evaluation. [s-2]"
    },
    "N": {
      "type": "unknown",
      "shape": [
        "iface"
      ],
      "units": "s^-1",
      "default": 0.0,
      "description": "Non-negative buoyancy frequency on interfaces, N(N_IFACE) = 0 (CS%N, F90:1452-1456), [s-1]"
    },
    "B0": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "m^2 s^-3",
      "default": 0.0,
      "description": "Surface buoyancy flux for the assumed OBL depth at layer k: B0(k) = buoyFlux(1) - buoyFlux(k+1) (surfBuoyFlux2(k), F90:1426-1427), [m2 s-3]"
    },
    "Ws_1d": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "m s^-1",
      "default": 0.0,
      "description": "Scalar turbulent velocity scale at sigma = 1 with OBL = -z_cell(k) and B0(k) (Ws_1d from CVMix_kpp_compute_turbulent_scales, F90:1509-1516), [m s-1]"
    },
    "Uk": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "m s^-1",
      "default": 0.0
    },
    "Vk": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "m s^-1",
      "default": 0.0
    },
    "deltaU2": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "m^2 s^-2",
      "default": 0.0,
      "description": "Square of the resolved surface-layer shear Uk^2 + Vk^2 (F90:1414), [m2 s-2]"
    },
    "Vt2": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "m^2 s^-2",
      "default": 0.0,
      "description": "Square of the unresolved shear (cvmix_kpp_compute_unresolved_shear, the NO_LANGMUIR_ENTRAINMENT branch), [m2 s-2]"
    },
    "BulkRi": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "dimensionless",
      "default": 0.0,
      "description": "Bulk Richardson number (cvmix_kpp_compute_bulk_Richardson), dimensionless"
    },
    "OBL_limit": {
      "type": "unknown",
      "units": "m",
      "default": 0.0,
      "description": "The OBL limit: min(-z_cell(N_LAYER), Monin-Obukhov) with Monin-Obukhov = u*^3/(B0(N_LAYER)*kappa) when B0(N_LAYER) > 0 (cvmix_kpp.F90:1743-1761), [m]"
    },
    "kfirst": {
      "type": "unknown",
      "units": "dimensionless",
      "default": 0.0,
      "description": "First layer (1-based) with BulkRi > RI_CRIT, or N_LAYER+1 when none (cvmix_kpp.F90:1765-1771), [-]"
    },
    "slope": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "m^-1",
      "default": 0.0,
      "description": "Slope of the OBL quadratic at x1 for the crossing layer k: (BulkRi(k-1)-BulkRi(k-2))/(z_cell(k-1)-z_cell(k-2)), zero for k <= 2 (the two-point case, cvmix_kpp.F90:1772-1779), [m-1]"
    },
    "root": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "m",
      "default": 0.0,
      "description": "Root of the OBL quadratic for crossing layer k (negative height), [m]"
    },
    "OBLdepth_interp": {
      "type": "unknown",
      "units": "m",
      "default": 0.0,
      "description": "OBL depth from the CVMix interpolation before the minOBLdepth floor and the MOM6 top/bottom bounds (cvmix_kpp.F90:1765-1810), [m]"
    },
    "OBLdepth": {
      "type": "unknown",
      "units": "m",
      "default": 0.0,
      "description": "The pre-smoothing boundary-layer depth: the CVMix value floored by minOBLdepth, bounded below by the top-layer interface and above by the bottom interface (F90:1557-1572), [m]"
    },
    "kwfirst": {
      "type": "unknown",
      "units": "dimensionless",
      "default": 0.0,
      "description": "First interface (1-based) below the OBL depth, or N_LAYER+1 when none (cvmix_kpp.F90:1833-1841), [-]"
    },
    "kOBL": {
      "type": "unknown",
      "units": "dimensionless",
      "default": 0.0,
      "description": "The fractional index of the OBL depth: kw + 0.25 when the OBL is above the cell center, kw + 0.75 below, N_LAYER + 0.75 when the OBL reaches the bottom (cvmix_kpp_compute_kOBL_depth, F90:1558), [-]"
    },
    "quad_a2": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "dimensionless",
      "default": 0.0,
      "description": "The constant coefficient a of the OBL-depth interpolation quadratic, already offset by -RI_CRIT (the CVMIX_MATH_INTERP_QUAD case of linear_through_cubic_poly_interp, cvmix_math.F90:103-138, with coeffs(1) = coeffs(1) - ri_crit, cvmix_kpp.F90:1799-1800): a = y1 - slope*x1 + c*x1^2 - RI_CRIT, from f(x1) = y1; dimensionless (Ri units), zero at k = 1"
    },
    "quad_b2": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "m^-1",
      "default": 0.0,
      "description": "The linear coefficient b of the OBL-depth interpolation quadratic: b = slope - 2*c*x1, from f'(x1) = slope; [m-1] for the bulk-Richardson use, zero at k = 1"
    },
    "quad_c2": {
      "type": "unknown",
      "shape": [
        "layer"
      ],
      "units": "m^-2",
      "default": 0.0,
      "description": "The quadratic coefficient c of the OBL-depth interpolation quadratic through (x1, y1), (x2, y2) with slope at x1 (the CVMIX_MATH_INTERP_QUAD case of linear_through_cubic_poly_interp, cvmix_math.F90:103-138): c = (y2 - y1 - slope*(x2 - x1))/(x2 - x1)^2; [m-2] for the bulk-Richardson use, zero at k = 1"
    }
  },
  "equations": [
    {
      "lhs": "unit_layer",
      "rhs": {
        "op": "const",
        "args": [],
        "value": 1.0,
        "units": "1"
      }
    },
    {
      "lhs": "depth",
      "rhs": {
        "op": "integral",
        "args": [
          "unit_layer"
        ],
        "var": "layer",
        "lower": "z_sfc",
        "upper": "iface"
      }
    },
    {
      "lhs": "z_sfc",
      "rhs": {
        "op": "const",
        "args": [],
        "value": 0.0,
        "units": "m"
      }
    },
    {
      "lhs": "z_top",
      "rhs": {
        "op": "index",
        "args": [
          "depth",
          "N_IFACE"
        ]
      }
    },
    {
      "lhs": "z_inter",
      "rhs": {
        "op": "-",
        "args": [
          "depth"
        ]
      }
    },
    {
      "lhs": "z_cell",
      "rhs": {
        "op": "-",
        "args": [
          {
            "op": "integral",
            "args": [
              "unit_layer"
            ],
            "var": "layer",
            "lower": "z_sfc",
            "upper": "layer"
          }
        ]
      }
    },
    {
      "lhs": "SLdepth",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "*",
          "args": [
            "SURF_LAYER_EXT",
            {
              "op": "max",
              "args": [
                {
                  "op": "max",
                  "args": [
                    {
                      "op": "-",
                      "args": [
                        {
                          "op": "index",
                          "args": [
                            "z_cell",
                            "i"
                          ]
                        }
                      ]
                    },
                    {
                      "op": "-",
                      "args": [
                        {
                          "op": "index",
                          "args": [
                            "z_inter",
                            2
                          ]
                        }
                      ]
                    }
                  ]
                },
                "MIN_OBL_DEPTH"
              ]
            }
          ]
        },
        "args": [
          "z_cell",
          "z_inter"
        ]
      }
    },
    {
      "lhs": "delH",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i",
          "j"
        ],
        "ranges": {
          "i": {
            "from": "layer"
          },
          "j": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "min",
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
                  "op": "+",
                  "args": [
                    {
                      "op": "index",
                      "args": [
                        "SLdepth",
                        "i"
                      ]
                    },
                    {
                      "op": "index",
                      "args": [
                        "z_inter",
                        "j"
                      ]
                    }
                  ]
                }
              ]
            },
            {
              "op": "index",
              "args": [
                "dz",
                "j"
              ]
            }
          ]
        },
        "args": [
          "SLdepth",
          "z_inter",
          "dz"
        ]
      }
    },
    {
      "lhs": "surfHtemp",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "layer"
          },
          "j": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "*",
          "args": [
            {
              "op": "index",
              "args": [
                "delH",
                "i",
                "j"
              ]
            },
            {
              "op": "index",
              "args": [
                "T",
                "j"
              ]
            }
          ]
        },
        "args": [
          "delH",
          "T"
        ]
      }
    },
    {
      "lhs": "surfHsalt",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "layer"
          },
          "j": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "*",
          "args": [
            {
              "op": "index",
              "args": [
                "delH",
                "i",
                "j"
              ]
            },
            {
              "op": "index",
              "args": [
                "S",
                "j"
              ]
            }
          ]
        },
        "args": [
          "delH",
          "S"
        ]
      }
    },
    {
      "lhs": "surfHu",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "layer"
          },
          "j": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "*",
          "args": [
            {
              "op": "index",
              "args": [
                "delH",
                "i",
                "j"
              ]
            },
            {
              "op": "index",
              "args": [
                "U_H",
                "j"
              ]
            }
          ]
        },
        "args": [
          "delH",
          "U_H"
        ]
      }
    },
    {
      "lhs": "surfHv",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "layer"
          },
          "j": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "*",
          "args": [
            {
              "op": "index",
              "args": [
                "delH",
                "i",
                "j"
              ]
            },
            {
              "op": "index",
              "args": [
                "V_H",
                "j"
              ]
            }
          ]
        },
        "args": [
          "delH",
          "V_H"
        ]
      }
    },
    {
      "lhs": "surfT",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "/",
          "args": [
            {
              "op": "index",
              "args": [
                "surfHtemp",
                "i"
              ]
            },
            {
              "op": "index",
              "args": [
                "SLdepth",
                "i"
              ]
            }
          ]
        },
        "args": [
          "surfHtemp",
          "SLdepth"
        ]
      }
    },
    {
      "lhs": "surfS",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "/",
          "args": [
            {
              "op": "index",
              "args": [
                "surfHsalt",
                "i"
              ]
            },
            {
              "op": "index",
              "args": [
                "SLdepth",
                "i"
              ]
            }
          ]
        },
        "args": [
          "surfHsalt",
          "SLdepth"
        ]
      }
    },
    {
      "lhs": "surfU",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "/",
          "args": [
            {
              "op": "index",
              "args": [
                "surfHu",
                "i"
              ]
            },
            {
              "op": "index",
              "args": [
                "SLdepth",
                "i"
              ]
            }
          ]
        },
        "args": [
          "surfHu",
          "SLdepth"
        ]
      }
    },
    {
      "lhs": "surfV",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "/",
          "args": [
            {
              "op": "index",
              "args": [
                "surfHv",
                "i"
              ]
            },
            {
              "op": "index",
              "args": [
                "SLdepth",
                "i"
              ]
            }
          ]
        },
        "args": [
          "surfHv",
          "SLdepth"
        ]
      }
    },
    {
      "lhs": "pRef",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "+",
          "args": [
            "p_surf",
            {
              "op": "*",
              "args": [
                "PRESS_STEP",
                {
                  "op": "index",
                  "args": [
                    "depth",
                    "i"
                  ]
                }
              ]
            }
          ]
        },
        "args": [
          "depth"
        ]
      }
    },
    {
      "lhs": "rho_surf",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "apply_expression_template",
          "args": [],
          "name": "wright_rho",
          "bindings": {
            "T": {
              "op": "index",
              "args": [
                "surfT",
                "i"
              ]
            },
            "S": {
              "op": "index",
              "args": [
                "surfS",
                "i"
              ]
            },
            "p": {
              "op": "index",
              "args": [
                "pRef",
                "i"
              ]
            }
          }
        },
        "args": [
          "surfT",
          "surfS",
          "pRef"
        ]
      }
    },
    {
      "lhs": "rho_k",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "apply_expression_template",
          "args": [],
          "name": "wright_rho",
          "bindings": {
            "T": {
              "op": "index",
              "args": [
                "T",
                "i"
              ]
            },
            "S": {
              "op": "index",
              "args": [
                "S",
                "i"
              ]
            },
            "p": {
              "op": "index",
              "args": [
                "pRef",
                "i"
              ]
            }
          }
        },
        "args": [
          "T",
          "S",
          "pRef"
        ]
      }
    },
    {
      "lhs": "rho_km1",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "apply_expression_template",
          "args": [],
          "name": "wright_rho",
          "bindings": {
            "T": {
              "op": "index",
              "args": [
                "T",
                {
                  "op": "max",
                  "args": [
                    {
                      "op": "-",
                      "args": [
                        "i",
                        1
                      ]
                    },
                    1
                  ]
                }
              ]
            },
            "S": {
              "op": "index",
              "args": [
                "S",
                {
                  "op": "max",
                  "args": [
                    {
                      "op": "-",
                      "args": [
                        "i",
                        1
                      ]
                    },
                    1
                  ]
                }
              ]
            },
            "p": {
              "op": "index",
              "args": [
                "pRef",
                "i"
              ]
            }
          }
        },
        "args": [
          "T",
          "S",
          "pRef"
        ]
      }
    },
    {
      "lhs": "deltaBuoy",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "*",
          "args": [
            "GORHO",
            {
              "op": "-",
              "args": [
                {
                  "op": "index",
                  "args": [
                    "rho_k",
                    "i"
                  ]
                },
                {
                  "op": "index",
                  "args": [
                    "rho_surf",
                    "i"
                  ]
                }
              ]
            }
          ]
        },
        "args": [
          "rho_k",
          "rho_surf"
        ]
      }
    },
    {
      "lhs": "N2",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "/",
          "args": [
            {
              "op": "*",
              "args": [
                "GORHO",
                {
                  "op": "-",
                  "args": [
                    {
                      "op": "index",
                      "args": [
                        "rho_k",
                        "i"
                      ]
                    },
                    {
                      "op": "index",
                      "args": [
                        "rho_km1",
                        "i"
                      ]
                    }
                  ]
                }
              ]
            },
            {
              "op": "*",
              "args": [
                0.5,
                {
                  "op": "+",
                  "args": [
                    {
                      "op": "index",
                      "args": [
                        "h",
                        {
                          "op": "max",
                          "args": [
                            {
                              "op": "-",
                              "args": [
                                "i",
                                1
                              ]
                            },
                            1
                          ]
                        }
                      ]
                    },
                    {
                      "op": "index",
                      "args": [
                        "h",
                        "i"
                      ]
                    }
                  ]
                }
              ]
            }
          ]
        },
        "args": [
          "rho_k",
          "rho_km1",
          "h"
        ]
      }
    },
    {
      "lhs": "N",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "iface"
          }
        },
        "expr": {
          "op": "ifelse",
          "args": [
            {
              "op": "==",
              "args": [
                "i",
                "N_IFACE"
              ]
            },
            {
              "op": "const",
              "args": [],
              "value": 0.0,
              "units": "s^-1"
            },
            {
              "op": "sqrt",
              "args": [
                {
                  "op": "max",
                  "args": [
                    {
                      "op": "index",
                      "args": [
                        "N2",
                        {
                          "op": "min",
                          "args": [
                            "i",
                            "N_LAYER"
                          ]
                        }
                      ]
                    },
                    {
                      "op": "const",
                      "args": [],
                      "value": 0.0,
                      "units": "s^-2"
                    }
                  ]
                }
              ]
            }
          ]
        },
        "args": [
          "N2"
        ]
      }
    },
    {
      "lhs": "B0",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "-",
          "args": [
            {
              "op": "index",
              "args": [
                "buoyFlux",
                1
              ]
            },
            {
              "op": "index",
              "args": [
                "buoyFlux",
                {
                  "op": "+",
                  "args": [
                    "i",
                    1
                  ]
                }
              ]
            }
          ]
        },
        "args": [
          "buoyFlux"
        ]
      }
    },
    {
      "lhs": "Ws_1d",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "apply_expression_template",
          "args": [],
          "name": "kpp_ws",
          "bindings": {
            "sigma": 1.0,
            "OBL": {
              "op": "-",
              "args": [
                {
                  "op": "index",
                  "args": [
                    "z_cell",
                    "i"
                  ]
                }
              ]
            },
            "B0": {
              "op": "index",
              "args": [
                "B0",
                "i"
              ]
            },
            "uStar": "uStar",
            "eps": "SURF_LAYER_EXT",
            "kappa": "VON_KARMAN",
            "zs": "ZETA_S",
            "as": "A_S",
            "cs": "C_S"
          }
        },
        "args": [
          "z_cell",
          "B0"
        ]
      }
    },
    {
      "lhs": "Vt2",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "apply_expression_template",
          "args": [],
          "name": "kpp_unresolved_shear",
          "bindings": {
            "zt": {
              "op": "index",
              "args": [
                "z_cell",
                "i"
              ]
            },
            "N": {
              "op": "index",
              "args": [
                "N",
                {
                  "op": "+",
                  "args": [
                    "i",
                    1
                  ]
                }
              ]
            },
            "ws": {
              "op": "index",
              "args": [
                "Ws_1d",
                "i"
              ]
            },
            "ri_crit": "RI_CRIT",
            "min_vtsqr": "MIN_VTSQR",
            "cs": "C_S",
            "eps": "SURF_LAYER_EXT",
            "kappa": "VON_KARMAN"
          }
        },
        "args": [
          "z_cell",
          "N",
          "Ws_1d"
        ]
      }
    },
    {
      "lhs": "Uk",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "-",
          "args": [
            {
              "op": "index",
              "args": [
                "U_H",
                "i"
              ]
            },
            {
              "op": "index",
              "args": [
                "surfU",
                "i"
              ]
            }
          ]
        },
        "args": [
          "U_H",
          "surfU"
        ]
      }
    },
    {
      "lhs": "Vk",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "-",
          "args": [
            {
              "op": "index",
              "args": [
                "V_H",
                "i"
              ]
            },
            {
              "op": "index",
              "args": [
                "surfV",
                "i"
              ]
            }
          ]
        },
        "args": [
          "V_H",
          "surfV"
        ]
      }
    },
    {
      "lhs": "deltaU2",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "+",
          "args": [
            {
              "op": "*",
              "args": [
                {
                  "op": "index",
                  "args": [
                    "Uk",
                    "i"
                  ]
                },
                {
                  "op": "index",
                  "args": [
                    "Uk",
                    "i"
                  ]
                }
              ]
            },
            {
              "op": "*",
              "args": [
                {
                  "op": "index",
                  "args": [
                    "Vk",
                    "i"
                  ]
                },
                {
                  "op": "index",
                  "args": [
                    "Vk",
                    "i"
                  ]
                }
              ]
            }
          ]
        },
        "args": [
          "Uk",
          "Vk"
        ]
      }
    },
    {
      "lhs": "BulkRi",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "i"
        ],
        "ranges": {
          "i": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "apply_expression_template",
          "args": [],
          "name": "kpp_bulk_richardson",
          "bindings": {
            "zt": {
              "op": "index",
              "args": [
                "z_cell",
                "i"
              ]
            },
            "delta_buoy": {
              "op": "index",
              "args": [
                "deltaBuoy",
                "i"
              ]
            },
            "delta_U2": {
              "op": "index",
              "args": [
                "deltaU2",
                "i"
              ]
            },
            "vt2": {
              "op": "index",
              "args": [
                "Vt2",
                "i"
              ]
            },
            "eps": "SURF_LAYER_EXT"
          }
        },
        "args": [
          "z_cell",
          "deltaBuoy",
          "deltaU2",
          "Vt2"
        ]
      }
    },
    {
      "lhs": "OBL_limit",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": ">",
            "args": [
              {
                "op": "index",
                "args": [
                  "B0",
                  "N_LAYER"
                ]
              },
              {
                "op": "const",
                "args": [],
                "value": 0.0,
                "units": "m^2 s^-3"
              }
            ]
          },
          {
            "op": "min",
            "args": [
              {
                "op": "-",
                "args": [
                  {
                    "op": "index",
                    "args": [
                      "z_cell",
                      "N_LAYER"
                    ]
                  }
                ]
              },
              {
                "op": "/",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      {
                        "op": "*",
                        "args": [
                          "uStar",
                          "uStar"
                        ]
                      },
                      "uStar"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      {
                        "op": "index",
                        "args": [
                          "B0",
                          "N_LAYER"
                        ]
                      },
                      "VON_KARMAN"
                    ]
                  }
                ]
              }
            ]
          },
          {
            "op": "-",
            "args": [
              {
                "op": "index",
                "args": [
                  "z_cell",
                  "N_LAYER"
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "kfirst",
      "rhs": {
        "op": "faq",
        "output_idx": [],
        "reduce": "min",
        "ranges": {
          "k": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "ifelse",
          "args": [
            {
              "op": ">",
              "args": [
                {
                  "op": "index",
                  "args": [
                    "BulkRi",
                    "k"
                  ]
                },
                "RI_CRIT"
              ]
            },
            "k",
            "N_IFACE"
          ]
        },
        "args": [
          "BulkRi"
        ]
      }
    },
    {
      "lhs": "slope",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "k"
        ],
        "ranges": {
          "k": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "ifelse",
          "args": [
            {
              "op": "==",
              "args": [
                "k",
                1
              ]
            },
            0.0,
            {
              "op": "ifelse",
              "args": [
                {
                  "op": "==",
                  "args": [
                    "k",
                    2
                  ]
                },
                0.0,
                {
                  "op": "/",
                  "args": [
                    {
                      "op": "-",
                      "args": [
                        {
                          "op": "index",
                          "args": [
                            "BulkRi",
                            {
                              "op": "-",
                              "args": [
                                "k",
                                1
                              ]
                            }
                          ]
                        },
                        {
                          "op": "index",
                          "args": [
                            "BulkRi",
                            {
                              "op": "-",
                              "args": [
                                "k",
                                2
                              ]
                            }
                          ]
                        }
                      ]
                    },
                    {
                      "op": "-",
                      "args": [
                        {
                          "op": "index",
                          "args": [
                            "z_cell",
                            {
                              "op": "-",
                              "args": [
                                "k",
                                1
                              ]
                            }
                          ]
                        },
                        {
                          "op": "index",
                          "args": [
                            "z_cell",
                            {
                              "op": "-",
                              "args": [
                                "k",
                                2
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
        },
        "args": [
          "BulkRi",
          "z_cell"
        ]
      }
    },
    {
      "lhs": "quad_c2",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "k"
        ],
        "ranges": {
          "k": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "ifelse",
          "args": [
            {
              "op": "==",
              "args": [
                "k",
                1
              ]
            },
            0.0,
            {
              "op": "apply_expression_template",
              "args": [],
              "name": "kpp_quad_interp_c",
              "bindings": {
                "x1": {
                  "op": "index",
                  "args": [
                    "z_cell",
                    {
                      "op": "-",
                      "args": [
                        "k",
                        1
                      ]
                    }
                  ]
                },
                "y1": {
                  "op": "index",
                  "args": [
                    "BulkRi",
                    {
                      "op": "-",
                      "args": [
                        "k",
                        1
                      ]
                    }
                  ]
                },
                "x2": {
                  "op": "index",
                  "args": [
                    "z_cell",
                    "k"
                  ]
                },
                "y2": {
                  "op": "index",
                  "args": [
                    "BulkRi",
                    "k"
                  ]
                },
                "slope": {
                  "op": "index",
                  "args": [
                    "slope",
                    "k"
                  ]
                }
              }
            }
          ]
        },
        "args": [
          "z_cell",
          "BulkRi",
          "slope"
        ]
      }
    },
    {
      "lhs": "quad_b2",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "k"
        ],
        "ranges": {
          "k": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "ifelse",
          "args": [
            {
              "op": "==",
              "args": [
                "k",
                1
              ]
            },
            0.0,
            {
              "op": "apply_expression_template",
              "args": [],
              "name": "kpp_quad_interp_b",
              "bindings": {
                "x1": {
                  "op": "index",
                  "args": [
                    "z_cell",
                    {
                      "op": "-",
                      "args": [
                        "k",
                        1
                      ]
                    }
                  ]
                },
                "slope": {
                  "op": "index",
                  "args": [
                    "slope",
                    "k"
                  ]
                },
                "c": {
                  "op": "index",
                  "args": [
                    "quad_c2",
                    "k"
                  ]
                }
              }
            }
          ]
        },
        "args": [
          "z_cell",
          "slope",
          "quad_c2"
        ]
      }
    },
    {
      "lhs": "quad_a2",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "k"
        ],
        "ranges": {
          "k": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "ifelse",
          "args": [
            {
              "op": "==",
              "args": [
                "k",
                1
              ]
            },
            0.0,
            {
              "op": "apply_expression_template",
              "args": [],
              "name": "kpp_quad_interp_a",
              "bindings": {
                "x1": {
                  "op": "index",
                  "args": [
                    "z_cell",
                    {
                      "op": "-",
                      "args": [
                        "k",
                        1
                      ]
                    }
                  ]
                },
                "y1": {
                  "op": "index",
                  "args": [
                    "BulkRi",
                    {
                      "op": "-",
                      "args": [
                        "k",
                        1
                      ]
                    }
                  ]
                },
                "slope": {
                  "op": "index",
                  "args": [
                    "slope",
                    "k"
                  ]
                },
                "c": {
                  "op": "index",
                  "args": [
                    "quad_c2",
                    "k"
                  ]
                },
                "ri_crit": "RI_CRIT"
              }
            }
          ]
        },
        "args": [
          "z_cell",
          "BulkRi",
          "slope",
          "quad_c2"
        ]
      }
    },
    {
      "lhs": "root",
      "rhs": {
        "op": "faq",
        "output_idx": [
          "k"
        ],
        "ranges": {
          "k": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "ifelse",
          "args": [
            {
              "op": "==",
              "args": [
                "k",
                1
              ]
            },
            0.0,
            {
              "op": "apply_expression_template",
              "args": [],
              "name": "kpp_quad_root",
              "bindings": {
                "a": {
                  "op": "index",
                  "args": [
                    "quad_a2",
                    "k"
                  ]
                },
                "b": {
                  "op": "index",
                  "args": [
                    "quad_b2",
                    "k"
                  ]
                },
                "c": {
                  "op": "index",
                  "args": [
                    "quad_c2",
                    "k"
                  ]
                },
                "x1": {
                  "op": "index",
                  "args": [
                    "z_cell",
                    {
                      "op": "-",
                      "args": [
                        "k",
                        1
                      ]
                    }
                  ]
                },
                "x2": {
                  "op": "index",
                  "args": [
                    "z_cell",
                    "k"
                  ]
                }
              }
            }
          ]
        },
        "args": [
          "quad_a2",
          "quad_b2",
          "quad_c2",
          "z_cell"
        ]
      }
    },
    {
      "lhs": "OBLdepth_interp",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "==",
            "args": [
              "kfirst",
              "N_IFACE"
            ]
          },
          "OBL_limit",
          {
            "op": "ifelse",
            "args": [
              {
                "op": "==",
                "args": [
                  "kfirst",
                  1.0
                ]
              },
              {
                "op": "-",
                "args": [
                  {
                    "op": "index",
                    "args": [
                      "z_cell",
                      1
                    ]
                  }
                ]
              },
              {
                "op": "min",
                "args": [
                  {
                    "op": "ifelse",
                    "args": [
                      {
                        "op": "==",
                        "args": [
                          "kfirst",
                          2.0
                        ]
                      },
                      {
                        "op": "max",
                        "args": [
                          {
                            "op": "-",
                            "args": [
                              {
                                "op": "index",
                                "args": [
                                  "root",
                                  {
                                    "op": "min",
                                    "args": [
                                      "kfirst",
                                      "N_LAYER"
                                    ]
                                  }
                                ]
                              }
                            ]
                          },
                          {
                            "op": "-",
                            "args": [
                              {
                                "op": "index",
                                "args": [
                                  "z_cell",
                                  1
                                ]
                              }
                            ]
                          }
                        ]
                      },
                      {
                        "op": "-",
                        "args": [
                          {
                            "op": "index",
                            "args": [
                              "root",
                              {
                                "op": "min",
                                "args": [
                                  "kfirst",
                                  "N_LAYER"
                                ]
                              }
                            ]
                          }
                        ]
                      }
                    ]
                  },
                  "OBL_limit"
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "OBLdepth",
      "rhs": {
        "op": "min",
        "args": [
          {
            "op": "-",
            "args": [
              {
                "op": "index",
                "args": [
                  "z_inter",
                  "N_IFACE"
                ]
              }
            ]
          },
          {
            "op": "max",
            "args": [
              {
                "op": "-",
                "args": [
                  {
                    "op": "index",
                    "args": [
                      "z_inter",
                      2
                    ]
                  }
                ]
              },
              {
                "op": "max",
                "args": [
                  "MIN_OBL_DEPTH",
                  "OBLdepth_interp"
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "kwfirst",
      "rhs": {
        "op": "faq",
        "output_idx": [],
        "reduce": "min",
        "ranges": {
          "kw": {
            "from": "layer"
          }
        },
        "expr": {
          "op": "ifelse",
          "args": [
            {
              "op": "<",
              "args": [
                "OBLdepth",
                {
                  "op": "-",
                  "args": [
                    {
                      "op": "index",
                      "args": [
                        "z_inter",
                        {
                          "op": "+",
                          "args": [
                            "kw",
                            1
                          ]
                        }
                      ]
                    }
                  ]
                }
              ]
            },
            "kw",
            "N_IFACE"
          ]
        },
        "args": [
          "z_inter"
        ]
      }
    },
    {
      "lhs": "kOBL",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "==",
            "args": [
              "kwfirst",
              "N_IFACE"
            ]
          },
          {
            "op": "+",
            "args": [
              "N_LAYER",
              0.75
            ]
          },
          {
            "op": "+",
            "args": [
              "kwfirst",
              {
                "op": "ifelse",
                "args": [
                  {
                    "op": "<",
                    "args": [
                      "OBLdepth",
                      {
                        "op": "-",
                        "args": [
                          {
                            "op": "index",
                            "args": [
                              "z_cell",
                              {
                                "op": "min",
                                "args": [
                                  "kwfirst",
                                  "N_LAYER"
                                ]
                              }
                            ]
                          }
                        ]
                      }
                    ]
                  },
                  0.25,
                  0.75
                ]
              }
            ]
          }
        ]
      }
    }
  ],
  "tests": [
    {
      "id": "uniform_column_bottom_limit",
      "description": "With no bulk Richardson crossing, the positive bottom buoyancy flux gives a 0.8 m Monin-Obukhov limit. The 100 m minimum depth is clipped to the bottom interface.",
      "parameter_overrides": {
        "h": 1.0,
        "dz": 1.0,
        "T": 10.0,
        "S": 35.0,
        "uStar": 0.02,
        "buoyFlux": [
          2.5e-05,
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
          0.0,
          0.0,
          0.0,
          0.0,
          0.0
        ],
        "MIN_OBL_DEPTH": 100.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "tolerance": {
        "abs": 1e-12
      },
      "assertions": [
        {
          "variable": "kfirst",
          "time": 0.0,
          "expected": 76
        },
        {
          "variable": "N",
          "time": 0.0,
          "expected": 0.0,
          "coords": {
            "iface": 76
          }
        },
        {
          "variable": "OBL_limit",
          "time": 0.0,
          "expected": 0.8
        },
        {
          "variable": "OBLdepth_interp",
          "time": 0.0,
          "expected": 0.8
        },
        {
          "variable": "OBLdepth",
          "time": 0.0,
          "expected": 75.0
        },
        {
          "variable": "kOBL",
          "time": 0.0,
          "expected": 75.75
        }
      ]
    },
    {
      "id": "cell782_step3600_quad_k3",
      "description": "mom6_kpp_obl.csv row (i, j, tod) = (7, 82, 3600): the slope-preserving OBL quadratic through cell centers 3..4 (kfirst = 4, 1-based, derived: not a dump column -- from the kpp_ref.py reference reimplementation, stage1/analysis/kpp_ref.py), interpolated OBL depth 6.613560999075406 m, kOBL = 3.75 (interface 4 lies below the OBL, so the kOBL fraction is .75). Pins OBLdepth/kOBL, BulkRi/deltaU2/N2 at layers 2..kOBL+3 = 2..6 (layer 1 is 0 by construction), spot z_cell at layers 1..6 and z_inter at ifaces 2..6 (iface 1 is the surface), plus the deep z_cell/z_inter at layer/iface 75, at rel 1e-12.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "h": [
          2.505951254018008,
          2.501892978164657,
          2.5017272545267977,
          2.5015693814166826,
          3.001726517137612,
          3.0015593590329077,
          4.001807120040217,
          5.0018870024358435,
          5.001492177647564,
          5.0011284090633845,
          5.00083930807502,
          5.000628417858856,
          5.000488628830354,
          5.000401849324857,
          5.000396867081619,
          5.000467952434573,
          5.000572200145099,
          5.000735150856453,
          5.001008941766694,
          5.001503210891359,
          5.0023653454907215,
          5.003790098254819,
          5.006071033680151,
          5.009629768138034,
          5.015074076068978,
          5.023160594684109,
          5.034925407435693,
          5.051731910594908,
          5.075367891423117,
          5.108103636445879,
          5.1527974185346865,
          5.213007285789468,
          5.293130012105934,
          5.398545436034885,
          5.535702362341015,
          5.71290727783589,
          5.93902285082774,
          6.225753904267744,
          6.586379406182547,
          7.036631765948616,
          7.594949272917944,
          8.282801837278132,
          9.125530909640725,
          10.151740250381746,
          11.394334798084529,
          12.891492437510122,
          14.687463397187956,
          16.832907389496818,
          19.381317682286536,
          22.396719964256963,
          25.95622227092345,
          30.135244286889563,
          35.02536929516961,
          40.729080456111625,
          47.358878422378254,
          49.631692734966386,
          0.001513827257149827,
          0.0010000085529628421,
          0.000999962085871611,
          0.0009999599688644196,
          0.0009999603995984824,
          0.0009999604862692374,
          0.0009999605668350338,
          0.0009999606417310767,
          0.0009999607118574131,
          0.0009999607791579305,
          0.0009999608479388797,
          0.0009999609278773275,
          0.000999961040885174,
          0.0009999612367414307,
          0.0009999616285651701,
          0.000999962472857992,
          0.0009999643486363742,
          0.0009999685535890417,
          0.0009999779638633285
        ],
        "dz": [
          2.505951254018008,
          2.501892978164657,
          2.5017272545267977,
          2.5015693814166826,
          3.001726517137612,
          3.0015593590329077,
          4.001807120040217,
          5.0018870024358435,
          5.001492177647564,
          5.0011284090633845,
          5.00083930807502,
          5.000628417858856,
          5.000488628830354,
          5.000401849324857,
          5.000396867081619,
          5.000467952434573,
          5.000572200145099,
          5.000735150856453,
          5.001008941766694,
          5.001503210891359,
          5.0023653454907215,
          5.003790098254819,
          5.006071033680151,
          5.009629768138034,
          5.015074076068978,
          5.023160594684109,
          5.034925407435693,
          5.051731910594908,
          5.075367891423117,
          5.108103636445879,
          5.1527974185346865,
          5.213007285789468,
          5.293130012105934,
          5.398545436034885,
          5.535702362341015,
          5.71290727783589,
          5.93902285082774,
          6.225753904267744,
          6.586379406182547,
          7.036631765948616,
          7.594949272917944,
          8.282801837278132,
          9.125530909640725,
          10.151740250381746,
          11.394334798084529,
          12.891492437510122,
          14.687463397187956,
          16.832907389496818,
          19.381317682286536,
          22.396719964256963,
          25.95622227092345,
          30.135244286889563,
          35.02536929516961,
          40.729080456111625,
          47.358878422378254,
          49.631692734966386,
          0.001513827257149827,
          0.0010000085529628421,
          0.000999962085871611,
          0.0009999599688644196,
          0.0009999603995984824,
          0.0009999604862692374,
          0.0009999605668350338,
          0.0009999606417310767,
          0.0009999607118574131,
          0.0009999607791579305,
          0.0009999608479388797,
          0.0009999609278773275,
          0.000999961040885174,
          0.0009999612367414307,
          0.0009999616285651701,
          0.000999962472857992,
          0.0009999643486363742,
          0.0009999685535890417,
          0.0009999779638633285
        ],
        "T": [
          1.9019792708374321,
          1.8515253625554617,
          1.8514055607269526,
          1.8862508282108714,
          1.8448579551802922,
          1.430724547487314,
          1.184740754822769,
          0.4545384997307825,
          -0.25447828091116215,
          -0.49110845069930276,
          -0.7745387986640418,
          -1.0108442754100886,
          -1.2172725851525845,
          -1.4044141170351905,
          -1.5241563554760427,
          -1.5632026230407188,
          -1.5827837524498456,
          -1.595232696516834,
          -1.623477480795172,
          -1.6357484297227263,
          -1.6466791888181294,
          -1.656221184292802,
          -1.654576424760375,
          -1.6489240159200447,
          -1.6486107320064047,
          -1.648368487671491,
          -1.6483276097363904,
          -1.648346876856009,
          -1.6483490468578914,
          -1.6483485152219775,
          -1.7240770995793384,
          -1.779316420795108,
          -1.779303855059408,
          -1.7793022937387388,
          -1.7792947412824167,
          -1.7522894115497871,
          -1.749246515320854,
          -1.7492462774605688,
          -1.7492489013831836,
          -1.7732489287041933,
          -1.8026864282434933,
          -1.8236396376574981,
          -1.8368274543826035,
          -1.8484545779130355,
          -1.8644139652470242,
          -1.882990351789187,
          -1.897117644563898,
          -1.906781666944587,
          -1.9150097745832726,
          -1.9148179312139284,
          -1.912509584509385,
          -1.8814568103622398,
          -1.8724260008079083,
          -1.8562907816743524,
          -1.870752635490293,
          -1.9368455913068205,
          -1.1062868181803074,
          -0.6946169759566972,
          -0.6945670544170301,
          -0.6945579964992634,
          -0.6945579959581468,
          -0.6945579959743844,
          -0.694557995989068,
          -0.6945579960022066,
          -0.6945579960138252,
          -0.6945579960239971,
          -0.6945579960329397,
          -0.6945579960413003,
          -0.6945579960509881,
          -0.6945579960676073,
          -0.6945579961075465,
          -0.6945579962186464,
          -0.6945579965403735,
          -0.6945579974789736,
          -0.6945580002170941
        ],
        "S": [
          33.59310698272627,
          33.588722523356644,
          33.588728173167695,
          33.782800236630365,
          33.90461160541478,
          33.965910906160445,
          34.00789518405837,
          34.070536794122596,
          34.148386895795504,
          34.21095418134514,
          34.24479571539441,
          34.25233415633717,
          34.26230440210986,
          34.27093940432499,
          34.303318701427465,
          34.33962416579716,
          34.34302443500428,
          34.34965119897978,
          34.365526903564955,
          34.37662928211302,
          34.38304962038136,
          34.38846319400944,
          34.39100055450505,
          34.39108359654662,
          34.39125830182479,
          34.39637823789326,
          34.40920736997063,
          34.417973261151076,
          34.42438357645966,
          34.428414420006455,
          34.43011324225855,
          34.430855379327674,
          34.431793412511745,
          34.43297586591467,
          34.4344236756591,
          34.43613455500456,
          34.43798378740711,
          34.43994122932394,
          34.44203177035942,
          34.44430555607114,
          34.44611056416715,
          34.44726421007603,
          34.4476414576481,
          34.44764924130422,
          34.447509850940904,
          34.44685009113937,
          34.44663806924799,
          34.44589694101489,
          34.445462825680195,
          34.450896101063485,
          34.455125716217445,
          34.45888024899668,
          34.464602805430374,
          34.47257909244512,
          34.476978569749,
          34.47695208208595,
          34.59731571231767,
          34.65569524651118,
          34.65570220934429,
          34.655703276547946,
          34.6557032765586,
          34.655703276558285,
          34.655703276557986,
          34.65570327655773,
          34.655703276557496,
          34.65570327655731,
          34.65570327655714,
          34.65570327655696,
          34.65570327655678,
          34.655703276556444,
          34.65570327655567,
          34.655703276553474,
          34.65570327654714,
          34.655703276528655,
          34.655703276474746
        ],
        "U_H": [
          -0.011744949960462428,
          -0.003082875063225063,
          -0.002894159631725595,
          -0.0027224625485312817,
          -0.002555315853637422,
          -0.002371928176757285,
          -0.002151568843396417,
          -0.0018990637150137731,
          -0.0016337100840623073,
          -0.001385059438783909,
          -0.0011767347919316871,
          -0.0010156302713940158,
          -0.00089086664332033,
          -0.0007930644021732478,
          -0.000735793736138542,
          -0.0007240502406329436,
          -0.0007259221913469982,
          -0.0007230211613037577,
          -0.000709635373296532,
          -0.0006998340242934605,
          -0.0006991325988758125,
          -0.0006972409451808818,
          -0.0006891618229383905,
          -0.0006801081578489303,
          -0.0006710022891237967,
          -0.0006576510109349701,
          -0.0006248921711630005,
          -0.0005722987938272106,
          -0.0005099628182155169,
          -0.0004446013104922014,
          -0.0003832827682377896,
          -0.0003300167325868044,
          -0.0002853457631861446,
          -0.00024691003312125116,
          -0.00021207517894702665,
          -0.00017615644703544885,
          -0.00013646756819329033,
          -9.361387770483545e-05,
          -4.638401514579684e-05,
          7.317794782823516e-06,
          7.110127389897756e-05,
          0.00014625907352091663,
          0.00023179731629133907,
          0.0003267109075294841,
          0.00042535715042386473,
          0.0005169362652334159,
          0.0006057938162116005,
          0.0007005283214426579,
          0.0008037532998542012,
          0.0009081505177409859,
          0.0009771374480927676,
          0.0009590757589003809,
          0.0008205733625316736,
          0.0005175262112227665,
          0.00021654589634319352,
          1.4440104680004613e-07,
          1.1172213802194629e-07,
          9.322259512050895e-08,
          7.766891661651353e-08,
          6.335561318167054e-08,
          5.028061451325909e-08,
          3.844391020656239e-08,
          2.784549862726395e-08,
          1.8485377068280157e-08,
          1.0363542859182835e-08,
          3.479993367726651e-09,
          -2.1652740045246866e-09,
          -6.572261819164076e-09,
          -9.740972605890162e-09,
          -1.1671408867841399e-08,
          -1.236357310002837e-08,
          -1.181746786739519e-08,
          -1.0033096013721018e-08,
          -7.010461341101246e-09,
          -2.7495706574896356e-09
        ],
        "V_H": [
          0.000633294655392449,
          -0.00010297676062454895,
          -1.3946229920801802e-05,
          6.346454797309793e-05,
          0.00011955910189441426,
          0.00016960888545457765,
          0.0002299937825180248,
          0.00029796511865690925,
          0.00037536588800442163,
          0.00043691011541982267,
          0.0004749306588601783,
          0.0004897850877946979,
          0.00048627594690528496,
          0.00047058132359638,
          0.0004456524760862578,
          0.00041821660075216807,
          0.00039274305201737357,
          0.0003710903923677794,
          0.00035585193057216996,
          0.00034148987237113296,
          0.00032519431897481385,
          0.00030823564311887724,
          0.00029186496282504167,
          0.00027542643043160383,
          0.0002587985446903029,
          0.00024362964762938437,
          0.00023555458568249517,
          0.00023492745683258135,
          0.00023805912917577483,
          0.00024253347072235792,
          0.0002461328661047029,
          0.000248218658444547,
          0.0002478749050152082,
          0.000245425050444354,
          0.00024153233620558017,
          0.00023708945107941558,
          0.00023278010188977226,
          0.00022896057251172217,
          0.00022623886524821788,
          0.00022576580844962485,
          0.00022843304621886635,
          0.0002335193041052691,
          0.0002394036976379037,
          0.00024464402700332484,
          0.0002487792705892675,
          0.00024902235518587773,
          0.0002456750023869458,
          0.00024098158079644276,
          0.0002346416574768733,
          0.00022577289867212674,
          0.00019890965487711867,
          0.00014632331814718946,
          8.807615824045946e-05,
          4.3577054604866784e-05,
          3.089412740396256e-05,
          4.355895090696674e-05,
          1.8877178202932105e-07,
          1.8274821735507876e-07,
          1.7762326536683558e-07,
          1.7262602204839438e-07,
          1.6834928415960636e-07,
          1.631273386636189e-07,
          1.5696018497975978e-07,
          1.498478226843555e-07,
          1.4179025133777025e-07,
          1.3278747047303708e-07,
          1.2283947959082604e-07,
          1.119462781184423e-07,
          1.0010786532066351e-07,
          8.7324240070805e-08,
          7.35954002552107e-08,
          5.8921341193208806e-08,
          4.330205140961883e-08,
          2.6737501088560796e-08,
          9.227609945217653e-09
        ],
        "buoyFlux": [
          9.720489412717717e-09,
          1.187333853570639e-08,
          7.266431588860586e-09,
          4.669054568599066e-09,
          3.0527239322026067e-09,
          1.8469915460907578e-09,
          1.120201536443827e-09,
          5.756394430112186e-10,
          2.5053327463291593e-10,
          1.0905178565726596e-10,
          4.7470785798709165e-11,
          2.0665263182301786e-11,
          8.996440085030281e-12,
          3.916611904194657e-12,
          1.7051266996931783e-12,
          7.423404570462271e-13,
          3.231799957620428e-13,
          1.4069487650159728e-13,
          6.124918654350935e-14,
          2.6662605886496567e-14,
          1.1605641810951505e-14,
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
          0.0,
          0.0,
          0.0,
          0.0,
          0.0
        ],
        "uStar": 0.00312023723466675,
        "p_surf": 99753.85917574639
      },
      "tolerance": {
        "rel": 1e-12
      },
      "assertions": [
        {
          "variable": "OBLdepth",
          "time": 0.0,
          "expected": 6.613560999075406
        },
        {
          "variable": "kOBL",
          "time": 0.0,
          "expected": 3.75
        },
        {
          "variable": "kfirst",
          "time": 0.0,
          "expected": 4.0
        },
        {
          "variable": "BulkRi",
          "time": 0.0,
          "expected": 0.0793751887996905,
          "coords": {
            "layer": 2
          }
        },
        {
          "variable": "deltaU2",
          "time": 0.0,
          "expected": 7.557363712339338e-05,
          "coords": {
            "layer": 2
          }
        },
        {
          "variable": "N2",
          "time": 0.0,
          "expected": 7.247179185594313e-07,
          "coords": {
            "layer": 2
          }
        },
        {
          "variable": "BulkRi",
          "time": 0.0,
          "expected": 0.013669628615001551,
          "coords": {
            "layer": 3
          }
        },
        {
          "variable": "deltaU2",
          "time": 0.0,
          "expected": 7.875541020688254e-05,
          "coords": {
            "layer": 3
          }
        },
        {
          "variable": "N2",
          "time": 0.0,
          "expected": 5.005263543983672e-08,
          "coords": {
            "layer": 3
          }
        },
        {
          "variable": "BulkRi",
          "time": 0.0,
          "expected": 14.641731074996242,
          "coords": {
            "layer": 4
          }
        },
        {
          "variable": "deltaU2",
          "time": 0.0,
          "expected": 8.172998544977756e-05,
          "coords": {
            "layer": 4
          }
        },
        {
          "variable": "N2",
          "time": 0.0,
          "expected": 0.0005757190097745598,
          "coords": {
            "layer": 4
          }
        },
        {
          "variable": "BulkRi",
          "time": 0.0,
          "expected": 32.79057224113919,
          "coords": {
            "layer": 5
          }
        },
        {
          "variable": "deltaU2",
          "time": 0.0,
          "expected": 8.471329923624932e-05,
          "coords": {
            "layer": 5
          }
        },
        {
          "variable": "N2",
          "time": 0.0,
          "expected": 0.00034454673949787064,
          "coords": {
            "layer": 5
          }
        },
        {
          "variable": "BulkRi",
          "time": 0.0,
          "expected": 64.41104198012629,
          "coords": {
            "layer": 6
          }
        },
        {
          "variable": "deltaU2",
          "time": 0.0,
          "expected": 8.806854185105401e-05,
          "coords": {
            "layer": 6
          }
        },
        {
          "variable": "N2",
          "time": 0.0,
          "expected": 0.00024730974283601994,
          "coords": {
            "layer": 6
          }
        },
        {
          "variable": "z_cell",
          "time": 0.0,
          "expected": -1.252975627009004,
          "coords": {
            "layer": 1
          }
        },
        {
          "variable": "z_cell",
          "time": 0.0,
          "expected": -3.7568977431003363,
          "coords": {
            "layer": 2
          }
        },
        {
          "variable": "z_cell",
          "time": 0.0,
          "expected": -6.258707859446064,
          "coords": {
            "layer": 3
          }
        },
        {
          "variable": "z_cell",
          "time": 0.0,
          "expected": -8.760356177417803,
          "coords": {
            "layer": 4
          }
        },
        {
          "variable": "z_cell",
          "time": 0.0,
          "expected": -11.51200412669495,
          "coords": {
            "layer": 5
          }
        },
        {
          "variable": "z_cell",
          "time": 0.0,
          "expected": -14.51364706478021,
          "coords": {
            "layer": 6
          }
        },
        {
          "variable": "z_inter",
          "time": 0.0,
          "expected": -2.505951254018008,
          "coords": {
            "iface": 2
          }
        },
        {
          "variable": "z_inter",
          "time": 0.0,
          "expected": -5.007844232182665,
          "coords": {
            "iface": 3
          }
        },
        {
          "variable": "z_inter",
          "time": 0.0,
          "expected": -7.509571486709462,
          "coords": {
            "iface": 4
          }
        },
        {
          "variable": "z_inter",
          "time": 0.0,
          "expected": -10.011140868126144,
          "coords": {
            "iface": 5
          }
        },
        {
          "variable": "z_inter",
          "time": 0.0,
          "expected": -13.012867385263757,
          "coords": {
            "iface": 6
          }
        },
        {
          "variable": "z_cell",
          "time": 0.0,
          "expected": -555.046640079803,
          "coords": {
            "layer": 75
          }
        },
        {
          "variable": "z_inter",
          "time": 0.0,
          "expected": -555.046140090821,
          "coords": {
            "iface": 75
          }
        }
      ]
    },
    {
      "id": "cell883_step3600_quad_k3",
      "description": "mom6_kpp_obl.csv row (i, j, tod) = (8, 83, 3600): the slope-preserving OBL quadratic through cell centers 3..4 (kfirst = 4, 1-based, derived: not a dump column -- from kpp_ref.py), interpolated OBL depth 5.974325344745279 m, kOBL = 3.25 (interface 4 is the first interface below the OBL; the OBL sits above the layer-3 cell center). Pins OBLdepth/kOBL, BulkRi/deltaU2/N2 at layers 2..kOBL+3 = 2..6 (layer 1 is 0 by construction), spot z_cell at layers 1..6 and z_inter at ifaces 2..6 (iface 1 is the surface), plus the deep z_cell/z_inter at layer/iface 75, at rel 1e-12.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "h": [
          2.5007670118695744,
          2.499096369946188,
          2.4992178925568598,
          2.4993072822599656,
          2.9992240312080063,
          2.9992790314342987,
          3.999132520794417,
          4.999022841658772,
          4.999094723688931,
          4.999140648932827,
          4.999165256190947,
          4.999174759074796,
          4.99916869286355,
          4.999154409456291,
          4.999142917129284,
          4.999122864036459,
          4.999120208377426,
          4.999192418144815,
          4.99940154770548,
          4.999839492828878,
          5.000630909658929,
          5.0019888165387485,
          5.004128789711089,
          5.007809498451454,
          5.0132314441334405,
          5.021240774642013,
          5.033016637769106,
          5.049893839187394,
          5.073627521373656,
          5.106467645243341,
          5.1512512145529685,
          5.211527171939047,
          5.291688457813497,
          5.397121726220941,
          5.534364760189119,
          5.711394630623783,
          5.937592356370004,
          6.224314359993038,
          6.584929197444869,
          7.035191422502465,
          7.593586701990416,
          8.281655738603002,
          9.124396996487878,
          10.150576262612299,
          11.393734452077767,
          12.892204422113524,
          14.68889663378581,
          16.832782333925735,
          19.382103018530685,
          22.400576732090475,
          25.9591440597924,
          30.138725920588676,
          35.030301803836174,
          40.738797368506226,
          47.37201146184635,
          55.057878758650055,
          2.3313753235594583,
          0.011427941237755226,
          0.0010045055379010368,
          0.0010000383846451133,
          0.0010000388480105283,
          0.0010000390236808135,
          0.001000039186335036,
          0.0010000393359466963,
          0.0010000394724563753,
          0.0010000395957358334,
          0.0010000397054575434,
          0.0010000398006201267,
          0.0010000398778746658,
          0.0010000399258117108,
          0.001000039906019588,
          0.0010000396919665785,
          0.0010000388775107413,
          0.0010000361995658135,
          0.0010000279027166505
        ],
        "dz": [
          2.5007670118695744,
          2.499096369946188,
          2.4992178925568598,
          2.4993072822599656,
          2.9992240312080063,
          2.9992790314342987,
          3.999132520794417,
          4.999022841658772,
          4.999094723688931,
          4.999140648932827,
          4.999165256190947,
          4.999174759074796,
          4.99916869286355,
          4.999154409456291,
          4.999142917129284,
          4.999122864036459,
          4.999120208377426,
          4.999192418144815,
          4.99940154770548,
          4.999839492828878,
          5.000630909658929,
          5.0019888165387485,
          5.004128789711089,
          5.007809498451454,
          5.0132314441334405,
          5.021240774642013,
          5.033016637769106,
          5.049893839187394,
          5.073627521373656,
          5.106467645243341,
          5.1512512145529685,
          5.211527171939047,
          5.291688457813497,
          5.397121726220941,
          5.534364760189119,
          5.711394630623783,
          5.937592356370004,
          6.224314359993038,
          6.584929197444869,
          7.035191422502465,
          7.593586701990416,
          8.281655738603002,
          9.124396996487878,
          10.150576262612299,
          11.393734452077767,
          12.892204422113524,
          14.68889663378581,
          16.832782333925735,
          19.382103018530685,
          22.400576732090475,
          25.9591440597924,
          30.138725920588676,
          35.030301803836174,
          40.738797368506226,
          47.37201146184635,
          55.057878758650055,
          2.3313753235594583,
          0.011427941237755226,
          0.0010045055379010368,
          0.0010000383846451133,
          0.0010000388480105283,
          0.0010000390236808135,
          0.001000039186335036,
          0.0010000393359466963,
          0.0010000394724563753,
          0.0010000395957358334,
          0.0010000397054575434,
          0.0010000398006201267,
          0.0010000398778746658,
          0.0010000399258117108,
          0.001000039906019588,
          0.0010000396919665785,
          0.0010000388775107413,
          0.0010000361995658135,
          0.0010000279027166505
        ],
        "T": [
          1.5039734541107654,
          1.4468781968241693,
          1.3960518648759517,
          1.3284166514767206,
          1.1329994899661675,
          0.842167222998681,
          0.6411268485556992,
          0.06352712864115473,
          -0.47001503508431536,
          -0.6847225244072493,
          -0.9712413739596555,
          -1.1885010735221946,
          -1.3350267845578188,
          -1.5179521648367642,
          -1.6380098974629247,
          -1.661915697986746,
          -1.6761578703334372,
          -1.686081679291501,
          -1.7223914264026425,
          -1.7525333033872175,
          -1.7788383841510769,
          -1.7866141797230035,
          -1.7977052443670114,
          -1.8065732550875298,
          -1.806572275353805,
          -1.8001103788234436,
          -1.7939107316150138,
          -1.7939182093532757,
          -1.7939338611363704,
          -1.793954415238192,
          -1.8634472051495463,
          -1.9141303984252465,
          -1.9141527219711427,
          -1.9141326667325786,
          -1.9141714354172277,
          -1.8603042971825678,
          -1.8541997501452299,
          -1.8542080299845725,
          -1.8542087035167696,
          -1.8793778485753518,
          -1.8841413217037173,
          -1.8841431401375117,
          -1.87808308869442,
          -1.8658353745268328,
          -1.8596930964284089,
          -1.85782367865988,
          -1.8621244798010042,
          -1.8703065398347463,
          -1.8615322356116153,
          -1.8607660550776284,
          -1.8676649763617041,
          -1.8838171967149098,
          -1.8927366811940574,
          -1.8690981724995626,
          -1.894191784285468,
          -1.9549262201292466,
          -1.9709795270991752,
          -1.718197900617739,
          -0.6955123184511207,
          -0.691389120081572,
          -0.6910043503015,
          -0.691004350402188,
          -0.691004350082529,
          -0.6910043499106019,
          -0.6910043497058108,
          -0.6910043494707875,
          -0.691004349224809,
          -0.6910043490002705,
          -0.6910043488721241,
          -0.6910043490517932,
          -0.69100435009727,
          -0.6910043536929547,
          -0.6910043656545449,
          -0.6910044423002493,
          -0.6910044013401307
        ],
        "S": [
          33.459339259401816,
          33.451931096006376,
          33.451946878158694,
          33.62743115302266,
          33.74178959273253,
          33.80746035142391,
          33.867349588079136,
          33.948243079221996,
          34.039333049517154,
          34.121234955388594,
          34.173795544341075,
          34.200720027012196,
          34.22679677217398,
          34.24514587236748,
          34.29403192409252,
          34.34066232419938,
          34.34351580758889,
          34.345290003065934,
          34.35726077182331,
          34.37215256036369,
          34.380304469015286,
          34.3850107171409,
          34.386038320061374,
          34.385671000529015,
          34.38567109073114,
          34.3868325406764,
          34.39064353833758,
          34.394443726478215,
          34.39852563627518,
          34.4029009415567,
          34.407553445816696,
          34.41198985635739,
          34.41579133433739,
          34.41893217119293,
          34.42138138695352,
          34.42317542193499,
          34.42469018127021,
          34.4260465033913,
          34.42722757848673,
          34.428230893649236,
          34.42919274313491,
          34.43017767981742,
          34.431204470245255,
          34.4325145661909,
          34.43436867749545,
          34.436427552311656,
          34.43749293481529,
          34.43760363302214,
          34.438355014582314,
          34.445030391006455,
          34.451854916504,
          34.45710959723118,
          34.45959747956249,
          34.468443163821796,
          34.46992986675055,
          34.47051182570338,
          34.46963202697293,
          34.5115870354672,
          34.65523767194702,
          34.655742250249844,
          34.65576934500735,
          34.655769345026016,
          34.655769345072265,
          34.6557693451061,
          34.65576934514026,
          34.655769345174576,
          34.65576934520775,
          34.65576934523766,
          34.65576934525929,
          34.65576934525848,
          34.65576934519778,
          34.6557693449638,
          34.655769344162806,
          34.655769338881534,
          34.65576934212278
        ],
        "U_H": [
          -0.021238088453720258,
          -0.00452440314171953,
          -0.004609704002289357,
          -0.0046370973051831355,
          -0.004525960034443836,
          -0.004369070504486651,
          -0.0041924640587660605,
          -0.003955665285352818,
          -0.0036544251505725416,
          -0.003337476788191179,
          -0.0030452060557292515,
          -0.0027904468843066633,
          -0.0025661853382741616,
          -0.0023603127582594078,
          -0.0022045273539775517,
          -0.002112489257666404,
          -0.0020314698131683943,
          -0.0019467085308593729,
          -0.0018559674911048517,
          -0.001777119134598667,
          -0.0017140272978285536,
          -0.0016558135803929083,
          -0.0015994259948942551,
          -0.0015428928335008705,
          -0.0014859617029728282,
          -0.0014256347256085523,
          -0.0013515641931104438,
          -0.001264861059643286,
          -0.0011725625359068157,
          -0.0010790300879024751,
          -0.000989441093122394,
          -0.0009074651098018757,
          -0.0008322464800315641,
          -0.0007613063692565884,
          -0.00069234875603752,
          -0.0006211815419831775,
          -0.0005454515271423907,
          -0.00046589466607374267,
          -0.00038163261301361765,
          -0.00029237481638160184,
          -0.00019515878803740583,
          -8.594599754645628e-05,
          3.691041743364662e-05,
          0.0001735333273415285,
          0.0003189985454496909,
          0.00046499416331628073,
          0.0006091850958539784,
          0.0007598690666667321,
          0.0009218110255986268,
          0.0010918884113659982,
          0.0012584713325287983,
          0.0014001495962532643,
          0.001526882989056504,
          0.001652904489764935,
          0.0017399482402696996,
          0.0017336113422386713,
          0.0014013508195567838,
          0.0009387125119731591,
          2.0581290419588087e-06,
          1.8978113291109964e-06,
          1.7642816463667467e-06,
          1.6322798700595952e-06,
          1.5018060197152703e-06,
          1.3728601117055376e-06,
          1.2454421623095349e-06,
          1.1195521877361971e-06,
          9.951902041358142e-07,
          8.72356227648726e-07,
          7.510502745156302e-07,
          6.312723614021579e-07,
          5.130225063217202e-07,
          3.963007314124331e-07,
          2.8110707104951265e-07,
          1.6744159370769897e-07,
          5.5304441685693554e-08
        ],
        "V_H": [
          0.0019899919953052896,
          0.00039787587254094993,
          0.0002903071164406842,
          0.00022433287675319106,
          0.00023272064379467166,
          0.00025066412867305956,
          0.00025185576831691713,
          0.00026767528935340093,
          0.00031821161026039635,
          0.00036019265491170474,
          0.0003837216076607951,
          0.0003950402459048976,
          0.00039286366987604176,
          0.0003860407879826739,
          0.0003761543554478254,
          0.0003702690931789721,
          0.0003743969440284206,
          0.00038157506529203864,
          0.00039176231401466755,
          0.0004009540772841908,
          0.00040702554304353217,
          0.00040769666085257864,
          0.0004017991018083789,
          0.000394814750844622,
          0.0003877470433668186,
          0.00038090191341674855,
          0.00037425334984789627,
          0.0003676382293972533,
          0.00036103103451486654,
          0.0003545675572757611,
          0.0003483731826844083,
          0.0003424579208260091,
          0.0003366584864329617,
          0.00033088237886838773,
          0.0003250050665568209,
          0.00031832975677485953,
          0.0003106716852757547,
          0.0003027325990213733,
          0.00029469552337789586,
          0.00028579163898688383,
          0.00027595682796772265,
          0.00026605179084676167,
          0.0002548406281874018,
          0.00024022650123263595,
          0.0002218544407938203,
          0.00020235337047181634,
          0.00018190615296801132,
          0.00015700881541826274,
          0.0001229851266998583,
          8.161419953638832e-05,
          6.627752813814512e-05,
          7.032505854614226e-05,
          1.1686832063669444e-05,
          -9.028191515057876e-05,
          -0.00017267214678089827,
          -0.00023572294669523875,
          -0.00027911344572671015,
          -0.00016339793314763628,
          1.6925115796303043e-07,
          1.8215199860871143e-07,
          1.8835953846720132e-07,
          1.9209266778865105e-07,
          1.9335138939990795e-07,
          1.9213570647108895e-07,
          1.8844562212236712e-07,
          1.822811394186232e-07,
          1.7364226140025066e-07,
          1.6252899112630453e-07,
          1.4894133183188018e-07,
          1.328792872781962e-07,
          1.1434286273441738e-07,
          9.333206761831705e-08,
          6.984692281285218e-08,
          4.3887480937400367e-08,
          1.545388207304728e-08
        ],
        "buoyFlux": [
          1.429513788060192e-08,
          9.081023074260452e-09,
          5.4381016996401365e-09,
          3.4180372424231917e-09,
          2.1860422348061454e-09,
          1.2881436590926979e-09,
          7.609017672696075e-10,
          3.7746679930797967e-10,
          1.5719300345761607e-10,
          6.546476130126951e-11,
          2.7263303014019892e-11,
          1.1353963133269464e-11,
          4.728416953324446e-12,
          1.9691759068934013e-12,
          8.200764643992884e-13,
          3.415270110688739e-13,
          1.4223199202087476e-13,
          5.923381844565831e-14,
          2.466815519877115e-14,
          1.027277319640633e-14,
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
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0
        ],
        "uStar": 0.0032447337772619567,
        "p_surf": 99769.71836115603
      },
      "tolerance": {
        "rel": 1e-12
      },
      "assertions": [
        {
          "variable": "OBLdepth",
          "time": 0.0,
          "expected": 5.974325344745279
        },
        {
          "variable": "kOBL",
          "time": 0.0,
          "expected": 3.25
        },
        {
          "variable": "kfirst",
          "time": 0.0,
          "expected": 4.0
        },
        {
          "variable": "BulkRi",
          "time": 0.0,
          "expected": -0.1951318385069328,
          "coords": {
            "layer": 2
          }
        },
        {
          "variable": "deltaU2",
          "time": 0.0,
          "expected": 0.00028188211045695506,
          "coords": {
            "layer": 2
          }
        },
        {
          "variable": "N2",
          "time": 0.0,
          "expected": -7.79188932624632e-06,
          "coords": {
            "layer": 2
          }
        },
        {
          "variable": "BulkRi",
          "time": 0.0,
          "expected": 0.07936778491278673,
          "coords": {
            "layer": 3
          }
        },
        {
          "variable": "deltaU2",
          "time": 0.0,
          "expected": 0.00027939209815203,
          "coords": {
            "layer": 3
          }
        },
        {
          "variable": "N2",
          "time": 0.0,
          "expected": 1.2929152851969106e-05,
          "coords": {
            "layer": 3
          }
        },
        {
          "variable": "BulkRi",
          "time": 0.0,
          "expected": 12.13222950910222,
          "coords": {
            "layer": 4
          }
        },
        {
          "variable": "deltaU2",
          "time": 0.0,
          "expected": 0.0002787104592367341,
          "coords": {
            "layer": 4
          }
        },
        {
          "variable": "N2",
          "time": 0.0,
          "expected": 0.0005478131600547072,
          "coords": {
            "layer": 4
          }
        },
        {
          "variable": "BulkRi",
          "time": 0.0,
          "expected": 29.367212953879278,
          "coords": {
            "layer": 5
          }
        },
        {
          "variable": "deltaU2",
          "time": 0.0,
          "expected": 0.00028238323890522664,
          "coords": {
            "layer": 5
          }
        },
        {
          "variable": "N2",
          "time": 0.0,
          "expected": 0.0003584720134579016,
          "coords": {
            "layer": 5
          }
        },
        {
          "variable": "BulkRi",
          "time": 0.0,
          "expected": 49.27735503181639,
          "coords": {
            "layer": 6
          }
        },
        {
          "variable": "deltaU2",
          "time": 0.0,
          "expected": 0.00028758902799920906,
          "coords": {
            "layer": 6
          }
        },
        {
          "variable": "N2",
          "time": 0.0,
          "expected": 0.00022302360987421765,
          "coords": {
            "layer": 6
          }
        },
        {
          "variable": "z_cell",
          "time": 0.0,
          "expected": -1.2503835059347872,
          "coords": {
            "layer": 1
          }
        },
        {
          "variable": "z_cell",
          "time": 0.0,
          "expected": -3.7503151968426685,
          "coords": {
            "layer": 2
          }
        },
        {
          "variable": "z_cell",
          "time": 0.0,
          "expected": -6.249472328094193,
          "coords": {
            "layer": 3
          }
        },
        {
          "variable": "z_cell",
          "time": 0.0,
          "expected": -8.748734915502606,
          "coords": {
            "layer": 4
          }
        },
        {
          "variable": "z_cell",
          "time": 0.0,
          "expected": -11.49800057223659,
          "coords": {
            "layer": 5
          }
        },
        {
          "variable": "z_cell",
          "time": 0.0,
          "expected": -14.497252103557743,
          "coords": {
            "layer": 6
          }
        },
        {
          "variable": "z_inter",
          "time": 0.0,
          "expected": -2.5007670118695744,
          "coords": {
            "iface": 2
          }
        },
        {
          "variable": "z_inter",
          "time": 0.0,
          "expected": -4.9998633818157625,
          "coords": {
            "iface": 3
          }
        },
        {
          "variable": "z_inter",
          "time": 0.0,
          "expected": -7.499081274372623,
          "coords": {
            "iface": 4
          }
        },
        {
          "variable": "z_inter",
          "time": 0.0,
          "expected": -9.998388556632587,
          "coords": {
            "iface": 5
          }
        },
        {
          "variable": "z_inter",
          "time": 0.0,
          "expected": -12.997612587840594,
          "coords": {
            "iface": 6
          }
        },
        {
          "variable": "z_cell",
          "time": 0.0,
          "expected": -562.7738571320723,
          "coords": {
            "layer": 75
          }
        },
        {
          "variable": "z_inter",
          "time": 0.0,
          "expected": -562.7733571181209,
          "coords": {
            "iface": 75
          }
        }
      ]
    },
    {
      "id": "cell784_step10800_two_point_k2",
      "description": "mom6_kpp_obl.csv row (i, j, tod) = (7, 84, 10800): kfirst = 3 (1-based, derived: not a dump column -- from kpp_ref.py), the slope-preserving OBL quadratic through cell centers 2..3; the interpolated OBL depth is below the MINIMUM_OBL_DEPTH = 5 m floor, so OBLdepth pins the floored value 5.0 and the interpolation itself is unpinned. Pins OBLdepth/kOBL, BulkRi/deltaU2/N2 at layers 2..kOBL+3 = 2..5 (layer 1 is 0 by construction), spot z_cell at layers 1..5 and z_inter at ifaces 2..5 (iface 1 is the surface), plus the deep z_cell/z_inter at layer/iface 75, at rel 1e-12.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "h": [
          2.500788929870075,
          2.4997787301248082,
          2.498848958329388,
          2.4993175074181737,
          2.9991221245614006,
          2.9990482502100626,
          3.998616063360791,
          4.998120950113459,
          4.997978400036197,
          4.9978252603509645,
          4.9976657703797205,
          4.997523749669076,
          4.997410581918274,
          4.997320938566282,
          4.997267699409599,
          4.997251566779764,
          4.997272682434672,
          4.997377501097539,
          4.997614584219173,
          4.998069012163172,
          4.998883783793018,
          5.00025879380595,
          5.0024677556579125,
          5.006010424868664,
          5.011450412499349,
          5.019464222960482,
          5.031205737649105,
          5.0480156286296936,
          5.0716669655981095,
          5.104419093265251,
          5.149119936384163,
          5.209318877543296,
          5.28940446046472,
          5.394760815306709,
          5.531928065849263,
          5.708815352450576,
          5.934880984668308,
          6.221426440855163,
          6.581822572812168,
          7.031810995500938,
          7.589849157118206,
          8.277441249719082,
          9.119602510379089,
          10.145126844726233,
          11.387288160495839,
          12.884171144130988,
          14.678525701898577,
          16.821902288385594,
          19.36818777755062,
          22.382863247681566,
          25.93673706520873,
          30.111011203664795,
          34.99550639324736,
          40.692476491342205,
          47.31657650221462,
          54.99281282263727,
          63.8556370864507,
          74.07730240050232,
          65.63209012664743,
          0.0010001173911367166,
          0.0010001175141116621,
          0.0010001175590141217,
          0.0010001175589218912,
          0.001000117555019384,
          0.001000117546162739,
          0.001000117521894813,
          0.0010001174801623203,
          0.0010001174361545465,
          0.0010001173805467831,
          0.001000117314421523,
          0.0010001172643384455,
          0.001000117232860926,
          0.0010001178463343895,
          0.001000126070817907,
          0.0010001094461188206
        ],
        "dz": [
          2.500788929870075,
          2.4997787301248082,
          2.498848958329388,
          2.4993175074181737,
          2.9991221245614006,
          2.9990482502100626,
          3.998616063360791,
          4.998120950113459,
          4.997978400036197,
          4.9978252603509645,
          4.9976657703797205,
          4.997523749669076,
          4.997410581918274,
          4.997320938566282,
          4.997267699409599,
          4.997251566779764,
          4.997272682434672,
          4.997377501097539,
          4.997614584219173,
          4.998069012163172,
          4.998883783793018,
          5.00025879380595,
          5.0024677556579125,
          5.006010424868664,
          5.011450412499349,
          5.019464222960482,
          5.031205737649105,
          5.0480156286296936,
          5.0716669655981095,
          5.104419093265251,
          5.149119936384163,
          5.209318877543296,
          5.28940446046472,
          5.394760815306709,
          5.531928065849263,
          5.708815352450576,
          5.934880984668308,
          6.221426440855163,
          6.581822572812168,
          7.031810995500938,
          7.589849157118206,
          8.277441249719082,
          9.119602510379089,
          10.145126844726233,
          11.387288160495839,
          12.884171144130988,
          14.678525701898577,
          16.821902288385594,
          19.36818777755062,
          22.382863247681566,
          25.93673706520873,
          30.111011203664795,
          34.99550639324736,
          40.692476491342205,
          47.31657650221462,
          54.99281282263727,
          63.8556370864507,
          74.07730240050232,
          65.63209012664743,
          0.0010001173911367166,
          0.0010001175141116621,
          0.0010001175590141217,
          0.0010001175589218912,
          0.001000117555019384,
          0.001000117546162739,
          0.001000117521894813,
          0.0010001174801623203,
          0.0010001174361545465,
          0.0010001173805467831,
          0.001000117314421523,
          0.0010001172643384455,
          0.001000117232860926,
          0.0010001178463343895,
          0.001000126070817907,
          0.0010001094461188206
        ],
        "T": [
          1.523185880769498,
          1.5057461449338072,
          1.4594501530603166,
          1.4081393794813832,
          1.2277783045748207,
          0.9418798047638595,
          0.719264327311581,
          0.1863690034993549,
          -0.36070938099601857,
          -0.6007422977850013,
          -0.8565083105702302,
          -1.0979622843771104,
          -1.2766028824733924,
          -1.4498216537377362,
          -1.563650228328297,
          -1.5936215324875793,
          -1.6176799611051336,
          -1.632136984456662,
          -1.6710248148815219,
          -1.6972311163895468,
          -1.7175815885784418,
          -1.7304995712277809,
          -1.7383422403723694,
          -1.7391433497166149,
          -1.739334358640172,
          -1.7401578746128357,
          -1.7415743311811605,
          -1.7439561140564128,
          -1.7478667129439664,
          -1.753738621382413,
          -1.814352625229798,
          -1.8556526864475764,
          -1.8560527528357096,
          -1.856037972788765,
          -1.855539365716857,
          -1.8333979758183765,
          -1.8302820197253387,
          -1.8302758836033242,
          -1.8304869650715583,
          -1.8532160587169875,
          -1.8744427606043046,
          -1.8865610481836517,
          -1.890718577554917,
          -1.8927609380077999,
          -1.8993950539896545,
          -1.9169443655094762,
          -1.939023073540397,
          -1.9391368551037071,
          -1.9474608288597388,
          -1.9529986210587837,
          -1.9459401212777834,
          -1.92815769352075,
          -1.9292929604967455,
          -1.9087304592818677,
          -1.9305310973224201,
          -1.9858766876375302,
          -1.873473516561889,
          -1.8406156318573372,
          -1.6220714153405735,
          -1.234067102333053,
          -1.2340626560101138,
          -1.2340589411542429,
          -1.234055184479874,
          -1.2340518119309323,
          -1.2340487532454911,
          -1.2340460019987158,
          -1.2340438035356716,
          -1.2340437868560166,
          -1.2340435859091896,
          -1.2340434175808734,
          -1.2340432795970235,
          -1.2340431817156088,
          -1.2340433088086387,
          -1.2340461378861536,
          -1.234040309237949
        ],
        "S": [
          33.51802520067947,
          33.515359056108146,
          33.51740771297672,
          33.68910764164756,
          33.81160632292133,
          33.88868286120603,
          33.947051919649184,
          34.02300815923254,
          34.11440538650539,
          34.19307105093119,
          34.23897000423775,
          34.25886608308804,
          34.279472250563494,
          34.293199407364774,
          34.325577496639596,
          34.358063421805205,
          34.36029125692388,
          34.363554580225,
          34.37570942661281,
          34.38632257662367,
          34.39284790716763,
          34.398507112980674,
          34.40119401850696,
          34.401362943245054,
          34.40166948426467,
          34.40516380886052,
          34.41370306817188,
          34.419974667466896,
          34.42494697069732,
          34.42861315626117,
          34.43101793324305,
          34.432819950238205,
          34.43457794901044,
          34.43633675806371,
          34.43810967100839,
          34.43983944410222,
          34.44150970891195,
          34.443038855946824,
          34.444416812611635,
          34.44565562229047,
          34.446836052842094,
          34.44799127255595,
          34.449109908131085,
          34.45020602930139,
          34.45134043850308,
          34.45196643957321,
          34.45126091201299,
          34.451255701706636,
          34.45118770571963,
          34.45549798886438,
          34.46181218756338,
          34.46783708085717,
          34.472020962020025,
          34.47539628407514,
          34.475827161928876,
          34.47597624880246,
          34.486593285679604,
          34.494759067560224,
          34.55181494761236,
          34.60546364875959,
          34.605464147891176,
          34.60546453783752,
          34.605464954648916,
          34.60546532358523,
          34.605465657573745,
          34.605465958068244,
          34.60546618229738,
          34.60546618423268,
          34.605466204674954,
          34.60546622188679,
          34.60546623604509,
          34.605466245849684,
          34.60546622949179,
          34.60546589789265,
          34.60546657992384
        ],
        "U_H": [
          -0.033755523678477374,
          -0.019687695136779284,
          -0.013812418319855864,
          -0.013638079385817282,
          -0.01342464463839757,
          -0.0131332395055209,
          -0.01274491757003818,
          -0.012246485445947655,
          -0.011689687202800704,
          -0.01112312076174498,
          -0.010598456857436286,
          -0.010109493187300964,
          -0.009628133181912746,
          -0.009154389728065203,
          -0.008766978583789867,
          -0.008530036635300605,
          -0.008340591540786809,
          -0.008144169171317443,
          -0.007943090392369744,
          -0.007775116547472882,
          -0.007637814942379755,
          -0.00751056433091426,
          -0.007370617193754306,
          -0.007217246939881362,
          -0.007105321822623413,
          -0.006925408869388237,
          -0.0067423518307140815,
          -0.006540023770968092,
          -0.006327721165941401,
          -0.006113401914259719,
          -0.005908052324430345,
          -0.005725523685197496,
          -0.005561120495634006,
          -0.005405641608968982,
          -0.005253351042150315,
          -0.00509845794552358,
          -0.004928478342265771,
          -0.004750848345615359,
          -0.004563086393293117,
          -0.004362346387703612,
          -0.0041441217138607975,
          -0.0039004191186977934,
          -0.0036234716851970316,
          -0.0033110938243058035,
          -0.0029678080614782476,
          -0.0025734254366108905,
          -0.0019711076870335686,
          -0.0019159965441555781,
          -0.0012069871419656888,
          -0.0006184731469373692,
          -2.8782520566066148e-05,
          0.0006617290718636885,
          0.0015138735475751397,
          0.0024113260708064025,
          0.0033239644778974204,
          0.004324849526668135,
          0.005692277914766524,
          0.007008223100467943,
          0.00698880117812414,
          3.467577489705551e-06,
          3.300854651732742e-06,
          3.0489344366459356e-06,
          2.6338200686875032e-06,
          2.218794833366426e-06,
          1.8039039888452225e-06,
          1.5525312913910925e-06,
          1.343839570709055e-06,
          1.3409135069916602e-06,
          1.0477493498117239e-06,
          7.831006535207458e-07,
          6.114027804342012e-07,
          6.080216515528407e-07,
          4.3259311799317177e-07,
          2.2306993865279618e-07,
          2.2013238406474303e-07
        ],
        "V_H": [
          0.0036518206546311007,
          0.0020236736032245182,
          0.003061105982184703,
          0.003188842955448381,
          0.003505967703543782,
          0.003914211972889558,
          0.004353278864356587,
          0.004896054163866447,
          0.005535405442283228,
          0.006124829630121118,
          0.0065966867047546635,
          0.006959469018238319,
          0.007230777646651823,
          0.0074414854377920815,
          0.0075636257579556766,
          0.007594259165859386,
          0.007614144234803325,
          0.007647877677457827,
          0.007704607842690154,
          0.007750096122830067,
          0.0077716388765190735,
          0.007784470759811636,
          0.007798255292460251,
          0.007807679393279017,
          0.007798656191166755,
          0.007828170911627196,
          0.00788264128824952,
          0.007973902178770906,
          0.00808599819167776,
          0.008205277237770831,
          0.00831793000229986,
          0.008413501184840789,
          0.008491164207319582,
          0.00855705359116402,
          0.0086243810194707,
          0.00866495261816496,
          0.008737748111387944,
          0.008808729309214166,
          0.008887300317398657,
          0.008976975906852407,
          0.009083586768955265,
          0.009212792449766534,
          0.00936079081450965,
          0.00951905547038439,
          0.00967336844038166,
          0.009818449154678463,
          0.010035430431775117,
          0.010031460753673272,
          0.010150058953618733,
          0.010302567359588417,
          0.010411344293178524,
          0.010462603249859842,
          0.010296448973210071,
          0.01020951998575541,
          0.010339044154610417,
          0.010507046933873283,
          0.010431746241389716,
          0.010343937294147471,
          0.010013668512116696,
          5.383177741744582e-06,
          5.378396466770832e-06,
          4.797715435384853e-06,
          4.216590951134481e-06,
          3.635087319381605e-06,
          3.053286138853298e-06,
          2.7548175287335114e-06,
          2.4563415301955894e-06,
          2.451529666952608e-06,
          2.024044581040242e-06,
          1.6148498302788916e-06,
          1.2374925489917787e-06,
          8.643839201881278e-07,
          4.819252284734431e-07,
          3.168131245528533e-07,
          3.1355794460942185e-07
        ],
        "buoyFlux": [
          2.800014818916761e-08,
          1.9446846695378854e-08,
          1.1476170394818108e-08,
          7.108255953602827e-09,
          4.47970159216021e-09,
          2.593608975513388e-09,
          1.505354688375117e-09,
          7.295216618961453e-10,
          2.950711165877147e-10,
          1.1935830418472038e-10,
          4.828259719702581e-11,
          1.9531749711523173e-11,
          7.90137814528887e-12,
          3.196490687332461e-12,
          1.2931565095264706e-12,
          5.231580643145882e-13,
          2.1164890547363232e-13,
          8.562438573337132e-14,
          3.463942443916278e-14,
          1.401280956161377e-14,
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
          0.0,
          0.0,
          0.0,
          0.0,
          0.0,
          0.0
        ],
        "uStar": 0.00255318326401385,
        "p_surf": 99754.14069184187
      },
      "tolerance": {
        "rel": 1e-12
      },
      "assertions": [
        {
          "variable": "OBLdepth",
          "time": 0.0,
          "expected": 5.0
        },
        {
          "variable": "kOBL",
          "time": 0.0,
          "expected": 2.75
        },
        {
          "variable": "kfirst",
          "time": 0.0,
          "expected": 3.0
        },
        {
          "variable": "BulkRi",
          "time": 0.0,
          "expected": -0.1278487836433136,
          "coords": {
            "layer": 2
          }
        },
        {
          "variable": "deltaU2",
          "time": 0.0,
          "expected": 0.00020055466269961936,
          "coords": {
            "layer": 2
          }
        },
        {
          "variable": "N2",
          "time": 0.0,
          "expected": -3.5529421850238117e-06,
          "coords": {
            "layer": 2
          }
        },
        {
          "variable": "BulkRi",
          "time": 0.0,
          "expected": 0.31437040108588454,
          "coords": {
            "layer": 3
          }
        },
        {
          "variable": "deltaU2",
          "time": 0.0,
          "expected": 0.0003980763951693214,
          "coords": {
            "layer": 3
          }
        },
        {
          "variable": "N2",
          "time": 0.0,
          "expected": 1.8096796275404396e-05,
          "coords": {
            "layer": 3
          }
        },
        {
          "variable": "BulkRi",
          "time": 0.0,
          "expected": 17.295503089776652,
          "coords": {
            "layer": 4
          }
        },
        {
          "variable": "deltaU2",
          "time": 0.0,
          "expected": 0.00040492591321822266,
          "coords": {
            "layer": 4
          }
        },
        {
          "variable": "N2",
          "time": 0.0,
          "expected": 0.0005323716519590551,
          "coords": {
            "layer": 4
          }
        },
        {
          "variable": "BulkRi",
          "time": 0.0,
          "expected": 42.29817166504173,
          "coords": {
            "layer": 5
          }
        },
        {
          "variable": "deltaU2",
          "time": 0.0,
          "expected": 0.0004133659156256972,
          "coords": {
            "layer": 5
          }
        },
        {
          "variable": "N2",
          "time": 0.0,
          "expected": 0.0003781963296646641,
          "coords": {
            "layer": 5
          }
        },
        {
          "variable": "z_cell",
          "time": 0.0,
          "expected": -1.2503944649350376,
          "coords": {
            "layer": 1
          }
        },
        {
          "variable": "z_cell",
          "time": 0.0,
          "expected": -3.750678294932479,
          "coords": {
            "layer": 2
          }
        },
        {
          "variable": "z_cell",
          "time": 0.0,
          "expected": -6.249992139159578,
          "coords": {
            "layer": 3
          }
        },
        {
          "variable": "z_cell",
          "time": 0.0,
          "expected": -8.749075372033358,
          "coords": {
            "layer": 4
          }
        },
        {
          "variable": "z_cell",
          "time": 0.0,
          "expected": -11.498295188023144,
          "coords": {
            "layer": 5
          }
        },
        {
          "variable": "z_inter",
          "time": 0.0,
          "expected": -2.500788929870075,
          "coords": {
            "iface": 2
          }
        },
        {
          "variable": "z_inter",
          "time": 0.0,
          "expected": -5.000567659994884,
          "coords": {
            "iface": 3
          }
        },
        {
          "variable": "z_inter",
          "time": 0.0,
          "expected": -7.499416618324272,
          "coords": {
            "iface": 4
          }
        },
        {
          "variable": "z_inter",
          "time": 0.0,
          "expected": -9.998734125742445,
          "coords": {
            "iface": 5
          }
        },
        {
          "variable": "z_cell",
          "time": 0.0,
          "expected": -763.5919605809715,
          "coords": {
            "layer": 75
          }
        },
        {
          "variable": "z_inter",
          "time": 0.0,
          "expected": -763.5914605262485,
          "coords": {
            "iface": 75
          }
        }
      ]
    },
    {
      "id": "cell1184_step3600_kfirst2",
      "description": "mom6_kpp_obl.csv row (i, j, tod) = (11, 84, 3600): kfirst = 2 (1-based, derived: not a dump column -- from kpp_ref.py), the two-point quadratic with zero slope at x1 (cvmix_kpp.F90:1773-1776) through cell centers 1..2 (the layer-2 BulkRi already exceeds RI_CRIT); the interpolated OBL depth 3.649 m is below the MINIMUM_OBL_DEPTH = 5 m floor, so OBLdepth pins the floored value 5.0; kOBL = 3.25. Pins OBLdepth/kOBL, BulkRi/deltaU2/N2 at layers 2..kOBL+3 = 2..6 (layer 1 is 0 by construction), spot z_cell at layers 1..6 and z_inter at ifaces 2..6 (iface 1 is the surface), plus the deep z_cell/z_inter at layer/iface 75, at rel 1e-12.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "h": [
          2.4871035945487163,
          2.498413302371859,
          2.4984636163347167,
          2.4984896065497355,
          2.9981379217849966,
          2.9980966879360187,
          3.9974456603890887,
          4.996834980969886,
          4.996925641759502,
          4.997076363758009,
          4.997261460140166,
          4.997451603550523,
          4.9976392161912875,
          4.997827909665866,
          4.997961819453403,
          4.99812590238134,
          4.998287502046111,
          4.9985712926683235,
          4.99893991619021,
          4.999504447368247,
          5.000421886054464,
          5.001902035388606,
          5.004310446986138,
          5.0078732437830205,
          5.013355512422344,
          5.021566357896912,
          5.033436801037826,
          5.050373503629741,
          5.074152828013639,
          5.10703361298613,
          5.151861609331785,
          5.212194490720269,
          5.29242817529179,
          5.397950222359949,
          5.535354252486961,
          5.712371007997995,
          5.9387543377285406,
          6.225626131417505,
          6.586407155810753,
          7.036883631868407,
          7.59551415304259,
          8.283847892086692,
          9.126871367179508,
          10.153565885245879,
          11.397161234956846,
          12.895816146652148,
          14.693145091585757,
          16.838789046558368,
          19.38924076886001,
          22.408121074455998,
          25.967525204431027,
          30.147966551781987,
          35.03959585681851,
          40.7440775198378,
          43.74283280420597,
          0.0017593870036773354,
          0.0010000823957908604,
          0.0010000820517989154,
          0.0010000818070983201,
          0.0010000817826533019,
          0.0010000817582120562,
          0.0010000817337736264,
          0.0010000817093365605,
          0.001000081684898762,
          0.0010000816604571403,
          0.0010000816360069532,
          0.0010000816115405726,
          0.0010000815870450247,
          0.0010000815624966947,
          0.001000081537848709,
          0.0010000815129965815,
          0.0010000814876650955,
          0.001000081460873459,
          0.0010000814230470088,
          0.0010000808539779441
        ],
        "dz": [
          2.4871035945487163,
          2.498413302371859,
          2.4984636163347167,
          2.4984896065497355,
          2.9981379217849966,
          2.9980966879360187,
          3.9974456603890887,
          4.996834980969886,
          4.996925641759502,
          4.997076363758009,
          4.997261460140166,
          4.997451603550523,
          4.9976392161912875,
          4.997827909665866,
          4.997961819453403,
          4.99812590238134,
          4.998287502046111,
          4.9985712926683235,
          4.99893991619021,
          4.999504447368247,
          5.000421886054464,
          5.001902035388606,
          5.004310446986138,
          5.0078732437830205,
          5.013355512422344,
          5.021566357896912,
          5.033436801037826,
          5.050373503629741,
          5.074152828013639,
          5.10703361298613,
          5.151861609331785,
          5.212194490720269,
          5.29242817529179,
          5.397950222359949,
          5.535354252486961,
          5.712371007997995,
          5.9387543377285406,
          6.225626131417505,
          6.586407155810753,
          7.036883631868407,
          7.59551415304259,
          8.283847892086692,
          9.126871367179508,
          10.153565885245879,
          11.397161234956846,
          12.895816146652148,
          14.693145091585757,
          16.838789046558368,
          19.38924076886001,
          22.408121074455998,
          25.967525204431027,
          30.147966551781987,
          35.03959585681851,
          40.7440775198378,
          43.74283280420597,
          0.0017593870036773354,
          0.0010000823957908604,
          0.0010000820517989154,
          0.0010000818070983201,
          0.0010000817826533019,
          0.0010000817582120562,
          0.0010000817337736264,
          0.0010000817093365605,
          0.001000081684898762,
          0.0010000816604571403,
          0.0010000816360069532,
          0.0010000816115405726,
          0.0010000815870450247,
          0.0010000815624966947,
          0.001000081537848709,
          0.0010000815129965815,
          0.0010000814876650955,
          0.001000081460873459,
          0.0010000814230470088,
          0.0010000808539779441
        ],
        "T": [
          1.6607833811937347,
          1.4928867785164637,
          1.4684280117808186,
          1.4457699507020516,
          1.3065067248204203,
          0.9858443513494252,
          0.7456835312514202,
          0.3296138517526932,
          0.02530065685166574,
          -0.20007147386219362,
          -0.5398081417257311,
          -0.7593826008918697,
          -0.8557235048236405,
          -1.1855228608000106,
          -1.3828957801737443,
          -1.4116866134188633,
          -1.4120319995795054,
          -1.4123103561933346,
          -1.4660242085361896,
          -1.512935264387252,
          -1.5565086084156623,
          -1.5682686222457247,
          -1.5756683301289272,
          -1.5802175633278004,
          -1.5802170555779347,
          -1.5676065745323686,
          -1.555469445366853,
          -1.5554701723088882,
          -1.5554788027980506,
          -1.5554787184955639,
          -1.6219238672791183,
          -1.670419375498139,
          -1.6704259308522633,
          -1.6704268079440694,
          -1.6704358270286706,
          -1.6357788350599085,
          -1.6318597737775915,
          -1.631859150478132,
          -1.6318689720231978,
          -1.6863621026159057,
          -1.6966502716726843,
          -1.69665205434674,
          -1.6945279925292953,
          -1.6933730447769857,
          -1.6957142386058823,
          -1.7196940094939872,
          -1.7465535073562757,
          -1.7666010607949465,
          -1.771353612785282,
          -1.7731994924051775,
          -1.8008021232833415,
          -1.866036353384365,
          -1.8906334228228723,
          -1.864272040983561,
          -1.890786131639456,
          -1.1924599228419959,
          -0.6870049646223689,
          -0.6870001262080228,
          -0.6869934828842448,
          -0.6869934828967081,
          -0.6869934829175333,
          -0.6869934829379427,
          -0.6869934829579367,
          -0.6869934829775136,
          -0.686993482996671,
          -0.6869934830154039,
          -0.6869934830337036,
          -0.6869934830515548,
          -0.686993483068928,
          -0.6869934830857641,
          -0.6869934831019264,
          -0.6869934831170459,
          -0.6869934831298329,
          -0.686993483136793,
          -0.6869934834497631
        ],
        "S": [
          33.467472794155434,
          33.45868278951647,
          33.45868315762573,
          33.647646473624114,
          33.74085385026331,
          33.76095785510792,
          33.801681874783725,
          33.85930100009265,
          33.921469810946896,
          33.98568540986409,
          34.033001577669936,
          34.07275873735322,
          34.107414420007956,
          34.124444949432046,
          34.20785598002516,
          34.255129991119475,
          34.25670744894207,
          34.26185903307561,
          34.282960586179016,
          34.308028924129545,
          34.32069171865757,
          34.3309234736942,
          34.3377133502802,
          34.33811339665909,
          34.338655790197464,
          34.342113225850994,
          34.35047943576404,
          34.35720324588949,
          34.36302379535271,
          34.3679378846917,
          34.37195942148805,
          34.375423652203565,
          34.378613011669856,
          34.38153519552919,
          34.38418605765033,
          34.38659228639152,
          34.38894145062746,
          34.39130829135094,
          34.39370601333748,
          34.3961264245905,
          34.3984222892823,
          34.40049135843291,
          34.40237558765785,
          34.40565348565611,
          34.412022487397934,
          34.420343579922445,
          34.42588014062876,
          34.42917063319703,
          34.43340031823423,
          34.437050048704755,
          34.44124652597061,
          34.448510701500076,
          34.45656176705909,
          34.46710372104415,
          34.46652746721304,
          34.57282815214046,
          34.65583635103022,
          34.655837165797884,
          34.65583813259517,
          34.65583813259554,
          34.65583813259512,
          34.6558381325947,
          34.65583813259429,
          34.655838132593885,
          34.655838132593495,
          34.65583813259311,
          34.65583813259274,
          34.65583813259235,
          34.655838132591995,
          34.65583813259164,
          34.65583813259131,
          34.655838132590986,
          34.6558381325907,
          34.65583813259052,
          34.65583813258381
        ],
        "U_H": [
          -0.021459094137468833,
          -0.0025375360030775885,
          -0.002449930599841866,
          -0.002404443533387943,
          -0.002422992870570039,
          -0.002420815969020599,
          -0.0023825222371003977,
          -0.0023129304664741713,
          -0.0022052388096918648,
          -0.0020608630961004553,
          -0.001896443291285098,
          -0.0017357071616308172,
          -0.0015848985643321246,
          -0.0014382729144698677,
          -0.0013045514572212148,
          -0.0011991998351477669,
          -0.0011082123524333673,
          -0.0010190358212987618,
          -0.0009250204424465908,
          -0.000837763987101757,
          -0.0007599149399366615,
          -0.0006859118796591436,
          -0.0006166571172598136,
          -0.0005501525944548589,
          -0.0004838512602678007,
          -0.00041921456374503574,
          -0.00036093050824115855,
          -0.00030889936596911147,
          -0.0002601142741924738,
          -0.00021262820461129077,
          -0.00016440083563997048,
          -0.00011416015938817534,
          -6.152280382571835e-05,
          -6.912743287110863e-06,
          4.923197071864409e-05,
          0.00010599073600706094,
          0.00016303150641228635,
          0.00022107112561881403,
          0.00028042512103038396,
          0.0003405108880421871,
          0.00040157905659340547,
          0.0004652487881276412,
          0.0005325248382542641,
          0.0006032220063354306,
          0.0006739703258207575,
          0.0007397731856719048,
          0.0007980893642066424,
          0.0008498959407347174,
          0.000898660135741558,
          0.0009549187898665858,
          0.0010424022484748722,
          0.0011388489919568847,
          0.0011838637426197587,
          0.00112204617253202,
          0.0010075420088704282,
          1.4739819654094683e-06,
          1.305293823719536e-06,
          1.1791498428533493e-06,
          1.0970212609993787e-06,
          1.0320246369561456e-06,
          9.668360061581929e-07,
          9.014553828371048e-07,
          8.358827651734644e-07,
          7.701181477419279e-07,
          7.041615250888343e-07,
          6.3801289174196e-07,
          5.716722422329063e-07,
          5.051395711528079e-07,
          4.3841487328965966e-07,
          3.7149814397821834e-07,
          3.0438938001296947e-07,
          2.370885820766379e-07,
          1.695957613161489e-07,
          1.0191095741370799e-07,
          3.4034292021153436e-08
        ],
        "V_H": [
          0.0033215273584691935,
          0.00039036554370956413,
          0.0004000315892748397,
          0.0003942747735676197,
          0.000438749011285657,
          0.0004938351894277204,
          0.0005449856416217656,
          0.0005814419380318484,
          0.0006014380951135394,
          0.0006066114564007651,
          0.0006049079810836429,
          0.0005992151550507385,
          0.0005880901064583569,
          0.0005753531799198703,
          0.0005708609067449904,
          0.0005634540452712068,
          0.0005455458407211191,
          0.0005293769576513241,
          0.0005253566732984418,
          0.0005298375597381913,
          0.0005355483288875116,
          0.000541569979833988,
          0.0005439140453994287,
          0.0005416380331668546,
          0.0005378894116280395,
          0.0005314427062269892,
          0.0005217805841772513,
          0.000511039702845637,
          0.0005006339604155403,
          0.0004913298628400023,
          0.0004844634141446547,
          0.00048103441551890756,
          0.0004798386155707127,
          0.0004801440861490886,
          0.00048112049985221905,
          0.0004812718839908261,
          0.00047985362547750077,
          0.0004774137207262189,
          0.0004738485159834172,
          0.00046855584405420007,
          0.00046112420382382575,
          0.00045099707617684393,
          0.00043716739621378365,
          0.000418002502360945,
          0.0003895405122723327,
          0.0003476297639092493,
          0.0002938335039436981,
          0.00022868397158723388,
          0.00012993254130362635,
          1.9800396014509996e-05,
          -7.691317559172143e-05,
          -0.00013102162236681059,
          -0.00014528664851317993,
          -0.00017808026265009905,
          -0.00021671245442938822,
          -0.00023261394293608333,
          -6.639474126118279e-07,
          -6.19211678683031e-07,
          -5.802924343229964e-07,
          -5.438144636903582e-07,
          -5.075052250402634e-07,
          -4.7136471219632546e-07,
          -4.353929194608411e-07,
          -3.995898410251495e-07,
          -3.639554710877477e-07,
          -3.284898038552858e-07,
          -2.931928335419827e-07,
          -2.5806455437011525e-07,
          -2.2310496057111173e-07,
          -1.8831404638709317e-07,
          -1.5369180607527053e-07,
          -1.1923823392221723e-07,
          -8.495332428692179e-08,
          -5.0837071776607915e-08,
          -1.688947432069574e-08
        ],
        "buoyFlux": [
          9.032828353872528e-09,
          1.2866555628338527e-08,
          7.807913415388703e-09,
          4.97532634390538e-09,
          3.2263179070693174e-09,
          1.9329936431418392e-09,
          1.1609583436030328e-09,
          5.888455304365381e-10,
          2.521178693556854e-10,
          1.0795035022678847e-10,
          4.6220365096926194e-11,
          1.9789236653736308e-11,
          8.472482783335893e-12,
          3.6272585812271554e-12,
          1.5528604461503458e-12,
          6.647777374007438e-13,
          2.84582643827872e-13,
          1.218227612682408e-13,
          5.2146786083149355e-14,
          2.2320271845149944e-14,
          9.552780401948823e-15,
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
          0.0,
          0.0,
          0.0,
          0.0,
          0.0
        ],
        "uStar": 0.005747923070719734,
        "p_surf": 99843.79217433969
      },
      "tolerance": {
        "rel": 1e-12
      },
      "assertions": [
        {
          "variable": "OBLdepth",
          "time": 0.0,
          "expected": 5.0
        },
        {
          "variable": "kOBL",
          "time": 0.0,
          "expected": 3.25
        },
        {
          "variable": "kfirst",
          "time": 0.0,
          "expected": 2.0
        },
        {
          "variable": "BulkRi",
          "time": 0.0,
          "expected": 0.32212992515778704,
          "coords": {
            "layer": 2
          }
        },
        {
          "variable": "deltaU2",
          "time": 0.0,
          "expected": 0.0003666170718174525,
          "coords": {
            "layer": 2
          }
        },
        {
          "variable": "N2",
          "time": 0.0,
          "expected": 1.727296730527845e-05,
          "coords": {
            "layer": 2
          }
        },
        {
          "variable": "BulkRi",
          "time": 0.0,
          "expected": 0.16929788493170425,
          "coords": {
            "layer": 3
          }
        },
        {
          "variable": "deltaU2",
          "time": 0.0,
          "expected": 0.0003698834359296671,
          "coords": {
            "layer": 3
          }
        },
        {
          "variable": "N2",
          "time": 0.0,
          "expected": 6.274410785296163e-06,
          "coords": {
            "layer": 3
          }
        },
        {
          "variable": "BulkRi",
          "time": 0.0,
          "expected": 6.2225753255175125,
          "coords": {
            "layer": 4
          }
        },
        {
          "variable": "deltaU2",
          "time": 0.0,
          "expected": 0.0003716485173394131,
          "coords": {
            "layer": 4
          }
        },
        {
          "variable": "N2",
          "time": 0.0,
          "expected": 0.0005773582527400012,
          "coords": {
            "layer": 4
          }
        },
        {
          "variable": "BulkRi",
          "time": 0.0,
          "expected": 14.820983319816479,
          "coords": {
            "layer": 5
          }
        },
        {
          "variable": "deltaU2",
          "time": 0.0,
          "expected": 0.00037068356244261615,
          "coords": {
            "layer": 5
          }
        },
        {
          "variable": "N2",
          "time": 0.0,
          "expected": 0.00028856037305597954,
          "coords": {
            "layer": 5
          }
        },
        {
          "variable": "BulkRi",
          "time": 0.0,
          "expected": 17.627734566321035,
          "coords": {
            "layer": 6
          }
        },
        {
          "variable": "deltaU2",
          "time": 0.0,
          "expected": 0.00037045187862207103,
          "coords": {
            "layer": 6
          }
        },
        {
          "variable": "N2",
          "time": 0.0,
          "expected": 0.00011595125916435778,
          "coords": {
            "layer": 6
          }
        },
        {
          "variable": "z_cell",
          "time": 0.0,
          "expected": -1.2435517972743582,
          "coords": {
            "layer": 1
          }
        },
        {
          "variable": "z_cell",
          "time": 0.0,
          "expected": -3.7363102457346455,
          "coords": {
            "layer": 2
          }
        },
        {
          "variable": "z_cell",
          "time": 0.0,
          "expected": -6.234748705087934,
          "coords": {
            "layer": 3
          }
        },
        {
          "variable": "z_cell",
          "time": 0.0,
          "expected": -8.73322531653016,
          "coords": {
            "layer": 4
          }
        },
        {
          "variable": "z_cell",
          "time": 0.0,
          "expected": -11.481539080697527,
          "coords": {
            "layer": 5
          }
        },
        {
          "variable": "z_cell",
          "time": 0.0,
          "expected": -14.479656385558034,
          "coords": {
            "layer": 6
          }
        },
        {
          "variable": "z_inter",
          "time": 0.0,
          "expected": -2.4871035945487163,
          "coords": {
            "iface": 2
          }
        },
        {
          "variable": "z_inter",
          "time": 0.0,
          "expected": -4.985516896920576,
          "coords": {
            "iface": 3
          }
        },
        {
          "variable": "z_inter",
          "time": 0.0,
          "expected": -7.483980513255292,
          "coords": {
            "iface": 4
          }
        },
        {
          "variable": "z_inter",
          "time": 0.0,
          "expected": -9.982470119805027,
          "coords": {
            "iface": 5
          }
        },
        {
          "variable": "z_inter",
          "time": 0.0,
          "expected": -12.980608041590024,
          "coords": {
            "iface": 6
          }
        },
        {
          "variable": "z_cell",
          "time": 0.0,
          "expected": -501.797147184804,
          "coords": {
            "layer": 75
          }
        },
        {
          "variable": "z_inter",
          "time": 0.0,
          "expected": -501.796647144377,
          "coords": {
            "iface": 75
          }
        }
      ]
    },
    {
      "id": "cell684_step10800_kfirst2_shallow",
      "description": "mom6_kpp_obl.csv row (i, j, tod) = (6, 84, 10800): kfirst = 2 (1-based, derived: not a dump column -- from kpp_ref.py), the two-point quadratic with zero slope at x1 through cell centers 1..2; the interpolated OBL depth 3.116 m is below the MINIMUM_OBL_DEPTH = 5 m floor, so OBLdepth pins the floored value 5.0; kOBL = 2.75 (the OBL sits between the layer-2 center and interface 3). Pins OBLdepth/kOBL, BulkRi/deltaU2/N2 at layers 2..kOBL+3 = 2..5 (layer 1 is 0 by construction), spot z_cell at layers 1..5 and z_inter at ifaces 2..5 (iface 1 is the surface), plus the deep z_cell/z_inter at layer/iface 75, at rel 1e-12.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "h": [
          2.5041168640077416,
          2.5033753934154017,
          2.502852239218575,
          2.5028792972384046,
          3.0033735442726885,
          3.00323944542302,
          4.004077240491185,
          5.004667857957694,
          5.00413485810045,
          5.003606989829584,
          5.003153627500254,
          5.002748644146832,
          5.00236063760573,
          5.001983366993674,
          5.001702051039733,
          5.001573341641267,
          5.001499403303531,
          5.001470838745779,
          5.001566558336097,
          5.001917642017238,
          5.002653532630114,
          5.003968229118622,
          5.0061403591881195,
          5.009609958438806,
          5.01493804540558,
          5.022913265250659,
          5.03457992195803,
          5.051300829417199,
          5.074855238826649,
          5.107508190287161,
          5.15211722103413,
          5.212247473471368,
          5.2922891642347025,
          5.397617038888854,
          5.534776788180079,
          5.711660783557889,
          5.937746738034335,
          6.224322188195828,
          6.584758523826822,
          7.034795655955988,
          7.592881879759502,
          8.28052407296319,
          9.122657886707753,
          10.148181084234881,
          11.390224442839799,
          12.886573744354058,
          14.682011506774685,
          16.825535183670343,
          19.371560327362538,
          22.385027510671108,
          25.938026599133845,
          30.110692433689966,
          34.99281533450334,
          40.68636117864267,
          47.30250231616687,
          54.96732652418979,
          63.81832795505333,
          74.00669641317309,
          17.81887059598174,
          0.0009999660571455287,
          0.0009999662390787192,
          0.0009999662440085526,
          0.0009999663674575847,
          0.0009999664927465705,
          0.0009999666204533256,
          0.0009999666342160672,
          0.000999966652052548,
          0.0009999666757344685,
          0.000999966813177764,
          0.0009999669310683972,
          0.0009999669822725332,
          0.0009999670151138564,
          0.0009999667843876572,
          0.000999962989978671,
          0.0009999704913697708
        ],
        "dz": [
          2.5041168640077416,
          2.5033753934154017,
          2.502852239218575,
          2.5028792972384046,
          3.0033735442726885,
          3.00323944542302,
          4.004077240491185,
          5.004667857957694,
          5.00413485810045,
          5.003606989829584,
          5.003153627500254,
          5.002748644146832,
          5.00236063760573,
          5.001983366993674,
          5.001702051039733,
          5.001573341641267,
          5.001499403303531,
          5.001470838745779,
          5.001566558336097,
          5.001917642017238,
          5.002653532630114,
          5.003968229118622,
          5.0061403591881195,
          5.009609958438806,
          5.01493804540558,
          5.022913265250659,
          5.03457992195803,
          5.051300829417199,
          5.074855238826649,
          5.107508190287161,
          5.15211722103413,
          5.212247473471368,
          5.2922891642347025,
          5.397617038888854,
          5.534776788180079,
          5.711660783557889,
          5.937746738034335,
          6.224322188195828,
          6.584758523826822,
          7.034795655955988,
          7.592881879759502,
          8.28052407296319,
          9.122657886707753,
          10.148181084234881,
          11.390224442839799,
          12.886573744354058,
          14.682011506774685,
          16.825535183670343,
          19.371560327362538,
          22.385027510671108,
          25.938026599133845,
          30.110692433689966,
          34.99281533450334,
          40.68636117864267,
          47.30250231616687,
          54.96732652418979,
          63.81832795505333,
          74.00669641317309,
          17.81887059598174,
          0.0009999660571455287,
          0.0009999662390787192,
          0.0009999662440085526,
          0.0009999663674575847,
          0.0009999664927465705,
          0.0009999666204533256,
          0.0009999666342160672,
          0.000999966652052548,
          0.0009999666757344685,
          0.000999966813177764,
          0.0009999669310683972,
          0.0009999669822725332,
          0.0009999670151138564,
          0.0009999667843876572,
          0.000999962989978671,
          0.0009999704913697708
        ],
        "T": [
          1.514663296426248,
          1.5078194156960034,
          1.4836225670727965,
          1.4438076529528194,
          1.2724699525138998,
          0.9906641927033523,
          0.766772962255386,
          0.22180542355605867,
          -0.36476103158057543,
          -0.6012520414343,
          -0.8407134535289784,
          -1.1061876787618898,
          -1.3098919702882694,
          -1.4613371371183412,
          -1.5526359677190538,
          -1.5897778504048556,
          -1.618784602685295,
          -1.6387292760777876,
          -1.6682742394723524,
          -1.6877604216556674,
          -1.7012762717686276,
          -1.7174043764023292,
          -1.7234486608232387,
          -1.7236697175051918,
          -1.723828286390059,
          -1.7241021791117543,
          -1.7265802558254313,
          -1.7337849168809631,
          -1.7459285586496625,
          -1.7627417538299863,
          -1.8125398252116656,
          -1.8390641030423902,
          -1.8396625916912335,
          -1.8396891967711915,
          -1.8395362116077145,
          -1.8300321985744081,
          -1.8285120353359745,
          -1.8284883043380933,
          -1.8286956894255875,
          -1.849584791140757,
          -1.872479476090263,
          -1.8874179853292852,
          -1.8955909483402908,
          -1.9035402609969427,
          -1.9180835647854193,
          -1.9401413745316354,
          -1.955500031087337,
          -1.9572621300681907,
          -1.9679574167731795,
          -1.9694111182209173,
          -1.965979703356985,
          -1.9436787360836396,
          -1.9403463835734942,
          -1.9258891862963528,
          -1.9394467705910081,
          -1.9909699186556977,
          -1.866034183644195,
          -1.8473600169830247,
          -1.8508934101714851,
          -1.585403821833288,
          -1.5851934656872473,
          -1.5851934636412581,
          -1.5851940178449655,
          -1.585184609650856,
          -1.58517242942471,
          -1.5851720389601025,
          -1.5851720406867318,
          -1.585172112037718,
          -1.5851685010196503,
          -1.5851680733484619,
          -1.5851681005732996,
          -1.5851681006161646,
          -1.585168100590758,
          -1.5851681006706184,
          -1.58516810091822
        ],
        "S": [
          33.51764375464253,
          33.51861770858134,
          33.52247877166672,
          33.710699997346374,
          33.845295370094924,
          33.92932899591545,
          33.98992553700961,
          34.067434632524545,
          34.15975971012252,
          34.23399629267246,
          34.275091245797334,
          34.29249640867812,
          34.31202076817955,
          34.324804379336754,
          34.34638917365343,
          34.37042821395161,
          34.37409030353961,
          34.379319475703646,
          34.38927722821,
          34.39706233958499,
          34.4023040293379,
          34.40708369446829,
          34.41059899468786,
          34.41108656434706,
          34.41188396803518,
          34.41654430057424,
          34.42671566810949,
          34.43383465669087,
          34.439006235792284,
          34.44225493529557,
          34.44362366798367,
          34.444234561605036,
          34.44504397355399,
          34.44614902832121,
          34.447566197619146,
          34.44925455471183,
          34.4509800663322,
          34.45262524406036,
          34.45417999051142,
          34.45565384196664,
          34.45704110512889,
          34.45831799866321,
          34.45974524363342,
          34.46010256766271,
          34.46007218583453,
          34.459647375904986,
          34.45904425161166,
          34.458975224249066,
          34.458823452609636,
          34.462097114958326,
          34.467390633863786,
          34.47364158805676,
          34.478662989632056,
          34.48190426202777,
          34.48231050884303,
          34.481821513959204,
          34.493716376848354,
          34.502878027691075,
          34.52107711743892,
          34.56758813228551,
          34.567601648645685,
          34.567601648945,
          34.56760274137758,
          34.56760440412144,
          34.56760543318764,
          34.56760514330064,
          34.567605143159135,
          34.567605397425446,
          34.56760600722265,
          34.567605769420666,
          34.56760576421831,
          34.56760576422335,
          34.56760576423253,
          34.56760576422958,
          34.5676057642086
        ],
        "U_H": [
          -0.015058069979878014,
          -0.00892317330611957,
          -0.0070254505046611895,
          -0.006984605332778976,
          -0.0069275000904106985,
          -0.006837236544568201,
          -0.0067026222040882785,
          -0.006515470860027463,
          -0.0062967961690595054,
          -0.006073005016718441,
          -0.005866939321332141,
          -0.005666194645519889,
          -0.005453322826411535,
          -0.005233116683967678,
          -0.005047523924584058,
          -0.004928825317659406,
          -0.004829657722948087,
          -0.00472317469539193,
          -0.004618417028598618,
          -0.004533967136118191,
          -0.004462995059999835,
          -0.00439835111271376,
          -0.00433084842704319,
          -0.004262999991383192,
          -0.004189979922406063,
          -0.004110519493668154,
          -0.004026772101108153,
          -0.0039391714220930185,
          -0.0038490169110690906,
          -0.003758060480068549,
          -0.0036698534599235695,
          -0.0035912669349337863,
          -0.0035196214727769197,
          -0.003450380923289337,
          -0.0033832286360367153,
          -0.003310032635798515,
          -0.0032356601212671214,
          -0.0031564813793267268,
          -0.0030728287750218597,
          -0.0029830122547828664,
          -0.0028862292189429013,
          -0.0027804903993340546,
          -0.0026603814144953637,
          -0.0025269032214826344,
          -0.0023823193702137103,
          -0.00220916387643184,
          -0.001971854295686637,
          -0.0019480726964868104,
          -0.0016310111748612675,
          -0.0013724523562408573,
          -0.001109490687830013,
          -0.0007969306750320288,
          -0.00038814813399518935,
          9.881428576544242e-05,
          0.0006287321720932888,
          0.0011698669418186147,
          0.0018236006291927202,
          0.0026695370516290695,
          0.0029379289166290693,
          9.658616405716074e-07,
          8.016051489691953e-07,
          8.006914158395017e-07,
          6.366411203662422e-07,
          4.72721897290104e-07,
          3.0895911265089367e-07,
          3.080451614231462e-07,
          3.0713115842745226e-07,
          3.0667310043441864e-07,
          1.8656610444569588e-07,
          9.294831006537962e-08,
          9.158380488859508e-08,
          9.067379537905855e-08,
          8.976345508141219e-08,
          8.885321749039102e-08,
          8.83959180362342e-08
        ],
        "V_H": [
          0.007237632704842369,
          0.0026810093739407324,
          0.0017807407962581784,
          0.0017178368458889049,
          0.0017659904829296518,
          0.001846849371212295,
          0.0019444535648347756,
          0.0020901551897853222,
          0.002284848539855461,
          0.002468421090070652,
          0.0026120414056994275,
          0.00272403682481078,
          0.002815963110283382,
          0.0028961035846039557,
          0.002948932867939202,
          0.00296511338017341,
          0.002978573317998702,
          0.003002880406127712,
          0.0030329522129120216,
          0.003053686350552756,
          0.003065766786839776,
          0.0030734939126790184,
          0.003080261375088341,
          0.003085746442683687,
          0.0030914328457897285,
          0.0030992865507618902,
          0.0031166621283410254,
          0.0031447844111883627,
          0.0031786885363046134,
          0.003214292637255756,
          0.003247602725596692,
          0.003274882674047569,
          0.0032962848487857258,
          0.0033139983323396635,
          0.0033291816033143994,
          0.0033448097005918886,
          0.0033615126364710743,
          0.0033800813938021975,
          0.003401161202556715,
          0.00342638846353357,
          0.003456899556955942,
          0.003492808299264428,
          0.003536380949275096,
          0.003581729495848931,
          0.003619417730372292,
          0.0036536020678741496,
          0.003691865663752225,
          0.003683246750505859,
          0.0037318420918416376,
          0.003748312948666897,
          0.003742142814363933,
          0.0037025421364148786,
          0.0036416951575622084,
          0.003543594341623433,
          0.003427342574815941,
          0.0033526879811078387,
          0.0033699102419387466,
          0.0034307044023119877,
          0.0033573559142625917,
          2.3730286868781763e-06,
          1.996325765124707e-06,
          1.994616885335119e-06,
          1.6173491522032178e-06,
          1.239830782889315e-06,
          8.620906429287654e-07,
          8.603743570152107e-07,
          8.59513332656633e-07,
          8.577933486042685e-07,
          4.801812966897735e-07,
          2.170655327184449e-07,
          2.144872108532211e-07,
          2.1276818468350018e-07,
          2.1104752713198177e-07,
          2.093252467140127e-07,
          2.0793839084522552e-07
        ],
        "buoyFlux": [
          4.357319887014113e-08,
          2.4300917727683458e-08,
          1.519242766407754e-08,
          9.979998575301585e-09,
          6.672200085298669e-09,
          4.146592082792006e-09,
          2.5832888400521458e-09,
          1.3758149516308767e-09,
          6.261715806348754e-10,
          2.8502763062231407e-10,
          1.2975276708240533e-10,
          5.907139958905437e-11,
          2.689462886646681e-11,
          1.2245608005242638e-11,
          5.57597631050029e-12,
          2.539105242213919e-12,
          1.1562434238891161e-12,
          5.265297317096402e-13,
          2.3977200487272277e-13,
          1.0918613967985063e-13,
          4.971787611259811e-14,
          2.2636399979419572e-14,
          1.030415423071857e-14,
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
          0.0,
          0.0,
          0.0
        ],
        "uStar": 0.0020634389900162525,
        "p_surf": 99750.64598157027
      },
      "tolerance": {
        "rel": 1e-12
      },
      "assertions": [
        {
          "variable": "OBLdepth",
          "time": 0.0,
          "expected": 5.0
        },
        {
          "variable": "kOBL",
          "time": 0.0,
          "expected": 2.75
        },
        {
          "variable": "kfirst",
          "time": 0.0,
          "expected": 2.0
        },
        {
          "variable": "BulkRi",
          "time": 0.0,
          "expected": 0.5410254394634735,
          "coords": {
            "layer": 2
          }
        },
        {
          "variable": "deltaU2",
          "time": 0.0,
          "expected": 5.8399773377409545e-05,
          "coords": {
            "layer": 2
          }
        },
        {
          "variable": "N2",
          "time": 0.0,
          "expected": 4.703450909358977e-06,
          "coords": {
            "layer": 2
          }
        },
        {
          "variable": "BulkRi",
          "time": 0.0,
          "expected": 1.6609929747627934,
          "coords": {
            "layer": 3
          }
        },
        {
          "variable": "deltaU2",
          "time": 0.0,
          "expected": 9.430064493560425e-05,
          "coords": {
            "layer": 3
          }
        },
        {
          "variable": "N2",
          "time": 0.0,
          "expected": 1.7883674218046472e-05,
          "coords": {
            "layer": 3
          }
        },
        {
          "variable": "BulkRi",
          "time": 0.0,
          "expected": 68.15523405922688,
          "coords": {
            "layer": 4
          }
        },
        {
          "variable": "deltaU2",
          "time": 0.0,
          "expected": 9.564897773247781e-05,
          "coords": {
            "layer": 4
          }
        },
        {
          "variable": "N2",
          "time": 0.0,
          "expected": 0.0005785182874386133,
          "coords": {
            "layer": 4
          }
        },
        {
          "variable": "BulkRi",
          "time": 0.0,
          "expected": 174.1088263557773,
          "coords": {
            "layer": 5
          }
        },
        {
          "variable": "deltaU2",
          "time": 0.0,
          "expected": 9.604503533213051e-05,
          "coords": {
            "layer": 5
          }
        },
        {
          "variable": "N2",
          "time": 0.0,
          "expected": 0.00040910973404685954,
          "coords": {
            "layer": 5
          }
        },
        {
          "variable": "z_cell",
          "time": 0.0,
          "expected": -1.2520584320038708,
          "coords": {
            "layer": 1
          }
        },
        {
          "variable": "z_cell",
          "time": 0.0,
          "expected": -3.7558045607154424,
          "coords": {
            "layer": 2
          }
        },
        {
          "variable": "z_cell",
          "time": 0.0,
          "expected": -6.258918377032431,
          "coords": {
            "layer": 3
          }
        },
        {
          "variable": "z_cell",
          "time": 0.0,
          "expected": -8.76178414526092,
          "coords": {
            "layer": 4
          }
        },
        {
          "variable": "z_cell",
          "time": 0.0,
          "expected": -11.514910566016466,
          "coords": {
            "layer": 5
          }
        },
        {
          "variable": "z_inter",
          "time": 0.0,
          "expected": -2.5041168640077416,
          "coords": {
            "iface": 2
          }
        },
        {
          "variable": "z_inter",
          "time": 0.0,
          "expected": -5.007492257423143,
          "coords": {
            "iface": 3
          }
        },
        {
          "variable": "z_inter",
          "time": 0.0,
          "expected": -7.510344496641718,
          "coords": {
            "iface": 4
          }
        },
        {
          "variable": "z_inter",
          "time": 0.0,
          "expected": -10.013223793880123,
          "coords": {
            "iface": 5
          }
        },
        {
          "variable": "z_cell",
          "time": 0.0,
          "expected": -715.8093954578029,
          "coords": {
            "layer": 75
          }
        },
        {
          "variable": "z_inter",
          "time": 0.0,
          "expected": -715.8088954725572,
          "coords": {
            "iface": 75
          }
        }
      ]
    }
  ]
}
```

</details>
