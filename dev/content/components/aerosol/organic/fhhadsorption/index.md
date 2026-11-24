---
title: "FHHAdsorption"
slug: "fhhadsorption"
domains: ["aerosol"]
component_types: ["model"]
subdomains: ["organic"]
domain: "aerosol"
subdomain: "organic"
component_type: "model"
esm_version: "1.0.0"
esm_path: "components/aerosol/organic/fhh.esm"
reference: "Seinfeld, J. H. and Pandis, S. N. (2006) Atmospheric Chemistry and Physics, 2nd Edition, Chapter 14, Section 14.5.3, Eq. 14.46 — FHH multilayer adsorption isotherm. Migrated from Aerosol.jl src/organic_aerosol.jl `FHHAdsorption` (esm-esy)."
description: "FHH (Frenkel-Halsey-Hill) adsorption isotherm for multilayer adsorption on flat surfaces governed by van der Waals forces. Relates adsorbed volume to the gas-phase saturation ratio via two empirical parameters. From Seinfeld and Pandis (2006), Chapter 14, Section 14.5.3, Equation 14.46."
tags: ["aerosol", "organic", "model", "fhh-adsorption"]
---

## Description

FHH (Frenkel-Halsey-Hill) adsorption isotherm for multilayer adsorption on flat surfaces governed by van der Waals forces. Relates adsorbed volume to the gas-phase saturation ratio via two empirical parameters. From Seinfeld and Pandis (2006), Chapter 14, Section 14.5.3, Equation 14.46.

## Reference

Seinfeld, J. H. and Pandis, S. N. (2006) Atmospheric Chemistry and Physics, 2nd Edition, Chapter 14, Section 14.5.3, Eq. 14.46 — FHH multilayer adsorption isotherm. Migrated from Aerosol.jl src/organic_aerosol.jl `FHHAdsorption` (esm-esy).

_source_ref: Aerosol.jl@main:src/organic_aerosol.jl:314
Upstream `FHHAdsorption` is an MTK `@component` with three parameters (V_m, A_FHH, B_FHH), and two variables (S, V). The equation is:
  • V ~ V_m * (A_FHH / (-log(S)))^B_FHH  (Eq. 14.46 — FHH isotherm)
The equation is algebraic (no derivatives), making this an observed-only component.

Observability classification: observed-only — the single output V is given by an algebraic equation. Test scenarios use `time_span: [0, 1]` and sample at t=0.

ESM representation note: in the upstream MTK component S is an `@variable` supplied externally as the input; in this .esm it is represented as a `parameter` (not a state) so the system is well-posed under the schema's equation-count rule (one equation per state) and to match the observed-only pattern used elsewhere in this rig (see components/aerosol/organic/bet.esm). Tests vary S via `parameter_overrides`, and the `saturation_sweep` example sweeps S as a parameter dimension.

Domain constraint: S must satisfy 0 < S < 1 so that -log(S) > 0 and the adsorbed volume is well-defined and positive.

Tolerance rationale (model-level rel=1e-9): observed-only algebraic system (no ODE integration); the equation involves logarithm and power. Floating-point round-off is ~1e-15. 1e-9 leaves comfortable headroom._

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `V_m` | `m^3` | `1.0` | Gas volume for monolayer formation |
| `A_FHH` | `1` | `2.25` | FHH adsorption coefficient (dimensionless). Controls the saturation-ratio dependence. |
| `B_FHH` | `1` | `0.4` | FHH adsorption exponent (dimensionless). Typically related to the surface-adsorbate interaction strength. |
| `S` | `1` | `0.5` | Gas-phase saturation ratio p/p_sat (dimensionless, 0 < S < 1). Input parameter — the observed-only model has one algebraic equation for V given S. |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `V` | `m^3` |  | Volume of gas adsorbed |

## Observed expressions

$$
V = V_{m} \cdot \frac{A_{FHH}}{\left(-1\right) \cdot \ln\left(S\right)}^{B_{FHH}}
$$
_Volume of gas adsorbed_

## Analyses

### saturation_sweep

Sweep saturation ratio from 0.01 to 0.99 to show the characteristic FHH isotherm shape (rapid multilayer growth as S approaches 1 due to the power-law divergence of -log(S)).

**Time span:** 0.0 → 1.0

**Swept over:** `S`

![FHH isotherm: V vs S — shows near-monolayer coverage at low S and rapid multilayer growth as S → 1.](/plots/aerosol/organic/fhhadsorption/saturation_sweep-fhh_isotherm.png)

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "reference": {
    "citation": "Seinfeld, J. H. and Pandis, S. N. (2006) Atmospheric Chemistry and Physics, 2nd Edition, Chapter 14, Section 14.5.3, Eq. 14.46 — FHH multilayer adsorption isotherm. Migrated from Aerosol.jl src/organic_aerosol.jl `FHHAdsorption` (esm-esy).",
    "notes": "source_ref: Aerosol.jl@main:src/organic_aerosol.jl:314\nUpstream `FHHAdsorption` is an MTK `@component` with three parameters (V_m, A_FHH, B_FHH), and two variables (S, V). The equation is:\n  • V ~ V_m * (A_FHH / (-log(S)))^B_FHH  (Eq. 14.46 — FHH isotherm)\nThe equation is algebraic (no derivatives), making this an observed-only component.\n\nObservability classification: observed-only — the single output V is given by an algebraic equation. Test scenarios use `time_span: [0, 1]` and sample at t=0.\n\nESM representation note: in the upstream MTK component S is an `@variable` supplied externally as the input; in this .esm it is represented as a `parameter` (not a state) so the system is well-posed under the schema's equation-count rule (one equation per state) and to match the observed-only pattern used elsewhere in this rig (see components/aerosol/organic/bet.esm). Tests vary S via `parameter_overrides`, and the `saturation_sweep` example sweeps S as a parameter dimension.\n\nDomain constraint: S must satisfy 0 < S < 1 so that -log(S) > 0 and the adsorbed volume is well-defined and positive.\n\nTolerance rationale (model-level rel=1e-9): observed-only algebraic system (no ODE integration); the equation involves logarithm and power. Floating-point round-off is ~1e-15. 1e-9 leaves comfortable headroom."
  },
  "tolerance": {
    "rel": 1e-09
  },
  "variables": {
    "V_m": {
      "type": "parameter",
      "units": "m^3",
      "default": 1.0,
      "description": "Gas volume for monolayer formation"
    },
    "A_FHH": {
      "type": "parameter",
      "units": "1",
      "default": 2.25,
      "description": "FHH adsorption coefficient (dimensionless). Controls the saturation-ratio dependence."
    },
    "B_FHH": {
      "type": "parameter",
      "units": "1",
      "default": 0.4,
      "description": "FHH adsorption exponent (dimensionless). Typically related to the surface-adsorbate interaction strength."
    },
    "S": {
      "type": "parameter",
      "units": "1",
      "default": 0.5,
      "description": "Gas-phase saturation ratio p/p_sat (dimensionless, 0 < S < 1). Input parameter — the observed-only model has one algebraic equation for V given S."
    },
    "V": {
      "type": "unknown",
      "units": "m^3",
      "description": "Volume of gas adsorbed"
    }
  },
  "equations": [
    {
      "lhs": "V",
      "rhs": {
        "op": "*",
        "args": [
          "V_m",
          {
            "op": "^",
            "args": [
              {
                "op": "/",
                "args": [
                  "A_FHH",
                  {
                    "op": "*",
                    "args": [
                      -1,
                      {
                        "op": "log",
                        "args": [
                          "S"
                        ]
                      }
                    ]
                  }
                ]
              },
              "B_FHH"
            ]
          }
        ]
      }
    }
  ],
  "tests": [
    {
      "id": "default_conditions",
      "description": "Default conditions: V_m = 1.0 m^3, A_FHH = 2.25, B_FHH = 0.4, S = 0.5. V = 1.0 * (2.25 / (-log(0.5)))^0.4 = (2.25/0.6931...)^0.4 = 3.2461^0.4 = 1.6016 m^3.",
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "parameter_overrides": {
        "S": 0.5
      },
      "assertions": [
        {
          "variable": "V",
          "time": 0.0,
          "expected": 1.6015585593609674,
          "tolerance": {
            "rel": 1e-06
          }
        }
      ]
    },
    {
      "id": "low_saturation",
      "description": "Low saturation: S = 0.1. V = (2.25 / (-log(0.1)))^0.4 = (2.25/2.3026)^0.4 = 0.9772^0.4 = 0.9908 m^3. Near-monolayer regime.",
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "parameter_overrides": {
        "S": 0.1
      },
      "assertions": [
        {
          "variable": "V",
          "time": 0.0,
          "expected": 0.9908016742099569,
          "tolerance": {
            "rel": 1e-06
          }
        }
      ]
    },
    {
      "id": "high_saturation",
      "description": "High saturation: S = 0.9. V = (2.25 / (-log(0.9)))^0.4 = (2.25/0.1054)^0.4 = 21.36^0.4 = 3.403 m^3. Thick multilayer regime near saturation.",
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "parameter_overrides": {
        "S": 0.9
      },
      "assertions": [
        {
          "variable": "V",
          "time": 0.0,
          "expected": 3.402529131880669,
          "tolerance": {
            "rel": 1e-06
          }
        }
      ]
    }
  ],
  "analyses": [
    {
      "id": "saturation_sweep",
      "description": "Sweep saturation ratio from 0.01 to 0.99 to show the characteristic FHH isotherm shape (rapid multilayer growth as S approaches 1 due to the power-law divergence of -log(S)).",
      "initial_state": {},
      "parameters": {
        "V_m": 1.0,
        "A_FHH": 2.25,
        "B_FHH": 0.4
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "parameter_sweep": {
        "type": "cartesian",
        "dimensions": [
          {
            "parameter": "S",
            "range": {
              "start": 0.01,
              "stop": 0.99,
              "count": 50
            }
          }
        ]
      },
      "plots": [
        {
          "id": "fhh_isotherm",
          "type": "line",
          "description": "FHH isotherm: V vs S — shows near-monolayer coverage at low S and rapid multilayer growth as S → 1.",
          "x": {
            "variable": "S",
            "label": "S (p/p_sat)"
          },
          "y": {
            "variable": "V",
            "label": "V (m^3)"
          }
        }
      ]
    }
  ]
}
```

</details>
