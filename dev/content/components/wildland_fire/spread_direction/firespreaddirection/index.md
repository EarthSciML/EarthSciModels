---
title: "FireSpreadDirection"
slug: "firespreaddirection"
domains: ["wildland_fire"]
component_types: ["model"]
subdomains: ["spread_direction"]
domain: "wildland_fire"
subdomain: "spread_direction"
component_type: "model"
esm_version: "1.0.0"
esm_path: "components/wildland_fire/spread_direction/fire_spread_direction.esm"
description: "Calculate fire behavior in direction of maximum spread"
tags: ["wildland_fire", "spread_direction", "model", "fire_spread"]
---

## Description

Calculate fire behavior in direction of maximum spread

## Reference

_source_ref: WildlandFire.jl/fire_spread_direction.jl
Calculate fire behavior in direction of maximum spread_

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `B_coeff` |  |  | Wind coefficient B (dimensionless) |
| `ω` |  |  | Wind direction relative to upslope |
| `C_coeff` |  |  | Wind coefficient C (dimensionless) |
| `one` |  | `1` | Dimensionless one for unit balancing |
| `U_ref` |  | `0.00508` | Reference wind speed (1 ft/min in m/s) |
| `φs` |  |  | Slope factor (dimensionless) |
| `R0` |  |  | No-wind no-slope rate of spread |
| `E_coeff` |  |  | Wind coefficient E (dimensionless) |
| `c_Z` |  | `0.559235` | Length-to-width ratio coefficient (SI) |
| `β_ratio` |  |  | Relative packing ratio β/β_op (dimensionless) |
| `φw` |  |  | Wind factor (dimensionless) |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `Z` |  |  | Fire length-to-width ratio (dimensionless) |
| `φ_combined` |  |  | Combined wind+slope factor magnitude (dimensionless) |
| `α` |  |  | Direction of maximum spread relative to upslope |
| `U_E` |  |  | Effective wind speed in direction of maximum spread |
| `φ_E` |  |  | Effective wind factor in direction of maximum spread (dimensionless) |
| `R_H` |  |  | Rate of spread in direction of maximum spread (head fire) |

## Observed expressions

$$
Z = one + U_{E} \cdot c_{Z}
$$
_Fire length-to-width ratio (dimensionless)_

$$
φ_{combined} = \sqrt{\left(\cos\left(ω\right) \cdot φw + φs\right)^{2} + \sin\left(ω\right)^{2} \cdot φw^{2}}
$$
_Combined wind+slope factor magnitude (dimensionless)_

$$
α = \mathrm{atan2}\left(\sin\left(ω\right) \cdot φw, \cos\left(ω\right) \cdot φw + φs\right)
$$
_Direction of maximum spread relative to upslope_

$$
U_{E} = U_{ref} \cdot \frac{β_{ratio}^{E_{coeff}} \cdot φ_{E}}{C_{coeff}}^{\frac{one}{B_{coeff}}}
$$
_Effective wind speed in direction of maximum spread_

$$
φ_{E} = φ_{combined}
$$
_Effective wind factor in direction of maximum spread (dimensionless)_

$$
R_{H} = R0 \cdot \left(one + φ_{combined}\right)
$$
_Rate of spread in direction of maximum spread (head fire)_

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "variables": {
    "Z": {
      "type": "unknown",
      "description": "Fire length-to-width ratio (dimensionless)"
    },
    "B_coeff": {
      "type": "parameter",
      "description": "Wind coefficient B (dimensionless)"
    },
    "ω": {
      "type": "parameter",
      "description": "Wind direction relative to upslope"
    },
    "C_coeff": {
      "type": "parameter",
      "description": "Wind coefficient C (dimensionless)"
    },
    "φ_combined": {
      "type": "unknown",
      "description": "Combined wind+slope factor magnitude (dimensionless)"
    },
    "one": {
      "default": 1,
      "type": "parameter",
      "description": "Dimensionless one for unit balancing"
    },
    "U_ref": {
      "default": 0.00508,
      "type": "parameter",
      "description": "Reference wind speed (1 ft/min in m/s)"
    },
    "α": {
      "type": "unknown",
      "description": "Direction of maximum spread relative to upslope"
    },
    "φs": {
      "type": "parameter",
      "description": "Slope factor (dimensionless)"
    },
    "R0": {
      "type": "parameter",
      "description": "No-wind no-slope rate of spread"
    },
    "E_coeff": {
      "type": "parameter",
      "description": "Wind coefficient E (dimensionless)"
    },
    "U_E": {
      "type": "unknown",
      "description": "Effective wind speed in direction of maximum spread"
    },
    "c_Z": {
      "default": 0.559235,
      "type": "parameter",
      "description": "Length-to-width ratio coefficient (SI)"
    },
    "φ_E": {
      "type": "unknown",
      "description": "Effective wind factor in direction of maximum spread (dimensionless)"
    },
    "R_H": {
      "type": "unknown",
      "description": "Rate of spread in direction of maximum spread (head fire)"
    },
    "β_ratio": {
      "type": "parameter",
      "description": "Relative packing ratio β/β_op (dimensionless)"
    },
    "φw": {
      "type": "parameter",
      "description": "Wind factor (dimensionless)"
    }
  },
  "reference": {
    "notes": "source_ref: WildlandFire.jl/fire_spread_direction.jl\nCalculate fire behavior in direction of maximum spread"
  },
  "equations": [
    {
      "rhs": {
        "args": [
          {
            "args": [
              {
                "args": [
                  {
                    "args": [
                      {
                        "args": [
                          {
                            "args": [
                              "ω"
                            ],
                            "op": "cos"
                          },
                          "φw"
                        ],
                        "op": "*"
                      },
                      "φs"
                    ],
                    "op": "+"
                  },
                  2
                ],
                "op": "^"
              },
              {
                "args": [
                  {
                    "args": [
                      {
                        "args": [
                          "ω"
                        ],
                        "op": "sin"
                      },
                      2
                    ],
                    "op": "^"
                  },
                  {
                    "args": [
                      "φw",
                      2
                    ],
                    "op": "^"
                  }
                ],
                "op": "*"
              }
            ],
            "op": "+"
          }
        ],
        "op": "sqrt"
      },
      "lhs": "φ_combined"
    },
    {
      "rhs": {
        "args": [
          "R0",
          {
            "args": [
              "one",
              "φ_combined"
            ],
            "op": "+"
          }
        ],
        "op": "*"
      },
      "lhs": "R_H"
    },
    {
      "rhs": {
        "args": [
          {
            "args": [
              {
                "args": [
                  "ω"
                ],
                "op": "sin"
              },
              "φw"
            ],
            "op": "*"
          },
          {
            "args": [
              {
                "args": [
                  {
                    "args": [
                      "ω"
                    ],
                    "op": "cos"
                  },
                  "φw"
                ],
                "op": "*"
              },
              "φs"
            ],
            "op": "+"
          }
        ],
        "op": "atan2"
      },
      "lhs": "α"
    },
    {
      "rhs": "φ_combined",
      "lhs": "φ_E"
    },
    {
      "rhs": {
        "args": [
          "U_ref",
          {
            "args": [
              {
                "args": [
                  {
                    "args": [
                      {
                        "args": [
                          "β_ratio",
                          "E_coeff"
                        ],
                        "op": "^"
                      },
                      "φ_E"
                    ],
                    "op": "*"
                  },
                  "C_coeff"
                ],
                "op": "/"
              },
              {
                "args": [
                  "one",
                  "B_coeff"
                ],
                "op": "/"
              }
            ],
            "op": "^"
          }
        ],
        "op": "*"
      },
      "lhs": "U_E"
    },
    {
      "rhs": {
        "args": [
          "one",
          {
            "args": [
              "U_E",
              "c_Z"
            ],
            "op": "*"
          }
        ],
        "op": "+"
      },
      "lhs": "Z"
    }
  ],
  "tests": [],
  "analyses": []
}
```

</details>
