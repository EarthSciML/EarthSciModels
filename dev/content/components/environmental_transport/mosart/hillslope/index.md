---
title: "Hillslope"
slug: "hillslope"
domains: ["environmental_transport"]
component_types: ["model"]
subdomains: ["mosart"]
domain: "environmental_transport"
subdomain: "mosart"
component_type: "model"
esm_version: "2.0.0"
esm_path: "components/environmental_transport/mosart/mosart_hillslope.esm"
reference: "10.1175/JHM-D-12-015.1"
description: "MOSART hillslope routing step (stage 2 of the EqESM project): the per-cell Euler step 1 of mosart_physics.F90:Euler (F90:74-80) composed of hillslopeRouting (F90:225-239) and updateState_hillslope (F90:352-360), written as a storage ODE with the pointwise laws imported from ./mosart_templates.esm. Equations, exactly as in the Fortran: ehout_manning = -CREHT_nosqrt(hslpsqrt, nh, Gxr, yh) (F90:232); the dry-cell clamp replaces ehout by -(qsur + wh/delt) when ehout < 0 and wh + (qsur + ehout)*delt < TINYVALUE (F90:233-236); dwh = qsur + ehout (F90:237); d(wh)/dt = dwh (the Fortran advances wh += dwh*DeltaT explicitly once per substep, F90:77; here a continuous ODE, not the limit of that scheme - see README.md, 'Continuous ODEs vs the Fortran 3600-s Euler stepping'); yh = wh (updateState_hillslope, F90:358); and the lateral inflow to the subnetwork etin = (-ehout + qsub)*area*frac (F90:79). Units per mosart_tstatusflux_type.F90 / mosart_tspatialunit_type.F90: wh, yh [m]; dwh, qsur, qsub, ehout [m/s]; etin [m3/s]; hslpsqrt [1]; Gxr [1/m]; area [m2]; frac [1]; nh is the hillslope Manning roughness (SI dimension s/m^(1/3), see mosart_templates.esm); delt is Tctl%DeltaT = delt_coupling/nsub (mosart_driver.F90:800). The qsur/qsub forcing arrives from the cap in m/s (mosart_driver.F90:806-813 converts the m3/s streams by /area). The tests block pins the overland law CREHT_nosqrt pointwise (instantaneous D-boundary tests, time_span {0,0}) and the one-substep storage traces in the continuous-ODE form, with numeric tuples from the EqESM instrumented-CESM dumps (stage1/dumps/mosart/ dry lane window: creht_nosqrt.csv, mosart_euler.csv, area from mosart_run_imports_wide.csv; stage1/dumps/mosart_wet/ wet window: the wet_overland_* pins); the trace assertions carry the measured Euler-vs-continuous scheme gaps (see README.md (Testing)). Reference: stage1/cesm/components/mosart/src/riverroute/mosart_physics.F90 (mosart1.1.13)."
tags: ["environmental_transport", "mosart", "model", "river-routing", "hydrology", "hillslope", "overland-flow", "manning", "cesm"]
---

## Description

MOSART hillslope routing step (stage 2 of the EqESM project): the per-cell Euler step 1 of mosart_physics.F90:Euler (F90:74-80) composed of hillslopeRouting (F90:225-239) and updateState_hillslope (F90:352-360), written as a storage ODE with the pointwise laws imported from ./mosart_templates.esm. Equations, exactly as in the Fortran: ehout_manning = -CREHT_nosqrt(hslpsqrt, nh, Gxr, yh) (F90:232); the dry-cell clamp replaces ehout by -(qsur + wh/delt) when ehout < 0 and wh + (qsur + ehout)*delt < TINYVALUE (F90:233-236); dwh = qsur + ehout (F90:237); d(wh)/dt = dwh (the Fortran advances wh += dwh*DeltaT explicitly once per substep, F90:77; here a continuous ODE, not the limit of that scheme - see README.md, 'Continuous ODEs vs the Fortran 3600-s Euler stepping'); yh = wh (updateState_hillslope, F90:358); and the lateral inflow to the subnetwork etin = (-ehout + qsub)*area*frac (F90:79). Units per mosart_tstatusflux_type.F90 / mosart_tspatialunit_type.F90: wh, yh [m]; dwh, qsur, qsub, ehout [m/s]; etin [m3/s]; hslpsqrt [1]; Gxr [1/m]; area [m2]; frac [1]; nh is the hillslope Manning roughness (SI dimension s/m^(1/3), see mosart_templates.esm); delt is Tctl%DeltaT = delt_coupling/nsub (mosart_driver.F90:800). The qsur/qsub forcing arrives from the cap in m/s (mosart_driver.F90:806-813 converts the m3/s streams by /area). The tests block pins the overland law CREHT_nosqrt pointwise (instantaneous D-boundary tests, time_span {0,0}) and the one-substep storage traces in the continuous-ODE form, with numeric tuples from the EqESM instrumented-CESM dumps (stage1/dumps/mosart/ dry lane window: creht_nosqrt.csv, mosart_euler.csv, area from mosart_run_imports_wide.csv; stage1/dumps/mosart_wet/ wet window: the wet_overland_* pins); the trace assertions carry the measured Euler-vs-continuous scheme gaps (see README.md (Testing)). Reference: stage1/cesm/components/mosart/src/riverroute/mosart_physics.F90 (mosart1.1.13).

## Reference

- Li, H., Wigmosta, M. S., Wu, H., Huang, M., Ke, Y., Coleman, A. M., and Leung, L. R. (2013). A physically based runoff routing model for land surface and earth system models. Journal of Hydrometeorology, 14(3), 808-828. The MOSART (Model for Scale Adaptive River Transport) routing scheme these components transcribe.
- CESM (Community Earth System Model), ESCOMP/CESM, cesm3.0-alphabranch: MOSART river-routing source (mosart1.1.13) - mosart_physics.F90, mosart_driver.F90, mosart_tstatusflux_type.F90, mosart_tspatialunit_type.F90, rof_comp_nuopc/rof_import_export.F90 - the reference implementation these components are transcribed from.
- EarthSciModels - the authoritative .esm corpus this component lives in.

## Variables

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `wh` | `m` | `0.0` | storage of surface water at the hillslope (TRunoff%wh), [m] |

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `qsur` | `m/s` | `0.0` | surface runoff generated from the hillslope (TRunoff%qsur, after the mosart_driver m3/s -> m/s /area conversion), [m/s] |
| `qsub` | `m/s` | `0.0` | subsurface runoff generated from the hillslope (TRunoff%qsub), [m/s] |
| `hslpsqrt` | `1` | `0.01` | sqrt of the hillslope slope (TUnit%hslpsqrt, from the frivinp network file hslp), [-] |
| `nh` | `s/m^(1/3)` | `0.03` | Manning's roughness of the hillslope, channel network excluded (TUnit%nh, from frivinp); network file stores a bare number; declared with its SI dimension s/m^(1/3) for dimensional consistency |
| `Gxr` | `1/m` | `0.001` | drainage density within the cell (TUnit%Gxr, from frivinp gxr), [1/m] |
| `area` | `m^2` | `10000000.0` | area of the local cell (TUnit%area, from frivinp), [m2] |
| `frac` | `1` | `1.0` | fraction of the cell included in the study area (TUnit%frac, from frivinp), [-] |
| `delt` | `s` | `3600.0` | routing substep Tctl%DeltaT = delt_coupling/nsub (mosart_driver.F90:800), [s] |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `dwh` | `m/s` |  | change of hillslope water storage (TRunoff%dwh) = qsur + ehout, [m/s] |
| `yh` | `m` |  | depth of surface water (TRunoff%yh), defined by updateState_hillslope as yh = wh, [m] |
| `ehout_manning` | `m/s` |  | unclamped overland flow from the hillslope into the sub-network channels, -CREHT_nosqrt(...), [m/s] |
| `ehout` | `m/s` |  | overland flow after the dry-cell clamp of hillslopeRouting (TRunoff%ehout), [m/s] |
| `etin` | `m^3/s` |  | lateral inflow from hillslope into the subnetwork (TRunoff%etin) = (-ehout + qsub)*area*frac, [m3/s] |

## Observed expressions

$$
dwh = qsur + ehout
$$
_change of hillslope water storage (TRunoff%dwh) = qsur + ehout, [m/s]_

$$
yh = wh
$$
_depth of surface water (TRunoff%yh), defined by updateState_hillslope as yh = wh, [m]_

$$
ehout_{manning} = \left(-1.0\right) \cdot \mathrm{overland_discharge}\left(sqrthslp=hslpsqrt, nh=nh, Gxr=Gxr, yh=yh\right)
$$
_unclamped overland flow from the hillslope into the sub-network channels, -CREHT_nosqrt(...), [m/s]_

$$
ehout = \mathrm{ifelse}\left(\mathrm{and}\left(\mathrm{<}\left(ehout_{manning}, 0.0\right), \mathrm{<}\left(wh + \left(qsur + ehout_{manning}\right) \cdot delt, \mathrm{const}\left(\right)\right)\right), \left(-1.0\right) \cdot \left(qsur + \frac{wh}{delt}\right), ehout_{manning}\right)
$$
_overland flow after the dry-cell clamp of hillslopeRouting (TRunoff%ehout), [m/s]_

$$
etin = \left(-ehout + qsub\right) \cdot area \cdot frac
$$
_lateral inflow from hillslope into the subnetwork (TRunoff%etin) = (-ehout + qsub)*area*frac, [m3/s]_

## Equations

$$
\mathrm{D}\left(wh\right) = dwh
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
    "wh": {
      "type": "unknown",
      "units": "m",
      "default": 0.0,
      "description": "storage of surface water at the hillslope (TRunoff%wh), [m]"
    },
    "dwh": {
      "type": "unknown",
      "units": "m/s",
      "description": "change of hillslope water storage (TRunoff%dwh) = qsur + ehout, [m/s]"
    },
    "yh": {
      "type": "unknown",
      "units": "m",
      "description": "depth of surface water (TRunoff%yh), defined by updateState_hillslope as yh = wh, [m]"
    },
    "ehout_manning": {
      "type": "unknown",
      "units": "m/s",
      "description": "unclamped overland flow from the hillslope into the sub-network channels, -CREHT_nosqrt(...), [m/s]"
    },
    "ehout": {
      "type": "unknown",
      "units": "m/s",
      "description": "overland flow after the dry-cell clamp of hillslopeRouting (TRunoff%ehout), [m/s]"
    },
    "etin": {
      "type": "unknown",
      "units": "m^3/s",
      "description": "lateral inflow from hillslope into the subnetwork (TRunoff%etin) = (-ehout + qsub)*area*frac, [m3/s]"
    },
    "qsur": {
      "type": "parameter",
      "units": "m/s",
      "default": 0.0,
      "description": "surface runoff generated from the hillslope (TRunoff%qsur, after the mosart_driver m3/s -> m/s /area conversion), [m/s]"
    },
    "qsub": {
      "type": "parameter",
      "units": "m/s",
      "default": 0.0,
      "description": "subsurface runoff generated from the hillslope (TRunoff%qsub), [m/s]"
    },
    "hslpsqrt": {
      "type": "parameter",
      "units": "1",
      "default": 0.01,
      "description": "sqrt of the hillslope slope (TUnit%hslpsqrt, from the frivinp network file hslp), [-]"
    },
    "nh": {
      "type": "parameter",
      "units": "s/m^(1/3)",
      "default": 0.03,
      "description": "Manning's roughness of the hillslope, channel network excluded (TUnit%nh, from frivinp); network file stores a bare number; declared with its SI dimension s/m^(1/3) for dimensional consistency"
    },
    "Gxr": {
      "type": "parameter",
      "units": "1/m",
      "default": 0.001,
      "description": "drainage density within the cell (TUnit%Gxr, from frivinp gxr), [1/m]"
    },
    "area": {
      "type": "parameter",
      "units": "m^2",
      "default": 10000000.0,
      "description": "area of the local cell (TUnit%area, from frivinp), [m2]"
    },
    "frac": {
      "type": "parameter",
      "units": "1",
      "default": 1.0,
      "description": "fraction of the cell included in the study area (TUnit%frac, from frivinp), [-]"
    },
    "delt": {
      "type": "parameter",
      "units": "s",
      "default": 3600.0,
      "description": "routing substep Tctl%DeltaT = delt_coupling/nsub (mosart_driver.F90:800), [s]"
    }
  },
  "equations": [
    {
      "lhs": "ehout_manning",
      "rhs": {
        "op": "*",
        "args": [
          -1.0,
          {
            "op": "apply_expression_template",
            "args": [],
            "name": "overland_discharge",
            "bindings": {
              "sqrthslp": "hslpsqrt",
              "nh": "nh",
              "Gxr": "Gxr",
              "yh": "yh"
            }
          }
        ]
      }
    },
    {
      "lhs": "ehout",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "and",
            "args": [
              {
                "op": "<",
                "args": [
                  "ehout_manning",
                  0.0
                ]
              },
              {
                "op": "<",
                "args": [
                  {
                    "op": "+",
                    "args": [
                      "wh",
                      {
                        "op": "*",
                        "args": [
                          {
                            "op": "+",
                            "args": [
                              "qsur",
                              "ehout_manning"
                            ]
                          },
                          "delt"
                        ]
                      }
                    ]
                  },
                  {
                    "op": "const",
                    "args": [],
                    "value": 1e-14,
                    "units": "m"
                  }
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              -1.0,
              {
                "op": "+",
                "args": [
                  "qsur",
                  {
                    "op": "/",
                    "args": [
                      "wh",
                      "delt"
                    ]
                  }
                ]
              }
            ]
          },
          "ehout_manning"
        ]
      }
    },
    {
      "lhs": "dwh",
      "rhs": {
        "op": "+",
        "args": [
          "qsur",
          "ehout"
        ]
      }
    },
    {
      "lhs": {
        "op": "D",
        "args": [
          "wh"
        ],
        "wrt": "t"
      },
      "rhs": "dwh"
    },
    {
      "lhs": "yh",
      "rhs": "wh"
    },
    {
      "lhs": "etin",
      "rhs": {
        "op": "*",
        "args": [
          {
            "op": "+",
            "args": [
              {
                "op": "-",
                "args": [
                  "ehout"
                ]
              },
              "qsub"
            ]
          },
          "area",
          "frac"
        ]
      }
    }
  ],
  "tests": [
    {
      "id": "overland_law_step1_sub2_cell100312",
      "description": "Instantaneous pin of the overland-flow law CREHT_nosqrt at the hillslope (mosart_physics.F90:426-437) from stage1/dumps/mosart/creht_nosqrt.csv row (step 1, ns 2, nr 1, gindex 100312): yh = wh = 9.32660989523826711e-11 m, sqrthslp = 3.78813938497516212e-01, nh = 7.74544477462768555e-02, Gxr = 2.99999999999999974e-04 give ehout_manning = -CREHT_nosqrt = eht_raw = -2.81432250323167531e-20 m/s, and etin = (-ehout + qsub)*area*frac = 8.16213652457282613e-11 m3/s with area = 2.900213644740529e9 m2 (the area column of mosart_run_imports_wide.csv, equal to the qsur_m3s/qsur_ms ratio of the step-1 dump rows; qsur = 2.59072497089951852e-14 m/s from mosart_euler.csv row (1,2,entry,100312)). time_span {0,0} keeps wh at its initial condition so the law is evaluated pointwise; the dry-cell clamp does not fire (wh + (qsur + ehout)*delt = 1.87e-10 > TINYVALUE). The Fortran value is reproduced to round-off (rel 1e-12; cross-language pow() ulps).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "qsur": 2.5907249708995185e-14,
        "qsub": 0.0,
        "hslpsqrt": 0.3788139384975162,
        "nh": 0.07745444774627686,
        "Gxr": 0.0003,
        "area": 2900213644.740529,
        "frac": 1.0,
        "delt": 3600.0
      },
      "initial_conditions": {
        "wh": 9.326609895238267e-11
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 1e-32
      },
      "assertions": [
        {
          "variable": "yh",
          "time": 0.0,
          "expected": 9.326609895238267e-11
        },
        {
          "variable": "ehout_manning",
          "time": 0.0,
          "expected": -2.8143225032316753e-20
        },
        {
          "variable": "ehout",
          "time": 0.0,
          "expected": -2.8143225032316753e-20
        },
        {
          "variable": "etin",
          "time": 0.0,
          "expected": 8.162136524572826e-11
        }
      ]
    },
    {
      "id": "overland_law_drain_cell101032",
      "description": "Instantaneous pin of CREHT_nosqrt from creht_nosqrt.csv row (step 5, ns 1, nr 4, gindex 101032), a cell with a steeper hillslope: yh = 2.79791921922257878e-10 m, sqrthslp = 3.88458491991100663e-01, nh = 7.58072286844253540e-02, Gxr = 2.99999999999999974e-04 give eht_raw = ehout = -1.83998326708271600e-19 m/s (qsur = qsub = 0 in step 5, mosart_euler.csv row (5,1,entry,101032); the clamp cannot fire with qsur = 0 and wh > TINYVALUE).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "qsur": 0.0,
        "qsub": 0.0,
        "hslpsqrt": 0.38845849199110066,
        "nh": 0.07580722868442535,
        "Gxr": 0.0003,
        "delt": 3600.0
      },
      "initial_conditions": {
        "wh": 2.797919219222579e-10
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 1e-32
      },
      "assertions": [
        {
          "variable": "yh",
          "time": 0.0,
          "expected": 2.797919219222579e-10
        },
        {
          "variable": "ehout_manning",
          "time": 0.0,
          "expected": -1.839983267082716e-19
        },
        {
          "variable": "ehout",
          "time": 0.0,
          "expected": -1.839983267082716e-19
        }
      ]
    },
    {
      "id": "overland_law_drain_cell100313",
      "description": "Instantaneous pin of CREHT_nosqrt from creht_nosqrt.csv row (step 5, ns 1, nr 2, gindex 100313): yh = 1.39897800399400462e-10 m, sqrthslp = 2.68886593194975043e-01, nh = 7.85291716456413269e-02, Gxr = 2.99999999999999974e-04 give eht_raw = ehout = -3.87267332350159691e-20 m/s. Varied mid-range inputs relative to the other law tests.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "qsur": 0.0,
        "qsub": 0.0,
        "hslpsqrt": 0.26888659319497504,
        "nh": 0.07852917164564133,
        "Gxr": 0.0003,
        "delt": 3600.0
      },
      "initial_conditions": {
        "wh": 1.3989780039940046e-10
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 1e-32
      },
      "assertions": [
        {
          "variable": "yh",
          "time": 0.0,
          "expected": 1.3989780039940046e-10
        },
        {
          "variable": "ehout_manning",
          "time": 0.0,
          "expected": -3.872673323501597e-20
        },
        {
          "variable": "ehout",
          "time": 0.0,
          "expected": -3.872673323501597e-20
        }
      ]
    },
    {
      "id": "overland_law_zero_storage",
      "description": "Zero-storage pin from creht_nosqrt.csv row (step 1, ns 1, nr 1, gindex 100312): with yh = wh = 0 the Manning velocity is zeroed by the rr <= 0 guard and CREHT_nosqrt returns 0, so ehout_manning = ehout = -0 (eht_raw = -0 in the dump) and etin = 0 even with qsur = 2.59072497089951852e-14 m/s.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "qsur": 2.5907249708995185e-14,
        "qsub": 0.0,
        "hslpsqrt": 0.3788139384975162,
        "nh": 0.07745444774627686,
        "Gxr": 0.0003,
        "area": 2900213644.740529,
        "frac": 1.0,
        "delt": 3600.0
      },
      "initial_conditions": {
        "wh": 0.0
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 1e-32
      },
      "assertions": [
        {
          "variable": "yh",
          "time": 0.0,
          "expected": 0.0
        },
        {
          "variable": "ehout_manning",
          "time": 0.0,
          "expected": 0.0
        },
        {
          "variable": "ehout",
          "time": 0.0,
          "expected": 0.0
        },
        {
          "variable": "etin",
          "time": 0.0,
          "expected": 0.0
        }
      ]
    },
    {
      "id": "one_step_growth_step1_sub2",
      "description": "One-substep trace in the continuous-ODE form over [0, 3600] (delt = Tctl%DeltaT from the mosart_euler.csv delt column): entry (step 1, ns 2, gindex 100312) wh = 9.32660989523826711e-11 m with qsur = 2.59072497089951852e-14 m/s, qsub = 0; the exit state (step 1, ns 2) is wh = 1.86532096589155226e-10 m, ehout = -2.81432250323167531e-20 m/s, etin = 8.16213652457282613e-11 m3/s (area = 2.900213644740529e9 m2, the qsur_m3s/qsur_ms ratio of the step-1 dump rows). The .esm integrates d(wh)/dt = qsur + ehout(wh) continuously while the Fortran advances wh += dwh*DeltaT with the law held at the substep-start depth (Euler step 1, F90:77); the measured scheme gap (continuous-ODE end state vs the Fortran's single Euler step, solver at reltol 1e-14) is 1.02e-17 m abs on wh = 5.5e-8 rel of the end state - the rel 1e-5 assertion bound is ~2x the measured gap.",
      "time_span": {
        "start": 0.0,
        "end": 3600.0
      },
      "parameter_overrides": {
        "qsur": 2.5907249708995185e-14,
        "qsub": 0.0,
        "hslpsqrt": 0.3788139384975162,
        "nh": 0.07745444774627686,
        "Gxr": 0.0003,
        "area": 2900213644.740529,
        "frac": 1.0,
        "delt": 3600.0
      },
      "initial_conditions": {
        "wh": 9.326609895238267e-11
      },
      "tolerance": {
        "rel": 1e-05,
        "abs": 1e-16
      },
      "assertions": [
        {
          "variable": "wh",
          "time": 3600.0,
          "expected": 1.8653209658915523e-10
        },
        {
          "variable": "ehout",
          "time": 0.0,
          "expected": -2.8143225032316753e-20,
          "tolerance": {
            "rel": 1e-12,
            "abs": 1e-32
          }
        },
        {
          "variable": "etin",
          "time": 0.0,
          "expected": 8.162136524572826e-11,
          "tolerance": {
            "rel": 1e-12,
            "abs": 1e-32
          }
        }
      ]
    },
    {
      "id": "one_step_drain_step2_sub1",
      "description": "One-substep drain trace over [0, 3600]: entry (step 2, ns 1, gindex 100312) wh = 2.79797873884816915e-10 m with qsur = qsub = 0 (step-2 imports carry no runoff); the exit state (step 2, ns 1) is wh = 2.79797241651524941e-10 m. The ehout/etin assertions sit at time 0, where the state is the entry state and the law values equal the Fortran's substep values (ehout = -1.75620358877005223e-19 m/s, etin = 5.09336561109318995e-10 m3/s at the entry depth). With qsur = 0 the storage drains through the overland law only; the measured scheme gap (continuous-ODE end state vs the Fortran's single Euler step, solver at reltol 1e-14) is 1.19e-21 m abs on wh = 4.3e-12 rel of the end state (the Euler second-order term of the tiny relative drain of 2.3e-6 per step) - the rel 1e-7 bound is >1000x the measured gap.",
      "time_span": {
        "start": 0.0,
        "end": 3600.0
      },
      "parameter_overrides": {
        "qsur": 0.0,
        "qsub": 0.0,
        "hslpsqrt": 0.3788139384975162,
        "nh": 0.07745444774627686,
        "Gxr": 0.0003,
        "area": 2900213644.740529,
        "frac": 1.0,
        "delt": 3600.0
      },
      "initial_conditions": {
        "wh": 2.797978738848169e-10
      },
      "tolerance": {
        "rel": 1e-07,
        "abs": 1e-17
      },
      "assertions": [
        {
          "variable": "wh",
          "time": 3600.0,
          "expected": 2.7979724165152494e-10
        },
        {
          "variable": "ehout",
          "time": 0.0,
          "expected": -1.7562035887700522e-19,
          "tolerance": {
            "rel": 1e-12,
            "abs": 1e-32
          }
        },
        {
          "variable": "etin",
          "time": 0.0,
          "expected": 5.09336561109319e-10,
          "tolerance": {
            "rel": 1e-12,
            "abs": 1e-32
          }
        }
      ]
    },
    {
      "id": "wet_overland_cell106268",
      "description": "Instantaneous pin of the wet hillslope overland-flow law ehout = -CREHT_nosqrt(hslpsqrt, nh, Gxr, yh) = -Gxr*yh*(yh^2)^(1/3)*hslpsqrt/nh (hillslopeRouting, mosart_physics.F90:63-84) at the first wet state of the cell-106268 hillslope, from stage1/dumps/mosart_wet/creht_nosqrt.csv row (step 1, ns 2, m 0, gindex 106268): wh = yh = 0.00011923842106852279 m (the hillslope has been filling with qsur since the cold start) gives ehout_manning = ehout = -1.4493945879189655e-10 m/s (the dry-cell clamp cannot fire: wh + (qsur + ehout)*delt > 0); the subnetwork inflow etin = (-ehout + qsub)*area*frac = 4.30149076384016338e-01 m3/s, the dumped exit-row value (mosart_euler.csv row step 1, ns 2, exit, gindex 106268), reproduced by the .esm with the cell area 2967784480.288577 m2 = qgwl_area/qgwl = 1.99127871364415199e2 m3/s / 6.70964730380464462e-08 m/s of the step-1 dump rows (crvrman_chan.csv qgwl_area at step 1, ns 1, m 1, gindex 106268 over the mosart_euler.csv entry-row qgwl at step 1, ns 1, gindex 106268; identical to the area column of the dry-lane mosart_run_imports_wide.csv for this gindex). Expected values are the dumped outputs of the EqESM instrumented-CESM wet window (CESM run, not a standalone driver). time_span {0,0}; rel 1e-12.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "qsur": 0.0,
        "qsub": 0.0,
        "hslpsqrt": 0.1216552506059644,
        "nh": 0.07273763418197632,
        "Gxr": 0.0003,
        "area": 2967784480.288577,
        "frac": 1.0,
        "delt": 3600.0
      },
      "initial_conditions": {
        "wh": 0.0001192384210685228
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 1e-26
      },
      "assertions": [
        {
          "variable": "yh",
          "time": 0.0,
          "expected": 0.0001192384210685228
        },
        {
          "variable": "ehout_manning",
          "time": 0.0,
          "expected": -1.4493945879189655e-10
        },
        {
          "variable": "ehout",
          "time": 0.0,
          "expected": -1.4493945879189655e-10
        },
        {
          "variable": "etin",
          "time": 0.0,
          "expected": 0.43014907638401634
        }
      ]
    },
    {
      "id": "wet_overland_cell223003",
      "description": "Instantaneous pin of the wet hillslope overland-flow law on the cell-223003 hillslope, from stage1/dumps/mosart_wet/creht_nosqrt.csv row (step 1, ns 2, m 0, gindex 223003): wh = yh = 1.0392437428203876e-06 m gives ehout_manning = ehout = -7.4254016341044596e-14 m/s (Gxr = 0.0007). Expected values are the dumped outputs of the EqESM instrumented-CESM wet window (CESM run, not a standalone driver). time_span {0,0}; rel 1e-12.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "qsur": 0.0,
        "qsub": 0.0,
        "hslpsqrt": 0.0648074069840786,
        "nh": 0.06514260172843933,
        "Gxr": 0.0007,
        "area": 10000000.0,
        "frac": 1.0,
        "delt": 3600.0
      },
      "initial_conditions": {
        "wh": 1.0392437428203876e-06
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 1e-26
      },
      "assertions": [
        {
          "variable": "yh",
          "time": 0.0,
          "expected": 1.0392437428203876e-06
        },
        {
          "variable": "ehout_manning",
          "time": 0.0,
          "expected": -7.42540163410446e-14
        },
        {
          "variable": "ehout",
          "time": 0.0,
          "expected": -7.42540163410446e-14
        }
      ]
    },
    {
      "id": "wet_overland_cell99771",
      "description": "Instantaneous pin of the wet hillslope overland-flow law on the cell-99771 hillslope, from stage1/dumps/mosart_wet/creht_nosqrt.csv row (step 1, ns 2, m 0, gindex 99771): wh = yh = 4.8191255559909953e-06 m gives ehout_manning = ehout = -2.8503549525741766e-13 m/s. Expected values are the dumped outputs of the EqESM instrumented-CESM wet window (CESM run, not a standalone driver). time_span {0,0}; rel 1e-12.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "qsur": 0.0,
        "qsub": 0.0,
        "hslpsqrt": 0.0282842712474619,
        "nh": 0.04093056172132492,
        "Gxr": 0.0003,
        "area": 10000000.0,
        "frac": 1.0,
        "delt": 3600.0
      },
      "initial_conditions": {
        "wh": 4.819125555990995e-06
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 1e-26
      },
      "assertions": [
        {
          "variable": "yh",
          "time": 0.0,
          "expected": 4.819125555990995e-06
        },
        {
          "variable": "ehout_manning",
          "time": 0.0,
          "expected": -2.8503549525741766e-13
        },
        {
          "variable": "ehout",
          "time": 0.0,
          "expected": -2.8503549525741766e-13
        }
      ]
    }
  ]
}
```

</details>
