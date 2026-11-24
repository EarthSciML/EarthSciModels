---
title: "GSWP3_Topo_Synthetic"
slug: "gswp3_topo_synthetic"
domains: ["data_models"]
component_types: ["data_source"]
subdomains: ["cdeps"]
domain: "data_models"
subdomain: "cdeps"
component_type: "data_source"
esm_version: "2.0.0"
esm_path: "components/data_models/cdeps/cdeps_datm_gswp3_synthetic.esm"
reference: "https://github.com/ESCOMP/CDEPS"
description: "Data-reading test of the CDEPS DATM GSWP3 chain on SYNTHETIC files: the same reader declarations as the GSWP3Files model of cdeps_datm_gswp3_data.esm (here GSWP3FilesSynthetic, reading sources named *_Synthetic, so the two documents' components and sources keep distinct names), the same Streams/Clmncep laws (mounted from ./cdeps_datm_gswp3.esm) and the same reader -> Streams -> Clmncep coupling edges as cdeps_datm_gswp3_data.esm, with the four data sources pointed at small GSWP3-shaped NetCDF files that tools/gen_synthetic_gswp3.py writes on demand into ./synthetic/ (git-ignored; CI generates them before the inline-test sweeps; no real data is downloaded). The record values are closed-form in the record and cell indices, so the expected values of the reader -> Streams -> Clmncep chain are known exactly. Run `python3 tools/gen_synthetic_gswp3.py` first; needs an esm CLI with data-source support (earthsci-ast-cli built with --features esio)."
tags: ["data_models", "cdeps", "data_source", "datm", "gswp3", "synthetic-data", "test"]
---

## Description

Data-reading test of the CDEPS DATM GSWP3 chain on SYNTHETIC files: the same reader declarations as the GSWP3Files model of cdeps_datm_gswp3_data.esm (here GSWP3FilesSynthetic, reading sources named *_Synthetic, so the two documents' components and sources keep distinct names), the same Streams/Clmncep laws (mounted from ./cdeps_datm_gswp3.esm) and the same reader -> Streams -> Clmncep coupling edges as cdeps_datm_gswp3_data.esm, with the four data sources pointed at small GSWP3-shaped NetCDF files that tools/gen_synthetic_gswp3.py writes on demand into ./synthetic/ (git-ignored; CI generates them before the inline-test sweeps; no real data is downloaded). The record values are closed-form in the record and cell indices, so the expected values of the reader -> Streams -> Clmncep chain are known exactly. Run `python3 tools/gen_synthetic_gswp3.py` first; needs an esm CLI with data-source support (earthsci-ast-cli built with --features esio).

## Reference

- CESM (Community Earth System Model), ESCOMP/CDEPS: Common Data model EXchange Platform source (cdeps1.0.112) - datm/datm_datamode_clmncep_mod.F90, streams/dshr_strdata_mod.F90, streams/dshr_tinterp_mod.F90, share/shr_precip_mod.F90, share/shr_const_mod.F90 - the reference implementation these components are transcribed from.

## Data source

| | |
| --- | --- |
| Kind | `static` |
| URL template | `synthetic/topodata.synthetic.nc` |

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "kind": "static",
  "source": {
    "url_template": "synthetic/topodata.synthetic.nc"
  },
  "select": {
    "axes": [
      "all",
      {
        "fixed": 1
      },
      {
        "fixed": 2
      }
    ]
  },
  "metadata": {
    "esio_format": "netcdf",
    "tags": [
      "topography",
      "static"
    ],
    "description": "Synthetic static topo file (TOPO = 1000 + 100i + 10j)."
  }
}
```

</details>
