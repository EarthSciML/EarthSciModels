---
title: "rate_ISO2"
slug: "rate_iso2"
domains: ["gaschem"]
component_types: ["model"]
domain: "gaschem"
component_type: "model"
esm_version: "1.0.0"
esm_path: "components/gaschem/geoschem_ratelaws.esm"
reference: "https://github.com/geoschem/geos-chem"
description: "GEOS-Chem gas-phase reaction rate laws — the 37 rate-coefficient builder functions of GasChem.jl src/geoschem_ratelaws.jl, adapted from the GEOS-Chem KPP/fullchem mechanism (github.com/geoschem/geos-chem, commit 4722f288). Each builder computes a single reaction rate coefficient k from temperature and air number density: constant rates (constant_k, constant_k_1), modified-Arrhenius forms in ppb and SI molecular units (arrhenius_ppb, arrhenius_ppb_3, arrhenius_mlc_SI, arrhenius_mlc_1, arrplus_*, tunplus_*), Troe / third-body pressure-dependent falloff rates (arr_3rdbody, arr_3rdbody_1, rate_OHCO, rate_PAN_abab, rate_PAN_acac, eq_const, eq_const_1), and a family of mechanism-specific rates for HO2, RO2+NO, isoprene, glycolaldehyde, DMS and HNO3 chemistry. Each rate law is migrated as an independent purely-algebraic model: the inputs (T, num_density, Arrhenius coefficients) are parameters, the rate coefficient k is the single state variable defined by one algebraic equation, and an inline test reproduces the rate constant asserted by the corresponding @testitem in GasChem.jl test/geoschem_ratelaws_test.jl (compiled at T=293 K, num_density = 2.7e19 molec/cm^3). The GEOS-Chem license applies (github.com/geoschem/geos-chem/blob/main/LICENSE.txt)."
tags: ["gaschem", "model", "geoschem", "rate-laws", "reaction-kinetics", "arrhenius", "troposphere-chemistry", "observed-only"]
---

## Description

GEOS-Chem gas-phase reaction rate laws — the 37 rate-coefficient builder functions of GasChem.jl src/geoschem_ratelaws.jl, adapted from the GEOS-Chem KPP/fullchem mechanism (github.com/geoschem/geos-chem, commit 4722f288). Each builder computes a single reaction rate coefficient k from temperature and air number density: constant rates (constant_k, constant_k_1), modified-Arrhenius forms in ppb and SI molecular units (arrhenius_ppb, arrhenius_ppb_3, arrhenius_mlc_SI, arrhenius_mlc_1, arrplus_*, tunplus_*), Troe / third-body pressure-dependent falloff rates (arr_3rdbody, arr_3rdbody_1, rate_OHCO, rate_PAN_abab, rate_PAN_acac, eq_const, eq_const_1), and a family of mechanism-specific rates for HO2, RO2+NO, isoprene, glycolaldehyde, DMS and HNO3 chemistry. Each rate law is migrated as an independent purely-algebraic model: the inputs (T, num_density, Arrhenius coefficients) are parameters, the rate coefficient k is the single state variable defined by one algebraic equation, and an inline test reproduces the rate constant asserted by the corresponding @testitem in GasChem.jl test/geoschem_ratelaws_test.jl (compiled at T=293 K, num_density = 2.7e19 molec/cm^3). The GEOS-Chem license applies (github.com/geoschem/geos-chem/blob/main/LICENSE.txt).

## Reference

_source_ref: GasChem.jl@8c12c048482b515fb8eb2110bf8ab4b4f4e71309:src/geoschem_ratelaws.jl:993 (`rate_ISO2` rate-law builder function).

Rate law for the ISOP + OH channel forming HPALD / fragmentation products: k = a0*exp(b0/T)*k2 * C, where k2 is the same tunnelling-modulated branching term as rate_ISO1 (this is its complement channel).

Migration shape: the upstream `rate_ISO2` returns a Catalyst `ReactionSystem` carrying zero reactions and one variable k(t) bound by a single algebraic equation k ~ <rate expression> (the @constants in the source are MTK unit-bookkeeping; their numeric values N_A=6.02214076e23, cm3_m3=1.0e6, ppb_unit=1.0e-9, k_unit_inv=1.0e6 are folded into the .esm expression AST as literals). It is migrated here as a purely-algebraic `model`: the rate-law inputs (T, num_density, Arrhenius coefficients) are `type: parameter`, the output k is the single `type: state` variable, and `equations` holds the one defining equation. No equation carries a D(.) operator, so the trajectory is constant in time and the inline test samples at t=0 (the observed-only convention of sibling files multiple_removal.esm / ope.esm).

Units: variables carry no `units` field — the rate expression folds the upstream MTK unit conversions into numeric literals, so every quantity is nominally dimensionless to the structural validator. This is the convention of the sibling GEOS-Chem file geoschem_fullchem.esm; physical units are documented in prose in each variable's `description`.

Tolerance rationale (model-level rel=1e-8 / abs=1e-30): the rate law is a single closed-form algebraic expression evaluated once (no time integration, no stiff dynamics). rel=1e-8 sits at the upstream Julia approximate-equality default (`approx` uses rtol=sqrt(eps(Float64))=~1.49e-8) and comfortably absorbs the libm exp / ^ / log10 rounding differences between the Julia reference values and the Python ESS runner; abs=1e-30 is a near-zero floor that gates no assertion here (the smallest pinned rate constant across the file is eq_const k=~2.1e-27).

Upstream test reproduction: the inline test `upstream_rate_ISO2` pins k at the parameter defaults to the value asserted by the `@testitem "rate_ISO2"` block in GasChem.jl test/geoschem_ratelaws_test.jl, which compiles the rate law at T=293.0 K and num_density=2.7e19/N_A*cm3_m3 mol/m^3 and checks the resulting rate constant k._

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `T` |  | `293.0` | Air temperature (K). Default 293.0 K is the scenario temperature of the upstream geoschem_ratelaws_test.jl `RateLawSetup` test snippet. |
| `num_density` |  | `44.834554813693856` | Number density of air (mol/m^3). Default 44.834554813693856 mol/m^3 equals 2.7e19 molec/cm^3 — the upstream test value 2.7e19/N_A*cm3_m3 (N_A = 6.02214076e23, cm3_m3 = 1.0e6). |
| `a0` |  | `1e-11` | Overall ISOP + OH pre-exponential. |
| `b0` |  | `390.0` | Overall ISOP + OH temperature term. [K] |
| `c0` |  | `0.3` | Branching-term scale factor. |
| `d0` |  | `1.0` | k0 pre-exponential of the branching term. |
| `e0` |  | `380.0` | k0 temperature term of the branching term. [K] |
| `f0` |  | `1.0` | k1 pre-exponential of the branching term. |
| `g0` |  | `380.0` | k1 temperature term of the branching term. [K] |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `k` |  |  | Reaction rate coefficient produced by the rate_ISO2 rate law, output in ppb^-1*s^-1. Defined by one algebraic equation; the system carries no time derivative. |

## Observed expressions

$$
k = a0 \cdot e^{\frac{b0}{T}} \cdot \frac{c0 \cdot d0 \cdot e^{\frac{e0}{T}} \cdot e^{\frac{100000000.0}{T^{3.0}}}}{d0 \cdot e^{\frac{e0}{T}} \cdot e^{\frac{100000000.0}{T^{3.0}}} + f0 \cdot e^{\frac{g0}{T}}} \cdot num_{density} \cdot 1 \times 10^{-9} \cdot 6.02214076 \times 10^{17}
$$
_Reaction rate coefficient produced by the rate_ISO2 rate law, output in ppb^-1*s^-1. Defined by one algebraic equation; the system carries no time derivative._

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "reference": {
    "notes": "source_ref: GasChem.jl@8c12c048482b515fb8eb2110bf8ab4b4f4e71309:src/geoschem_ratelaws.jl:993 (`rate_ISO2` rate-law builder function).\n\nRate law for the ISOP + OH channel forming HPALD / fragmentation products: k = a0*exp(b0/T)*k2 * C, where k2 is the same tunnelling-modulated branching term as rate_ISO1 (this is its complement channel).\n\nMigration shape: the upstream `rate_ISO2` returns a Catalyst `ReactionSystem` carrying zero reactions and one variable k(t) bound by a single algebraic equation k ~ <rate expression> (the @constants in the source are MTK unit-bookkeeping; their numeric values N_A=6.02214076e23, cm3_m3=1.0e6, ppb_unit=1.0e-9, k_unit_inv=1.0e6 are folded into the .esm expression AST as literals). It is migrated here as a purely-algebraic `model`: the rate-law inputs (T, num_density, Arrhenius coefficients) are `type: parameter`, the output k is the single `type: state` variable, and `equations` holds the one defining equation. No equation carries a D(.) operator, so the trajectory is constant in time and the inline test samples at t=0 (the observed-only convention of sibling files multiple_removal.esm / ope.esm).\n\nUnits: variables carry no `units` field — the rate expression folds the upstream MTK unit conversions into numeric literals, so every quantity is nominally dimensionless to the structural validator. This is the convention of the sibling GEOS-Chem file geoschem_fullchem.esm; physical units are documented in prose in each variable's `description`.\n\nTolerance rationale (model-level rel=1e-8 / abs=1e-30): the rate law is a single closed-form algebraic expression evaluated once (no time integration, no stiff dynamics). rel=1e-8 sits at the upstream Julia approximate-equality default (`approx` uses rtol=sqrt(eps(Float64))=~1.49e-8) and comfortably absorbs the libm exp / ^ / log10 rounding differences between the Julia reference values and the Python ESS runner; abs=1e-30 is a near-zero floor that gates no assertion here (the smallest pinned rate constant across the file is eq_const k=~2.1e-27).\n\nUpstream test reproduction: the inline test `upstream_rate_ISO2` pins k at the parameter defaults to the value asserted by the `@testitem \"rate_ISO2\"` block in GasChem.jl test/geoschem_ratelaws_test.jl, which compiles the rate law at T=293.0 K and num_density=2.7e19/N_A*cm3_m3 mol/m^3 and checks the resulting rate constant k."
  },
  "tolerance": {
    "rel": 1e-08,
    "abs": 1e-30
  },
  "variables": {
    "T": {
      "type": "parameter",
      "default": 293.0,
      "description": "Air temperature (K). Default 293.0 K is the scenario temperature of the upstream geoschem_ratelaws_test.jl `RateLawSetup` test snippet."
    },
    "num_density": {
      "type": "parameter",
      "default": 44.834554813693856,
      "description": "Number density of air (mol/m^3). Default 44.834554813693856 mol/m^3 equals 2.7e19 molec/cm^3 — the upstream test value 2.7e19/N_A*cm3_m3 (N_A = 6.02214076e23, cm3_m3 = 1.0e6)."
    },
    "a0": {
      "type": "parameter",
      "default": 1e-11,
      "description": "Overall ISOP + OH pre-exponential."
    },
    "b0": {
      "type": "parameter",
      "default": 390.0,
      "description": "Overall ISOP + OH temperature term. [K]"
    },
    "c0": {
      "type": "parameter",
      "default": 0.3,
      "description": "Branching-term scale factor."
    },
    "d0": {
      "type": "parameter",
      "default": 1.0,
      "description": "k0 pre-exponential of the branching term."
    },
    "e0": {
      "type": "parameter",
      "default": 380.0,
      "description": "k0 temperature term of the branching term. [K]"
    },
    "f0": {
      "type": "parameter",
      "default": 1.0,
      "description": "k1 pre-exponential of the branching term."
    },
    "g0": {
      "type": "parameter",
      "default": 380.0,
      "description": "k1 temperature term of the branching term. [K]"
    },
    "k": {
      "type": "unknown",
      "description": "Reaction rate coefficient produced by the rate_ISO2 rate law, output in ppb^-1*s^-1. Defined by one algebraic equation; the system carries no time derivative."
    }
  },
  "equations": [
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
                  "b0",
                  "T"
                ]
              }
            ]
          },
          {
            "op": "/",
            "args": [
              {
                "op": "*",
                "args": [
                  "c0",
                  {
                    "op": "*",
                    "args": [
                      "d0",
                      {
                        "op": "exp",
                        "args": [
                          {
                            "op": "/",
                            "args": [
                              "e0",
                              "T"
                            ]
                          }
                        ]
                      },
                      {
                        "op": "exp",
                        "args": [
                          {
                            "op": "/",
                            "args": [
                              100000000.0,
                              {
                                "op": "^",
                                "args": [
                                  "T",
                                  3.0
                                ]
                              }
                            ]
                          }
                        ]
                      }
                    ]
                  }
                ]
              },
              {
                "op": "+",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      "d0",
                      {
                        "op": "exp",
                        "args": [
                          {
                            "op": "/",
                            "args": [
                              "e0",
                              "T"
                            ]
                          }
                        ]
                      },
                      {
                        "op": "exp",
                        "args": [
                          {
                            "op": "/",
                            "args": [
                              100000000.0,
                              {
                                "op": "^",
                                "args": [
                                  "T",
                                  3.0
                                ]
                              }
                            ]
                          }
                        ]
                      }
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "f0",
                      {
                        "op": "exp",
                        "args": [
                          {
                            "op": "/",
                            "args": [
                              "g0",
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
          },
          {
            "op": "*",
            "args": [
              "num_density",
              1e-09,
              6.02214076e+17
            ]
          }
        ]
      }
    }
  ],
  "tests": [
    {
      "id": "upstream_rate_ISO2",
      "description": "Reproduces the upstream `rate_ISO2` rate-law test (GasChem.jl test/geoschem_ratelaws_test.jl). All parameters are at their declared defaults — the exact coefficient values the upstream @testitem passes to `rate_ISO2` — and the rate coefficient k is pinned to the upstream expected value 0.3009403732544113.",
      "parameter_overrides": {},
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "k",
          "time": 0.0,
          "expected": 0.3009403732544113
        }
      ]
    }
  ]
}
```

</details>
