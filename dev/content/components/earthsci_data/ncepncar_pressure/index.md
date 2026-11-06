---
title: "NCEPNCAR_Pressure"
slug: "ncepncar_pressure"
domains: ["earthsci_data"]
component_types: ["data_source"]
domain: "earthsci_data"
component_type: "data_source"
esm_version: "1.0.0"
esm_path: "components/earthsci_data/ncep_ncar.esm"
reference: "10.1175/1520-0477(1996)077<0437:TNYRP>2.0.CO;2"
description: "NCEP/NCAR Reanalysis 1 regridding model — the coupler half of the ncep_ncar loader+regridding-model split (RFC pure-io-data-loaders §6/§7; bead esm-3nc.2, esm-3nc.1 era5 pattern). Exposes 6-hourly pressure-level atmospheric variables (temperature, geopotential height, vertical velocity, horizontal winds) and static surface geopotential on the simulation's target grid."
tags: ["earthsci_data", "data_source", "meteorology", "reanalysis", "ncep", "ncar", "pressure_levels", "data_loader", "regridding_model", "longlat", "pure-io-split"]
---

## Description

NCEP/NCAR Reanalysis 1 regridding model — the coupler half of the ncep_ncar loader+regridding-model split (RFC pure-io-data-loaders §6/§7; bead esm-3nc.2, esm-3nc.1 era5 pattern). Exposes 6-hourly pressure-level atmospheric variables (temperature, geopotential height, vertical velocity, horizontal winds) and static surface geopotential on the simulation's target grid.

Structure (RFC §6): at 0.7.0 it declared two pure-I/O loaders as subsystems — NCEPNCAR_Pressure (./ncep_ncar_pressure_loader.esm, time-varying) and NCEPNCAR_Surface (./ncep_ncar_surface_loader.esm, static); at esm 1.0.0 both files are merged BACK into this one as the `data_sources` entries NCEPNCAR_Pressure and NCEPNCAR_Surface, keeping the SAME registry names, and their fields are re-exposed as model observeds (T, Z, omega, u, v, Z_sfc). Each merged file's own metadata is preserved verbatim under its registry entry's metadata.merged_file_metadata. Native grids are geographic (longlat/WGS84) → longlat identity reprojection (esd-47z.1). Regridding is per-variable (`regrid`): horizontal winds uwnd/vwnd → B-spline (esd-47z.3); centered scalars air/hgt/omega and the static hgt_sfc → conservative.

Data covers 1948–present at 2.5°×2.5° global resolution with 17 standard pressure levels (10–1000 hPa). Migrated from EarthSciData.jl src/NCEP-NCAR_Reanalysis.jl:224 (NCEPNCARReanalysis, esm-k3bb); split into pure loaders + regridding model by esm-3nc.2.

## Reference

Kalnay, E. et al. (1996). The NCEP/NCAR 40-year reanalysis project. Bull. Amer. Meteor. Soc. 77, 437–471.
- **DOI**: 10.1175/1520-0477(1996)077<0437:TNYRP>2.0.CO;2
- **URL**: https://psl.noaa.gov/data/gridded/data.ncep.reanalysis.html

## Data source

| | |
| --- | --- |
| Kind | `grid` |
| URL template | `https://downloads.psl.noaa.gov/Datasets/ncep.reanalysis/pressure/{var}.{date:%Y}.nc` |
| Coverage | 1948-01-01T00:00:00Z |
| File period | `P1Y` |
| Sample frequency | `PT6H` |
| Records per file | 1460 |

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "kind": "grid",
  "source": {
    "url_template": "https://downloads.psl.noaa.gov/Datasets/ncep.reanalysis/pressure/{var}.{date:%Y}.nc"
  },
  "temporal": {
    "start": "1948-01-01T00:00:00Z",
    "file_period": "P1Y",
    "frequency": "PT6H",
    "records_per_file": 1460,
    "time_variable": "time"
  },
  "reference": {
    "citation": "Kalnay, E. et al. (1996). The NCEP/NCAR 40-year reanalysis project. Bull. Amer. Meteor. Soc. 77, 437–471.",
    "url": "https://psl.noaa.gov/data/gridded/data.ncep.reanalysis.html",
    "doi": "10.1175/1520-0477(1996)077<0437:TNYRP>2.0.CO;2"
  },
  "metadata": {
    "tags": [
      "meteorology",
      "reanalysis",
      "pressure-level",
      "6-hourly",
      "ncep",
      "ncar"
    ],
    "earthscidata_source": "src/NCEP-NCAR_Reanalysis.jl::NCEPNCARReanalysisFileSet (pressure variables)",
    "pressure_levels_hPa": [
      1000,
      925,
      850,
      700,
      600,
      500,
      400,
      300,
      250,
      200,
      150,
      100,
      70,
      50,
      30,
      20,
      10
    ],
    "unit_note": "NCEP NC files store air temperature with scale_factor/add_offset packed encoding; earthsci_ast applies CF conventions to decode to physical units (K). omega raw units in the file are Pa/s; no conversion needed.",
    "native_resolution_deg": {
      "longitude": 2.5,
      "latitude": 2.5
    },
    "native_extent": {
      "longitude": [
        -180.0,
        180.0
      ],
      "latitude": [
        -90.0,
        90.0
      ],
      "pressure_level_hpa": [
        10.0,
        1000.0
      ]
    },
    "regridding_provenance": "Former co-located data_loaders.regridding block (fill_value=0.0, extrapolation=clamp) removed in the 0.6.0 hard break; at 0.7.0 regridding became a per-variable model `regrid` map; 0.8.0 removed that too — the kernel is now a coupling expression (esm-spec §8.6), and ncep_ncar.esm keeps the per-variable choice verbatim in Model.reference.notes.",
    "native_grid_family": "cartesian",
    "native_crs_epsg": "EPSG:4326 (geographic longlat / WGS84). At esm 0.8.0 the crs is documentation only — a data source no longer carries a `grid`/crs descriptor; the longlat identity reprojection is applied at the coupling edge via ESD reprojection/longlat.esm (esd-47z.1).",
    "native_crs_descriptor": {
      "projection": "longlat",
      "datum": "WGS84"
    },
    "native_dimensions": [
      "lon",
      "lat",
      "level"
    ],
    "native_dimension_extents": {
      "lon": {
        "n": 144,
        "spacing": "uniform"
      },
      "lat": {
        "n": 72,
        "spacing": "uniform"
      },
      "level": {
        "n": 17,
        "spacing": "nonuniform"
      }
    },
    "native_staggering": "Not stated by the former `grid` block, which recorded family/crs/dimensions/extents only — no staggering field was ever serialized for this source, so none is asserted here. The only staggering-adjacent statement in the corpus is ncep_ncar.esm's demoted `regrid` map, which describes air/hgt/omega/hgt_sfc as centered scalars carried by a conservative kernel and uwnd/vwnd as horizontal winds carried by a B-spline kernel. At esm 0.8.0 that kernel choice is a coupling expression, not a model `regrid` block.",
    "native_grid_description": "Native NCEP/NCAR Reanalysis 1 grid: regular global 2.5°×2.5° longitude/latitude lattice on 17 standard pressure levels (1000, 925, 850, 700, 600, 500, 400, 300, 250, 200, 150, 100, 70, 50, 30, 20, 10 hPa — non-uniform vertical spacing). Geographic (unprojected) longlat/WGS84 crs — the regridding model applies the longlat IDENTITY reprojection (ESD reprojection/longlat.esm, esd-47z.1). Migrated from the loader's former DataLoaderSpatial block (RFC pure-io-data-loaders §4.1). Dimension cell counts resolve from the source dataset at load time; documented native geometry: lon ∈ [-180°,180°] (144 cells, 2.5°), lat ∈ [-90°,90°] (72 cells, 2.5°), level = 17 pressure surfaces.",
    "migration_note": "esm 0.7.0 -> 0.8.0: removed the `grid` block (family/crs/dimensions/extents/description), which no schema at or after 0.8.0 permits — 0.8.0 deleted the native-grid descriptor outright (esm-spec §8.4; the 1.0.0 DataSource is additionalProperties:false over {kind, source, temporal, determinism, reader_options, select, record_filter, extent, reference, metadata}, with no `grid` key). Nothing was dropped: `family` → native_grid_family; `crs` → native_crs_epsg + native_crs_descriptor (verbatim); `dimensions` → native_dimensions; `extents` (per-dimension cell count + spacing) → native_dimension_extents; `description` → native_grid_description (verbatim). Native grid geometry is now ordinary data — a source exposes its coordinates/connectivity/metric arrays as ordinary `file_variable`s bound to consuming parameters, and reprojection/regridding are ordinary `aggregate` coupling expressions (esm-spec §8.6), not a loader `grid` or a model `regrid` block. No other field changed.",
    "merged_from": "components/earthsci_data/ncep_ncar_pressure_loader.esm",
    "merge_note": "Merged from the standalone pure-I/O file components/earthsci_data/ncep_ncar_pressure_loader.esm, which is deleted by the same commit. The 0.x `X.esm` + `X_loader.esm` split existed only because a loader was a COMPONENT and a {\"ref\"} target had to contain exactly one component. At esm 1.0.0 a data source is NOT a component, not a coupling endpoint and not a scoped-name path root, and `data_sources` no longer counts toward a file's top-level system count — so one file may hold a model AND the data_sources that model consumes and still be mountable by {\"ref\"}. This registry entry is byte-identical to the one the deleted file declared (it was already mirrored here so this document would validate), and the deleted file's own top-level metadata — name, description, tags, created, authors, references — is preserved verbatim in `merged_file_metadata` so no provenance, citation or migration note is lost.",
    "merged_file_metadata": {
      "name": "NCEPNCAR_Pressure_loader",
      "description": "Pure-I/O data loader for NCEP/NCAR Reanalysis 1 pressure-level fields (6-hourly air temperature, geopotential height, vertical velocity, and horizontal winds) on the native 2.5°×2.5° global longitude/latitude grid with 17 standard pressure levels, from NOAA PSL.\n\nThis is the time-varying loader half of the ncep_ncar loader+regridding-model split (RFC pure-io-data-loaders §4.1/§7; bead esm-3nc.2, esm-3nc.1 era5 pattern). It is PURE I/O: source, file variables (with units), and temporal cadence (6-hourly). It declares NO grid: esm 0.8.0 removed the loader `grid`/GDD-Grid descriptor outright, so the native 2.5°×2.5° longlat/WGS84 lattice and its 17 pressure levels are recorded as documentation in the data source's metadata and are materialized downstream by `aggregate` coupling expressions. It performs NO reprojection and NO regridding — those are per-variable concerns of the regridding model (components/earthsci_data/ncep_ncar.esm), which references this file as the subsystem NCEPNCAR_Pressure via {\"ref\": \"./ncep_ncar_pressure_loader.esm\"}.\n\nThe removed co-located blocks: the old DataLoaderSpatial block (proj4 crs / grid_type / staggering / resolution / extent) became the GDD `grid` at 0.7.0 and, at 0.8.0, metadata documentation (see metadata.migration_note on the data source); the old per-loader `regridding` block (fill_value / extrapolation) is gone, and so is the model-level `regrid` map — at 0.8.0 the regridding kernel is a coupling expression, and ncep_ncar.esm keeps the per-variable kernel choice verbatim in Model.reference.notes. Because a `temporal` block is present, this loader seeds DISCRETE cadence (ess-v9a.5): the runtime refreshes the file buffers 6-hourly.\n\nMigrated from EarthSciData.jl src/NCEP-NCAR_Reanalysis.jl (NCEPNCARReanalysisFileSet, pressure variables). Split out of the pre-migration components/earthsci_data/ncep_ncar.esm (esm-k3bb).",
      "tags": [
        "earthsci_data",
        "meteorology",
        "reanalysis",
        "ncep",
        "ncar",
        "pressure_levels",
        "data_loader",
        "pure-io",
        "longlat"
      ],
      "created": "2026-06-25T00:00:00Z",
      "authors": [
        "NOAA NCEP",
        "NCAR",
        "EarthSciModels migration (esm-3nc.2)"
      ],
      "references": [
        {
          "citation": "Kalnay, E., Kanamitsu, M., Kistler, R., Collins, W., Deaven, D., Gandin, L., Iredell, M., Saha, S., White, G., Woollen, J., Zhu, Y., Leetmaa, A., Reynolds, R., Chelliah, M., Ebisuzaki, W., Higgins, W., Janowiak, J., Mo, K. C., Ropelewski, C., Wang, J., Jenne, R., Joseph, D. (1996). The NCEP/NCAR 40-year reanalysis project. Bulletin of the American Meteorological Society, 77(3), 437–471.",
          "url": "https://psl.noaa.gov/data/gridded/data.ncep.reanalysis.html",
          "doi": "10.1175/1520-0477(1996)077<0437:TNYRP>2.0.CO;2"
        },
        {
          "citation": "Source: EarthSciData.jl src/NCEP-NCAR_Reanalysis.jl:4-66 (NCEPNCARReanalysisFileSet), :72-79 (relpath), :224 (NCEPNCARReanalysis constructor). Test: test/NCEP-NCAR_Reanalysis_test.jl."
        }
      ]
    }
  }
}
```

</details>
