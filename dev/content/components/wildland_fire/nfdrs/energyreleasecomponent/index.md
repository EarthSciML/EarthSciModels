---
title: "EnergyReleaseComponent"
slug: "energyreleasecomponent"
domains: ["wildland_fire"]
component_types: ["model"]
subdomains: ["nfdrs"]
domain: "wildland_fire"
subdomain: "nfdrs"
component_type: "model"
esm_version: "1.0.0"
esm_path: "components/wildland_fire/nfdrs/energy_release_component.esm"
reference: "Burgan, R.E. (1988). 1988 Revised National Fire-Danger Rating System. Research Paper INT-390. Ogden, UT: USDA Forest Service, Intermountain Research Station. 23 p."
description: "NFDRS Energy Release Component (ERC) - potential energy release per unit area in a burning fuel bed (BTU/ft^2)"
tags: ["wildland_fire", "nfdrs", "model", "wildland-fire", "energy-release"]
---

## Description

NFDRS Energy Release Component (ERC) - potential energy release per unit area in a burning fuel bed (BTU/ft^2)

## Reference

Burgan, R.E. (1988). 1988 Revised National Fire-Danger Rating System. Research Paper INT-390. Ogden, UT: USDA Forest Service, Intermountain Research Station. 23 p.

_source_ref: WildlandFire.jl@126976f2508ceacca6c486b21ae6da5b168c6f46:src/nfdrs.jl:1017
Upstream EnergyReleaseComponent is an MTK @component that calculates the potential energy release per unit area in a burning fuel bed. The ERC is computed from effective fuel moisture using the Burgan (1988) formulation.

ERC = 548.8 - 1225.4*M_eff + 1048.4*M_eff^2 - 324.8*M_eff^3

where M_eff is the effective fuel moisture (decimal), computed as a weighted combination of 1-hour, 10-hour, 100-hour, and 1000-hour dead fuel moistures plus live fuel moisture.

TODO_GAP: None - all operators (exp, power, polynomial) are supported._

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `M1` | `1` | `0.06` | 1-hour dead fuel moisture (decimal, 0-1). Typical range 0.03-0.30. |
| `M10` | `1` | `0.08` | 10-hour dead fuel moisture (decimal, 0-1). Typical range 0.04-0.35. |
| `M100` | `1` | `0.12` | 100-hour dead fuel moisture (decimal, 0-1). Typical range 0.06-0.40. |
| `M1000` | `1` | `0.15` | 1000-hour dead fuel moisture (decimal, 0-1). Typical range 0.08-0.45. |
| `M_LIVE` | `1` | `0.5` | Live fuel moisture (decimal, 0-1). Typical range 0.30-1.50 for herbaceous, 0.60-2.00 for woody. |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `M_EFF` | `1` |  | Effective fuel moisture (decimal). Weighted combination of dead and live fuel moistures. |
| `ERC` | `BTU/ft^2` |  | Energy Release Component (BTU/ft^2). Potential energy release per unit area in a burning fuel bed. Typical range 0-100+ BTU/ft^2. |

## Observed expressions

$$
M_{EFF} = 0.15 \cdot M1 + 0.2 \cdot M10 + 0.25 \cdot M100 + 0.2 \cdot M1000 + 0.2 \cdot M_{LIVE}
$$
_Effective fuel moisture (decimal). Weighted combination of dead and live fuel moistures._

$$
ERC = 548.8 + \left(-1225.4\right) \cdot M_{EFF} + 1048.4 \cdot M_{EFF}^{2} + \left(-324.8\right) \cdot M_{EFF}^{3}
$$
_Energy Release Component (BTU/ft^2). Potential energy release per unit area in a burning fuel bed. Typical range 0-100+ BTU/ft^2._

## Analyses

### default_energy_release_component

Default EnergyReleaseComponent run with typical summer fuel moisture conditions.

**Time span:** 0.0 → 1.0

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "reference": {
    "citation": "Burgan, R.E. (1988). 1988 Revised National Fire-Danger Rating System. Research Paper INT-390. Ogden, UT: USDA Forest Service, Intermountain Research Station. 23 p.",
    "notes": "source_ref: WildlandFire.jl@126976f2508ceacca6c486b21ae6da5b168c6f46:src/nfdrs.jl:1017\nUpstream EnergyReleaseComponent is an MTK @component that calculates the potential energy release per unit area in a burning fuel bed. The ERC is computed from effective fuel moisture using the Burgan (1988) formulation.\n\nERC = 548.8 - 1225.4*M_eff + 1048.4*M_eff^2 - 324.8*M_eff^3\n\nwhere M_eff is the effective fuel moisture (decimal), computed as a weighted combination of 1-hour, 10-hour, 100-hour, and 1000-hour dead fuel moistures plus live fuel moisture.\n\nTODO_GAP: None - all operators (exp, power, polynomial) are supported."
  },
  "tolerance": {
    "rel": 1e-09,
    "abs": 1e-12
  },
  "variables": {
    "M1": {
      "type": "parameter",
      "units": "1",
      "default": 0.06,
      "description": "1-hour dead fuel moisture (decimal, 0-1). Typical range 0.03-0.30."
    },
    "M10": {
      "type": "parameter",
      "units": "1",
      "default": 0.08,
      "description": "10-hour dead fuel moisture (decimal, 0-1). Typical range 0.04-0.35."
    },
    "M100": {
      "type": "parameter",
      "units": "1",
      "default": 0.12,
      "description": "100-hour dead fuel moisture (decimal, 0-1). Typical range 0.06-0.40."
    },
    "M1000": {
      "type": "parameter",
      "units": "1",
      "default": 0.15,
      "description": "1000-hour dead fuel moisture (decimal, 0-1). Typical range 0.08-0.45."
    },
    "M_LIVE": {
      "type": "parameter",
      "units": "1",
      "default": 0.5,
      "description": "Live fuel moisture (decimal, 0-1). Typical range 0.30-1.50 for herbaceous, 0.60-2.00 for woody."
    },
    "M_EFF": {
      "type": "unknown",
      "units": "1",
      "description": "Effective fuel moisture (decimal). Weighted combination of dead and live fuel moistures."
    },
    "ERC": {
      "type": "unknown",
      "units": "BTU/ft^2",
      "description": "Energy Release Component (BTU/ft^2). Potential energy release per unit area in a burning fuel bed. Typical range 0-100+ BTU/ft^2."
    }
  },
  "equations": [
    {
      "lhs": "M_EFF",
      "rhs": {
        "op": "+",
        "args": [
          {
            "op": "*",
            "args": [
              0.15,
              "M1"
            ]
          },
          {
            "op": "*",
            "args": [
              0.2,
              "M10"
            ]
          },
          {
            "op": "*",
            "args": [
              0.25,
              "M100"
            ]
          },
          {
            "op": "*",
            "args": [
              0.2,
              "M1000"
            ]
          },
          {
            "op": "*",
            "args": [
              0.2,
              "M_LIVE"
            ]
          }
        ]
      }
    },
    {
      "lhs": "ERC",
      "rhs": {
        "op": "+",
        "args": [
          548.8,
          {
            "op": "*",
            "args": [
              -1225.4,
              "M_EFF"
            ]
          },
          {
            "op": "*",
            "args": [
              1048.4,
              {
                "op": "^",
                "args": [
                  "M_EFF",
                  2
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              -324.8,
              {
                "op": "^",
                "args": [
                  "M_EFF",
                  3
                ]
              }
            ]
          }
        ]
      }
    }
  ],
  "tests": [
    {
      "id": "dry_conditions",
      "description": "Very dry conditions with low fuel moistures should produce low ERC",
      "parameter_overrides": {
        "M1": 0.04,
        "M10": 0.05,
        "M100": 0.08,
        "M1000": 0.1,
        "M_LIVE": 0.35
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "ERC",
          "time": 0.0,
          "expected": 410.39427627519996
        }
      ]
    },
    {
      "id": "moist_conditions",
      "description": "Moist conditions with high fuel moistures should produce moderate-high ERC",
      "parameter_overrides": {
        "M1": 0.15,
        "M10": 0.2,
        "M100": 0.25,
        "M1000": 0.3,
        "M_LIVE": 0.8
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "ERC",
          "time": 0.0,
          "expected": 237.4853445999999
        }
      ]
    },
    {
      "id": "typical_summer",
      "description": "Typical summer conditions with moderate fuel moistures",
      "parameter_overrides": {
        "M1": 0.06,
        "M10": 0.08,
        "M100": 0.12,
        "M1000": 0.15,
        "M_LIVE": 0.5
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "ERC",
          "time": 0.0,
          "expected": 355.9259781999999
        }
      ]
    },
    {
      "id": "erc_range_validation",
      "description": "Verify ERC stays within physically reasonable bounds across conditions",
      "parameter_overrides": {
        "M1": 0.1,
        "M10": 0.12,
        "M100": 0.18,
        "M1000": 0.22,
        "M_LIVE": 0.65
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "ERC",
          "time": 0.0,
          "expected": 296.85454090239983
        }
      ]
    },
    {
      "id": "moisture_sensitivity",
      "description": "ERC should decrease as fuel moisture increases",
      "parameter_overrides": {
        "M1": 0.08,
        "M10": 0.1,
        "M100": 0.15,
        "M1000": 0.18,
        "M_LIVE": 0.55
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "ERC",
          "time": 0.0,
          "expected": 330.1637006653999
        }
      ]
    }
  ],
  "analyses": [
    {
      "id": "default_energy_release_component",
      "description": "Default EnergyReleaseComponent run with typical summer fuel moisture conditions.",
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "parameters": {
        "M1": 0.06,
        "M10": 0.08,
        "M100": 0.12,
        "M1000": 0.15,
        "M_LIVE": 0.5
      }
    }
  ]
}
```

</details>
