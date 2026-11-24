---
title: "CBMZTendencies"
slug: "cbmztendencies"
domains: ["gaschem"]
component_types: ["model"]
subdomains: ["cbmz"]
domain: "gaschem"
subdomain: "cbmz"
component_type: "model"
esm_version: "1.1.0"
esm_path: "components/gaschem/cbmz/cbmz.esm"
reference: "10.1029/1999JD900876"
description: "The CBM-Z gas-phase mechanism exactly as WRF-Chem chem_opt = 170 (CBMZ_MOSAIC_KPP: CBM-Z through KPP, paired with 8-bin MOSAIC) integrates it: 139 reactions over 66 variable species plus the two fixed species H2O and M, translated from chem/KPP/mechanisms/cbmz_mosaic/cbmz_mosaic.eqn and cbmz_mosaic.spc of WRF v4.8.0. Species are in molec/cm^3 (the KPP units; WRF converts its ppmV chem array with conv = 1e-6 dens2con_a rho), so every rate coefficient is applied by mass action exactly as KPP applies RCONST."
tags: ["gaschem", "cbmz", "model", "wrf-chem", "kpp", "reaction-system"]
---

## Description

The CBM-Z gas-phase mechanism exactly as WRF-Chem chem_opt = 170 (CBMZ_MOSAIC_KPP: CBM-Z through KPP, paired with 8-bin MOSAIC) integrates it: 139 reactions over 66 variable species plus the two fixed species H2O and M, translated from chem/KPP/mechanisms/cbmz_mosaic/cbmz_mosaic.eqn and cbmz_mosaic.spc of WRF v4.8.0. Species are in molec/cm^3 (the KPP units; WRF converts its ppmV chem array with conv = 1e-6 dens2con_a rho), so every rate coefficient is applied by mass action exactly as KPP applies RCONST.

The document carries the stoichiometry only. Each reaction's rate is a scoped reference to CBMZRateConstants, the component mounted here from ./cbmz_rate_constants.esm, which builds all 142 RCONST entries from the hand-authored rate-law templates of cbmz_ratelaws.esm. That component's own inline tests pin every coefficient to the dumped RCONST at rel 1e-9, so what this document adds -- and what its tests are about -- is the reaction network.

139 reactions, not 142: the .eqn's identity rows are omitted. cbmz_mosaic.eqn {124:104}, {125:105} and {126:106} are HCl = HCl, NH3 = NH3 and H2SO4 = H2SO4 at rate 1 s^-1. Their net stoichiometry is zero, they exist only so that KPP keeps the three species in the mechanism for MOSAIC to find, and KPP's own generated Fun eliminates them -- A(124), A(125) and A(126) do not appear in cbmz_mosaic_Integrator.f90 at all. Writing them here would not be more faithful, it would be actively wrong: a 1 s^-1 production and an identical 1 s^-1 loss of H2SO4 (~1e8 molec/cm^3) added to a net tendency of order 1e3 would destroy that tendency by cancellation, an error the Fortran does not make. The three coefficients are still exposed by CBMZRateConstants, so all 142 dumped RCONST entries remain assertable. A reader looking for an identity reaction and not finding one has found this paragraph instead.

Ten rate coefficients read the state, and a coupling edge closes that loop. CBM-Z writes its peroxy-peroxy chemistry pseudo-first-order: reactions {127:107}..{136:116} are unimolecular decays of CH3O2, ETHP, RO2, C2O3, ANO2, NAP, ISOPP, ISOPN, ISOPO2 and XO2 whose rate coefficient is the sum over the whole peroxy pool, so each carries a hidden dependence on the other nine concentrations. CBMZRateConstants takes those ten as parameters -- that is what makes its coefficients assertable pointwise -- and the ten variable_map edges below drive them from this system's own species. The mechanism is not second-order in the peroxy radicals by accident of this spelling: it genuinely is, and the coupling is where that shows.

Fixed species. H2O and M are cbmz_mosaic.spc #DEFFIX species, declared here with constant: true (esm-spec 7.4): they take part in mass action -- O(1D) + H2O, the water-enhanced HO2 self-reaction, N2O5 + H2O, and M as the third body of O(1D) + M, O(3P) + M and OH + M -- but the mechanism does not advance them. They are therefore set through parameter_overrides, not initial_conditions. A handful of reactions also write M or H2O as a PRODUCT ({024:004} O3P + O3 = 0.42 M, {032:012} OH + M = HO2 + H2O, {039:019} OH + HO2 = H2O + 0.21 M); those are the .eqn's atom bookkeeping and, being products of a constant species, change nothing, exactly as in KPP.

Stoichiometric coefficients are the float32 roundings of the .eqn's decimals, for the same reason the rate coefficients are (see cbmz_rate_constants.esm). KPP's generated cbmz_mosaic_Fun writes its stoichiometry as default-real literals inside a real64 computation -- Vdot(9) = 0.008*A(68)+... -- so the mechanism evaluates 0.00800000037997961, not 0.008. Binding the decimals instead leaves a 4.8e-8 floor on every tendency; binding the roundings takes it to 5e-16. The exact decimals the chemistry intends are recoverable from cbmz_mosaic.eqn, and each reaction's reference.notes here quotes its .eqn line verbatim, so nothing is lost. One reaction needs a second word about this. KPP folds a reaction's NET stoichiometry at code-generation time and rounds the FOLDED value, while an esm reaction system folds at run time from the two already-rounded coefficients (esm-spec 7.4: net = product - substrate). Those agree everywhere in CBM-Z but one place: {096:076} ROOH + OH = .77 RO2 + ... + .23 OH + ..., where Fun writes -0.77*A(96) and float32(0.23) - 1 is not -float32(0.77). Only four reactions carry a species on both sides at all -- R048, R094, R095, R096 -- and the first three agree bit for bit, so R096's OH product is transcribed as 1 + float32(-0.77) and nothing else moves. It matters only because OH's budget cancels: 1.9e-8 on that one coefficient is 5.1e-8 to 9.4e-6 on dOH_dt through an amplification of 1.4e3 to 2.0e5.

Provenance of the references. The test descriptions name files of the EqWeFiC reference project that produced the expected values -- the dumped WRF states and reference outputs under data/eqwefic/ (dumps/chem170_wrf, dumps/chem170_rich, replay/), the run scripts, and the replay driver kernels/cbmz_driver that runs WRF's own KPP-generated cbmz_mosaic code standalone in real64 on a dumped state. None of them is part of this repository; they are cited so that each expected value can be traced, and every description states in its own words what the reference computed.

The third component of this document, CBMZTendencies, is the derivative-test surface of the mechanism: 64 observeds d<SPC>_dt = D(CBMZ.<SPC>, t), asserted at t = 0 against Vdot from KPP's own cbmz_mosaic_Fun. That is the quantity WRF never writes -- over its 60 s step the finite increment (var_out - var_in)/60 differs from Fun by a factor of 4 to 35 at the dumped daytime states -- and it pins the whole stoichiometric matrix and every rate law at once, independently of any integrator.

## Reference

_The instantaneous net production rate of every integrated CBM-Z species, exposed as an observed so that it can be asserted at t = 0. Each equation is the identity d<SPC>_dt = D(CBMZ.<SPC>, t): esm-spec 7.4 resolves a right-hand-side time derivative over a mechanism species to the tendency the reaction system already derives, so this model adds no physics. It is the derivative-test surface of the mechanism and the companion to the CBMZ trajectory tests, which check the same network through an integrator. Reference: Vdot from KPP's own cbmz_mosaic_Fun, the quantity WRF never writes -- CBM-Z's finite 60 s increment differs from it by a factor of 4 to 35 over the dumped daytime steps._

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `dH2SO4_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of H2SO4: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(1) of cbmz_mosaic_Fun. |
| `dHCOOH_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of HCOOH: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(4) of cbmz_mosaic_Fun. |
| `dRCOOH_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of RCOOH: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(5) of cbmz_mosaic_Fun. |
| `dARO1_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of ARO1: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(6) of cbmz_mosaic_Fun. |
| `dARO2_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of ARO2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(7) of cbmz_mosaic_Fun. |
| `dALK1_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of ALK1: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(8) of cbmz_mosaic_Fun. |
| `dOLE1_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of OLE1: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(9) of cbmz_mosaic_Fun. |
| `dAPI1_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of API1: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(10) of cbmz_mosaic_Fun. |
| `dAPI2_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of API2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(11) of cbmz_mosaic_Fun. |
| `dLIM1_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of LIM1: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(12) of cbmz_mosaic_Fun. |
| `dLIM2_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of LIM2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(13) of cbmz_mosaic_Fun. |
| `dSO2_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of SO2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(14) of cbmz_mosaic_Fun. |
| `dO1D_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of O1D: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(15) of cbmz_mosaic_Fun. |
| `dANOL_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of ANOL: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(16) of cbmz_mosaic_Fun. |
| `dH2O2_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of H2O2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(17) of cbmz_mosaic_Fun. |
| `dPAN_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of PAN: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(18) of cbmz_mosaic_Fun. |
| `dTOL_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of TOL: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(19) of cbmz_mosaic_Fun. |
| `dN2O5_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of N2O5: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(20) of cbmz_mosaic_Fun. |
| `dXYL_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of XYL: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(21) of cbmz_mosaic_Fun. |
| `dCH4_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of CH4: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(22) of cbmz_mosaic_Fun. |
| `dCRO_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of CRO: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(23) of cbmz_mosaic_Fun. |
| `dAPI_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of API: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(24) of cbmz_mosaic_Fun. |
| `dLIM_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of LIM: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(25) of cbmz_mosaic_Fun. |
| `dHNO4_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of HNO4: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(26) of cbmz_mosaic_Fun. |
| `dTO2_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of TO2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(27) of cbmz_mosaic_Fun. |
| `dC2H6_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of C2H6: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(28) of cbmz_mosaic_Fun. |
| `dXPAR_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of XPAR: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(29) of cbmz_mosaic_Fun. |
| `dETHOOH_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of ETHOOH: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(30) of cbmz_mosaic_Fun. |
| `dHONO_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of HONO: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(31) of cbmz_mosaic_Fun. |
| `dCH3OOH_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of CH3OOH: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(32) of cbmz_mosaic_Fun. |
| `dC2H4_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of C2H4: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(33) of cbmz_mosaic_Fun. |
| `dCH3OH_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of CH3OH: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(34) of cbmz_mosaic_Fun. |
| `dCRES_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of CRES: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(35) of cbmz_mosaic_Fun. |
| `dO3P_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of O3P: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(36) of cbmz_mosaic_Fun. |
| `dHNO3_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of HNO3: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(37) of cbmz_mosaic_Fun. |
| `dCO_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of CO: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(38) of cbmz_mosaic_Fun. |
| `dISOPN_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of ISOPN: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(39) of cbmz_mosaic_Fun. |
| `dPAR_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of PAR: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(40) of cbmz_mosaic_Fun. |
| `dOPEN_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of OPEN: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(41) of cbmz_mosaic_Fun. |
| `dISOPP_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of ISOPP: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(42) of cbmz_mosaic_Fun. |
| `dISOPO2_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of ISOPO2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(43) of cbmz_mosaic_Fun. |
| `dOLET_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of OLET: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(44) of cbmz_mosaic_Fun. |
| `dISOP_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of ISOP: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(45) of cbmz_mosaic_Fun. |
| `dHCHO_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of HCHO: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(46) of cbmz_mosaic_Fun. |
| `dXO2_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of XO2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(47) of cbmz_mosaic_Fun. |
| `dAONE_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of AONE: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(48) of cbmz_mosaic_Fun. |
| `dOLEI_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of OLEI: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(49) of cbmz_mosaic_Fun. |
| `dMGLY_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of MGLY: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(50) of cbmz_mosaic_Fun. |
| `dETHP_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of ETHP: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(51) of cbmz_mosaic_Fun. |
| `dNAP_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of NAP: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(52) of cbmz_mosaic_Fun. |
| `dALD2_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of ALD2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(53) of cbmz_mosaic_Fun. |
| `dCH3O2_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of CH3O2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(54) of cbmz_mosaic_Fun. |
| `dISOPRD_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of ISOPRD: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(55) of cbmz_mosaic_Fun. |
| `dROOH_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of ROOH: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(56) of cbmz_mosaic_Fun. |
| `dANO2_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of ANO2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(57) of cbmz_mosaic_Fun. |
| `dRO2_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of RO2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(58) of cbmz_mosaic_Fun. |
| `dONIT_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of ONIT: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(59) of cbmz_mosaic_Fun. |
| `dNO3_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of NO3: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(60) of cbmz_mosaic_Fun. |
| `dNO_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of NO: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(61) of cbmz_mosaic_Fun. |
| `dNO2_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of NO2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(62) of cbmz_mosaic_Fun. |
| `dOH_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of OH: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(63) of cbmz_mosaic_Fun. |
| `dO3_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of O3: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(64) of cbmz_mosaic_Fun. |
| `dHO2_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of HO2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(65) of cbmz_mosaic_Fun. |
| `dC2O3_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of C2O3: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(66) of cbmz_mosaic_Fun. |

## Observed expressions

$$
dH2SO4_{dt} = \mathrm{D}\left(CBMZ.H2SO4\right)
$$
_Instantaneous net production rate of H2SO4: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(1) of cbmz_mosaic_Fun._

$$
dHCOOH_{dt} = \mathrm{D}\left(CBMZ.HCOOH\right)
$$
_Instantaneous net production rate of HCOOH: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(4) of cbmz_mosaic_Fun._

$$
dRCOOH_{dt} = \mathrm{D}\left(CBMZ.RCOOH\right)
$$
_Instantaneous net production rate of RCOOH: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(5) of cbmz_mosaic_Fun._

$$
dARO1_{dt} = \mathrm{D}\left(CBMZ.ARO1\right)
$$
_Instantaneous net production rate of ARO1: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(6) of cbmz_mosaic_Fun._

$$
dARO2_{dt} = \mathrm{D}\left(CBMZ.ARO2\right)
$$
_Instantaneous net production rate of ARO2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(7) of cbmz_mosaic_Fun._

$$
dALK1_{dt} = \mathrm{D}\left(CBMZ.ALK1\right)
$$
_Instantaneous net production rate of ALK1: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(8) of cbmz_mosaic_Fun._

$$
dOLE1_{dt} = \mathrm{D}\left(CBMZ.OLE1\right)
$$
_Instantaneous net production rate of OLE1: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(9) of cbmz_mosaic_Fun._

$$
dAPI1_{dt} = \mathrm{D}\left(CBMZ.API1\right)
$$
_Instantaneous net production rate of API1: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(10) of cbmz_mosaic_Fun._

$$
dAPI2_{dt} = \mathrm{D}\left(CBMZ.API2\right)
$$
_Instantaneous net production rate of API2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(11) of cbmz_mosaic_Fun._

$$
dLIM1_{dt} = \mathrm{D}\left(CBMZ.LIM1\right)
$$
_Instantaneous net production rate of LIM1: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(12) of cbmz_mosaic_Fun._

$$
dLIM2_{dt} = \mathrm{D}\left(CBMZ.LIM2\right)
$$
_Instantaneous net production rate of LIM2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(13) of cbmz_mosaic_Fun._

$$
dSO2_{dt} = \mathrm{D}\left(CBMZ.SO2\right)
$$
_Instantaneous net production rate of SO2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(14) of cbmz_mosaic_Fun._

$$
dO1D_{dt} = \mathrm{D}\left(CBMZ.O1D\right)
$$
_Instantaneous net production rate of O1D: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(15) of cbmz_mosaic_Fun._

$$
dANOL_{dt} = \mathrm{D}\left(CBMZ.ANOL\right)
$$
_Instantaneous net production rate of ANOL: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(16) of cbmz_mosaic_Fun._

$$
dH2O2_{dt} = \mathrm{D}\left(CBMZ.H2O2\right)
$$
_Instantaneous net production rate of H2O2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(17) of cbmz_mosaic_Fun._

$$
dPAN_{dt} = \mathrm{D}\left(CBMZ.PAN\right)
$$
_Instantaneous net production rate of PAN: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(18) of cbmz_mosaic_Fun._

$$
dTOL_{dt} = \mathrm{D}\left(CBMZ.TOL\right)
$$
_Instantaneous net production rate of TOL: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(19) of cbmz_mosaic_Fun._

$$
dN2O5_{dt} = \mathrm{D}\left(CBMZ.N2O5\right)
$$
_Instantaneous net production rate of N2O5: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(20) of cbmz_mosaic_Fun._

$$
dXYL_{dt} = \mathrm{D}\left(CBMZ.XYL\right)
$$
_Instantaneous net production rate of XYL: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(21) of cbmz_mosaic_Fun._

$$
dCH4_{dt} = \mathrm{D}\left(CBMZ.CH4\right)
$$
_Instantaneous net production rate of CH4: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(22) of cbmz_mosaic_Fun._

$$
dCRO_{dt} = \mathrm{D}\left(CBMZ.CRO\right)
$$
_Instantaneous net production rate of CRO: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(23) of cbmz_mosaic_Fun._

$$
dAPI_{dt} = \mathrm{D}\left(CBMZ.API\right)
$$
_Instantaneous net production rate of API: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(24) of cbmz_mosaic_Fun._

$$
dLIM_{dt} = \mathrm{D}\left(CBMZ.LIM\right)
$$
_Instantaneous net production rate of LIM: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(25) of cbmz_mosaic_Fun._

$$
dHNO4_{dt} = \mathrm{D}\left(CBMZ.HNO4\right)
$$
_Instantaneous net production rate of HNO4: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(26) of cbmz_mosaic_Fun._

$$
dTO2_{dt} = \mathrm{D}\left(CBMZ.TO2\right)
$$
_Instantaneous net production rate of TO2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(27) of cbmz_mosaic_Fun._

$$
dC2H6_{dt} = \mathrm{D}\left(CBMZ.C2H6\right)
$$
_Instantaneous net production rate of C2H6: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(28) of cbmz_mosaic_Fun._

$$
dXPAR_{dt} = \mathrm{D}\left(CBMZ.XPAR\right)
$$
_Instantaneous net production rate of XPAR: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(29) of cbmz_mosaic_Fun._

$$
dETHOOH_{dt} = \mathrm{D}\left(CBMZ.ETHOOH\right)
$$
_Instantaneous net production rate of ETHOOH: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(30) of cbmz_mosaic_Fun._

$$
dHONO_{dt} = \mathrm{D}\left(CBMZ.HONO\right)
$$
_Instantaneous net production rate of HONO: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(31) of cbmz_mosaic_Fun._

$$
dCH3OOH_{dt} = \mathrm{D}\left(CBMZ.CH3OOH\right)
$$
_Instantaneous net production rate of CH3OOH: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(32) of cbmz_mosaic_Fun._

$$
dC2H4_{dt} = \mathrm{D}\left(CBMZ.C2H4\right)
$$
_Instantaneous net production rate of C2H4: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(33) of cbmz_mosaic_Fun._

$$
dCH3OH_{dt} = \mathrm{D}\left(CBMZ.CH3OH\right)
$$
_Instantaneous net production rate of CH3OH: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(34) of cbmz_mosaic_Fun._

$$
dCRES_{dt} = \mathrm{D}\left(CBMZ.CRES\right)
$$
_Instantaneous net production rate of CRES: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(35) of cbmz_mosaic_Fun._

$$
dO3P_{dt} = \mathrm{D}\left(CBMZ.O3P\right)
$$
_Instantaneous net production rate of O3P: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(36) of cbmz_mosaic_Fun._

$$
dHNO3_{dt} = \mathrm{D}\left(CBMZ.HNO3\right)
$$
_Instantaneous net production rate of HNO3: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(37) of cbmz_mosaic_Fun._

$$
dCO_{dt} = \mathrm{D}\left(CBMZ.CO\right)
$$
_Instantaneous net production rate of CO: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(38) of cbmz_mosaic_Fun._

$$
dISOPN_{dt} = \mathrm{D}\left(CBMZ.ISOPN\right)
$$
_Instantaneous net production rate of ISOPN: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(39) of cbmz_mosaic_Fun._

$$
dPAR_{dt} = \mathrm{D}\left(CBMZ.PAR\right)
$$
_Instantaneous net production rate of PAR: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(40) of cbmz_mosaic_Fun._

$$
dOPEN_{dt} = \mathrm{D}\left(CBMZ.OPEN\right)
$$
_Instantaneous net production rate of OPEN: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(41) of cbmz_mosaic_Fun._

$$
dISOPP_{dt} = \mathrm{D}\left(CBMZ.ISOPP\right)
$$
_Instantaneous net production rate of ISOPP: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(42) of cbmz_mosaic_Fun._

$$
dISOPO2_{dt} = \mathrm{D}\left(CBMZ.ISOPO2\right)
$$
_Instantaneous net production rate of ISOPO2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(43) of cbmz_mosaic_Fun._

$$
dOLET_{dt} = \mathrm{D}\left(CBMZ.OLET\right)
$$
_Instantaneous net production rate of OLET: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(44) of cbmz_mosaic_Fun._

$$
dISOP_{dt} = \mathrm{D}\left(CBMZ.ISOP\right)
$$
_Instantaneous net production rate of ISOP: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(45) of cbmz_mosaic_Fun._

$$
dHCHO_{dt} = \mathrm{D}\left(CBMZ.HCHO\right)
$$
_Instantaneous net production rate of HCHO: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(46) of cbmz_mosaic_Fun._

$$
dXO2_{dt} = \mathrm{D}\left(CBMZ.XO2\right)
$$
_Instantaneous net production rate of XO2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(47) of cbmz_mosaic_Fun._

$$
dAONE_{dt} = \mathrm{D}\left(CBMZ.AONE\right)
$$
_Instantaneous net production rate of AONE: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(48) of cbmz_mosaic_Fun._

$$
dOLEI_{dt} = \mathrm{D}\left(CBMZ.OLEI\right)
$$
_Instantaneous net production rate of OLEI: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(49) of cbmz_mosaic_Fun._

$$
dMGLY_{dt} = \mathrm{D}\left(CBMZ.MGLY\right)
$$
_Instantaneous net production rate of MGLY: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(50) of cbmz_mosaic_Fun._

$$
dETHP_{dt} = \mathrm{D}\left(CBMZ.ETHP\right)
$$
_Instantaneous net production rate of ETHP: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(51) of cbmz_mosaic_Fun._

$$
dNAP_{dt} = \mathrm{D}\left(CBMZ.NAP\right)
$$
_Instantaneous net production rate of NAP: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(52) of cbmz_mosaic_Fun._

$$
dALD2_{dt} = \mathrm{D}\left(CBMZ.ALD2\right)
$$
_Instantaneous net production rate of ALD2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(53) of cbmz_mosaic_Fun._

$$
dCH3O2_{dt} = \mathrm{D}\left(CBMZ.CH3O2\right)
$$
_Instantaneous net production rate of CH3O2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(54) of cbmz_mosaic_Fun._

$$
dISOPRD_{dt} = \mathrm{D}\left(CBMZ.ISOPRD\right)
$$
_Instantaneous net production rate of ISOPRD: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(55) of cbmz_mosaic_Fun._

$$
dROOH_{dt} = \mathrm{D}\left(CBMZ.ROOH\right)
$$
_Instantaneous net production rate of ROOH: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(56) of cbmz_mosaic_Fun._

$$
dANO2_{dt} = \mathrm{D}\left(CBMZ.ANO2\right)
$$
_Instantaneous net production rate of ANO2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(57) of cbmz_mosaic_Fun._

$$
dRO2_{dt} = \mathrm{D}\left(CBMZ.RO2\right)
$$
_Instantaneous net production rate of RO2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(58) of cbmz_mosaic_Fun._

$$
dONIT_{dt} = \mathrm{D}\left(CBMZ.ONIT\right)
$$
_Instantaneous net production rate of ONIT: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(59) of cbmz_mosaic_Fun._

$$
dNO3_{dt} = \mathrm{D}\left(CBMZ.NO3\right)
$$
_Instantaneous net production rate of NO3: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(60) of cbmz_mosaic_Fun._

$$
dNO_{dt} = \mathrm{D}\left(CBMZ.NO\right)
$$
_Instantaneous net production rate of NO: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(61) of cbmz_mosaic_Fun._

$$
dNO2_{dt} = \mathrm{D}\left(CBMZ.NO2\right)
$$
_Instantaneous net production rate of NO2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(62) of cbmz_mosaic_Fun._

$$
dOH_{dt} = \mathrm{D}\left(CBMZ.OH\right)
$$
_Instantaneous net production rate of OH: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(63) of cbmz_mosaic_Fun._

$$
dO3_{dt} = \mathrm{D}\left(CBMZ.O3\right)
$$
_Instantaneous net production rate of O3: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(64) of cbmz_mosaic_Fun._

$$
dHO2_{dt} = \mathrm{D}\left(CBMZ.HO2\right)
$$
_Instantaneous net production rate of HO2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(65) of cbmz_mosaic_Fun._

$$
dC2O3_{dt} = \mathrm{D}\left(CBMZ.C2O3\right)
$$
_Instantaneous net production rate of C2O3: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(66) of cbmz_mosaic_Fun._

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "reference": {
    "notes": "The instantaneous net production rate of every integrated CBM-Z species, exposed as an observed so that it can be asserted at t = 0. Each equation is the identity d<SPC>_dt = D(CBMZ.<SPC>, t): esm-spec 7.4 resolves a right-hand-side time derivative over a mechanism species to the tendency the reaction system already derives, so this model adds no physics. It is the derivative-test surface of the mechanism and the companion to the CBMZ trajectory tests, which check the same network through an integrator. Reference: Vdot from KPP's own cbmz_mosaic_Fun, the quantity WRF never writes -- CBM-Z's finite 60 s increment differs from it by a factor of 4 to 35 over the dumped daytime steps."
  },
  "variables": {
    "dH2SO4_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of H2SO4: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(1) of cbmz_mosaic_Fun."
    },
    "dHCOOH_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of HCOOH: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(4) of cbmz_mosaic_Fun."
    },
    "dRCOOH_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of RCOOH: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(5) of cbmz_mosaic_Fun."
    },
    "dARO1_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of ARO1: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(6) of cbmz_mosaic_Fun."
    },
    "dARO2_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of ARO2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(7) of cbmz_mosaic_Fun."
    },
    "dALK1_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of ALK1: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(8) of cbmz_mosaic_Fun."
    },
    "dOLE1_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of OLE1: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(9) of cbmz_mosaic_Fun."
    },
    "dAPI1_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of API1: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(10) of cbmz_mosaic_Fun."
    },
    "dAPI2_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of API2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(11) of cbmz_mosaic_Fun."
    },
    "dLIM1_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of LIM1: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(12) of cbmz_mosaic_Fun."
    },
    "dLIM2_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of LIM2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(13) of cbmz_mosaic_Fun."
    },
    "dSO2_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of SO2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(14) of cbmz_mosaic_Fun."
    },
    "dO1D_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of O1D: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(15) of cbmz_mosaic_Fun."
    },
    "dANOL_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of ANOL: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(16) of cbmz_mosaic_Fun."
    },
    "dH2O2_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of H2O2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(17) of cbmz_mosaic_Fun."
    },
    "dPAN_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of PAN: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(18) of cbmz_mosaic_Fun."
    },
    "dTOL_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of TOL: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(19) of cbmz_mosaic_Fun."
    },
    "dN2O5_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of N2O5: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(20) of cbmz_mosaic_Fun."
    },
    "dXYL_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of XYL: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(21) of cbmz_mosaic_Fun."
    },
    "dCH4_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of CH4: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(22) of cbmz_mosaic_Fun."
    },
    "dCRO_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of CRO: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(23) of cbmz_mosaic_Fun."
    },
    "dAPI_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of API: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(24) of cbmz_mosaic_Fun."
    },
    "dLIM_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of LIM: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(25) of cbmz_mosaic_Fun."
    },
    "dHNO4_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of HNO4: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(26) of cbmz_mosaic_Fun."
    },
    "dTO2_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of TO2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(27) of cbmz_mosaic_Fun."
    },
    "dC2H6_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of C2H6: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(28) of cbmz_mosaic_Fun."
    },
    "dXPAR_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of XPAR: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(29) of cbmz_mosaic_Fun."
    },
    "dETHOOH_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of ETHOOH: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(30) of cbmz_mosaic_Fun."
    },
    "dHONO_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of HONO: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(31) of cbmz_mosaic_Fun."
    },
    "dCH3OOH_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of CH3OOH: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(32) of cbmz_mosaic_Fun."
    },
    "dC2H4_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of C2H4: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(33) of cbmz_mosaic_Fun."
    },
    "dCH3OH_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of CH3OH: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(34) of cbmz_mosaic_Fun."
    },
    "dCRES_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of CRES: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(35) of cbmz_mosaic_Fun."
    },
    "dO3P_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of O3P: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(36) of cbmz_mosaic_Fun."
    },
    "dHNO3_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of HNO3: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(37) of cbmz_mosaic_Fun."
    },
    "dCO_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of CO: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(38) of cbmz_mosaic_Fun."
    },
    "dISOPN_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of ISOPN: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(39) of cbmz_mosaic_Fun."
    },
    "dPAR_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of PAR: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(40) of cbmz_mosaic_Fun."
    },
    "dOPEN_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of OPEN: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(41) of cbmz_mosaic_Fun."
    },
    "dISOPP_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of ISOPP: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(42) of cbmz_mosaic_Fun."
    },
    "dISOPO2_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of ISOPO2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(43) of cbmz_mosaic_Fun."
    },
    "dOLET_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of OLET: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(44) of cbmz_mosaic_Fun."
    },
    "dISOP_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of ISOP: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(45) of cbmz_mosaic_Fun."
    },
    "dHCHO_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of HCHO: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(46) of cbmz_mosaic_Fun."
    },
    "dXO2_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of XO2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(47) of cbmz_mosaic_Fun."
    },
    "dAONE_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of AONE: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(48) of cbmz_mosaic_Fun."
    },
    "dOLEI_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of OLEI: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(49) of cbmz_mosaic_Fun."
    },
    "dMGLY_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of MGLY: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(50) of cbmz_mosaic_Fun."
    },
    "dETHP_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of ETHP: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(51) of cbmz_mosaic_Fun."
    },
    "dNAP_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of NAP: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(52) of cbmz_mosaic_Fun."
    },
    "dALD2_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of ALD2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(53) of cbmz_mosaic_Fun."
    },
    "dCH3O2_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of CH3O2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(54) of cbmz_mosaic_Fun."
    },
    "dISOPRD_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of ISOPRD: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(55) of cbmz_mosaic_Fun."
    },
    "dROOH_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of ROOH: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(56) of cbmz_mosaic_Fun."
    },
    "dANO2_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of ANO2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(57) of cbmz_mosaic_Fun."
    },
    "dRO2_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of RO2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(58) of cbmz_mosaic_Fun."
    },
    "dONIT_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of ONIT: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(59) of cbmz_mosaic_Fun."
    },
    "dNO3_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of NO3: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(60) of cbmz_mosaic_Fun."
    },
    "dNO_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of NO: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(61) of cbmz_mosaic_Fun."
    },
    "dNO2_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of NO2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(62) of cbmz_mosaic_Fun."
    },
    "dOH_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of OH: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(63) of cbmz_mosaic_Fun."
    },
    "dO3_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of O3: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(64) of cbmz_mosaic_Fun."
    },
    "dHO2_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of HO2: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(65) of cbmz_mosaic_Fun."
    },
    "dC2O3_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of C2O3: the mass-action tendency the CBMZ reaction system derives for it, which is KPP's Vdot(66) of cbmz_mosaic_Fun."
    }
  },
  "equations": [
    {
      "lhs": "dH2SO4_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.H2SO4"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dHCOOH_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.HCOOH"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dRCOOH_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.RCOOH"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dARO1_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.ARO1"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dARO2_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.ARO2"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dALK1_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.ALK1"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dOLE1_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.OLE1"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dAPI1_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.API1"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dAPI2_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.API2"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dLIM1_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.LIM1"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dLIM2_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.LIM2"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dSO2_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.SO2"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dO1D_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.O1D"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dANOL_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.ANOL"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dH2O2_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.H2O2"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dPAN_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.PAN"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dTOL_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.TOL"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dN2O5_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.N2O5"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dXYL_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.XYL"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dCH4_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.CH4"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dCRO_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.CRO"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dAPI_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.API"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dLIM_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.LIM"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dHNO4_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.HNO4"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dTO2_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.TO2"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dC2H6_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.C2H6"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dXPAR_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.XPAR"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dETHOOH_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.ETHOOH"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dHONO_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.HONO"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dCH3OOH_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.CH3OOH"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dC2H4_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.C2H4"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dCH3OH_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.CH3OH"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dCRES_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.CRES"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dO3P_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.O3P"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dHNO3_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.HNO3"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dCO_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.CO"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dISOPN_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.ISOPN"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dPAR_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.PAR"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dOPEN_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.OPEN"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dISOPP_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.ISOPP"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dISOPO2_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.ISOPO2"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dOLET_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.OLET"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dISOP_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.ISOP"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dHCHO_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.HCHO"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dXO2_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.XO2"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dAONE_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.AONE"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dOLEI_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.OLEI"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dMGLY_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.MGLY"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dETHP_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.ETHP"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dNAP_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.NAP"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dALD2_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.ALD2"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dCH3O2_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.CH3O2"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dISOPRD_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.ISOPRD"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dROOH_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.ROOH"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dANO2_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.ANO2"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dRO2_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.RO2"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dONIT_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.ONIT"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dNO3_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.NO3"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dNO_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.NO"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dNO2_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.NO2"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dOH_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.OH"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dO3_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.O3"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dHO2_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.HO2"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dC2O3_dt",
      "rhs": {
        "op": "D",
        "args": [
          "CBMZ.C2O3"
        ],
        "wrt": "t"
      }
    }
  ],
  "tests": [
    {
      "id": "scm_surface_noon_tendencies",
      "description": "The instantaneous net production rate of every integrated CBM-Z species at the reference column's surface layer at local noon (step 364 level 1, T = 309.11 K, M = 2.3344e19 molec/cm3, j(NO2) = 5.56e-3 /s) -- the regime with the fastest photochemistry and the largest peroxy pool in the run.\n\nReference: Vdot from cbmz_mosaic_Fun, the KPP-generated right-hand side, evaluated on the dumped var_in with the dumped RCONST by the real64 replay driver kernels/cbmz_driver (a standalone program that calls WRF's KPP-generated cbmz_mosaic routines on the dumped inputs; WRF's KPP is already real64, so this is an independent replay of the same arithmetic rather than a precision upgrade). This is the INSTANTANEOUS rate, which WRF never writes: over its 60 s step the finite increment (var_out - var_in)/60 reaches only 2.7e5 to 8.0e6 molec/cm3/s where Fun reaches 1.1e6 to 3.6e7, a factor of 4 to 35, so a tendency test referenced against differenced states would be testing something else entirely.\n\nShape: each d<SPC>_dt is an observed written D(CBMZ.<SPC>, t), which esm-spec 7.4 resolves to the tendency the reaction system already derives, so asserting it at time 0 evaluates the mechanism's right-hand side at the given state. The time_span is empty ({start: 0, end: 0}), the shape esm-spec 6.6.2 names for a document with ODE states all of whose assertions sit at t0: the runner answers from the initial state without integrating. This adds no physics -- it is the derivative-test surface of the mechanism, and it pins the whole stoichiometric matrix and every rate law at once, independently of any integrator. The peroxy coefficients are live here as everywhere in this document, but at t = 0 that is no different from WRF: the operator split WRF makes -- it computes the ten state-dependent peroxy coefficients once, before INTEGRATE, and holds them at the step's input state for the whole 60 s step -- opens up only as the step proceeds.\n\nHCl and NH3 are absent from the 64: they are reservoir species of this mechanism (see their declarations), so no D(CBMZ.X, t) exists for them. What such an assertion would say -- that the CBM-Z gas phase produces and destroys neither -- is structural in this document rather than numerical.\n\nMeasured: 40 of the 64 assertions are BIT-IDENTICAL to KPP and the largest residual is 3.5e-13 (dANO2_dt)\n\nState: data/eqwefic/dumps/chem170_wrf/esm_dump_cbmz_kpp_364.json level k = 1; reference chem170_scm/replay/kp_364.out.json (variable vdot). The run is described in data/eqwefic/notes/chem170_scm_reference_run.md.",
      "time_span": {
        "start": 0,
        "end": 0
      },
      "tolerance": {
        "rel": 1e-09
      },
      "initial_conditions": {
        "CBMZ.H2SO4": 167793844.05364805,
        "CBMZ.HCOOH": 940608081.176528,
        "CBMZ.RCOOH": 1871595543.3164022,
        "CBMZ.ARO1": 0.019269287283393336,
        "CBMZ.ARO2": 0.049231992040399915,
        "CBMZ.ALK1": 41404903.617511705,
        "CBMZ.OLE1": 23412777.21823148,
        "CBMZ.API1": 0.020963994745431522,
        "CBMZ.API2": 0.16323119740707312,
        "CBMZ.LIM1": 0.11241999951580842,
        "CBMZ.LIM2": 0.16322906187546485,
        "CBMZ.SO2": 1776460782.9190242,
        "CBMZ.O1D": 0.015631994976912787,
        "CBMZ.ANOL": 0.0023344358935166254,
        "CBMZ.H2O2": 34609555069.201675,
        "CBMZ.PAN": 76961905.56287676,
        "CBMZ.TOL": 0.17251449172224936,
        "CBMZ.N2O5": 220.88139920702284,
        "CBMZ.XYL": 0.06824991934412515,
        "CBMZ.CH4": 39614358539959.875,
        "CBMZ.CRO": 0.002334436047996632,
        "CBMZ.API": 0.002334436047996632,
        "CBMZ.LIM": 0.002334436047996632,
        "CBMZ.HNO4": 680922.8781017046,
        "CBMZ.TO2": 0.00762607976860755,
        "CBMZ.C2H6": 14786722795.741589,
        "CBMZ.XPAR": 325848.33383532846,
        "CBMZ.ETHOOH": 11751147678.880539,
        "CBMZ.HONO": 2089409.45981405,
        "CBMZ.CH3OOH": 33300024418.017097,
        "CBMZ.C2H4": 2811012193.6878138,
        "CBMZ.CH3OH": 1396016519.0598223,
        "CBMZ.CRES": 0.026854379180866954,
        "CBMZ.O3P": 3178.723362318046,
        "CBMZ.HNO3": 1281738355.665585,
        "CBMZ.CO": 1859614695183.867,
        "CBMZ.ISOPN": 0.002334436047996632,
        "CBMZ.PAR": 82446455956.48032,
        "CBMZ.OPEN": 0.03164054794570781,
        "CBMZ.ISOPP": 0.002334436047996632,
        "CBMZ.ISOPO2": 0.002334436047996632,
        "CBMZ.OLET": 488564804.74004686,
        "CBMZ.ISOP": 0.0023344358935166254,
        "CBMZ.HCHO": 13675582656.10723,
        "CBMZ.XO2": 28514423.691775426,
        "CBMZ.AONE": 1646337413.6016686,
        "CBMZ.OLEI": 1361143.7044709132,
        "CBMZ.MGLY": 22782305.734912343,
        "CBMZ.ETHP": 60357708.15285586,
        "CBMZ.NAP": 60865.86883023894,
        "CBMZ.ALD2": 5105662743.560515,
        "CBMZ.CH3O2": 532135723.9773575,
        "CBMZ.ISOPRD": 0.02044606406674669,
        "CBMZ.ROOH": 1155927542.929869,
        "CBMZ.ANO2": 288706.23094594415,
        "CBMZ.RO2": 21524268.839473903,
        "CBMZ.ONIT": 35702621.324967004,
        "CBMZ.NO3": 71597.9041400192,
        "CBMZ.NO": 102327007.9526251,
        "CBMZ.NO2": 380883629.9772625,
        "CBMZ.OH": 3333652.469351868,
        "CBMZ.O3": 598460989073.2762,
        "CBMZ.HO2": 385375296.0868791,
        "CBMZ.C2O3": 30461029.609013133
      },
      "parameter_overrides": {
        "CBMZ.H2O": 5.741257675631493e+17,
        "CBMZ.M": 2.334435809094009e+19,
        "CBMZRateConstants.T": 309.1141357421875,
        "CBMZRateConstants.j_o31d": 2.0706509531009942e-05,
        "CBMZRateConstants.j_o33p": 0.0003176535537932068,
        "CBMZRateConstants.j_no2": 0.00555551378056407,
        "CBMZRateConstants.j_no3o": 0.1376122534275055,
        "CBMZRateConstants.j_hno2": 0.0012127247173339128,
        "CBMZRateConstants.j_hno3": 3.8736078522561e-07,
        "CBMZRateConstants.j_hno4": 2.5663800897746114e-06,
        "CBMZRateConstants.j_h2o2": 4.608004019246437e-06,
        "CBMZRateConstants.j_ch2or": 1.7385642422595993e-05,
        "CBMZRateConstants.j_ch2om": 2.7755671908380464e-05,
        "CBMZRateConstants.j_n2o5": 0.0,
        "CBMZ.HCl": 6853211902.568538,
        "CBMZ.NH3": 14056082.525449336
      },
      "assertions": [
        {
          "variable": "dH2SO4_dt",
          "time": 0.0,
          "expected": 4978.052883767861
        },
        {
          "variable": "dHCOOH_dt",
          "time": 0.0,
          "expected": 2917.7562211703753
        },
        {
          "variable": "dRCOOH_dt",
          "time": 0.0,
          "expected": 54046.194098630534
        },
        {
          "variable": "dARO1_dt",
          "time": 0.0,
          "expected": 4.978201361183206e-07
        },
        {
          "variable": "dARO2_dt",
          "time": 0.0,
          "expected": 1.3785788457971813e-06
        },
        {
          "variable": "dALK1_dt",
          "time": 0.0,
          "expected": 2671.520945291269
        },
        {
          "variable": "dOLE1_dt",
          "time": 0.0,
          "expected": 387.8626736567367
        },
        {
          "variable": "dAPI1_dt",
          "time": 0.0,
          "expected": 0.0001784951369443125
        },
        {
          "variable": "dAPI2_dt",
          "time": 0.0,
          "expected": 0.001541548790984133
        },
        {
          "variable": "dLIM1_dt",
          "time": 0.0,
          "expected": 0.0022158004419500716
        },
        {
          "variable": "dLIM2_dt",
          "time": 0.0,
          "expected": 0.003238480206298745
        },
        {
          "variable": "dSO2_dt",
          "time": 0.0,
          "expected": -4978.052883767861
        },
        {
          "variable": "dO1D_dt",
          "time": 0.0,
          "expected": -64879.80419322918
        },
        {
          "variable": "dANOL_dt",
          "time": 0.0,
          "expected": -2.5470272163321412e-08
        },
        {
          "variable": "dH2O2_dt",
          "time": 0.0,
          "expected": 413003.33419616206
        },
        {
          "variable": "dPAN_dt",
          "time": 0.0,
          "expected": -53291.95174785558
        },
        {
          "variable": "dTOL_dt",
          "time": 0.0,
          "expected": -3.4226608590475125e-06
        },
        {
          "variable": "dN2O5_dt",
          "time": 0.0,
          "expected": -1.9796299787376483
        },
        {
          "variable": "dXYL_dt",
          "time": 0.0,
          "expected": -5.629208106319955e-06
        },
        {
          "variable": "dCH4_dt",
          "time": 0.0,
          "expected": -1037343.5321528742
        },
        {
          "variable": "dCRO_dt",
          "time": 0.0,
          "expected": -1.0937598914518352e-05
        },
        {
          "variable": "dAPI_dt",
          "time": 0.0,
          "expected": -0.008113696157603375
        },
        {
          "variable": "dLIM_dt",
          "time": 0.0,
          "expected": -0.017045571411767203
        },
        {
          "variable": "dHNO4_dt",
          "time": 0.0,
          "expected": -14669.941993948916
        },
        {
          "variable": "dTO2_dt",
          "time": 0.0,
          "expected": -1.049594484772334e-06
        },
        {
          "variable": "dC2H6_dt",
          "time": 0.0,
          "expected": -10796.389621732204
        },
        {
          "variable": "dXPAR_dt",
          "time": 0.0,
          "expected": -3017.2674398112295
        },
        {
          "variable": "dETHOOH_dt",
          "time": 0.0,
          "expected": -154265.0856783972
        },
        {
          "variable": "dHONO_dt",
          "time": 0.0,
          "expected": -176.93324344832888
        },
        {
          "variable": "dCH3OOH_dt",
          "time": 0.0,
          "expected": 123667.18610818288
        },
        {
          "variable": "dC2H4_dt",
          "time": 0.0,
          "expected": -80296.335461047
        },
        {
          "variable": "dCH3OH_dt",
          "time": 0.0,
          "expected": 111657.35850026582
        },
        {
          "variable": "dCRES_dt",
          "time": 0.0,
          "expected": -3.0205699426813473e-06
        },
        {
          "variable": "dO3P_dt",
          "time": 0.0,
          "expected": -1037184.4624540649
        },
        {
          "variable": "dHNO3_dt",
          "time": 0.0,
          "expected": 8954.732362642682
        },
        {
          "variable": "dCO_dt",
          "time": 0.0,
          "expected": -386528.45369424176
        },
        {
          "variable": "dISOPN_dt",
          "time": 0.0,
          "expected": -1.3579706286541012e-05
        },
        {
          "variable": "dPAR_dt",
          "time": 0.0,
          "expected": -491277.1465131183
        },
        {
          "variable": "dOPEN_dt",
          "time": 0.0,
          "expected": -1.2340818049585425e-06
        },
        {
          "variable": "dISOPP_dt",
          "time": 0.0,
          "expected": -1.2820012610064688e-05
        },
        {
          "variable": "dISOPO2_dt",
          "time": 0.0,
          "expected": -1.2455183563893732e-05
        },
        {
          "variable": "dOLET_dt",
          "time": 0.0,
          "expected": -47978.35645607815
        },
        {
          "variable": "dISOP_dt",
          "time": 0.0,
          "expected": -7.84830923745357e-07
        },
        {
          "variable": "dHCHO_dt",
          "time": 0.0,
          "expected": 79511.06201877291
        },
        {
          "variable": "dXO2_dt",
          "time": 0.0,
          "expected": -3587.8631765186037
        },
        {
          "variable": "dAONE_dt",
          "time": 0.0,
          "expected": 89451.04925558977
        },
        {
          "variable": "dOLEI_dt",
          "time": 0.0,
          "expected": -504.475448202994
        },
        {
          "variable": "dMGLY_dt",
          "time": 0.0,
          "expected": 413.21584056857944
        },
        {
          "variable": "dETHP_dt",
          "time": 0.0,
          "expected": -14546.196592783761
        },
        {
          "variable": "dNAP_dt",
          "time": 0.0,
          "expected": 0.8620102751426018
        },
        {
          "variable": "dALD2_dt",
          "time": 0.0,
          "expected": 47019.44993032983
        },
        {
          "variable": "dCH3O2_dt",
          "time": 0.0,
          "expected": -22533.111378653033
        },
        {
          "variable": "dISOPRD_dt",
          "time": 0.0,
          "expected": 1.0962032654656154e-06
        },
        {
          "variable": "dROOH_dt",
          "time": 0.0,
          "expected": 63762.67415045524
        },
        {
          "variable": "dANO2_dt",
          "time": 0.0,
          "expected": -0.3257667608112911
        },
        {
          "variable": "dRO2_dt",
          "time": 0.0,
          "expected": -4900.938310057216
        },
        {
          "variable": "dONIT_dt",
          "time": 0.0,
          "expected": 1357.4016529658397
        },
        {
          "variable": "dNO3_dt",
          "time": 0.0,
          "expected": 226.3871199653705
        },
        {
          "variable": "dNO_dt",
          "time": 0.0,
          "expected": -44365.17941390458
        },
        {
          "variable": "dNO2_dt",
          "time": 0.0,
          "expected": 101968.58211746797
        },
        {
          "variable": "dOH_dt",
          "time": 0.0,
          "expected": -8218.324068112028
        },
        {
          "variable": "dO3_dt",
          "time": 0.0,
          "expected": -689231.3370882943
        },
        {
          "variable": "dHO2_dt",
          "time": 0.0,
          "expected": 65486.225474116545
        },
        {
          "variable": "dC2O3_dt",
          "time": 0.0,
          "expected": 10032.362280277577
        }
      ]
    },
    {
      "id": "scm_early_morning_tendencies",
      "description": "Surface at 06 LST, step 1 level 1 (T = 306.17 K, M = 2.3565e19 molec/cm3, j(NO2) = 2.11e-4 /s). The first chemistry call of the run, with the initial idealized profile still almost untouched and photolysis only just switched on.\n\nReference: Vdot from cbmz_mosaic_Fun, the KPP-generated right-hand side, evaluated on the dumped var_in with the dumped RCONST by the real64 replay driver kernels/cbmz_driver (a standalone program that calls WRF's KPP-generated cbmz_mosaic routines on the dumped inputs; WRF's KPP is already real64, so this is an independent replay of the same arithmetic rather than a precision upgrade). This is the INSTANTANEOUS rate, which WRF never writes: over its 60 s step the finite increment (var_out - var_in)/60 reaches only 2.7e5 to 8.0e6 molec/cm3/s where Fun reaches 1.1e6 to 3.6e7, a factor of 4 to 35, so a tendency test referenced against differenced states would be testing something else entirely.\n\nShape: each d<SPC>_dt is an observed written D(CBMZ.<SPC>, t), which esm-spec 7.4 resolves to the tendency the reaction system already derives, so asserting it at time 0 evaluates the mechanism's right-hand side at the given state. The time_span is empty ({start: 0, end: 0}), the shape esm-spec 6.6.2 names for a document with ODE states all of whose assertions sit at t0: the runner answers from the initial state without integrating. This adds no physics -- it is the derivative-test surface of the mechanism, and it pins the whole stoichiometric matrix and every rate law at once, independently of any integrator. The peroxy coefficients are live here as everywhere in this document, but at t = 0 that is no different from WRF: the operator split WRF makes -- it computes the ten state-dependent peroxy coefficients once, before INTEGRATE, and holds them at the step's input state for the whole 60 s step -- opens up only as the step proceeds.\n\nHCl and NH3 are absent from the 64: they are reservoir species of this mechanism (see their declarations), so no D(CBMZ.X, t) exists for them. What such an assertion would say -- that the CBM-Z gas phase produces and destroys neither -- is structural in this document rather than numerical.\n\nMeasured: 58 of the 64 assertions are BIT-IDENTICAL to KPP and the largest residual is 3.0e-16 (dH2O2_dt)\n\nState: data/eqwefic/dumps/chem170_wrf/esm_dump_cbmz_kpp_1.json level k = 1; reference chem170_scm/replay/kp_1.out.json (variable vdot). The run is described in data/eqwefic/notes/chem170_scm_reference_run.md.",
      "time_span": {
        "start": 0,
        "end": 0
      },
      "tolerance": {
        "rel": 1e-09
      },
      "initial_conditions": {
        "CBMZ.H2SO4": 1178234084.113183,
        "CBMZ.HCOOH": 1178233912.6575658,
        "CBMZ.RCOOH": 1413880712.3346407,
        "CBMZ.ARO1": 0.0023564680960358074,
        "CBMZ.ARO2": 0.0023564680960358074,
        "CBMZ.ALK1": 0.0023564680960358074,
        "CBMZ.OLE1": 0.0023564680960358074,
        "CBMZ.API1": 0.0023564680960358074,
        "CBMZ.API2": 0.0023564680960358074,
        "CBMZ.LIM1": 0.0023564680960358074,
        "CBMZ.LIM2": 0.0023564680960358074,
        "CBMZ.SO2": 2356468168.226366,
        "CBMZ.O1D": 0.0,
        "CBMZ.ANOL": 0.0023564680960358074,
        "CBMZ.H2O2": 32519259898.53689,
        "CBMZ.PAN": 275706740.19117206,
        "CBMZ.TOL": 0.23564680149480602,
        "CBMZ.N2O5": 291761.36864263384,
        "CBMZ.XYL": 0.23564680149480602,
        "CBMZ.CH4": 40059958080753.9,
        "CBMZ.CRO": 0.0023564680960358074,
        "CBMZ.API": 0.0023564680960358074,
        "CBMZ.LIM": 0.0023564680960358074,
        "CBMZ.HNO4": 3795479.8402734455,
        "CBMZ.TO2": 0.0023564680960358074,
        "CBMZ.C2H6": 15081396550.977728,
        "CBMZ.XPAR": 0.0023564680960358074,
        "CBMZ.ETHOOH": 18144802289.21764,
        "CBMZ.HONO": 0.23564680149480602,
        "CBMZ.CH3OOH": 36289604578.43528,
        "CBMZ.C2H4": 4359465836.88979,
        "CBMZ.CH3OH": 0.0023564680960358074,
        "CBMZ.CRES": 0.23564680149480602,
        "CBMZ.O3P": 0.0,
        "CBMZ.HNO3": 1649527683.4673326,
        "CBMZ.CO": 1885174402903.1787,
        "CBMZ.ISOPN": 0.0023564680960358074,
        "CBMZ.PAR": 94209940061.98004,
        "CBMZ.OPEN": 0.0023564680960358074,
        "CBMZ.ISOPP": 0.0023564680960358074,
        "CBMZ.ISOPO2": 0.0023564680960358074,
        "CBMZ.OLET": 2299912847.146947,
        "CBMZ.ISOP": 0.0023564680960358074,
        "CBMZ.HCHO": 12041551557.799116,
        "CBMZ.XO2": 0.0023564680960358074,
        "CBMZ.AONE": 299271450.16361254,
        "CBMZ.OLEI": 1149956423.5734735,
        "CBMZ.MGLY": 0.23564680149480602,
        "CBMZ.ETHP": 0.0023564680960358074,
        "CBMZ.NAP": 0.0023564680960358074,
        "CBMZ.ALD2": 704583913.0316142,
        "CBMZ.CH3O2": 0.0023564680960358074,
        "CBMZ.ISOPRD": 0.0023564680960358074,
        "CBMZ.ROOH": 0.0023564680960358074,
        "CBMZ.ANO2": 0.0023564680960358074,
        "CBMZ.RO2": 0.0023564680960358074,
        "CBMZ.ONIT": 0.23564680149480602,
        "CBMZ.NO3": 2625852.3177837045,
        "CBMZ.NO": 127249279.5411232,
        "CBMZ.NO2": 381747817.19141746,
        "CBMZ.OH": 1308192.6276228107,
        "CBMZ.O3": 706940401088.692,
        "CBMZ.HO2": 1084422829.1115165,
        "CBMZ.C2O3": 0.0023564680960358074
      },
      "parameter_overrides": {
        "CBMZ.H2O": 5.357267327123456e+17,
        "CBMZ.M": 2.35646804299371e+19,
        "CBMZRateConstants.T": 306.1650695800781,
        "CBMZRateConstants.j_o31d": 1.0315505249991475e-07,
        "CBMZRateConstants.j_o33p": 9.906222658173647e-06,
        "CBMZRateConstants.j_no2": 0.000210850645089522,
        "CBMZRateConstants.j_no3o": 0.004483486991375685,
        "CBMZRateConstants.j_hno2": 4.64483855466824e-05,
        "CBMZRateConstants.j_hno3": 4.801096853412901e-09,
        "CBMZRateConstants.j_hno4": 2.8821148134738905e-08,
        "CBMZRateConstants.j_h2o2": 1.1240952346724953e-07,
        "CBMZRateConstants.j_ch2or": 3.2001688055061095e-07,
        "CBMZRateConstants.j_ch2om": 8.588341415816103e-07,
        "CBMZRateConstants.j_n2o5": 0.0,
        "CBMZ.HCl": 9425872672.905464,
        "CBMZ.NH3": 117823410.5545135
      },
      "assertions": [
        {
          "variable": "dH2SO4_dt",
          "time": 0.0,
          "expected": 2626.740569556716
        },
        {
          "variable": "dHCOOH_dt",
          "time": 0.0,
          "expected": 7777.756193090514
        },
        {
          "variable": "dRCOOH_dt",
          "time": 0.0,
          "expected": 33894.386550775656
        },
        {
          "variable": "dARO1_dt",
          "time": 0.0,
          "expected": 1.3946395275093201e-06
        },
        {
          "variable": "dARO2_dt",
          "time": 0.0,
          "expected": 3.862078712059092e-06
        },
        {
          "variable": "dALK1_dt",
          "time": 0.0,
          "expected": 1197.938971060986
        },
        {
          "variable": "dOLE1_dt",
          "time": 0.0,
          "expected": 3290.4116598870232
        },
        {
          "variable": "dAPI1_dt",
          "time": 0.0,
          "expected": 0.00021611254637444877
        },
        {
          "variable": "dAPI2_dt",
          "time": 0.0,
          "expected": 0.001866426480186265
        },
        {
          "variable": "dLIM1_dt",
          "time": 0.0,
          "expected": 0.0026421090539509805
        },
        {
          "variable": "dLIM2_dt",
          "time": 0.0,
          "expected": 0.003861545108851519
        },
        {
          "variable": "dSO2_dt",
          "time": 0.0,
          "expected": -2626.740569556716
        },
        {
          "variable": "dO1D_dt",
          "time": 0.0,
          "expected": 72924.47418861481
        },
        {
          "variable": "dANOL_dt",
          "time": 0.0,
          "expected": -1.0015769363272459e-08
        },
        {
          "variable": "dH2O2_dt",
          "time": 0.0,
          "expected": 6201554.933787202
        },
        {
          "variable": "dPAN_dt",
          "time": 0.0,
          "expected": -348560.87235065264
        },
        {
          "variable": "dTOL_dt",
          "time": 0.0,
          "expected": -1.853142590358898e-06
        },
        {
          "variable": "dN2O5_dt",
          "time": 0.0,
          "expected": -32106.600565909124
        },
        {
          "variable": "dXYL_dt",
          "time": 0.0,
          "expected": -7.654695413271516e-06
        },
        {
          "variable": "dCH4_dt",
          "time": 0.0,
          "expected": -372294.19232623046
        },
        {
          "variable": "dCRO_dt",
          "time": 0.0,
          "expected": 6.0746008439604295e-06
        },
        {
          "variable": "dAPI_dt",
          "time": 0.0,
          "expected": -0.009823410396663138
        },
        {
          "variable": "dLIM_dt",
          "time": 0.0,
          "expected": -0.020324293657128092
        },
        {
          "variable": "dHNO4_dt",
          "time": 0.0,
          "expected": -275152.0667873204
        },
        {
          "variable": "dTO2_dt",
          "time": 0.0,
          "expected": 2.498270112493591e-06
        },
        {
          "variable": "dC2H6_dt",
          "time": 0.0,
          "expected": -3359.829303448886
        },
        {
          "variable": "dXPAR_dt",
          "time": 0.0,
          "expected": 781626.5132863278
        },
        {
          "variable": "dETHOOH_dt",
          "time": 0.0,
          "expected": -174771.06871450343
        },
        {
          "variable": "dHONO_dt",
          "time": 0.0,
          "expected": 1361.6430043569758
        },
        {
          "variable": "dCH3OOH_dt",
          "time": 0.0,
          "expected": -349542.13745347597
        },
        {
          "variable": "dC2H4_dt",
          "time": 0.0,
          "expected": -53285.18404614276
        },
        {
          "variable": "dCH3OH_dt",
          "time": 0.0,
          "expected": 8616.851235628379
        },
        {
          "variable": "dCRES_dt",
          "time": 0.0,
          "expected": -2.5647037261171095e-05
        },
        {
          "variable": "dO3P_dt",
          "time": 0.0,
          "expected": 7094078.740081251
        },
        {
          "variable": "dHNO3_dt",
          "time": 0.0,
          "expected": 7384.779901563314
        },
        {
          "variable": "dCO_dt",
          "time": 0.0,
          "expected": -348529.2265978557
        },
        {
          "variable": "dISOPN_dt",
          "time": 0.0,
          "expected": -3.15309691890627e-05
        },
        {
          "variable": "dPAR_dt",
          "time": 0.0,
          "expected": -99828.24886947432
        },
        {
          "variable": "dOPEN_dt",
          "time": 0.0,
          "expected": 5.982283148307289e-06
        },
        {
          "variable": "dISOPP_dt",
          "time": 0.0,
          "expected": -3.123045417389972e-05
        },
        {
          "variable": "dISOPO2_dt",
          "time": 0.0,
          "expected": -3.148442957401364e-05
        },
        {
          "variable": "dOLET_dt",
          "time": 0.0,
          "expected": -102317.97963760888
        },
        {
          "variable": "dISOP_dt",
          "time": 0.0,
          "expected": -3.370515645878994e-07
        },
        {
          "variable": "dHCHO_dt",
          "time": 0.0,
          "expected": 108427.72571403914
        },
        {
          "variable": "dXO2_dt",
          "time": 0.0,
          "expected": 229895.82022953767
        },
        {
          "variable": "dAONE_dt",
          "time": 0.0,
          "expected": 37057.8998687383
        },
        {
          "variable": "dOLEI_dt",
          "time": 0.0,
          "expected": -308983.45831249905
        },
        {
          "variable": "dMGLY_dt",
          "time": 0.0,
          "expected": 14840.732324773395
        },
        {
          "variable": "dETHP_dt",
          "time": 0.0,
          "expected": 138102.9401959635
        },
        {
          "variable": "dNAP_dt",
          "time": 0.0,
          "expected": 7618.1683680559545
        },
        {
          "variable": "dALD2_dt",
          "time": 0.0,
          "expected": 527952.9774230273
        },
        {
          "variable": "dCH3O2_dt",
          "time": 0.0,
          "expected": 653728.4175271279
        },
        {
          "variable": "dISOPRD_dt",
          "time": 0.0,
          "expected": 1.2360519145041408e-06
        },
        {
          "variable": "dROOH_dt",
          "time": 0.0,
          "expected": 0.00011239842657077862
        },
        {
          "variable": "dANO2_dt",
          "time": 0.0,
          "expected": 22212.303775939985
        },
        {
          "variable": "dRO2_dt",
          "time": 0.0,
          "expected": 118499.88995482707
        },
        {
          "variable": "dONIT_dt",
          "time": 0.0,
          "expected": 7.440836572350641e-05
        },
        {
          "variable": "dNO3_dt",
          "time": 0.0,
          "expected": 4731.026944569337
        },
        {
          "variable": "dNO_dt",
          "time": 0.0,
          "expected": -2879451.5707543143
        },
        {
          "variable": "dNO2_dt",
          "time": 0.0,
          "expected": 3546282.0925872517
        },
        {
          "variable": "dOH_dt",
          "time": 0.0,
          "expected": 591890.0926524985
        },
        {
          "variable": "dO3_dt",
          "time": 0.0,
          "expected": -10888275.90688942
        },
        {
          "variable": "dHO2_dt",
          "time": 0.0,
          "expected": -13859662.695769189
        },
        {
          "variable": "dC2O3_dt",
          "time": 0.0,
          "expected": 401730.02117673395
        }
      ]
    },
    {
      "id": "scm_midtrop_afternoon_tendencies",
      "description": "Mid-troposphere, step 601 level 41 (T = 265.53 K, M = 1.3856e19 molec/cm3). Half the surface air density and 43 K colder.\n\nReference: Vdot from cbmz_mosaic_Fun, the KPP-generated right-hand side, evaluated on the dumped var_in with the dumped RCONST by the real64 replay driver kernels/cbmz_driver (a standalone program that calls WRF's KPP-generated cbmz_mosaic routines on the dumped inputs; WRF's KPP is already real64, so this is an independent replay of the same arithmetic rather than a precision upgrade). This is the INSTANTANEOUS rate, which WRF never writes: over its 60 s step the finite increment (var_out - var_in)/60 reaches only 2.7e5 to 8.0e6 molec/cm3/s where Fun reaches 1.1e6 to 3.6e7, a factor of 4 to 35, so a tendency test referenced against differenced states would be testing something else entirely.\n\nShape: each d<SPC>_dt is an observed written D(CBMZ.<SPC>, t), which esm-spec 7.4 resolves to the tendency the reaction system already derives, so asserting it at time 0 evaluates the mechanism's right-hand side at the given state. The time_span is empty ({start: 0, end: 0}), the shape esm-spec 6.6.2 names for a document with ODE states all of whose assertions sit at t0: the runner answers from the initial state without integrating. This adds no physics -- it is the derivative-test surface of the mechanism, and it pins the whole stoichiometric matrix and every rate law at once, independently of any integrator. The peroxy coefficients are live here as everywhere in this document, but at t = 0 that is no different from WRF: the operator split WRF makes -- it computes the ten state-dependent peroxy coefficients once, before INTEGRATE, and holds them at the step's input state for the whole 60 s step -- opens up only as the step proceeds.\n\nHCl and NH3 are absent from the 64: they are reservoir species of this mechanism (see their declarations), so no D(CBMZ.X, t) exists for them. What such an assertion would say -- that the CBM-Z gas phase produces and destroys neither -- is structural in this document rather than numerical.\n\nMeasured: 42 of the 64 assertions are BIT-IDENTICAL to KPP and the largest residual is 1.4e-12 (dOH_dt)\n\nState: data/eqwefic/dumps/chem170_wrf/esm_dump_cbmz_kpp_601.json level k = 41; reference chem170_scm/replay/kp_601.out.json (variable vdot). The run is described in data/eqwefic/notes/chem170_scm_reference_run.md.",
      "time_span": {
        "start": 0,
        "end": 0
      },
      "tolerance": {
        "rel": 1e-09
      },
      "initial_conditions": {
        "CBMZ.H2SO4": 11847540.94704923,
        "CBMZ.HCOOH": 713186777.263838,
        "CBMZ.RCOOH": 1710186635.1802225,
        "CBMZ.ARO1": 0.013215428904178804,
        "CBMZ.ARO2": 0.03414579126401534,
        "CBMZ.ALK1": 32399318.127933003,
        "CBMZ.OLE1": 15236480.198375171,
        "CBMZ.API1": 0.019667536716742557,
        "CBMZ.API2": 0.15927741261444098,
        "CBMZ.LIM1": 0.10941551139760468,
        "CBMZ.LIM2": 0.15927499495675485,
        "CBMZ.SO2": 1310889904.6743295,
        "CBMZ.O1D": 0.003999577834909692,
        "CBMZ.ANOL": 0.0013855662398690011,
        "CBMZ.H2O2": 19454938226.286568,
        "CBMZ.PAN": 378091251.32597,
        "CBMZ.TOL": 0.08695689744210441,
        "CBMZ.N2O5": 837.1965399755329,
        "CBMZ.XYL": 0.024643715857813255,
        "CBMZ.CH4": 23550064280573.51,
        "CBMZ.CRO": 0.0013855662398690011,
        "CBMZ.API": 0.0013855662398690011,
        "CBMZ.LIM": 0.0013855662398690011,
        "CBMZ.HNO4": 7814739.223561938,
        "CBMZ.TO2": 0.00461794293348315,
        "CBMZ.C2H6": 8800251302.712246,
        "CBMZ.XPAR": 31483.13992680837,
        "CBMZ.ETHOOH": 6915395093.916344,
        "CBMZ.HONO": 136902.97403534682,
        "CBMZ.CH3OOH": 16495270440.675514,
        "CBMZ.C2H4": 1500894074.9456296,
        "CBMZ.CH3OH": 507774517.5063688,
        "CBMZ.CRES": 0.01261549771194939,
        "CBMZ.O3P": 936.1915909042899,
        "CBMZ.HNO3": 932479151.0805724,
        "CBMZ.CO": 1111863035121.7878,
        "CBMZ.ISOPN": 0.0013855662398690011,
        "CBMZ.PAR": 48022380948.34894,
        "CBMZ.OPEN": 0.006400610090121497,
        "CBMZ.ISOPP": 0.0013855662398690011,
        "CBMZ.ISOPO2": 0.0013855662398690011,
        "CBMZ.OLET": 123674118.33771768,
        "CBMZ.ISOP": 0.0013855662398690011,
        "CBMZ.HCHO": 3305593800.7833447,
        "CBMZ.XO2": 3695907.9954618416,
        "CBMZ.AONE": 989051089.1044973,
        "CBMZ.OLEI": 222165.83306922263,
        "CBMZ.MGLY": 11006220.837409338,
        "CBMZ.ETHP": 14463157.811701568,
        "CBMZ.NAP": 5055.303490329639,
        "CBMZ.ALD2": 3510003876.4139476,
        "CBMZ.CH3O2": 78506177.00101075,
        "CBMZ.ISOPRD": 0.010581683526693638,
        "CBMZ.ROOH": 1426778722.8211954,
        "CBMZ.ANO2": 34436.002799633556,
        "CBMZ.RO2": 4628614.492934034,
        "CBMZ.ONIT": 15365691.230273679,
        "CBMZ.NO3": 10300.691630687637,
        "CBMZ.NO": 13768698.134249192,
        "CBMZ.NO2": 50453990.6740849,
        "CBMZ.OH": 323905.0927830306,
        "CBMZ.O3": 408235731433.6474,
        "CBMZ.HO2": 78616164.21380737,
        "CBMZ.C2O3": 6610929.463040047
      },
      "parameter_overrides": {
        "CBMZ.H2O": 3.797923615735808e+16,
        "CBMZ.M": 1.3855661803675058e+19,
        "CBMZRateConstants.T": 265.53271484375,
        "CBMZRateConstants.j_o31d": 4.190368144918466e-06,
        "CBMZRateConstants.j_o33p": 6.95342241670005e-05,
        "CBMZRateConstants.j_no2": 0.0016093809390440583,
        "CBMZRateConstants.j_no3o": 0.02909519150853157,
        "CBMZRateConstants.j_hno2": 0.00036650561378337443,
        "CBMZRateConstants.j_hno3": 1.150374586700309e-07,
        "CBMZRateConstants.j_hno4": 7.747925678813772e-07,
        "CBMZRateConstants.j_h2o2": 1.4816707789577777e-06,
        "CBMZRateConstants.j_ch2or": 5.617866918328218e-06,
        "CBMZRateConstants.j_ch2om": 9.354756002721842e-06,
        "CBMZRateConstants.j_n2o5": 0.0,
        "CBMZ.HCl": 1635605727.649102,
        "CBMZ.NH3": 1768266.667950874
      },
      "assertions": [
        {
          "variable": "dH2SO4_dt",
          "time": 0.0,
          "expected": 354.50686311275496
        },
        {
          "variable": "dHCOOH_dt",
          "time": 0.0,
          "expected": 244.023033263407
        },
        {
          "variable": "dRCOOH_dt",
          "time": 0.0,
          "expected": 4066.752932103549
        },
        {
          "variable": "dARO1_dt",
          "time": 0.0,
          "expected": 2.2593169322274044e-08
        },
        {
          "variable": "dARO2_dt",
          "time": 0.0,
          "expected": 6.25656999936982e-08
        },
        {
          "variable": "dALK1_dt",
          "time": 0.0,
          "expected": 151.19162462969328
        },
        {
          "variable": "dOLE1_dt",
          "time": 0.0,
          "expected": 13.367482847904036
        },
        {
          "variable": "dAPI1_dt",
          "time": 0.0,
          "expected": 9.374170010155187e-05
        },
        {
          "variable": "dAPI2_dt",
          "time": 0.0,
          "expected": 0.0008095873963118291
        },
        {
          "variable": "dLIM1_dt",
          "time": 0.0,
          "expected": 0.0008971041153502436
        },
        {
          "variable": "dLIM2_dt",
          "time": 0.0,
          "expected": 0.0013111523478122919
        },
        {
          "variable": "dSO2_dt",
          "time": 0.0,
          "expected": -354.50686311275496
        },
        {
          "variable": "dO1D_dt",
          "time": 0.0,
          "expected": 25.90647316184186
        },
        {
          "variable": "dANOL_dt",
          "time": 0.0,
          "expected": -1.2965423023307812e-09
        },
        {
          "variable": "dH2O2_dt",
          "time": 0.0,
          "expected": -14725.32338377923
        },
        {
          "variable": "dPAN_dt",
          "time": 0.0,
          "expected": 2893.3961376880934
        },
        {
          "variable": "dTOL_dt",
          "time": 0.0,
          "expected": -1.9888003076010327e-07
        },
        {
          "variable": "dN2O5_dt",
          "time": 0.0,
          "expected": 0.21056070803115495
        },
        {
          "variable": "dXYL_dt",
          "time": 0.0,
          "expected": -2.100379452217936e-07
        },
        {
          "variable": "dCH4_dt",
          "time": 0.0,
          "expected": -23450.578863683746
        },
        {
          "variable": "dCRO_dt",
          "time": 0.0,
          "expected": -9.088299083964851e-07
        },
        {
          "variable": "dAPI_dt",
          "time": 0.0,
          "expected": -0.004261006889774636
        },
        {
          "variable": "dLIM_dt",
          "time": 0.0,
          "expected": -0.006900856041497088
        },
        {
          "variable": "dHNO4_dt",
          "time": 0.0,
          "expected": -2201.289029301972
        },
        {
          "variable": "dTO2_dt",
          "time": 0.0,
          "expected": -2.614017044189043e-07
        },
        {
          "variable": "dC2H6_dt",
          "time": 0.0,
          "expected": -317.3164905006506
        },
        {
          "variable": "dXPAR_dt",
          "time": 0.0,
          "expected": -32.57622868401658
        },
        {
          "variable": "dETHOOH_dt",
          "time": 0.0,
          "expected": -13344.644309018699
        },
        {
          "variable": "dHONO_dt",
          "time": 0.0,
          "expected": -20.044383422169293
        },
        {
          "variable": "dCH3OOH_dt",
          "time": 0.0,
          "expected": -12513.695501350041
        },
        {
          "variable": "dC2H4_dt",
          "time": 0.0,
          "expected": -4274.517033980743
        },
        {
          "variable": "dCH3OH_dt",
          "time": 0.0,
          "expected": 3775.6486870237886
        },
        {
          "variable": "dCRES_dt",
          "time": 0.0,
          "expected": -1.3602654539462706e-07
        },
        {
          "variable": "dO3P_dt",
          "time": 0.0,
          "expected": 160505.1296033498
        },
        {
          "variable": "dHNO3_dt",
          "time": 0.0,
          "expected": -11.480392911260946
        },
        {
          "variable": "dCO_dt",
          "time": 0.0,
          "expected": -6714.988957172872
        },
        {
          "variable": "dISOPN_dt",
          "time": 0.0,
          "expected": -2.8834305467577072e-06
        },
        {
          "variable": "dPAR_dt",
          "time": 0.0,
          "expected": -27718.255327129496
        },
        {
          "variable": "dOPEN_dt",
          "time": 0.0,
          "expected": 1.3081244461227373e-07
        },
        {
          "variable": "dISOPP_dt",
          "time": 0.0,
          "expected": -2.828993010646291e-06
        },
        {
          "variable": "dISOPO2_dt",
          "time": 0.0,
          "expected": -2.826885420018177e-06
        },
        {
          "variable": "dOLET_dt",
          "time": 0.0,
          "expected": -1647.0341764102718
        },
        {
          "variable": "dISOP_dt",
          "time": 0.0,
          "expected": -5.791559551024339e-08
        },
        {
          "variable": "dHCHO_dt",
          "time": 0.0,
          "expected": -5181.44972686427
        },
        {
          "variable": "dXO2_dt",
          "time": 0.0,
          "expected": 6.083605561856984
        },
        {
          "variable": "dAONE_dt",
          "time": 0.0,
          "expected": 4932.719124742479
        },
        {
          "variable": "dOLEI_dt",
          "time": 0.0,
          "expected": -23.90110021256564
        },
        {
          "variable": "dMGLY_dt",
          "time": 0.0,
          "expected": 63.98173948926695
        },
        {
          "variable": "dETHP_dt",
          "time": 0.0,
          "expected": -1000.1826458492781
        },
        {
          "variable": "dNAP_dt",
          "time": 0.0,
          "expected": 0.12237400644521468
        },
        {
          "variable": "dALD2_dt",
          "time": 0.0,
          "expected": -461.13269476193204
        },
        {
          "variable": "dCH3O2_dt",
          "time": 0.0,
          "expected": -6672.411268275278
        },
        {
          "variable": "dISOPRD_dt",
          "time": 0.0,
          "expected": 2.7189586718484047e-07
        },
        {
          "variable": "dROOH_dt",
          "time": 0.0,
          "expected": 3106.505876557562
        },
        {
          "variable": "dANO2_dt",
          "time": 0.0,
          "expected": -0.06773889154294732
        },
        {
          "variable": "dRO2_dt",
          "time": 0.0,
          "expected": 200.5622824846114
        },
        {
          "variable": "dONIT_dt",
          "time": 0.0,
          "expected": 37.56767919845616
        },
        {
          "variable": "dNO3_dt",
          "time": 0.0,
          "expected": -0.9061809592921589
        },
        {
          "variable": "dNO_dt",
          "time": 0.0,
          "expected": 166.63645141161695
        },
        {
          "variable": "dNO2_dt",
          "time": 0.0,
          "expected": -864.4237863056418
        },
        {
          "variable": "dOH_dt",
          "time": 0.0,
          "expected": 10.576781250298021
        },
        {
          "variable": "dO3_dt",
          "time": 0.0,
          "expected": -226842.921019744
        },
        {
          "variable": "dHO2_dt",
          "time": 0.0,
          "expected": -1244.1824742242566
        },
        {
          "variable": "dC2O3_dt",
          "time": 0.0,
          "expected": 44.8465631264735
        }
      ]
    },
    {
      "id": "scm_boundary_layer_evening_tendencies",
      "description": "Boundary-layer top at 17 LST, step 2101 level 21 (T = 291.17 K, M = 2.0171e19 molec/cm3). A well-aged photochemical state 35 h into the run, so the secondary species carry real burdens rather than their initial-profile values.\n\nReference: Vdot from cbmz_mosaic_Fun, the KPP-generated right-hand side, evaluated on the dumped var_in with the dumped RCONST by the real64 replay driver kernels/cbmz_driver (a standalone program that calls WRF's KPP-generated cbmz_mosaic routines on the dumped inputs; WRF's KPP is already real64, so this is an independent replay of the same arithmetic rather than a precision upgrade). This is the INSTANTANEOUS rate, which WRF never writes: over its 60 s step the finite increment (var_out - var_in)/60 reaches only 2.7e5 to 8.0e6 molec/cm3/s where Fun reaches 1.1e6 to 3.6e7, a factor of 4 to 35, so a tendency test referenced against differenced states would be testing something else entirely.\n\nShape: each d<SPC>_dt is an observed written D(CBMZ.<SPC>, t), which esm-spec 7.4 resolves to the tendency the reaction system already derives, so asserting it at time 0 evaluates the mechanism's right-hand side at the given state. The time_span is empty ({start: 0, end: 0}), the shape esm-spec 6.6.2 names for a document with ODE states all of whose assertions sit at t0: the runner answers from the initial state without integrating. This adds no physics -- it is the derivative-test surface of the mechanism, and it pins the whole stoichiometric matrix and every rate law at once, independently of any integrator. The peroxy coefficients are live here as everywhere in this document, but at t = 0 that is no different from WRF: the operator split WRF makes -- it computes the ten state-dependent peroxy coefficients once, before INTEGRATE, and holds them at the step's input state for the whole 60 s step -- opens up only as the step proceeds.\n\nHCl and NH3 are absent from the 64: they are reservoir species of this mechanism (see their declarations), so no D(CBMZ.X, t) exists for them. What such an assertion would say -- that the CBM-Z gas phase produces and destroys neither -- is structural in this document rather than numerical.\n\nMeasured: 45 of the 64 assertions are BIT-IDENTICAL to KPP and the largest residual is 1.8e-14 (dXPAR_dt)\n\nState: data/eqwefic/dumps/chem170_wrf/esm_dump_cbmz_kpp_2101.json level k = 21; reference chem170_scm/replay/kp_2101.out.json (variable vdot). The run is described in data/eqwefic/notes/chem170_scm_reference_run.md.",
      "time_span": {
        "start": 0,
        "end": 0
      },
      "tolerance": {
        "rel": 1e-09
      },
      "initial_conditions": {
        "CBMZ.H2SO4": 14805431.257794367,
        "CBMZ.HCOOH": 874488339.7339191,
        "CBMZ.RCOOH": 4109649222.6035433,
        "CBMZ.ARO1": 0.026962404302894958,
        "CBMZ.ARO2": 0.07109703767048507,
        "CBMZ.ALK1": 156208360.95129856,
        "CBMZ.OLE1": 23610450.994069703,
        "CBMZ.API1": 0.09513694358994965,
        "CBMZ.API2": 0.8062716390168456,
        "CBMZ.LIM1": 0.5522834684938772,
        "CBMZ.LIM2": 0.8062567405582417,
        "CBMZ.SO2": 1261628460.8926244,
        "CBMZ.O1D": 0.002954947273254597,
        "CBMZ.ANOL": 0.0020170866612402574,
        "CBMZ.H2O2": 39892139100.13111,
        "CBMZ.PAN": 96793836.03175862,
        "CBMZ.TOL": 0.04158971352305638,
        "CBMZ.N2O5": 290.6666463952859,
        "CBMZ.XYL": 0.0020170866612402574,
        "CBMZ.CH4": 34165217969042.117,
        "CBMZ.CRO": 0.0020170866612402574,
        "CBMZ.API": 0.0020170866612402574,
        "CBMZ.LIM": 0.0020170866612402574,
        "CBMZ.HNO4": 764921.6641667098,
        "CBMZ.TO2": 0.0020170866612402574,
        "CBMZ.C2H6": 12258724809.951603,
        "CBMZ.XPAR": 77287.39737629013,
        "CBMZ.ETHOOH": 4214383838.356277,
        "CBMZ.HONO": 371940.8439136318,
        "CBMZ.CH3OOH": 28202272273.290115,
        "CBMZ.C2H4": 432013375.61711,
        "CBMZ.CH3OH": 5391883266.731131,
        "CBMZ.CRES": 0.0020170866612402574,
        "CBMZ.O3P": 926.004191225174,
        "CBMZ.HNO3": 1196059290.961729,
        "CBMZ.CO": 1583356247670.3655,
        "CBMZ.ISOPN": 0.0020170866612402574,
        "CBMZ.PAR": 49165660987.431816,
        "CBMZ.OPEN": 0.004003400135506379,
        "CBMZ.ISOPP": 0.0020170866612402574,
        "CBMZ.ISOPO2": 0.0020170866612402574,
        "CBMZ.OLET": 1125548.548398567,
        "CBMZ.ISOP": 0.0020170866612402574,
        "CBMZ.HCHO": 7623844185.76056,
        "CBMZ.XO2": 3478170.0898351567,
        "CBMZ.AONE": 5587299707.972182,
        "CBMZ.OLEI": 0.0020170866612402574,
        "CBMZ.MGLY": 41762419.68325026,
        "CBMZ.ETHP": 12024767.094067333,
        "CBMZ.NAP": 46571.86290084972,
        "CBMZ.ALD2": 2550446411.6127834,
        "CBMZ.CH3O2": 192718783.80884176,
        "CBMZ.ISOPRD": 0.01738139372753668,
        "CBMZ.ROOH": 2543676263.575171,
        "CBMZ.ANO2": 382737.265596396,
        "CBMZ.RO2": 7440550.50874509,
        "CBMZ.ONIT": 70080259.87318046,
        "CBMZ.NO3": 32450.089826708994,
        "CBMZ.NO": 31299489.683780853,
        "CBMZ.NO2": 135027882.0027851,
        "CBMZ.OH": 669354.0661303757,
        "CBMZ.O3": 427254380406.4668,
        "CBMZ.HO2": 150672741.26303324,
        "CBMZ.C2O3": 8482814.423056977
      },
      "parameter_overrides": {
        "CBMZ.H2O": 2.784622633109422e+17,
        "CBMZ.M": 2.017086626699254e+19,
        "CBMZRateConstants.T": 291.17279052734375,
        "CBMZRateConstants.j_o31d": 4.450288088264642e-06,
        "CBMZRateConstants.j_o33p": 0.00011352879664627835,
        "CBMZRateConstants.j_no2": 0.002311962191015482,
        "CBMZRateConstants.j_no3o": 0.04923992604017258,
        "CBMZRateConstants.j_hno2": 0.0005148722557350993,
        "CBMZRateConstants.j_hno3": 1.2324466069912887e-07,
        "CBMZRateConstants.j_hno4": 8.289279094242374e-07,
        "CBMZRateConstants.j_h2o2": 1.7962703395824065e-06,
        "CBMZRateConstants.j_ch2or": 6.516909706988372e-06,
        "CBMZRateConstants.j_ch2om": 1.1636845556495246e-05,
        "CBMZRateConstants.j_n2o5": 0.0,
        "CBMZ.HCl": 4987006986.776166,
        "CBMZ.NH3": 4093142.822379669
      },
      "assertions": [
        {
          "variable": "dH2SO4_dt",
          "time": 0.0,
          "expected": 721.964206134774
        },
        {
          "variable": "dHCOOH_dt",
          "time": 0.0,
          "expected": 138.5220931245124
        },
        {
          "variable": "dRCOOH_dt",
          "time": 0.0,
          "expected": 7135.185784967911
        },
        {
          "variable": "dARO1_dt",
          "time": 0.0,
          "expected": 1.0437990362151366e-08
        },
        {
          "variable": "dARO2_dt",
          "time": 0.0,
          "expected": 2.8905204233194482e-08
        },
        {
          "variable": "dALK1_dt",
          "time": 0.0,
          "expected": 319.8777679128793
        },
        {
          "variable": "dOLE1_dt",
          "time": 0.0,
          "expected": 0.2138997517873956
        },
        {
          "variable": "dAPI1_dt",
          "time": 0.0,
          "expected": 0.00012140448022677937
        },
        {
          "variable": "dAPI2_dt",
          "time": 0.0,
          "expected": 0.0010484932103759525
        },
        {
          "variable": "dLIM1_dt",
          "time": 0.0,
          "expected": 0.0013668377433490564
        },
        {
          "variable": "dLIM2_dt",
          "time": 0.0,
          "expected": 0.0019976864247840923
        },
        {
          "variable": "dSO2_dt",
          "time": 0.0,
          "expected": -721.964206134774
        },
        {
          "variable": "dO1D_dt",
          "time": 0.0,
          "expected": -25649.234339016723
        },
        {
          "variable": "dANOL_dt",
          "time": 0.0,
          "expected": -4.216651598651749e-09
        },
        {
          "variable": "dH2O2_dt",
          "time": 0.0,
          "expected": -2680.438191087109
        },
        {
          "variable": "dPAN_dt",
          "time": 0.0,
          "expected": -2272.305131971072
        },
        {
          "variable": "dTOL_dt",
          "time": 0.0,
          "expected": -1.7665888342938746e-07
        },
        {
          "variable": "dN2O5_dt",
          "time": 0.0,
          "expected": 0.05124540931304633
        },
        {
          "variable": "dXYL_dt",
          "time": 0.0,
          "expected": -3.41859359156689e-08
        },
        {
          "variable": "dCH4_dt",
          "time": 0.0,
          "expected": -126129.83051113039
        },
        {
          "variable": "dCRO_dt",
          "time": 0.0,
          "expected": -3.789498772484837e-06
        },
        {
          "variable": "dAPI_dt",
          "time": 0.0,
          "expected": -0.0055184387189933706
        },
        {
          "variable": "dLIM_dt",
          "time": 0.0,
          "expected": -0.010514302037262314
        },
        {
          "variable": "dHNO4_dt",
          "time": 0.0,
          "expected": 79.64865929072766
        },
        {
          "variable": "dTO2_dt",
          "time": 0.0,
          "expected": -3.546728638687585e-07
        },
        {
          "variable": "dC2H6_dt",
          "time": 0.0,
          "expected": -1684.119773975869
        },
        {
          "variable": "dXPAR_dt",
          "time": 0.0,
          "expected": -202.4685390161762
        },
        {
          "variable": "dETHOOH_dt",
          "time": 0.0,
          "expected": -11564.095204366718
        },
        {
          "variable": "dHONO_dt",
          "time": 0.0,
          "expected": -38.94385134534205
        },
        {
          "variable": "dCH3OOH_dt",
          "time": 0.0,
          "expected": -5856.879398708232
        },
        {
          "variable": "dC2H4_dt",
          "time": 0.0,
          "expected": -2610.3471235673337
        },
        {
          "variable": "dCH3OH_dt",
          "time": 0.0,
          "expected": 11502.083962094854
        },
        {
          "variable": "dCRES_dt",
          "time": 0.0,
          "expected": -3.3887591290635583e-08
        },
        {
          "variable": "dO3P_dt",
          "time": 0.0,
          "expected": -281618.35224389454
        },
        {
          "variable": "dHNO3_dt",
          "time": 0.0,
          "expected": 522.6917195359791
        },
        {
          "variable": "dCO_dt",
          "time": 0.0,
          "expected": -40516.557246180426
        },
        {
          "variable": "dISOPN_dt",
          "time": 0.0,
          "expected": -5.510961398328352e-06
        },
        {
          "variable": "dPAR_dt",
          "time": 0.0,
          "expected": -64655.34019673133
        },
        {
          "variable": "dOPEN_dt",
          "time": 0.0,
          "expected": 1.6959271097843543e-07
        },
        {
          "variable": "dISOPP_dt",
          "time": 0.0,
          "expected": -5.36798550530808e-06
        },
        {
          "variable": "dISOPO2_dt",
          "time": 0.0,
          "expected": -5.319037786002218e-06
        },
        {
          "variable": "dOLET_dt",
          "time": 0.0,
          "expected": -26.737467409719915
        },
        {
          "variable": "dISOP_dt",
          "time": 0.0,
          "expected": -1.5334406982730964e-07
        },
        {
          "variable": "dHCHO_dt",
          "time": 0.0,
          "expected": -28358.210417833594
        },
        {
          "variable": "dXO2_dt",
          "time": 0.0,
          "expected": -356.61467035720443
        },
        {
          "variable": "dAONE_dt",
          "time": 0.0,
          "expected": 12343.93105641699
        },
        {
          "variable": "dOLEI_dt",
          "time": 0.0,
          "expected": -2.9374296035182877e-07
        },
        {
          "variable": "dMGLY_dt",
          "time": 0.0,
          "expected": -633.1775560907315
        },
        {
          "variable": "dETHP_dt",
          "time": 0.0,
          "expected": -1269.967443025162
        },
        {
          "variable": "dNAP_dt",
          "time": 0.0,
          "expected": -4.509760543671009
        },
        {
          "variable": "dALD2_dt",
          "time": 0.0,
          "expected": -4426.281787194443
        },
        {
          "variable": "dCH3O2_dt",
          "time": 0.0,
          "expected": -19159.997920815826
        },
        {
          "variable": "dISOPRD_dt",
          "time": 0.0,
          "expected": 6.149313662954615e-07
        },
        {
          "variable": "dROOH_dt",
          "time": 0.0,
          "expected": 1104.8249719473033
        },
        {
          "variable": "dANO2_dt",
          "time": 0.0,
          "expected": -35.16527049332515
        },
        {
          "variable": "dRO2_dt",
          "time": 0.0,
          "expected": -470.36666789945957
        },
        {
          "variable": "dONIT_dt",
          "time": 0.0,
          "expected": 128.19136812958558
        },
        {
          "variable": "dNO3_dt",
          "time": 0.0,
          "expected": 8.221938756192577
        },
        {
          "variable": "dNO_dt",
          "time": 0.0,
          "expected": -1931.8278417242304
        },
        {
          "variable": "dNO2_dt",
          "time": 0.0,
          "expected": 3508.7303629923795
        },
        {
          "variable": "dOH_dt",
          "time": 0.0,
          "expected": -1679.9558711547613
        },
        {
          "variable": "dO3_dt",
          "time": 0.0,
          "expected": 81553.27857045054
        },
        {
          "variable": "dHO2_dt",
          "time": 0.0,
          "expected": -9991.144062991889
        },
        {
          "variable": "dC2O3_dt",
          "time": 0.0,
          "expected": -739.7627484056384
        }
      ]
    },
    {
      "id": "scm_upper_trop_morning_tendencies",
      "description": "Upper troposphere, step 230 level 56 (T = 213.13 K, M = 5.4026e18 molec/cm3, the strongest photolysis in the run). The coldest and thinnest state of the column.\n\nReference: Vdot from cbmz_mosaic_Fun, the KPP-generated right-hand side, evaluated on the dumped var_in with the dumped RCONST by the real64 replay driver kernels/cbmz_driver (a standalone program that calls WRF's KPP-generated cbmz_mosaic routines on the dumped inputs; WRF's KPP is already real64, so this is an independent replay of the same arithmetic rather than a precision upgrade). This is the INSTANTANEOUS rate, which WRF never writes: over its 60 s step the finite increment (var_out - var_in)/60 reaches only 2.7e5 to 8.0e6 molec/cm3/s where Fun reaches 1.1e6 to 3.6e7, a factor of 4 to 35, so a tendency test referenced against differenced states would be testing something else entirely.\n\nShape: each d<SPC>_dt is an observed written D(CBMZ.<SPC>, t), which esm-spec 7.4 resolves to the tendency the reaction system already derives, so asserting it at time 0 evaluates the mechanism's right-hand side at the given state. The time_span is empty ({start: 0, end: 0}), the shape esm-spec 6.6.2 names for a document with ODE states all of whose assertions sit at t0: the runner answers from the initial state without integrating. This adds no physics -- it is the derivative-test surface of the mechanism, and it pins the whole stoichiometric matrix and every rate law at once, independently of any integrator. The peroxy coefficients are live here as everywhere in this document, but at t = 0 that is no different from WRF: the operator split WRF makes -- it computes the ten state-dependent peroxy coefficients once, before INTEGRATE, and holds them at the step's input state for the whole 60 s step -- opens up only as the step proceeds.\n\nHCl and NH3 are absent from the 64: they are reservoir species of this mechanism (see their declarations), so no D(CBMZ.X, t) exists for them. What such an assertion would say -- that the CBM-Z gas phase produces and destroys neither -- is structural in this document rather than numerical.\n\nMeasured: 47 of the 64 assertions are BIT-IDENTICAL to KPP and the largest residual is 1.4e-13 (dNO2_dt)\n\nState: data/eqwefic/dumps/chem170_wrf/esm_dump_cbmz_kpp_230.json level k = 56; reference chem170_scm/replay/kp_230.out.json (variable vdot). The run is described in data/eqwefic/notes/chem170_scm_reference_run.md.",
      "time_span": {
        "start": 0,
        "end": 0
      },
      "tolerance": {
        "rel": 1e-09
      },
      "initial_conditions": {
        "CBMZ.H2SO4": 1811387.8405784573,
        "CBMZ.HCOOH": 270369052.50548035,
        "CBMZ.RCOOH": 405261325.06435287,
        "CBMZ.ARO1": 0.0026348647707279465,
        "CBMZ.ARO2": 0.006340923442538957,
        "CBMZ.ALK1": 3202550.74634394,
        "CBMZ.OLE1": 4206172.892542022,
        "CBMZ.API1": 0.0032609383765461776,
        "CBMZ.API2": 0.024037967760510984,
        "CBMZ.LIM1": 0.016617031532120404,
        "CBMZ.LIM2": 0.02403729048480456,
        "CBMZ.SO2": 533732585.7525701,
        "CBMZ.O1D": 0.046466344042827554,
        "CBMZ.ANOL": 0.0005402609075876606,
        "CBMZ.H2O2": 7331866956.266747,
        "CBMZ.PAN": 69086045.17539033,
        "CBMZ.TOL": 0.04651324538549759,
        "CBMZ.N2O5": 68680.79886887764,
        "CBMZ.XYL": 0.03406547390812569,
        "CBMZ.CH4": 9184494856048.287,
        "CBMZ.CRO": 0.00457110077350483,
        "CBMZ.API": 0.0005402609075876606,
        "CBMZ.LIM": 0.0005402609075876606,
        "CBMZ.HNO4": 36264448.83092496,
        "CBMZ.TO2": 0.0026002547808804156,
        "CBMZ.C2H6": 3455116626.404724,
        "CBMZ.XPAR": 252657.09694052048,
        "CBMZ.ETHOOH": 3526576885.2025046,
        "CBMZ.HONO": 167707.14734599978,
        "CBMZ.CH3OOH": 7164695524.134667,
        "CBMZ.C2H4": 884098134.2221612,
        "CBMZ.CH3OH": 14043006.68202382,
        "CBMZ.CRES": 0.029690140135182133,
        "CBMZ.O3P": 15670.554731691816,
        "CBMZ.HNO3": 367532757.85080326,
        "CBMZ.CO": 434186019086.59924,
        "CBMZ.ISOPN": 0.0005402609075876606,
        "CBMZ.PAR": 20457800552.907276,
        "CBMZ.OPEN": 0.003633820982665567,
        "CBMZ.ISOPP": 0.0005402609075876606,
        "CBMZ.ISOPO2": 0.0005402609075876606,
        "CBMZ.OLET": 222744013.99590564,
        "CBMZ.ISOP": 0.0005402609075876606,
        "CBMZ.HCHO": 1554056535.7512794,
        "CBMZ.XO2": 3927426.190717308,
        "CBMZ.AONE": 138867822.9749797,
        "CBMZ.OLEI": 42441090.46456618,
        "CBMZ.MGLY": 1230953.7098337566,
        "CBMZ.ETHP": 11504806.346635204,
        "CBMZ.NAP": 265.098892085952,
        "CBMZ.ALD2": 1189860731.5401313,
        "CBMZ.CH3O2": 36883543.35594019,
        "CBMZ.ISOPRD": 0.0023661921006950634,
        "CBMZ.ROOH": 223585603.21664065,
        "CBMZ.ANO2": 16702.32271785899,
        "CBMZ.RO2": 2675215.13737437,
        "CBMZ.ONIT": 1275687.2140389304,
        "CBMZ.NO3": 944.4484697359901,
        "CBMZ.NO": 66316499.443752676,
        "CBMZ.NO2": 11425137.757762901,
        "CBMZ.OH": 1767684.666015048,
        "CBMZ.O3": 163570739261.9892,
        "CBMZ.HO2": 138576257.19121563,
        "CBMZ.C2O3": 4626199.438994764
      },
      "parameter_overrides": {
        "CBMZ.H2O": 348292655349760.0,
        "CBMZ.M": 5.402608162995962e+18,
        "CBMZRateConstants.T": 213.1254425048828,
        "CBMZRateConstants.j_o31d": 5.1105926104355603e-05,
        "CBMZRateConstants.j_o33p": 0.000720627314876765,
        "CBMZRateConstants.j_no2": 0.01589580997824669,
        "CBMZRateConstants.j_no3o": 0.3092559576034546,
        "CBMZRateConstants.j_hno2": 0.0035564873833209276,
        "CBMZRateConstants.j_hno3": 1.3515866612578975e-06,
        "CBMZRateConstants.j_hno4": 8.961714229371864e-06,
        "CBMZRateConstants.j_h2o2": 1.5117954717425164e-05,
        "CBMZRateConstants.j_ch2or": 5.850818342878483e-05,
        "CBMZRateConstants.j_ch2om": 9.562480408931151e-05,
        "CBMZRateConstants.j_n2o5": 0.0,
        "CBMZ.HCl": 692073807.2491941,
        "CBMZ.NH3": 0.011926014060986851
      },
      "assertions": [
        {
          "variable": "dH2SO4_dt",
          "time": 0.0,
          "expected": 729.3609037771017
        },
        {
          "variable": "dHCOOH_dt",
          "time": 0.0,
          "expected": 11.177620093263663
        },
        {
          "variable": "dRCOOH_dt",
          "time": 0.0,
          "expected": 12747.203085092422
        },
        {
          "variable": "dARO1_dt",
          "time": 0.0,
          "expected": 1.8325589865645555e-07
        },
        {
          "variable": "dARO2_dt",
          "time": 0.0,
          "expected": 5.074778758955155e-07
        },
        {
          "variable": "dALK1_dt",
          "time": 0.0,
          "expected": 351.5037831385003
        },
        {
          "variable": "dOLE1_dt",
          "time": 0.0,
          "expected": 237.7988862678649
        },
        {
          "variable": "dAPI1_dt",
          "time": 0.0,
          "expected": 2.3055956589636884e-05
        },
        {
          "variable": "dAPI2_dt",
          "time": 0.0,
          "expected": 0.00019911959836353146
        },
        {
          "variable": "dLIM1_dt",
          "time": 0.0,
          "expected": 0.00014016224662615064
        },
        {
          "variable": "dLIM2_dt",
          "time": 0.0,
          "expected": 0.00020485283329476793
        },
        {
          "variable": "dSO2_dt",
          "time": 0.0,
          "expected": -729.3609037771017
        },
        {
          "variable": "dO1D_dt",
          "time": 0.0,
          "expected": 31711.23422942692
        },
        {
          "variable": "dANOL_dt",
          "time": 0.0,
          "expected": -2.2194083254880037e-09
        },
        {
          "variable": "dH2O2_dt",
          "time": 0.0,
          "expected": -34218.506244615484
        },
        {
          "variable": "dPAN_dt",
          "time": 0.0,
          "expected": 756.1846297196684
        },
        {
          "variable": "dTOL_dt",
          "time": 0.0,
          "expected": -7.822640619705796e-07
        },
        {
          "variable": "dN2O5_dt",
          "time": 0.0,
          "expected": -0.032808370462773365
        },
        {
          "variable": "dXYL_dt",
          "time": 0.0,
          "expected": -1.7641931162360069e-06
        },
        {
          "variable": "dCH4_dt",
          "time": 0.0,
          "expected": -9951.195219142492
        },
        {
          "variable": "dCRO_dt",
          "time": 0.0,
          "expected": 1.301785353624509e-07
        },
        {
          "variable": "dAPI_dt",
          "time": 0.0,
          "expected": -0.0010480638365412472
        },
        {
          "variable": "dLIM_dt",
          "time": 0.0,
          "expected": -0.0010782879946590583
        },
        {
          "variable": "dHNO4_dt",
          "time": 0.0,
          "expected": 1329.730915247313
        },
        {
          "variable": "dTO2_dt",
          "time": 0.0,
          "expected": 2.293580286520253e-08
        },
        {
          "variable": "dC2H6_dt",
          "time": 0.0,
          "expected": -325.1096849453735
        },
        {
          "variable": "dXPAR_dt",
          "time": 0.0,
          "expected": -17.57804999385919
        },
        {
          "variable": "dETHOOH_dt",
          "time": 0.0,
          "expected": -65947.94922576525
        },
        {
          "variable": "dHONO_dt",
          "time": 0.0,
          "expected": -1.0152471197691657
        },
        {
          "variable": "dCH3OOH_dt",
          "time": 0.0,
          "expected": -115939.95744041976
        },
        {
          "variable": "dC2H4_dt",
          "time": 0.0,
          "expected": -12174.7563042209
        },
        {
          "variable": "dCH3OH_dt",
          "time": 0.0,
          "expected": 1647.6389285319526
        },
        {
          "variable": "dCRES_dt",
          "time": 0.0,
          "expected": -1.9703305786994474e-06
        },
        {
          "variable": "dO3P_dt",
          "time": 0.0,
          "expected": -146358.89150588648
        },
        {
          "variable": "dHNO3_dt",
          "time": 0.0,
          "expected": -541.6874454553648
        },
        {
          "variable": "dCO_dt",
          "time": 0.0,
          "expected": 150734.46833814774
        },
        {
          "variable": "dISOPN_dt",
          "time": 0.0,
          "expected": -5.949028896280193e-06
        },
        {
          "variable": "dPAR_dt",
          "time": 0.0,
          "expected": -80980.0666346425
        },
        {
          "variable": "dOPEN_dt",
          "time": 0.0,
          "expected": -1.4529266701048467e-07
        },
        {
          "variable": "dISOPP_dt",
          "time": 0.0,
          "expected": -5.779822285160565e-06
        },
        {
          "variable": "dISOPO2_dt",
          "time": 0.0,
          "expected": -5.880014840471451e-06
        },
        {
          "variable": "dOLET_dt",
          "time": 0.0,
          "expected": -21544.788666946853
        },
        {
          "variable": "dISOP_dt",
          "time": 0.0,
          "expected": -1.6929084156473625e-07
        },
        {
          "variable": "dHCHO_dt",
          "time": 0.0,
          "expected": -83305.43820310391
        },
        {
          "variable": "dXO2_dt",
          "time": 0.0,
          "expected": -254.64583554840624
        },
        {
          "variable": "dAONE_dt",
          "time": 0.0,
          "expected": 5712.659860438036
        },
        {
          "variable": "dOLEI_dt",
          "time": 0.0,
          "expected": -8180.0707046812
        },
        {
          "variable": "dMGLY_dt",
          "time": 0.0,
          "expected": 68.46064886051334
        },
        {
          "variable": "dETHP_dt",
          "time": 0.0,
          "expected": 42.803508336627715
        },
        {
          "variable": "dNAP_dt",
          "time": 0.0,
          "expected": 0.025364191522523283
        },
        {
          "variable": "dALD2_dt",
          "time": 0.0,
          "expected": 56013.98355050501
        },
        {
          "variable": "dCH3O2_dt",
          "time": 0.0,
          "expected": 548.4140516298969
        },
        {
          "variable": "dISOPRD_dt",
          "time": 0.0,
          "expected": 1.455582100030607e-07
        },
        {
          "variable": "dROOH_dt",
          "time": 0.0,
          "expected": 22009.550655359697
        },
        {
          "variable": "dANO2_dt",
          "time": 0.0,
          "expected": -2.361289507242901
        },
        {
          "variable": "dRO2_dt",
          "time": 0.0,
          "expected": 49.39050690862996
        },
        {
          "variable": "dONIT_dt",
          "time": 0.0,
          "expected": 111.5129666663231
        },
        {
          "variable": "dNO3_dt",
          "time": 0.0,
          "expected": 0.4219432714236906
        },
        {
          "variable": "dNO_dt",
          "time": 0.0,
          "expected": -1604.2191497168933
        },
        {
          "variable": "dNO2_dt",
          "time": 0.0,
          "expected": -50.88837961561962
        },
        {
          "variable": "dOH_dt",
          "time": 0.0,
          "expected": 168.43551806733032
        },
        {
          "variable": "dO3_dt",
          "time": 0.0,
          "expected": 244576.91497547645
        },
        {
          "variable": "dHO2_dt",
          "time": 0.0,
          "expected": -1912.669465025445
        },
        {
          "variable": "dC2O3_dt",
          "time": 0.0,
          "expected": 303.41413852034987
        }
      ]
    },
    {
      "id": "scm_surface_night_tendencies",
      "description": "Surface at midnight, step 1080 level 1 (T = 304.77 K, M = 2.3673e19 molec/cm3). Every photolysis frequency is exactly zero, so the twenty photolysis reactions contribute nothing and the NO3/N2O5 night chemistry carries the whole budget -- a completely different set of stoichiometric columns from the daylight regimes.\n\nReference: Vdot from cbmz_mosaic_Fun, the KPP-generated right-hand side, evaluated on the dumped var_in with the dumped RCONST by the real64 replay driver kernels/cbmz_driver (a standalone program that calls WRF's KPP-generated cbmz_mosaic routines on the dumped inputs; WRF's KPP is already real64, so this is an independent replay of the same arithmetic rather than a precision upgrade). This is the INSTANTANEOUS rate, which WRF never writes: over its 60 s step the finite increment (var_out - var_in)/60 reaches only 2.7e5 to 8.0e6 molec/cm3/s where Fun reaches 1.1e6 to 3.6e7, a factor of 4 to 35, so a tendency test referenced against differenced states would be testing something else entirely.\n\nShape: each d<SPC>_dt is an observed written D(CBMZ.<SPC>, t), which esm-spec 7.4 resolves to the tendency the reaction system already derives, so asserting it at time 0 evaluates the mechanism's right-hand side at the given state. The time_span is empty ({start: 0, end: 0}), the shape esm-spec 6.6.2 names for a document with ODE states all of whose assertions sit at t0: the runner answers from the initial state without integrating. This adds no physics -- it is the derivative-test surface of the mechanism, and it pins the whole stoichiometric matrix and every rate law at once, independently of any integrator. The peroxy coefficients are live here as everywhere in this document, but at t = 0 that is no different from WRF: the operator split WRF makes -- it computes the ten state-dependent peroxy coefficients once, before INTEGRATE, and holds them at the step's input state for the whole 60 s step -- opens up only as the step proceeds.\n\nHCl and NH3 are absent from the 64: they are reservoir species of this mechanism (see their declarations), so no D(CBMZ.X, t) exists for them. What such an assertion would say -- that the CBM-Z gas phase produces and destroys neither -- is structural in this document rather than numerical.\n\nMeasured: 46 of the 64 assertions are BIT-IDENTICAL to KPP and the largest residual is 1.0e-13 (dXPAR_dt)\n\nState: data/eqwefic/dumps/chem170_wrf/esm_dump_cbmz_kpp_1080.json level k = 1; reference chem170_scm/replay/kp_1080.out.json (variable vdot). The run is described in data/eqwefic/notes/chem170_scm_reference_run.md.",
      "time_span": {
        "start": 0,
        "end": 0
      },
      "tolerance": {
        "rel": 1e-09
      },
      "initial_conditions": {
        "CBMZ.H2SO4": 936988.0799003674,
        "CBMZ.HCOOH": 585342859.4948878,
        "CBMZ.RCOOH": 1757656971.4712565,
        "CBMZ.ARO1": 0.025202729835157964,
        "CBMZ.ARO2": 0.06560453268211414,
        "CBMZ.ALK1": 78632340.77567872,
        "CBMZ.OLE1": 26879965.405289248,
        "CBMZ.API1": 0.058518816509900214,
        "CBMZ.API2": 0.4873120499890077,
        "CBMZ.LIM1": 0.3341692526559263,
        "CBMZ.LIM2": 0.48730880159438505,
        "CBMZ.SO2": 1150714307.501945,
        "CBMZ.O1D": 0.0,
        "CBMZ.ANOL": 0.002367300948723647,
        "CBMZ.H2O2": 30032058791.35429,
        "CBMZ.PAN": 6080373.379778968,
        "CBMZ.TOL": 0.1304813648133024,
        "CBMZ.N2O5": 196418.49869104094,
        "CBMZ.XYL": 0.02161075983220233,
        "CBMZ.CH4": 39994399673368.41,
        "CBMZ.CRO": 0.002367300948723647,
        "CBMZ.API": 0.002367300948723647,
        "CBMZ.LIM": 0.002367300948723647,
        "CBMZ.HNO4": 11037.363994896636,
        "CBMZ.TO2": 0.0024177688698090835,
        "CBMZ.C2H6": 14792375630.277622,
        "CBMZ.XPAR": 1273.7479049599551,
        "CBMZ.ETHOOH": 6282662582.688564,
        "CBMZ.HONO": 331383.130666366,
        "CBMZ.CH3OOH": 30501193057.848385,
        "CBMZ.C2H4": 1856940543.1426015,
        "CBMZ.CH3OH": 2515566082.104675,
        "CBMZ.CRES": 0.002367300948723647,
        "CBMZ.O3P": 0.0,
        "CBMZ.HNO3": 790499706.5482893,
        "CBMZ.CO": 1873317203564.4214,
        "CBMZ.ISOPN": 0.002367300948723647,
        "CBMZ.PAR": 76795462459.57317,
        "CBMZ.OPEN": 0.014843913946484943,
        "CBMZ.ISOPP": 0.002367300948723647,
        "CBMZ.ISOPO2": 0.002367300948723647,
        "CBMZ.OLET": 104183499.00741659,
        "CBMZ.ISOP": 0.002367300948723647,
        "CBMZ.HCHO": 11670244356.51484,
        "CBMZ.XO2": 678757.3918590436,
        "CBMZ.AONE": 2716069762.6113443,
        "CBMZ.OLEI": 109.05196656246814,
        "CBMZ.MGLY": 28235871.374624837,
        "CBMZ.ETHP": 1785325.769123058,
        "CBMZ.NAP": 178738.73963360942,
        "CBMZ.ALD2": 4864737753.296712,
        "CBMZ.CH3O2": 37738016.07647786,
        "CBMZ.ISOPRD": 0.034952089494294035,
        "CBMZ.ROOH": 1256989427.6944225,
        "CBMZ.ANO2": 17318.429725484893,
        "CBMZ.RO2": 424510.262457848,
        "CBMZ.ONIT": 51130332.99581393,
        "CBMZ.NO3": 45822946.77761542,
        "CBMZ.NO": 1047.1971011966268,
        "CBMZ.NO2": 339613853.6423892,
        "CBMZ.OH": 3792.47566260538,
        "CBMZ.O3": 450435434307.3917,
        "CBMZ.HO2": 4580499.170600212,
        "CBMZ.C2O3": 2217212.1541062975
      },
      "parameter_overrides": {
        "CBMZ.H2O": 5.904958807930307e+17,
        "CBMZ.M": 2.36730087135521e+19,
        "CBMZRateConstants.T": 304.7676696777344,
        "CBMZRateConstants.j_o31d": 0.0,
        "CBMZRateConstants.j_o33p": 0.0,
        "CBMZRateConstants.j_no2": 0.0,
        "CBMZRateConstants.j_no3o": 0.0,
        "CBMZRateConstants.j_hno2": 0.0,
        "CBMZRateConstants.j_hno3": 0.0,
        "CBMZRateConstants.j_hno4": 0.0,
        "CBMZRateConstants.j_h2o2": 0.0,
        "CBMZRateConstants.j_ch2or": 0.0,
        "CBMZRateConstants.j_ch2om": 0.0,
        "CBMZRateConstants.j_n2o5": 0.0,
        "CBMZ.HCl": 3848321169.919787,
        "CBMZ.NH3": 24882152.505644355
      },
      "assertions": [
        {
          "variable": "dH2SO4_dt",
          "time": 0.0,
          "expected": 3.7424967732952705
        },
        {
          "variable": "dHCOOH_dt",
          "time": 0.0,
          "expected": 1051.0135546706592
        },
        {
          "variable": "dRCOOH_dt",
          "time": 0.0,
          "expected": 96.93901163586735
        },
        {
          "variable": "dARO1_dt",
          "time": 0.0,
          "expected": 9.328345316968249e-08
        },
        {
          "variable": "dARO2_dt",
          "time": 0.0,
          "expected": 2.583234101484223e-07
        },
        {
          "variable": "dALK1_dt",
          "time": 0.0,
          "expected": 2.8309006701063177
        },
        {
          "variable": "dOLE1_dt",
          "time": 0.0,
          "expected": 4.811851443810821
        },
        {
          "variable": "dAPI1_dt",
          "time": 0.0,
          "expected": 0.00013934986667463062
        },
        {
          "variable": "dAPI2_dt",
          "time": 0.0,
          "expected": 0.001203476112573255
        },
        {
          "variable": "dLIM1_dt",
          "time": 0.0,
          "expected": 0.0016911775370971225
        },
        {
          "variable": "dLIM2_dt",
          "time": 0.0,
          "expected": 0.002471721078355868
        },
        {
          "variable": "dSO2_dt",
          "time": 0.0,
          "expected": -3.7424967732952705
        },
        {
          "variable": "dO1D_dt",
          "time": 0.0,
          "expected": 0.0
        },
        {
          "variable": "dANOL_dt",
          "time": 0.0,
          "expected": -2.906691151349243e-11
        },
        {
          "variable": "dH2O2_dt",
          "time": 0.0,
          "expected": -74.03705771689334
        },
        {
          "variable": "dPAN_dt",
          "time": 0.0,
          "expected": 21.657553123530306
        },
        {
          "variable": "dTOL_dt",
          "time": 0.0,
          "expected": -2.9891050051968833e-09
        },
        {
          "variable": "dN2O5_dt",
          "time": 0.0,
          "expected": 18.56931465433445
        },
        {
          "variable": "dXYL_dt",
          "time": 0.0,
          "expected": -2.0386467120411825e-09
        },
        {
          "variable": "dCH4_dt",
          "time": 0.0,
          "expected": -1065.5660999600193
        },
        {
          "variable": "dCRO_dt",
          "time": 0.0,
          "expected": -8.868920014548903e-06
        },
        {
          "variable": "dAPI_dt",
          "time": 0.0,
          "expected": -0.006334085223736605
        },
        {
          "variable": "dLIM_dt",
          "time": 0.0,
          "expected": -0.013009059574812146
        },
        {
          "variable": "dHNO4_dt",
          "time": 0.0,
          "expected": 1.4426432882471545
        },
        {
          "variable": "dTO2_dt",
          "time": 0.0,
          "expected": 3.2881668034365815e-09
        },
        {
          "variable": "dC2H6_dt",
          "time": 0.0,
          "expected": -3.7354685633044173
        },
        {
          "variable": "dXPAR_dt",
          "time": 0.0,
          "expected": -0.58548853177947
        },
        {
          "variable": "dETHOOH_dt",
          "time": 0.0,
          "expected": -113.54136966220688
        },
        {
          "variable": "dHONO_dt",
          "time": 0.0,
          "expected": 0.7715364988922653
        },
        {
          "variable": "dCH3OOH_dt",
          "time": 0.0,
          "expected": 59.45434602561693
        },
        {
          "variable": "dC2H4_dt",
          "time": 0.0,
          "expected": -1851.4637734989722
        },
        {
          "variable": "dCH3OH_dt",
          "time": 0.0,
          "expected": 421.8155748570832
        },
        {
          "variable": "dCRES_dt",
          "time": 0.0,
          "expected": -2.386394988610039e-06
        },
        {
          "variable": "dO3P_dt",
          "time": 0.0,
          "expected": 0.0
        },
        {
          "variable": "dHNO3_dt",
          "time": 0.0,
          "expected": 1666.6228159572897
        },
        {
          "variable": "dCO_dt",
          "time": 0.0,
          "expected": -294.94212524230437
        },
        {
          "variable": "dISOPN_dt",
          "time": 0.0,
          "expected": -2.0596736542953216e-07
        },
        {
          "variable": "dPAR_dt",
          "time": 0.0,
          "expected": -1214.0889807402586
        },
        {
          "variable": "dOPEN_dt",
          "time": 0.0,
          "expected": -7.155504183512505e-08
        },
        {
          "variable": "dISOPP_dt",
          "time": 0.0,
          "expected": -2.8039352462320725e-07
        },
        {
          "variable": "dISOPO2_dt",
          "time": 0.0,
          "expected": -2.7909962278011095e-07
        },
        {
          "variable": "dOLET_dt",
          "time": 0.0,
          "expected": -601.4568018332807
        },
        {
          "variable": "dISOP_dt",
          "time": 0.0,
          "expected": -9.353229905535735e-08
        },
        {
          "variable": "dHCHO_dt",
          "time": 0.0,
          "expected": 4393.647134851897
        },
        {
          "variable": "dXO2_dt",
          "time": 0.0,
          "expected": -21.08136412614555
        },
        {
          "variable": "dAONE_dt",
          "time": 0.0,
          "expected": 146.25270503719887
        },
        {
          "variable": "dOLEI_dt",
          "time": 0.0,
          "expected": -0.02460007423842763
        },
        {
          "variable": "dMGLY_dt",
          "time": 0.0,
          "expected": 22.908927131310406
        },
        {
          "variable": "dETHP_dt",
          "time": 0.0,
          "expected": -111.16625774036802
        },
        {
          "variable": "dNAP_dt",
          "time": 0.0,
          "expected": 4.3117854284794355
        },
        {
          "variable": "dALD2_dt",
          "time": 0.0,
          "expected": -226.54537469653607
        },
        {
          "variable": "dCH3O2_dt",
          "time": 0.0,
          "expected": -1495.629454827325
        },
        {
          "variable": "dISOPRD_dt",
          "time": 0.0,
          "expected": 4.5108576359719455e-08
        },
        {
          "variable": "dROOH_dt",
          "time": 0.0,
          "expected": -10.702248566897078
        },
        {
          "variable": "dANO2_dt",
          "time": 0.0,
          "expected": -0.4528766724503156
        },
        {
          "variable": "dRO2_dt",
          "time": 0.0,
          "expected": 9.41473456392751
        },
        {
          "variable": "dONIT_dt",
          "time": 0.0,
          "expected": 29.454986983911688
        },
        {
          "variable": "dNO3_dt",
          "time": 0.0,
          "expected": 1221.653263412373
        },
        {
          "variable": "dNO_dt",
          "time": 0.0,
          "expected": 0.017133380916107034
        },
        {
          "variable": "dNO2_dt",
          "time": 0.0,
          "expected": -2983.070347176424
        },
        {
          "variable": "dOH_dt",
          "time": 0.0,
          "expected": -0.05521255033223675
        },
        {
          "variable": "dO3_dt",
          "time": 0.0,
          "expected": -12739.670033807633
        },
        {
          "variable": "dHO2_dt",
          "time": 0.0,
          "expected": -21.23632205652322
        },
        {
          "variable": "dC2O3_dt",
          "time": 0.0,
          "expected": -8.436533399358641
        }
      ]
    },
    {
      "id": "rich_surface_terpenes_tendencies",
      "description": "The rich column's first chemistry call (step 1, 06 LST, surface). API 1.2e10 and LIM 4.7e9 molec/cm3, so reactions {137:117}..{142:122} carry flux here and nowhere else in either column -- alpha-pinene's lifetime against ozone at 30 ppb is under a quarter of a second, and limonene's under an eighth, so dAPI_dt and dLIM_dt are among the largest tendencies in the whole test suite. Those sub-second ozonolysis lifetimes are a WRF bug carried here unchanged: cbmz_mosaic.eqn swaps the NO3 and O3 rate expressions of both terpenes (see k_R138, k_R139, k_R141 and k_R142 in cbmz_rate_constants.esm); with the rates on their correct rows the ozone lifetimes would be about 4 h (API) and 2 h (LIM). The aromatic and isoprene primaries are at their initial values too.\n\nWhich column this is. The reference is the RICH chem_opt = 170 column, dumps/chem170_rich -- a SECOND reference run, not a recapture of the first. Same sounding, location, dates, namelist and binary as the six idealized regimes; the only difference is ESM_RICH_IC=1, which raises seven initial mixing ratios that WRF-Chem's idealized gas profile leaves at its 1e-11 to 1e-13 ppb floor: TOL 0.50, XYL 0.30, CSL 0.01, ISO 2.00, API 0.50, LIM 0.20 and C2H5OH 1.00 ppb (chem/chemics_init.F, CBMZ_MOSAIC_KPP case, WRF fork branch earthsciml-instrumented-chem170). dumps/chem170_wrf is untouched. Without it the aromatic, isoprene and terpene columns of the stoichiometric matrix are multiplied by concentrations of 1e-3 molec/cm3 and the test cannot tell a right coefficient from a wrong one; here those reactions carry flux. The two columns are not the same run at different times -- their meteorology diverges as well, because WRF-Chem's Dudhia shortwave adds the chemistry's PM2.5 dry and water mass to its layer scattering whatever aer_ra_feedback says (phys/module_ra_sw.F, the PRESENT(pm2_5_dry) branch, refilled every step by sum_pm_driver in chem/chem_driver.F).\n\nNothing else changes: same Fun reference from kernels/cbmz_driver, same t = 0 evaluation on an empty time_span, same rel 1e-9. WRF's frozen peroxy coefficients do not enter at t = 0.\n\nMeasured: 58 of the 64 assertions are BIT-IDENTICAL to KPP and the largest residual is 3.0e-16 (dH2O2_dt)\n\nState: data/eqwefic/dumps/chem170_rich/esm_dump_cbmz_kpp_1.json level k = 1; reference chem170_rich/replay/kp_1.out.json (variable vdot); run script data/eqwefic/chem170_rich/run.sh.",
      "time_span": {
        "start": 0,
        "end": 0
      },
      "tolerance": {
        "rel": 1e-09
      },
      "initial_conditions": {
        "CBMZ.H2SO4": 1178234084.113183,
        "CBMZ.HCOOH": 1178233912.6575658,
        "CBMZ.RCOOH": 1413880712.3346407,
        "CBMZ.ARO1": 0.0023564680960358074,
        "CBMZ.ARO2": 0.0023564680960358074,
        "CBMZ.ALK1": 0.0023564680960358074,
        "CBMZ.OLE1": 0.0023564680960358074,
        "CBMZ.API1": 0.0023564680960358074,
        "CBMZ.API2": 0.0023564680960358074,
        "CBMZ.LIM1": 0.0023564680960358074,
        "CBMZ.LIM2": 0.0023564680960358074,
        "CBMZ.SO2": 2356468168.226366,
        "CBMZ.O1D": 0.0,
        "CBMZ.ANOL": 23564681682.263657,
        "CBMZ.H2O2": 32519259898.53689,
        "CBMZ.PAN": 275706740.19117206,
        "CBMZ.TOL": 11782340841.131828,
        "CBMZ.N2O5": 291761.36864263384,
        "CBMZ.XYL": 7069404504.679097,
        "CBMZ.CH4": 40059958080753.9,
        "CBMZ.CRO": 0.0023564680960358074,
        "CBMZ.API": 11782340841.131828,
        "CBMZ.LIM": 4712935650.630263,
        "CBMZ.HNO4": 3795479.8402734455,
        "CBMZ.TO2": 0.0023564680960358074,
        "CBMZ.C2H6": 15081396550.977728,
        "CBMZ.XPAR": 0.0023564680960358074,
        "CBMZ.ETHOOH": 18144802289.21764,
        "CBMZ.HONO": 0.23564680149480602,
        "CBMZ.CH3OOH": 36289604578.43528,
        "CBMZ.C2H4": 4359465836.88979,
        "CBMZ.CH3OH": 0.0023564680960358074,
        "CBMZ.CRES": 235646799.67707488,
        "CBMZ.O3P": 0.0,
        "CBMZ.HNO3": 1649527683.4673326,
        "CBMZ.CO": 1885174402903.1787,
        "CBMZ.ISOPN": 0.0023564680960358074,
        "CBMZ.PAR": 94209940061.98004,
        "CBMZ.OPEN": 0.0023564680960358074,
        "CBMZ.ISOPP": 0.0023564680960358074,
        "CBMZ.ISOPO2": 0.0023564680960358074,
        "CBMZ.OLET": 2299912847.146947,
        "CBMZ.ISOP": 47129363364.52731,
        "CBMZ.HCHO": 12041551557.799116,
        "CBMZ.XO2": 0.0023564680960358074,
        "CBMZ.AONE": 299271450.16361254,
        "CBMZ.OLEI": 1149956423.5734735,
        "CBMZ.MGLY": 0.23564680149480602,
        "CBMZ.ETHP": 0.0023564680960358074,
        "CBMZ.NAP": 0.0023564680960358074,
        "CBMZ.ALD2": 704583913.0316142,
        "CBMZ.CH3O2": 0.0023564680960358074,
        "CBMZ.ISOPRD": 0.0023564680960358074,
        "CBMZ.ROOH": 0.0023564680960358074,
        "CBMZ.ANO2": 0.0023564680960358074,
        "CBMZ.RO2": 0.0023564680960358074,
        "CBMZ.ONIT": 0.23564680149480602,
        "CBMZ.NO3": 2625852.3177837045,
        "CBMZ.NO": 127249279.5411232,
        "CBMZ.NO2": 381747817.19141746,
        "CBMZ.OH": 1308192.6276228107,
        "CBMZ.O3": 706940401088.692,
        "CBMZ.HO2": 1084422829.1115165,
        "CBMZ.C2O3": 0.0023564680960358074
      },
      "parameter_overrides": {
        "CBMZ.H2O": 5.357267327123456e+17,
        "CBMZ.M": 2.35646804299371e+19,
        "CBMZRateConstants.T": 306.1650695800781,
        "CBMZRateConstants.j_o31d": 1.0315505249991475e-07,
        "CBMZRateConstants.j_o33p": 9.906222658173647e-06,
        "CBMZRateConstants.j_no2": 0.000210850645089522,
        "CBMZRateConstants.j_no3o": 0.004483486991375685,
        "CBMZRateConstants.j_hno2": 4.64483855466824e-05,
        "CBMZRateConstants.j_hno3": 4.801096853412901e-09,
        "CBMZRateConstants.j_hno4": 2.8821148134738905e-08,
        "CBMZRateConstants.j_h2o2": 1.1240952346724953e-07,
        "CBMZRateConstants.j_ch2or": 3.2001688055061095e-07,
        "CBMZRateConstants.j_ch2om": 8.588341415816103e-07,
        "CBMZRateConstants.j_n2o5": 0.0,
        "CBMZ.HCl": 9425872672.905464,
        "CBMZ.NH3": 117823410.5545135
      },
      "assertions": [
        {
          "variable": "dH2SO4_dt",
          "time": 0.0,
          "expected": 2626.740569556716
        },
        {
          "variable": "dHCOOH_dt",
          "time": 0.0,
          "expected": 7777.756193090514
        },
        {
          "variable": "dRCOOH_dt",
          "time": 0.0,
          "expected": 251406.83289066455
        },
        {
          "variable": "dARO1_dt",
          "time": 0.0,
          "expected": 13593.456591489079
        },
        {
          "variable": "dARO2_dt",
          "time": 0.0,
          "expected": 37643.41845311599
        },
        {
          "variable": "dALK1_dt",
          "time": 0.0,
          "expected": 1197.938971060986
        },
        {
          "variable": "dOLE1_dt",
          "time": 0.0,
          "expected": 3290.4116598870232
        },
        {
          "variable": "dAPI1_dt",
          "time": 0.0,
          "expected": 1080562764.9753554
        },
        {
          "variable": "dAPI2_dt",
          "time": 0.0,
          "expected": 9332132686.821825
        },
        {
          "variable": "dLIM1_dt",
          "time": 0.0,
          "expected": 5284217500.829411
        },
        {
          "variable": "dLIM2_dt",
          "time": 0.0,
          "expected": 7723089330.442902
        },
        {
          "variable": "dSO2_dt",
          "time": 0.0,
          "expected": -2626.740569556716
        },
        {
          "variable": "dO1D_dt",
          "time": 0.0,
          "expected": 72924.47418861481
        },
        {
          "variable": "dANOL_dt",
          "time": 0.0,
          "expected": -100157.69670106223
        },
        {
          "variable": "dH2O2_dt",
          "time": 0.0,
          "expected": 6201554.933787202
        },
        {
          "variable": "dPAN_dt",
          "time": 0.0,
          "expected": -348560.87235065264
        },
        {
          "variable": "dTOL_dt",
          "time": 0.0,
          "expected": -92657.13554490037
        },
        {
          "variable": "dN2O5_dt",
          "time": 0.0,
          "expected": -32106.600565909124
        },
        {
          "variable": "dXYL_dt",
          "time": 0.0,
          "expected": -229640.87733531505
        },
        {
          "variable": "dCH4_dt",
          "time": 0.0,
          "expected": -372294.19232623046
        },
        {
          "variable": "dCRO_dt",
          "time": 0.0,
          "expected": 18668.67241456043
        },
        {
          "variable": "dAPI_dt",
          "time": 0.0,
          "expected": -49117053488.01987
        },
        {
          "variable": "dLIM_dt",
          "time": 0.0,
          "expected": -40648582644.38051
        },
        {
          "variable": "dHNO4_dt",
          "time": 0.0,
          "expected": -275152.0667873204
        },
        {
          "variable": "dTO2_dt",
          "time": 0.0,
          "expected": 177464.10160140975
        },
        {
          "variable": "dC2H6_dt",
          "time": 0.0,
          "expected": -3359.829303448886
        },
        {
          "variable": "dXPAR_dt",
          "time": 0.0,
          "expected": 781626.5132863278
        },
        {
          "variable": "dETHOOH_dt",
          "time": 0.0,
          "expected": -174771.06871450343
        },
        {
          "variable": "dHONO_dt",
          "time": 0.0,
          "expected": 1361.6430043569758
        },
        {
          "variable": "dCH3OOH_dt",
          "time": 0.0,
          "expected": -349542.13745347597
        },
        {
          "variable": "dC2H4_dt",
          "time": 0.0,
          "expected": -53285.18404614276
        },
        {
          "variable": "dCH3OH_dt",
          "time": 0.0,
          "expected": 8616.851235628379
        },
        {
          "variable": "dCRES_dt",
          "time": 0.0,
          "expected": -3651.2488861829315
        },
        {
          "variable": "dO3P_dt",
          "time": 0.0,
          "expected": 7094078.740081251
        },
        {
          "variable": "dHNO3_dt",
          "time": 0.0,
          "expected": 20997.8011803782
        },
        {
          "variable": "dCO_dt",
          "time": 0.0,
          "expected": -309488.52950273355
        },
        {
          "variable": "dISOPN_dt",
          "time": 0.0,
          "expected": 86503.38448983255
        },
        {
          "variable": "dPAR_dt",
          "time": 0.0,
          "expected": 152776.72166601723
        },
        {
          "variable": "dOPEN_dt",
          "time": 0.0,
          "expected": 3791.7384474043292
        },
        {
          "variable": "dISOPP_dt",
          "time": 0.0,
          "expected": 6096803.871875469
        },
        {
          "variable": "dISOPO2_dt",
          "time": 0.0,
          "expected": -3.148442957401364e-05
        },
        {
          "variable": "dOLET_dt",
          "time": 0.0,
          "expected": -102317.97963760888
        },
        {
          "variable": "dISOP_dt",
          "time": 0.0,
          "expected": -6741031.498269933
        },
        {
          "variable": "dHCHO_dt",
          "time": 0.0,
          "expected": 443062.2841161416
        },
        {
          "variable": "dXO2_dt",
          "time": 0.0,
          "expected": 959001.4553350274
        },
        {
          "variable": "dAONE_dt",
          "time": 0.0,
          "expected": 37057.8998687383
        },
        {
          "variable": "dOLEI_dt",
          "time": 0.0,
          "expected": -308983.45831249905
        },
        {
          "variable": "dMGLY_dt",
          "time": 0.0,
          "expected": 198553.43692443427
        },
        {
          "variable": "dETHP_dt",
          "time": 0.0,
          "expected": 138102.9401959635
        },
        {
          "variable": "dNAP_dt",
          "time": 0.0,
          "expected": 7618.1683680559545
        },
        {
          "variable": "dALD2_dt",
          "time": 0.0,
          "expected": 711769.3137246051
        },
        {
          "variable": "dCH3O2_dt",
          "time": 0.0,
          "expected": 653728.4175271279
        },
        {
          "variable": "dISOPRD_dt",
          "time": 0.0,
          "expected": 362520.7439010509
        },
        {
          "variable": "dROOH_dt",
          "time": 0.0,
          "expected": 0.00011239842657077862
        },
        {
          "variable": "dANO2_dt",
          "time": 0.0,
          "expected": 22212.303775939985
        },
        {
          "variable": "dRO2_dt",
          "time": 0.0,
          "expected": 118499.88995482707
        },
        {
          "variable": "dONIT_dt",
          "time": 0.0,
          "expected": 7.440836572350641e-05
        },
        {
          "variable": "dNO3_dt",
          "time": 0.0,
          "expected": -95390.71471961704
        },
        {
          "variable": "dNO_dt",
          "time": 0.0,
          "expected": -2879451.5707543143
        },
        {
          "variable": "dNO2_dt",
          "time": 0.0,
          "expected": 3546282.0925872517
        },
        {
          "variable": "dOH_dt",
          "time": 0.0,
          "expected": -7638957.537055225
        },
        {
          "variable": "dO3_dt",
          "time": 0.0,
          "expected": -89775232592.71121
        },
        {
          "variable": "dHO2_dt",
          "time": 0.0,
          "expected": -13568046.912437672
        },
        {
          "variable": "dC2O3_dt",
          "time": 0.0,
          "expected": 513274.87120718847
        }
      ]
    },
    {
      "id": "rich_surface_noon_tendencies",
      "description": "The rich column's surface layer at local noon (step 364), six hours into the aromatic and isoprene chemistry. Every product and radical of those chains carries a real burden, so the tendencies of ARO1, ARO2, API1, API2, LIM1, LIM2, ISOPRD, ISOPP, ISOPN, ISOPO2, TO2, CRO and OPEN are differences of real production and real loss instead of zero minus zero.\n\nWhich column this is. The reference is the RICH chem_opt = 170 column, dumps/chem170_rich -- a SECOND reference run, not a recapture of the first. Same sounding, location, dates, namelist and binary as the six idealized regimes; the only difference is ESM_RICH_IC=1, which raises seven initial mixing ratios that WRF-Chem's idealized gas profile leaves at its 1e-11 to 1e-13 ppb floor: TOL 0.50, XYL 0.30, CSL 0.01, ISO 2.00, API 0.50, LIM 0.20 and C2H5OH 1.00 ppb (chem/chemics_init.F, CBMZ_MOSAIC_KPP case, WRF fork branch earthsciml-instrumented-chem170). dumps/chem170_wrf is untouched. Without it the aromatic, isoprene and terpene columns of the stoichiometric matrix are multiplied by concentrations of 1e-3 molec/cm3 and the test cannot tell a right coefficient from a wrong one; here those reactions carry flux. The two columns are not the same run at different times -- their meteorology diverges as well, because WRF-Chem's Dudhia shortwave adds the chemistry's PM2.5 dry and water mass to its layer scattering whatever aer_ra_feedback says (phys/module_ra_sw.F, the PRESENT(pm2_5_dry) branch, refilled every step by sum_pm_driver in chem/chem_driver.F).\n\nNothing else changes: same Fun reference from kernels/cbmz_driver, same t = 0 evaluation on an empty time_span, same rel 1e-9. WRF's frozen peroxy coefficients do not enter at t = 0.\n\nMeasured: 41 of the 64 assertions are BIT-IDENTICAL to KPP and the largest residual is 1.5e-14 (dCH3O2_dt)\n\nState: data/eqwefic/dumps/chem170_rich/esm_dump_cbmz_kpp_364.json level k = 1; reference chem170_rich/replay/kp_364.out.json (variable vdot); run script data/eqwefic/chem170_rich/run.sh.",
      "time_span": {
        "start": 0,
        "end": 0
      },
      "tolerance": {
        "rel": 1e-09
      },
      "initial_conditions": {
        "CBMZ.H2SO4": 139733817.99135187,
        "CBMZ.HCOOH": 951027927.0500613,
        "CBMZ.RCOOH": 4484118207.435507,
        "CBMZ.ARO1": 136608387.8453574,
        "CBMZ.ARO2": 378300137.89077175,
        "CBMZ.ALK1": 13715407.988296159,
        "CBMZ.OLE1": 17108511.603515647,
        "CBMZ.API1": 256786826.1579364,
        "CBMZ.API2": 2217699659.5688715,
        "CBMZ.LIM1": 606946935.5267426,
        "CBMZ.LIM2": 887076551.697291,
        "CBMZ.SO2": 1826343953.4665484,
        "CBMZ.O1D": 0.015210925236693306,
        "CBMZ.ANOL": 20919221754.6005,
        "CBMZ.H2O2": 28273371149.376915,
        "CBMZ.PAN": 105924993.60697371,
        "CBMZ.TOL": 10583228410.863705,
        "CBMZ.N2O5": 38.85817729873145,
        "CBMZ.XYL": 4723816564.624308,
        "CBMZ.CH4": 39623304533288.69,
        "CBMZ.CRO": 3228854.5980307264,
        "CBMZ.API": 0.0023344397650064464,
        "CBMZ.LIM": 0.0023344397650064464,
        "CBMZ.HNO4": 183080.89031049405,
        "CBMZ.TO2": 472571602.88638705,
        "CBMZ.C2H6": 14938768702.579609,
        "CBMZ.XPAR": 542750.7969326712,
        "CBMZ.ETHOOH": 13113515204.305584,
        "CBMZ.HONO": 326767.6586339333,
        "CBMZ.CH3OOH": 32810441996.84365,
        "CBMZ.C2H4": 3695001644.871035,
        "CBMZ.CH3OH": 2258043614.194084,
        "CBMZ.CRES": 256904534.17170885,
        "CBMZ.O3P": 3060.546309084236,
        "CBMZ.HNO3": 1179840331.1989155,
        "CBMZ.CO": 1874537485590.7734,
        "CBMZ.ISOPN": 30551.44133176359,
        "CBMZ.PAR": 88032054992.70636,
        "CBMZ.OPEN": 496734654.6962726,
        "CBMZ.ISOPP": 265614587.48520228,
        "CBMZ.ISOPO2": 68743231.6504553,
        "CBMZ.OLET": 1262295304.405014,
        "CBMZ.ISOP": 7823777532.9807415,
        "CBMZ.HCHO": 15226920637.939892,
        "CBMZ.XO2": 120942818.52755655,
        "CBMZ.AONE": 2385409629.9450493,
        "CBMZ.OLEI": 14536763.213186832,
        "CBMZ.MGLY": 940772043.0968233,
        "CBMZ.ETHP": 50963811.9695222,
        "CBMZ.NAP": 420403.88497895753,
        "CBMZ.ALD2": 6847657076.951434,
        "CBMZ.CH3O2": 469398157.46745855,
        "CBMZ.ISOPRD": 12961187106.551676,
        "CBMZ.ROOH": 15044894111.914577,
        "CBMZ.ANO2": 256349.4770061826,
        "CBMZ.RO2": 17818244.32319223,
        "CBMZ.ONIT": 415809758.27959067,
        "CBMZ.NO3": 28657.080473191934,
        "CBMZ.NO": 37007981.27601202,
        "CBMZ.NO2": 168070058.38367787,
        "CBMZ.OH": 1478238.169004505,
        "CBMZ.O3": 579523997812.9054,
        "CBMZ.HO2": 235633481.63526702,
        "CBMZ.C2O3": 96418234.96108417
      },
      "parameter_overrides": {
        "CBMZ.H2O": 5.7413411697957274e+17,
        "CBMZ.M": 2.3344395474335433e+19,
        "CBMZRateConstants.T": 309.1135559082031,
        "CBMZRateConstants.j_o31d": 2.0807125110877678e-05,
        "CBMZRateConstants.j_o33p": 0.00031756257521919906,
        "CBMZRateConstants.j_no2": 0.005552865099161863,
        "CBMZRateConstants.j_no3o": 0.13754792511463165,
        "CBMZRateConstants.j_hno2": 0.001212133327499032,
        "CBMZRateConstants.j_hno3": 3.8843518268549815e-07,
        "CBMZRateConstants.j_hno4": 2.5732028916536365e-06,
        "CBMZRateConstants.j_h2o2": 4.612214979715645e-06,
        "CBMZRateConstants.j_ch2or": 1.740917650749907e-05,
        "CBMZRateConstants.j_ch2om": 2.7758238502428867e-05,
        "CBMZRateConstants.j_n2o5": 0.0,
        "CBMZ.HCl": 6852189429.966592,
        "CBMZ.NH3": 14321837.010685463
      },
      "assertions": [
        {
          "variable": "dH2SO4_dt",
          "time": 0.0,
          "expected": 2269.403255930855
        },
        {
          "variable": "dHCOOH_dt",
          "time": 0.0,
          "expected": 4696.227580214368
        },
        {
          "variable": "dRCOOH_dt",
          "time": 0.0,
          "expected": 160763.18173925343
        },
        {
          "variable": "dARO1_dt",
          "time": 0.0,
          "expected": 10982.66880060894
        },
        {
          "variable": "dARO2_dt",
          "time": 0.0,
          "expected": 30413.54453231205
        },
        {
          "variable": "dALK1_dt",
          "time": 0.0,
          "expected": 1264.8863925959347
        },
        {
          "variable": "dOLE1_dt",
          "time": 0.0,
          "expected": 507.4205859159832
        },
        {
          "variable": "dAPI1_dt",
          "time": 0.0,
          "expected": 0.0001728465068771256
        },
        {
          "variable": "dAPI2_dt",
          "time": 0.0,
          "expected": 0.0014927652281331242
        },
        {
          "variable": "dLIM1_dt",
          "time": 0.0,
          "expected": 0.0021456638451950853
        },
        {
          "variable": "dLIM2_dt",
          "time": 0.0,
          "expected": 0.0031359714457617973
        },
        {
          "variable": "dSO2_dt",
          "time": 0.0,
          "expected": -2269.403255930855
        },
        {
          "variable": "dO1D_dt",
          "time": 0.0,
          "expected": -63195.426515638595
        },
        {
          "variable": "dANOL_dt",
          "time": 0.0,
          "expected": -101209.34790530641
        },
        {
          "variable": "dH2O2_dt",
          "time": 0.0,
          "expected": 85945.32859003858
        },
        {
          "variable": "dPAN_dt",
          "time": 0.0,
          "expected": -71395.03907449995
        },
        {
          "variable": "dTOL_dt",
          "time": 0.0,
          "expected": -93106.79819958268
        },
        {
          "variable": "dN2O5_dt",
          "time": 0.0,
          "expected": -0.32490875661304486
        },
        {
          "variable": "dXYL_dt",
          "time": 0.0,
          "expected": -172767.71175117028
        },
        {
          "variable": "dCH4_dt",
          "time": 0.0,
          "expected": -459476.89310350426
        },
        {
          "variable": "dCRO_dt",
          "time": 0.0,
          "expected": -1207.3020458998035
        },
        {
          "variable": "dAPI_dt",
          "time": 0.0,
          "expected": -0.007856783960581547
        },
        {
          "variable": "dLIM_dt",
          "time": 0.0,
          "expected": -0.01650552925301866
        },
        {
          "variable": "dHNO4_dt",
          "time": 0.0,
          "expected": -3768.84780310098
        },
        {
          "variable": "dTO2_dt",
          "time": 0.0,
          "expected": 10570.647545386077
        },
        {
          "variable": "dC2H6_dt",
          "time": 0.0,
          "expected": -637.3223833091442
        },
        {
          "variable": "dXPAR_dt",
          "time": 0.0,
          "expected": -8811.735269918212
        },
        {
          "variable": "dETHOOH_dt",
          "time": 0.0,
          "expected": -96316.67181780313
        },
        {
          "variable": "dHONO_dt",
          "time": 0.0,
          "expected": -6.832735909920828
        },
        {
          "variable": "dCH3OOH_dt",
          "time": 0.0,
          "expected": 101236.98457822204
        },
        {
          "variable": "dC2H4_dt",
          "time": 0.0,
          "expected": -49613.79488012995
        },
        {
          "variable": "dCH3OH_dt",
          "time": 0.0,
          "expected": 210956.6674915897
        },
        {
          "variable": "dCRES_dt",
          "time": 0.0,
          "expected": 4078.8246881647833
        },
        {
          "variable": "dO3P_dt",
          "time": 0.0,
          "expected": -1002276.3130684027
        },
        {
          "variable": "dHNO3_dt",
          "time": 0.0,
          "expected": 1436.2986790592086
        },
        {
          "variable": "dCO_dt",
          "time": 0.0,
          "expected": 579324.2394470061
        },
        {
          "variable": "dISOPN_dt",
          "time": 0.0,
          "expected": 13.8701187653202
        },
        {
          "variable": "dPAR_dt",
          "time": 0.0,
          "expected": -385790.9284291231
        },
        {
          "variable": "dOPEN_dt",
          "time": 0.0,
          "expected": 35960.08405135695
        },
        {
          "variable": "dISOPP_dt",
          "time": 0.0,
          "expected": -76238.08024264453
        },
        {
          "variable": "dISOPO2_dt",
          "time": 0.0,
          "expected": -6498.14536937284
        },
        {
          "variable": "dOLET_dt",
          "time": 0.0,
          "expected": -59895.09177221823
        },
        {
          "variable": "dISOP_dt",
          "time": 0.0,
          "expected": -1210156.9401501757
        },
        {
          "variable": "dHCHO_dt",
          "time": 0.0,
          "expected": 86741.1823826769
        },
        {
          "variable": "dXO2_dt",
          "time": 0.0,
          "expected": -15627.048926935298
        },
        {
          "variable": "dAONE_dt",
          "time": 0.0,
          "expected": 217154.04966264934
        },
        {
          "variable": "dOLEI_dt",
          "time": 0.0,
          "expected": -3532.4784546317464
        },
        {
          "variable": "dMGLY_dt",
          "time": 0.0,
          "expected": 36717.54917246015
        },
        {
          "variable": "dETHP_dt",
          "time": 0.0,
          "expected": -9390.776603252736
        },
        {
          "variable": "dNAP_dt",
          "time": 0.0,
          "expected": 10.965518034405477
        },
        {
          "variable": "dALD2_dt",
          "time": 0.0,
          "expected": 285115.555689059
        },
        {
          "variable": "dCH3O2_dt",
          "time": 0.0,
          "expected": -7934.589674100338
        },
        {
          "variable": "dISOPRD_dt",
          "time": 0.0,
          "expected": -152932.9750182008
        },
        {
          "variable": "dROOH_dt",
          "time": 0.0,
          "expected": 736537.0226391036
        },
        {
          "variable": "dANO2_dt",
          "time": 0.0,
          "expected": 4.002955798012181
        },
        {
          "variable": "dRO2_dt",
          "time": 0.0,
          "expected": -5292.3532003874425
        },
        {
          "variable": "dONIT_dt",
          "time": 0.0,
          "expected": 18257.58402889388
        },
        {
          "variable": "dNO3_dt",
          "time": 0.0,
          "expected": 94.60316410348341
        },
        {
          "variable": "dNO_dt",
          "time": 0.0,
          "expected": -14978.912566852889
        },
        {
          "variable": "dNO2_dt",
          "time": 0.0,
          "expected": 70336.95994058193
        },
        {
          "variable": "dOH_dt",
          "time": 0.0,
          "expected": 2868.373077694631
        },
        {
          "variable": "dO3_dt",
          "time": 0.0,
          "expected": -798609.4056163704
        },
        {
          "variable": "dHO2_dt",
          "time": 0.0,
          "expected": 50801.49683551224
        },
        {
          "variable": "dC2O3_dt",
          "time": 0.0,
          "expected": 6756.813398313049
        }
      ]
    },
    {
      "id": "rich_surface_afternoon_tendencies",
      "description": "The rich column's surface layer in the late afternoon (step 601, 16 LST). Isoprene is 50 times below its noon value while its products are near their peak, so the same reactions are exercised with the flux distributed quite differently.\n\nWhich column this is. The reference is the RICH chem_opt = 170 column, dumps/chem170_rich -- a SECOND reference run, not a recapture of the first. Same sounding, location, dates, namelist and binary as the six idealized regimes; the only difference is ESM_RICH_IC=1, which raises seven initial mixing ratios that WRF-Chem's idealized gas profile leaves at its 1e-11 to 1e-13 ppb floor: TOL 0.50, XYL 0.30, CSL 0.01, ISO 2.00, API 0.50, LIM 0.20 and C2H5OH 1.00 ppb (chem/chemics_init.F, CBMZ_MOSAIC_KPP case, WRF fork branch earthsciml-instrumented-chem170). dumps/chem170_wrf is untouched. Without it the aromatic, isoprene and terpene columns of the stoichiometric matrix are multiplied by concentrations of 1e-3 molec/cm3 and the test cannot tell a right coefficient from a wrong one; here those reactions carry flux. The two columns are not the same run at different times -- their meteorology diverges as well, because WRF-Chem's Dudhia shortwave adds the chemistry's PM2.5 dry and water mass to its layer scattering whatever aer_ra_feedback says (phys/module_ra_sw.F, the PRESENT(pm2_5_dry) branch, refilled every step by sum_pm_driver in chem/chem_driver.F).\n\nNothing else changes: same Fun reference from kernels/cbmz_driver, same t = 0 evaluation on an empty time_span, same rel 1e-9. WRF's frozen peroxy coefficients do not enter at t = 0.\n\nMeasured: 48 of the 64 assertions are BIT-IDENTICAL to KPP and the largest residual is 5.9e-13 (dO3P_dt)\n\nState: data/eqwefic/dumps/chem170_rich/esm_dump_cbmz_kpp_601.json level k = 1; reference chem170_rich/replay/kp_601.out.json (variable vdot); run script data/eqwefic/chem170_rich/run.sh.",
      "time_span": {
        "start": 0,
        "end": 0
      },
      "tolerance": {
        "rel": 1e-09
      },
      "initial_conditions": {
        "CBMZ.H2SO4": 26103281.498322044,
        "CBMZ.HCOOH": 750327459.7871988,
        "CBMZ.RCOOH": 5268818671.027761,
        "CBMZ.ARO1": 271819745.45893085,
        "CBMZ.ARO2": 752731754.3340108,
        "CBMZ.ALK1": 31198763.190763317,
        "CBMZ.OLE1": 22332187.028463755,
        "CBMZ.API1": 258957416.24851945,
        "CBMZ.API2": 2236444589.2378774,
        "CBMZ.LIM1": 612077568.6145576,
        "CBMZ.LIM2": 894574769.6265165,
        "CBMZ.SO2": 1449858898.027273,
        "CBMZ.O1D": 0.0025963149226620116,
        "CBMZ.ANOL": 18257984460.58647,
        "CBMZ.H2O2": 26432671564.122803,
        "CBMZ.PAN": 35810884.08752975,
        "CBMZ.TOL": 9371488455.038336,
        "CBMZ.N2O5": 36.44753735340667,
        "CBMZ.XYL": 2829654016.826571,
        "CBMZ.CH4": 39874628099083.55,
        "CBMZ.CRO": 1508060.95269215,
        "CBMZ.API": 0.0023541747011317457,
        "CBMZ.LIM": 0.0023541747011317457,
        "CBMZ.HNO4": 70893.48550085393,
        "CBMZ.TO2": 891710564.7845317,
        "CBMZ.C2H6": 15018344139.10546,
        "CBMZ.XPAR": 148432.32424392801,
        "CBMZ.ETHOOH": 9714860735.90047,
        "CBMZ.HONO": 88839.80328818549,
        "CBMZ.CH3OOH": 32334862592.51974,
        "CBMZ.C2H4": 3093078129.822657,
        "CBMZ.CH3OH": 4251720116.059124,
        "CBMZ.CRES": 228418666.0829618,
        "CBMZ.O3P": 693.530553783269,
        "CBMZ.HNO3": 878205303.2490066,
        "CBMZ.CO": 1893134706812.0947,
        "CBMZ.ISOPN": 10341.490358107261,
        "CBMZ.PAR": 82621131558.68764,
        "CBMZ.OPEN": 602148216.6794686,
        "CBMZ.ISOPP": 15891928.061159626,
        "CBMZ.ISOPO2": 22996384.58431711,
        "CBMZ.OLET": 650893098.2611861,
        "CBMZ.ISOP": 889021588.334339,
        "CBMZ.HCHO": 13447831843.247477,
        "CBMZ.XO2": 41441977.67371765,
        "CBMZ.AONE": 4963026456.876871,
        "CBMZ.OLEI": 575205.3553412644,
        "CBMZ.MGLY": 985673920.7964337,
        "CBMZ.ETHP": 22447588.809553143,
        "CBMZ.NAP": 317175.6637221918,
        "CBMZ.ALD2": 9189691482.240993,
        "CBMZ.CH3O2": 251872249.78269702,
        "CBMZ.ISOPRD": 7824304316.6925125,
        "CBMZ.ROOH": 15475724842.010252,
        "CBMZ.ANO2": 246956.99881611476,
        "CBMZ.RO2": 10692775.190653529,
        "CBMZ.ONIT": 586261570.4675149,
        "CBMZ.NO3": 39315.39442287416,
        "CBMZ.NO": 6598813.469786765,
        "CBMZ.NO2": 87702602.30237964,
        "CBMZ.OH": 417493.41285513126,
        "CBMZ.O3": 495239200165.17755,
        "CBMZ.HO2": 134511407.13685837,
        "CBMZ.C2O3": 55058167.40991793
      },
      "parameter_overrides": {
        "CBMZ.H2O": 5.7131156755185664e+17,
        "CBMZ.M": 2.3541746816404947e+19,
        "CBMZRateConstants.T": 306.4400329589844,
        "CBMZRateConstants.j_o31d": 4.1950684135372285e-06,
        "CBMZRateConstants.j_o33p": 8.92544849193655e-05,
        "CBMZRateConstants.j_no2": 0.0016410461394116282,
        "CBMZRateConstants.j_no3o": 0.03880280256271362,
        "CBMZRateConstants.j_hno2": 0.00036108357016928494,
        "CBMZRateConstants.j_hno3": 9.483603236049021e-08,
        "CBMZRateConstants.j_hno4": 6.349395107463351e-07,
        "CBMZRateConstants.j_h2o2": 1.2844245702581247e-06,
        "CBMZRateConstants.j_ch2or": 4.726083261630265e-06,
        "CBMZRateConstants.j_ch2om": 8.086236448434647e-06,
        "CBMZRateConstants.j_n2o5": 0.0,
        "CBMZ.HCl": 4973305837.373668,
        "CBMZ.NH3": 11149333.311450541
      },
      "assertions": [
        {
          "variable": "dH2SO4_dt",
          "time": 0.0,
          "expected": 515.1082728014372
        },
        {
          "variable": "dHCOOH_dt",
          "time": 0.0,
          "expected": 2628.4846049197495
        },
        {
          "variable": "dRCOOH_dt",
          "time": 0.0,
          "expected": 50562.45231544572
        },
        {
          "variable": "dARO1_dt",
          "time": 0.0,
          "expected": 2220.252292929155
        },
        {
          "variable": "dARO2_dt",
          "time": 0.0,
          "expected": 6148.3909976621335
        },
        {
          "variable": "dALK1_dt",
          "time": 0.0,
          "expected": 335.2795269055089
        },
        {
          "variable": "dOLE1_dt",
          "time": 0.0,
          "expected": 91.14466024117561
        },
        {
          "variable": "dAPI1_dt",
          "time": 0.0,
          "expected": 0.00015103045598183058
        },
        {
          "variable": "dAPI2_dt",
          "time": 0.0,
          "expected": 0.0013043539149134725
        },
        {
          "variable": "dLIM1_dt",
          "time": 0.0,
          "expected": 0.0018490911899989768
        },
        {
          "variable": "dLIM2_dt",
          "time": 0.0,
          "expected": 0.002702518281498261
        },
        {
          "variable": "dSO2_dt",
          "time": 0.0,
          "expected": -515.1082728014372
        },
        {
          "variable": "dO1D_dt",
          "time": 0.0,
          "expected": -9396.079333329108
        },
        {
          "variable": "dANOL_dt",
          "time": 0.0,
          "expected": -24782.928334501834
        },
        {
          "variable": "dH2O2_dt",
          "time": 0.0,
          "expected": 46266.217770516894
        },
        {
          "variable": "dPAN_dt",
          "time": 0.0,
          "expected": -7050.468055693054
        },
        {
          "variable": "dTOL_dt",
          "time": 0.0,
          "expected": -23497.624177499045
        },
        {
          "variable": "dN2O5_dt",
          "time": 0.0,
          "expected": -0.06919076701955884
        },
        {
          "variable": "dXYL_dt",
          "time": 0.0,
          "expected": -29324.457654563914
        },
        {
          "variable": "dCH4_dt",
          "time": 0.0,
          "expected": -124150.75036620628
        },
        {
          "variable": "dCRO_dt",
          "time": 0.0,
          "expected": -90.1260867361541
        },
        {
          "variable": "dAPI_dt",
          "time": 0.0,
          "expected": -0.006865056674324936
        },
        {
          "variable": "dLIM_dt",
          "time": 0.0,
          "expected": -0.01422389913944261
        },
        {
          "variable": "dHNO4_dt",
          "time": 0.0,
          "expected": -432.837470568802
        },
        {
          "variable": "dTO2_dt",
          "time": 0.0,
          "expected": -15668.171439924052
        },
        {
          "variable": "dC2H6_dt",
          "time": 0.0,
          "expected": -694.2572864996207
        },
        {
          "variable": "dXPAR_dt",
          "time": 0.0,
          "expected": -1142.8844639376873
        },
        {
          "variable": "dETHOOH_dt",
          "time": 0.0,
          "expected": -16100.642710999371
        },
        {
          "variable": "dHONO_dt",
          "time": 0.0,
          "expected": -7.294780364022179
        },
        {
          "variable": "dCH3OOH_dt",
          "time": 0.0,
          "expected": 47589.653642186415
        },
        {
          "variable": "dC2H4_dt",
          "time": 0.0,
          "expected": -13952.128769820167
        },
        {
          "variable": "dCH3OH_dt",
          "time": 0.0,
          "expected": 45432.794071235534
        },
        {
          "variable": "dCRES_dt",
          "time": 0.0,
          "expected": 178.47477696331407
        },
        {
          "variable": "dO3P_dt",
          "time": 0.0,
          "expected": -12667.041269935962
        },
        {
          "variable": "dHNO3_dt",
          "time": 0.0,
          "expected": 367.65201112610106
        },
        {
          "variable": "dCO_dt",
          "time": 0.0,
          "expected": 142518.90087755746
        },
        {
          "variable": "dISOPN_dt",
          "time": 0.0,
          "expected": -0.5858978158055201
        },
        {
          "variable": "dPAR_dt",
          "time": 0.0,
          "expected": -118193.45599514233
        },
        {
          "variable": "dOPEN_dt",
          "time": 0.0,
          "expected": 10034.366820529662
        },
        {
          "variable": "dISOPP_dt",
          "time": 0.0,
          "expected": -1629.9275808840139
        },
        {
          "variable": "dISOPO2_dt",
          "time": 0.0,
          "expected": -1374.6920303549014
        },
        {
          "variable": "dOLET_dt",
          "time": 0.0,
          "expected": -11306.473643441974
        },
        {
          "variable": "dISOP_dt",
          "time": 0.0,
          "expected": -44097.13114274243
        },
        {
          "variable": "dHCHO_dt",
          "time": 0.0,
          "expected": -15715.126696925976
        },
        {
          "variable": "dXO2_dt",
          "time": 0.0,
          "expected": -2053.8003586452505
        },
        {
          "variable": "dAONE_dt",
          "time": 0.0,
          "expected": 49451.82018232431
        },
        {
          "variable": "dOLEI_dt",
          "time": 0.0,
          "expected": -86.6083455626201
        },
        {
          "variable": "dMGLY_dt",
          "time": 0.0,
          "expected": 4598.838347706991
        },
        {
          "variable": "dETHP_dt",
          "time": 0.0,
          "expected": -1601.041261661619
        },
        {
          "variable": "dNAP_dt",
          "time": 0.0,
          "expected": -5.495496162006873
        },
        {
          "variable": "dALD2_dt",
          "time": 0.0,
          "expected": 28572.13795383877
        },
        {
          "variable": "dCH3O2_dt",
          "time": 0.0,
          "expected": -911.9828019172273
        },
        {
          "variable": "dISOPRD_dt",
          "time": 0.0,
          "expected": -118713.90439338607
        },
        {
          "variable": "dROOH_dt",
          "time": 0.0,
          "expected": 18078.828600196433
        },
        {
          "variable": "dANO2_dt",
          "time": 0.0,
          "expected": -10.036326040350048
        },
        {
          "variable": "dRO2_dt",
          "time": 0.0,
          "expected": -2177.4105841886703
        },
        {
          "variable": "dONIT_dt",
          "time": 0.0,
          "expected": 4165.797519069131
        },
        {
          "variable": "dNO3_dt",
          "time": 0.0,
          "expected": 4.2220099748178015
        },
        {
          "variable": "dNO_dt",
          "time": 0.0,
          "expected": -735.0634836800632
        },
        {
          "variable": "dNO2_dt",
          "time": 0.0,
          "expected": 3694.211474356306
        },
        {
          "variable": "dOH_dt",
          "time": 0.0,
          "expected": 8813.817587031741
        },
        {
          "variable": "dO3_dt",
          "time": 0.0,
          "expected": -397442.0073312365
        },
        {
          "variable": "dHO2_dt",
          "time": 0.0,
          "expected": 20792.02328795953
        },
        {
          "variable": "dC2O3_dt",
          "time": 0.0,
          "expected": -1142.6079488575956
        }
      ]
    }
  ]
}
```

</details>
