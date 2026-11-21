---
title: "FireOccurrenceLogistic"
slug: "fireoccurrencelogistic"
domains: ["wildland_fire"]
component_types: ["model"]
subdomains: ["fsim"]
domain: "wildland_fire"
subdomain: "fsim"
component_type: "model"
esm_version: "1.0.0"
esm_path: "components/wildland_fire/fsim/fire_occurrence_logistic.esm"
description: "Logistic regression model for large fire occurrence probability"
tags: ["wildland_fire", "fsim", "model", "wildfire", "fire-occurrence", "logistic-regression"]
---

## Description

Logistic regression model for large fire occurrence probability

## Reference

_source_ref: WildlandFire.jl/fsim.jl:53
Logistic regression model for large fire occurrence probability_

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `β₀` |  |  | Logistic regression intercept (dimensionless) |
| `β₁` |  |  | Logistic regression slope coefficient (dimensionless) |
| `ERC` |  |  | Energy Release Component index (dimensionless) |
| `one` |  | `1` | Dimensionless unity (dimensionless) |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `P_fire` |  |  | Probability of at least one large fire (dimensionless) |

## Observed expressions

$$
P_{fire} = \frac{one}{e^{\left(-1\right) \cdot ERC \cdot β₁ + \left(-1\right) \cdot β₀} + one}
$$
_Probability of at least one large fire (dimensionless)_

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "variables": {
    "β₀": {
      "type": "parameter",
      "description": "Logistic regression intercept (dimensionless)"
    },
    "β₁": {
      "type": "parameter",
      "description": "Logistic regression slope coefficient (dimensionless)"
    },
    "P_fire": {
      "type": "unknown",
      "description": "Probability of at least one large fire (dimensionless)"
    },
    "ERC": {
      "type": "parameter",
      "description": "Energy Release Component index (dimensionless)"
    },
    "one": {
      "default": 1,
      "type": "parameter",
      "description": "Dimensionless unity (dimensionless)"
    }
  },
  "reference": {
    "notes": "source_ref: WildlandFire.jl/fsim.jl:53\nLogistic regression model for large fire occurrence probability"
  },
  "equations": [
    {
      "rhs": {
        "args": [
          "one",
          {
            "args": [
              {
                "args": [
                  {
                    "args": [
                      {
                        "args": [
                          -1,
                          "ERC",
                          "β₁"
                        ],
                        "op": "*"
                      },
                      {
                        "args": [
                          -1,
                          "β₀"
                        ],
                        "op": "*"
                      }
                    ],
                    "op": "+"
                  }
                ],
                "op": "exp"
              },
              "one"
            ],
            "op": "+"
          }
        ],
        "op": "/"
      },
      "lhs": "P_fire"
    }
  ],
  "tests": [],
  "analyses": []
}
```

</details>
