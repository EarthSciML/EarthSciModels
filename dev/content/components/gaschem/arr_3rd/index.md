---
title: "arr_3rd"
slug: "arr_3rd"
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

_source_ref: GasChem.jl@8c12c048482b515fb8eb2110bf8ab4b4f4e71309:src/SuperFast.jl:64

`arr_3rd(t, T, P, a1, b1, c1, a2, b2, c2, fv)` is the SuperFast third-body / pressure-dependent (Troe falloff) rate builder. (a1,b1,c1) are the Arrhenius parameters of the low-pressure limit, (a2,b2,c2) of the high-pressure limit, and fv is the Troe falloff broadening parameter (Atkinson et al. 1992, J. Phys. Chem. Ref. Data 21 p.1145; usually 0.6). It builds the single SuperFast third-body reaction `arr3(T, P, 1.8e-30, 3.0, 0.0, 2.8e-11, 0.0, 0.0, 0.6), NO2 + OH --> HNO3` (SuperFast.jl:282).

Upstream arr_3rd composes two `arrh` sub-systems (`alow`, `ahigh`) and combines their k via the Julia locals num_density_unitless, rlow, rhigh, xyrat, blog, fexp:
  num_density_unitless = A*P/(R*T)*num_density_unit_inv
  alow.k, ahigh.k       = arrh(a1,b1,c1), arrh(a2,b2,c2)
  rlow  = alow.k*num_density_unitless ; rhigh = ahigh.k
  xyrat = rlow/rhigh ; blog = log10(xyrat)
  fexp  = 1/(1+blog*blog)
  k     = rlow*(fv^fexp)/(1+xyrat)
This migration makes each upstream-named quantity a `type: state` cascade variable: air_volume, c (the shared ppb conversion, used by both sub-arrh equations), num_density_unitless, alow_k, ahigh_k, rlow, xyrat, blog, fexp and the output k — ten equations, topologically ordered. The trivial alias rhigh = ahigh.k is folded into xyrat = rlow/ahigh_k. The two sub-arrh k's are the genuine MTK `@variables k(t)` of the composed `arrh` ReactionSystems; the rest are upstream Julia locals reproduced verbatim. a1/b1/c1/a2/b2/c2/fv and A/R/ppb_unit/num_density_unit_inv/K_300 are `type: parameter`.

Defaults are the NO2+OH coefficient set: a1=1.8e-30, b1=3.0, c1=0.0, a2=2.8e-11, b2=0.0, c2=0.0, fv=0.6. At T=280 K, P=101325 Pa the low-pressure branch gives alow_k=5.801058263845591e-20, rlow=1.5200304203222663, the falloff ratio xyrat=2.071806522801997 and k=0.3110225103483613 (s*ppb)^-1.

Algebraic, no time derivative. Tolerance rel=1e-10, purely relative — the cascade is ten small expression trees including one log10 and two pow calls; 1e-10 pins the falloff combination while absorbing library ULP noise. No abs floor: every cascade value is solidly non-zero across the tested scenarios._

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `T` | `K` | `280.0` | Air temperature. Upstream the rate-law builders receive T as a `ParentScope` parameter; the default 280.0 K is the SuperFast() `@parameters T` default (SuperFast.jl:250). |
| `P` | `Pa` | `101325.0` | Air pressure. Upstream a `ParentScope` parameter; the default 101325 Pa (1 atm) is the SuperFast() `@parameters P` default (SuperFast.jl:251). |
| `A` | `molec/mol` | `6.02e+23` | Avogadro's number. Upstream `@constants A = 6.02e23` (SuperFast.jl). Appears in the ppb conversion factor c = A/air_volume*ppb_unit. |
| `R` | `(Pa*cm^3)/(K*mol)` | `8314000.0` | Universal gas constant in the upstream's mixed Pa-cm^3 unit system. Upstream `@constants R = 8.314e6`. Sets the molar air volume air_volume = R*T/P. |
| `ppb_unit` | `1/ppb` | `1e-09` | mol/mol_air per ppb: 1 ppb is 1e-9 mol/mol, so the factor is 1e-9 with units 1/ppb, and c = A/air_volume*ppb_unit carries molec/(cm^3*ppb). Upstream `@constants ppb_unit = 1.0e-9` declares the unit as `ppb`, the exponent the wrong way round (the value is unchanged). |
| `num_density_unit_inv` | `cm^3/molec` | `1.0` | Unit-stripping factor that turns the air number density into the dimensionless num_density_unitless. Upstream `@constants num_density_unit_inv = 1`. |
| `K_300` | `K` | `300.0` | Arrhenius reference temperature (300 K). Upstream `@constants K_300 = 300`. |
| `a1` | `cm^3/molec/s` | `1.8e-30` | Low-pressure-limit Arrhenius pre-exponential. Default 1.8e-30 from `NO2 + OH --> HNO3` (SuperFast.jl:282). |
| `b1` | `1` | `3.0` | Low-pressure-limit power-law exponent. Default 3.0. |
| `c1` | `K` | `0.0` | Low-pressure-limit activation-temperature parameter. Default 0.0. |
| `a2` | `cm^3/molec/s` | `2.8e-11` | High-pressure-limit Arrhenius pre-exponential. Default 2.8e-11 from `NO2 + OH --> HNO3`. |
| `b2` | `1` | `0.0` | High-pressure-limit power-law exponent. Default 0.0. |
| `c2` | `K` | `0.0` | High-pressure-limit activation-temperature parameter. Default 0.0. |
| `fv` | `1` | `0.6` | Troe falloff broadening parameter (Atkinson et al. 1992). Default 0.6 from `NO2 + OH --> HNO3`. |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `air_volume` | `cm^3/mol` |  | Molar volume of air, R*T/P. |
| `c` | `molec/(cm^3*ppb)` |  | ppb conversion factor A/air_volume*ppb_unit, shared by both sub-arrh equations. |
| `num_density_unitless` | `1` |  | Dimensionless air number density A*P/(R*T)*num_density_unit_inv. |
| `alow_k` | `1/(s*ppb)` |  | Low-pressure-limit Arrhenius rate (arrh with a1,b1,c1). |
| `ahigh_k` | `1/(s*ppb)` |  | High-pressure-limit Arrhenius rate (arrh with a2,b2,c2). |
| `rlow` | `1/(s*ppb)` |  | Low-pressure rate scaled by number density, alow_k*num_density_unitless. |
| `xyrat` | `1` |  | Falloff ratio rlow/rhigh (rhigh = ahigh_k). |
| `blog` | `1` |  | log10 of the falloff ratio. |
| `fexp` | `1` |  | Troe broadening exponent 1/(1+blog*blog). |
| `k` | `1/(s*ppb)` |  | Third-body / falloff rate coefficient rlow*(fv^fexp)/(1+xyrat). |

## Observed expressions

$$
air_{volume} = \frac{R \cdot T}{P}
$$
_Molar volume of air, R*T/P._

$$
c = \frac{A}{air_{volume}} \cdot ppb_{unit}
$$
_ppb conversion factor A/air_volume*ppb_unit, shared by both sub-arrh equations._

$$
num_{density\,unitless} = \frac{A \cdot P}{R \cdot T} \cdot num_{density\,unit\,inv}
$$
_Dimensionless air number density A*P/(R*T)*num_density_unit_inv._

$$
alow_{k} = a1 \cdot e^{\frac{c1}{T}} \cdot \frac{K_{300}}{T}^{b1} \cdot c
$$
_Low-pressure-limit Arrhenius rate (arrh with a1,b1,c1)._

$$
ahigh_{k} = a2 \cdot e^{\frac{c2}{T}} \cdot \frac{K_{300}}{T}^{b2} \cdot c
$$
_High-pressure-limit Arrhenius rate (arrh with a2,b2,c2)._

$$
rlow = alow_{k} \cdot num_{density\,unitless}
$$
_Low-pressure rate scaled by number density, alow_k*num_density_unitless._

$$
xyrat = \frac{rlow}{ahigh_{k}}
$$
_Falloff ratio rlow/rhigh (rhigh = ahigh_k)._

$$
blog = \log_{10}\left(xyrat\right)
$$
_log10 of the falloff ratio._

$$
fexp = \frac{1.0}{1.0 + blog \cdot blog}
$$
_Troe broadening exponent 1/(1+blog*blog)._

$$
k = \frac{rlow \cdot fv^{fexp}}{1.0 + xyrat}
$$
_Third-body / falloff rate coefficient rlow*(fv^fexp)/(1+xyrat)._

## Analyses

### third_body_rate_vs_pressure

Sweeps pressure P from 20000 Pa to 101325 Pa (upper troposphere to surface) with the default NO2+OH coefficients. num_density_unitless is proportional to P, so the low-pressure branch and the falloff ratio xyrat both strengthen with pressure — the defining behaviour of a third-body / falloff rate law.

**Time span:** 0.0 → 1.0

**Swept over:** `P`

![Third-body rate coefficient k versus pressure — k climbs as the low-pressure branch fills in.](/plots/gaschem/arr_3rd/third_body_rate_vs_pressure-third_body_k_vs_p.png)

![Falloff ratio xyrat = rlow/rhigh versus pressure, showing the transition between the low- and high-pressure limits.](/plots/gaschem/arr_3rd/third_body_rate_vs_pressure-falloff_ratio_vs_p.png)

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "reference": {
    "notes": "source_ref: GasChem.jl@8c12c048482b515fb8eb2110bf8ab4b4f4e71309:src/SuperFast.jl:64\n\n`arr_3rd(t, T, P, a1, b1, c1, a2, b2, c2, fv)` is the SuperFast third-body / pressure-dependent (Troe falloff) rate builder. (a1,b1,c1) are the Arrhenius parameters of the low-pressure limit, (a2,b2,c2) of the high-pressure limit, and fv is the Troe falloff broadening parameter (Atkinson et al. 1992, J. Phys. Chem. Ref. Data 21 p.1145; usually 0.6). It builds the single SuperFast third-body reaction `arr3(T, P, 1.8e-30, 3.0, 0.0, 2.8e-11, 0.0, 0.0, 0.6), NO2 + OH --> HNO3` (SuperFast.jl:282).\n\nUpstream arr_3rd composes two `arrh` sub-systems (`alow`, `ahigh`) and combines their k via the Julia locals num_density_unitless, rlow, rhigh, xyrat, blog, fexp:\n  num_density_unitless = A*P/(R*T)*num_density_unit_inv\n  alow.k, ahigh.k       = arrh(a1,b1,c1), arrh(a2,b2,c2)\n  rlow  = alow.k*num_density_unitless ; rhigh = ahigh.k\n  xyrat = rlow/rhigh ; blog = log10(xyrat)\n  fexp  = 1/(1+blog*blog)\n  k     = rlow*(fv^fexp)/(1+xyrat)\nThis migration makes each upstream-named quantity a `type: state` cascade variable: air_volume, c (the shared ppb conversion, used by both sub-arrh equations), num_density_unitless, alow_k, ahigh_k, rlow, xyrat, blog, fexp and the output k — ten equations, topologically ordered. The trivial alias rhigh = ahigh.k is folded into xyrat = rlow/ahigh_k. The two sub-arrh k's are the genuine MTK `@variables k(t)` of the composed `arrh` ReactionSystems; the rest are upstream Julia locals reproduced verbatim. a1/b1/c1/a2/b2/c2/fv and A/R/ppb_unit/num_density_unit_inv/K_300 are `type: parameter`.\n\nDefaults are the NO2+OH coefficient set: a1=1.8e-30, b1=3.0, c1=0.0, a2=2.8e-11, b2=0.0, c2=0.0, fv=0.6. At T=280 K, P=101325 Pa the low-pressure branch gives alow_k=5.801058263845591e-20, rlow=1.5200304203222663, the falloff ratio xyrat=2.071806522801997 and k=0.3110225103483613 (s*ppb)^-1.\n\nAlgebraic, no time derivative. Tolerance rel=1e-10, purely relative — the cascade is ten small expression trees including one log10 and two pow calls; 1e-10 pins the falloff combination while absorbing library ULP noise. No abs floor: every cascade value is solidly non-zero across the tested scenarios."
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
    "num_density_unit_inv": {
      "type": "parameter",
      "units": "cm^3/molec",
      "default": 1.0,
      "description": "Unit-stripping factor that turns the air number density into the dimensionless num_density_unitless. Upstream `@constants num_density_unit_inv = 1`."
    },
    "K_300": {
      "type": "parameter",
      "units": "K",
      "default": 300.0,
      "description": "Arrhenius reference temperature (300 K). Upstream `@constants K_300 = 300`."
    },
    "a1": {
      "type": "parameter",
      "units": "cm^3/molec/s",
      "default": 1.8e-30,
      "description": "Low-pressure-limit Arrhenius pre-exponential. Default 1.8e-30 from `NO2 + OH --> HNO3` (SuperFast.jl:282)."
    },
    "b1": {
      "type": "parameter",
      "units": "1",
      "default": 3.0,
      "description": "Low-pressure-limit power-law exponent. Default 3.0."
    },
    "c1": {
      "type": "parameter",
      "units": "K",
      "default": 0.0,
      "description": "Low-pressure-limit activation-temperature parameter. Default 0.0."
    },
    "a2": {
      "type": "parameter",
      "units": "cm^3/molec/s",
      "default": 2.8e-11,
      "description": "High-pressure-limit Arrhenius pre-exponential. Default 2.8e-11 from `NO2 + OH --> HNO3`."
    },
    "b2": {
      "type": "parameter",
      "units": "1",
      "default": 0.0,
      "description": "High-pressure-limit power-law exponent. Default 0.0."
    },
    "c2": {
      "type": "parameter",
      "units": "K",
      "default": 0.0,
      "description": "High-pressure-limit activation-temperature parameter. Default 0.0."
    },
    "fv": {
      "type": "parameter",
      "units": "1",
      "default": 0.6,
      "description": "Troe falloff broadening parameter (Atkinson et al. 1992). Default 0.6 from `NO2 + OH --> HNO3`."
    },
    "air_volume": {
      "type": "unknown",
      "units": "cm^3/mol",
      "description": "Molar volume of air, R*T/P."
    },
    "c": {
      "type": "unknown",
      "units": "molec/(cm^3*ppb)",
      "description": "ppb conversion factor A/air_volume*ppb_unit, shared by both sub-arrh equations."
    },
    "num_density_unitless": {
      "type": "unknown",
      "units": "1",
      "description": "Dimensionless air number density A*P/(R*T)*num_density_unit_inv."
    },
    "alow_k": {
      "type": "unknown",
      "units": "1/(s*ppb)",
      "description": "Low-pressure-limit Arrhenius rate (arrh with a1,b1,c1)."
    },
    "ahigh_k": {
      "type": "unknown",
      "units": "1/(s*ppb)",
      "description": "High-pressure-limit Arrhenius rate (arrh with a2,b2,c2)."
    },
    "rlow": {
      "type": "unknown",
      "units": "1/(s*ppb)",
      "description": "Low-pressure rate scaled by number density, alow_k*num_density_unitless."
    },
    "xyrat": {
      "type": "unknown",
      "units": "1",
      "description": "Falloff ratio rlow/rhigh (rhigh = ahigh_k)."
    },
    "blog": {
      "type": "unknown",
      "units": "1",
      "description": "log10 of the falloff ratio."
    },
    "fexp": {
      "type": "unknown",
      "units": "1",
      "description": "Troe broadening exponent 1/(1+blog*blog)."
    },
    "k": {
      "type": "unknown",
      "units": "1/(s*ppb)",
      "description": "Third-body / falloff rate coefficient rlow*(fv^fexp)/(1+xyrat)."
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
      "lhs": "num_density_unitless",
      "rhs": {
        "op": "*",
        "args": [
          {
            "op": "/",
            "args": [
              {
                "op": "*",
                "args": [
                  "A",
                  "P"
                ]
              },
              {
                "op": "*",
                "args": [
                  "R",
                  "T"
                ]
              }
            ]
          },
          "num_density_unit_inv"
        ]
      }
    },
    {
      "lhs": "alow_k",
      "rhs": {
        "op": "*",
        "args": [
          "a1",
          {
            "op": "exp",
            "args": [
              {
                "op": "/",
                "args": [
                  "c1",
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
              "b1"
            ]
          },
          "c"
        ]
      }
    },
    {
      "lhs": "ahigh_k",
      "rhs": {
        "op": "*",
        "args": [
          "a2",
          {
            "op": "exp",
            "args": [
              {
                "op": "/",
                "args": [
                  "c2",
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
              "b2"
            ]
          },
          "c"
        ]
      }
    },
    {
      "lhs": "rlow",
      "rhs": {
        "op": "*",
        "args": [
          "alow_k",
          "num_density_unitless"
        ]
      }
    },
    {
      "lhs": "xyrat",
      "rhs": {
        "op": "/",
        "args": [
          "rlow",
          "ahigh_k"
        ]
      }
    },
    {
      "lhs": "blog",
      "rhs": {
        "op": "log10",
        "args": [
          "xyrat"
        ]
      }
    },
    {
      "lhs": "fexp",
      "rhs": {
        "op": "/",
        "args": [
          1.0,
          {
            "op": "+",
            "args": [
              1.0,
              {
                "op": "*",
                "args": [
                  "blog",
                  "blog"
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "k",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "*",
            "args": [
              "rlow",
              {
                "op": "^",
                "args": [
                  "fv",
                  "fexp"
                ]
              }
            ]
          },
          {
            "op": "+",
            "args": [
              1.0,
              "xyrat"
            ]
          }
        ]
      }
    }
  ],
  "tests": [
    {
      "id": "default_no2_oh_reaction",
      "description": "All parameters at their defaults: the NO2 + OH --> HNO3 coefficient set (a1=1.8e-30, b1=3.0, c1=0.0, a2=2.8e-11, b2=0.0, c2=0.0, fv=0.6) at T=280 K, P=101325 Pa. Pins all ten cascade variables — the two sub-arrh limits, the falloff ratio xyrat, the Troe exponent fexp and the output k. k asserted at t=0 and t=1 for time-invariance.",
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
          "variable": "num_density_unitless",
          "time": 0.0,
          "expected": 2.620264012509021e+19
        },
        {
          "variable": "alow_k",
          "time": 0.0,
          "expected": 5.801058263845591e-20
        },
        {
          "variable": "ahigh_k",
          "time": 0.0,
          "expected": 0.7336739235025259
        },
        {
          "variable": "rlow",
          "time": 0.0,
          "expected": 1.5200304203222663
        },
        {
          "variable": "xyrat",
          "time": 0.0,
          "expected": 2.071806522801997
        },
        {
          "variable": "blog",
          "time": 0.0,
          "expected": 0.3163491960525565
        },
        {
          "variable": "fexp",
          "time": 0.0,
          "expected": 0.9090274310086746
        },
        {
          "variable": "k",
          "time": 0.0,
          "expected": 0.3110225103483613
        },
        {
          "variable": "k",
          "time": 1.0,
          "expected": 0.3110225103483613
        }
      ]
    },
    {
      "id": "warm_temperature",
      "description": "T raised to 300 K. Both Arrhenius limits and num_density_unitless shift; the falloff ratio xyrat and the broadening fexp move with them. Pins the full recomputed cascade.",
      "parameter_overrides": {
        "arr_3rd.T": 300.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "num_density_unitless",
          "time": 0.0,
          "expected": 2.4455797450084196e+19
        },
        {
          "variable": "alow_k",
          "time": 0.0,
          "expected": 4.402043541015156e-20
        },
        {
          "variable": "ahigh_k",
          "time": 0.0,
          "expected": 0.6847623286023575
        },
        {
          "variable": "rlow",
          "time": 0.0,
          "expected": 1.0765548520551804
        },
        {
          "variable": "xyrat",
          "time": 0.0,
          "expected": 1.5721584075054125
        },
        {
          "variable": "fexp",
          "time": 0.0,
          "expected": 0.9628245758394326
        },
        {
          "variable": "k",
          "time": 0.0,
          "expected": 0.25593932670573394
        }
      ]
    },
    {
      "id": "low_pressure",
      "description": "P lowered to 80000 Pa. num_density_unitless is proportional to P, so the low-pressure branch rlow weakens and the falloff ratio xyrat shifts — the headline pressure dependence of the third-body rate.",
      "parameter_overrides": {
        "arr_3rd.P": 80000.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "num_density_unitless",
          "time": 0.0,
          "expected": 2.0687996151070482e+19
        },
        {
          "variable": "rlow",
          "time": 0.0,
          "expected": 0.9475432206035881
        },
        {
          "variable": "xyrat",
          "time": 0.0,
          "expected": 1.6357712491898322
        },
        {
          "variable": "k",
          "time": 0.0,
          "expected": 0.22056336170821683
        }
      ]
    },
    {
      "id": "falloff_parameter_unity",
      "description": "fv set to 1.0 (no Troe broadening) with all else at defaults. fv enters only as fv^fexp, which becomes 1.0^fexp = 1.0, so k = rlow/(1+xyrat); the sub-arrh limits, rlow, xyrat, blog and fexp are all unchanged from the default test.",
      "parameter_overrides": {
        "arr_3rd.fv": 1.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "xyrat",
          "time": 0.0,
          "expected": 2.071806522801997
        },
        {
          "variable": "fexp",
          "time": 0.0,
          "expected": 0.9090274310086746
        },
        {
          "variable": "k",
          "time": 0.0,
          "expected": 0.4948327341058403
        }
      ]
    }
  ],
  "analyses": [
    {
      "id": "third_body_rate_vs_pressure",
      "description": "Sweeps pressure P from 20000 Pa to 101325 Pa (upper troposphere to surface) with the default NO2+OH coefficients. num_density_unitless is proportional to P, so the low-pressure branch and the falloff ratio xyrat both strengthen with pressure — the defining behaviour of a third-body / falloff rate law.",
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "parameter_sweep": {
        "type": "cartesian",
        "dimensions": [
          {
            "parameter": "P",
            "range": {
              "start": 20000.0,
              "stop": 101325.0,
              "count": 60,
              "scale": "linear"
            }
          }
        ]
      },
      "plots": [
        {
          "id": "third_body_k_vs_p",
          "type": "line",
          "description": "Third-body rate coefficient k versus pressure — k climbs as the low-pressure branch fills in.",
          "x": {
            "variable": "P",
            "label": "Pressure (Pa)"
          },
          "y": {
            "variable": "k",
            "label": "Rate coefficient k (1/(s*ppb))"
          }
        },
        {
          "id": "falloff_ratio_vs_p",
          "type": "line",
          "description": "Falloff ratio xyrat = rlow/rhigh versus pressure, showing the transition between the low- and high-pressure limits.",
          "x": {
            "variable": "P",
            "label": "Pressure (Pa)"
          },
          "y": {
            "variable": "xyrat",
            "label": "Falloff ratio xyrat (dimensionless)"
          }
        }
      ]
    }
  ]
}
```

</details>
