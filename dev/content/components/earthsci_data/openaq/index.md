---
title: "OpenAQ"
slug: "openaq"
domains: ["earthsci_data"]
component_types: ["model"]
domain: "earthsci_data"
component_type: "model"
esm_version: "1.0.0"
esm_path: "components/earthsci_data/openaq.esm"
reference: "https://openaq.org/"
description: "OpenAQ regridding model — the coupler half of the openaq loader+regridding-model split (RFC pure-io-data-loaders §6/§7; bead esm-3nc.5). Exposes ground-based air quality monitoring observations (PM2.5, PM10, O3, NO2, SO2, CO, BC, PM1, NO, NOx) on the simulation's target grid for coupling into EarthSciML systems."
tags: ["earthsci_data", "model", "air_quality", "observations", "monitoring_stations", "hourly", "regridding_model", "point_observations", "longlat"]
---

## Description

OpenAQ regridding model — the coupler half of the openaq loader+regridding-model split (RFC pure-io-data-loaders §6/§7; bead esm-3nc.5). Exposes ground-based air quality monitoring observations (PM2.5, PM10, O3, NO2, SO2, CO, BC, PM1, NO, NOx) on the simulation's target grid for coupling into EarthSciML systems.

Structure (RFC pure-io-data-loaders §6):
  1. It declares the pure-I/O source inline: at 0.7.0 the loader was the separate file components/earthsci_data/openaq_loader.esm, mounted as the subsystem `obs`; at esm 1.0.0 it is the `OpenAQ_obs` entry in this file's own `data_sources` and the standalone file is gone (a data source is not a component, so it neither needs nor may be a subsystem). Loader fields are referenced as obs.<var> (e.g. obs.pm25).
  2. Reprojection: OpenAQ's station coordinates are geographic (longlat/WGS84), so the coordinate transform is the longlat IDENTITY (ESD reprojection/longlat.esm, esd-47z.1) — selected by convention from the loader's native geographic crs (recorded in the loader metadata, since this points loader resolves its native grid at runtime and carries no formal GDD `grid`); a no-op for unprojected station coordinates.
  3. Regridding (per variable, RFC §5.2): every variable is a scattered point field → cell-averaging regridder (ESD regridding/point_cell_average_regrid.esm, esd-47z.4): the source stations falling within each target cell are bin-averaged, and a target cell containing no station is filled with `missing_value`. The esm schema defined the model-level `regrid` map only before 0.8.0; esm 1.0.0 has no such map (esm-spec §8.6 — a data source performs no regridding, and the carrier of a kernel is the `transform` on the `variable_map` entry of the coupling edge that consumes the field). No such coupling edge exists in this document, so the demoted map is recorded verbatim under `models.OpenAQ.reference.notes` to keep the per-variable kernel and `missing_value` recoverable.

This model re-exposes the representative parameter pm25 at the model top level (OpenAQ.pm25, expression obs.pm25) to preserve the pre-migration coupling interface. One OpenAQ instantiation covers one parameter; other instantiations use the respective variable name (pm10, o3, no2, so2, co, bc, pm1, no, nox), all available as obs.<var> and all covered by the verbatim `regrid` record in `models.OpenAQ.reference.notes`.

Migrated from EarthSciData.jl@830435a065f27e99f10bba91107ca1730322cc6b:src/openaq.jl:595 (OpenAQ constructor, esm-mfi7); split into pure loader + regridding model by esm-3nc.5.

## Reference

_source_ref: EarthSciData.jl@830435a065f27e99f10bba91107ca1730322cc6b:src/openaq.jl:595

This is the regridding-model half of the pure-IO loader migration (RFC pure-io-data-loaders §6/§7, bead esm-3nc.5). The pre-migration openaq.esm carried both the coupler model AND a co-located data_loaders.OpenAQ_obs block (with the now-removed `spatial` and `regridding` sub-blocks). That loader became, at 0.7.0, the pure-I/O file components/earthsci_data/openaq_loader.esm, referenced as subsystem `obs`; at esm 1.0.0 it is the `OpenAQ_obs` entry in THIS file's `data_sources` and the standalone file is gone.

Upstream constructor OpenAQ(parameter, domaininfo; api_key, station_filter, fill_value=0.0, name=:OpenAQ, stream=true, spatial_interp=:linear) created an MTK System with:
  - @parameters: lon (rad), lat (rad) from domaininfo pvars (surface point observations: 2-D [x, y], no vertical level).
  - One observed equation via create_interp_equation(itp, "", t, t_ref, [x, y]; spatial_interp) where itp = DataSetInterpolator{dt}(FileSetWithRegridder(fs, copy_regridder), parameter, ...) and fs = OpenAQFileSet(parameter, starttime, endtime, bbox; grid_lon_edges, grid_lat_edges, ...). The variable name matches the parameter string (e.g. pm25(t)). These are now provided by the loader subsystem `obs` (obs.<var>); pm25 is re-exposed as a model observed (expression obs.pm25) to preserve the OpenAQ.pm25 coupling interface.
  - discrete_events: build_interp_event fires hourly to reload S3 data buffers (now seeded by the loader's `temporal` block → DISCRETE cadence, ess-v9a.5).
  - metadata: Dict(CoupleType => OpenAQCoupler, SysDomainInfo => domaininfo).

Data flow (upstream implementation, now performed by the runtime via the loader + cell-averaging regridder):
  1. Station discovery: OpenAQ API v3 /locations query, bbox-filtered, parameter-filtered, paginated; cached to $EARTHSCIDATADIR/openaq_stations/{parameter}_{bbox}.json.
  2. S3 download: asyncmap over (station, date) pairs; per-station daily CSV.gz cached to $EARTHSCIDATADIR/openaq_data/locationid=N/year=YYYY/month=MM/location-N-YYYYMMDD.csv.gz.
  3. loadslice!: for each hourly time step, reads daily CSV caches, filters by parameter column, averages readings within the hour per station, then averages across all stations in each grid cell (the cell-averaging regrid), applies unit_scale (to_unit(unit_string)).
  4. DataSetInterpolator + create_interp_equation: wraps the gridded hourly slices and produces the MTK observed equation.

gt-p3ep resolution: the @register_symbolic interp_unsafe pattern is replaced by the data_loaders §8 mechanism. obs.{parameter} is the loader variable that the runtime aggregates from station observations and provides as a gridded hourly field. The model observed is a direct pass-through: pm25(t) ~ obs.pm25.

Reprojection (RFC §6 step 2): OpenAQ's station coordinates are geographic (longlat/WGS84), so the reprojection rule selected by convention is ESD reprojection/longlat.esm (esd-47z.1) — the IDENTITY transform (a no-op). Because this is a `points` loader whose native point set is resolved at runtime (station discovery), the loader carries no formal GDD `grid`; the geographic crs is recorded in the loader's metadata.native_crs for provenance and convention selection.

Regridding (RFC §6 step 3 / §5.2): declared per variable in the model `regrid` block. All OpenAQ fields are scattered station observations → the cell_average kernel (ESD regridding/point_cell_average_regrid.esm, esd-47z.4): bin-average the stations falling within each target cell. `missing_value` 0.0 fills target cells that contain no station.

Note on missing_value (carried from the pre-migration data_loaders.regridding.fill_value = 0.0): the upstream constructor default fill_value is 0.0 (not NaN/missing) because DataSetInterpolator's BSpline propagates NaN to the entire field; grid cells with no stations receive 0.0. Upstream TODO comment: switch to NaN when BSpline handling is improved. The pre-migration `extrapolation: "clamp"` knob has no analogue in the cell-averaging kernel (empty cells are filled with missing_value rather than extrapolated) and is dropped.

Note on spatial_interp: :linear (default) uses full multilinear interpolation; :nearest uses nearest-grid + time-only linear interpolation (~8x speedup when queries are always at grid-point centres).

Supported parameters and their OpenAQ API IDs: pm25(2), pm10(1), o3(3), no2(5), so2(4), co(6), bc(11), pm1(19), no(7), nox(8). All report in µg/m³ (converted to kg/m³ by the loader's unit_conversion 1e-9).

Coordinate conventions:
  - lon/lat: radians; the runtime cell-averaging regridder converts to degrees to bin station coordinates into the target grid cells.
  - Surface observations: no lev parameter (2-D point data).

Coupler identity: this model was serialized with the model-level field `coupletype: "OpenAQCoupler"`, the EarthSciMLBase `CoupleType` metadata tag naming the Julia coupler struct that `EarthSciMLBase.couple2` dispatches on to find this component's pairwise coupling rules. The esm schema defined `coupletype` only before 0.8.0 ("informational label identifying this system's role in coupling"); 0.8.0 removed it in favour of explicit coupling — `coupling` entries naming components directly, or `coupling_roles` + `coupling_import` in a coupling-library file (esm-spec §10.9–§10.11). esm 1.0.0 has no model-level coupler-identity field, so the tag is recorded here to keep it recoverable.

Regridding intent: this model was serialized with the model-level `regrid` map, one entry per variable naming the kernel that carries the loaded native-grid field onto the consuming model's grid. The esm schema defined `regrid` only before 0.8.0. esm 1.0.0 states (esm-spec §8.6) that a data source performs no regridding and that there is NO `Model.regrid` map: the carrier is the `variable_map` entry's `transform` field on the coupling edge that consumes the field (§10.4/§10.5) — an ordinary `aggregate` expression, typically an `apply_expression_template` invocation of an imported overlap-weight library. No such coupling edge exists in this document, so the map is recorded here VERBATIM to keep every field recoverable. This is a demotion from a structured field to prose, not an equivalent: the transform expression still has to be authored on whichever coupling edge consumes these fields.

`regrid` (verbatim):
{
  "pm25": {
    "method": "cell_average",
    "missing_value": 0.0,
    "description": "PM2.5 concentration. Scattered station observations → cell-averaging regridder (ESD regridding/point_cell_average_regrid.esm, esd-47z.4): bin-average stations within each target cell. Target cells with no station are filled with missing_value 0.0 (carried from the pre-migration fill_value 0.0)."
  },
  "pm10": {
    "method": "cell_average",
    "missing_value": 0.0,
    "description": "PM10 concentration. Scattered station observations → cell-averaging regridder (esd-47z.4); empty target cells filled with missing_value 0.0."
  },
  "o3": {
    "method": "cell_average",
    "missing_value": 0.0,
    "description": "Ozone concentration. Scattered station observations → cell-averaging regridder (esd-47z.4); empty target cells filled with missing_value 0.0."
  },
  "no2": {
    "method": "cell_average",
    "missing_value": 0.0,
    "description": "Nitrogen dioxide concentration. Scattered station observations → cell-averaging regridder (esd-47z.4); empty target cells filled with missing_value 0.0."
  },
  "so2": {
    "method": "cell_average",
    "missing_value": 0.0,
    "description": "Sulfur dioxide concentration. Scattered station observations → cell-averaging regridder (esd-47z.4); empty target cells filled with missing_value 0.0."
  },
  "co": {
    "method": "cell_average",
    "missing_value": 0.0,
    "description": "Carbon monoxide concentration. Scattered station observations → cell-averaging regridder (esd-47z.4); empty target cells filled with missing_value 0.0."
  },
  "bc": {
    "method": "cell_average",
    "missing_value": 0.0,
    "description": "Black carbon concentration. Scattered station observations → cell-averaging regridder (esd-47z.4); empty target cells filled with missing_value 0.0."
  },
  "pm1": {
    "method": "cell_average",
    "missing_value": 0.0,
    "description": "PM1 concentration. Scattered station observations → cell-averaging regridder (esd-47z.4); empty target cells filled with missing_value 0.0."
  },
  "no": {
    "method": "cell_average",
    "missing_value": 0.0,
    "description": "Nitric oxide concentration. Scattered station observations → cell-averaging regridder (esd-47z.4); empty target cells filled with missing_value 0.0."
  },
  "nox": {
    "method": "cell_average",
    "missing_value": 0.0,
    "description": "Nitrogen oxides (NOx) concentration. Scattered station observations → cell-averaging regridder (esd-47z.4); empty target cells filled with missing_value 0.0."
  }
}_

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `lon` | `rad` | `0.0` | Longitude of the model grid point (radians). Coupled to the simulation domain's longitude coordinate via param_to_var when composed into a CoupledSystem. The runtime cell-averaging regridder converts radians to degrees to bin OpenAQ station coordinates into target grid cells. |
| `lat` | `rad` | `0.0` | Latitude of the model grid point (radians). Coupled to the simulation domain's latitude coordinate via param_to_var when composed into a CoupledSystem. The runtime cell-averaging regridder converts radians to degrees to bin OpenAQ station coordinates into target grid cells. |
| `pm25` | `kg/m^3` |  | Hourly-averaged PM2.5 concentration at the model grid point (kg/m³), aggregated from monitoring stations within the grid cell by the cell-averaging regridder and converted from µg/m³. Target cells with no stations receive missing_value (0.0; see `regrid`). Sourced from the loader field obs.pm25. Variable name matches the constructor parameter ('pm25' shown here as the representative case; other instantiations use the respective parameter name: pm10, o3, no2, so2, co, bc, pm1, no, nox — each available as obs.<var>). |
| `pm10` | `kg/m^3` |  | PM10 particulate matter concentration. Raw CSV 'value' column in µg/m³ (filtered where 'parameter' column == 'pm10'); converted to kg/m³. OpenAQ API parameter ID: 1. |
| `o3` | `kg/m^3` |  | Ozone concentration. Raw CSV 'value' column in µg/m³ (filtered where 'parameter' column == 'o3'); converted to kg/m³. OpenAQ API parameter ID: 3. |
| `no2` | `kg/m^3` |  | Nitrogen dioxide concentration. Raw CSV 'value' column in µg/m³ (filtered where 'parameter' column == 'no2'); converted to kg/m³. OpenAQ API parameter ID: 5. |
| `so2` | `kg/m^3` |  | Sulfur dioxide concentration. Raw CSV 'value' column in µg/m³ (filtered where 'parameter' column == 'so2'); converted to kg/m³. OpenAQ API parameter ID: 4. |
| `co` | `kg/m^3` |  | Carbon monoxide concentration. Raw CSV 'value' column in µg/m³ (filtered where 'parameter' column == 'co'); converted to kg/m³. OpenAQ API parameter ID: 6. |
| `bc` | `kg/m^3` |  | Black carbon concentration. Raw CSV 'value' column in µg/m³ (filtered where 'parameter' column == 'bc'); converted to kg/m³. OpenAQ API parameter ID: 11. |
| `pm1` | `kg/m^3` |  | PM1 particulate matter concentration. Raw CSV 'value' column in µg/m³ (filtered where 'parameter' column == 'pm1'); converted to kg/m³. OpenAQ API parameter ID: 19. |
| `no` | `kg/m^3` |  | Nitric oxide concentration. Raw CSV 'value' column in µg/m³ (filtered where 'parameter' column == 'no'); converted to kg/m³. OpenAQ API parameter ID: 7. |
| `nox` | `kg/m^3` |  | Nitrogen oxides (NOx) concentration. Raw CSV 'value' column in µg/m³ (filtered where 'parameter' column == 'nox'); converted to kg/m³. OpenAQ API parameter ID: 8. |

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "reference": {
    "notes": "source_ref: EarthSciData.jl@830435a065f27e99f10bba91107ca1730322cc6b:src/openaq.jl:595\n\nThis is the regridding-model half of the pure-IO loader migration (RFC pure-io-data-loaders §6/§7, bead esm-3nc.5). The pre-migration openaq.esm carried both the coupler model AND a co-located data_loaders.OpenAQ_obs block (with the now-removed `spatial` and `regridding` sub-blocks). That loader became, at 0.7.0, the pure-I/O file components/earthsci_data/openaq_loader.esm, referenced as subsystem `obs`; at esm 1.0.0 it is the `OpenAQ_obs` entry in THIS file's `data_sources` and the standalone file is gone.\n\nUpstream constructor OpenAQ(parameter, domaininfo; api_key, station_filter, fill_value=0.0, name=:OpenAQ, stream=true, spatial_interp=:linear) created an MTK System with:\n  - @parameters: lon (rad), lat (rad) from domaininfo pvars (surface point observations: 2-D [x, y], no vertical level).\n  - One observed equation via create_interp_equation(itp, \"\", t, t_ref, [x, y]; spatial_interp) where itp = DataSetInterpolator{dt}(FileSetWithRegridder(fs, copy_regridder), parameter, ...) and fs = OpenAQFileSet(parameter, starttime, endtime, bbox; grid_lon_edges, grid_lat_edges, ...). The variable name matches the parameter string (e.g. pm25(t)). These are now provided by the loader subsystem `obs` (obs.<var>); pm25 is re-exposed as a model observed (expression obs.pm25) to preserve the OpenAQ.pm25 coupling interface.\n  - discrete_events: build_interp_event fires hourly to reload S3 data buffers (now seeded by the loader's `temporal` block → DISCRETE cadence, ess-v9a.5).\n  - metadata: Dict(CoupleType => OpenAQCoupler, SysDomainInfo => domaininfo).\n\nData flow (upstream implementation, now performed by the runtime via the loader + cell-averaging regridder):\n  1. Station discovery: OpenAQ API v3 /locations query, bbox-filtered, parameter-filtered, paginated; cached to $EARTHSCIDATADIR/openaq_stations/{parameter}_{bbox}.json.\n  2. S3 download: asyncmap over (station, date) pairs; per-station daily CSV.gz cached to $EARTHSCIDATADIR/openaq_data/locationid=N/year=YYYY/month=MM/location-N-YYYYMMDD.csv.gz.\n  3. loadslice!: for each hourly time step, reads daily CSV caches, filters by parameter column, averages readings within the hour per station, then averages across all stations in each grid cell (the cell-averaging regrid), applies unit_scale (to_unit(unit_string)).\n  4. DataSetInterpolator + create_interp_equation: wraps the gridded hourly slices and produces the MTK observed equation.\n\ngt-p3ep resolution: the @register_symbolic interp_unsafe pattern is replaced by the data_loaders §8 mechanism. obs.{parameter} is the loader variable that the runtime aggregates from station observations and provides as a gridded hourly field. The model observed is a direct pass-through: pm25(t) ~ obs.pm25.\n\nReprojection (RFC §6 step 2): OpenAQ's station coordinates are geographic (longlat/WGS84), so the reprojection rule selected by convention is ESD reprojection/longlat.esm (esd-47z.1) — the IDENTITY transform (a no-op). Because this is a `points` loader whose native point set is resolved at runtime (station discovery), the loader carries no formal GDD `grid`; the geographic crs is recorded in the loader's metadata.native_crs for provenance and convention selection.\n\nRegridding (RFC §6 step 3 / §5.2): declared per variable in the model `regrid` block. All OpenAQ fields are scattered station observations → the cell_average kernel (ESD regridding/point_cell_average_regrid.esm, esd-47z.4): bin-average the stations falling within each target cell. `missing_value` 0.0 fills target cells that contain no station.\n\nNote on missing_value (carried from the pre-migration data_loaders.regridding.fill_value = 0.0): the upstream constructor default fill_value is 0.0 (not NaN/missing) because DataSetInterpolator's BSpline propagates NaN to the entire field; grid cells with no stations receive 0.0. Upstream TODO comment: switch to NaN when BSpline handling is improved. The pre-migration `extrapolation: \"clamp\"` knob has no analogue in the cell-averaging kernel (empty cells are filled with missing_value rather than extrapolated) and is dropped.\n\nNote on spatial_interp: :linear (default) uses full multilinear interpolation; :nearest uses nearest-grid + time-only linear interpolation (~8x speedup when queries are always at grid-point centres).\n\nSupported parameters and their OpenAQ API IDs: pm25(2), pm10(1), o3(3), no2(5), so2(4), co(6), bc(11), pm1(19), no(7), nox(8). All report in µg/m³ (converted to kg/m³ by the loader's unit_conversion 1e-9).\n\nCoordinate conventions:\n  - lon/lat: radians; the runtime cell-averaging regridder converts to degrees to bin station coordinates into the target grid cells.\n  - Surface observations: no lev parameter (2-D point data).\n\nCoupler identity: this model was serialized with the model-level field `coupletype: \"OpenAQCoupler\"`, the EarthSciMLBase `CoupleType` metadata tag naming the Julia coupler struct that `EarthSciMLBase.couple2` dispatches on to find this component's pairwise coupling rules. The esm schema defined `coupletype` only before 0.8.0 (\"informational label identifying this system's role in coupling\"); 0.8.0 removed it in favour of explicit coupling — `coupling` entries naming components directly, or `coupling_roles` + `coupling_import` in a coupling-library file (esm-spec §10.9–§10.11). esm 1.0.0 has no model-level coupler-identity field, so the tag is recorded here to keep it recoverable.\n\nRegridding intent: this model was serialized with the model-level `regrid` map, one entry per variable naming the kernel that carries the loaded native-grid field onto the consuming model's grid. The esm schema defined `regrid` only before 0.8.0. esm 1.0.0 states (esm-spec §8.6) that a data source performs no regridding and that there is NO `Model.regrid` map: the carrier is the `variable_map` entry's `transform` field on the coupling edge that consumes the field (§10.4/§10.5) — an ordinary `aggregate` expression, typically an `apply_expression_template` invocation of an imported overlap-weight library. No such coupling edge exists in this document, so the map is recorded here VERBATIM to keep every field recoverable. This is a demotion from a structured field to prose, not an equivalent: the transform expression still has to be authored on whichever coupling edge consumes these fields.\n\n`regrid` (verbatim):\n{\n  \"pm25\": {\n    \"method\": \"cell_average\",\n    \"missing_value\": 0.0,\n    \"description\": \"PM2.5 concentration. Scattered station observations → cell-averaging regridder (ESD regridding/point_cell_average_regrid.esm, esd-47z.4): bin-average stations within each target cell. Target cells with no station are filled with missing_value 0.0 (carried from the pre-migration fill_value 0.0).\"\n  },\n  \"pm10\": {\n    \"method\": \"cell_average\",\n    \"missing_value\": 0.0,\n    \"description\": \"PM10 concentration. Scattered station observations → cell-averaging regridder (esd-47z.4); empty target cells filled with missing_value 0.0.\"\n  },\n  \"o3\": {\n    \"method\": \"cell_average\",\n    \"missing_value\": 0.0,\n    \"description\": \"Ozone concentration. Scattered station observations → cell-averaging regridder (esd-47z.4); empty target cells filled with missing_value 0.0.\"\n  },\n  \"no2\": {\n    \"method\": \"cell_average\",\n    \"missing_value\": 0.0,\n    \"description\": \"Nitrogen dioxide concentration. Scattered station observations → cell-averaging regridder (esd-47z.4); empty target cells filled with missing_value 0.0.\"\n  },\n  \"so2\": {\n    \"method\": \"cell_average\",\n    \"missing_value\": 0.0,\n    \"description\": \"Sulfur dioxide concentration. Scattered station observations → cell-averaging regridder (esd-47z.4); empty target cells filled with missing_value 0.0.\"\n  },\n  \"co\": {\n    \"method\": \"cell_average\",\n    \"missing_value\": 0.0,\n    \"description\": \"Carbon monoxide concentration. Scattered station observations → cell-averaging regridder (esd-47z.4); empty target cells filled with missing_value 0.0.\"\n  },\n  \"bc\": {\n    \"method\": \"cell_average\",\n    \"missing_value\": 0.0,\n    \"description\": \"Black carbon concentration. Scattered station observations → cell-averaging regridder (esd-47z.4); empty target cells filled with missing_value 0.0.\"\n  },\n  \"pm1\": {\n    \"method\": \"cell_average\",\n    \"missing_value\": 0.0,\n    \"description\": \"PM1 concentration. Scattered station observations → cell-averaging regridder (esd-47z.4); empty target cells filled with missing_value 0.0.\"\n  },\n  \"no\": {\n    \"method\": \"cell_average\",\n    \"missing_value\": 0.0,\n    \"description\": \"Nitric oxide concentration. Scattered station observations → cell-averaging regridder (esd-47z.4); empty target cells filled with missing_value 0.0.\"\n  },\n  \"nox\": {\n    \"method\": \"cell_average\",\n    \"missing_value\": 0.0,\n    \"description\": \"Nitrogen oxides (NOx) concentration. Scattered station observations → cell-averaging regridder (esd-47z.4); empty target cells filled with missing_value 0.0.\"\n  }\n}"
  },
  "tolerance": {
    "rel": 1e-06
  },
  "variables": {
    "lon": {
      "type": "parameter",
      "units": "rad",
      "default": 0.0,
      "description": "Longitude of the model grid point (radians). Coupled to the simulation domain's longitude coordinate via param_to_var when composed into a CoupledSystem. The runtime cell-averaging regridder converts radians to degrees to bin OpenAQ station coordinates into target grid cells."
    },
    "lat": {
      "type": "parameter",
      "units": "rad",
      "default": 0.0,
      "description": "Latitude of the model grid point (radians). Coupled to the simulation domain's latitude coordinate via param_to_var when composed into a CoupledSystem. The runtime cell-averaging regridder converts radians to degrees to bin OpenAQ station coordinates into target grid cells."
    },
    "pm25": {
      "type": "parameter",
      "units": "kg/m^3",
      "description": "Hourly-averaged PM2.5 concentration at the model grid point (kg/m³), aggregated from monitoring stations within the grid cell by the cell-averaging regridder and converted from µg/m³. Target cells with no stations receive missing_value (0.0; see `regrid`). Sourced from the loader field obs.pm25. Variable name matches the constructor parameter ('pm25' shown here as the representative case; other instantiations use the respective parameter name: pm10, o3, no2, so2, co, bc, pm1, no, nox — each available as obs.<var>).",
      "update": {
        "kind": "data",
        "source": "OpenAQ_obs",
        "from": {
          "file_variable": "value",
          "description": "PM2.5 particulate matter concentration. Raw CSV 'value' column in µg/m³ (filtered where 'parameter' column == 'pm25'); converted to kg/m³ (1 µg/m³ = 1×10⁻⁹ kg/m³). OpenAQ API parameter ID: 2."
        }
      }
    },
    "pm10": {
      "type": "parameter",
      "units": "kg/m^3",
      "description": "PM10 particulate matter concentration. Raw CSV 'value' column in µg/m³ (filtered where 'parameter' column == 'pm10'); converted to kg/m³. OpenAQ API parameter ID: 1.",
      "update": {
        "kind": "data",
        "source": "OpenAQ_obs",
        "from": {
          "file_variable": "value",
          "description": "PM10 particulate matter concentration. Raw CSV 'value' column in µg/m³ (filtered where 'parameter' column == 'pm10'); converted to kg/m³. OpenAQ API parameter ID: 1."
        }
      }
    },
    "o3": {
      "type": "parameter",
      "units": "kg/m^3",
      "description": "Ozone concentration. Raw CSV 'value' column in µg/m³ (filtered where 'parameter' column == 'o3'); converted to kg/m³. OpenAQ API parameter ID: 3.",
      "update": {
        "kind": "data",
        "source": "OpenAQ_obs",
        "from": {
          "file_variable": "value",
          "description": "Ozone concentration. Raw CSV 'value' column in µg/m³ (filtered where 'parameter' column == 'o3'); converted to kg/m³. OpenAQ API parameter ID: 3."
        }
      }
    },
    "no2": {
      "type": "parameter",
      "units": "kg/m^3",
      "description": "Nitrogen dioxide concentration. Raw CSV 'value' column in µg/m³ (filtered where 'parameter' column == 'no2'); converted to kg/m³. OpenAQ API parameter ID: 5.",
      "update": {
        "kind": "data",
        "source": "OpenAQ_obs",
        "from": {
          "file_variable": "value",
          "description": "Nitrogen dioxide concentration. Raw CSV 'value' column in µg/m³ (filtered where 'parameter' column == 'no2'); converted to kg/m³. OpenAQ API parameter ID: 5."
        }
      }
    },
    "so2": {
      "type": "parameter",
      "units": "kg/m^3",
      "description": "Sulfur dioxide concentration. Raw CSV 'value' column in µg/m³ (filtered where 'parameter' column == 'so2'); converted to kg/m³. OpenAQ API parameter ID: 4.",
      "update": {
        "kind": "data",
        "source": "OpenAQ_obs",
        "from": {
          "file_variable": "value",
          "description": "Sulfur dioxide concentration. Raw CSV 'value' column in µg/m³ (filtered where 'parameter' column == 'so2'); converted to kg/m³. OpenAQ API parameter ID: 4."
        }
      }
    },
    "co": {
      "type": "parameter",
      "units": "kg/m^3",
      "description": "Carbon monoxide concentration. Raw CSV 'value' column in µg/m³ (filtered where 'parameter' column == 'co'); converted to kg/m³. OpenAQ API parameter ID: 6.",
      "update": {
        "kind": "data",
        "source": "OpenAQ_obs",
        "from": {
          "file_variable": "value",
          "description": "Carbon monoxide concentration. Raw CSV 'value' column in µg/m³ (filtered where 'parameter' column == 'co'); converted to kg/m³. OpenAQ API parameter ID: 6."
        }
      }
    },
    "bc": {
      "type": "parameter",
      "units": "kg/m^3",
      "description": "Black carbon concentration. Raw CSV 'value' column in µg/m³ (filtered where 'parameter' column == 'bc'); converted to kg/m³. OpenAQ API parameter ID: 11.",
      "update": {
        "kind": "data",
        "source": "OpenAQ_obs",
        "from": {
          "file_variable": "value",
          "description": "Black carbon concentration. Raw CSV 'value' column in µg/m³ (filtered where 'parameter' column == 'bc'); converted to kg/m³. OpenAQ API parameter ID: 11."
        }
      }
    },
    "pm1": {
      "type": "parameter",
      "units": "kg/m^3",
      "description": "PM1 particulate matter concentration. Raw CSV 'value' column in µg/m³ (filtered where 'parameter' column == 'pm1'); converted to kg/m³. OpenAQ API parameter ID: 19.",
      "update": {
        "kind": "data",
        "source": "OpenAQ_obs",
        "from": {
          "file_variable": "value",
          "description": "PM1 particulate matter concentration. Raw CSV 'value' column in µg/m³ (filtered where 'parameter' column == 'pm1'); converted to kg/m³. OpenAQ API parameter ID: 19."
        }
      }
    },
    "no": {
      "type": "parameter",
      "units": "kg/m^3",
      "description": "Nitric oxide concentration. Raw CSV 'value' column in µg/m³ (filtered where 'parameter' column == 'no'); converted to kg/m³. OpenAQ API parameter ID: 7.",
      "update": {
        "kind": "data",
        "source": "OpenAQ_obs",
        "from": {
          "file_variable": "value",
          "description": "Nitric oxide concentration. Raw CSV 'value' column in µg/m³ (filtered where 'parameter' column == 'no'); converted to kg/m³. OpenAQ API parameter ID: 7."
        }
      }
    },
    "nox": {
      "type": "parameter",
      "units": "kg/m^3",
      "description": "Nitrogen oxides (NOx) concentration. Raw CSV 'value' column in µg/m³ (filtered where 'parameter' column == 'nox'); converted to kg/m³. OpenAQ API parameter ID: 8.",
      "update": {
        "kind": "data",
        "source": "OpenAQ_obs",
        "from": {
          "file_variable": "value",
          "description": "Nitrogen oxides (NOx) concentration. Raw CSV 'value' column in µg/m³ (filtered where 'parameter' column == 'nox'); converted to kg/m³. OpenAQ API parameter ID: 8."
        }
      }
    }
  },
  "equations": [],
  "tests": []
}
```

</details>
