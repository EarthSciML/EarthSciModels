---
title: "AqueousEquilibria"
slug: "aqueousequilibria"
domains: ["aerosol"]
component_types: ["model"]
subdomains: ["aq_eq"]
domain: "aerosol"
subdomain: "aq_eq"
component_type: "model"
esm_version: "1.0.0"
esm_path: "components/aerosol/aq_eq/all.esm"
reference: "Seinfeld, J. H., & Pandis, S. N. (2016). Atmospheric Chemistry and Physics: From Air Pollution to Climate Change, 3rd ed. Wiley. Chapter 7 (Eqs. 7.10–7.51) and Table 7.4. ISBN 978-1-118-94740-1."
description: "Coupled gas-aqueous chemical equilibrium for cloud droplets and aerosol water. Migrated from Aerosol.jl@c8c640bb src/aqueous_equilibria.jl:642. Composes WaterEquilibrium, CO2Equilibria, SO2Equilibria, NH3Equilibria, HNO3Equilibria, H2O2Equilibria, and O3Equilibria via a quadratic charge-balance approximation for H+. Reference: Seinfeld & Pandis (2016) Ch. 7 §7.3."
tags: ["aerosol", "aq_eq", "model", "aqueous_equilibria", "cloud_chemistry", "charge_balance", "seinfeld-pandis"]
---

## Description

Coupled gas-aqueous chemical equilibrium for cloud droplets and aerosol water. Migrated from Aerosol.jl@c8c640bb src/aqueous_equilibria.jl:642. Composes WaterEquilibrium, CO2Equilibria, SO2Equilibria, NH3Equilibria, HNO3Equilibria, H2O2Equilibria, and O3Equilibria via a quadratic charge-balance approximation for H+. Reference: Seinfeld & Pandis (2016) Ch. 7 §7.3.

## Reference

_source_ref: Aerosol.jl@c8c640bb:src/aqueous_equilibria.jl:642

Upstream `AqueousEquilibria` uses EarthSciML `coupling.couple` to compose seven sub-equilibria, adding the electroneutrality (charge-balance) equation:
  H+ + NH4+ = OH- + HCO3- + 2·CO3²- + HSO3- + 2·SO3²- + NO3- + HO2-

The upstream Julia MTK system uses structural_simplify to eliminate the implicit H+ cycle. The ESS algebraic solver cannot directly handle this implicit polynomial system (it requires a DAG-structured equation graph). Instead, this ESM uses a quadratic approximation that retains only the mono-anion terms (ignoring CO3²- and SO3²-):

  H+ = sqrt[(K_w + K_c1·CO2_aq + K_s1·SO2_aq + K_n1·HNO3_aq + K_h1·H2O2_aq) / (1 + K_a1·NH3_aq / K_w)]

Accuracy of the approximation:
- Valid for pH 4–7 where CO3²-/HCO3- = K_c2/H+ << 1 and SO3²-/HSO3- = K_s2/H+ << 1
- Error < 0.1% for CO2-only (pH 5.6), NH3-only, O3/H2O2 presence, and temperature sweeps
- Error < 0.5% for small SO2 at low pH (pH < 5)
- Error ~12% at pH 6.4 with significant SO2+NH3 (SO3²-/HSO3- ≈ 17%)

All van't Hoff constants and Henry's law constants are identical to the standalone sub-component ESMs (water.esm, co2.esm, so2.esm, nh3.esm, hno3.esm, h2o2.esm, o3.esm).

Tolerance rationale (model-level rel=1e-6): fully explicit DAG algebraic system. Each equation is a closed-form expression; rel=1e-6 covers float64 roundoff in the van't Hoff exponentials and the sqrt expression across the atmospheric ranges._

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `T` | `K` | `298.0` | Temperature. |
| `p_CO2` | `Pa` | `40.0` | Partial pressure of CO2 (≈ 400 ppm at 1 atm ≈ 40 Pa). |
| `p_SO2` | `Pa` | `0.0` | Partial pressure of SO2. |
| `p_NH3` | `Pa` | `0.0` | Partial pressure of NH3. |
| `p_HNO3` | `Pa` | `0.0` | Partial pressure of HNO3. |
| `p_H2O2` | `Pa` | `0.0` | Partial pressure of H2O2. |
| `p_O3` | `Pa` | `0.0` | Partial pressure of O3. |
| `R_gas` | `J/mol/K` | `8.314` | Gas constant. |
| `T_ref` | `K` | `298.0` | Reference temperature. |
| `C_ref` | `mol/m^3` | `1000.0` | Reference concentration for pH (1 mol/L = 1000 mol/m³). |
| `K_w_298` | `mol^2/m^6` | `1e-08` | Water dissociation constant at 298 K (1e-14 M² → mol²/m⁶). |
| `dH_Kw` | `J/mol` | `55856.4` | Enthalpy for K_w (13.35 kcal/mol; Seinfeld & Pandis Table 7.4). |
| `H_CO2_298` | `mol/m^3/Pa` | `0.0003355539106834444` | Henry constant for CO2 at 298 K (3.4e-2 M/atm → mol/m³/Pa). |
| `dH_H_CO2` | `J/mol` | `-20292.4` | Heat of dissolution for CO2 (-4.85 kcal/mol; Seinfeld & Pandis Table 7.4). |
| `K_c1_298` | `mol/m^3` | `0.00043` | K_c1 at 298 K (4.3e-7 M → mol/m³). |
| `K_c2_298` | `mol/m^3` | `4.7e-08` | K_c2 at 298 K (4.7e-11 M → mol/m³). |
| `dH_Kc1` | `J/mol` | `7657.12` | Enthalpy for K_c1 (upstream literal verbatim). |
| `dH_Kc2` | `J/mol` | `14853.2` | Enthalpy for K_c2 (3.55 kcal/mol). |
| `H_SO2_298` | `mol/m^3/Pa` | `0.012139156180606956` | Henry constant for SO2 at 298 K. |
| `dH_H_SO2` | `J/mol` | `-26150.0` | Heat of dissolution for SO2 (-6.25 kcal/mol; Seinfeld & Pandis Table 7.4). |
| `K_s1_298` | `mol/m^3` | `13.0` | K_s1 at 298 K (0.013 M → mol/m³). |
| `K_s2_298` | `mol/m^3` | `6.6e-05` | K_s2 at 298 K (6.6e-8 M → mol/m³). |
| `dH_Ks1` | `J/mol` | `-17405.44` | Enthalpy for K_s1 (-4.16 kcal/mol; Seinfeld & Pandis Table 7.4). |
| `dH_Ks2` | `J/mol` | `-9330.32` | Enthalpy for K_s2 (-2.23 kcal/mol; Seinfeld & Pandis Table 7.4). |
| `H_NH3_298` | `mol/m^3/Pa` | `0.611892425363928` | Henry constant for NH3 at 298 K (62.0 M/atm → mol/m³/Pa). |
| `dH_H_NH3` | `J/mol` | `-34183.28` | Heat of dissolution for NH3 (-8.17 kcal/mol; Seinfeld & Pandis Table 7.4). |
| `K_a1_298` | `mol/m^3` | `0.017` | NH3·H2O dissociation constant at 298 K (1.7e-5 M → mol/m³). |
| `dH_Ka1` | `J/mol` | `36191.6` | Enthalpy for K_a1 (8.65 kcal/mol; Seinfeld & Pandis Table 7.4). |
| `H_HNO3_298` | `mol/m^3/Pa` | `2072.53886010363` | Henry constant for HNO3 at 298 K (2.1e5 M/atm → mol/m³/Pa). |
| `dH_H_HNO3` | `J/mol` | `0.0` | Heat of dissolution for HNO3 (temperature-independent; Seinfeld & Pandis Table 7.4). |
| `K_n1_298` | `mol/m^3` | `15400.0` | HNO3 dissociation constant (15.4 M → mol/m³; strong acid, temperature-independent). |
| `H_H2O2_298` | `mol/m^3/Pa` | `986.9232667160128` | Henry constant for H2O2 at 298 K (1.0e5 M/atm → mol/m³/Pa). |
| `dH_H_H2O2` | `J/mol` | `-60668.0` | Heat of dissolution for H2O2 (-14.5 kcal/mol; Seinfeld & Pandis Table 7.4). |
| `K_h1_298` | `mol/m^3` | `2.2e-09` | H2O2 dissociation constant at 298 K (2.2e-12 M → mol/m³; temperature-independent). |
| `H_O3_298` | `mol/m^3/Pa` | `0.0001085615593387614` | Henry constant for O3 at 298 K (1.1e-2 M/atm → mol/m³/Pa). |
| `dH_H_O3` | `J/mol` | `-21087.36` | Heat of dissolution for O3 (-5.04 kcal/mol; Seinfeld & Pandis Table 7.4). |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `K_w` | `mol^2/m^6` |  | Water dissociation constant K_w(T) via van't Hoff (Seinfeld & Pandis Eq 7.10). |
| `H_CO2` | `mol/m^3/Pa` |  | Henry's law constant for CO2 at temperature T. |
| `K_c1` | `mol/m^3` |  | CO2 first dissociation constant K_c1(T). |
| `K_c2` | `mol/m^3` |  | CO2 second dissociation constant K_c2(T). |
| `CO2_aq` | `mol/m^3` |  | Aqueous CO2 concentration [CO2·H2O]. |
| `H_SO2` | `mol/m^3/Pa` |  | Henry's law constant for SO2 at temperature T. |
| `K_s1` | `mol/m^3` |  | SO2 first dissociation constant K_s1(T). |
| `K_s2` | `mol/m^3` |  | SO2 second dissociation constant K_s2(T). |
| `SO2_aq` | `mol/m^3` |  | Aqueous SO2 concentration [SO2·H2O]. |
| `H_NH3` | `mol/m^3/Pa` |  | Henry's law constant for NH3 at temperature T. |
| `K_a1` | `mol/m^3` |  | NH3·H2O dissociation constant K_a1(T). |
| `NH3_aq` | `mol/m^3` |  | Aqueous NH3 concentration [NH3·H2O]. |
| `H_HNO3` | `mol/m^3/Pa` |  | Henry's law constant for HNO3 (≈ H_HNO3_298, dH≈0). |
| `K_n1` | `mol/m^3` |  | HNO3 dissociation constant (= K_n1_298; strong acid, temperature-independent). |
| `HNO3_aq` | `mol/m^3` |  | Undissociated HNO3 concentration [HNO3(aq)]. |
| `H_H2O2` | `mol/m^3/Pa` |  | Henry's law constant for H2O2 at temperature T. |
| `K_h1` | `mol/m^3` |  | H2O2 dissociation constant (= K_h1_298; temperature-independent). |
| `H2O2_aq` | `mol/m^3` |  | Aqueous H2O2 concentration. |
| `H_O3` | `mol/m^3/Pa` |  | Henry's law constant for O3 at temperature T. |
| `O3_aq` | `mol/m^3` |  | Aqueous O3 concentration. |
| `H_plus` | `mol/m^3` |  | Hydrogen ion concentration solved by the quadratic charge-balance approximation. See reference notes for the accuracy bounds. |
| `OH_minus` | `mol/m^3` |  | Hydroxide ion concentration [OH-]. |
| `pH` | `1` |  | pH = -log10([H+] / C_ref). |
| `HCO3_minus` | `mol/m^3` |  | Bicarbonate concentration [HCO3-]. |
| `CO3_2minus` | `mol/m^3` |  | Carbonate concentration [CO3²-]. |
| `C_total` | `mol/m^3` |  | Total dissolved inorganic carbon (CO2_aq + HCO3- + CO3²-). |
| `H_CO2_eff` | `mol/m^3/Pa` |  | Effective Henry constant for CO2 (S&P Eq 7.24). |
| `HSO3_minus` | `mol/m^3` |  | Bisulfite concentration [HSO3-]. |
| `SO3_2minus` | `mol/m^3` |  | Sulfite concentration [SO3²-]. |
| `S_IV_total` | `mol/m^3` |  | Total S(IV) concentration (SO2_aq + HSO3- + SO3²-). |
| `H_SO2_eff` | `mol/m^3/Pa` |  | Effective Henry constant for SO2. |
| `alpha_0` | `1` |  | Fraction of S(IV) as SO2(aq). |
| `alpha_1` | `1` |  | Fraction of S(IV) as HSO3-. |
| `alpha_2` | `1` |  | Fraction of S(IV) as SO3²-. |
| `NH4_plus` | `mol/m^3` |  | Ammonium concentration [NH4+]. |
| `NH3_total` | `mol/m^3` |  | Total dissolved ammonia (NH3_aq + NH4+). |
| `H_NH3_eff` | `mol/m^3/Pa` |  | Effective Henry constant for NH3. |
| `NO3_minus` | `mol/m^3` |  | Nitrate concentration [NO3-]. |
| `HNO3_total` | `mol/m^3` |  | Total dissolved nitric acid. |
| `H_HNO3_eff` | `mol/m^3/Pa` |  | Effective Henry constant for HNO3. |
| `HO2_minus` | `mol/m^3` |  | Peroxide anion concentration [HO2-]. |
| `H2O2_total` | `mol/m^3` |  | Total dissolved H2O2. |
| `H_H2O2_eff` | `mol/m^3/Pa` |  | Effective Henry constant for H2O2. |

## Observed expressions

$$
K_{w} = K_{w\,298} \cdot e^{\left(-1\right) \cdot \frac{dH_{Kw}}{R_{gas}} \cdot \left(\frac{1}{T} + \frac{-1}{T_{ref}}\right)}
$$
_Water dissociation constant K_w(T) via van't Hoff (Seinfeld & Pandis Eq 7.10)._

$$
H_{CO2} = H_{CO2\,298} \cdot e^{\frac{dH_{H\,CO2}}{R_{gas}} \cdot \left(\frac{1}{T_{ref}} + \frac{-1}{T}\right)}
$$
_Henry's law constant for CO2 at temperature T._

$$
K_{c1} = K_{c1\,298} \cdot e^{\left(-1\right) \cdot \frac{dH_{Kc1}}{R_{gas}} \cdot \left(\frac{1}{T} + \frac{-1}{T_{ref}}\right)}
$$
_CO2 first dissociation constant K_c1(T)._

$$
K_{c2} = K_{c2\,298} \cdot e^{\left(-1\right) \cdot \frac{dH_{Kc2}}{R_{gas}} \cdot \left(\frac{1}{T} + \frac{-1}{T_{ref}}\right)}
$$
_CO2 second dissociation constant K_c2(T)._

$$
CO2_{aq} = H_{CO2} \cdot p_{CO2}
$$
_Aqueous CO2 concentration [CO2·H2O]._

$$
H_{SO2} = H_{SO2\,298} \cdot e^{\frac{dH_{H\,SO2}}{R_{gas}} \cdot \left(\frac{1}{T_{ref}} + \frac{-1}{T}\right)}
$$
_Henry's law constant for SO2 at temperature T._

$$
K_{s1} = K_{s1\,298} \cdot e^{\left(-1\right) \cdot \frac{dH_{Ks1}}{R_{gas}} \cdot \left(\frac{1}{T} + \frac{-1}{T_{ref}}\right)}
$$
_SO2 first dissociation constant K_s1(T)._

$$
K_{s2} = K_{s2\,298} \cdot e^{\left(-1\right) \cdot \frac{dH_{Ks2}}{R_{gas}} \cdot \left(\frac{1}{T} + \frac{-1}{T_{ref}}\right)}
$$
_SO2 second dissociation constant K_s2(T)._

$$
SO2_{aq} = H_{SO2} \cdot p_{SO2}
$$
_Aqueous SO2 concentration [SO2·H2O]._

$$
H_{NH3} = H_{NH3\,298} \cdot e^{\frac{dH_{H\,NH3}}{R_{gas}} \cdot \left(\frac{1}{T_{ref}} + \frac{-1}{T}\right)}
$$
_Henry's law constant for NH3 at temperature T._

$$
K_{a1} = K_{a1\,298} \cdot e^{\left(-1\right) \cdot \frac{dH_{Ka1}}{R_{gas}} \cdot \left(\frac{1}{T} + \frac{-1}{T_{ref}}\right)}
$$
_NH3·H2O dissociation constant K_a1(T)._

$$
NH3_{aq} = H_{NH3} \cdot p_{NH3}
$$
_Aqueous NH3 concentration [NH3·H2O]._

$$
H_{HNO3} = H_{HNO3\,298} \cdot e^{\frac{dH_{H\,HNO3}}{R_{gas}} \cdot \left(\frac{1}{T_{ref}} + \frac{-1}{T}\right)}
$$
_Henry's law constant for HNO3 (≈ H_HNO3_298, dH≈0)._

$$
K_{n1} = K_{n1\,298}
$$
_HNO3 dissociation constant (= K_n1_298; strong acid, temperature-independent)._

$$
HNO3_{aq} = H_{HNO3} \cdot p_{HNO3}
$$
_Undissociated HNO3 concentration [HNO3(aq)]._

$$
H_{H2O2} = H_{H2O2\,298} \cdot e^{\frac{dH_{H\,H2O2}}{R_{gas}} \cdot \left(\frac{1}{T_{ref}} + \frac{-1}{T}\right)}
$$
_Henry's law constant for H2O2 at temperature T._

$$
K_{h1} = K_{h1\,298}
$$
_H2O2 dissociation constant (= K_h1_298; temperature-independent)._

$$
H2O2_{aq} = H_{H2O2} \cdot p_{H2O2}
$$
_Aqueous H2O2 concentration._

$$
H_{O3} = H_{O3\,298} \cdot e^{\frac{dH_{H\,O3} \cdot \left(\frac{1}{T_{ref}} + \frac{-1}{T}\right)}{R_{gas}}}
$$
_Henry's law constant for O3 at temperature T._

$$
O3_{aq} = H_{O3} \cdot p_{O3}
$$
_Aqueous O3 concentration._

$$
H_{plus} = \frac{K_{w} + K_{c1} \cdot CO2_{aq} + K_{s1} \cdot SO2_{aq} + K_{n1} \cdot HNO3_{aq} + K_{h1} \cdot H2O2_{aq}}{1 + \frac{K_{a1} \cdot NH3_{aq}}{K_{w}}}^{0.5}
$$
_Hydrogen ion concentration solved by the quadratic charge-balance approximation. See reference notes for the accuracy bounds._

$$
OH_{minus} = \frac{K_{w}}{H_{plus}}
$$
_Hydroxide ion concentration [OH-]._

$$
pH = \left(-1\right) \cdot \log_{10}\left(\frac{H_{plus}}{C_{ref}}\right)
$$
_pH = -log10([H+] / C_ref)._

$$
HCO3_{minus} = \frac{K_{c1} \cdot CO2_{aq}}{H_{plus}}
$$
_Bicarbonate concentration [HCO3-]._

$$
CO3_{2minus} = \frac{K_{c2} \cdot HCO3_{minus}}{H_{plus}}
$$
_Carbonate concentration [CO3²-]._

$$
C_{total} = CO2_{aq} + HCO3_{minus} + CO3_{2minus}
$$
_Total dissolved inorganic carbon (CO2_aq + HCO3- + CO3²-)._

$$
H_{CO2\,eff} = H_{CO2} \cdot \left(1 + \frac{K_{c1}}{H_{plus}} + \frac{K_{c1} \cdot K_{c2}}{H_{plus}^{2}}\right)
$$
_Effective Henry constant for CO2 (S&P Eq 7.24)._

$$
HSO3_{minus} = \frac{K_{s1} \cdot SO2_{aq}}{H_{plus}}
$$
_Bisulfite concentration [HSO3-]._

$$
SO3_{2minus} = \frac{K_{s2} \cdot HSO3_{minus}}{H_{plus}}
$$
_Sulfite concentration [SO3²-]._

$$
S_{IV\,total} = SO2_{aq} + HSO3_{minus} + SO3_{2minus}
$$
_Total S(IV) concentration (SO2_aq + HSO3- + SO3²-)._

$$
H_{SO2\,eff} = H_{SO2} \cdot \left(1 + \frac{K_{s1}}{H_{plus}} + \frac{K_{s1} \cdot K_{s2}}{H_{plus}^{2}}\right)
$$
_Effective Henry constant for SO2._

$$
alpha_{0} = \frac{H_{plus}^{2}}{H_{plus}^{2} + K_{s1} \cdot H_{plus} + K_{s1} \cdot K_{s2}}
$$
_Fraction of S(IV) as SO2(aq)._

$$
alpha_{1} = \frac{K_{s1} \cdot H_{plus}}{H_{plus}^{2} + K_{s1} \cdot H_{plus} + K_{s1} \cdot K_{s2}}
$$
_Fraction of S(IV) as HSO3-._

$$
alpha_{2} = \frac{K_{s1} \cdot K_{s2}}{H_{plus}^{2} + K_{s1} \cdot H_{plus} + K_{s1} \cdot K_{s2}}
$$
_Fraction of S(IV) as SO3²-._

$$
NH4_{plus} = \frac{K_{a1} \cdot NH3_{aq}}{OH_{minus}}
$$
_Ammonium concentration [NH4+]._

$$
NH3_{total} = NH3_{aq} + NH4_{plus}
$$
_Total dissolved ammonia (NH3_aq + NH4+)._

$$
H_{NH3\,eff} = H_{NH3} \cdot \left(1 + \frac{K_{a1} \cdot H_{plus}}{K_{w}}\right)
$$
_Effective Henry constant for NH3._

$$
NO3_{minus} = \frac{K_{n1} \cdot HNO3_{aq}}{H_{plus}}
$$
_Nitrate concentration [NO3-]._

$$
HNO3_{total} = HNO3_{aq} + NO3_{minus}
$$
_Total dissolved nitric acid._

$$
H_{HNO3\,eff} = H_{HNO3} \cdot \left(1 + \frac{K_{n1}}{H_{plus}}\right)
$$
_Effective Henry constant for HNO3._

$$
HO2_{minus} = \frac{K_{h1} \cdot H2O2_{aq}}{H_{plus}}
$$
_Peroxide anion concentration [HO2-]._

$$
H2O2_{total} = H2O2_{aq} + HO2_{minus}
$$
_Total dissolved H2O2._

$$
H_{H2O2\,eff} = H_{H2O2} \cdot \left(1 + \frac{K_{h1}}{H_{plus}}\right)
$$
_Effective Henry constant for H2O2._

## Analyses

### ph_vs_temperature_co2_only

pH of CO2-only cloud water vs temperature (273-318 K). Higher T decreases CO2 solubility (raising pH); K_w change is secondary. Net effect: pH increases slightly with T.

**Time span:** 0.0 → 1.0

**Swept over:** `T`

![pH vs temperature for CO2-only cloud water.](/plots/aerosol/aq_eq/aqueousequilibria/ph_vs_temperature_co2_only-ph_vs_T.png)

![(HCO3-) vs temperature at p_CO2=40 Pa.](/plots/aerosol/aq_eq/aqueousequilibria/ph_vs_temperature_co2_only-hco3_vs_T.png)

### ph_vs_p_SO2

SO2 acidification curve: pH vs p_SO2 at 298 K with p_CO2=40 Pa background. Transition from CO2-dominated (pH 5.6) to SO2-dominated (pH < 4) regimes.

**Time span:** 0.0 → 1.0

**Swept over:** `p_SO2`

![pH vs p_SO2 showing SO2 acidification.](/plots/aerosol/aq_eq/aqueousequilibria/ph_vs_p_SO2-ph_vs_pSO2.png)

![(S(IV)) vs p_SO2.](/plots/aerosol/aq_eq/aqueousequilibria/ph_vs_p_SO2-SIV_vs_pSO2.png)

### ph_vs_p_NH3

NH3 buffering curve: pH vs p_NH3 at 298 K with p_CO2=40 Pa background. NH3 forms NH4+ and OH-, raising pH from 5.6 toward 7.

**Time span:** 0.0 → 1.0

**Swept over:** `p_NH3`

![pH vs p_NH3 showing NH3 buffering.](/plots/aerosol/aq_eq/aqueousequilibria/ph_vs_p_NH3-ph_vs_pNH3.png)

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "reference": {
    "notes": "source_ref: Aerosol.jl@c8c640bb:src/aqueous_equilibria.jl:642\n\nUpstream `AqueousEquilibria` uses EarthSciML `coupling.couple` to compose seven sub-equilibria, adding the electroneutrality (charge-balance) equation:\n  H+ + NH4+ = OH- + HCO3- + 2·CO3²- + HSO3- + 2·SO3²- + NO3- + HO2-\n\nThe upstream Julia MTK system uses structural_simplify to eliminate the implicit H+ cycle. The ESS algebraic solver cannot directly handle this implicit polynomial system (it requires a DAG-structured equation graph). Instead, this ESM uses a quadratic approximation that retains only the mono-anion terms (ignoring CO3²- and SO3²-):\n\n  H+ = sqrt[(K_w + K_c1·CO2_aq + K_s1·SO2_aq + K_n1·HNO3_aq + K_h1·H2O2_aq) / (1 + K_a1·NH3_aq / K_w)]\n\nAccuracy of the approximation:\n- Valid for pH 4–7 where CO3²-/HCO3- = K_c2/H+ << 1 and SO3²-/HSO3- = K_s2/H+ << 1\n- Error < 0.1% for CO2-only (pH 5.6), NH3-only, O3/H2O2 presence, and temperature sweeps\n- Error < 0.5% for small SO2 at low pH (pH < 5)\n- Error ~12% at pH 6.4 with significant SO2+NH3 (SO3²-/HSO3- ≈ 17%)\n\nAll van't Hoff constants and Henry's law constants are identical to the standalone sub-component ESMs (water.esm, co2.esm, so2.esm, nh3.esm, hno3.esm, h2o2.esm, o3.esm).\n\nTolerance rationale (model-level rel=1e-6): fully explicit DAG algebraic system. Each equation is a closed-form expression; rel=1e-6 covers float64 roundoff in the van't Hoff exponentials and the sqrt expression across the atmospheric ranges."
  },
  "tolerance": {
    "rel": 1e-06
  },
  "variables": {
    "T": {
      "type": "parameter",
      "units": "K",
      "default": 298.0,
      "description": "Temperature."
    },
    "p_CO2": {
      "type": "parameter",
      "units": "Pa",
      "default": 40.0,
      "description": "Partial pressure of CO2 (≈ 400 ppm at 1 atm ≈ 40 Pa)."
    },
    "p_SO2": {
      "type": "parameter",
      "units": "Pa",
      "default": 0.0,
      "description": "Partial pressure of SO2."
    },
    "p_NH3": {
      "type": "parameter",
      "units": "Pa",
      "default": 0.0,
      "description": "Partial pressure of NH3."
    },
    "p_HNO3": {
      "type": "parameter",
      "units": "Pa",
      "default": 0.0,
      "description": "Partial pressure of HNO3."
    },
    "p_H2O2": {
      "type": "parameter",
      "units": "Pa",
      "default": 0.0,
      "description": "Partial pressure of H2O2."
    },
    "p_O3": {
      "type": "parameter",
      "units": "Pa",
      "default": 0.0,
      "description": "Partial pressure of O3."
    },
    "R_gas": {
      "type": "parameter",
      "units": "J/mol/K",
      "default": 8.314,
      "description": "Gas constant."
    },
    "T_ref": {
      "type": "parameter",
      "units": "K",
      "default": 298.0,
      "description": "Reference temperature."
    },
    "C_ref": {
      "type": "parameter",
      "units": "mol/m^3",
      "default": 1000.0,
      "description": "Reference concentration for pH (1 mol/L = 1000 mol/m³)."
    },
    "K_w_298": {
      "type": "parameter",
      "units": "mol^2/m^6",
      "default": 1e-08,
      "description": "Water dissociation constant at 298 K (1e-14 M² → mol²/m⁶)."
    },
    "dH_Kw": {
      "type": "parameter",
      "units": "J/mol",
      "default": 55856.4,
      "description": "Enthalpy for K_w (13.35 kcal/mol; Seinfeld & Pandis Table 7.4)."
    },
    "H_CO2_298": {
      "type": "parameter",
      "units": "mol/m^3/Pa",
      "default": 0.0003355539106834444,
      "description": "Henry constant for CO2 at 298 K (3.4e-2 M/atm → mol/m³/Pa)."
    },
    "dH_H_CO2": {
      "type": "parameter",
      "units": "J/mol",
      "default": -20292.4,
      "description": "Heat of dissolution for CO2 (-4.85 kcal/mol; Seinfeld & Pandis Table 7.4)."
    },
    "K_c1_298": {
      "type": "parameter",
      "units": "mol/m^3",
      "default": 0.00043,
      "description": "K_c1 at 298 K (4.3e-7 M → mol/m³)."
    },
    "K_c2_298": {
      "type": "parameter",
      "units": "mol/m^3",
      "default": 4.7e-08,
      "description": "K_c2 at 298 K (4.7e-11 M → mol/m³)."
    },
    "dH_Kc1": {
      "type": "parameter",
      "units": "J/mol",
      "default": 7657.12,
      "description": "Enthalpy for K_c1 (upstream literal verbatim)."
    },
    "dH_Kc2": {
      "type": "parameter",
      "units": "J/mol",
      "default": 14853.2,
      "description": "Enthalpy for K_c2 (3.55 kcal/mol)."
    },
    "H_SO2_298": {
      "type": "parameter",
      "units": "mol/m^3/Pa",
      "default": 0.012139156180606956,
      "description": "Henry constant for SO2 at 298 K."
    },
    "dH_H_SO2": {
      "type": "parameter",
      "units": "J/mol",
      "default": -26150.0,
      "description": "Heat of dissolution for SO2 (-6.25 kcal/mol; Seinfeld & Pandis Table 7.4)."
    },
    "K_s1_298": {
      "type": "parameter",
      "units": "mol/m^3",
      "default": 13.0,
      "description": "K_s1 at 298 K (0.013 M → mol/m³)."
    },
    "K_s2_298": {
      "type": "parameter",
      "units": "mol/m^3",
      "default": 6.6e-05,
      "description": "K_s2 at 298 K (6.6e-8 M → mol/m³)."
    },
    "dH_Ks1": {
      "type": "parameter",
      "units": "J/mol",
      "default": -17405.44,
      "description": "Enthalpy for K_s1 (-4.16 kcal/mol; Seinfeld & Pandis Table 7.4)."
    },
    "dH_Ks2": {
      "type": "parameter",
      "units": "J/mol",
      "default": -9330.32,
      "description": "Enthalpy for K_s2 (-2.23 kcal/mol; Seinfeld & Pandis Table 7.4)."
    },
    "H_NH3_298": {
      "type": "parameter",
      "units": "mol/m^3/Pa",
      "default": 0.611892425363928,
      "description": "Henry constant for NH3 at 298 K (62.0 M/atm → mol/m³/Pa)."
    },
    "dH_H_NH3": {
      "type": "parameter",
      "units": "J/mol",
      "default": -34183.28,
      "description": "Heat of dissolution for NH3 (-8.17 kcal/mol; Seinfeld & Pandis Table 7.4)."
    },
    "K_a1_298": {
      "type": "parameter",
      "units": "mol/m^3",
      "default": 0.017,
      "description": "NH3·H2O dissociation constant at 298 K (1.7e-5 M → mol/m³)."
    },
    "dH_Ka1": {
      "type": "parameter",
      "units": "J/mol",
      "default": 36191.6,
      "description": "Enthalpy for K_a1 (8.65 kcal/mol; Seinfeld & Pandis Table 7.4)."
    },
    "H_HNO3_298": {
      "type": "parameter",
      "units": "mol/m^3/Pa",
      "default": 2072.53886010363,
      "description": "Henry constant for HNO3 at 298 K (2.1e5 M/atm → mol/m³/Pa)."
    },
    "dH_H_HNO3": {
      "type": "parameter",
      "units": "J/mol",
      "default": 0.0,
      "description": "Heat of dissolution for HNO3 (temperature-independent; Seinfeld & Pandis Table 7.4)."
    },
    "K_n1_298": {
      "type": "parameter",
      "units": "mol/m^3",
      "default": 15400.0,
      "description": "HNO3 dissociation constant (15.4 M → mol/m³; strong acid, temperature-independent)."
    },
    "H_H2O2_298": {
      "type": "parameter",
      "units": "mol/m^3/Pa",
      "default": 986.9232667160128,
      "description": "Henry constant for H2O2 at 298 K (1.0e5 M/atm → mol/m³/Pa)."
    },
    "dH_H_H2O2": {
      "type": "parameter",
      "units": "J/mol",
      "default": -60668.0,
      "description": "Heat of dissolution for H2O2 (-14.5 kcal/mol; Seinfeld & Pandis Table 7.4)."
    },
    "K_h1_298": {
      "type": "parameter",
      "units": "mol/m^3",
      "default": 2.2e-09,
      "description": "H2O2 dissociation constant at 298 K (2.2e-12 M → mol/m³; temperature-independent)."
    },
    "H_O3_298": {
      "type": "parameter",
      "units": "mol/m^3/Pa",
      "default": 0.0001085615593387614,
      "description": "Henry constant for O3 at 298 K (1.1e-2 M/atm → mol/m³/Pa)."
    },
    "dH_H_O3": {
      "type": "parameter",
      "units": "J/mol",
      "default": -21087.36,
      "description": "Heat of dissolution for O3 (-5.04 kcal/mol; Seinfeld & Pandis Table 7.4)."
    },
    "K_w": {
      "type": "unknown",
      "units": "mol^2/m^6",
      "description": "Water dissociation constant K_w(T) via van't Hoff (Seinfeld & Pandis Eq 7.10)."
    },
    "H_CO2": {
      "type": "unknown",
      "units": "mol/m^3/Pa",
      "description": "Henry's law constant for CO2 at temperature T."
    },
    "K_c1": {
      "type": "unknown",
      "units": "mol/m^3",
      "description": "CO2 first dissociation constant K_c1(T)."
    },
    "K_c2": {
      "type": "unknown",
      "units": "mol/m^3",
      "description": "CO2 second dissociation constant K_c2(T)."
    },
    "CO2_aq": {
      "type": "unknown",
      "units": "mol/m^3",
      "description": "Aqueous CO2 concentration [CO2·H2O]."
    },
    "H_SO2": {
      "type": "unknown",
      "units": "mol/m^3/Pa",
      "description": "Henry's law constant for SO2 at temperature T."
    },
    "K_s1": {
      "type": "unknown",
      "units": "mol/m^3",
      "description": "SO2 first dissociation constant K_s1(T)."
    },
    "K_s2": {
      "type": "unknown",
      "units": "mol/m^3",
      "description": "SO2 second dissociation constant K_s2(T)."
    },
    "SO2_aq": {
      "type": "unknown",
      "units": "mol/m^3",
      "description": "Aqueous SO2 concentration [SO2·H2O]."
    },
    "H_NH3": {
      "type": "unknown",
      "units": "mol/m^3/Pa",
      "description": "Henry's law constant for NH3 at temperature T."
    },
    "K_a1": {
      "type": "unknown",
      "units": "mol/m^3",
      "description": "NH3·H2O dissociation constant K_a1(T)."
    },
    "NH3_aq": {
      "type": "unknown",
      "units": "mol/m^3",
      "description": "Aqueous NH3 concentration [NH3·H2O]."
    },
    "H_HNO3": {
      "type": "unknown",
      "units": "mol/m^3/Pa",
      "description": "Henry's law constant for HNO3 (≈ H_HNO3_298, dH≈0)."
    },
    "K_n1": {
      "type": "unknown",
      "units": "mol/m^3",
      "description": "HNO3 dissociation constant (= K_n1_298; strong acid, temperature-independent)."
    },
    "HNO3_aq": {
      "type": "unknown",
      "units": "mol/m^3",
      "description": "Undissociated HNO3 concentration [HNO3(aq)]."
    },
    "H_H2O2": {
      "type": "unknown",
      "units": "mol/m^3/Pa",
      "description": "Henry's law constant for H2O2 at temperature T."
    },
    "K_h1": {
      "type": "unknown",
      "units": "mol/m^3",
      "description": "H2O2 dissociation constant (= K_h1_298; temperature-independent)."
    },
    "H2O2_aq": {
      "type": "unknown",
      "units": "mol/m^3",
      "description": "Aqueous H2O2 concentration."
    },
    "H_O3": {
      "type": "unknown",
      "units": "mol/m^3/Pa",
      "description": "Henry's law constant for O3 at temperature T."
    },
    "O3_aq": {
      "type": "unknown",
      "units": "mol/m^3",
      "description": "Aqueous O3 concentration."
    },
    "H_plus": {
      "type": "unknown",
      "units": "mol/m^3",
      "description": "Hydrogen ion concentration solved by the quadratic charge-balance approximation. See reference notes for the accuracy bounds."
    },
    "OH_minus": {
      "type": "unknown",
      "units": "mol/m^3",
      "description": "Hydroxide ion concentration [OH-]."
    },
    "pH": {
      "type": "unknown",
      "units": "1",
      "description": "pH = -log10([H+] / C_ref)."
    },
    "HCO3_minus": {
      "type": "unknown",
      "units": "mol/m^3",
      "description": "Bicarbonate concentration [HCO3-]."
    },
    "CO3_2minus": {
      "type": "unknown",
      "units": "mol/m^3",
      "description": "Carbonate concentration [CO3²-]."
    },
    "C_total": {
      "type": "unknown",
      "units": "mol/m^3",
      "description": "Total dissolved inorganic carbon (CO2_aq + HCO3- + CO3²-)."
    },
    "H_CO2_eff": {
      "type": "unknown",
      "units": "mol/m^3/Pa",
      "description": "Effective Henry constant for CO2 (S&P Eq 7.24)."
    },
    "HSO3_minus": {
      "type": "unknown",
      "units": "mol/m^3",
      "description": "Bisulfite concentration [HSO3-]."
    },
    "SO3_2minus": {
      "type": "unknown",
      "units": "mol/m^3",
      "description": "Sulfite concentration [SO3²-]."
    },
    "S_IV_total": {
      "type": "unknown",
      "units": "mol/m^3",
      "description": "Total S(IV) concentration (SO2_aq + HSO3- + SO3²-)."
    },
    "H_SO2_eff": {
      "type": "unknown",
      "units": "mol/m^3/Pa",
      "description": "Effective Henry constant for SO2."
    },
    "alpha_0": {
      "type": "unknown",
      "units": "1",
      "description": "Fraction of S(IV) as SO2(aq)."
    },
    "alpha_1": {
      "type": "unknown",
      "units": "1",
      "description": "Fraction of S(IV) as HSO3-."
    },
    "alpha_2": {
      "type": "unknown",
      "units": "1",
      "description": "Fraction of S(IV) as SO3²-."
    },
    "NH4_plus": {
      "type": "unknown",
      "units": "mol/m^3",
      "description": "Ammonium concentration [NH4+]."
    },
    "NH3_total": {
      "type": "unknown",
      "units": "mol/m^3",
      "description": "Total dissolved ammonia (NH3_aq + NH4+)."
    },
    "H_NH3_eff": {
      "type": "unknown",
      "units": "mol/m^3/Pa",
      "description": "Effective Henry constant for NH3."
    },
    "NO3_minus": {
      "type": "unknown",
      "units": "mol/m^3",
      "description": "Nitrate concentration [NO3-]."
    },
    "HNO3_total": {
      "type": "unknown",
      "units": "mol/m^3",
      "description": "Total dissolved nitric acid."
    },
    "H_HNO3_eff": {
      "type": "unknown",
      "units": "mol/m^3/Pa",
      "description": "Effective Henry constant for HNO3."
    },
    "HO2_minus": {
      "type": "unknown",
      "units": "mol/m^3",
      "description": "Peroxide anion concentration [HO2-]."
    },
    "H2O2_total": {
      "type": "unknown",
      "units": "mol/m^3",
      "description": "Total dissolved H2O2."
    },
    "H_H2O2_eff": {
      "type": "unknown",
      "units": "mol/m^3/Pa",
      "description": "Effective Henry constant for H2O2."
    }
  },
  "equations": [
    {
      "lhs": "K_w",
      "rhs": {
        "op": "*",
        "args": [
          "K_w_298",
          {
            "op": "exp",
            "args": [
              {
                "op": "*",
                "args": [
                  -1,
                  {
                    "op": "/",
                    "args": [
                      "dH_Kw",
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
                          "T"
                        ]
                      },
                      {
                        "op": "/",
                        "args": [
                          -1,
                          "T_ref"
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
      "lhs": "H_CO2",
      "rhs": {
        "op": "*",
        "args": [
          "H_CO2_298",
          {
            "op": "exp",
            "args": [
              {
                "op": "*",
                "args": [
                  {
                    "op": "/",
                    "args": [
                      "dH_H_CO2",
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
      "lhs": "K_c1",
      "rhs": {
        "op": "*",
        "args": [
          "K_c1_298",
          {
            "op": "exp",
            "args": [
              {
                "op": "*",
                "args": [
                  -1,
                  {
                    "op": "/",
                    "args": [
                      "dH_Kc1",
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
                          "T"
                        ]
                      },
                      {
                        "op": "/",
                        "args": [
                          -1,
                          "T_ref"
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
      "lhs": "K_c2",
      "rhs": {
        "op": "*",
        "args": [
          "K_c2_298",
          {
            "op": "exp",
            "args": [
              {
                "op": "*",
                "args": [
                  -1,
                  {
                    "op": "/",
                    "args": [
                      "dH_Kc2",
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
                          "T"
                        ]
                      },
                      {
                        "op": "/",
                        "args": [
                          -1,
                          "T_ref"
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
      "lhs": "CO2_aq",
      "rhs": {
        "op": "*",
        "args": [
          "H_CO2",
          "p_CO2"
        ]
      }
    },
    {
      "lhs": "H_SO2",
      "rhs": {
        "op": "*",
        "args": [
          "H_SO2_298",
          {
            "op": "exp",
            "args": [
              {
                "op": "*",
                "args": [
                  {
                    "op": "/",
                    "args": [
                      "dH_H_SO2",
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
      "lhs": "K_s1",
      "rhs": {
        "op": "*",
        "args": [
          "K_s1_298",
          {
            "op": "exp",
            "args": [
              {
                "op": "*",
                "args": [
                  -1,
                  {
                    "op": "/",
                    "args": [
                      "dH_Ks1",
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
                          "T"
                        ]
                      },
                      {
                        "op": "/",
                        "args": [
                          -1,
                          "T_ref"
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
      "lhs": "K_s2",
      "rhs": {
        "op": "*",
        "args": [
          "K_s2_298",
          {
            "op": "exp",
            "args": [
              {
                "op": "*",
                "args": [
                  -1,
                  {
                    "op": "/",
                    "args": [
                      "dH_Ks2",
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
                          "T"
                        ]
                      },
                      {
                        "op": "/",
                        "args": [
                          -1,
                          "T_ref"
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
      "lhs": "SO2_aq",
      "rhs": {
        "op": "*",
        "args": [
          "H_SO2",
          "p_SO2"
        ]
      }
    },
    {
      "lhs": "H_NH3",
      "rhs": {
        "op": "*",
        "args": [
          "H_NH3_298",
          {
            "op": "exp",
            "args": [
              {
                "op": "*",
                "args": [
                  {
                    "op": "/",
                    "args": [
                      "dH_H_NH3",
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
      "lhs": "K_a1",
      "rhs": {
        "op": "*",
        "args": [
          "K_a1_298",
          {
            "op": "exp",
            "args": [
              {
                "op": "*",
                "args": [
                  -1,
                  {
                    "op": "/",
                    "args": [
                      "dH_Ka1",
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
                          "T"
                        ]
                      },
                      {
                        "op": "/",
                        "args": [
                          -1,
                          "T_ref"
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
      "lhs": "NH3_aq",
      "rhs": {
        "op": "*",
        "args": [
          "H_NH3",
          "p_NH3"
        ]
      }
    },
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
      "lhs": "H_H2O2",
      "rhs": {
        "op": "*",
        "args": [
          "H_H2O2_298",
          {
            "op": "exp",
            "args": [
              {
                "op": "*",
                "args": [
                  {
                    "op": "/",
                    "args": [
                      "dH_H_H2O2",
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
      "lhs": "K_h1",
      "rhs": "K_h1_298"
    },
    {
      "lhs": "H2O2_aq",
      "rhs": {
        "op": "*",
        "args": [
          "H_H2O2",
          "p_H2O2"
        ]
      }
    },
    {
      "lhs": "H_O3",
      "rhs": {
        "op": "*",
        "args": [
          "H_O3_298",
          {
            "op": "exp",
            "args": [
              {
                "op": "/",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      "dH_H_O3",
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
                  },
                  "R_gas"
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "O3_aq",
      "rhs": {
        "op": "*",
        "args": [
          "H_O3",
          "p_O3"
        ]
      }
    },
    {
      "lhs": "H_plus",
      "rhs": {
        "op": "^",
        "args": [
          {
            "op": "/",
            "args": [
              {
                "op": "+",
                "args": [
                  "K_w",
                  {
                    "op": "*",
                    "args": [
                      "K_c1",
                      "CO2_aq"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "K_s1",
                      "SO2_aq"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "K_n1",
                      "HNO3_aq"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "K_h1",
                      "H2O2_aq"
                    ]
                  }
                ]
              },
              {
                "op": "+",
                "args": [
                  1,
                  {
                    "op": "/",
                    "args": [
                      {
                        "op": "*",
                        "args": [
                          "K_a1",
                          "NH3_aq"
                        ]
                      },
                      "K_w"
                    ]
                  }
                ]
              }
            ]
          },
          0.5
        ]
      }
    },
    {
      "lhs": "OH_minus",
      "rhs": {
        "op": "/",
        "args": [
          "K_w",
          "H_plus"
        ]
      }
    },
    {
      "lhs": "pH",
      "rhs": {
        "op": "*",
        "args": [
          -1,
          {
            "op": "log10",
            "args": [
              {
                "op": "/",
                "args": [
                  "H_plus",
                  "C_ref"
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "HCO3_minus",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "*",
            "args": [
              "K_c1",
              "CO2_aq"
            ]
          },
          "H_plus"
        ]
      }
    },
    {
      "lhs": "CO3_2minus",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "*",
            "args": [
              "K_c2",
              "HCO3_minus"
            ]
          },
          "H_plus"
        ]
      }
    },
    {
      "lhs": "C_total",
      "rhs": {
        "op": "+",
        "args": [
          "CO2_aq",
          "HCO3_minus",
          "CO3_2minus"
        ]
      }
    },
    {
      "lhs": "H_CO2_eff",
      "rhs": {
        "op": "*",
        "args": [
          "H_CO2",
          {
            "op": "+",
            "args": [
              1,
              {
                "op": "/",
                "args": [
                  "K_c1",
                  "H_plus"
                ]
              },
              {
                "op": "/",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      "K_c1",
                      "K_c2"
                    ]
                  },
                  {
                    "op": "^",
                    "args": [
                      "H_plus",
                      2
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
      "lhs": "HSO3_minus",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "*",
            "args": [
              "K_s1",
              "SO2_aq"
            ]
          },
          "H_plus"
        ]
      }
    },
    {
      "lhs": "SO3_2minus",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "*",
            "args": [
              "K_s2",
              "HSO3_minus"
            ]
          },
          "H_plus"
        ]
      }
    },
    {
      "lhs": "S_IV_total",
      "rhs": {
        "op": "+",
        "args": [
          "SO2_aq",
          "HSO3_minus",
          "SO3_2minus"
        ]
      }
    },
    {
      "lhs": "H_SO2_eff",
      "rhs": {
        "op": "*",
        "args": [
          "H_SO2",
          {
            "op": "+",
            "args": [
              1,
              {
                "op": "/",
                "args": [
                  "K_s1",
                  "H_plus"
                ]
              },
              {
                "op": "/",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      "K_s1",
                      "K_s2"
                    ]
                  },
                  {
                    "op": "^",
                    "args": [
                      "H_plus",
                      2
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
      "lhs": "alpha_0",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "^",
            "args": [
              "H_plus",
              2
            ]
          },
          {
            "op": "+",
            "args": [
              {
                "op": "^",
                "args": [
                  "H_plus",
                  2
                ]
              },
              {
                "op": "*",
                "args": [
                  "K_s1",
                  "H_plus"
                ]
              },
              {
                "op": "*",
                "args": [
                  "K_s1",
                  "K_s2"
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "alpha_1",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "*",
            "args": [
              "K_s1",
              "H_plus"
            ]
          },
          {
            "op": "+",
            "args": [
              {
                "op": "^",
                "args": [
                  "H_plus",
                  2
                ]
              },
              {
                "op": "*",
                "args": [
                  "K_s1",
                  "H_plus"
                ]
              },
              {
                "op": "*",
                "args": [
                  "K_s1",
                  "K_s2"
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "alpha_2",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "*",
            "args": [
              "K_s1",
              "K_s2"
            ]
          },
          {
            "op": "+",
            "args": [
              {
                "op": "^",
                "args": [
                  "H_plus",
                  2
                ]
              },
              {
                "op": "*",
                "args": [
                  "K_s1",
                  "H_plus"
                ]
              },
              {
                "op": "*",
                "args": [
                  "K_s1",
                  "K_s2"
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "NH4_plus",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "*",
            "args": [
              "K_a1",
              "NH3_aq"
            ]
          },
          "OH_minus"
        ]
      }
    },
    {
      "lhs": "NH3_total",
      "rhs": {
        "op": "+",
        "args": [
          "NH3_aq",
          "NH4_plus"
        ]
      }
    },
    {
      "lhs": "H_NH3_eff",
      "rhs": {
        "op": "*",
        "args": [
          "H_NH3",
          {
            "op": "+",
            "args": [
              1,
              {
                "op": "/",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      "K_a1",
                      "H_plus"
                    ]
                  },
                  "K_w"
                ]
              }
            ]
          }
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
    },
    {
      "lhs": "HO2_minus",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "*",
            "args": [
              "K_h1",
              "H2O2_aq"
            ]
          },
          "H_plus"
        ]
      }
    },
    {
      "lhs": "H2O2_total",
      "rhs": {
        "op": "+",
        "args": [
          "H2O2_aq",
          "HO2_minus"
        ]
      }
    },
    {
      "lhs": "H_H2O2_eff",
      "rhs": {
        "op": "*",
        "args": [
          "H_H2O2",
          {
            "op": "+",
            "args": [
              1,
              {
                "op": "/",
                "args": [
                  "K_h1",
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
      "id": "pure_water_298K",
      "description": "Pure water (no trace gases) at 298 K. H_plus = OH_minus = sqrt(K_w) = 1e-4 mol/m³ (pH 7). All trace-gas species are zero.",
      "parameter_overrides": {
        "T": 298.0,
        "p_CO2": 0.0,
        "p_SO2": 0.0,
        "p_NH3": 0.0,
        "p_HNO3": 0.0,
        "p_H2O2": 0.0,
        "p_O3": 0.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "H_plus",
          "time": 0.0,
          "expected": 0.0001
        },
        {
          "variable": "OH_minus",
          "time": 0.0,
          "expected": 0.0001
        },
        {
          "variable": "pH",
          "time": 0.0,
          "expected": 7.0
        },
        {
          "variable": "K_w",
          "time": 0.0,
          "expected": 1e-08
        },
        {
          "variable": "CO2_aq",
          "time": 0.0,
          "expected": 0.0
        },
        {
          "variable": "SO2_aq",
          "time": 0.0,
          "expected": 0.0
        }
      ]
    },
    {
      "id": "co2_rainwater_298K",
      "description": "CO2-only rainwater at 298 K (p_CO2=40 Pa ≈ 400 ppm). The quadratic charge balance H+ ≈ HCO3- gives pH ≈ 5.62.",
      "parameter_overrides": {
        "T": 298.0,
        "p_CO2": 40.0,
        "p_SO2": 0.0,
        "p_NH3": 0.0,
        "p_HNO3": 0.0,
        "p_H2O2": 0.0,
        "p_O3": 0.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "H_plus",
          "time": 0.0,
          "expected": 0.002404481,
          "tolerance": {
            "rel": 0.0001
          }
        },
        {
          "variable": "pH",
          "time": 0.0,
          "expected": 5.618979,
          "tolerance": {
            "rel": 0.0001
          }
        },
        {
          "variable": "OH_minus",
          "time": 0.0,
          "expected": 4.158902e-06,
          "tolerance": {
            "rel": 0.0001
          }
        },
        {
          "variable": "HCO3_minus",
          "time": 0.0,
          "expected": 0.002400322,
          "tolerance": {
            "rel": 0.0001
          }
        },
        {
          "variable": "CO2_aq",
          "time": 0.0,
          "expected": 0.01342216,
          "tolerance": {
            "rel": 0.0001
          }
        }
      ]
    },
    {
      "id": "so2_acidification_298K",
      "description": "SO2 acidification at 298 K (p_CO2=40 Pa, p_SO2=0.001 Pa). SO2 dissolves and dissociates, lowering pH from 5.62 to 4.89. The dominant anion is HSO3-.",
      "parameter_overrides": {
        "T": 298.0,
        "p_CO2": 40.0,
        "p_SO2": 0.001,
        "p_NH3": 0.0,
        "p_HNO3": 0.0,
        "p_H2O2": 0.0,
        "p_O3": 0.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "H_plus",
          "time": 0.0,
          "expected": 0.01279025,
          "tolerance": {
            "rel": 0.0001
          }
        },
        {
          "variable": "pH",
          "time": 0.0,
          "expected": 4.893121,
          "tolerance": {
            "rel": 0.0001
          }
        },
        {
          "variable": "HSO3_minus",
          "time": 0.0,
          "expected": 0.01233823,
          "tolerance": {
            "rel": 0.0001
          }
        },
        {
          "variable": "SO3_2minus",
          "time": 0.0,
          "expected": 6.366746e-05,
          "tolerance": {
            "rel": 0.0001
          }
        },
        {
          "variable": "S_IV_total",
          "time": 0.0,
          "expected": 0.01241403,
          "tolerance": {
            "rel": 0.0001
          }
        }
      ]
    },
    {
      "id": "nh3_buffering_298K",
      "description": "NH3 buffering at 298 K (p_CO2=40 Pa, p_NH3=0.001 Pa). NH3 dissolves and forms NH4+, raising pH from 5.62 to 7.13.",
      "parameter_overrides": {
        "T": 298.0,
        "p_CO2": 40.0,
        "p_SO2": 0.0,
        "p_NH3": 0.001,
        "p_HNO3": 0.0,
        "p_H2O2": 0.0,
        "p_O3": 0.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "H_plus",
          "time": 0.0,
          "expected": 7.451619e-05,
          "tolerance": {
            "rel": 0.0001
          }
        },
        {
          "variable": "pH",
          "time": 0.0,
          "expected": 7.127749,
          "tolerance": {
            "rel": 0.0001
          }
        },
        {
          "variable": "NH4_plus",
          "time": 0.0,
          "expected": 0.07751302,
          "tolerance": {
            "rel": 0.0001
          }
        },
        {
          "variable": "OH_minus",
          "time": 0.0,
          "expected": 0.000134199,
          "tolerance": {
            "rel": 0.0001
          }
        },
        {
          "variable": "HCO3_minus",
          "time": 0.0,
          "expected": 0.07745333,
          "tolerance": {
            "rel": 0.0001
          }
        }
      ]
    },
    {
      "id": "cold_cloud_273K",
      "description": "Cold cloud water at 273.15 K (p_CO2=40 Pa). Lower T increases CO2 solubility and decreases K_w, shifting pH down to 5.52 vs 5.62 at 298 K.",
      "parameter_overrides": {
        "T": 273.15,
        "p_CO2": 40.0,
        "p_SO2": 0.0,
        "p_NH3": 0.0,
        "p_HNO3": 0.0,
        "p_H2O2": 0.0,
        "p_O3": 0.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "H_plus",
          "time": 0.0,
          "expected": 0.003029871,
          "tolerance": {
            "rel": 0.0001
          }
        },
        {
          "variable": "pH",
          "time": 0.0,
          "expected": 5.518576,
          "tolerance": {
            "rel": 0.0001
          }
        },
        {
          "variable": "CO2_aq",
          "time": 0.0,
          "expected": 0.02827668,
          "tolerance": {
            "rel": 0.0001
          }
        },
        {
          "variable": "K_w",
          "time": 0.0,
          "expected": 1.286025e-09,
          "tolerance": {
            "rel": 0.0001
          }
        }
      ]
    },
    {
      "id": "warm_cloud_310K",
      "description": "Warm cloud water at 310 K (p_CO2=40 Pa). Higher T decreases CO2 solubility, shifting pH up to 5.66 vs 5.62 at 298 K.",
      "parameter_overrides": {
        "T": 310.0,
        "p_CO2": 40.0,
        "p_SO2": 0.0,
        "p_NH3": 0.0,
        "p_HNO3": 0.0,
        "p_H2O2": 0.0,
        "p_O3": 0.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "H_plus",
          "time": 0.0,
          "expected": 0.002182085,
          "tolerance": {
            "rel": 0.0001
          }
        },
        {
          "variable": "pH",
          "time": 0.0,
          "expected": 5.661128,
          "tolerance": {
            "rel": 0.0001
          }
        },
        {
          "variable": "CO2_aq",
          "time": 0.0,
          "expected": 0.009775288,
          "tolerance": {
            "rel": 0.0001
          }
        },
        {
          "variable": "K_w",
          "time": 0.0,
          "expected": 2.39337e-08,
          "tolerance": {
            "rel": 0.0001
          }
        }
      ]
    },
    {
      "id": "so2_nh3_competition_298K",
      "description": "SO2+NH3 competition at 298 K (p_CO2=40 Pa, p_SO2=0.001 Pa, p_NH3=0.001 Pa). The quadratic approximation (ignoring CO3²- and SO3²-) gives pH 6.40. Note: at this pH SO3²-/HSO3- ≈ 17%, so the exact charge balance yields slightly higher H_plus; the model error here is ~12%.",
      "parameter_overrides": {
        "T": 298.0,
        "p_CO2": 40.0,
        "p_SO2": 0.001,
        "p_NH3": 0.001,
        "p_HNO3": 0.0,
        "p_H2O2": 0.0,
        "p_O3": 0.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "H_plus",
          "time": 0.0,
          "expected": 0.000396377,
          "tolerance": {
            "rel": 0.001
          }
        },
        {
          "variable": "pH",
          "time": 0.0,
          "expected": 6.401892,
          "tolerance": {
            "rel": 0.001
          }
        },
        {
          "variable": "NH4_plus",
          "time": 0.0,
          "expected": 0.4123182,
          "tolerance": {
            "rel": 0.001
          }
        },
        {
          "variable": "HSO3_minus",
          "time": 0.0,
          "expected": 0.3981286,
          "tolerance": {
            "rel": 0.001
          }
        }
      ]
    },
    {
      "id": "o3_h2o2_dissolution_298K",
      "description": "O3 and H2O2 dissolution at 298 K (p_O3=0.004 Pa ≈ 40 ppb, p_H2O2=0.001 Pa). Both gases dissolve via Henry's law. O3 has low solubility (H_O3 is small); H2O2 is very soluble. Neither changes pH significantly (K_h1 is tiny).",
      "parameter_overrides": {
        "T": 298.0,
        "p_CO2": 0.0,
        "p_SO2": 0.0,
        "p_NH3": 0.0,
        "p_HNO3": 0.0,
        "p_H2O2": 0.001,
        "p_O3": 0.004
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "assertions": [
        {
          "variable": "H_plus",
          "time": 0.0,
          "expected": 0.00011032330301,
          "tolerance": {
            "rel": 0.0001
          }
        },
        {
          "variable": "H2O2_aq",
          "time": 0.0,
          "expected": 0.98692326672,
          "tolerance": {
            "rel": 0.0001
          }
        },
        {
          "variable": "O3_aq",
          "time": 0.0,
          "expected": 4.3424623736e-07,
          "tolerance": {
            "rel": 0.0001
          }
        },
        {
          "variable": "HO2_minus",
          "time": 0.0,
          "expected": 1.968062166e-05,
          "tolerance": {
            "rel": 0.001
          }
        }
      ]
    }
  ],
  "analyses": [
    {
      "id": "ph_vs_temperature_co2_only",
      "description": "pH of CO2-only cloud water vs temperature (273-318 K). Higher T decreases CO2 solubility (raising pH); K_w change is secondary. Net effect: pH increases slightly with T.",
      "initial_state": {},
      "parameters": {
        "p_CO2": 40.0,
        "p_SO2": 0.0,
        "p_NH3": 0.0,
        "p_HNO3": 0.0,
        "p_H2O2": 0.0,
        "p_O3": 0.0
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
          "id": "ph_vs_T",
          "type": "line",
          "description": "pH vs temperature for CO2-only cloud water.",
          "x": {
            "variable": "T",
            "label": "Temperature (K)"
          },
          "y": {
            "variable": "pH",
            "label": "pH"
          }
        },
        {
          "id": "hco3_vs_T",
          "type": "line",
          "description": "[HCO3-] vs temperature at p_CO2=40 Pa.",
          "x": {
            "variable": "T",
            "label": "Temperature (K)"
          },
          "y": {
            "variable": "HCO3_minus",
            "label": "[HCO3⁻] (mol/m³)"
          }
        }
      ]
    },
    {
      "id": "ph_vs_p_SO2",
      "description": "SO2 acidification curve: pH vs p_SO2 at 298 K with p_CO2=40 Pa background. Transition from CO2-dominated (pH 5.6) to SO2-dominated (pH < 4) regimes.",
      "initial_state": {},
      "parameters": {
        "T": 298.0,
        "p_CO2": 40.0,
        "p_NH3": 0.0,
        "p_HNO3": 0.0,
        "p_H2O2": 0.0,
        "p_O3": 0.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "parameter_sweep": {
        "type": "cartesian",
        "dimensions": [
          {
            "parameter": "p_SO2",
            "range": {
              "start": 1e-06,
              "stop": 0.1,
              "count": 25,
              "scale": "log"
            }
          }
        ]
      },
      "plots": [
        {
          "id": "ph_vs_pSO2",
          "type": "line",
          "description": "pH vs p_SO2 showing SO2 acidification.",
          "x": {
            "variable": "p_SO2",
            "label": "p_SO2 (Pa, log)"
          },
          "y": {
            "variable": "pH",
            "label": "pH"
          }
        },
        {
          "id": "SIV_vs_pSO2",
          "type": "line",
          "description": "[S(IV)] vs p_SO2.",
          "x": {
            "variable": "p_SO2",
            "label": "p_SO2 (Pa, log)"
          },
          "y": {
            "variable": "S_IV_total",
            "label": "[S(IV)] (mol/m³)"
          }
        }
      ]
    },
    {
      "id": "ph_vs_p_NH3",
      "description": "NH3 buffering curve: pH vs p_NH3 at 298 K with p_CO2=40 Pa background. NH3 forms NH4+ and OH-, raising pH from 5.6 toward 7.",
      "initial_state": {},
      "parameters": {
        "T": 298.0,
        "p_CO2": 40.0,
        "p_SO2": 0.0,
        "p_HNO3": 0.0,
        "p_H2O2": 0.0,
        "p_O3": 0.0
      },
      "time_span": {
        "start": 0.0,
        "end": 1.0
      },
      "parameter_sweep": {
        "type": "cartesian",
        "dimensions": [
          {
            "parameter": "p_NH3",
            "range": {
              "start": 1e-06,
              "stop": 0.01,
              "count": 25,
              "scale": "log"
            }
          }
        ]
      },
      "plots": [
        {
          "id": "ph_vs_pNH3",
          "type": "line",
          "description": "pH vs p_NH3 showing NH3 buffering.",
          "x": {
            "variable": "p_NH3",
            "label": "p_NH3 (Pa, log)"
          },
          "y": {
            "variable": "pH",
            "label": "pH"
          }
        }
      ]
    }
  ]
}
```

</details>
