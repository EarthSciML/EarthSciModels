---
title: "GSWP3Files"
slug: "gswp3files"
domains: ["data_models"]
component_types: ["model"]
subdomains: ["cdeps"]
domain: "data_models"
subdomain: "cdeps"
component_type: "model"
esm_version: "2.0.0"
esm_path: "components/data_models/cdeps/cdeps_datm_gswp3_data.esm"
reference: "https://github.com/ESCOMP/CDEPS"
description: "The CDEPS DATM GSWP3 chain with data: the four GSWP3v1 data sources on the public NCAR CESM inputdata server (Solar FSDS, Precip PRECTmms, TPQW TBOT/PSRF/WIND/QBOT/FLDS, static topo TOPO; url_templates with {date:%Y-%m} over the archived 1901-01..2014-12 months), the GSWP3Files reader model (one data-fed parameter per file variable: the 3-hourly fields shaped over the record axis rec, so each receives the pair of records bracketing t, and the static TOPO a scalar), the Streams and Clmncep laws mounted from ./cdeps_datm_gswp3.esm, and the reader -> Streams -> Clmncep wiring (param_to_var edges; the same edges as cdeps_datm_gswp3_synthetic.esm). The Streams model computes the CDEPS time-interpolation factors from t. The time origin is 2000-01-01T00:00:00Z (domain.temporal.reference_time), the origin Streams.calday0 = 1 and the record offsets t0_* assume; the TPQW and Precip sources declare temporal.start at their first record time (01:30Z) because the records sit at 01:30, 04:30, .. Z. Carries no inline test: running it reads the real archive, and CI does not download data. The same wiring is tested on synthetic files by cdeps_datm_gswp3_synthetic.esm. No data is redistributed; the sources are referenced by URL only (GSWP3: Kim 2017, doi:10.20783/DIAS.501). Known differences from the reference CESM run: the reference cycles 1991-2010 (taxmode cycle, year_align 1991) and reads the 1991 files for model year 2000, while a data source here reads the file of the model date itself; and the bilinear map from the 0.5 deg source grid to the model mesh is not represented (the select picks one source cell)."
tags: ["data_models", "cdeps", "model", "datm", "gswp3", "forcing", "data-sources"]
---

## Description

The CDEPS DATM GSWP3 chain with data: the four GSWP3v1 data sources on the public NCAR CESM inputdata server (Solar FSDS, Precip PRECTmms, TPQW TBOT/PSRF/WIND/QBOT/FLDS, static topo TOPO; url_templates with {date:%Y-%m} over the archived 1901-01..2014-12 months), the GSWP3Files reader model (one data-fed parameter per file variable: the 3-hourly fields shaped over the record axis rec, so each receives the pair of records bracketing t, and the static TOPO a scalar), the Streams and Clmncep laws mounted from ./cdeps_datm_gswp3.esm, and the reader -> Streams -> Clmncep wiring (param_to_var edges; the same edges as cdeps_datm_gswp3_synthetic.esm). The Streams model computes the CDEPS time-interpolation factors from t. The time origin is 2000-01-01T00:00:00Z (domain.temporal.reference_time), the origin Streams.calday0 = 1 and the record offsets t0_* assume; the TPQW and Precip sources declare temporal.start at their first record time (01:30Z) because the records sit at 01:30, 04:30, .. Z. Carries no inline test: running it reads the real archive, and CI does not download data. The same wiring is tested on synthetic files by cdeps_datm_gswp3_synthetic.esm. No data is redistributed; the sources are referenced by URL only (GSWP3: Kim 2017, doi:10.20783/DIAS.501). Known differences from the reference CESM run: the reference cycles 1991-2010 (taxmode cycle, year_align 1991) and reads the 1991 files for model year 2000, while a data source here reads the file of the model date itself; and the bilinear map from the 0.5 deg source grid to the model mesh is not represented (the select picks one source cell).

## Reference

- CESM (Community Earth System Model), ESCOMP/CDEPS: Common Data model EXchange Platform source (cdeps1.0.112) - datm/datm_datamode_clmncep_mod.F90, streams/dshr_strdata_mod.F90, streams/dshr_tinterp_mod.F90, share/shr_precip_mod.F90, share/shr_const_mod.F90 - the reference implementation these components are transcribed from.
- Kim, H. (2017). Global Soil Wetness Project Phase 3 Atmospheric Boundary Conditions (Experiment 1) [Data set]. Data Integration and Analysis System (DIAS). The GSWP3v1 0.5x0.5 deg, 3-hourly atmospheric forcing the datm consumes, as archived on the NCAR CESM inputdata server (atm_forcing.datm7.GSWP3.0.5d.v1.c170516).

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `FSDS` | `W/m^2` | `0.0` | GSWP3 FSDS: total incident solar radiation, as read from the GSWP3_Solar source. Shaped over the record axis rec, so at time t it receives the pair of records bracketing t, [the record at or before t (CDEPS LB), the next record (UB)] (esm-spec 8.5.1); the param_to_var edge to Streams.swdn_rec (declared with the same shape) hands the pair to the stream layer. Read from the public NCAR CESM inputdata archive. |
| `PRECTmms` | `kg/m^2/s` | `0.0` | GSWP3 PRECTmms: total precipitation rate (mm H2O/s = kg/m2/s), as read from the GSWP3_Precip source. Shaped over the record axis rec, so at time t it receives the pair of records bracketing t, [the record at or before t (CDEPS LB), the next record (UB)] (esm-spec 8.5.1); the param_to_var edge to Streams.precn_rec (declared with the same shape) hands the pair to the stream layer. Read from the public NCAR CESM inputdata archive. |
| `TBOT` | `K` | `0.0` | GSWP3 TBOT: temperature at the lowest atmospheric level, as read from the GSWP3_TPQW source. Shaped over the record axis rec, so at time t it receives the pair of records bracketing t, [the record at or before t (CDEPS LB), the next record (UB)] (esm-spec 8.5.1); the param_to_var edge to Streams.tbot_rec (declared with the same shape) hands the pair to the stream layer. Read from the public NCAR CESM inputdata archive. |
| `PSRF` | `Pa` | `0.0` | GSWP3 PSRF: surface pressure at the lowest atmospheric level, as read from the GSWP3_TPQW source. Shaped over the record axis rec, so at time t it receives the pair of records bracketing t, [the record at or before t (CDEPS LB), the next record (UB)] (esm-spec 8.5.1); the param_to_var edge to Streams.pbot_rec (declared with the same shape) hands the pair to the stream layer. Read from the public NCAR CESM inputdata archive. |
| `WIND` | `m/s` | `0.0` | GSWP3 WIND: wind speed at the lowest atmospheric level, as read from the GSWP3_TPQW source. Shaped over the record axis rec, so at time t it receives the pair of records bracketing t, [the record at or before t (CDEPS LB), the next record (UB)] (esm-spec 8.5.1); the param_to_var edge to Streams.wind_rec (declared with the same shape) hands the pair to the stream layer. Read from the public NCAR CESM inputdata archive. |
| `QBOT` | `kg/kg` | `0.0` | GSWP3 QBOT: specific humidity at the lowest atmospheric level, as read from the GSWP3_TPQW source. Shaped over the record axis rec, so at time t it receives the pair of records bracketing t, [the record at or before t (CDEPS LB), the next record (UB)] (esm-spec 8.5.1); the param_to_var edge to Streams.shum_rec (declared with the same shape) hands the pair to the stream layer. Read from the public NCAR CESM inputdata archive. |
| `FLDS` | `W/m^2` | `0.0` | GSWP3 FLDS: incident longwave radiation, as read from the GSWP3_TPQW source. Shaped over the record axis rec, so at time t it receives the pair of records bracketing t, [the record at or before t (CDEPS LB), the next record (UB)] (esm-spec 8.5.1); the param_to_var edge to Streams.lwdn_rec (declared with the same shape) hands the pair to the stream layer. Read from the public NCAR CESM inputdata archive. |
| `TOPO` | `m` | `0.0` | GSWP3 TOPO: surface topography height, as read from the static GSWP3_Topo source: declared a scalar (shape []), so it receives the file's single record (esm-spec 8.5.1). Feeds Streams.topo_in. Read from the public NCAR CESM inputdata archive. |

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "variables": {
    "FSDS": {
      "type": "parameter",
      "units": "W/m^2",
      "default": 0.0,
      "shape": [
        "rec"
      ],
      "description": "GSWP3 FSDS: total incident solar radiation, as read from the GSWP3_Solar source. Shaped over the record axis rec, so at time t it receives the pair of records bracketing t, [the record at or before t (CDEPS LB), the next record (UB)] (esm-spec 8.5.1); the param_to_var edge to Streams.swdn_rec (declared with the same shape) hands the pair to the stream layer. Read from the public NCAR CESM inputdata archive.",
      "update": {
        "kind": "data",
        "source": "GSWP3_Solar",
        "from": {
          "file_variable": "FSDS"
        }
      }
    },
    "PRECTmms": {
      "type": "parameter",
      "units": "kg/m^2/s",
      "default": 0.0,
      "shape": [
        "rec"
      ],
      "description": "GSWP3 PRECTmms: total precipitation rate (mm H2O/s = kg/m2/s), as read from the GSWP3_Precip source. Shaped over the record axis rec, so at time t it receives the pair of records bracketing t, [the record at or before t (CDEPS LB), the next record (UB)] (esm-spec 8.5.1); the param_to_var edge to Streams.precn_rec (declared with the same shape) hands the pair to the stream layer. Read from the public NCAR CESM inputdata archive.",
      "update": {
        "kind": "data",
        "source": "GSWP3_Precip",
        "from": {
          "file_variable": "PRECTmms"
        }
      }
    },
    "TBOT": {
      "type": "parameter",
      "units": "K",
      "default": 0.0,
      "shape": [
        "rec"
      ],
      "description": "GSWP3 TBOT: temperature at the lowest atmospheric level, as read from the GSWP3_TPQW source. Shaped over the record axis rec, so at time t it receives the pair of records bracketing t, [the record at or before t (CDEPS LB), the next record (UB)] (esm-spec 8.5.1); the param_to_var edge to Streams.tbot_rec (declared with the same shape) hands the pair to the stream layer. Read from the public NCAR CESM inputdata archive.",
      "update": {
        "kind": "data",
        "source": "GSWP3_TPQW",
        "from": {
          "file_variable": "TBOT"
        }
      }
    },
    "PSRF": {
      "type": "parameter",
      "units": "Pa",
      "default": 0.0,
      "shape": [
        "rec"
      ],
      "description": "GSWP3 PSRF: surface pressure at the lowest atmospheric level, as read from the GSWP3_TPQW source. Shaped over the record axis rec, so at time t it receives the pair of records bracketing t, [the record at or before t (CDEPS LB), the next record (UB)] (esm-spec 8.5.1); the param_to_var edge to Streams.pbot_rec (declared with the same shape) hands the pair to the stream layer. Read from the public NCAR CESM inputdata archive.",
      "update": {
        "kind": "data",
        "source": "GSWP3_TPQW",
        "from": {
          "file_variable": "PSRF"
        }
      }
    },
    "WIND": {
      "type": "parameter",
      "units": "m/s",
      "default": 0.0,
      "shape": [
        "rec"
      ],
      "description": "GSWP3 WIND: wind speed at the lowest atmospheric level, as read from the GSWP3_TPQW source. Shaped over the record axis rec, so at time t it receives the pair of records bracketing t, [the record at or before t (CDEPS LB), the next record (UB)] (esm-spec 8.5.1); the param_to_var edge to Streams.wind_rec (declared with the same shape) hands the pair to the stream layer. Read from the public NCAR CESM inputdata archive.",
      "update": {
        "kind": "data",
        "source": "GSWP3_TPQW",
        "from": {
          "file_variable": "WIND"
        }
      }
    },
    "QBOT": {
      "type": "parameter",
      "units": "kg/kg",
      "default": 0.0,
      "shape": [
        "rec"
      ],
      "description": "GSWP3 QBOT: specific humidity at the lowest atmospheric level, as read from the GSWP3_TPQW source. Shaped over the record axis rec, so at time t it receives the pair of records bracketing t, [the record at or before t (CDEPS LB), the next record (UB)] (esm-spec 8.5.1); the param_to_var edge to Streams.shum_rec (declared with the same shape) hands the pair to the stream layer. Read from the public NCAR CESM inputdata archive.",
      "update": {
        "kind": "data",
        "source": "GSWP3_TPQW",
        "from": {
          "file_variable": "QBOT"
        }
      }
    },
    "FLDS": {
      "type": "parameter",
      "units": "W/m^2",
      "default": 0.0,
      "shape": [
        "rec"
      ],
      "description": "GSWP3 FLDS: incident longwave radiation, as read from the GSWP3_TPQW source. Shaped over the record axis rec, so at time t it receives the pair of records bracketing t, [the record at or before t (CDEPS LB), the next record (UB)] (esm-spec 8.5.1); the param_to_var edge to Streams.lwdn_rec (declared with the same shape) hands the pair to the stream layer. Read from the public NCAR CESM inputdata archive.",
      "update": {
        "kind": "data",
        "source": "GSWP3_TPQW",
        "from": {
          "file_variable": "FLDS"
        }
      }
    },
    "TOPO": {
      "type": "parameter",
      "units": "m",
      "default": 0.0,
      "description": "GSWP3 TOPO: surface topography height, as read from the static GSWP3_Topo source: declared a scalar (shape []), so it receives the file's single record (esm-spec 8.5.1). Feeds Streams.topo_in. Read from the public NCAR CESM inputdata archive.",
      "shape": [],
      "update": {
        "kind": "data",
        "source": "GSWP3_Topo",
        "from": {
          "file_variable": "TOPO"
        }
      }
    }
  },
  "equations": []
}
```

</details>
