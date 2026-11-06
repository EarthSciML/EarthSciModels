---
title: "rate_2HO2"
slug: "rate_2ho2"
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

_source_ref: GasChem.jl@8c12c048482b515fb8eb2110bf8ab4b4f4e71309:src/SuperFast.jl:102

`rate_2HO2(t, T, P, H2O, a0, c0, a1, c1)` is the SuperFast rate builder for `HO2 + HO2 --> H2O2 + O2` (SuperFast.jl:278). It sums a bimolecular channel and a termolecular (number-density-scaled) channel and multiplies by a water-vapour enhancement factor.

Upstream it composes two b0=0 `arrh` sub-systems (`k0`, `k1`) and uses the Julia locals num_density_unitless and H2O_ppb_molec_cm3:
  num_density_unitless = A*P/(R*T)*num_density_unit_inv
  H2O_ppb_molec_cm3    = H2O*ppb_inv*1.0e-9*num_density_unitless
  k0.k = arrh(a0,0.0,c0) ; k1.k = arrh(a1,0.0,c1)
  k    = (k0.k + k1.k*num_density_unitless)
         * (1 + 1.4e-21*H2O*H2O_ppb_molec_cm3*exp(T_0/T))
That upstream line multiplies by H2O twice: once as the raw ppb value and once inside H2O_ppb_molec_cm3, which is already the water number density (molec/cm^3, unit-stripped). The JPL water-vapour enhancement of HO2 + HO2 is 1 + 1.4e-21*[H2O]*exp(2200/T) with [H2O] in molec/cm^3 (the JPL kinetics evaluation, e.g. Burkholder et al. 2019, JPL Publication 19-5, HO2 + HO2 entry), so here the term is 1 + 1.4e-21*H2O_ppb_molec_cm3*exp(T_0/T). With the doubled factor the enhancement at the defaults is ~3.2e7, a rate seven orders of magnitude too fast; with the JPL form it is 2.74.

This migration reproduces each named quantity as a `type: state` cascade variable: air_volume, c, num_density_unitless, H2O_ppb_molec_cm3, the two sub-arrh outputs k0_k and k1_k, and the output k — seven equations. Both sub-arrh calls fix b0=0, so the (K_300/T)^0.0 factor is written verbatim and evaluates to exactly 1.0.

Defaults H2O=1.839e7 ppb (the SuperFast() `@parameters H2O` default, SuperFast.jl:254), a0=3.0e-13, c0=460.0, a1=2.1e-33, c1=920.0 (the HO2+HO2 coefficient set, SuperFast.jl:278). At T=280 K, P=101325 Pa the water-enhancement factor is 2.7433, so k = 0.2172039948232169 (s*ppb)^-1; with H2O=0 the factor collapses to exactly 1.0 and k = 0.07917658137395685 (the bare k0_k + k1_k*num_density_unitless sum). The h2o_zero test pins both that k and H2O_ppb_molec_cm3 = 0.0 exactly.

Algebraic, no time derivative. Tolerance rel=1e-10, purely relative: relative tolerance handles the orders-of-magnitude spread between the small k1_k channel and k. The single exact-zero assertion (H2O_ppb_molec_cm3 at H2O=0) is bit-exactly 0.0 because 0.0*x = 0.0 in IEEE-754, so it passes the runner's exact-match path with no abs floor required._

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `T` | `K` | `280.0` | Air temperature. Upstream the rate-law builders receive T as a `ParentScope` parameter; the default 280.0 K is the SuperFast() `@parameters T` default (SuperFast.jl:250). |
| `P` | `Pa` | `101325.0` | Air pressure. Upstream a `ParentScope` parameter; the default 101325 Pa (1 atm) is the SuperFast() `@parameters P` default (SuperFast.jl:251). |
| `A` | `molec/mol` | `6.02e+23` | Avogadro's number. Upstream `@constants A = 6.02e23` (SuperFast.jl). Appears in the ppb conversion factor c = A/air_volume*ppb_unit. |
| `R` | `(Pa*cm^3)/(K*mol)` | `8314000.0` | Universal gas constant in the upstream's mixed Pa-cm^3 unit system. Upstream `@constants R = 8.314e6`. Sets the molar air volume air_volume = R*T/P. |
| `ppb_unit` | `1/ppb` | `1e-09` | mol/mol_air per ppb: 1 ppb is 1e-9 mol/mol, so the factor is 1e-9 with units 1/ppb, and c = A/air_volume*ppb_unit carries molec/(cm^3*ppb). Upstream `@constants ppb_unit = 1.0e-9` declares the unit as `ppb`, the exponent the wrong way round (the value is unchanged). |
| `num_density_unit_inv` | `cm^3/molec` | `1.0` | Unit-stripping factor that turns the air number density into the dimensionless num_density_unitless. Upstream `@constants num_density_unit_inv = 1`. |
| `ppb_inv` | `1/ppb` | `1.0` | Unit-stripping factor (ppb^-1). Upstream `@constants ppb_inv = 1`. |
| `K_300` | `K` | `300.0` | Arrhenius reference temperature (300 K). Upstream `@constants K_300 = 300`. |
| `T_0` | `K` | `2200.0` | Characteristic temperature of the HO2+HO2 water-vapour enhancement term. Upstream `@constants T_0 = 2200.0`. |
| `H2O` | `ppb` | `18390000.0` | Water-vapour mixing ratio in ppb. Default 1.839e7 ppb (~1.8%) is the SuperFast() `@parameters H2O` default (SuperFast.jl:254). |
| `a0` | `cm^3/molec/s` | `3e-13` | Bimolecular-channel Arrhenius pre-exponential. Default 3.0e-13 from `HO2 + HO2 --> H2O2 + O2` (SuperFast.jl:278). |
| `c0` | `K` | `460.0` | Bimolecular-channel activation-temperature parameter. Default 460.0. |
| `a1` | `cm^3/molec/s` | `2.1e-33` | Termolecular-channel Arrhenius pre-exponential. Default 2.1e-33 from `HO2 + HO2 --> H2O2 + O2`. |
| `c1` | `K` | `920.0` | Termolecular-channel activation-temperature parameter. Default 920.0. |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `air_volume` | `cm^3/mol` |  | Molar volume of air, R*T/P. |
| `c` | `molec/(cm^3*ppb)` |  | ppb conversion factor A/air_volume*ppb_unit. |
| `num_density_unitless` | `1` |  | Dimensionless air number density A*P/(R*T)*num_density_unit_inv. |
| `H2O_ppb_molec_cm3` | `1` |  | Water-vapour concentration converted from ppb toward a molec/cm^3 number density, H2O*ppb_inv*1.0e-9*num_density_unitless. |
| `k0_k` | `1/(s*ppb)` |  | Bimolecular HO2+HO2 channel (arrh with a0,0,c0). |
| `k1_k` | `1/(s*ppb)` |  | Termolecular HO2+HO2 channel base rate (arrh with a1,0,c1), scaled by num_density_unitless in k. |
| `k` | `1/(s*ppb)` |  | HO2+HO2 rate coefficient including the water-vapour enhancement factor. |

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
num_{density\,unitless} = \frac{A \cdot P}{R \cdot T} \cdot num_{density\,unit\,inv}
$$
_Dimensionless air number density A*P/(R*T)*num_density_unit_inv._

$$
H2O_{ppb\,molec\,cm3} = H2O \cdot ppb_{inv} \cdot 1 \times 10^{-9} \cdot num_{density\,unitless}
$$
_Water-vapour concentration converted from ppb toward a molec/cm^3 number density, H2O*ppb_inv*1.0e-9*num_density_unitless._

$$
k0_{k} = a0 \cdot e^{\frac{c0}{T}} \cdot \frac{K_{300}}{T}^{0.0} \cdot c
$$
_Bimolecular HO2+HO2 channel (arrh with a0,0,c0)._

$$
k1_{k} = a1 \cdot e^{\frac{c1}{T}} \cdot \frac{K_{300}}{T}^{0.0} \cdot c
$$
_Termolecular HO2+HO2 channel base rate (arrh with a1,0,c1), scaled by num_density_unitless in k._

$$
k = \left(k0_{k} + k1_{k} \cdot num_{density\,unitless}\right) \cdot \left(1.0 + 1.4 \times 10^{-21} \cdot H2O_{ppb\,molec\,cm3} \cdot e^{\frac{T_{0}}{T}}\right)
$$
_HO2+HO2 rate coefficient including the water-vapour enhancement factor._

## Analyses

### ho2_rate_vs_water_vapour

Sweeps the water-vapour mixing ratio H2O from 0 to 3.678e7 ppb (dry air to twice the SuperFast default ~1.8%) with T and P at defaults. The HO2+HO2 rate carries a water-enhancement factor 1 + 1.4e-21*H2O_ppb_molec_cm3*exp(T_0/T); since H2O_ppb_molec_cm3 is linear in H2O, k grows linearly in water vapour.

**Time span:** 0.0 → 1.0

**Swept over:** `H2O`

![HO2+HO2 rate coefficient k versus water-vapour mixing ratio — a linear rise driven by the water-enhancement factor.](/plots/gaschem/rate_2ho2/ho2_rate_vs_water_vapour-ho2_k_vs_h2o.png)

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "reference": {
    "notes": "source_ref: GasChem.jl@8c12c048482b515fb8eb2110bf8ab4b4f4e71309:src/SuperFast.jl:102\n\n`rate_2HO2(t, T, P, H2O, a0, c0, a1, c1)` is the SuperFast rate builder for `HO2 + HO2 --> H2O2 + O2` (SuperFast.jl:278). It sums a bimolecular channel and a termolecular (number-density-scaled) channel and multiplies by a water-vapour enhancement factor.\n\nUpstream it composes two b0=0 `arrh` sub-systems (`k0`, `k1`) and uses the Julia locals num_density_unitless and H2O_ppb_molec_cm3:\n  num_density_unitless = A*P/(R*T)*num_density_unit_inv\n  H2O_ppb_molec_cm3    = H2O*ppb_inv*1.0e-9*num_density_unitless\n  k0.k = arrh(a0,0.0,c0) ; k1.k = arrh(a1,0.0,c1)\n  k    = (k0.k + k1.k*num_density_unitless)\n         * (1 + 1.4e-21*H2O*H2O_ppb_molec_cm3*exp(T_0/T))\nThat upstream line multiplies by H2O twice: once as the raw ppb value and once inside H2O_ppb_molec_cm3, which is already the water number density (molec/cm^3, unit-stripped). The JPL water-vapour enhancement of HO2 + HO2 is 1 + 1.4e-21*[H2O]*exp(2200/T) with [H2O] in molec/cm^3 (the JPL kinetics evaluation, e.g. Burkholder et al. 2019, JPL Publication 19-5, HO2 + HO2 entry), so here the term is 1 + 1.4e-21*H2O_ppb_molec_cm3*exp(T_0/T). With the doubled factor the enhancement at the defaults is ~3.2e7, a rate seven orders of magnitude too fast; with the JPL form it is 2.74.\n\nThis migration reproduces each named quantity as a `type: state` cascade variable: air_volume, c, num_density_unitless, H2O_ppb_molec_cm3, the two sub-arrh outputs k0_k and k1_k, and the output k — seven equations. Both sub-arrh calls fix b0=0, so the (K_300/T)^0.0 factor is written verbatim and evaluates to exactly 1.0.\n\nDefaults H2O=1.839e7 ppb (the SuperFast() `@parameters H2O` default, SuperFast.jl:254), a0=3.0e-13, c0=460.0, a1=2.1e-33, c1=920.0 (the HO2+HO2 coefficient set, SuperFast.jl:278). At T=280 K, P=101325 Pa the water-enhancement factor is 2.7433, so k = 0.2172039948232169 (s*ppb)^-1; with H2O=0 the factor collapses to exactly 1.0 and k = 0.07917658137395685 (the bare k0_k + k1_k*num_density_unitless sum). The h2o_zero test pins both that k and H2O_ppb_molec_cm3 = 0.0 exactly.\n\nAlgebraic, no time derivative. Tolerance rel=1e-10, purely relative: relative tolerance handles the orders-of-magnitude spread between the small k1_k channel and k. The single exact-zero assertion (H2O_ppb_molec_cm3 at H2O=0) is bit-exactly 0.0 because 0.0*x = 0.0 in IEEE-754, so it passes the runner's exact-match path with no abs floor required."
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
    "ppb_inv": {
      "type": "parameter",
      "units": "1/ppb",
      "default": 1.0,
      "description": "Unit-stripping factor (ppb^-1). Upstream `@constants ppb_inv = 1`."
    },
    "K_300": {
      "type": "parameter",
      "units": "K",
      "default": 300.0,
      "description": "Arrhenius reference temperature (300 K). Upstream `@constants K_300 = 300`."
    },
    "T_0": {
      "type": "parameter",
      "units": "K",
      "default": 2200.0,
      "description": "Characteristic temperature of the HO2+HO2 water-vapour enhancement term. Upstream `@constants T_0 = 2200.0`."
    },
    "H2O": {
      "type": "parameter",
      "units": "ppb",
      "default": 18390000.0,
      "description": "Water-vapour mixing ratio in ppb. Default 1.839e7 ppb (~1.8%) is the SuperFast() `@parameters H2O` default (SuperFast.jl:254)."
    },
    "a0": {
      "type": "parameter",
      "units": "cm^3/molec/s",
      "default": 3e-13,
      "description": "Bimolecular-channel Arrhenius pre-exponential. Default 3.0e-13 from `HO2 + HO2 --> H2O2 + O2` (SuperFast.jl:278)."
    },
    "c0": {
      "type": "parameter",
      "units": "K",
      "default": 460.0,
      "description": "Bimolecular-channel activation-temperature parameter. Default 460.0."
    },
    "a1": {
      "type": "parameter",
      "units": "cm^3/molec/s",
      "default": 2.1e-33,
      "description": "Termolecular-channel Arrhenius pre-exponential. Default 2.1e-33 from `HO2 + HO2 --> H2O2 + O2`."
    },
    "c1": {
      "type": "parameter",
      "units": "K",
      "default": 920.0,
      "description": "Termolecular-channel activation-temperature parameter. Default 920.0."
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
    "num_density_unitless": {
      "type": "unknown",
      "units": "1",
      "description": "Dimensionless air number density A*P/(R*T)*num_density_unit_inv."
    },
    "H2O_ppb_molec_cm3": {
      "type": "unknown",
      "units": "1",
      "description": "Water-vapour concentration converted from ppb toward a molec/cm^3 number density, H2O*ppb_inv*1.0e-9*num_density_unitless."
    },
    "k0_k": {
      "type": "unknown",
      "units": "1/(s*ppb)",
      "description": "Bimolecular HO2+HO2 channel (arrh with a0,0,c0)."
    },
    "k1_k": {
      "type": "unknown",
      "units": "1/(s*ppb)",
      "description": "Termolecular HO2+HO2 channel base rate (arrh with a1,0,c1), scaled by num_density_unitless in k."
    },
    "k": {
      "type": "unknown",
      "units": "1/(s*ppb)",
      "description": "HO2+HO2 rate coefficient including the water-vapour enhancement factor."
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
      "lhs": "H2O_ppb_molec_cm3",
      "rhs": {
        "op": "*",
        "args": [
          "H2O",
          "ppb_inv",
          1e-09,
          "num_density_unitless"
        ]
      }
    },
    {
      "lhs": "k0_k",
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
              0.0
            ]
          },
          "c"
        ]
      }
    },
    {
      "lhs": "k1_k",
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
              0.0
            ]
          },
          "c"
        ]
      }
    },
    {
      "lhs": "k",
      "rhs": {
        "op": "*",
        "args": [
          {
            "op": "+",
            "args": [
              "k0_k",
              {
                "op": "*",
                "args": [
                  "k1_k",
                  "num_density_unitless"
                ]
              }
            ]
          },
          {
            "op": "+",
            "args": [
              1.0,
              {
                "op": "*",
                "args": [
                  1.4e-21,
                  "H2O_ppb_molec_cm3",
                  {
                    "op": "exp",
                    "args": [
                      {
                        "op": "/",
                        "args": [
                          "T_0",
                          "T"
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
      "id": "default_ho2_ho2_reaction",
      "description": "All parameters at their defaults: H2O=1.839e7 ppb, a0=3.0e-13, c0=460.0, a1=2.1e-33, c1=920.0 (the HO2 + HO2 --> H2O2 + O2 coefficient set) at T=280 K, P=101325 Pa. The water-vapour enhancement factor 1 + 1.4e-21*[H2O]*exp(2200/T) is 2.74, so k = 0.2172 (s*ppb)^-1. Pins all seven cascade variables; k asserted at t=0 and t=1 for time-invariance.",
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
          "variable": "H2O_ppb_molec_cm3",
          "time": 0.0,
          "expected": 4.8186655190040896e+17
        },
        {
          "variable": "k0_k",
          "time": 0.0,
          "expected": 0.04063966305858998
        },
        {
          "variable": "k1_k",
          "time": 0.0,
          "expected": 1.4707265424931754e-21
        },
        {
          "variable": "k",
          "time": 0.0,
          "expected": 0.2172039948232169
        },
        {
          "variable": "k",
          "time": 1.0,
          "expected": 0.2172039948232169
        }
      ]
    },
    {
      "id": "dry_air_no_water_enhancement",
      "description": "H2O set to 0.0. H2O_ppb_molec_cm3 becomes exactly 0.0 (0.0*x=0.0 in IEEE-754) and the water-enhancement factor collapses to exactly 1.0, so k reduces to the bare two-channel sum k0_k + k1_k*num_density_unitless ~ 0.079 (s*ppb)^-1. Isolates the non-water part of the rate law.",
      "parameter_overrides": {
        "rate_2HO2.H2O": 0.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "H2O_ppb_molec_cm3",
          "time": 0.0,
          "expected": 0.0
        },
        {
          "variable": "k0_k",
          "time": 0.0,
          "expected": 0.04063966305858998
        },
        {
          "variable": "k1_k",
          "time": 0.0,
          "expected": 1.4707265424931754e-21
        },
        {
          "variable": "k",
          "time": 0.0,
          "expected": 0.07917658137395685
        }
      ]
    },
    {
      "id": "doubled_water_vapour",
      "description": "H2O doubled to 3.678e7 ppb. The enhancement term is linear in the water number density H2O_ppb_molec_cm3, so the excess over 1 doubles: factor 1 + 2*1.7433 = 4.487, k = 0.3552 (s*ppb)^-1.",
      "parameter_overrides": {
        "rate_2HO2.H2O": 36780000.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "H2O_ppb_molec_cm3",
          "time": 0.0,
          "expected": 9.637331038008179e+17
        },
        {
          "variable": "k",
          "time": 0.0,
          "expected": 0.35523140827247696
        }
      ]
    },
    {
      "id": "warm_temperature",
      "description": "T raised to 300 K with H2O at default. The exp(T_0/T) term in the water enhancement weakens as T rises (T_0=2200 K), and both sub-arrh channels and num_density_unitless shift; pins the recomputed cascade.",
      "parameter_overrides": {
        "rate_2HO2.T": 300.0
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
          "variable": "H2O_ppb_molec_cm3",
          "time": 0.0,
          "expected": 4.497421151070484e+17
        },
        {
          "variable": "k0_k",
          "time": 0.0,
          "expected": 0.03399548872805895
        },
        {
          "variable": "k1_k",
          "time": 0.0,
          "expected": 1.1026496264711838e-21
        },
        {
          "variable": "k",
          "time": 0.0,
          "expected": 0.11970716564289985
        }
      ]
    }
  ],
  "analyses": [
    {
      "id": "ho2_rate_vs_water_vapour",
      "description": "Sweeps the water-vapour mixing ratio H2O from 0 to 3.678e7 ppb (dry air to twice the SuperFast default ~1.8%) with T and P at defaults. The HO2+HO2 rate carries a water-enhancement factor 1 + 1.4e-21*H2O_ppb_molec_cm3*exp(T_0/T); since H2O_ppb_molec_cm3 is linear in H2O, k grows linearly in water vapour.",
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "parameter_sweep": {
        "type": "cartesian",
        "dimensions": [
          {
            "parameter": "H2O",
            "range": {
              "start": 0.0,
              "stop": 36780000.0,
              "count": 60,
              "scale": "linear"
            }
          }
        ]
      },
      "plots": [
        {
          "id": "ho2_k_vs_h2o",
          "type": "line",
          "description": "HO2+HO2 rate coefficient k versus water-vapour mixing ratio — a linear rise driven by the water-enhancement factor.",
          "x": {
            "variable": "H2O",
            "label": "Water vapour (ppb)"
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
