---
title: "GSWP3FilesSynthetic"
slug: "gswp3filessynthetic"
domains: ["data_models"]
component_types: ["model"]
subdomains: ["cdeps"]
domain: "data_models"
subdomain: "cdeps"
component_type: "model"
esm_version: "2.0.0"
esm_path: "components/data_models/cdeps/cdeps_datm_gswp3_synthetic.esm"
reference: "https://github.com/ESCOMP/CDEPS"
description: "Data-reading test of the CDEPS DATM GSWP3 chain on SYNTHETIC files: the same reader declarations as the GSWP3Files model of cdeps_datm_gswp3_data.esm (here GSWP3FilesSynthetic, reading sources named *_Synthetic, so the two documents' components and sources keep distinct names), the same Streams/Clmncep laws (mounted from ./cdeps_datm_gswp3.esm) and the same reader -> Streams -> Clmncep coupling edges as cdeps_datm_gswp3_data.esm, with the four data sources pointed at small GSWP3-shaped NetCDF files that tools/gen_synthetic_gswp3.py writes on demand into ./synthetic/ (git-ignored; CI generates them before the inline-test sweeps; no real data is downloaded). The record values are closed-form in the record and cell indices, so the expected values of the reader -> Streams -> Clmncep chain are known exactly. Run `python3 tools/gen_synthetic_gswp3.py` first; needs an esm CLI with data-source support (earthsci-ast-cli built with --features esio)."
tags: ["data_models", "cdeps", "model", "datm", "gswp3", "synthetic-data", "test"]
---

## Description

Data-reading test of the CDEPS DATM GSWP3 chain on SYNTHETIC files: the same reader declarations as the GSWP3Files model of cdeps_datm_gswp3_data.esm (here GSWP3FilesSynthetic, reading sources named *_Synthetic, so the two documents' components and sources keep distinct names), the same Streams/Clmncep laws (mounted from ./cdeps_datm_gswp3.esm) and the same reader -> Streams -> Clmncep coupling edges as cdeps_datm_gswp3_data.esm, with the four data sources pointed at small GSWP3-shaped NetCDF files that tools/gen_synthetic_gswp3.py writes on demand into ./synthetic/ (git-ignored; CI generates them before the inline-test sweeps; no real data is downloaded). The record values are closed-form in the record and cell indices, so the expected values of the reader -> Streams -> Clmncep chain are known exactly. Run `python3 tools/gen_synthetic_gswp3.py` first; needs an esm CLI with data-source support (earthsci-ast-cli built with --features esio).

## Reference

- CESM (Community Earth System Model), ESCOMP/CDEPS: Common Data model EXchange Platform source (cdeps1.0.112) - datm/datm_datamode_clmncep_mod.F90, streams/dshr_strdata_mod.F90, streams/dshr_tinterp_mod.F90, share/shr_precip_mod.F90, share/shr_const_mod.F90 - the reference implementation these components are transcribed from.

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `FSDS` | `W/m^2` | `0.0` | GSWP3 FSDS: total incident solar radiation, as read from the GSWP3_Solar source. Shaped over the record axis rec, so at time t it receives the pair of records bracketing t, [the record at or before t (CDEPS LB), the next record (UB)] (esm-spec 8.5.1); the param_to_var edge to Streams.swdn_rec (declared with the same shape) hands the pair to the stream layer. Read from the synthetic files of tools/gen_synthetic_gswp3.py. |
| `PRECTmms` | `kg/m^2/s` | `0.0` | GSWP3 PRECTmms: total precipitation rate (mm H2O/s = kg/m2/s), as read from the GSWP3_Precip source. Shaped over the record axis rec, so at time t it receives the pair of records bracketing t, [the record at or before t (CDEPS LB), the next record (UB)] (esm-spec 8.5.1); the param_to_var edge to Streams.precn_rec (declared with the same shape) hands the pair to the stream layer. Read from the synthetic files of tools/gen_synthetic_gswp3.py. |
| `TBOT` | `K` | `0.0` | GSWP3 TBOT: temperature at the lowest atmospheric level, as read from the GSWP3_TPQW source. Shaped over the record axis rec, so at time t it receives the pair of records bracketing t, [the record at or before t (CDEPS LB), the next record (UB)] (esm-spec 8.5.1); the param_to_var edge to Streams.tbot_rec (declared with the same shape) hands the pair to the stream layer. Read from the synthetic files of tools/gen_synthetic_gswp3.py. |
| `PSRF` | `Pa` | `0.0` | GSWP3 PSRF: surface pressure at the lowest atmospheric level, as read from the GSWP3_TPQW source. Shaped over the record axis rec, so at time t it receives the pair of records bracketing t, [the record at or before t (CDEPS LB), the next record (UB)] (esm-spec 8.5.1); the param_to_var edge to Streams.pbot_rec (declared with the same shape) hands the pair to the stream layer. Read from the synthetic files of tools/gen_synthetic_gswp3.py. |
| `WIND` | `m/s` | `0.0` | GSWP3 WIND: wind speed at the lowest atmospheric level, as read from the GSWP3_TPQW source. Shaped over the record axis rec, so at time t it receives the pair of records bracketing t, [the record at or before t (CDEPS LB), the next record (UB)] (esm-spec 8.5.1); the param_to_var edge to Streams.wind_rec (declared with the same shape) hands the pair to the stream layer. Read from the synthetic files of tools/gen_synthetic_gswp3.py. |
| `QBOT` | `kg/kg` | `0.0` | GSWP3 QBOT: specific humidity at the lowest atmospheric level, as read from the GSWP3_TPQW source. Shaped over the record axis rec, so at time t it receives the pair of records bracketing t, [the record at or before t (CDEPS LB), the next record (UB)] (esm-spec 8.5.1); the param_to_var edge to Streams.shum_rec (declared with the same shape) hands the pair to the stream layer. Read from the synthetic files of tools/gen_synthetic_gswp3.py. |
| `FLDS` | `W/m^2` | `0.0` | GSWP3 FLDS: incident longwave radiation, as read from the GSWP3_TPQW source. Shaped over the record axis rec, so at time t it receives the pair of records bracketing t, [the record at or before t (CDEPS LB), the next record (UB)] (esm-spec 8.5.1); the param_to_var edge to Streams.lwdn_rec (declared with the same shape) hands the pair to the stream layer. Read from the synthetic files of tools/gen_synthetic_gswp3.py. |
| `TOPO` | `m` | `0.0` | GSWP3 TOPO: surface topography height, as read from the static GSWP3_Topo source: declared a scalar (shape []), so it receives the file's single record (esm-spec 8.5.1). Feeds Streams.topo_in. Read from the synthetic files of tools/gen_synthetic_gswp3.py. |

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
      "description": "GSWP3 FSDS: total incident solar radiation, as read from the GSWP3_Solar source. Shaped over the record axis rec, so at time t it receives the pair of records bracketing t, [the record at or before t (CDEPS LB), the next record (UB)] (esm-spec 8.5.1); the param_to_var edge to Streams.swdn_rec (declared with the same shape) hands the pair to the stream layer. Read from the synthetic files of tools/gen_synthetic_gswp3.py.",
      "update": {
        "kind": "data",
        "source": "GSWP3_Solar_Synthetic",
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
      "description": "GSWP3 PRECTmms: total precipitation rate (mm H2O/s = kg/m2/s), as read from the GSWP3_Precip source. Shaped over the record axis rec, so at time t it receives the pair of records bracketing t, [the record at or before t (CDEPS LB), the next record (UB)] (esm-spec 8.5.1); the param_to_var edge to Streams.precn_rec (declared with the same shape) hands the pair to the stream layer. Read from the synthetic files of tools/gen_synthetic_gswp3.py.",
      "update": {
        "kind": "data",
        "source": "GSWP3_Precip_Synthetic",
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
      "description": "GSWP3 TBOT: temperature at the lowest atmospheric level, as read from the GSWP3_TPQW source. Shaped over the record axis rec, so at time t it receives the pair of records bracketing t, [the record at or before t (CDEPS LB), the next record (UB)] (esm-spec 8.5.1); the param_to_var edge to Streams.tbot_rec (declared with the same shape) hands the pair to the stream layer. Read from the synthetic files of tools/gen_synthetic_gswp3.py.",
      "update": {
        "kind": "data",
        "source": "GSWP3_TPQW_Synthetic",
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
      "description": "GSWP3 PSRF: surface pressure at the lowest atmospheric level, as read from the GSWP3_TPQW source. Shaped over the record axis rec, so at time t it receives the pair of records bracketing t, [the record at or before t (CDEPS LB), the next record (UB)] (esm-spec 8.5.1); the param_to_var edge to Streams.pbot_rec (declared with the same shape) hands the pair to the stream layer. Read from the synthetic files of tools/gen_synthetic_gswp3.py.",
      "update": {
        "kind": "data",
        "source": "GSWP3_TPQW_Synthetic",
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
      "description": "GSWP3 WIND: wind speed at the lowest atmospheric level, as read from the GSWP3_TPQW source. Shaped over the record axis rec, so at time t it receives the pair of records bracketing t, [the record at or before t (CDEPS LB), the next record (UB)] (esm-spec 8.5.1); the param_to_var edge to Streams.wind_rec (declared with the same shape) hands the pair to the stream layer. Read from the synthetic files of tools/gen_synthetic_gswp3.py.",
      "update": {
        "kind": "data",
        "source": "GSWP3_TPQW_Synthetic",
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
      "description": "GSWP3 QBOT: specific humidity at the lowest atmospheric level, as read from the GSWP3_TPQW source. Shaped over the record axis rec, so at time t it receives the pair of records bracketing t, [the record at or before t (CDEPS LB), the next record (UB)] (esm-spec 8.5.1); the param_to_var edge to Streams.shum_rec (declared with the same shape) hands the pair to the stream layer. Read from the synthetic files of tools/gen_synthetic_gswp3.py.",
      "update": {
        "kind": "data",
        "source": "GSWP3_TPQW_Synthetic",
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
      "description": "GSWP3 FLDS: incident longwave radiation, as read from the GSWP3_TPQW source. Shaped over the record axis rec, so at time t it receives the pair of records bracketing t, [the record at or before t (CDEPS LB), the next record (UB)] (esm-spec 8.5.1); the param_to_var edge to Streams.lwdn_rec (declared with the same shape) hands the pair to the stream layer. Read from the synthetic files of tools/gen_synthetic_gswp3.py.",
      "update": {
        "kind": "data",
        "source": "GSWP3_TPQW_Synthetic",
        "from": {
          "file_variable": "FLDS"
        }
      }
    },
    "TOPO": {
      "type": "parameter",
      "units": "m",
      "default": 0.0,
      "description": "GSWP3 TOPO: surface topography height, as read from the static GSWP3_Topo source: declared a scalar (shape []), so it receives the file's single record (esm-spec 8.5.1). Feeds Streams.topo_in. Read from the synthetic files of tools/gen_synthetic_gswp3.py.",
      "shape": [],
      "update": {
        "kind": "data",
        "source": "GSWP3_Topo_Synthetic",
        "from": {
          "file_variable": "TOPO"
        }
      }
    }
  },
  "equations": [],
  "tests": [
    {
      "id": "synthetic_chain_0530",
      "description": "Reads the synthetic GSWP3 files (tools/gen_synthetic_gswp3.py) through the netcdf reader, interpolates them in Streams and derives the exports in Clmncep. t = 05:30Z: TPQW between records 1 (04:30) and 2 (07:30), flb = 2/3; Precip nearest picks record 1; Solar LB record 1 (03Z). Expected values follow from the generator's closed-form record values at cell (lat, lon) = (1, 2) and the same Python transcriptions of the CDEPS laws the law tests use.",
      "time_span": {
        "start": 19800.0,
        "end": 19800.0
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 1e-15
      },
      "assertions": [
        {
          "variable": "Streams.flb_tpqw",
          "time": 19800.0,
          "expected": 0.6666666666666666
        },
        {
          "variable": "Streams.flb_precip",
          "time": 19800.0,
          "expected": 1.0
        },
        {
          "variable": "Streams.flb_solar",
          "time": 19800.0,
          "expected": 0.9998396108711267
        },
        {
          "variable": "Streams.swdn",
          "time": 19800.0,
          "expected": 171.9724130698338
        },
        {
          "variable": "Streams.precn",
          "time": 19800.0,
          "expected": 1.33514404296875e-05
        },
        {
          "variable": "Streams.tbot",
          "time": 19800.0,
          "expected": 273.3333333333333
        },
        {
          "variable": "Streams.pbot",
          "time": 19800.0,
          "expected": 91221.33333333334
        },
        {
          "variable": "Streams.wind",
          "time": 19800.0,
          "expected": 5.166666666666667
        },
        {
          "variable": "Streams.shum",
          "time": 19800.0,
          "expected": 0.006998697916666667
        },
        {
          "variable": "Streams.lwdn",
          "time": 19800.0,
          "expected": 262.6666666666667
        },
        {
          "variable": "Streams.topo",
          "time": 19800.0,
          "expected": 1120
        },
        {
          "variable": "Clmncep.Sa_tbot",
          "time": 19800.0,
          "expected": 273.3333333333333
        },
        {
          "variable": "Clmncep.Sa_pbot",
          "time": 19800.0,
          "expected": 91221.33333333334
        },
        {
          "variable": "Clmncep.Sa_u",
          "time": 19800.0,
          "expected": 3.6533850361304956
        },
        {
          "variable": "Clmncep.Sa_shum",
          "time": 19800.0,
          "expected": 0.004231293430386882
        },
        {
          "variable": "Clmncep.Sa_dens",
          "time": 19800.0,
          "expected": 1.1596917712084673
        },
        {
          "variable": "Clmncep.Sa_topo",
          "time": 19800.0,
          "expected": 1120
        },
        {
          "variable": "Clmncep.Faxa_lwdn",
          "time": 19800.0,
          "expected": 262.6666666666667
        },
        {
          "variable": "Clmncep.Faxa_swndr",
          "time": 19800.0,
          "expected": 53.97565598129927
        },
        {
          "variable": "Clmncep.Faxa_swvdf",
          "time": 19800.0,
          "expected": 48.00283248569796
        },
        {
          "variable": "Clmncep.Faxa_rainc",
          "time": 19800.0,
          "expected": 1.2238820393880462e-07
        },
        {
          "variable": "Clmncep.Faxa_rainl",
          "time": 19800.0,
          "expected": 1.1014938354492414e-06
        },
        {
          "variable": "Clmncep.Faxa_snowc",
          "time": 19800.0,
          "expected": 1.2127558390299454e-06
        },
        {
          "variable": "Clmncep.Faxa_snowl",
          "time": 19800.0,
          "expected": 1.0914802551269508e-05
        }
      ]
    },
    {
      "id": "synthetic_chain_2100",
      "description": "Reads the synthetic GSWP3 files (tools/gen_synthetic_gswp3.py) through the netcdf reader, interpolates them in Streams and derives the exports in Clmncep. t = 21:00Z: TPQW midway between records 6 (19:30) and 7 (22:30), flb = 1/2 (tie in nearest goes to LB); Solar exactly on record 7 (21Z); TBOT ~ 273.6 K, so the rain/snow ramp is mid-way (rain and snow both nonzero). Expected values follow from the generator's closed-form record values at cell (lat, lon) = (1, 2) and the same Python transcriptions of the CDEPS laws the law tests use.",
      "time_span": {
        "start": 75600.0,
        "end": 75600.0
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 1e-15
      },
      "assertions": [
        {
          "variable": "Streams.flb_tpqw",
          "time": 75600.0,
          "expected": 0.5
        },
        {
          "variable": "Streams.flb_precip",
          "time": 75600.0,
          "expected": 1.0
        },
        {
          "variable": "Streams.flb_solar",
          "time": 75600.0,
          "expected": 1.0001727114094672
        },
        {
          "variable": "Streams.swdn",
          "time": 75600.0,
          "expected": 184.03177889934196
        },
        {
          "variable": "Streams.precn",
          "time": 75600.0,
          "expected": 1.811981201171875e-05
        },
        {
          "variable": "Streams.tbot",
          "time": 75600.0,
          "expected": 274.625
        },
        {
          "variable": "Streams.pbot",
          "time": 75600.0,
          "expected": 91304.0
        },
        {
          "variable": "Streams.wind",
          "time": 75600.0,
          "expected": 5.8125
        },
        {
          "variable": "Streams.shum",
          "time": 75600.0,
          "expected": 0.00762939453125
        },
        {
          "variable": "Streams.lwdn",
          "time": 75600.0,
          "expected": 265.25
        },
        {
          "variable": "Streams.topo",
          "time": 75600.0,
          "expected": 1120
        },
        {
          "variable": "Clmncep.Sa_tbot",
          "time": 75600.0,
          "expected": 274.625
        },
        {
          "variable": "Clmncep.Sa_pbot",
          "time": 75600.0,
          "expected": 91304.0
        },
        {
          "variable": "Clmncep.Sa_u",
          "time": 75600.0,
          "expected": 4.110058165646807
        },
        {
          "variable": "Clmncep.Sa_shum",
          "time": 75600.0,
          "expected": 0.004641500193233483
        },
        {
          "variable": "Clmncep.Sa_dens",
          "time": 75600.0,
          "expected": 1.1549960999151696
        },
        {
          "variable": "Clmncep.Sa_topo",
          "time": 75600.0,
          "expected": 1120
        },
        {
          "variable": "Clmncep.Faxa_lwdn",
          "time": 75600.0,
          "expected": 265.25
        },
        {
          "variable": "Clmncep.Faxa_swndr",
          "time": 75600.0,
          "expected": 59.276080484712104
        },
        {
          "variable": "Clmncep.Faxa_swvdf",
          "time": 75600.0,
          "expected": 50.04256255425609
        },
        {
          "variable": "Clmncep.Faxa_rainc",
          "time": 75600.0,
          "expected": 1.3363361358642785e-06
        },
        {
          "variable": "Clmncep.Faxa_rainl",
          "time": 75600.0,
          "expected": 1.2027025222778507e-05
        },
        {
          "variable": "Clmncep.Faxa_snowc",
          "time": 75600.0,
          "expected": 4.756450653075966e-07
        },
        {
          "variable": "Clmncep.Faxa_snowl",
          "time": 75600.0,
          "expected": 4.28080558776837e-06
        }
      ]
    }
  ]
}
```

</details>
