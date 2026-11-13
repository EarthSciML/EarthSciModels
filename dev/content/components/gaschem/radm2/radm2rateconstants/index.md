---
title: "RADM2RateConstants"
slug: "radm2rateconstants"
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

- Stockwell, W. R., P. Middleton, J. S. Chang, and X. Tang (1990). The second generation regional acid deposition model chemical mechanism for regional air quality modeling. J. Geophys. Res. 95, 16343-16367.
- Grell, G. A., et al. (2005). Fully coupled online chemistry within the WRF model. Atmos. Environ. 39, 6957-6975.
- Damian, V., A. Sandu, M. Damian, F. Potra, and G. R. Carmichael (2002). The kinetic preprocessor KPP - a software environment for solving chemical kinetics. Comput. Chem. Eng. 26, 1567-1579.

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `T` | `K` | `298.0` | Air temperature (KPP TEMP). |
| `T_ref` | `K` | `300.0` | Reference temperature of the (T/300)^n forms (WRF literal 300). |
| `p` | `Pa` | `101325.0` | Air pressure (WRF p_phy), used only to derive RH for the heterogeneous N2O5 rate. |
| `M` | `molec/cm^3` | `2.4623522626293244e+19` | Air number density, the KPP fixed species M (C_M = FIX(indf_M) = dens2con_a rho_phy, chem_driver.F). This is the single source of M for the whole document: the Troe, termolecular and CO + OH forms read it as a rate-law argument, and the reactions in which KPP multiplies by FIX(indf_M) (R022, R024, R036) multiply their rate by it. RADM2 therefore carries no M species to fall out of step with it. |
| `H2O` | `molec/cm^3` | `6.9628642030342e+17` | Water vapour number density, the KPP fixed species H2O (FIX(indf_H2O) = dens2con_w qv rho_phy). The single source of water vapour for the whole document: R025 and R033 multiply their rate by it, as KPP multiplies by FIX(indf_H2O), and RH -- hence the heterogeneous N2O5 rate -- is derived from it, so the two humidity paths cannot disagree. |
| `j_no2` | `1/s` | `0.0085` | Photolysis frequency ph_no2 (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_no2)). |
| `j_o31d` | `1/s` | `3.2e-05` | Photolysis frequency ph_o31d (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_o31d)). |
| `j_o33p` | `1/s` | `0.00042` | Photolysis frequency ph_o33p (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_o33p)). |
| `j_hno2` | `1/s` | `0.0017` | Photolysis frequency ph_hno2 (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_hno2)). |
| `j_hno3` | `1/s` | `6.5e-07` | Photolysis frequency ph_hno3 (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_hno3)). |
| `j_hno4` | `1/s` | `4.2e-06` | Photolysis frequency ph_hno4 (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_hno4)). |
| `j_no3o2` | `1/s` | `0.023` | Photolysis frequency ph_no3o2 (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_no3o2)). |
| `j_no3o` | `1/s` | `0.185` | Photolysis frequency ph_no3o (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_no3o)). |
| `j_h2o2` | `1/s` | `7.3e-06` | Photolysis frequency ph_h2o2 (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_h2o2)). |
| `j_ch2om` | `1/s` | `4.6e-05` | Photolysis frequency ph_ch2om (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_ch2om)). |
| `j_ch2or` | `1/s` | `3.1e-05` | Photolysis frequency ph_ch2or (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_ch2or)). |
| `j_ch3cho` | `1/s` | `5.5e-06` | Photolysis frequency ph_ch3cho (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_ch3cho)). |
| `j_ch3o2h` | `1/s` | `5.4e-06` | Photolysis frequency ph_ch3o2h (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_ch3o2h)). |
| `j_ch3coch3` | `1/s` | `6.8e-07` | Photolysis frequency ph_ch3coch3 (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_ch3coch3)). |
| `j_ch3coo2h` | `1/s` | `3.2e-06` | Photolysis frequency ph_ch3coo2h (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_ch3coo2h)). |
| `j_ch3coc2h5` | `1/s` | `1.6e-06` | Photolysis frequency ph_ch3coc2h5 (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_ch3coc2h5)). |
| `j_hcocho` | `1/s` | `0.00011` | Photolysis frequency ph_hcocho (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_hcocho)). |
| `j_hcochob` | `1/s` | `2.1e-05` | Photolysis frequency ph_hcochob (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_hcochob)). |
| `j_ch3cocho` | `1/s` | `0.00016` | Photolysis frequency ph_ch3cocho (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_ch3cocho)). |
| `j_hcochest` | `1/s` | `0.00022` | Photolysis frequency ph_hcochest (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_hcochest)). |
| `j_ch3ono2` | `1/s` | `1.1e-06` | Photolysis frequency ph_ch3ono2 (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_ch3ono2)). |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `qv` | `kg/kg` |  | Water-vapour mass mixing ratio implied by H2O and M (WRF moist(P_QV)), the input of the WRF relative humidity. |
| `es` | `Pa` |  | Saturation vapour pressure over water at T, the WRF Bolton-type form of kpp_mechd_ibu_radm2.inc. |
| `RH` | `1` |  | Relative humidity in [0, 1] for the heterogeneous N2O5 rate, derived from qv, es and p with the formula and the clip of kpp_mechd_ibu_radm2.inc. Derived, not an input, because WRF itself derives it from the same water vapour that FIX(indf_H2O) carries. |
| `k_R022` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 22 {22:001} O3P+M=O3 (radm2.eqn: .20946e0*(C_M *6.00D-34*(TEMP/300.0)**(-2.3))). |
| `k_R023` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 23 {23:002} O3P+NO2=NO (radm2.eqn: ARR2(6.5D-12, -120.0_dp, TEMP)). |
| `k_R024` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 24 {24:003} O1D+M=O3P (radm2.eqn: .78084* ARR2(1.8D-11, -110.0_dp, TEMP) + .20946e0* ARR2(3.2D-11, -70.0_dp, TEMP)). |
| `k_R025` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 25 {26:005} O1D+H2O=OH+OH (radm2.eqn: 2.2D-10). |
| `k_R026` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 26 {27:006} O3+NO=NO2 (radm2.eqn: ARR2(2.0D-12, 1400.0_dp, TEMP)). |
| `k_R027` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 27 {28:007} O3+OH=HO2 (radm2.eqn: ARR2(1.6D-12, 940.0_dp, TEMP)). |
| `k_R028` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 28 {29:008} O3+HO2=OH (radm2.eqn: ARR2(1.1D-14, 500.0_dp, TEMP)). |
| `k_R029` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 29 {30:009} HO2+NO=NO2+OH (radm2.eqn: ARR2(3.7D-12, -240.0_dp, TEMP)). |
| `k_R030` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 30 {31:010} HO2+NO2=HNO4 (radm2.eqn: TROE( 1.80D-31 , 3.2_dp , 4.70D-12 , 1.4_dp , TEMP, C_M)). |
| `k_R031` | `1/s` |  | Rate coefficient of RADM2 reaction 31 {32:011} HNO4=HO2+NO2 (radm2.eqn: TROEE( 4.76D26,10900.0_dp, 1.80D-31 , 3.2_dp , 4.70D-12 , 1.4_dp , TEMP, C_M )). |
| `k_R032` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 32 {33:012} HO2+HO2=H2O2 (radm2.eqn: (2.2D-13*EXP(600./TEMP) + 1.9D-33* C_M *EXP(980._dp/TEMP))). |
| `k_R033` | `cm^6/molec^2/s` |  | Rate coefficient of RADM2 reaction 33 {34:013} HO2+HO2+H2O=H2O2 (radm2.eqn: (3.08D-34* EXP(2800._dp/TEMP)+ 2.66D-54* C_M *EXP(3180._dp/TEMP))). |
| `k_R034` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 34 {35:014} H2O2+OH=HO2+H2O (radm2.eqn: ARR2(3.3D-12, 200.0_dp, TEMP)). |
| `k_R035` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 35 {36:015} NO+OH=HONO (radm2.eqn: TROE( 7.00D-31 , 2.6_dp , 1.50D-11 , 0.5_dp , TEMP, C_M)). |
| `k_R036` | `cm^6/molec^2/s` |  | Rate coefficient of RADM2 reaction 36 {37:016} NO+NO+M=NO2+NO2 (radm2.eqn: .20946e0* ARR2(3.3D-39, -530.0_dp, TEMP)). |
| `k_R037` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 37 {38:017} O3+NO2=NO3 (radm2.eqn: ARR2(1.4D-13, 2500.0_dp, TEMP)). |
| `k_R038` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 38 {39:018} NO3+NO=NO2+NO2 (radm2.eqn: ARR2(1.7D-11, -150.0_dp, TEMP)). |
| `k_R039` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 39 {40:019} NO3+NO2=NO+NO2 (radm2.eqn: ARR2(2.5D-14, 1230.0_dp, TEMP)). |
| `k_R040` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 40 {41:020} NO3+HO2=HNO3 (radm2.eqn: 2.5D-12). |
| `k_R041` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 41 {42:021} NO3+NO2=N2O5 (radm2.eqn: TROE( 2.20D-30 , 4.3_dp , 1.50D-12 , 0.5_dp , TEMP, C_M)). |
| `k_R042` | `1/s` |  | Rate coefficient of RADM2 reaction 42 {43:022} N2O5=NO2+NO3 (radm2.eqn: TROEE(9.09D26,11200.0_dp, 2.20D-30 , 4.3_dp , 1.50D-12 , 0.5_dp , TEMP, C_M )). |
| `k_R043` | `1/s` |  | Rate coefficient of RADM2 reaction 43 {44:137, 14} N2O5=2.00 HNO3 (radm2.eqn: rc_n2o5). |
| `k_R044` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 44 {45:024} OH+NO2=HNO3 (radm2.eqn: TROE( 2.60D-30 , 3.2_dp , 2.40D-11 , 1.3_dp , TEMP, C_M)). |
| `k_R045` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 45 {46:025} OH+HNO3=NO3+H2O (radm2.eqn: k46(TEMP,C_M)). |
| `k_R046` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 46 {47:026} OH+HNO4=NO2+H2O (radm2.eqn: ARR2(1.3D-12, -380.0_dp, TEMP)). |
| `k_R047` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 47 {48:027} OH+HO2=H2O (radm2.eqn: ARR2(4.6D-11, -230.0_dp, TEMP)). |
| `k_R048` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 48 {49:028} OH+SO2=SULF+HO2 (radm2.eqn: TROE( 3.00D-31 , 3.3_dp , 1.50D-12 , 0.0_dp , TEMP, C_M)). |
| `k_R049` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 49 {50:029} CO+OH=HO2+CO2 (radm2.eqn: (1.5D-13 * (1._dp + 2.439D-20*C_M))). |
| `k_R050` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 50 {51:030} CH4+OH=MO2+H2O (radm2.eqn: THERMAL_T2(6.95D-18, 1280.0_dp, TEMP)). |
| `k_R051` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 51 {52:031} ETH+OH=ETHP+H2O (radm2.eqn: THERMAL_T2(1.37D-17, 444.0_dp, TEMP)). |
| `k_R052` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 52 {53:032} HC3+OH=0.83 HC3P+0.17 HO2 +0.009 HCHO+0.075 ALD +0.025 KET+H2O (radm2.eqn: ARR2(1.59D-11, 540.0_dp, TEMP)). |
| `k_R053` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 53 {54:033} HC5+OH=HC5P+0.25 XO2+H2O (radm2.eqn: ARR2(1.73D-11, 380.0_dp, TEMP)). |
| `k_R054` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 54 {55:034} HC8+OH=HC8P+0.75 XO2+H2O (radm2.eqn: ARR2(3.64D-11, 380.0_dp, TEMP)). |
| `k_R055` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 55 {56:035} OL2+OH=OL2P (radm2.eqn: ARR2(2.15D-12, -411.0_dp, TEMP)). |
| `k_R056` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 56 {57:036} OLT+OH=OLTP (radm2.eqn: ARR2(5.32D-12, -504.0_dp, TEMP)). |
| `k_R057` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 57 {58:037} OLI+OH=OLIP (radm2.eqn: ARR2(1.07D-11, -549.0_dp, TEMP)). |
| `k_R058` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 58 {59:038} TOL+OH=0.75 TOLP+0.25 CSL +0.25 HO2 (radm2.eqn: ARR2(2.1D-12, -322.0_dp, TEMP)). |
| `k_R059` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 59 {60:039} XYL+OH=0.83 XYLP+0.17 CSL +0.17 HO2 (radm2.eqn: ARR2(1.89D-11, -116.0_dp, TEMP)). |
| `k_R060` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 60 {61:040} CSL+OH=0.10 HO2+0.90 XO2 +0.90 TCO3-0.90 OH (radm2.eqn: 4.0D-11). |
| `k_R061` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 61 {62:041} HCHO+OH=HO2+CO+H2O (radm2.eqn: 9.0D-12). |
| `k_R062` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 62 {63:042} ALD+OH=ACO3+H2O (radm2.eqn: ARR2(6.87D-12, -256.0_dp, TEMP)). |
| `k_R063` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 63 {64:043} KET+OH=KETP+H2O (radm2.eqn: ARR2(1.2D-11, 745.0_dp, TEMP)). |
| `k_R064` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 64 {65:044} GLY+OH=HO2+2.00 CO+H2O (radm2.eqn: 1.15D-11). |
| `k_R065` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 65 {66:045} MGLY+OH=ACO3+CO+H2O (radm2.eqn: 1.7D-11). |
| `k_R066` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 66 {67:046} DCB+OH=TCO3+H2O (radm2.eqn: 2.8D-11). |
| `k_R067` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 67 {68:047} OP1+OH=0.50 MO2+0.50 HCHO +0.50 OH (radm2.eqn: 1.0D-11). |
| `k_R068` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 68 {69:048} OP2+OH=0.50 HC3P+0.50 ALD +0.50 OH (radm2.eqn: 1.0D-11). |
| `k_R069` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 69 {70:049} PAA+OH=ACO3+H2O (radm2.eqn: 1.0D-11). |
| `k_R070` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 70 {71:050} PAN+OH=HCHO+NO3+XO2 (radm2.eqn: THERMAL_T2(6.85D-18, 444.0_dp, TEMP)). |
| `k_R071` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 71 {72:051} ONIT+OH=HC3P+NO2 (radm2.eqn: ARR2(1.55D-11, 540.0_dp, TEMP)). |
| `k_R072` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 72 {73:052} ISO+OH=OLTP (radm2.eqn: ARR2(2.55D-11, -409.0_dp, TEMP)). |
| `k_R073` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 73 {74:053} ACO3+NO2=PAN (radm2.eqn: ARR2(2.8D-12, -181.0_dp, TEMP)). |
| `k_R074` | `1/s` |  | Rate coefficient of RADM2 reaction 74 {75:054} PAN=ACO3+NO2 (radm2.eqn: ARR2(1.95D+16, 13543.0_dp, TEMP)). |
| `k_R075` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 75 {76:055} TCO3+NO2=TPAN (radm2.eqn: 4.7D-12). |
| `k_R076` | `1/s` |  | Rate coefficient of RADM2 reaction 76 {77:056} TPAN=TCO3+NO2 (radm2.eqn: ARR2(1.95D+16, 13543.0_dp, TEMP)). |
| `k_R077` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 77 {78:057} MO2+NO=HCHO+HO2+NO2 (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP)). |
| `k_R078` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 78 {79:058} HC3P+NO=0.75 ALD+0.25 KET +0.09 HCHO+0.036 ONIT +0.964 NO2+0.964 HO2 (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP)). |
| `k_R079` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 79 {80:060} HC5P+NO=0.38 ALD+0.69 KET +0.08 ONIT+0.92 NO2 +0.92 HO2 (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP)). |
| `k_R080` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 80 {81:062} HC8P+NO=0.35 ALD+1.06 KET +0.04 HCHO+0.24 ONIT +0.76 NO2+0.76 HO2 (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP)). |
| `k_R081` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 81 {82:064} OL2P+NO=1.60 HCHO+HO2+NO2 +0.20 ALD (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP)). |
| `k_R082` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 82 {83:065} OLTP+NO=ALD+HCHO+HO2+NO2 (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP)). |
| `k_R083` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 83 {84:066} OLIP+NO=HO2+1.45 ALD +0.28 HCHO+0.10 KET+NO2 (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP)). |
| `k_R084` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 84 {85:067} ACO3+NO=MO2+NO2 (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP)). |
| `k_R085` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 85 {86:068} TCO3+NO=NO2+0.92 HO2 +0.89 GLY+0.11 MGLY +0.05 ACO3+0.95 CO +2.00 XO2 (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP)). |
| `k_R086` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 86 {87:069} TOLP+NO=NO2+HO2+0.17 MGLY +0.16 GLY+0.70 DCB (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP)). |
| `k_R087` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 87 {88:070} XYLP+NO=NO2+HO2+0.45 MGLY +0.806 DCB (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP)). |
| `k_R088` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 88 {89:071} ETHP+NO=ALD+HO2+NO2 (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP)). |
| `k_R089` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 89 {90:072} KETP+NO=MGLY+NO2+HO2 (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP)). |
| `k_R090` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 90 {91:073} OLN+NO=HCHO+ALD+2.00 NO2 (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP)). |
| `k_R091` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 91 {92:074} HCHO+NO3=HO2+HNO3+CO (radm2.eqn: ARR2(6.0D-13, 2058.0_dp, TEMP)). |
| `k_R092` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 92 {93:075} ALD+NO3=ACO3+HNO3 (radm2.eqn: ARR2(1.4D-12, 1900.0_dp, TEMP)). |
| `k_R093` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 93 {94:076} GLY+NO3=HNO3+HO2+2.00 CO (radm2.eqn: ARR2(6.0D-13, 2058.0_dp, TEMP)). |
| `k_R094` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 94 {95:077} MGLY+NO3=HNO3+ACO3+CO (radm2.eqn: ARR2(1.4D-12, 1900.0_dp, TEMP)). |
| `k_R095` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 95 {96:078} DCB+NO3=HNO3+TCO3 (radm2.eqn: ARR2(1.4D-12, 1900.0_dp, TEMP)). |
| `k_R096` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 96 {97:079} CSL+NO3=HNO3+XNO2+0.50 CSL (radm2.eqn: 2.2D-11). |
| `k_R097` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 97 {98:080} OL2+NO3=OLN (radm2.eqn: ARR2(2.0D-12, 2923.0_dp, TEMP)). |
| `k_R098` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 98 {99:081} OLT+NO3=OLN (radm2.eqn: ARR2(1.0D-11, 1895.0_dp, TEMP)). |
| `k_R099` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 99 {100:082} OLI+NO3=OLN (radm2.eqn: ARR2(3.23D-11, 975.0_dp, TEMP)). |
| `k_R100` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 100 {101:083} ISO+NO3=OLN (radm2.eqn: 5.81D-13). |
| `k_R101` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 101 {102:084} OL2+O3=HCHO+0.42 CO+0.40 ORA1 +0.12 HO2 (radm2.eqn: ARR2(1.2D-14, 2633.0_dp, TEMP)). |
| `k_R102` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 102 {103:085} OLT+O3=0.53 HCHO+0.50 ALD +0.33 CO+0.20 ORA1 +0.20 ORA2+0.23 HO2 +0.22 MO2+0.10 OH +0.06 CH4 (radm2.eqn: ARR2(1.32D-14, 2105.0_dp, TEMP)). |
| `k_R103` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 103 {104:086} OLI+O3=0.18 HCHO+0.72 ALD +0.10 KET+0.23 CO +0.06 ORA1+0.29 ORA2 +0.09 CH4+0.26 HO2 +0.31 MO2+0.14 OH (radm2.eqn: ARR2(7.29D-15, 1136.0_dp, TEMP)). |
| `k_R104` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 104 {105:087} ISO+O3=0.53 HCHO+0.50 ALD +0.33 CO+0.20 ORA1 +0.20 ORA2+0.23 HO2 +0.22 MO2+0.10 OH (radm2.eqn: ARR2(1.23D-14, 2013.0_dp, TEMP)). |
| `k_R105` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 105 {106:088} HO2+MO2=OP1 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP)). |
| `k_R106` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 106 {107:089} HO2+ETHP=OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP)). |
| `k_R107` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 107 {108:090} HO2+HC3P=OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP)). |
| `k_R108` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 108 {109:091} HO2+HC5P=OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP)). |
| `k_R109` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 109 {110:092} HO2+HC8P=OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP)). |
| `k_R110` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 110 {111:093} HO2+OL2P=OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP)). |
| `k_R111` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 111 {112:094} HO2+OLTP=OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP)). |
| `k_R112` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 112 {113:095} HO2+OLIP=OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP)). |
| `k_R113` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 113 {114:096} HO2+KETP=OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP)). |
| `k_R114` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 114 {115:097} HO2+ACO3=PAA (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP)). |
| `k_R115` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 115 {116:098} HO2+TOLP= OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP)). |
| `k_R116` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 116 {117:099} HO2+XYLP=OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP)). |
| `k_R117` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 117 {118:100} HO2+TCO3=OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP)). |
| `k_R118` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 118 {119:101} HO2+OLN=ONIT (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP)). |
| `k_R119` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 119 {120:102} MO2+MO2=1.50 HCHO+HO2 (radm2.eqn: ARR2(1.9D-13, -220.0_dp, TEMP)). |
| `k_R120` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 120 {121:103} MO2+ETHP=0.75 HCHO+HO2 +0.75 ALD (radm2.eqn: ARR2(1.4D-13, -220.0_dp, TEMP)). |
| `k_R121` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 121 {122:104} MO2+HC3P=0.75 HCHO+HO2 +0.15 ALD+0.6 KET (radm2.eqn: ARR2(4.2D-14, -220.0_dp, TEMP)). |
| `k_R122` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 122 {123:105} MO2+HC5P=0.77 HCHO+HO2 +0.41 ALD+0.75 KET (radm2.eqn: ARR2(3.4D-14, -220.0_dp, TEMP)). |
| `k_R123` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 123 {124:106} MO2+HC8P=0.80 HCHO+HO2 +0.46 ALD+1.39 KET (radm2.eqn: ARR2(2.9D-14, -220.0_dp, TEMP)). |
| `k_R124` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 124 {125:107} MO2+OL2P=1.55 HCHO+HO2 +0.35 ALD (radm2.eqn: ARR2(1.4D-13, -220.0_dp, TEMP)). |
| `k_R125` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 125 {126:108} MO2+OLTP=1.25 HCHO+HO2 +0.75 ALD (radm2.eqn: ARR2(1.4D-13, -220.0_dp, TEMP)). |
| `k_R126` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 126 {127:109} MO2+OLIP=0.89 HCHO+HO2 +0.725 ALD+0.55 KET (radm2.eqn: ARR2(1.7D-14, -220.0_dp, TEMP)). |
| `k_R127` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 127 {128:110} MO2+KETP=0.75 HCHO+HO2 +0.75 MGLY (radm2.eqn: ARR2(1.7D-14, -220.0_dp, TEMP)). |
| `k_R128` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 128 {129:111} MO2+ACO3=HCHO+0.50 HO2 +0.50 MO2+0.50 ORA2 (radm2.eqn: ARR2(9.6D-13, -220.0_dp, TEMP)). |
| `k_R129` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 129 {130:112} MO2+TOLP=HCHO+2.00 HO2 +0.17 MGLY+0.16 GLY +0.70 DCB (radm2.eqn: ARR2(1.7D-14, -220.0_dp, TEMP)). |
| `k_R130` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 130 {131:113} MO2+XYLP=HCHO+2.00 HO2 +0.45 MGLY+0.806 DCB (radm2.eqn: ARR2(1.7D-14, -220.0_dp, TEMP)). |
| `k_R131` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 131 {132:114} MO2+TCO3=0.50 HCHO+0.50 ORA2 +0.445 GLY+0.055 MGLY +0.025 ACO3+0.475 CO +0.46 HO2+XO2 (radm2.eqn: ARR2(9.6D-13, -220.0_dp, TEMP)). |
| `k_R132` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 132 {133:115} ETHP+ACO3=ALD+0.50 HO2 +0.50 MO2+0.50 ORA2 (radm2.eqn: ARR2(3.4D-13, -220.0_dp, TEMP)). |
| `k_R133` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 133 {134:116} HC3P+ACO3=0.2 ALD+0.8 KET +0.50 HO2+0.50 ORA2 +0.50 MO2 (radm2.eqn: ARR2(1.0D-13, -220.0_dp, TEMP)). |
| `k_R134` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 134 {135:117} HC5P+ACO3=0.14 ALD+0.86 KET +0.50 HO2+0.50 ORA2 +0.50 MO2 (radm2.eqn: ARR2(8.4D-14, -220.0_dp, TEMP)). |
| `k_R135` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 135 {136:118} HC8P+ACO3=0.1 ALD+0.9 KET +0.50 HO2+0.50 ORA2 +0.50 MO2 (radm2.eqn: ARR2(7.2D-14, -220.0_dp, TEMP)). |
| `k_R136` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 136 {137:119} OL2P+ACO3=0.80 HCHO+0.60 ALD +0.50 HO2+0.50 ORA2 +0.50 MO2 (radm2.eqn: ARR2(3.4D-13, -220.0_dp, TEMP)). |
| `k_R137` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 137 {138:120} OLTP+ACO3=ALD+0.50 HCHO +0.50 HO2+0.50 ORA2 +0.50 MO2 (radm2.eqn: ARR2(3.4D-13, -220.0_dp, TEMP)). |
| `k_R138` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 138 {139:121} OLIP+ACO3=0.725 ALD+0.55 KET +0.14 HCHO+0.50 HO2 +0.50 MO2+0.50 ORA2 (radm2.eqn: ARR2(4.2D-14, -220.0_dp, TEMP)). |
| `k_R139` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 139 {140:122} KETP+ACO3=MGLY+0.50 HO2 +0.50 ORA2+0.50 MO2 (radm2.eqn: ARR2(4.2D-14, -220.0_dp, TEMP)). |
| `k_R140` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 140 {141:123} ACO3+ACO3=2.00 MO2 (radm2.eqn: ARR2(1.19D-12, -220.0_dp, TEMP)). |
| `k_R141` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 141 {142:124} ACO3+TOLP=0.8 MGLY+0.2 GLY +1.00 DCB+HO2+MO2 (radm2.eqn: ARR2(4.2D-14, -220.0_dp, TEMP)). |
| `k_R142` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 142 {143:125} ACO3+XYLP=MO2+1.00 MGLY +1.00 DCB+HO2 (radm2.eqn: ARR2(4.2D-14, -220.0_dp, TEMP)). |
| `k_R143` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 143 {144:126} ACO3+TCO3=MO2+0.92 HO2 +0.89 GLY+0.11 MGLY +0.05 ACO3+0.95 CO +2.00 XO2 (radm2.eqn: ARR2(1.19D-12, -220.0_dp, TEMP)). |
| `k_R144` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 144 {145:127} XO2+HO2=OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP)). |
| `k_R145` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 145 {146:128} XO2+MO2=HCHO+HO2 (radm2.eqn: ARR2(1.7D-14, -220.0_dp, TEMP)). |
| `k_R146` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 146 {147:129} XO2+ACO3=MO2 (radm2.eqn: ARR2(4.2D-14, -220.0_dp, TEMP)). |
| `k_R147` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 147 {148:130} XO2+XO2=H2O (radm2.eqn: ARR2(3.6D-16, -220.0_dp, TEMP)). |
| `k_R148` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 148 {149:131} XO2+NO=NO2 (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP)). |
| `k_R149` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 149 {150:132} XNO2+NO2=ONIT (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP)). |
| `k_R150` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 150 {151:133} XNO2+HO2=OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP)). |
| `k_R151` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 151 {152:134} XNO2+MO2=HCHO+HO2 (radm2.eqn: ARR2(1.7D-14, -220.0_dp, TEMP)). |
| `k_R152` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 152 {153:135} XNO2+ACO3=MO2 (radm2.eqn: ARR2(4.2D-14, -220.0_dp, TEMP)). |
| `k_R153` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 153 {154:136} XNO2+XNO2=H2O (radm2.eqn: ARR2(3.6D-16, -220.0_dp, TEMP)). |
| `k_R154` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 154 {155:138} MO2+OLN=1.75 HCHO+.5 HO2 +ALD+NO2 (radm2.eqn: ARR2(1.7D-14, -220.0_dp, TEMP)). |
| `k_R155` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 155 {156:139} ACO3+OLN=HCHO+ALD+0.50 ORA2 +NO2+0.50 MO2 (radm2.eqn: ARR2(4.2D-14, -220.0_dp, TEMP)). |
| `k_R156` | `cm^3/molec/s` |  | Rate coefficient of RADM2 reaction 156 {157:140} OLN+OLN=2.00 HCHO+2.00 ALD +2.00 NO2 (radm2.eqn: ARR2(3.6D-16, -220.0_dp, TEMP)). |

## Observed expressions

$$
qv = \mathrm{wrf_kpp_qv}\left(H2O=H2O, M=M, mw_{h2o}=18.015199661254883, mw_{air}=28.969999313354492\right)
$$
_Water-vapour mass mixing ratio implied by H2O and M (WRF moist(P_QV)), the input of the WRF relative humidity._

$$
es = \mathrm{wrf_es}\left(T=T, es0=611.199951171875, a=17.670000076293945, T0=273.1499938964844, T1=29.649999618530273\right)
$$
_Saturation vapour pressure over water at T, the WRF Bolton-type form of kpp_mechd_ibu_radm2.inc._

$$
RH = \mathrm{wrf_rh}\left(qv=qv, es=es, p=p\right)
$$
_Relative humidity in [0, 1] for the heterogeneous N2O5 rate, derived from qv, es and p with the formula and the clip of kpp_mechd_ibu_radm2.inc. Derived, not an input, because WRF itself derives it from the same water vapour that FIX(indf_H2O) carries._

$$
k_{R022} = \mathrm{wrf_o3p_o2_m}\left(f_{o2}=0.20946000516414642, a=6 \times 10^{-34}, n=-2.299999952316284, T=T, T_{ref}=T_{ref}, M=M\right)
$$
_Rate coefficient of RADM2 reaction 22 {22:001} O3P+M=O3 (radm2.eqn: .20946e0*(C_M *6.00D-34*(TEMP/300.0)**(-2.3)))._

$$
k_{R023} = \mathrm{wrf_arr2}\left(A=6.5 \times 10^{-12}, B=-120.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 23 {23:002} O3P+NO2=NO (radm2.eqn: ARR2(6.5D-12, -120.0_dp, TEMP))._

$$
k_{R024} = \mathrm{wrf_o1d_quenching}\left(f_{n2}=0.7808399796485901, A_{n2}=1.8 \times 10^{-11}, B_{n2}=-110.0, f_{o2}=0.20946000516414642, A_{o2}=3.2 \times 10^{-11}, B_{o2}=-70.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 24 {24:003} O1D+M=O3P (radm2.eqn: .78084* ARR2(1.8D-11, -110.0_dp, TEMP) + .20946e0* ARR2(3.2D-11, -70.0_dp, TEMP))._

$$
k_{R025} = 2.2 \times 10^{-10}
$$
_Rate coefficient of RADM2 reaction 25 {26:005} O1D+H2O=OH+OH (radm2.eqn: 2.2D-10)._

$$
k_{R026} = \mathrm{wrf_arr2}\left(A=2 \times 10^{-12}, B=1400.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 26 {27:006} O3+NO=NO2 (radm2.eqn: ARR2(2.0D-12, 1400.0_dp, TEMP))._

$$
k_{R027} = \mathrm{wrf_arr2}\left(A=1.6 \times 10^{-12}, B=940.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 27 {28:007} O3+OH=HO2 (radm2.eqn: ARR2(1.6D-12, 940.0_dp, TEMP))._

$$
k_{R028} = \mathrm{wrf_arr2}\left(A=1.1 \times 10^{-14}, B=500.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 28 {29:008} O3+HO2=OH (radm2.eqn: ARR2(1.1D-14, 500.0_dp, TEMP))._

$$
k_{R029} = \mathrm{wrf_arr2}\left(A=3.7 \times 10^{-12}, B=-240.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 29 {30:009} HO2+NO=NO2+OH (radm2.eqn: ARR2(3.7D-12, -240.0_dp, TEMP))._

$$
k_{R030} = \mathrm{wrf_troe}\left(k0_{300}=1.8 \times 10^{-31}, n=3.2, kinf_{300}=4.7 \times 10^{-12}, m=1.4, T=T, T_{ref}=T_{ref}, M=M\right)
$$
_Rate coefficient of RADM2 reaction 30 {31:010} HO2+NO2=HNO4 (radm2.eqn: TROE( 1.80D-31 , 3.2_dp , 4.70D-12 , 1.4_dp , TEMP, C_M))._

$$
k_{R031} = \mathrm{wrf_troee}\left(A=4.76 \times 10^{26}, B=10900.0, k0_{300}=1.8 \times 10^{-31}, n=3.2, kinf_{300}=4.7 \times 10^{-12}, m=1.4, T=T, T_{ref}=T_{ref}, M=M\right)
$$
_Rate coefficient of RADM2 reaction 31 {32:011} HNO4=HO2+NO2 (radm2.eqn: TROEE( 4.76D26,10900.0_dp, 1.80D-31 , 3.2_dp , 4.70D-12 , 1.4_dp , TEMP, C_M ))._

$$
k_{R032} = \mathrm{wrf_ho2_self}\left(a1=2.2 \times 10^{-13}, e1=600.0, a2=1.9 \times 10^{-33}, e2=980.0, T=T, M=M\right)
$$
_Rate coefficient of RADM2 reaction 32 {33:012} HO2+HO2=H2O2 (radm2.eqn: (2.2D-13*EXP(600./TEMP) + 1.9D-33* C_M *EXP(980._dp/TEMP)))._

$$
k_{R033} = \mathrm{wrf_ho2_self}\left(a1=3.08 \times 10^{-34}, e1=2800.0, a2=2.66 \times 10^{-54}, e2=3180.0, T=T, M=M\right)
$$
_Rate coefficient of RADM2 reaction 33 {34:013} HO2+HO2+H2O=H2O2 (radm2.eqn: (3.08D-34* EXP(2800._dp/TEMP)+ 2.66D-54* C_M *EXP(3180._dp/TEMP)))._

$$
k_{R034} = \mathrm{wrf_arr2}\left(A=3.3 \times 10^{-12}, B=200.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 34 {35:014} H2O2+OH=HO2+H2O (radm2.eqn: ARR2(3.3D-12, 200.0_dp, TEMP))._

$$
k_{R035} = \mathrm{wrf_troe}\left(k0_{300}=7 \times 10^{-31}, n=2.6, kinf_{300}=1.5 \times 10^{-11}, m=0.5, T=T, T_{ref}=T_{ref}, M=M\right)
$$
_Rate coefficient of RADM2 reaction 35 {36:015} NO+OH=HONO (radm2.eqn: TROE( 7.00D-31 , 2.6_dp , 1.50D-11 , 0.5_dp , TEMP, C_M))._

$$
k_{R036} = \mathrm{wrf_arr2_scaled}\left(f=0.20946000516414642, A=3.3 \times 10^{-39}, B=-530.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 36 {37:016} NO+NO+M=NO2+NO2 (radm2.eqn: .20946e0* ARR2(3.3D-39, -530.0_dp, TEMP))._

$$
k_{R037} = \mathrm{wrf_arr2}\left(A=1.4 \times 10^{-13}, B=2500.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 37 {38:017} O3+NO2=NO3 (radm2.eqn: ARR2(1.4D-13, 2500.0_dp, TEMP))._

$$
k_{R038} = \mathrm{wrf_arr2}\left(A=1.7 \times 10^{-11}, B=-150.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 38 {39:018} NO3+NO=NO2+NO2 (radm2.eqn: ARR2(1.7D-11, -150.0_dp, TEMP))._

$$
k_{R039} = \mathrm{wrf_arr2}\left(A=2.5 \times 10^{-14}, B=1230.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 39 {40:019} NO3+NO2=NO+NO2 (radm2.eqn: ARR2(2.5D-14, 1230.0_dp, TEMP))._

$$
k_{R040} = 2.5 \times 10^{-12}
$$
_Rate coefficient of RADM2 reaction 40 {41:020} NO3+HO2=HNO3 (radm2.eqn: 2.5D-12)._

$$
k_{R041} = \mathrm{wrf_troe}\left(k0_{300}=2.2 \times 10^{-30}, n=4.3, kinf_{300}=1.5 \times 10^{-12}, m=0.5, T=T, T_{ref}=T_{ref}, M=M\right)
$$
_Rate coefficient of RADM2 reaction 41 {42:021} NO3+NO2=N2O5 (radm2.eqn: TROE( 2.20D-30 , 4.3_dp , 1.50D-12 , 0.5_dp , TEMP, C_M))._

$$
k_{R042} = \mathrm{wrf_troee}\left(A=9.09 \times 10^{26}, B=11200.0, k0_{300}=2.2 \times 10^{-30}, n=4.3, kinf_{300}=1.5 \times 10^{-12}, m=0.5, T=T, T_{ref}=T_{ref}, M=M\right)
$$
_Rate coefficient of RADM2 reaction 42 {43:022} N2O5=NO2+NO3 (radm2.eqn: TROEE(9.09D26,11200.0_dp, 2.20D-30 , 4.3_dp , 1.50D-12 , 0.5_dp , TEMP, C_M ))._

$$
k_{R043} = \mathrm{wrf_n2o5_aerosol}\left(rh=RH, tau_{dry}=36000.0, rh_{scale}=0.2800000011920929, exponent=2.799999952316284, tau_{min}=300.0\right)
$$
_Rate coefficient of RADM2 reaction 43 {44:137, 14} N2O5=2.00 HNO3 (radm2.eqn: rc_n2o5)._

$$
k_{R044} = \mathrm{wrf_troe}\left(k0_{300}=2.6 \times 10^{-30}, n=3.2, kinf_{300}=2.4 \times 10^{-11}, m=1.3, T=T, T_{ref}=T_{ref}, M=M\right)
$$
_Rate coefficient of RADM2 reaction 44 {45:024} OH+NO2=HNO3 (radm2.eqn: TROE( 2.60D-30 , 3.2_dp , 2.40D-11 , 1.3_dp , TEMP, C_M))._

$$
k_{R045} = \mathrm{wrf_termolecular_sum}\left(a0=7.2 \times 10^{-15}, b0=785.0, a2=4.1 \times 10^{-16}, b2=1440.0, a3=1.9 \times 10^{-33}, b3=725.0, T=T, M=M\right)
$$
_Rate coefficient of RADM2 reaction 45 {46:025} OH+HNO3=NO3+H2O (radm2.eqn: k46(TEMP,C_M))._

$$
k_{R046} = \mathrm{wrf_arr2}\left(A=1.3 \times 10^{-12}, B=-380.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 46 {47:026} OH+HNO4=NO2+H2O (radm2.eqn: ARR2(1.3D-12, -380.0_dp, TEMP))._

$$
k_{R047} = \mathrm{wrf_arr2}\left(A=4.6 \times 10^{-11}, B=-230.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 47 {48:027} OH+HO2=H2O (radm2.eqn: ARR2(4.6D-11, -230.0_dp, TEMP))._

$$
k_{R048} = \mathrm{wrf_troe}\left(k0_{300}=3 \times 10^{-31}, n=3.3, kinf_{300}=1.5 \times 10^{-12}, m=0.0, T=T, T_{ref}=T_{ref}, M=M\right)
$$
_Rate coefficient of RADM2 reaction 48 {49:028} OH+SO2=SULF+HO2 (radm2.eqn: TROE( 3.00D-31 , 3.3_dp , 1.50D-12 , 0.0_dp , TEMP, C_M))._

$$
k_{R049} = \mathrm{wrf_co_oh}\left(a=1.5 \times 10^{-13}, b=2.439 \times 10^{-20}, M=M\right)
$$
_Rate coefficient of RADM2 reaction 49 {50:029} CO+OH=HO2+CO2 (radm2.eqn: (1.5D-13 * (1._dp + 2.439D-20*C_M)))._

$$
k_{R050} = \mathrm{wrf_thermal_t2}\left(c=6.95 \times 10^{-18}, d=1280.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 50 {51:030} CH4+OH=MO2+H2O (radm2.eqn: THERMAL_T2(6.95D-18, 1280.0_dp, TEMP))._

$$
k_{R051} = \mathrm{wrf_thermal_t2}\left(c=1.37 \times 10^{-17}, d=444.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 51 {52:031} ETH+OH=ETHP+H2O (radm2.eqn: THERMAL_T2(1.37D-17, 444.0_dp, TEMP))._

$$
k_{R052} = \mathrm{wrf_arr2}\left(A=1.59 \times 10^{-11}, B=540.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 52 {53:032} HC3+OH=0.83 HC3P+0.17 HO2 +0.009 HCHO+0.075 ALD +0.025 KET+H2O (radm2.eqn: ARR2(1.59D-11, 540.0_dp, TEMP))._

$$
k_{R053} = \mathrm{wrf_arr2}\left(A=1.73 \times 10^{-11}, B=380.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 53 {54:033} HC5+OH=HC5P+0.25 XO2+H2O (radm2.eqn: ARR2(1.73D-11, 380.0_dp, TEMP))._

$$
k_{R054} = \mathrm{wrf_arr2}\left(A=3.64 \times 10^{-11}, B=380.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 54 {55:034} HC8+OH=HC8P+0.75 XO2+H2O (radm2.eqn: ARR2(3.64D-11, 380.0_dp, TEMP))._

$$
k_{R055} = \mathrm{wrf_arr2}\left(A=2.15 \times 10^{-12}, B=-411.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 55 {56:035} OL2+OH=OL2P (radm2.eqn: ARR2(2.15D-12, -411.0_dp, TEMP))._

$$
k_{R056} = \mathrm{wrf_arr2}\left(A=5.32 \times 10^{-12}, B=-504.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 56 {57:036} OLT+OH=OLTP (radm2.eqn: ARR2(5.32D-12, -504.0_dp, TEMP))._

$$
k_{R057} = \mathrm{wrf_arr2}\left(A=1.07 \times 10^{-11}, B=-549.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 57 {58:037} OLI+OH=OLIP (radm2.eqn: ARR2(1.07D-11, -549.0_dp, TEMP))._

$$
k_{R058} = \mathrm{wrf_arr2}\left(A=2.1 \times 10^{-12}, B=-322.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 58 {59:038} TOL+OH=0.75 TOLP+0.25 CSL +0.25 HO2 (radm2.eqn: ARR2(2.1D-12, -322.0_dp, TEMP))._

$$
k_{R059} = \mathrm{wrf_arr2}\left(A=1.89 \times 10^{-11}, B=-116.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 59 {60:039} XYL+OH=0.83 XYLP+0.17 CSL +0.17 HO2 (radm2.eqn: ARR2(1.89D-11, -116.0_dp, TEMP))._

$$
k_{R060} = 4 \times 10^{-11}
$$
_Rate coefficient of RADM2 reaction 60 {61:040} CSL+OH=0.10 HO2+0.90 XO2 +0.90 TCO3-0.90 OH (radm2.eqn: 4.0D-11)._

$$
k_{R061} = 9 \times 10^{-12}
$$
_Rate coefficient of RADM2 reaction 61 {62:041} HCHO+OH=HO2+CO+H2O (radm2.eqn: 9.0D-12)._

$$
k_{R062} = \mathrm{wrf_arr2}\left(A=6.87 \times 10^{-12}, B=-256.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 62 {63:042} ALD+OH=ACO3+H2O (radm2.eqn: ARR2(6.87D-12, -256.0_dp, TEMP))._

$$
k_{R063} = \mathrm{wrf_arr2}\left(A=1.2 \times 10^{-11}, B=745.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 63 {64:043} KET+OH=KETP+H2O (radm2.eqn: ARR2(1.2D-11, 745.0_dp, TEMP))._

$$
k_{R064} = 1.15 \times 10^{-11}
$$
_Rate coefficient of RADM2 reaction 64 {65:044} GLY+OH=HO2+2.00 CO+H2O (radm2.eqn: 1.15D-11)._

$$
k_{R065} = 1.7 \times 10^{-11}
$$
_Rate coefficient of RADM2 reaction 65 {66:045} MGLY+OH=ACO3+CO+H2O (radm2.eqn: 1.7D-11)._

$$
k_{R066} = 2.8 \times 10^{-11}
$$
_Rate coefficient of RADM2 reaction 66 {67:046} DCB+OH=TCO3+H2O (radm2.eqn: 2.8D-11)._

$$
k_{R067} = 1 \times 10^{-11}
$$
_Rate coefficient of RADM2 reaction 67 {68:047} OP1+OH=0.50 MO2+0.50 HCHO +0.50 OH (radm2.eqn: 1.0D-11)._

$$
k_{R068} = 1 \times 10^{-11}
$$
_Rate coefficient of RADM2 reaction 68 {69:048} OP2+OH=0.50 HC3P+0.50 ALD +0.50 OH (radm2.eqn: 1.0D-11)._

$$
k_{R069} = 1 \times 10^{-11}
$$
_Rate coefficient of RADM2 reaction 69 {70:049} PAA+OH=ACO3+H2O (radm2.eqn: 1.0D-11)._

$$
k_{R070} = \mathrm{wrf_thermal_t2}\left(c=6.85 \times 10^{-18}, d=444.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 70 {71:050} PAN+OH=HCHO+NO3+XO2 (radm2.eqn: THERMAL_T2(6.85D-18, 444.0_dp, TEMP))._

$$
k_{R071} = \mathrm{wrf_arr2}\left(A=1.55 \times 10^{-11}, B=540.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 71 {72:051} ONIT+OH=HC3P+NO2 (radm2.eqn: ARR2(1.55D-11, 540.0_dp, TEMP))._

$$
k_{R072} = \mathrm{wrf_arr2}\left(A=2.55 \times 10^{-11}, B=-409.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 72 {73:052} ISO+OH=OLTP (radm2.eqn: ARR2(2.55D-11, -409.0_dp, TEMP))._

$$
k_{R073} = \mathrm{wrf_arr2}\left(A=2.8 \times 10^{-12}, B=-181.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 73 {74:053} ACO3+NO2=PAN (radm2.eqn: ARR2(2.8D-12, -181.0_dp, TEMP))._

$$
k_{R074} = \mathrm{wrf_arr2}\left(A=1.95 \times 10^{16}, B=13543.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 74 {75:054} PAN=ACO3+NO2 (radm2.eqn: ARR2(1.95D+16, 13543.0_dp, TEMP))._

$$
k_{R075} = 4.7 \times 10^{-12}
$$
_Rate coefficient of RADM2 reaction 75 {76:055} TCO3+NO2=TPAN (radm2.eqn: 4.7D-12)._

$$
k_{R076} = \mathrm{wrf_arr2}\left(A=1.95 \times 10^{16}, B=13543.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 76 {77:056} TPAN=TCO3+NO2 (radm2.eqn: ARR2(1.95D+16, 13543.0_dp, TEMP))._

$$
k_{R077} = \mathrm{wrf_arr2}\left(A=4.2 \times 10^{-12}, B=-180.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 77 {78:057} MO2+NO=HCHO+HO2+NO2 (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP))._

$$
k_{R078} = \mathrm{wrf_arr2}\left(A=4.2 \times 10^{-12}, B=-180.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 78 {79:058} HC3P+NO=0.75 ALD+0.25 KET +0.09 HCHO+0.036 ONIT +0.964 NO2+0.964 HO2 (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP))._

$$
k_{R079} = \mathrm{wrf_arr2}\left(A=4.2 \times 10^{-12}, B=-180.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 79 {80:060} HC5P+NO=0.38 ALD+0.69 KET +0.08 ONIT+0.92 NO2 +0.92 HO2 (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP))._

$$
k_{R080} = \mathrm{wrf_arr2}\left(A=4.2 \times 10^{-12}, B=-180.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 80 {81:062} HC8P+NO=0.35 ALD+1.06 KET +0.04 HCHO+0.24 ONIT +0.76 NO2+0.76 HO2 (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP))._

$$
k_{R081} = \mathrm{wrf_arr2}\left(A=4.2 \times 10^{-12}, B=-180.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 81 {82:064} OL2P+NO=1.60 HCHO+HO2+NO2 +0.20 ALD (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP))._

$$
k_{R082} = \mathrm{wrf_arr2}\left(A=4.2 \times 10^{-12}, B=-180.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 82 {83:065} OLTP+NO=ALD+HCHO+HO2+NO2 (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP))._

$$
k_{R083} = \mathrm{wrf_arr2}\left(A=4.2 \times 10^{-12}, B=-180.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 83 {84:066} OLIP+NO=HO2+1.45 ALD +0.28 HCHO+0.10 KET+NO2 (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP))._

$$
k_{R084} = \mathrm{wrf_arr2}\left(A=4.2 \times 10^{-12}, B=-180.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 84 {85:067} ACO3+NO=MO2+NO2 (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP))._

$$
k_{R085} = \mathrm{wrf_arr2}\left(A=4.2 \times 10^{-12}, B=-180.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 85 {86:068} TCO3+NO=NO2+0.92 HO2 +0.89 GLY+0.11 MGLY +0.05 ACO3+0.95 CO +2.00 XO2 (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP))._

$$
k_{R086} = \mathrm{wrf_arr2}\left(A=4.2 \times 10^{-12}, B=-180.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 86 {87:069} TOLP+NO=NO2+HO2+0.17 MGLY +0.16 GLY+0.70 DCB (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP))._

$$
k_{R087} = \mathrm{wrf_arr2}\left(A=4.2 \times 10^{-12}, B=-180.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 87 {88:070} XYLP+NO=NO2+HO2+0.45 MGLY +0.806 DCB (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP))._

$$
k_{R088} = \mathrm{wrf_arr2}\left(A=4.2 \times 10^{-12}, B=-180.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 88 {89:071} ETHP+NO=ALD+HO2+NO2 (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP))._

$$
k_{R089} = \mathrm{wrf_arr2}\left(A=4.2 \times 10^{-12}, B=-180.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 89 {90:072} KETP+NO=MGLY+NO2+HO2 (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP))._

$$
k_{R090} = \mathrm{wrf_arr2}\left(A=4.2 \times 10^{-12}, B=-180.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 90 {91:073} OLN+NO=HCHO+ALD+2.00 NO2 (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP))._

$$
k_{R091} = \mathrm{wrf_arr2}\left(A=6 \times 10^{-13}, B=2058.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 91 {92:074} HCHO+NO3=HO2+HNO3+CO (radm2.eqn: ARR2(6.0D-13, 2058.0_dp, TEMP))._

$$
k_{R092} = \mathrm{wrf_arr2}\left(A=1.4 \times 10^{-12}, B=1900.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 92 {93:075} ALD+NO3=ACO3+HNO3 (radm2.eqn: ARR2(1.4D-12, 1900.0_dp, TEMP))._

$$
k_{R093} = \mathrm{wrf_arr2}\left(A=6 \times 10^{-13}, B=2058.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 93 {94:076} GLY+NO3=HNO3+HO2+2.00 CO (radm2.eqn: ARR2(6.0D-13, 2058.0_dp, TEMP))._

$$
k_{R094} = \mathrm{wrf_arr2}\left(A=1.4 \times 10^{-12}, B=1900.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 94 {95:077} MGLY+NO3=HNO3+ACO3+CO (radm2.eqn: ARR2(1.4D-12, 1900.0_dp, TEMP))._

$$
k_{R095} = \mathrm{wrf_arr2}\left(A=1.4 \times 10^{-12}, B=1900.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 95 {96:078} DCB+NO3=HNO3+TCO3 (radm2.eqn: ARR2(1.4D-12, 1900.0_dp, TEMP))._

$$
k_{R096} = 2.2 \times 10^{-11}
$$
_Rate coefficient of RADM2 reaction 96 {97:079} CSL+NO3=HNO3+XNO2+0.50 CSL (radm2.eqn: 2.2D-11)._

$$
k_{R097} = \mathrm{wrf_arr2}\left(A=2 \times 10^{-12}, B=2923.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 97 {98:080} OL2+NO3=OLN (radm2.eqn: ARR2(2.0D-12, 2923.0_dp, TEMP))._

$$
k_{R098} = \mathrm{wrf_arr2}\left(A=1 \times 10^{-11}, B=1895.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 98 {99:081} OLT+NO3=OLN (radm2.eqn: ARR2(1.0D-11, 1895.0_dp, TEMP))._

$$
k_{R099} = \mathrm{wrf_arr2}\left(A=3.23 \times 10^{-11}, B=975.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 99 {100:082} OLI+NO3=OLN (radm2.eqn: ARR2(3.23D-11, 975.0_dp, TEMP))._

$$
k_{R100} = 5.81 \times 10^{-13}
$$
_Rate coefficient of RADM2 reaction 100 {101:083} ISO+NO3=OLN (radm2.eqn: 5.81D-13)._

$$
k_{R101} = \mathrm{wrf_arr2}\left(A=1.2 \times 10^{-14}, B=2633.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 101 {102:084} OL2+O3=HCHO+0.42 CO+0.40 ORA1 +0.12 HO2 (radm2.eqn: ARR2(1.2D-14, 2633.0_dp, TEMP))._

$$
k_{R102} = \mathrm{wrf_arr2}\left(A=1.32 \times 10^{-14}, B=2105.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 102 {103:085} OLT+O3=0.53 HCHO+0.50 ALD +0.33 CO+0.20 ORA1 +0.20 ORA2+0.23 HO2 +0.22 MO2+0.10 OH +0.06 CH4 (radm2.eqn: ARR2(1.32D-14, 2105.0_dp, TEMP))._

$$
k_{R103} = \mathrm{wrf_arr2}\left(A=7.29 \times 10^{-15}, B=1136.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 103 {104:086} OLI+O3=0.18 HCHO+0.72 ALD +0.10 KET+0.23 CO +0.06 ORA1+0.29 ORA2 +0.09 CH4+0.26 HO2 +0.31 MO2+0.14 OH (radm2.eqn: ARR2(7.29D-15, 1136.0_dp, TEMP))._

$$
k_{R104} = \mathrm{wrf_arr2}\left(A=1.23 \times 10^{-14}, B=2013.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 104 {105:087} ISO+O3=0.53 HCHO+0.50 ALD +0.33 CO+0.20 ORA1 +0.20 ORA2+0.23 HO2 +0.22 MO2+0.10 OH (radm2.eqn: ARR2(1.23D-14, 2013.0_dp, TEMP))._

$$
k_{R105} = \mathrm{wrf_arr2}\left(A=7.7 \times 10^{-14}, B=-1300.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 105 {106:088} HO2+MO2=OP1 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP))._

$$
k_{R106} = \mathrm{wrf_arr2}\left(A=7.7 \times 10^{-14}, B=-1300.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 106 {107:089} HO2+ETHP=OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP))._

$$
k_{R107} = \mathrm{wrf_arr2}\left(A=7.7 \times 10^{-14}, B=-1300.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 107 {108:090} HO2+HC3P=OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP))._

$$
k_{R108} = \mathrm{wrf_arr2}\left(A=7.7 \times 10^{-14}, B=-1300.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 108 {109:091} HO2+HC5P=OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP))._

$$
k_{R109} = \mathrm{wrf_arr2}\left(A=7.7 \times 10^{-14}, B=-1300.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 109 {110:092} HO2+HC8P=OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP))._

$$
k_{R110} = \mathrm{wrf_arr2}\left(A=7.7 \times 10^{-14}, B=-1300.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 110 {111:093} HO2+OL2P=OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP))._

$$
k_{R111} = \mathrm{wrf_arr2}\left(A=7.7 \times 10^{-14}, B=-1300.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 111 {112:094} HO2+OLTP=OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP))._

$$
k_{R112} = \mathrm{wrf_arr2}\left(A=7.7 \times 10^{-14}, B=-1300.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 112 {113:095} HO2+OLIP=OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP))._

$$
k_{R113} = \mathrm{wrf_arr2}\left(A=7.7 \times 10^{-14}, B=-1300.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 113 {114:096} HO2+KETP=OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP))._

$$
k_{R114} = \mathrm{wrf_arr2}\left(A=7.7 \times 10^{-14}, B=-1300.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 114 {115:097} HO2+ACO3=PAA (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP))._

$$
k_{R115} = \mathrm{wrf_arr2}\left(A=7.7 \times 10^{-14}, B=-1300.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 115 {116:098} HO2+TOLP= OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP))._

$$
k_{R116} = \mathrm{wrf_arr2}\left(A=7.7 \times 10^{-14}, B=-1300.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 116 {117:099} HO2+XYLP=OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP))._

$$
k_{R117} = \mathrm{wrf_arr2}\left(A=7.7 \times 10^{-14}, B=-1300.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 117 {118:100} HO2+TCO3=OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP))._

$$
k_{R118} = \mathrm{wrf_arr2}\left(A=7.7 \times 10^{-14}, B=-1300.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 118 {119:101} HO2+OLN=ONIT (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP))._

$$
k_{R119} = \mathrm{wrf_arr2}\left(A=1.9 \times 10^{-13}, B=-220.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 119 {120:102} MO2+MO2=1.50 HCHO+HO2 (radm2.eqn: ARR2(1.9D-13, -220.0_dp, TEMP))._

$$
k_{R120} = \mathrm{wrf_arr2}\left(A=1.4 \times 10^{-13}, B=-220.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 120 {121:103} MO2+ETHP=0.75 HCHO+HO2 +0.75 ALD (radm2.eqn: ARR2(1.4D-13, -220.0_dp, TEMP))._

$$
k_{R121} = \mathrm{wrf_arr2}\left(A=4.2 \times 10^{-14}, B=-220.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 121 {122:104} MO2+HC3P=0.75 HCHO+HO2 +0.15 ALD+0.6 KET (radm2.eqn: ARR2(4.2D-14, -220.0_dp, TEMP))._

$$
k_{R122} = \mathrm{wrf_arr2}\left(A=3.4 \times 10^{-14}, B=-220.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 122 {123:105} MO2+HC5P=0.77 HCHO+HO2 +0.41 ALD+0.75 KET (radm2.eqn: ARR2(3.4D-14, -220.0_dp, TEMP))._

$$
k_{R123} = \mathrm{wrf_arr2}\left(A=2.9 \times 10^{-14}, B=-220.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 123 {124:106} MO2+HC8P=0.80 HCHO+HO2 +0.46 ALD+1.39 KET (radm2.eqn: ARR2(2.9D-14, -220.0_dp, TEMP))._

$$
k_{R124} = \mathrm{wrf_arr2}\left(A=1.4 \times 10^{-13}, B=-220.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 124 {125:107} MO2+OL2P=1.55 HCHO+HO2 +0.35 ALD (radm2.eqn: ARR2(1.4D-13, -220.0_dp, TEMP))._

$$
k_{R125} = \mathrm{wrf_arr2}\left(A=1.4 \times 10^{-13}, B=-220.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 125 {126:108} MO2+OLTP=1.25 HCHO+HO2 +0.75 ALD (radm2.eqn: ARR2(1.4D-13, -220.0_dp, TEMP))._

$$
k_{R126} = \mathrm{wrf_arr2}\left(A=1.7 \times 10^{-14}, B=-220.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 126 {127:109} MO2+OLIP=0.89 HCHO+HO2 +0.725 ALD+0.55 KET (radm2.eqn: ARR2(1.7D-14, -220.0_dp, TEMP))._

$$
k_{R127} = \mathrm{wrf_arr2}\left(A=1.7 \times 10^{-14}, B=-220.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 127 {128:110} MO2+KETP=0.75 HCHO+HO2 +0.75 MGLY (radm2.eqn: ARR2(1.7D-14, -220.0_dp, TEMP))._

$$
k_{R128} = \mathrm{wrf_arr2}\left(A=9.6 \times 10^{-13}, B=-220.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 128 {129:111} MO2+ACO3=HCHO+0.50 HO2 +0.50 MO2+0.50 ORA2 (radm2.eqn: ARR2(9.6D-13, -220.0_dp, TEMP))._

$$
k_{R129} = \mathrm{wrf_arr2}\left(A=1.7 \times 10^{-14}, B=-220.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 129 {130:112} MO2+TOLP=HCHO+2.00 HO2 +0.17 MGLY+0.16 GLY +0.70 DCB (radm2.eqn: ARR2(1.7D-14, -220.0_dp, TEMP))._

$$
k_{R130} = \mathrm{wrf_arr2}\left(A=1.7 \times 10^{-14}, B=-220.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 130 {131:113} MO2+XYLP=HCHO+2.00 HO2 +0.45 MGLY+0.806 DCB (radm2.eqn: ARR2(1.7D-14, -220.0_dp, TEMP))._

$$
k_{R131} = \mathrm{wrf_arr2}\left(A=9.6 \times 10^{-13}, B=-220.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 131 {132:114} MO2+TCO3=0.50 HCHO+0.50 ORA2 +0.445 GLY+0.055 MGLY +0.025 ACO3+0.475 CO +0.46 HO2+XO2 (radm2.eqn: ARR2(9.6D-13, -220.0_dp, TEMP))._

$$
k_{R132} = \mathrm{wrf_arr2}\left(A=3.4 \times 10^{-13}, B=-220.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 132 {133:115} ETHP+ACO3=ALD+0.50 HO2 +0.50 MO2+0.50 ORA2 (radm2.eqn: ARR2(3.4D-13, -220.0_dp, TEMP))._

$$
k_{R133} = \mathrm{wrf_arr2}\left(A=1 \times 10^{-13}, B=-220.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 133 {134:116} HC3P+ACO3=0.2 ALD+0.8 KET +0.50 HO2+0.50 ORA2 +0.50 MO2 (radm2.eqn: ARR2(1.0D-13, -220.0_dp, TEMP))._

$$
k_{R134} = \mathrm{wrf_arr2}\left(A=8.4 \times 10^{-14}, B=-220.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 134 {135:117} HC5P+ACO3=0.14 ALD+0.86 KET +0.50 HO2+0.50 ORA2 +0.50 MO2 (radm2.eqn: ARR2(8.4D-14, -220.0_dp, TEMP))._

$$
k_{R135} = \mathrm{wrf_arr2}\left(A=7.2 \times 10^{-14}, B=-220.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 135 {136:118} HC8P+ACO3=0.1 ALD+0.9 KET +0.50 HO2+0.50 ORA2 +0.50 MO2 (radm2.eqn: ARR2(7.2D-14, -220.0_dp, TEMP))._

$$
k_{R136} = \mathrm{wrf_arr2}\left(A=3.4 \times 10^{-13}, B=-220.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 136 {137:119} OL2P+ACO3=0.80 HCHO+0.60 ALD +0.50 HO2+0.50 ORA2 +0.50 MO2 (radm2.eqn: ARR2(3.4D-13, -220.0_dp, TEMP))._

$$
k_{R137} = \mathrm{wrf_arr2}\left(A=3.4 \times 10^{-13}, B=-220.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 137 {138:120} OLTP+ACO3=ALD+0.50 HCHO +0.50 HO2+0.50 ORA2 +0.50 MO2 (radm2.eqn: ARR2(3.4D-13, -220.0_dp, TEMP))._

$$
k_{R138} = \mathrm{wrf_arr2}\left(A=4.2 \times 10^{-14}, B=-220.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 138 {139:121} OLIP+ACO3=0.725 ALD+0.55 KET +0.14 HCHO+0.50 HO2 +0.50 MO2+0.50 ORA2 (radm2.eqn: ARR2(4.2D-14, -220.0_dp, TEMP))._

$$
k_{R139} = \mathrm{wrf_arr2}\left(A=4.2 \times 10^{-14}, B=-220.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 139 {140:122} KETP+ACO3=MGLY+0.50 HO2 +0.50 ORA2+0.50 MO2 (radm2.eqn: ARR2(4.2D-14, -220.0_dp, TEMP))._

$$
k_{R140} = \mathrm{wrf_arr2}\left(A=1.19 \times 10^{-12}, B=-220.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 140 {141:123} ACO3+ACO3=2.00 MO2 (radm2.eqn: ARR2(1.19D-12, -220.0_dp, TEMP))._

$$
k_{R141} = \mathrm{wrf_arr2}\left(A=4.2 \times 10^{-14}, B=-220.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 141 {142:124} ACO3+TOLP=0.8 MGLY+0.2 GLY +1.00 DCB+HO2+MO2 (radm2.eqn: ARR2(4.2D-14, -220.0_dp, TEMP))._

$$
k_{R142} = \mathrm{wrf_arr2}\left(A=4.2 \times 10^{-14}, B=-220.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 142 {143:125} ACO3+XYLP=MO2+1.00 MGLY +1.00 DCB+HO2 (radm2.eqn: ARR2(4.2D-14, -220.0_dp, TEMP))._

$$
k_{R143} = \mathrm{wrf_arr2}\left(A=1.19 \times 10^{-12}, B=-220.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 143 {144:126} ACO3+TCO3=MO2+0.92 HO2 +0.89 GLY+0.11 MGLY +0.05 ACO3+0.95 CO +2.00 XO2 (radm2.eqn: ARR2(1.19D-12, -220.0_dp, TEMP))._

$$
k_{R144} = \mathrm{wrf_arr2}\left(A=7.7 \times 10^{-14}, B=-1300.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 144 {145:127} XO2+HO2=OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP))._

$$
k_{R145} = \mathrm{wrf_arr2}\left(A=1.7 \times 10^{-14}, B=-220.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 145 {146:128} XO2+MO2=HCHO+HO2 (radm2.eqn: ARR2(1.7D-14, -220.0_dp, TEMP))._

$$
k_{R146} = \mathrm{wrf_arr2}\left(A=4.2 \times 10^{-14}, B=-220.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 146 {147:129} XO2+ACO3=MO2 (radm2.eqn: ARR2(4.2D-14, -220.0_dp, TEMP))._

$$
k_{R147} = \mathrm{wrf_arr2}\left(A=3.6 \times 10^{-16}, B=-220.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 147 {148:130} XO2+XO2=H2O (radm2.eqn: ARR2(3.6D-16, -220.0_dp, TEMP))._

$$
k_{R148} = \mathrm{wrf_arr2}\left(A=4.2 \times 10^{-12}, B=-180.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 148 {149:131} XO2+NO=NO2 (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP))._

$$
k_{R149} = \mathrm{wrf_arr2}\left(A=4.2 \times 10^{-12}, B=-180.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 149 {150:132} XNO2+NO2=ONIT (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP))._

$$
k_{R150} = \mathrm{wrf_arr2}\left(A=7.7 \times 10^{-14}, B=-1300.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 150 {151:133} XNO2+HO2=OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP))._

$$
k_{R151} = \mathrm{wrf_arr2}\left(A=1.7 \times 10^{-14}, B=-220.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 151 {152:134} XNO2+MO2=HCHO+HO2 (radm2.eqn: ARR2(1.7D-14, -220.0_dp, TEMP))._

$$
k_{R152} = \mathrm{wrf_arr2}\left(A=4.2 \times 10^{-14}, B=-220.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 152 {153:135} XNO2+ACO3=MO2 (radm2.eqn: ARR2(4.2D-14, -220.0_dp, TEMP))._

$$
k_{R153} = \mathrm{wrf_arr2}\left(A=3.6 \times 10^{-16}, B=-220.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 153 {154:136} XNO2+XNO2=H2O (radm2.eqn: ARR2(3.6D-16, -220.0_dp, TEMP))._

$$
k_{R154} = \mathrm{wrf_arr2}\left(A=1.7 \times 10^{-14}, B=-220.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 154 {155:138} MO2+OLN=1.75 HCHO+.5 HO2 +ALD+NO2 (radm2.eqn: ARR2(1.7D-14, -220.0_dp, TEMP))._

$$
k_{R155} = \mathrm{wrf_arr2}\left(A=4.2 \times 10^{-14}, B=-220.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 155 {156:139} ACO3+OLN=HCHO+ALD+0.50 ORA2 +NO2+0.50 MO2 (radm2.eqn: ARR2(4.2D-14, -220.0_dp, TEMP))._

$$
k_{R156} = \mathrm{wrf_arr2}\left(A=3.6 \times 10^{-16}, B=-220.0, T=T\right)
$$
_Rate coefficient of RADM2 reaction 156 {157:140} OLN+OLN=2.00 HCHO+2.00 ALD +2.00 NO2 (radm2.eqn: ARR2(3.6D-16, -220.0_dp, TEMP))._

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "expression_template_imports": [
    {
      "ref": "./radm2_ratelaws.esm"
    }
  ],
  "variables": {
    "T": {
      "type": "parameter",
      "units": "K",
      "default": 298.0,
      "description": "Air temperature (KPP TEMP)."
    },
    "T_ref": {
      "type": "parameter",
      "units": "K",
      "default": 300.0,
      "description": "Reference temperature of the (T/300)^n forms (WRF literal 300)."
    },
    "p": {
      "type": "parameter",
      "units": "Pa",
      "default": 101325.0,
      "description": "Air pressure (WRF p_phy), used only to derive RH for the heterogeneous N2O5 rate."
    },
    "M": {
      "type": "parameter",
      "units": "molec/cm^3",
      "default": 2.4623522626293244e+19,
      "description": "Air number density, the KPP fixed species M (C_M = FIX(indf_M) = dens2con_a rho_phy, chem_driver.F). This is the single source of M for the whole document: the Troe, termolecular and CO + OH forms read it as a rate-law argument, and the reactions in which KPP multiplies by FIX(indf_M) (R022, R024, R036) multiply their rate by it. RADM2 therefore carries no M species to fall out of step with it."
    },
    "H2O": {
      "type": "parameter",
      "units": "molec/cm^3",
      "default": 6.9628642030342e+17,
      "description": "Water vapour number density, the KPP fixed species H2O (FIX(indf_H2O) = dens2con_w qv rho_phy). The single source of water vapour for the whole document: R025 and R033 multiply their rate by it, as KPP multiplies by FIX(indf_H2O), and RH -- hence the heterogeneous N2O5 rate -- is derived from it, so the two humidity paths cannot disagree."
    },
    "qv": {
      "type": "unknown",
      "units": "kg/kg",
      "description": "Water-vapour mass mixing ratio implied by H2O and M (WRF moist(P_QV)), the input of the WRF relative humidity."
    },
    "es": {
      "type": "unknown",
      "units": "Pa",
      "description": "Saturation vapour pressure over water at T, the WRF Bolton-type form of kpp_mechd_ibu_radm2.inc."
    },
    "RH": {
      "type": "unknown",
      "units": "1",
      "description": "Relative humidity in [0, 1] for the heterogeneous N2O5 rate, derived from qv, es and p with the formula and the clip of kpp_mechd_ibu_radm2.inc. Derived, not an input, because WRF itself derives it from the same water vapour that FIX(indf_H2O) carries."
    },
    "j_no2": {
      "type": "parameter",
      "units": "1/s",
      "default": 0.0085,
      "description": "Photolysis frequency ph_no2 (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_no2))."
    },
    "j_o31d": {
      "type": "parameter",
      "units": "1/s",
      "default": 3.2e-05,
      "description": "Photolysis frequency ph_o31d (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_o31d))."
    },
    "j_o33p": {
      "type": "parameter",
      "units": "1/s",
      "default": 0.00042,
      "description": "Photolysis frequency ph_o33p (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_o33p))."
    },
    "j_hno2": {
      "type": "parameter",
      "units": "1/s",
      "default": 0.0017,
      "description": "Photolysis frequency ph_hno2 (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_hno2))."
    },
    "j_hno3": {
      "type": "parameter",
      "units": "1/s",
      "default": 6.5e-07,
      "description": "Photolysis frequency ph_hno3 (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_hno3))."
    },
    "j_hno4": {
      "type": "parameter",
      "units": "1/s",
      "default": 4.2e-06,
      "description": "Photolysis frequency ph_hno4 (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_hno4))."
    },
    "j_no3o2": {
      "type": "parameter",
      "units": "1/s",
      "default": 0.023,
      "description": "Photolysis frequency ph_no3o2 (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_no3o2))."
    },
    "j_no3o": {
      "type": "parameter",
      "units": "1/s",
      "default": 0.185,
      "description": "Photolysis frequency ph_no3o (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_no3o))."
    },
    "j_h2o2": {
      "type": "parameter",
      "units": "1/s",
      "default": 7.3e-06,
      "description": "Photolysis frequency ph_h2o2 (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_h2o2))."
    },
    "j_ch2om": {
      "type": "parameter",
      "units": "1/s",
      "default": 4.6e-05,
      "description": "Photolysis frequency ph_ch2om (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_ch2om))."
    },
    "j_ch2or": {
      "type": "parameter",
      "units": "1/s",
      "default": 3.1e-05,
      "description": "Photolysis frequency ph_ch2or (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_ch2or))."
    },
    "j_ch3cho": {
      "type": "parameter",
      "units": "1/s",
      "default": 5.5e-06,
      "description": "Photolysis frequency ph_ch3cho (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_ch3cho))."
    },
    "j_ch3o2h": {
      "type": "parameter",
      "units": "1/s",
      "default": 5.4e-06,
      "description": "Photolysis frequency ph_ch3o2h (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_ch3o2h))."
    },
    "j_ch3coch3": {
      "type": "parameter",
      "units": "1/s",
      "default": 6.8e-07,
      "description": "Photolysis frequency ph_ch3coch3 (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_ch3coch3))."
    },
    "j_ch3coo2h": {
      "type": "parameter",
      "units": "1/s",
      "default": 3.2e-06,
      "description": "Photolysis frequency ph_ch3coo2h (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_ch3coo2h))."
    },
    "j_ch3coc2h5": {
      "type": "parameter",
      "units": "1/s",
      "default": 1.6e-06,
      "description": "Photolysis frequency ph_ch3coc2h5 (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_ch3coc2h5))."
    },
    "j_hcocho": {
      "type": "parameter",
      "units": "1/s",
      "default": 0.00011,
      "description": "Photolysis frequency ph_hcocho (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_hcocho))."
    },
    "j_hcochob": {
      "type": "parameter",
      "units": "1/s",
      "default": 2.1e-05,
      "description": "Photolysis frequency ph_hcochob (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_hcochob))."
    },
    "j_ch3cocho": {
      "type": "parameter",
      "units": "1/s",
      "default": 0.00016,
      "description": "Photolysis frequency ph_ch3cocho (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_ch3cocho))."
    },
    "j_hcochest": {
      "type": "parameter",
      "units": "1/s",
      "default": 0.00022,
      "description": "Photolysis frequency ph_hcochest (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_hcochest))."
    },
    "j_ch3ono2": {
      "type": "parameter",
      "units": "1/s",
      "default": 1.1e-06,
      "description": "Photolysis frequency ph_ch3ono2 (WRF Registry, min^-1) divided by 60 (KPP interface jv(Pj_ch3ono2))."
    },
    "k_R022": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 22 {22:001} O3P+M=O3 (radm2.eqn: .20946e0*(C_M *6.00D-34*(TEMP/300.0)**(-2.3)))."
    },
    "k_R023": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 23 {23:002} O3P+NO2=NO (radm2.eqn: ARR2(6.5D-12, -120.0_dp, TEMP))."
    },
    "k_R024": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 24 {24:003} O1D+M=O3P (radm2.eqn: .78084* ARR2(1.8D-11, -110.0_dp, TEMP) + .20946e0* ARR2(3.2D-11, -70.0_dp, TEMP))."
    },
    "k_R025": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 25 {26:005} O1D+H2O=OH+OH (radm2.eqn: 2.2D-10)."
    },
    "k_R026": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 26 {27:006} O3+NO=NO2 (radm2.eqn: ARR2(2.0D-12, 1400.0_dp, TEMP))."
    },
    "k_R027": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 27 {28:007} O3+OH=HO2 (radm2.eqn: ARR2(1.6D-12, 940.0_dp, TEMP))."
    },
    "k_R028": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 28 {29:008} O3+HO2=OH (radm2.eqn: ARR2(1.1D-14, 500.0_dp, TEMP))."
    },
    "k_R029": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 29 {30:009} HO2+NO=NO2+OH (radm2.eqn: ARR2(3.7D-12, -240.0_dp, TEMP))."
    },
    "k_R030": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 30 {31:010} HO2+NO2=HNO4 (radm2.eqn: TROE( 1.80D-31 , 3.2_dp , 4.70D-12 , 1.4_dp , TEMP, C_M))."
    },
    "k_R031": {
      "type": "unknown",
      "units": "1/s",
      "description": "Rate coefficient of RADM2 reaction 31 {32:011} HNO4=HO2+NO2 (radm2.eqn: TROEE( 4.76D26,10900.0_dp, 1.80D-31 , 3.2_dp , 4.70D-12 , 1.4_dp , TEMP, C_M ))."
    },
    "k_R032": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 32 {33:012} HO2+HO2=H2O2 (radm2.eqn: (2.2D-13*EXP(600./TEMP) + 1.9D-33* C_M *EXP(980._dp/TEMP)))."
    },
    "k_R033": {
      "type": "unknown",
      "units": "cm^6/molec^2/s",
      "description": "Rate coefficient of RADM2 reaction 33 {34:013} HO2+HO2+H2O=H2O2 (radm2.eqn: (3.08D-34* EXP(2800._dp/TEMP)+ 2.66D-54* C_M *EXP(3180._dp/TEMP)))."
    },
    "k_R034": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 34 {35:014} H2O2+OH=HO2+H2O (radm2.eqn: ARR2(3.3D-12, 200.0_dp, TEMP))."
    },
    "k_R035": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 35 {36:015} NO+OH=HONO (radm2.eqn: TROE( 7.00D-31 , 2.6_dp , 1.50D-11 , 0.5_dp , TEMP, C_M))."
    },
    "k_R036": {
      "type": "unknown",
      "units": "cm^6/molec^2/s",
      "description": "Rate coefficient of RADM2 reaction 36 {37:016} NO+NO+M=NO2+NO2 (radm2.eqn: .20946e0* ARR2(3.3D-39, -530.0_dp, TEMP))."
    },
    "k_R037": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 37 {38:017} O3+NO2=NO3 (radm2.eqn: ARR2(1.4D-13, 2500.0_dp, TEMP))."
    },
    "k_R038": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 38 {39:018} NO3+NO=NO2+NO2 (radm2.eqn: ARR2(1.7D-11, -150.0_dp, TEMP))."
    },
    "k_R039": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 39 {40:019} NO3+NO2=NO+NO2 (radm2.eqn: ARR2(2.5D-14, 1230.0_dp, TEMP))."
    },
    "k_R040": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 40 {41:020} NO3+HO2=HNO3 (radm2.eqn: 2.5D-12)."
    },
    "k_R041": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 41 {42:021} NO3+NO2=N2O5 (radm2.eqn: TROE( 2.20D-30 , 4.3_dp , 1.50D-12 , 0.5_dp , TEMP, C_M))."
    },
    "k_R042": {
      "type": "unknown",
      "units": "1/s",
      "description": "Rate coefficient of RADM2 reaction 42 {43:022} N2O5=NO2+NO3 (radm2.eqn: TROEE(9.09D26,11200.0_dp, 2.20D-30 , 4.3_dp , 1.50D-12 , 0.5_dp , TEMP, C_M ))."
    },
    "k_R043": {
      "type": "unknown",
      "units": "1/s",
      "description": "Rate coefficient of RADM2 reaction 43 {44:137, 14} N2O5=2.00 HNO3 (radm2.eqn: rc_n2o5)."
    },
    "k_R044": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 44 {45:024} OH+NO2=HNO3 (radm2.eqn: TROE( 2.60D-30 , 3.2_dp , 2.40D-11 , 1.3_dp , TEMP, C_M))."
    },
    "k_R045": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 45 {46:025} OH+HNO3=NO3+H2O (radm2.eqn: k46(TEMP,C_M))."
    },
    "k_R046": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 46 {47:026} OH+HNO4=NO2+H2O (radm2.eqn: ARR2(1.3D-12, -380.0_dp, TEMP))."
    },
    "k_R047": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 47 {48:027} OH+HO2=H2O (radm2.eqn: ARR2(4.6D-11, -230.0_dp, TEMP))."
    },
    "k_R048": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 48 {49:028} OH+SO2=SULF+HO2 (radm2.eqn: TROE( 3.00D-31 , 3.3_dp , 1.50D-12 , 0.0_dp , TEMP, C_M))."
    },
    "k_R049": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 49 {50:029} CO+OH=HO2+CO2 (radm2.eqn: (1.5D-13 * (1._dp + 2.439D-20*C_M)))."
    },
    "k_R050": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 50 {51:030} CH4+OH=MO2+H2O (radm2.eqn: THERMAL_T2(6.95D-18, 1280.0_dp, TEMP))."
    },
    "k_R051": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 51 {52:031} ETH+OH=ETHP+H2O (radm2.eqn: THERMAL_T2(1.37D-17, 444.0_dp, TEMP))."
    },
    "k_R052": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 52 {53:032} HC3+OH=0.83 HC3P+0.17 HO2 +0.009 HCHO+0.075 ALD +0.025 KET+H2O (radm2.eqn: ARR2(1.59D-11, 540.0_dp, TEMP))."
    },
    "k_R053": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 53 {54:033} HC5+OH=HC5P+0.25 XO2+H2O (radm2.eqn: ARR2(1.73D-11, 380.0_dp, TEMP))."
    },
    "k_R054": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 54 {55:034} HC8+OH=HC8P+0.75 XO2+H2O (radm2.eqn: ARR2(3.64D-11, 380.0_dp, TEMP))."
    },
    "k_R055": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 55 {56:035} OL2+OH=OL2P (radm2.eqn: ARR2(2.15D-12, -411.0_dp, TEMP))."
    },
    "k_R056": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 56 {57:036} OLT+OH=OLTP (radm2.eqn: ARR2(5.32D-12, -504.0_dp, TEMP))."
    },
    "k_R057": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 57 {58:037} OLI+OH=OLIP (radm2.eqn: ARR2(1.07D-11, -549.0_dp, TEMP))."
    },
    "k_R058": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 58 {59:038} TOL+OH=0.75 TOLP+0.25 CSL +0.25 HO2 (radm2.eqn: ARR2(2.1D-12, -322.0_dp, TEMP))."
    },
    "k_R059": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 59 {60:039} XYL+OH=0.83 XYLP+0.17 CSL +0.17 HO2 (radm2.eqn: ARR2(1.89D-11, -116.0_dp, TEMP))."
    },
    "k_R060": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 60 {61:040} CSL+OH=0.10 HO2+0.90 XO2 +0.90 TCO3-0.90 OH (radm2.eqn: 4.0D-11)."
    },
    "k_R061": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 61 {62:041} HCHO+OH=HO2+CO+H2O (radm2.eqn: 9.0D-12)."
    },
    "k_R062": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 62 {63:042} ALD+OH=ACO3+H2O (radm2.eqn: ARR2(6.87D-12, -256.0_dp, TEMP))."
    },
    "k_R063": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 63 {64:043} KET+OH=KETP+H2O (radm2.eqn: ARR2(1.2D-11, 745.0_dp, TEMP))."
    },
    "k_R064": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 64 {65:044} GLY+OH=HO2+2.00 CO+H2O (radm2.eqn: 1.15D-11)."
    },
    "k_R065": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 65 {66:045} MGLY+OH=ACO3+CO+H2O (radm2.eqn: 1.7D-11)."
    },
    "k_R066": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 66 {67:046} DCB+OH=TCO3+H2O (radm2.eqn: 2.8D-11)."
    },
    "k_R067": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 67 {68:047} OP1+OH=0.50 MO2+0.50 HCHO +0.50 OH (radm2.eqn: 1.0D-11)."
    },
    "k_R068": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 68 {69:048} OP2+OH=0.50 HC3P+0.50 ALD +0.50 OH (radm2.eqn: 1.0D-11)."
    },
    "k_R069": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 69 {70:049} PAA+OH=ACO3+H2O (radm2.eqn: 1.0D-11)."
    },
    "k_R070": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 70 {71:050} PAN+OH=HCHO+NO3+XO2 (radm2.eqn: THERMAL_T2(6.85D-18, 444.0_dp, TEMP))."
    },
    "k_R071": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 71 {72:051} ONIT+OH=HC3P+NO2 (radm2.eqn: ARR2(1.55D-11, 540.0_dp, TEMP))."
    },
    "k_R072": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 72 {73:052} ISO+OH=OLTP (radm2.eqn: ARR2(2.55D-11, -409.0_dp, TEMP))."
    },
    "k_R073": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 73 {74:053} ACO3+NO2=PAN (radm2.eqn: ARR2(2.8D-12, -181.0_dp, TEMP))."
    },
    "k_R074": {
      "type": "unknown",
      "units": "1/s",
      "description": "Rate coefficient of RADM2 reaction 74 {75:054} PAN=ACO3+NO2 (radm2.eqn: ARR2(1.95D+16, 13543.0_dp, TEMP))."
    },
    "k_R075": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 75 {76:055} TCO3+NO2=TPAN (radm2.eqn: 4.7D-12)."
    },
    "k_R076": {
      "type": "unknown",
      "units": "1/s",
      "description": "Rate coefficient of RADM2 reaction 76 {77:056} TPAN=TCO3+NO2 (radm2.eqn: ARR2(1.95D+16, 13543.0_dp, TEMP))."
    },
    "k_R077": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 77 {78:057} MO2+NO=HCHO+HO2+NO2 (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP))."
    },
    "k_R078": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 78 {79:058} HC3P+NO=0.75 ALD+0.25 KET +0.09 HCHO+0.036 ONIT +0.964 NO2+0.964 HO2 (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP))."
    },
    "k_R079": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 79 {80:060} HC5P+NO=0.38 ALD+0.69 KET +0.08 ONIT+0.92 NO2 +0.92 HO2 (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP))."
    },
    "k_R080": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 80 {81:062} HC8P+NO=0.35 ALD+1.06 KET +0.04 HCHO+0.24 ONIT +0.76 NO2+0.76 HO2 (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP))."
    },
    "k_R081": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 81 {82:064} OL2P+NO=1.60 HCHO+HO2+NO2 +0.20 ALD (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP))."
    },
    "k_R082": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 82 {83:065} OLTP+NO=ALD+HCHO+HO2+NO2 (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP))."
    },
    "k_R083": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 83 {84:066} OLIP+NO=HO2+1.45 ALD +0.28 HCHO+0.10 KET+NO2 (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP))."
    },
    "k_R084": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 84 {85:067} ACO3+NO=MO2+NO2 (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP))."
    },
    "k_R085": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 85 {86:068} TCO3+NO=NO2+0.92 HO2 +0.89 GLY+0.11 MGLY +0.05 ACO3+0.95 CO +2.00 XO2 (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP))."
    },
    "k_R086": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 86 {87:069} TOLP+NO=NO2+HO2+0.17 MGLY +0.16 GLY+0.70 DCB (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP))."
    },
    "k_R087": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 87 {88:070} XYLP+NO=NO2+HO2+0.45 MGLY +0.806 DCB (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP))."
    },
    "k_R088": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 88 {89:071} ETHP+NO=ALD+HO2+NO2 (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP))."
    },
    "k_R089": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 89 {90:072} KETP+NO=MGLY+NO2+HO2 (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP))."
    },
    "k_R090": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 90 {91:073} OLN+NO=HCHO+ALD+2.00 NO2 (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP))."
    },
    "k_R091": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 91 {92:074} HCHO+NO3=HO2+HNO3+CO (radm2.eqn: ARR2(6.0D-13, 2058.0_dp, TEMP))."
    },
    "k_R092": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 92 {93:075} ALD+NO3=ACO3+HNO3 (radm2.eqn: ARR2(1.4D-12, 1900.0_dp, TEMP))."
    },
    "k_R093": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 93 {94:076} GLY+NO3=HNO3+HO2+2.00 CO (radm2.eqn: ARR2(6.0D-13, 2058.0_dp, TEMP))."
    },
    "k_R094": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 94 {95:077} MGLY+NO3=HNO3+ACO3+CO (radm2.eqn: ARR2(1.4D-12, 1900.0_dp, TEMP))."
    },
    "k_R095": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 95 {96:078} DCB+NO3=HNO3+TCO3 (radm2.eqn: ARR2(1.4D-12, 1900.0_dp, TEMP))."
    },
    "k_R096": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 96 {97:079} CSL+NO3=HNO3+XNO2+0.50 CSL (radm2.eqn: 2.2D-11)."
    },
    "k_R097": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 97 {98:080} OL2+NO3=OLN (radm2.eqn: ARR2(2.0D-12, 2923.0_dp, TEMP))."
    },
    "k_R098": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 98 {99:081} OLT+NO3=OLN (radm2.eqn: ARR2(1.0D-11, 1895.0_dp, TEMP))."
    },
    "k_R099": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 99 {100:082} OLI+NO3=OLN (radm2.eqn: ARR2(3.23D-11, 975.0_dp, TEMP))."
    },
    "k_R100": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 100 {101:083} ISO+NO3=OLN (radm2.eqn: 5.81D-13)."
    },
    "k_R101": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 101 {102:084} OL2+O3=HCHO+0.42 CO+0.40 ORA1 +0.12 HO2 (radm2.eqn: ARR2(1.2D-14, 2633.0_dp, TEMP))."
    },
    "k_R102": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 102 {103:085} OLT+O3=0.53 HCHO+0.50 ALD +0.33 CO+0.20 ORA1 +0.20 ORA2+0.23 HO2 +0.22 MO2+0.10 OH +0.06 CH4 (radm2.eqn: ARR2(1.32D-14, 2105.0_dp, TEMP))."
    },
    "k_R103": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 103 {104:086} OLI+O3=0.18 HCHO+0.72 ALD +0.10 KET+0.23 CO +0.06 ORA1+0.29 ORA2 +0.09 CH4+0.26 HO2 +0.31 MO2+0.14 OH (radm2.eqn: ARR2(7.29D-15, 1136.0_dp, TEMP))."
    },
    "k_R104": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 104 {105:087} ISO+O3=0.53 HCHO+0.50 ALD +0.33 CO+0.20 ORA1 +0.20 ORA2+0.23 HO2 +0.22 MO2+0.10 OH (radm2.eqn: ARR2(1.23D-14, 2013.0_dp, TEMP))."
    },
    "k_R105": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 105 {106:088} HO2+MO2=OP1 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP))."
    },
    "k_R106": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 106 {107:089} HO2+ETHP=OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP))."
    },
    "k_R107": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 107 {108:090} HO2+HC3P=OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP))."
    },
    "k_R108": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 108 {109:091} HO2+HC5P=OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP))."
    },
    "k_R109": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 109 {110:092} HO2+HC8P=OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP))."
    },
    "k_R110": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 110 {111:093} HO2+OL2P=OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP))."
    },
    "k_R111": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 111 {112:094} HO2+OLTP=OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP))."
    },
    "k_R112": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 112 {113:095} HO2+OLIP=OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP))."
    },
    "k_R113": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 113 {114:096} HO2+KETP=OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP))."
    },
    "k_R114": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 114 {115:097} HO2+ACO3=PAA (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP))."
    },
    "k_R115": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 115 {116:098} HO2+TOLP= OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP))."
    },
    "k_R116": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 116 {117:099} HO2+XYLP=OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP))."
    },
    "k_R117": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 117 {118:100} HO2+TCO3=OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP))."
    },
    "k_R118": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 118 {119:101} HO2+OLN=ONIT (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP))."
    },
    "k_R119": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 119 {120:102} MO2+MO2=1.50 HCHO+HO2 (radm2.eqn: ARR2(1.9D-13, -220.0_dp, TEMP))."
    },
    "k_R120": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 120 {121:103} MO2+ETHP=0.75 HCHO+HO2 +0.75 ALD (radm2.eqn: ARR2(1.4D-13, -220.0_dp, TEMP))."
    },
    "k_R121": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 121 {122:104} MO2+HC3P=0.75 HCHO+HO2 +0.15 ALD+0.6 KET (radm2.eqn: ARR2(4.2D-14, -220.0_dp, TEMP))."
    },
    "k_R122": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 122 {123:105} MO2+HC5P=0.77 HCHO+HO2 +0.41 ALD+0.75 KET (radm2.eqn: ARR2(3.4D-14, -220.0_dp, TEMP))."
    },
    "k_R123": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 123 {124:106} MO2+HC8P=0.80 HCHO+HO2 +0.46 ALD+1.39 KET (radm2.eqn: ARR2(2.9D-14, -220.0_dp, TEMP))."
    },
    "k_R124": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 124 {125:107} MO2+OL2P=1.55 HCHO+HO2 +0.35 ALD (radm2.eqn: ARR2(1.4D-13, -220.0_dp, TEMP))."
    },
    "k_R125": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 125 {126:108} MO2+OLTP=1.25 HCHO+HO2 +0.75 ALD (radm2.eqn: ARR2(1.4D-13, -220.0_dp, TEMP))."
    },
    "k_R126": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 126 {127:109} MO2+OLIP=0.89 HCHO+HO2 +0.725 ALD+0.55 KET (radm2.eqn: ARR2(1.7D-14, -220.0_dp, TEMP))."
    },
    "k_R127": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 127 {128:110} MO2+KETP=0.75 HCHO+HO2 +0.75 MGLY (radm2.eqn: ARR2(1.7D-14, -220.0_dp, TEMP))."
    },
    "k_R128": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 128 {129:111} MO2+ACO3=HCHO+0.50 HO2 +0.50 MO2+0.50 ORA2 (radm2.eqn: ARR2(9.6D-13, -220.0_dp, TEMP))."
    },
    "k_R129": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 129 {130:112} MO2+TOLP=HCHO+2.00 HO2 +0.17 MGLY+0.16 GLY +0.70 DCB (radm2.eqn: ARR2(1.7D-14, -220.0_dp, TEMP))."
    },
    "k_R130": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 130 {131:113} MO2+XYLP=HCHO+2.00 HO2 +0.45 MGLY+0.806 DCB (radm2.eqn: ARR2(1.7D-14, -220.0_dp, TEMP))."
    },
    "k_R131": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 131 {132:114} MO2+TCO3=0.50 HCHO+0.50 ORA2 +0.445 GLY+0.055 MGLY +0.025 ACO3+0.475 CO +0.46 HO2+XO2 (radm2.eqn: ARR2(9.6D-13, -220.0_dp, TEMP))."
    },
    "k_R132": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 132 {133:115} ETHP+ACO3=ALD+0.50 HO2 +0.50 MO2+0.50 ORA2 (radm2.eqn: ARR2(3.4D-13, -220.0_dp, TEMP))."
    },
    "k_R133": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 133 {134:116} HC3P+ACO3=0.2 ALD+0.8 KET +0.50 HO2+0.50 ORA2 +0.50 MO2 (radm2.eqn: ARR2(1.0D-13, -220.0_dp, TEMP))."
    },
    "k_R134": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 134 {135:117} HC5P+ACO3=0.14 ALD+0.86 KET +0.50 HO2+0.50 ORA2 +0.50 MO2 (radm2.eqn: ARR2(8.4D-14, -220.0_dp, TEMP))."
    },
    "k_R135": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 135 {136:118} HC8P+ACO3=0.1 ALD+0.9 KET +0.50 HO2+0.50 ORA2 +0.50 MO2 (radm2.eqn: ARR2(7.2D-14, -220.0_dp, TEMP))."
    },
    "k_R136": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 136 {137:119} OL2P+ACO3=0.80 HCHO+0.60 ALD +0.50 HO2+0.50 ORA2 +0.50 MO2 (radm2.eqn: ARR2(3.4D-13, -220.0_dp, TEMP))."
    },
    "k_R137": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 137 {138:120} OLTP+ACO3=ALD+0.50 HCHO +0.50 HO2+0.50 ORA2 +0.50 MO2 (radm2.eqn: ARR2(3.4D-13, -220.0_dp, TEMP))."
    },
    "k_R138": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 138 {139:121} OLIP+ACO3=0.725 ALD+0.55 KET +0.14 HCHO+0.50 HO2 +0.50 MO2+0.50 ORA2 (radm2.eqn: ARR2(4.2D-14, -220.0_dp, TEMP))."
    },
    "k_R139": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 139 {140:122} KETP+ACO3=MGLY+0.50 HO2 +0.50 ORA2+0.50 MO2 (radm2.eqn: ARR2(4.2D-14, -220.0_dp, TEMP))."
    },
    "k_R140": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 140 {141:123} ACO3+ACO3=2.00 MO2 (radm2.eqn: ARR2(1.19D-12, -220.0_dp, TEMP))."
    },
    "k_R141": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 141 {142:124} ACO3+TOLP=0.8 MGLY+0.2 GLY +1.00 DCB+HO2+MO2 (radm2.eqn: ARR2(4.2D-14, -220.0_dp, TEMP))."
    },
    "k_R142": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 142 {143:125} ACO3+XYLP=MO2+1.00 MGLY +1.00 DCB+HO2 (radm2.eqn: ARR2(4.2D-14, -220.0_dp, TEMP))."
    },
    "k_R143": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 143 {144:126} ACO3+TCO3=MO2+0.92 HO2 +0.89 GLY+0.11 MGLY +0.05 ACO3+0.95 CO +2.00 XO2 (radm2.eqn: ARR2(1.19D-12, -220.0_dp, TEMP))."
    },
    "k_R144": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 144 {145:127} XO2+HO2=OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP))."
    },
    "k_R145": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 145 {146:128} XO2+MO2=HCHO+HO2 (radm2.eqn: ARR2(1.7D-14, -220.0_dp, TEMP))."
    },
    "k_R146": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 146 {147:129} XO2+ACO3=MO2 (radm2.eqn: ARR2(4.2D-14, -220.0_dp, TEMP))."
    },
    "k_R147": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 147 {148:130} XO2+XO2=H2O (radm2.eqn: ARR2(3.6D-16, -220.0_dp, TEMP))."
    },
    "k_R148": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 148 {149:131} XO2+NO=NO2 (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP))."
    },
    "k_R149": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 149 {150:132} XNO2+NO2=ONIT (radm2.eqn: ARR2(4.2D-12, -180.0_dp, TEMP))."
    },
    "k_R150": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 150 {151:133} XNO2+HO2=OP2 (radm2.eqn: ARR2(7.7D-14, -1300.0_dp, TEMP))."
    },
    "k_R151": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 151 {152:134} XNO2+MO2=HCHO+HO2 (radm2.eqn: ARR2(1.7D-14, -220.0_dp, TEMP))."
    },
    "k_R152": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 152 {153:135} XNO2+ACO3=MO2 (radm2.eqn: ARR2(4.2D-14, -220.0_dp, TEMP))."
    },
    "k_R153": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 153 {154:136} XNO2+XNO2=H2O (radm2.eqn: ARR2(3.6D-16, -220.0_dp, TEMP))."
    },
    "k_R154": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 154 {155:138} MO2+OLN=1.75 HCHO+.5 HO2 +ALD+NO2 (radm2.eqn: ARR2(1.7D-14, -220.0_dp, TEMP))."
    },
    "k_R155": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 155 {156:139} ACO3+OLN=HCHO+ALD+0.50 ORA2 +NO2+0.50 MO2 (radm2.eqn: ARR2(4.2D-14, -220.0_dp, TEMP))."
    },
    "k_R156": {
      "type": "unknown",
      "units": "cm^3/molec/s",
      "description": "Rate coefficient of RADM2 reaction 156 {157:140} OLN+OLN=2.00 HCHO+2.00 ALD +2.00 NO2 (radm2.eqn: ARR2(3.6D-16, -220.0_dp, TEMP))."
    }
  },
  "equations": [
    {
      "lhs": "qv",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_kpp_qv",
        "bindings": {
          "H2O": "H2O",
          "M": "M",
          "mw_h2o": 18.015199661254883,
          "mw_air": 28.969999313354492
        }
      }
    },
    {
      "lhs": "es",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_es",
        "bindings": {
          "T": "T",
          "es0": 611.199951171875,
          "a": 17.670000076293945,
          "T0": 273.1499938964844,
          "T1": 29.649999618530273
        }
      }
    },
    {
      "lhs": "RH",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_rh",
        "bindings": {
          "qv": "qv",
          "es": "es",
          "p": "p"
        }
      }
    },
    {
      "lhs": "k_R022",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_o3p_o2_m",
        "bindings": {
          "f_o2": 0.20946000516414642,
          "a": 6e-34,
          "n": -2.299999952316284,
          "T": "T",
          "T_ref": "T_ref",
          "M": "M"
        }
      }
    },
    {
      "lhs": "k_R023",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 6.5e-12,
          "B": -120.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R024",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_o1d_quenching",
        "bindings": {
          "f_n2": 0.7808399796485901,
          "A_n2": 1.8e-11,
          "B_n2": -110.0,
          "f_o2": 0.20946000516414642,
          "A_o2": 3.2e-11,
          "B_o2": -70.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R025",
      "rhs": 2.2e-10
    },
    {
      "lhs": "k_R026",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 2e-12,
          "B": 1400.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R027",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 1.6e-12,
          "B": 940.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R028",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 1.1e-14,
          "B": 500.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R029",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 3.7e-12,
          "B": -240.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R030",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_troe",
        "bindings": {
          "k0_300": 1.8e-31,
          "n": 3.2,
          "kinf_300": 4.7e-12,
          "m": 1.4,
          "T": "T",
          "T_ref": "T_ref",
          "M": "M"
        }
      }
    },
    {
      "lhs": "k_R031",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_troee",
        "bindings": {
          "A": 4.76e+26,
          "B": 10900.0,
          "k0_300": 1.8e-31,
          "n": 3.2,
          "kinf_300": 4.7e-12,
          "m": 1.4,
          "T": "T",
          "T_ref": "T_ref",
          "M": "M"
        }
      }
    },
    {
      "lhs": "k_R032",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_ho2_self",
        "bindings": {
          "a1": 2.2e-13,
          "e1": 600.0,
          "a2": 1.9e-33,
          "e2": 980.0,
          "T": "T",
          "M": "M"
        }
      }
    },
    {
      "lhs": "k_R033",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_ho2_self",
        "bindings": {
          "a1": 3.08e-34,
          "e1": 2800.0,
          "a2": 2.66e-54,
          "e2": 3180.0,
          "T": "T",
          "M": "M"
        }
      }
    },
    {
      "lhs": "k_R034",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 3.3e-12,
          "B": 200.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R035",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_troe",
        "bindings": {
          "k0_300": 7e-31,
          "n": 2.6,
          "kinf_300": 1.5e-11,
          "m": 0.5,
          "T": "T",
          "T_ref": "T_ref",
          "M": "M"
        }
      }
    },
    {
      "lhs": "k_R036",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2_scaled",
        "bindings": {
          "f": 0.20946000516414642,
          "A": 3.3e-39,
          "B": -530.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R037",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 1.4e-13,
          "B": 2500.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R038",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 1.7e-11,
          "B": -150.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R039",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 2.5e-14,
          "B": 1230.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R040",
      "rhs": 2.5e-12
    },
    {
      "lhs": "k_R041",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_troe",
        "bindings": {
          "k0_300": 2.2e-30,
          "n": 4.3,
          "kinf_300": 1.5e-12,
          "m": 0.5,
          "T": "T",
          "T_ref": "T_ref",
          "M": "M"
        }
      }
    },
    {
      "lhs": "k_R042",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_troee",
        "bindings": {
          "A": 9.09e+26,
          "B": 11200.0,
          "k0_300": 2.2e-30,
          "n": 4.3,
          "kinf_300": 1.5e-12,
          "m": 0.5,
          "T": "T",
          "T_ref": "T_ref",
          "M": "M"
        }
      }
    },
    {
      "lhs": "k_R043",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_n2o5_aerosol",
        "bindings": {
          "rh": "RH",
          "tau_dry": 36000.0,
          "rh_scale": 0.2800000011920929,
          "exponent": 2.799999952316284,
          "tau_min": 300.0
        }
      }
    },
    {
      "lhs": "k_R044",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_troe",
        "bindings": {
          "k0_300": 2.6e-30,
          "n": 3.2,
          "kinf_300": 2.4e-11,
          "m": 1.3,
          "T": "T",
          "T_ref": "T_ref",
          "M": "M"
        }
      }
    },
    {
      "lhs": "k_R045",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_termolecular_sum",
        "bindings": {
          "a0": 7.2e-15,
          "b0": 785.0,
          "a2": 4.1e-16,
          "b2": 1440.0,
          "a3": 1.9e-33,
          "b3": 725.0,
          "T": "T",
          "M": "M"
        }
      }
    },
    {
      "lhs": "k_R046",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 1.3e-12,
          "B": -380.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R047",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 4.6e-11,
          "B": -230.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R048",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_troe",
        "bindings": {
          "k0_300": 3e-31,
          "n": 3.3,
          "kinf_300": 1.5e-12,
          "m": 0.0,
          "T": "T",
          "T_ref": "T_ref",
          "M": "M"
        }
      }
    },
    {
      "lhs": "k_R049",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_co_oh",
        "bindings": {
          "a": 1.5e-13,
          "b": 2.439e-20,
          "M": "M"
        }
      }
    },
    {
      "lhs": "k_R050",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_thermal_t2",
        "bindings": {
          "c": 6.95e-18,
          "d": 1280.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R051",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_thermal_t2",
        "bindings": {
          "c": 1.37e-17,
          "d": 444.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R052",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 1.59e-11,
          "B": 540.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R053",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 1.73e-11,
          "B": 380.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R054",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 3.64e-11,
          "B": 380.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R055",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 2.15e-12,
          "B": -411.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R056",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 5.32e-12,
          "B": -504.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R057",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 1.07e-11,
          "B": -549.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R058",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 2.1e-12,
          "B": -322.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R059",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 1.89e-11,
          "B": -116.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R060",
      "rhs": 4e-11
    },
    {
      "lhs": "k_R061",
      "rhs": 9e-12
    },
    {
      "lhs": "k_R062",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 6.87e-12,
          "B": -256.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R063",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 1.2e-11,
          "B": 745.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R064",
      "rhs": 1.15e-11
    },
    {
      "lhs": "k_R065",
      "rhs": 1.7e-11
    },
    {
      "lhs": "k_R066",
      "rhs": 2.8e-11
    },
    {
      "lhs": "k_R067",
      "rhs": 1e-11
    },
    {
      "lhs": "k_R068",
      "rhs": 1e-11
    },
    {
      "lhs": "k_R069",
      "rhs": 1e-11
    },
    {
      "lhs": "k_R070",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_thermal_t2",
        "bindings": {
          "c": 6.85e-18,
          "d": 444.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R071",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 1.55e-11,
          "B": 540.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R072",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 2.55e-11,
          "B": -409.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R073",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 2.8e-12,
          "B": -181.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R074",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 1.95e+16,
          "B": 13543.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R075",
      "rhs": 4.7e-12
    },
    {
      "lhs": "k_R076",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 1.95e+16,
          "B": 13543.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R077",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 4.2e-12,
          "B": -180.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R078",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 4.2e-12,
          "B": -180.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R079",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 4.2e-12,
          "B": -180.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R080",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 4.2e-12,
          "B": -180.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R081",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 4.2e-12,
          "B": -180.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R082",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 4.2e-12,
          "B": -180.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R083",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 4.2e-12,
          "B": -180.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R084",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 4.2e-12,
          "B": -180.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R085",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 4.2e-12,
          "B": -180.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R086",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 4.2e-12,
          "B": -180.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R087",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 4.2e-12,
          "B": -180.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R088",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 4.2e-12,
          "B": -180.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R089",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 4.2e-12,
          "B": -180.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R090",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 4.2e-12,
          "B": -180.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R091",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 6e-13,
          "B": 2058.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R092",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 1.4e-12,
          "B": 1900.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R093",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 6e-13,
          "B": 2058.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R094",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 1.4e-12,
          "B": 1900.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R095",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 1.4e-12,
          "B": 1900.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R096",
      "rhs": 2.2e-11
    },
    {
      "lhs": "k_R097",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 2e-12,
          "B": 2923.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R098",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 1e-11,
          "B": 1895.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R099",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 3.23e-11,
          "B": 975.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R100",
      "rhs": 5.81e-13
    },
    {
      "lhs": "k_R101",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 1.2e-14,
          "B": 2633.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R102",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 1.32e-14,
          "B": 2105.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R103",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 7.29e-15,
          "B": 1136.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R104",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 1.23e-14,
          "B": 2013.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R105",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 7.7e-14,
          "B": -1300.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R106",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 7.7e-14,
          "B": -1300.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R107",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 7.7e-14,
          "B": -1300.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R108",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 7.7e-14,
          "B": -1300.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R109",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 7.7e-14,
          "B": -1300.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R110",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 7.7e-14,
          "B": -1300.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R111",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 7.7e-14,
          "B": -1300.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R112",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 7.7e-14,
          "B": -1300.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R113",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 7.7e-14,
          "B": -1300.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R114",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 7.7e-14,
          "B": -1300.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R115",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 7.7e-14,
          "B": -1300.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R116",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 7.7e-14,
          "B": -1300.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R117",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 7.7e-14,
          "B": -1300.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R118",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 7.7e-14,
          "B": -1300.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R119",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 1.9e-13,
          "B": -220.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R120",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 1.4e-13,
          "B": -220.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R121",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 4.2e-14,
          "B": -220.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R122",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 3.4e-14,
          "B": -220.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R123",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 2.9e-14,
          "B": -220.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R124",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 1.4e-13,
          "B": -220.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R125",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 1.4e-13,
          "B": -220.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R126",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 1.7e-14,
          "B": -220.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R127",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 1.7e-14,
          "B": -220.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R128",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 9.6e-13,
          "B": -220.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R129",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 1.7e-14,
          "B": -220.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R130",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 1.7e-14,
          "B": -220.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R131",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 9.6e-13,
          "B": -220.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R132",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 3.4e-13,
          "B": -220.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R133",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 1e-13,
          "B": -220.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R134",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 8.4e-14,
          "B": -220.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R135",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 7.2e-14,
          "B": -220.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R136",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 3.4e-13,
          "B": -220.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R137",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 3.4e-13,
          "B": -220.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R138",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 4.2e-14,
          "B": -220.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R139",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 4.2e-14,
          "B": -220.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R140",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 1.19e-12,
          "B": -220.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R141",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 4.2e-14,
          "B": -220.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R142",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 4.2e-14,
          "B": -220.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R143",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 1.19e-12,
          "B": -220.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R144",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 7.7e-14,
          "B": -1300.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R145",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 1.7e-14,
          "B": -220.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R146",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 4.2e-14,
          "B": -220.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R147",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 3.6e-16,
          "B": -220.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R148",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 4.2e-12,
          "B": -180.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R149",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 4.2e-12,
          "B": -180.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R150",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 7.7e-14,
          "B": -1300.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R151",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 1.7e-14,
          "B": -220.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R152",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 4.2e-14,
          "B": -220.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R153",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 3.6e-16,
          "B": -220.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R154",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 1.7e-14,
          "B": -220.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R155",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 4.2e-14,
          "B": -220.0,
          "T": "T"
        }
      }
    },
    {
      "lhs": "k_R156",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wrf_arr2",
        "bindings": {
          "A": 3.6e-16,
          "B": -220.0,
          "T": "T"
        }
      }
    }
  ],
  "tests": [
    {
      "id": "box_urban_noon_rate_constants",
      "description": "Every thermal rate coefficient of RADM2 at the urban noon box state (T 298 K, p 101325 Pa, M 2.462e19 and H2O 6.963e17 molec/cm3 (RH 0.550), clear-sky noon photolysis), against RCONST(22:156) of the WRF-conform KPP Update_RCONST (radm2_Update_Rconst.f90 generated by KPP 2.1 from the radm2.eqn of WRF v4.8.0, compiled real64 with gfortran 13.3 in the WRF build container; standalone box driver, dump box_urban_noon.json). Pointwise, no time step. Expected agreement is binary64 round-off (the same double-precision arithmetic in both), so the tolerance is the tolerance contract for a double-precision reference rel 1e-9; the single-precision literals of radm2.eqn (.20946e0, .78084, -2.3) are bound as their binary64 values so no rounding residual remains. The one exception is k_R043 (N2O5 + aerosol water, rc_n2o5), which WRF evaluates in SINGLE precision in kpp_mechd_ibu_radm2.inc: tolerance rel 1e-6 (measured residual ~1e-7). RH is not an input: the test sets T, p, M and H2O, and RH is asserted first, against the RH the box driver was given, to pin the WRF relative-humidity formula of kpp_mechd_ibu_radm2.inc (rel 1e-12: the same binary64 arithmetic on both sides). The photolysis frequencies are not set because no rate coefficient here reads them. The box states are typical mixing-ratio boxes written by make_states.py; there is no WRF-Chem run behind them. make_states.py builds M and H2O from a nominal T, p and RH (0.55, 0.80, 0.90) and then hands the box driver the RH that WRF's formula gives back from that M, H2O, T and p, the same RH this document derives, so the box driver and the document see one water-vapour state.",
      "parameter_overrides": {
        "T": 298.0,
        "p": 101325.0,
        "M": 2.4623522626293244e+19,
        "H2O": 6.9628642030342e+17
      },
      "time_span": {
        "start": 0,
        "end": 1
      },
      "tolerance": {
        "rel": 1e-09
      },
      "assertions": [
        {
          "variable": "RH",
          "time": 0.0,
          "expected": 0.5499967642780721,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "k_R022",
          "time": 0.0,
          "expected": 3.142563207573703e-15
        },
        {
          "variable": "k_R023",
          "time": 0.0,
          "expected": 9.722927348386447e-12
        },
        {
          "variable": "k_R024",
          "time": 0.0,
          "expected": 2.8807813619467456e-11
        },
        {
          "variable": "k_R025",
          "time": 0.0,
          "expected": 2.2e-10
        },
        {
          "variable": "k_R026",
          "time": 0.0,
          "expected": 1.8227216376153518e-14
        },
        {
          "variable": "k_R027",
          "time": 0.0,
          "expected": 6.826495234993903e-14
        },
        {
          "variable": "k_R028",
          "time": 0.0,
          "expected": 2.0545213966272006e-15
        },
        {
          "variable": "k_R029",
          "time": 0.0,
          "expected": 8.27883242654211e-12
        },
        {
          "variable": "k_R030",
          "time": 0.0,
          "expected": 1.3903877609042402e-12
        },
        {
          "variable": "k_R031",
          "time": 0.0,
          "expected": 0.08619358147124852
        },
        {
          "variable": "k_R032",
          "time": 0.0,
          "expected": 2.9016258866310828e-12
        },
        {
          "variable": "k_R033",
          "time": 0.0,
          "expected": 6.53085927634856e-30
        },
        {
          "variable": "k_R034",
          "time": 0.0,
          "expected": 1.686712771054746e-12
        },
        {
          "variable": "k_R035",
          "time": 0.0,
          "expected": 4.870788581022207e-12
        },
        {
          "variable": "k_R036",
          "time": 0.0,
          "expected": 4.0927761063867036e-39
        },
        {
          "variable": "k_R037",
          "time": 0.0,
          "expected": 3.182130253748133e-17
        },
        {
          "variable": "k_R038",
          "time": 0.0,
          "expected": 2.8122474157384917e-11
        },
        {
          "variable": "k_R039",
          "time": 0.0,
          "expected": 4.0307164500994725e-16
        },
        {
          "variable": "k_R040",
          "time": 0.0,
          "expected": 2.5e-12
        },
        {
          "variable": "k_R041",
          "time": 0.0,
          "expected": 1.2643688089514872e-12
        },
        {
          "variable": "k_R042",
          "time": 0.0,
          "expected": 0.05469661934962397
        },
        {
          "variable": "k_R043",
          "time": 0.0,
          "expected": 0.002874186262488365,
          "tolerance": {
            "rel": 1e-06
          }
        },
        {
          "variable": "k_R044",
          "time": 0.0,
          "expected": 1.1487199251748885e-11
        },
        {
          "variable": "k_R045",
          "time": 0.0,
          "expected": 1.4723511265441259e-13
        },
        {
          "variable": "k_R046",
          "time": 0.0,
          "expected": 4.653092487855136e-12
        },
        {
          "variable": "k_R047",
          "time": 0.0,
          "expected": 9.952943972411954e-11
        },
        {
          "variable": "k_R048",
          "time": 0.0,
          "expected": 8.887738128557556e-13
        },
        {
          "variable": "k_R049",
          "time": 0.0,
          "expected": 2.400851575282938e-13
        },
        {
          "variable": "k_R050",
          "time": 0.0,
          "expected": 8.413784225856462e-15
        },
        {
          "variable": "k_R051",
          "time": 0.0,
          "expected": 2.742101109901881e-13
        },
        {
          "variable": "k_R052",
          "time": 0.0,
          "expected": 2.5966926363166388e-12
        },
        {
          "variable": "k_R053",
          "time": 0.0,
          "expected": 4.8333447183137484e-12
        },
        {
          "variable": "k_R054",
          "time": 0.0,
          "expected": 1.0169580794602337e-11
        },
        {
          "variable": "k_R055",
          "time": 0.0,
          "expected": 8.539158554363374e-12
        },
        {
          "variable": "k_R056",
          "time": 0.0,
          "expected": 2.886842597729431e-11
        },
        {
          "variable": "k_R057",
          "time": 0.0,
          "expected": 6.752687188537704e-11
        },
        {
          "variable": "k_R058",
          "time": 0.0,
          "expected": 6.187148124320653e-12
        },
        {
          "variable": "k_R059",
          "time": 0.0,
          "expected": 2.789433626686177e-11
        },
        {
          "variable": "k_R060",
          "time": 0.0,
          "expected": 4e-11
        },
        {
          "variable": "k_R061",
          "time": 0.0,
          "expected": 9e-12
        },
        {
          "variable": "k_R062",
          "time": 0.0,
          "expected": 1.621966684837726e-11
        },
        {
          "variable": "k_R063",
          "time": 0.0,
          "expected": 9.850199834867856e-13
        },
        {
          "variable": "k_R064",
          "time": 0.0,
          "expected": 1.15e-11
        },
        {
          "variable": "k_R065",
          "time": 0.0,
          "expected": 1.7e-11
        },
        {
          "variable": "k_R066",
          "time": 0.0,
          "expected": 2.8e-11
        },
        {
          "variable": "k_R067",
          "time": 0.0,
          "expected": 1e-11
        },
        {
          "variable": "k_R068",
          "time": 0.0,
          "expected": 1e-11
        },
        {
          "variable": "k_R069",
          "time": 0.0,
          "expected": 1e-11
        },
        {
          "variable": "k_R070",
          "time": 0.0,
          "expected": 1.3710505549509405e-13
        },
        {
          "variable": "k_R071",
          "time": 0.0,
          "expected": 2.5313670354030126e-12
        },
        {
          "variable": "k_R072",
          "time": 0.0,
          "expected": 1.0060094725156997e-10
        },
        {
          "variable": "k_R073",
          "time": 0.0,
          "expected": 5.139737291289061e-12
        },
        {
          "variable": "k_R074",
          "time": 0.0,
          "expected": 0.0003572345945698504
        },
        {
          "variable": "k_R075",
          "time": 0.0,
          "expected": 4.7e-12
        },
        {
          "variable": "k_R076",
          "time": 0.0,
          "expected": 0.0003572345945698504
        },
        {
          "variable": "k_R077",
          "time": 0.0,
          "expected": 7.683778135545332e-12
        },
        {
          "variable": "k_R078",
          "time": 0.0,
          "expected": 7.683778135545332e-12
        },
        {
          "variable": "k_R079",
          "time": 0.0,
          "expected": 7.683778135545332e-12
        },
        {
          "variable": "k_R080",
          "time": 0.0,
          "expected": 7.683778135545332e-12
        },
        {
          "variable": "k_R081",
          "time": 0.0,
          "expected": 7.683778135545332e-12
        },
        {
          "variable": "k_R082",
          "time": 0.0,
          "expected": 7.683778135545332e-12
        },
        {
          "variable": "k_R083",
          "time": 0.0,
          "expected": 7.683778135545332e-12
        },
        {
          "variable": "k_R084",
          "time": 0.0,
          "expected": 7.683778135545332e-12
        },
        {
          "variable": "k_R085",
          "time": 0.0,
          "expected": 7.683778135545332e-12
        },
        {
          "variable": "k_R086",
          "time": 0.0,
          "expected": 7.683778135545332e-12
        },
        {
          "variable": "k_R087",
          "time": 0.0,
          "expected": 7.683778135545332e-12
        },
        {
          "variable": "k_R088",
          "time": 0.0,
          "expected": 7.683778135545332e-12
        },
        {
          "variable": "k_R089",
          "time": 0.0,
          "expected": 7.683778135545332e-12
        },
        {
          "variable": "k_R090",
          "time": 0.0,
          "expected": 7.683778135545332e-12
        },
        {
          "variable": "k_R091",
          "time": 0.0,
          "expected": 6.010298891984333e-16
        },
        {
          "variable": "k_R092",
          "time": 0.0,
          "expected": 2.3830676574575245e-15
        },
        {
          "variable": "k_R093",
          "time": 0.0,
          "expected": 6.010298891984333e-16
        },
        {
          "variable": "k_R094",
          "time": 0.0,
          "expected": 2.3830676574575245e-15
        },
        {
          "variable": "k_R095",
          "time": 0.0,
          "expected": 2.3830676574575245e-15
        },
        {
          "variable": "k_R096",
          "time": 0.0,
          "expected": 2.2e-11
        },
        {
          "variable": "k_R097",
          "time": 0.0,
          "expected": 1.0993979593802023e-16
        },
        {
          "variable": "k_R098",
          "time": 0.0,
          "expected": 1.7309923837959162e-14
        },
        {
          "variable": "k_R099",
          "time": 0.0,
          "expected": 1.2253850849904171e-12
        },
        {
          "variable": "k_R100",
          "time": 0.0,
          "expected": 5.81e-13
        },
        {
          "variable": "k_R101",
          "time": 0.0,
          "expected": 1.745587995331548e-18
        },
        {
          "variable": "k_R102",
          "time": 0.0,
          "expected": 1.129334618737847e-17
        },
        {
          "variable": "k_R103",
          "time": 0.0,
          "expected": 1.6112464984846102e-16
        },
        {
          "variable": "k_R104",
          "time": 0.0,
          "expected": 1.4329509098053106e-17
        },
        {
          "variable": "k_R105",
          "time": 0.0,
          "expected": 6.040375931075073e-12
        },
        {
          "variable": "k_R106",
          "time": 0.0,
          "expected": 6.040375931075073e-12
        },
        {
          "variable": "k_R107",
          "time": 0.0,
          "expected": 6.040375931075073e-12
        },
        {
          "variable": "k_R108",
          "time": 0.0,
          "expected": 6.040375931075073e-12
        },
        {
          "variable": "k_R109",
          "time": 0.0,
          "expected": 6.040375931075073e-12
        },
        {
          "variable": "k_R110",
          "time": 0.0,
          "expected": 6.040375931075073e-12
        },
        {
          "variable": "k_R111",
          "time": 0.0,
          "expected": 6.040375931075073e-12
        },
        {
          "variable": "k_R112",
          "time": 0.0,
          "expected": 6.040375931075073e-12
        },
        {
          "variable": "k_R113",
          "time": 0.0,
          "expected": 6.040375931075073e-12
        },
        {
          "variable": "k_R114",
          "time": 0.0,
          "expected": 6.040375931075073e-12
        },
        {
          "variable": "k_R115",
          "time": 0.0,
          "expected": 6.040375931075073e-12
        },
        {
          "variable": "k_R116",
          "time": 0.0,
          "expected": 6.040375931075073e-12
        },
        {
          "variable": "k_R117",
          "time": 0.0,
          "expected": 6.040375931075073e-12
        },
        {
          "variable": "k_R118",
          "time": 0.0,
          "expected": 6.040375931075073e-12
        },
        {
          "variable": "k_R119",
          "time": 0.0,
          "expected": 3.975334596283567e-13
        },
        {
          "variable": "k_R120",
          "time": 0.0,
          "expected": 2.929193913051049e-13
        },
        {
          "variable": "k_R121",
          "time": 0.0,
          "expected": 8.787581739153147e-14
        },
        {
          "variable": "k_R122",
          "time": 0.0,
          "expected": 7.113756645981119e-14
        },
        {
          "variable": "k_R123",
          "time": 0.0,
          "expected": 6.067615962748602e-14
        },
        {
          "variable": "k_R124",
          "time": 0.0,
          "expected": 2.929193913051049e-13
        },
        {
          "variable": "k_R125",
          "time": 0.0,
          "expected": 2.929193913051049e-13
        },
        {
          "variable": "k_R126",
          "time": 0.0,
          "expected": 3.5568783229905595e-14
        },
        {
          "variable": "k_R127",
          "time": 0.0,
          "expected": 3.5568783229905595e-14
        },
        {
          "variable": "k_R128",
          "time": 0.0,
          "expected": 2.0085901118064334e-12
        },
        {
          "variable": "k_R129",
          "time": 0.0,
          "expected": 3.5568783229905595e-14
        },
        {
          "variable": "k_R130",
          "time": 0.0,
          "expected": 3.5568783229905595e-14
        },
        {
          "variable": "k_R131",
          "time": 0.0,
          "expected": 2.0085901118064334e-12
        },
        {
          "variable": "k_R132",
          "time": 0.0,
          "expected": 7.11375664598112e-13
        },
        {
          "variable": "k_R133",
          "time": 0.0,
          "expected": 2.092281366465035e-13
        },
        {
          "variable": "k_R134",
          "time": 0.0,
          "expected": 1.7575163478306295e-13
        },
        {
          "variable": "k_R135",
          "time": 0.0,
          "expected": 1.506442583854825e-13
        },
        {
          "variable": "k_R136",
          "time": 0.0,
          "expected": 7.11375664598112e-13
        },
        {
          "variable": "k_R137",
          "time": 0.0,
          "expected": 7.11375664598112e-13
        },
        {
          "variable": "k_R138",
          "time": 0.0,
          "expected": 8.787581739153147e-14
        },
        {
          "variable": "k_R139",
          "time": 0.0,
          "expected": 8.787581739153147e-14
        },
        {
          "variable": "k_R140",
          "time": 0.0,
          "expected": 2.4898148260933916e-12
        },
        {
          "variable": "k_R141",
          "time": 0.0,
          "expected": 8.787581739153147e-14
        },
        {
          "variable": "k_R142",
          "time": 0.0,
          "expected": 8.787581739153147e-14
        },
        {
          "variable": "k_R143",
          "time": 0.0,
          "expected": 2.4898148260933916e-12
        },
        {
          "variable": "k_R144",
          "time": 0.0,
          "expected": 6.040375931075073e-12
        },
        {
          "variable": "k_R145",
          "time": 0.0,
          "expected": 3.5568783229905595e-14
        },
        {
          "variable": "k_R146",
          "time": 0.0,
          "expected": 8.787581739153147e-14
        },
        {
          "variable": "k_R147",
          "time": 0.0,
          "expected": 7.532212919274126e-16
        },
        {
          "variable": "k_R148",
          "time": 0.0,
          "expected": 7.683778135545332e-12
        },
        {
          "variable": "k_R149",
          "time": 0.0,
          "expected": 7.683778135545332e-12
        },
        {
          "variable": "k_R150",
          "time": 0.0,
          "expected": 6.040375931075073e-12
        },
        {
          "variable": "k_R151",
          "time": 0.0,
          "expected": 3.5568783229905595e-14
        },
        {
          "variable": "k_R152",
          "time": 0.0,
          "expected": 8.787581739153147e-14
        },
        {
          "variable": "k_R153",
          "time": 0.0,
          "expected": 7.532212919274126e-16
        },
        {
          "variable": "k_R154",
          "time": 0.0,
          "expected": 3.5568783229905595e-14
        },
        {
          "variable": "k_R155",
          "time": 0.0,
          "expected": 8.787581739153147e-14
        },
        {
          "variable": "k_R156",
          "time": 0.0,
          "expected": 7.532212919274126e-16
        }
      ]
    },
    {
      "id": "box_rural_morning_rate_constants",
      "description": "Every thermal rate coefficient of RADM2 at the rural morning box state (T 288 K, p 95000 Pa, M 2.389e19 and H2O 5.558e17 molec/cm3 (RH 0.800), 35 % of noon photolysis), against RCONST(22:156) of the WRF-conform KPP Update_RCONST (radm2_Update_Rconst.f90 generated by KPP 2.1 from the radm2.eqn of WRF v4.8.0, compiled real64 with gfortran 13.3 in the WRF build container; standalone box driver, dump box_rural_morning.json). Pointwise, no time step. Expected agreement is binary64 round-off (the same double-precision arithmetic in both), so the tolerance is the tolerance contract for a double-precision reference rel 1e-9; the single-precision literals of radm2.eqn (.20946e0, .78084, -2.3) are bound as their binary64 values so no rounding residual remains. The one exception is k_R043 (N2O5 + aerosol water, rc_n2o5), which WRF evaluates in SINGLE precision in kpp_mechd_ibu_radm2.inc: tolerance rel 1e-6 (measured residual ~1e-7). RH is not an input: the test sets T, p, M and H2O, and RH is asserted first, against the RH the box driver was given, to pin the WRF relative-humidity formula of kpp_mechd_ibu_radm2.inc (rel 1e-12: the same binary64 arithmetic on both sides). The photolysis frequencies are not set because no rate coefficient here reads them. The box states are typical mixing-ratio boxes written by make_states.py; there is no WRF-Chem run behind them. make_states.py builds M and H2O from a nominal T, p and RH (0.55, 0.80, 0.90) and then hands the box driver the RH that WRF's formula gives back from that M, H2O, T and p, the same RH this document derives, so the box driver and the document see one water-vapour state.",
      "parameter_overrides": {
        "T": 288.0,
        "p": 95000.0,
        "M": 2.3888063901580513e+19,
        "H2O": 5.5580701458619514e+17
      },
      "time_span": {
        "start": 0,
        "end": 1
      },
      "tolerance": {
        "rel": 1e-09
      },
      "assertions": [
        {
          "variable": "RH",
          "time": 0.0,
          "expected": 0.799995285964452,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "k_R022",
          "time": 0.0,
          "expected": 3.2976873294859445e-15
        },
        {
          "variable": "k_R023",
          "time": 0.0,
          "expected": 9.859829176523387e-12
        },
        {
          "variable": "k_R024",
          "time": 0.0,
          "expected": 2.913949007456919e-11
        },
        {
          "variable": "k_R025",
          "time": 0.0,
          "expected": 2.2e-10
        },
        {
          "variable": "k_R026",
          "time": 0.0,
          "expected": 1.548375404969326e-14
        },
        {
          "variable": "k_R027",
          "time": 0.0,
          "expected": 6.118303953560311e-14
        },
        {
          "variable": "k_R028",
          "time": 0.0,
          "expected": 1.938247398037435e-15
        },
        {
          "variable": "k_R029",
          "time": 0.0,
          "expected": 8.513610796303453e-12
        },
        {
          "variable": "k_R030",
          "time": 0.0,
          "expected": 1.4813923087111242e-12
        },
        {
          "variable": "k_R031",
          "time": 0.0,
          "expected": 0.02578916446149822
        },
        {
          "variable": "k_R032",
          "time": 0.0,
          "expected": 3.130636141240742e-12
        },
        {
          "variable": "k_R033",
          "time": 0.0,
          "expected": 9.105167144413931e-30
        },
        {
          "variable": "k_R034",
          "time": 0.0,
          "expected": 1.6478609023776114e-12
        },
        {
          "variable": "k_R035",
          "time": 0.0,
          "expected": 5.056009039102375e-12
        },
        {
          "variable": "k_R036",
          "time": 0.0,
          "expected": 4.353489825800161e-39
        },
        {
          "variable": "k_R037",
          "time": 0.0,
          "expected": 2.3779934718597495e-17
        },
        {
          "variable": "k_R038",
          "time": 0.0,
          "expected": 2.8618308701312432e-11
        },
        {
          "variable": "k_R039",
          "time": 0.0,
          "expected": 3.492534130203685e-16
        },
        {
          "variable": "k_R040",
          "time": 0.0,
          "expected": 2.5e-12
        },
        {
          "variable": "k_R041",
          "time": 0.0,
          "expected": 1.2966196089353091e-12
        },
        {
          "variable": "k_R042",
          "time": 0.0,
          "expected": 0.015210609490938717
        },
        {
          "variable": "k_R043",
          "time": 0.0,
          "expected": 0.0033333308529108763,
          "tolerance": {
            "rel": 1e-06
          }
        },
        {
          "variable": "k_R044",
          "time": 0.0,
          "expected": 1.21769572437996e-11
        },
        {
          "variable": "k_R045",
          "time": 0.0,
          "expected": 1.648330455021863e-13
        },
        {
          "variable": "k_R046",
          "time": 0.0,
          "expected": 4.8637449591892965e-12
        },
        {
          "variable": "k_R047",
          "time": 0.0,
          "expected": 1.0223279406906406e-10
        },
        {
          "variable": "k_R048",
          "time": 0.0,
          "expected": 9.108960622911923e-13
        },
        {
          "variable": "k_R049",
          "time": 0.0,
          "expected": 2.373944817839323e-13
        },
        {
          "variable": "k_R050",
          "time": 0.0,
          "expected": 6.7697414552373e-15
        },
        {
          "variable": "k_R051",
          "time": 0.0,
          "expected": 2.4320260161312094e-13
        },
        {
          "variable": "k_R052",
          "time": 0.0,
          "expected": 2.438343972834363e-12
        },
        {
          "variable": "k_R053",
          "time": 0.0,
          "expected": 4.624008904395492e-12
        },
        {
          "variable": "k_R054",
          "time": 0.0,
          "expected": 9.729128561849475e-12
        },
        {
          "variable": "k_R055",
          "time": 0.0,
          "expected": 8.958037513385826e-12
        },
        {
          "variable": "k_R056",
          "time": 0.0,
          "expected": 3.061448623635049e-11
        },
        {
          "variable": "k_R057",
          "time": 0.0,
          "expected": 7.19875898861732e-11
        },
        {
          "variable": "k_R058",
          "time": 0.0,
          "expected": 6.423691164890288e-12
        },
        {
          "variable": "k_R059",
          "time": 0.0,
          "expected": 2.8273916461721554e-11
        },
        {
          "variable": "k_R060",
          "time": 0.0,
          "expected": 4e-11
        },
        {
          "variable": "k_R061",
          "time": 0.0,
          "expected": 9e-12
        },
        {
          "variable": "k_R062",
          "time": 0.0,
          "expected": 1.6710762870953117e-11
        },
        {
          "variable": "k_R063",
          "time": 0.0,
          "expected": 9.031208473629343e-13
        },
        {
          "variable": "k_R064",
          "time": 0.0,
          "expected": 1.15e-11
        },
        {
          "variable": "k_R065",
          "time": 0.0,
          "expected": 1.7e-11
        },
        {
          "variable": "k_R066",
          "time": 0.0,
          "expected": 2.8e-11
        },
        {
          "variable": "k_R067",
          "time": 0.0,
          "expected": 1e-11
        },
        {
          "variable": "k_R068",
          "time": 0.0,
          "expected": 1e-11
        },
        {
          "variable": "k_R069",
          "time": 0.0,
          "expected": 1e-11
        },
        {
          "variable": "k_R070",
          "time": 0.0,
          "expected": 1.2160130080656047e-13
        },
        {
          "variable": "k_R071",
          "time": 0.0,
          "expected": 2.3770019860963916e-12
        },
        {
          "variable": "k_R072",
          "time": 0.0,
          "expected": 1.0551122454553778e-10
        },
        {
          "variable": "k_R073",
          "time": 0.0,
          "expected": 5.249283753561643e-12
        },
        {
          "variable": "k_R074",
          "time": 0.0,
          "expected": 7.372897448827063e-05
        },
        {
          "variable": "k_R075",
          "time": 0.0,
          "expected": 4.7e-12
        },
        {
          "variable": "k_R076",
          "time": 0.0,
          "expected": 7.372897448827063e-05
        },
        {
          "variable": "k_R077",
          "time": 0.0,
          "expected": 7.846633021215333e-12
        },
        {
          "variable": "k_R078",
          "time": 0.0,
          "expected": 7.846633021215333e-12
        },
        {
          "variable": "k_R079",
          "time": 0.0,
          "expected": 7.846633021215333e-12
        },
        {
          "variable": "k_R080",
          "time": 0.0,
          "expected": 7.846633021215333e-12
        },
        {
          "variable": "k_R081",
          "time": 0.0,
          "expected": 7.846633021215333e-12
        },
        {
          "variable": "k_R082",
          "time": 0.0,
          "expected": 7.846633021215333e-12
        },
        {
          "variable": "k_R083",
          "time": 0.0,
          "expected": 7.846633021215333e-12
        },
        {
          "variable": "k_R084",
          "time": 0.0,
          "expected": 7.846633021215333e-12
        },
        {
          "variable": "k_R085",
          "time": 0.0,
          "expected": 7.846633021215333e-12
        },
        {
          "variable": "k_R086",
          "time": 0.0,
          "expected": 7.846633021215333e-12
        },
        {
          "variable": "k_R087",
          "time": 0.0,
          "expected": 7.846633021215333e-12
        },
        {
          "variable": "k_R088",
          "time": 0.0,
          "expected": 7.846633021215333e-12
        },
        {
          "variable": "k_R089",
          "time": 0.0,
          "expected": 7.846633021215333e-12
        },
        {
          "variable": "k_R090",
          "time": 0.0,
          "expected": 7.846633021215333e-12
        },
        {
          "variable": "k_R091",
          "time": 0.0,
          "expected": 4.728847025070594e-16
        },
        {
          "variable": "k_R092",
          "time": 0.0,
          "expected": 1.909812927188062e-15
        },
        {
          "variable": "k_R093",
          "time": 0.0,
          "expected": 4.728847025070594e-16
        },
        {
          "variable": "k_R094",
          "time": 0.0,
          "expected": 1.909812927188062e-15
        },
        {
          "variable": "k_R095",
          "time": 0.0,
          "expected": 1.909812927188062e-15
        },
        {
          "variable": "k_R096",
          "time": 0.0,
          "expected": 2.2e-11
        },
        {
          "variable": "k_R097",
          "time": 0.0,
          "expected": 7.820645453600083e-17
        },
        {
          "variable": "k_R098",
          "time": 0.0,
          "expected": 1.3880420650689461e-14
        },
        {
          "variable": "k_R099",
          "time": 0.0,
          "expected": 1.0937920061356462e-12
        },
        {
          "variable": "k_R100",
          "time": 0.0,
          "expected": 5.81e-13
        },
        {
          "variable": "k_R101",
          "time": 0.0,
          "expected": 1.2844117323100874e-18
        },
        {
          "variable": "k_R102",
          "time": 0.0,
          "expected": 8.836972413233901e-18
        },
        {
          "variable": "k_R103",
          "time": 0.0,
          "expected": 1.4114876153539734e-16
        },
        {
          "variable": "k_R104",
          "time": 0.0,
          "expected": 1.1333593686553824e-17
        },
        {
          "variable": "k_R105",
          "time": 0.0,
          "expected": 7.028259066944054e-12
        },
        {
          "variable": "k_R106",
          "time": 0.0,
          "expected": 7.028259066944054e-12
        },
        {
          "variable": "k_R107",
          "time": 0.0,
          "expected": 7.028259066944054e-12
        },
        {
          "variable": "k_R108",
          "time": 0.0,
          "expected": 7.028259066944054e-12
        },
        {
          "variable": "k_R109",
          "time": 0.0,
          "expected": 7.028259066944054e-12
        },
        {
          "variable": "k_R110",
          "time": 0.0,
          "expected": 7.028259066944054e-12
        },
        {
          "variable": "k_R111",
          "time": 0.0,
          "expected": 7.028259066944054e-12
        },
        {
          "variable": "k_R112",
          "time": 0.0,
          "expected": 7.028259066944054e-12
        },
        {
          "variable": "k_R113",
          "time": 0.0,
          "expected": 7.028259066944054e-12
        },
        {
          "variable": "k_R114",
          "time": 0.0,
          "expected": 7.028259066944054e-12
        },
        {
          "variable": "k_R115",
          "time": 0.0,
          "expected": 7.028259066944054e-12
        },
        {
          "variable": "k_R116",
          "time": 0.0,
          "expected": 7.028259066944054e-12
        },
        {
          "variable": "k_R117",
          "time": 0.0,
          "expected": 7.028259066944054e-12
        },
        {
          "variable": "k_R118",
          "time": 0.0,
          "expected": 7.028259066944054e-12
        },
        {
          "variable": "k_R119",
          "time": 0.0,
          "expected": 4.0785550654351373e-13
        },
        {
          "variable": "k_R120",
          "time": 0.0,
          "expected": 3.0052511008469435e-13
        },
        {
          "variable": "k_R121",
          "time": 0.0,
          "expected": 9.01575330254083e-14
        },
        {
          "variable": "k_R122",
          "time": 0.0,
          "expected": 7.29846695919972e-14
        },
        {
          "variable": "k_R123",
          "time": 0.0,
          "expected": 6.225162994611527e-14
        },
        {
          "variable": "k_R124",
          "time": 0.0,
          "expected": 3.0052511008469435e-13
        },
        {
          "variable": "k_R125",
          "time": 0.0,
          "expected": 3.0052511008469435e-13
        },
        {
          "variable": "k_R126",
          "time": 0.0,
          "expected": 3.64923347959986e-14
        },
        {
          "variable": "k_R127",
          "time": 0.0,
          "expected": 3.64923347959986e-14
        },
        {
          "variable": "k_R128",
          "time": 0.0,
          "expected": 2.0607436120093325e-12
        },
        {
          "variable": "k_R129",
          "time": 0.0,
          "expected": 3.64923347959986e-14
        },
        {
          "variable": "k_R130",
          "time": 0.0,
          "expected": 3.64923347959986e-14
        },
        {
          "variable": "k_R131",
          "time": 0.0,
          "expected": 2.0607436120093325e-12
        },
        {
          "variable": "k_R132",
          "time": 0.0,
          "expected": 7.29846695919972e-13
        },
        {
          "variable": "k_R133",
          "time": 0.0,
          "expected": 2.1466079291763883e-13
        },
        {
          "variable": "k_R134",
          "time": 0.0,
          "expected": 1.803150660508166e-13
        },
        {
          "variable": "k_R135",
          "time": 0.0,
          "expected": 1.5455577090069994e-13
        },
        {
          "variable": "k_R136",
          "time": 0.0,
          "expected": 7.29846695919972e-13
        },
        {
          "variable": "k_R137",
          "time": 0.0,
          "expected": 7.29846695919972e-13
        },
        {
          "variable": "k_R138",
          "time": 0.0,
          "expected": 9.01575330254083e-14
        },
        {
          "variable": "k_R139",
          "time": 0.0,
          "expected": 9.01575330254083e-14
        },
        {
          "variable": "k_R140",
          "time": 0.0,
          "expected": 2.554463435719902e-12
        },
        {
          "variable": "k_R141",
          "time": 0.0,
          "expected": 9.01575330254083e-14
        },
        {
          "variable": "k_R142",
          "time": 0.0,
          "expected": 9.01575330254083e-14
        },
        {
          "variable": "k_R143",
          "time": 0.0,
          "expected": 2.554463435719902e-12
        },
        {
          "variable": "k_R144",
          "time": 0.0,
          "expected": 7.028259066944054e-12
        },
        {
          "variable": "k_R145",
          "time": 0.0,
          "expected": 3.64923347959986e-14
        },
        {
          "variable": "k_R146",
          "time": 0.0,
          "expected": 9.01575330254083e-14
        },
        {
          "variable": "k_R147",
          "time": 0.0,
          "expected": 7.727788545034997e-16
        },
        {
          "variable": "k_R148",
          "time": 0.0,
          "expected": 7.846633021215333e-12
        },
        {
          "variable": "k_R149",
          "time": 0.0,
          "expected": 7.846633021215333e-12
        },
        {
          "variable": "k_R150",
          "time": 0.0,
          "expected": 7.028259066944054e-12
        },
        {
          "variable": "k_R151",
          "time": 0.0,
          "expected": 3.64923347959986e-14
        },
        {
          "variable": "k_R152",
          "time": 0.0,
          "expected": 9.01575330254083e-14
        },
        {
          "variable": "k_R153",
          "time": 0.0,
          "expected": 7.727788545034997e-16
        },
        {
          "variable": "k_R154",
          "time": 0.0,
          "expected": 3.64923347959986e-14
        },
        {
          "variable": "k_R155",
          "time": 0.0,
          "expected": 9.01575330254083e-14
        },
        {
          "variable": "k_R156",
          "time": 0.0,
          "expected": 7.727788545034997e-16
        }
      ]
    },
    {
      "id": "box_urban_night_rate_constants",
      "description": "Every thermal rate coefficient of RADM2 at the urban night box state (T 283 K, p 101325 Pa, M 2.593e19 and H2O 4.554e17 molec/cm3 (RH 0.900), every photolysis rate zero), against RCONST(22:156) of the WRF-conform KPP Update_RCONST (radm2_Update_Rconst.f90 generated by KPP 2.1 from the radm2.eqn of WRF v4.8.0, compiled real64 with gfortran 13.3 in the WRF build container; standalone box driver, dump box_urban_night.json). Pointwise, no time step. Expected agreement is binary64 round-off (the same double-precision arithmetic in both), so the tolerance is the tolerance contract for a double-precision reference rel 1e-9; the single-precision literals of radm2.eqn (.20946e0, .78084, -2.3) are bound as their binary64 values so no rounding residual remains. The one exception is k_R043 (N2O5 + aerosol water, rc_n2o5), which WRF evaluates in SINGLE precision in kpp_mechd_ibu_radm2.inc: tolerance rel 1e-6 (measured residual ~1e-7). RH is not an input: the test sets T, p, M and H2O, and RH is asserted first, against the RH the box driver was given, to pin the WRF relative-humidity formula of kpp_mechd_ibu_radm2.inc (rel 1e-12: the same binary64 arithmetic on both sides). The photolysis frequencies are not set because no rate coefficient here reads them. The box states are typical mixing-ratio boxes written by make_states.py; there is no WRF-Chem run behind them. make_states.py builds M and H2O from a nominal T, p and RH (0.55, 0.80, 0.90) and then hands the box driver the RH that WRF's formula gives back from that M, H2O, T and p, the same RH this document derives, so the box driver and the document see one water-vapour state.",
      "parameter_overrides": {
        "T": 283.0,
        "p": 101325.0,
        "M": 2.5928656334400664e+19,
        "H2O": 4.5539885211985715e+17
      },
      "time_span": {
        "start": 0,
        "end": 1
      },
      "tolerance": {
        "rel": 1e-09
      },
      "assertions": [
        {
          "variable": "RH",
          "time": 0.0,
          "expected": 0.899994691897405,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "k_R022",
          "time": 0.0,
          "expected": 3.726511405005005e-15
        },
        {
          "variable": "k_R023",
          "time": 0.0,
          "expected": 9.932681138133424e-12
        },
        {
          "variable": "k_R024",
          "time": 0.0,
          "expected": 2.931570316410466e-11
        },
        {
          "variable": "k_R025",
          "time": 0.0,
          "expected": 2.2e-10
        },
        {
          "variable": "k_R026",
          "time": 0.0,
          "expected": 1.4209432336076987e-14
        },
        {
          "variable": "k_R027",
          "time": 0.0,
          "expected": 5.775466572479997e-14
        },
        {
          "variable": "k_R028",
          "time": 0.0,
          "expected": 1.8796974264314436e-15
        },
        {
          "variable": "k_R029",
          "time": 0.0,
          "expected": 8.639885727568673e-12
        },
        {
          "variable": "k_R030",
          "time": 0.0,
          "expected": 1.6063734598802963e-12
        },
        {
          "variable": "k_R031",
          "time": 0.0,
          "expected": 0.0143288117500859
        },
        {
          "variable": "k_R032",
          "time": 0.0,
          "expected": 3.4051033818817526e-12
        },
        {
          "variable": "k_R033",
          "time": 0.0,
          "expected": 1.1334416996007313e-29
        },
        {
          "variable": "k_R034",
          "time": 0.0,
          "expected": 1.6277662684966163e-12
        },
        {
          "variable": "k_R035",
          "time": 0.0,
          "expected": 5.402588730433619e-12
        },
        {
          "variable": "k_R036",
          "time": 0.0,
          "expected": 4.497364344321946e-39
        },
        {
          "variable": "k_R037",
          "time": 0.0,
          "expected": 2.0398787036908492e-17
        },
        {
          "variable": "k_R038",
          "time": 0.0,
          "expected": 2.8882869824590716e-11
        },
        {
          "variable": "k_R039",
          "time": 0.0,
          "expected": 3.238697248699157e-16
        },
        {
          "variable": "k_R040",
          "time": 0.0,
          "expected": 2.5e-12
        },
        {
          "variable": "k_R041",
          "time": 0.0,
          "expected": 1.322757221435577e-12
        },
        {
          "variable": "k_R042",
          "time": 0.0,
          "expected": 0.007805808373474311
        },
        {
          "variable": "k_R043",
          "time": 0.0,
          "expected": 0.0033333334140479565,
          "tolerance": {
            "rel": 1e-06
          }
        },
        {
          "variable": "k_R044",
          "time": 0.0,
          "expected": 1.3033611492621531e-11
        },
        {
          "variable": "k_R045",
          "time": 0.0,
          "expected": 1.7554728365512021e-13
        },
        {
          "variable": "k_R046",
          "time": 0.0,
          "expected": 4.978459213144045e-12
        },
        {
          "variable": "k_R047",
          "time": 0.0,
          "expected": 1.0368549642379886e-10
        },
        {
          "variable": "k_R048",
          "time": 0.0,
          "expected": 9.473252145596131e-13
        },
        {
          "variable": "k_R049",
          "time": 0.0,
          "expected": 2.4485998919940483e-13
        },
        {
          "variable": "k_R050",
          "time": 0.0,
          "expected": 6.043068894350007e-15
        },
        {
          "variable": "k_R051",
          "time": 0.0,
          "expected": 2.285213760699054e-13
        },
        {
          "variable": "k_R052",
          "time": 0.0,
          "expected": 2.3588917251399846e-12
        },
        {
          "variable": "k_R053",
          "time": 0.0,
          "expected": 4.517461936942715e-12
        },
        {
          "variable": "k_R054",
          "time": 0.0,
          "expected": 9.504948815301434e-12
        },
        {
          "variable": "k_R055",
          "time": 0.0,
          "expected": 9.186772354823863e-12
        },
        {
          "variable": "k_R056",
          "time": 0.0,
          "expected": 3.157583242371404e-11
        },
        {
          "variable": "k_R057",
          "time": 0.0,
          "expected": 7.44533734773806e-11
        },
        {
          "variable": "k_R058",
          "time": 0.0,
          "expected": 6.551843968977161e-12
        },
        {
          "variable": "k_R059",
          "time": 0.0,
          "expected": 2.8475837338628132e-11
        },
        {
          "variable": "k_R060",
          "time": 0.0,
          "expected": 4e-11
        },
        {
          "variable": "k_R061",
          "time": 0.0,
          "expected": 9e-12
        },
        {
          "variable": "k_R062",
          "time": 0.0,
          "expected": 1.697527283059636e-11
        },
        {
          "variable": "k_R063",
          "time": 0.0,
          "expected": 8.627742719748066e-13
        },
        {
          "variable": "k_R064",
          "time": 0.0,
          "expected": 1.15e-11
        },
        {
          "variable": "k_R065",
          "time": 0.0,
          "expected": 1.7e-11
        },
        {
          "variable": "k_R066",
          "time": 0.0,
          "expected": 2.8e-11
        },
        {
          "variable": "k_R067",
          "time": 0.0,
          "expected": 1e-11
        },
        {
          "variable": "k_R068",
          "time": 0.0,
          "expected": 1e-11
        },
        {
          "variable": "k_R069",
          "time": 0.0,
          "expected": 1e-11
        },
        {
          "variable": "k_R070",
          "time": 0.0,
          "expected": 1.142606880349527e-13
        },
        {
          "variable": "k_R071",
          "time": 0.0,
          "expected": 2.2995485370861486e-12
        },
        {
          "variable": "k_R072",
          "time": 0.0,
          "expected": 1.0819207655860168e-10
        },
        {
          "variable": "k_R073",
          "time": 0.0,
          "expected": 5.307895287158433e-12
        },
        {
          "variable": "k_R074",
          "time": 0.0,
          "expected": 3.212317536202336e-05
        },
        {
          "variable": "k_R075",
          "time": 0.0,
          "expected": 4.7e-12
        },
        {
          "variable": "k_R076",
          "time": 0.0,
          "expected": 3.212317536202336e-05
        },
        {
          "variable": "k_R077",
          "time": 0.0,
          "expected": 7.933758857859381e-12
        },
        {
          "variable": "k_R078",
          "time": 0.0,
          "expected": 7.933758857859381e-12
        },
        {
          "variable": "k_R079",
          "time": 0.0,
          "expected": 7.933758857859381e-12
        },
        {
          "variable": "k_R080",
          "time": 0.0,
          "expected": 7.933758857859381e-12
        },
        {
          "variable": "k_R081",
          "time": 0.0,
          "expected": 7.933758857859381e-12
        },
        {
          "variable": "k_R082",
          "time": 0.0,
          "expected": 7.933758857859381e-12
        },
        {
          "variable": "k_R083",
          "time": 0.0,
          "expected": 7.933758857859381e-12
        },
        {
          "variable": "k_R084",
          "time": 0.0,
          "expected": 7.933758857859381e-12
        },
        {
          "variable": "k_R085",
          "time": 0.0,
          "expected": 7.933758857859381e-12
        },
        {
          "variable": "k_R086",
          "time": 0.0,
          "expected": 7.933758857859381e-12
        },
        {
          "variable": "k_R087",
          "time": 0.0,
          "expected": 7.933758857859381e-12
        },
        {
          "variable": "k_R088",
          "time": 0.0,
          "expected": 7.933758857859381e-12
        },
        {
          "variable": "k_R089",
          "time": 0.0,
          "expected": 7.933758857859381e-12
        },
        {
          "variable": "k_R090",
          "time": 0.0,
          "expected": 7.933758857859381e-12
        },
        {
          "variable": "k_R091",
          "time": 0.0,
          "expected": 4.16797348370772e-16
        },
        {
          "variable": "k_R092",
          "time": 0.0,
          "expected": 1.6996912159293588e-15
        },
        {
          "variable": "k_R093",
          "time": 0.0,
          "expected": 4.16797348370772e-16
        },
        {
          "variable": "k_R094",
          "time": 0.0,
          "expected": 1.6996912159293588e-15
        },
        {
          "variable": "k_R095",
          "time": 0.0,
          "expected": 1.6996912159293588e-15
        },
        {
          "variable": "k_R096",
          "time": 0.0,
          "expected": 2.2e-11
        },
        {
          "variable": "k_R097",
          "time": 0.0,
          "expected": 6.536819534044092e-17
        },
        {
          "variable": "k_R098",
          "time": 0.0,
          "expected": 1.2357056763853329e-14
        },
        {
          "variable": "k_R099",
          "time": 0.0,
          "expected": 1.0302871484073928e-12
        },
        {
          "variable": "k_R100",
          "time": 0.0,
          "expected": 5.81e-13
        },
        {
          "variable": "k_R101",
          "time": 0.0,
          "expected": 1.092834744096461e-18
        },
        {
          "variable": "k_R102",
          "time": 0.0,
          "expected": 7.766421962281843e-18
        },
        {
          "variable": "k_R103",
          "time": 0.0,
          "expected": 1.31647059424982e-16
        },
        {
          "variable": "k_R104",
          "time": 0.0,
          "expected": 1.001696681156916e-17
        },
        {
          "variable": "k_R105",
          "time": 0.0,
          "expected": 7.61172421774007e-12
        },
        {
          "variable": "k_R106",
          "time": 0.0,
          "expected": 7.61172421774007e-12
        },
        {
          "variable": "k_R107",
          "time": 0.0,
          "expected": 7.61172421774007e-12
        },
        {
          "variable": "k_R108",
          "time": 0.0,
          "expected": 7.61172421774007e-12
        },
        {
          "variable": "k_R109",
          "time": 0.0,
          "expected": 7.61172421774007e-12
        },
        {
          "variable": "k_R110",
          "time": 0.0,
          "expected": 7.61172421774007e-12
        },
        {
          "variable": "k_R111",
          "time": 0.0,
          "expected": 7.61172421774007e-12
        },
        {
          "variable": "k_R112",
          "time": 0.0,
          "expected": 7.61172421774007e-12
        },
        {
          "variable": "k_R113",
          "time": 0.0,
          "expected": 7.61172421774007e-12
        },
        {
          "variable": "k_R114",
          "time": 0.0,
          "expected": 7.61172421774007e-12
        },
        {
          "variable": "k_R115",
          "time": 0.0,
          "expected": 7.61172421774007e-12
        },
        {
          "variable": "k_R116",
          "time": 0.0,
          "expected": 7.61172421774007e-12
        },
        {
          "variable": "k_R117",
          "time": 0.0,
          "expected": 7.61172421774007e-12
        },
        {
          "variable": "k_R118",
          "time": 0.0,
          "expected": 7.61172421774007e-12
        },
        {
          "variable": "k_R119",
          "time": 0.0,
          "expected": 4.133973476024504e-13
        },
        {
          "variable": "k_R120",
          "time": 0.0,
          "expected": 3.0460857191759504e-13
        },
        {
          "variable": "k_R121",
          "time": 0.0,
          "expected": 9.13825715752785e-14
        },
        {
          "variable": "k_R122",
          "time": 0.0,
          "expected": 7.397636746570165e-14
        },
        {
          "variable": "k_R123",
          "time": 0.0,
          "expected": 6.309748989721612e-14
        },
        {
          "variable": "k_R124",
          "time": 0.0,
          "expected": 3.0460857191759504e-13
        },
        {
          "variable": "k_R125",
          "time": 0.0,
          "expected": 3.0460857191759504e-13
        },
        {
          "variable": "k_R126",
          "time": 0.0,
          "expected": 3.698818373285082e-14
        },
        {
          "variable": "k_R127",
          "time": 0.0,
          "expected": 3.698818373285082e-14
        },
        {
          "variable": "k_R128",
          "time": 0.0,
          "expected": 2.0887444931492227e-12
        },
        {
          "variable": "k_R129",
          "time": 0.0,
          "expected": 3.698818373285082e-14
        },
        {
          "variable": "k_R130",
          "time": 0.0,
          "expected": 3.698818373285082e-14
        },
        {
          "variable": "k_R131",
          "time": 0.0,
          "expected": 2.0887444931492227e-12
        },
        {
          "variable": "k_R132",
          "time": 0.0,
          "expected": 7.397636746570165e-13
        },
        {
          "variable": "k_R133",
          "time": 0.0,
          "expected": 2.1757755136971074e-13
        },
        {
          "variable": "k_R134",
          "time": 0.0,
          "expected": 1.82765143150557e-13
        },
        {
          "variable": "k_R135",
          "time": 0.0,
          "expected": 1.5665583698619173e-13
        },
        {
          "variable": "k_R136",
          "time": 0.0,
          "expected": 7.397636746570165e-13
        },
        {
          "variable": "k_R137",
          "time": 0.0,
          "expected": 7.397636746570165e-13
        },
        {
          "variable": "k_R138",
          "time": 0.0,
          "expected": 9.13825715752785e-14
        },
        {
          "variable": "k_R139",
          "time": 0.0,
          "expected": 9.13825715752785e-14
        },
        {
          "variable": "k_R140",
          "time": 0.0,
          "expected": 2.5891728612995578e-12
        },
        {
          "variable": "k_R141",
          "time": 0.0,
          "expected": 9.13825715752785e-14
        },
        {
          "variable": "k_R142",
          "time": 0.0,
          "expected": 9.13825715752785e-14
        },
        {
          "variable": "k_R143",
          "time": 0.0,
          "expected": 2.5891728612995578e-12
        },
        {
          "variable": "k_R144",
          "time": 0.0,
          "expected": 7.61172421774007e-12
        },
        {
          "variable": "k_R145",
          "time": 0.0,
          "expected": 3.698818373285082e-14
        },
        {
          "variable": "k_R146",
          "time": 0.0,
          "expected": 9.13825715752785e-14
        },
        {
          "variable": "k_R147",
          "time": 0.0,
          "expected": 7.832791849309586e-16
        },
        {
          "variable": "k_R148",
          "time": 0.0,
          "expected": 7.933758857859381e-12
        },
        {
          "variable": "k_R149",
          "time": 0.0,
          "expected": 7.933758857859381e-12
        },
        {
          "variable": "k_R150",
          "time": 0.0,
          "expected": 7.61172421774007e-12
        },
        {
          "variable": "k_R151",
          "time": 0.0,
          "expected": 3.698818373285082e-14
        },
        {
          "variable": "k_R152",
          "time": 0.0,
          "expected": 9.13825715752785e-14
        },
        {
          "variable": "k_R153",
          "time": 0.0,
          "expected": 7.832791849309586e-16
        },
        {
          "variable": "k_R154",
          "time": 0.0,
          "expected": 3.698818373285082e-14
        },
        {
          "variable": "k_R155",
          "time": 0.0,
          "expected": 9.13825715752785e-14
        },
        {
          "variable": "k_R156",
          "time": 0.0,
          "expected": 7.832791849309586e-16
        }
      ]
    },
    {
      "id": "wrfchem_scm_midtrop_rate_constants",
      "description": "Every thermal rate coefficient of RADM2 at a real WRF-Chem state: the mid-troposphere level k = 45 (T = 254.674 K, p = 490.1 hPa, M = 1.3939e19 and H2O = 1.027e16 molec/cm3, RH = 0.156, late-afternoon TUV/Madronich photolysis) of the first chemistry call of an idealized single-column WRF-Chem run: WRF v4.8.0 em_scm_xy ideal case, 1999-10-22 19:00 UTC, 59 levels, chem_opt = 101 (RADM2 KPP), phot_opt = 1 (Madronich TUV), emiss_opt = 0, chem_in_opt = 0 (species from the built-in idealized profiles of chem/module_input_chem_data.F), no dry deposition; ctessum-claude/WRF branch earthsciml-instrumented-chem, commit 2ce0388 (v4.8.0-6-g2ce03882). Expected values are RCONST(22:156) written by the fork's chem/KPP/inc/radm2/kpp_mechd_*_radm2.inc hooks straight after Update_Rconst (dump esm_dump_radm2_kpp_1.json, level k = 45); T, p, M and H2O are that dump's temp, p_phy, c_m and c_h2o. Pointwise, no time step. Unlike the three box regimes this state comes from a full WRF-Chem column: T, M and the photolysis frequencies are whatever the model's own meteorology and radiative transfer produced, and T = 254.7 K sits well outside the 283-298 K of the box regimes, so the Arrhenius and Troe forms are exercised far from them. WRF is built single precision (RWORDSIZE = 4), but the KPP interface promotes t_phy, rho_phy and the photolysis rates to KIND = dp = real64 before Update_Rconst, so every rate law is evaluated in double there exactly as in the box driver; the dumped inputs are bound here as their exact binary64 values, hence the same rel 1e-9 double-precision contract as the box regimes (largest measured residual over the 134 double-precision coefficients: 6.2e-16, one ulp). The exception is again k_R043 (N2O5 + aerosol water): WRF evaluates rc_n2o5 in single precision from a single-precision RH computed from qv, p_phy and T, and does not carry that RH out of the loop. This document derives RH in binary64 from H2O and M (qv = H2O/M mw_h2o/mw_air, exact up to the single-precision products WRF forms c_h2o and c_m with); the RH assertion is against the float32 reconstruction from the dumped qv, p_phy and T (agreement 4e-8), and the derived k_R043 reproduces WRF's own rc_n2o5 to 6e-8, so both carry rel 1e-6. Cross-check: at this state all 156 RCONST entries of the WRF-Chem run agree bit-for-bit with the standalone real64 KPP box driver fed the same T, C_M, C_H2O, RH and jv, which is what ties this regime to the other three, and what the wrfchem_scm_midtrop tendency and trajectory tests build on.",
      "parameter_overrides": {
        "T": 254.67430114746094,
        "p": 49010.94140625,
        "M": 1.393857377650239e+19,
        "H2O": 1.0274926497890304e+16
      },
      "time_span": {
        "start": 0,
        "end": 1
      },
      "tolerance": {
        "rel": 1e-09
      },
      "assertions": [
        {
          "variable": "RH",
          "time": 0.0,
          "expected": 0.15637393295764923,
          "tolerance": {
            "rel": 1e-06
          }
        },
        {
          "variable": "k_R022",
          "time": 0.0,
          "expected": 2.553193897851265e-15
        },
        {
          "variable": "k_R023",
          "time": 0.0,
          "expected": 1.0412346233502217e-11
        },
        {
          "variable": "k_R024",
          "time": 0.0,
          "expected": 3.047106292962544e-11
        },
        {
          "variable": "k_R025",
          "time": 0.0,
          "expected": 2.2e-10
        },
        {
          "variable": "k_R026",
          "time": 0.0,
          "expected": 8.19631823716641e-15
        },
        {
          "variable": "k_R027",
          "time": 0.0,
          "expected": 3.991571402039555e-14
        },
        {
          "variable": "k_R028",
          "time": 0.0,
          "expected": 1.5443503610929227e-15
        },
        {
          "variable": "k_R029",
          "time": 0.0,
          "expected": 9.49450248803344e-12
        },
        {
          "variable": "k_R030",
          "time": 0.0,
          "expected": 1.4965203427334097e-12
        },
        {
          "variable": "k_R031",
          "time": 0.0,
          "expected": 0.00018407220789110187
        },
        {
          "variable": "k_R032",
          "time": 0.0,
          "expected": 3.5627017641608453e-12
        },
        {
          "variable": "k_R033",
          "time": 0.0,
          "expected": 2.815487799495812e-29
        },
        {
          "variable": "k_R034",
          "time": 0.0,
          "expected": 1.5047182882908575e-12
        },
        {
          "variable": "k_R035",
          "time": 0.0,
          "expected": 4.677281844951951e-12
        },
        {
          "variable": "k_R036",
          "time": 0.0,
          "expected": 5.538864131759072e-39
        },
        {
          "variable": "k_R037",
          "time": 0.0,
          "expected": 7.636489865652444e-18
        },
        {
          "variable": "k_R038",
          "time": 0.0,
          "expected": 3.0636770037826265e-11
        },
        {
          "variable": "k_R039",
          "time": 0.0,
          "expected": 1.997233098980286e-16
        },
        {
          "variable": "k_R040",
          "time": 0.0,
          "expected": 2.5e-12
        },
        {
          "variable": "k_R041",
          "time": 0.0,
          "expected": 1.3708979856198328e-12
        },
        {
          "variable": "k_R042",
          "time": 0.0,
          "expected": 9.91469947727236e-05
        },
        {
          "variable": "k_R043",
          "time": 0.0,
          "expected": 3.3443742722738534e-05,
          "tolerance": {
            "rel": 1e-06
          }
        },
        {
          "variable": "k_R044",
          "time": 0.0,
          "expected": 1.2560313119788338e-11
        },
        {
          "variable": "k_R045",
          "time": 0.0,
          "expected": 2.5019472058230635e-13
        },
        {
          "variable": "k_R046",
          "time": 0.0,
          "expected": 5.780360960266008e-12
        },
        {
          "variable": "k_R047",
          "time": 0.0,
          "expected": 1.1349464825705583e-10
        },
        {
          "variable": "k_R048",
          "time": 0.0,
          "expected": 8.749589024394499e-13
        },
        {
          "variable": "k_R049",
          "time": 0.0,
          "expected": 2.00994272161334e-13
        },
        {
          "variable": "k_R050",
          "time": 0.0,
          "expected": 2.9592326615677176e-15
        },
        {
          "variable": "k_R051",
          "time": 0.0,
          "expected": 1.5543199076671823e-13
        },
        {
          "variable": "k_R052",
          "time": 0.0,
          "expected": 1.9078249542544693e-12
        },
        {
          "variable": "k_R053",
          "time": 0.0,
          "expected": 3.890760482709548e-12
        },
        {
          "variable": "k_R054",
          "time": 0.0,
          "expected": 8.186339975180782e-12
        },
        {
          "variable": "k_R055",
          "time": 0.0,
          "expected": 1.0797275220339933e-11
        },
        {
          "variable": "k_R056",
          "time": 0.0,
          "expected": 3.849281374579783e-11
        },
        {
          "variable": "k_R057",
          "time": 0.0,
          "expected": 9.238256585795889e-11
        },
        {
          "variable": "k_R058",
          "time": 0.0,
          "expected": 7.435734370232975e-12
        },
        {
          "variable": "k_R059",
          "time": 0.0,
          "expected": 2.980409051287694e-11
        },
        {
          "variable": "k_R060",
          "time": 0.0,
          "expected": 4e-11
        },
        {
          "variable": "k_R061",
          "time": 0.0,
          "expected": 9e-12
        },
        {
          "variable": "k_R062",
          "time": 0.0,
          "expected": 1.8772059620293012e-11
        },
        {
          "variable": "k_R063",
          "time": 0.0,
          "expected": 6.437799366072661e-13
        },
        {
          "variable": "k_R064",
          "time": 0.0,
          "expected": 1.15e-11
        },
        {
          "variable": "k_R065",
          "time": 0.0,
          "expected": 1.7e-11
        },
        {
          "variable": "k_R066",
          "time": 0.0,
          "expected": 2.8e-11
        },
        {
          "variable": "k_R067",
          "time": 0.0,
          "expected": 1e-11
        },
        {
          "variable": "k_R068",
          "time": 0.0,
          "expected": 1e-11
        },
        {
          "variable": "k_R069",
          "time": 0.0,
          "expected": 1e-11
        },
        {
          "variable": "k_R070",
          "time": 0.0,
          "expected": 7.771599538335912e-14
        },
        {
          "variable": "k_R071",
          "time": 0.0,
          "expected": 1.8598293579210236e-12
        },
        {
          "variable": "k_R072",
          "time": 0.0,
          "expected": 1.270589624774473e-10
        },
        {
          "variable": "k_R073",
          "time": 0.0,
          "expected": 5.699230099911499e-12
        },
        {
          "variable": "k_R074",
          "time": 0.0,
          "expected": 1.5676243475897762e-07
        },
        {
          "variable": "k_R075",
          "time": 0.0,
          "expected": 4.7e-12
        },
        {
          "variable": "k_R076",
          "time": 0.0,
          "expected": 1.5676243475897762e-07
        },
        {
          "variable": "k_R077",
          "time": 0.0,
          "expected": 8.515343209628439e-12
        },
        {
          "variable": "k_R078",
          "time": 0.0,
          "expected": 8.515343209628439e-12
        },
        {
          "variable": "k_R079",
          "time": 0.0,
          "expected": 8.515343209628439e-12
        },
        {
          "variable": "k_R080",
          "time": 0.0,
          "expected": 8.515343209628439e-12
        },
        {
          "variable": "k_R081",
          "time": 0.0,
          "expected": 8.515343209628439e-12
        },
        {
          "variable": "k_R082",
          "time": 0.0,
          "expected": 8.515343209628439e-12
        },
        {
          "variable": "k_R083",
          "time": 0.0,
          "expected": 8.515343209628439e-12
        },
        {
          "variable": "k_R084",
          "time": 0.0,
          "expected": 8.515343209628439e-12
        },
        {
          "variable": "k_R085",
          "time": 0.0,
          "expected": 8.515343209628439e-12
        },
        {
          "variable": "k_R086",
          "time": 0.0,
          "expected": 8.515343209628439e-12
        },
        {
          "variable": "k_R087",
          "time": 0.0,
          "expected": 8.515343209628439e-12
        },
        {
          "variable": "k_R088",
          "time": 0.0,
          "expected": 8.515343209628439e-12
        },
        {
          "variable": "k_R089",
          "time": 0.0,
          "expected": 8.515343209628439e-12
        },
        {
          "variable": "k_R090",
          "time": 0.0,
          "expected": 8.515343209628439e-12
        },
        {
          "variable": "k_R091",
          "time": 0.0,
          "expected": 1.8563369568359767e-16
        },
        {
          "variable": "k_R092",
          "time": 0.0,
          "expected": 8.055082654945737e-16
        },
        {
          "variable": "k_R093",
          "time": 0.0,
          "expected": 1.8563369568359767e-16
        },
        {
          "variable": "k_R094",
          "time": 0.0,
          "expected": 8.055082654945737e-16
        },
        {
          "variable": "k_R095",
          "time": 0.0,
          "expected": 8.055082654945737e-16
        },
        {
          "variable": "k_R096",
          "time": 0.0,
          "expected": 2.2e-11
        },
        {
          "variable": "k_R097",
          "time": 0.0,
          "expected": 2.0723184979845597e-17
        },
        {
          "variable": "k_R098",
          "time": 0.0,
          "expected": 5.86770719579129e-15
        },
        {
          "variable": "k_R099",
          "time": 0.0,
          "expected": 7.023299075481664e-13
        },
        {
          "variable": "k_R100",
          "time": 0.0,
          "expected": 5.81e-13
        },
        {
          "variable": "k_R101",
          "time": 0.0,
          "expected": 3.8827812853454716e-19
        },
        {
          "variable": "k_R102",
          "time": 0.0,
          "expected": 3.3957107358850148e-18
        },
        {
          "variable": "k_R103",
          "time": 0.0,
          "expected": 8.423913184306872e-17
        },
        {
          "variable": "k_R104",
          "time": 0.0,
          "expected": 4.540972674894058e-18
        },
        {
          "variable": "k_R105",
          "time": 0.0,
          "expected": 1.2687397254646713e-11
        },
        {
          "variable": "k_R106",
          "time": 0.0,
          "expected": 1.2687397254646713e-11
        },
        {
          "variable": "k_R107",
          "time": 0.0,
          "expected": 1.2687397254646713e-11
        },
        {
          "variable": "k_R108",
          "time": 0.0,
          "expected": 1.2687397254646713e-11
        },
        {
          "variable": "k_R109",
          "time": 0.0,
          "expected": 1.2687397254646713e-11
        },
        {
          "variable": "k_R110",
          "time": 0.0,
          "expected": 1.2687397254646713e-11
        },
        {
          "variable": "k_R111",
          "time": 0.0,
          "expected": 1.2687397254646713e-11
        },
        {
          "variable": "k_R112",
          "time": 0.0,
          "expected": 1.2687397254646713e-11
        },
        {
          "variable": "k_R113",
          "time": 0.0,
          "expected": 1.2687397254646713e-11
        },
        {
          "variable": "k_R114",
          "time": 0.0,
          "expected": 1.2687397254646713e-11
        },
        {
          "variable": "k_R115",
          "time": 0.0,
          "expected": 1.2687397254646713e-11
        },
        {
          "variable": "k_R116",
          "time": 0.0,
          "expected": 1.2687397254646713e-11
        },
        {
          "variable": "k_R117",
          "time": 0.0,
          "expected": 1.2687397254646713e-11
        },
        {
          "variable": "k_R118",
          "time": 0.0,
          "expected": 1.2687397254646713e-11
        },
        {
          "variable": "k_R119",
          "time": 0.0,
          "expected": 4.507318166136446e-13
        },
        {
          "variable": "k_R120",
          "time": 0.0,
          "expected": 3.321181806626855e-13
        },
        {
          "variable": "k_R121",
          "time": 0.0,
          "expected": 9.963545419880565e-14
        },
        {
          "variable": "k_R122",
          "time": 0.0,
          "expected": 8.065727244665219e-14
        },
        {
          "variable": "k_R123",
          "time": 0.0,
          "expected": 6.879590885155629e-14
        },
        {
          "variable": "k_R124",
          "time": 0.0,
          "expected": 3.321181806626855e-13
        },
        {
          "variable": "k_R125",
          "time": 0.0,
          "expected": 3.321181806626855e-13
        },
        {
          "variable": "k_R126",
          "time": 0.0,
          "expected": 4.0328636223326096e-14
        },
        {
          "variable": "k_R127",
          "time": 0.0,
          "expected": 4.0328636223326096e-14
        },
        {
          "variable": "k_R128",
          "time": 0.0,
          "expected": 2.277381810258415e-12
        },
        {
          "variable": "k_R129",
          "time": 0.0,
          "expected": 4.0328636223326096e-14
        },
        {
          "variable": "k_R130",
          "time": 0.0,
          "expected": 4.0328636223326096e-14
        },
        {
          "variable": "k_R131",
          "time": 0.0,
          "expected": 2.277381810258415e-12
        },
        {
          "variable": "k_R132",
          "time": 0.0,
          "expected": 8.065727244665219e-13
        },
        {
          "variable": "k_R133",
          "time": 0.0,
          "expected": 2.3722727190191824e-13
        },
        {
          "variable": "k_R134",
          "time": 0.0,
          "expected": 1.992709083976113e-13
        },
        {
          "variable": "k_R135",
          "time": 0.0,
          "expected": 1.708036357693811e-13
        },
        {
          "variable": "k_R136",
          "time": 0.0,
          "expected": 8.065727244665219e-13
        },
        {
          "variable": "k_R137",
          "time": 0.0,
          "expected": 8.065727244665219e-13
        },
        {
          "variable": "k_R138",
          "time": 0.0,
          "expected": 9.963545419880565e-14
        },
        {
          "variable": "k_R139",
          "time": 0.0,
          "expected": 9.963545419880565e-14
        },
        {
          "variable": "k_R140",
          "time": 0.0,
          "expected": 2.8230045356328266e-12
        },
        {
          "variable": "k_R141",
          "time": 0.0,
          "expected": 9.963545419880565e-14
        },
        {
          "variable": "k_R142",
          "time": 0.0,
          "expected": 9.963545419880565e-14
        },
        {
          "variable": "k_R143",
          "time": 0.0,
          "expected": 2.8230045356328266e-12
        },
        {
          "variable": "k_R144",
          "time": 0.0,
          "expected": 1.2687397254646713e-11
        },
        {
          "variable": "k_R145",
          "time": 0.0,
          "expected": 4.0328636223326096e-14
        },
        {
          "variable": "k_R146",
          "time": 0.0,
          "expected": 9.963545419880565e-14
        },
        {
          "variable": "k_R147",
          "time": 0.0,
          "expected": 8.540181788469055e-16
        },
        {
          "variable": "k_R148",
          "time": 0.0,
          "expected": 8.515343209628439e-12
        },
        {
          "variable": "k_R149",
          "time": 0.0,
          "expected": 8.515343209628439e-12
        },
        {
          "variable": "k_R150",
          "time": 0.0,
          "expected": 1.2687397254646713e-11
        },
        {
          "variable": "k_R151",
          "time": 0.0,
          "expected": 4.0328636223326096e-14
        },
        {
          "variable": "k_R152",
          "time": 0.0,
          "expected": 9.963545419880565e-14
        },
        {
          "variable": "k_R153",
          "time": 0.0,
          "expected": 8.540181788469055e-16
        },
        {
          "variable": "k_R154",
          "time": 0.0,
          "expected": 4.0328636223326096e-14
        },
        {
          "variable": "k_R155",
          "time": 0.0,
          "expected": 9.963545419880565e-14
        },
        {
          "variable": "k_R156",
          "time": 0.0,
          "expected": 8.540181788469055e-16
        }
      ]
    }
  ]
}
```

</details>
