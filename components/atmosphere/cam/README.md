# CAM6 stage 2 — the CAM physics `.esm` components

Stage-2 implementation of the CAM6 atmospheric physics slice of the EqESM
project, ported into the corpus as esm 2.0.0 files: the saturation
thermodynamics (`qsat`), the energy fixer, the Rayleigh friction, the surface
exchange (cam_out exports + cam_in imports), the implicit vertical-diffusion
solve, the `physics_update` state law, the RRTMG radiation chain (state
construction, solar input, solver inputs, McICA subcolumn masking, heating
rates), the RRTMG shortwave and longwave column solvers, and the
Zhang–McFarlane deep-convection subassembly (parcel/CAPE, closure, q1q2
tendencies, rain evaporation). Every file is pinned by the stage-1
instrumentation dumps of the SCAM reference run `C_JRA_t62_scam_inst`
(`stage1/dumps/cam/cam_qsat.csv`, `cam_phys_tend.csv`, `cam_vdiff_prof.csv`,
`cam_vdiff_q.csv`, `cam_surface_exchange.csv`, `cam_surface_cflx.csv`,
`cam_rad_*.csv`, `cam_rad_rtrnmc*.csv`, `cam_zm*.csv`,
`cam_zm_parcel*.csv`, `cam_tend_total.csv`; 48-step window, `dt = 1800 s`).

Sources: `components/cam/src/` of the instrumented cam6_4_212 fork
(`stage1/EqESM-cesm-cam`, branch `instrument/cam-dumps`, cam submodule
`81922142`): `atmos_phys/to_be_ccppized/wv_saturation.F90` and
`wv_sat_methods.F90`, `atmos_phys/schemes/rayleigh_friction/
rayleigh_friction.F90`, `atmos_phys/schemes/vertical_diffusion/
vertical_diffusion_solver.F90` + `diffusion_solver.F90` +
`linear_1d_operators.F90`, `physics/cam/check_energy.F90` +
`atmos_phys/schemes/conservation_adjust/check_energy/check_energy_fix.F90`,
`control/camsrfexch.F90` + `utils/cam_diagnostic_utils.F90`,
`physics/cam/physics_types.F90` (`physics_update`) + `physpkg.F90`,
`physics/rrtmg/` (`radiation.F90`, `radsw.F90`, `radlw.F90`,
`rrtmg_state.F90`, `radconstants.F90`, `aer_src/mcica_subcol_gen_sw.f90`,
`aer_src/mcica_subcol_gen_lw.f90`, `aer_src/rrtmg_sw_cldprmc.f90`,
`aer_src/rrtmg_sw_reftra.f90`, `aer_src/rrtmg_sw_spcvmc.f90`,
`aer_src/rrtmg_sw_vrtqdr.f90`, `aer_src/rrtmg_lw_rtrnmc.f90`,
`rrtmg_sw_init.f90`, `rrtmg_lw_init.f90`, `rrlw_tbl.f90`,
`rrtmg_lw_rad.f90`), and `atmos_phys/schemes/zhang_mcfarlane/zm_convr.F90` +
`physics/cam/zm_conv_intr.F90` + `zm_conv_evap.F90`.  Site numbering per
`stage1/runs/CAM_LANE.md` and the boundary table in
`stage1/runs/cam_instrument.json`; dump validation:
`stage1/analysis/validate_cam_*.py` (ALL DUMP CHECKS PASSED 2026-11-05/08).

The lane leaves out the EqESM driver assembly (`cam_physics_column*.esm`,
stage-3 work) and the orographic gravity-wave drag lane (`cam_gw.esm`, still
in progress in the EqESM project).  All model logic lives in the `.esm`
files; this README is the human-readable map, merged from the nine stage-2
lane READMEs (`README-cam.md`, `README-cam-physics-update.md`,
`README-cam-radiation.md`, `README-cam-rrtmg-solver.md`,
`README-cam-rrtmg-lw.md`, `README-cam-zm.md`, `README-cam-zm-assembly.md`,
`README-cam-zm-evap.md`, `README-cam-zm-parcel.md`).

## File map

| File | Contents |
|---|---|
| `cam_templates.esm` | the shared expression-template library (33 templates): the saturation laws (`ice_weight`, `goff_gratch_water`, `goff_gratch_ice`, `svp_trans`, `svp_to_qsat`, `hltalt_no_ip`, `hltalt_mixed`, `pcf_transition_poly`, `tterm_transition`, the constant fragments `tkfrz`/`tboil`/`ttrice`, `estbl_tmax`, `estbl_es0`), the `physics_update` laws (`constituent_update`, `state_cnst_min_nz_mask`, `virtual_temperature_factor`), the surface-exchange laws (`density_dry_air`, `exner_function`), the vertical-diffusion laws (`interface_diffusivity`, `surface_layer_source`, `surface_stress_coefficient`, `wind_damping_rate`), the ZM/evap laws (`zm_mass_flux_excess`, `zm_flux`, `zm_flux_divergence`, `zm_subcloud_tendency`, `zm_evap_flux_step`, `zm_evap_snow_frac`), `guarded_ratio`, `edge_shift`, `band_gather`, `physics_update_step`, `zero_if`, `fortran_sign`, `tndmax_ratio`; imports `tkfrz` by reference from the CDEPS templates and `linear` from `esm:std/interp.esm` |
| `cam_wv_saturation.esm` | the `estbl` function table (251 knots, Goff–Gratch mixed phase) + `WvSaturation` (the run's qsat law) + `SvpTransLaw` (pins the table-generation formula) — 65 assertions |
| `cam_energy_fixer.esm` | `EnergyFixer` — the uniform `heat_glob` dry-energy tendency and the implied surface flux (`check_energy_fix.F90:37-44`) — 6 assertions |
| `cam_rayleigh_friction.esm` | `RayleighFriction` — the otau profile + Euler-backward tendencies — 27 assertions |
| `cam_surface_exchange.esm` | `CamOutExport` (the cam_out export laws: rho, thbot, topo, the cpslec sea-level-pressure chain incl. the flat branch, the precipitation split, co2diag/co2prog; the pass-throughs as documented imports) + `CamInImports` (the cam_in coupler imports with their consumption sites and the flx_net accumulation) — 23 assertions |
| `cam_vertical_diffusion.esm` | `VerticalDiffusion` — the implicit Euler-backward vdiff solve as four PDEs on the `column_nonuniform_1d` grid, lowered by the ESD `varcoeff_face_laplacian_lev_flux_bc` and `integral_lev_whole` rules — 31 assertions |
| `cam_physics_update.esm` | `PhysicsUpdate` + `TendAccumulation` — the state-update law applied after every parameterization (windowed u/v/q/T update, the qneg3/number clamps, the CLDLIQ/CLDICE pair zeroing, the hydrostatic geopotential recomputation, the s update, the per-call tend accumulation as a masked sum over the 15 tphysbc call sites) — 162 assertions |
| `cam_radiation.esm` | the RRTMG radiation chain as six models (`CamRadState` state construction, `CamRadSolin` incident solar, `CamRadSolverInputs` ssa/asm/fsfc ratios, `CamRadMcicaSw`/`CamRadMcicaLw` subcolumn masking, `CamRadHeating` flux-divergence heating) — 192 assertions |
| `cam_rrtmg_solver.esm` | the RRTMG shortwave column solver as five models (delta-M cloud scaling via the CICE `dEdd_scaled_*` laws, the PIFM layer solve, the direct beam, the adding-method flux assembly, the band sums) — 76 assertions |
| `cam_rrtmg_lw.esm` | the RRTMG longwave `rtrnmc` solver as two models (`CamRrtmgLwSweep`: the secdiff angles, the McICA cloud scaling, the Pade-table gas laws, the unified direction-matched sweeps, the specular surface, the per-g-point flux scaling; `CamRrtmgLwFluxes`: the band sums and heating rates) — 1188 assertions |
| `cam_zm.esm` | the ZM deep-convection subassembly: mounts Parcel/Closure/Q1Q2/Evap by reference, the inline `Control` driver model (the precipitation budget, the t1/q1 physics_update advance), the 37 wiring edges imported from the coupling library — 50 assertions |
| `cam_zm_parcel.esm` | `Parcel` — buoyan_dilute (qst/hmn/hsat, the virtual temperatures, the Raymond–Blyth entropy, the CAPE integral) — 250 assertions |
| `cam_zm_closure.esm` | `Closure` — the closure mass flux mb (dsubcld, the launch-level block, the cumulus heating/drying, the virtual potential temperatures, the dadt integral) — 30 assertions |
| `cam_zm_q1q2.esm` | `ZMq1q2` — the q1q2_pjr temperature/moisture tendencies (the plume-flux divergence and subcloud forms) — 30 assertions |
| `cam_zm_evap.esm` | `ZMevap` — the zm_conv_evap_run rain/snow evaporation step (the Sundqvist rate with its three limits, the melt split, the flux steps, the estbl qs lookup) — 68 assertions |
| `cam_zm_templates.esm` | the 17 ZM expression templates (zm_qsat_hPa, the moist static energies, the virtual temperatures, the entropy, the closure per-level laws) |
| `cam_zm_coupling.esm` | coupling library (esm-spec §10.9) — the single source of the 37 ZM-internal wiring edges, imported by `cam_zm.esm` (and by the EqESM `cam_physics_column.esm` driver) |

2198 assertions total (65 + 6 + 27 + 23 + 31 + 162 + 192 + 76 + 1188 + 50 +
250 + 30 + 30 + 68).  Every expected value is a real dump row — step, cell
and level cited in the test description — except the explicitly-labelled
compiled-Fortran references (the rayleigh/energy-fixer enabled branches, the
nonzero-K vdiff operator) and the DERIVED replicas (the entropy and
virtual-temperature states of the parcel lane, the evap `evpvint` running
accumulator).

## The qsat law and the estbl table (`cam_wv_saturation.esm`, `cam_templates.esm`)

The run's `qsat_line` with ip = 0 evaluates the **tabulated** form
(`wv_saturation.F90:739-784`):

```
es0 = estblf(T)                       ! linear interp of the estbl table,
                                      ! t_tmp = clamp(T - 127.16 K, 0, 248 K),
                                      ! flat clamps at both ends (F90:378-393)
qs  = svp_to_qsat(es0, p)             ! epsilo·es/(p - omeps·es), or 1 when
                                      ! p - es <= 0 (wv_sat_methods.F90:185-197)
es  = min(es0, p)
hltalt = calc_hltalt(T)               ! mixed-phase latent heat (F90:521-573)
tterm  = transition d(es)/dT term     ! pcf polynomial / ttrice (F90:548-573)
desdt = hltalt·es/(rh2o·T²) + tterm   ! d(es)/dT (F90:671-673)
dqsdt = qs·p·desdt/(es·(p - omeps·es)), 0 when qs == 1   (F90:676-679)
gam   = dqsdt·hltalt/cpair            ! the dumped gam (dqsdT), (F90:683-686)
```

`wv_sat_init` (F90:191-254) builds the 251-knot `estbl` at T = 127.16..377.16 K
from `svp_trans` (`wv_sat_methods.F90:479-513`): the Goff–Gratch water
(F90:569-580) and ice (F90:611-620) formulas blended by `ice_weight` over the
20 K band below 273.15 K.  In the esm the table is a `function_tables` entry
and `estblf` is `table_lookup` with `interpolation: linear`,
`out_of_bounds: clamp` on `min(T, 375.16 K)` — the esm blend `tᵢ + w·(tᵢ₊₁ −
tᵢ)` differs from the Fortran's `(1−w)·tᵢ + w·tᵢ₊₁` by at most 1 ulp.  The
`SvpTransLaw` model pins the analytic generation formula itself at five
temperatures spanning the pure-ice, transition, and water branches (incl. the
estbl first and last reachable knots 127.16 and 375.16 K).  The Goff–Gratch
curve-fit coefficients are dimensionless as written (dimensionally incoherent
fit: a log10 of an hPa-valued number, exponentiated and ×100); the ×100
factor carries the Pa dimension so the analytic laws read as Pa.

`table_lookup` resolves only against the declaring document's
`function_tables` block (there is no by-reference table mechanism in the CLI,
probed), so the 251 values are a per-document data copy — the identical
`function_tables.estbl` entry in `cam_wv_saturation.esm` and
`cam_zm_evap.esm`, data-identical and script-verified.  `cam_templates.esm`
imports the freezing point `tkfrz` = 273.15 K by reference from the CDEPS
templates (`../../data_models/cdeps/cdeps_templates.esm`, SHR_CONST_TKFRZ) so
the constant has one canonical definition across the CAM and CDEPS lanes.

## The energy fixer (`cam_energy_fixer.esm`)

```
ptend_s = heat_glob                     ! uniform dry-energy tendency, J/kg/s
eshflx  = heat_glob·(ps − ptop)/gravit  ! = heat_glob·(pint(pver+1) − pint(1))/gravit
```

`heat_glob` is the global-mean heating from `check_energy_cam_fix`
(`check_energy.F90:637-702`); in the SCAM run it is 0 (the IOP forcing is not
CAM-generated, `use_camiop = .false.`), so the dumped `ptend_s` rows are all
0 and the dump pins exercise exactly that branch.  `ps` is dumped; `ptop` =
pint(1) is **not** dumped and is derived from the dump rows as `ps − Σ pdel =
225.5239523947239 Pa`, constant across the window (documented in the model).
The nonzero-branch pin (heat_glob = 0.25 J/kg/s → eshflx =
2361.3585380814457 W/m²) is a compiled-Fortran reference.

## The Rayleigh friction (`cam_rayleigh_friction.esm`)

```
krange = raykrange, or (rayk0 − 1)/2 when raykrange = 0     (F90:89-92)
otau(k) = otau0·(1 + tanh((rayk0 − k)/krange))/2,  otau0 = 1/(86400·raytau0)
c2 = 1/(1 + otau·ztodt);  c1 = −otau·c2;  c3 = 0.5·(1 − c2²)/ztodt
dudt = c1·u;  dvdt = c1·v;  dsdt = c3·(u² + v²)              (F90:149-156)
```

When `raytau0 = 0` the run returns zeros before the profile (F90:113-115);
the model reproduces that branch exactly.  The dump window runs raytau0 = 0,
so the dump pins exercise the zero branch; the enabled-branch pins are
compiled-Fortran references.  Note the glibc tanh saturation: with the
default profile (krange = 0.5) the argument (2 − k)/0.5 reaches −20 at k = 12
and tanh(−20) = −1 exactly, so otau and the tendencies vanish exactly at k ≥
12 even when enabled — pinned as `enabled_krange0_k12_saturation`; a
raykrange = 10 pin set exercises nonzero damping of the O(1) winds.  The esm
c3 writes `/ztodt` where the Fortran multiplies by rztodt = 1/ztodt (≤ 1
ulp).

## The surface exchange (`cam_surface_exchange.esm`)

Model `CamOutExport` transcribes the cam_out export laws of `cam_export`
(`camsrfexch.F90:405-577`):

```
rho    = pbot/(rair·tbot)                 ! dry-air density (F90:503)
thbot  = tbot·exner_function(pbot, ps, κ) ! (F90:496, dp_coupling.F90:731-733),
                                          ! κ = cappa = rair/cpair (this run)
topo   = phis/gravit                      ! surface topographic height (F90:498)
psl    = cpslec(t, pmid, ps, phis)        ! ECMWF sea-level pressure
                                          ! (cam_diagnostics.F90:1080-1081,
                                          !  cam_diagnostic_utils.F90:20-81)
precc  = max(0, prec_dp + prec_sh)        ! pbuf PREC/Snow fields (F90:537-575)
precl  = max(0, prec_sed + prec_pcw)
precsc = min(precc, max(0, snow_dp + snow_sh))
precsl = min(precl, max(0, snow_sed + snow_pcw))
co2diag = co2vmr·1e6 [ppmv]               ! chem_surfvals CO2VMR (F90:506-511)
co2prog = 0                               ! co2_transport() false here (F90:512-516)
```

The remaining cam_out exports (tbot/zbot/ubot/vbot/qbot/pbot direct state
copies; ozone/netsw/flwds/soll/sols/solld/solsd pbuf pass-throughs) are
**documented imports** — no equations (an equation `tbot = t_bot` cannot fail
and would only restate the import).  The psl law runs in
`diag_phys_writeout` **before** this step's radiation update (verified
bit-exact against the dumped psl using the pre-radiation state), so the model
takes two bottom-level temperatures: `tbot` (at cam_export) and `t_psl` (at
psl time).  The cpslec chain transcribes the branch structure of
`cam_diagnostic_utils.F90:44-77` with the named shared predicates
psl_b1/psl_b2 and the flat branch (|phis/gravit| < 1e-4 → psl = ps) as
`ifelse(|topo| < 1e-4 m, ps, ps·exp(...))`.  Transcription note: the first
draft had the two series signs flipped (1 + αβ/2 − (αβ)²/3); all 48 window
steps take branch 2 where α = 0 makes the correction vanish, so the dump pins
could not detect it — the esm now transcribes the Fortran signs exactly.

Model `CamInImports` documents the 20 cam_in fields as pure coupler imports
with their physics consumption sites, and the one CAM-side combination of
coupler fluxes, the flx_net accumulation of tphysac (physpkg.F90:1533):

```
flx_net = net_flx_rad + shf
         + (precc + precl)·latvap·rhoh2o + (precsc + precsl)·latice·rhoh2o
```

CAM has **no law** relating cam_in%lhf to cam_in%cflx: the coupler computes
both consistently (dumped lhf/cflx_Q = LATVAP exactly on every row), so the
esm keeps them as independent inputs — the consistency is a coupler property,
not implemented.

## The vertical diffusion solve (`cam_vertical_diffusion.esm`)

The CAM6 vertical-diffusion solve (the implicit Euler-backward finite-volume
solve of `diffusion_solver.F90` called by `vertical_diffusion_solver.F90`)
as four PDEs on the EarthSciDiscretizations `column_nonuniform_1d` grid:

```
du/dt = d/dz(K_mom du/dz) + tau_damp u + src_u        (v mirrored)
ds/dt = d/dz(K_th   ds/dz) + dtk/dt + src_s
dq/dt = d/dz(K_q    dq/dz) + src_q
```

with `K_* = interface_diffusivity(kv_*, dpidz_sq) = kv_*·dpidz_sq` on the
interfaces and the surface sources `src_* = surface_layer_source(flux, g,
dz, zero)` — the pver injection g·flux/dz[1]: `src_u = g·tauresx_enter·ramda/
dz[1]` (residual-stress injection, F90:491-499), `src_s = g·shflux/dz[1]`
(F90:779), `src_q = g·cflx·dryfac/dz[1]` (F90:974-975, 1056-1061) — with
`ramda = dt/timeres = 0.25`.  The wind damping `tau_damp = wind_damping_rate`
is −g·ksrf/dz[1] at the surface layer and 0 elsewhere (F90:274-285), with the
drag coefficient `ksrf = surface_stress_coefficient(taux, tauy, u0, v0,
ksrftms) = ksrftms + max(sqrt(taux²+tauy²)/max(sqrt(u0²+v0²), wsmin),
ksrfmin)` (F90:232-239).  The diffusion term is lowered by the ESD rule
`varcoeff_face_laplacian_lev_flux_bc`, whose stencil is exactly the CAM
`linear_1d_operators.F90` finite-volume operator (spr/sub/diag, deriv_diag) —
verified term by term; the residual-stress memory `tauresx = tauresx_enter −
tauimpx` with `tauimpx = ∫ (u−u0)/(g·dt) dz` lowers by the ESD rule
`integral_lev_whole`; `dtk = 0.5(u0²+v0²) − 0.5(u²+v²)` is the do_beljaars
kinetic-energy dissipation (F90:598-646), bit-exact against the dump.

All parameters and states are stored in esd order (lev 1 = surface), reversed
from the dump rows; the double sign flip (coordinate reversal plus the
flux-direction flip of the conservative stencil) makes the esd operator row i
equal to the CAM matrix row 33−i exactly: `L u[i] = (A·u)[33−i]`.  Verified
laws (window-wide, site vdiff): tau_damp(32) to rel 5.2e-15, ptend_u/v(32)
to rel 4.4e-12 (u) / 9.8e-11 (v) window maxima, dtk bit-equal (rel 0), the
taures law to rel ≤ 9.3e-12, ptend_q(32) to rel ≤ 3.8e-15.  The dump window
runs all kvh/kvm/kvq ≡ 0, so no dump row exercises the diffusion operator:
the operator is pinned by a compiled-Fortran reference driver
(`stage1/analysis/cam_vdiff_driver/`, `coords_1d.F90` and
`linear_1d_operators.F90` verbatim from the fork, K = dpidz_sq with kv ≡ 1
m²/s, zero prescribed face fluxes), all 32 rows bit-identical to an
independent Python replication.

## The `physics_update` state law (`cam_physics_update.esm`)

The single state-update step CAM6 applies after **every** parameterization,
`physics_update` of `physics_types.F90:207-495` — the first fully-assembled,
fully coupled piece of the CAM stage-2 chain (every other CAM component feeds
or consumes it).  Per call, given the pre-call state and the call's `ptend`
and flags (`ls/lu/lv/lq`, `top_level/bot_level`) and `dt`:

1. **Window**: `win(k) = 1` for `NLEV+1-bot_level <= k <= NLEV+1-top_level`
   (every active site in this run uses the full column).
2. **u, v**: `u_after = u + lu*win*ptend_u*dt` (F90:287-301).
3. **Constituents** (F90:313-334): `qraw = q + win*ptend_q*dt` computed once,
   then either the qneg3 floor `qclamp = max(qraw, qmin)` over the whole
   column or the number-concentration clamp `min(max(qraw, 1e-12), 1e10)` for
   NUMICE/NUMLIQ/NUMRAI/NUMSNO; `lq = 0` short-circuits to `q` unchanged.
4. **CLDLIQ/CLDICE zeroing** (F90:353-375): at the convect_deep sites, the
   (CLDLIQ, NUMLIQ) and (CLDICE, NUMICE) pairs are zeroed together wherever
   the post-clamp qclamp < 1e-36 (the `state_cnst_min_nz_mask` template).
5. **Temperature** (F90:415-421): `T_after = T + ls*win*ptend_s*dt/cpairv`.
6. **Geopotential** (F90:423-449, geopotential_temp.F90:133-216): when
   `derive_new_geopotential` is true, `zm_after = integral(f_tv, z_sfc ->
   lev)` and `zi_after = integral(f_tv, z_sfc -> lev_nodes)` with measure
   `dz = pdel/pmid` — cumulative integrals lowered by the ESD rules
   `integral_lev_cumulative_from_bottom` and
   `integral_lev_nodes_cumulative_from_bottom`; otherwise the identity.
7. **Static energy** (F90:445-448): `s_after = T_after*cpairv + gravit*zm_after + phis`.
8. **Tend accumulation**: `tend%dudt += ptend_u`, etc. — the per-call
   increment is the `dudt`/`dvdt`/`dtdt` equation of `PhysicsUpdate`; the
   accumulation over the call sequence is the `TendAccumulation` model (one
   masked `faq` sum over the `site` axis of the 15 consecutive tphysbc calls).

Eight tests (162 assertions, rel 1e-12) pin the law at six call sites plus
the tend accumulation, from `cam_phys_tend.csv`, `cam_phys_tend_q.csv`,
`cam_tend_total.csv`: convect_deep at steps 18/40 (the ZM-active steps, incl.
the CLDLIQ/CLDICE pair zeroing, the number clamp and the geopotential),
clubb#1 macmic substep 1, microp#1 macmic substep 1 (ls only), aero_calcsize
(q-only, the num_a1 1e-5 floor), radiation (ls-only, last tphysbc call), vdiff
(lu/lv/ls + all 34 constituents at the single active level), and the
tend_accumulation_bc phase sum vs the cam_tend_total.csv phase=bc row.
**Pinning rules**: every assertion is pinned at a few informative levels —
never every level — and **only where the law changes the value** (the
extractor drops any assertion whose expected value equals the overridden
input it derives from), and every expected value is chained to a later call
site's dump rows (`state_before(next site) == state_after(this site)`), so
every pin can fail.  The committed extractor
(`stage1/analysis/extract_cam_physics_update_pins.py`) re-verifies the full
48-step × 26-site chain for every level and constituent (worst relative error
0 for the column state, 4.3e-16 for the geopotential zm/s).

## The RRTMG radiation chain (`cam_radiation.esm`)

Six models transcribing `radiation_tend` (tphysbc site 11, `radiation.F90`),
pinned by the eight `cam_rad_*.csv` dumps of run 12255018 (23 radiation steps
of the 48-step run — every iradsw=iradlw=2 step, 13 day and 10 night steps):

```
state + cam_in (ts, albedos) + pbuf (cld, cldfsnow, ICLWP, ICIWP, DEI, ...)
  | CamRadState        rrtmg_state_create (rrtmg_state.F90:60-247): the
  |                    RRTMG 33-layer gas state (32 CAM layers + the extra
  |                    top layer); pmid, the shared pint_hi/T_ifc_hi edges
  |                    (edge_shift), h2ovmr = (q/(1-q))*amdw,
  |                    cfc22vmr = ccl4vmr = 0
  | CamRadSolin        solin = sum_b sfac_b*solar_band_irrad_b * eccf *
  |                    coszrs (radsw.F90:395-397; 0 at night), the band sum
  |                    a faq reduce over band (the 14 radconstants.F90:34-40
  |                    irradiances, sum 1368.22 W/m²)
  | CamRadSolverInputs ssa = tau_w/tau (tau>0) else 1; asm = tau_w_g/tau_w,
  |                    fsfc = tau_w_f/tau_w (tau_w>0) else 0
  |                    (radsw.F90:437-475, the guarded_ratio template);
  |                    cldfprime = max(cld, cldfsnow) (radiation.F90:1012-1016)
  | CamRadMcicaSw      tauc_sto = cld_sto*tau(band(gpt)), ssac_sto =
  |                    cld_sto*ssa + (1-cld_sto), asmc_sto = cld_sto*asm,
  |                    fsfc_sto = cld_sto*fsfc (mcica_subcol_gen_sw.f90:439-444)
  | CamRadMcicaLw      tauc_sto_lw = cld_sto*tau_lw(band_lw(gpt_lw))
  |                    (mcica_subcol_gen_lw.f90:408-416)
  | CamRadHeating      fns = fds - fus, fnl = ful - fdl at the interfaces;
  |                    qrs = g*D(fns), qrl = -g*D(fnl) (the layer flux
  |                    divergence on the ze = -pint_hi-reversed esd column);
  |                    the history scalars as index picks; sw_net/lw_net as
  |                    whole-column integrals (the telescoping identities)
  v
qrs, qrl (W/kg)  ->  heating rates for the state update
```

The McICA masking uses the `stable_blend` template imported by reference from
the CMEPS templates (`../../coupler/cmeps/cmeps_templates.esm`); the
band→gpt k-distribution maps come from `rrtmg_sw_init.f90:266-280` /
`rrtmg_lw_init.f90:308`.  The stochastic `cld_sto` is an input (deterministic
RNG, permuteseed 1 SW / 150 LW, single column — out of scope).  19 tests /
198 assertions, all rel 1e-12, `time_span {0,0}`; every model's first test
runs on the step-3 parameter defaults, and the extractor copy-checks every
tuple against the input rows and drops exact input copies (nothing in the
tests block is a pass-through of an overridden input).

Known gaps: the k-distribution gas optics and the two-stream radiance solves
are not dumped (CamRadHeating takes the interface fluxes as inputs); the
o3vmr P_top decay is not pinnable; the cldfsnow > cld branch of cldfprime is
untested (cldfsnow = 0 in the dump); the tau_w = 0 → asm = fsfc = 0 else
branch is unpinned.

## The RRTMG shortwave column solver (`cam_rrtmg_solver.esm`)

The SW solver chain following the cloud-optics conversion, as five models:
the delta-M cloud scaling (`rrtmg_sw_cldprmc.f90:94-113`, applied per g-point
through the CICE `dEdd_scaled_tau/w0/g` laws of
`../../cryosphere/cice/cice_templates.esm` — the same delta-M algebra), the
PIFM two-stream layer solve (`rrtmg_sw_reftra.f90:132-206`: the gamma1..4
coefficients, the zwcrit = 0.9999995 conservative/non-conservative branch,
the four layer arrays pref/ptra/prefd/ptrad, solved twice per layer on the
sky axis with the cld_sto <= repclc = 1e-12 clear-cell guard), the direct
beam (`rrtmg_sw_spcvmc.f90:453-490`: the od_lo = 0.06 quadratic branch and
the exp_tbl lookup), the adding-method flux assembly (`rrtmg_sw_vrtqdr.f90:
60-210`: the prupd/prdnd/ztdn chains and the interface fluxes pfu/pfd with
the zreflect = 1/(1 − prdnd·prupd) factor), and the band flux sums
(`rrtmg_sw_init.f90` zincflx weights).  The `gpt` axis is the pinned 4-member
subset {1, 9, 13, 47} of the 112 SW g-points; every dump array is sliced to
those columns by the extractor.

Factoring: the adding recurrences apply per-step templates whose bodies nest
the `pifm_zreflect` application — the Fortran's per-iteration `zreflect`
cannot be hoisted into a named intermediate (the CLI rejects the coupled
recurrence, `observed_cycle`, esm-spec §4.9.6 — probed), so the factor is
applied inline inside the step templates; `esm-pin-lint.py` inline-repeat
findings for the adding model are zero.  39 assertions across the four
solver models plus 12 for the band sums, every expected a dump-derived pin
(rel 1e-12).  Coverage gaps: the gas k-distribution optics is not dumped (the
chain starts at the cloud optics); the conservative layer-solve branch and
the clear-cell guard are not pinned; the full 112-g-point axis returns in
stage 3.

## The RRTMG longwave rtrnmc solver (`cam_rrtmg_lw.esm`)

The LW column solver `rtrnmc` (`rrtmg_lw_rtrnmc.f90` with the Pade tables of
`rrtmg_lw_init.f90:96-112`, `rrlw_tbl.f90` and the spectral data), as two
models: `CamRrtmgLwSweep` (the variable diffusivity angle secdiff = 1.66 for
bands 1, 4, 10-16 and the clamped a0 + a1·exp(a2·pwvcm) form for bands 2-3
and 5-9; the McICA cloud scaling odcld/abscld/efclfrac; the layer Planck
sources; the quadratic/Pade-table gas laws with the 10000-knot tables; the
specular surface rad0/reflect; the per-g-point flux contributions
wtdiff·delwave·fluxfac) and `CamRrtmgLwFluxes` (the band-summed totals, the
layer heating rates htr = heatfac·(fnet(k+1) − fnet(k))/(pz(k+1) − pz(k))
with heatfac = g·cday·1e-5/(cpair·1e-3) = 8.433391304347827, the CAM heating
rates qrl/qrlc, the flnsc/flntc nets).  The `gpt` axis carries all 140 LW
g-points.

The Fortran's down and up loops share the layer laws but not the source: the
down loop accumulates with `bbd` (the layer-bottom Planck difference) and the
up loop reassigns `gassrc = bbugas*atrans` (the layer-top difference) before
its update (f90:310-313 vs 416-418).  The esm keeps one template,
`lw_cloudy_update`, for the unified recurrence `rad' = rad − rad·A + gassrc +
cldfmc·(bbtot·atot − gassrc)` and binds the *direction-matched* source on
each sweep.  An early transcription bound the down source on the up sweep too
— the unified form then quietly reduced to `rad + (bbd − rad)·atrans` and the
up fluxes came out ~1e-2 W/m² high with no down-sweep error (visible only in
the per-g-point assertions); the fix adds the `gassrc_up` law.

The three Pade columns tau_tbl/exp_tbl/tfn_tbl are **computed from the
Fortran formula**, not dump-derived, with tfn = float(itr)/float(ntbl)
carrying the build's single-precision rounding (reproduced exactly with numpy
float32 by the extractor); the solver's integer index itr =
int(10000·odepth/(bpade + odepth) + 0.5) is reproduced by the `lw_tbl_lookup`
nearest-knot law through the `esm:std/interp.esm` searchsorted insertion
point with the tie-breaking distance comparison (the itr = 0 entry is
unreachable and the itr = 10000 endpoint is the explicit tau = 1e10/exp =
0/tfn = 1 assignment).  1188 assertions across the two models (sweep
222/234/234/234, fluxes 66×4), every expected a dump-derived pin spliced by
`stage1/analysis/splice_cam_rrtmg_lw.py` (numbers only, never hand-typed).
Tolerance contract (measured, deterministic on the CLI): uflux/uclfl rel
1e-11 (measured max 2.1e-12), dflux/dclfl rel 1e-12 (9.1e-13), the band
totals rel 1e-12 (1.4e-15), qrl/qrlc rel 1e-10 (2.8e-11), flnsc/flntc rel
1e-12 (4.3e-15) — the residuals are last-ulp association differences between
the esm expression tree and gfortran's own association, telescoping away in
the band sums and re-amplified in the heating rates by the fnet cancellation.

**Reuse assessment**: the corpus's `atmospheric_radiation/rrtm_lw` is WRF
RRTM (module_ra_rrtm.F, WRF 4.8), not CAM RRTMG — different band structure
and constants (5000-knot tables, a real32 build contract and the WRF
column/k-dist setup against the CAM RRTMG's 10000-knot tables, real64 build
and McICA cloud scaling).  The two share the RRTM lineage (bpade = 1/0.278,
the Pade tau-transition, the RTRN sweep), so the WRF lane's
`rrtm_parameters.esm`/`rtrn_sweep.esm` serve as a cross-check of the shared
physics, but its components cannot be imported into the CAM lane; `rrtm_lw`
is deliberately **not reused**.  The CAM SW lane (`cam_rrtmg_solver.esm`) is
not reused either: the `pifm_*`/`vrtqdr_*` templates are bound to the SW
layer laws and parameter shapes, so the LW lane's templates stay independent
until stage 3 couples the lanes by data.

## The ZM deep-convection subassembly (`cam_zm.esm` + the four components)

The Zhang–McFarlane chain (`convect_deep.ZM` at tphysbc site 3) as four
stage-2 components mounted **by reference** in `cam_zm.esm` and wired with
the driver couplings only — no component law is restated in the assembly.
The dump window is the 15 ZM-active steps 18–23 and 40–48 (rows only where
cape > capelmt), all columns g = 1.  Working pressures are **hPa** (p =
0.01·pmid, dp = 0.01·pdel); the dumped mu/md/mc are mb/s and eu/du/ed are
1/s, with the continuity identity mu(k) − mu(k+1) = (eu(k) − du(k))·dp(k).

### Parcel and closure (`cam_zm_parcel.esm`, `cam_zm_closure.esm`, `cam_zm_templates.esm`)

`Parcel` transcribes buoyan_dilute (`zm_convr.F90:890-1490`): qst (the
qsat_hPa wrapper reusing `goff_gratch_water`/`svp_to_qsat` of
`cam_templates.esm` by reference), the moist static energies hmn/hsat
(F90:1829-1830), the virtual temperatures tv/tpv (F90:1005-1006, 1088, 1415,
1476), the Raymond–Blyth entropy ent (F90:1489-1513), the buoyancy
`buoy = tpv − tv + tiedke_add` for msg+1 ≤ k ≤ maxi else 0, and the CAPE
integral `cape = max(0, integral over d(ln p) of rd·buoy over lel < k ≤
maxi)` lowered by the ESD rule `integral_lev_whole` with the true d(ln p)
measure log(pf_hi/pf_lo).  **Carried as parameters** (not expressible in the
CLI, probed): `maxi` (the argmax of hmn — argmax is not evaluable), the
parcel-ascent solve outputs `tp`/`qstp`/`qtot` (the ientropy Brent root-find,
F90:1517-1632), and `lel` (with num_cin = 1 the candidate selection collapses
to lel = lelten(1), verified against the dumped capeten/lelten columns); the
pl ≥ 600 gate is omitted (pl is dumped ≥ 600 mb on all active rows).

`Closure` transcribes closure + the driver's dsubcld (`zm_convr.F90:2318-2506`,
F90:597-603): dsubcld in its telescoped closed form `pf_hi(pver) − pf_lo(mx)`
(the interface-pressure difference over the subcloud layer, needing no
integral rule), the launch-level block (eb, dtbdt/dqbdt, debdt, dtldt), the
cumulus heating/drying with beta = 0 (F90:2433), the virtual potential
temperatures thetavp/thetavm (F90:2457-2480), dqsdtp/dtpdt, dboydt above and
below the LCL, and `dadt` = integral of dboydt over the height measure
zf_lo − zf_hi (F90:2490-2499), then `mb = max((capelmt − cape)/(tau·dadt),
0)`, zero when dadt = 0.  The closure consumes the **normalized** fluxes
(mu/md/mc dimensionless fractions of mb, du per hPa) — the tests feed
dump/mb.  The lel/lcl/jt/mx region guards live inside the `zm_*` template
bodies (an ifelse guard short-circuits the untaken branch, so the
(1000/p)^(rd/cp) law is never evaluated at p = 0).

Tests: Parcel 250 assertions (15 steps × 16 pins of hmn/hsat/qst/tpv/buoy/
cape + 10 ent/tv replica pins), Closure 30 (dsubcld worst rel 8.3e-15, mb
worst rel 2.5e-16).  The step-18 test runs on the model defaults (every
step-18 profile equals a default, so the default run *is* the step-18 state).
Transcription note: binary `-` in the esm operator set is subtraction, so
negations are written `0 − x`, never `x − 0` (the latter evaluates to +x;
this bit the dtldt and entropy rgas terms during development and is
regression-covered by the tests).

### q1q2 tendencies and rain evaporation (`cam_zm_q1q2.esm`, `cam_zm_evap.esm`)

`ZMq1q2` transcribes q1q2_pjr (`zm_convr.F90:2584-2622`): over the convection
layer jt ≤ k < pver the plume-flux divergences

```
dqdt = emc + ( mu(k+1)(qu−qhat)(k+1) − mu(k)(qu−qhat)(k)
             + md(k+1)(qd−qhat)(k+1) − md(k)(qd−qhat)(k) ) / dp      (F90:2596-2601)
dsdt = −rl/cp·emc + ( mu(k+1)(su−shat)(k+1) − mu(k)(su−shat)(k)
                   + md(k+1)(sd−shat)(k+1) − md(k)(sd−shat)(k) ) / dp (F90:2589-2594)
dl   = du(k)·qcde(k+1)                                                 (F90:2603-2604)
```

with the subcloud form `(1/dsubcld)(−mu(x−xhat) − md(y−xhat))` at k = maxg
and the copy-down for k > maxg, factored into three `cam_templates.esm`
templates (`zm_flux`, `zm_flux_divergence`, `zm_subcloud_tendency`) with the
piecewise `ifelse(k >= maxg, subcloud, ifelse(k >= jt, flux form, 0))` mask.
The ESD `face_flux_D_lev_supplied_faces` rule was probed and not used: it
lowers to the geometric-height divergence while the ZM divergence is per
pressure thickness dp on a grid-less CAM level set.

`ZMevap` transcribes zm_conv_evap_run (`zm_conv_evap.F90:118-236`, called
from `zm_conv_intr.F90:671-679`): the evaporation is the min of the Sundqvist
rate `evpprec_raw = ke·(1−cldfrc)·max(1−q/qs, 0)·sqrt(flxprec_lo)` and three
upper bounds (the deltat saturation limit, the falling-flux limit, the
remaining-precipitation limit), then the snow chain with old_snow = .true.
(the melt split at t1 > tmelt, the work1/work2 fractions), `ntprprd = rprd −
evpprec`, `ntsnprd = rprd·work2 − evpsnow − snowmlt`, and the flux steps with
the roundoff guard `flxprec_hi = max(flxprec_lo + ntprprd·pdel/gravit, 0)` via
the shared `zm_evap_flux_step` template.  **The precipitation flux is the
top-down vertical integral of the net production** `flxprec(k+1) = flxprec(k)
+ ntprprd(k)·pdel(k)/gravit`, and the coupling is two-way (the evaporation at
a level depends on the flux entering it and vice versa) — the CLI rejects the
coupled recurrence with the exact error `Observed dependency cycle: evpprec
-> flxprec_hi -> ntprprd -> evpprec` (esm-spec §4.9.6, reproduced with
`scratch/probe_cycle.esm`), and the ESD `integral_lev_cumulative_to_top`
route is rejected the same way, so `cam_zm_evap.esm` pins the per-level step:
the accumulated boundary flux `flxprec_lo`/`flxsnow_lo` enters as a dumped
input at every level (the recurrence boundary), and the Fortran's running
accumulator `evpvint(k) = Σ_{j<k} (rprd(j) − ntprprd(j))·pdel(j)/gravit` is a
derived input (each increment equals evpprec(j)·pdel(j)/gravit exactly
because ntprprd = rprd − evpprec; the vertical coupling is preserved as data
in the tests and can be re-imposed as an ESD integral in stage 3).  qs comes
from the estbl table lookup + `svp_to_qsat` (the estbl_es0 template of
`cam_templates.esm`; the 251-knot table data is the per-document copy, see
the qsat section).

Tests: cam_zm_q1q2 30 assertions, cam_zm_evap 68 (steps 18/22/40/48), all
rel 1e-12 (abs 1e-24 for the identically-zero guard pins).  The step-18/22
columns evaporate their precipitation completely (prec_evap = 0; the roundoff
guard fires at lev 31 on steps 18, 21-23); steps 40/48 are the active
columns.  Every column melts its snow at lev 22, so `snow_evap` is unpinned
everywhere (the melt mechanism is pinned by `flxsnow_hi(22) = 0` instead).
The `ke_lnd`/`landfrac` dead-argument finding is recorded as bugs.md entry 33
(kemask = ke unconditionally, identical in the vanilla CESM checkout).

### The assembly and its couplings (`cam_zm.esm`, `cam_zm_coupling.esm`)

`cam_zm.esm` mounts Parcel/Closure/Q1Q2/Evap by reference with the inline
`Control` model holding the driver couplings: (1) **the precipitation
budget** (zm_convr.F90:770-779) `prec = max(0, −∫ pdel (dqdt + dlf)) ·
rgrav / density_fresh_water`, written as an integral over the layer pressure
measure dz = pdel (the ESD `integral_lev_whole` rule), pinned against the
dumped prec_convr; (2) **the physics_update state advance**
(zm_conv_intr.F90:640) `t1 = t0 + delt dsdt`, `q1 = q + delt dqdt`; (3) the
mb-scaling expression edges `Q1Q2.mu = Closure.mb × Closure.mu` (etc., the
×mb scaling of zm_convr.F90:725-735).  The 37 wiring edges enter by reference
as a `coupling_import` of the `cam_zm_coupling.esm` coupling library — the
same library the EqESM `cam_physics_column.esm` driver imports, so every ZM
edge is authored once.  What stays boundary (documented gaps the stage-3
driver will close): the parcel-ascent solve outputs, the level indices, the
cldprp outputs (gathered profiles, plume states, normalized fluxes), and the
evap recurrence boundary.  Three end-to-end tests (s19_g1/s40_g1/s48_g1, 50
assertions, rel 1e-12) run the whole coupled chain with **boundary inputs
only** overridden — 42 override entries per step, none of them a component
output — pinning Parcel.cape, Closure.mb, Q1Q2.dqdt/dsdt/dlf, Control.prec
(== dumped prec_convr), Control.t1/q1, Evap.tend_s/tend_q and Evap.prec_evap
(steps 40/48).

## Coverage gaps (summary)

Per-lane gaps are documented in the sections above and in the `.esm`
descriptions.  The headline items, all of which are documented rather than
bridged (no data was invented anywhere):

- **Saturated branches** of qsat (p − es ≤ 0), the estblf clamps, and the
  gam/dqsdT intermediates: the dump window never saturates and spans only
  T = 208.7..302.5 K.
- **energy-fixer ptop** is not dumped (supplied as the dump-derived
  ps − Σpdel); the **rayleigh enabled branch** pins are compiled-Fortran
  references (raytau0 = 0 in the run).
- **Surface exchange**: zbot/topo/precipitation-split/co2diag provenance
  gaps; the cpslec branches 1 and 3 are implemented but unpinned (the 887 m
  SCAM column only takes branch 2); flx_net and net_flx_rad are not dumped;
  the dump's co2diag ≈ 1.127 ppmv could not be traced to any prescribed
  input (open question, not a CESM defect); the dump header labels co2diag
  mol/mol while the values are ppmv-scale — an instrumentation labeling slip
  in the fork, not data corruption.
- **Vertical diffusion**: the s-equation top boundary (BoundaryFixedLayer)
  differs from the rule's zero-flux kdudz_top whenever K(1) > 0 (kvh(1) = 0
  in the window, so they coincide here); the countergradient terms
  (cgh/cgs, qmincg, dropmixnuc, ubc_mmr) are zero/inert in the window and
  not carried; the nonzero-K stencil is pinned by the compiled reference,
  not dumps.
- **Radiation**: the k-distribution gas optics and the two-stream solves are
  not dumped; the o3vmr P_top decay is not pinnable; cldfsnow > cld and the
  asm/fsfc else branches are unpinned; the night SW side is the all-zero
  boundary and is never pinned.
- **RRTMG SW**: the chain starts at the cloud optics (no gas optics dump);
  the gpt axis is the 4 pinned g-points; the conservative layer-solve branch
  and the clear-cell guard are not pinned.
- **RRTMG LW**: none beyond the documented association residuals (the
  tolerance table above).
- **physics_update**: the ac-phase dtdt SE scaling (`cp_or_cv_dycore` not
  dumped — the ac-phase tend accumulation test was dropped rather than fed
  fabricated inputs); zi is not dumped (identity branch covered
  structurally); the sslt_rebin_adv mutation creates a documented chain
  discontinuity between convect_shallow and ssatcontrail; the WACCM-X
  branches and the lagrangian piln geopotential branch are not transcribed.
- **ZM**: the parcel-ascent solve (ientropy) and argmax(maxi) are not CLI-
  expressible (carried as parameters); the cldprp and convtran1 blocks are
  separate lanes; the flxprec top-down integral is preserved as data
  (re-imposable as an ESD integral in stage 3); the deltat saturation limit
  and the k > maxg copy-down are not exercised by the window; the dead
  `new_snow` branch is not transcribed.

## Testing

All tests are instantaneous (`time_span {0,0}`), rel 1e-12 (abs 1e-24 on the
identically-zero guard pins of the evap lane), citing the dump file, step,
cell and level.  Suite results on the ported directory (Rust CLI 0.14.0,
`$M/esm`, with `ESD_ROOT` = EarthSciDiscretizations main):

```
esm test components/atmosphere/cam     -> 2198P / 0F / 0E
esm validate <file>                    -> PASS on all 16 standalone files
esm units <file>                       -> PASS on all 17 files, no
                                          units_dimensionless_literal_mismatch
```

`cam_zm_coupling.esm` (a coupling library, esm-spec §10.9) cannot be
validated standalone — its `coupling_roles` carry no bound models and the
structural validator has no role suspension, so every scoped reference of the
37 edges reports "cannot be resolved" (a known CLI gap, shared with the
CMEPS coupling library) — it is validated and tested **through its importer**
`cam_zm.esm`, which flattens the `coupling_import` and exercises all 37
edges.  The Python inline gate (`tools/run_esm_inline_tests.py`, earthsci_ast
0.13.0) runs the same files with runner-specific limitations: 149P / 0F /
2052E, all errors being Python-runner gaps (the native compiler refusing the
LW `atrans` construction rule, unresolved scoped symbols such as
`PhysicsUpdate.u`/`Parcel.p`/`CamRrtmgSwCloudScale.fsfc_sto`, and numpy
out-of-bounds index errors on the radiation level axes) that do not occur on
the Rust runner; the identical error set reproduces on the EqESM stage-2
originals, so nothing in the port introduces them.
