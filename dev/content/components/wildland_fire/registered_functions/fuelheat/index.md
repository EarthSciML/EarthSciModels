---
title: "FuelHeat"
slug: "fuelheat"
domains: ["wildland_fire"]
component_types: ["model"]
subdomains: ["registered_functions"]
domain: "wildland_fire"
subdomain: "registered_functions"
component_type: "model"
esm_version: "1.0.0"
esm_path: "components/wildland_fire/registered_functions/fuel_heat.esm"
reference: "Anderson, H.E. (1982). Aids to determining fuel models for estimating fire behavior. USDA Forest Service Gen. Tech. Rep. INT-122."
description: "Anderson (1982) 13-fuel-model heat content lookup: maps integer fuel model code (1–13) to low heat content in J/kg (8,000 BTU/lb for all Anderson models = 18,608,000 J/kg). Non-burnable LANDFIRE codes (91-99) and out-of-range codes return 0.0 J/kg. Migrated from WildlandFire.jl src/coupling.jl:127 (`@register_symbolic fuel_heat`). NOTE: fuel_heat is implementable without a lookup table because all 13 Anderson models share the same h=8000 BTU/lb; see reference notes on the gt-p3ep blocking gap for the other fuel_* functions."
tags: ["wildland_fire", "registered_functions", "model", "fuel_model", "anderson1982", "registered_function", "lookup"]
---

## Description

Anderson (1982) 13-fuel-model heat content lookup: maps integer fuel model code (1–13) to low heat content in J/kg (8,000 BTU/lb for all Anderson models = 18,608,000 J/kg). Non-burnable LANDFIRE codes (91-99) and out-of-range codes return 0.0 J/kg. Migrated from WildlandFire.jl src/coupling.jl:127 (`@register_symbolic fuel_heat`). NOTE: fuel_heat is implementable without a lookup table because all 13 Anderson models share the same h=8000 BTU/lb; see reference notes on the gt-p3ep blocking gap for the other fuel_* functions.

## Reference

Anderson, H.E. (1982). Aids to determining fuel models for estimating fire behavior. USDA Forest Service Gen. Tech. Rep. INT-122.

_source_ref: WildlandFire.jl:src/coupling.jl:127
Upstream `fuel_heat(code)` is a @register_symbolic Julia function. It maps an Anderson (1982) fuel model code (integer 1–13) to low heat content in J/kg, built from ANDERSON_FUEL_DATA (src/level_set_fire_spread.jl:334) where h=8000 BTU/lb for all 13 models, converted to SI: 8000 × 2326 = 18,608,000 J/kg. Non-burnable LANDFIRE codes (91=urban, 92=snow/ice, 93=agriculture, 98=water, 99=barren) and any unrecognized code return the default value 0.0 J/kg (zero heat → zero Rothermel reaction intensity → zero fire spread rate).

Implementation note: Because all 13 Anderson models share the same h=8000 BTU/lb, fuel_heat reduces to a piecewise constant expressible with ifelse/and AST ops without a table_lookup. The other five fuel_* registered functions (fuel_savr, fuel_load, fuel_depth, fuel_mce, fuel_weight) have varying values across models and require discrete-categorical lookup.

TODO_GAP gt-p3ep: The blocking gap gt-p3ep('lookup') covers the general fuel_* family. function_tables (ESM 0.4.0 §9.5) supports only linear interpolation over continuous axes; it cannot represent discrete integer-keyed categorical lookups with a separate default for unmapped codes. fuel_heat is the sole exception because the uniformity of h across models lets it degenerate to a step function. When gt-p3ep is resolved (adding nearest-neighbor / index interpolation mode to function_tables, or restoring a cross-file function registry), the other five fuel_* ESMs and FuelModelLookup can be migrated.

Tolerance: observed-only algebraic model (no ODE); tolerance={abs:0, rel:0} — exact IEEE-754 float64 arithmetic on literal constants propagated through ifelse and comparison ops with integer-valued code inputs._

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `code` | `1` | `1.0` | Anderson 13 fuel model code (1–13). In coupled WRF-SFIRE/LANDFIRE pipelines, sourced from integer raster data. Non-burnable LANDFIRE codes (91-99) return h=0. |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `h` | `J/kg` |  | Low heat content. 18,608,000 J/kg for Anderson codes 1–13 (all models share h=8000 BTU/lb); 0 J/kg for non-burnable LANDFIRE codes and unrecognized codes. |

## Observed expressions

$$
h = \mathrm{ifelse}\left(\mathrm{and}\left(\mathrm{>=}\left(code, 1.0\right), \mathrm{<=}\left(code, 13.0\right)\right), 18608000.0, 0.0\right)
$$
_Low heat content. 18,608,000 J/kg for Anderson codes 1–13 (all models share h=8000 BTU/lb); 0 J/kg for non-burnable LANDFIRE codes and unrecognized codes._

## Analyses

### heat_step_function

Sweep fuel model codes 0–14 to visualise the step function: 0 J/kg for codes outside [1,13], 18,608,000 J/kg for Anderson models 1–13. Illustrates the zero-return for non-burnable/invalid codes.

**Time span:** 0.0 → 1.0

**Swept over:** `code`

![Heat content h (J/kg) as a function of fuel model code — step function: 18,608,000 J/kg for codes 1–13, 0 otherwise.](/plots/wildland_fire/registered_functions/fuelheat/heat_step_function-h_vs_code.png)

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "reference": {
    "citation": "Anderson, H.E. (1982). Aids to determining fuel models for estimating fire behavior. USDA Forest Service Gen. Tech. Rep. INT-122.",
    "notes": "source_ref: WildlandFire.jl:src/coupling.jl:127\nUpstream `fuel_heat(code)` is a @register_symbolic Julia function. It maps an Anderson (1982) fuel model code (integer 1–13) to low heat content in J/kg, built from ANDERSON_FUEL_DATA (src/level_set_fire_spread.jl:334) where h=8000 BTU/lb for all 13 models, converted to SI: 8000 × 2326 = 18,608,000 J/kg. Non-burnable LANDFIRE codes (91=urban, 92=snow/ice, 93=agriculture, 98=water, 99=barren) and any unrecognized code return the default value 0.0 J/kg (zero heat → zero Rothermel reaction intensity → zero fire spread rate).\n\nImplementation note: Because all 13 Anderson models share the same h=8000 BTU/lb, fuel_heat reduces to a piecewise constant expressible with ifelse/and AST ops without a table_lookup. The other five fuel_* registered functions (fuel_savr, fuel_load, fuel_depth, fuel_mce, fuel_weight) have varying values across models and require discrete-categorical lookup.\n\nTODO_GAP gt-p3ep: The blocking gap gt-p3ep('lookup') covers the general fuel_* family. function_tables (ESM 0.4.0 §9.5) supports only linear interpolation over continuous axes; it cannot represent discrete integer-keyed categorical lookups with a separate default for unmapped codes. fuel_heat is the sole exception because the uniformity of h across models lets it degenerate to a step function. When gt-p3ep is resolved (adding nearest-neighbor / index interpolation mode to function_tables, or restoring a cross-file function registry), the other five fuel_* ESMs and FuelModelLookup can be migrated.\n\nTolerance: observed-only algebraic model (no ODE); tolerance={abs:0, rel:0} — exact IEEE-754 float64 arithmetic on literal constants propagated through ifelse and comparison ops with integer-valued code inputs."
  },
  "tolerance": {
    "abs": 0.0,
    "rel": 0.0
  },
  "variables": {
    "code": {
      "type": "parameter",
      "units": "1",
      "default": 1.0,
      "description": "Anderson 13 fuel model code (1–13). In coupled WRF-SFIRE/LANDFIRE pipelines, sourced from integer raster data. Non-burnable LANDFIRE codes (91-99) return h=0."
    },
    "h": {
      "type": "unknown",
      "units": "J/kg",
      "description": "Low heat content. 18,608,000 J/kg for Anderson codes 1–13 (all models share h=8000 BTU/lb); 0 J/kg for non-burnable LANDFIRE codes and unrecognized codes."
    }
  },
  "equations": [
    {
      "lhs": "h",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "and",
            "args": [
              {
                "op": ">=",
                "args": [
                  "code",
                  1.0
                ]
              },
              {
                "op": "<=",
                "args": [
                  "code",
                  13.0
                ]
              }
            ]
          },
          18608000.0,
          0.0
        ]
      }
    }
  ],
  "tests": [
    {
      "id": "code_1_short_grass",
      "description": "Anderson fuel model 1 (short grass): code=1 → h=18,608,000 J/kg (8000 BTU/lb × 2326 J/BTU). Lowest-numbered valid Anderson model.",
      "parameter_overrides": {
        "code": 1.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "h",
          "time": 0.0,
          "expected": 18608000.0,
          "tolerance": {
            "abs": 0.0,
            "rel": 0.0
          }
        }
      ]
    },
    {
      "id": "code_7_southern_rough",
      "description": "Anderson fuel model 7 (southern rough): code=7 → h=18,608,000 J/kg. Mid-range model; confirms uniformity across the Anderson table.",
      "parameter_overrides": {
        "code": 7.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "h",
          "time": 0.0,
          "expected": 18608000.0,
          "tolerance": {
            "abs": 0.0,
            "rel": 0.0
          }
        }
      ]
    },
    {
      "id": "code_13_heavy_slash",
      "description": "Anderson fuel model 13 (heavy logging slash): code=13 → h=18,608,000 J/kg. Highest-numbered valid Anderson model.",
      "parameter_overrides": {
        "code": 13.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "h",
          "time": 0.0,
          "expected": 18608000.0,
          "tolerance": {
            "abs": 0.0,
            "rel": 0.0
          }
        }
      ]
    },
    {
      "id": "nonburnable_urban",
      "description": "Non-burnable LANDFIRE code 91 (urban): h=0.0 J/kg. Zero heat content → zero Rothermel reaction intensity → zero fire spread rate.",
      "parameter_overrides": {
        "code": 91.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "h",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "abs": 0.0,
            "rel": 0.0
          }
        }
      ]
    },
    {
      "id": "invalid_below_range",
      "description": "Code 0 (below the valid range 1–13): h=0.0 J/kg (default for unrecognized codes, matching WildlandFire.jl _lookup_fuel default=0.0).",
      "parameter_overrides": {
        "code": 0.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "h",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "abs": 0.0,
            "rel": 0.0
          }
        }
      ]
    },
    {
      "id": "invalid_above_range",
      "description": "Code 14 (above the valid range 1–13): h=0.0 J/kg. Confirms the upper boundary condition (>13 → out-of-range → 0).",
      "parameter_overrides": {
        "code": 14.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "h",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "abs": 0.0,
            "rel": 0.0
          }
        }
      ]
    }
  ],
  "analyses": [
    {
      "id": "heat_step_function",
      "description": "Sweep fuel model codes 0–14 to visualise the step function: 0 J/kg for codes outside [1,13], 18,608,000 J/kg for Anderson models 1–13. Illustrates the zero-return for non-burnable/invalid codes.",
      "initial_state": {},
      "parameters": {
        "code": 1.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "parameter_sweep": {
        "type": "cartesian",
        "dimensions": [
          {
            "parameter": "code",
            "range": {
              "start": 0.0,
              "stop": 14.0,
              "count": 15,
              "scale": "linear"
            }
          }
        ]
      },
      "plots": [
        {
          "id": "h_vs_code",
          "type": "line",
          "description": "Heat content h (J/kg) as a function of fuel model code — step function: 18,608,000 J/kg for codes 1–13, 0 otherwise.",
          "x": {
            "variable": "code",
            "label": "fuel model code"
          },
          "y": {
            "variable": "h",
            "label": "h (J/kg)"
          }
        }
      ]
    }
  ]
}
```

</details>
