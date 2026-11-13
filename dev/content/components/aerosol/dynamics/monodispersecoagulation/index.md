---
title: "MonodisperseCoagulation"
slug: "monodispersecoagulation"
domains: ["aerosol"]
component_types: ["model"]
subdomains: ["dynamics"]
domain: "aerosol"
subdomain: "dynamics"
component_type: "model"
esm_version: "1.0.0"
esm_path: "components/aerosol/dynamics/monodisperse_coag.esm"
reference: "Seinfeld, J. H. and Pandis, S. N.: Atmospheric Chemistry and Physics: From Air Pollution to Climate Change, 2nd edition, John Wiley & Sons, 2006. Chapter 13, Eqs. 13.65-13.67."
description: "Total aerosol number concentration evolution for a monodisperse aerosol undergoing Brownian coagulation with constant coagulation coefficient (Seinfeld & Pandis 2006, Ch. 13, Eqs. 13.65-13.67). ODE: dN/dt = -K·N²/2; algebraic characteristic coagulation time τ_c = 2/(K·N₀). Source: Aerosol.jl@c8c640bb:src/dynamics.jl:178."
tags: ["aerosol", "dynamics", "model", "coagulation", "seinfeld-pandis"]
---

## Description

Total aerosol number concentration evolution for a monodisperse aerosol undergoing Brownian coagulation with constant coagulation coefficient (Seinfeld & Pandis 2006, Ch. 13, Eqs. 13.65-13.67). ODE: dN/dt = -K·N²/2; algebraic characteristic coagulation time τ_c = 2/(K·N₀). Source: Aerosol.jl@c8c640bb:src/dynamics.jl:178.

## Reference

Seinfeld, J. H. and Pandis, S. N.: Atmospheric Chemistry and Physics: From Air Pollution to Climate Change, 2nd edition, John Wiley & Sons, 2006. Chapter 13, Eqs. 13.65-13.67.

_Source: Aerosol.jl src/dynamics.jl:178 @ commit c8c640bb636b22f2425460e9ed5cba50793bfee1 (esm-7pd). The model implements Eq. 13.65 (dN/dt = -K·N²/2) with algebraic characteristic coagulation time τ_c = 2/(K·N₀) (Eq. 13.67). N₀ is a parameter representing the initial number concentration; the user sets the ODE initial condition N(t=0) = N₀ consistently. τ_c is constant in time (algebraic, computed from parameters K and N₀). Analytical solution (Eq. 13.66): N(t) = N₀/(1 + t/τ_c). Tests mirror Aerosol.jl test/dynamics_test.jl ('MonodisperseCoagulation analytical solution', 'MonodisperseCoagulation characteristic time').

Tolerance rationale (model-level rel=1e-4): the ODE dN/dt = -K/2·N² has the exact Bernoulli solution N(t) = N₀/(1 + t/τ_c); numerical error from LSODA over 5τ_c is well below 1e-4 relative. The clean-background test (τ_c = 2×10⁵ s) and k-sensitivity test use the same tolerance._

## Variables

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `N` | `m^-3` | `1000000000000.0` | Total number concentration |

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `K` | `m^3/s` | `1e-15` | Coagulation coefficient |
| `N_0` | `m^-3` | `1000000000000.0` | Initial number concentration |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `τ_c` | `s` | `2000.0` | Characteristic coagulation time |

## Observed expressions

$$
τ_{c} = \frac{2}{K \cdot N_{0}}
$$
_Characteristic coagulation time_

## Equations

$$
\mathrm{D}\left(N\right) = \left(-0.5\right) \cdot K \cdot N^{2}
$$

## Analyses

### standard_urban_coagulation

Monodisperse coagulation for polluted urban aerosol (N₀ = 10¹² m⁻³, K = 10⁻¹⁵ m³/s). Characteristic coagulation time τ_c = 2000 s ≈ 33 minutes. N(t)/N₀ decays from 1 to 1/6 over five coagulation lifetimes (Seinfeld & Pandis 2006, Eq. 13.66).

**Time span:** 0.0 → 10000.0

![Total number concentration N(t) vs time, showing decay from N₀ = 10¹² m⁻³ over 5 coagulation lifetimes.](/plots/aerosol/dynamics/monodispersecoagulation/standard_urban_coagulation-N_vs_time_urban.png)

### clean_background_slow_coagulation

Monodisperse coagulation for clean background aerosol (N₀ = 10¹⁰ m⁻³, K = 10⁻¹⁵ m³/s). Characteristic coagulation time τ_c = 2×10⁵ s ≈ 55.6 hours. Number concentration decays far more slowly than the polluted urban case, illustrating the N₀-dependent timescale.

**Time span:** 0.0 → 400000.0

![Total number concentration N(t) vs time for clean background aerosol, showing the much longer coagulation timescale compared to polluted conditions.](/plots/aerosol/dynamics/monodispersecoagulation/clean_background_slow_coagulation-N_vs_time_clean.png)

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "variables": {
    "K": {
      "default": 1e-15,
      "type": "parameter",
      "units": "m^3/s",
      "description": "Coagulation coefficient"
    },
    "N_0": {
      "default": 1000000000000.0,
      "type": "parameter",
      "units": "m^-3",
      "description": "Initial number concentration"
    },
    "N": {
      "default": 1000000000000.0,
      "type": "unknown",
      "units": "m^-3",
      "description": "Total number concentration"
    },
    "τ_c": {
      "default": 2000.0,
      "type": "unknown",
      "units": "s",
      "description": "Characteristic coagulation time"
    }
  },
  "equations": [
    {
      "lhs": "τ_c",
      "rhs": {
        "op": "/",
        "args": [
          2,
          {
            "op": "*",
            "args": [
              "K",
              "N_0"
            ]
          }
        ]
      }
    },
    {
      "lhs": {
        "op": "D",
        "wrt": "t",
        "args": [
          "N"
        ]
      },
      "rhs": {
        "op": "*",
        "args": [
          -0.5,
          "K",
          {
            "op": "^",
            "args": [
              "N",
              2
            ]
          }
        ]
      }
    }
  ],
  "tolerance": {
    "rel": 0.0001
  },
  "tests": [
    {
      "id": "analytical_solution_default",
      "description": "Verify N(t) against analytical solution N(t) = N₀/(1 + t/τ_c) (Eq. 13.66) at multiple time points with default parameters (K = 10⁻¹⁵ m³/s, N₀ = 10¹² m⁻³). Characteristic coagulation time τ_c = 2/(K·N₀) = 2000 s. Samples the half-life (N = N₀/2 at t = τ_c = 2000 s) and quarter-life (N = N₀/5 at t = 4τ_c = 8000 s), and confirms τ_c is constant throughout (algebraic, parameterized). Mirrors the 'MonodisperseCoagulation analytical solution' test in Aerosol.jl/test/dynamics_test.jl.",
      "initial_conditions": {
        "N": 1000000000000.0
      },
      "time_span": {
        "start": 0.0,
        "end": 10000.0
      },
      "assertions": [
        {
          "variable": "N",
          "time": 0.0,
          "expected": 1000000000000.0
        },
        {
          "variable": "N",
          "time": 500.0,
          "expected": 800000000000.0
        },
        {
          "variable": "N",
          "time": 2000.0,
          "expected": 500000000000.0
        },
        {
          "variable": "N",
          "time": 8000.0,
          "expected": 200000000000.0
        },
        {
          "variable": "N",
          "time": 10000.0,
          "expected": 166666666666.66666
        },
        {
          "variable": "τ_c",
          "time": 0.0,
          "expected": 2000.0
        },
        {
          "variable": "τ_c",
          "time": 10000.0,
          "expected": 2000.0
        }
      ]
    },
    {
      "id": "clean_background_characteristic_time",
      "description": "Characteristic coagulation time for clean background aerosol (N₀ = 10¹⁰ m⁻³, K = 10⁻¹⁵ m³/s): τ_c = 2/(K·N₀) = 2×10⁵ s ≈ 55.6 hours. Verifies both the algebraic τ_c and the analytical N(t) decay at t = τ_c (half-life) and t = 2τ_c. Mirrors the first case in the 'MonodisperseCoagulation characteristic time' test in Aerosol.jl.",
      "initial_conditions": {
        "N": 10000000000.0
      },
      "parameter_overrides": {
        "N_0": 10000000000.0
      },
      "time_span": {
        "start": 0.0,
        "end": 400000.0
      },
      "assertions": [
        {
          "variable": "τ_c",
          "time": 0.0,
          "expected": 200000.0
        },
        {
          "variable": "N",
          "time": 0.0,
          "expected": 10000000000.0
        },
        {
          "variable": "N",
          "time": 200000.0,
          "expected": 5000000000.0
        },
        {
          "variable": "N",
          "time": 400000.0,
          "expected": 3333333333.3333335
        }
      ]
    },
    {
      "id": "k_sensitivity_10x",
      "description": "Ten-fold increase in coagulation coefficient (K = 10⁻¹⁴ m³/s) reduces τ_c from 2000 s to 200 s and accelerates decay proportionally: N(200 s) = N₀/2 and N(800 s) = N₀/5. Verifies the linear scaling τ_c ∝ 1/K and its effect on the decay trajectory.",
      "initial_conditions": {
        "N": 1000000000000.0
      },
      "parameter_overrides": {
        "K": 1e-14
      },
      "time_span": {
        "start": 0.0,
        "end": 1000.0
      },
      "assertions": [
        {
          "variable": "τ_c",
          "time": 0.0,
          "expected": 200.0
        },
        {
          "variable": "N",
          "time": 0.0,
          "expected": 1000000000000.0
        },
        {
          "variable": "N",
          "time": 200.0,
          "expected": 500000000000.0
        },
        {
          "variable": "N",
          "time": 800.0,
          "expected": 200000000000.0
        }
      ]
    }
  ],
  "reference": {
    "citation": "Seinfeld, J. H. and Pandis, S. N.: Atmospheric Chemistry and Physics: From Air Pollution to Climate Change, 2nd edition, John Wiley & Sons, 2006. Chapter 13, Eqs. 13.65-13.67.",
    "notes": "Source: Aerosol.jl src/dynamics.jl:178 @ commit c8c640bb636b22f2425460e9ed5cba50793bfee1 (esm-7pd). The model implements Eq. 13.65 (dN/dt = -K·N²/2) with algebraic characteristic coagulation time τ_c = 2/(K·N₀) (Eq. 13.67). N₀ is a parameter representing the initial number concentration; the user sets the ODE initial condition N(t=0) = N₀ consistently. τ_c is constant in time (algebraic, computed from parameters K and N₀). Analytical solution (Eq. 13.66): N(t) = N₀/(1 + t/τ_c). Tests mirror Aerosol.jl test/dynamics_test.jl ('MonodisperseCoagulation analytical solution', 'MonodisperseCoagulation characteristic time').\n\nTolerance rationale (model-level rel=1e-4): the ODE dN/dt = -K/2·N² has the exact Bernoulli solution N(t) = N₀/(1 + t/τ_c); numerical error from LSODA over 5τ_c is well below 1e-4 relative. The clean-background test (τ_c = 2×10⁵ s) and k-sensitivity test use the same tolerance."
  },
  "analyses": [
    {
      "id": "standard_urban_coagulation",
      "description": "Monodisperse coagulation for polluted urban aerosol (N₀ = 10¹² m⁻³, K = 10⁻¹⁵ m³/s). Characteristic coagulation time τ_c = 2000 s ≈ 33 minutes. N(t)/N₀ decays from 1 to 1/6 over five coagulation lifetimes (Seinfeld & Pandis 2006, Eq. 13.66).",
      "time_span": {
        "start": 0.0,
        "end": 10000.0
      },
      "initial_state": {
        "N": 1000000000000.0
      },
      "plots": [
        {
          "id": "N_vs_time_urban",
          "type": "line",
          "description": "Total number concentration N(t) vs time, showing decay from N₀ = 10¹² m⁻³ over 5 coagulation lifetimes.",
          "x": {
            "variable": "t",
            "label": "time (s)"
          },
          "y": {
            "variable": "N",
            "label": "N (m⁻³)"
          }
        }
      ]
    },
    {
      "id": "clean_background_slow_coagulation",
      "description": "Monodisperse coagulation for clean background aerosol (N₀ = 10¹⁰ m⁻³, K = 10⁻¹⁵ m³/s). Characteristic coagulation time τ_c = 2×10⁵ s ≈ 55.6 hours. Number concentration decays far more slowly than the polluted urban case, illustrating the N₀-dependent timescale.",
      "time_span": {
        "start": 0.0,
        "end": 400000.0
      },
      "initial_state": {
        "N": 10000000000.0
      },
      "parameters": {
        "N_0": 10000000000.0
      },
      "plots": [
        {
          "id": "N_vs_time_clean",
          "type": "line",
          "description": "Total number concentration N(t) vs time for clean background aerosol, showing the much longer coagulation timescale compared to polluted conditions.",
          "x": {
            "variable": "t",
            "label": "time (s)"
          },
          "y": {
            "variable": "N",
            "label": "N (m⁻³)"
          }
        }
      ]
    }
  ]
}
```

</details>
