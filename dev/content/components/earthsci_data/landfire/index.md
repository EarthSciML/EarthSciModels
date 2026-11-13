---
title: "LANDFIRE"
slug: "landfire"
domains: ["earthsci_data"]
component_types: ["data_source"]
domain: "earthsci_data"
component_type: "data_source"
esm_version: "1.0.0"
esm_path: "components/earthsci_data/landfire.esm"
reference: "https://landfire.gov/"
description: "LANDFIRE regridding model — the coupler half of the landfire loader+regridding-model split (RFC pure-io-data-loaders §6/§7; bead esm-3nc.4). Exposes the LANDFIRE fire-behavior fuel-model code (Anderson 13 / Scott & Burgan 40) on the simulation's target grid for wildland-fire coupling in EarthSciML systems."
tags: ["earthsci_data", "data_source", "wildland_fire", "fuel_model", "regridding_model", "landfire", "static", "conus", "longlat"]
---

## Description

LANDFIRE regridding model — the coupler half of the landfire loader+regridding-model split (RFC pure-io-data-loaders §6/§7; bead esm-3nc.4). Exposes the LANDFIRE fire-behavior fuel-model code (Anderson 13 / Scott & Burgan 40) on the simulation's target grid for wildland-fire coupling in EarthSciML systems.

Structure (RFC pure-io-data-loaders §6):
  1. It declares the pure-I/O source inline: at 0.7.0 the loader was the separate file components/earthsci_data/landfire_loader.esm, mounted as the subsystem `raw`; at esm 1.0.0 it is the `LANDFIRE` entry in this file's own `data_sources` and the standalone file is gone (a data source is not a component, so it neither needs nor may be a subsystem). The loader field is referenced as raw.fuel_model and re-exposed as the model-level observed variable LANDFIRE.fuel_model (Pattern B), preserving the public symbol path for downstream consumers (e.g. the wildland_fire fuel-model lookup family).
  2. Reprojection & regridding are NOT model concerns at esm 0.8.0. LANDFIRE's native grid is geographic (longlat/WGS84); the identity longlat reprojection and the conservative overlap-area regridding of the fuel_model field onto a consuming grid are expressed at the COUPLING EDGE as coupling expressions (esm-spec §8.6/§10.5), by importing the earthscidiscretizations reprojection/longlat.esm and regridding/conservative_overlap.esm — see the wildlandfire.esm assembler. This model no longer carries a `regrid` block. NOTE: fuel_model is CATEGORICAL; conservative area-weighting of integer fuel-model codes can produce non-integer codes between categories (the upstream loader used nearest-neighbour). Downstream consumers (FuelModelLookup, fuel_* functions) ifelse/clamp to integer codes and tolerate non-integer inputs; a nearest/mode regrid kernel is the future fix. See reference.notes (gt-categorical).

This is a STATIC (time-invariant) dataset: the loader carries no `temporal` block (CONST cadence). The fuel-model code is fetched once per simulation domain.

Migration esm 0.7.0 -> 0.8.0 (this file): v0.8.0 is a clean break that REMOVED `Model.regrid`/`RegridSpec` (esm-spec §8.6). Accordingly the former model `regrid` block (fuel_model -> conservative) has been REMOVED and the regridding is now performed at the coupling edge via imported template libraries. `fuel_model` (= raw.fuel_model) is the model's sole physics output.

Migrated from EarthSciData.jl@830435a065f27e99f10bba91107ca1730322cc6b:src/landfire.jl:246 (LANDFIRE constructor, esm-19u5); split into pure loader + regridding model by esm-3nc.4.

## Reference

USGS LANDFIRE (2022). LF2022 Fire Behavior Fuel Model 13 (FBFM13) / Fuel Model 40 (FBFM40). U.S. Department of Agriculture, Forest Service; U.S. Department of Interior.
- **URL**: https://landfire.gov/

## Data source

| | |
| --- | --- |
| Kind | `static` |
| URL template | `https://lfps.usgs.gov/arcgis/rest/services/Landfire_{version}/{version}_{product}_CONUS/ImageServer/exportImage?bbox={bbox_west_deg},{bbox_south_deg},{bbox_east_deg},{bbox_north_deg}&bboxSR=4326&imageSR=4326&size={image_width},{image_height}&format=tiff&pixelType=S16&interpolation=+RSP_NearestNeighbor&f=image` |

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "kind": "static",
  "source": {
    "url_template": "https://lfps.usgs.gov/arcgis/rest/services/Landfire_{version}/{version}_{product}_CONUS/ImageServer/exportImage?bbox={bbox_west_deg},{bbox_south_deg},{bbox_east_deg},{bbox_north_deg}&bboxSR=4326&imageSR=4326&size={image_width},{image_height}&format=tiff&pixelType=S16&interpolation=+RSP_NearestNeighbor&f=image"
  },
  "reference": {
    "citation": "USGS LANDFIRE (2022). LF2022 Fire Behavior Fuel Model 13 (FBFM13) / Fuel Model 40 (FBFM40). U.S. Department of Agriculture, Forest Service; U.S. Department of Interior.",
    "url": "https://landfire.gov/"
  },
  "metadata": {
    "tags": [
      "wildland_fire",
      "fuel_model",
      "landfire",
      "static",
      "conus",
      "categorical",
      "longlat"
    ],
    "earthscidata_source": "src/landfire.jl::LANDFIREFileSet",
    "api_type": "ArcGIS ImageServer REST (exportImage endpoint)",
    "file_format": "GeoTIFF, S16 signed 16-bit integer pixels (Q0f15 fixed-point in TiffImages; multiply by 32768 to get integer fuel model codes)",
    "native_resolution_deg": {
      "lon": 0.00027778,
      "lat": 0.00027778
    },
    "native_staggering": "Cell-centered (lon 'center', lat 'center') — LANDFIRE is a regular non-staggered raster. The regridding model regrids fuel_model conservatively per the migration spec (RFC §5.2; bead esm-3nc.4); see landfire.esm regrid.fuel_model and interpolation_note below for the categorical caveat.",
    "native_extent": {
      "comment": "Approximate CONUS envelope; the actual requested bbox is domain-derived at load time (WGS84 envelope of the model domain with a one-cell buffer).",
      "lon": [
        -125.0,
        -66.0
      ],
      "lat": [
        24.0,
        50.0
      ]
    },
    "interpolation_note": "The upstream EarthSciData.jl loader regrids this CATEGORICAL dataset with nearest-neighbour (BSpline(Constant())) interpolation — interpolated values BETWEEN integer codes are physically meaningless. The new ESS RegridSpec offers only {conservative, bspline, cell_average}; per the esm-3nc.4 migration spec (cell-centered → conservative) the regridding model declares regrid.fuel_model.method = conservative. Downstream consumers (components/wildland_fire/fuel_model_lookup.esm and the fuel_* registered functions) round/clamp to integer codes via ifelse + interp.linear, tolerating non-integer inputs. This nearest-neighbour-vs-conservative consideration is carried forward as a documented gap (gotcha §8) pending a nearest/mode regrid kernel in ESS.",
    "bbox_computation": "The URL template substitutions {bbox_west_deg}, {bbox_south_deg}, {bbox_east_deg}, {bbox_north_deg}, {image_width}, {image_height} are domain-derived at runtime: the bounding box is the WGS84 envelope of the model domain (with a one-resolution-cell buffer), and the image dimensions are computed from the bbox extent divided by the requested resolution (default 1.0 arc-second ≈ 30m, clamped to 4000×4000 pixels per LANDFIRE ImageServer limit).",
    "url_substitutions": "{version}=LF2022 (default), {product}=FBFM13 (default, use FBFM40 for Scott & Burgan 40 models), {bbox_*_deg}=domain WGS84 bounding box in degrees, {image_width}/{image_height}=computed pixel dimensions",
    "url_defaults": {
      "version": "LF2022",
      "product": "FBFM13",
      "size_cap": 4000
    },
    "coverage": "Contiguous United States (CONUS) only. Requests outside CONUS may return fill values or errors.",
    "valid_products": [
      "FBFM13",
      "FBFM40"
    ],
    "valid_versions": [
      "LF2020",
      "LF2022"
    ],
    "cache_path_pattern": "landfire/{product}_{bbox_west}_{bbox_south}_{bbox_east}_{bbox_north}_{width}x{height}.tif",
    "static_note": "No temporal block: kind='static' and the absence of `temporal` seed CONST cadence (ess-v9a.5). The runtime fetches the GeoTIFF once per simulation domain and never reloads it (upstream DataFrequencyInfo uses a single interval spanning [starttime, endtime + 1 day], with build_interp_event firing once at simulation start).",
    "merged_from": "components/earthsci_data/landfire_loader.esm",
    "merge_note": "Merged from the standalone pure-I/O file components/earthsci_data/landfire_loader.esm, which is deleted by the same commit. The 0.x `X.esm` + `X_loader.esm` split existed only because a loader was a COMPONENT and a {\"ref\"} target had to contain exactly one component. At esm 1.0.0 a data source is NOT a component, not a coupling endpoint and not a scoped-name path root, and `data_sources` no longer counts toward a file's top-level system count — so one file may hold a model AND the data_sources that model consumes and still be mountable by {\"ref\"}. This registry entry is byte-identical to the one the deleted file declared (it was already mirrored here so this document would validate), and the deleted file's own top-level metadata — name, description, tags, created, authors, references — is preserved verbatim in `merged_file_metadata` so no provenance, citation or migration note is lost.",
    "merged_file_metadata": {
      "name": "LANDFIRE_loader",
      "description": "Pure-I/O data loader for LANDFIRE (Landscape Fire and Resource Management Planning Tools) fire-behavior fuel-model classifications. Provides the Anderson 13 (FBFM13) or Scott & Burgan 40 (FBFM40) fuel-model code at ~30 m (~1 arc-second) resolution over the contiguous United States (CONUS), on a geographic (longlat/WGS84) lattice, sourced from the USGS LANDFIRE ImageServer REST API as a GeoTIFF cropped to the model domain.\n\nThis is the loader half of the landfire loader+regridding-model split (RFC pure-io-data-loaders §4.1/§7; bead esm-3nc.4). It is PURE I/O: it declares its source (url_template) and the file variable it reads (with units). It performs NO reprojection and NO regridding — those are per-variable concerns of the regridding model (components/earthsci_data/landfire.esm), which references this file as a subsystem via {\"ref\": \"./landfire_loader.esm\"}.\n\nThis is a STATIC (time-invariant) dataset: there is NO `temporal` block, so the loader seeds CONST cadence (ess-v9a.5) — the runtime folds the field once at bind (kind: static; the GeoTIFF is fetched once per simulation domain and never refreshed). Cadence derives from the absence of `temporal`, orthogonal to the `kind` enum.\n\nMigration esm 0.7.0 -> 0.8.0 (this file): v0.8.0 is a clean break that REMOVED the DataLoader `grid`/`mesh` descriptor (esm-spec §8.4: 'the former native-grid descriptor was removed in v0.8.0'; esm-schema.json DataLoader is now additionalProperties:false over {kind, source, temporal, determinism, variables, reference, metadata} with no `grid` key). Accordingly the former GDD `grid` block (family/crs/dimensions/extents + the n_lon/n_lat grid parameters) has been REMOVED. Grid geometry is now ordinary data: the native geographic lattice (its lon/lat origin = the fetched bbox, its ~0.00027778° spacing, and its runtime-resolved cell counts) is documented in metadata below and is materialized downstream by `aggregate` FAQs / coupling expressions (esm-spec §8.6). Reprojection (longlat identity) and conservative regridding onto a consuming grid are performed at the coupling edge via the reprojection/ and regridding/ template libraries in earthscidiscretizations, NOT here.\n\nMigrated from EarthSciData.jl@830435a065f27e99f10bba91107ca1730322cc6b:src/landfire.jl:246 (LANDFIREFileSet, LANDFIRE constructor). Split out of the pre-migration components/earthsci_data/landfire.esm (esm-19u5); grid block removed in the 0.7.0 -> 0.8.0 migration.",
      "tags": [
        "earthsci_data",
        "wildland_fire",
        "fuel_model",
        "landfire",
        "static",
        "data_loader",
        "pure-io",
        "conus",
        "longlat",
        "categorical"
      ],
      "created": "2026-06-25T00:00:00Z",
      "authors": [
        "EarthSciData.jl contributors",
        "EarthSciModels migration (esm-3nc.4)"
      ],
      "references": [
        {
          "citation": "LANDFIRE (2022). LANDFIRE 2022 Fire Behavior Fuel Model (FBFM13/FBFM40). U.S. Department of Agriculture, Forest Service; U.S. Department of Interior. Available: https://landfire.gov/",
          "url": "https://landfire.gov/"
        },
        {
          "citation": "Anderson, H.E. (1982). Aids to determining fuel models for estimating fire behavior. USDA Forest Service, Intermountain Forest and Range Experiment Station. Gen. Tech. Rep. INT-122. — Source for Anderson 13 fuel model codes 1–13."
        },
        {
          "citation": "Scott, J.H. and Burgan, R.E. (2005). Standard fire behavior fuel models: a comprehensive set for use with Rothermel's surface fire spread model. USDA Forest Service Gen. Tech. Rep. RMRS-GTR-153. — Source for Scott & Burgan 40 fuel model codes (FBFM40 product)."
        },
        {
          "citation": "Source: EarthSciData.jl@830435a065f27e99f10bba91107ca1730322cc6b:src/landfire.jl (LANDFIREFileSet, LANDFIRE constructor). Test: test/landfire_test.jl. Docs: docs/src/landfire.md."
        }
      ]
    }
  }
}
```

</details>
