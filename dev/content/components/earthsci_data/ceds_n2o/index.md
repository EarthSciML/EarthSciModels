---
title: "CEDS_N2O"
slug: "ceds_n2o"
domains: ["earthsci_data"]
component_types: ["data_source"]
domain: "earthsci_data"
component_type: "data_source"
esm_version: "1.0.0"
esm_path: "components/earthsci_data/ceds.esm"
reference: "https://doi.org/10.5194/gmd-11-369-2018"
description: "CEDS (Community Emissions Data System) global gridded anthropogenic emissions data loader. Provides monthly surface emission fluxes (kg m⁻² s⁻¹) at 0.5° × 0.5° global resolution for 10 species: BC, CH4, CO, CO2, N2O, NH3, NMVOC, NOx, OC, SO2."
tags: ["earthsci_data", "data_source", "emissions", "anthropogenic", "ceds", "monthly", "data_loader", "surface_flux", "global", "multi_species", "regridding_model"]
---

## Description

CEDS (Community Emissions Data System) global gridded anthropogenic emissions data loader. Provides monthly surface emission fluxes (kg m⁻² s⁻¹) at 0.5° × 0.5° global resolution for 10 species: BC, CH4, CO, CO2, N2O, NH3, NMVOC, NOx, OC, SO2.

Data source: CEDS-CMIP release v20250421 (CEDS-CMIP-2025-04-18), available from the ORNL ESGF THREDDS server. Files are NetCDF with dimensions (time, sector, lat, lon) and variable name {species}_em_anthro. The sector dimension has 8 entries (Agriculture, Energy, Industrial, Transportation, Residential/Commercial/Other, Solvents, Waste, International Shipping); the data_loaders emit sector-summed total anthropogenic flux.

Temporal coverage: 1750–2023, monthly. Data is organized in 50-year file chunks: 1750-1799, 1800-1849, 1850-1899, 1900-1949, 1950-1999, and 2000-2023. This ESM documents the modern-era chunk (2000-2023) as the primary temporal range. For simulations outside 2000-2023, different chunk file URLs are required (see reference.notes).

The gt-p3ep (@register_symbolic interp_unsafe) blocking gap is resolved by the data_loaders §8 mechanism: the runtime handles file download, sector-summing, temporal interpolation, and spatial regridding from the native 0.5°×0.5° lat/lon grid to the model domain. Each species equation is a direct pass-through: {species}_em_anthro(t) ~ CEDS_{species}.{species}_em_anthro. No registered functions remain in the migrated component.

Longitude convention: the raw CEDS NC files use [0, 360) longitude. The upstream loadslice! reorders to [−180, 180) via a permutation vector computed at FileSet construction time. This ESM documents the reordered [−180, 180) coordinate as the effective spatial extent.

Coupling: lon and lat parameters are coupled to the simulation domain via param_to_var when composed into a CoupledSystem. Unlike EDGAR, CEDS has no lev parameter (surface-only flux).

Migrated from EarthSciData.jl@830435a065f27e99f10bba91107ca1730322cc6b src/ceds.jl:313 (CEDS constructor, esm-4ega).

[esm-3nc.3] Split at 0.7.0 into ten pure-I/O species loaders (ceds_<species>_loader.esm) + this regridding model per RFC pure-io-data-loaders §6/§7; at esm 1.0.0 those ten files are merged BACK into this one, which now holds both the CEDS model and the ten `data_sources` entries (CEDS_BC … CEDS_SO2) that model consumes. Each merged file's own metadata is preserved verbatim under its registry entry's metadata.merged_file_metadata. Each loader is referenced as the subsystem CEDS_<species>; every species flux is regridded conservatively (cell-centered emissions).

## Reference

Hoesly et al. (2018). Historical (1750–2014) anthropogenic emissions from CEDS. GMD 11, 369–408.
- **URL**: https://doi.org/10.5194/gmd-11-369-2018

## Data source

| | |
| --- | --- |
| Kind | `grid` |
| URL template | `https://esgf-node.ornl.gov/thredds/fileServer/user_pub_work/input4MIPs/CMIP7/CMIP/PNNL-JGCRI/CEDS-CMIP-2025-04-18/atmos/mon/N2O_em_anthro/gn/v20250421/N2O-em-anthro_input4MIPs_emissions_CMIP_CEDS-CMIP-2025-04-18_gn_200001-202312.nc` |
| Coverage | 2000-01-01T00:00:00Z → 2023-12-31T23:59:59Z |
| File period | `P1Y` |
| Sample frequency | `P1M` |
| Records per file | 12 |

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "kind": "grid",
  "source": {
    "url_template": "https://esgf-node.ornl.gov/thredds/fileServer/user_pub_work/input4MIPs/CMIP7/CMIP/PNNL-JGCRI/CEDS-CMIP-2025-04-18/atmos/mon/N2O_em_anthro/gn/v20250421/N2O-em-anthro_input4MIPs_emissions_CMIP_CEDS-CMIP-2025-04-18_gn_200001-202312.nc"
  },
  "temporal": {
    "start": "2000-01-01T00:00:00Z",
    "end": "2023-12-31T23:59:59Z",
    "file_period": "P1Y",
    "frequency": "P1M",
    "records_per_file": 12,
    "time_variable": "time"
  },
  "reference": {
    "citation": "Hoesly et al. (2018). Historical (1750–2014) anthropogenic emissions from CEDS. GMD 11, 369–408.",
    "url": "https://doi.org/10.5194/gmd-11-369-2018"
  },
  "metadata": {
    "tags": [
      "emissions",
      "anthropogenic",
      "ceds",
      "monthly",
      "gridded",
      "nitrous_oxide"
    ],
    "earthscidata_source": "src/ceds.jl::CEDSFileSet",
    "species": "N2O",
    "nc_varname": "N2O_em_anthro",
    "chunk": "2000-2023",
    "sector_aggregation": "sum",
    "sector_dim": "sector",
    "sector_count": 8,
    "grid_size": "720 lon × 360 lat",
    "version": "CEDS-CMIP-2025-04-18",
    "data_version": "v20250421",
    "native_resolution_deg": {
      "lon": 0.5,
      "lat": 0.5
    },
    "native_extent": {
      "lon": [
        -180.0,
        180.0
      ],
      "lat": [
        -90.0,
        90.0
      ]
    },
    "proj4_string": "+proj=longlat +datum=WGS84 +no_defs",
    "former_regridding": "Pre-migration per-loader regridding block was {fill_value: 0.0, extrapolation: clamp}; at 0.7.0 regridding became a per-variable model `regrid` map; 0.8.0 removed that too — the kernel is now a coupling expression (esm-spec §8.6), and ceds.esm keeps the per-variable choice verbatim in Model.reference.notes.",
    "native_grid_family": "cartesian",
    "native_crs_epsg": "EPSG:4326 (geographic longlat / WGS84). At esm 0.8.0 the crs is documentation only — a data source no longer carries a `grid`/crs descriptor; the longlat identity reprojection is applied at the coupling edge via ESD reprojection/longlat.esm (esd-47z.1).",
    "native_crs_descriptor": {
      "projection": "longlat",
      "datum": "WGS84"
    },
    "native_dimensions": [
      "lon",
      "lat"
    ],
    "native_dimension_extents": {
      "lon": {
        "n": 720,
        "spacing": "uniform"
      },
      "lat": {
        "n": 360,
        "spacing": "uniform"
      }
    },
    "native_staggering": "Cell-centered (lon 'center', lat 'center') — the native CEDS 0.5°×0.5° lattice is a regular non-staggered raster (the former `grid.description`, preserved verbatim in native_grid_description, said 'cell-centered'). At esm 0.8.0 the regridding kernel that carries this field onto a consuming grid is a coupling expression, not a model `regrid` block; the per-variable kernel choice is recorded verbatim in ceds.esm's Model.reference.notes until a consuming coupling edge exists to carry it.",
    "native_grid_description": "Native CEDS grid: regular global 0.5°×0.5° longitude/latitude lattice (720×360), cell-centered. Geographic (unprojected) crs — the regridding model applies the longlat identity reprojection (ESD reprojection/longlat.esm, esd-47z.1). Migrated from the loader's former DataLoaderSpatial block (proj4 +proj=longlat +datum=WGS84). Longitude is reordered from the raw NC [0, 360) to [-180°, 180°] by the upstream CEDSFileSet.loadslice! permutation; the loader describes this reordered grid but performs no reprojection or regridding. Documented native geometry: lon ∈ [-180°, 180°] (720 cells), lat ∈ [-90°, 90°] (360 cells).",
    "migration_note": "esm 0.7.0 -> 0.8.0: removed the `grid` block (family/crs/dimensions/extents/description), which no schema at or after 0.8.0 permits — 0.8.0 deleted the native-grid descriptor outright (esm-spec §8.4; the 1.0.0 DataSource is additionalProperties:false over {kind, source, temporal, determinism, reader_options, select, record_filter, extent, reference, metadata}, with no `grid` key). Nothing was dropped: `family` → native_grid_family; `crs` → native_crs_epsg + native_crs_descriptor (verbatim); `dimensions` → native_dimensions; `extents` (per-dimension cell count + spacing) → native_dimension_extents; `description` → native_grid_description (verbatim). Native grid geometry is now ordinary data — a source exposes its coordinates/connectivity/metric arrays as ordinary `file_variable`s bound to consuming parameters, and reprojection/regridding are ordinary `aggregate` coupling expressions (esm-spec §8.6), not a loader `grid` or a model `regrid` block. No other field changed.",
    "merged_from": "components/earthsci_data/ceds_n2o_loader.esm",
    "merge_note": "Merged from the standalone pure-I/O file components/earthsci_data/ceds_n2o_loader.esm, which is deleted by the same commit. The 0.x `X.esm` + `X_loader.esm` split existed only because a loader was a COMPONENT and a {\"ref\"} target had to contain exactly one component. At esm 1.0.0 a data source is NOT a component, not a coupling endpoint and not a scoped-name path root, and `data_sources` no longer counts toward a file's top-level system count — so one file may hold a model AND the data_sources that model consumes and still be mountable by {\"ref\"}. This registry entry is byte-identical to the one the deleted file declared (it was already mirrored here so this document would validate), and the deleted file's own top-level metadata — name, description, tags, created, authors, references — is preserved verbatim in `merged_file_metadata` so no provenance, citation or migration note is lost.",
    "merged_file_metadata": {
      "name": "CEDS_N2O_loader",
      "description": "Pure-I/O data loader for CEDS (Community Emissions Data System) monthly anthropogenic N2O emissions. Supplies the sector-summed surface emission flux N2O_em_anthro (kg m⁻² s⁻¹) on the native 0.5°×0.5° global longitude/latitude grid, monthly, 2000–2023 chunk (CEDS-CMIP-2025-04-18, v20250421).\n\nThis is one of the ten loader halves of the ceds loader+regridding-model split (RFC pure-io-data-loaders §4.1/§7; bead esm-3nc.3) — CEDS sources each species from a separate NetCDF FileSet, so each becomes its own single-component loader file (a {\"ref\"} target must contain exactly one component, RFC §4.7). It is PURE I/O: it declares its source (url_template), the file variable it reads (N2O_em_anthro, sector-summed at load time, with units), and its temporal cadence. It declares NO grid: esm 0.8.0 removed the loader `grid`/GDD-Grid descriptor outright, so the native 0.5°×0.5° longlat/WGS84 lattice is recorded as documentation in the data source's metadata (native_grid_family / native_crs_epsg / native_crs_descriptor / native_dimensions / native_dimension_extents / native_staggering / native_grid_description) and is materialized downstream by `aggregate` coupling expressions. It performs NO reprojection and NO regridding — those are per-variable concerns of the regridding model (components/earthsci_data/ceds.esm), which references this file as the subsystem `CEDS_N2O` via {\"ref\": \"./ceds_n2o_loader.esm\"}.\n\nThe removed co-located blocks: the old DataLoaderSpatial block (proj4 crs string / grid_type / staggering / resolution / extent) became the GDD `grid` at 0.7.0 and, at 0.8.0, metadata documentation (see metadata.migration_note on the data source); the old per-loader `regridding` block (fill_value / extrapolation) is gone, and so is the model-level `regrid` map that briefly replaced it — at 0.8.0 the regridding kernel is a coupling expression, and ceds.esm keeps the per-variable kernel choice verbatim in Model.reference.notes. Because a `temporal` block is present, this loader seeds DISCRETE cadence (ess-v9a.5).\n\nMigrated from EarthSciData.jl@830435a src/ceds.jl:1-378 (CEDSFileSet). Split out of the pre-migration components/earthsci_data/ceds.esm (esm-4ega).",
      "tags": [
        "earthsci_data",
        "emissions",
        "anthropogenic",
        "ceds",
        "monthly",
        "data_loader",
        "surface_flux",
        "global",
        "pure-io",
        "longlat",
        "n2o"
      ],
      "created": "2026-06-25T00:00:00Z",
      "authors": [
        "EarthSciData.jl contributors",
        "EarthSciModels migration (esm-3nc.3)"
      ],
      "references": [
        {
          "citation": "Hoesly, R. M., Smith, S. J., Feng, L., Klimont, Z., Janssens-Maenhout, G., Pitkanen, T., Seibert, J. J., Vu, L., Andres, R. J., Bolt, R. M., Bond, T. C., Dawidowski, L., Kholod, N., Kurokawa, J., Li, M., Liu, L., Lu, Z., Moura, M. C. P., O'Rourke, P. R., and Zhang, Q. (2018). Historical (1750–2014) anthropogenic emissions of reactive gases and aerosols from the Community Emissions Data System (CEDS). Geoscientific Model Development, 11, 369–408.",
          "url": "https://doi.org/10.5194/gmd-11-369-2018"
        },
        {
          "citation": "CEDS-CMIP 2025 release (v20250421, CEDS-CMIP-2025-04-18). Available from ORNL ESGF THREDDS: https://esgf-node.ornl.gov/thredds/fileServer/user_pub_work/input4MIPs/CMIP7/CMIP/PNNL-JGCRI/CEDS-CMIP-2025-04-18/"
        },
        {
          "citation": "Source: EarthSciData.jl@830435a065f27e99f10bba91107ca1730322cc6b:src/ceds.jl:1-378 (CEDSFileSet, CEDS constructor). Test: test/ceds_test.jl. Docs: docs/src/ceds.md."
        }
      ]
    }
  }
}
```

</details>
