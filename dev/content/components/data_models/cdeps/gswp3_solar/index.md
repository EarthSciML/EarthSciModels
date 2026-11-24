---
title: "GSWP3_Solar"
slug: "gswp3_solar"
domains: ["data_models"]
component_types: ["data_source"]
subdomains: ["cdeps"]
domain: "data_models"
subdomain: "cdeps"
component_type: "data_source"
esm_version: "2.0.0"
esm_path: "components/data_models/cdeps/cdeps_datm_gswp3_data.esm"
reference: "10.20783/DIAS.501"
description: "The CDEPS DATM GSWP3 chain with data: the four GSWP3v1 data sources on the public NCAR CESM inputdata server (Solar FSDS, Precip PRECTmms, TPQW TBOT/PSRF/WIND/QBOT/FLDS, static topo TOPO; url_templates with {date:%Y-%m} over the archived 1901-01..2014-12 months), the GSWP3Files reader model (one data-fed parameter per file variable: the 3-hourly fields shaped over the record axis rec, so each receives the pair of records bracketing t, and the static TOPO a scalar), the Streams and Clmncep laws mounted from ./cdeps_datm_gswp3.esm, and the reader -> Streams -> Clmncep wiring (param_to_var edges; the same edges as cdeps_datm_gswp3_synthetic.esm). The Streams model computes the CDEPS time-interpolation factors from t. The time origin is 2000-01-01T00:00:00Z (domain.temporal.reference_time), the origin Streams.calday0 = 1 and the record offsets t0_* assume; the TPQW and Precip sources declare temporal.start at their first record time (01:30Z) because the records sit at 01:30, 04:30, .. Z. Carries no inline test: running it reads the real archive, and CI does not download data. The same wiring is tested on synthetic files by cdeps_datm_gswp3_synthetic.esm. No data is redistributed; the sources are referenced by URL only (GSWP3: Kim 2017, doi:10.20783/DIAS.501). Known differences from the reference CESM run: the reference cycles 1991-2010 (taxmode cycle, year_align 1991) and reads the 1991 files for model year 2000, while a data source here reads the file of the model date itself; and the bilinear map from the 0.5 deg source grid to the model mesh is not represented (the select picks one source cell)."
tags: ["data_models", "cdeps", "data_source", "datm", "gswp3", "forcing", "data-sources"]
---

## Description

The CDEPS DATM GSWP3 chain with data: the four GSWP3v1 data sources on the public NCAR CESM inputdata server (Solar FSDS, Precip PRECTmms, TPQW TBOT/PSRF/WIND/QBOT/FLDS, static topo TOPO; url_templates with {date:%Y-%m} over the archived 1901-01..2014-12 months), the GSWP3Files reader model (one data-fed parameter per file variable: the 3-hourly fields shaped over the record axis rec, so each receives the pair of records bracketing t, and the static TOPO a scalar), the Streams and Clmncep laws mounted from ./cdeps_datm_gswp3.esm, and the reader -> Streams -> Clmncep wiring (param_to_var edges; the same edges as cdeps_datm_gswp3_synthetic.esm). The Streams model computes the CDEPS time-interpolation factors from t. The time origin is 2000-01-01T00:00:00Z (domain.temporal.reference_time), the origin Streams.calday0 = 1 and the record offsets t0_* assume; the TPQW and Precip sources declare temporal.start at their first record time (01:30Z) because the records sit at 01:30, 04:30, .. Z. Carries no inline test: running it reads the real archive, and CI does not download data. The same wiring is tested on synthetic files by cdeps_datm_gswp3_synthetic.esm. No data is redistributed; the sources are referenced by URL only (GSWP3: Kim 2017, doi:10.20783/DIAS.501). Known differences from the reference CESM run: the reference cycles 1991-2010 (taxmode cycle, year_align 1991) and reads the 1991 files for model year 2000, while a data source here reads the file of the model date itself; and the bilinear map from the 0.5 deg source grid to the model mesh is not represented (the select picks one source cell).

## Reference

Kim, H. (2017). Global Soil Wetness Project Phase 3 Atmospheric Boundary Conditions (Experiment 1) [Data set]. Data Integration and Analysis System (DIAS).
- **DOI**: 10.20783/DIAS.501
- **URL**: https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/datm7/atm_forcing.datm7.GSWP3.0.5d.v1.c170516/Solar/

## Data source

| | |
| --- | --- |
| Kind | `grid` |
| URL template | `https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/datm7/atm_forcing.datm7.GSWP3.0.5d.v1.c170516/Solar/clmforc.GSWP3.c2011.0.5x0.5.Solr.{date:%Y-%m}.nc` |
| Coverage | 1901-01-01T00:00:00Z → 2014-12-31T23:59:59Z |
| File period | `P1M` |
| Sample frequency | `PT3H` |
| Records per file | auto |

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "kind": "grid",
  "source": {
    "url_template": "https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/datm7/atm_forcing.datm7.GSWP3.0.5d.v1.c170516/Solar/clmforc.GSWP3.c2011.0.5x0.5.Solr.{date:%Y-%m}.nc"
  },
  "temporal": {
    "start": "1901-01-01T00:00:00Z",
    "end": "2014-12-31T23:59:59Z",
    "file_period": "P1M",
    "frequency": "PT3H",
    "records_per_file": "auto",
    "time_variable": "time"
  },
  "select": {
    "axes": [
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
      "gswp3",
      "datm",
      "forcing",
      "solar",
      "3-hourly"
    ],
    "description": "GSWP3v1 FSDS [W/m2], 0.5x0.5 deg (360 x 720), 3-hourly records at 00..21Z (time = 0, 0.125, .. days since the month start), the Solar stream of the I2000Clm60Sp reference case (tintalgo coszen). The select fixes (lat, lon) = (0, 0) as a placeholder cell; a consumer selects its own cell or regrids (out of scope here)."
  },
  "reference": {
    "citation": "Kim, H. (2017). Global Soil Wetness Project Phase 3 Atmospheric Boundary Conditions (Experiment 1) [Data set]. Data Integration and Analysis System (DIAS).",
    "doi": "10.20783/DIAS.501",
    "url": "https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/datm7/atm_forcing.datm7.GSWP3.0.5d.v1.c170516/Solar/"
  }
}
```

</details>
