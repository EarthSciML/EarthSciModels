---
title: "GEOSFP_A3mstE"
slug: "geosfp_a3mste"
domains: ["earthsci_data"]
component_types: ["data_source"]
domain: "earthsci_data"
component_type: "data_source"
esm_version: "1.0.0"
esm_path: "components/earthsci_data/geosfp.esm"
reference: "http://geoschemdata.wustl.edu/ExtData/"
description: "GEOS-FP regridding model — the coupler half of the geosfp loader+regridding-model split (RFC pure-io-data-loaders §6/§7; bead esm-3nc.2, following the esm-3nc.1 era5/wrf pattern). Exposes NASA GMAO GEOS-FP assimilated meteorology (0.25°×0.3125° global, GEOS-Chem 72-level) on the simulation's target grid for coupling into EarthSciML systems."
tags: ["earthsci_data", "data_source", "meteorology", "atmospheric_dynamics", "data_loader", "geos_fp", "global", "hybrid_pressure", "geos_chem", "nasa", "regridding_model", "longlat", "pure-io-split"]
---

## Description

GEOS-FP regridding model — the coupler half of the geosfp loader+regridding-model split (RFC pure-io-data-loaders §6/§7; bead esm-3nc.2, following the esm-3nc.1 era5/wrf pattern). Exposes NASA GMAO GEOS-FP assimilated meteorology (0.25°×0.3125° global, GEOS-Chem 72-level) on the simulation's target grid for coupling into EarthSciML systems.

Structure (RFC §6): at 0.7.0 it declared the six pure-I/O GEOS-FP grid loaders as subsystems under their original names (GEOSFP_A1/A3cld/A3dyn/A3mstC/A3mstE/I3 → ./geosfp_<coll>_loader.esm); at esm 1.0.0 those six files are merged BACK into this one as the `data_sources` entries GEOSFP_A1 … GEOSFP_I3, keeping the SAME registry names, so fields are still referenced as GEOSFP.<coll>.<var> and re-exposed as model observeds (GEOSFP.T, GEOSFP.U, …). Each merged file's own metadata is preserved verbatim under its registry entry's metadata.merged_file_metadata. Native grids are geographic (longlat/WGS84) → longlat identity reprojection (esd-47z.1). Regridding is per-variable (`regrid`): A3dyn staggered winds U/V/OMEGA → B-spline (esd-47z.3); all other fields → conservative. The hybrid sigma-pressure Ap/Bp tables (former GEOSFP_hybrid_coefs kind:lookup, removed in the 0.6.0 hard break) are now the top-level function_tables geosfp_Ap_pa and geosfp_Bp, consumed by P = Ap(lev)+Bp(lev)·PS.

Derived observeds on the target grid: pressure P, virtual temperature Tv and Tv_sfc, layer-mean virtual temperature Tv_bar, and the lat/lon coordinate metrics δxδlon, δyδlat. MeanWind coupling: GEOSFP.U/V/OMEGA → MeanWind v_lon/v_lat/v_lev.

Migrated from EarthSciData.jl@830435a065f27e99f10bba91107ca1730322cc6b:src/geosfp.jl:410 (GEOSFP constructor, esm-1c6s); split into pure loaders + regridding model by esm-3nc.2.

## Reference

GEOS-FP A3mstE collection. NASA GMAO.
- **URL**: http://geoschemdata.wustl.edu/ExtData/

## Data source

| | |
| --- | --- |
| Kind | `grid` |
| URL template | `https://geos-chem.s3-us-west-2.amazonaws.com/GEOS_0.25x0.3125/GEOS_FP/{date:%Y}/{date:%m}/GEOSFP.{date:%Y%m%d}.A3mstE.025x03125.nc` |
| Coverage | 2013-01-01T01:30:00Z |
| File period | `P1D` |
| Sample frequency | `PT3H` |
| Records per file | 8 |

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "kind": "grid",
  "source": {
    "url_template": "https://geos-chem.s3-us-west-2.amazonaws.com/GEOS_0.25x0.3125/GEOS_FP/{date:%Y}/{date:%m}/GEOSFP.{date:%Y%m%d}.A3mstE.025x03125.nc"
  },
  "temporal": {
    "start": "2013-01-01T01:30:00Z",
    "file_period": "P1D",
    "frequency": "PT3H",
    "records_per_file": 8,
    "time_variable": "time"
  },
  "reference": {
    "citation": "GEOS-FP A3mstE collection. NASA GMAO.",
    "url": "http://geoschemdata.wustl.edu/ExtData/"
  },
  "metadata": {
    "esio_format": "netcdf",
    "tags": [
      "geos_fp",
      "moisture",
      "precipitation",
      "3-hourly",
      "3d"
    ],
    "earthscidata_source": "src/geosfp.jl::GEOSFPFileSet (filetype=A3mstE)",
    "filetype": "A3mstE",
    "domain": "0.25x0.3125",
    "time_center_note": "A3mstE record times are centered: 01:30, 04:30, ..., 22:30 UTC (Delta_Time=030000).",
    "native_resolution_deg": {
      "longitude": 0.3125,
      "latitude": 0.25
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
      "lev_edge_index": [
        1,
        73
      ]
    },
    "regridding_provenance": "Former co-located data_loaders.regridding block (fill_value=0.0, extrapolation=clamp) removed in the 0.6.0 hard break; regridding is now declared per-variable on the GEOSFP model `regrid` (RFC pure-io-data-loaders §4.1/§5.2).",
    "crs_provenance": "Former DataLoaderSpatial.crs '+proj=longlat +datum=WGS84 +no_defs' is now the structured GDD grid.crs {projection: longlat, datum: WGS84}.",
    "merged_from": "components/earthsci_data/geosfp_a3mste_loader.esm",
    "merge_note": "Merged from the standalone pure-I/O file components/earthsci_data/geosfp_a3mste_loader.esm, which is deleted by the same commit. The 0.x `X.esm` + `X_loader.esm` split existed only because a loader was a COMPONENT and a {\"ref\"} target had to contain exactly one component. At esm 1.0.0 a data source is NOT a component, not a coupling endpoint and not a scoped-name path root, and `data_sources` no longer counts toward a file's top-level system count — so one file may hold a model AND the data_sources that model consumes and still be mountable by {\"ref\"}. This registry entry is byte-identical to the one the deleted file declared (it was already mirrored here so this document would validate), and the deleted file's own top-level metadata — name, description, tags, created, authors, references — is preserved verbatim in `merged_file_metadata` so no provenance, citation or migration note is lost.",
    "merged_file_metadata": {
      "name": "GEOSFP_A3mstE_loader",
      "description": "Pure-I/O data loader for GEOS-FP (A3MSTE collection): 3-hourly time-averaged 3-D moist fields on layer edges on the native 0.3125°×0.25° global longitude/latitude grid, from the GEOS-Chem GEOS_FP 0.25x0.3125 archive.\n\nThis is one loader half of the geosfp loader+regridding-model split (RFC pure-io-data-loaders §4.1/§7; bead esm-3nc.2, following the esm-3nc.1 era5/wrf pattern). It is PURE I/O: it declares its source (url_template), the file variables it reads (with units), its temporal cadence, and its NATIVE grid expressed as a GDD Grid with a geographic (longlat/WGS84) crs descriptor. It performs NO reprojection and NO regridding — those are per-variable concerns of the regridding model (components/earthsci_data/geosfp.esm), which references this file as a subsystem via {\"ref\": \"./geosfp_a3mste_loader.esm\"} under the subsystem key GEOSFP_A3mstE.\n\nThe removed co-located blocks: the old DataLoaderSpatial block (proj4 crs string / grid_type / staggering / resolution / extent) is replaced by the GDD `grid` (family + crs + dimensions + extents); the old per-loader `regridding` block (fill_value / extrapolation) is gone — regridding is declared per-variable on the model (geosfp.esm `regrid`). Because a `temporal` block is present, this loader seeds DISCRETE cadence (ess-v9a.5): the runtime refreshes the file buffers on its update schedule.\n\nMigrated from EarthSciData.jl@830435a065f27e99f10bba91107ca1730322cc6b:src/geosfp.jl (GEOSFPFileSet, filetype=A3MSTE). Split out of the pre-migration components/earthsci_data/geosfp.esm (esm-1c6s).",
      "tags": [
        "earthsci_data",
        "meteorology",
        "geos_fp",
        "global",
        "data_loader",
        "pure-io",
        "longlat"
      ],
      "created": "2026-06-25T00:00:00Z",
      "authors": [
        "NASA GMAO / GEOS-Chem",
        "EarthSciModels migration (esm-3nc.2)"
      ],
      "references": [
        {
          "citation": "GEOS-FP data archived for GEOS-Chem classic. NASA Global Modeling and Assimilation Office (GMAO). AWS S3 mirror: s3://geos-chem/GEOS_{domain}/GEOS_FP/. See http://geoschemdata.wustl.edu/ExtData/ for current domain and file-type options.",
          "url": "http://geoschemdata.wustl.edu/ExtData/"
        },
        {
          "citation": "Molod, A., Takacs, L., Suarez, M., and Bacmeister, J. (2015). Development of the GEOS-5 atmospheric general circulation model: evolution from MERRA to MERRA2. Geosci. Model Dev., 8, 1339–1356.",
          "doi": "10.5194/gmd-8-1339-2015"
        },
        {
          "citation": "GEOS-Chem vertical grid documentation: https://wiki.seas.harvard.edu/geos-chem/index.php/GEOS-Chem_vertical_grids",
          "url": "https://wiki.seas.harvard.edu/geos-chem/index.php/GEOS-Chem_vertical_grids"
        },
        {
          "citation": "Source: EarthSciData.jl@830435a065f27e99f10bba91107ca1730322cc6b:src/geosfp.jl (GEOSFPFileSet, GEOSFP constructor, Ap/Bp hybrid grid coefficients, geosfp_staggering). Test: test/geosfp_test.jl. Docs: docs present in pinned commit."
        }
      ]
    },
    "vertical_note": "A3mstE fields live on the 73 level EDGES (interfaces) of the 72-layer GEOS-FP grid, not on layer centres, so their lev axis has 73 entries where A3cld/A3dyn/A3mstC/I3 have 72. In the GEOS-Chem-processed files edge 1 is the surface and edge 73 the model top (~1 Pa), the same surface-first order as the layer collections: edge k is the BOTTOM edge of layer k and edge k+1 its top. Checked on GEOSFP.20160502.A3mstE.4x5.nc: PFLCU/PFLLSAN are largest at edge 1 and exactly 0 at edge 73; I3 T and QV are warmest/wettest at layer 1. GEOS-Chem itself allocates these fields with NZ+1 levels (state_met_mod onEdges=.TRUE.); its convective scavenging reads edges 1..NZ and its default large-scale scheme reads edge L+1 for layer L (wetscav_mod MAKE_QQ)."
  }
}
```

</details>
