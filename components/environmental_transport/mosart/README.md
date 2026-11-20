# MOSART stage 2 — `.esm` skeleton

Stage-2 implementation of the CESM MOSART river-routing component (mosart1.1.13,
cesm3.0-alphabranch checkout `e59f2512`) as esm 2.0.0 files: component structure,
imports/exports, solver block, the pointwise flow laws of `mosart_physics.F90`
transcribed exactly, subcomponent routing steps, and top-level assembly. Most
`tests` blocks hold numeric tuples dumped from instrumented CESM runs; a few are
hand-derived or come from a standalone Fortran driver, and each test says which —
see [Testing](#testing).

All model logic lives in `.esm` files; this README is the human-readable map.

**Provenance paths.** The `stage1/...` paths cited throughout (here and in the
`.esm` descriptions) refer to the EqESM project's working checkout, which is not
public: `stage1/cesm/...` is the CESM source tree (instrumented with a
dump-only module that observes the physics without changing it), and
`stage1/dumps/...` holds the CSV files that instrumentation wrote. Line numbers
like `F90:497` refer to that CESM tree (mosart1.1.13 in cesm3.0-alphabranch). The
dump files the tests cite, and their columns, are:

| Dump file (`stage1/dumps/mosart/` = dry lane window, `stage1/dumps/mosart_wet/` = wet window) | Columns |
|---|---|
| `creht_nosqrt.csv` (hillslope law, one row per Euler call) | `step,ns,m,nt,nr,gindex,sqrthslp,nh,Gxr,yh,eht_raw,ehout,clamped` |
| `crvrman_trib.csv` (tributary Manning law, one row per numDT_t substep) | `step,ns,m,nt,nr,gindex,tslpsqrt,n_t,rt,vt,mt,etout_raw,etout,dwt,clamped` |
| `crvrman_chan.csv` (main-channel Manning law, one row per numDT_r substep) | `step,ns,m,nt,nr,gindex,rslpsqrt,n_r,rr,vr,mr,erin,erlateral,erout_raw,erout,dwr,qgwl_area,clamped` |
| `gr_subnet.csv` (subnetwork geometry after each wt update) | `step,ns,m,nt,nr,gindex,wt,tlen,twidth,mt,yt,pt,rt` |
| `gr_chan.csv` (channel geometry after each wr update) | `step,ns,m,nt,nr,gindex,wr,rlen,rwidth,rwidth0,rdepth,mr,yr,pr,rr` |
| `mosart_euler.csv` (Euler substep entry/exit; qsur/qsub/qgwl in m/s) | `step,ns,nt,nr,gindex,phase,delt,wt,wr,wh,qsur,qsub,qgwl,ehout,etin,etout,erout,erlat_avg,flow` |
| `mosart_run_imports.csv` (coupling-step imports and initial state, m³/s) | `step,ymd,tod,nt,nr,gindex,mask,qsur,qsub,qgwl,qirrig,qglc_liq,qglc_ice,volr,wt,wr,wh` |
| `mosart_run_imports_wide.csv` (dry window only; every cell with a nonzero import) | `step,ymd,tod,nt,nr,gindex,mask,area,areacor,qsur,qsub,qgwl,qirrig,qglc_liq,qglc_ice` (`area` = `ctl%area`, `areacor` = `med2mod_areacor`) |
| `mosart_run_exports.csv` (coupling-step exports and final state) | `step,ymd,tod,nt,nr,gindex,mask,runofftot,runoff,runofflnd,runoffocn,flood,direct,direct_glc,qirrig_actual,volr,dvolrdt,flow,erout_prev,eroutup_avg,erlat_avg,volrmch,wt,wr,wh` (`volrmch` = `wr/area` in m) |

Static network inputs (slopes, roughness, `Gxr`, `area`, the `dnID` topology used
to recompute `areaTotal2`) come from the CESM input file
`MOSART_routing_Global_0.5x0.5_c170601.nc` (the frivinp network file).

Sources: `stage1/cesm/components/mosart/src/riverroute/mosart_physics.F90`,
`stage1/cesm/components/mosart/src/riverroute/mosart_driver.F90`,
`stage1/cesm/components/mosart/src/riverroute/mosart_tstatusflux_type.F90`,
`stage1/cesm/components/mosart/src/riverroute/mosart_tspatialunit_type.F90`,
`stage1/cesm/components/mosart/src/cpl/nuopc/rof_import_export.F90`,
and the boundary/subassembly plan in `stage1/boundaries.md` (§1.5, §2.6).

## File map

| File | Contents | Fortran source |
|---|---|---|
| `mosart_templates.esm` | Expression-template library: `manning_velocity`, `overland_discharge`, `wetted_area`, `rectangular_depth`, `rectangular_perimeter`, `hydraulic_radius`, `channel_depth`, `channel_perimeter` | `mosart_physics.F90`: CRVRMAN_nosqrt 406-422, CREHT_nosqrt 426-437, GRMR 441-449, GRHT 453-465, GRPT 469-481, GRRR 485-497, GRHR 501-532, GRPR 536-572 |
| `mosart_hillslope.esm` | Model `Hillslope` — Euler step 1: hillslopeRouting + updateState_hillslope, `etin` lateral inflow | `mosart_physics.F90`: Euler 74-80, hillslopeRouting 225-239, updateState_hillslope 352-360 |
| `mosart_subnetwork.esm` | Model `Subnetwork` — Euler step 2: subnetworkRouting + updateState_subnetwork, `erlateral` | `mosart_physics.F90`: Euler 114-132, subnetworkRouting 243-269, updateState_subnetwork 364-381 |
| `mosart_channel.esm` | Model `Channel` — Euler step 4: Routing_KW + updateState_mainchannel, `flow` | `mosart_physics.F90`: Euler 175-209, Routing_KW 273-348, updateState_mainchannel 385-402 |
| `mosart_coupling.esm` | Model `RofCap` — med↔rof cap unit conversions only | `rof_import_export.F90`: state_getimport 589-595, state_setexport 636-643, fields 88-117, areacor 209-210, tdepth_max 401 |
| `mosart_routing_coupling.esm` | Coupling library (esm-spec §10.9-10.10): the single source of the 43 `variable_map` `param_to_var` edges wiring the assembly (Euler-cascade data flow, cap stream conversions, the irrigation withdrawal into the channel, and 13 cell-geometry edges from `Control`), imported by `coupling_import` in `mosart_routing.esm` | `mosart_physics.F90` Euler cascade 74-209; `mosart_driver.F90`: mosart_run 375-873; `rof_import_export.F90`: 389-402, 636-643 |
| `mosart_routing.esm` | Top-level assembly: mounts RofCap/Hillslope/Subnetwork/Channel by reference + inline `Control` (mosart_run steps 2-8, subtimestep logic, aggregation, single source of the cell geometry), the 43 coupling edges via the `mosart_routing_coupling.esm` library (`coupling_import`, bind: RofCap/Control/Hillslope/Subnetwork/Channel), enums, solver block | `mosart_driver.F90`: mosart_run 375-873; `mosart_tspatialunit_type.F90`: set_subtimesteps 624-684 |

The routing steps are written as storage ODEs (`D(wh)/dt`, `D(wt)/dt`, `D(wr)/dt`)
with the pointwise laws as observed variables via `apply_expression_template`;
at stage 3 the ODEs are integrated with `github.com/earthsciml/earthsciintegrator`.
Dry-cell clamps and the Fortran if/else branches are transcribed as `ifelse`
expressions. These ODEs are **not** the continuous limit of the Fortran scheme
and cannot match CESM's trajectory structurally — see
[Continuous ODEs vs the Fortran 3600-s Euler stepping](#continuous-odes-vs-the-fortran-3600-s-euler-stepping).

## Units

Per `mosart_tstatusflux_type.F90` and `mosart_tspatialunit_type.F90` geometry:

| Quantity | Symbol | Units |
|---|---|---|
| Hillslope storage / depth | `wh`, `yh` | m |
| Subnetwork storage | `wt` | m³ |
| Main-channel storage | `wr` | m³ |
| Hillslope fluxes | `qsur`, `qsub`, `ehout`, `dwh` | m/s |
| Subnetwork / channel fluxes | `etin`, `etout`, `erlateral`, `erin`, `erout`, `dwr`, `eroutUp`, `flow`, `qirrig_actual` (= `Channel.qirrig`), `flood` | m³/s |
| Velocities | `vt`, `vr` | m/s |
| Cross-section areas | `mt`, `mr` | m² |
| Depths / perimeters / radii | `yt`, `pt`, `rt`, `yr`, `pr`, `rr` | m |
| Slopes (sqrt) | `hslpsqrt`, `tslpsqrt`, `rslpsqrt` | 1 |
| CFL indicators / substep counts | `phi_r`, `phi_t`, `numDT_r`, `numDT_t` (integers) | 1 |
| Drainage density | `Gxr` | 1/m |
| Lengths / widths | `tlen`, `hlen`, `twidth`, `rlen`, `rwidth`, `rwidth0`, `rdepth` | m |
| Areas | `area`, `areaTotal2` | m² |
| Manning roughness | `nh`, `nt`, `nr` | s/m^(1/3) |
| Times | `delt`, `localdelt`, `coupling_period`, `delt_coupling`, `delt_mosart` | s |
| Cap fields (CMEPS) | `Flrl_*`, `Fgrg_*`, `Forr_*`, `Flrr_flood` | mm/s |
| Cap depth fields | `Flrr_volr`, `Flrr_volrmch`, `Sr_tdepth`, `Sr_tdepth_max` | m |

**Unit notes**

- Manning's n is declared with its SI dimension `s/m^(1/3)` (the frivinp network
  file stores bare numbers). This keeps the equations dimensionally consistent:
  `(rr²)^(1/3)·sqrt(slope)/n` has units `m^(2/3)/(s/m^(1/3)) = m/s`. The esm
  unit checker treats a mismatch as a hard error, so this declaration is required.
- Cap fields are imported in `mm/s` (= CMEPS kg/m²/s for water) and converted
  with `mm_to_m` [m/mm] = 0.001 exactly as `state_getimport`
  (`q [m³/s] = field [mm/s] · med2mod_areacor · area · 0.001`).
- `Flrr_volr = volr/area` and `Flrr_volrmch = wr/area` are depths [m] with **no**
  mm scaling, per `state_setexport` (F90:396-397); like every export they are
  multiplied by `mod2med_areacor = 1/med2mod_areacor` (F90:209-210, 420-423).
- `TINYVALUE = 1.0e-14` is inlined as a literal in the templates (as a unit-tagged
  `const` where it is compared with a dimensional quantity). `SLOPE1` is a
  dimensionless template parameter of `channel_depth` / `channel_perimeter`,
  bound to the constant `0.1` (the Fortran `SLOPE1def`, F90:41) at the `Channel`
  call sites.

## §2.6 mapping, as implemented

| Subassembly (boundaries.md §2.6) | Proposed | Implemented |
|---|---|---|
| Cap boundary (kg/m²s↔m³/s) | `mosart_coupling.esm` | ✓ `mosart_coupling.esm` (RofCap) — pure unit conversions |
| Direct transfer (mosart_run steps 2-4) | `mosart_coupling.esm` | ⚠ moved into inline `Control` in `mosart_routing.esm`: the qgwl threshold option and the flood rule need `Channel.wr`, so the orchestration lives with the systems (annotated deviation from the §2.6 table) |
| Irrigation/flood (steps 2-3) | `mosart_routing.esm` | ✓ `Control` (rate rules) |
| Routing hillslope+subnetwork+channel | `mosart_routing.esm` | ✓ mounted subassemblies, coupled in Euler order |
| Flow laws / geometry (D, first test targets) | `mosart_routing.esm` templates | ✓ factored into `mosart_templates.esm`, imported by reference |
| Network topology (Init, set_routehandles, set_subtimesteps) | data source + discretization | ◐ set_subtimesteps (CFL phi/numDT/localdelt) is in `Control`; set_routehandles / frivinp network data source deferred (stage 2.5) |
| Lakes/reservoirs/groundwater | TBD | — (not present in this MOSART; §2.5) |
| State/budget | harness | — (stage 3, with `mosart_budget_type.F90` as a conservation test) |

## Pointwise laws — Fortran vs esm transcription notes

All templates are match-less, invoked by name, and transcribed exactly. Fortran
formula → esm formula:

| Template | Fortran (mosart_physics.F90) | esm |
|---|---|---|
| `manning_velocity` | CRVRMAN_nosqrt: `v = ((rr²)^(1/3))·sqrtslp/n`, zeroed when `rr <= 0` | `ifelse(rr <= 0, 0, ((rr²)^(1/3))·sqrtslp/n)` |
| `overland_discharge` | CREHT_nosqrt: `eht = Gxr·yh·CRVRMAN_nosqrt(sqrthslp, nh, yh)` | same, calling `manning_velocity` by reference (the one shared-law factoring) |
| `wetted_area` | GRMR: `m = w/len` | `w/len` |
| `rectangular_depth` | GRHT: `h = m/twid`, zeroed when `m <= TINYVALUE` | `ifelse(m <= 1e-14, 0, m/twid)` |
| `rectangular_perimeter` | GRPT: `p = twid + 2·h`, zeroed when `h <= TINYVALUE` | `ifelse(h <= 1e-14, 0, twid + 2·h)` |
| `hydraulic_radius` | GRRR: `r = m/p`, zeroed when `p <= TINYVALUE` | `ifelse(p <= 1e-14, 0, area/p)` (template parameter `area`) |
| `channel_depth` | GRHR three-part cross section (bankfull rectangle → trapezoid of slope SLOPE1=0.1 → flood plain): `h=0` if `m<=TINYVALUE`; `m/rwidth` if `m - rdepth·rwidth <= TINYVALUE`; trapezoid `rdepth + (-rwidth + sqrt(rwidth² + 4·deltam/SLOPE1))·SLOPE1/2`, `deltam = m - rdepth·rwidth`; flood plain `rdepth + SLOPE1·((rwidth0-rwidth)/2) + deltam/rwidth0`, `deltam = m - rdepth·rwidth - (rwidth+rwidth0)·SLOPE1·((rwidth0-rwidth)/2)/2` | nested `ifelse` with `SLOPE1` a template parameter (bound to 0.1 by `Channel`); trapezoid threshold test `m > rdepth·rwidth + (rwidth+rwidth0)·0.1·((rwidth0-rwidth)/2)/2 + 1e-14` as in F90:517-518 |
| `channel_perimeter` | GRPR: `p=0` if `h<TINYVALUE`; bankfull `rwidth + 2·h` if `h <= rdepth+TINYVALUE`; flood plain `rwidth + 2·(rdepth + ((rwidth0-rwidth)/2)·SLOPE1·sinatan + deltah)`, `deltah = h - rdepth - ((rwidth0-rwidth)/2)·SLOPE1`; trapezoid `rwidth + 2·(rdepth + (h-rdepth)·sinatan)`; `sinatan = sinatanSLOPE1defr = 1/sin(atan(SLOPE1def))` (F90:554) | same structure; `sinatan` spelled as the identical expression `1/sin(atan(0.1))` |

Substep / routing transcriptions:

- **Hillslope** (Euler step 1): `ehout_manning = -CREHT_nosqrt(...)`;
  dry-cell clamp fires when `ehout_manning < 0` **and**
  `wh + (qsur + ehout_manning)·delt < TINYVALUE`, replacing `ehout` by
  `-(qsur + wh/delt)`; `dwh = qsur + ehout`; `yh = wh`;
  `etin = (-ehout + qsub)·area·frac`.
- **Subnetwork** (Euler step 2): no tributaries (`tlen <= hlen`) → `etout = -etin`
  (pass-through); otherwise `vt_manning = manning_velocity(tslpsqrt, nt, rt)`,
  `etout_manning = -vt_manning·mt`, dry-cell clamp `etout = -(etin + wt/localdelt)`
  when `wt + (etin + etout_manning)·localdelt < TINYVALUE`; `vt = -etout/mt` when
  the clamp fired and `mt > 0` (F90:257-259); `dwt = etin + etout`;
  `erlateral = -etout`. Geometry (`mt, yt, pt, rt`) from GRMR/GRHT/GRPT/GRRR when
  `tlen > 0` and `wt > 0`, else all zero (updateState_subnetwork).
- **Channel** (Euler step 4, RoutingMethod=1 only, F90:280-284): `erin = -eroutUp`;
  `rlen <= 0` → `vr = 0`, `erout = -(erin + erlateral)`;
  `areaTotal2/(rwidth·rlen) > 1e6` → `erout = -(erin + erlateral)` (F90:310-312);
  else `vr_manning = manning_velocity(rslpsqrt, nr, rr)`, `erout_manning = -vr_manning·mr`,
  dry-cell clamp fires when `-erout_manning > TINYVALUE` **and**
  `wr + (erlateral + erin + erout_manning)·localdelt < TINYVALUE`, then
  `erout = -(erlateral + erin + wr/localdelt)` and `vr = -erout/mr` when `mr > 0`;
  `dwr = erlateral + erin + erout + qgwl·area·frac + qirrig`, where `qirrig` is
  `Control.qirrig_actual` (≤ 0) wired in by the coupling library — the
  Fortran's once-per-period `wr -= irrig_volume` (mosart_driver.F90:497) as a
  rate; `flow = -erout`. Geometry
  (`mr, yr, pr, rr`) from GRMR/GRHR/GRPR/GRRR when `rlen > 0` and `wr > 0`, else zero.
- **Control** (mosart_run + set_subtimesteps): `Control` is the single source of
  the cell geometry (`area`, `frac`, `rlen`, `rwidth`, `rdepth`, `areaTotal2`,
  `rslpsqrt`, `tlen`, `twidth`, `tslpsqrt`); the coupling library wires each to
  the routing systems that use it, so the CFL rule and the routing laws can
  never see different cells. `nsub = ceil(coupling_period/delt_mosart)`
  (F90:786-789), `delt = delt_coupling/nsub`; CFL indicators (set_subtimesteps,
  mosart_tspatialunit_type.F90:645-663) `phi_r = areaTotal2·rslpsqrt/(rlen·rwidth)`
  only when `mask > 0` and `rlen > 0`, `phi_t = area·tslpsqrt/(tlen·twidth)` only
  when `tlen > 0` (else 0); `numDT_* = max(floor(ifelse(phi >= 10, DLevelR·log10(phi) + 1, DLevelR + 1)), 1)`
  inside the same guards and 1 outside them — `numDT_r`/`numDT_t` are Fortran
  `integer` arrays (F90:64-65), so the real right-hand side is truncated on
  assignment (`floor`, the value being ≥ 1); `localdelt_t = delt/DLevelH2R/numDT_t`,
  `localdelt_r = delt/DLevelH2R/numDT_r`.
  Irrigation: `irrig_volume = -qirrig_m3s·coupling_period`,
  `qirrig_actual = -min(irrig_volume, wr)/coupling_period` → `Channel.qirrig`
  (removed from `wr`), overage returned to subsurface:
  `qsub_i = qsub_m3s + ifelse(irrig_volume > wr, (wr - irrig_volume)/coupling_period, 0)`.
  Flood (mask==1 only): `volr = wt + wr + wh·area`, `flood = ifelse(volr > fthresh, (volr - fthresh)/delt_coupling, 0)`.
  Direct transfer: negative `qsur_f`/`qsub_i` and mask==0 cells to `direct_liq`;
  `qgwl` under `qgwl_runoff_option` (all/negative/threshold: `qgwl_m3s·coupling_period + wr < river_depth_minimum·area`),
  active only for `bypass_routing_option` direct_in_place/direct_to_outlet; frozen
  runoff `direct_ice = qsur_ice_m3s`; glc streams under `rof_from_glc`.
  Aggregation: `runoffocn_liq = -erout` (= `Channel.flow`) for mask>=2; `runofftot_liq = direct_liq + runoffocn_liq + direct_glc_liq`;
  `runofftot_ice = direct_ice + direct_glc_ice`; the ice_runoff branch of
  export_fields (rof_import_export.F90:362-382): with `ice_runoff` on,
  `rofl_m3s = runofftot_liq - direct_glc_liq`, `rofi_m3s = direct_ice`;
  with it off, `rofl_m3s = runofftot_liq + direct_ice - direct_glc_liq`, `rofi_m3s = 0`.

## Documented divergences (all annotated in file metadata)

1. **Subnetwork `vt` when no tributaries** (`tlen <= hlen`): the Fortran leaves
   `vt` stale (unused in the pass-through branch); here `vt` always takes the
   Manning value (the `ifelse` on the clamp condition handles the other branch).
   Values agree whenever `vt` is used downstream.
2. **Channel `vr` in the `areaTotal2/(rwidth·rlen) > 1e6` branch**: the Fortran
   leaves `vr` at the Manning value (unused); here the same is expressed (the
   `vr` ifelse only zeroes for `rlen <= 0` and overrides on the dry-cell clamp).
3. **`volr` uses the running `wr`** (the F90:854 sum `wt + wr + wh·area` is
   computed *after* the irrigation/flood rules in mosart_run; the esm Control
   computes `volr` from the coupled `wr` — consistent because the flood rule is
   a rate rule in the same algebraic system).
4. **Irrigation and flood as rate rules**: the Fortran removes the irrigation
   volume from `wr` in one jump at the start of each coupling period
   (`wr -= irrig_volume`, F90:497) and subtracts the flood flux from `qsur`
   (F90:527); the esm writes both as rates over the period:
   `qirrig_actual = -min(irrig_volume, wr)/coupling_period` enters
   `d(wr)/dt` through `Channel.qirrig`, and `flood = (volr - fthresh)/delt_coupling`
   is subtracted from `qsur`. Mass is conserved in both: the water withdrawn for irrigation leaves
   the channel (or, for the overage, the subsurface stream).
   When the demand fits in the channel (`irrig_volume ≤ wr` all period) the
   period totals are identical to the Fortran (pinned by the
   `irrigation_withdrawal_within_storage` test). When the demand exceeds the
   storage they are not: the Fortran empties the channel in one jump, while the
   esm rate, which depends on the running `wr`, decays it exponentially
   (`wr(T) = wr0/e` with no other flows), so the channel/subsurface split of the
   (fully met) demand differs. Only the instantaneous split is pinned there
   (`irrigation_overage_to_subsurface`). Both rules are evaluated on the running
   state rather than the period-start state. Stage-3 integration may replace
   them with discrete events.
5. **Negative-storage warning** (`write_msg` in updateState_*, F90:361, 384)
   not transcribed (diagnostic only).
6. **`eroutUp` upstream gather and the `rh_direct` outlet gather** are plain
   parameters (`Channel.eroutUp`, `Control.direct_*`) — placeholders until the
   frivinp network data source lands (stage 2.5, boundaries.md §2.4); the
   ID/dnID ESMF SMM topology is not expressible without it.
7. **Fortran logicals** (`rof_from_glc`, `flds_r2l_stream_channel_depths`,
   `ice_runoff`) are 0/1 parameters compared with `== 1.0`.
8. **Continuous storage ODEs** in place of the Fortran's fixed-step forward
   Euler cascade — see the next section; this is the one structural
   divergence, and it is why the tests do not assert the wt/wr split.

## Continuous ODEs vs the Fortran 3600-s Euler stepping

The Fortran advances `wh` once per 3600-s substep and `wt`, `wr`
`DLevelH2R·numDT` times per substep with forward Euler, evaluating every flux —
including the dry-cell clamps — on the state at the start of each step. The
clamps are *per-step* constructs: "if this step's outflow would leave less than
`TINYVALUE` in storage, take only what is there" (e.g.
`etout = -(etin + wt/localdelt)`) refers explicitly to the step length
`localdelt`, and the hillslope outflow `etin` that feeds the subnetwork is held
fixed for a whole 3600-s substep.

Here the same expressions are carried into continuous ODEs as `ifelse`
branches on the instantaneous state. That is a different dynamical system, not a
refinement of the Fortran one: there is no step-size limit in which the
Fortran's clamp (which depends on `localdelt`) becomes the esm's, the subcycle
counts `numDT_*` enter the esm only through `localdelt` inside the clamp tests,
and `etin` reaches the subnetwork as a smooth ramp rather than a staircase. So:

- **What matches:** total water. Every flux leaving one store enters another or
  leaves the cell explicitly, so `volr = wt + wr + wh·area` is conserved exactly
  as in the Fortran (the assembly test pins it to 2.4e-16 rel), and slow,
  forcing-dominated states such as `wh` agree closely (1.0e-6 rel).
- **What does not:** how that water is split between stores within a coupling
  period. For cell 100312 the esm ends the first period with
  `wt = 2.0628e-6 m³` and `wr = 8.523e-16 m³` against CESM's
  `wt = 1.2267e-6 m³` and `wr = 2.620e-16 m³` (×1.68 and ×3.3), with solver
  reltol 1e-14 — a structural difference, not a convergence error.
- **What the tests therefore assert:** pointwise laws, branches and clamps at
  dumped states (exact to round-off), one-substep storage traces where the
  difference is measurably small (each test states its measured gap and bound),
  `volr`/`wh` over a coupling period, and the wt/wr split **not at all** (it is
  quoted in the test description; `wr` is only bounded below the dry-channel
  threshold).

Matching CESM's wt/wr split would need the routing written as the discrete map
it is (fixed-step updates with per-step clamps), which is a stage-3 design
decision for the integrator, not something tolerances can paper over.

## Notes on the Fortran source

No bugs in the MOSART physics were found during this transcription. Two
observations: the `dwt`/`dwr` type comments say [m3] but the code assigns flux
sums and advances storage by `·localdelt` (the rate reading is adopted, noted in
the variable descriptions); and `qgwl` is added to `dwr` unconditionally
(F90:327), also when `bypass_routing_option = none`.

## Testing

Run the suite with

    esm test components/environmental_transport/mosart/mosart_*.esm

(tests of mounted models run when their own file is a target; the assembly run
additionally reports its 4 mounts). `esm validate` passes for the six model and
template files; the coupling library `mosart_routing_coupling.esm` cannot be
validated on its own by the esm 0.12 CLI (its role-scoped references resolve
only through a `coupling_import`), and is validated as part of
`mosart_routing.esm`.

Every test description names its source. There are four kinds:

1. **Dry-window CESM dumps** (`stage1/dumps/mosart/`): the instrumented lane run
   `I2000Clm60Sp_mosart_inst` (cold start 2000-01-01, 8 coupling steps of
   10800 s). Only cell 100312 and a few neighbors carry runoff, and every
   channel stays dry (`mr < TINYVALUE`).
2. **Wet-window CESM dumps** (`stage1/dumps/mosart_wet/`): the same compset,
   grid and dates with 42 traced cells chosen where the day-1 runoff pulse drives
   reaches above bankfull (up to 6.5× bankfull depth) and where `qgwl` is
   large; the instrumented run reproduces the uninstrumented lane restart files
   bit-for-bit, so the dumps only observe the physics.
3. **Standalone gfortran driver** (not a CESM run): the five
   `geometry_*_cell100312` channel pins (in-bank, three trapezoid levels, flood
   plain) take their expected values from the unmodified `GRHR`/`GRPR`/`GRRR`
   compiled out of `mosart_physics.F90` into a small driver and evaluated at
   chosen storages (EqESM checkout, `stage1/analysis/mosart_geometry/mosart_geometry_driver.f90`,
   output `mosart_geometry_reference.txt`; gitignored). They were written
   before the wet window existed, caught the GRHR trapezoid transcription bug,
   and now complement the wet-window `floodplain_geom_*` CESM pins.
4. **Hand-derived from the Fortran algorithm**: the two irrigation tests in
   `mosart_routing.esm` (no dumped window has a nonzero irrigation demand).

| File | Tests | Assertions | What is pinned |
|---|---|---|---|
| `mosart_hillslope.esm` | 9 | 30 | CREHT_nosqrt pointwise at dry-window states (cells 100312/101032/100313, zero storage) and wet-window states (106268/223003/99771), incl. `etin` with the dumped area; one-step growth/drain traces of `d(wh)/dt = qsur + ehout` (ehout/etin at t = 0 with rel 1e-12) |
| `mosart_subnetwork.esm` | 12 | 46 | GRMR/GRHT/GRPT/GRRR chain pointwise (incl. the TINYVALUE zero guards), dry and wet (217950/208214); tributary Manning law dry and wet incl. `etout`/`dwt`; one-step `d(wt)/dt` trace |
| `mosart_channel.esm` | 17 | 89 | dry geometry chain and dry routing branches (2 cells + zero guard) and the one-step `d(wr)/dt = erlateral` trace (dry window); flood-plain geometry (205774/217950/106268) and wet Manning routing with upstream inflow and `qgwl` (205774/217950/208659/99771) plus one wet m-level storage trace (wet window); in-bank/trapezoid/flood-plain geometry (gfortran driver) |
| `mosart_coupling.esm` | 1 | 16 | med↔rof conversions with the run's `med2mod_areacor`: `Flrl_rofsur → qsur_m3s`, `volr`/`wr → Flrr_volr`/`Flrr_volrmch`, all-zero streams |
| `mosart_routing_coupling.esm` | — | — | coupling library (esm-spec §10.9): the 43 edges carry no standalone tests; exercised through the `mosart_routing.esm` tests |
| `mosart_routing.esm` | 5 | 73 | one coupling period of the full assembly for cell 100312 (mass-conserved `volr`, `wh`, CFL/subcycling with the cell's real geometry, zero branches, default `fthresh`); wet-window positive-`qgwl` import (99771, `numDT_r = 7`) and negative-`qgwl` direct transfer (222599); irrigation withdrawal from the channel (mass conservation) and the overage-to-subsurface split; the `rlen = tlen = 0` guards of set_subtimesteps |

### Derived inputs and conversions

- **Per-cell area and area correction** are dumped in
  `mosart_run_imports_wide.csv` (`area`, `areacor` columns): cell 100312 has
  `area = 2.90021364474052906e9 m²`, `med2mod_areacor = 1.00000405527865333`.
  The wet dump has no wide file; the mesh is identical, so the wet-cell tests
  take `area`/`areacor` from the dry-lane wide file (or, for the isolated
  Channel/Hillslope pins, `area·frac = qgwl_area/qgwl` from the dump rows, which
  agrees with it).
- **Cap import fields** (`Flrl_*`) are not dumped; the tests set them to the value
  `state_getimport` maps onto the dumped m³/s stream with the run's own
  `areacor`, `Flrl = q/(med2mod_areacor·area·0.001)`. Exports use
  `mod2med_areacor = 1/med2mod_areacor`.
- **Geometry and slopes** come from the dump columns (`rlen`, `rwidth`,
  `rwidth0`, `rdepth`, `tlen`, `twidth`, `rslpsqrt`, `tslpsqrt`) and the frivinp
  network file (`hslp`, `nh`, `nr`, `nt`, `gxr`); `hlen = 1/(2·Gxr)`
  (mosart_tspatialunit_type.F90:340-359), consistent with the dumped
  `tlen = area/rlen/2 - hlen`. `areaTotal2` is not dumped: it is recomputed from
  the network file as the sum of `area` over every cell whose `dnID` chain
  reaches the cell (what `set_areatotal2` accumulates) — cell 100312 is a
  headwater (`areaTotal2 = area`), 99771 drains 5.88e11 m², 222599 3.98e9 m².
- **numDT** follows from the Fortran formula with those inputs and agrees with
  the dump row multiplicities (`DLevelH2R·numDT` rows per `(step, ns)` key in
  `crvrman_chan.csv`/`crvrman_trib.csv`) for every traced cell checked:
  cell 100312 `phi_r = 21.197 → floor(4.979) = 4`, cell 99771
  `phi_r = 115.5 → floor(7.188) = 7`; without the integer truncation both
  would be wrong, and the tests fail if it is removed.
- **`fthresh`** defaults to the Fortran's `abs(spval) = 1e36`
  (mosart_control_type.F90:388), so the flood rule is inactive unless a test
  sets a threshold; the assembly test asserts `flood = 0` at that default.

### Measured gaps of the one-substep traces

Each trace test states its measured gap (solver reltol 1e-14) and bound:

- hillslope fill: 1.0e-17 m abs = 5.5e-8 rel (growth step); drain step
  1.2e-21 m = 4.3e-12 rel;
- subnetwork: ~6e-17 m³ abs = 2e-11 rel on wt (the `etout` term is ~1e-8 of
  `etin` here);
- channel `wr` accumulation in the dry window: **exact** — the dumped
  `erlat_avg` is the DLevelH2R mean of the five m-level erlateral values, and the
  Fortran's per-m-level sum Σ erlateral(m)·720 equals mean·3600;
- wet channel m-level (cell 217950, first 720 s): 1.06e-4 rel, asserted at
  rel 1.2e-4 (the integrated `erout` is only ~5e-4 of `wr`, so the pin mainly
  checks the `qgwl` + `erlateral` drive; the Manning law is pinned pointwise
  by the `wet_manning_*` tests).

The coupling-period gap of the assembly (the wt/wr split) is the structural one
described in
[Continuous ODEs vs the Fortran 3600-s Euler stepping](#continuous-odes-vs-the-fortran-3600-s-euler-stepping).

### Coverage gaps

- **Irrigation and flood from CESM**: neither dumped window has a nonzero
  irrigation demand or an active flood threshold, so the irrigation tests are
  hand-derived and the flood branch is pinned only at its inactive default.
- **Clamp firing on a wet cell**: the dry-cell clamps fire in the dumps only at
  zero storage (cold start); the clamp's `vt = -etout/mt` / `vr = -erout/mr`
  override (with `mt`, `mr > 0`) is not exercised by any dumped row.
- **Branches not present in either window**: `areaTotal2/(rwidth·rlen) > 1e6`;
  `rlen <= 0` and the `tlen <= hlen` pass-through only through the hand-derived
  irrigation test; the `qgwl_runoff_option = threshold`/`all` paths; `mask = 0`
  and outlet (`mask >= 2`) aggregation with routed flow.
- **Coupling-period end states of wet cells**: the isolated-cell assembly has
  `eroutUp = 0`, so for cells with upstream inflow only t = 0 diagnostics are
  asserted (the network gather is a stage-2.5 item).

## Next steps (stage 2.5 / stage 3)

1. A stage-1 window with irrigation demand and an active flood threshold, to
   replace the hand-derived irrigation tests with CESM pins.
2. frivinp network `data_sources` (static) + ID/dnID gather → replace the
   `eroutUp`/`direct` placeholders.
3. Decide how the integrator represents the Fortran's fixed-step cascade
   (see the continuous-ODE section) if the wt/wr split must match CESM.
4. Mount into `eqesm.esm` and integrate with earthsciintegrator; compare
   against full-CESM simulations (conservation via `mosart_budget_type.F90`).
