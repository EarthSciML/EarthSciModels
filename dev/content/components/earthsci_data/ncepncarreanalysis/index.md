---
title: "NCEPNCARReanalysis"
slug: "ncepncarreanalysis"
domains: ["earthsci_data"]
component_types: ["model"]
domain: "earthsci_data"
component_type: "model"
esm_version: "1.0.0"
esm_path: "components/earthsci_data/ncep_ncar.esm"
reference: "10.1175/1520-0477(1996)077<0437:TNYRP>2.0.CO;2"
description: "NCEP/NCAR Reanalysis 1 regridding model — the coupler half of the ncep_ncar loader+regridding-model split (RFC pure-io-data-loaders §6/§7; bead esm-3nc.2, esm-3nc.1 era5 pattern). Exposes 6-hourly pressure-level atmospheric variables (temperature, geopotential height, vertical velocity, horizontal winds) and static surface geopotential on the simulation's target grid."
tags: ["earthsci_data", "model", "meteorology", "reanalysis", "ncep", "ncar", "pressure_levels", "data_loader", "regridding_model", "longlat", "pure-io-split"]
---

## Description

NCEP/NCAR Reanalysis 1 regridding model — the coupler half of the ncep_ncar loader+regridding-model split (RFC pure-io-data-loaders §6/§7; bead esm-3nc.2, esm-3nc.1 era5 pattern). Exposes 6-hourly pressure-level atmospheric variables (temperature, geopotential height, vertical velocity, horizontal winds) and static surface geopotential on the simulation's target grid.

Structure (RFC §6): at 0.7.0 it declared two pure-I/O loaders as subsystems — NCEPNCAR_Pressure (./ncep_ncar_pressure_loader.esm, time-varying) and NCEPNCAR_Surface (./ncep_ncar_surface_loader.esm, static); at esm 1.0.0 both files are merged BACK into this one as the `data_sources` entries NCEPNCAR_Pressure and NCEPNCAR_Surface, keeping the SAME registry names, and their fields are re-exposed as model observeds (T, Z, omega, u, v, Z_sfc). Each merged file's own metadata is preserved verbatim under its registry entry's metadata.merged_file_metadata. Native grids are geographic (longlat/WGS84) → longlat identity reprojection (esd-47z.1). Regridding is per-variable (`regrid`): horizontal winds uwnd/vwnd → B-spline (esd-47z.3); centered scalars air/hgt/omega and the static hgt_sfc → conservative.

Data covers 1948–present at 2.5°×2.5° global resolution with 17 standard pressure levels (10–1000 hPa). Migrated from EarthSciData.jl src/NCEP-NCAR_Reanalysis.jl:224 (NCEPNCARReanalysis, esm-k3bb); split into pure loaders + regridding model by esm-3nc.2.

## Reference

_This is the regridding-model half of the pure-IO loader migration (RFC pure-io-data-loaders §6/§7; esm-3nc.1 era5 pattern, bead esm-3nc.2). The pre-migration ncep_ncar.esm carried the NCEPNCARReanalysis coupler model AND two co-located data_loaders blocks: NCEPNCAR_Pressure (grid, 6-hourly time-varying pressure-level fields) and NCEPNCAR_Surface (static surface geopotential). Both became, at 0.7.0, pure-I/O files referenced as subsystems under their ORIGINAL names (NCEPNCAR_Pressure → ./ncep_ncar_pressure_loader.esm, NCEPNCAR_Surface → ./ncep_ncar_surface_loader.esm). At esm 1.0.0 they are two `data_sources` entries in THIS file under those same names — a data source is not a component, so it neither needs nor may be a subsystem — and the observed expressions NCEPNCAR_Pressure.<var> and NCEPNCAR_Surface.hgt_sfc keep resolving unchanged. The removed co-located spatial/regridding sub-blocks become the loaders' GDD grid (longlat/WGS84) and the model's per-variable regrid.

Reprojection (RFC §6 step 2): both loaders' grid.crs.projection is 'longlat' (geographic WGS84), so the reprojection rule selected by convention is ESD reprojection/longlat.esm (esd-47z.1) — the IDENTITY transform.

Regridding (RFC §6 step 3 / §5.2): declared per variable in the model `regrid` block. The horizontal wind components uwnd, vwnd → B-spline interpolating regridder (ESD regridding/bspline_regrid.esm, esd-47z.3); the centered scalars air, hgt, omega (vertical-velocity scalar) and the static hgt_sfc → conservative area-weighted overlap join (ESD regridding/conservative_regrid_overlap_join.esm).

source_ref: EarthSciData.jl src/NCEP-NCAR_Reanalysis.jl:224

Upstream constructor NCEPNCARReanalysis(domaininfo; kwargs...) creates an MTK System with:
  - @parameters: lon (rad), lat (rad), lev (hPa)
  - One DataSetInterpolator per varnames(fileset): builds interp_unsafe equation for each NC variable
  - Equation template (from create_interp_equation, pressure-level variables):
      var(t) ~ interp_unsafe(data, fit, fi_lon, fi_lat, fi_lev, extrap)
    where fit  = 1 + (t_ref + t - tstart) / tstep
          fi_lon = 1 + (lon - lonstart) / lonstep
          fi_lat = 1 + (lat - latstart) / latstep
          fi_lev = 1 + (lev - levstart) / levstep
  - Surface variable (hgt.sfc.nc, static): fi_time argument omitted, read once
  - discrete_events: build_interp_event fires at 6-hourly tstops to reload pressure-level data buffers
  - metadata: Dict(CoupleType => NCEPNCARReanalysisCoupler, SysDomainInfo => domaininfo)

gt-p3ep resolution: the @register_symbolic interp_unsafe pattern is replaced by the data_loaders §8
mechanism. NCEPNCAR_Pressure.* variables are loader outputs regridded from the 2.5°×2.5°/17-level grid
to the model domain (lon, lat, lev) at each 6-hourly timestep. NCEPNCAR_Surface.hgt_sfc is the
static surface geopotential height, read once. The runtime handles the build_interp_event discrete
callbacks implicitly via data_loaders.temporal.frequency = PT6H.

Parameter units: lon and lat are in radians (matching EarthSciML convention for MTK integration;
the NCEP NC files store longitude in degrees, conversion handled by the runtime regridder).
lev is in hPa (matching the NCEP NC 'level' coordinate in millibars = hPa).

Coupler identity: this model was serialized with the model-level field `coupletype: "NCEPNCARReanalysisCoupler"`, the EarthSciMLBase `CoupleType` metadata tag naming the Julia coupler struct that `EarthSciMLBase.couple2` dispatches on to find this component's pairwise coupling rules. The esm schema defined `coupletype` only before 0.8.0 ("informational label identifying this system's role in coupling"); 0.8.0 removed it in favour of explicit coupling — `coupling` entries naming components directly, or `coupling_roles` + `coupling_import` in a coupling-library file (esm-spec §10.9–§10.11). esm 1.0.0 has no model-level coupler-identity field, so the tag is recorded here to keep it recoverable.

Regridding intent: this model was serialized with the model-level `regrid` map, one entry per variable naming the kernel that carries the loaded native-grid field onto the consuming model's grid. The esm schema defined `regrid` only before 0.8.0. esm 1.0.0 states (esm-spec §8.6) that a data source performs no regridding and that there is NO `Model.regrid` map: the carrier is the `variable_map` entry's `transform` field on the coupling edge that consumes the field (§10.4/§10.5) — an ordinary `aggregate` expression, typically an `apply_expression_template` invocation of an imported overlap-weight library. No such coupling edge exists in this document, so the map is recorded here VERBATIM to keep every field recoverable. This is a demotion from a structured field to prose, not an equivalent: the transform expression still has to be authored on whichever coupling edge consumes these fields.

`regrid` (verbatim):
{
  "air": {
    "method": "conservative",
    "description": "Air temperature (K). Cell-centered scalar → conservative area-weighted overlap-join regridder (ESD regridding/conservative_regrid_overlap_join.esm)."
  },
  "hgt": {
    "method": "conservative",
    "description": "Geopotential height (m). Cell-centered scalar → conservative regridder."
  },
  "omega": {
    "method": "conservative",
    "description": "Vertical velocity (Pa/s). A centered scalar (not a horizontal wind) → conservative regridder."
  },
  "uwnd": {
    "method": "bspline",
    "description": "Zonal wind component (m/s). Horizontal wind → B-spline interpolating regridder (ESD regridding/bspline_regrid.esm, esd-47z.3). Re-exposed as model observed u; coupled to MeanWind.v_lon."
  },
  "vwnd": {
    "method": "bspline",
    "description": "Meridional wind component (m/s). Horizontal wind → B-spline interpolating regridder (esd-47z.3). Re-exposed as model observed v; coupled to MeanWind.v_lat."
  },
  "hgt_sfc": {
    "method": "conservative",
    "description": "Static surface geopotential height (m). Cell-centered scalar → conservative regridder."
  }
}_

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `lon` | `rad` | `0.0` | Longitude of the grid point (radians). Coupled to the simulation domain's longitude coordinate via param_to_var when composed into a CoupledSystem. The runtime regridder converts radians to degrees for spatial interpolation against the NCEP 2.5°×2.5° grid. |
| `lat` | `rad` | `0.0` | Latitude of the grid point (radians). Coupled to the simulation domain's latitude coordinate via param_to_var when composed into a CoupledSystem. The runtime regridder converts radians to degrees for spatial interpolation. |
| `lev` | `hPa` | `500.0` | Pressure level (hPa). Corresponds to the 'level' coordinate in NCEP NC files. Standard levels: 1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 70, 50, 30, 20, 10 hPa. Coupled to the simulation domain's pressure coordinate via param_to_var when composed into a CoupledSystem. |
| `T` | `K` |  | Air temperature at the current grid point and pressure level (K). Interpolated in time (6-hourly), space (2.5°×2.5° → model domain), and pressure level from the NCEP/NCAR Reanalysis 1 'air' variable. |
| `Z` | `m` |  | Geopotential height at the current grid point and pressure level (m). Interpolated in time (6-hourly), space, and pressure level from the NCEP/NCAR Reanalysis 1 'hgt' variable. |
| `omega` | `Pa/s` |  | Lagrangian tendency of pressure (vertical velocity in pressure coordinates) at the current grid point and pressure level (Pa/s). Interpolated from the NCEP/NCAR Reanalysis 1 'omega' variable. |
| `u` | `m/s` |  | Zonal (west–east) wind component at the current grid point and pressure level (m/s). Interpolated from the NCEP/NCAR Reanalysis 1 'uwnd' variable. |
| `v` | `m/s` |  | Meridional (south–north) wind component at the current grid point and pressure level (m/s). Interpolated from the NCEP/NCAR Reanalysis 1 'vwnd' variable. |
| `Z_sfc` | `m` |  | Surface geopotential height (m). Static field read once from the NCEP/NCAR Reanalysis 1 'hgt.sfc.nc' file. Spatially interpolated to the model domain; does not vary in time or pressure level. |

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "reference": {
    "notes": "This is the regridding-model half of the pure-IO loader migration (RFC pure-io-data-loaders §6/§7; esm-3nc.1 era5 pattern, bead esm-3nc.2). The pre-migration ncep_ncar.esm carried the NCEPNCARReanalysis coupler model AND two co-located data_loaders blocks: NCEPNCAR_Pressure (grid, 6-hourly time-varying pressure-level fields) and NCEPNCAR_Surface (static surface geopotential). Both became, at 0.7.0, pure-I/O files referenced as subsystems under their ORIGINAL names (NCEPNCAR_Pressure → ./ncep_ncar_pressure_loader.esm, NCEPNCAR_Surface → ./ncep_ncar_surface_loader.esm). At esm 1.0.0 they are two `data_sources` entries in THIS file under those same names — a data source is not a component, so it neither needs nor may be a subsystem — and the observed expressions NCEPNCAR_Pressure.<var> and NCEPNCAR_Surface.hgt_sfc keep resolving unchanged. The removed co-located spatial/regridding sub-blocks become the loaders' GDD grid (longlat/WGS84) and the model's per-variable regrid.\n\nReprojection (RFC §6 step 2): both loaders' grid.crs.projection is 'longlat' (geographic WGS84), so the reprojection rule selected by convention is ESD reprojection/longlat.esm (esd-47z.1) — the IDENTITY transform.\n\nRegridding (RFC §6 step 3 / §5.2): declared per variable in the model `regrid` block. The horizontal wind components uwnd, vwnd → B-spline interpolating regridder (ESD regridding/bspline_regrid.esm, esd-47z.3); the centered scalars air, hgt, omega (vertical-velocity scalar) and the static hgt_sfc → conservative area-weighted overlap join (ESD regridding/conservative_regrid_overlap_join.esm).\n\nsource_ref: EarthSciData.jl src/NCEP-NCAR_Reanalysis.jl:224\n\nUpstream constructor NCEPNCARReanalysis(domaininfo; kwargs...) creates an MTK System with:\n  - @parameters: lon (rad), lat (rad), lev (hPa)\n  - One DataSetInterpolator per varnames(fileset): builds interp_unsafe equation for each NC variable\n  - Equation template (from create_interp_equation, pressure-level variables):\n      var(t) ~ interp_unsafe(data, fit, fi_lon, fi_lat, fi_lev, extrap)\n    where fit  = 1 + (t_ref + t - tstart) / tstep\n          fi_lon = 1 + (lon - lonstart) / lonstep\n          fi_lat = 1 + (lat - latstart) / latstep\n          fi_lev = 1 + (lev - levstart) / levstep\n  - Surface variable (hgt.sfc.nc, static): fi_time argument omitted, read once\n  - discrete_events: build_interp_event fires at 6-hourly tstops to reload pressure-level data buffers\n  - metadata: Dict(CoupleType => NCEPNCARReanalysisCoupler, SysDomainInfo => domaininfo)\n\ngt-p3ep resolution: the @register_symbolic interp_unsafe pattern is replaced by the data_loaders §8\nmechanism. NCEPNCAR_Pressure.* variables are loader outputs regridded from the 2.5°×2.5°/17-level grid\nto the model domain (lon, lat, lev) at each 6-hourly timestep. NCEPNCAR_Surface.hgt_sfc is the\nstatic surface geopotential height, read once. The runtime handles the build_interp_event discrete\ncallbacks implicitly via data_loaders.temporal.frequency = PT6H.\n\nParameter units: lon and lat are in radians (matching EarthSciML convention for MTK integration;\nthe NCEP NC files store longitude in degrees, conversion handled by the runtime regridder).\nlev is in hPa (matching the NCEP NC 'level' coordinate in millibars = hPa).\n\nCoupler identity: this model was serialized with the model-level field `coupletype: \"NCEPNCARReanalysisCoupler\"`, the EarthSciMLBase `CoupleType` metadata tag naming the Julia coupler struct that `EarthSciMLBase.couple2` dispatches on to find this component's pairwise coupling rules. The esm schema defined `coupletype` only before 0.8.0 (\"informational label identifying this system's role in coupling\"); 0.8.0 removed it in favour of explicit coupling — `coupling` entries naming components directly, or `coupling_roles` + `coupling_import` in a coupling-library file (esm-spec §10.9–§10.11). esm 1.0.0 has no model-level coupler-identity field, so the tag is recorded here to keep it recoverable.\n\nRegridding intent: this model was serialized with the model-level `regrid` map, one entry per variable naming the kernel that carries the loaded native-grid field onto the consuming model's grid. The esm schema defined `regrid` only before 0.8.0. esm 1.0.0 states (esm-spec §8.6) that a data source performs no regridding and that there is NO `Model.regrid` map: the carrier is the `variable_map` entry's `transform` field on the coupling edge that consumes the field (§10.4/§10.5) — an ordinary `aggregate` expression, typically an `apply_expression_template` invocation of an imported overlap-weight library. No such coupling edge exists in this document, so the map is recorded here VERBATIM to keep every field recoverable. This is a demotion from a structured field to prose, not an equivalent: the transform expression still has to be authored on whichever coupling edge consumes these fields.\n\n`regrid` (verbatim):\n{\n  \"air\": {\n    \"method\": \"conservative\",\n    \"description\": \"Air temperature (K). Cell-centered scalar → conservative area-weighted overlap-join regridder (ESD regridding/conservative_regrid_overlap_join.esm).\"\n  },\n  \"hgt\": {\n    \"method\": \"conservative\",\n    \"description\": \"Geopotential height (m). Cell-centered scalar → conservative regridder.\"\n  },\n  \"omega\": {\n    \"method\": \"conservative\",\n    \"description\": \"Vertical velocity (Pa/s). A centered scalar (not a horizontal wind) → conservative regridder.\"\n  },\n  \"uwnd\": {\n    \"method\": \"bspline\",\n    \"description\": \"Zonal wind component (m/s). Horizontal wind → B-spline interpolating regridder (ESD regridding/bspline_regrid.esm, esd-47z.3). Re-exposed as model observed u; coupled to MeanWind.v_lon.\"\n  },\n  \"vwnd\": {\n    \"method\": \"bspline\",\n    \"description\": \"Meridional wind component (m/s). Horizontal wind → B-spline interpolating regridder (esd-47z.3). Re-exposed as model observed v; coupled to MeanWind.v_lat.\"\n  },\n  \"hgt_sfc\": {\n    \"method\": \"conservative\",\n    \"description\": \"Static surface geopotential height (m). Cell-centered scalar → conservative regridder.\"\n  }\n}"
  },
  "tolerance": {
    "rel": 1e-06
  },
  "variables": {
    "lon": {
      "type": "parameter",
      "units": "rad",
      "default": 0.0,
      "description": "Longitude of the grid point (radians). Coupled to the simulation domain's longitude coordinate via param_to_var when composed into a CoupledSystem. The runtime regridder converts radians to degrees for spatial interpolation against the NCEP 2.5°×2.5° grid."
    },
    "lat": {
      "type": "parameter",
      "units": "rad",
      "default": 0.0,
      "description": "Latitude of the grid point (radians). Coupled to the simulation domain's latitude coordinate via param_to_var when composed into a CoupledSystem. The runtime regridder converts radians to degrees for spatial interpolation."
    },
    "lev": {
      "type": "parameter",
      "units": "hPa",
      "default": 500.0,
      "description": "Pressure level (hPa). Corresponds to the 'level' coordinate in NCEP NC files. Standard levels: 1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 70, 50, 30, 20, 10 hPa. Coupled to the simulation domain's pressure coordinate via param_to_var when composed into a CoupledSystem."
    },
    "T": {
      "type": "parameter",
      "units": "K",
      "description": "Air temperature at the current grid point and pressure level (K). Interpolated in time (6-hourly), space (2.5°×2.5° → model domain), and pressure level from the NCEP/NCAR Reanalysis 1 'air' variable.",
      "update": {
        "kind": "data",
        "source": "NCEPNCAR_Pressure",
        "from": {
          "file_variable": "air",
          "description": "Air temperature at pressure levels"
        }
      }
    },
    "Z": {
      "type": "parameter",
      "units": "m",
      "description": "Geopotential height at the current grid point and pressure level (m). Interpolated in time (6-hourly), space, and pressure level from the NCEP/NCAR Reanalysis 1 'hgt' variable.",
      "update": {
        "kind": "data",
        "source": "NCEPNCAR_Pressure",
        "from": {
          "file_variable": "hgt",
          "description": "Geopotential height at pressure levels"
        }
      }
    },
    "omega": {
      "type": "parameter",
      "units": "Pa/s",
      "description": "Lagrangian tendency of pressure (vertical velocity in pressure coordinates) at the current grid point and pressure level (Pa/s). Interpolated from the NCEP/NCAR Reanalysis 1 'omega' variable.",
      "update": {
        "kind": "data",
        "source": "NCEPNCAR_Pressure",
        "from": {
          "file_variable": "omega",
          "description": "Lagrangian tendency of pressure (vertical velocity in pressure coordinates)"
        }
      }
    },
    "u": {
      "type": "parameter",
      "units": "m/s",
      "description": "Zonal (west–east) wind component at the current grid point and pressure level (m/s). Interpolated from the NCEP/NCAR Reanalysis 1 'uwnd' variable.",
      "update": {
        "kind": "data",
        "source": "NCEPNCAR_Pressure",
        "from": {
          "file_variable": "uwnd",
          "description": "Zonal wind component (positive eastward)"
        }
      }
    },
    "v": {
      "type": "parameter",
      "units": "m/s",
      "description": "Meridional (south–north) wind component at the current grid point and pressure level (m/s). Interpolated from the NCEP/NCAR Reanalysis 1 'vwnd' variable.",
      "update": {
        "kind": "data",
        "source": "NCEPNCAR_Pressure",
        "from": {
          "file_variable": "vwnd",
          "description": "Meridional wind component (positive northward)"
        }
      }
    },
    "Z_sfc": {
      "type": "parameter",
      "units": "m",
      "description": "Surface geopotential height (m). Static field read once from the NCEP/NCAR Reanalysis 1 'hgt.sfc.nc' file. Spatially interpolated to the model domain; does not vary in time or pressure level.",
      "update": {
        "kind": "data",
        "source": "NCEPNCAR_Surface",
        "from": {
          "file_variable": "hgt",
          "description": "Surface geopotential height (static). Read from 'hgt.sfc.nc' on the NOAA PSL server. The variable name in the file is 'hgt'; the schema-level name 'hgt_sfc' distinguishes it from the pressure-level geopotential height in NCEPNCAR_Pressure."
        }
      }
    }
  },
  "equations": [],
  "tests": []
}
```

</details>
