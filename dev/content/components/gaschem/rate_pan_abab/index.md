---
title: "rate_PAN_abab"
slug: "rate_pan_abab"
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

_source_ref: GasChem.jl@8c12c048482b515fb8eb2110bf8ab4b4f4e71309:src/geoschem_ratelaws.jl:1052 (`rate_PAN_abab` rate-law builder function).

Troe-falloff rate law for BZPAN -> BZCO3 + NO2 with low- and high-pressure Arrhenius rates of the exp(b/T) form: k = k0*k1*f/(k0 + k1), f the broadened falloff factor and k0 scaled by the air number density.

Migration shape: the upstream `rate_PAN_abab` returns a Catalyst `ReactionSystem` carrying zero reactions and one variable k(t) bound by a single algebraic equation k ~ <rate expression> (the @constants in the source are MTK unit-bookkeeping; their numeric values N_A=6.02214076e23, cm3_m3=1.0e6, ppb_unit=1.0e-9, k_unit_inv=1.0e6 are folded into the .esm expression AST as literals). It is migrated here as a purely-algebraic `model`: the rate-law inputs (T, num_density, Arrhenius coefficients) are `type: parameter`, the output k is the single `type: state` variable, and `equations` holds the one defining equation. No equation carries a D(.) operator, so the trajectory is constant in time and the inline test samples at t=0 (the observed-only convention of sibling files multiple_removal.esm / ope.esm).

Units: variables carry no `units` field — the rate expression folds the upstream MTK unit conversions into numeric literals, so every quantity is nominally dimensionless to the structural validator. This is the convention of the sibling GEOS-Chem file geoschem_fullchem.esm; physical units are documented in prose in each variable's `description`.

Tolerance rationale (model-level rel=1e-8 / abs=1e-30): the rate law is a single closed-form algebraic expression evaluated once (no time integration, no stiff dynamics). rel=1e-8 sits at the upstream Julia approximate-equality default (`approx` uses rtol=sqrt(eps(Float64))=~1.49e-8) and comfortably absorbs the libm exp / ^ / log10 rounding differences between the Julia reference values and the Python ESS runner; abs=1e-30 is a near-zero floor that gates no assertion here (the smallest pinned rate constant across the file is eq_const k=~2.1e-27).

Upstream test reproduction: the inline test `upstream_rate_PAN_abab` pins k at the parameter defaults to the value asserted by the `@testitem "rate_PAN_abab"` block in GasChem.jl test/geoschem_ratelaws_test.jl, which compiles the rate law at T=293.0 K and num_density=2.7e19/N_A*cm3_m3 mol/m^3 and checks the resulting rate constant k._

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `T` |  | `293.0` | Air temperature (K). Default 293.0 K is the scenario temperature of the upstream geoschem_ratelaws_test.jl `RateLawSetup` test snippet. |
| `num_density` |  | `44.834554813693856` | Number density of air (mol/m^3). Default 44.834554813693856 mol/m^3 equals 2.7e19 molec/cm^3 — the upstream test value 2.7e19/N_A*cm3_m3 (N_A = 6.02214076e23, cm3_m3 = 1.0e6). |
| `a0` |  | `0.0049` | Low-limit pre-exponential. |
| `b0` |  | `12100.0` | Low-limit exponential temperature term. [K] |
| `a1` |  | `5.4e+16` | High-limit pre-exponential. |
| `b1` |  | `-13830.0` | High-limit exponential temperature term. [K] |
| `cf` |  | `0.3` | Falloff-curve broadening factor. |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `k` |  |  | Reaction rate coefficient produced by the rate_PAN_abab rate law, output in s^-1. Defined by one algebraic equation; the system carries no time derivative. |

## Observed expressions

$$
k = \frac{a0 \cdot e^{\frac{b0}{T}} \cdot num_{density} \cdot 6.02214076 \times 10^{17} \cdot a1 \cdot e^{\frac{b1}{T}} \cdot 10.0^{\frac{\log_{10}\left(cf\right)}{1.0 + \frac{\log_{10}\left(\frac{a0 \cdot e^{\frac{b0}{T}} \cdot num_{density} \cdot 6.02214076 \times 10^{17}}{a1 \cdot e^{\frac{b1}{T}}}\right)}{0.75 - 1.27 \cdot \log_{10}\left(cf\right)}^{2.0}}}}{a0 \cdot e^{\frac{b0}{T}} \cdot num_{density} \cdot 6.02214076 \times 10^{17} + a1 \cdot e^{\frac{b1}{T}}} \cdot 1.0
$$
_Reaction rate coefficient produced by the rate_PAN_abab rate law, output in s^-1. Defined by one algebraic equation; the system carries no time derivative._

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "reference": {
    "notes": "source_ref: GasChem.jl@8c12c048482b515fb8eb2110bf8ab4b4f4e71309:src/geoschem_ratelaws.jl:1052 (`rate_PAN_abab` rate-law builder function).\n\nTroe-falloff rate law for BZPAN -> BZCO3 + NO2 with low- and high-pressure Arrhenius rates of the exp(b/T) form: k = k0*k1*f/(k0 + k1), f the broadened falloff factor and k0 scaled by the air number density.\n\nMigration shape: the upstream `rate_PAN_abab` returns a Catalyst `ReactionSystem` carrying zero reactions and one variable k(t) bound by a single algebraic equation k ~ <rate expression> (the @constants in the source are MTK unit-bookkeeping; their numeric values N_A=6.02214076e23, cm3_m3=1.0e6, ppb_unit=1.0e-9, k_unit_inv=1.0e6 are folded into the .esm expression AST as literals). It is migrated here as a purely-algebraic `model`: the rate-law inputs (T, num_density, Arrhenius coefficients) are `type: parameter`, the output k is the single `type: state` variable, and `equations` holds the one defining equation. No equation carries a D(.) operator, so the trajectory is constant in time and the inline test samples at t=0 (the observed-only convention of sibling files multiple_removal.esm / ope.esm).\n\nUnits: variables carry no `units` field — the rate expression folds the upstream MTK unit conversions into numeric literals, so every quantity is nominally dimensionless to the structural validator. This is the convention of the sibling GEOS-Chem file geoschem_fullchem.esm; physical units are documented in prose in each variable's `description`.\n\nTolerance rationale (model-level rel=1e-8 / abs=1e-30): the rate law is a single closed-form algebraic expression evaluated once (no time integration, no stiff dynamics). rel=1e-8 sits at the upstream Julia approximate-equality default (`approx` uses rtol=sqrt(eps(Float64))=~1.49e-8) and comfortably absorbs the libm exp / ^ / log10 rounding differences between the Julia reference values and the Python ESS runner; abs=1e-30 is a near-zero floor that gates no assertion here (the smallest pinned rate constant across the file is eq_const k=~2.1e-27).\n\nUpstream test reproduction: the inline test `upstream_rate_PAN_abab` pins k at the parameter defaults to the value asserted by the `@testitem \"rate_PAN_abab\"` block in GasChem.jl test/geoschem_ratelaws_test.jl, which compiles the rate law at T=293.0 K and num_density=2.7e19/N_A*cm3_m3 mol/m^3 and checks the resulting rate constant k."
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
      "default": 0.0049,
      "description": "Low-limit pre-exponential."
    },
    "b0": {
      "type": "parameter",
      "default": 12100.0,
      "description": "Low-limit exponential temperature term. [K]"
    },
    "a1": {
      "type": "parameter",
      "default": 5.4e+16,
      "description": "High-limit pre-exponential."
    },
    "b1": {
      "type": "parameter",
      "default": -13830.0,
      "description": "High-limit exponential temperature term. [K]"
    },
    "cf": {
      "type": "parameter",
      "default": 0.3,
      "description": "Falloff-curve broadening factor."
    },
    "k": {
      "type": "unknown",
      "description": "Reaction rate coefficient produced by the rate_PAN_abab rate law, output in s^-1. Defined by one algebraic equation; the system carries no time derivative."
    }
  },
  "equations": [
    {
      "lhs": "k",
      "rhs": {
        "op": "*",
        "args": [
          {
            "op": "/",
            "args": [
              {
                "op": "*",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      {
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
                          }
                        ]
                      },
                      "num_density",
                      6.02214076e+17
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "a1",
                      {
                        "op": "exp",
                        "args": [
                          {
                            "op": "/",
                            "args": [
                              "b1",
                              "T"
                            ]
                          }
                        ]
                      }
                    ]
                  },
                  {
                    "op": "^",
                    "args": [
                      10.0,
                      {
                        "op": "/",
                        "args": [
                          {
                            "op": "log10",
                            "args": [
                              "cf"
                            ]
                          },
                          {
                            "op": "+",
                            "args": [
                              1.0,
                              {
                                "op": "^",
                                "args": [
                                  {
                                    "op": "/",
                                    "args": [
                                      {
                                        "op": "log10",
                                        "args": [
                                          {
                                            "op": "/",
                                            "args": [
                                              {
                                                "op": "*",
                                                "args": [
                                                  {
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
                                                      }
                                                    ]
                                                  },
                                                  "num_density",
                                                  6.02214076e+17
                                                ]
                                              },
                                              {
                                                "op": "*",
                                                "args": [
                                                  "a1",
                                                  {
                                                    "op": "exp",
                                                    "args": [
                                                      {
                                                        "op": "/",
                                                        "args": [
                                                          "b1",
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
                                        "op": "-",
                                        "args": [
                                          0.75,
                                          {
                                            "op": "*",
                                            "args": [
                                              1.27,
                                              {
                                                "op": "log10",
                                                "args": [
                                                  "cf"
                                                ]
                                              }
                                            ]
                                          }
                                        ]
                                      }
                                    ]
                                  },
                                  2.0
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
                      {
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
                          }
                        ]
                      },
                      "num_density",
                      6.02214076e+17
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "a1",
                      {
                        "op": "exp",
                        "args": [
                          {
                            "op": "/",
                            "args": [
                              "b1",
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
          1.0
        ]
      }
    }
  ],
  "tests": [
    {
      "id": "upstream_rate_PAN_abab",
      "description": "Reproduces the upstream `rate_PAN_abab` rate-law test (GasChem.jl test/geoschem_ratelaws_test.jl). All parameters are at their declared defaults — the exact coefficient values the upstream @testitem passes to `rate_PAN_abab` — and the rate coefficient k is pinned to the upstream expected value 0.00017076882173869417.",
      "parameter_overrides": {},
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "k",
          "time": 0.0,
          "expected": 0.00017076882173869417
        }
      ]
    }
  ]
}
```

</details>
