---
title: "FuelLoad"
slug: "fuelload"
domains: ["wildland_fire"]
component_types: ["model"]
subdomains: ["registered_functions"]
domain: "wildland_fire"
subdomain: "registered_functions"
component_type: "model"
esm_version: "1.0.0"
esm_path: "components/wildland_fire/registered_functions/fuel_load.esm"
reference: "Anderson, H.E. (1982). Aids to determining fuel models for estimating fire behavior. USDA Forest Service Gen. Tech. Rep. INT-122."
description: "Anderson (1982) 13-fuel-model total fine fuel load lookup: maps integer fuel model code (1–13) to oven-dry fuel load w₀ in kg/m², converted from the upstream lb/ft² values in ANDERSON_FUEL_DATA via w₀_kg_m2 = load_lb_ft2 × (0.45359237/0.09290304). Out-of-range codes (including LANDFIRE non-burnable codes 91–99) return the fuel-model-1 default 0.034 × (0.45359237/0.09290304) ≈ 0.1660 kg/m². Migrated from WildlandFire.jl src/coupling.jl:124 (`@register_symbolic fuel_load`). Resolves the gt-p3ep blocking gap via ifelse + interp.linear over the integer axis [1..13]."
tags: ["wildland_fire", "registered_functions", "model", "fuel_model", "anderson1982", "registered_function", "lookup"]
---

## Description

Anderson (1982) 13-fuel-model total fine fuel load lookup: maps integer fuel model code (1–13) to oven-dry fuel load w₀ in kg/m², converted from the upstream lb/ft² values in ANDERSON_FUEL_DATA via w₀_kg_m2 = load_lb_ft2 × (0.45359237/0.09290304). Out-of-range codes (including LANDFIRE non-burnable codes 91–99) return the fuel-model-1 default 0.034 × (0.45359237/0.09290304) ≈ 0.1660 kg/m². Migrated from WildlandFire.jl src/coupling.jl:124 (`@register_symbolic fuel_load`). Resolves the gt-p3ep blocking gap via ifelse + interp.linear over the integer axis [1..13].

## Reference

Anderson, H.E. (1982). Aids to determining fuel models for estimating fire behavior. USDA Forest Service Gen. Tech. Rep. INT-122.

_source_ref: WildlandFire.jl@126976f2508ceacca6c486b21ae6da5b168c6f46:src/coupling.jl:124

Upstream `fuel_load(code)` is a @register_symbolic Julia function:
  const _FUEL_LOAD = Dict(k => v.load * (0.45359237 / 0.3048^2) for (k, v) in ANDERSON_FUEL_DATA)
  fuel_load(code) = _lookup_fuel(_FUEL_LOAD, code, 0.034 * (0.45359237 / 0.3048^2))
  @register_symbolic fuel_load(code)

where ANDERSON_FUEL_DATA.load values (in lb/ft²) are (from Anderson 1982 / Mandel et al. 2011 Table 1):
  code  1 (short grass):                 0.034 lb/ft² → 0.16600253963702372 kg/m²
  code  2 (timber/grass/shrub):          0.092 lb/ft² → 0.44918334254724060 kg/m²
  code  3 (tall grass):                  0.138 lb/ft² → 0.67377501382086100 kg/m²
  code  4 (chaparral):                   0.230 lb/ft² → 1.12295835636810160 kg/m²
  code  5 (brush):                       0.046 lb/ft² → 0.22459167127362030 kg/m²
  code  6 (dormant brush/hardwood):      0.069 lb/ft² → 0.33688750691043050 kg/m²
  code  7 (southern rough):              0.052 lb/ft² → 0.25388623709191860 kg/m²
  code  8 (closed timber litter):        0.069 lb/ft² → 0.33688750691043050 kg/m²
  code  9 (hardwood litter):             0.134 lb/ft² → 0.65424530327532870 kg/m²
  code 10 (timber litter/understory):    0.138 lb/ft² → 0.67377501382086100 kg/m²
  code 11 (light logging slash):         0.069 lb/ft² → 0.33688750691043050 kg/m²
  code 12 (medium logging slash):        0.184 lb/ft² → 0.89836668509448130 kg/m²
  code 13 (heavy logging slash):         0.322 lb/ft² → 1.57214169891534230 kg/m²

Default for out-of-range codes: 0.034 lb/ft² × (0.45359237/0.09290304) = 0.16600253963702372 kg/m²
(fuel model 1). This matches the upstream _lookup_fuel fallback.

Non-burnable LANDFIRE codes (91, 92, 93, 98, 99) are outside [1, 13] and
return the FM1 default 0.166 kg/m². In practice, fire spread is zero for
non-burnable codes regardless of fuel load because fuel_heat returns 0 for
those codes, zeroing Rothermel Reaction Intensity and Rate of Spread.

gt-p3ep resolution: ESM 0.4.0 §9.5 interp.linear supports continuous-axis
interpolation. For discrete integer-keyed lookup with separate default, we
compose ifelse(AND(code>=1, code<=13), interp.linear(...), default).
interp.linear at an exact integer grid knot returns the stored value
(blend weight 0 or 1 at the endpoints). Out-of-range codes return the
default 0.16600253963702372 kg/m² exactly.

Tolerance: observed-only algebraic model (no ODE); tolerance={rel:1e-12} —
interp.linear on float64 hardware at grid knots is exact for in-range codes;
1e-12 covers the one-ULP float64 rounding without admitting any physical
imprecision._

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `code` | `1` | `1.0` | Anderson 13 fuel model code (dimensionless integer 1–13). Values outside this range return the fuel-model-1 default load. |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `fuel_load` | `kg/m^2` |  | Oven-dry total fine fuel load w₀ (kg/m²). Encodes the Anderson (1982) fuel load parameter for the given fuel model code. Used by FuelModelLookup to set the w₀ input for the Rothermel fire spread equations. |

## Observed expressions

$$
fuel_{load} = \mathrm{ifelse}\left(\mathrm{and}\left(\mathrm{>=}\left(code, 1.0\right), \mathrm{<=}\left(code, 13.0\right)\right), \mathrm{fn}\left(\mathrm{const}\left(\right), \mathrm{const}\left(\right), code\right), 0.16600253963702372\right)
$$
_Oven-dry total fine fuel load w₀ (kg/m²). Encodes the Anderson (1982) fuel load parameter for the given fuel model code. Used by FuelModelLookup to set the w₀ input for the Rothermel fire spread equations._

## Analyses

### fuel_load_by_code

Oven-dry fuel load w₀ (kg/m²) for each Anderson 13 fuel model code, showing the range from short grass (0.166 kg/m²) to chaparral (1.123 kg/m²). Compare with Table 1 of Mandel et al. (2011).

**Time span:** 0.0 → 1.0

**Swept over:** `code`

### default_for_nonburnable_codes

Out-of-range inputs (including LANDFIRE non-burnable codes 91-99) return the FM1 default 0.16600 kg/m².

**Time span:** 0.0 → 1.0

**Swept over:** `code`

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "reference": {
    "citation": "Anderson, H.E. (1982). Aids to determining fuel models for estimating fire behavior. USDA Forest Service Gen. Tech. Rep. INT-122.",
    "notes": "source_ref: WildlandFire.jl@126976f2508ceacca6c486b21ae6da5b168c6f46:src/coupling.jl:124\n\nUpstream `fuel_load(code)` is a @register_symbolic Julia function:\n  const _FUEL_LOAD = Dict(k => v.load * (0.45359237 / 0.3048^2) for (k, v) in ANDERSON_FUEL_DATA)\n  fuel_load(code) = _lookup_fuel(_FUEL_LOAD, code, 0.034 * (0.45359237 / 0.3048^2))\n  @register_symbolic fuel_load(code)\n\nwhere ANDERSON_FUEL_DATA.load values (in lb/ft²) are (from Anderson 1982 / Mandel et al. 2011 Table 1):\n  code  1 (short grass):                 0.034 lb/ft² → 0.16600253963702372 kg/m²\n  code  2 (timber/grass/shrub):          0.092 lb/ft² → 0.44918334254724060 kg/m²\n  code  3 (tall grass):                  0.138 lb/ft² → 0.67377501382086100 kg/m²\n  code  4 (chaparral):                   0.230 lb/ft² → 1.12295835636810160 kg/m²\n  code  5 (brush):                       0.046 lb/ft² → 0.22459167127362030 kg/m²\n  code  6 (dormant brush/hardwood):      0.069 lb/ft² → 0.33688750691043050 kg/m²\n  code  7 (southern rough):              0.052 lb/ft² → 0.25388623709191860 kg/m²\n  code  8 (closed timber litter):        0.069 lb/ft² → 0.33688750691043050 kg/m²\n  code  9 (hardwood litter):             0.134 lb/ft² → 0.65424530327532870 kg/m²\n  code 10 (timber litter/understory):    0.138 lb/ft² → 0.67377501382086100 kg/m²\n  code 11 (light logging slash):         0.069 lb/ft² → 0.33688750691043050 kg/m²\n  code 12 (medium logging slash):        0.184 lb/ft² → 0.89836668509448130 kg/m²\n  code 13 (heavy logging slash):         0.322 lb/ft² → 1.57214169891534230 kg/m²\n\nDefault for out-of-range codes: 0.034 lb/ft² × (0.45359237/0.09290304) = 0.16600253963702372 kg/m²\n(fuel model 1). This matches the upstream _lookup_fuel fallback.\n\nNon-burnable LANDFIRE codes (91, 92, 93, 98, 99) are outside [1, 13] and\nreturn the FM1 default 0.166 kg/m². In practice, fire spread is zero for\nnon-burnable codes regardless of fuel load because fuel_heat returns 0 for\nthose codes, zeroing Rothermel Reaction Intensity and Rate of Spread.\n\ngt-p3ep resolution: ESM 0.4.0 §9.5 interp.linear supports continuous-axis\ninterpolation. For discrete integer-keyed lookup with separate default, we\ncompose ifelse(AND(code>=1, code<=13), interp.linear(...), default).\ninterp.linear at an exact integer grid knot returns the stored value\n(blend weight 0 or 1 at the endpoints). Out-of-range codes return the\ndefault 0.16600253963702372 kg/m² exactly.\n\nTolerance: observed-only algebraic model (no ODE); tolerance={rel:1e-12} —\ninterp.linear on float64 hardware at grid knots is exact for in-range codes;\n1e-12 covers the one-ULP float64 rounding without admitting any physical\nimprecision."
  },
  "tolerance": {
    "rel": 1e-12
  },
  "variables": {
    "code": {
      "type": "parameter",
      "units": "1",
      "default": 1.0,
      "description": "Anderson 13 fuel model code (dimensionless integer 1–13). Values outside this range return the fuel-model-1 default load."
    },
    "fuel_load": {
      "type": "unknown",
      "units": "kg/m^2",
      "description": "Oven-dry total fine fuel load w₀ (kg/m²). Encodes the Anderson (1982) fuel load parameter for the given fuel model code. Used by FuelModelLookup to set the w₀ input for the Rothermel fire spread equations."
    }
  },
  "equations": [
    {
      "lhs": "fuel_load",
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
                  0.16600253963702372,
                  0.4491833425472406,
                  0.673775013820861,
                  1.1229583563681016,
                  0.2245916712736203,
                  0.3368875069104305,
                  0.2538862370919186,
                  0.3368875069104305,
                  0.6542453032753287,
                  0.673775013820861,
                  0.3368875069104305,
                  0.8983666850944813,
                  1.5721416989153423
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
          0.16600253963702372
        ]
      }
    }
  ],
  "tests": [
    {
      "id": "fm1_short_grass",
      "description": "Fuel model 1 (short grass): w₀=0.034 lb/ft² → 0.16600 kg/m². Lowest-numbered valid Anderson model and default value for out-of-range codes.",
      "parameter_overrides": {
        "code": 1.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "fuel_load",
          "time": 0.0,
          "expected": 0.16600253963702372,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "fm2_timber_grass",
      "description": "Fuel model 2 (timber/grass/shrub): w₀=0.092 lb/ft² → 0.44918 kg/m².",
      "parameter_overrides": {
        "code": 2.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "fuel_load",
          "time": 0.0,
          "expected": 0.4491833425472406,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "fm3_tall_grass",
      "description": "Fuel model 3 (tall grass): w₀=0.138 lb/ft² → 0.67378 kg/m². Same load as fuel model 10.",
      "parameter_overrides": {
        "code": 3.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "fuel_load",
          "time": 0.0,
          "expected": 0.673775013820861,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "fm4_chaparral",
      "description": "Fuel model 4 (chaparral): w₀=0.230 lb/ft² → 1.12296 kg/m². Highest fuel load among Anderson 13 models.",
      "parameter_overrides": {
        "code": 4.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "fuel_load",
          "time": 0.0,
          "expected": 1.1229583563681016,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "fm5_brush",
      "description": "Fuel model 5 (brush): w₀=0.046 lb/ft² → 0.22459 kg/m².",
      "parameter_overrides": {
        "code": 5.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "fuel_load",
          "time": 0.0,
          "expected": 0.2245916712736203,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "fm7_southern_rough",
      "description": "Fuel model 7 (southern rough): w₀=0.052 lb/ft² → 0.25389 kg/m². Unique value not shared with adjacent models.",
      "parameter_overrides": {
        "code": 7.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "fuel_load",
          "time": 0.0,
          "expected": 0.2538862370919186,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "fm8_closed_timber",
      "description": "Fuel model 8 (closed timber litter): w₀=0.069 lb/ft² → 0.33689 kg/m². Same load as FM6 and FM11.",
      "parameter_overrides": {
        "code": 8.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "fuel_load",
          "time": 0.0,
          "expected": 0.3368875069104305,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "fm9_hardwood_litter",
      "description": "Fuel model 9 (hardwood litter): w₀=0.134 lb/ft² → 0.65425 kg/m². Unique value.",
      "parameter_overrides": {
        "code": 9.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "fuel_load",
          "time": 0.0,
          "expected": 0.6542453032753287,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "fm12_medium_logging_slash",
      "description": "Fuel model 12 (medium logging slash): w₀=0.184 lb/ft² → 0.89837 kg/m². Unique value.",
      "parameter_overrides": {
        "code": 12.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "fuel_load",
          "time": 0.0,
          "expected": 0.8983666850944813,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "fm13_heavy_logging_slash",
      "description": "Fuel model 13 (heavy logging slash): w₀=0.322 lb/ft² → 1.57214 kg/m². Highest-numbered valid Anderson model; second highest load.",
      "parameter_overrides": {
        "code": 13.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "fuel_load",
          "time": 0.0,
          "expected": 1.5721416989153423,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "nonburnable_urban_code91",
      "description": "LANDFIRE non-burnable code 91 (urban): outside [1, 13] → returns FM1 default 0.16600 kg/m².",
      "parameter_overrides": {
        "code": 91.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "fuel_load",
          "time": 0.0,
          "expected": 0.16600253963702372,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "nonburnable_water_code98",
      "description": "LANDFIRE non-burnable code 98 (water): outside [1, 13] → returns FM1 default 0.16600 kg/m².",
      "parameter_overrides": {
        "code": 98.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "fuel_load",
          "time": 0.0,
          "expected": 0.16600253963702372,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "unrecognized_code0",
      "description": "Unrecognized code 0 (below lower bound): returns FM1 default 0.16600 kg/m².",
      "parameter_overrides": {
        "code": 0.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "fuel_load",
          "time": 0.0,
          "expected": 0.16600253963702372,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "unrecognized_code14",
      "description": "Unrecognized code 14 (one above upper bound): returns FM1 default 0.16600 kg/m².",
      "parameter_overrides": {
        "code": 14.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "fuel_load",
          "time": 0.0,
          "expected": 0.16600253963702372,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    }
  ],
  "analyses": [
    {
      "id": "fuel_load_by_code",
      "description": "Oven-dry fuel load w₀ (kg/m²) for each Anderson 13 fuel model code, showing the range from short grass (0.166 kg/m²) to chaparral (1.123 kg/m²). Compare with Table 1 of Mandel et al. (2011).",
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
          "id": "load_by_code",
          "type": "scatter",
          "x": {
            "variable": "code",
            "label": "Fuel model code (1-13)"
          },
          "y": {
            "variable": "fuel_load",
            "label": "w₀ (kg/m²)"
          }
        }
      ]
    },
    {
      "id": "default_for_nonburnable_codes",
      "description": "Out-of-range inputs (including LANDFIRE non-burnable codes 91-99) return the FM1 default 0.16600 kg/m².",
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
              99.0
            ]
          }
        ]
      },
      "plots": [
        {
          "id": "load_nonburnable",
          "type": "scatter",
          "x": {
            "variable": "code",
            "label": "Code (out-of-range)"
          },
          "y": {
            "variable": "fuel_load",
            "label": "w₀ (kg/m²)"
          }
        }
      ]
    }
  ]
}
```

</details>
