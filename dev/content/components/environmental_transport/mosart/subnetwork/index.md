---
title: "Subnetwork"
slug: "subnetwork"
domains: ["environmental_transport"]
component_types: ["model"]
subdomains: ["mosart"]
domain: "environmental_transport"
subdomain: "mosart"
component_type: "model"
esm_version: "2.0.0"
esm_path: "components/environmental_transport/mosart/mosart_subnetwork.esm"
reference: "10.1175/JHM-D-12-015.1"
description: "MOSART subnetwork (tributary) routing step (stage 2 of the EqESM project): the per-cell Euler step 2 of mosart_physics.F90:Euler (F90:114-132) composed of subnetworkRouting (F90:243-269) and updateState_subnetwork (F90:364-381), written as a storage ODE with the pointwise laws imported from ./mosart_templates.esm. Equations, exactly as in the Fortran: with no tributaries (tlen <= hlen) the subnetwork passes the inflow straight through, etout = -etin (F90:250-252); otherwise the Manning velocity vt = CRVRMAN_nosqrt(tslpsqrt, nt, rt) (F90:253) and etout = -vt*mt (F90:254), with the dry-cell clamp etout = -(etin + wt/localdelt) when wt + (etin + etout)*localdelt < TINYVALUE (F90:255-260), in which case vt = -etout/mt when mt > 0 (F90:257-259); dwt = etin + etout (F90:262); d(wt)/dt = dwt (the Fortran advances wt += dwt*localdelt explicitly per substep, F90:123; here a continuous ODE, not the limit of that scheme - see README.md, 'Continuous ODEs vs the Fortran 3600-s Euler stepping'); updateState_subnetwork (F90:370-380) sets mt = GRMR(wt, tlen), yt = GRHT(mt, twidth), pt = GRPT(yt, twidth), rt = GRRR(mt, pt) when tlen > 0 and wt > 0, and zeroes all four otherwise; and the lateral outflow to the main channel erlateral = -etout (the instantaneous value of the Fortran's per-substep accumulation and numDT_t average, F90:125-127). Units per mosart_tstatusflux_type.F90 / mosart_tspatialunit_type.F90: wt [m3]; etin, etout, dwt, erlateral [m3/s]; vt [m/s]; mt [m2]; yt, rt, pt [m]; tslpsqrt [1]; tlen, hlen, twidth [m]; nt is the subnetwork Manning roughness (SI dimension s/m^(1/3)); localdelt = Tctl%DeltaT/DLevelH2R/numDT_t(nr) (F90:120). One deliberate divergence, documented for reviewers: when tlen <= hlen the Fortran leaves vt stale (it is unused in that branch) while here vt always takes the Manning value; and when the dry-cell clamp fires with mt <= 0 the Fortran also leaves vt at the Manning value, which is what the ifelse expresses. The tests block pins the geometry chain GRMR/GRHT/GRPT/GRRR pointwise (instantaneous tests, time_span {0,0}) and the one-substep storage traces in the continuous-ODE form, with numeric tuples from the EqESM instrumented-CESM dumps (stage1/dumps/mosart/ dry lane window: gr_subnet.csv, crvrman_trib.csv, mosart_euler.csv; stage1/dumps/mosart_wet/ wet window: wet_geometry_* and wet_manning_trib_* pins); the trace assertions carry the measured Euler-vs-continuous scheme gaps (see README.md (Testing)). Reference: stage1/cesm/components/mosart/src/riverroute/mosart_physics.F90 (mosart1.1.13)."
tags: ["environmental_transport", "mosart", "model", "river-routing", "hydrology", "subnetwork", "tributary", "manning", "cesm"]
---

## Description

MOSART subnetwork (tributary) routing step (stage 2 of the EqESM project): the per-cell Euler step 2 of mosart_physics.F90:Euler (F90:114-132) composed of subnetworkRouting (F90:243-269) and updateState_subnetwork (F90:364-381), written as a storage ODE with the pointwise laws imported from ./mosart_templates.esm. Equations, exactly as in the Fortran: with no tributaries (tlen <= hlen) the subnetwork passes the inflow straight through, etout = -etin (F90:250-252); otherwise the Manning velocity vt = CRVRMAN_nosqrt(tslpsqrt, nt, rt) (F90:253) and etout = -vt*mt (F90:254), with the dry-cell clamp etout = -(etin + wt/localdelt) when wt + (etin + etout)*localdelt < TINYVALUE (F90:255-260), in which case vt = -etout/mt when mt > 0 (F90:257-259); dwt = etin + etout (F90:262); d(wt)/dt = dwt (the Fortran advances wt += dwt*localdelt explicitly per substep, F90:123; here a continuous ODE, not the limit of that scheme - see README.md, 'Continuous ODEs vs the Fortran 3600-s Euler stepping'); updateState_subnetwork (F90:370-380) sets mt = GRMR(wt, tlen), yt = GRHT(mt, twidth), pt = GRPT(yt, twidth), rt = GRRR(mt, pt) when tlen > 0 and wt > 0, and zeroes all four otherwise; and the lateral outflow to the main channel erlateral = -etout (the instantaneous value of the Fortran's per-substep accumulation and numDT_t average, F90:125-127). Units per mosart_tstatusflux_type.F90 / mosart_tspatialunit_type.F90: wt [m3]; etin, etout, dwt, erlateral [m3/s]; vt [m/s]; mt [m2]; yt, rt, pt [m]; tslpsqrt [1]; tlen, hlen, twidth [m]; nt is the subnetwork Manning roughness (SI dimension s/m^(1/3)); localdelt = Tctl%DeltaT/DLevelH2R/numDT_t(nr) (F90:120). One deliberate divergence, documented for reviewers: when tlen <= hlen the Fortran leaves vt stale (it is unused in that branch) while here vt always takes the Manning value; and when the dry-cell clamp fires with mt <= 0 the Fortran also leaves vt at the Manning value, which is what the ifelse expresses. The tests block pins the geometry chain GRMR/GRHT/GRPT/GRRR pointwise (instantaneous tests, time_span {0,0}) and the one-substep storage traces in the continuous-ODE form, with numeric tuples from the EqESM instrumented-CESM dumps (stage1/dumps/mosart/ dry lane window: gr_subnet.csv, crvrman_trib.csv, mosart_euler.csv; stage1/dumps/mosart_wet/ wet window: wet_geometry_* and wet_manning_trib_* pins); the trace assertions carry the measured Euler-vs-continuous scheme gaps (see README.md (Testing)). Reference: stage1/cesm/components/mosart/src/riverroute/mosart_physics.F90 (mosart1.1.13).

## Reference

- Li, H., Wigmosta, M. S., Wu, H., Huang, M., Ke, Y., Coleman, A. M., and Leung, L. R. (2013). A physically based runoff routing model for land surface and earth system models. Journal of Hydrometeorology, 14(3), 808-828. The MOSART (Model for Scale Adaptive River Transport) routing scheme these components transcribe.
- CESM (Community Earth System Model), ESCOMP/CESM, cesm3.0-alphabranch: MOSART river-routing source (mosart1.1.13) - mosart_physics.F90, mosart_driver.F90, mosart_tstatusflux_type.F90, mosart_tspatialunit_type.F90, rof_comp_nuopc/rof_import_export.F90 - the reference implementation these components are transcribed from.
- EarthSciModels - the authoritative .esm corpus this component lives in.

## Variables

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `wt` | `m^3` | `0.0` | storage of surface water in the subnetwork (TRunoff%wt), [m3] |

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `etin` | `m^3/s` | `0.0` | lateral inflow from the hillslope, including surface and subsurface runoff generation components (TRunoff%etin, computed by the hillslope step), [m3/s] |
| `tslpsqrt` | `1` | `0.01` | sqrt of the average slope of the tributaries (TUnit%tslpsqrt, from frivinp tslp), [-] |
| `nt` | `s/m^(1/3)` | `0.03` | Manning's roughness of the subnetwork at the hillslope (TUnit%nt, from frivinp); network file stores a bare number; declared with its SI dimension s/m^(1/3) for dimensional consistency |
| `tlen` | `m` | `1000.0` | length of all sub-network reaches within the cell (TUnit%tlen, from frivinp), [m] |
| `hlen` | `m` | `500.0` | length of the hillslope within the cell (TUnit%hlen); the Fortran branch condition tlen <= hlen selects cells with no tributaries (F90:250), [m] |
| `twidth` | `m` | `10.0` | bankfull width of the sub-reach (TUnit%twidth, from frivinp twid), [m] |
| `localdelt` | `s` | `180.0` | local subnetwork substep = Tctl%DeltaT/DLevelH2R/numDT_t(nr) (F90:120), [s] |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `dwt` | `m^3/s` |  | change of subnetwork water storage (TRunoff%dwt) = etin + etout; the Fortran type comment says [m3] but the code assigns etin + etout [m3/s] and advances wt += dwt*localdelt, so the rate reading is the code's, [m3/s] |
| `etout_manning` | `m^3/s` |  | unclamped discharge from the subnetwork into the main reach, -vt*mt, [m3/s] |
| `etout` | `m^3/s` |  | discharge from the subnetwork into the main reach after the no-tributary branch and the dry-cell clamp (TRunoff%etout), [m3/s] |
| `vt_manning` | `m/s` |  | Manning velocity of the tributary flow CRVRMAN_nosqrt(tslpsqrt, nt, rt), [m/s] |
| `vt` | `m/s` |  | tributary flow velocity (TRunoff%vt): -etout/mt when the dry-cell clamp fired and mt > 0, the Manning value otherwise, [m/s] |
| `mt` | `m^2` |  | wetted cross-section area of the subnetwork (TRunoff%mt), [m2] |
| `yt` | `m` |  | water depth of the subnetwork (TRunoff%yt), [m] |
| `pt` | `m` |  | wetted perimeter of the subnetwork (TRunoff%pt), [m] |
| `rt` | `m` |  | hydraulic radius of the subnetwork (TRunoff%rt), [m] |
| `erlateral` | `m^3/s` |  | lateral flow from the subnetwork into the main reach (TRunoff%erlateral) = -etout, the instantaneous value of the Fortran's per-substep accumulation and numDT_t average (F90:125-127), [m3/s] |

## Observed expressions

$$
dwt = etin + etout
$$
_change of subnetwork water storage (TRunoff%dwt) = etin + etout; the Fortran type comment says [m3] but the code assigns etin + etout [m3/s] and advances wt += dwt*localdelt, so the rate reading is the code's, [m3/s]_

$$
etout_{manning} = \left(-vt_{manning}\right) \cdot mt
$$
_unclamped discharge from the subnetwork into the main reach, -vt*mt, [m3/s]_

$$
etout = \mathrm{ifelse}\left(\mathrm{<=}\left(tlen, hlen\right), -etin, \mathrm{ifelse}\left(\mathrm{<}\left(wt + \left(etin + etout_{manning}\right) \cdot localdelt, \mathrm{const}\left(\right)\right), -\left(etin + \frac{wt}{localdelt}\right), etout_{manning}\right)\right)
$$
_discharge from the subnetwork into the main reach after the no-tributary branch and the dry-cell clamp (TRunoff%etout), [m3/s]_

$$
vt_{manning} = \mathrm{manning_velocity}\left(sqrtslp=tslpsqrt, n=nt, rr=rt\right)
$$
_Manning velocity of the tributary flow CRVRMAN_nosqrt(tslpsqrt, nt, rt), [m/s]_

$$
vt = \mathrm{ifelse}\left(\mathrm{and}\left(\mathrm{>}\left(tlen, hlen\right), \mathrm{and}\left(\mathrm{<}\left(wt + \left(etin + etout_{manning}\right) \cdot localdelt, \mathrm{const}\left(\right)\right), \mathrm{>}\left(mt, 0.0\right)\right)\right), \frac{-etout}{mt}, vt_{manning}\right)
$$
_tributary flow velocity (TRunoff%vt): -etout/mt when the dry-cell clamp fired and mt > 0, the Manning value otherwise, [m/s]_

$$
mt = \mathrm{ifelse}\left(\mathrm{and}\left(\mathrm{>}\left(tlen, 0.0\right), \mathrm{>}\left(wt, 0.0\right)\right), \mathrm{wetted_area}\left(w=wt, len=tlen\right), 0.0\right)
$$
_wetted cross-section area of the subnetwork (TRunoff%mt), [m2]_

$$
yt = \mathrm{ifelse}\left(\mathrm{and}\left(\mathrm{>}\left(tlen, 0.0\right), \mathrm{>}\left(wt, 0.0\right)\right), \mathrm{rectangular_depth}\left(m=mt, twid=twidth\right), 0.0\right)
$$
_water depth of the subnetwork (TRunoff%yt), [m]_

$$
pt = \mathrm{ifelse}\left(\mathrm{and}\left(\mathrm{>}\left(tlen, 0.0\right), \mathrm{>}\left(wt, 0.0\right)\right), \mathrm{rectangular_perimeter}\left(h=yt, twid=twidth\right), 0.0\right)
$$
_wetted perimeter of the subnetwork (TRunoff%pt), [m]_

$$
rt = \mathrm{ifelse}\left(\mathrm{and}\left(\mathrm{>}\left(tlen, 0.0\right), \mathrm{>}\left(wt, 0.0\right)\right), \mathrm{hydraulic_radius}\left(area=mt, p=pt\right), 0.0\right)
$$
_hydraulic radius of the subnetwork (TRunoff%rt), [m]_

$$
erlateral = -etout
$$
_lateral flow from the subnetwork into the main reach (TRunoff%erlateral) = -etout, the instantaneous value of the Fortran's per-substep accumulation and numDT_t average (F90:125-127), [m3/s]_

## Equations

$$
\mathrm{D}\left(wt\right) = dwt
$$

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "expression_template_imports": [
    {
      "ref": "./mosart_templates.esm"
    }
  ],
  "variables": {
    "wt": {
      "type": "unknown",
      "units": "m^3",
      "default": 0.0,
      "description": "storage of surface water in the subnetwork (TRunoff%wt), [m3]"
    },
    "dwt": {
      "type": "unknown",
      "units": "m^3/s",
      "description": "change of subnetwork water storage (TRunoff%dwt) = etin + etout; the Fortran type comment says [m3] but the code assigns etin + etout [m3/s] and advances wt += dwt*localdelt, so the rate reading is the code's, [m3/s]"
    },
    "etout_manning": {
      "type": "unknown",
      "units": "m^3/s",
      "description": "unclamped discharge from the subnetwork into the main reach, -vt*mt, [m3/s]"
    },
    "etout": {
      "type": "unknown",
      "units": "m^3/s",
      "description": "discharge from the subnetwork into the main reach after the no-tributary branch and the dry-cell clamp (TRunoff%etout), [m3/s]"
    },
    "vt_manning": {
      "type": "unknown",
      "units": "m/s",
      "description": "Manning velocity of the tributary flow CRVRMAN_nosqrt(tslpsqrt, nt, rt), [m/s]"
    },
    "vt": {
      "type": "unknown",
      "units": "m/s",
      "description": "tributary flow velocity (TRunoff%vt): -etout/mt when the dry-cell clamp fired and mt > 0, the Manning value otherwise, [m/s]"
    },
    "mt": {
      "type": "unknown",
      "units": "m^2",
      "description": "wetted cross-section area of the subnetwork (TRunoff%mt), [m2]"
    },
    "yt": {
      "type": "unknown",
      "units": "m",
      "description": "water depth of the subnetwork (TRunoff%yt), [m]"
    },
    "pt": {
      "type": "unknown",
      "units": "m",
      "description": "wetted perimeter of the subnetwork (TRunoff%pt), [m]"
    },
    "rt": {
      "type": "unknown",
      "units": "m",
      "description": "hydraulic radius of the subnetwork (TRunoff%rt), [m]"
    },
    "erlateral": {
      "type": "unknown",
      "units": "m^3/s",
      "description": "lateral flow from the subnetwork into the main reach (TRunoff%erlateral) = -etout, the instantaneous value of the Fortran's per-substep accumulation and numDT_t average (F90:125-127), [m3/s]"
    },
    "etin": {
      "type": "parameter",
      "units": "m^3/s",
      "default": 0.0,
      "description": "lateral inflow from the hillslope, including surface and subsurface runoff generation components (TRunoff%etin, computed by the hillslope step), [m3/s]"
    },
    "tslpsqrt": {
      "type": "parameter",
      "units": "1",
      "default": 0.01,
      "description": "sqrt of the average slope of the tributaries (TUnit%tslpsqrt, from frivinp tslp), [-]"
    },
    "nt": {
      "type": "parameter",
      "units": "s/m^(1/3)",
      "default": 0.03,
      "description": "Manning's roughness of the subnetwork at the hillslope (TUnit%nt, from frivinp); network file stores a bare number; declared with its SI dimension s/m^(1/3) for dimensional consistency"
    },
    "tlen": {
      "type": "parameter",
      "units": "m",
      "default": 1000.0,
      "description": "length of all sub-network reaches within the cell (TUnit%tlen, from frivinp), [m]"
    },
    "hlen": {
      "type": "parameter",
      "units": "m",
      "default": 500.0,
      "description": "length of the hillslope within the cell (TUnit%hlen); the Fortran branch condition tlen <= hlen selects cells with no tributaries (F90:250), [m]"
    },
    "twidth": {
      "type": "parameter",
      "units": "m",
      "default": 10.0,
      "description": "bankfull width of the sub-reach (TUnit%twidth, from frivinp twid), [m]"
    },
    "localdelt": {
      "type": "parameter",
      "units": "s",
      "default": 180.0,
      "description": "local subnetwork substep = Tctl%DeltaT/DLevelH2R/numDT_t(nr) (F90:120), [s]"
    }
  },
  "equations": [
    {
      "lhs": "vt_manning",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "manning_velocity",
        "bindings": {
          "sqrtslp": "tslpsqrt",
          "n": "nt",
          "rr": "rt"
        }
      }
    },
    {
      "lhs": "etout_manning",
      "rhs": {
        "op": "*",
        "args": [
          {
            "op": "-",
            "args": [
              "vt_manning"
            ]
          },
          "mt"
        ]
      }
    },
    {
      "lhs": "etout",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "<=",
            "args": [
              "tlen",
              "hlen"
            ]
          },
          {
            "op": "-",
            "args": [
              "etin"
            ]
          },
          {
            "op": "ifelse",
            "args": [
              {
                "op": "<",
                "args": [
                  {
                    "op": "+",
                    "args": [
                      "wt",
                      {
                        "op": "*",
                        "args": [
                          {
                            "op": "+",
                            "args": [
                              "etin",
                              "etout_manning"
                            ]
                          },
                          "localdelt"
                        ]
                      }
                    ]
                  },
                  {
                    "op": "const",
                    "args": [],
                    "value": 1e-14,
                    "units": "m^3"
                  }
                ]
              },
              {
                "op": "-",
                "args": [
                  {
                    "op": "+",
                    "args": [
                      "etin",
                      {
                        "op": "/",
                        "args": [
                          "wt",
                          "localdelt"
                        ]
                      }
                    ]
                  }
                ]
              },
              "etout_manning"
            ]
          }
        ]
      }
    },
    {
      "lhs": "vt",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "and",
            "args": [
              {
                "op": ">",
                "args": [
                  "tlen",
                  "hlen"
                ]
              },
              {
                "op": "and",
                "args": [
                  {
                    "op": "<",
                    "args": [
                      {
                        "op": "+",
                        "args": [
                          "wt",
                          {
                            "op": "*",
                            "args": [
                              {
                                "op": "+",
                                "args": [
                                  "etin",
                                  "etout_manning"
                                ]
                              },
                              "localdelt"
                            ]
                          }
                        ]
                      },
                      {
                        "op": "const",
                        "args": [],
                        "value": 1e-14,
                        "units": "m^3"
                      }
                    ]
                  },
                  {
                    "op": ">",
                    "args": [
                      "mt",
                      0.0
                    ]
                  }
                ]
              }
            ]
          },
          {
            "op": "/",
            "args": [
              {
                "op": "-",
                "args": [
                  "etout"
                ]
              },
              "mt"
            ]
          },
          "vt_manning"
        ]
      }
    },
    {
      "lhs": "dwt",
      "rhs": {
        "op": "+",
        "args": [
          "etin",
          "etout"
        ]
      }
    },
    {
      "lhs": {
        "op": "D",
        "args": [
          "wt"
        ],
        "wrt": "t"
      },
      "rhs": "dwt"
    },
    {
      "lhs": "mt",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "and",
            "args": [
              {
                "op": ">",
                "args": [
                  "tlen",
                  0.0
                ]
              },
              {
                "op": ">",
                "args": [
                  "wt",
                  0.0
                ]
              }
            ]
          },
          {
            "op": "apply_expression_template",
            "args": [],
            "name": "wetted_area",
            "bindings": {
              "w": "wt",
              "len": "tlen"
            }
          },
          0.0
        ]
      }
    },
    {
      "lhs": "yt",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "and",
            "args": [
              {
                "op": ">",
                "args": [
                  "tlen",
                  0.0
                ]
              },
              {
                "op": ">",
                "args": [
                  "wt",
                  0.0
                ]
              }
            ]
          },
          {
            "op": "apply_expression_template",
            "args": [],
            "name": "rectangular_depth",
            "bindings": {
              "m": "mt",
              "twid": "twidth"
            }
          },
          0.0
        ]
      }
    },
    {
      "lhs": "pt",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "and",
            "args": [
              {
                "op": ">",
                "args": [
                  "tlen",
                  0.0
                ]
              },
              {
                "op": ">",
                "args": [
                  "wt",
                  0.0
                ]
              }
            ]
          },
          {
            "op": "apply_expression_template",
            "args": [],
            "name": "rectangular_perimeter",
            "bindings": {
              "h": "yt",
              "twid": "twidth"
            }
          },
          0.0
        ]
      }
    },
    {
      "lhs": "rt",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "and",
            "args": [
              {
                "op": ">",
                "args": [
                  "tlen",
                  0.0
                ]
              },
              {
                "op": ">",
                "args": [
                  "wt",
                  0.0
                ]
              }
            ]
          },
          {
            "op": "apply_expression_template",
            "args": [],
            "name": "hydraulic_radius",
            "bindings": {
              "area": "mt",
              "p": "pt"
            }
          },
          0.0
        ]
      }
    },
    {
      "lhs": "erlateral",
      "rhs": {
        "op": "-",
        "args": [
          "etout"
        ]
      }
    }
  ],
  "tests": [
    {
      "id": "geometry_chain_cell100312",
      "description": "Instantaneous pin of the subnetwork geometry chain GRMR/GRHT/GRPT/GRRR (mosart_physics.F90:441-497) from stage1/dumps/mosart/gr_subnet.csv row (step 8, ns 3, m 5, k 4, gindex 100312): wt = 3.97311021312352278e-05 m3, tlen = 8.34171976659353095e+03 m, twidth = 8.16804371744665605e+03 m give mt = wt/tlen = 4.76293896737555222e-09 m2, yt = mt/twidth = 5.83118691835853067e-13 m, pt = twidth + 2*yt = 8.16804371744665696e+03 m, rt = mt/pt = 5.83118691835852966e-13 m (all above TINYVALUE, so every nonzero branch of the ifelse guards is exercised). The Fortran values are reproduced to round-off (rel 1e-12).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "tlen": 8341.719766593531,
        "twidth": 8168.043717446656
      },
      "initial_conditions": {
        "wt": 3.973110213123523e-05
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 1e-24
      },
      "assertions": [
        {
          "variable": "mt",
          "time": 0.0,
          "expected": 4.762938967375552e-09
        },
        {
          "variable": "yt",
          "time": 0.0,
          "expected": 5.831186918358531e-13
        },
        {
          "variable": "pt",
          "time": 0.0,
          "expected": 8168.043717446657
        },
        {
          "variable": "rt",
          "time": 0.0,
          "expected": 5.83118691835853e-13
        }
      ]
    },
    {
      "id": "geometry_chain_cell101032",
      "description": "Instantaneous pin of the geometry chain from gr_subnet.csv row (step 8, ns 3, m 5, k 4, gindex 101032), a narrower tributary: wt = 4.17603130711973979e-05 m3, tlen = 2.53029464608684866e+04 m, twidth = 1.96594306825645049e+03 m give mt = 1.65041305113539083e-09 m2, yt = 8.39501955974291802e-13 m, pt = 1.96594306825645208e+03 m, rt = 8.39501955974291095e-13 m (note rt differs from yt in the last two digits: the chain is not degenerate).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "tlen": 25302.946460868487,
        "twidth": 1965.9430682564505
      },
      "initial_conditions": {
        "wt": 4.17603130711974e-05
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 1e-24
      },
      "assertions": [
        {
          "variable": "mt",
          "time": 0.0,
          "expected": 1.6504130511353908e-09
        },
        {
          "variable": "yt",
          "time": 0.0,
          "expected": 8.395019559742918e-13
        },
        {
          "variable": "pt",
          "time": 0.0,
          "expected": 1965.943068256452
        },
        {
          "variable": "rt",
          "time": 0.0,
          "expected": 8.395019559742911e-13
        }
      ]
    },
    {
      "id": "geometry_chain_tiny_depth_guard",
      "description": "TINYVALUE guard pin from gr_subnet.csv row (step 1, ns 2, m 5, k 4, gindex 100312): at wt = 2.93836914884621747e-07 m3 the chain computes mt = 3.52249803525364102e-11 m2 and yt = 4.31253572716525559e-15 m (mt > TINYVALUE so GRHT is taken, yt > 0), but yt <= TINYVALUE zeroes the wetted perimeter GRPT and hence the hydraulic radius GRRR: pt = 0 and rt = 0 exactly as in the Fortran (GRPT F90:471-479, GRRR F90:489-495).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "tlen": 8341.719766593531,
        "twidth": 8168.043717446656
      },
      "initial_conditions": {
        "wt": 2.9383691488462175e-07
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 1e-24
      },
      "assertions": [
        {
          "variable": "mt",
          "time": 0.0,
          "expected": 3.522498035253641e-11
        },
        {
          "variable": "yt",
          "time": 0.0,
          "expected": 4.3125357271652556e-15
        },
        {
          "variable": "pt",
          "time": 0.0,
          "expected": 0.0
        },
        {
          "variable": "rt",
          "time": 0.0,
          "expected": 0.0
        }
      ]
    },
    {
      "id": "geometry_chain_dry",
      "description": "Dry-cell guard pin from gr_subnet.csv row (step 0, ns 0, m 0, nt 1, gindex 100312): with wt = 0 the updateState_subnetwork guard (tlen > 0 and wt > 0) zeroes the whole geometry chain - mt = yt = pt = rt = 0 (F90:370-380).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "tlen": 8341.719766593531,
        "twidth": 8168.043717446656
      },
      "initial_conditions": {
        "wt": 0.0
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 1e-24
      },
      "assertions": [
        {
          "variable": "mt",
          "time": 0.0,
          "expected": 0.0
        },
        {
          "variable": "yt",
          "time": 0.0,
          "expected": 0.0
        },
        {
          "variable": "pt",
          "time": 0.0,
          "expected": 0.0
        },
        {
          "variable": "rt",
          "time": 0.0,
          "expected": 0.0
        }
      ]
    },
    {
      "id": "manning_velocity_cell100312",
      "description": "Instantaneous pin of the subnetwork Manning law CRVRMAN_nosqrt (F90:406-422) through the full geometry chain: crvrman_trib.csv row (step 8, ns 3, m 5, k 4, gindex 100312) records rt = 5.81773231372646289e-13 m, vt = 1.38680929192335890e-08 m/s, mt = 4.75194918749198407e-09 m2 with tslpsqrt = 9.94987437106620021e-02, n_t = 5.00000007450580597e-02; the matching gr_subnet.csv row (k 3) carries the storage wt = 3.96394284671499548e-05 m3 that produces exactly that rt through GRMR/GRHT/GRPT/GRRR. The test sets wt and asserts both the chain output rt and the law output vt_manning (= the dump's vt; the dry-cell clamp does not fire at this storage), reproducing the Fortran to round-off.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "tslpsqrt": 0.099498743710662,
        "nt": 0.05000000074505806,
        "tlen": 8341.719766593531,
        "twidth": 8168.043717446656,
        "localdelt": 180.0
      },
      "initial_conditions": {
        "wt": 3.9639428467149955e-05
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 1e-24
      },
      "assertions": [
        {
          "variable": "mt",
          "time": 0.0,
          "expected": 4.751949187491984e-09
        },
        {
          "variable": "rt",
          "time": 0.0,
          "expected": 5.817732313726463e-13
        },
        {
          "variable": "vt_manning",
          "time": 0.0,
          "expected": 1.3868092919233589e-08
        },
        {
          "variable": "vt",
          "time": 0.0,
          "expected": 1.3868092919233589e-08
        }
      ]
    },
    {
      "id": "manning_velocity_cell101032",
      "description": "Instantaneous pin of the Manning law from crvrman_trib.csv row (step 8, ns 3, m 5, k 4, gindex 101032): rt = 8.37564932353432923e-13 m, vt = 2.51318221409314064e-09 m/s with tslpsqrt = 1.41421356237309507e-02, n_t = 5.00000007450580597e-02; the matching gr_subnet.csv row (k 3) gives wt = 4.16639574733840902e-05 m3, tlen = 2.53029464608684866e+04 m, twidth = 1.96594306825645049e+03 m.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "tslpsqrt": 0.01414213562373095,
        "nt": 0.05000000074505806,
        "tlen": 25302.946460868487,
        "twidth": 1965.9430682564505,
        "localdelt": 180.0
      },
      "initial_conditions": {
        "wt": 4.166395747338409e-05
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 1e-24
      },
      "assertions": [
        {
          "variable": "rt",
          "time": 0.0,
          "expected": 8.375649323534329e-13
        },
        {
          "variable": "vt_manning",
          "time": 0.0,
          "expected": 2.5131822140931406e-09
        },
        {
          "variable": "vt",
          "time": 0.0,
          "expected": 2.5131822140931406e-09
        }
      ]
    },
    {
      "id": "manning_velocity_dry_guard",
      "description": "Dry-cell law guard from crvrman_trib.csv row (step 1, ns 1, m 1, k 1, gindex 100312, clamped = 1): with wt = 0 the geometry chain zeroes mt and rt, the rr <= 0 guard zeroes the Manning velocity (vt_manning = 0), and the dry-cell clamp of subnetworkRouting (F90:255-260) fires (wt + (etin + etout)*localdelt = 0 < TINYVALUE) replacing etout by -(etin + wt/localdelt) = -0 and leaving vt at the Manning value 0 (mt <= 0 keeps the clamp's vt override off).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "tslpsqrt": 0.099498743710662,
        "nt": 0.05000000074505806,
        "tlen": 8341.719766593531,
        "twidth": 8168.043717446656,
        "localdelt": 180.0
      },
      "initial_conditions": {
        "wt": 0.0
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 1e-24
      },
      "assertions": [
        {
          "variable": "mt",
          "time": 0.0,
          "expected": 0.0
        },
        {
          "variable": "rt",
          "time": 0.0,
          "expected": 0.0
        },
        {
          "variable": "vt_manning",
          "time": 0.0,
          "expected": 0.0
        },
        {
          "variable": "vt",
          "time": 0.0,
          "expected": 0.0
        },
        {
          "variable": "etout",
          "time": 0.0,
          "expected": 0.0
        }
      ]
    },
    {
      "id": "one_step_growth_step2_sub1",
      "description": "One-substep trace over [0, 3600] (one Euler substep = one DLevelH2R x numDT_t cascade): entry (step 2, ns 1, gindex 100312) wt = 1.22671012572302206e-06 m3 with etin = 5.09336561109318995e-10 m3/s (the substep's lateral inflow, mosart_euler.csv row (2,1,exit)); the exit state is wt = 3.06032174388425321e-06 m3. localdelt = 180 s = delt/DLevelH2R/numDT_t with DLevelH2R = 5 and numDT_t = 4 (the dump's 4 rows per (step,ns,m,gindex) key; phi_t < 10 in the CFL rule). The .esm integrates d(wt)/dt = etin + etout(wt) continuously while the Fortran left-sums the Manning outflow over 20 Euler substeps of 180 s; the measured scheme gap on wt (solver at reltol 1e-14) is ~6e-17 m3 abs = 2e-11 rel of the end state (the etout term is ~1e-8 of etin here) - the rel 1e-6 bound is 2-5x the measured gap. etout at time 0 pins the entry-state outflow = -1.88446035662946316e-19 m3/s (the value the Fortran's first sub-step evaluates).",
      "time_span": {
        "start": 0.0,
        "end": 3600.0
      },
      "parameter_overrides": {
        "etin": 5.09336561109319e-10,
        "tslpsqrt": 0.099498743710662,
        "nt": 0.05000000074505806,
        "tlen": 8341.719766593531,
        "twidth": 8168.043717446656,
        "hlen": 500.0,
        "localdelt": 180.0
      },
      "initial_conditions": {
        "wt": 1.226710125723022e-06
      },
      "tolerance": {
        "rel": 1e-06,
        "abs": 1e-15
      },
      "assertions": [
        {
          "variable": "wt",
          "time": 3600.0,
          "expected": 3.060321743884253e-06
        },
        {
          "variable": "etout",
          "time": 0.0,
          "expected": -1.8844603566294632e-19
        }
      ]
    },
    {
      "id": "wet_geometry_cell217950",
      "description": "Instantaneous pin of the wet subnetwork geometry chain mt = GRMR(wt,tlen), yt = GRHT(mt,twidth), pt = GRPT(yt,twidth), rt = GRRR(mt,pt) (mosart_physics.F90:104-119) on the cell-217950 subnetwork after the first numDT_t substep of coupling step 1, ns 1, from stage1/dumps/mosart_wet/gr_subnet.csv row (step 1, ns 1, m 1, gindex 217950): wt = 3162.2739530139029 m3 (the tributary fills with etin = 17.568188627855015 m3/s over localdelt_t = 180 s) gives mt = wt/tlen = 0.2161250997158731 m2, yt = mt/twidth = 5.6441803202263181e-05 m, pt = twidth + 2*yt = 3829.1672807250302 m and rt = mt/pt = 5.6441801538362434e-05 m, all nonzero (wet-window branch; the dry guard yt = 0 is not hit). Expected values are the dumped outputs of the EqESM instrumented-CESM wet window (CESM run, not a standalone driver). time_span {0,0}; rel 1e-12.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "tlen": 14631.683026039815,
        "twidth": 3829.1671678414236
      },
      "initial_conditions": {
        "wt": 3162.273953013903
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 1e-24
      },
      "assertions": [
        {
          "variable": "mt",
          "time": 0.0,
          "expected": 0.2161250997158731
        },
        {
          "variable": "yt",
          "time": 0.0,
          "expected": 5.644180320226318e-05
        },
        {
          "variable": "pt",
          "time": 0.0,
          "expected": 3829.16728072503
        },
        {
          "variable": "rt",
          "time": 0.0,
          "expected": 5.6441801538362434e-05
        }
      ]
    },
    {
      "id": "wet_geometry_cell208214",
      "description": "Instantaneous pin of the wet subnetwork geometry chain on the cell-208214 subnetwork, from stage1/dumps/mosart_wet/gr_subnet.csv row (step 1, ns 1, m 1, gindex 208214): wt = 428.59175773750707 m3 gives mt = wt/tlen = 0.063474578317007146 m2, yt = mt/twidth = 1.8926221008805886e-05 m, pt = twidth + 2*yt = 3353.7904372921425 m and rt = mt/pt = 1.8926220795195734e-05 m (wet-window branch). Expected values are the dumped outputs of the EqESM instrumented-CESM wet window (CESM run, not a standalone driver). time_span {0,0}; rel 1e-12.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "tlen": 6752.179677303532,
        "twidth": 3353.7903994397006
      },
      "initial_conditions": {
        "wt": 428.59175773750707
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 1e-24
      },
      "assertions": [
        {
          "variable": "mt",
          "time": 0.0,
          "expected": 0.06347457831700715
        },
        {
          "variable": "yt",
          "time": 0.0,
          "expected": 1.8926221008805886e-05
        },
        {
          "variable": "pt",
          "time": 0.0,
          "expected": 3353.7904372921425
        },
        {
          "variable": "rt",
          "time": 0.0,
          "expected": 1.8926220795195734e-05
        }
      ]
    },
    {
      "id": "wet_manning_trib_cell217950",
      "description": "Instantaneous pin of the wet tributary Manning law (subnetworkRouting, mosart_physics.F90:120-143) on the cell-217950 subnetwork at its first flowing substep, from stage1/dumps/mosart_wet/crvrman_trib.csv row (step 1, ns 1, m 1, substep k=2 of numDT_t = 4, gindex 217950): wt = mt*tlen = 3162.2739530139029 m3 (recovered from the dumped pre-update mt = 0.2161250997158731 m2) gives rt = mt/(twidth + 2*yt) = 5.6441801538362434e-05 m; the wet Manning law returns vt = CRVRMAN_nosqrt(tslpsqrt, n_t, rt) = 0.00036500900904041633 m/s and etout = -vt*mt = -7.8887608476052007e-05 m3/s (tlen > hlen and the dry-cell clamp cannot fire: wt + (etin + etout)*localdelt > 0), so dwt = etin + etout = 17.568188627855015 - 7.8887608476052007e-05 = 17.568109740246538 m3/s. Expected values are the dumped outputs of the EqESM instrumented-CESM wet window (CESM run, not a standalone driver). time_span {0,0}; rel 1e-12.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "tslpsqrt": 0.01,
        "nt": 0.040311627089977264,
        "tlen": 14631.683026039815,
        "twidth": 3829.1671678414236,
        "etin": 17.568188627855015,
        "localdelt": 180.0
      },
      "initial_conditions": {
        "wt": 3162.273953013903
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 1e-24
      },
      "assertions": [
        {
          "variable": "rt",
          "time": 0.0,
          "expected": 5.6441801538362434e-05
        },
        {
          "variable": "vt",
          "time": 0.0,
          "expected": 0.0003650090090404163
        },
        {
          "variable": "etout",
          "time": 0.0,
          "expected": -7.888760847605201e-05
        },
        {
          "variable": "dwt",
          "time": 0.0,
          "expected": 17.568109740246538
        }
      ]
    },
    {
      "id": "wet_manning_trib_cell208214",
      "description": "Instantaneous pin of the wet tributary Manning law on the cell-208214 subnetwork at its first flowing substep, from stage1/dumps/mosart_wet/crvrman_trib.csv row (step 1, ns 1, m 1, substep k=2 of numDT_t = 4, gindex 208214): wt = mt*tlen = 428.59175773750707 m3 (mt = 0.063474578317007146 m2) gives rt = 1.8926220795195734e-05 m, vt = CRVRMAN_nosqrt(tslpsqrt, n_t, rt) = 0.00025166376699942622 m/s and etout = -vt*mt = -1.5974251487958117e-05 m3/s, so dwt = etin + etout = 2.3810653207639283 - 1.5974251487958117e-05 = 2.3810493465124405 m3/s. Expected values are the dumped outputs of the EqESM instrumented-CESM wet window (CESM run, not a standalone driver). time_span {0,0}; rel 1e-12.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "tslpsqrt": 0.017320508075688773,
        "nt": 0.048878274857997894,
        "tlen": 6752.179677303532,
        "twidth": 3353.7903994397006,
        "etin": 2.3810653207639283,
        "localdelt": 180.0
      },
      "initial_conditions": {
        "wt": 428.59175773750707
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 1e-24
      },
      "assertions": [
        {
          "variable": "rt",
          "time": 0.0,
          "expected": 1.8926220795195734e-05
        },
        {
          "variable": "vt",
          "time": 0.0,
          "expected": 0.0002516637669994262
        },
        {
          "variable": "etout",
          "time": 0.0,
          "expected": -1.5974251487958117e-05
        },
        {
          "variable": "dwt",
          "time": 0.0,
          "expected": 2.3810493465124405
        }
      ]
    }
  ]
}
```

</details>
