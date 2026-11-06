---
title: "BurnProbability"
slug: "burnprobability"
domains: ["wildland_fire"]
component_types: ["model"]
subdomains: ["fsim"]
domain: "wildland_fire"
subdomain: "fsim"
component_type: "model"
esm_version: "1.0.0"
esm_path: "components/wildland_fire/fsim/burn_probability.esm"
description: "Burn probability calculation for wildland fire FSIM"
tags: ["wildland_fire", "fsim", "model", "fire", "probability"]
---

## Description

Burn probability calculation for wildland fire FSIM

## Reference

_source_ref: WildlandFire.jl/src/fsim.jl:231
Burn probability calculation for wildland fire FSIM_

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `N_burned` |  |  | Number of times cell burned in simulation (dimensionless) |
| `A_FPU` |  |  | Total Fire Planning Unit area |
| `N_years` |  |  | Total number of simulated years (dimensionless) |
| `P_FL_given_burn` |  |  | Conditional probability of flame length category given burning (dimensionless) |
| `A_burned` |  |  | Total area burned across all simulated years |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `BP_conditional` |  |  | Conditional burn probability at given flame length (dimensionless) |
| `BP_FPU` |  |  | FPU-level annual burn probability (dimensionless) |
| `BP` |  |  | Cell-level annual burn probability (dimensionless) |

## Observed expressions

$$
BP_{conditional} = BP \cdot P_{FL\,given\,burn}
$$
_Conditional burn probability at given flame length (dimensionless)_

$$
BP_{FPU} = \frac{A_{burned}}{A_{FPU} \cdot N_{years}}
$$
_FPU-level annual burn probability (dimensionless)_

$$
BP = \frac{N_{burned}}{N_{years}}
$$
_Cell-level annual burn probability (dimensionless)_

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "variables": {
    "N_burned": {
      "type": "parameter",
      "description": "Number of times cell burned in simulation (dimensionless)"
    },
    "A_FPU": {
      "type": "parameter",
      "description": "Total Fire Planning Unit area"
    },
    "BP_conditional": {
      "type": "unknown",
      "description": "Conditional burn probability at given flame length (dimensionless)"
    },
    "N_years": {
      "type": "parameter",
      "description": "Total number of simulated years (dimensionless)"
    },
    "P_FL_given_burn": {
      "type": "parameter",
      "description": "Conditional probability of flame length category given burning (dimensionless)"
    },
    "BP_FPU": {
      "type": "unknown",
      "description": "FPU-level annual burn probability (dimensionless)"
    },
    "BP": {
      "type": "unknown",
      "description": "Cell-level annual burn probability (dimensionless)"
    },
    "A_burned": {
      "type": "parameter",
      "description": "Total area burned across all simulated years"
    }
  },
  "reference": {
    "notes": "source_ref: WildlandFire.jl/src/fsim.jl:231\nBurn probability calculation for wildland fire FSIM"
  },
  "equations": [
    {
      "rhs": {
        "args": [
          "N_burned",
          "N_years"
        ],
        "op": "/"
      },
      "lhs": "BP"
    },
    {
      "rhs": {
        "args": [
          "A_burned",
          {
            "args": [
              "A_FPU",
              "N_years"
            ],
            "op": "*"
          }
        ],
        "op": "/"
      },
      "lhs": "BP_FPU"
    },
    {
      "rhs": {
        "args": [
          "BP",
          "P_FL_given_burn"
        ],
        "op": "*"
      },
      "lhs": "BP_conditional"
    }
  ],
  "tests": [],
  "analyses": []
}
```

</details>
