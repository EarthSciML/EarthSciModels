---
title: "HNO3Equilibria"
slug: "hno3equilibria"
domains: ["aerosol"]
component_types: ["model"]
subdomains: ["aq_eq"]
domain: "aerosol"
subdomain: "aq_eq"
component_type: "model"
esm_version: "1.0.0"
esm_path: "components/aerosol/aq_eq/hno3.esm"
reference: "Seinfeld, J. H., & Pandis, S. N. (2016). Atmospheric Chemistry and Physics: From Air Pollution to Climate Change, 3rd ed. Wiley. Chapter 7, Section 7.3.5 (HNO3 dissolution/dissociation, Eq 7.53–7.54, 7.58, 7.61) and Table 7.4 (equilibrium-constant temperature dependence). ISBN 978-1-118-94740-1."
description: "HNO3 gas-aqueous dissolution and dissociation equilibria. Migrated from Aerosol.jl@c8c640bb src/aqueous_equilibria.jl:438 (`HNO3Equilibria` @component). Implements Seinfeld & Pandis Ch 7 §7.3.5 (Eq 7.53–7.54, 7.58, 7.61): K_H(HNO3, 298 K) = 2.1×10⁵ M/atm (temperature-independent, dH≈0), K_n1(HNO3, 298 K) = 15.4 M (temperature-independent). HNO3 is a strong acid (pKa ≈ −1.2) that essentially completely dissociates at all atmospheric pH values. Parameterized as observed-only: T, H_plus, and p_HNO3 are inputs; H_HNO3, K_n1, HNO3_aq, NO3_minus, HNO3_total, H_HNO3_eff are algebraic outputs."
tags: ["aerosol", "aq_eq", "model", "aqueous_equilibria", "observed-only", "seinfeld-pandis"]
---

## Description

HNO3 gas-aqueous dissolution and dissociation equilibria. Migrated from Aerosol.jl@c8c640bb src/aqueous_equilibria.jl:438 (`HNO3Equilibria` @component). Implements Seinfeld & Pandis Ch 7 §7.3.5 (Eq 7.53–7.54, 7.58, 7.61): K_H(HNO3, 298 K) = 2.1×10⁵ M/atm (temperature-independent, dH≈0), K_n1(HNO3, 298 K) = 15.4 M (temperature-independent). HNO3 is a strong acid (pKa ≈ −1.2) that essentially completely dissociates at all atmospheric pH values. Parameterized as observed-only: T, H_plus, and p_HNO3 are inputs; H_HNO3, K_n1, HNO3_aq, NO3_minus, HNO3_total, H_HNO3_eff are algebraic outputs.

## Reference

_source_ref: Aerosol.jl@c8c640bb:src/aqueous_equilibria.jl:438

Upstream `HNO3Equilibria` is an MTK `@component` where T, H_plus, and p_HNO3 are `@variables` driven by a parent `AqueousEquilibria` system. For standalone serialization (and to make the component well-posed in isolation), T, H_plus, and p_HNO3 are declared as parameters here — matching the bead's `(S, observed-only)` classification. The six algebraic equations are unchanged from upstream.

Key property: HNO3 is a strong acid (K_n1 = 15.4 M, pKa ≈ −1.2). At all atmospheric pH values (pH 0–7), K_n1/[H+] ≫ 1: e.g. at pH 4 K_n1/H+ = 1.54×10⁵, at pH 2 K_n1/H+ = 1540. This means NO3⁻ ≫ HNO3(aq) and H*_HNO3 ≫ H_HNO3 for virtually all atmospheric conditions. Only at [H+] ≥ K_n1 (≥ 15.4 mol/L, extremely concentrated acid) does incomplete dissociation occur.

Key difference from SO2/CO2/NH3/H2O2: both dH_H_HNO3 and the temperature dependence of K_n1 are zero (upstream uses K_n1 ~ K_n1_298 with no van't Hoff correction). The van't Hoff form for H_HNO3 is retained for interface consistency, but exp(0) = 1 so H_HNO3 = H_HNO3_298 at all temperatures.

H_HNO3_298 = 2.1×10⁵ M/atm × 1000 mol·m⁻³/M ÷ 101325 Pa/atm = 2072.5389 mol/(m³·Pa). K_n1_298 = 15.4 M × 1000 = 15400 mol/m³.

Tolerance rationale (model-level rel=1e-6): observed-only algebraic system (no ODE integration); 1e-6 covers float64 roundoff in the simple arithmetic expressions. Since dH=0 the van't Hoff exp() evaluates to exactly 1.0 at any T; all other operations are multiplications, divisions, and additions._

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `T` | `K` | `298.0` | Temperature |
| `H_plus` | `mol/m^3` | `0.0001` | Hydrogen ion concentration (1e-4 mol/m³ = pH 7 in pure water at 298 K) |
| `p_HNO3` | `Pa` | `1.0` | Partial pressure of HNO3 |
| `R_gas` | `J/mol/K` | `8.314` | Gas constant |
| `T_ref` | `K` | `298.0` | Reference temperature |
| `H_HNO3_298` | `mol/m^3/Pa` | `2072.53886010363` | Henry's law constant for HNO3 at 298 K (2.1×10⁵ M/atm converted to mol/(m³·Pa): 2.1e5 / 101325.0 * 1000.0) |
| `dH_H_HNO3` | `J/mol` | `0.0` | Heat of dissolution for HNO3 (negligible temperature dependence; Seinfeld & Pandis Table 7.4) |
| `K_n1_298` | `mol/m^3` | `15400.0` | Dissociation constant for HNO3 → H⁺ + NO3⁻ at 298 K (15.4 M converted to mol/m³; temperature-independent in upstream source; pKa ≈ −1.2) |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `H_HNO3` | `mol/m^3/Pa` |  | Temperature-dependent Henry's law constant for HNO3 (equals H_HNO3_298 since dH=0) |
| `K_n1` | `mol/m^3` |  | Dissociation constant HNO3 → H⁺ + NO3⁻ (temperature-independent: K_n1 = K_n1_298) |
| `HNO3_aq` | `mol/m^3` |  | Undissociated aqueous HNO3 concentration |
| `NO3_minus` | `mol/m^3` |  | Nitrate anion concentration [NO3-] |
| `HNO3_total` | `mol/m^3` |  | Total dissolved nitric acid: [HNO3(aq)] + [NO3-] |
| `H_HNO3_eff` | `mol/m^3/Pa` |  | Effective Henry's law constant for HNO3 accounting for dissociation: H_HNO3 × (1 + K_n1/[H+]) |

## Observed expressions

$$
H_{HNO3} = H_{HNO3\,298} \cdot e^{\frac{dH_{H\,HNO3}}{R_{gas}} \cdot \left(\frac{1}{T_{ref}} + \frac{-1}{T}\right)}
$$
_Temperature-dependent Henry's law constant for HNO3 (equals H_HNO3_298 since dH=0)_

$$
K_{n1} = K_{n1\,298}
$$
_Dissociation constant HNO3 → H⁺ + NO3⁻ (temperature-independent: K_n1 = K_n1_298)_

$$
HNO3_{aq} = H_{HNO3} \cdot p_{HNO3}
$$
_Undissociated aqueous HNO3 concentration_

$$
NO3_{minus} = \frac{K_{n1} \cdot HNO3_{aq}}{H_{plus}}
$$
_Nitrate anion concentration [NO3-]_

$$
HNO3_{total} = HNO3_{aq} + NO3_{minus}
$$
_Total dissolved nitric acid: [HNO3(aq)] + [NO3-]_

$$
H_{HNO3\,eff} = H_{HNO3} \cdot \left(1 + \frac{K_{n1}}{H_{plus}}\right)
$$
_Effective Henry's law constant for HNO3 accounting for dissociation: H_HNO3 × (1 + K_n1/[H+])_

## Analyses

### H_HNO3_eff_vs_pH

Effective Henry's constant H*_HNO3 = H_HNO3 × (1 + K_n1/[H+]) vs [H+] at 298 K. HNO3 pKa ≈ −1.2, so K_n1/[H+] ≫ 1 across the entire atmospheric pH range (pH 0–7). H*_HNO3 decreases proportionally with increasing [H+]: at pH 7 H*_HNO3 ≈ 1.54×10⁸ × H_HNO3; at pH 2 H*_HNO3 ≈ 1540 × H_HNO3. Only at [H+] ≥ K_n1 (> 15 mol/L, beyond physically realizable aqueous solutions) does incomplete dissociation occur.

**Time span:** 0.0 → 1.0

**Swept over:** `H_plus`

![H*_HNO3 vs (H+) — steeply decreasing effective Henry's constant showing nearly complete dissociation at all atmospheric (H+) values.](/plots/aerosol/aq_eq/hno3equilibria/H_HNO3_eff_vs_pH-Hstar_curve.png)

![NO3⁻ fraction of total dissolved HNO3 vs (H+). Fraction = K_n1/(K_n1 + H_plus). Equals 1 (complete dissociation) for all atmospheric conditions, approaching 0.5 only at (H+) = K_n1 ≈ 15 mol/L.](/plots/aerosol/aq_eq/hno3equilibria/H_HNO3_eff_vs_pH-dissociation_fraction.png)

### NO3_minus_vs_p_HNO3

Aqueous nitrate concentration [NO3-] as a function of HNO3 partial pressure at pH 7. Shows perfect linearity: [NO3-] = H_HNO3 × K_n1/[H+] × p_HNO3. Since HNO3 is a strong acid, essentially all dissolved HNO3 appears as NO3⁻ at atmospheric pH, making [NO3-] ≈ HNO3_total. Henry's law linearity spans the full atmospheric HNO3 range.

**Time span:** 0.0 → 1.0

**Swept over:** `p_HNO3`

![(NO3-) vs p_HNO3 at pH 7 — linear Henry's law partitioning demonstrating that dissolved HNO3 is quantitatively converted to nitrate.](/plots/aerosol/aq_eq/hno3equilibria/NO3_minus_vs_p_HNO3-NO3_vs_p_HNO3.png)

### temperature_invariance_sweep

H_HNO3 vs temperature from 273 K to 318 K. Unlike SO2, CO2, NH3, and H2O2 (which all have significant van't Hoff temperature dependencies), HNO3 has dH_H_HNO3 = 0 and remains constant across the full atmospheric temperature range. This flat response is characteristic of strong inorganic acids.

**Time span:** 0.0 → 1.0

**Swept over:** `T`

![H_HNO3(T) — flat line demonstrating temperature-independent HNO3 solubility (dH=0).](/plots/aerosol/aq_eq/hno3equilibria/temperature_invariance_sweep-H_HNO3_vs_T.png)

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "reference": {
    "notes": "source_ref: Aerosol.jl@c8c640bb:src/aqueous_equilibria.jl:438\n\nUpstream `HNO3Equilibria` is an MTK `@component` where T, H_plus, and p_HNO3 are `@variables` driven by a parent `AqueousEquilibria` system. For standalone serialization (and to make the component well-posed in isolation), T, H_plus, and p_HNO3 are declared as parameters here — matching the bead's `(S, observed-only)` classification. The six algebraic equations are unchanged from upstream.\n\nKey property: HNO3 is a strong acid (K_n1 = 15.4 M, pKa ≈ −1.2). At all atmospheric pH values (pH 0–7), K_n1/[H+] ≫ 1: e.g. at pH 4 K_n1/H+ = 1.54×10⁵, at pH 2 K_n1/H+ = 1540. This means NO3⁻ ≫ HNO3(aq) and H*_HNO3 ≫ H_HNO3 for virtually all atmospheric conditions. Only at [H+] ≥ K_n1 (≥ 15.4 mol/L, extremely concentrated acid) does incomplete dissociation occur.\n\nKey difference from SO2/CO2/NH3/H2O2: both dH_H_HNO3 and the temperature dependence of K_n1 are zero (upstream uses K_n1 ~ K_n1_298 with no van't Hoff correction). The van't Hoff form for H_HNO3 is retained for interface consistency, but exp(0) = 1 so H_HNO3 = H_HNO3_298 at all temperatures.\n\nH_HNO3_298 = 2.1×10⁵ M/atm × 1000 mol·m⁻³/M ÷ 101325 Pa/atm = 2072.5389 mol/(m³·Pa). K_n1_298 = 15.4 M × 1000 = 15400 mol/m³.\n\nTolerance rationale (model-level rel=1e-6): observed-only algebraic system (no ODE integration); 1e-6 covers float64 roundoff in the simple arithmetic expressions. Since dH=0 the van't Hoff exp() evaluates to exactly 1.0 at any T; all other operations are multiplications, divisions, and additions."
  },
  "tolerance": {
    "rel": 1e-06
  },
  "variables": {
    "T": {
      "type": "parameter",
      "units": "K",
      "default": 298.0,
      "description": "Temperature"
    },
    "H_plus": {
      "type": "parameter",
      "units": "mol/m^3",
      "default": 0.0001,
      "description": "Hydrogen ion concentration (1e-4 mol/m³ = pH 7 in pure water at 298 K)"
    },
    "p_HNO3": {
      "type": "parameter",
      "units": "Pa",
      "default": 1.0,
      "description": "Partial pressure of HNO3"
    },
    "R_gas": {
      "type": "parameter",
      "units": "J/mol/K",
      "default": 8.314,
      "description": "Gas constant"
    },
    "T_ref": {
      "type": "parameter",
      "units": "K",
      "default": 298.0,
      "description": "Reference temperature"
    },
    "H_HNO3_298": {
      "type": "parameter",
      "units": "mol/m^3/Pa",
      "default": 2072.53886010363,
      "description": "Henry's law constant for HNO3 at 298 K (2.1×10⁵ M/atm converted to mol/(m³·Pa): 2.1e5 / 101325.0 * 1000.0)"
    },
    "dH_H_HNO3": {
      "type": "parameter",
      "units": "J/mol",
      "default": 0.0,
      "description": "Heat of dissolution for HNO3 (negligible temperature dependence; Seinfeld & Pandis Table 7.4)"
    },
    "K_n1_298": {
      "type": "parameter",
      "units": "mol/m^3",
      "default": 15400.0,
      "description": "Dissociation constant for HNO3 → H⁺ + NO3⁻ at 298 K (15.4 M converted to mol/m³; temperature-independent in upstream source; pKa ≈ −1.2)"
    },
    "H_HNO3": {
      "type": "unknown",
      "units": "mol/m^3/Pa",
      "description": "Temperature-dependent Henry's law constant for HNO3 (equals H_HNO3_298 since dH=0)"
    },
    "K_n1": {
      "type": "unknown",
      "units": "mol/m^3",
      "description": "Dissociation constant HNO3 → H⁺ + NO3⁻ (temperature-independent: K_n1 = K_n1_298)"
    },
    "HNO3_aq": {
      "type": "unknown",
      "units": "mol/m^3",
      "description": "Undissociated aqueous HNO3 concentration"
    },
    "NO3_minus": {
      "type": "unknown",
      "units": "mol/m^3",
      "description": "Nitrate anion concentration [NO3-]"
    },
    "HNO3_total": {
      "type": "unknown",
      "units": "mol/m^3",
      "description": "Total dissolved nitric acid: [HNO3(aq)] + [NO3-]"
    },
    "H_HNO3_eff": {
      "type": "unknown",
      "units": "mol/m^3/Pa",
      "description": "Effective Henry's law constant for HNO3 accounting for dissociation: H_HNO3 × (1 + K_n1/[H+])"
    }
  },
  "equations": [
    {
      "lhs": "H_HNO3",
      "rhs": {
        "op": "*",
        "args": [
          "H_HNO3_298",
          {
            "op": "exp",
            "args": [
              {
                "op": "*",
                "args": [
                  {
                    "op": "/",
                    "args": [
                      "dH_H_HNO3",
                      "R_gas"
                    ]
                  },
                  {
                    "op": "+",
                    "args": [
                      {
                        "op": "/",
                        "args": [
                          1,
                          "T_ref"
                        ]
                      },
                      {
                        "op": "/",
                        "args": [
                          -1,
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
    },
    {
      "lhs": "K_n1",
      "rhs": "K_n1_298"
    },
    {
      "lhs": "HNO3_aq",
      "rhs": {
        "op": "*",
        "args": [
          "H_HNO3",
          "p_HNO3"
        ]
      }
    },
    {
      "lhs": "NO3_minus",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "*",
            "args": [
              "K_n1",
              "HNO3_aq"
            ]
          },
          "H_plus"
        ]
      }
    },
    {
      "lhs": "HNO3_total",
      "rhs": {
        "op": "+",
        "args": [
          "HNO3_aq",
          "NO3_minus"
        ]
      }
    },
    {
      "lhs": "H_HNO3_eff",
      "rhs": {
        "op": "*",
        "args": [
          "H_HNO3",
          {
            "op": "+",
            "args": [
              1,
              {
                "op": "/",
                "args": [
                  "K_n1",
                  "H_plus"
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
      "id": "reference_298K_pH7",
      "description": "Reference state at 298 K with neutral water (pH 7, [H+]=1e-4 mol/m³) and 1 Pa HNO3. At T=T_ref the van't Hoff exponent is zero so H_HNO3 = H_HNO3_298. K_n1 is temperature-independent. K_n1/H_plus = 15400/1e-4 = 1.54e8 — HNO3 is essentially completely dissociated (NO3⁻ ≈ 1.54×10⁸ × HNO3_aq). H_HNO3_eff ≈ H_HNO3 × K_n1/H_plus to excellent approximation.",
      "parameter_overrides": {
        "T": 298.0,
        "H_plus": 0.0001,
        "p_HNO3": 1.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "H_HNO3",
          "time": 0.0,
          "expected": 2072.53886010363
        },
        {
          "variable": "K_n1",
          "time": 0.0,
          "expected": 15400.0
        },
        {
          "variable": "HNO3_aq",
          "time": 0.0,
          "expected": 2072.53886010363
        },
        {
          "variable": "NO3_minus",
          "time": 0.0,
          "expected": 319170984455.958
        },
        {
          "variable": "HNO3_total",
          "time": 0.0,
          "expected": 319170986528.497
        },
        {
          "variable": "H_HNO3_eff",
          "time": 0.0,
          "expected": 319170986528.497
        }
      ]
    },
    {
      "id": "temperature_invariance_cold",
      "description": "Cold cloud water at 273.15 K (0°C), pH 7. Because dH_H_HNO3 = 0, H_HNO3 = H_HNO3_298 exactly at any temperature. K_n1 is also temperature-independent. All state values are identical to the 298 K reference — unique among the aqueous equilibria models.",
      "parameter_overrides": {
        "T": 273.15,
        "H_plus": 0.0001,
        "p_HNO3": 1.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "H_HNO3",
          "time": 0.0,
          "expected": 2072.53886010363
        },
        {
          "variable": "K_n1",
          "time": 0.0,
          "expected": 15400.0
        },
        {
          "variable": "HNO3_aq",
          "time": 0.0,
          "expected": 2072.53886010363
        },
        {
          "variable": "NO3_minus",
          "time": 0.0,
          "expected": 319170984455.958
        },
        {
          "variable": "HNO3_total",
          "time": 0.0,
          "expected": 319170986528.497
        },
        {
          "variable": "H_HNO3_eff",
          "time": 0.0,
          "expected": 319170986528.497
        }
      ]
    },
    {
      "id": "temperature_invariance_warm",
      "description": "Warm cloud water at 310 K (37°C), pH 7. Same as reference and cold cases — H_HNO3 and all equilibrium values are temperature-independent for HNO3.",
      "parameter_overrides": {
        "T": 310.0,
        "H_plus": 0.0001,
        "p_HNO3": 1.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "H_HNO3",
          "time": 0.0,
          "expected": 2072.53886010363
        },
        {
          "variable": "HNO3_aq",
          "time": 0.0,
          "expected": 2072.53886010363
        },
        {
          "variable": "H_HNO3_eff",
          "time": 0.0,
          "expected": 319170986528.497
        }
      ]
    },
    {
      "id": "acidic_pH4",
      "description": "Acidic cloud water (pH 4, [H+] = 0.1 mol/m³) at 298 K. K_n1/H_plus = 15400/0.1 = 1.54×10⁵ — still nearly complete dissociation. Represents typical acid-rain conditions.",
      "parameter_overrides": {
        "T": 298.0,
        "H_plus": 0.1,
        "p_HNO3": 1.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "H_HNO3",
          "time": 0.0,
          "expected": 2072.53886010363
        },
        {
          "variable": "HNO3_aq",
          "time": 0.0,
          "expected": 2072.53886010363
        },
        {
          "variable": "NO3_minus",
          "time": 0.0,
          "expected": 319170984.455958
        },
        {
          "variable": "HNO3_total",
          "time": 0.0,
          "expected": 319173056.994819
        },
        {
          "variable": "H_HNO3_eff",
          "time": 0.0,
          "expected": 319173056.994819
        }
      ]
    },
    {
      "id": "acidic_pH2",
      "description": "Strongly acidic (pH 2, [H+] = 10 mol/m³) at 298 K. K_n1/H_plus = 15400/10 = 1540 — still >99.9% dissociated. Exercises the high-acid tail of NO3_minus and H_HNO3_eff.",
      "parameter_overrides": {
        "T": 298.0,
        "H_plus": 10.0,
        "p_HNO3": 1.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "HNO3_aq",
          "time": 0.0,
          "expected": 2072.53886010363
        },
        {
          "variable": "NO3_minus",
          "time": 0.0,
          "expected": 3191709.84455958
        },
        {
          "variable": "HNO3_total",
          "time": 0.0,
          "expected": 3193782.38341969
        },
        {
          "variable": "H_HNO3_eff",
          "time": 0.0,
          "expected": 3193782.38341969
        }
      ]
    },
    {
      "id": "very_acidic_Hplus100",
      "description": "Extreme acid regime ([H+] = 100 mol/m³) at 298 K. K_n1/H_plus = 15400/100 = 154 — still 99% dissociated. Stress-tests the NO3_minus and H_HNO3_eff expressions deep into the concentrated-acid tail.",
      "parameter_overrides": {
        "T": 298.0,
        "H_plus": 100.0,
        "p_HNO3": 1.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "HNO3_aq",
          "time": 0.0,
          "expected": 2072.53886010363
        },
        {
          "variable": "NO3_minus",
          "time": 0.0,
          "expected": 319170.984455958
        },
        {
          "variable": "HNO3_total",
          "time": 0.0,
          "expected": 321243.523316062
        },
        {
          "variable": "H_HNO3_eff",
          "time": 0.0,
          "expected": 321243.523316062
        }
      ]
    },
    {
      "id": "pKa_equiv_Hplus15400",
      "description": "At [H+] = K_n1 = 15400 mol/m³ (pKa-equivalent point), exactly 50% of dissolved HNO3 is undissociated: NO3_minus = HNO3_aq, HNO3_total = 2 × HNO3_aq, and H_HNO3_eff = 2 × H_HNO3. This extreme concentration (far beyond physical liquids) is a mathematical symmetry check.",
      "parameter_overrides": {
        "T": 298.0,
        "H_plus": 15400.0,
        "p_HNO3": 1.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "H_HNO3",
          "time": 0.0,
          "expected": 2072.53886010363
        },
        {
          "variable": "HNO3_aq",
          "time": 0.0,
          "expected": 2072.53886010363
        },
        {
          "variable": "NO3_minus",
          "time": 0.0,
          "expected": 2072.53886010363
        },
        {
          "variable": "HNO3_total",
          "time": 0.0,
          "expected": 4145.07772020725
        },
        {
          "variable": "H_HNO3_eff",
          "time": 0.0,
          "expected": 4145.07772020725
        }
      ]
    },
    {
      "id": "pressure_linearity_high",
      "description": "Henry's-law linearity check: 10× p_HNO3 at fixed T and H_plus scales HNO3_aq, NO3_minus, HNO3_total by 10× while leaving H_HNO3, K_n1, H_HNO3_eff unchanged.",
      "parameter_overrides": {
        "T": 298.0,
        "H_plus": 0.0001,
        "p_HNO3": 10.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "H_HNO3",
          "time": 0.0,
          "expected": 2072.53886010363
        },
        {
          "variable": "HNO3_aq",
          "time": 0.0,
          "expected": 20725.3886010363
        },
        {
          "variable": "NO3_minus",
          "time": 0.0,
          "expected": 3191709844559.58
        },
        {
          "variable": "HNO3_total",
          "time": 0.0,
          "expected": 3191709865284.97
        },
        {
          "variable": "H_HNO3_eff",
          "time": 0.0,
          "expected": 319170986528.497
        }
      ]
    },
    {
      "id": "pressure_linearity_low",
      "description": "Henry's-law linearity at low partial pressure: p_HNO3 = 0.01 Pa scales HNO3_aq, NO3_minus, HNO3_total by 0.01× from baseline. H_HNO3 and H_HNO3_eff are pressure-independent.",
      "parameter_overrides": {
        "T": 298.0,
        "H_plus": 0.0001,
        "p_HNO3": 0.01
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "HNO3_aq",
          "time": 0.0,
          "expected": 20.7253886010363
        },
        {
          "variable": "NO3_minus",
          "time": 0.0,
          "expected": 3191709844.55958
        },
        {
          "variable": "HNO3_total",
          "time": 0.0,
          "expected": 3191709865.28497
        },
        {
          "variable": "H_HNO3_eff",
          "time": 0.0,
          "expected": 319170986528.497
        }
      ]
    }
  ],
  "analyses": [
    {
      "id": "H_HNO3_eff_vs_pH",
      "description": "Effective Henry's constant H*_HNO3 = H_HNO3 × (1 + K_n1/[H+]) vs [H+] at 298 K. HNO3 pKa ≈ −1.2, so K_n1/[H+] ≫ 1 across the entire atmospheric pH range (pH 0–7). H*_HNO3 decreases proportionally with increasing [H+]: at pH 7 H*_HNO3 ≈ 1.54×10⁸ × H_HNO3; at pH 2 H*_HNO3 ≈ 1540 × H_HNO3. Only at [H+] ≥ K_n1 (> 15 mol/L, beyond physically realizable aqueous solutions) does incomplete dissociation occur.",
      "initial_state": {},
      "parameters": {
        "T": 298.0,
        "p_HNO3": 1.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "parameter_sweep": {
        "type": "cartesian",
        "dimensions": [
          {
            "parameter": "H_plus",
            "range": {
              "start": 1e-06,
              "stop": 10000.0,
              "count": 30,
              "scale": "log"
            }
          }
        ]
      },
      "plots": [
        {
          "id": "Hstar_curve",
          "type": "line",
          "description": "H*_HNO3 vs [H+] — steeply decreasing effective Henry's constant showing nearly complete dissociation at all atmospheric [H+] values.",
          "x": {
            "variable": "H_plus",
            "label": "[H⁺] (mol/m³, log scale)"
          },
          "y": {
            "variable": "H_HNO3_eff",
            "label": "H*_HNO3 (mol/(m³·Pa), log scale)"
          }
        },
        {
          "id": "dissociation_fraction",
          "type": "line",
          "description": "NO3⁻ fraction of total dissolved HNO3 vs [H+]. Fraction = K_n1/(K_n1 + H_plus). Equals 1 (complete dissociation) for all atmospheric conditions, approaching 0.5 only at [H+] = K_n1 ≈ 15 mol/L.",
          "x": {
            "variable": "H_plus",
            "label": "[H⁺] (mol/m³, log scale)"
          },
          "y": {
            "variable": "NO3_minus",
            "label": "[NO3-] (mol/m³, log scale)"
          }
        }
      ]
    },
    {
      "id": "NO3_minus_vs_p_HNO3",
      "description": "Aqueous nitrate concentration [NO3-] as a function of HNO3 partial pressure at pH 7. Shows perfect linearity: [NO3-] = H_HNO3 × K_n1/[H+] × p_HNO3. Since HNO3 is a strong acid, essentially all dissolved HNO3 appears as NO3⁻ at atmospheric pH, making [NO3-] ≈ HNO3_total. Henry's law linearity spans the full atmospheric HNO3 range.",
      "initial_state": {},
      "parameters": {
        "T": 298.0,
        "H_plus": 0.0001
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "parameter_sweep": {
        "type": "cartesian",
        "dimensions": [
          {
            "parameter": "p_HNO3",
            "range": {
              "start": 0.0001,
              "stop": 10.0,
              "count": 20,
              "scale": "log"
            }
          }
        ]
      },
      "plots": [
        {
          "id": "NO3_vs_p_HNO3",
          "type": "line",
          "description": "[NO3-] vs p_HNO3 at pH 7 — linear Henry's law partitioning demonstrating that dissolved HNO3 is quantitatively converted to nitrate.",
          "x": {
            "variable": "p_HNO3",
            "label": "p(HNO3) (Pa, log scale)"
          },
          "y": {
            "variable": "NO3_minus",
            "label": "[NO3-] (mol/m³, log scale)"
          }
        }
      ]
    },
    {
      "id": "temperature_invariance_sweep",
      "description": "H_HNO3 vs temperature from 273 K to 318 K. Unlike SO2, CO2, NH3, and H2O2 (which all have significant van't Hoff temperature dependencies), HNO3 has dH_H_HNO3 = 0 and remains constant across the full atmospheric temperature range. This flat response is characteristic of strong inorganic acids.",
      "initial_state": {},
      "parameters": {
        "H_plus": 0.0001,
        "p_HNO3": 1.0
      },
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
              "start": 273.15,
              "stop": 318.0,
              "count": 20,
              "scale": "linear"
            }
          }
        ]
      },
      "plots": [
        {
          "id": "H_HNO3_vs_T",
          "type": "line",
          "description": "H_HNO3(T) — flat line demonstrating temperature-independent HNO3 solubility (dH=0).",
          "x": {
            "variable": "T",
            "label": "Temperature (K)"
          },
          "y": {
            "variable": "H_HNO3",
            "label": "H_HNO3 (mol/(m³·Pa))"
          }
        }
      ]
    }
  ]
}
```

</details>
