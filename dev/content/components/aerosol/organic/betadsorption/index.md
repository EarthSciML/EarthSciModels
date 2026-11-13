---
title: "BETAdsorption"
slug: "betadsorption"
domains: ["aerosol"]
component_types: ["model"]
subdomains: ["organic"]
domain: "aerosol"
subdomain: "organic"
component_type: "model"
esm_version: "1.0.0"
esm_path: "components/aerosol/organic/bet.esm"
reference: "Seinfeld, J. H. and Pandis, S. N. (2006) Atmospheric Chemistry and Physics, 2nd Edition, Chapter 14, Section 14.5.3, Eq. 14.45 — BET multilayer adsorption isotherm. Migrated from Aerosol.jl src/organic_aerosol.jl `BETAdsorption` (esm-1c7)."
description: "BET (Brunauer-Emmett-Teller) adsorption isotherm for multilayer adsorption. Extends the Langmuir model to include formation of additional molecular layers, assuming each adsorbed molecule can serve as an adsorption site for the next layer. From Seinfeld and Pandis (2006), Chapter 14, Section 14.5.3, Equation 14.45."
tags: ["aerosol", "organic", "model", "bet-adsorption"]
---

## Description

BET (Brunauer-Emmett-Teller) adsorption isotherm for multilayer adsorption. Extends the Langmuir model to include formation of additional molecular layers, assuming each adsorbed molecule can serve as an adsorption site for the next layer. From Seinfeld and Pandis (2006), Chapter 14, Section 14.5.3, Equation 14.45.

## Reference

Seinfeld, J. H. and Pandis, S. N. (2006) Atmospheric Chemistry and Physics, 2nd Edition, Chapter 14, Section 14.5.3, Eq. 14.45 — BET multilayer adsorption isotherm. Migrated from Aerosol.jl src/organic_aerosol.jl `BETAdsorption` (esm-1c7).

_source_ref: Aerosol.jl@main:src/organic_aerosol.jl:279
Upstream `BETAdsorption` is an MTK `@component` with two parameters (V_m, c_BET), and two variables (S, V). The equation is:
  • V ~ V_m * c_BET * S / ((1 - S) * (1 + (c_BET - 1) * S))  (Eq. 14.45 — BET isotherm)
The equation is algebraic (no derivatives), making this an observed-only component.

Observability classification: observed-only — the single output V is given by an algebraic equation. Test scenarios use `time_span: [0, 1]` and sample at t=0.

ESM representation note: in the upstream MTK component S is an `@variable` supplied externally as the input; in this .esm it is represented as a `parameter` (not a state) so the system is well-posed under the schema's equation-count rule (one equation per state) and to match the observed-only pattern used elsewhere in this rig (see components/wildland_fire/midflame_wind.esm where all inputs are parameters and only algebraic outputs are states). Tests vary S via `parameter_overrides`, and the `saturation_sweep` example sweeps S as a parameter dimension.

Tolerance rationale (model-level rel=1e-9): observed-only algebraic system (no ODE integration); the equation involves multiplication, division, and addition. Floating-point round-off is ~1e-15. 1e-9 leaves comfortable headroom._

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `V_m` | `m^3` | `1.0` | Gas volume for monolayer formation |
| `c_BET` | `1` | `10.0` | BET constant for the adsorbing surface (dimensionless) |
| `S` | `1` | `0.5` | Gas-phase saturation ratio p/p_sat (dimensionless). Input parameter — the observed-only model has one algebraic equation for V given S. |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `V` | `m^3` |  | Volume of gas adsorbed |

## Observed expressions

$$
V = \frac{c_{BET} \cdot V_{m} \cdot S}{\left(1 + \left(-1\right) \cdot S\right) \cdot \left(1 + \left(-1 + c_{BET}\right) \cdot S\right)}
$$
_Volume of gas adsorbed_

## Analyses

### saturation_sweep

Sweep saturation ratio from 0.01 to 0.99 to show the characteristic BET isotherm shape (multilayer adsorption as S approaches 1).

**Time span:** 0.0 → 1.0

**Swept over:** `S`

![BET isotherm: V/V_m vs S — shows monolayer completion at intermediate S and multilayer adsorption as S → 1.](/plots/aerosol/organic/betadsorption/saturation_sweep-bet_isotherm.png)

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "reference": {
    "citation": "Seinfeld, J. H. and Pandis, S. N. (2006) Atmospheric Chemistry and Physics, 2nd Edition, Chapter 14, Section 14.5.3, Eq. 14.45 — BET multilayer adsorption isotherm. Migrated from Aerosol.jl src/organic_aerosol.jl `BETAdsorption` (esm-1c7).",
    "notes": "source_ref: Aerosol.jl@main:src/organic_aerosol.jl:279\nUpstream `BETAdsorption` is an MTK `@component` with two parameters (V_m, c_BET), and two variables (S, V). The equation is:\n  • V ~ V_m * c_BET * S / ((1 - S) * (1 + (c_BET - 1) * S))  (Eq. 14.45 — BET isotherm)\nThe equation is algebraic (no derivatives), making this an observed-only component.\n\nObservability classification: observed-only — the single output V is given by an algebraic equation. Test scenarios use `time_span: [0, 1]` and sample at t=0.\n\nESM representation note: in the upstream MTK component S is an `@variable` supplied externally as the input; in this .esm it is represented as a `parameter` (not a state) so the system is well-posed under the schema's equation-count rule (one equation per state) and to match the observed-only pattern used elsewhere in this rig (see components/wildland_fire/midflame_wind.esm where all inputs are parameters and only algebraic outputs are states). Tests vary S via `parameter_overrides`, and the `saturation_sweep` example sweeps S as a parameter dimension.\n\nTolerance rationale (model-level rel=1e-9): observed-only algebraic system (no ODE integration); the equation involves multiplication, division, and addition. Floating-point round-off is ~1e-15. 1e-9 leaves comfortable headroom."
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
    "c_BET": {
      "type": "parameter",
      "units": "1",
      "default": 10.0,
      "description": "BET constant for the adsorbing surface (dimensionless)"
    },
    "S": {
      "type": "parameter",
      "units": "1",
      "default": 0.5,
      "description": "Gas-phase saturation ratio p/p_sat (dimensionless). Input parameter — the observed-only model has one algebraic equation for V given S."
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
        "op": "/",
        "args": [
          {
            "op": "*",
            "args": [
              "c_BET",
              "V_m",
              "S"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "+",
                "args": [
                  1,
                  {
                    "op": "*",
                    "args": [
                      -1,
                      "S"
                    ]
                  }
                ]
              },
              {
                "op": "+",
                "args": [
                  1,
                  {
                    "op": "*",
                    "args": [
                      {
                        "op": "+",
                        "args": [
                          -1,
                          "c_BET"
                        ]
                      },
                      "S"
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
      "description": "Default conditions: V_m = 1.0 m^3, c_BET = 10.0, S = 0.5. V = 1.0*10.0*0.5 / ((1-0.5)*(1+9*0.5)) = 5.0/2.75 = 1.8181818181818181 m^3.",
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
          "expected": 1.8181818181818181,
          "tolerance": {
            "rel": 1e-06
          }
        }
      ]
    },
    {
      "id": "low_saturation",
      "description": "Low saturation regime: S = 0.001, V approaches V_m * c_BET * S = 0.01 m^3 (linear approximation).",
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "parameter_overrides": {
        "S": 0.001
      },
      "assertions": [
        {
          "variable": "V",
          "time": 0.0,
          "expected": 0.009921,
          "tolerance": {
            "rel": 0.0001
          }
        }
      ]
    }
  ],
  "analyses": [
    {
      "id": "saturation_sweep",
      "description": "Sweep saturation ratio from 0.01 to 0.99 to show the characteristic BET isotherm shape (multilayer adsorption as S approaches 1).",
      "initial_state": {},
      "parameters": {
        "V_m": 1.0,
        "c_BET": 10.0
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
          "id": "bet_isotherm",
          "type": "line",
          "description": "BET isotherm: V/V_m vs S — shows monolayer completion at intermediate S and multilayer adsorption as S → 1.",
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
