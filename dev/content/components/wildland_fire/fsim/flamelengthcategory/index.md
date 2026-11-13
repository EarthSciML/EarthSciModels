---
title: "FlameLengthCategory"
slug: "flamelengthcategory"
domains: ["wildland_fire"]
component_types: ["model"]
subdomains: ["fsim"]
domain: "wildland_fire"
subdomain: "fsim"
component_type: "model"
esm_version: "1.0.0"
esm_path: "components/wildland_fire/fsim/flame_length_category.esm"
description: "Flame length categorization into 6 categories (0.6 m thresholds) based on Byram flame length. Migrated from WildlandFire.jl@126976f2 src/fsim.jl:418."
tags: ["wildland_fire", "fsim", "model", "flame_length", "observed-only"]
---

## Description

Flame length categorization into 6 categories (0.6 m thresholds) based on Byram flame length. Migrated from WildlandFire.jl@126976f2 src/fsim.jl:418.

## Reference

_Flame length categorization into 6 categories (0.6 m thresholds) based on Byram flame length. Migrated from WildlandFire.jl@126976f2 src/fsim.jl:418._

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `F_L` |  |  | Flame length (Byram) |
| `zero` |  | `0` | Dimensionless zero (dimensionless) |
| `FL_5` |  | `3.7` | FL category 5 upper bound |
| `FL_1` |  | `0.6` | FL category 1 upper bound |
| `one` |  | `1` | Dimensionless unity (dimensionless) |
| `FL_2` |  | `1.2` | FL category 2 upper bound |
| `FL_3` |  | `1.8` | FL category 3 upper bound |
| `FL_4` |  | `2.4` | FL category 4 upper bound |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `cat_3` |  |  | In FL category 3: 1.2–1.8 m (dimensionless) |
| `cat_6` |  |  | In FL category 6: > 3.7 m (dimensionless) |
| `cat_5` |  |  | In FL category 5: 2.4–3.7 m (dimensionless) |
| `cat_2` |  |  | In FL category 2: 0.6–1.2 m (dimensionless) |
| `cat_1` |  |  | In FL category 1: ≤ 0.6 m (dimensionless) |
| `cat_4` |  |  | In FL category 4: 1.8–2.4 m (dimensionless) |

## Observed expressions

$$
cat_{3} = \mathrm{ifelse}\left(\mathrm{<=}\left(F_{L}, FL_{3}\right), one, zero\right) \cdot \mathrm{ifelse}\left(\mathrm{<}\left(FL_{2}, F_{L}\right), one, zero\right)
$$
_In FL category 3: 1.2–1.8 m (dimensionless)_

$$
cat_{6} = \mathrm{ifelse}\left(\mathrm{<}\left(FL_{5}, F_{L}\right), one, zero\right)
$$
_In FL category 6: > 3.7 m (dimensionless)_

$$
cat_{5} = \mathrm{ifelse}\left(\mathrm{<}\left(FL_{4}, F_{L}\right), one, zero\right) \cdot \mathrm{ifelse}\left(\mathrm{<=}\left(F_{L}, FL_{5}\right), one, zero\right)
$$
_In FL category 5: 2.4–3.7 m (dimensionless)_

$$
cat_{2} = \mathrm{ifelse}\left(\mathrm{<=}\left(F_{L}, FL_{2}\right), one, zero\right) \cdot \mathrm{ifelse}\left(\mathrm{<}\left(FL_{1}, F_{L}\right), one, zero\right)
$$
_In FL category 2: 0.6–1.2 m (dimensionless)_

$$
cat_{1} = \mathrm{ifelse}\left(\mathrm{<=}\left(F_{L}, FL_{1}\right), one, zero\right)
$$
_In FL category 1: ≤ 0.6 m (dimensionless)_

$$
cat_{4} = \mathrm{ifelse}\left(\mathrm{<}\left(FL_{3}, F_{L}\right), one, zero\right) \cdot \mathrm{ifelse}\left(\mathrm{<=}\left(F_{L}, FL_{4}\right), one, zero\right)
$$
_In FL category 4: 1.8–2.4 m (dimensionless)_

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "variables": {
    "F_L": {
      "type": "parameter",
      "description": "Flame length (Byram)"
    },
    "cat_3": {
      "type": "unknown",
      "description": "In FL category 3: 1.2–1.8 m (dimensionless)"
    },
    "zero": {
      "default": 0,
      "type": "parameter",
      "description": "Dimensionless zero (dimensionless)"
    },
    "cat_6": {
      "type": "unknown",
      "description": "In FL category 6: > 3.7 m (dimensionless)"
    },
    "FL_5": {
      "default": 3.7,
      "type": "parameter",
      "description": "FL category 5 upper bound"
    },
    "FL_1": {
      "default": 0.6,
      "type": "parameter",
      "description": "FL category 1 upper bound"
    },
    "cat_5": {
      "type": "unknown",
      "description": "In FL category 5: 2.4–3.7 m (dimensionless)"
    },
    "cat_2": {
      "type": "unknown",
      "description": "In FL category 2: 0.6–1.2 m (dimensionless)"
    },
    "one": {
      "default": 1,
      "type": "parameter",
      "description": "Dimensionless unity (dimensionless)"
    },
    "FL_2": {
      "default": 1.2,
      "type": "parameter",
      "description": "FL category 2 upper bound"
    },
    "cat_1": {
      "type": "unknown",
      "description": "In FL category 1: ≤ 0.6 m (dimensionless)"
    },
    "cat_4": {
      "type": "unknown",
      "description": "In FL category 4: 1.8–2.4 m (dimensionless)"
    },
    "FL_3": {
      "default": 1.8,
      "type": "parameter",
      "description": "FL category 3 upper bound"
    },
    "FL_4": {
      "default": 2.4,
      "type": "parameter",
      "description": "FL category 4 upper bound"
    }
  },
  "reference": {
    "notes": "Flame length categorization into 6 categories (0.6 m thresholds) based on Byram flame length. Migrated from WildlandFire.jl@126976f2 src/fsim.jl:418."
  },
  "equations": [
    {
      "rhs": {
        "args": [
          {
            "args": [
              "F_L",
              "FL_1"
            ],
            "op": "<="
          },
          "one",
          "zero"
        ],
        "op": "ifelse"
      },
      "lhs": "cat_1"
    },
    {
      "rhs": {
        "args": [
          {
            "args": [
              {
                "args": [
                  "F_L",
                  "FL_2"
                ],
                "op": "<="
              },
              "one",
              "zero"
            ],
            "op": "ifelse"
          },
          {
            "args": [
              {
                "args": [
                  "FL_1",
                  "F_L"
                ],
                "op": "<"
              },
              "one",
              "zero"
            ],
            "op": "ifelse"
          }
        ],
        "op": "*"
      },
      "lhs": "cat_2"
    },
    {
      "rhs": {
        "args": [
          {
            "args": [
              {
                "args": [
                  "F_L",
                  "FL_3"
                ],
                "op": "<="
              },
              "one",
              "zero"
            ],
            "op": "ifelse"
          },
          {
            "args": [
              {
                "args": [
                  "FL_2",
                  "F_L"
                ],
                "op": "<"
              },
              "one",
              "zero"
            ],
            "op": "ifelse"
          }
        ],
        "op": "*"
      },
      "lhs": "cat_3"
    },
    {
      "rhs": {
        "args": [
          {
            "args": [
              {
                "args": [
                  "FL_3",
                  "F_L"
                ],
                "op": "<"
              },
              "one",
              "zero"
            ],
            "op": "ifelse"
          },
          {
            "args": [
              {
                "args": [
                  "F_L",
                  "FL_4"
                ],
                "op": "<="
              },
              "one",
              "zero"
            ],
            "op": "ifelse"
          }
        ],
        "op": "*"
      },
      "lhs": "cat_4"
    },
    {
      "rhs": {
        "args": [
          {
            "args": [
              {
                "args": [
                  "FL_4",
                  "F_L"
                ],
                "op": "<"
              },
              "one",
              "zero"
            ],
            "op": "ifelse"
          },
          {
            "args": [
              {
                "args": [
                  "F_L",
                  "FL_5"
                ],
                "op": "<="
              },
              "one",
              "zero"
            ],
            "op": "ifelse"
          }
        ],
        "op": "*"
      },
      "lhs": "cat_5"
    },
    {
      "rhs": {
        "args": [
          {
            "args": [
              "FL_5",
              "F_L"
            ],
            "op": "<"
          },
          "one",
          "zero"
        ],
        "op": "ifelse"
      },
      "lhs": "cat_6"
    }
  ],
  "tests": [
    {
      "id": "below_0_6",
      "description": "F_L = 0m (below 0.6) → cat_1 = 1, all others 0",
      "parameter_overrides": {
        "F_L": 0.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "cat_1",
          "time": 0.0,
          "expected": 1.0,
          "tolerance": {
            "abs": 1e-15
          }
        },
        {
          "variable": "cat_2",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "abs": 1e-15
          }
        },
        {
          "variable": "cat_3",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "abs": 1e-15
          }
        },
        {
          "variable": "cat_4",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "abs": 1e-15
          }
        },
        {
          "variable": "cat_5",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "abs": 1e-15
          }
        },
        {
          "variable": "cat_6",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "abs": 1e-15
          }
        }
      ]
    },
    {
      "id": "cat_1_upper_edge",
      "description": "F_L = 0.6 (exactly FL_1) → cat_1 = 1 (≤ includes equality)",
      "parameter_overrides": {
        "F_L": 0.6
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "cat_1",
          "time": 0.0,
          "expected": 1.0,
          "tolerance": {
            "abs": 1e-15
          }
        },
        {
          "variable": "cat_2",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "abs": 1e-15
          }
        },
        {
          "variable": "cat_6",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "abs": 1e-15
          }
        }
      ]
    },
    {
      "id": "cat_2_mid",
      "description": "F_L = 0.9 (0.6–1.2) → cat_2 = 1",
      "parameter_overrides": {
        "F_L": 0.9
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "cat_1",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "abs": 1e-15
          }
        },
        {
          "variable": "cat_2",
          "time": 0.0,
          "expected": 1.0,
          "tolerance": {
            "abs": 1e-15
          }
        },
        {
          "variable": "cat_3",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "abs": 1e-15
          }
        }
      ]
    },
    {
      "id": "cat_3_mid",
      "description": "F_L = 1.5 (1.2–1.8) → cat_3 = 1",
      "parameter_overrides": {
        "F_L": 1.5
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "cat_2",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "abs": 1e-15
          }
        },
        {
          "variable": "cat_3",
          "time": 0.0,
          "expected": 1.0,
          "tolerance": {
            "abs": 1e-15
          }
        },
        {
          "variable": "cat_4",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "abs": 1e-15
          }
        }
      ]
    },
    {
      "id": "cat_4_mid",
      "description": "F_L = 2.0 (1.8–2.4) → cat_4 = 1",
      "parameter_overrides": {
        "F_L": 2.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "cat_3",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "abs": 1e-15
          }
        },
        {
          "variable": "cat_4",
          "time": 0.0,
          "expected": 1.0,
          "tolerance": {
            "abs": 1e-15
          }
        },
        {
          "variable": "cat_5",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "abs": 1e-15
          }
        }
      ]
    },
    {
      "id": "cat_5_mid",
      "description": "F_L = 3.0 (2.4–3.7) → cat_5 = 1",
      "parameter_overrides": {
        "F_L": 3.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "cat_4",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "abs": 1e-15
          }
        },
        {
          "variable": "cat_5",
          "time": 0.0,
          "expected": 1.0,
          "tolerance": {
            "abs": 1e-15
          }
        },
        {
          "variable": "cat_6",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "abs": 1e-15
          }
        }
      ]
    },
    {
      "id": "cat_5_upper_edge",
      "description": "F_L = 3.7 (exactly FL_5) → cat_5 = 1 (≤ threshold includes equality)",
      "parameter_overrides": {
        "F_L": 3.7
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "cat_5",
          "time": 0.0,
          "expected": 1.0,
          "tolerance": {
            "abs": 1e-15
          }
        },
        {
          "variable": "cat_6",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "abs": 1e-15
          }
        }
      ]
    },
    {
      "id": "cat_6_above",
      "description": "F_L = 5.0 (> 3.7) → cat_6 = 1",
      "parameter_overrides": {
        "F_L": 5.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "cat_5",
          "time": 0.0,
          "expected": 0.0,
          "tolerance": {
            "abs": 1e-15
          }
        },
        {
          "variable": "cat_6",
          "time": 0.0,
          "expected": 1.0,
          "tolerance": {
            "abs": 1e-15
          }
        }
      ]
    }
  ],
  "analyses": []
}
```

</details>
