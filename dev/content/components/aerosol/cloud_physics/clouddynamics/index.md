---
title: "CloudDynamics"
slug: "clouddynamics"
domains: ["aerosol"]
component_types: ["model"]
subdomains: ["cloud_physics"]
domain: "aerosol"
subdomain: "cloud_physics"
component_type: "model"
esm_version: "1.0.0"
esm_path: "components/aerosol/cloud_physics/cloud_dynamics.esm"
reference: "Seinfeld, J. H., and Pandis, S. N. (2006). Atmospheric Chemistry and Physics: From Air Pollution to Climate Change, 2nd Edition, John Wiley & Sons, Chapter 17. Key equations: Eq. 17.43 (dew-point temperature), Eq. 17.44 (dry adiabatic lapse rate), Eq. 17.46 (saturation mixing ratio), Eq. 17.49 (LCL height)."
description: "Adiabatic cooling and cloud-base thermodynamics — Seinfeld & Pandis (2006), Ch. 17. Computes five purely-algebraic quantities that characterize when and where a lifted air parcel reaches its lifting condensation level (LCL): the dry adiabatic lapse rate Γ_d, the saturation vapor pressure p_sat (Magnus formula), the saturation mixing ratio w_vs, the dew-point temperature T_d (Eq. 17.43), and the LCL height h_LCL (Eq. 17.49). Migrated from Aerosol.jl CloudDynamics."
tags: ["aerosol", "cloud_physics", "model", "thermodynamics", "adiabatic", "lifting-condensation-level"]
---

## Description

Adiabatic cooling and cloud-base thermodynamics — Seinfeld & Pandis (2006), Ch. 17. Computes five purely-algebraic quantities that characterize when and where a lifted air parcel reaches its lifting condensation level (LCL): the dry adiabatic lapse rate Γ_d, the saturation vapor pressure p_sat (Magnus formula), the saturation mixing ratio w_vs, the dew-point temperature T_d (Eq. 17.43), and the LCL height h_LCL (Eq. 17.49). Migrated from Aerosol.jl CloudDynamics.

## Reference

Seinfeld, J. H., and Pandis, S. N. (2006). Atmospheric Chemistry and Physics: From Air Pollution to Climate Change, 2nd Edition, John Wiley & Sons, Chapter 17. Key equations: Eq. 17.43 (dew-point temperature), Eq. 17.44 (dry adiabatic lapse rate), Eq. 17.46 (saturation mixing ratio), Eq. 17.49 (LCL height).

_source_ref: Aerosol.jl@c8c640bb636b22f2425460e9ed5cba50793bfee1:src/cloud_physics.jl:455

Upstream CloudDynamics is a pure-algebraic MTK @component. It declares 9 @constants (M_w, M_a, R, g, c_p_air, p_sat_ref, magnus_a, T_magnus_offset, magnus_b) and 4 @parameters (T_0, RH, p_a, ΔH_v) and 5 @variables (Γ_d, T_d, h_LCL, p_sat, w_vs). All 5 equations use ~ (algebraic). After MTK structural_simplify the compiled system has zero ODE states and all variables become observed quantities. Serialized as type: observed with inline expression, equations array empty — matching the pure-algebraic pattern of cloud_kelvin.esm and kohler.esm in this directory.

Equation derivations:
  Γ_d ~ g / c_p_air (Eq. 17.44 dry adiabatic lapse rate)
  p_sat ~ p_sat_ref * exp(magnus_a * (T_0 - T_magnus_offset) / ((T_0 - T_magnus_offset) + magnus_b)) (Magnus saturation vapor pressure)
  w_vs ~ M_w * p_sat / (M_a * p_a) (saturation mixing ratio)
  T_d ~ T_0 + (R * T_0² / (ΔH_v * M_w)) * ln(RH) (Eq. 17.43 dew-point)
  h_LCL ~ (T_0 - T_d) / Γ_d (Eq. 17.49 lifting condensation level)

Note on 'depends_on' in the migration tracker (DropletGrowth, CloudKelvinEffect): CloudDynamics does not call couple() internally; those dependencies are only needed at the CloudPhysics (parent) level where all cloud sub-models are composed together. This file is a self-contained component.

Tolerance rationale (rel=1e-9): all outputs are short closed-form expressions; float64 roundoff is at the few-ULP level, rel=1e-9 gives ample headroom._

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `M_w` | `kg/mol` | `0.018015` | Molecular weight of water. |
| `M_a` | `kg/mol` | `0.02897` | Molecular weight of dry air. |
| `R` | `J/(mol*K)` | `8.314` | Universal gas constant. |
| `g` | `m/s^2` | `9.81` | Gravitational acceleration. |
| `c_p_air` | `J/(kg*K)` | `1005.0` | Specific heat of air at constant pressure. |
| `p_sat_ref` | `Pa` | `610.94` | Magnus formula reference saturation pressure at 0°C. |
| `magnus_a` | `1` | `17.625` | Magnus formula coefficient a (dimensionless). |
| `T_magnus_offset` | `K` | `273.15` | Magnus formula temperature offset (0°C in Kelvin). |
| `magnus_b` | `K` | `243.04` | Magnus formula coefficient b. |
| `T_0` | `K` | `293.15` | Initial (surface) temperature of the air parcel. Default 293.15 K (20°C). |
| `RH` | `1` | `0.8` | Relative humidity (dimensionless, 0–1). Default 0.8 (80 %). |
| `p_a` | `Pa` | `101325.0` | Atmospheric pressure. Default 101325 Pa (1 atm). |
| `ΔH_v` | `J/kg` | `2500000.0` | Latent heat of vaporization. Default 2.5×10⁶ J/kg (S&P Table 17.1, at 0°C). |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `Γ_d` | `K/m` |  | Dry adiabatic lapse rate Γ_d = g/c_p ≈ 9.76 K/km (Eq. 17.44). Constant for a given gravitational field and specific heat. |
| `p_sat` | `Pa` |  | Saturation vapor pressure at T_0, computed via the Magnus formula. p_sat ≈ 2333 Pa at 20°C. |
| `w_vs` | `1` |  | Saturation water vapor mixing ratio w_vs = M_w p_sat / (M_a p_a) (Eq. 17.46, dimensionless mass ratio). |
| `T_d` | `K` |  | Dew-point temperature T_d = T_0 + (R T_0² / (ΔH_v M_w)) ln(RH) (Eq. 17.43). T_d ≤ T_0 with equality at RH=1. |
| `h_LCL` | `m` |  | Lifting condensation level height h_LCL = (T_0 - T_d) / Γ_d (Eq. 17.49). Height at which a rising air parcel cools to its dew point and cloud base forms. h_LCL ≥ 0 with equality at RH=1. |

## Observed expressions

$$
Γ_{d} = \frac{g}{c_{p\,air}}
$$
_Dry adiabatic lapse rate Γ_d = g/c_p ≈ 9.76 K/km (Eq. 17.44). Constant for a given gravitational field and specific heat._

$$
p_{sat} = p_{sat\,ref} \cdot e^{\frac{magnus_{a} \cdot \left(T_{0} + \left(-1\right) \cdot T_{magnus\,offset}\right)}{T_{0} + \left(-1\right) \cdot T_{magnus\,offset} + magnus_{b}}}
$$
_Saturation vapor pressure at T_0, computed via the Magnus formula. p_sat ≈ 2333 Pa at 20°C._

$$
w_{vs} = \frac{M_{w} \cdot p_{sat}}{M_{a} \cdot p_{a}}
$$
_Saturation water vapor mixing ratio w_vs = M_w p_sat / (M_a p_a) (Eq. 17.46, dimensionless mass ratio)._

$$
T_{d} = T_{0} + \frac{R \cdot T_{0}^{2}}{ΔH_{v} \cdot M_{w}} \cdot \ln\left(RH\right)
$$
_Dew-point temperature T_d = T_0 + (R T_0² / (ΔH_v M_w)) ln(RH) (Eq. 17.43). T_d ≤ T_0 with equality at RH=1._

$$
h_{LCL} = \frac{T_{0} + \left(-1\right) \cdot T_{d}}{Γ_{d}}
$$
_Lifting condensation level height h_LCL = (T_0 - T_d) / Γ_d (Eq. 17.49). Height at which a rising air parcel cools to its dew point and cloud base forms. h_LCL ≥ 0 with equality at RH=1._

## Analyses

### dew_point_vs_rh

Dew-point temperature T_d and LCL height h_LCL as a function of relative humidity RH at T_0=293.15 K. As RH decreases from 1 to 0.2 the dew-point depression grows and the cloud base rises (Eq. 17.43 and 17.49).

**Time span:** 0.0 → 1.0

**Swept over:** `RH`

![Dew-point temperature T_d as a function of relative humidity RH at T_0=293.15 K.](/plots/aerosol/cloud_physics/clouddynamics/dew_point_vs_rh-T_d_vs_RH.png)

![LCL height h_LCL as a function of relative humidity at T_0=293.15 K.](/plots/aerosol/cloud_physics/clouddynamics/dew_point_vs_rh-h_LCL_vs_RH.png)

### lcl_height_vs_temperature

LCL height h_LCL as a function of surface temperature T_0 at RH=0.8. Although higher T_0 increases the dew-point depression (larger numerator in T_0 - T_d), h_LCL depends on the interplay of the T_0-linear dew-point formula and the constant lapse rate; the net effect is a monotonic increase.

**Time span:** 0.0 → 1.0

**Swept over:** `T_0`

![LCL height h_LCL vs surface temperature T_0 at RH=0.8.](/plots/aerosol/cloud_physics/clouddynamics/lcl_height_vs_temperature-h_LCL_vs_T0.png)

### p_sat_mixing_ratio_heatmap

Joint dependence of saturation vapor pressure p_sat and saturation mixing ratio w_vs on surface temperature T_0 and atmospheric pressure p_a. p_sat depends only on T_0 (Magnus formula) while w_vs = M_w p_sat / (M_a p_a) also decreases with increasing p_a.

**Time span:** 0.0 → 1.0

**Swept over:** `T_0`, `p_a`

![Saturation mixing ratio w_vs(T_0, p_a).](/plots/aerosol/cloud_physics/clouddynamics/p_sat_mixing_ratio_heatmap-w_vs_T0_pa_heatmap.png)

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "reference": {
    "citation": "Seinfeld, J. H., and Pandis, S. N. (2006). Atmospheric Chemistry and Physics: From Air Pollution to Climate Change, 2nd Edition, John Wiley & Sons, Chapter 17. Key equations: Eq. 17.43 (dew-point temperature), Eq. 17.44 (dry adiabatic lapse rate), Eq. 17.46 (saturation mixing ratio), Eq. 17.49 (LCL height).",
    "notes": "source_ref: Aerosol.jl@c8c640bb636b22f2425460e9ed5cba50793bfee1:src/cloud_physics.jl:455\n\nUpstream CloudDynamics is a pure-algebraic MTK @component. It declares 9 @constants (M_w, M_a, R, g, c_p_air, p_sat_ref, magnus_a, T_magnus_offset, magnus_b) and 4 @parameters (T_0, RH, p_a, ΔH_v) and 5 @variables (Γ_d, T_d, h_LCL, p_sat, w_vs). All 5 equations use ~ (algebraic). After MTK structural_simplify the compiled system has zero ODE states and all variables become observed quantities. Serialized as type: observed with inline expression, equations array empty — matching the pure-algebraic pattern of cloud_kelvin.esm and kohler.esm in this directory.\n\nEquation derivations:\n  Γ_d ~ g / c_p_air (Eq. 17.44 dry adiabatic lapse rate)\n  p_sat ~ p_sat_ref * exp(magnus_a * (T_0 - T_magnus_offset) / ((T_0 - T_magnus_offset) + magnus_b)) (Magnus saturation vapor pressure)\n  w_vs ~ M_w * p_sat / (M_a * p_a) (saturation mixing ratio)\n  T_d ~ T_0 + (R * T_0² / (ΔH_v * M_w)) * ln(RH) (Eq. 17.43 dew-point)\n  h_LCL ~ (T_0 - T_d) / Γ_d (Eq. 17.49 lifting condensation level)\n\nNote on 'depends_on' in the migration tracker (DropletGrowth, CloudKelvinEffect): CloudDynamics does not call couple() internally; those dependencies are only needed at the CloudPhysics (parent) level where all cloud sub-models are composed together. This file is a self-contained component.\n\nTolerance rationale (rel=1e-9): all outputs are short closed-form expressions; float64 roundoff is at the few-ULP level, rel=1e-9 gives ample headroom."
  },
  "variables": {
    "M_w": {
      "type": "parameter",
      "units": "kg/mol",
      "default": 0.018015,
      "description": "Molecular weight of water."
    },
    "M_a": {
      "type": "parameter",
      "units": "kg/mol",
      "default": 0.02897,
      "description": "Molecular weight of dry air."
    },
    "R": {
      "type": "parameter",
      "units": "J/(mol*K)",
      "default": 8.314,
      "description": "Universal gas constant."
    },
    "g": {
      "type": "parameter",
      "units": "m/s^2",
      "default": 9.81,
      "description": "Gravitational acceleration."
    },
    "c_p_air": {
      "type": "parameter",
      "units": "J/(kg*K)",
      "default": 1005.0,
      "description": "Specific heat of air at constant pressure."
    },
    "p_sat_ref": {
      "type": "parameter",
      "units": "Pa",
      "default": 610.94,
      "description": "Magnus formula reference saturation pressure at 0°C."
    },
    "magnus_a": {
      "type": "parameter",
      "units": "1",
      "default": 17.625,
      "description": "Magnus formula coefficient a (dimensionless)."
    },
    "T_magnus_offset": {
      "type": "parameter",
      "units": "K",
      "default": 273.15,
      "description": "Magnus formula temperature offset (0°C in Kelvin)."
    },
    "magnus_b": {
      "type": "parameter",
      "units": "K",
      "default": 243.04,
      "description": "Magnus formula coefficient b."
    },
    "T_0": {
      "type": "parameter",
      "units": "K",
      "default": 293.15,
      "description": "Initial (surface) temperature of the air parcel. Default 293.15 K (20°C)."
    },
    "RH": {
      "type": "parameter",
      "units": "1",
      "default": 0.8,
      "description": "Relative humidity (dimensionless, 0–1). Default 0.8 (80 %)."
    },
    "p_a": {
      "type": "parameter",
      "units": "Pa",
      "default": 101325.0,
      "description": "Atmospheric pressure. Default 101325 Pa (1 atm)."
    },
    "ΔH_v": {
      "type": "parameter",
      "units": "J/kg",
      "default": 2500000.0,
      "description": "Latent heat of vaporization. Default 2.5×10⁶ J/kg (S&P Table 17.1, at 0°C)."
    },
    "Γ_d": {
      "type": "unknown",
      "units": "K/m",
      "description": "Dry adiabatic lapse rate Γ_d = g/c_p ≈ 9.76 K/km (Eq. 17.44). Constant for a given gravitational field and specific heat."
    },
    "p_sat": {
      "type": "unknown",
      "units": "Pa",
      "description": "Saturation vapor pressure at T_0, computed via the Magnus formula. p_sat ≈ 2333 Pa at 20°C."
    },
    "w_vs": {
      "type": "unknown",
      "units": "1",
      "description": "Saturation water vapor mixing ratio w_vs = M_w p_sat / (M_a p_a) (Eq. 17.46, dimensionless mass ratio)."
    },
    "T_d": {
      "type": "unknown",
      "units": "K",
      "description": "Dew-point temperature T_d = T_0 + (R T_0² / (ΔH_v M_w)) ln(RH) (Eq. 17.43). T_d ≤ T_0 with equality at RH=1."
    },
    "h_LCL": {
      "type": "unknown",
      "units": "m",
      "description": "Lifting condensation level height h_LCL = (T_0 - T_d) / Γ_d (Eq. 17.49). Height at which a rising air parcel cools to its dew point and cloud base forms. h_LCL ≥ 0 with equality at RH=1."
    }
  },
  "equations": [
    {
      "lhs": "Γ_d",
      "rhs": {
        "op": "/",
        "args": [
          "g",
          "c_p_air"
        ]
      }
    },
    {
      "lhs": "p_sat",
      "rhs": {
        "op": "*",
        "args": [
          "p_sat_ref",
          {
            "op": "exp",
            "args": [
              {
                "op": "/",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      "magnus_a",
                      {
                        "op": "+",
                        "args": [
                          "T_0",
                          {
                            "op": "*",
                            "args": [
                              -1,
                              "T_magnus_offset"
                            ]
                          }
                        ]
                      }
                    ]
                  },
                  {
                    "op": "+",
                    "args": [
                      {
                        "op": "+",
                        "args": [
                          "T_0",
                          {
                            "op": "*",
                            "args": [
                              -1,
                              "T_magnus_offset"
                            ]
                          }
                        ]
                      },
                      "magnus_b"
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "w_vs",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "*",
            "args": [
              "M_w",
              "p_sat"
            ]
          },
          {
            "op": "*",
            "args": [
              "M_a",
              "p_a"
            ]
          }
        ]
      }
    },
    {
      "lhs": "T_d",
      "rhs": {
        "op": "+",
        "args": [
          "T_0",
          {
            "op": "*",
            "args": [
              {
                "op": "/",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      "R",
                      {
                        "op": "^",
                        "args": [
                          "T_0",
                          2
                        ]
                      }
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "ΔH_v",
                      "M_w"
                    ]
                  }
                ]
              },
              {
                "op": "log",
                "args": [
                  "RH"
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "h_LCL",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "+",
            "args": [
              "T_0",
              {
                "op": "*",
                "args": [
                  -1,
                  "T_d"
                ]
              }
            ]
          },
          "Γ_d"
        ]
      }
    }
  ],
  "tolerance": {
    "rel": 1e-09
  },
  "tests": [
    {
      "id": "default_parameters",
      "description": "Default parameterization: T_0=293.15 K (20°C), RH=0.8 (80%), p_a=101325 Pa, ΔH_v=2.5e6 J/kg. Expected: Γ_d=0.00976119 K/m, p_sat=2333.44 Pa, w_vs=0.01432, T_d=289.610 K, h_LCL=362.66 m. All outputs are time-invariant; same values at t=0 and t=1.",
      "parameter_overrides": {},
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "Γ_d",
          "time": 0.0,
          "expected": 0.009761194029850746
        },
        {
          "variable": "Γ_d",
          "time": 1.0,
          "expected": 0.009761194029850746
        },
        {
          "variable": "p_sat",
          "time": 0.0,
          "expected": 2333.4406230993577
        },
        {
          "variable": "p_sat",
          "time": 1.0,
          "expected": 2333.4406230993577
        },
        {
          "variable": "w_vs",
          "time": 0.0,
          "expected": 0.014320754941837679
        },
        {
          "variable": "w_vs",
          "time": 1.0,
          "expected": 0.014320754941837679
        },
        {
          "variable": "T_d",
          "time": 0.0,
          "expected": 289.6100275457325
        },
        {
          "variable": "T_d",
          "time": 1.0,
          "expected": 289.6100275457325
        },
        {
          "variable": "h_LCL",
          "time": 0.0,
          "expected": 362.65772849528986
        },
        {
          "variable": "h_LCL",
          "time": 1.0,
          "expected": 362.65772849528986
        }
      ]
    },
    {
      "id": "saturation_rh_100",
      "description": "At RH=1.0 (100% humidity) the dew point equals the air temperature and the parcel is already at saturation: T_d = T_0 = 293.15 K and h_LCL = 0 m. This is the log(1)=0 case in Eq. 17.43.",
      "parameter_overrides": {
        "RH": 1.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "T_d",
          "time": 0.0,
          "expected": 293.15
        },
        {
          "variable": "T_d",
          "time": 1.0,
          "expected": 293.15
        },
        {
          "variable": "h_LCL",
          "time": 0.0,
          "expected": 0.0
        },
        {
          "variable": "h_LCL",
          "time": 1.0,
          "expected": 0.0
        }
      ]
    },
    {
      "id": "dew_point_rh_0_6",
      "description": "At RH=0.6 (60%) the dew point depression is larger than at RH=0.8. T_d=285.046 K and h_LCL=830.20 m. Comparing with the default (RH=0.8) confirms the monotonic relation: lower RH → lower T_d → higher h_LCL.",
      "parameter_overrides": {
        "RH": 0.6
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "T_d",
          "time": 0.0,
          "expected": 285.04620929479916
        },
        {
          "variable": "h_LCL",
          "time": 0.0,
          "expected": 830.2048581780659
        }
      ]
    },
    {
      "id": "dry_air_rh_0_5",
      "description": "At RH=0.5 (50%) the LCL height reaches 1126.5 m. Confirms h_LCL increases monotonically as RH decreases from the RH=0.6 case.",
      "parameter_overrides": {
        "RH": 0.5
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "T_d",
          "time": 0.0,
          "expected": 282.15384119781146
        },
        {
          "variable": "h_LCL",
          "time": 0.0,
          "expected": 1126.5177977777228
        }
      ]
    },
    {
      "id": "lapse_rate_is_constant",
      "description": "Γ_d = g / c_p_air is a constant that does not depend on temperature, humidity, or pressure. At T_0=263.15 K (cold) and T_0=303.15 K (warm) Γ_d must equal the default value 0.00976119 K/m.",
      "parameter_overrides": {
        "T_0": 263.15
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "Γ_d",
          "time": 0.0,
          "expected": 0.009761194029850746
        }
      ]
    },
    {
      "id": "cold_temperature_T0_263",
      "description": "At T_0=263.15 K (freezing point), the saturation vapor pressure drops to 286.77 Pa and the saturation mixing ratio falls to 0.00176. The dew-point depression (T_0 - T_d) is smaller than at 293.15 K because the dew-point derivative dT_d/dT_0 ≈ 1 + (2R T_0/(ΔH_v M_w)) ln(RH) approaches 1 as T_0 decreases; h_LCL = 292.23 m.",
      "parameter_overrides": {
        "T_0": 263.15
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "p_sat",
          "time": 0.0,
          "expected": 286.77296061847886
        },
        {
          "variable": "w_vs",
          "time": 0.0,
          "expected": 0.0017599784851211257
        },
        {
          "variable": "T_d",
          "time": 0.0,
          "expected": 260.2974922415886
        },
        {
          "variable": "h_LCL",
          "time": 0.0,
          "expected": 292.22938809413193
        }
      ]
    },
    {
      "id": "warm_temperature_T0_303",
      "description": "At T_0=303.15 K (30°C), the saturation vapor pressure jumps to 4236.65 Pa and the saturation mixing ratio rises to 0.02600 (nearly 2× the 20°C value). The larger dew-point depression shifts h_LCL to 387.82 m.",
      "parameter_overrides": {
        "T_0": 303.15
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "p_sat",
          "time": 0.0,
          "expected": 4236.650251295475
        },
        {
          "variable": "w_vs",
          "time": 0.0,
          "expected": 0.026001103016065095
        },
        {
          "variable": "T_d",
          "time": 0.0,
          "expected": 299.3643955736917
        },
        {
          "variable": "h_LCL",
          "time": 0.0,
          "expected": 387.8218601875457
        }
      ]
    }
  ],
  "analyses": [
    {
      "id": "dew_point_vs_rh",
      "description": "Dew-point temperature T_d and LCL height h_LCL as a function of relative humidity RH at T_0=293.15 K. As RH decreases from 1 to 0.2 the dew-point depression grows and the cloud base rises (Eq. 17.43 and 17.49).",
      "parameters": {},
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "parameter_sweep": {
        "type": "cartesian",
        "dimensions": [
          {
            "parameter": "RH",
            "range": {
              "start": 0.2,
              "stop": 1.0,
              "count": 50,
              "scale": "linear"
            }
          }
        ]
      },
      "plots": [
        {
          "id": "T_d_vs_RH",
          "type": "line",
          "description": "Dew-point temperature T_d as a function of relative humidity RH at T_0=293.15 K.",
          "x": {
            "variable": "RH",
            "label": "Relative humidity RH (dimensionless)"
          },
          "y": {
            "variable": "T_d",
            "label": "Dew-point temperature T_d (K)"
          }
        },
        {
          "id": "h_LCL_vs_RH",
          "type": "line",
          "description": "LCL height h_LCL as a function of relative humidity at T_0=293.15 K.",
          "x": {
            "variable": "RH",
            "label": "Relative humidity RH (dimensionless)"
          },
          "y": {
            "variable": "h_LCL",
            "label": "LCL height h_LCL (m)"
          }
        }
      ]
    },
    {
      "id": "lcl_height_vs_temperature",
      "description": "LCL height h_LCL as a function of surface temperature T_0 at RH=0.8. Although higher T_0 increases the dew-point depression (larger numerator in T_0 - T_d), h_LCL depends on the interplay of the T_0-linear dew-point formula and the constant lapse rate; the net effect is a monotonic increase.",
      "parameters": {},
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "parameter_sweep": {
        "type": "cartesian",
        "dimensions": [
          {
            "parameter": "T_0",
            "range": {
              "start": 263.15,
              "stop": 313.15,
              "count": 50,
              "scale": "linear"
            }
          }
        ]
      },
      "plots": [
        {
          "id": "h_LCL_vs_T0",
          "type": "line",
          "description": "LCL height h_LCL vs surface temperature T_0 at RH=0.8.",
          "x": {
            "variable": "T_0",
            "label": "Surface temperature T_0 (K)"
          },
          "y": {
            "variable": "h_LCL",
            "label": "LCL height h_LCL (m)"
          }
        }
      ]
    },
    {
      "id": "p_sat_mixing_ratio_heatmap",
      "description": "Joint dependence of saturation vapor pressure p_sat and saturation mixing ratio w_vs on surface temperature T_0 and atmospheric pressure p_a. p_sat depends only on T_0 (Magnus formula) while w_vs = M_w p_sat / (M_a p_a) also decreases with increasing p_a.",
      "parameters": {},
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "parameter_sweep": {
        "type": "cartesian",
        "dimensions": [
          {
            "parameter": "T_0",
            "range": {
              "start": 263.15,
              "stop": 313.15,
              "count": 30,
              "scale": "linear"
            }
          },
          {
            "parameter": "p_a",
            "range": {
              "start": 70000.0,
              "stop": 110000.0,
              "count": 20,
              "scale": "linear"
            }
          }
        ]
      },
      "plots": [
        {
          "id": "w_vs_T0_pa_heatmap",
          "type": "heatmap",
          "description": "Saturation mixing ratio w_vs(T_0, p_a).",
          "x": {
            "variable": "T_0",
            "label": "Surface temperature T_0 (K)"
          },
          "y": {
            "variable": "p_a",
            "label": "Atmospheric pressure p_a (Pa)"
          },
          "value": {
            "variable": "w_vs",
            "reduce": "final"
          }
        }
      ]
    }
  ]
}
```

</details>
