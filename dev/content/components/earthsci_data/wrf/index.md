---
title: "WRF"
slug: "wrf"
domains: ["earthsci_data"]
component_types: ["model"]
domain: "earthsci_data"
component_type: "model"
esm_version: "1.0.0"
esm_path: "components/earthsci_data/wrf.esm"
reference: "https://www2.mmm.ucar.edu/wrf/users/"
description: "WRF regridding model — the coupler half of the wrf loader+regridding-model split (RFC pure-io-data-loaders §6/§7; bead esm-3nc.1). Exposes WRF regional weather fields (UCAR RDA d340000, WRF-Chem v3.9.1 CONUS 12 km) on the simulation's target grid for advection and chemistry coupling in EarthSciML systems."
tags: ["earthsci_data", "model", "meteorology", "atmospheric_dynamics", "regridding_model", "regional_climate", "wrf", "conus", "lambert_conformal"]
---

## Description

WRF regridding model — the coupler half of the wrf loader+regridding-model split (RFC pure-io-data-loaders §6/§7; bead esm-3nc.1). Exposes WRF regional weather fields (UCAR RDA d340000, WRF-Chem v3.9.1 CONUS 12 km) on the simulation's target grid for advection and chemistry coupling in EarthSciML systems.

Structure (RFC pure-io-data-loaders §6):
  1. It declares the pure-I/O source inline: at 0.7.0 the loader was the separate file components/earthsci_data/wrf_loader.esm, mounted as the subsystem `raw`; at esm 1.0.0 it is the `WRF_hourly_d01` entry in this file's own `data_sources` and the standalone file is gone (a data source is not a component, so it neither needs nor may be a subsystem). Loader fields are referenced as raw.<var> (e.g. raw.U) and re-exposed as model-level observed variables (WRF.U, WRF.V, ...) to preserve the runtime MeanWind coupling contract (WRF.U/V/W → MeanWind via WRFCoupler/couple2).
  2. Reprojection: WRF's native grid is projected (lambert_conformal), so the coordinate transform is the LCC reproject (ESD reprojection/lambert_conformal.esm, esd-47z.2) — selected by convention from the loader's grid.crs.projection = 'lambert_conformal' and parameterized by the loader's crs parameters {lat_1:30, lat_2:60, lat_0:38.999996, lon_0:-97, R:6370000}.
  3. Regridding (per variable, RFC §5.2): the Arakawa-C-grid wind components U, V, W are edge/face-staggered → B-spline interpolation; the cell-centered scalars T, PH, PHB, P, PB, QVAPOR → conservative (area-weighted, mass-conserving) regridding. Declared in the `regrid` block.

Top-level derived quantities computed on the target grid: total pressure P_total = P + PB, geopotential height z = (PH + PHB)/g, and the lat/lon coordinate metrics δxδlon and δyδlat (emitted only for lat/lon coordinate domains).

MeanWind coupling (from EarthSciData.jl@830435a coupling.jl): MeanWind.v_lon ~ WRF.U, MeanWind.v_lat ~ WRF.V, MeanWind.v_lev ~ WRF.W.

Migrated from EarthSciData.jl@830435a065f27e99f10bba91107ca1730322cc6b:src/wrf.jl:169 (WRF constructor, esm-4l84); split into pure loader + regridding model by esm-3nc.1.

## Reference

_source_ref: EarthSciData.jl@830435a065f27e99f10bba91107ca1730322cc6b:src/wrf.jl:169

This is the regridding-model half of the pure-IO loader migration (RFC pure-io-data-loaders §6/§7, bead esm-3nc.1). The pre-migration wrf.esm carried both the coupler model AND a co-located data_loaders.WRF_hourly_d01 block (with the now-removed `spatial` and `regridding` sub-blocks). That loader became, at 0.7.0, the pure-I/O file components/earthsci_data/wrf_loader.esm, referenced as subsystem `raw`; at esm 1.0.0 it is the `WRF_hourly_d01` entry in THIS file's `data_sources` and the standalone file is gone.

Upstream WRF(domaininfo; name=:WRF, stream=true, spatial_interp=:linear) created an MTK System with:
  - @parameters: lon/lat (rad) when pvars include :lat/:lon, or x/y (m) when pvars include :x/:y; lev (1); t_ref (s)
  - For every varname in WRFFileSet.varnames(fs), one DataSetInterpolator and one observed equation via create_interp_equation (uses interp_unsafe). These are now provided by the loader subsystem `raw` (raw.<var>) and re-exposed as model observed variables U/V/W/T/PH/PHB/P/PB/QVAPOR for the coupling contract.
  - Staggered grids: PH/PHB/W on bottom_top_stag (N+1 z-points), U on west_east_stag (N+1 x-points), V on south_north_stag (N+1 y-points); the upstream loader de-staggers to mass centres in loadmetadata. In the new pipeline the native staggered dimensions are preserved on the loader's GDD grid and the wind components are regridded with a B-spline kernel (RFC §5.2).
  - Extrapolation: W uses extrapolate_type=0.0 (zero below ground); all others use Flat() (clamp).
  - Derived observed variables: P_total ~ P + PB; z ~ (PH + PHB)/g with g=9.80665 m/s²; δxδlon ~ lon2m·cos(lat) and δyδlat ~ lat2meters (only when :lat in pvdict), lon2m = 40075e3/(2π) ≈ 6378134.3, lat2meters = 111.32e3·180/π ≈ 6378166.0.
  - couple2 with MeanWindCoupler: maps WRF.U/V/W → MeanWind v_lon/v_lat/v_lev via _couple_meanwind.

Reprojection (RFC §6 step 2): WRF's native grid.crs.projection is 'lambert_conformal', so the reprojection rule selected by convention is ESD reprojection/lambert_conformal.esm (esd-47z.2), parameterized by the loader crs parameters {lat_1:30, lat_2:60, lat_0:38.999996, lon_0:-97} on a sphere of radius R=6370000 m. The projected-grid construction (corner geometry via inverse LCC) is ESD discretizations/grids/lambert_conformal/wrf_lcc.esm (esd-47z.5).

Regridding (RFC §6 step 3 / §5.2): declared per variable in the model `regrid` block. The Arakawa-C-grid wind components U (west_east_stag), V (south_north_stag), W (bottom_top_stag) are edge/face-staggered → B-spline interpolating regridder (ESD regridding/bspline_regrid.esm, esd-47z.3). The cell-centered scalars T, PH, PHB, P, PB, QVAPOR → conservative area-weighted overlap join (ESD regridding/conservative_regrid_overlap_join.esm). (PH/PHB are geopotential scalars even though they reside on the staggered w-levels; they are mass-like quantities regridded conservatively.)

δzδlev gap (gt-p3ep(lookup)): evaluating PH and PHB at lev+1 requires the indexed-offset form of loader evaluation (a gt-p3ep(lookup) expression) not yet representable in the ESM expression language. δzδlev is omitted from this migration. When gt-p3ep(lookup) is resolved, add δzδlev = (raw.PH@lev+1 + raw.PHB@lev+1 - raw.PH - raw.PHB)/9.80665.

Coordinate system: this ESM targets the lat/lon coordinate form (pvars contain :lat and :lon). For LCC-projected (x/y) domains the loader uses pvars :x and :y; δxδlon/δyδlat are not emitted in that case.

Live tests (informational; require UCAR RDA NetCDF files, not run in CI): EarthSciData.jl wrf_test.jl expected values at (lon=-118.2707°, lat=34.0059°):
  P_total at lev=[1,1.5,2,21.5,30,31.5]: [100331.86, 100235.72, 100139.58, 67846.08, 30679.47, 28729.87] Pa
  W at lev=[0.5,1,1.5,2,21.5,30,31.5]: [0.0, 5.205e-3, 1.041e-2, 1.164e-2, -1.698e-2, 2.697e-2, 2.244e-2] m/s

Coupler identity: this model was serialized with the model-level field `coupletype: "WRFCoupler"`, the EarthSciMLBase `CoupleType` metadata tag naming the Julia coupler struct that `EarthSciMLBase.couple2` dispatches on to find this component's pairwise coupling rules. The esm schema defined `coupletype` only before 0.8.0 ("informational label identifying this system's role in coupling"); 0.8.0 removed it in favour of explicit coupling — `coupling` entries naming components directly, or `coupling_roles` + `coupling_import` in a coupling-library file (esm-spec §10.9–§10.11). esm 1.0.0 has no model-level coupler-identity field, so the tag is recorded here to keep it recoverable.

Regridding intent: this model was serialized with the model-level `regrid` map, one entry per variable naming the kernel that carries the loaded native-grid field onto the consuming model's grid. The esm schema defined `regrid` only before 0.8.0. esm 1.0.0 states (esm-spec §8.6) that a data source performs no regridding and that there is NO `Model.regrid` map: the carrier is the `variable_map` entry's `transform` field on the coupling edge that consumes the field (§10.4/§10.5) — an ordinary `aggregate` expression, typically an `apply_expression_template` invocation of an imported overlap-weight library. No such coupling edge exists in this document, so the map is recorded here VERBATIM to keep every field recoverable. This is a demotion from a structured field to prose, not an equivalent: the transform expression still has to be authored on whichever coupling edge consumes these fields.

`regrid` (verbatim):
{
  "U": {
    "method": "bspline",
    "description": "Zonal wind on west_east_stag (Arakawa-C x-edges). Edge-staggered C-grid wind → B-spline interpolating regridder (ESD regridding/bspline_regrid.esm, esd-47z.3)."
  },
  "V": {
    "method": "bspline",
    "description": "Meridional wind on south_north_stag (Arakawa-C y-edges). Edge-staggered C-grid wind → B-spline interpolating regridder (esd-47z.3)."
  },
  "W": {
    "method": "bspline",
    "description": "Vertical wind on bottom_top_stag (Arakawa-C z-edges). Face-staggered C-grid wind → B-spline interpolating regridder (esd-47z.3)."
  },
  "T": {
    "method": "conservative",
    "description": "Perturbation potential temperature (K). Cell-centered scalar → conservative area-weighted overlap-join regridder (ESD regridding/conservative_regrid_overlap_join.esm)."
  },
  "PH": {
    "method": "conservative",
    "description": "Perturbation geopotential (m²/s²). A geopotential scalar (mass-like quantity, regridded conservatively even though it resides on the staggered w-levels)."
  },
  "PHB": {
    "method": "conservative",
    "description": "Base-state geopotential (m²/s²). A geopotential scalar → conservative regridder (see PH)."
  },
  "P": {
    "method": "conservative",
    "description": "Perturbation pressure (Pa). Cell-centered scalar → conservative regridder."
  },
  "PB": {
    "method": "conservative",
    "description": "Base-state pressure (Pa). Cell-centered scalar → conservative regridder."
  },
  "QVAPOR": {
    "method": "conservative",
    "description": "Water vapor mixing ratio (kg/kg). Cell-centered scalar → conservative regridder."
  }
}_

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `lon` | `rad` | `0.0` | Longitude of the model grid point (radians). Coupled to the simulation domain's longitude coordinate via param_to_var when composed into a CoupledSystem. Used as the x-axis coordinate for WRF data interpolation in lat/lon domains. |
| `lat` | `rad` | `0.0` | Latitude of the model grid point (radians). Coupled to the simulation domain's latitude coordinate via param_to_var when composed into a CoupledSystem. Used as the y-axis coordinate for WRF data interpolation in lat/lon domains. |
| `lev` | `1` | `1.0` | Vertical level index (dimensionless, 1-based integer corresponding to the WRF bottom_top layer). Fractional values interpolate between layers. Coupled from the simulation domain's lev coordinate. |
| `t_ref` | `s` | `0.0` | Reference epoch (seconds since the Julian date epoch) from which the WRF file time axis is offset. Set from DomainInfo.get_tref(domaininfo) at construction time. |
| `U` | `m/s` |  | Zonal (west–east) wind component (m/s). Sourced from the loader field raw.U (WRF variable U on the west_east_stag C-grid edges), regridded with a B-spline kernel. Coupled to MeanWind.v_lon via WRFCoupler/couple2. |
| `V` | `m/s` |  | Meridional (south–north) wind component (m/s). Sourced from the loader field raw.V (WRF variable V on the south_north_stag C-grid edges), regridded with a B-spline kernel. Coupled to MeanWind.v_lat via WRFCoupler/couple2. |
| `W` | `m/s` |  | Vertical wind component (m/s). Sourced from the loader field raw.W (WRF variable W on the bottom_top_stag C-grid edges), regridded with a B-spline kernel. Zero-extrapolated below the surface in the upstream loader. Coupled to MeanWind.v_lev via WRFCoupler/couple2. |
| `T` | `K` |  | Perturbation potential temperature (K). Full potential temperature θ = T + 300 K. Cell-centred (mass grid), conservatively regridded. Sourced from raw.T. |
| `PH` | `m^2/s^2` |  | Perturbation geopotential (m² s⁻²). On the w-level (bottom_top_stag) grid. PH + PHB gives total geopotential. Sourced from raw.PH. |
| `PHB` | `m^2/s^2` |  | Base-state geopotential (m² s⁻²). On the w-level (bottom_top_stag) grid. PH + PHB gives total geopotential. Sourced from raw.PHB. |
| `P` | `Pa` |  | Perturbation pressure (Pa). Cell-centred (mass grid). P + PB gives total atmospheric pressure. Sourced from raw.P. |
| `PB` | `Pa` |  | Base-state pressure (Pa). Cell-centred (mass grid). P + PB gives total atmospheric pressure. Sourced from raw.PB. |
| `QVAPOR` | `kg/kg` |  | Water vapor mixing ratio (kg water per kg dry air). Cell-centred (mass grid). Sourced from raw.QVAPOR. |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `P_total` | `Pa` |  | Total atmospheric pressure (Pa): P_total = P + PB. Sum of perturbation and base-state pressure components, both on the mass grid. Computed from the loader fields raw.P and raw.PB. |
| `z` | `m` |  | Geopotential height (m): z = (PH + PHB) / g, where g = 9.80665 m s⁻². Computed from the w-level geopotential components. Corresponds to the upstream z ~ (PH_itp + PHB_itp) / g_const equation. |
| `δxδlon` | `m/rad` |  | Coordinate metric: x-distance per unit longitude (m rad⁻¹). δxδlon = lon2m·cos(lat) where lon2m = 40075×10³/(2π) ≈ 6378134 m rad⁻¹ (equatorial circumference metric). Non-zero only in lat/lon coordinate domains; the upstream constructor emits this equation only when :lat is in DomainInfo.pvars. |
| `δyδlat` | `m/rad` |  | Coordinate metric: y-distance per unit latitude (m rad⁻¹). δyδlat = lat2meters = 111.32×10³·(180/π) ≈ 6378166 m rad⁻¹. Constant (does not depend on position). Emitted only in lat/lon coordinate domains. |

## Observed expressions

$$
P_{total} = P + PB
$$
_Total atmospheric pressure (Pa): P_total = P + PB. Sum of perturbation and base-state pressure components, both on the mass grid. Computed from the loader fields raw.P and raw.PB._

$$
z = \frac{PH + PHB}{9.80665}
$$
_Geopotential height (m): z = (PH + PHB) / g, where g = 9.80665 m s⁻². Computed from the w-level geopotential components. Corresponds to the upstream z ~ (PH_itp + PHB_itp) / g_const equation._

$$
δxδlon = 6378134.3 \cdot \cos\left(lat\right)
$$
_Coordinate metric: x-distance per unit longitude (m rad⁻¹). δxδlon = lon2m·cos(lat) where lon2m = 40075×10³/(2π) ≈ 6378134 m rad⁻¹ (equatorial circumference metric). Non-zero only in lat/lon coordinate domains; the upstream constructor emits this equation only when :lat is in DomainInfo.pvars._

$$
δyδlat = 6378166.0
$$
_Coordinate metric: y-distance per unit latitude (m rad⁻¹). δyδlat = lat2meters = 111.32×10³·(180/π) ≈ 6378166 m rad⁻¹. Constant (does not depend on position). Emitted only in lat/lon coordinate domains._

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "reference": {
    "notes": "source_ref: EarthSciData.jl@830435a065f27e99f10bba91107ca1730322cc6b:src/wrf.jl:169\n\nThis is the regridding-model half of the pure-IO loader migration (RFC pure-io-data-loaders §6/§7, bead esm-3nc.1). The pre-migration wrf.esm carried both the coupler model AND a co-located data_loaders.WRF_hourly_d01 block (with the now-removed `spatial` and `regridding` sub-blocks). That loader became, at 0.7.0, the pure-I/O file components/earthsci_data/wrf_loader.esm, referenced as subsystem `raw`; at esm 1.0.0 it is the `WRF_hourly_d01` entry in THIS file's `data_sources` and the standalone file is gone.\n\nUpstream WRF(domaininfo; name=:WRF, stream=true, spatial_interp=:linear) created an MTK System with:\n  - @parameters: lon/lat (rad) when pvars include :lat/:lon, or x/y (m) when pvars include :x/:y; lev (1); t_ref (s)\n  - For every varname in WRFFileSet.varnames(fs), one DataSetInterpolator and one observed equation via create_interp_equation (uses interp_unsafe). These are now provided by the loader subsystem `raw` (raw.<var>) and re-exposed as model observed variables U/V/W/T/PH/PHB/P/PB/QVAPOR for the coupling contract.\n  - Staggered grids: PH/PHB/W on bottom_top_stag (N+1 z-points), U on west_east_stag (N+1 x-points), V on south_north_stag (N+1 y-points); the upstream loader de-staggers to mass centres in loadmetadata. In the new pipeline the native staggered dimensions are preserved on the loader's GDD grid and the wind components are regridded with a B-spline kernel (RFC §5.2).\n  - Extrapolation: W uses extrapolate_type=0.0 (zero below ground); all others use Flat() (clamp).\n  - Derived observed variables: P_total ~ P + PB; z ~ (PH + PHB)/g with g=9.80665 m/s²; δxδlon ~ lon2m·cos(lat) and δyδlat ~ lat2meters (only when :lat in pvdict), lon2m = 40075e3/(2π) ≈ 6378134.3, lat2meters = 111.32e3·180/π ≈ 6378166.0.\n  - couple2 with MeanWindCoupler: maps WRF.U/V/W → MeanWind v_lon/v_lat/v_lev via _couple_meanwind.\n\nReprojection (RFC §6 step 2): WRF's native grid.crs.projection is 'lambert_conformal', so the reprojection rule selected by convention is ESD reprojection/lambert_conformal.esm (esd-47z.2), parameterized by the loader crs parameters {lat_1:30, lat_2:60, lat_0:38.999996, lon_0:-97} on a sphere of radius R=6370000 m. The projected-grid construction (corner geometry via inverse LCC) is ESD discretizations/grids/lambert_conformal/wrf_lcc.esm (esd-47z.5).\n\nRegridding (RFC §6 step 3 / §5.2): declared per variable in the model `regrid` block. The Arakawa-C-grid wind components U (west_east_stag), V (south_north_stag), W (bottom_top_stag) are edge/face-staggered → B-spline interpolating regridder (ESD regridding/bspline_regrid.esm, esd-47z.3). The cell-centered scalars T, PH, PHB, P, PB, QVAPOR → conservative area-weighted overlap join (ESD regridding/conservative_regrid_overlap_join.esm). (PH/PHB are geopotential scalars even though they reside on the staggered w-levels; they are mass-like quantities regridded conservatively.)\n\nδzδlev gap (gt-p3ep(lookup)): evaluating PH and PHB at lev+1 requires the indexed-offset form of loader evaluation (a gt-p3ep(lookup) expression) not yet representable in the ESM expression language. δzδlev is omitted from this migration. When gt-p3ep(lookup) is resolved, add δzδlev = (raw.PH@lev+1 + raw.PHB@lev+1 - raw.PH - raw.PHB)/9.80665.\n\nCoordinate system: this ESM targets the lat/lon coordinate form (pvars contain :lat and :lon). For LCC-projected (x/y) domains the loader uses pvars :x and :y; δxδlon/δyδlat are not emitted in that case.\n\nLive tests (informational; require UCAR RDA NetCDF files, not run in CI): EarthSciData.jl wrf_test.jl expected values at (lon=-118.2707°, lat=34.0059°):\n  P_total at lev=[1,1.5,2,21.5,30,31.5]: [100331.86, 100235.72, 100139.58, 67846.08, 30679.47, 28729.87] Pa\n  W at lev=[0.5,1,1.5,2,21.5,30,31.5]: [0.0, 5.205e-3, 1.041e-2, 1.164e-2, -1.698e-2, 2.697e-2, 2.244e-2] m/s\n\nCoupler identity: this model was serialized with the model-level field `coupletype: \"WRFCoupler\"`, the EarthSciMLBase `CoupleType` metadata tag naming the Julia coupler struct that `EarthSciMLBase.couple2` dispatches on to find this component's pairwise coupling rules. The esm schema defined `coupletype` only before 0.8.0 (\"informational label identifying this system's role in coupling\"); 0.8.0 removed it in favour of explicit coupling — `coupling` entries naming components directly, or `coupling_roles` + `coupling_import` in a coupling-library file (esm-spec §10.9–§10.11). esm 1.0.0 has no model-level coupler-identity field, so the tag is recorded here to keep it recoverable.\n\nRegridding intent: this model was serialized with the model-level `regrid` map, one entry per variable naming the kernel that carries the loaded native-grid field onto the consuming model's grid. The esm schema defined `regrid` only before 0.8.0. esm 1.0.0 states (esm-spec §8.6) that a data source performs no regridding and that there is NO `Model.regrid` map: the carrier is the `variable_map` entry's `transform` field on the coupling edge that consumes the field (§10.4/§10.5) — an ordinary `aggregate` expression, typically an `apply_expression_template` invocation of an imported overlap-weight library. No such coupling edge exists in this document, so the map is recorded here VERBATIM to keep every field recoverable. This is a demotion from a structured field to prose, not an equivalent: the transform expression still has to be authored on whichever coupling edge consumes these fields.\n\n`regrid` (verbatim):\n{\n  \"U\": {\n    \"method\": \"bspline\",\n    \"description\": \"Zonal wind on west_east_stag (Arakawa-C x-edges). Edge-staggered C-grid wind → B-spline interpolating regridder (ESD regridding/bspline_regrid.esm, esd-47z.3).\"\n  },\n  \"V\": {\n    \"method\": \"bspline\",\n    \"description\": \"Meridional wind on south_north_stag (Arakawa-C y-edges). Edge-staggered C-grid wind → B-spline interpolating regridder (esd-47z.3).\"\n  },\n  \"W\": {\n    \"method\": \"bspline\",\n    \"description\": \"Vertical wind on bottom_top_stag (Arakawa-C z-edges). Face-staggered C-grid wind → B-spline interpolating regridder (esd-47z.3).\"\n  },\n  \"T\": {\n    \"method\": \"conservative\",\n    \"description\": \"Perturbation potential temperature (K). Cell-centered scalar → conservative area-weighted overlap-join regridder (ESD regridding/conservative_regrid_overlap_join.esm).\"\n  },\n  \"PH\": {\n    \"method\": \"conservative\",\n    \"description\": \"Perturbation geopotential (m²/s²). A geopotential scalar (mass-like quantity, regridded conservatively even though it resides on the staggered w-levels).\"\n  },\n  \"PHB\": {\n    \"method\": \"conservative\",\n    \"description\": \"Base-state geopotential (m²/s²). A geopotential scalar → conservative regridder (see PH).\"\n  },\n  \"P\": {\n    \"method\": \"conservative\",\n    \"description\": \"Perturbation pressure (Pa). Cell-centered scalar → conservative regridder.\"\n  },\n  \"PB\": {\n    \"method\": \"conservative\",\n    \"description\": \"Base-state pressure (Pa). Cell-centered scalar → conservative regridder.\"\n  },\n  \"QVAPOR\": {\n    \"method\": \"conservative\",\n    \"description\": \"Water vapor mixing ratio (kg/kg). Cell-centered scalar → conservative regridder.\"\n  }\n}"
  },
  "tolerance": {
    "rel": 1e-06
  },
  "variables": {
    "lon": {
      "type": "parameter",
      "units": "rad",
      "default": 0.0,
      "description": "Longitude of the model grid point (radians). Coupled to the simulation domain's longitude coordinate via param_to_var when composed into a CoupledSystem. Used as the x-axis coordinate for WRF data interpolation in lat/lon domains."
    },
    "lat": {
      "type": "parameter",
      "units": "rad",
      "default": 0.0,
      "description": "Latitude of the model grid point (radians). Coupled to the simulation domain's latitude coordinate via param_to_var when composed into a CoupledSystem. Used as the y-axis coordinate for WRF data interpolation in lat/lon domains."
    },
    "lev": {
      "type": "parameter",
      "units": "1",
      "default": 1.0,
      "description": "Vertical level index (dimensionless, 1-based integer corresponding to the WRF bottom_top layer). Fractional values interpolate between layers. Coupled from the simulation domain's lev coordinate."
    },
    "t_ref": {
      "type": "parameter",
      "units": "s",
      "default": 0.0,
      "description": "Reference epoch (seconds since the Julian date epoch) from which the WRF file time axis is offset. Set from DomainInfo.get_tref(domaininfo) at construction time."
    },
    "U": {
      "type": "parameter",
      "units": "m/s",
      "description": "Zonal (west–east) wind component (m/s). Sourced from the loader field raw.U (WRF variable U on the west_east_stag C-grid edges), regridded with a B-spline kernel. Coupled to MeanWind.v_lon via WRFCoupler/couple2.",
      "update": {
        "kind": "data",
        "source": "WRF_hourly_d01",
        "from": {
          "file_variable": "U",
          "description": "Zonal (west–east) wind component. WRF output variable U on the west_east_stag grid (C-grid x-edges). The regridding model interpolates this staggered field with a B-spline kernel."
        }
      }
    },
    "V": {
      "type": "parameter",
      "units": "m/s",
      "description": "Meridional (south–north) wind component (m/s). Sourced from the loader field raw.V (WRF variable V on the south_north_stag C-grid edges), regridded with a B-spline kernel. Coupled to MeanWind.v_lat via WRFCoupler/couple2.",
      "update": {
        "kind": "data",
        "source": "WRF_hourly_d01",
        "from": {
          "file_variable": "V",
          "description": "Meridional (south–north) wind component. WRF output variable V on the south_north_stag grid (C-grid y-edges). The regridding model interpolates this staggered field with a B-spline kernel."
        }
      }
    },
    "W": {
      "type": "parameter",
      "units": "m/s",
      "description": "Vertical wind component (m/s). Sourced from the loader field raw.W (WRF variable W on the bottom_top_stag C-grid edges), regridded with a B-spline kernel. Zero-extrapolated below the surface in the upstream loader. Coupled to MeanWind.v_lev via WRFCoupler/couple2.",
      "update": {
        "kind": "data",
        "source": "WRF_hourly_d01",
        "from": {
          "file_variable": "W",
          "description": "Vertical wind component. WRF output variable W on the bottom_top_stag grid (C-grid z-edges). The regridding model interpolates this staggered field with a B-spline kernel. Zero extrapolation below the surface (extrapolate_type=0.0 in the upstream loader, overriding the default clamp for this variable only)."
        }
      }
    },
    "T": {
      "type": "parameter",
      "units": "K",
      "description": "Perturbation potential temperature (K). Full potential temperature θ = T + 300 K. Cell-centred (mass grid), conservatively regridded. Sourced from raw.T.",
      "update": {
        "kind": "data",
        "source": "WRF_hourly_d01",
        "from": {
          "file_variable": "T",
          "description": "Perturbation potential temperature (K). On the mass (bottom_top) grid, cell-centred. Full potential temperature θ = T + 300 K."
        }
      }
    },
    "PH": {
      "type": "parameter",
      "units": "m^2/s^2",
      "description": "Perturbation geopotential (m² s⁻²). On the w-level (bottom_top_stag) grid. PH + PHB gives total geopotential. Sourced from raw.PH.",
      "update": {
        "kind": "data",
        "source": "WRF_hourly_d01",
        "from": {
          "file_variable": "PH",
          "description": "Perturbation geopotential (m² s⁻²). On the w-level (bottom_top_stag) grid. Together with PHB provides geopotential height z = (PH+PHB)/g."
        }
      }
    },
    "PHB": {
      "type": "parameter",
      "units": "m^2/s^2",
      "description": "Base-state geopotential (m² s⁻²). On the w-level (bottom_top_stag) grid. PH + PHB gives total geopotential. Sourced from raw.PHB.",
      "update": {
        "kind": "data",
        "source": "WRF_hourly_d01",
        "from": {
          "file_variable": "PHB",
          "description": "Base-state geopotential (m² s⁻²). On the w-level (bottom_top_stag) grid. Together with PH provides geopotential height z = (PH+PHB)/g."
        }
      }
    },
    "P": {
      "type": "parameter",
      "units": "Pa",
      "description": "Perturbation pressure (Pa). Cell-centred (mass grid). P + PB gives total atmospheric pressure. Sourced from raw.P.",
      "update": {
        "kind": "data",
        "source": "WRF_hourly_d01",
        "from": {
          "file_variable": "P",
          "description": "Perturbation pressure (Pa). On the mass (bottom_top) grid, cell-centred. Together with PB provides total atmospheric pressure P_total = P + PB."
        }
      }
    },
    "PB": {
      "type": "parameter",
      "units": "Pa",
      "description": "Base-state pressure (Pa). Cell-centred (mass grid). P + PB gives total atmospheric pressure. Sourced from raw.PB.",
      "update": {
        "kind": "data",
        "source": "WRF_hourly_d01",
        "from": {
          "file_variable": "PB",
          "description": "Base-state pressure (Pa). On the mass (bottom_top) grid, cell-centred. Together with P provides total atmospheric pressure P_total = P + PB."
        }
      }
    },
    "QVAPOR": {
      "type": "parameter",
      "units": "kg/kg",
      "description": "Water vapor mixing ratio (kg water per kg dry air). Cell-centred (mass grid). Sourced from raw.QVAPOR.",
      "update": {
        "kind": "data",
        "source": "WRF_hourly_d01",
        "from": {
          "file_variable": "QVAPOR",
          "description": "Water vapor mixing ratio (kg water kg⁻¹ dry air). On the mass (bottom_top) grid, cell-centred."
        }
      }
    },
    "P_total": {
      "type": "unknown",
      "units": "Pa",
      "description": "Total atmospheric pressure (Pa): P_total = P + PB. Sum of perturbation and base-state pressure components, both on the mass grid. Computed from the loader fields raw.P and raw.PB."
    },
    "z": {
      "type": "unknown",
      "units": "m",
      "description": "Geopotential height (m): z = (PH + PHB) / g, where g = 9.80665 m s⁻². Computed from the w-level geopotential components. Corresponds to the upstream z ~ (PH_itp + PHB_itp) / g_const equation."
    },
    "δxδlon": {
      "type": "unknown",
      "units": "m/rad",
      "description": "Coordinate metric: x-distance per unit longitude (m rad⁻¹). δxδlon = lon2m·cos(lat) where lon2m = 40075×10³/(2π) ≈ 6378134 m rad⁻¹ (equatorial circumference metric). Non-zero only in lat/lon coordinate domains; the upstream constructor emits this equation only when :lat is in DomainInfo.pvars."
    },
    "δyδlat": {
      "type": "unknown",
      "units": "m/rad",
      "description": "Coordinate metric: y-distance per unit latitude (m rad⁻¹). δyδlat = lat2meters = 111.32×10³·(180/π) ≈ 6378166 m rad⁻¹. Constant (does not depend on position). Emitted only in lat/lon coordinate domains."
    }
  },
  "equations": [
    {
      "lhs": "P_total",
      "rhs": {
        "op": "+",
        "args": [
          "P",
          "PB"
        ]
      }
    },
    {
      "lhs": "z",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "+",
            "args": [
              "PH",
              "PHB"
            ]
          },
          9.80665
        ]
      }
    },
    {
      "lhs": "δxδlon",
      "rhs": {
        "op": "*",
        "args": [
          6378134.3,
          {
            "op": "cos",
            "args": [
              "lat"
            ]
          }
        ]
      }
    },
    {
      "lhs": "δyδlat",
      "rhs": 6378166.0
    }
  ],
  "tests": []
}
```

</details>
