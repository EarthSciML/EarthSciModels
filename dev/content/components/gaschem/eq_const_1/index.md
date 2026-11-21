---
title: "eq_const_1"
slug: "eq_const_1"
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

_source_ref: GasChem.jl@8c12c048482b515fb8eb2110bf8ab4b4f4e71309:src/geoschem_ratelaws.jl:607 (`eq_const_1` rate-law builder function).

Equilibrium-constant rate law for first-order thermal decompositions (ClOO = Cl + O2, Cl2O2 = 2ClO). Same forward/backward ratio as eq_const (k = k1/k0); the output is labelled s^-1 for first-order use.

Migration shape: the upstream `eq_const_1` returns a Catalyst `ReactionSystem` carrying zero reactions and one variable k(t) bound by a single algebraic equation k ~ <rate expression> (the @constants in the source are MTK unit-bookkeeping; their numeric values N_A=6.02214076e23, cm3_m3=1.0e6, ppb_unit=1.0e-9, k_unit_inv=1.0e6 are folded into the .esm expression AST as literals). It is migrated here as a purely-algebraic `model`: the rate-law inputs (T, num_density, Arrhenius coefficients) are `type: parameter`, the output k is the single `type: state` variable, and `equations` holds the one defining equation. No equation carries a D(.) operator, so the trajectory is constant in time and the inline test samples at t=0 (the observed-only convention of sibling files multiple_removal.esm / ope.esm).

Units: variables carry no `units` field — the rate expression folds the upstream MTK unit conversions into numeric literals, so every quantity is nominally dimensionless to the structural validator. This is the convention of the sibling GEOS-Chem file geoschem_fullchem.esm; physical units are documented in prose in each variable's `description`.

Tolerance rationale (model-level rel=1e-8 / abs=1e-30): the rate law is a single closed-form algebraic expression evaluated once (no time integration, no stiff dynamics). rel=1e-8 sits at the upstream Julia approximate-equality default (`approx` uses rtol=sqrt(eps(Float64))=~1.49e-8) and comfortably absorbs the libm exp / ^ / log10 rounding differences between the Julia reference values and the Python ESS runner; abs=1e-30 is a near-zero floor that gates no assertion here (the smallest pinned rate constant across the file is eq_const k=~2.1e-27).

Upstream test reproduction: the inline test `upstream_eq_const_1` pins k at the parameter defaults to the value asserted by the `@testitem "eq_const_1"` block in GasChem.jl test/geoschem_ratelaws_test.jl, which compiles the rate law at T=293.0 K and num_density=2.7e19/N_A*cm3_m3 mol/m^3 and checks the resulting rate constant k._

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `T` |  | `293.0` | Air temperature (K). Default 293.0 K is the scenario temperature of the upstream geoschem_ratelaws_test.jl `RateLawSetup` test snippet. |
| `num_density` |  | `44.834554813693856` | Number density of air (mol/m^3). Default 44.834554813693856 mol/m^3 equals 2.7e19 molec/cm^3 — the upstream test value 2.7e19/N_A*cm3_m3 (N_A = 6.02214076e23, cm3_m3 = 1.0e6). |
| `a0` |  | `0.0049` | Backward-rate (arrhenius_ppb) pre-exponential. |
| `c0` |  | `12100.0` | Backward-rate Arrhenius temperature term. [K] |
| `a1` |  | `9.7e-29` | Forward-rate low-limit pre-exponential. |
| `b1` |  | `5.6` | Forward-rate low-limit temperature exponent. |
| `a2` |  | `9.3e-12` | Forward-rate high-limit pre-exponential. |
| `b2` |  | `1.5` | Forward-rate high-limit temperature exponent. |
| `fv` |  | `0.6` | Falloff-curve broadening parameter. |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `k` |  |  | Reaction rate coefficient produced by the eq_const_1 rate law, output in s^-1. Defined by one algebraic equation; the system carries no time derivative. |

## Observed expressions

$$
k = \frac{a1 \cdot e^{\frac{0.0}{T}} \cdot \frac{300.0}{T}^{b1} \cdot 1 \times 10^{-6} \cdot 1000000.0 \cdot num_{density} \cdot 6.02214076 \times 10^{17} \cdot fv^{\frac{1.0}{1.0 + \log_{10}\left(\frac{a1 \cdot e^{\frac{0.0}{T}} \cdot \frac{300.0}{T}^{b1} \cdot 1 \times 10^{-6} \cdot 1000000.0 \cdot num_{density} \cdot 6.02214076 \times 10^{17}}{a2 \cdot e^{\frac{0.0}{T}} \cdot \frac{300.0}{T}^{b2} \cdot 1 \times 10^{-6} \cdot 1000000.0}\right) \cdot \log_{10}\left(\frac{a1 \cdot e^{\frac{0.0}{T}} \cdot \frac{300.0}{T}^{b1} \cdot 1 \times 10^{-6} \cdot 1000000.0 \cdot num_{density} \cdot 6.02214076 \times 10^{17}}{a2 \cdot e^{\frac{0.0}{T}} \cdot \frac{300.0}{T}^{b2} \cdot 1 \times 10^{-6} \cdot 1000000.0}\right)}} \cdot \frac{1.0}{1.0 + \frac{a1 \cdot e^{\frac{0.0}{T}} \cdot \frac{300.0}{T}^{b1} \cdot 1 \times 10^{-6} \cdot 1000000.0 \cdot num_{density} \cdot 6.02214076 \times 10^{17}}{a2 \cdot e^{\frac{0.0}{T}} \cdot \frac{300.0}{T}^{b2} \cdot 1 \times 10^{-6} \cdot 1000000.0}} \cdot num_{density} \cdot 1 \times 10^{-9} \cdot 6.02214076 \times 10^{17}}{a0 \cdot e^{\frac{c0}{T}} \cdot \frac{300.0}{T}^{0.0} \cdot num_{density} \cdot 1 \times 10^{-9} \cdot 6.02214076 \times 10^{17}}
$$
_Reaction rate coefficient produced by the eq_const_1 rate law, output in s^-1. Defined by one algebraic equation; the system carries no time derivative._

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "reference": {
    "notes": "source_ref: GasChem.jl@8c12c048482b515fb8eb2110bf8ab4b4f4e71309:src/geoschem_ratelaws.jl:607 (`eq_const_1` rate-law builder function).\n\nEquilibrium-constant rate law for first-order thermal decompositions (ClOO = Cl + O2, Cl2O2 = 2ClO). Same forward/backward ratio as eq_const (k = k1/k0); the output is labelled s^-1 for first-order use.\n\nMigration shape: the upstream `eq_const_1` returns a Catalyst `ReactionSystem` carrying zero reactions and one variable k(t) bound by a single algebraic equation k ~ <rate expression> (the @constants in the source are MTK unit-bookkeeping; their numeric values N_A=6.02214076e23, cm3_m3=1.0e6, ppb_unit=1.0e-9, k_unit_inv=1.0e6 are folded into the .esm expression AST as literals). It is migrated here as a purely-algebraic `model`: the rate-law inputs (T, num_density, Arrhenius coefficients) are `type: parameter`, the output k is the single `type: state` variable, and `equations` holds the one defining equation. No equation carries a D(.) operator, so the trajectory is constant in time and the inline test samples at t=0 (the observed-only convention of sibling files multiple_removal.esm / ope.esm).\n\nUnits: variables carry no `units` field — the rate expression folds the upstream MTK unit conversions into numeric literals, so every quantity is nominally dimensionless to the structural validator. This is the convention of the sibling GEOS-Chem file geoschem_fullchem.esm; physical units are documented in prose in each variable's `description`.\n\nTolerance rationale (model-level rel=1e-8 / abs=1e-30): the rate law is a single closed-form algebraic expression evaluated once (no time integration, no stiff dynamics). rel=1e-8 sits at the upstream Julia approximate-equality default (`approx` uses rtol=sqrt(eps(Float64))=~1.49e-8) and comfortably absorbs the libm exp / ^ / log10 rounding differences between the Julia reference values and the Python ESS runner; abs=1e-30 is a near-zero floor that gates no assertion here (the smallest pinned rate constant across the file is eq_const k=~2.1e-27).\n\nUpstream test reproduction: the inline test `upstream_eq_const_1` pins k at the parameter defaults to the value asserted by the `@testitem \"eq_const_1\"` block in GasChem.jl test/geoschem_ratelaws_test.jl, which compiles the rate law at T=293.0 K and num_density=2.7e19/N_A*cm3_m3 mol/m^3 and checks the resulting rate constant k."
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
      "description": "Backward-rate (arrhenius_ppb) pre-exponential."
    },
    "c0": {
      "type": "parameter",
      "default": 12100.0,
      "description": "Backward-rate Arrhenius temperature term. [K]"
    },
    "a1": {
      "type": "parameter",
      "default": 9.7e-29,
      "description": "Forward-rate low-limit pre-exponential."
    },
    "b1": {
      "type": "parameter",
      "default": 5.6,
      "description": "Forward-rate low-limit temperature exponent."
    },
    "a2": {
      "type": "parameter",
      "default": 9.3e-12,
      "description": "Forward-rate high-limit pre-exponential."
    },
    "b2": {
      "type": "parameter",
      "default": 1.5,
      "description": "Forward-rate high-limit temperature exponent."
    },
    "fv": {
      "type": "parameter",
      "default": 0.6,
      "description": "Falloff-curve broadening parameter."
    },
    "k": {
      "type": "unknown",
      "description": "Reaction rate coefficient produced by the eq_const_1 rate law, output in s^-1. Defined by one algebraic equation; the system carries no time derivative."
    }
  },
  "equations": [
    {
      "lhs": "k",
      "rhs": {
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
                      {
                        "op": "*",
                        "args": [
                          "a1",
                          {
                            "op": "*",
                            "args": [
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
                                      300.0,
                                      "T"
                                    ]
                                  },
                                  "b1"
                                ]
                              }
                            ]
                          },
                          1e-06
                        ]
                      },
                      1000000.0,
                      "num_density",
                      6.02214076e+17
                    ]
                  },
                  {
                    "op": "^",
                    "args": [
                      "fv",
                      {
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
                                                  "a1",
                                                  {
                                                    "op": "*",
                                                    "args": [
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
                                                              300.0,
                                                              "T"
                                                            ]
                                                          },
                                                          "b1"
                                                        ]
                                                      }
                                                    ]
                                                  },
                                                  1e-06
                                                ]
                                              },
                                              1000000.0,
                                              "num_density",
                                              6.02214076e+17
                                            ]
                                          },
                                          {
                                            "op": "*",
                                            "args": [
                                              {
                                                "op": "*",
                                                "args": [
                                                  "a2",
                                                  {
                                                    "op": "*",
                                                    "args": [
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
                                                              300.0,
                                                              "T"
                                                            ]
                                                          },
                                                          "b2"
                                                        ]
                                                      }
                                                    ]
                                                  },
                                                  1e-06
                                                ]
                                              },
                                              1000000.0
                                            ]
                                          }
                                        ]
                                      }
                                    ]
                                  },
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
                                                  "a1",
                                                  {
                                                    "op": "*",
                                                    "args": [
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
                                                              300.0,
                                                              "T"
                                                            ]
                                                          },
                                                          "b1"
                                                        ]
                                                      }
                                                    ]
                                                  },
                                                  1e-06
                                                ]
                                              },
                                              1000000.0,
                                              "num_density",
                                              6.02214076e+17
                                            ]
                                          },
                                          {
                                            "op": "*",
                                            "args": [
                                              {
                                                "op": "*",
                                                "args": [
                                                  "a2",
                                                  {
                                                    "op": "*",
                                                    "args": [
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
                                                              300.0,
                                                              "T"
                                                            ]
                                                          },
                                                          "b2"
                                                        ]
                                                      }
                                                    ]
                                                  },
                                                  1e-06
                                                ]
                                              },
                                              1000000.0
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
                        ]
                      }
                    ]
                  },
                  {
                    "op": "/",
                    "args": [
                      1.0,
                      {
                        "op": "+",
                        "args": [
                          1.0,
                          {
                            "op": "/",
                            "args": [
                              {
                                "op": "*",
                                "args": [
                                  {
                                    "op": "*",
                                    "args": [
                                      "a1",
                                      {
                                        "op": "*",
                                        "args": [
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
                                                  300.0,
                                                  "T"
                                                ]
                                              },
                                              "b1"
                                            ]
                                          }
                                        ]
                                      },
                                      1e-06
                                    ]
                                  },
                                  1000000.0,
                                  "num_density",
                                  6.02214076e+17
                                ]
                              },
                              {
                                "op": "*",
                                "args": [
                                  {
                                    "op": "*",
                                    "args": [
                                      "a2",
                                      {
                                        "op": "*",
                                        "args": [
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
                                                  300.0,
                                                  "T"
                                                ]
                                              },
                                              "b2"
                                            ]
                                          }
                                        ]
                                      },
                                      1e-06
                                    ]
                                  },
                                  1000000.0
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
          },
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
                      300.0,
                      "T"
                    ]
                  },
                  0.0
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
        ]
      }
    }
  ],
  "tests": [
    {
      "id": "upstream_eq_const_1",
      "description": "Reproduces the upstream `eq_const_1` rate-law test (GasChem.jl test/geoschem_ratelaws_test.jl). All parameters are at their declared defaults — the exact coefficient values the upstream @testitem passes to `eq_const_1` — and the rate coefficient k is pinned to the upstream expected value 2.1206340759025532e-27.",
      "parameter_overrides": {},
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "k",
          "time": 0.0,
          "expected": 2.1206340759025532e-27
        }
      ]
    }
  ]
}
```

</details>
