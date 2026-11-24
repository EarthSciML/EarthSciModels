---
title: "GSWP3_Topo"
slug: "gswp3_topo"
domains: ["data_models"]
component_types: ["data_source"]
subdomains: ["cdeps"]
domain: "data_models"
subdomain: "cdeps"
component_type: "data_source"
esm_version: "2.0.0"
esm_path: "components/data_models/cdeps/cdeps_datm_gswp3_data.esm"
reference: "https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/datm7/topo_forcing/"
description: "The CDEPS DATM GSWP3 chain with data: the four GSWP3v1 data sources on the public NCAR CESM inputdata server (Solar FSDS, Precip PRECTmms, TPQW TBOT/PSRF/WIND/QBOT/FLDS, static topo TOPO; url_templates with {date:%Y-%m} over the archived 1901-01..2014-12 months), the GSWP3Files reader model (one data-fed parameter per file variable: the 3-hourly fields shaped over the record axis rec, so each receives the pair of records bracketing t, and the static TOPO a scalar), the Streams and Clmncep laws mounted from ./cdeps_datm_gswp3.esm, and the reader -> Streams -> Clmncep wiring (param_to_var edges; the same edges as cdeps_datm_gswp3_synthetic.esm). The Streams model computes the CDEPS time-interpolation factors from t. The time origin is 2000-01-01T00:00:00Z (domain.temporal.reference_time), the origin Streams.calday0 = 1 and the record offsets t0_* assume; the TPQW and Precip sources declare temporal.start at their first record time (01:30Z) because the records sit at 01:30, 04:30, .. Z. Carries no inline test: running it reads the real archive, and CI does not download data. The same wiring is tested on synthetic files by cdeps_datm_gswp3_synthetic.esm. No data is redistributed; the sources are referenced by URL only (GSWP3: Kim 2017, doi:10.20783/DIAS.501). Known differences from the reference CESM run: the reference cycles 1991-2010 (taxmode cycle, year_align 1991) and reads the 1991 files for model year 2000, while a data source here reads the file of the model date itself; and the bilinear map from the 0.5 deg source grid to the model mesh is not represented (the select picks one source cell)."
tags: ["data_models", "cdeps", "data_source", "datm", "gswp3", "forcing", "data-sources"]
---

## Description

The CDEPS DATM GSWP3 chain with data: the four GSWP3v1 data sources on the public NCAR CESM inputdata server (Solar FSDS, Precip PRECTmms, TPQW TBOT/PSRF/WIND/QBOT/FLDS, static topo TOPO; url_templates with {date:%Y-%m} over the archived 1901-01..2014-12 months), the GSWP3Files reader model (one data-fed parameter per file variable: the 3-hourly fields shaped over the record axis rec, so each receives the pair of records bracketing t, and the static TOPO a scalar), the Streams and Clmncep laws mounted from ./cdeps_datm_gswp3.esm, and the reader -> Streams -> Clmncep wiring (param_to_var edges; the same edges as cdeps_datm_gswp3_synthetic.esm). The Streams model computes the CDEPS time-interpolation factors from t. The time origin is 2000-01-01T00:00:00Z (domain.temporal.reference_time), the origin Streams.calday0 = 1 and the record offsets t0_* assume; the TPQW and Precip sources declare temporal.start at their first record time (01:30Z) because the records sit at 01:30, 04:30, .. Z. Carries no inline test: running it reads the real archive, and CI does not download data. The same wiring is tested on synthetic files by cdeps_datm_gswp3_synthetic.esm. No data is redistributed; the sources are referenced by URL only (GSWP3: Kim 2017, doi:10.20783/DIAS.501). Known differences from the reference CESM run: the reference cycles 1991-2010 (taxmode cycle, year_align 1991) and reads the 1991 files for model year 2000, while a data source here reads the file of the model date itself; and the bilinear map from the 0.5 deg source grid to the model mesh is not represented (the select picks one source cell).

## Reference

USGS 30-arc-second GTOPO30-based surface topography (TOPO), remapped to the 0.9x1.25 deg grid and archived on the NCAR CESM inputdata server.
- **URL**: https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/datm7/topo_forcing/

## Data source

| | |
| --- | --- |
| Kind | `static` |
| URL template | `https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/datm7/topo_forcing/topodata_0.9x1.25_USGS_070110_stream_c151201.nc` |

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "kind": "static",
  "source": {
    "url_template": "https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/datm7/topo_forcing/topodata_0.9x1.25_USGS_070110_stream_c151201.nc"
  },
  "select": {
    "axes": [
      "all",
      {
        "fixed": 0
      },
      {
        "fixed": 0
      }
    ]
  },
  "metadata": {
    "esio_format": "netcdf",
    "tags": [
      "topography",
      "static"
    ],
    "description": "USGS surface topography TOPO [m] on the 0.9x1.25 deg grid (192 x 288), the topo.observed stream (tintalgo lower); one record on a degenerate time dimension of length 1. The source is static (no temporal block), so its select names every native dimension: the degenerate time axis (\"all\" - the netcdf reader refuses a subset of a time dimension) and the (lat, lon) cell."
  },
  "reference": {
    "citation": "USGS 30-arc-second GTOPO30-based surface topography (TOPO), remapped to the 0.9x1.25 deg grid and archived on the NCAR CESM inputdata server.",
    "url": "https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/datm7/topo_forcing/"
  }
}
```

</details>
