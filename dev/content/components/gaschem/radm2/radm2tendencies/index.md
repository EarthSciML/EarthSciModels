---
title: "RADM2Tendencies"
slug: "radm2tendencies"
domains: ["gaschem"]
component_types: ["model"]
subdomains: ["radm2"]
domain: "gaschem"
subdomain: "radm2"
component_type: "model"
esm_version: "1.1.0"
esm_path: "components/gaschem/radm2/radm2.esm"
reference: "10.1029/JD095iD10p16343"
description: "The RADM2 gas-phase mechanism (Stockwell et al. 1990) exactly as WRF-Chem chem_opt = 101 (the KPP build of RADM2; chem_opt = 1 is the older hand-coded RADM2 of chem/module_radm.F, a different code path) integrates it: the 156 reactions of radm2.eqn (21 photolysis + 135 thermal) over 59 variable species, translated from chem/KPP/mechanisms/radm2/radm2.eqn and radm2.spc of WRF v4.8.0 by a translation script. The reaction system has 157 entries, one more than the .eqn, because the negative product \"-0.9 OH\" of reaction 60 is written as the extra entry R060x. The document holds three components. The model RADM2RateConstants evaluates every thermal rate coefficient from the hand-authored WRF rate-law templates (radm2_ratelaws.esm) with the .eqn coefficients bound once, and exposes them as observeds tested at t = 0 against the real64 KPP box driver and against a real WRF-Chem chem_opt = 101 single-column run. The reaction system RADM2 carries the stoichiometry only, each rate being a scoped reference to that model (photolysis rates are its parameters j_*). The model RADM2Tendencies exposes the mass-action tendency of every species as an observed, so the right-hand side is tested at t = 0 independently of any integrator. Species are in molec/cm^3 (the KPP units; WRF converts its ppmV chem array with conv = 1e-6 dens2con_a rho). The two KPP fixed species are not species here: air (M) and water vapour (H2O) are the parameters RADM2RateConstants.M and RADM2RateConstants.H2O, the single source of each for the whole document. The rate laws read them as arguments, the five reactions in which KPP multiplies by a fixed species (R022, R024 and R036 by M; R025 and R033 by H2O) multiply their rate by them, and the relative humidity of the heterogeneous N2O5 rate is derived from H2O, M, T and p with WRF's own formula, so no override can leave two copies of one quantity disagreeing. Mass action is that of esm-spec 7.4, v = k prod S_i^n_i with no 1/n_i! factor, which is also what KPP generates. The eight reactions with a doubled substrate (R032 and R033 HO2 + HO2, R036 NO + NO, R119 MO2 + MO2, R140 ACO3 + ACO3, R147 XO2 + XO2, R153 XNO2 + XNO2, R156 OLN + OLN) carry their .eqn coefficients unchanged on that understanding: a binding that lowers this document to Catalyst.jl must build it with combinatoric_ratelaws = false, or those eight rates come out at half the KPP value. Single-precision literals of radm2.eqn and of the WRF-Chem coupler (.20946e0, .78084, -2.3, the constants of rc_n2o5 and of the relative humidity) are transcribed as the binary64 value of the single-precision number, since that is what the Fortran evaluates."
tags: ["gaschem", "radm2", "model", "wrf-chem", "kpp", "mechanism"]
---

## Description

The RADM2 gas-phase mechanism (Stockwell et al. 1990) exactly as WRF-Chem chem_opt = 101 (the KPP build of RADM2; chem_opt = 1 is the older hand-coded RADM2 of chem/module_radm.F, a different code path) integrates it: the 156 reactions of radm2.eqn (21 photolysis + 135 thermal) over 59 variable species, translated from chem/KPP/mechanisms/radm2/radm2.eqn and radm2.spc of WRF v4.8.0 by a translation script. The reaction system has 157 entries, one more than the .eqn, because the negative product "-0.9 OH" of reaction 60 is written as the extra entry R060x. The document holds three components. The model RADM2RateConstants evaluates every thermal rate coefficient from the hand-authored WRF rate-law templates (radm2_ratelaws.esm) with the .eqn coefficients bound once, and exposes them as observeds tested at t = 0 against the real64 KPP box driver and against a real WRF-Chem chem_opt = 101 single-column run. The reaction system RADM2 carries the stoichiometry only, each rate being a scoped reference to that model (photolysis rates are its parameters j_*). The model RADM2Tendencies exposes the mass-action tendency of every species as an observed, so the right-hand side is tested at t = 0 independently of any integrator. Species are in molec/cm^3 (the KPP units; WRF converts its ppmV chem array with conv = 1e-6 dens2con_a rho). The two KPP fixed species are not species here: air (M) and water vapour (H2O) are the parameters RADM2RateConstants.M and RADM2RateConstants.H2O, the single source of each for the whole document. The rate laws read them as arguments, the five reactions in which KPP multiplies by a fixed species (R022, R024 and R036 by M; R025 and R033 by H2O) multiply their rate by them, and the relative humidity of the heterogeneous N2O5 rate is derived from H2O, M, T and p with WRF's own formula, so no override can leave two copies of one quantity disagreeing. Mass action is that of esm-spec 7.4, v = k prod S_i^n_i with no 1/n_i! factor, which is also what KPP generates. The eight reactions with a doubled substrate (R032 and R033 HO2 + HO2, R036 NO + NO, R119 MO2 + MO2, R140 ACO3 + ACO3, R147 XO2 + XO2, R153 XNO2 + XNO2, R156 OLN + OLN) carry their .eqn coefficients unchanged on that understanding: a binding that lowers this document to Catalyst.jl must build it with combinatoric_ratelaws = false, or those eight rates come out at half the KPP value. Single-precision literals of radm2.eqn and of the WRF-Chem coupler (.20946e0, .78084, -2.3, the constants of rc_n2o5 and of the relative humidity) are transcribed as the binary64 value of the single-precision number, since that is what the Fortran evaluates.

## Reference

_The instantaneous net production rate of every variable RADM2 species, exposed as an observed so that it can be asserted at t = 0. Each equation is the identity d<SPC>_dt = D(RADM2.<SPC>, t): esm-spec 7.4 resolves a right-hand-side time derivative over a mechanism species to the tendency the reaction system already derives, so this model adds no physics -- it is the derivative-test surface of the mechanism, and the companion to the RADM2 trajectory tests that check the same mechanism through an integrator: each of the four regimes has a tendency test here and a trajectory test there, with identical initial_conditions and parameter_overrides._

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `dSULF_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of SULF, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dORA1_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of ORA1, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dORA2_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of ORA2, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dCO2_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of CO2, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dSO2_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of SO2, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dETH_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of ETH, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dO1D_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of O1D, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dHC5_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of HC5, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dHC8_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of HC8, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dTOL_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of TOL, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dXYL_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of XYL, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dTPAN_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of TPAN, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dHONO_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of HONO, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dH2O2_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of H2O2, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dN2O5_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of N2O5, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dHC3_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of HC3, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dCH4_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of CH4, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dPAA_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of PAA, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dO3P_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of O3P, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dHNO4_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of HNO4, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dOP1_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of OP1, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dCSL_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of CSL, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dPAN_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of PAN, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dOL2_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of OL2, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dHNO3_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of HNO3, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dCO_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of CO, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dISO_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of ISO, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dOLT_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of OLT, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dOLI_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of OLI, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dDCB_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of DCB, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dGLY_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of GLY, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dXNO2_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of XNO2, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dKET_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of KET, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dMGLY_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of MGLY, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dTOLP_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of TOLP, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dXYLP_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of XYLP, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dOLTP_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of OLTP, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dOLN_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of OLN, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dXO2_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of XO2, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dOL2P_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of OL2P, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dHC5P_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of HC5P, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dOP2_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of OP2, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dHCHO_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of HCHO, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dHC8P_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of HC8P, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dTCO3_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of TCO3, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dO3_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of O3, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dONIT_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of ONIT, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dALD_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of ALD, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dOLIP_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of OLIP, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dKETP_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of KETP, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dHO2_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of HO2, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dMO2_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of MO2, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dOH_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of OH, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dNO3_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of NO3, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dACO3_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of ACO3, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dHC3P_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of HC3P, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dETHP_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of ETHP, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dNO_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of NO, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |
| `dNO2_dt` | `molec/cm^3/s` |  | Instantaneous net production rate of NO2, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun). |

## Observed expressions

$$
dSULF_{dt} = \mathrm{D}\left(RADM2.SULF\right)
$$
_Instantaneous net production rate of SULF, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dORA1_{dt} = \mathrm{D}\left(RADM2.ORA1\right)
$$
_Instantaneous net production rate of ORA1, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dORA2_{dt} = \mathrm{D}\left(RADM2.ORA2\right)
$$
_Instantaneous net production rate of ORA2, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dCO2_{dt} = \mathrm{D}\left(RADM2.CO2\right)
$$
_Instantaneous net production rate of CO2, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dSO2_{dt} = \mathrm{D}\left(RADM2.SO2\right)
$$
_Instantaneous net production rate of SO2, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dETH_{dt} = \mathrm{D}\left(RADM2.ETH\right)
$$
_Instantaneous net production rate of ETH, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dO1D_{dt} = \mathrm{D}\left(RADM2.O1D\right)
$$
_Instantaneous net production rate of O1D, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dHC5_{dt} = \mathrm{D}\left(RADM2.HC5\right)
$$
_Instantaneous net production rate of HC5, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dHC8_{dt} = \mathrm{D}\left(RADM2.HC8\right)
$$
_Instantaneous net production rate of HC8, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dTOL_{dt} = \mathrm{D}\left(RADM2.TOL\right)
$$
_Instantaneous net production rate of TOL, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dXYL_{dt} = \mathrm{D}\left(RADM2.XYL\right)
$$
_Instantaneous net production rate of XYL, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dTPAN_{dt} = \mathrm{D}\left(RADM2.TPAN\right)
$$
_Instantaneous net production rate of TPAN, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dHONO_{dt} = \mathrm{D}\left(RADM2.HONO\right)
$$
_Instantaneous net production rate of HONO, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dH2O2_{dt} = \mathrm{D}\left(RADM2.H2O2\right)
$$
_Instantaneous net production rate of H2O2, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dN2O5_{dt} = \mathrm{D}\left(RADM2.N2O5\right)
$$
_Instantaneous net production rate of N2O5, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dHC3_{dt} = \mathrm{D}\left(RADM2.HC3\right)
$$
_Instantaneous net production rate of HC3, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dCH4_{dt} = \mathrm{D}\left(RADM2.CH4\right)
$$
_Instantaneous net production rate of CH4, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dPAA_{dt} = \mathrm{D}\left(RADM2.PAA\right)
$$
_Instantaneous net production rate of PAA, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dO3P_{dt} = \mathrm{D}\left(RADM2.O3P\right)
$$
_Instantaneous net production rate of O3P, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dHNO4_{dt} = \mathrm{D}\left(RADM2.HNO4\right)
$$
_Instantaneous net production rate of HNO4, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dOP1_{dt} = \mathrm{D}\left(RADM2.OP1\right)
$$
_Instantaneous net production rate of OP1, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dCSL_{dt} = \mathrm{D}\left(RADM2.CSL\right)
$$
_Instantaneous net production rate of CSL, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dPAN_{dt} = \mathrm{D}\left(RADM2.PAN\right)
$$
_Instantaneous net production rate of PAN, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dOL2_{dt} = \mathrm{D}\left(RADM2.OL2\right)
$$
_Instantaneous net production rate of OL2, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dHNO3_{dt} = \mathrm{D}\left(RADM2.HNO3\right)
$$
_Instantaneous net production rate of HNO3, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dCO_{dt} = \mathrm{D}\left(RADM2.CO\right)
$$
_Instantaneous net production rate of CO, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dISO_{dt} = \mathrm{D}\left(RADM2.ISO\right)
$$
_Instantaneous net production rate of ISO, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dOLT_{dt} = \mathrm{D}\left(RADM2.OLT\right)
$$
_Instantaneous net production rate of OLT, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dOLI_{dt} = \mathrm{D}\left(RADM2.OLI\right)
$$
_Instantaneous net production rate of OLI, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dDCB_{dt} = \mathrm{D}\left(RADM2.DCB\right)
$$
_Instantaneous net production rate of DCB, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dGLY_{dt} = \mathrm{D}\left(RADM2.GLY\right)
$$
_Instantaneous net production rate of GLY, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dXNO2_{dt} = \mathrm{D}\left(RADM2.XNO2\right)
$$
_Instantaneous net production rate of XNO2, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dKET_{dt} = \mathrm{D}\left(RADM2.KET\right)
$$
_Instantaneous net production rate of KET, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dMGLY_{dt} = \mathrm{D}\left(RADM2.MGLY\right)
$$
_Instantaneous net production rate of MGLY, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dTOLP_{dt} = \mathrm{D}\left(RADM2.TOLP\right)
$$
_Instantaneous net production rate of TOLP, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dXYLP_{dt} = \mathrm{D}\left(RADM2.XYLP\right)
$$
_Instantaneous net production rate of XYLP, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dOLTP_{dt} = \mathrm{D}\left(RADM2.OLTP\right)
$$
_Instantaneous net production rate of OLTP, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dOLN_{dt} = \mathrm{D}\left(RADM2.OLN\right)
$$
_Instantaneous net production rate of OLN, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dXO2_{dt} = \mathrm{D}\left(RADM2.XO2\right)
$$
_Instantaneous net production rate of XO2, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dOL2P_{dt} = \mathrm{D}\left(RADM2.OL2P\right)
$$
_Instantaneous net production rate of OL2P, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dHC5P_{dt} = \mathrm{D}\left(RADM2.HC5P\right)
$$
_Instantaneous net production rate of HC5P, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dOP2_{dt} = \mathrm{D}\left(RADM2.OP2\right)
$$
_Instantaneous net production rate of OP2, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dHCHO_{dt} = \mathrm{D}\left(RADM2.HCHO\right)
$$
_Instantaneous net production rate of HCHO, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dHC8P_{dt} = \mathrm{D}\left(RADM2.HC8P\right)
$$
_Instantaneous net production rate of HC8P, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dTCO3_{dt} = \mathrm{D}\left(RADM2.TCO3\right)
$$
_Instantaneous net production rate of TCO3, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dO3_{dt} = \mathrm{D}\left(RADM2.O3\right)
$$
_Instantaneous net production rate of O3, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dONIT_{dt} = \mathrm{D}\left(RADM2.ONIT\right)
$$
_Instantaneous net production rate of ONIT, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dALD_{dt} = \mathrm{D}\left(RADM2.ALD\right)
$$
_Instantaneous net production rate of ALD, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dOLIP_{dt} = \mathrm{D}\left(RADM2.OLIP\right)
$$
_Instantaneous net production rate of OLIP, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dKETP_{dt} = \mathrm{D}\left(RADM2.KETP\right)
$$
_Instantaneous net production rate of KETP, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dHO2_{dt} = \mathrm{D}\left(RADM2.HO2\right)
$$
_Instantaneous net production rate of HO2, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dMO2_{dt} = \mathrm{D}\left(RADM2.MO2\right)
$$
_Instantaneous net production rate of MO2, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dOH_{dt} = \mathrm{D}\left(RADM2.OH\right)
$$
_Instantaneous net production rate of OH, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dNO3_{dt} = \mathrm{D}\left(RADM2.NO3\right)
$$
_Instantaneous net production rate of NO3, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dACO3_{dt} = \mathrm{D}\left(RADM2.ACO3\right)
$$
_Instantaneous net production rate of ACO3, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dHC3P_{dt} = \mathrm{D}\left(RADM2.HC3P\right)
$$
_Instantaneous net production rate of HC3P, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dETHP_{dt} = \mathrm{D}\left(RADM2.ETHP\right)
$$
_Instantaneous net production rate of ETHP, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dNO_{dt} = \mathrm{D}\left(RADM2.NO\right)
$$
_Instantaneous net production rate of NO, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

$$
dNO2_{dt} = \mathrm{D}\left(RADM2.NO2\right)
$$
_Instantaneous net production rate of NO2, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)._

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "reference": {
    "notes": "The instantaneous net production rate of every variable RADM2 species, exposed as an observed so that it can be asserted at t = 0. Each equation is the identity d<SPC>_dt = D(RADM2.<SPC>, t): esm-spec 7.4 resolves a right-hand-side time derivative over a mechanism species to the tendency the reaction system already derives, so this model adds no physics -- it is the derivative-test surface of the mechanism, and the companion to the RADM2 trajectory tests that check the same mechanism through an integrator: each of the four regimes has a tendency test here and a trajectory test there, with identical initial_conditions and parameter_overrides."
  },
  "variables": {
    "dSULF_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of SULF, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dORA1_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of ORA1, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dORA2_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of ORA2, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dCO2_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of CO2, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dSO2_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of SO2, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dETH_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of ETH, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dO1D_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of O1D, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dHC5_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of HC5, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dHC8_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of HC8, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dTOL_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of TOL, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dXYL_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of XYL, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dTPAN_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of TPAN, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dHONO_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of HONO, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dH2O2_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of H2O2, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dN2O5_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of N2O5, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dHC3_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of HC3, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dCH4_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of CH4, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dPAA_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of PAA, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dO3P_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of O3P, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dHNO4_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of HNO4, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dOP1_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of OP1, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dCSL_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of CSL, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dPAN_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of PAN, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dOL2_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of OL2, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dHNO3_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of HNO3, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dCO_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of CO, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dISO_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of ISO, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dOLT_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of OLT, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dOLI_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of OLI, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dDCB_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of DCB, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dGLY_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of GLY, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dXNO2_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of XNO2, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dKET_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of KET, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dMGLY_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of MGLY, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dTOLP_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of TOLP, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dXYLP_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of XYLP, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dOLTP_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of OLTP, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dOLN_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of OLN, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dXO2_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of XO2, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dOL2P_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of OL2P, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dHC5P_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of HC5P, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dOP2_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of OP2, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dHCHO_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of HCHO, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dHC8P_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of HC8P, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dTCO3_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of TCO3, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dO3_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of O3, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dONIT_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of ONIT, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dALD_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of ALD, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dOLIP_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of OLIP, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dKETP_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of KETP, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dHO2_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of HO2, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dMO2_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of MO2, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dOH_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of OH, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dNO3_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of NO3, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dACO3_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of ACO3, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dHC3P_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of HC3P, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dETHP_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of ETHP, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dNO_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of NO, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    },
    "dNO2_dt": {
      "type": "unknown",
      "units": "molec/cm^3/s",
      "description": "Instantaneous net production rate of NO2, the mass-action tendency the RADM2 reaction system derives for it (KPP Vdot of radm2_Fun)."
    }
  },
  "equations": [
    {
      "lhs": "dSULF_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.SULF"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dORA1_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.ORA1"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dORA2_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.ORA2"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dCO2_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.CO2"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dSO2_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.SO2"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dETH_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.ETH"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dO1D_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.O1D"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dHC5_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.HC5"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dHC8_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.HC8"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dTOL_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.TOL"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dXYL_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.XYL"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dTPAN_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.TPAN"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dHONO_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.HONO"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dH2O2_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.H2O2"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dN2O5_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.N2O5"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dHC3_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.HC3"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dCH4_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.CH4"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dPAA_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.PAA"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dO3P_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.O3P"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dHNO4_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.HNO4"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dOP1_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.OP1"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dCSL_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.CSL"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dPAN_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.PAN"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dOL2_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.OL2"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dHNO3_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.HNO3"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dCO_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.CO"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dISO_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.ISO"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dOLT_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.OLT"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dOLI_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.OLI"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dDCB_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.DCB"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dGLY_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.GLY"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dXNO2_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.XNO2"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dKET_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.KET"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dMGLY_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.MGLY"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dTOLP_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.TOLP"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dXYLP_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.XYLP"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dOLTP_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.OLTP"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dOLN_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.OLN"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dXO2_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.XO2"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dOL2P_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.OL2P"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dHC5P_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.HC5P"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dOP2_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.OP2"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dHCHO_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.HCHO"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dHC8P_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.HC8P"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dTCO3_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.TCO3"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dO3_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.O3"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dONIT_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.ONIT"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dALD_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.ALD"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dOLIP_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.OLIP"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dKETP_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.KETP"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dHO2_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.HO2"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dMO2_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.MO2"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dOH_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.OH"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dNO3_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.NO3"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dACO3_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.ACO3"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dHC3P_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.HC3P"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dETHP_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.ETHP"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dNO_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.NO"
        ],
        "wrt": "t"
      }
    },
    {
      "lhs": "dNO2_dt",
      "rhs": {
        "op": "D",
        "args": [
          "RADM2.NO2"
        ],
        "wrt": "t"
      }
    }
  ],
  "tests": [
    {
      "id": "box_urban_noon_tendencies",
      "description": "Instantaneous net production rate of all 59 variable species at the urban noon box state (T 298 K, p 101325 Pa, M 2.462e19 and H2O 6.963e17 molec/cm3 (RH 0.550), clear-sky noon photolysis), against Vdot from radm2_Fun of the standalone WRF-Chem RADM2 KPP box driver (real64, KPP-generated code from chem/KPP/mechanisms/radm2 of WRF v4.8.0 with WRFUserRateLaws; dump dumps/radm2/box_urban_noon.json). This is the instantaneous-derivative shape PLAN.md section 6 asks for: each d<SPC>_dt is an observed written D(RADM2.<SPC>, t), which esm-spec section 7.4 resolves to the tendency the reaction system already derives, so asserting it at time 0 evaluates the mechanism right-hand side at the given state and pins the whole stoichiometric matrix and every rate law independently of any integrator. The environment (T, p, M, H2O and the photolysis frequencies) is set through the same scoped parameter_overrides, and the species through the same initial_conditions, as the matching trajectory test of RADM2. Measured agreement with the Fortran (Rust CLI, real64 both sides): 140 of the 236 assertions across the four regimes are BIT-IDENTICAL to KPP, the largest residual anywhere is 9.5e-7 relative (dALD_dt, rural morning) and every other species is within 7.2e-8 (dN2O5_dt, urban noon). That residual is summation-order rounding amplified by cancellation, not a stoichiometric difference: ALD sums 35 terms whose net is 1.1 % of the largest of them, and reconstructing the budget from this document's own stoichiometry times the dump's reaction rates A reproduces the esm value rather than the Fortran one. The tolerance is held at rel 1e-5 rather than tightened to that residual because evaluation ORDER differs between bindings, so a tolerance tuned to one binding's rounding would not hold in the others; every error class this test exists to catch -- a wrong stoichiometric coefficient, a misbound rate law -- moves a tendency by O(1), not by 1e-6.",
      "time_span": {
        "start": 0,
        "end": 1
      },
      "tolerance": {
        "rel": 1e-05
      },
      "initial_conditions": {
        "RADM2.O3": 1477411357577.5947,
        "RADM2.H2O2": 24623522626.293247,
        "RADM2.NO": 492470452525.86487,
        "RADM2.NO2": 984940905051.7297,
        "RADM2.NO3": 49247045.2525865,
        "RADM2.N2O5": 1231176131.3146625,
        "RADM2.HONO": 12311761313.146624,
        "RADM2.HNO3": 49247045252.586494,
        "RADM2.HNO4": 1231176131.3146625,
        "RADM2.SO2": 123117613131.46622,
        "RADM2.SULF": 2462352262.629325,
        "RADM2.CO": 12311761313146.623,
        "RADM2.ETH": 246235226262.93243,
        "RADM2.HC3": 492470452525.86487,
        "RADM2.HC5": 246235226262.93243,
        "RADM2.HC8": 123117613131.46622,
        "RADM2.OL2": 123117613131.46622,
        "RADM2.OLT": 49247045252.586494,
        "RADM2.OLI": 24623522626.293247,
        "RADM2.ISO": 24623522626.293247,
        "RADM2.TOL": 123117613131.46622,
        "RADM2.XYL": 73870567878.87975,
        "RADM2.CSL": 4924704525.25865,
        "RADM2.HCHO": 123117613131.46622,
        "RADM2.ALD": 49247045252.586494,
        "RADM2.ETHP": 24623522.62629325,
        "RADM2.KET": 49247045252.586494,
        "RADM2.GLY": 4924704525.25865,
        "RADM2.MGLY": 7387056787.887973,
        "RADM2.MO2": 123117613.13146622,
        "RADM2.DCB": 2462352262.629325,
        "RADM2.ONIT": 12311761313.146624,
        "RADM2.PAN": 24623522626.293247,
        "RADM2.TPAN": 1231176131.3146625,
        "RADM2.OP1": 12311761313.146624,
        "RADM2.OP2": 7387056787.887973,
        "RADM2.PAA": 2462352262.629325,
        "RADM2.ORA1": 12311761313.146624,
        "RADM2.ORA2": 12311761313.146624,
        "RADM2.OH": 4924704.525258649,
        "RADM2.HO2": 492470452.5258649,
        "RADM2.O3P": 2462.3522626293243,
        "RADM2.O1D": 2.4623522626293246,
        "RADM2.HC3P": 24623522.62629325,
        "RADM2.HC5P": 12311761.313146625,
        "RADM2.HC8P": 7387056.787887973,
        "RADM2.OLTP": 7387056.787887973,
        "RADM2.OLIP": 4924704.525258649,
        "RADM2.TOLP": 4924704.525258649,
        "RADM2.XYLP": 4924704.525258649,
        "RADM2.ACO3": 49247045.2525865,
        "RADM2.TCO3": 4924704.525258649,
        "RADM2.KETP": 4924704.525258649,
        "RADM2.OLN": 2462352.2626293246,
        "RADM2.XO2": 24623522.62629325,
        "RADM2.XNO2": 2462352.2626293246,
        "RADM2.CH4": 44322340727327.84,
        "RADM2.CO2": 9849409050517298.0,
        "RADM2.OL2P": 7387056.787887973
      },
      "parameter_overrides": {
        "RADM2RateConstants.T": 298.0,
        "RADM2RateConstants.p": 101325.0,
        "RADM2RateConstants.M": 2.4623522626293244e+19,
        "RADM2RateConstants.H2O": 6.9628642030342e+17,
        "RADM2RateConstants.j_no2": 0.0085,
        "RADM2RateConstants.j_o31d": 3.2e-05,
        "RADM2RateConstants.j_o33p": 0.00042,
        "RADM2RateConstants.j_hno2": 0.0017,
        "RADM2RateConstants.j_hno3": 6.5e-07,
        "RADM2RateConstants.j_hno4": 4.2e-06,
        "RADM2RateConstants.j_no3o2": 0.023,
        "RADM2RateConstants.j_no3o": 0.185,
        "RADM2RateConstants.j_h2o2": 7.3e-06,
        "RADM2RateConstants.j_ch2om": 4.6e-05,
        "RADM2RateConstants.j_ch2or": 3.1e-05,
        "RADM2RateConstants.j_ch3cho": 5.5e-06,
        "RADM2RateConstants.j_ch3o2h": 5.4e-06,
        "RADM2RateConstants.j_ch3coch3": 6.8e-07,
        "RADM2RateConstants.j_ch3coo2h": 3.2e-06,
        "RADM2RateConstants.j_ch3coc2h5": 1.6e-06,
        "RADM2RateConstants.j_hcocho": 0.00011,
        "RADM2RateConstants.j_hcochob": 2.1e-05,
        "RADM2RateConstants.j_ch3cocho": 0.00016,
        "RADM2RateConstants.j_hcochest": 0.00022,
        "RADM2RateConstants.j_ch3ono2": 1.1e-06
      },
      "assertions": [
        {
          "variable": "dSULF_dt",
          "time": 0.0,
          "expected": 538879.4420362803
        },
        {
          "variable": "dORA1_dt",
          "time": 0.0,
          "expected": 747295.0851294074
        },
        {
          "variable": "dORA2_dt",
          "time": 0.0,
          "expected": 1976071.739171624
        },
        {
          "variable": "dCO2_dt",
          "time": 0.0,
          "expected": 14556792.049749197
        },
        {
          "variable": "dSO2_dt",
          "time": 0.0,
          "expected": -538879.4420362803
        },
        {
          "variable": "dETH_dt",
          "time": 0.0,
          "expected": -332516.978951721
        },
        {
          "variable": "dO1D_dt",
          "time": 0.0,
          "expected": -2076582583.2093546
        },
        {
          "variable": "dHC5_dt",
          "time": 0.0,
          "expected": -5861086.515600634
        },
        {
          "variable": "dHC8_dt",
          "time": 0.0,
          "expected": -6165998.530863093
        },
        {
          "variable": "dTOL_dt",
          "time": 0.0,
          "expected": -3751378.450628188
        },
        {
          "variable": "dXYL_dt",
          "time": 0.0,
          "expected": -10147700.672115842
        },
        {
          "variable": "dTPAN_dt",
          "time": 0.0,
          "expected": 22357733.075322565
        },
        {
          "variable": "dHONO_dt",
          "time": 0.0,
          "expected": -9117009.669340214
        },
        {
          "variable": "dH2O2_dt",
          "time": 0.0,
          "expected": 1422290.0010474222
        },
        {
          "variable": "dN2O5_dt",
          "time": 0.0,
          "expected": -9551049.83039074
        },
        {
          "variable": "dHC3_dt",
          "time": 0.0,
          "expected": -6297684.557117478
        },
        {
          "variable": "dCH4_dt",
          "time": 0.0,
          "expected": -1259672.1068281143
        },
        {
          "variable": "dPAA_dt",
          "time": 0.0,
          "expected": 17352.413356229314
        },
        {
          "variable": "dO3P_dt",
          "time": 0.0,
          "expected": 10557727573.119297
        },
        {
          "variable": "dHNO4_dt",
          "time": 0.0,
          "expected": 568260689.0192308
        },
        {
          "variable": "dOP1_dt",
          "time": 0.0,
          "expected": -306562.5928631717
        },
        {
          "variable": "dCSL_dt",
          "time": 0.0,
          "expected": -974953.4541032109
        },
        {
          "variable": "dPAN_dt",
          "time": 0.0,
          "expected": 240492163.94609526
        },
        {
          "variable": "dOL2_dt",
          "time": 0.0,
          "expected": -5495625.337997163
        },
        {
          "variable": "dHNO3_dt",
          "time": 0.0,
          "expected": 68135647.53002009
        },
        {
          "variable": "dCO_dt",
          "time": 0.0,
          "expected": 23816618.840455897
        },
        {
          "variable": "dISO_dt",
          "time": 0.0,
          "expected": -13425065.945633195
        },
        {
          "variable": "dOLT_dt",
          "time": 0.0,
          "expected": -7865041.151744312
        },
        {
          "variable": "dOLI_dt",
          "time": 0.0,
          "expected": -15536060.756244041
        },
        {
          "variable": "dDCB_dt",
          "time": 0.0,
          "expected": 27183213.575081337
        },
        {
          "variable": "dGLY_dt",
          "time": 0.0,
          "expected": 18643908.7246103
        },
        {
          "variable": "dXNO2_dt",
          "time": 0.0,
          "expected": -13306996.862576583
        },
        {
          "variable": "dKET_dt",
          "time": 0.0,
          "expected": 87370858.18563263
        },
        {
          "variable": "dMGLY_dt",
          "time": 0.0,
          "expected": 30437960.981503617
        },
        {
          "variable": "dTOLP_dt",
          "time": 0.0,
          "expected": -15836406.45573939
        },
        {
          "variable": "dXYLP_dt",
          "time": 0.0,
          "expected": -10227348.90521241
        },
        {
          "variable": "dOLTP_dt",
          "time": 0.0,
          "expected": -8774763.997361593
        },
        {
          "variable": "dOLN_dt",
          "time": 0.0,
          "expected": -7091835.20528191
        },
        {
          "variable": "dXO2_dt",
          "time": 0.0,
          "expected": -48997287.03370748
        },
        {
          "variable": "dOL2P_dt",
          "time": 0.0,
          "expected": -22797926.921809237
        },
        {
          "variable": "dHC5P_dt",
          "time": 0.0,
          "expected": -40763871.41432572
        },
        {
          "variable": "dOP2_dt",
          "time": 0.0,
          "expected": 34048.744698626106
        },
        {
          "variable": "dHCHO_dt",
          "time": 0.0,
          "expected": 550325987.0522168
        },
        {
          "variable": "dHC8P_dt",
          "time": 0.0,
          "expected": -21808957.578855377
        },
        {
          "variable": "dTCO3_dt",
          "time": 0.0,
          "expected": -39254809.99552578
        },
        {
          "variable": "dO3_dt",
          "time": 0.0,
          "expected": -13794853796.530283
        },
        {
          "variable": "dONIT_dt",
          "time": 0.0,
          "expected": 32265631.438031107
        },
        {
          "variable": "dALD_dt",
          "time": 0.0,
          "expected": 261773479.8402832
        },
        {
          "variable": "dOLIP_dt",
          "time": 0.0,
          "expected": -10461390.514745986
        },
        {
          "variable": "dKETP_dt",
          "time": 0.0,
          "expected": -18411046.20776064
        },
        {
          "variable": "dHO2_dt",
          "time": 0.0,
          "expected": -1684839608.5053043
        },
        {
          "variable": "dMO2_dt",
          "time": 0.0,
          "expected": -275371664.95982623
        },
        {
          "variable": "dOH_dt",
          "time": 0.0,
          "expected": 2621995331.735931
        },
        {
          "variable": "dNO3_dt",
          "time": 0.0,
          "expected": -647577624.5308689
        },
        {
          "variable": "dACO3_dt",
          "time": 0.0,
          "expected": -420162020.3746819
        },
        {
          "variable": "dHC3P_dt",
          "time": 0.0,
          "expected": -87687552.45486586
        },
        {
          "variable": "dETHP_dt",
          "time": 0.0,
          "expected": -92839925.47674929
        },
        {
          "variable": "dNO_dt",
          "time": 0.0,
          "expected": -8734133640.122599
        },
        {
          "variable": "dNO2_dt",
          "time": 0.0,
          "expected": 8485510343.069271
        }
      ]
    },
    {
      "id": "box_rural_morning_tendencies",
      "description": "Instantaneous net production rate of all 59 variable species at the rural morning box state (T 288 K, p 95000 Pa, M 2.389e19 and H2O 5.558e17 molec/cm3 (RH 0.800), 35 % of noon photolysis), against Vdot from radm2_Fun of the standalone WRF-Chem RADM2 KPP box driver (real64, KPP-generated code from chem/KPP/mechanisms/radm2 of WRF v4.8.0 with WRFUserRateLaws; dump dumps/radm2/box_rural_morning.json). This is the instantaneous-derivative shape PLAN.md section 6 asks for: each d<SPC>_dt is an observed written D(RADM2.<SPC>, t), which esm-spec section 7.4 resolves to the tendency the reaction system already derives, so asserting it at time 0 evaluates the mechanism right-hand side at the given state and pins the whole stoichiometric matrix and every rate law independently of any integrator. The environment (T, p, M, H2O and the photolysis frequencies) is set through the same scoped parameter_overrides, and the species through the same initial_conditions, as the matching trajectory test of RADM2. Measured agreement with the Fortran (Rust CLI, real64 both sides): 140 of the 236 assertions across the four regimes are BIT-IDENTICAL to KPP, the largest residual anywhere is 9.5e-7 relative (dALD_dt, rural morning) and every other species is within 7.2e-8 (dN2O5_dt, urban noon). That residual is summation-order rounding amplified by cancellation, not a stoichiometric difference: ALD sums 35 terms whose net is 1.1 % of the largest of them, and reconstructing the budget from this document's own stoichiometry times the dump's reaction rates A reproduces the esm value rather than the Fortran one. The tolerance is held at rel 1e-5 rather than tightened to that residual because evaluation ORDER differs between bindings, so a tolerance tuned to one binding's rounding would not hold in the others; every error class this test exists to catch -- a wrong stoichiometric coefficient, a misbound rate law -- moves a tendency by O(1), not by 1e-6.",
      "time_span": {
        "start": 0,
        "end": 1
      },
      "tolerance": {
        "rel": 1e-05
      },
      "initial_conditions": {
        "RADM2.O3": 1074962875571.1233,
        "RADM2.H2O2": 47776127803.161026,
        "RADM2.NO": 2388806390.1580515,
        "RADM2.NO2": 11944031950.790257,
        "RADM2.NO3": 23888063.901580516,
        "RADM2.N2O5": 119440319.50790258,
        "RADM2.HONO": 238880639.01580516,
        "RADM2.HNO3": 11944031950.790257,
        "RADM2.HNO4": 238880639.01580516,
        "RADM2.SO2": 11944031950.790257,
        "RADM2.SULF": 1194403195.0790257,
        "RADM2.CO": 2866567668189.662,
        "RADM2.ETH": 23888063901.580513,
        "RADM2.HC3": 47776127803.161026,
        "RADM2.HC5": 23888063901.580513,
        "RADM2.HC8": 11944031950.790257,
        "RADM2.OL2": 7166419170.4741535,
        "RADM2.OLT": 4777612780.316103,
        "RADM2.OLI": 2388806390.1580515,
        "RADM2.ISO": 47776127803.161026,
        "RADM2.TOL": 4777612780.316103,
        "RADM2.XYL": 2388806390.1580515,
        "RADM2.CSL": 477761278.0316103,
        "RADM2.HCHO": 23888063901.580513,
        "RADM2.ALD": 11944031950.790257,
        "RADM2.ETHP": 11944031.950790258,
        "RADM2.KET": 11944031950.790257,
        "RADM2.GLY": 1194403195.0790257,
        "RADM2.MGLY": 2388806390.1580515,
        "RADM2.MO2": 191104511.21264413,
        "RADM2.DCB": 477761278.0316103,
        "RADM2.ONIT": 2388806390.1580515,
        "RADM2.PAN": 7166419170.4741535,
        "RADM2.TPAN": 238880639.01580516,
        "RADM2.OP1": 11944031950.790257,
        "RADM2.OP2": 4777612780.316103,
        "RADM2.PAA": 1194403195.0790257,
        "RADM2.ORA1": 7166419170.4741535,
        "RADM2.ORA2": 7166419170.4741535,
        "RADM2.OH": 7166419.170474154,
        "RADM2.HO2": 716641917.0474154,
        "RADM2.O3P": 2388.8063901580513,
        "RADM2.O1D": 2.3888063901580514,
        "RADM2.HC3P": 11944031.950790258,
        "RADM2.HC5P": 4777612.780316103,
        "RADM2.HC8P": 2388806.3901580516,
        "RADM2.OLTP": 4777612.780316103,
        "RADM2.OLIP": 2388806.3901580516,
        "RADM2.TOLP": 1194403.1950790258,
        "RADM2.XYLP": 1194403.1950790258,
        "RADM2.ACO3": 47776127.80316103,
        "RADM2.TCO3": 1194403.1950790258,
        "RADM2.KETP": 2388806.3901580516,
        "RADM2.OLN": 1194403.1950790258,
        "RADM2.XO2": 11944031.950790258,
        "RADM2.XNO2": 477761.27803161036,
        "RADM2.CH4": 42998515022844.93,
        "RADM2.CO2": 9555225560632206.0,
        "RADM2.OL2P": 2388806.3901580516
      },
      "parameter_overrides": {
        "RADM2RateConstants.T": 288.0,
        "RADM2RateConstants.p": 95000.0,
        "RADM2RateConstants.M": 2.3888063901580513e+19,
        "RADM2RateConstants.H2O": 5.5580701458619514e+17,
        "RADM2RateConstants.j_no2": 0.002975,
        "RADM2RateConstants.j_o31d": 1.12e-05,
        "RADM2RateConstants.j_o33p": 0.000147,
        "RADM2RateConstants.j_hno2": 0.0005949999999999999,
        "RADM2RateConstants.j_hno3": 2.275e-07,
        "RADM2RateConstants.j_hno4": 1.4699999999999997e-06,
        "RADM2RateConstants.j_no3o2": 0.00805,
        "RADM2RateConstants.j_no3o": 0.06475,
        "RADM2RateConstants.j_h2o2": 2.555e-06,
        "RADM2RateConstants.j_ch2om": 1.61e-05,
        "RADM2RateConstants.j_ch2or": 1.085e-05,
        "RADM2RateConstants.j_ch3cho": 1.9249999999999998e-06,
        "RADM2RateConstants.j_ch3o2h": 1.89e-06,
        "RADM2RateConstants.j_ch3coch3": 2.3799999999999996e-07,
        "RADM2RateConstants.j_ch3coo2h": 1.1199999999999999e-06,
        "RADM2RateConstants.j_ch3coc2h5": 5.599999999999999e-07,
        "RADM2RateConstants.j_hcocho": 3.85e-05,
        "RADM2RateConstants.j_hcochob": 7.349999999999999e-06,
        "RADM2RateConstants.j_ch3cocho": 5.6e-05,
        "RADM2RateConstants.j_hcochest": 7.7e-05,
        "RADM2RateConstants.j_ch3ono2": 3.85e-07
      },
      "assertions": [
        {
          "variable": "dSULF_dt",
          "time": 0.0,
          "expected": 77969.00427956354
        },
        {
          "variable": "dORA1_dt",
          "time": 0.0,
          "expected": 151195.08591286273
        },
        {
          "variable": "dORA2_dt",
          "time": 0.0,
          "expected": 240680.7923408179
        },
        {
          "variable": "dCO2_dt",
          "time": 0.0,
          "expected": 4876800.890656829
        },
        {
          "variable": "dSO2_dt",
          "time": 0.0,
          "expected": -77969.00427956354
        },
        {
          "variable": "dETH_dt",
          "time": 0.0,
          "expected": -41634.31036967776
        },
        {
          "variable": "dO1D_dt",
          "time": 0.0,
          "expected": -1942872479.5786755
        },
        {
          "variable": "dHC5_dt",
          "time": 0.0,
          "expected": -791592.7732714234
        },
        {
          "variable": "dHC8_dt",
          "time": 0.0,
          "expected": -832773.9002046188
        },
        {
          "variable": "dTOL_dt",
          "time": 0.0,
          "expected": -219936.75224202065
        },
        {
          "variable": "dXYL_dt",
          "time": 0.0,
          "expected": -484026.48883100913
        },
        {
          "variable": "dTPAN_dt",
          "time": 0.0,
          "expected": 49437.72810376622
        },
        {
          "variable": "dHONO_dt",
          "time": 0.0,
          "expected": -55579.21140450999
        },
        {
          "variable": "dH2O2_dt",
          "time": 0.0,
          "expected": 3520609.9615562474
        },
        {
          "variable": "dN2O5_dt",
          "time": 0.0,
          "expected": -1844942.9140743553
        },
        {
          "variable": "dHC3_dt",
          "time": 0.0,
          "expected": -834849.3731535969
        },
        {
          "variable": "dCH4_dt",
          "time": 0.0,
          "expected": -2050720.7414150622
        },
        {
          "variable": "dPAA_dt",
          "time": 0.0,
          "expected": 153702.5041566253
        },
        {
          "variable": "dO3P_dt",
          "time": 0.0,
          "expected": 1669735098.912638
        },
        {
          "variable": "dHNO4_dt",
          "time": 0.0,
          "expected": 6510907.072696074
        },
        {
          "variable": "dOP1_dt",
          "time": 0.0,
          "expected": 84011.08528406709
        },
        {
          "variable": "dCSL_dt",
          "time": 0.0,
          "expected": -125225.52257707377
        },
        {
          "variable": "dPAN_dt",
          "time": 0.0,
          "expected": 2460831.2827449627
        },
        {
          "variable": "dOL2_dt",
          "time": 0.0,
          "expected": -469971.0093809974
        },
        {
          "variable": "dHNO3_dt",
          "time": 0.0,
          "expected": 2116578.4103442803
        },
        {
          "variable": "dCO_dt",
          "time": 0.0,
          "expected": -1631415.2611701014
        },
        {
          "variable": "dISO_dt",
          "time": 0.0,
          "expected": -37370478.56171941
        },
        {
          "variable": "dOLT_dt",
          "time": 0.0,
          "expected": -1095158.966149673
        },
        {
          "variable": "dOLI_dt",
          "time": 0.0,
          "expected": -1657238.007107199
        },
        {
          "variable": "dDCB_dt",
          "time": 0.0,
          "expected": -98937.70926862406
        },
        {
          "variable": "dGLY_dt",
          "time": 0.0,
          "expected": -129363.39963060312
        },
        {
          "variable": "dXNO2_dt",
          "time": 0.0,
          "expected": 203893.67577806333
        },
        {
          "variable": "dKET_dt",
          "time": 0.0,
          "expected": 143938.19459267962
        },
        {
          "variable": "dMGLY_dt",
          "time": 0.0,
          "expected": -363709.98684831464
        },
        {
          "variable": "dTOLP_dt",
          "time": 0.0,
          "expected": 136535.18794136422
        },
        {
          "variable": "dXYLP_dt",
          "time": 0.0,
          "expected": 373324.6014115228
        },
        {
          "variable": "dOLTP_dt",
          "time": 0.0,
          "expected": 37059463.289429024
        },
        {
          "variable": "dOLN_dt",
          "time": 0.0,
          "expected": 698679.4680231046
        },
        {
          "variable": "dXO2_dt",
          "time": 0.0,
          "expected": 713345.8392220119
        },
        {
          "variable": "dOL2P_dt",
          "time": 0.0,
          "expected": 403034.6895433235
        },
        {
          "variable": "dHC5P_dt",
          "time": 0.0,
          "expected": 677869.3709735421
        },
        {
          "variable": "dOP2_dt",
          "time": 0.0,
          "expected": -46335.153550495685
        },
        {
          "variable": "dHCHO_dt",
          "time": 0.0,
          "expected": 2540277.9498040196
        },
        {
          "variable": "dHC8P_dt",
          "time": 0.0,
          "expected": 775920.0386683729
        },
        {
          "variable": "dTCO3_dt",
          "time": 0.0,
          "expected": 177477.24210590697
        },
        {
          "variable": "dO3_dt",
          "time": 0.0,
          "expected": -24910028.702258974
        },
        {
          "variable": "dONIT_dt",
          "time": 0.0,
          "expected": 35149.94168981585
        },
        {
          "variable": "dALD_dt",
          "time": 0.0,
          "expected": -15243.505080385481
        },
        {
          "variable": "dOLIP_dt",
          "time": 0.0,
          "expected": 1175534.3258956717
        },
        {
          "variable": "dKETP_dt",
          "time": 0.0,
          "expected": 20468.72497231325
        },
        {
          "variable": "dHO2_dt",
          "time": 0.0,
          "expected": -19715045.128834024
        },
        {
          "variable": "dMO2_dt",
          "time": 0.0,
          "expected": -889234.7909566378
        },
        {
          "variable": "dOH_dt",
          "time": 0.0,
          "expected": 544441053.0366713
        },
        {
          "variable": "dNO3_dt",
          "time": 0.0,
          "expected": -2621554.1982682375
        },
        {
          "variable": "dACO3_dt",
          "time": 0.0,
          "expected": -1685542.2095617428
        },
        {
          "variable": "dHC3P_dt",
          "time": 0.0,
          "expected": 620441.8856943204
        },
        {
          "variable": "dETHP_dt",
          "time": 0.0,
          "expected": -236818.4963313962
        },
        {
          "variable": "dNO_dt",
          "time": 0.0,
          "expected": -25783325.00094299
        },
        {
          "variable": "dNO2_dt",
          "time": 0.0,
          "expected": 20278760.33248312
        }
      ]
    },
    {
      "id": "box_urban_night_tendencies",
      "description": "Instantaneous net production rate of all 59 variable species at the urban night box state (T 283 K, p 101325 Pa, M 2.593e19 and H2O 4.554e17 molec/cm3 (RH 0.900), every photolysis rate zero), against Vdot from radm2_Fun of the standalone WRF-Chem RADM2 KPP box driver (real64, KPP-generated code from chem/KPP/mechanisms/radm2 of WRF v4.8.0 with WRFUserRateLaws; dump dumps/radm2/box_urban_night.json). This is the instantaneous-derivative shape PLAN.md section 6 asks for: each d<SPC>_dt is an observed written D(RADM2.<SPC>, t), which esm-spec section 7.4 resolves to the tendency the reaction system already derives, so asserting it at time 0 evaluates the mechanism right-hand side at the given state and pins the whole stoichiometric matrix and every rate law independently of any integrator. The environment (T, p, M, H2O and the photolysis frequencies) is set through the same scoped parameter_overrides, and the species through the same initial_conditions, as the matching trajectory test of RADM2. Measured agreement with the Fortran (Rust CLI, real64 both sides): 140 of the 236 assertions across the four regimes are BIT-IDENTICAL to KPP, the largest residual anywhere is 9.5e-7 relative (dALD_dt, rural morning) and every other species is within 7.2e-8 (dN2O5_dt, urban noon). That residual is summation-order rounding amplified by cancellation, not a stoichiometric difference: ALD sums 35 terms whose net is 1.1 % of the largest of them, and reconstructing the budget from this document's own stoichiometry times the dump's reaction rates A reproduces the esm value rather than the Fortran one. The tolerance is held at rel 1e-5 rather than tightened to that residual because evaluation ORDER differs between bindings, so a tolerance tuned to one binding's rounding would not hold in the others; every error class this test exists to catch -- a wrong stoichiometric coefficient, a misbound rate law -- moves a tendency by O(1), not by 1e-6.",
      "time_span": {
        "start": 0,
        "end": 1
      },
      "tolerance": {
        "rel": 1e-05
      },
      "initial_conditions": {
        "RADM2.O3": 518573126688.0133,
        "RADM2.H2O2": 25928656334.400665,
        "RADM2.NO": 51857312668.80133,
        "RADM2.NO2": 777859690032.02,
        "RADM2.NO3": 1296432816.7200334,
        "RADM2.N2O5": 25928656334.400665,
        "RADM2.HONO": 25928656334.400665,
        "RADM2.HNO3": 51857312668.80133,
        "RADM2.HNO4": 1296432816.7200334,
        "RADM2.SO2": 129643281672.00333,
        "RADM2.SULF": 2592865633.440067,
        "RADM2.CO": 12964328167200.334,
        "RADM2.ETH": 259286563344.00665,
        "RADM2.HC3": 518573126688.0133,
        "RADM2.HC5": 259286563344.00665,
        "RADM2.HC8": 129643281672.00333,
        "RADM2.OL2": 129643281672.00333,
        "RADM2.OLT": 51857312668.80133,
        "RADM2.OLI": 25928656334.400665,
        "RADM2.ISO": 25928656334.400665,
        "RADM2.TOL": 129643281672.00333,
        "RADM2.XYL": 77785969003.202,
        "RADM2.CSL": 5185731266.880134,
        "RADM2.HCHO": 129643281672.00333,
        "RADM2.ALD": 51857312668.80133,
        "RADM2.ETHP": 25928656.33440067,
        "RADM2.KET": 51857312668.80133,
        "RADM2.GLY": 5185731266.880134,
        "RADM2.MGLY": 7778596900.320199,
        "RADM2.MO2": 12964328.167200334,
        "RADM2.DCB": 2592865633.440067,
        "RADM2.ONIT": 12964328167.200333,
        "RADM2.PAN": 25928656334.400665,
        "RADM2.TPAN": 1296432816.7200334,
        "RADM2.OP1": 12964328167.200333,
        "RADM2.OP2": 7778596900.320199,
        "RADM2.PAA": 2592865633.440067,
        "RADM2.ORA1": 12964328167.200333,
        "RADM2.ORA2": 12964328167.200333,
        "RADM2.OH": 51857.31266880133,
        "RADM2.HO2": 51857312.66880134,
        "RADM2.O3P": 0.0,
        "RADM2.O1D": 0.0,
        "RADM2.HC3P": 25928656.33440067,
        "RADM2.HC5P": 12964328.167200334,
        "RADM2.HC8P": 7778596.900320198,
        "RADM2.OLTP": 7778596.900320198,
        "RADM2.OLIP": 5185731.266880133,
        "RADM2.TOLP": 5185731.266880133,
        "RADM2.XYLP": 5185731.266880133,
        "RADM2.ACO3": 51857312.66880134,
        "RADM2.TCO3": 5185731.266880133,
        "RADM2.KETP": 5185731.266880133,
        "RADM2.OLN": 51857312.66880134,
        "RADM2.XO2": 25928656.33440067,
        "RADM2.XNO2": 2592865.6334400666,
        "RADM2.CH4": 46671581401921.195,
        "RADM2.CO2": 1.0371462533760266e+16,
        "RADM2.OL2P": 7778596.900320198
      },
      "parameter_overrides": {
        "RADM2RateConstants.T": 283.0,
        "RADM2RateConstants.p": 101325.0,
        "RADM2RateConstants.M": 2.5928656334400664e+19,
        "RADM2RateConstants.H2O": 4.5539885211985715e+17,
        "RADM2RateConstants.j_no2": 0.0,
        "RADM2RateConstants.j_o31d": 0.0,
        "RADM2RateConstants.j_o33p": 0.0,
        "RADM2RateConstants.j_hno2": 0.0,
        "RADM2RateConstants.j_hno3": 0.0,
        "RADM2RateConstants.j_hno4": 0.0,
        "RADM2RateConstants.j_no3o2": 0.0,
        "RADM2RateConstants.j_no3o": 0.0,
        "RADM2RateConstants.j_h2o2": 0.0,
        "RADM2RateConstants.j_ch2om": 0.0,
        "RADM2RateConstants.j_ch2or": 0.0,
        "RADM2RateConstants.j_ch3cho": 0.0,
        "RADM2RateConstants.j_ch3o2h": 0.0,
        "RADM2RateConstants.j_ch3coch3": 0.0,
        "RADM2RateConstants.j_ch3coo2h": 0.0,
        "RADM2RateConstants.j_ch3coc2h5": 0.0,
        "RADM2RateConstants.j_hcocho": 0.0,
        "RADM2RateConstants.j_hcochob": 0.0,
        "RADM2RateConstants.j_ch3cocho": 0.0,
        "RADM2RateConstants.j_hcochest": 0.0,
        "RADM2RateConstants.j_ch3ono2": 0.0
      },
      "assertions": [
        {
          "variable": "dSULF_dt",
          "time": 0.0,
          "expected": 6368.822128778376
        },
        {
          "variable": "dORA1_dt",
          "time": 0.0,
          "expected": 204303.1909190173
        },
        {
          "variable": "dORA2_dt",
          "time": 0.0,
          "expected": 583995.8801971587
        },
        {
          "variable": "dCO2_dt",
          "time": 0.0,
          "expected": 164618.20013843512
        },
        {
          "variable": "dSO2_dt",
          "time": 0.0,
          "expected": -6368.822128778376
        },
        {
          "variable": "dETH_dt",
          "time": 0.0,
          "expected": -3072.6765728271725
        },
        {
          "variable": "dO1D_dt",
          "time": 0.0,
          "expected": 0.0
        },
        {
          "variable": "dHC5_dt",
          "time": 0.0,
          "expected": -60741.36127219973
        },
        {
          "variable": "dHC8_dt",
          "time": 0.0,
          "expected": -63901.316482892194
        },
        {
          "variable": "dTOL_dt",
          "time": 0.0,
          "expected": -44047.73377991732
        },
        {
          "variable": "dXYL_dt",
          "time": 0.0,
          "expected": -114865.01585121862
        },
        {
          "variable": "dTPAN_dt",
          "time": 0.0,
          "expected": 18917079.645753674
        },
        {
          "variable": "dHONO_dt",
          "time": 0.0,
          "expected": 14528.538301419434
        },
        {
          "variable": "dH2O2_dt",
          "time": 0.0,
          "expected": 20848.952405170756
        },
        {
          "variable": "dN2O5_dt",
          "time": 0.0,
          "expected": 1045102055.1445019
        },
        {
          "variable": "dHC3_dt",
          "time": 0.0,
          "expected": -63434.86518702115
        },
        {
          "variable": "dCH4_dt",
          "time": 0.0,
          "expected": 157215.61896332423
        },
        {
          "variable": "dPAA_dt",
          "time": 0.0,
          "expected": 19124.71277047882
        },
        {
          "variable": "dO3P_dt",
          "time": 0.0,
          "expected": 0.0
        },
        {
          "variable": "dHNO4_dt",
          "time": 0.0,
          "expected": 46220755.373146206
        },
        {
          "variable": "dOP1_dt",
          "time": 0.0,
          "expected": -1605.6263908011233
        },
        {
          "variable": "dCSL_dt",
          "time": 0.0,
          "expected": -73932691.860984
        },
        {
          "variable": "dPAN_dt",
          "time": 0.0,
          "expected": 213275293.16031116
        },
        {
          "variable": "dOL2_dt",
          "time": 0.0,
          "expected": -146219.67005058716
        },
        {
          "variable": "dHNO3_dt",
          "time": 0.0,
          "expected": 321665987.27580667
        },
        {
          "variable": "dCO_dt",
          "time": 0.0,
          "expected": 2580663.2802475328
        },
        {
          "variable": "dISO_dt",
          "time": 0.0,
          "expected": -19810337.330543768
        },
        {
          "variable": "dOLT_dt",
          "time": 0.0,
          "expected": -1124525.277696071
        },
        {
          "variable": "dOLI_dt",
          "time": 0.0,
          "expected": -36503079.28725638
        },
        {
          "variable": "dDCB_dt",
          "time": 0.0,
          "expected": 3203672.609885295
        },
        {
          "variable": "dGLY_dt",
          "time": 0.0,
          "expected": 2235000.6058505145
        },
        {
          "variable": "dXNO2_dt",
          "time": 0.0,
          "expected": 131902426.78755467
        },
        {
          "variable": "dKET_dt",
          "time": 0.0,
          "expected": 10129648.30180794
        },
        {
          "variable": "dMGLY_dt",
          "time": 0.0,
          "expected": 3667167.7612315766
        },
        {
          "variable": "dTOLP_dt",
          "time": 0.0,
          "expected": -2102569.4516210966
        },
        {
          "variable": "dXYLP_dt",
          "time": 0.0,
          "expected": -2040267.2907165403
        },
        {
          "variable": "dOLTP_dt",
          "time": 0.0,
          "expected": -2973309.251618668
        },
        {
          "variable": "dOLN_dt",
          "time": 0.0,
          "expected": 33648721.30798298
        },
        {
          "variable": "dXO2_dt",
          "time": 0.0,
          "expected": -6336485.803414819
        },
        {
          "variable": "dOL2P_dt",
          "time": 0.0,
          "expected": -3141934.176679582
        },
        {
          "variable": "dHC5P_dt",
          "time": 0.0,
          "expected": -5278339.421428659
        },
        {
          "variable": "dOP2_dt",
          "time": 0.0,
          "expected": 52256.81250916302
        },
        {
          "variable": "dHCHO_dt",
          "time": 0.0,
          "expected": 37125583.58880713
        },
        {
          "variable": "dHC8P_dt",
          "time": 0.0,
          "expected": -3139535.5241679875
        },
        {
          "variable": "dTCO3_dt",
          "time": 0.0,
          "expected": -21034335.16177023
        },
        {
          "variable": "dO3_dt",
          "time": 0.0,
          "expected": -392584967.7819948
        },
        {
          "variable": "dONIT_dt",
          "time": 0.0,
          "expected": 17599220.87109293
        },
        {
          "variable": "dALD_dt",
          "time": 0.0,
          "expected": 51379725.84250195
        },
        {
          "variable": "dOLIP_dt",
          "time": 0.0,
          "expected": -2035495.957855724
        },
        {
          "variable": "dKETP_dt",
          "time": 0.0,
          "expected": -2133285.095882474
        },
        {
          "variable": "dHO2_dt",
          "time": 0.0,
          "expected": -18396126.607018925
        },
        {
          "variable": "dMO2_dt",
          "time": 0.0,
          "expected": 16653413.802215045
        },
        {
          "variable": "dOH_dt",
          "time": 0.0,
          "expected": 21942845.92016215
        },
        {
          "variable": "dNO3_dt",
          "time": 0.0,
          "expected": -3268697794.398154
        },
        {
          "variable": "dACO3_dt",
          "time": 0.0,
          "expected": -234357827.73144573
        },
        {
          "variable": "dHC3P_dt",
          "time": 0.0,
          "expected": -10622000.426694347
        },
        {
          "variable": "dETHP_dt",
          "time": 0.0,
          "expected": -10675915.350192912
        },
        {
          "variable": "dNO_dt",
          "time": 0.0,
          "expected": -2452431431.9260073
        },
        {
          "variable": "dNO2_dt",
          "time": 0.0,
          "expected": 2979583529.7355943
        }
      ]
    },
    {
      "id": "wrfchem_scm_midtrop_tendencies",
      "description": "Instantaneous net production rate of all 59 variable species at a real WRF-Chem state, the mid-troposphere level k = 45 (T = 254.674 K, p = 490.1 hPa, M = 1.3939e19 and H2O = 1.027e16 molec/cm3, RH = 0.156, late-afternoon TUV/Madronich photolysis) of the first chemistry call of an idealized single-column WRF-Chem run: WRF v4.8.0 em_scm_xy ideal case, 1999-10-22 19:00 UTC, 59 levels, chem_opt = 101 (RADM2 KPP), phot_opt = 1 (Madronich TUV), emiss_opt = 0, chem_in_opt = 0 (species from the built-in idealized profiles of chem/module_input_chem_data.F), no dry deposition; ctessum-claude/WRF branch earthsciml-instrumented-chem, commit 2ce0388 (v4.8.0-6-g2ce03882): the species, T, p, M, H2O and photolysis frequencies of that level as the fork's KPP hooks dumped them (esm_dump_radm2_kpp_1.json, var_in), against Vdot from radm2_Fun of the standalone real64 KPP box driver fed that state (dump dumps/radm2/box_wrfchem_k45.json; its RCONST is bit-identical to WRF-Chem's, see wrfchem_scm_midtrop_rate_constants). WRF-Chem does not dump Vdot itself, hence the box driver. This is the one tendency test at cold, low-density conditions (254.7 K, 0.57 of the box regimes' M), where the Troe falloff and the termolecular forms sit far from their box-regime values. This is the instantaneous-derivative shape PLAN.md section 6 asks for: each d<SPC>_dt is an observed written D(RADM2.<SPC>, t), which esm-spec section 7.4 resolves to the tendency the reaction system already derives, so asserting it at time 0 evaluates the mechanism right-hand side at the given state and pins the whole stoichiometric matrix and every rate law independently of any integrator. The environment (T, p, M, H2O and the photolysis frequencies) is set through the same scoped parameter_overrides, and the species through the same initial_conditions, as the matching trajectory test of RADM2. Measured agreement with the Fortran (Rust CLI, real64 both sides): 140 of the 236 assertions across the four regimes are BIT-IDENTICAL to KPP, the largest residual anywhere is 9.5e-7 relative (dALD_dt, rural morning) and every other species is within 7.2e-8 (dN2O5_dt, urban noon). That residual is summation-order rounding amplified by cancellation, not a stoichiometric difference: ALD sums 35 terms whose net is 1.1 % of the largest of them, and reconstructing the budget from this document's own stoichiometry times the dump's reaction rates A reproduces the esm value rather than the Fortran one. The tolerance is held at rel 1e-5 rather than tightened to that residual because evaluation ORDER differs between bindings, so a tolerance tuned to one binding's rounding would not hold in the others; every error class this test exists to catch -- a wrong stoichiometric coefficient, a misbound rate law -- moves a tendency by O(1), not by 1e-6.",
      "time_span": {
        "start": 0,
        "end": 1
      },
      "tolerance": {
        "rel": 1e-05
      },
      "initial_conditions": {
        "RADM2.SULF": 696928722.0572433,
        "RADM2.ORA1": 696928671.3490074,
        "RADM2.ORA2": 836314405.6188089,
        "RADM2.CO2": 427354071.527174,
        "RADM2.SO2": 1393857444.1144867,
        "RADM2.ETH": 8920687804.599072,
        "RADM2.O1D": 0.0,
        "RADM2.HC5": 6007525202.807504,
        "RADM2.HC8": 2578636109.345445,
        "RADM2.TOL": 0.13938573534499446,
        "RADM2.XYL": 0.13938573534499446,
        "RADM2.TPAN": 9589738.761161875,
        "RADM2.HONO": 0.13938573534499446,
        "RADM2.H2O2": 19235232241.980854,
        "RADM2.N2O5": 172577.6695157276,
        "RADM2.HC3": 345676650.3998845,
        "RADM2.CH4": 23695576089109.83,
        "RADM2.PAA": 801798881.3224971,
        "RADM2.O3P": 0.0,
        "RADM2.HNO4": 2245036.8312564474,
        "RADM2.OP1": 21465403178.9659,
        "RADM2.CSL": 0.13938573534499446,
        "RADM2.PAN": 163081312.64524424,
        "RADM2.OL2": 2578636109.345445,
        "RADM2.HNO3": 975700190.5968463,
        "RADM2.CO": 1115085877403.739,
        "RADM2.ISO": 0.0013938574014135715,
        "RADM2.OLT": 1360404815.153169,
        "RADM2.OLI": 680202407.5765845,
        "RADM2.DCB": 0.13938573534499446,
        "RADM2.GLY": 0.13938573534499446,
        "RADM2.XNO2": 0.0,
        "RADM2.KET": 177019878.465989,
        "RADM2.MGLY": 0.13938573534499446,
        "RADM2.TOLP": 0.0,
        "RADM2.XYLP": 0.0,
        "RADM2.OLTP": 0.0,
        "RADM2.OLN": 0.0,
        "RADM2.XO2": 0.0,
        "RADM2.OL2P": 0.0,
        "RADM2.HC5P": 0.0,
        "RADM2.OP2": 10732701589.48295,
        "RADM2.HCHO": 7122611076.965915,
        "RADM2.HC8P": 0.0,
        "RADM2.TCO3": 0.0,
        "RADM2.O3": 418157204026.4021,
        "RADM2.ONIT": 0.13938573534499446,
        "RADM2.ALD": 416763360.1720949,
        "RADM2.OLIP": 0.0,
        "RADM2.KETP": 0.0,
        "RADM2.HO2": 0.0013938574014135715,
        "RADM2.MO2": 0.0,
        "RADM2.OH": 0.0013938574014135715,
        "RADM2.NO3": 1553198.9142220845,
        "RADM2.ACO3": 801798881.3224971,
        "RADM2.HC3P": 0.0,
        "RADM2.ETHP": 0.0,
        "RADM2.NO": 75268294.73090453,
        "RADM2.NO2": 225804890.53124312
      },
      "parameter_overrides": {
        "RADM2RateConstants.T": 254.67430114746094,
        "RADM2RateConstants.p": 49010.94140625,
        "RADM2RateConstants.M": 1.393857377650239e+19,
        "RADM2RateConstants.H2O": 1.0274926497890304e+16,
        "RADM2RateConstants.j_no2": 0.0022306586615741253,
        "RADM2RateConstants.j_o31d": 5.278966455080081e-06,
        "RADM2RateConstants.j_o33p": 9.7237279987894e-05,
        "RADM2RateConstants.j_hno2": 0.0005067039164714515,
        "RADM2RateConstants.j_hno3": 1.553695199163485e-07,
        "RADM2RateConstants.j_hno4": 1.0463734270160785e-06,
        "RADM2RateConstants.j_no3o2": 0.005006307270377874,
        "RADM2RateConstants.j_no3o": 0.04101721942424774,
        "RADM2RateConstants.j_h2o2": 2.0200568542350084e-06,
        "RADM2RateConstants.j_ch2om": 1.266889194084797e-05,
        "RADM2RateConstants.j_ch2or": 7.632468623341992e-06,
        "RADM2RateConstants.j_ch3cho": 1.827575829338457e-06,
        "RADM2RateConstants.j_ch3o2h": 1.3792540585200186e-06,
        "RADM2RateConstants.j_ch3coch3": 2.232719964467833e-07,
        "RADM2RateConstants.j_ch3coo2h": 5.342035933608713e-07,
        "RADM2RateConstants.j_ch3coc2h5": 2.30299747272511e-07,
        "RADM2RateConstants.j_hcocho": 2.4606755687273107e-05,
        "RADM2RateConstants.j_hcochob": 9.255511031369679e-06,
        "RADM2RateConstants.j_ch3cocho": 3.875107358908281e-05,
        "RADM2RateConstants.j_hcochest": 0.00014294766879174858,
        "RADM2RateConstants.j_ch3ono2": 7.263005841195991e-07
      },
      "assertions": [
        {
          "variable": "dSULF_dt",
          "time": 0.0,
          "expected": 1.6999038546965743e-06
        },
        {
          "variable": "dORA1_dt",
          "time": 0.0,
          "expected": 1991.4230907823535
        },
        {
          "variable": "dORA2_dt",
          "time": 0.0,
          "expected": 7334.815759634299
        },
        {
          "variable": "dCO2_dt",
          "time": 0.0,
          "expected": 0.000312399508777788
        },
        {
          "variable": "dSO2_dt",
          "time": 0.0,
          "expected": -1.6999038546965743e-06
        },
        {
          "variable": "dETH_dt",
          "time": 0.0,
          "expected": -1.9326672871475304e-06
        },
        {
          "variable": "dO1D_dt",
          "time": 0.0,
          "expected": 2207437.853005454
        },
        {
          "variable": "dHC5_dt",
          "time": 0.0,
          "expected": -3.257980219442352e-05
        },
        {
          "variable": "dHC8_dt",
          "time": 0.0,
          "expected": -2.942376085959089e-05
        },
        {
          "variable": "dTOL_dt",
          "time": 0.0,
          "expected": -1.4446430182076757e-15
        },
        {
          "variable": "dXYL_dt",
          "time": 0.0,
          "expected": -5.790453118635042e-15
        },
        {
          "variable": "dTPAN_dt",
          "time": 0.0,
          "expected": -1.5033107969022774
        },
        {
          "variable": "dHONO_dt",
          "time": 0.0,
          "expected": -7.01365890678881e-05
        },
        {
          "variable": "dH2O2_dt",
          "time": 0.0,
          "expected": -38856.262773558905
        },
        {
          "variable": "dN2O5_dt",
          "time": 0.0,
          "expected": 457.9190187550021
        },
        {
          "variable": "dHC3_dt",
          "time": 0.0,
          "expected": -9.192357699732517e-07
        },
        {
          "variable": "dCH4_dt",
          "time": 0.0,
          "expected": 2272.325568722634
        },
        {
          "variable": "dPAA_dt",
          "time": 0.0,
          "expected": -428.32384055178755
        },
        {
          "variable": "dO3P_dt",
          "time": 0.0,
          "expected": 41227870.66243364
        },
        {
          "variable": "dHNO4_dt",
          "time": 0.0,
          "expected": -415.5980327561902
        },
        {
          "variable": "dOP1_dt",
          "time": 0.0,
          "expected": -29606.24475155434
        },
        {
          "variable": "dCSL_dt",
          "time": 0.0,
          "expected": -2.38143150718063e-06
        },
        {
          "variable": "dPAN_dt",
          "time": 0.0,
          "expected": 1031820.6636447628
        },
        {
          "variable": "dOL2_dt",
          "time": 0.0,
          "expected": -418.75374016297815
        },
        {
          "variable": "dHNO3_dt",
          "time": 0.0,
          "expected": -137.47572239623247
        },
        {
          "variable": "dCO_dt",
          "time": 0.0,
          "expected": 151686.57780302176
        },
        {
          "variable": "dISO_dt",
          "time": 0.0,
          "expected": -3.9045419077075734e-09
        },
        {
          "variable": "dOLT_dt",
          "time": 0.0,
          "expected": -1944.0928638427504
        },
        {
          "variable": "dOLI_dt",
          "time": 0.0,
          "expected": -24702.27009869543
        },
        {
          "variable": "dDCB_dt",
          "time": 0.0,
          "expected": -1.9925040323353953e-05
        },
        {
          "variable": "dGLY_dt",
          "time": 0.0,
          "expected": -4.719957137799759e-06
        },
        {
          "variable": "dXNO2_dt",
          "time": 0.0,
          "expected": 4.762863001509629e-06
        },
        {
          "variable": "dKET_dt",
          "time": 0.0,
          "expected": 2355.2589763046444
        },
        {
          "variable": "dMGLY_dt",
          "time": 0.0,
          "expected": -5.401521278448541e-06
        },
        {
          "variable": "dTOLP_dt",
          "time": 0.0,
          "expected": 1.0834822636557568e-15
        },
        {
          "variable": "dXYLP_dt",
          "time": 0.0,
          "expected": 4.8060759918284724e-15
        },
        {
          "variable": "dOLTP_dt",
          "time": 0.0,
          "expected": 7.299047069087921e-05
        },
        {
          "variable": "dOLN_dt",
          "time": 0.0,
          "expected": 754.4856147053915
        },
        {
          "variable": "dXO2_dt",
          "time": 0.0,
          "expected": 3.0230436985992663e-05
        },
        {
          "variable": "dOL2P_dt",
          "time": 0.0,
          "expected": 3.8808117544794846e-05
        },
        {
          "variable": "dHC5P_dt",
          "time": 0.0,
          "expected": 3.257980219442352e-05
        },
        {
          "variable": "dOP2_dt",
          "time": 0.0,
          "expected": -2396.311860749978
        },
        {
          "variable": "dHCHO_dt",
          "time": 0.0,
          "expected": -109239.18804431034
        },
        {
          "variable": "dHC8P_dt",
          "time": 0.0,
          "expected": 2.942376085959089e-05
        },
        {
          "variable": "dTCO3_dt",
          "time": 0.0,
          "expected": 1.503330721942608
        },
        {
          "variable": "dO3_dt",
          "time": 0.0,
          "expected": -43152909.41660793
        },
        {
          "variable": "dONIT_dt",
          "time": 0.0,
          "expected": -1.0123594136034411e-07
        },
        {
          "variable": "dALD_dt",
          "time": 0.0,
          "expected": 19851.362954177108
        },
        {
          "variable": "dOLIP_dt",
          "time": 0.0,
          "expected": 8.758838740798578e-05
        },
        {
          "variable": "dKETP_dt",
          "time": 0.0,
          "expected": 1.588465627168962e-07
        },
        {
          "variable": "dHO2_dt",
          "time": 0.0,
          "expected": 148631.4629505015
        },
        {
          "variable": "dMO2_dt",
          "time": 0.0,
          "expected": 4152658.3789215423
        },
        {
          "variable": "dOH_dt",
          "time": 0.0,
          "expected": 113843.42740248427
        },
        {
          "variable": "dNO3_dt",
          "time": 0.0,
          "expected": -75564.28032075884
        },
        {
          "variable": "dACO3_dt",
          "time": 0.0,
          "expected": -5175395.107554172
        },
        {
          "variable": "dHC3P_dt",
          "time": 0.0,
          "expected": 7.55622434124178e-05
        },
        {
          "variable": "dETHP_dt",
          "time": 0.0,
          "expected": 40.76763520559517
        },
        {
          "variable": "dNO_dt",
          "time": 0.0,
          "expected": -263984.1567247306
        },
        {
          "variable": "dNO2_dt",
          "time": 0.0,
          "expected": -693387.973115372
        }
      ]
    }
  ]
}
```

</details>
