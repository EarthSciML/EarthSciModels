---
title: "FuelDepth"
slug: "fueldepth"
domains: ["wildland_fire"]
component_types: ["model"]
subdomains: ["registered_functions"]
domain: "wildland_fire"
subdomain: "registered_functions"
component_type: "model"
esm_version: "1.0.0"
esm_path: "components/wildland_fire/registered_functions/fuel_depth.esm"
reference: "Anderson, H.E. (1982). Aids to determining fuel models for estimating fire behavior. USDA Forest Service Gen. Tech. Rep. INT-122."
description: "Anderson (1982) 13-fuel-model fuel-bed depth lookup: maps integer fuel model code (1–13) to fuel bed depth δ in metres, converted from the upstream ft values in ANDERSON_FUEL_DATA via δ_m = depth_ft × 0.3048. Out-of-range codes (including LANDFIRE non-burnable codes 91–99) return the fuel-model-1 default 1.0 × 0.3048 = 0.3048 m. Migrated from WildlandFire.jl src/coupling.jl:125 (`@register_symbolic fuel_depth`). Resolves the gt-p3ep blocking gap via ifelse + interp.linear over the integer axis [1..13]."
tags: ["wildland_fire", "registered_functions", "model", "fuel_model", "anderson1982", "registered_function", "lookup"]
---

## Description

Anderson (1982) 13-fuel-model fuel-bed depth lookup: maps integer fuel model code (1–13) to fuel bed depth δ in metres, converted from the upstream ft values in ANDERSON_FUEL_DATA via δ_m = depth_ft × 0.3048. Out-of-range codes (including LANDFIRE non-burnable codes 91–99) return the fuel-model-1 default 1.0 × 0.3048 = 0.3048 m. Migrated from WildlandFire.jl src/coupling.jl:125 (`@register_symbolic fuel_depth`). Resolves the gt-p3ep blocking gap via ifelse + interp.linear over the integer axis [1..13].

## Reference

Anderson, H.E. (1982). Aids to determining fuel models for estimating fire behavior. USDA Forest Service Gen. Tech. Rep. INT-122.

_source_ref: WildlandFire.jl@126976f2508ceacca6c486b21ae6da5b168c6f46:src/coupling.jl:125

Upstream `fuel_depth(code)` is a @register_symbolic Julia function:
  const _FUEL_DEPTH = Dict(k => v.depth * 0.3048 for (k, v) in ANDERSON_FUEL_DATA)
  fuel_depth(code) = _lookup_fuel(_FUEL_DEPTH, code, 1.0 * 0.3048)
  @register_symbolic fuel_depth(code)

where ANDERSON_FUEL_DATA.depth values (in ft) are (from Anderson 1982 / Mandel et al. 2011 Table 1):
  codes 1, 2:    1.0  ft → 0.3048 m
  code  3:       2.5  ft → 0.762  m
  code  4:       6.0  ft → 1.8288 m
  code  5:       2.0  ft → 0.6096 m
  codes 6, 7:    2.5  ft → 0.762  m
  codes 8, 9:    0.2  ft → 0.06096 m
  codes 10, 11:  1.0  ft → 0.3048 m
  code  12:      2.3  ft → 0.70104 m
  code  13:      3.0  ft → 0.9144  m

Default for out-of-range codes: 1.0 ft * 0.3048 = 0.3048 m (fuel model 1). This matches the upstream _lookup_fuel fallback (default argument = 1.0 * 0.3048).

Non-burnable LANDFIRE codes (91, 92, 93, 98, 99) are outside [1, 13] and return 0.3048 m. In practice, fire spread is zero for non-burnable codes regardless of depth because fuel_heat returns 0 for those codes, zeroing Rothermel Reaction Intensity and Rate of Spread.

gt-p3ep resolution: ESM 0.4.0 §9.5 interp.linear supports continuous-axis interpolation. For discrete integer-keyed lookup with separate default, we compose ifelse(AND(code>=1, code<=13), interp.linear(...), default). interp.linear at an exact integer grid knot returns the stored value (blend weight 0 or 1 at the endpoints). Out-of-range codes return the default 0.3048 m exactly.

Tolerance: observed-only algebraic model (no ODE); tolerance={rel:1e-12} — interp.linear on float64 hardware at grid knots is exact for the default branch (literal constant); 1e-12 covers the one-ULP float64 rounding without admitting any physical imprecision._

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `code` | `1` | `1.0` | Anderson 13 fuel model code (dimensionless integer 1–13). Values outside this range return the fuel-model-1 default depth. |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `fuel_depth` | `m` |  | Fuel bed depth δ (m). Encodes the Anderson (1982) depth parameter for the given fuel model code. Used by FuelModelLookup to set the δ input for the Rothermel spread-rate equations. |

## Observed expressions

$$
fuel_{depth} = \mathrm{ifelse}\left(\mathrm{and}\left(\mathrm{>=}\left(code, 1.0\right), \mathrm{<=}\left(code, 13.0\right)\right), \mathrm{fn}\left(\mathrm{const}\left(\right), \mathrm{const}\left(\right), code\right), 0.3048\right)
$$
_Fuel bed depth δ (m). Encodes the Anderson (1982) depth parameter for the given fuel model code. Used by FuelModelLookup to set the δ input for the Rothermel spread-rate equations._

## Analyses

### fuel_depth_by_code

Fuel bed depth δ (m) for each Anderson 13 fuel model code, showing the range from shallow timber litter (0.06 m) to deep chaparral (1.83 m). Compare with Table 1 of Mandel et al. (2011).

**Time span:** 0.0 → 1.0

**Swept over:** `code`

![depth_by_code](/plots/wildland_fire/registered_functions/fueldepth/fuel_depth_by_code-depth_by_code.png)

### default_for_nonburnable_codes

Out-of-range inputs (including LANDFIRE non-burnable codes 91-99) return the FM1 default 0.3048 m.

**Time span:** 0.0 → 1.0

**Swept over:** `code`

![depth_nonburnable](/plots/wildland_fire/registered_functions/fueldepth/default_for_nonburnable_codes-depth_nonburnable.png)

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "reference": {
    "citation": "Anderson, H.E. (1982). Aids to determining fuel models for estimating fire behavior. USDA Forest Service Gen. Tech. Rep. INT-122.",
    "notes": "source_ref: WildlandFire.jl@126976f2508ceacca6c486b21ae6da5b168c6f46:src/coupling.jl:125\n\nUpstream `fuel_depth(code)` is a @register_symbolic Julia function:\n  const _FUEL_DEPTH = Dict(k => v.depth * 0.3048 for (k, v) in ANDERSON_FUEL_DATA)\n  fuel_depth(code) = _lookup_fuel(_FUEL_DEPTH, code, 1.0 * 0.3048)\n  @register_symbolic fuel_depth(code)\n\nwhere ANDERSON_FUEL_DATA.depth values (in ft) are (from Anderson 1982 / Mandel et al. 2011 Table 1):\n  codes 1, 2:    1.0  ft → 0.3048 m\n  code  3:       2.5  ft → 0.762  m\n  code  4:       6.0  ft → 1.8288 m\n  code  5:       2.0  ft → 0.6096 m\n  codes 6, 7:    2.5  ft → 0.762  m\n  codes 8, 9:    0.2  ft → 0.06096 m\n  codes 10, 11:  1.0  ft → 0.3048 m\n  code  12:      2.3  ft → 0.70104 m\n  code  13:      3.0  ft → 0.9144  m\n\nDefault for out-of-range codes: 1.0 ft * 0.3048 = 0.3048 m (fuel model 1). This matches the upstream _lookup_fuel fallback (default argument = 1.0 * 0.3048).\n\nNon-burnable LANDFIRE codes (91, 92, 93, 98, 99) are outside [1, 13] and return 0.3048 m. In practice, fire spread is zero for non-burnable codes regardless of depth because fuel_heat returns 0 for those codes, zeroing Rothermel Reaction Intensity and Rate of Spread.\n\ngt-p3ep resolution: ESM 0.4.0 §9.5 interp.linear supports continuous-axis interpolation. For discrete integer-keyed lookup with separate default, we compose ifelse(AND(code>=1, code<=13), interp.linear(...), default). interp.linear at an exact integer grid knot returns the stored value (blend weight 0 or 1 at the endpoints). Out-of-range codes return the default 0.3048 m exactly.\n\nTolerance: observed-only algebraic model (no ODE); tolerance={rel:1e-12} — interp.linear on float64 hardware at grid knots is exact for the default branch (literal constant); 1e-12 covers the one-ULP float64 rounding without admitting any physical imprecision."
  },
  "tolerance": {
    "rel": 1e-12
  },
  "variables": {
    "code": {
      "type": "parameter",
      "units": "1",
      "default": 1.0,
      "description": "Anderson 13 fuel model code (dimensionless integer 1–13). Values outside this range return the fuel-model-1 default depth."
    },
    "fuel_depth": {
      "type": "unknown",
      "units": "m",
      "description": "Fuel bed depth δ (m). Encodes the Anderson (1982) depth parameter for the given fuel model code. Used by FuelModelLookup to set the δ input for the Rothermel spread-rate equations."
    }
  },
  "equations": [
    {
      "lhs": "fuel_depth",
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
          {
            "op": "fn",
            "name": "interp.linear",
            "args": [
              {
                "op": "const",
                "value": [
                  0.3048,
                  0.3048,
                  0.762,
                  1.8288,
                  0.6096,
                  0.762,
                  0.762,
                  0.06096,
                  0.06096,
                  0.3048,
                  0.3048,
                  0.70104,
                  0.9144
                ],
                "args": []
              },
              {
                "op": "const",
                "value": [
                  1.0,
                  2.0,
                  3.0,
                  4.0,
                  5.0,
                  6.0,
                  7.0,
                  8.0,
                  9.0,
                  10.0,
                  11.0,
                  12.0,
                  13.0
                ],
                "args": []
              },
              "code"
            ]
          },
          0.3048
        ]
      }
    }
  ],
  "tests": [
    {
      "id": "fm1_short_grass",
      "description": "Fuel model 1 (short grass): depth=1.0 ft → δ=0.3048 m. Lowest-numbered valid Anderson model.",
      "parameter_overrides": {
        "code": 1.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "fuel_depth",
          "time": 0.0,
          "expected": 0.3048,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "fm2_timber_grass",
      "description": "Fuel model 2 (timber/grass): depth=1.0 ft → same δ as FM1.",
      "parameter_overrides": {
        "code": 2.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "fuel_depth",
          "time": 0.0,
          "expected": 0.3048,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "fm3_tall_grass",
      "description": "Fuel model 3 (tall grass): depth=2.5 ft → δ=0.762 m.",
      "parameter_overrides": {
        "code": 3.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "fuel_depth",
          "time": 0.0,
          "expected": 0.762,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "fm4_chaparral",
      "description": "Fuel model 4 (chaparral): depth=6.0 ft → δ=1.8288 m. Deepest fuel bed among Anderson 13 models.",
      "parameter_overrides": {
        "code": 4.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "fuel_depth",
          "time": 0.0,
          "expected": 1.8288,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "fm5_brush",
      "description": "Fuel model 5 (brush): depth=2.0 ft → δ=0.6096 m.",
      "parameter_overrides": {
        "code": 5.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "fuel_depth",
          "time": 0.0,
          "expected": 0.6096,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "fm8_closed_timber",
      "description": "Fuel model 8 (closed timber litter): depth=0.2 ft → δ=0.06096 m. Shallowest fuel bed among Anderson 13 models.",
      "parameter_overrides": {
        "code": 8.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "fuel_depth",
          "time": 0.0,
          "expected": 0.06096,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "fm13_heavy_logging_slash",
      "description": "Fuel model 13 (heavy logging slash): depth=3.0 ft → δ=0.9144 m. Upper boundary of valid range.",
      "parameter_overrides": {
        "code": 13.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "fuel_depth",
          "time": 0.0,
          "expected": 0.9144,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "nonburnable_urban_code91",
      "description": "LANDFIRE non-burnable code 91 (urban): outside [1, 13] → returns FM1 default 0.3048 m.",
      "parameter_overrides": {
        "code": 91.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "fuel_depth",
          "time": 0.0,
          "expected": 0.3048,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "nonburnable_water_code98",
      "description": "LANDFIRE non-burnable code 98 (water): outside [1, 13] → returns FM1 default 0.3048 m.",
      "parameter_overrides": {
        "code": 98.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "fuel_depth",
          "time": 0.0,
          "expected": 0.3048,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "unrecognized_code0",
      "description": "Unrecognized code 0 (below lower bound): returns FM1 default 0.3048 m.",
      "parameter_overrides": {
        "code": 0.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "fuel_depth",
          "time": 0.0,
          "expected": 0.3048,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "unrecognized_code999",
      "description": "Unrecognized code 999 (far above upper bound): returns FM1 default 0.3048 m.",
      "parameter_overrides": {
        "code": 999.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "fuel_depth",
          "time": 0.0,
          "expected": 0.3048,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    }
  ],
  "analyses": [
    {
      "id": "fuel_depth_by_code",
      "description": "Fuel bed depth δ (m) for each Anderson 13 fuel model code, showing the range from shallow timber litter (0.06 m) to deep chaparral (1.83 m). Compare with Table 1 of Mandel et al. (2011).",
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "parameter_sweep": {
        "type": "cartesian",
        "dimensions": [
          {
            "parameter": "code",
            "values": [
              1.0,
              2.0,
              3.0,
              4.0,
              5.0,
              6.0,
              7.0,
              8.0,
              9.0,
              10.0,
              11.0,
              12.0,
              13.0
            ]
          }
        ]
      },
      "plots": [
        {
          "id": "depth_by_code",
          "type": "scatter",
          "x": {
            "variable": "code",
            "label": "Fuel model code (1-13)"
          },
          "y": {
            "variable": "fuel_depth",
            "label": "δ (m)"
          }
        }
      ]
    },
    {
      "id": "default_for_nonburnable_codes",
      "description": "Out-of-range inputs (including LANDFIRE non-burnable codes 91-99) return the FM1 default 0.3048 m.",
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "parameter_sweep": {
        "type": "cartesian",
        "dimensions": [
          {
            "parameter": "code",
            "values": [
              0.0,
              14.0,
              91.0,
              92.0,
              93.0,
              98.0,
              99.0,
              999.0
            ]
          }
        ]
      },
      "plots": [
        {
          "id": "depth_nonburnable",
          "type": "scatter",
          "x": {
            "variable": "code",
            "label": "Code (out-of-range)"
          },
          "y": {
            "variable": "fuel_depth",
            "label": "δ (m)"
          }
        }
      ]
    }
  ]
}
```

</details>
