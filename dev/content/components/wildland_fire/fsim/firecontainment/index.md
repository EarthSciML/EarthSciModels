---
title: "FireContainment"
slug: "firecontainment"
domains: ["wildland_fire"]
component_types: ["model"]
subdomains: ["fsim"]
domain: "wildland_fire"
subdomain: "fsim"
component_type: "model"
esm_version: "1.0.0"
esm_path: "components/wildland_fire/fsim/fire_containment.esm"
description: "Statistical fire containment probability model"
tags: ["wildland_fire", "fsim", "model", "wildfire", "containment", "FSIM"]
---

## Description

Statistical fire containment probability model

## Reference

_Statistical fire containment probability model.

This model estimates the probability of fire containment based on fire growth rate characteristics and fire duration. It represents the influence of modern fire management policy on large fire patterns.

The containment probability increases with:
1. Lower fire growth rates (low spread intervals)
2. Longer fire duration (more previous intervals)
3. Non-timber fuel types (easier to suppress)

The model uses a logistic-type function:
  P_contain = 1 / (1 + exp(-(α₀ + α₁ × NPI + α₂ × is_high_spread + α₃ × is_timber)))

References:
- Finney, M.A., McHugh, C.W., Grenfell, I.C., Riley, K.L., Short, K.C. (2011). A simulation of probabilistic wildfire risk components for the continental United States. Stochastic Environmental Research and Risk Assessment, 25:973–1000. DOI: 10.1007/s00477-011-0462-z (Section 2.4, Fig. 6)
- Finney, M.A., Grenfell, I.C., McHugh, C.W. (2009). Modeling large fire containment using generalized linear mixed model analysis. For Sci 55(3):249–255.

source_ref: WildlandFire.jl@126976f2508ceacca6c486b21ae6da5b168c6f46:src/fsim.jl:139_

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `α₀` |  |  | Containment model intercept (dimensionless) |
| `α₁` |  |  | Containment model NPI coefficient (dimensionless) |
| `α₂` |  |  | Containment model high-spread coefficient (dimensionless) |
| `α₃` |  |  | Containment model timber fuel coefficient (dimensionless) |
| `NPI` |  |  | Number of previous spread intervals (dimensionless) |
| `is_high_spread` |  |  | High spread interval indicator, 0 or 1 (dimensionless) |
| `is_timber` |  |  | Timber fuel type indicator, 0 or 1 (dimensionless) |
| `one` |  | `1.0` | Dimensionless unity (dimensionless) |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `P_contain` |  |  | Probability of fire containment (dimensionless) |

## Observed expressions

$$
P_{contain} = \frac{one}{one + e^{\left(-1\right) \cdot \left(α₀ \cdot one + α₁ \cdot NPI + α₂ \cdot is_{high\,spread} + α₃ \cdot is_{timber}\right)}}
$$
_Probability of fire containment (dimensionless)_

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "variables": {
    "α₀": {
      "type": "parameter",
      "description": "Containment model intercept (dimensionless)"
    },
    "α₁": {
      "type": "parameter",
      "description": "Containment model NPI coefficient (dimensionless)"
    },
    "α₂": {
      "type": "parameter",
      "description": "Containment model high-spread coefficient (dimensionless)"
    },
    "α₃": {
      "type": "parameter",
      "description": "Containment model timber fuel coefficient (dimensionless)"
    },
    "NPI": {
      "type": "parameter",
      "description": "Number of previous spread intervals (dimensionless)"
    },
    "is_high_spread": {
      "type": "parameter",
      "description": "High spread interval indicator, 0 or 1 (dimensionless)"
    },
    "is_timber": {
      "type": "parameter",
      "description": "Timber fuel type indicator, 0 or 1 (dimensionless)"
    },
    "one": {
      "default": 1.0,
      "type": "parameter",
      "description": "Dimensionless unity (dimensionless)"
    },
    "P_contain": {
      "type": "unknown",
      "description": "Probability of fire containment (dimensionless)"
    }
  },
  "reference": {
    "notes": "Statistical fire containment probability model.\n\nThis model estimates the probability of fire containment based on fire growth rate characteristics and fire duration. It represents the influence of modern fire management policy on large fire patterns.\n\nThe containment probability increases with:\n1. Lower fire growth rates (low spread intervals)\n2. Longer fire duration (more previous intervals)\n3. Non-timber fuel types (easier to suppress)\n\nThe model uses a logistic-type function:\n  P_contain = 1 / (1 + exp(-(α₀ + α₁ × NPI + α₂ × is_high_spread + α₃ × is_timber)))\n\nReferences:\n- Finney, M.A., McHugh, C.W., Grenfell, I.C., Riley, K.L., Short, K.C. (2011). A simulation of probabilistic wildfire risk components for the continental United States. Stochastic Environmental Research and Risk Assessment, 25:973–1000. DOI: 10.1007/s00477-011-0462-z (Section 2.4, Fig. 6)\n- Finney, M.A., Grenfell, I.C., McHugh, C.W. (2009). Modeling large fire containment using generalized linear mixed model analysis. For Sci 55(3):249–255.\n\nsource_ref: WildlandFire.jl@126976f2508ceacca6c486b21ae6da5b168c6f46:src/fsim.jl:139"
  },
  "tolerance": {
    "rel": 1e-14
  },
  "equations": [
    {
      "lhs": "P_contain",
      "rhs": {
        "op": "/",
        "args": [
          "one",
          {
            "op": "+",
            "args": [
              "one",
              {
                "op": "exp",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      -1,
                      {
                        "op": "+",
                        "args": [
                          {
                            "op": "*",
                            "args": [
                              "α₀",
                              "one"
                            ]
                          },
                          {
                            "op": "*",
                            "args": [
                              "α₁",
                              "NPI"
                            ]
                          },
                          {
                            "op": "*",
                            "args": [
                              "α₂",
                              "is_high_spread"
                            ]
                          },
                          {
                            "op": "*",
                            "args": [
                              "α₃",
                              "is_timber"
                            ]
                          }
                        ]
                      }
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    }
  ],
  "tests": [],
  "analyses": []
}
```

</details>
