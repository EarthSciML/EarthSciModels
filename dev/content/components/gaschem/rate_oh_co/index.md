---
title: "rate_OH_CO"
slug: "rate_oh_co"
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

_source_ref: GasChem.jl@8c12c048482b515fb8eb2110bf8ab4b4f4e71309:src/SuperFast.jl:142

`rate_OH_CO(t, T, P)` is the SuperFast rate builder for `OH + CO --> HO2` (SuperFast.jl:284), the JPL 15-10 parameterization of the OH+CO reaction. Unlike the other four builders it takes no Arrhenius-coefficient arguments — its inputs are only T and P. The rate is the sum of two pressure-dependent (Troe-style) channels, each combining a low- and high-pressure-limit `arrh` sub-system.

Because the four sub-arrh coefficient sets are hard-coded literals in the upstream function body (not function arguments), they are transcribed here as numeric literals inside the equations rather than as parameters:
  klo1 = arrh(5.9e-33, 1, 0)   khi1 = arrh(1.1e-12, -1.3, 0)
  klo2 = arrh(1.5e-13, 0, 0)   khi2 = arrh(2.1e9,  -6.1, 0)
All four have c0 = 0, so each exp(0.0/T) factor is written verbatim and evaluates to exactly 1.0. The two channels are combined through the upstream Julia locals:
  num_density_unitless = A*P/(R*T)*num_density_unit_inv
  xyrat1 = klo1.k*num_density_unitless/khi1.k ; blog1 = log10(xyrat1)
  fexp1  = 1/(1+blog1*blog1)
  kco1   = klo1.k*num_density_unitless*0.6^fexp1/(1+xyrat1)
  xyrat2 = klo2.k*num_density_unitless/khi2.k ; blog2 = log10(xyrat2)
  fexp2  = 1/(1+blog2*blog2)
  kco2   = klo2.k*0.6^fexp2/(1+xyrat2)
  k      = kco1 + kco2
Note kco2 — unlike kco1 — does NOT carry a num_density_unitless factor; this asymmetry is preserved verbatim from the source. This migration reproduces every upstream-named quantity as a `type: state` cascade variable (air_volume, c, num_density_unitless, the four sub-arrh k's, xyrat1/blog1/fexp1/kco1, xyrat2/blog2/fexp2/kco2 and the output k) — sixteen topologically-ordered equations. The only `type: parameter`s are T, P and the physical constants A/R/ppb_unit/num_density_unit_inv/K_300.

At T=280 K, P=101325 Pa the first channel gives kco1 = 0.0027151547323616947, the second kco2 = 0.0036604066483741124, for k = 0.0063755613807358075 (s*ppb)^-1.

Algebraic, no time derivative. Tolerance rel=1e-10, purely relative — the cascade spans from klo1_k ~ 1.7e-22 to khi2_k ~ 3.6e19, ~41 orders of magnitude, which a single absolute floor could not cover; relative tolerance pins every channel uniformly. 1e-10 is far tighter than any plausible regression yet absorbs the ULP-level noise of the two log10 and two pow calls per channel._

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

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `air_volume` | `cm^3/mol` |  | Molar volume of air, R*T/P. |
| `c` | `molec/(cm^3*ppb)` |  | ppb conversion factor A/air_volume*ppb_unit, shared by all four sub-arrh equations. |
| `num_density_unitless` | `1` |  | Dimensionless air number density A*P/(R*T)*num_density_unit_inv. |
| `klo1_k` | `1/(s*ppb)` |  | Channel-1 low-pressure-limit arrh rate (5.9e-33, 1, 0). |
| `khi1_k` | `1/(s*ppb)` |  | Channel-1 high-pressure-limit arrh rate (1.1e-12, -1.3, 0). |
| `xyrat1` | `1` |  | Channel-1 falloff ratio klo1_k*num_density_unitless/khi1_k. |
| `blog1` | `1` |  | log10 of the channel-1 falloff ratio. |
| `fexp1` | `1` |  | Channel-1 Troe broadening exponent 1/(1+blog1^2). |
| `kco1` | `1/(s*ppb)` |  | Channel-1 rate contribution klo1_k*num_density_unitless*0.6^fexp1/(1+xyrat1). |
| `klo2_k` | `1/(s*ppb)` |  | Channel-2 low-pressure-limit arrh rate (1.5e-13, 0, 0). |
| `khi2_k` | `1/(s*ppb)` |  | Channel-2 high-pressure-limit arrh rate (2.1e9, -6.1, 0). |
| `xyrat2` | `1` |  | Channel-2 falloff ratio klo2_k*num_density_unitless/khi2_k. |
| `blog2` | `1` |  | log10 of the channel-2 falloff ratio. |
| `fexp2` | `1` |  | Channel-2 Troe broadening exponent 1/(1+blog2^2). |
| `kco2` | `1/(s*ppb)` |  | Channel-2 rate contribution klo2_k*0.6^fexp2/(1+xyrat2) (no number-density factor). |
| `k` | `1/(s*ppb)` |  | Total OH+CO rate coefficient kco1 + kco2. |

## Observed expressions

$$
air_{volume} = \frac{R \cdot T}{P}
$$
_Molar volume of air, R*T/P._

$$
c = \frac{A}{air_{volume}} \cdot ppb_{unit}
$$
_ppb conversion factor A/air_volume*ppb_unit, shared by all four sub-arrh equations._

$$
num_{density\,unitless} = \frac{A \cdot P}{R \cdot T} \cdot num_{density\,unit\,inv}
$$
_Dimensionless air number density A*P/(R*T)*num_density_unit_inv._

$$
klo1_{k} = 5.9 \times 10^{-33} \cdot e^{\frac{0.0}{T}} \cdot \frac{K_{300}}{T}^{1.0} \cdot c
$$
_Channel-1 low-pressure-limit arrh rate (5.9e-33, 1, 0)._

$$
khi1_{k} = 1.1 \times 10^{-12} \cdot e^{\frac{0.0}{T}} \cdot \frac{K_{300}}{T}^{-1.3} \cdot c
$$
_Channel-1 high-pressure-limit arrh rate (1.1e-12, -1.3, 0)._

$$
xyrat1 = \frac{klo1_{k} \cdot num_{density\,unitless}}{khi1_{k}}
$$
_Channel-1 falloff ratio klo1_k*num_density_unitless/khi1_k._

$$
blog1 = \log_{10}\left(xyrat1\right)
$$
_log10 of the channel-1 falloff ratio._

$$
fexp1 = \frac{1.0}{1.0 + blog1 \cdot blog1}
$$
_Channel-1 Troe broadening exponent 1/(1+blog1^2)._

$$
kco1 = \frac{klo1_{k} \cdot num_{density\,unitless} \cdot 0.6^{fexp1}}{1.0 + xyrat1}
$$
_Channel-1 rate contribution klo1_k*num_density_unitless*0.6^fexp1/(1+xyrat1)._

$$
klo2_{k} = 1.5 \times 10^{-13} \cdot e^{\frac{0.0}{T}} \cdot \frac{K_{300}}{T}^{0.0} \cdot c
$$
_Channel-2 low-pressure-limit arrh rate (1.5e-13, 0, 0)._

$$
khi2_{k} = 2100000000.0 \cdot e^{\frac{0.0}{T}} \cdot \frac{K_{300}}{T}^{-6.1} \cdot c
$$
_Channel-2 high-pressure-limit arrh rate (2.1e9, -6.1, 0)._

$$
xyrat2 = \frac{klo2_{k} \cdot num_{density\,unitless}}{khi2_{k}}
$$
_Channel-2 falloff ratio klo2_k*num_density_unitless/khi2_k._

$$
blog2 = \log_{10}\left(xyrat2\right)
$$
_log10 of the channel-2 falloff ratio._

$$
fexp2 = \frac{1.0}{1.0 + blog2 \cdot blog2}
$$
_Channel-2 Troe broadening exponent 1/(1+blog2^2)._

$$
kco2 = \frac{klo2_{k} \cdot 0.6^{fexp2}}{1.0 + xyrat2}
$$
_Channel-2 rate contribution klo2_k*0.6^fexp2/(1+xyrat2) (no number-density factor)._

$$
k = kco1 + kco2
$$
_Total OH+CO rate coefficient kco1 + kco2._

## Analyses

### oh_co_rate_vs_pressure

Sweeps pressure P from 20000 Pa to 101325 Pa with T at its default. Both OH+CO channels are pressure-dependent through num_density_unitless; the total rate k = kco1 + kco2 rises with pressure.

**Time span:** 0.0 → 1.0

**Swept over:** `P`

![Total OH + CO rate coefficient k versus pressure.](/plots/gaschem/rate_oh_co/oh_co_rate_vs_pressure-oh_co_k_vs_p.png)

### oh_co_rate_vs_temperature

Sweeps temperature T from 230 K to 320 K with P at its default, showing the weak temperature dependence of the JPL 15-10 OH+CO parameterization.

**Time span:** 0.0 → 1.0

**Swept over:** `T`

![Total OH + CO rate coefficient k versus temperature.](/plots/gaschem/rate_oh_co/oh_co_rate_vs_temperature-oh_co_k_vs_t.png)

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "reference": {
    "notes": "source_ref: GasChem.jl@8c12c048482b515fb8eb2110bf8ab4b4f4e71309:src/SuperFast.jl:142\n\n`rate_OH_CO(t, T, P)` is the SuperFast rate builder for `OH + CO --> HO2` (SuperFast.jl:284), the JPL 15-10 parameterization of the OH+CO reaction. Unlike the other four builders it takes no Arrhenius-coefficient arguments — its inputs are only T and P. The rate is the sum of two pressure-dependent (Troe-style) channels, each combining a low- and high-pressure-limit `arrh` sub-system.\n\nBecause the four sub-arrh coefficient sets are hard-coded literals in the upstream function body (not function arguments), they are transcribed here as numeric literals inside the equations rather than as parameters:\n  klo1 = arrh(5.9e-33, 1, 0)   khi1 = arrh(1.1e-12, -1.3, 0)\n  klo2 = arrh(1.5e-13, 0, 0)   khi2 = arrh(2.1e9,  -6.1, 0)\nAll four have c0 = 0, so each exp(0.0/T) factor is written verbatim and evaluates to exactly 1.0. The two channels are combined through the upstream Julia locals:\n  num_density_unitless = A*P/(R*T)*num_density_unit_inv\n  xyrat1 = klo1.k*num_density_unitless/khi1.k ; blog1 = log10(xyrat1)\n  fexp1  = 1/(1+blog1*blog1)\n  kco1   = klo1.k*num_density_unitless*0.6^fexp1/(1+xyrat1)\n  xyrat2 = klo2.k*num_density_unitless/khi2.k ; blog2 = log10(xyrat2)\n  fexp2  = 1/(1+blog2*blog2)\n  kco2   = klo2.k*0.6^fexp2/(1+xyrat2)\n  k      = kco1 + kco2\nNote kco2 — unlike kco1 — does NOT carry a num_density_unitless factor; this asymmetry is preserved verbatim from the source. This migration reproduces every upstream-named quantity as a `type: state` cascade variable (air_volume, c, num_density_unitless, the four sub-arrh k's, xyrat1/blog1/fexp1/kco1, xyrat2/blog2/fexp2/kco2 and the output k) — sixteen topologically-ordered equations. The only `type: parameter`s are T, P and the physical constants A/R/ppb_unit/num_density_unit_inv/K_300.\n\nAt T=280 K, P=101325 Pa the first channel gives kco1 = 0.0027151547323616947, the second kco2 = 0.0036604066483741124, for k = 0.0063755613807358075 (s*ppb)^-1.\n\nAlgebraic, no time derivative. Tolerance rel=1e-10, purely relative — the cascade spans from klo1_k ~ 1.7e-22 to khi2_k ~ 3.6e19, ~41 orders of magnitude, which a single absolute floor could not cover; relative tolerance pins every channel uniformly. 1e-10 is far tighter than any plausible regression yet absorbs the ULP-level noise of the two log10 and two pow calls per channel."
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
    "air_volume": {
      "type": "unknown",
      "units": "cm^3/mol",
      "description": "Molar volume of air, R*T/P."
    },
    "c": {
      "type": "unknown",
      "units": "molec/(cm^3*ppb)",
      "description": "ppb conversion factor A/air_volume*ppb_unit, shared by all four sub-arrh equations."
    },
    "num_density_unitless": {
      "type": "unknown",
      "units": "1",
      "description": "Dimensionless air number density A*P/(R*T)*num_density_unit_inv."
    },
    "klo1_k": {
      "type": "unknown",
      "units": "1/(s*ppb)",
      "description": "Channel-1 low-pressure-limit arrh rate (5.9e-33, 1, 0)."
    },
    "khi1_k": {
      "type": "unknown",
      "units": "1/(s*ppb)",
      "description": "Channel-1 high-pressure-limit arrh rate (1.1e-12, -1.3, 0)."
    },
    "xyrat1": {
      "type": "unknown",
      "units": "1",
      "description": "Channel-1 falloff ratio klo1_k*num_density_unitless/khi1_k."
    },
    "blog1": {
      "type": "unknown",
      "units": "1",
      "description": "log10 of the channel-1 falloff ratio."
    },
    "fexp1": {
      "type": "unknown",
      "units": "1",
      "description": "Channel-1 Troe broadening exponent 1/(1+blog1^2)."
    },
    "kco1": {
      "type": "unknown",
      "units": "1/(s*ppb)",
      "description": "Channel-1 rate contribution klo1_k*num_density_unitless*0.6^fexp1/(1+xyrat1)."
    },
    "klo2_k": {
      "type": "unknown",
      "units": "1/(s*ppb)",
      "description": "Channel-2 low-pressure-limit arrh rate (1.5e-13, 0, 0)."
    },
    "khi2_k": {
      "type": "unknown",
      "units": "1/(s*ppb)",
      "description": "Channel-2 high-pressure-limit arrh rate (2.1e9, -6.1, 0)."
    },
    "xyrat2": {
      "type": "unknown",
      "units": "1",
      "description": "Channel-2 falloff ratio klo2_k*num_density_unitless/khi2_k."
    },
    "blog2": {
      "type": "unknown",
      "units": "1",
      "description": "log10 of the channel-2 falloff ratio."
    },
    "fexp2": {
      "type": "unknown",
      "units": "1",
      "description": "Channel-2 Troe broadening exponent 1/(1+blog2^2)."
    },
    "kco2": {
      "type": "unknown",
      "units": "1/(s*ppb)",
      "description": "Channel-2 rate contribution klo2_k*0.6^fexp2/(1+xyrat2) (no number-density factor)."
    },
    "k": {
      "type": "unknown",
      "units": "1/(s*ppb)",
      "description": "Total OH+CO rate coefficient kco1 + kco2."
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
      "lhs": "klo1_k",
      "rhs": {
        "op": "*",
        "args": [
          5.9e-33,
          {
            "op": "exp",
            "args": [
              {
                "op": "/",
                "args": [
                  0.0,
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
              1.0
            ]
          },
          "c"
        ]
      }
    },
    {
      "lhs": "khi1_k",
      "rhs": {
        "op": "*",
        "args": [
          1.1e-12,
          {
            "op": "exp",
            "args": [
              {
                "op": "/",
                "args": [
                  0.0,
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
              -1.3
            ]
          },
          "c"
        ]
      }
    },
    {
      "lhs": "xyrat1",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "*",
            "args": [
              "klo1_k",
              "num_density_unitless"
            ]
          },
          "khi1_k"
        ]
      }
    },
    {
      "lhs": "blog1",
      "rhs": {
        "op": "log10",
        "args": [
          "xyrat1"
        ]
      }
    },
    {
      "lhs": "fexp1",
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
                  "blog1",
                  "blog1"
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "kco1",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "*",
            "args": [
              "klo1_k",
              "num_density_unitless",
              {
                "op": "^",
                "args": [
                  0.6,
                  "fexp1"
                ]
              }
            ]
          },
          {
            "op": "+",
            "args": [
              1.0,
              "xyrat1"
            ]
          }
        ]
      }
    },
    {
      "lhs": "klo2_k",
      "rhs": {
        "op": "*",
        "args": [
          1.5e-13,
          {
            "op": "exp",
            "args": [
              {
                "op": "/",
                "args": [
                  0.0,
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
              0.0
            ]
          },
          "c"
        ]
      }
    },
    {
      "lhs": "khi2_k",
      "rhs": {
        "op": "*",
        "args": [
          2100000000.0,
          {
            "op": "exp",
            "args": [
              {
                "op": "/",
                "args": [
                  0.0,
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
              -6.1
            ]
          },
          "c"
        ]
      }
    },
    {
      "lhs": "xyrat2",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "*",
            "args": [
              "klo2_k",
              "num_density_unitless"
            ]
          },
          "khi2_k"
        ]
      }
    },
    {
      "lhs": "blog2",
      "rhs": {
        "op": "log10",
        "args": [
          "xyrat2"
        ]
      }
    },
    {
      "lhs": "fexp2",
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
                  "blog2",
                  "blog2"
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "kco2",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "*",
            "args": [
              "klo2_k",
              {
                "op": "^",
                "args": [
                  0.6,
                  "fexp2"
                ]
              }
            ]
          },
          {
            "op": "+",
            "args": [
              1.0,
              "xyrat2"
            ]
          }
        ]
      }
    },
    {
      "lhs": "k",
      "rhs": {
        "op": "+",
        "args": [
          "kco1",
          "kco2"
        ]
      }
    }
  ],
  "tests": [
    {
      "id": "default_oh_co_reaction",
      "description": "T=280 K, P=101325 Pa — the SuperFast() defaults. rate_OH_CO takes no coefficient arguments (the four sub-arrh coefficient sets are hard-coded JPL 15-10 literals), so this default test pins the entire sixteen-variable cascade for both Troe-style channels and the total rate k = kco1 + kco2 ~ 0.0064 (s*ppb)^-1. k asserted at t=0 and t=1.",
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
          "variable": "klo1_k",
          "time": 0.0,
          "expected": 1.6563811793360597e-22
        },
        {
          "variable": "khi1_k",
          "time": 0.0,
          "expected": 0.026350298961086337
        },
        {
          "variable": "xyrat1",
          "time": 0.0,
          "expected": 0.1647099337135034
        },
        {
          "variable": "blog1",
          "time": 0.0,
          "expected": -0.7832802075888214
        },
        {
          "variable": "fexp1",
          "time": 0.0,
          "expected": 0.6197599745029656
        },
        {
          "variable": "kco1",
          "time": 0.0,
          "expected": 0.0027151547323616947
        },
        {
          "variable": "klo2_k",
          "time": 0.0,
          "expected": 0.003930396018763532
        },
        {
          "variable": "khi2_k",
          "time": 0.0,
          "expected": 3.6123405334999413e+19
        },
        {
          "variable": "xyrat2",
          "time": 0.0,
          "expected": 0.0028509702081981137
        },
        {
          "variable": "blog2",
          "time": 0.0,
          "expected": -2.5450073209166946
        },
        {
          "variable": "fexp2",
          "time": 0.0,
          "expected": 0.13374236628722203
        },
        {
          "variable": "kco2",
          "time": 0.0,
          "expected": 0.0036604066483741124
        },
        {
          "variable": "k",
          "time": 0.0,
          "expected": 0.0063755613807358075
        },
        {
          "variable": "k",
          "time": 1.0,
          "expected": 0.0063755613807358075
        }
      ]
    },
    {
      "id": "warm_temperature",
      "description": "T raised to 300 K. Every sub-arrh limit, num_density_unitless and both falloff ratios shift; pins the recomputed two-channel cascade.",
      "parameter_overrides": {
        "rate_OH_CO.T": 300.0
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
          "variable": "klo1_k",
          "time": 0.0,
          "expected": 1.4428920495549676e-22
        },
        {
          "variable": "khi1_k",
          "time": 0.0,
          "expected": 0.026901377195092616
        },
        {
          "variable": "xyrat1",
          "time": 0.0,
          "expected": 0.13117200450499705
        },
        {
          "variable": "kco1",
          "time": 0.0,
          "expected": 0.0023405990613121035
        },
        {
          "variable": "klo2_k",
          "time": 0.0,
          "expected": 0.0036683696175126295
        },
        {
          "variable": "khi2_k",
          "time": 0.0,
          "expected": 5.135717464517682e+19
        },
        {
          "variable": "xyrat2",
          "time": 0.0,
          "expected": 0.0017468426750060137
        },
        {
          "variable": "kco2",
          "time": 0.0,
          "expected": 0.0034509146663411045
        },
        {
          "variable": "k",
          "time": 0.0,
          "expected": 0.005791513727653208
        }
      ]
    },
    {
      "id": "low_pressure",
      "description": "P lowered to 80000 Pa. num_density_unitless scales with P, shifting both pressure-dependent channels and lowering the total OH+CO rate.",
      "parameter_overrides": {
        "rate_OH_CO.P": 80000.0
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
          "variable": "xyrat1",
          "time": 0.0,
          "expected": 0.13004485267288696
        },
        {
          "variable": "kco1",
          "time": 0.0,
          "expected": 0.001798289544833046
        },
        {
          "variable": "xyrat2",
          "time": 0.0,
          "expected": 0.0022509510649479304
        },
        {
          "variable": "kco2",
          "time": 0.0,
          "expected": 0.002904936319144779
        },
        {
          "variable": "k",
          "time": 0.0,
          "expected": 0.004703225863977825
        }
      ]
    }
  ],
  "analyses": [
    {
      "id": "oh_co_rate_vs_pressure",
      "description": "Sweeps pressure P from 20000 Pa to 101325 Pa with T at its default. Both OH+CO channels are pressure-dependent through num_density_unitless; the total rate k = kco1 + kco2 rises with pressure.",
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
          "id": "oh_co_k_vs_p",
          "type": "line",
          "description": "Total OH + CO rate coefficient k versus pressure.",
          "x": {
            "variable": "P",
            "label": "Pressure (Pa)"
          },
          "y": {
            "variable": "k",
            "label": "Rate coefficient k (1/(s*ppb))"
          }
        }
      ]
    },
    {
      "id": "oh_co_rate_vs_temperature",
      "description": "Sweeps temperature T from 230 K to 320 K with P at its default, showing the weak temperature dependence of the JPL 15-10 OH+CO parameterization.",
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
          "id": "oh_co_k_vs_t",
          "type": "line",
          "description": "Total OH + CO rate coefficient k versus temperature.",
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
