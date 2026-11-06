---
title: "rate_toppb"
slug: "rate_toppb"
domains: ["gaschem"]
component_types: ["model"]
domain: "gaschem"
component_type: "model"
esm_version: "1.0.0"
esm_path: "components/gaschem/superfast_ratelaws.esm"
reference: "Brown-Steiner, B., Selin, N. E., Prinn, R. G., Tilmes, S., Emmons, L., Lamarque, J.-F., & Cameron-Smith, P. (2018). Evaluating simplified chemical mechanisms within present-day simulations of the Community Earth System Model version 1.2 with CAM4 (CESM1.2 CAM-chem): MOZART-4 vs. Reduced Hydrocarbon vs. Super-Fast chemistry. Geoscientific Model Development, 11, 4155-4174. The Super-Fast mechanism whose rate laws these builder functions construct."
description: "The five SuperFast rate-law helper functions migrated from GasChem.jl@8c12c048482b515fb8eb2110bf8ab4b4f4e71309 src/SuperFast.jl — the reusable builder functions the SuperFast() chemical mechanism uses to construct the rate coefficient of every gas-phase reaction. Each is migrated as its own observed-only algebraic `models` entry: rate_toppb (SuperFast.jl:6) the constant-rate / `constant_k` converter, arrh (:33) the modified-Arrhenius workhorse, arr_3rd (:64) the third-body / Troe-falloff law, rate_2HO2 (:102) the HO2+HO2 law with water-vapour enhancement, and rate_OH_CO (:142) the JPL 15-10 OH+CO law. Upstream each function returns a one-variable ReactionSystem (`@variables k(t)`); the composed builders (arr_3rd, rate_2HO2, rate_OH_CO) compose `arrh` sub-systems. This file reproduces each function's compiled rate as a topologically-ordered cascade of `type: state` algebraic equations whose named intermediates mirror the upstream Julia locals and sub-system k's verbatim, with the Arrhenius coefficients exposed as `type: parameter` (defaults taken from the representative SuperFast reaction each builder serves). All five models are purely algebraic — no time derivatives — so each rate coefficient is constant in time. Units follow the upstream's mixed CGS / ppb system (rate coefficients in 1/(s*ppb), Arrhenius pre-exponentials in cm^3/molec/s)."
tags: ["gaschem", "model", "superfast", "rate-laws", "reaction-rate", "arrhenius", "troe-falloff", "interface", "observed-only", "tropospheric-chemistry"]
---

## Description

The five SuperFast rate-law helper functions migrated from GasChem.jl@8c12c048482b515fb8eb2110bf8ab4b4f4e71309 src/SuperFast.jl — the reusable builder functions the SuperFast() chemical mechanism uses to construct the rate coefficient of every gas-phase reaction. Each is migrated as its own observed-only algebraic `models` entry: rate_toppb (SuperFast.jl:6) the constant-rate / `constant_k` converter, arrh (:33) the modified-Arrhenius workhorse, arr_3rd (:64) the third-body / Troe-falloff law, rate_2HO2 (:102) the HO2+HO2 law with water-vapour enhancement, and rate_OH_CO (:142) the JPL 15-10 OH+CO law. Upstream each function returns a one-variable ReactionSystem (`@variables k(t)`); the composed builders (arr_3rd, rate_2HO2, rate_OH_CO) compose `arrh` sub-systems. This file reproduces each function's compiled rate as a topologically-ordered cascade of `type: state` algebraic equations whose named intermediates mirror the upstream Julia locals and sub-system k's verbatim, with the Arrhenius coefficients exposed as `type: parameter` (defaults taken from the representative SuperFast reaction each builder serves). All five models are purely algebraic — no time derivatives — so each rate coefficient is constant in time. Units follow the upstream's mixed CGS / ppb system (rate coefficients in 1/(s*ppb), Arrhenius pre-exponentials in cm^3/molec/s).

## Reference

_source_ref: GasChem.jl@8c12c048482b515fb8eb2110bf8ab4b4f4e71309:src/SuperFast.jl:6

`rate_toppb(t, T, P, a0)` is the SuperFast constant-rate (a.k.a. `constant_k`) builder: it wraps a temperature-independent reaction rate coefficient a0, supplied in CGS cm^3/molec/s, and converts it to the (s*ppb)^-1 units the SuperFast mechanism's ppb-based species require. It is the rate law used for the single constant-rate SuperFast reaction `cons(4.0e-24, T, P), H2O + NO2 --> 0.5HNO3` (SuperFast.jl:291); the SuperFast() builder calls it through the local `cons` closure, hence the `constant_k` alias in the migration tracker title.

Upstream the function returns a one-variable `ReactionSystem` with `@variables k(t)` and the single equation `k ~ a0 * c`, where `air_volume = R*T/P` and `c = A/air_volume*ppb_unit` are Julia locals. This migration preserves that decomposition explicitly: air_volume and c are `type: state` cascade variables (each defined by one algebraic equation) and k is the `type: state` output. The rate coefficient a0 and the three physical constants A/R/ppb_unit are `type: parameter`. The upstream `@constants` block also declares num_density_unit_inv, which rate_toppb's equation never references; it is omitted here so every declared parameter is load-bearing.

Default a0 = 4.0e-24 cm^3/molec/s is the coefficient of the only SuperFast reaction that uses this builder (H2O + NO2 --> 0.5HNO3). T = 280 K and P = 101325 Pa are the SuperFast() parameter defaults. At those defaults air_volume = 22974.784110535405 cm^3/mol, c = 26202640125.09021 and k = 1.0481056050036084e-13 (s*ppb)^-1.

Algebraic, no time derivative: every variable is the LHS of exactly one equation in T, P and the constants, so the trajectory is constant in time (the default test pins k at t=0 and t=1). Tolerance rel=1e-10 is purely relative — the three equations are a handful of IEEE-754 ops each, correctly-rounded to ~1 ULP, and 1e-10 leaves ~5 orders of magnitude of headroom while still catching any coefficient or operator regression. No abs floor is needed: every value is solidly non-zero._

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `T` | `K` | `280.0` | Air temperature. Upstream the rate-law builders receive T as a `ParentScope` parameter; the default 280.0 K is the SuperFast() `@parameters T` default (SuperFast.jl:250). |
| `P` | `Pa` | `101325.0` | Air pressure. Upstream a `ParentScope` parameter; the default 101325 Pa (1 atm) is the SuperFast() `@parameters P` default (SuperFast.jl:251). |
| `A` | `molec/mol` | `6.02e+23` | Avogadro's number. Upstream `@constants A = 6.02e23` (SuperFast.jl). Appears in the ppb conversion factor c = A/air_volume*ppb_unit. |
| `R` | `(Pa*cm^3)/(K*mol)` | `8314000.0` | Universal gas constant in the upstream's mixed Pa-cm^3 unit system. Upstream `@constants R = 8.314e6`. Sets the molar air volume air_volume = R*T/P. |
| `ppb_unit` | `1/ppb` | `1e-09` | mol/mol_air per ppb: 1 ppb is 1e-9 mol/mol, so the factor is 1e-9 with units 1/ppb, and c = A/air_volume*ppb_unit carries molec/(cm^3*ppb). Upstream `@constants ppb_unit = 1.0e-9` declares the unit as `ppb`, the exponent the wrong way round (the value is unchanged). |
| `a0` | `cm^3/molec/s` | `4e-24` | Constant (temperature-independent) reaction rate coefficient in CGS cm^3/molec/s. Default 4.0e-24 from the SuperFast reaction `H2O + NO2 --> 0.5HNO3` (SuperFast.jl:291). |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `air_volume` | `cm^3/mol` |  | Molar volume of air, R*T/P. |
| `c` | `molec/(cm^3*ppb)` |  | ppb conversion factor A/air_volume*ppb_unit applied to the CGS rate coefficient. |
| `k` | `1/(s*ppb)` |  | Reaction rate coefficient in SuperFast (s*ppb)^-1 units: k = a0 * c. |

## Observed expressions

$$
air_{volume} = \frac{R \cdot T}{P}
$$
_Molar volume of air, R*T/P._

$$
c = \frac{A}{air_{volume}} \cdot ppb_{unit}
$$
_ppb conversion factor A/air_volume*ppb_unit applied to the CGS rate coefficient._

$$
k = a0 \cdot c
$$
_Reaction rate coefficient in SuperFast (s*ppb)^-1 units: k = a0 * c._

## Analyses

### constant_rate_vs_temperature

Sweeps temperature T from 230 K to 320 K (the tropospheric range) with P and a0 at defaults. The constant-rate builder has no Arrhenius factor, so the only temperature dependence is through c = A*P/(R*T)*ppb_unit: k falls as 1/T across the sweep.

**Time span:** 0.0 → 1.0

**Swept over:** `T`

![Converted constant rate coefficient k versus temperature — a smooth 1/T decay.](/plots/gaschem/rate_toppb/constant_rate_vs_temperature-constant_rate_k_vs_t.png)

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "reference": {
    "notes": "source_ref: GasChem.jl@8c12c048482b515fb8eb2110bf8ab4b4f4e71309:src/SuperFast.jl:6\n\n`rate_toppb(t, T, P, a0)` is the SuperFast constant-rate (a.k.a. `constant_k`) builder: it wraps a temperature-independent reaction rate coefficient a0, supplied in CGS cm^3/molec/s, and converts it to the (s*ppb)^-1 units the SuperFast mechanism's ppb-based species require. It is the rate law used for the single constant-rate SuperFast reaction `cons(4.0e-24, T, P), H2O + NO2 --> 0.5HNO3` (SuperFast.jl:291); the SuperFast() builder calls it through the local `cons` closure, hence the `constant_k` alias in the migration tracker title.\n\nUpstream the function returns a one-variable `ReactionSystem` with `@variables k(t)` and the single equation `k ~ a0 * c`, where `air_volume = R*T/P` and `c = A/air_volume*ppb_unit` are Julia locals. This migration preserves that decomposition explicitly: air_volume and c are `type: state` cascade variables (each defined by one algebraic equation) and k is the `type: state` output. The rate coefficient a0 and the three physical constants A/R/ppb_unit are `type: parameter`. The upstream `@constants` block also declares num_density_unit_inv, which rate_toppb's equation never references; it is omitted here so every declared parameter is load-bearing.\n\nDefault a0 = 4.0e-24 cm^3/molec/s is the coefficient of the only SuperFast reaction that uses this builder (H2O + NO2 --> 0.5HNO3). T = 280 K and P = 101325 Pa are the SuperFast() parameter defaults. At those defaults air_volume = 22974.784110535405 cm^3/mol, c = 26202640125.09021 and k = 1.0481056050036084e-13 (s*ppb)^-1.\n\nAlgebraic, no time derivative: every variable is the LHS of exactly one equation in T, P and the constants, so the trajectory is constant in time (the default test pins k at t=0 and t=1). Tolerance rel=1e-10 is purely relative — the three equations are a handful of IEEE-754 ops each, correctly-rounded to ~1 ULP, and 1e-10 leaves ~5 orders of magnitude of headroom while still catching any coefficient or operator regression. No abs floor is needed: every value is solidly non-zero."
  },
  "tolerance": {
    "rel": 1e-10
  },
  "variables": {
    "T": {
      "type": "parameter",
      "units": "K",
      "default": 280.0,
      "description": "Air temperature. Upstream the rate-law builders receive T as a `ParentScope` parameter; the default 280.0 K is the SuperFast() `@parameters T` default (SuperFast.jl:250)."
    },
    "P": {
      "type": "parameter",
      "units": "Pa",
      "default": 101325.0,
      "description": "Air pressure. Upstream a `ParentScope` parameter; the default 101325 Pa (1 atm) is the SuperFast() `@parameters P` default (SuperFast.jl:251)."
    },
    "A": {
      "type": "parameter",
      "units": "molec/mol",
      "default": 6.02e+23,
      "description": "Avogadro's number. Upstream `@constants A = 6.02e23` (SuperFast.jl). Appears in the ppb conversion factor c = A/air_volume*ppb_unit."
    },
    "R": {
      "type": "parameter",
      "units": "(Pa*cm^3)/(K*mol)",
      "default": 8314000.0,
      "description": "Universal gas constant in the upstream's mixed Pa-cm^3 unit system. Upstream `@constants R = 8.314e6`. Sets the molar air volume air_volume = R*T/P."
    },
    "ppb_unit": {
      "type": "parameter",
      "units": "1/ppb",
      "default": 1e-09,
      "description": "mol/mol_air per ppb: 1 ppb is 1e-9 mol/mol, so the factor is 1e-9 with units 1/ppb, and c = A/air_volume*ppb_unit carries molec/(cm^3*ppb). Upstream `@constants ppb_unit = 1.0e-9` declares the unit as `ppb`, the exponent the wrong way round (the value is unchanged)."
    },
    "a0": {
      "type": "parameter",
      "units": "cm^3/molec/s",
      "default": 4e-24,
      "description": "Constant (temperature-independent) reaction rate coefficient in CGS cm^3/molec/s. Default 4.0e-24 from the SuperFast reaction `H2O + NO2 --> 0.5HNO3` (SuperFast.jl:291)."
    },
    "air_volume": {
      "type": "unknown",
      "units": "cm^3/mol",
      "description": "Molar volume of air, R*T/P."
    },
    "c": {
      "type": "unknown",
      "units": "molec/(cm^3*ppb)",
      "description": "ppb conversion factor A/air_volume*ppb_unit applied to the CGS rate coefficient."
    },
    "k": {
      "type": "unknown",
      "units": "1/(s*ppb)",
      "description": "Reaction rate coefficient in SuperFast (s*ppb)^-1 units: k = a0 * c."
    }
  },
  "equations": [
    {
      "lhs": "air_volume",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "*",
            "args": [
              "R",
              "T"
            ]
          },
          "P"
        ]
      }
    },
    {
      "lhs": "c",
      "rhs": {
        "op": "*",
        "args": [
          {
            "op": "/",
            "args": [
              "A",
              "air_volume"
            ]
          },
          "ppb_unit"
        ]
      }
    },
    {
      "lhs": "k",
      "rhs": {
        "op": "*",
        "args": [
          "a0",
          "c"
        ]
      }
    }
  ],
  "tests": [
    {
      "id": "default_h2o_no2_reaction",
      "description": "All parameters at their defaults: T=280 K, P=101325 Pa, a0=4.0e-24 cm^3/molec/s (the H2O + NO2 --> 0.5HNO3 coefficient). Pins every cascade variable, so any wrong constant or operator is caught. k is asserted at t=0 and t=1 — the model is algebraic with no time derivative, so the trajectory must be exactly constant.",
      "parameter_overrides": {},
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "air_volume",
          "time": 0.0,
          "expected": 22974.784110535405
        },
        {
          "variable": "c",
          "time": 0.0,
          "expected": 26202640125.09021
        },
        {
          "variable": "k",
          "time": 0.0,
          "expected": 1.0481056050036084e-13
        },
        {
          "variable": "k",
          "time": 1.0,
          "expected": 1.0481056050036084e-13
        }
      ]
    },
    {
      "id": "cold_temperature",
      "description": "T lowered to 250 K with P and a0 at defaults. air_volume = R*T/P falls with T, so the conversion factor c = A/air_volume*ppb_unit rises and k rises proportionally — k is inversely proportional to temperature.",
      "parameter_overrides": {
        "rate_toppb.T": 250.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "air_volume",
          "time": 0.0,
          "expected": 20513.200098692327
        },
        {
          "variable": "c",
          "time": 0.0,
          "expected": 29346956940.101036
        },
        {
          "variable": "k",
          "time": 0.0,
          "expected": 1.1738782776040414e-13
        }
      ]
    },
    {
      "id": "high_pressure",
      "description": "P raised to 120000 Pa with T and a0 at defaults. air_volume falls with rising P, so c and k both rise — k is linearly proportional to pressure.",
      "parameter_overrides": {
        "rate_toppb.P": 120000.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "air_volume",
          "time": 0.0,
          "expected": 19399.333333333332
        },
        {
          "variable": "c",
          "time": 0.0,
          "expected": 31031994226.60573
        },
        {
          "variable": "k",
          "time": 0.0,
          "expected": 1.241279769064229e-13
        }
      ]
    },
    {
      "id": "rate_coefficient_doubled",
      "description": "a0 doubled to 8.0e-24 cm^3/molec/s with T and P at defaults. Since k = a0*c and c depends only on T and P, k doubles exactly while air_volume and c are unchanged — confirms a0 is wired as a linear multiplier.",
      "parameter_overrides": {
        "rate_toppb.a0": 8e-24
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "c",
          "time": 0.0,
          "expected": 26202640125.09021
        },
        {
          "variable": "k",
          "time": 0.0,
          "expected": 2.0962112100072168e-13
        }
      ]
    }
  ],
  "analyses": [
    {
      "id": "constant_rate_vs_temperature",
      "description": "Sweeps temperature T from 230 K to 320 K (the tropospheric range) with P and a0 at defaults. The constant-rate builder has no Arrhenius factor, so the only temperature dependence is through c = A*P/(R*T)*ppb_unit: k falls as 1/T across the sweep.",
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "parameter_sweep": {
        "type": "cartesian",
        "dimensions": [
          {
            "parameter": "T",
            "range": {
              "start": 230.0,
              "stop": 320.0,
              "count": 60,
              "scale": "linear"
            }
          }
        ]
      },
      "plots": [
        {
          "id": "constant_rate_k_vs_t",
          "type": "line",
          "description": "Converted constant rate coefficient k versus temperature — a smooth 1/T decay.",
          "x": {
            "variable": "T",
            "label": "Temperature (K)"
          },
          "y": {
            "variable": "k",
            "label": "Rate coefficient k (1/(s*ppb))"
          }
        }
      ]
    }
  ]
}
```

</details>
