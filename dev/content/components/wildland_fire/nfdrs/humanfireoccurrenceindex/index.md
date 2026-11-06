---
title: "HumanFireOccurrenceIndex"
slug: "humanfireoccurrenceindex"
domains: ["wildland_fire"]
component_types: ["model"]
subdomains: ["nfdrs"]
domain: "wildland_fire"
subdomain: "nfdrs"
component_type: "model"
esm_version: "1.0.0"
esm_path: "components/wildland_fire/nfdrs/human_fire_occurrence.esm"
description: "Human-caused fire occurrence index (MCOI) from Cohen & Deeming (1985)"
tags: ["wildland_fire", "nfdrs", "model", "wildland-fire", "ignition"]
---

## Description

Human-caused fire occurrence index (MCOI) from Cohen & Deeming (1985)

## Reference

_Human-caused fire occurrence index (MCOI) from Cohen & Deeming (1985)_

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `MRISK` |  |  | Human-caused risk 0-100 (dimensionless) |
| `IC` |  |  | Ignition component 0-100 (dimensionless) |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `MCOI` |  |  | Human-caused fire occurrence index 0-100 (dimensionless) |

## Observed expressions

$$
MCOI = 0.01 \cdot MRISK \cdot IC
$$
_Human-caused fire occurrence index 0-100 (dimensionless)_

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "variables": {
    "MRISK": {
      "type": "parameter",
      "description": "Human-caused risk 0-100 (dimensionless)"
    },
    "IC": {
      "type": "parameter",
      "description": "Ignition component 0-100 (dimensionless)"
    },
    "MCOI": {
      "type": "unknown",
      "description": "Human-caused fire occurrence index 0-100 (dimensionless)"
    }
  },
  "reference": {
    "notes": "Human-caused fire occurrence index (MCOI) from Cohen & Deeming (1985)"
  },
  "equations": [
    {
      "rhs": {
        "args": [
          0.01,
          "MRISK",
          "IC"
        ],
        "op": "*"
      },
      "lhs": "MCOI"
    }
  ],
  "tests": [],
  "analyses": []
}
```

</details>
