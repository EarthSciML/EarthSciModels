---
title: "SlipCorrection"
slug: "slipcorrection"
domains: ["aerosol"]
component_types: ["model"]
subdomains: ["particle_dyn"]
domain: "aerosol"
subdomain: "particle_dyn"
component_type: "model"
esm_version: "1.0.0"
esm_path: "components/aerosol/particle_dyn/slip.esm"
reference: "Seinfeld, J. H. and Pandis, S. N. (2006) Atmospheric Chemistry and Physics, 2nd Edition, Chapter 9, Eq. 9.34."
description: "Cunningham slip correction factor for noncontinuum aerosol effects. Migrated from Aerosol.jl@c8c640bb src/single_particle_dynamics.jl:64 (`SlipCorrection` @component). Calculates the slip correction factor C_c and Knudsen number Kn for particle-gas interactions."
tags: ["aerosol", "particle_dyn", "model", "particle-dynamics", "slip-correction", "noncontinuum"]
---

## Description

Cunningham slip correction factor for noncontinuum aerosol effects. Migrated from Aerosol.jl@c8c640bb src/single_particle_dynamics.jl:64 (`SlipCorrection` @component). Calculates the slip correction factor C_c and Knudsen number Kn for particle-gas interactions.

## Reference

_source_ref: Aerosol.jl@c8c640bb636b22f2425460e9ed5cba50793bfee1:src/single_particle_dynamics.jl:64
Upstream `SlipCorrection` is an MTK `@component` with three constants (A1, A2, A3), two parameters (D_p, λ), and two variables (C_c, Kn). The equations are:
  • Kn  ~  2 * λ / D_p              (Eq. 9.1 — Knudsen number)
  • C_c ~  1 + Kn * (A1 + A2 * exp(-A3 / Kn))  (Eq. 9.34 — slip correction factor)
Both equations are algebraic (no derivatives), making this an observed-only component.

Observability classification: observed-only — every output is given by a single algebraic equation. Test scenarios use `time_span: [0, 1]` and sample at t=0.

Tolerance rationale (model-level rel=1e-9): observed-only algebraic system (no ODE integration); the Kn equation is a simple division, and the C_c equation involves exp() and multiplication. Floating-point round-off is ~1e-15. 1e-9 leaves comfortable headroom._

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `A1` | `1` | `1.257` | Slip correction constant A1 (dimensionless) |
| `A2` | `1` | `0.4` | Slip correction constant A2 (dimensionless) |
| `A3` | `1` | `1.1` | Slip correction constant A3 (dimensionless) |
| `D_p` | `m` | `1e-06` | Particle diameter |
| `λ` | `m` | `6.51e-08` | Mean free path of air |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `Kn` | `1` |  | Knudsen number (dimensionless) |
| `C_c` | `1` |  | Cunningham slip correction factor (dimensionless) |

## Observed expressions

$$
Kn = 2 \cdot \frac{λ}{D_{p}}
$$
_Knudsen number (dimensionless)_

$$
C_{c} = 1 + Kn \cdot \left(A1 + A2 \cdot e^{\frac{\left(-1\right) \cdot A3}{Kn}}\right)
$$
_Cunningham slip correction factor (dimensionless)_

## Analyses

### size_dependence

Sweep particle diameter from 1 nm to 10 μm to show how Kn and C_c vary across regimes (continuum, transition, free molecular).

**Time span:** 0.0 → 1.0

**Swept over:** `D_p`

![Knudsen number vs particle diameter (log-log scale) — shows inverse relationship Kn ∝ 1/D_p.](/plots/aerosol/particle_dyn/slipcorrection/size_dependence-knudsen_vs_diameter.png)

![Slip correction factor C_c vs particle diameter — shows C_c → 1 for large particles, C_c >> 1 for nanoparticles.](/plots/aerosol/particle_dyn/slipcorrection/size_dependence-slip_correction_vs_diameter.png)

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "reference": {
    "notes": "source_ref: Aerosol.jl@c8c640bb636b22f2425460e9ed5cba50793bfee1:src/single_particle_dynamics.jl:64\nUpstream `SlipCorrection` is an MTK `@component` with three constants (A1, A2, A3), two parameters (D_p, λ), and two variables (C_c, Kn). The equations are:\n  • Kn  ~  2 * λ / D_p              (Eq. 9.1 — Knudsen number)\n  • C_c ~  1 + Kn * (A1 + A2 * exp(-A3 / Kn))  (Eq. 9.34 — slip correction factor)\nBoth equations are algebraic (no derivatives), making this an observed-only component.\n\nObservability classification: observed-only — every output is given by a single algebraic equation. Test scenarios use `time_span: [0, 1]` and sample at t=0.\n\nTolerance rationale (model-level rel=1e-9): observed-only algebraic system (no ODE integration); the Kn equation is a simple division, and the C_c equation involves exp() and multiplication. Floating-point round-off is ~1e-15. 1e-9 leaves comfortable headroom."
  },
  "tolerance": {
    "rel": 1e-09
  },
  "variables": {
    "A1": {
      "type": "parameter",
      "units": "1",
      "default": 1.257,
      "description": "Slip correction constant A1 (dimensionless)"
    },
    "A2": {
      "type": "parameter",
      "units": "1",
      "default": 0.4,
      "description": "Slip correction constant A2 (dimensionless)"
    },
    "A3": {
      "type": "parameter",
      "units": "1",
      "default": 1.1,
      "description": "Slip correction constant A3 (dimensionless)"
    },
    "D_p": {
      "type": "parameter",
      "units": "m",
      "default": 1e-06,
      "description": "Particle diameter"
    },
    "λ": {
      "type": "parameter",
      "units": "m",
      "default": 6.51e-08,
      "description": "Mean free path of air"
    },
    "Kn": {
      "type": "unknown",
      "units": "1",
      "description": "Knudsen number (dimensionless)"
    },
    "C_c": {
      "type": "unknown",
      "units": "1",
      "description": "Cunningham slip correction factor (dimensionless)"
    }
  },
  "equations": [
    {
      "lhs": "Kn",
      "rhs": {
        "op": "*",
        "args": [
          2,
          {
            "op": "/",
            "args": [
              "λ",
              "D_p"
            ]
          }
        ]
      }
    },
    {
      "lhs": "C_c",
      "rhs": {
        "op": "+",
        "args": [
          1,
          {
            "op": "*",
            "args": [
              "Kn",
              {
                "op": "+",
                "args": [
                  "A1",
                  {
                    "op": "*",
                    "args": [
                      "A2",
                      {
                        "op": "exp",
                        "args": [
                          {
                            "op": "/",
                            "args": [
                              {
                                "op": "*",
                                "args": [
                                  -1,
                                  "A3"
                                ]
                              },
                              "Kn"
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
  "tests": [
    {
      "id": "default_conditions",
      "description": "Default conditions: D_p = 1.0e-6 m (1 μm particle), λ = 6.51e-8 m. Kn = 2*6.51e-8/1e-6 = 0.1302, C_c = 1 + 0.1302*(1.257 + 0.4*exp(-1.1/0.1302)) ≈ 1.164.",
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "Kn",
          "time": 0.0,
          "expected": 0.1302,
          "tolerance": {
            "rel": 0.0001
          }
        },
        {
          "variable": "C_c",
          "time": 0.0,
          "expected": 1.164,
          "tolerance": {
            "rel": 0.001
          }
        }
      ]
    },
    {
      "id": "large_particle_continuum",
      "description": "Large particle (D_p = 1.0e-5 m = 10 μm): Kn = 2*6.51e-8/1e-5 = 0.01302 (continuum regime, Kn << 1). exp(-1.1/0.01302) ≈ 2e-37 is negligible, so C_c ≈ 1 + 0.01302*1.257 = 1.01636614.",
      "parameter_overrides": {
        "D_p": 1e-05
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "Kn",
          "time": 0.0,
          "expected": 0.01302,
          "tolerance": {
            "rel": 0.0001
          }
        },
        {
          "variable": "C_c",
          "time": 0.0,
          "expected": 1.01636614,
          "tolerance": {
            "rel": 1e-06
          }
        }
      ]
    },
    {
      "id": "small_particle_free_molecular",
      "description": "Small particle (D_p = 1.0e-8 m = 10 nm): Kn = 2*6.51e-8/1e-8 = 13.02 (free molecular regime, Kn >> 1). C_c should be large (~20+), indicating significant slip.",
      "parameter_overrides": {
        "D_p": 1e-08
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "Kn",
          "time": 0.0,
          "expected": 13.02,
          "tolerance": {
            "rel": 0.0001
          }
        },
        {
          "variable": "C_c",
          "time": 0.0,
          "expected": 22.0,
          "tolerance": {
            "rel": 0.01
          }
        }
      ]
    },
    {
      "id": "nanoparticle",
      "description": "Nanoparticle (D_p = 1.0e-9 m = 1 nm): Kn = 2*6.51e-8/1e-9 = 130.2 (deep free molecular regime). exp(-1.1/130.2) ≈ 0.99158, so C_c = 1 + 130.2*(1.257 + 0.4*0.99158) ≈ 216.30.",
      "parameter_overrides": {
        "D_p": 1e-09
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "Kn",
          "time": 0.0,
          "expected": 130.2,
          "tolerance": {
            "rel": 0.0001
          }
        },
        {
          "variable": "C_c",
          "time": 0.0,
          "expected": 216.3,
          "tolerance": {
            "rel": 0.001
          }
        }
      ]
    },
    {
      "id": "high_pressure_small_mfp",
      "description": "High pressure condition: λ = 1.0e-8 m (smaller mean free path). For D_p = 1.0e-6 m: Kn = 0.02, exp(-1.1/0.02) ≈ 1e-24 is negligible, so C_c ≈ 1 + 0.02*1.257 = 1.02514 (near continuum).",
      "parameter_overrides": {
        "D_p": 1e-06,
        "λ": 1e-08
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "Kn",
          "time": 0.0,
          "expected": 0.02,
          "tolerance": {
            "rel": 0.0001
          }
        },
        {
          "variable": "C_c",
          "time": 0.0,
          "expected": 1.02514,
          "tolerance": {
            "rel": 1e-06
          }
        }
      ]
    },
    {
      "id": "transition_regime",
      "description": "Transition regime: D_p = 2.0e-7 m (200 nm), λ = 6.51e-8 m. Kn = 0.651, exp(-1.1/0.651) ≈ 0.18452, so C_c = 1 + 0.651*(1.257 + 0.4*0.18452) ≈ 1.86637.",
      "parameter_overrides": {
        "D_p": 2e-07
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "Kn",
          "time": 0.0,
          "expected": 0.651,
          "tolerance": {
            "rel": 0.0001
          }
        },
        {
          "variable": "C_c",
          "time": 0.0,
          "expected": 1.86637,
          "tolerance": {
            "rel": 0.0001
          }
        }
      ]
    }
  ],
  "analyses": [
    {
      "id": "size_dependence",
      "description": "Sweep particle diameter from 1 nm to 10 μm to show how Kn and C_c vary across regimes (continuum, transition, free molecular).",
      "initial_state": {},
      "parameters": {
        "λ": 6.51e-08
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "parameter_sweep": {
        "type": "cartesian",
        "dimensions": [
          {
            "parameter": "D_p",
            "range": {
              "start": 1e-09,
              "stop": 1e-05,
              "count": 50,
              "scale": "log"
            }
          }
        ]
      },
      "plots": [
        {
          "id": "knudsen_vs_diameter",
          "type": "line",
          "description": "Knudsen number vs particle diameter (log-log scale) — shows inverse relationship Kn ∝ 1/D_p.",
          "x": {
            "variable": "D_p",
            "label": "D_p (m)"
          },
          "y": {
            "variable": "Kn",
            "label": "Kn (dimensionless)"
          }
        },
        {
          "id": "slip_correction_vs_diameter",
          "type": "line",
          "description": "Slip correction factor C_c vs particle diameter — shows C_c → 1 for large particles, C_c >> 1 for nanoparticles.",
          "x": {
            "variable": "D_p",
            "label": "D_p (m)"
          },
          "y": {
            "variable": "C_c",
            "label": "C_c (dimensionless)"
          }
        }
      ]
    }
  ]
}
```

</details>
