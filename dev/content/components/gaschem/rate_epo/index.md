---
title: "rate_EPO"
slug: "rate_epo"
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

_source_ref: GasChem.jl@8c12c048482b515fb8eb2110bf8ab4b4f4e71309:src/geoschem_ratelaws.jl:1028 (`rate_EPO` rate-law builder function).

Rate law for epoxide-forming OH reactions (RIPA/RIPB/IEPOX/IHN + OH): k = a1*exp(e1/T) * k1 * C, where k1 = 1/(m1*[M] + 1) is a pressure-dependent suppression factor.

Migration shape: the upstream `rate_EPO` returns a Catalyst `ReactionSystem` carrying zero reactions and one variable k(t) bound by a single algebraic equation k ~ <rate expression> (the @constants in the source are MTK unit-bookkeeping; their numeric values N_A=6.02214076e23, cm3_m3=1.0e6, ppb_unit=1.0e-9, k_unit_inv=1.0e6 are folded into the .esm expression AST as literals). It is migrated here as a purely-algebraic `model`: the rate-law inputs (T, num_density, Arrhenius coefficients) are `type: parameter`, the output k is the single `type: state` variable, and `equations` holds the one defining equation. No equation carries a D(.) operator, so the trajectory is constant in time and the inline test samples at t=0 (the observed-only convention of sibling files multiple_removal.esm / ope.esm).

Units: variables carry no `units` field — the rate expression folds the upstream MTK unit conversions into numeric literals, so every quantity is nominally dimensionless to the structural validator. This is the convention of the sibling GEOS-Chem file geoschem_fullchem.esm; physical units are documented in prose in each variable's `description`.

Tolerance rationale (model-level rel=1e-8 / abs=1e-30): the rate law is a single closed-form algebraic expression evaluated once (no time integration, no stiff dynamics). rel=1e-8 sits at the upstream Julia approximate-equality default (`approx` uses rtol=sqrt(eps(Float64))=~1.49e-8) and comfortably absorbs the libm exp / ^ / log10 rounding differences between the Julia reference values and the Python ESS runner; abs=1e-30 is a near-zero floor that gates no assertion here (the smallest pinned rate constant across the file is eq_const k=~2.1e-27).

Upstream test reproduction: the inline test `upstream_rate_EPO` pins k at the parameter defaults to the value asserted by the `@testitem "rate_EPO"` block in GasChem.jl test/geoschem_ratelaws_test.jl, which compiles the rate law at T=293.0 K and num_density=2.7e19/N_A*cm3_m3 mol/m^3 and checks the resulting rate constant k._

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `T` |  | `293.0` | Air temperature (K). Default 293.0 K is the scenario temperature of the upstream geoschem_ratelaws_test.jl `RateLawSetup` test snippet. |
| `num_density` |  | `44.834554813693856` | Number density of air (mol/m^3). Default 44.834554813693856 mol/m^3 equals 2.7e19 molec/cm^3 — the upstream test value 2.7e19/N_A*cm3_m3 (N_A = 6.02214076e23, cm3_m3 = 1.0e6). |
| `a1` |  | `1e-11` | Arrhenius pre-exponential. |
| `e1` |  | `390.0` | Arrhenius exponential temperature term. [K] |
| `m1` |  | `0.00015` | Pressure-suppression coefficient. |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `k` |  |  | Reaction rate coefficient produced by the rate_EPO rate law, output in ppb^-1*s^-1. Defined by one algebraic equation; the system carries no time derivative. |

## Observed expressions

$$
k = a1 \cdot e^{\frac{e1}{T}} \cdot \frac{1.0}{m1 \cdot num_{density} \cdot 6.02214076 \times 10^{17} + 1.0} \cdot num_{density} \cdot 1 \times 10^{-9} \cdot 6.02214076 \times 10^{17}
$$
_Reaction rate coefficient produced by the rate_EPO rate law, output in ppb^-1*s^-1. Defined by one algebraic equation; the system carries no time derivative._

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "reference": {
    "notes": "source_ref: GasChem.jl@8c12c048482b515fb8eb2110bf8ab4b4f4e71309:src/geoschem_ratelaws.jl:1028 (`rate_EPO` rate-law builder function).\n\nRate law for epoxide-forming OH reactions (RIPA/RIPB/IEPOX/IHN + OH): k = a1*exp(e1/T) * k1 * C, where k1 = 1/(m1*[M] + 1) is a pressure-dependent suppression factor.\n\nMigration shape: the upstream `rate_EPO` returns a Catalyst `ReactionSystem` carrying zero reactions and one variable k(t) bound by a single algebraic equation k ~ <rate expression> (the @constants in the source are MTK unit-bookkeeping; their numeric values N_A=6.02214076e23, cm3_m3=1.0e6, ppb_unit=1.0e-9, k_unit_inv=1.0e6 are folded into the .esm expression AST as literals). It is migrated here as a purely-algebraic `model`: the rate-law inputs (T, num_density, Arrhenius coefficients) are `type: parameter`, the output k is the single `type: state` variable, and `equations` holds the one defining equation. No equation carries a D(.) operator, so the trajectory is constant in time and the inline test samples at t=0 (the observed-only convention of sibling files multiple_removal.esm / ope.esm).\n\nUnits: variables carry no `units` field — the rate expression folds the upstream MTK unit conversions into numeric literals, so every quantity is nominally dimensionless to the structural validator. This is the convention of the sibling GEOS-Chem file geoschem_fullchem.esm; physical units are documented in prose in each variable's `description`.\n\nTolerance rationale (model-level rel=1e-8 / abs=1e-30): the rate law is a single closed-form algebraic expression evaluated once (no time integration, no stiff dynamics). rel=1e-8 sits at the upstream Julia approximate-equality default (`approx` uses rtol=sqrt(eps(Float64))=~1.49e-8) and comfortably absorbs the libm exp / ^ / log10 rounding differences between the Julia reference values and the Python ESS runner; abs=1e-30 is a near-zero floor that gates no assertion here (the smallest pinned rate constant across the file is eq_const k=~2.1e-27).\n\nUpstream test reproduction: the inline test `upstream_rate_EPO` pins k at the parameter defaults to the value asserted by the `@testitem \"rate_EPO\"` block in GasChem.jl test/geoschem_ratelaws_test.jl, which compiles the rate law at T=293.0 K and num_density=2.7e19/N_A*cm3_m3 mol/m^3 and checks the resulting rate constant k."
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
    "a1": {
      "type": "parameter",
      "default": 1e-11,
      "description": "Arrhenius pre-exponential."
    },
    "e1": {
      "type": "parameter",
      "default": 390.0,
      "description": "Arrhenius exponential temperature term. [K]"
    },
    "m1": {
      "type": "parameter",
      "default": 0.00015,
      "description": "Pressure-suppression coefficient."
    },
    "k": {
      "type": "unknown",
      "description": "Reaction rate coefficient produced by the rate_EPO rate law, output in ppb^-1*s^-1. Defined by one algebraic equation; the system carries no time derivative."
    }
  },
  "equations": [
    {
      "lhs": "k",
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
                  "e1",
                  "T"
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
                  {
                    "op": "*",
                    "args": [
                      "m1",
                      "num_density",
                      6.02214076e+17
                    ]
                  },
                  1.0
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
      "id": "upstream_rate_EPO",
      "description": "Reproduces the upstream `rate_EPO` rate-law test (GasChem.jl test/geoschem_ratelaws_test.jl). All parameters are at their declared defaults — the exact coefficient values the upstream @testitem passes to `rate_EPO` — and the rate coefficient k is pinned to the upstream expected value 2.523363950607153e-16.",
      "parameter_overrides": {},
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "k",
          "time": 0.0,
          "expected": 2.523363950607153e-16
        }
      ]
    }
  ]
}
```

</details>
