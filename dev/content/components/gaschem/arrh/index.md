---
title: "arrh"
slug: "arrh"
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

_source_ref: GasChem.jl@8c12c048482b515fb8eb2110bf8ab4b4f4e71309:src/SuperFast.jl:33

`arrh(t, T, P, a0, b0, c0)` is the SuperFast modified-Arrhenius rate builder. It is the workhorse rate law of the SuperFast mechanism: most of the ~20 gas-phase reactions in SuperFast() are built with it (through the local `arr` closure), and the three other builders in this file (arr_3rd, rate_2HO2, rate_OH_CO) all compose arrh sub-systems internally.

The compiled equation is `k ~ a0 * exp(c0/T) * (K_300/T)^b0 * c`, with `air_volume = R*T/P` and `c = A/air_volume*ppb_unit` as Julia locals. NOTE the exponent base: the source CODE uses (K_300/T)^b0 = (300/T)^b0, whereas the function's docstring writes (T/300)^b0 — the code is authoritative and is what every SuperFast reaction actually uses, so this migration transcribes (K_300/T)^b0. air_volume and c are `type: state` cascade variables; k is the `type: state` output. a0/b0/c0 and A/R/ppb_unit/K_300 are `type: parameter`; the unused upstream `@constants num_density_unit_inv` is omitted.

Defaults a0 = 1.7e-12 cm^3/molec/s, b0 = 0 (dimensionless), c0 = -940 K are the coefficients of the first SuperFast reaction, `arr(T, P, 1.7e-12, 0.0, -940.0), O3 + OH --> HO2 + O2` (SuperFast.jl:275). With b0 = 0 the (K_300/T)^b0 factor is exactly 1.0; the b0_nonzero test exercises a non-trivial power-law factor and the o3_no_reaction_coefficients test swaps in a second real SuperFast coefficient set. At the defaults k = 0.0015516914092470017 (s*ppb)^-1.

Algebraic, no time derivative. Tolerance rel=1e-10, purely relative: the equation adds one exp and one pow to the rate_toppb expression tree; both are correctly-rounded library calls and 1e-10 absorbs any libm/numpy ULP-level difference while still pinning a0, b0, c0 and the (K_300/T) base to full working precision._

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `T` | `K` | `280.0` | Air temperature. Upstream the rate-law builders receive T as a `ParentScope` parameter; the default 280.0 K is the SuperFast() `@parameters T` default (SuperFast.jl:250). |
| `P` | `Pa` | `101325.0` | Air pressure. Upstream a `ParentScope` parameter; the default 101325 Pa (1 atm) is the SuperFast() `@parameters P` default (SuperFast.jl:251). |
| `A` | `molec/mol` | `6.02e+23` | Avogadro's number. Upstream `@constants A = 6.02e23` (SuperFast.jl). Appears in the ppb conversion factor c = A/air_volume*ppb_unit. |
| `R` | `(Pa*cm^3)/(K*mol)` | `8314000.0` | Universal gas constant in the upstream's mixed Pa-cm^3 unit system. Upstream `@constants R = 8.314e6`. Sets the molar air volume air_volume = R*T/P. |
| `ppb_unit` | `1/ppb` | `1e-09` | mol/mol_air per ppb: 1 ppb is 1e-9 mol/mol, so the factor is 1e-9 with units 1/ppb, and c = A/air_volume*ppb_unit carries molec/(cm^3*ppb). Upstream `@constants ppb_unit = 1.0e-9` declares the unit as `ppb`, the exponent the wrong way round (the value is unchanged). |
| `K_300` | `K` | `300.0` | Arrhenius reference temperature (300 K). Upstream `@constants K_300 = 300`. |
| `a0` | `cm^3/molec/s` | `1.7e-12` | Arrhenius pre-exponential factor in CGS cm^3/molec/s. Default 1.7e-12 from `O3 + OH --> HO2 + O2` (SuperFast.jl:275). |
| `b0` | `1` | `0.0` | Arrhenius power-law (temperature) exponent for the (K_300/T)^b0 factor. Default 0.0 (no power-law dependence) from `O3 + OH --> HO2 + O2`. |
| `c0` | `K` | `-940.0` | Arrhenius activation-temperature parameter (-Ea/R) in K for the exp(c0/T) factor. Default -940.0 from `O3 + OH --> HO2 + O2`. |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `air_volume` | `cm^3/mol` |  | Molar volume of air, R*T/P. |
| `c` | `molec/(cm^3*ppb)` |  | ppb conversion factor A/air_volume*ppb_unit. |
| `k` | `1/(s*ppb)` |  | Modified-Arrhenius rate coefficient in (s*ppb)^-1: k = a0*exp(c0/T)*(K_300/T)^b0*c. |

## Observed expressions

$$
air_{volume} = \frac{R \cdot T}{P}
$$
_Molar volume of air, R*T/P._

$$
c = \frac{A}{air_{volume}} \cdot ppb_{unit}
$$
_ppb conversion factor A/air_volume*ppb_unit._

$$
k = a0 \cdot e^{\frac{c0}{T}} \cdot \frac{K_{300}}{T}^{b0} \cdot c
$$
_Modified-Arrhenius rate coefficient in (s*ppb)^-1: k = a0*exp(c0/T)*(K_300/T)^b0*c._

## Analyses

### arrhenius_rate_vs_temperature

Sweeps temperature T from 230 K to 320 K with the default O3+OH coefficients (a0=1.7e-12, b0=0, c0=-940). With c0 negative the exp(c0/T) Arrhenius factor rises steeply with temperature, the classic Arrhenius rate-vs-temperature curve.

**Time span:** 0.0 → 1.0

**Swept over:** `T`

![Modified-Arrhenius rate coefficient k versus temperature for the O3 + OH reaction — a rising Arrhenius curve.](/plots/gaschem/arrh/arrhenius_rate_vs_temperature-arrhenius_k_vs_t.png)

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "reference": {
    "notes": "source_ref: GasChem.jl@8c12c048482b515fb8eb2110bf8ab4b4f4e71309:src/SuperFast.jl:33\n\n`arrh(t, T, P, a0, b0, c0)` is the SuperFast modified-Arrhenius rate builder. It is the workhorse rate law of the SuperFast mechanism: most of the ~20 gas-phase reactions in SuperFast() are built with it (through the local `arr` closure), and the three other builders in this file (arr_3rd, rate_2HO2, rate_OH_CO) all compose arrh sub-systems internally.\n\nThe compiled equation is `k ~ a0 * exp(c0/T) * (K_300/T)^b0 * c`, with `air_volume = R*T/P` and `c = A/air_volume*ppb_unit` as Julia locals. NOTE the exponent base: the source CODE uses (K_300/T)^b0 = (300/T)^b0, whereas the function's docstring writes (T/300)^b0 — the code is authoritative and is what every SuperFast reaction actually uses, so this migration transcribes (K_300/T)^b0. air_volume and c are `type: state` cascade variables; k is the `type: state` output. a0/b0/c0 and A/R/ppb_unit/K_300 are `type: parameter`; the unused upstream `@constants num_density_unit_inv` is omitted.\n\nDefaults a0 = 1.7e-12 cm^3/molec/s, b0 = 0 (dimensionless), c0 = -940 K are the coefficients of the first SuperFast reaction, `arr(T, P, 1.7e-12, 0.0, -940.0), O3 + OH --> HO2 + O2` (SuperFast.jl:275). With b0 = 0 the (K_300/T)^b0 factor is exactly 1.0; the b0_nonzero test exercises a non-trivial power-law factor and the o3_no_reaction_coefficients test swaps in a second real SuperFast coefficient set. At the defaults k = 0.0015516914092470017 (s*ppb)^-1.\n\nAlgebraic, no time derivative. Tolerance rel=1e-10, purely relative: the equation adds one exp and one pow to the rate_toppb expression tree; both are correctly-rounded library calls and 1e-10 absorbs any libm/numpy ULP-level difference while still pinning a0, b0, c0 and the (K_300/T) base to full working precision."
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
    "K_300": {
      "type": "parameter",
      "units": "K",
      "default": 300.0,
      "description": "Arrhenius reference temperature (300 K). Upstream `@constants K_300 = 300`."
    },
    "a0": {
      "type": "parameter",
      "units": "cm^3/molec/s",
      "default": 1.7e-12,
      "description": "Arrhenius pre-exponential factor in CGS cm^3/molec/s. Default 1.7e-12 from `O3 + OH --> HO2 + O2` (SuperFast.jl:275)."
    },
    "b0": {
      "type": "parameter",
      "units": "1",
      "default": 0.0,
      "description": "Arrhenius power-law (temperature) exponent for the (K_300/T)^b0 factor. Default 0.0 (no power-law dependence) from `O3 + OH --> HO2 + O2`."
    },
    "c0": {
      "type": "parameter",
      "units": "K",
      "default": -940.0,
      "description": "Arrhenius activation-temperature parameter (-Ea/R) in K for the exp(c0/T) factor. Default -940.0 from `O3 + OH --> HO2 + O2`."
    },
    "air_volume": {
      "type": "unknown",
      "units": "cm^3/mol",
      "description": "Molar volume of air, R*T/P."
    },
    "c": {
      "type": "unknown",
      "units": "molec/(cm^3*ppb)",
      "description": "ppb conversion factor A/air_volume*ppb_unit."
    },
    "k": {
      "type": "unknown",
      "units": "1/(s*ppb)",
      "description": "Modified-Arrhenius rate coefficient in (s*ppb)^-1: k = a0*exp(c0/T)*(K_300/T)^b0*c."
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
          {
            "op": "exp",
            "args": [
              {
                "op": "/",
                "args": [
                  "c0",
                  "T"
                ]
              }
            ]
          },
          {
            "op": "^",
            "args": [
              {
                "op": "/",
                "args": [
                  "K_300",
                  "T"
                ]
              },
              "b0"
            ]
          },
          "c"
        ]
      }
    }
  ],
  "tests": [
    {
      "id": "default_o3_oh_reaction",
      "description": "All parameters at their defaults: T=280 K, P=101325 Pa, a0=1.7e-12, b0=0.0, c0=-940.0 (the O3 + OH --> HO2 + O2 coefficient set). With b0=0 the (K_300/T)^b0 power-law factor is exactly 1.0. Pins every cascade variable; k asserted at t=0 and t=1 for time-invariance.",
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
          "expected": 0.0015516914092470017
        },
        {
          "variable": "k",
          "time": 1.0,
          "expected": 0.0015516914092470017
        }
      ]
    },
    {
      "id": "warm_temperature",
      "description": "T raised to 300 K. Both the exp(c0/T) Arrhenius factor and the conversion factor c shift with temperature; the test pins the combined result.",
      "parameter_overrides": {
        "arrh.T": 300.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "air_volume",
          "time": 0.0,
          "expected": 24615.84011843079
        },
        {
          "variable": "c",
          "time": 0.0,
          "expected": 24455797450.084198
        },
        {
          "variable": "k",
          "time": 0.0,
          "expected": 0.0018115126600967313
        }
      ]
    },
    {
      "id": "nonzero_power_law_exponent",
      "description": "b0 set to 2.0 with all else at defaults, activating the (K_300/T)^b0 power-law factor. At T=280 K, K_300/T = 300/280 > 1, so (K_300/T)^2 > 1 and k is larger than the b0=0 default.",
      "parameter_overrides": {
        "arrh.b0": 2.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "k",
          "time": 0.0,
          "expected": 0.0017812784034723233
        }
      ]
    },
    {
      "id": "zero_activation_temperature",
      "description": "c0 set to 0.0, so the exp(c0/T) factor collapses to exp(0)=1.0 and k reduces to a0*(K_300/T)^b0*c. With the default b0=0 this is just a0*c = the rate_toppb form — k jumps by exactly the factor 1/exp(-940/280) relative to the default.",
      "parameter_overrides": {
        "arrh.c0": 0.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "k",
          "time": 0.0,
          "expected": 0.04454448821265336
        }
      ]
    },
    {
      "id": "o3_no_reaction_coefficients",
      "description": "A second real SuperFast coefficient set: a0=3.0e-12, b0=0.0, c0=-1500.0, the O3 + NO --> NO2 + O2 reaction (SuperFast.jl:280). Exercises arrh with a different pre-exponential and a stronger (more negative) activation temperature.",
      "parameter_overrides": {
        "arrh.a0": 3e-12,
        "arrh.b0": 0.0,
        "arrh.c0": -1500.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "k",
          "time": 0.0,
          "expected": 0.00037058575829340316
        }
      ]
    }
  ],
  "analyses": [
    {
      "id": "arrhenius_rate_vs_temperature",
      "description": "Sweeps temperature T from 230 K to 320 K with the default O3+OH coefficients (a0=1.7e-12, b0=0, c0=-940). With c0 negative the exp(c0/T) Arrhenius factor rises steeply with temperature, the classic Arrhenius rate-vs-temperature curve.",
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
          "id": "arrhenius_k_vs_t",
          "type": "line",
          "description": "Modified-Arrhenius rate coefficient k versus temperature for the O3 + OH reaction — a rising Arrhenius curve.",
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
