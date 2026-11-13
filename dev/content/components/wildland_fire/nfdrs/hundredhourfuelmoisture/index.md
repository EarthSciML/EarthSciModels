---
title: "HundredHourFuelMoisture"
slug: "hundredhourfuelmoisture"
domains: ["wildland_fire"]
component_types: ["model"]
subdomains: ["nfdrs"]
domain: "wildland_fire"
subdomain: "nfdrs"
component_type: "model"
esm_version: "1.0.0"
esm_path: "components/wildland_fire/nfdrs/moisture_100h.esm"
reference: "Cohen, J. D., & Deeming, J. E. (1985). The National Fire-Danger Rating System: basic equations. Gen. Tech. Rep. PSW-82. Berkeley, CA: USDA Forest Service, Pacific Southwest Forest and Range Experiment Station. Page 5 (100-hour timelag fuel moisture)."
description: "100-hour timelag dead fuel moisture content per the NFDRS (Cohen & Deeming 1985), page 5. Migrated from WildlandFire.jl@126976f2 src/nfdrs.jl:279 (`HundredHourFuelMoisture` @component). State-variable model: MC100, EMCBAR, BNDRYH are time-indexed state variables with daily discrete update equations."
tags: ["wildland_fire", "nfdrs", "model", "fuel_moisture"]
---

## Description

100-hour timelag dead fuel moisture content per the NFDRS (Cohen & Deeming 1985), page 5. Migrated from WildlandFire.jl@126976f2 src/nfdrs.jl:279 (`HundredHourFuelMoisture` @component). State-variable model: MC100, EMCBAR, BNDRYH are time-indexed state variables with daily discrete update equations.

## Reference

_source_ref: WildlandFire.jl@126976f2508ceacca6c486b21ae6da5b168c6f46:src/nfdrs.jl:279
Upstream `HundredHourFuelMoisture` is an MTK `@component` with three state variables (MC100, EMCBAR, BNDRYH) that follow daily discrete update equations. The model computes weighted 24-hour averages of equilibrium moisture content (EMCBAR) and boundary conditions (BNDRYH), then updates the 100-hour fuel moisture (MC100) using a response coefficient. Daylength is computed from latitude and Julian day using solar declination. The response_coef constant is computed as 1.0 - 0.87 * exp(-0.24) ≈ 0.2804._

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `s_ref` | `s` | `1.0` | Reference time for non-dimensionalization. |
| `rad_ref` | `rad` | `1.0` | Reference angle for non-dimensionalization. |
| `hr_to_s` | `1` | `3600.0` | Hours to seconds conversion factor (dimensionless after non-dimensionalization). |
| `response_coef` | `1` | `0.280401` | Moisture response coefficient (dimensionless), computed as 1.0 - 0.87 * exp(-0.24) ≈ 0.2804. |
| `EMCMIN` | `1` | `0.05` | EMC at maximum temperature / minimum RH (dimensionless fraction). Default 0.05 = 5%. |
| `EMCMAX` | `1` | `0.2` | EMC at minimum temperature / maximum RH (dimensionless fraction). Default 0.20 = 20%. |
| `PPTDUR` | `s` | `0.0` | Duration of precipitation (seconds). |
| `LAT` | `rad` | `0.6981` | Station latitude in radians. Default 0.6981 rad ≈ 40 degrees. |
| `JDATE` | `1` | `180.0` | Julian day of year (1-366, dimensionless). Default 180 ≈ summer solstice. |
| `YMC100` | `1` | `0.1` | Previous day's MC100 value (dimensionless fraction). Default 0.10 = 10%. |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `PPTDUR_hr` | `1` |  | Precipitation duration in hours (algebraic intermediate). |
| `LAT_nd` | `1` |  | Non-dimensionalized latitude (algebraic intermediate). |
| `DECL` | `1` |  | Solar declination (radians, algebraic intermediate). |
| `tan_product` | `1` |  | Product tan(LAT)*tan(DECL) used in daylength calc (algebraic intermediate). |
| `tan_product_clamped` | `1` |  | tan_product clamped to [-0.99, 0.99] before acos (algebraic intermediate). |
| `DAYLIT` | `1` |  | Daylength in hours derived from latitude and Julian date (algebraic intermediate). |
| `MC100` | `1` |  | 100-hour fuel moisture content (dimensionless fraction). |
| `EMCBAR` | `1` |  | Weighted 24-hour average EMC (dimensionless fraction). |
| `BNDRYH` | `1` |  | Weighted 24-hour average boundary condition (dimensionless fraction). |

## Observed expressions

$$
PPTDUR_{hr} = \frac{\frac{PPTDUR}{s_{ref}}}{hr_{to\,s}}
$$
_Precipitation duration in hours (algebraic intermediate)._

$$
LAT_{nd} = \frac{LAT}{rad_{ref}}
$$
_Non-dimensionalized latitude (algebraic intermediate)._

$$
DECL = 0.41008 \cdot \sin\left(\left(JDATE - 82\right) \cdot 0.01745\right)
$$
_Solar declination (radians, algebraic intermediate)._

$$
tan_{product} = \tan\left(LAT_{nd}\right) \cdot \tan\left(DECL\right)
$$
_Product tan(LAT)*tan(DECL) used in daylength calc (algebraic intermediate)._

$$
tan_{product\,clamped} = \mathrm{max}\left(-0.99, \mathrm{min}\left(0.99, tan_{product}\right)\right)
$$
_tan_product clamped to [-0.99, 0.99] before acos (algebraic intermediate)._

$$
DAYLIT = 24.0 \cdot \left(1.0 - \frac{\mathrm{acos}\left(tan_{product\,clamped}\right)}{3.1416}\right)
$$
_Daylength in hours derived from latitude and Julian date (algebraic intermediate)._

$$
MC100 = YMC100 + \left(BNDRYH - YMC100\right) \cdot response_{coef}
$$
_100-hour fuel moisture content (dimensionless fraction)._

$$
EMCBAR = \frac{DAYLIT \cdot EMCMIN + \left(24.0 - DAYLIT\right) \cdot EMCMAX}{24.0}
$$
_Weighted 24-hour average EMC (dimensionless fraction)._

$$
BNDRYH = \frac{\left(24.0 - PPTDUR_{hr}\right) \cdot EMCBAR + PPTDUR_{hr} \cdot \frac{0.5 \cdot PPTDUR_{hr} \cdot PPTDUR_{hr} + 41.0}{100.0}}{24.0}
$$
_Weighted 24-hour average boundary condition (dimensionless fraction)._

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "reference": {
    "notes": "source_ref: WildlandFire.jl@126976f2508ceacca6c486b21ae6da5b168c6f46:src/nfdrs.jl:279\nUpstream `HundredHourFuelMoisture` is an MTK `@component` with three state variables (MC100, EMCBAR, BNDRYH) that follow daily discrete update equations. The model computes weighted 24-hour averages of equilibrium moisture content (EMCBAR) and boundary conditions (BNDRYH), then updates the 100-hour fuel moisture (MC100) using a response coefficient. Daylength is computed from latitude and Julian day using solar declination. The response_coef constant is computed as 1.0 - 0.87 * exp(-0.24) ≈ 0.2804."
  },
  "tolerance": {
    "rel": 1e-12
  },
  "variables": {
    "s_ref": {
      "type": "parameter",
      "units": "s",
      "default": 1.0,
      "description": "Reference time for non-dimensionalization."
    },
    "rad_ref": {
      "type": "parameter",
      "units": "rad",
      "default": 1.0,
      "description": "Reference angle for non-dimensionalization."
    },
    "hr_to_s": {
      "type": "parameter",
      "units": "1",
      "default": 3600.0,
      "description": "Hours to seconds conversion factor (dimensionless after non-dimensionalization)."
    },
    "response_coef": {
      "type": "parameter",
      "units": "1",
      "default": 0.280401,
      "description": "Moisture response coefficient (dimensionless), computed as 1.0 - 0.87 * exp(-0.24) ≈ 0.2804."
    },
    "EMCMIN": {
      "type": "parameter",
      "units": "1",
      "default": 0.05,
      "description": "EMC at maximum temperature / minimum RH (dimensionless fraction). Default 0.05 = 5%."
    },
    "EMCMAX": {
      "type": "parameter",
      "units": "1",
      "default": 0.2,
      "description": "EMC at minimum temperature / maximum RH (dimensionless fraction). Default 0.20 = 20%."
    },
    "PPTDUR": {
      "type": "parameter",
      "units": "s",
      "default": 0.0,
      "description": "Duration of precipitation (seconds)."
    },
    "LAT": {
      "type": "parameter",
      "units": "rad",
      "default": 0.6981,
      "description": "Station latitude in radians. Default 0.6981 rad ≈ 40 degrees."
    },
    "JDATE": {
      "type": "parameter",
      "units": "1",
      "default": 180.0,
      "description": "Julian day of year (1-366, dimensionless). Default 180 ≈ summer solstice."
    },
    "YMC100": {
      "type": "parameter",
      "units": "1",
      "default": 0.1,
      "description": "Previous day's MC100 value (dimensionless fraction). Default 0.10 = 10%."
    },
    "PPTDUR_hr": {
      "type": "unknown",
      "units": "1",
      "description": "Precipitation duration in hours (algebraic intermediate)."
    },
    "LAT_nd": {
      "type": "unknown",
      "units": "1",
      "description": "Non-dimensionalized latitude (algebraic intermediate)."
    },
    "DECL": {
      "type": "unknown",
      "units": "1",
      "description": "Solar declination (radians, algebraic intermediate)."
    },
    "tan_product": {
      "type": "unknown",
      "units": "1",
      "description": "Product tan(LAT)*tan(DECL) used in daylength calc (algebraic intermediate)."
    },
    "tan_product_clamped": {
      "type": "unknown",
      "units": "1",
      "description": "tan_product clamped to [-0.99, 0.99] before acos (algebraic intermediate)."
    },
    "DAYLIT": {
      "type": "unknown",
      "units": "1",
      "description": "Daylength in hours derived from latitude and Julian date (algebraic intermediate)."
    },
    "MC100": {
      "type": "unknown",
      "units": "1",
      "description": "100-hour fuel moisture content (dimensionless fraction)."
    },
    "EMCBAR": {
      "type": "unknown",
      "units": "1",
      "description": "Weighted 24-hour average EMC (dimensionless fraction)."
    },
    "BNDRYH": {
      "type": "unknown",
      "units": "1",
      "description": "Weighted 24-hour average boundary condition (dimensionless fraction)."
    }
  },
  "equations": [
    {
      "lhs": "PPTDUR_hr",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "/",
            "args": [
              "PPTDUR",
              "s_ref"
            ]
          },
          "hr_to_s"
        ]
      }
    },
    {
      "lhs": "LAT_nd",
      "rhs": {
        "op": "/",
        "args": [
          "LAT",
          "rad_ref"
        ]
      }
    },
    {
      "lhs": "DECL",
      "rhs": {
        "op": "*",
        "args": [
          0.41008,
          {
            "op": "sin",
            "args": [
              {
                "op": "*",
                "args": [
                  {
                    "op": "-",
                    "args": [
                      "JDATE",
                      82
                    ]
                  },
                  0.01745
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "tan_product",
      "rhs": {
        "op": "*",
        "args": [
          {
            "op": "tan",
            "args": [
              "LAT_nd"
            ]
          },
          {
            "op": "tan",
            "args": [
              "DECL"
            ]
          }
        ]
      }
    },
    {
      "lhs": "tan_product_clamped",
      "rhs": {
        "op": "max",
        "args": [
          -0.99,
          {
            "op": "min",
            "args": [
              0.99,
              "tan_product"
            ]
          }
        ]
      }
    },
    {
      "lhs": "DAYLIT",
      "rhs": {
        "op": "*",
        "args": [
          24.0,
          {
            "op": "-",
            "args": [
              1.0,
              {
                "op": "/",
                "args": [
                  {
                    "op": "acos",
                    "args": [
                      "tan_product_clamped"
                    ]
                  },
                  3.1416
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "EMCBAR",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "+",
            "args": [
              {
                "op": "*",
                "args": [
                  "DAYLIT",
                  "EMCMIN"
                ]
              },
              {
                "op": "*",
                "args": [
                  {
                    "op": "-",
                    "args": [
                      24.0,
                      "DAYLIT"
                    ]
                  },
                  "EMCMAX"
                ]
              }
            ]
          },
          24.0
        ]
      }
    },
    {
      "lhs": "BNDRYH",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "+",
            "args": [
              {
                "op": "*",
                "args": [
                  {
                    "op": "-",
                    "args": [
                      24.0,
                      "PPTDUR_hr"
                    ]
                  },
                  "EMCBAR"
                ]
              },
              {
                "op": "*",
                "args": [
                  "PPTDUR_hr",
                  {
                    "op": "/",
                    "args": [
                      {
                        "op": "+",
                        "args": [
                          {
                            "op": "*",
                            "args": [
                              0.5,
                              {
                                "op": "*",
                                "args": [
                                  "PPTDUR_hr",
                                  "PPTDUR_hr"
                                ]
                              }
                            ]
                          },
                          41.0
                        ]
                      },
                      100.0
                    ]
                  }
                ]
              }
            ]
          },
          24.0
        ]
      }
    },
    {
      "lhs": "MC100",
      "rhs": {
        "op": "+",
        "args": [
          "YMC100",
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "BNDRYH",
                  "YMC100"
                ]
              },
              "response_coef"
            ]
          }
        ]
      }
    }
  ],
  "tests": [
    {
      "id": "default_summer_no_precip",
      "description": "Summer conditions (JDATE=180, LAT≈40deg), no precipitation. EMCMIN=0.05, EMCMAX=0.20, YMC100=0.10. DAYLIT ≈ 14.82 h ⇒ EMCBAR=BNDRYH ≈ 0.10737 ⇒ MC100 = 0.10 + (0.10737-0.10)*0.280401 ≈ 0.10207.",
      "parameter_overrides": {
        "LAT": 0.6981,
        "JDATE": 180.0,
        "PPTDUR": 0.0,
        "EMCMIN": 0.05,
        "EMCMAX": 0.2,
        "YMC100": 0.1
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "MC100",
          "time": 0.0,
          "expected": 0.1020680892,
          "tolerance": {
            "rel": 1e-08
          }
        }
      ]
    },
    {
      "id": "winter_short_day",
      "description": "Winter conditions (JDATE=30, LAT≈40deg), short daylength. DAYLIT ≈ 9.82 h ⇒ EMCBAR=BNDRYH ≈ 0.13860 ⇒ MC100 ≈ 0.11082.",
      "parameter_overrides": {
        "LAT": 0.6981,
        "JDATE": 30.0,
        "PPTDUR": 0.0,
        "EMCMIN": 0.05,
        "EMCMAX": 0.2,
        "YMC100": 0.1
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "MC100",
          "time": 0.0,
          "expected": 0.1108226212,
          "tolerance": {
            "rel": 1e-08
          }
        }
      ]
    },
    {
      "id": "with_precipitation",
      "description": "Moderate precipitation (PPTDUR=3600s = 1 hour). Saturated-fuel formula contributes 1 hour of 0.415 vs 23 h of EMCBAR=0.10737 in BNDRYH average ⇒ BNDRYH ≈ 0.12019 ⇒ MC100 ≈ 0.10566.",
      "parameter_overrides": {
        "LAT": 0.6981,
        "JDATE": 180.0,
        "PPTDUR": 3600.0,
        "EMCMIN": 0.05,
        "EMCMAX": 0.2,
        "YMC100": 0.1
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "MC100",
          "time": 0.0,
          "expected": 0.1056621819,
          "tolerance": {
            "rel": 1e-08
          }
        }
      ]
    },
    {
      "id": "dry_conditions",
      "description": "Dry conditions: EMCMIN=0.03, EMCMAX=0.10, YMC100=0.05. DAYLIT ≈ 14.82 h ⇒ EMCBAR=BNDRYH ≈ 0.05678 ⇒ MC100 ≈ 0.05190.",
      "parameter_overrides": {
        "LAT": 0.6981,
        "JDATE": 180.0,
        "PPTDUR": 0.0,
        "EMCMIN": 0.03,
        "EMCMAX": 0.1,
        "YMC100": 0.05
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "MC100",
          "time": 0.0,
          "expected": 0.0518997783,
          "tolerance": {
            "rel": 1e-08
          }
        }
      ]
    },
    {
      "id": "humid_conditions",
      "description": "Humid conditions: EMCMIN=0.15, EMCMAX=0.30, YMC100=0.20. DAYLIT ≈ 14.82 h ⇒ EMCBAR=BNDRYH ≈ 0.20737 ⇒ MC100 ≈ 0.20207.",
      "parameter_overrides": {
        "LAT": 0.6981,
        "JDATE": 180.0,
        "PPTDUR": 0.0,
        "EMCMIN": 0.15,
        "EMCMAX": 0.3,
        "YMC100": 0.2
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "MC100",
          "time": 0.0,
          "expected": 0.2020680892,
          "tolerance": {
            "rel": 1e-08
          }
        }
      ]
    },
    {
      "id": "equator_latitude",
      "description": "Equatorial location (LAT=0): tan(0)=0 ⇒ acos(0)=π/2 ⇒ DAYLIT = 12 h exactly. EMCBAR=BNDRYH = (12*0.05 + 12*0.20)/24 = 0.125 ⇒ MC100 = 0.10 + 0.025*0.280401 ≈ 0.10701.",
      "parameter_overrides": {
        "LAT": 0.0,
        "JDATE": 180.0,
        "PPTDUR": 0.0,
        "EMCMIN": 0.05,
        "EMCMAX": 0.2,
        "YMC100": 0.1
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "MC100",
          "time": 0.0,
          "expected": 0.1070099758,
          "tolerance": {
            "rel": 1e-08
          }
        }
      ]
    }
  ]
}
```

</details>
