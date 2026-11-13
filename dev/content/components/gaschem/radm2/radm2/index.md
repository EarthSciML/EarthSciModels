---
title: "RADM2"
slug: "radm2"
domains: ["gaschem"]
component_types: ["reaction_system"]
subdomains: ["radm2"]
domain: "gaschem"
subdomain: "radm2"
component_type: "reaction_system"
esm_version: "1.1.0"
esm_path: "components/gaschem/radm2/radm2.esm"
reference: "10.1029/JD095iD10p16343"
description: "The RADM2 gas-phase mechanism (Stockwell et al. 1990) exactly as WRF-Chem chem_opt = 101 (the KPP build of RADM2; chem_opt = 1 is the older hand-coded RADM2 of chem/module_radm.F, a different code path) integrates it: the 156 reactions of radm2.eqn (21 photolysis + 135 thermal) over 59 variable species, translated from chem/KPP/mechanisms/radm2/radm2.eqn and radm2.spc of WRF v4.8.0 by a translation script. The reaction system has 157 entries, one more than the .eqn, because the negative product \"-0.9 OH\" of reaction 60 is written as the extra entry R060x. The document holds three components. The model RADM2RateConstants evaluates every thermal rate coefficient from the hand-authored WRF rate-law templates (radm2_ratelaws.esm) with the .eqn coefficients bound once, and exposes them as observeds tested at t = 0 against the real64 KPP box driver and against a real WRF-Chem chem_opt = 101 single-column run. The reaction system RADM2 carries the stoichiometry only, each rate being a scoped reference to that model (photolysis rates are its parameters j_*). The model RADM2Tendencies exposes the mass-action tendency of every species as an observed, so the right-hand side is tested at t = 0 independently of any integrator. Species are in molec/cm^3 (the KPP units; WRF converts its ppmV chem array with conv = 1e-6 dens2con_a rho). The two KPP fixed species are not species here: air (M) and water vapour (H2O) are the parameters RADM2RateConstants.M and RADM2RateConstants.H2O, the single source of each for the whole document. The rate laws read them as arguments, the five reactions in which KPP multiplies by a fixed species (R022, R024 and R036 by M; R025 and R033 by H2O) multiply their rate by them, and the relative humidity of the heterogeneous N2O5 rate is derived from H2O, M, T and p with WRF's own formula, so no override can leave two copies of one quantity disagreeing. Mass action is that of esm-spec 7.4, v = k prod S_i^n_i with no 1/n_i! factor, which is also what KPP generates. The eight reactions with a doubled substrate (R032 and R033 HO2 + HO2, R036 NO + NO, R119 MO2 + MO2, R140 ACO3 + ACO3, R147 XO2 + XO2, R153 XNO2 + XNO2, R156 OLN + OLN) carry their .eqn coefficients unchanged on that understanding: a binding that lowers this document to Catalyst.jl must build it with combinatoric_ratelaws = false, or those eight rates come out at half the KPP value. Single-precision literals of radm2.eqn and of the WRF-Chem coupler (.20946e0, .78084, -2.3, the constants of rc_n2o5 and of the relative humidity) are transcribed as the binary64 value of the single-precision number, since that is what the Fortran evaluates."
tags: ["gaschem", "radm2", "reaction_system", "wrf-chem", "kpp", "mechanism"]
---

## Description

The RADM2 gas-phase mechanism (Stockwell et al. 1990) exactly as WRF-Chem chem_opt = 101 (the KPP build of RADM2; chem_opt = 1 is the older hand-coded RADM2 of chem/module_radm.F, a different code path) integrates it: the 156 reactions of radm2.eqn (21 photolysis + 135 thermal) over 59 variable species, translated from chem/KPP/mechanisms/radm2/radm2.eqn and radm2.spc of WRF v4.8.0 by a translation script. The reaction system has 157 entries, one more than the .eqn, because the negative product "-0.9 OH" of reaction 60 is written as the extra entry R060x. The document holds three components. The model RADM2RateConstants evaluates every thermal rate coefficient from the hand-authored WRF rate-law templates (radm2_ratelaws.esm) with the .eqn coefficients bound once, and exposes them as observeds tested at t = 0 against the real64 KPP box driver and against a real WRF-Chem chem_opt = 101 single-column run. The reaction system RADM2 carries the stoichiometry only, each rate being a scoped reference to that model (photolysis rates are its parameters j_*). The model RADM2Tendencies exposes the mass-action tendency of every species as an observed, so the right-hand side is tested at t = 0 independently of any integrator. Species are in molec/cm^3 (the KPP units; WRF converts its ppmV chem array with conv = 1e-6 dens2con_a rho). The two KPP fixed species are not species here: air (M) and water vapour (H2O) are the parameters RADM2RateConstants.M and RADM2RateConstants.H2O, the single source of each for the whole document. The rate laws read them as arguments, the five reactions in which KPP multiplies by a fixed species (R022, R024 and R036 by M; R025 and R033 by H2O) multiply their rate by them, and the relative humidity of the heterogeneous N2O5 rate is derived from H2O, M, T and p with WRF's own formula, so no override can leave two copies of one quantity disagreeing. Mass action is that of esm-spec 7.4, v = k prod S_i^n_i with no 1/n_i! factor, which is also what KPP generates. The eight reactions with a doubled substrate (R032 and R033 HO2 + HO2, R036 NO + NO, R119 MO2 + MO2, R140 ACO3 + ACO3, R147 XO2 + XO2, R153 XNO2 + XNO2, R156 OLN + OLN) carry their .eqn coefficients unchanged on that understanding: a binding that lowers this document to Catalyst.jl must build it with combinatoric_ratelaws = false, or those eight rates come out at half the KPP value. Single-precision literals of radm2.eqn and of the WRF-Chem coupler (.20946e0, .78084, -2.3, the constants of rc_n2o5 and of the relative humidity) are transcribed as the binary64 value of the single-precision number, since that is what the Fortran evaluates.

## Reference

_WRF v4.8.0 chem/KPP/mechanisms/radm2/radm2.eqn and radm2.spc; WRF species name HO is KPP OH (radm2_wrfkpp.equiv). Reaction ids R001-R156 are the KPP reaction indices, i.e. the position in radm2.eqn and the index into RCONST; each reaction's name is its .eqn label {a:b}. The first label number is 001-021 for photolysis and 22-157 for the thermal reactions, with 25 absent, so from R025 on the label runs one ahead of the id (R025 is {26:005}). The second number, the RADM2 thermal reaction number, runs 001-140 with 004, 023, 059, 061 and 063 absent and 137 out of place: it labels R043, {44:137, 14}, the heterogeneous N2O5 rate that WRF-Chem adds to RADM2. R060x is not a KPP reaction but the second half of R060 (see its notes). M and H2O, the fixed species of radm2.spc, are parameters of RADM2RateConstants (see the document description); the reactions that list H2O as a product omit it, since KPP generates no tendency for a fixed species._

## Species

| Species | Units | Default | Constant | Description |
| --- | --- | --- | --- | --- |
| `O3` | `molec/cm^3` | `1477411357577.5947` |  | RADM2 species O3 (KPP index 46); default = the urban-noon box state. |
| `H2O2` | `molec/cm^3` | `24623522626.293247` |  | RADM2 species H2O2 (KPP index 14); default = the urban-noon box state. |
| `NO` | `molec/cm^3` | `492470452525.86487` |  | RADM2 species NO (KPP index 58); default = the urban-noon box state. |
| `NO2` | `molec/cm^3` | `984940905051.7297` |  | RADM2 species NO2 (KPP index 59); default = the urban-noon box state. |
| `NO3` | `molec/cm^3` | `49247045.2525865` |  | RADM2 species NO3 (KPP index 54); default = the urban-noon box state. |
| `N2O5` | `molec/cm^3` | `1231176131.3146625` |  | RADM2 species N2O5 (KPP index 15); default = the urban-noon box state. |
| `HONO` | `molec/cm^3` | `12311761313.146624` |  | RADM2 species HONO (KPP index 13); default = the urban-noon box state. |
| `HNO3` | `molec/cm^3` | `49247045252.586494` |  | RADM2 species HNO3 (KPP index 25); default = the urban-noon box state. |
| `HNO4` | `molec/cm^3` | `1231176131.3146625` |  | RADM2 species HNO4 (KPP index 20); default = the urban-noon box state. |
| `SO2` | `molec/cm^3` | `123117613131.46622` |  | RADM2 species SO2 (KPP index 5); default = the urban-noon box state. |
| `SULF` | `molec/cm^3` | `2462352262.629325` |  | RADM2 species SULF (KPP index 1); default = the urban-noon box state. |
| `CO` | `molec/cm^3` | `12311761313146.623` |  | RADM2 species CO (KPP index 26); default = the urban-noon box state. |
| `ETH` | `molec/cm^3` | `246235226262.93243` |  | RADM2 species ETH (KPP index 6); default = the urban-noon box state. |
| `HC3` | `molec/cm^3` | `492470452525.86487` |  | RADM2 species HC3 (KPP index 16); default = the urban-noon box state. |
| `HC5` | `molec/cm^3` | `246235226262.93243` |  | RADM2 species HC5 (KPP index 8); default = the urban-noon box state. |
| `HC8` | `molec/cm^3` | `123117613131.46622` |  | RADM2 species HC8 (KPP index 9); default = the urban-noon box state. |
| `OL2` | `molec/cm^3` | `123117613131.46622` |  | RADM2 species OL2 (KPP index 24); default = the urban-noon box state. |
| `OLT` | `molec/cm^3` | `49247045252.586494` |  | RADM2 species OLT (KPP index 28); default = the urban-noon box state. |
| `OLI` | `molec/cm^3` | `24623522626.293247` |  | RADM2 species OLI (KPP index 29); default = the urban-noon box state. |
| `ISO` | `molec/cm^3` | `24623522626.293247` |  | RADM2 species ISO (KPP index 27); default = the urban-noon box state. |
| `TOL` | `molec/cm^3` | `123117613131.46622` |  | RADM2 species TOL (KPP index 10); default = the urban-noon box state. |
| `XYL` | `molec/cm^3` | `73870567878.87975` |  | RADM2 species XYL (KPP index 11); default = the urban-noon box state. |
| `CSL` | `molec/cm^3` | `4924704525.25865` |  | RADM2 species CSL (KPP index 22); default = the urban-noon box state. |
| `HCHO` | `molec/cm^3` | `123117613131.46622` |  | RADM2 species HCHO (KPP index 43); default = the urban-noon box state. |
| `ALD` | `molec/cm^3` | `49247045252.586494` |  | RADM2 species ALD (KPP index 48); default = the urban-noon box state. |
| `ETHP` | `molec/cm^3` | `24623522.62629325` |  | RADM2 species ETHP (KPP index 57); default = the urban-noon box state. |
| `KET` | `molec/cm^3` | `49247045252.586494` |  | RADM2 species KET (KPP index 33); default = the urban-noon box state. |
| `GLY` | `molec/cm^3` | `4924704525.25865` |  | RADM2 species GLY (KPP index 31); default = the urban-noon box state. |
| `MGLY` | `molec/cm^3` | `7387056787.887973` |  | RADM2 species MGLY (KPP index 34); default = the urban-noon box state. |
| `MO2` | `molec/cm^3` | `123117613.13146622` |  | RADM2 species MO2 (KPP index 52); default = the urban-noon box state. |
| `DCB` | `molec/cm^3` | `2462352262.629325` |  | RADM2 species DCB (KPP index 30); default = the urban-noon box state. |
| `ONIT` | `molec/cm^3` | `12311761313.146624` |  | RADM2 species ONIT (KPP index 47); default = the urban-noon box state. |
| `PAN` | `molec/cm^3` | `24623522626.293247` |  | RADM2 species PAN (KPP index 23); default = the urban-noon box state. |
| `TPAN` | `molec/cm^3` | `1231176131.3146625` |  | RADM2 species TPAN (KPP index 12); default = the urban-noon box state. |
| `OP1` | `molec/cm^3` | `12311761313.146624` |  | RADM2 species OP1 (KPP index 21); default = the urban-noon box state. |
| `OP2` | `molec/cm^3` | `7387056787.887973` |  | RADM2 species OP2 (KPP index 42); default = the urban-noon box state. |
| `PAA` | `molec/cm^3` | `2462352262.629325` |  | RADM2 species PAA (KPP index 18); default = the urban-noon box state. |
| `ORA1` | `molec/cm^3` | `12311761313.146624` |  | RADM2 species ORA1 (KPP index 2); default = the urban-noon box state. |
| `ORA2` | `molec/cm^3` | `12311761313.146624` |  | RADM2 species ORA2 (KPP index 3); default = the urban-noon box state. |
| `OH` | `molec/cm^3` | `4924704.525258649` |  | RADM2 species OH (KPP index 53); default = the urban-noon box state. |
| `HO2` | `molec/cm^3` | `492470452.5258649` |  | RADM2 species HO2 (KPP index 51); default = the urban-noon box state. |
| `O3P` | `molec/cm^3` | `2462.3522626293243` |  | RADM2 species O3P (KPP index 19); default = the urban-noon box state. |
| `O1D` | `molec/cm^3` | `2.4623522626293246` |  | RADM2 species O1D (KPP index 7); default = the urban-noon box state. |
| `HC3P` | `molec/cm^3` | `24623522.62629325` |  | RADM2 species HC3P (KPP index 56); default = the urban-noon box state. |
| `HC5P` | `molec/cm^3` | `12311761.313146625` |  | RADM2 species HC5P (KPP index 41); default = the urban-noon box state. |
| `HC8P` | `molec/cm^3` | `7387056.787887973` |  | RADM2 species HC8P (KPP index 44); default = the urban-noon box state. |
| `OLTP` | `molec/cm^3` | `7387056.787887973` |  | RADM2 species OLTP (KPP index 37); default = the urban-noon box state. |
| `OLIP` | `molec/cm^3` | `4924704.525258649` |  | RADM2 species OLIP (KPP index 49); default = the urban-noon box state. |
| `TOLP` | `molec/cm^3` | `4924704.525258649` |  | RADM2 species TOLP (KPP index 35); default = the urban-noon box state. |
| `XYLP` | `molec/cm^3` | `4924704.525258649` |  | RADM2 species XYLP (KPP index 36); default = the urban-noon box state. |
| `ACO3` | `molec/cm^3` | `49247045.2525865` |  | RADM2 species ACO3 (KPP index 55); default = the urban-noon box state. |
| `TCO3` | `molec/cm^3` | `4924704.525258649` |  | RADM2 species TCO3 (KPP index 45); default = the urban-noon box state. |
| `KETP` | `molec/cm^3` | `4924704.525258649` |  | RADM2 species KETP (KPP index 50); default = the urban-noon box state. |
| `OLN` | `molec/cm^3` | `2462352.2626293246` |  | RADM2 species OLN (KPP index 38); default = the urban-noon box state. |
| `XO2` | `molec/cm^3` | `24623522.62629325` |  | RADM2 species XO2 (KPP index 39); default = the urban-noon box state. |
| `XNO2` | `molec/cm^3` | `2462352.2626293246` |  | RADM2 species XNO2 (KPP index 32); default = the urban-noon box state. |
| `CH4` | `molec/cm^3` | `44322340727327.84` |  | RADM2 species CH4 (KPP index 17); default = the urban-noon box state. |
| `CO2` | `molec/cm^3` | `9849409050517298.0` |  | RADM2 species CO2 (KPP index 4); default = the urban-noon box state. |
| `OL2P` | `molec/cm^3` | `7387056.787887973` |  | RADM2 species OL2P (KPP index 40); default = the urban-noon box state. |

## Reactions

| ID | Substrates | | Products | Rate |
| --- | --- | --- | --- | --- |
| `R001` | `NO2` | → | `O3P` + `NO` | $$RADM2RateConstants.j_{no2}$$ |
| `R002` | `O3` | → | `O1D` | $$RADM2RateConstants.j_{o31d}$$ |
| `R003` | `O3` | → | `O3P` | $$RADM2RateConstants.j_{o33p}$$ |
| `R004` | `HONO` | → | `OH` + `NO` | $$RADM2RateConstants.j_{hno2}$$ |
| `R005` | `HNO3` | → | `OH` + `NO2` | $$RADM2RateConstants.j_{hno3}$$ |
| `R006` | `HNO4` | → | 0.65 `HO2` + 0.65 `NO2` + 0.35 `OH` + 0.35 `NO3` | $$RADM2RateConstants.j_{hno4}$$ |
| `R007` | `NO3` | → | `NO` | $$RADM2RateConstants.j_{no3o2}$$ |
| `R008` | `NO3` | → | `NO2` + `O3P` | $$RADM2RateConstants.j_{no3o}$$ |
| `R009` | `H2O2` | → | 2.0 `OH` | $$RADM2RateConstants.j_{h2o2}$$ |
| `R010` | `HCHO` | → | `CO` | $$RADM2RateConstants.j_{ch2om}$$ |
| `R011` | `HCHO` | → | 2.0 `HO2` + `CO` | $$RADM2RateConstants.j_{ch2or}$$ |
| `R012` | `ALD` | → | `MO2` + `HO2` + `CO` | $$RADM2RateConstants.j_{ch3cho}$$ |
| `R013` | `OP1` | → | `HCHO` + `HO2` + `OH` | $$RADM2RateConstants.j_{ch3o2h}$$ |
| `R014` | `OP2` | → | `ALD` + `HO2` + `OH` | $$RADM2RateConstants.j_{ch3coch3}$$ |
| `R015` | `PAA` | → | `MO2` + `OH` | $$RADM2RateConstants.j_{ch3coo2h}$$ |
| `R016` | `KET` | → | `ACO3` + `ETHP` | $$RADM2RateConstants.j_{ch3coc2h5}$$ |
| `R017` | `GLY` | → | 0.13 `HCHO` + 1.87 `CO` | $$RADM2RateConstants.j_{hcocho}$$ |
| `R018` | `GLY` | → | 0.45 `HCHO` + 1.55 `CO` + 0.8 `HO2` | $$RADM2RateConstants.j_{hcochob}$$ |
| `R019` | `MGLY` | → | `ACO3` + `HO2` + `CO` | $$RADM2RateConstants.j_{ch3cocho}$$ |
| `R020` | `DCB` | → | `HO2` + `TCO3` | $$RADM2RateConstants.j_{hcochest}$$ |
| `R021` | `ONIT` | → | 0.2 `ALD` + 0.8 `KET` + `HO2` + `NO2` | $$RADM2RateConstants.j_{ch3ono2}$$ |
| `R022` | `O3P` | → | `O3` | $$RADM2RateConstants.k_{R022} \cdot RADM2RateConstants.M$$ |
| `R023` | `O3P` + `NO2` | → | `NO` | $$RADM2RateConstants.k_{R023}$$ |
| `R024` | `O1D` | → | `O3P` | $$RADM2RateConstants.k_{R024} \cdot RADM2RateConstants.M$$ |
| `R025` | `O1D` | → | 2.0 `OH` | $$RADM2RateConstants.k_{R025} \cdot RADM2RateConstants.H2O$$ |
| `R026` | `O3` + `NO` | → | `NO2` | $$RADM2RateConstants.k_{R026}$$ |
| `R027` | `O3` + `OH` | → | `HO2` | $$RADM2RateConstants.k_{R027}$$ |
| `R028` | `O3` + `HO2` | → | `OH` | $$RADM2RateConstants.k_{R028}$$ |
| `R029` | `HO2` + `NO` | → | `NO2` + `OH` | $$RADM2RateConstants.k_{R029}$$ |
| `R030` | `HO2` + `NO2` | → | `HNO4` | $$RADM2RateConstants.k_{R030}$$ |
| `R031` | `HNO4` | → | `HO2` + `NO2` | $$RADM2RateConstants.k_{R031}$$ |
| `R032` | 2 `HO2` | → | `H2O2` | $$RADM2RateConstants.k_{R032}$$ |
| `R033` | 2 `HO2` | → | `H2O2` | $$RADM2RateConstants.k_{R033} \cdot RADM2RateConstants.H2O$$ |
| `R034` | `H2O2` + `OH` | → | `HO2` | $$RADM2RateConstants.k_{R034}$$ |
| `R035` | `NO` + `OH` | → | `HONO` | $$RADM2RateConstants.k_{R035}$$ |
| `R036` | 2 `NO` | → | 2.0 `NO2` | $$RADM2RateConstants.k_{R036} \cdot RADM2RateConstants.M$$ |
| `R037` | `O3` + `NO2` | → | `NO3` | $$RADM2RateConstants.k_{R037}$$ |
| `R038` | `NO3` + `NO` | → | 2.0 `NO2` | $$RADM2RateConstants.k_{R038}$$ |
| `R039` | `NO3` + `NO2` | → | `NO` + `NO2` | $$RADM2RateConstants.k_{R039}$$ |
| `R040` | `NO3` + `HO2` | → | `HNO3` | $$RADM2RateConstants.k_{R040}$$ |
| `R041` | `NO3` + `NO2` | → | `N2O5` | $$RADM2RateConstants.k_{R041}$$ |
| `R042` | `N2O5` | → | `NO2` + `NO3` | $$RADM2RateConstants.k_{R042}$$ |
| `R043` | `N2O5` | → | 2.0 `HNO3` | $$RADM2RateConstants.k_{R043}$$ |
| `R044` | `OH` + `NO2` | → | `HNO3` | $$RADM2RateConstants.k_{R044}$$ |
| `R045` | `OH` + `HNO3` | → | `NO3` | $$RADM2RateConstants.k_{R045}$$ |
| `R046` | `OH` + `HNO4` | → | `NO2` | $$RADM2RateConstants.k_{R046}$$ |
| `R047` | `OH` + `HO2` | → |  | $$RADM2RateConstants.k_{R047}$$ |
| `R048` | `OH` + `SO2` | → | `SULF` + `HO2` | $$RADM2RateConstants.k_{R048}$$ |
| `R049` | `CO` + `OH` | → | `HO2` + `CO2` | $$RADM2RateConstants.k_{R049}$$ |
| `R050` | `CH4` + `OH` | → | `MO2` | $$RADM2RateConstants.k_{R050}$$ |
| `R051` | `ETH` + `OH` | → | `ETHP` | $$RADM2RateConstants.k_{R051}$$ |
| `R052` | `HC3` + `OH` | → | 0.83 `HC3P` + 0.17 `HO2` + 0.009 `HCHO` + 0.075 `ALD` + 0.025 `KET` | $$RADM2RateConstants.k_{R052}$$ |
| `R053` | `HC5` + `OH` | → | `HC5P` + 0.25 `XO2` | $$RADM2RateConstants.k_{R053}$$ |
| `R054` | `HC8` + `OH` | → | `HC8P` + 0.75 `XO2` | $$RADM2RateConstants.k_{R054}$$ |
| `R055` | `OL2` + `OH` | → | `OL2P` | $$RADM2RateConstants.k_{R055}$$ |
| `R056` | `OLT` + `OH` | → | `OLTP` | $$RADM2RateConstants.k_{R056}$$ |
| `R057` | `OLI` + `OH` | → | `OLIP` | $$RADM2RateConstants.k_{R057}$$ |
| `R058` | `TOL` + `OH` | → | 0.75 `TOLP` + 0.25 `CSL` + 0.25 `HO2` | $$RADM2RateConstants.k_{R058}$$ |
| `R059` | `XYL` + `OH` | → | 0.83 `XYLP` + 0.17 `CSL` + 0.17 `HO2` | $$RADM2RateConstants.k_{R059}$$ |
| `R060` | `CSL` + `OH` | → | 0.1 `HO2` + 0.9 `XO2` + 0.9 `TCO3` | $$RADM2RateConstants.k_{R060}$$ |
| `R060x` | `CSL` + `OH` | → | `CSL` | $$0.9 \cdot RADM2RateConstants.k_{R060}$$ |
| `R061` | `HCHO` + `OH` | → | `HO2` + `CO` | $$RADM2RateConstants.k_{R061}$$ |
| `R062` | `ALD` + `OH` | → | `ACO3` | $$RADM2RateConstants.k_{R062}$$ |
| `R063` | `KET` + `OH` | → | `KETP` | $$RADM2RateConstants.k_{R063}$$ |
| `R064` | `GLY` + `OH` | → | `HO2` + 2.0 `CO` | $$RADM2RateConstants.k_{R064}$$ |
| `R065` | `MGLY` + `OH` | → | `ACO3` + `CO` | $$RADM2RateConstants.k_{R065}$$ |
| `R066` | `DCB` + `OH` | → | `TCO3` | $$RADM2RateConstants.k_{R066}$$ |
| `R067` | `OP1` + `OH` | → | 0.5 `MO2` + 0.5 `HCHO` + 0.5 `OH` | $$RADM2RateConstants.k_{R067}$$ |
| `R068` | `OP2` + `OH` | → | 0.5 `HC3P` + 0.5 `ALD` + 0.5 `OH` | $$RADM2RateConstants.k_{R068}$$ |
| `R069` | `PAA` + `OH` | → | `ACO3` | $$RADM2RateConstants.k_{R069}$$ |
| `R070` | `PAN` + `OH` | → | `HCHO` + `NO3` + `XO2` | $$RADM2RateConstants.k_{R070}$$ |
| `R071` | `ONIT` + `OH` | → | `HC3P` + `NO2` | $$RADM2RateConstants.k_{R071}$$ |
| `R072` | `ISO` + `OH` | → | `OLTP` | $$RADM2RateConstants.k_{R072}$$ |
| `R073` | `ACO3` + `NO2` | → | `PAN` | $$RADM2RateConstants.k_{R073}$$ |
| `R074` | `PAN` | → | `ACO3` + `NO2` | $$RADM2RateConstants.k_{R074}$$ |
| `R075` | `TCO3` + `NO2` | → | `TPAN` | $$RADM2RateConstants.k_{R075}$$ |
| `R076` | `TPAN` | → | `TCO3` + `NO2` | $$RADM2RateConstants.k_{R076}$$ |
| `R077` | `MO2` + `NO` | → | `HCHO` + `HO2` + `NO2` | $$RADM2RateConstants.k_{R077}$$ |
| `R078` | `HC3P` + `NO` | → | 0.75 `ALD` + 0.25 `KET` + 0.09 `HCHO` + 0.036 `ONIT` + 0.964 `NO2` + 0.964 `HO2` | $$RADM2RateConstants.k_{R078}$$ |
| `R079` | `HC5P` + `NO` | → | 0.38 `ALD` + 0.69 `KET` + 0.08 `ONIT` + 0.92 `NO2` + 0.92 `HO2` | $$RADM2RateConstants.k_{R079}$$ |
| `R080` | `HC8P` + `NO` | → | 0.35 `ALD` + 1.06 `KET` + 0.04 `HCHO` + 0.24 `ONIT` + 0.76 `NO2` + 0.76 `HO2` | $$RADM2RateConstants.k_{R080}$$ |
| `R081` | `OL2P` + `NO` | → | 1.6 `HCHO` + `HO2` + `NO2` + 0.2 `ALD` | $$RADM2RateConstants.k_{R081}$$ |
| `R082` | `OLTP` + `NO` | → | `ALD` + `HCHO` + `HO2` + `NO2` | $$RADM2RateConstants.k_{R082}$$ |
| `R083` | `OLIP` + `NO` | → | `HO2` + 1.45 `ALD` + 0.28 `HCHO` + 0.1 `KET` + `NO2` | $$RADM2RateConstants.k_{R083}$$ |
| `R084` | `ACO3` + `NO` | → | `MO2` + `NO2` | $$RADM2RateConstants.k_{R084}$$ |
| `R085` | `TCO3` + `NO` | → | `NO2` + 0.92 `HO2` + 0.89 `GLY` + 0.11 `MGLY` + 0.05 `ACO3` + 0.95 `CO` + 2.0 `XO2` | $$RADM2RateConstants.k_{R085}$$ |
| `R086` | `TOLP` + `NO` | → | `NO2` + `HO2` + 0.17 `MGLY` + 0.16 `GLY` + 0.7 `DCB` | $$RADM2RateConstants.k_{R086}$$ |
| `R087` | `XYLP` + `NO` | → | `NO2` + `HO2` + 0.45 `MGLY` + 0.806 `DCB` | $$RADM2RateConstants.k_{R087}$$ |
| `R088` | `ETHP` + `NO` | → | `ALD` + `HO2` + `NO2` | $$RADM2RateConstants.k_{R088}$$ |
| `R089` | `KETP` + `NO` | → | `MGLY` + `NO2` + `HO2` | $$RADM2RateConstants.k_{R089}$$ |
| `R090` | `OLN` + `NO` | → | `HCHO` + `ALD` + 2.0 `NO2` | $$RADM2RateConstants.k_{R090}$$ |
| `R091` | `HCHO` + `NO3` | → | `HO2` + `HNO3` + `CO` | $$RADM2RateConstants.k_{R091}$$ |
| `R092` | `ALD` + `NO3` | → | `ACO3` + `HNO3` | $$RADM2RateConstants.k_{R092}$$ |
| `R093` | `GLY` + `NO3` | → | `HNO3` + `HO2` + 2.0 `CO` | $$RADM2RateConstants.k_{R093}$$ |
| `R094` | `MGLY` + `NO3` | → | `HNO3` + `ACO3` + `CO` | $$RADM2RateConstants.k_{R094}$$ |
| `R095` | `DCB` + `NO3` | → | `HNO3` + `TCO3` | $$RADM2RateConstants.k_{R095}$$ |
| `R096` | `CSL` + `NO3` | → | `HNO3` + `XNO2` + 0.5 `CSL` | $$RADM2RateConstants.k_{R096}$$ |
| `R097` | `OL2` + `NO3` | → | `OLN` | $$RADM2RateConstants.k_{R097}$$ |
| `R098` | `OLT` + `NO3` | → | `OLN` | $$RADM2RateConstants.k_{R098}$$ |
| `R099` | `OLI` + `NO3` | → | `OLN` | $$RADM2RateConstants.k_{R099}$$ |
| `R100` | `ISO` + `NO3` | → | `OLN` | $$RADM2RateConstants.k_{R100}$$ |
| `R101` | `OL2` + `O3` | → | `HCHO` + 0.42 `CO` + 0.4 `ORA1` + 0.12 `HO2` | $$RADM2RateConstants.k_{R101}$$ |
| `R102` | `OLT` + `O3` | → | 0.53 `HCHO` + 0.5 `ALD` + 0.33 `CO` + 0.2 `ORA1` + 0.2 `ORA2` + 0.23 `HO2` + 0.22 `MO2` + 0.1 `OH` + 0.06 `CH4` | $$RADM2RateConstants.k_{R102}$$ |
| `R103` | `OLI` + `O3` | → | 0.18 `HCHO` + 0.72 `ALD` + 0.1 `KET` + 0.23 `CO` + 0.06 `ORA1` + 0.29 `ORA2` + 0.09 `CH4` + 0.26 `HO2` + 0.31 `MO2` + 0.14 `OH` | $$RADM2RateConstants.k_{R103}$$ |
| `R104` | `ISO` + `O3` | → | 0.53 `HCHO` + 0.5 `ALD` + 0.33 `CO` + 0.2 `ORA1` + 0.2 `ORA2` + 0.23 `HO2` + 0.22 `MO2` + 0.1 `OH` | $$RADM2RateConstants.k_{R104}$$ |
| `R105` | `HO2` + `MO2` | → | `OP1` | $$RADM2RateConstants.k_{R105}$$ |
| `R106` | `HO2` + `ETHP` | → | `OP2` | $$RADM2RateConstants.k_{R106}$$ |
| `R107` | `HO2` + `HC3P` | → | `OP2` | $$RADM2RateConstants.k_{R107}$$ |
| `R108` | `HO2` + `HC5P` | → | `OP2` | $$RADM2RateConstants.k_{R108}$$ |
| `R109` | `HO2` + `HC8P` | → | `OP2` | $$RADM2RateConstants.k_{R109}$$ |
| `R110` | `HO2` + `OL2P` | → | `OP2` | $$RADM2RateConstants.k_{R110}$$ |
| `R111` | `HO2` + `OLTP` | → | `OP2` | $$RADM2RateConstants.k_{R111}$$ |
| `R112` | `HO2` + `OLIP` | → | `OP2` | $$RADM2RateConstants.k_{R112}$$ |
| `R113` | `HO2` + `KETP` | → | `OP2` | $$RADM2RateConstants.k_{R113}$$ |
| `R114` | `HO2` + `ACO3` | → | `PAA` | $$RADM2RateConstants.k_{R114}$$ |
| `R115` | `HO2` + `TOLP` | → | `OP2` | $$RADM2RateConstants.k_{R115}$$ |
| `R116` | `HO2` + `XYLP` | → | `OP2` | $$RADM2RateConstants.k_{R116}$$ |
| `R117` | `HO2` + `TCO3` | → | `OP2` | $$RADM2RateConstants.k_{R117}$$ |
| `R118` | `HO2` + `OLN` | → | `ONIT` | $$RADM2RateConstants.k_{R118}$$ |
| `R119` | 2 `MO2` | → | 1.5 `HCHO` + `HO2` | $$RADM2RateConstants.k_{R119}$$ |
| `R120` | `MO2` + `ETHP` | → | 0.75 `HCHO` + `HO2` + 0.75 `ALD` | $$RADM2RateConstants.k_{R120}$$ |
| `R121` | `MO2` + `HC3P` | → | 0.75 `HCHO` + `HO2` + 0.15 `ALD` + 0.6 `KET` | $$RADM2RateConstants.k_{R121}$$ |
| `R122` | `MO2` + `HC5P` | → | 0.77 `HCHO` + `HO2` + 0.41 `ALD` + 0.75 `KET` | $$RADM2RateConstants.k_{R122}$$ |
| `R123` | `MO2` + `HC8P` | → | 0.8 `HCHO` + `HO2` + 0.46 `ALD` + 1.39 `KET` | $$RADM2RateConstants.k_{R123}$$ |
| `R124` | `MO2` + `OL2P` | → | 1.55 `HCHO` + `HO2` + 0.35 `ALD` | $$RADM2RateConstants.k_{R124}$$ |
| `R125` | `MO2` + `OLTP` | → | 1.25 `HCHO` + `HO2` + 0.75 `ALD` | $$RADM2RateConstants.k_{R125}$$ |
| `R126` | `MO2` + `OLIP` | → | 0.89 `HCHO` + `HO2` + 0.725 `ALD` + 0.55 `KET` | $$RADM2RateConstants.k_{R126}$$ |
| `R127` | `MO2` + `KETP` | → | 0.75 `HCHO` + `HO2` + 0.75 `MGLY` | $$RADM2RateConstants.k_{R127}$$ |
| `R128` | `MO2` + `ACO3` | → | `HCHO` + 0.5 `HO2` + 0.5 `MO2` + 0.5 `ORA2` | $$RADM2RateConstants.k_{R128}$$ |
| `R129` | `MO2` + `TOLP` | → | `HCHO` + 2.0 `HO2` + 0.17 `MGLY` + 0.16 `GLY` + 0.7 `DCB` | $$RADM2RateConstants.k_{R129}$$ |
| `R130` | `MO2` + `XYLP` | → | `HCHO` + 2.0 `HO2` + 0.45 `MGLY` + 0.806 `DCB` | $$RADM2RateConstants.k_{R130}$$ |
| `R131` | `MO2` + `TCO3` | → | 0.5 `HCHO` + 0.5 `ORA2` + 0.445 `GLY` + 0.055 `MGLY` + 0.025 `ACO3` + 0.475 `CO` + 0.46 `HO2` + `XO2` | $$RADM2RateConstants.k_{R131}$$ |
| `R132` | `ETHP` + `ACO3` | → | `ALD` + 0.5 `HO2` + 0.5 `MO2` + 0.5 `ORA2` | $$RADM2RateConstants.k_{R132}$$ |
| `R133` | `HC3P` + `ACO3` | → | 0.2 `ALD` + 0.8 `KET` + 0.5 `HO2` + 0.5 `ORA2` + 0.5 `MO2` | $$RADM2RateConstants.k_{R133}$$ |
| `R134` | `HC5P` + `ACO3` | → | 0.14 `ALD` + 0.86 `KET` + 0.5 `HO2` + 0.5 `ORA2` + 0.5 `MO2` | $$RADM2RateConstants.k_{R134}$$ |
| `R135` | `HC8P` + `ACO3` | → | 0.1 `ALD` + 0.9 `KET` + 0.5 `HO2` + 0.5 `ORA2` + 0.5 `MO2` | $$RADM2RateConstants.k_{R135}$$ |
| `R136` | `OL2P` + `ACO3` | → | 0.8 `HCHO` + 0.6 `ALD` + 0.5 `HO2` + 0.5 `ORA2` + 0.5 `MO2` | $$RADM2RateConstants.k_{R136}$$ |
| `R137` | `OLTP` + `ACO3` | → | `ALD` + 0.5 `HCHO` + 0.5 `HO2` + 0.5 `ORA2` + 0.5 `MO2` | $$RADM2RateConstants.k_{R137}$$ |
| `R138` | `OLIP` + `ACO3` | → | 0.725 `ALD` + 0.55 `KET` + 0.14 `HCHO` + 0.5 `HO2` + 0.5 `MO2` + 0.5 `ORA2` | $$RADM2RateConstants.k_{R138}$$ |
| `R139` | `KETP` + `ACO3` | → | `MGLY` + 0.5 `HO2` + 0.5 `ORA2` + 0.5 `MO2` | $$RADM2RateConstants.k_{R139}$$ |
| `R140` | 2 `ACO3` | → | 2.0 `MO2` | $$RADM2RateConstants.k_{R140}$$ |
| `R141` | `ACO3` + `TOLP` | → | 0.8 `MGLY` + 0.2 `GLY` + `DCB` + `HO2` + `MO2` | $$RADM2RateConstants.k_{R141}$$ |
| `R142` | `ACO3` + `XYLP` | → | `MO2` + `MGLY` + `DCB` + `HO2` | $$RADM2RateConstants.k_{R142}$$ |
| `R143` | `ACO3` + `TCO3` | → | `MO2` + 0.92 `HO2` + 0.89 `GLY` + 0.11 `MGLY` + 0.05 `ACO3` + 0.95 `CO` + 2.0 `XO2` | $$RADM2RateConstants.k_{R143}$$ |
| `R144` | `XO2` + `HO2` | → | `OP2` | $$RADM2RateConstants.k_{R144}$$ |
| `R145` | `XO2` + `MO2` | → | `HCHO` + `HO2` | $$RADM2RateConstants.k_{R145}$$ |
| `R146` | `XO2` + `ACO3` | → | `MO2` | $$RADM2RateConstants.k_{R146}$$ |
| `R147` | 2 `XO2` | → |  | $$RADM2RateConstants.k_{R147}$$ |
| `R148` | `XO2` + `NO` | → | `NO2` | $$RADM2RateConstants.k_{R148}$$ |
| `R149` | `XNO2` + `NO2` | → | `ONIT` | $$RADM2RateConstants.k_{R149}$$ |
| `R150` | `XNO2` + `HO2` | → | `OP2` | $$RADM2RateConstants.k_{R150}$$ |
| `R151` | `XNO2` + `MO2` | → | `HCHO` + `HO2` | $$RADM2RateConstants.k_{R151}$$ |
| `R152` | `XNO2` + `ACO3` | → | `MO2` | $$RADM2RateConstants.k_{R152}$$ |
| `R153` | 2 `XNO2` | → |  | $$RADM2RateConstants.k_{R153}$$ |
| `R154` | `MO2` + `OLN` | → | 1.75 `HCHO` + 0.5 `HO2` + `ALD` + `NO2` | $$RADM2RateConstants.k_{R154}$$ |
| `R155` | `ACO3` + `OLN` | → | `HCHO` + `ALD` + 0.5 `ORA2` + `NO2` + 0.5 `MO2` | $$RADM2RateConstants.k_{R155}$$ |
| `R156` | 2 `OLN` | → | 2.0 `HCHO` + 2.0 `ALD` + 2.0 `NO2` | $$RADM2RateConstants.k_{R156}$$ |

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "reference": {
    "notes": "WRF v4.8.0 chem/KPP/mechanisms/radm2/radm2.eqn and radm2.spc; WRF species name HO is KPP OH (radm2_wrfkpp.equiv). Reaction ids R001-R156 are the KPP reaction indices, i.e. the position in radm2.eqn and the index into RCONST; each reaction's name is its .eqn label {a:b}. The first label number is 001-021 for photolysis and 22-157 for the thermal reactions, with 25 absent, so from R025 on the label runs one ahead of the id (R025 is {26:005}). The second number, the RADM2 thermal reaction number, runs 001-140 with 004, 023, 059, 061 and 063 absent and 137 out of place: it labels R043, {44:137, 14}, the heterogeneous N2O5 rate that WRF-Chem adds to RADM2. R060x is not a KPP reaction but the second half of R060 (see its notes). M and H2O, the fixed species of radm2.spc, are parameters of RADM2RateConstants (see the document description); the reactions that list H2O as a product omit it, since KPP generates no tendency for a fixed species."
  },
  "species": {
    "O3": {
      "units": "molec/cm^3",
      "default": 1477411357577.5947,
      "description": "RADM2 species O3 (KPP index 46); default = the urban-noon box state."
    },
    "H2O2": {
      "units": "molec/cm^3",
      "default": 24623522626.293247,
      "description": "RADM2 species H2O2 (KPP index 14); default = the urban-noon box state."
    },
    "NO": {
      "units": "molec/cm^3",
      "default": 492470452525.86487,
      "description": "RADM2 species NO (KPP index 58); default = the urban-noon box state."
    },
    "NO2": {
      "units": "molec/cm^3",
      "default": 984940905051.7297,
      "description": "RADM2 species NO2 (KPP index 59); default = the urban-noon box state."
    },
    "NO3": {
      "units": "molec/cm^3",
      "default": 49247045.2525865,
      "description": "RADM2 species NO3 (KPP index 54); default = the urban-noon box state."
    },
    "N2O5": {
      "units": "molec/cm^3",
      "default": 1231176131.3146625,
      "description": "RADM2 species N2O5 (KPP index 15); default = the urban-noon box state."
    },
    "HONO": {
      "units": "molec/cm^3",
      "default": 12311761313.146624,
      "description": "RADM2 species HONO (KPP index 13); default = the urban-noon box state."
    },
    "HNO3": {
      "units": "molec/cm^3",
      "default": 49247045252.586494,
      "description": "RADM2 species HNO3 (KPP index 25); default = the urban-noon box state."
    },
    "HNO4": {
      "units": "molec/cm^3",
      "default": 1231176131.3146625,
      "description": "RADM2 species HNO4 (KPP index 20); default = the urban-noon box state."
    },
    "SO2": {
      "units": "molec/cm^3",
      "default": 123117613131.46622,
      "description": "RADM2 species SO2 (KPP index 5); default = the urban-noon box state."
    },
    "SULF": {
      "units": "molec/cm^3",
      "default": 2462352262.629325,
      "description": "RADM2 species SULF (KPP index 1); default = the urban-noon box state."
    },
    "CO": {
      "units": "molec/cm^3",
      "default": 12311761313146.623,
      "description": "RADM2 species CO (KPP index 26); default = the urban-noon box state."
    },
    "ETH": {
      "units": "molec/cm^3",
      "default": 246235226262.93243,
      "description": "RADM2 species ETH (KPP index 6); default = the urban-noon box state."
    },
    "HC3": {
      "units": "molec/cm^3",
      "default": 492470452525.86487,
      "description": "RADM2 species HC3 (KPP index 16); default = the urban-noon box state."
    },
    "HC5": {
      "units": "molec/cm^3",
      "default": 246235226262.93243,
      "description": "RADM2 species HC5 (KPP index 8); default = the urban-noon box state."
    },
    "HC8": {
      "units": "molec/cm^3",
      "default": 123117613131.46622,
      "description": "RADM2 species HC8 (KPP index 9); default = the urban-noon box state."
    },
    "OL2": {
      "units": "molec/cm^3",
      "default": 123117613131.46622,
      "description": "RADM2 species OL2 (KPP index 24); default = the urban-noon box state."
    },
    "OLT": {
      "units": "molec/cm^3",
      "default": 49247045252.586494,
      "description": "RADM2 species OLT (KPP index 28); default = the urban-noon box state."
    },
    "OLI": {
      "units": "molec/cm^3",
      "default": 24623522626.293247,
      "description": "RADM2 species OLI (KPP index 29); default = the urban-noon box state."
    },
    "ISO": {
      "units": "molec/cm^3",
      "default": 24623522626.293247,
      "description": "RADM2 species ISO (KPP index 27); default = the urban-noon box state."
    },
    "TOL": {
      "units": "molec/cm^3",
      "default": 123117613131.46622,
      "description": "RADM2 species TOL (KPP index 10); default = the urban-noon box state."
    },
    "XYL": {
      "units": "molec/cm^3",
      "default": 73870567878.87975,
      "description": "RADM2 species XYL (KPP index 11); default = the urban-noon box state."
    },
    "CSL": {
      "units": "molec/cm^3",
      "default": 4924704525.25865,
      "description": "RADM2 species CSL (KPP index 22); default = the urban-noon box state."
    },
    "HCHO": {
      "units": "molec/cm^3",
      "default": 123117613131.46622,
      "description": "RADM2 species HCHO (KPP index 43); default = the urban-noon box state."
    },
    "ALD": {
      "units": "molec/cm^3",
      "default": 49247045252.586494,
      "description": "RADM2 species ALD (KPP index 48); default = the urban-noon box state."
    },
    "ETHP": {
      "units": "molec/cm^3",
      "default": 24623522.62629325,
      "description": "RADM2 species ETHP (KPP index 57); default = the urban-noon box state."
    },
    "KET": {
      "units": "molec/cm^3",
      "default": 49247045252.586494,
      "description": "RADM2 species KET (KPP index 33); default = the urban-noon box state."
    },
    "GLY": {
      "units": "molec/cm^3",
      "default": 4924704525.25865,
      "description": "RADM2 species GLY (KPP index 31); default = the urban-noon box state."
    },
    "MGLY": {
      "units": "molec/cm^3",
      "default": 7387056787.887973,
      "description": "RADM2 species MGLY (KPP index 34); default = the urban-noon box state."
    },
    "MO2": {
      "units": "molec/cm^3",
      "default": 123117613.13146622,
      "description": "RADM2 species MO2 (KPP index 52); default = the urban-noon box state."
    },
    "DCB": {
      "units": "molec/cm^3",
      "default": 2462352262.629325,
      "description": "RADM2 species DCB (KPP index 30); default = the urban-noon box state."
    },
    "ONIT": {
      "units": "molec/cm^3",
      "default": 12311761313.146624,
      "description": "RADM2 species ONIT (KPP index 47); default = the urban-noon box state."
    },
    "PAN": {
      "units": "molec/cm^3",
      "default": 24623522626.293247,
      "description": "RADM2 species PAN (KPP index 23); default = the urban-noon box state."
    },
    "TPAN": {
      "units": "molec/cm^3",
      "default": 1231176131.3146625,
      "description": "RADM2 species TPAN (KPP index 12); default = the urban-noon box state."
    },
    "OP1": {
      "units": "molec/cm^3",
      "default": 12311761313.146624,
      "description": "RADM2 species OP1 (KPP index 21); default = the urban-noon box state."
    },
    "OP2": {
      "units": "molec/cm^3",
      "default": 7387056787.887973,
      "description": "RADM2 species OP2 (KPP index 42); default = the urban-noon box state."
    },
    "PAA": {
      "units": "molec/cm^3",
      "default": 2462352262.629325,
      "description": "RADM2 species PAA (KPP index 18); default = the urban-noon box state."
    },
    "ORA1": {
      "units": "molec/cm^3",
      "default": 12311761313.146624,
      "description": "RADM2 species ORA1 (KPP index 2); default = the urban-noon box state."
    },
    "ORA2": {
      "units": "molec/cm^3",
      "default": 12311761313.146624,
      "description": "RADM2 species ORA2 (KPP index 3); default = the urban-noon box state."
    },
    "OH": {
      "units": "molec/cm^3",
      "default": 4924704.525258649,
      "description": "RADM2 species OH (KPP index 53); default = the urban-noon box state."
    },
    "HO2": {
      "units": "molec/cm^3",
      "default": 492470452.5258649,
      "description": "RADM2 species HO2 (KPP index 51); default = the urban-noon box state."
    },
    "O3P": {
      "units": "molec/cm^3",
      "default": 2462.3522626293243,
      "description": "RADM2 species O3P (KPP index 19); default = the urban-noon box state."
    },
    "O1D": {
      "units": "molec/cm^3",
      "default": 2.4623522626293246,
      "description": "RADM2 species O1D (KPP index 7); default = the urban-noon box state."
    },
    "HC3P": {
      "units": "molec/cm^3",
      "default": 24623522.62629325,
      "description": "RADM2 species HC3P (KPP index 56); default = the urban-noon box state."
    },
    "HC5P": {
      "units": "molec/cm^3",
      "default": 12311761.313146625,
      "description": "RADM2 species HC5P (KPP index 41); default = the urban-noon box state."
    },
    "HC8P": {
      "units": "molec/cm^3",
      "default": 7387056.787887973,
      "description": "RADM2 species HC8P (KPP index 44); default = the urban-noon box state."
    },
    "OLTP": {
      "units": "molec/cm^3",
      "default": 7387056.787887973,
      "description": "RADM2 species OLTP (KPP index 37); default = the urban-noon box state."
    },
    "OLIP": {
      "units": "molec/cm^3",
      "default": 4924704.525258649,
      "description": "RADM2 species OLIP (KPP index 49); default = the urban-noon box state."
    },
    "TOLP": {
      "units": "molec/cm^3",
      "default": 4924704.525258649,
      "description": "RADM2 species TOLP (KPP index 35); default = the urban-noon box state."
    },
    "XYLP": {
      "units": "molec/cm^3",
      "default": 4924704.525258649,
      "description": "RADM2 species XYLP (KPP index 36); default = the urban-noon box state."
    },
    "ACO3": {
      "units": "molec/cm^3",
      "default": 49247045.2525865,
      "description": "RADM2 species ACO3 (KPP index 55); default = the urban-noon box state."
    },
    "TCO3": {
      "units": "molec/cm^3",
      "default": 4924704.525258649,
      "description": "RADM2 species TCO3 (KPP index 45); default = the urban-noon box state."
    },
    "KETP": {
      "units": "molec/cm^3",
      "default": 4924704.525258649,
      "description": "RADM2 species KETP (KPP index 50); default = the urban-noon box state."
    },
    "OLN": {
      "units": "molec/cm^3",
      "default": 2462352.2626293246,
      "description": "RADM2 species OLN (KPP index 38); default = the urban-noon box state."
    },
    "XO2": {
      "units": "molec/cm^3",
      "default": 24623522.62629325,
      "description": "RADM2 species XO2 (KPP index 39); default = the urban-noon box state."
    },
    "XNO2": {
      "units": "molec/cm^3",
      "default": 2462352.2626293246,
      "description": "RADM2 species XNO2 (KPP index 32); default = the urban-noon box state."
    },
    "CH4": {
      "units": "molec/cm^3",
      "default": 44322340727327.84,
      "description": "RADM2 species CH4 (KPP index 17); default = the urban-noon box state."
    },
    "CO2": {
      "units": "molec/cm^3",
      "default": 9849409050517298.0,
      "description": "RADM2 species CO2 (KPP index 4); default = the urban-noon box state."
    },
    "OL2P": {
      "units": "molec/cm^3",
      "default": 7387056.787887973,
      "description": "RADM2 species OL2P (KPP index 40); default = the urban-noon box state."
    }
  },
  "parameters": {},
  "reactions": [
    {
      "id": "R001",
      "name": "001:J01",
      "substrates": [
        {
          "species": "NO2",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "O3P",
          "stoichiometry": 1.0
        },
        {
          "species": "NO",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.j_no2",
      "reference": {
        "notes": "radm2.eqn {001:J01} NO2+hv=O3P+NO"
      }
    },
    {
      "id": "R002",
      "name": "002:J02",
      "substrates": [
        {
          "species": "O3",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "O1D",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.j_o31d",
      "reference": {
        "notes": "radm2.eqn {002:J02} O3+hv=O1D"
      }
    },
    {
      "id": "R003",
      "name": "003:J03",
      "substrates": [
        {
          "species": "O3",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "O3P",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.j_o33p",
      "reference": {
        "notes": "radm2.eqn {003:J03} O3+hv=O3P"
      }
    },
    {
      "id": "R004",
      "name": "004:J04",
      "substrates": [
        {
          "species": "HONO",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "OH",
          "stoichiometry": 1.0
        },
        {
          "species": "NO",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.j_hno2",
      "reference": {
        "notes": "radm2.eqn {004:J04} HONO+hv=OH+NO"
      }
    },
    {
      "id": "R005",
      "name": "005:J05",
      "substrates": [
        {
          "species": "HNO3",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "OH",
          "stoichiometry": 1.0
        },
        {
          "species": "NO2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.j_hno3",
      "reference": {
        "notes": "radm2.eqn {005:J05} HNO3+hv=OH+NO2"
      }
    },
    {
      "id": "R006",
      "name": "006:J06",
      "substrates": [
        {
          "species": "HNO4",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HO2",
          "stoichiometry": 0.65
        },
        {
          "species": "NO2",
          "stoichiometry": 0.65
        },
        {
          "species": "OH",
          "stoichiometry": 0.35
        },
        {
          "species": "NO3",
          "stoichiometry": 0.35
        }
      ],
      "rate": "RADM2RateConstants.j_hno4",
      "reference": {
        "notes": "radm2.eqn {006:J06} HNO4+hv=0.65 HO2+0.65 NO2+0.35 OH+0.35 NO3"
      }
    },
    {
      "id": "R007",
      "name": "007:J07",
      "substrates": [
        {
          "species": "NO3",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "NO",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.j_no3o2",
      "reference": {
        "notes": "radm2.eqn {007:J07} NO3+hv=NO"
      }
    },
    {
      "id": "R008",
      "name": "008:J08",
      "substrates": [
        {
          "species": "NO3",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "NO2",
          "stoichiometry": 1.0
        },
        {
          "species": "O3P",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.j_no3o",
      "reference": {
        "notes": "radm2.eqn {008:J08} NO3+hv=NO2+O3P"
      }
    },
    {
      "id": "R009",
      "name": "009:J09",
      "substrates": [
        {
          "species": "H2O2",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "OH",
          "stoichiometry": 2.0
        }
      ],
      "rate": "RADM2RateConstants.j_h2o2",
      "reference": {
        "notes": "radm2.eqn {009:J09} H2O2+hv=OH+OH"
      }
    },
    {
      "id": "R010",
      "name": "010:J10",
      "substrates": [
        {
          "species": "HCHO",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "CO",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.j_ch2om",
      "reference": {
        "notes": "radm2.eqn {010:J10} HCHO+hv=CO"
      }
    },
    {
      "id": "R011",
      "name": "011:J11",
      "substrates": [
        {
          "species": "HCHO",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HO2",
          "stoichiometry": 2.0
        },
        {
          "species": "CO",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.j_ch2or",
      "reference": {
        "notes": "radm2.eqn {011:J11} HCHO+hv=HO2+HO2+CO"
      }
    },
    {
      "id": "R012",
      "name": "012:J12",
      "substrates": [
        {
          "species": "ALD",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "MO2",
          "stoichiometry": 1.0
        },
        {
          "species": "HO2",
          "stoichiometry": 1.0
        },
        {
          "species": "CO",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.j_ch3cho",
      "reference": {
        "notes": "radm2.eqn {012:J12} ALD+hv=MO2+HO2+CO"
      }
    },
    {
      "id": "R013",
      "name": "013:J13",
      "substrates": [
        {
          "species": "OP1",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HCHO",
          "stoichiometry": 1.0
        },
        {
          "species": "HO2",
          "stoichiometry": 1.0
        },
        {
          "species": "OH",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.j_ch3o2h",
      "reference": {
        "notes": "radm2.eqn {013:J13} OP1+hv=HCHO+HO2+OH"
      }
    },
    {
      "id": "R014",
      "name": "014:J14",
      "substrates": [
        {
          "species": "OP2",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "ALD",
          "stoichiometry": 1.0
        },
        {
          "species": "HO2",
          "stoichiometry": 1.0
        },
        {
          "species": "OH",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.j_ch3coch3",
      "reference": {
        "notes": "radm2.eqn {014:J14} OP2+hv=ALD+HO2+OH"
      }
    },
    {
      "id": "R015",
      "name": "015:J15",
      "substrates": [
        {
          "species": "PAA",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "MO2",
          "stoichiometry": 1.0
        },
        {
          "species": "OH",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.j_ch3coo2h",
      "reference": {
        "notes": "radm2.eqn {015:J15} PAA+hv=MO2+OH"
      }
    },
    {
      "id": "R016",
      "name": "016:J16",
      "substrates": [
        {
          "species": "KET",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "ACO3",
          "stoichiometry": 1.0
        },
        {
          "species": "ETHP",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.j_ch3coc2h5",
      "reference": {
        "notes": "radm2.eqn {016:J16} KET+hv=ACO3+ETHP"
      }
    },
    {
      "id": "R017",
      "name": "017:J17",
      "substrates": [
        {
          "species": "GLY",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HCHO",
          "stoichiometry": 0.13
        },
        {
          "species": "CO",
          "stoichiometry": 1.87
        }
      ],
      "rate": "RADM2RateConstants.j_hcocho",
      "reference": {
        "notes": "radm2.eqn {017:J17} GLY+hv=0.13 HCHO+1.87 CO"
      }
    },
    {
      "id": "R018",
      "name": "018:J18",
      "substrates": [
        {
          "species": "GLY",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HCHO",
          "stoichiometry": 0.45
        },
        {
          "species": "CO",
          "stoichiometry": 1.55
        },
        {
          "species": "HO2",
          "stoichiometry": 0.8
        }
      ],
      "rate": "RADM2RateConstants.j_hcochob",
      "reference": {
        "notes": "radm2.eqn {018:J18} GLY+hv=0.45 HCHO+1.55 CO+0.80 HO2"
      }
    },
    {
      "id": "R019",
      "name": "019:J19",
      "substrates": [
        {
          "species": "MGLY",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "ACO3",
          "stoichiometry": 1.0
        },
        {
          "species": "HO2",
          "stoichiometry": 1.0
        },
        {
          "species": "CO",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.j_ch3cocho",
      "reference": {
        "notes": "radm2.eqn {019:J19} MGLY+hv=ACO3+HO2+CO"
      }
    },
    {
      "id": "R020",
      "name": "020:J20",
      "substrates": [
        {
          "species": "DCB",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HO2",
          "stoichiometry": 1.0
        },
        {
          "species": "TCO3",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.j_hcochest",
      "reference": {
        "notes": "radm2.eqn {020:J20} DCB+hv=HO2+TCO3"
      }
    },
    {
      "id": "R021",
      "name": "021:J21",
      "substrates": [
        {
          "species": "ONIT",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "ALD",
          "stoichiometry": 0.2
        },
        {
          "species": "KET",
          "stoichiometry": 0.8
        },
        {
          "species": "HO2",
          "stoichiometry": 1.0
        },
        {
          "species": "NO2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.j_ch3ono2",
      "reference": {
        "notes": "radm2.eqn {021:J21} ONIT+hv=0.20 ALD+0.80 KET+HO2+NO2"
      }
    },
    {
      "id": "R022",
      "name": "22:001",
      "substrates": [
        {
          "species": "O3P",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "O3",
          "stoichiometry": 1.0
        }
      ],
      "rate": {
        "op": "*",
        "args": [
          "RADM2RateConstants.k_R022",
          "RADM2RateConstants.M"
        ]
      },
      "reference": {
        "notes": "radm2.eqn {22:001} O3P+M=O3. KPP multiplies this rate by the fixed species M; the factor is RADM2RateConstants.M in the rate."
      }
    },
    {
      "id": "R023",
      "name": "23:002",
      "substrates": [
        {
          "species": "O3P",
          "stoichiometry": 1
        },
        {
          "species": "NO2",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "NO",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R023",
      "reference": {
        "notes": "radm2.eqn {23:002} O3P+NO2=NO"
      }
    },
    {
      "id": "R024",
      "name": "24:003",
      "substrates": [
        {
          "species": "O1D",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "O3P",
          "stoichiometry": 1.0
        }
      ],
      "rate": {
        "op": "*",
        "args": [
          "RADM2RateConstants.k_R024",
          "RADM2RateConstants.M"
        ]
      },
      "reference": {
        "notes": "radm2.eqn {24:003} O1D+M=O3P. KPP multiplies this rate by the fixed species M; the factor is RADM2RateConstants.M in the rate."
      }
    },
    {
      "id": "R025",
      "name": "26:005",
      "substrates": [
        {
          "species": "O1D",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "OH",
          "stoichiometry": 2.0
        }
      ],
      "rate": {
        "op": "*",
        "args": [
          "RADM2RateConstants.k_R025",
          "RADM2RateConstants.H2O"
        ]
      },
      "reference": {
        "notes": "radm2.eqn {26:005} O1D+H2O=OH+OH. KPP multiplies this rate by the fixed species H2O; the factor is RADM2RateConstants.H2O in the rate."
      }
    },
    {
      "id": "R026",
      "name": "27:006",
      "substrates": [
        {
          "species": "O3",
          "stoichiometry": 1
        },
        {
          "species": "NO",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "NO2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R026",
      "reference": {
        "notes": "radm2.eqn {27:006} O3+NO=NO2"
      }
    },
    {
      "id": "R027",
      "name": "28:007",
      "substrates": [
        {
          "species": "O3",
          "stoichiometry": 1
        },
        {
          "species": "OH",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HO2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R027",
      "reference": {
        "notes": "radm2.eqn {28:007} O3+OH=HO2"
      }
    },
    {
      "id": "R028",
      "name": "29:008",
      "substrates": [
        {
          "species": "O3",
          "stoichiometry": 1
        },
        {
          "species": "HO2",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "OH",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R028",
      "reference": {
        "notes": "radm2.eqn {29:008} O3+HO2=OH"
      }
    },
    {
      "id": "R029",
      "name": "30:009",
      "substrates": [
        {
          "species": "HO2",
          "stoichiometry": 1
        },
        {
          "species": "NO",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "NO2",
          "stoichiometry": 1.0
        },
        {
          "species": "OH",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R029",
      "reference": {
        "notes": "radm2.eqn {30:009} HO2+NO=NO2+OH"
      }
    },
    {
      "id": "R030",
      "name": "31:010",
      "substrates": [
        {
          "species": "HO2",
          "stoichiometry": 1
        },
        {
          "species": "NO2",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HNO4",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R030",
      "reference": {
        "notes": "radm2.eqn {31:010} HO2+NO2=HNO4"
      }
    },
    {
      "id": "R031",
      "name": "32:011",
      "substrates": [
        {
          "species": "HNO4",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HO2",
          "stoichiometry": 1.0
        },
        {
          "species": "NO2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R031",
      "reference": {
        "notes": "radm2.eqn {32:011} HNO4=HO2+NO2"
      }
    },
    {
      "id": "R032",
      "name": "33:012",
      "substrates": [
        {
          "species": "HO2",
          "stoichiometry": 2
        }
      ],
      "products": [
        {
          "species": "H2O2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R032",
      "reference": {
        "notes": "radm2.eqn {33:012} HO2+HO2=H2O2"
      }
    },
    {
      "id": "R033",
      "name": "34:013",
      "substrates": [
        {
          "species": "HO2",
          "stoichiometry": 2
        }
      ],
      "products": [
        {
          "species": "H2O2",
          "stoichiometry": 1.0
        }
      ],
      "rate": {
        "op": "*",
        "args": [
          "RADM2RateConstants.k_R033",
          "RADM2RateConstants.H2O"
        ]
      },
      "reference": {
        "notes": "radm2.eqn {34:013} HO2+HO2+H2O=H2O2. KPP multiplies this rate by the fixed species H2O; the factor is RADM2RateConstants.H2O in the rate."
      }
    },
    {
      "id": "R034",
      "name": "35:014",
      "substrates": [
        {
          "species": "H2O2",
          "stoichiometry": 1
        },
        {
          "species": "OH",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HO2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R034",
      "reference": {
        "notes": "radm2.eqn {35:014} H2O2+OH=HO2+H2O. The fixed product H2O is omitted (KPP generates no tendency for a fixed species)."
      }
    },
    {
      "id": "R035",
      "name": "36:015",
      "substrates": [
        {
          "species": "NO",
          "stoichiometry": 1
        },
        {
          "species": "OH",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HONO",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R035",
      "reference": {
        "notes": "radm2.eqn {36:015} NO+OH=HONO"
      }
    },
    {
      "id": "R036",
      "name": "37:016",
      "substrates": [
        {
          "species": "NO",
          "stoichiometry": 2
        }
      ],
      "products": [
        {
          "species": "NO2",
          "stoichiometry": 2.0
        }
      ],
      "rate": {
        "op": "*",
        "args": [
          "RADM2RateConstants.k_R036",
          "RADM2RateConstants.M"
        ]
      },
      "reference": {
        "notes": "radm2.eqn {37:016} NO+NO+M=NO2+NO2. KPP multiplies this rate by the fixed species M; the factor is RADM2RateConstants.M in the rate."
      }
    },
    {
      "id": "R037",
      "name": "38:017",
      "substrates": [
        {
          "species": "O3",
          "stoichiometry": 1
        },
        {
          "species": "NO2",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "NO3",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R037",
      "reference": {
        "notes": "radm2.eqn {38:017} O3+NO2=NO3"
      }
    },
    {
      "id": "R038",
      "name": "39:018",
      "substrates": [
        {
          "species": "NO3",
          "stoichiometry": 1
        },
        {
          "species": "NO",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "NO2",
          "stoichiometry": 2.0
        }
      ],
      "rate": "RADM2RateConstants.k_R038",
      "reference": {
        "notes": "radm2.eqn {39:018} NO3+NO=NO2+NO2"
      }
    },
    {
      "id": "R039",
      "name": "40:019",
      "substrates": [
        {
          "species": "NO3",
          "stoichiometry": 1
        },
        {
          "species": "NO2",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "NO",
          "stoichiometry": 1.0
        },
        {
          "species": "NO2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R039",
      "reference": {
        "notes": "radm2.eqn {40:019} NO3+NO2=NO+NO2"
      }
    },
    {
      "id": "R040",
      "name": "41:020",
      "substrates": [
        {
          "species": "NO3",
          "stoichiometry": 1
        },
        {
          "species": "HO2",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HNO3",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R040",
      "reference": {
        "notes": "radm2.eqn {41:020} NO3+HO2=HNO3"
      }
    },
    {
      "id": "R041",
      "name": "42:021",
      "substrates": [
        {
          "species": "NO3",
          "stoichiometry": 1
        },
        {
          "species": "NO2",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "N2O5",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R041",
      "reference": {
        "notes": "radm2.eqn {42:021} NO3+NO2=N2O5"
      }
    },
    {
      "id": "R042",
      "name": "43:022",
      "substrates": [
        {
          "species": "N2O5",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "NO2",
          "stoichiometry": 1.0
        },
        {
          "species": "NO3",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R042",
      "reference": {
        "notes": "radm2.eqn {43:022} N2O5=NO2+NO3"
      }
    },
    {
      "id": "R043",
      "name": "44:137, 14",
      "substrates": [
        {
          "species": "N2O5",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HNO3",
          "stoichiometry": 2.0
        }
      ],
      "rate": "RADM2RateConstants.k_R043",
      "reference": {
        "notes": "radm2.eqn {44:137, 14} N2O5=2.00 HNO3"
      }
    },
    {
      "id": "R044",
      "name": "45:024",
      "substrates": [
        {
          "species": "OH",
          "stoichiometry": 1
        },
        {
          "species": "NO2",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HNO3",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R044",
      "reference": {
        "notes": "radm2.eqn {45:024} OH+NO2=HNO3"
      }
    },
    {
      "id": "R045",
      "name": "46:025",
      "substrates": [
        {
          "species": "OH",
          "stoichiometry": 1
        },
        {
          "species": "HNO3",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "NO3",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R045",
      "reference": {
        "notes": "radm2.eqn {46:025} OH+HNO3=NO3+H2O. The fixed product H2O is omitted (KPP generates no tendency for a fixed species)."
      }
    },
    {
      "id": "R046",
      "name": "47:026",
      "substrates": [
        {
          "species": "OH",
          "stoichiometry": 1
        },
        {
          "species": "HNO4",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "NO2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R046",
      "reference": {
        "notes": "radm2.eqn {47:026} OH+HNO4=NO2+H2O. The fixed product H2O is omitted (KPP generates no tendency for a fixed species)."
      }
    },
    {
      "id": "R047",
      "name": "48:027",
      "substrates": [
        {
          "species": "OH",
          "stoichiometry": 1
        },
        {
          "species": "HO2",
          "stoichiometry": 1
        }
      ],
      "products": null,
      "rate": "RADM2RateConstants.k_R047",
      "reference": {
        "notes": "radm2.eqn {48:027} OH+HO2=H2O. The fixed product H2O is omitted (KPP generates no tendency for a fixed species)."
      }
    },
    {
      "id": "R048",
      "name": "49:028",
      "substrates": [
        {
          "species": "OH",
          "stoichiometry": 1
        },
        {
          "species": "SO2",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "SULF",
          "stoichiometry": 1.0
        },
        {
          "species": "HO2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R048",
      "reference": {
        "notes": "radm2.eqn {49:028} OH+SO2=SULF+HO2"
      }
    },
    {
      "id": "R049",
      "name": "50:029",
      "substrates": [
        {
          "species": "CO",
          "stoichiometry": 1
        },
        {
          "species": "OH",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HO2",
          "stoichiometry": 1.0
        },
        {
          "species": "CO2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R049",
      "reference": {
        "notes": "radm2.eqn {50:029} CO+OH=HO2+CO2"
      }
    },
    {
      "id": "R050",
      "name": "51:030",
      "substrates": [
        {
          "species": "CH4",
          "stoichiometry": 1
        },
        {
          "species": "OH",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "MO2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R050",
      "reference": {
        "notes": "radm2.eqn {51:030} CH4+OH=MO2+H2O. The fixed product H2O is omitted (KPP generates no tendency for a fixed species)."
      }
    },
    {
      "id": "R051",
      "name": "52:031",
      "substrates": [
        {
          "species": "ETH",
          "stoichiometry": 1
        },
        {
          "species": "OH",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "ETHP",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R051",
      "reference": {
        "notes": "radm2.eqn {52:031} ETH+OH=ETHP+H2O. The fixed product H2O is omitted (KPP generates no tendency for a fixed species)."
      }
    },
    {
      "id": "R052",
      "name": "53:032",
      "substrates": [
        {
          "species": "HC3",
          "stoichiometry": 1
        },
        {
          "species": "OH",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HC3P",
          "stoichiometry": 0.83
        },
        {
          "species": "HO2",
          "stoichiometry": 0.17
        },
        {
          "species": "HCHO",
          "stoichiometry": 0.009
        },
        {
          "species": "ALD",
          "stoichiometry": 0.075
        },
        {
          "species": "KET",
          "stoichiometry": 0.025
        }
      ],
      "rate": "RADM2RateConstants.k_R052",
      "reference": {
        "notes": "radm2.eqn {53:032} HC3+OH=0.83 HC3P+0.17 HO2 +0.009 HCHO+0.075 ALD +0.025 KET+H2O. The fixed product H2O is omitted (KPP generates no tendency for a fixed species)."
      }
    },
    {
      "id": "R053",
      "name": "54:033",
      "substrates": [
        {
          "species": "HC5",
          "stoichiometry": 1
        },
        {
          "species": "OH",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HC5P",
          "stoichiometry": 1.0
        },
        {
          "species": "XO2",
          "stoichiometry": 0.25
        }
      ],
      "rate": "RADM2RateConstants.k_R053",
      "reference": {
        "notes": "radm2.eqn {54:033} HC5+OH=HC5P+0.25 XO2+H2O. The fixed product H2O is omitted (KPP generates no tendency for a fixed species)."
      }
    },
    {
      "id": "R054",
      "name": "55:034",
      "substrates": [
        {
          "species": "HC8",
          "stoichiometry": 1
        },
        {
          "species": "OH",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HC8P",
          "stoichiometry": 1.0
        },
        {
          "species": "XO2",
          "stoichiometry": 0.75
        }
      ],
      "rate": "RADM2RateConstants.k_R054",
      "reference": {
        "notes": "radm2.eqn {55:034} HC8+OH=HC8P+0.75 XO2+H2O. The fixed product H2O is omitted (KPP generates no tendency for a fixed species)."
      }
    },
    {
      "id": "R055",
      "name": "56:035",
      "substrates": [
        {
          "species": "OL2",
          "stoichiometry": 1
        },
        {
          "species": "OH",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "OL2P",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R055",
      "reference": {
        "notes": "radm2.eqn {56:035} OL2+OH=OL2P"
      }
    },
    {
      "id": "R056",
      "name": "57:036",
      "substrates": [
        {
          "species": "OLT",
          "stoichiometry": 1
        },
        {
          "species": "OH",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "OLTP",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R056",
      "reference": {
        "notes": "radm2.eqn {57:036} OLT+OH=OLTP"
      }
    },
    {
      "id": "R057",
      "name": "58:037",
      "substrates": [
        {
          "species": "OLI",
          "stoichiometry": 1
        },
        {
          "species": "OH",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "OLIP",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R057",
      "reference": {
        "notes": "radm2.eqn {58:037} OLI+OH=OLIP"
      }
    },
    {
      "id": "R058",
      "name": "59:038",
      "substrates": [
        {
          "species": "TOL",
          "stoichiometry": 1
        },
        {
          "species": "OH",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "TOLP",
          "stoichiometry": 0.75
        },
        {
          "species": "CSL",
          "stoichiometry": 0.25
        },
        {
          "species": "HO2",
          "stoichiometry": 0.25
        }
      ],
      "rate": "RADM2RateConstants.k_R058",
      "reference": {
        "notes": "radm2.eqn {59:038} TOL+OH=0.75 TOLP+0.25 CSL +0.25 HO2"
      }
    },
    {
      "id": "R059",
      "name": "60:039",
      "substrates": [
        {
          "species": "XYL",
          "stoichiometry": 1
        },
        {
          "species": "OH",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "XYLP",
          "stoichiometry": 0.83
        },
        {
          "species": "CSL",
          "stoichiometry": 0.17
        },
        {
          "species": "HO2",
          "stoichiometry": 0.17
        }
      ],
      "rate": "RADM2RateConstants.k_R059",
      "reference": {
        "notes": "radm2.eqn {60:039} XYL+OH=0.83 XYLP+0.17 CSL +0.17 HO2"
      }
    },
    {
      "id": "R060",
      "name": "61:040",
      "substrates": [
        {
          "species": "CSL",
          "stoichiometry": 1
        },
        {
          "species": "OH",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HO2",
          "stoichiometry": 0.1
        },
        {
          "species": "XO2",
          "stoichiometry": 0.9
        },
        {
          "species": "TCO3",
          "stoichiometry": 0.9
        }
      ],
      "rate": "RADM2RateConstants.k_R060",
      "reference": {
        "notes": "radm2.eqn {61:040} CSL+OH=0.10 HO2+0.90 XO2 +0.90 TCO3-0.90 OH"
      }
    },
    {
      "id": "R060x",
      "name": "61:040 (extra loss of OH)",
      "substrates": [
        {
          "species": "CSL",
          "stoichiometry": 1
        },
        {
          "species": "OH",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "CSL",
          "stoichiometry": 1
        }
      ],
      "rate": {
        "op": "*",
        "args": [
          0.9,
          "RADM2RateConstants.k_R060"
        ]
      },
      "reference": {
        "notes": "KPP net stoichiometry of OH in reaction 60 is -1.9: the product term \"-0.9 OH\" of radm2.eqn is an additional loss written here as a shadow reaction of rate 0.9 k."
      }
    },
    {
      "id": "R061",
      "name": "62:041",
      "substrates": [
        {
          "species": "HCHO",
          "stoichiometry": 1
        },
        {
          "species": "OH",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HO2",
          "stoichiometry": 1.0
        },
        {
          "species": "CO",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R061",
      "reference": {
        "notes": "radm2.eqn {62:041} HCHO+OH=HO2+CO+H2O. The fixed product H2O is omitted (KPP generates no tendency for a fixed species)."
      }
    },
    {
      "id": "R062",
      "name": "63:042",
      "substrates": [
        {
          "species": "ALD",
          "stoichiometry": 1
        },
        {
          "species": "OH",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "ACO3",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R062",
      "reference": {
        "notes": "radm2.eqn {63:042} ALD+OH=ACO3+H2O. The fixed product H2O is omitted (KPP generates no tendency for a fixed species)."
      }
    },
    {
      "id": "R063",
      "name": "64:043",
      "substrates": [
        {
          "species": "KET",
          "stoichiometry": 1
        },
        {
          "species": "OH",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "KETP",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R063",
      "reference": {
        "notes": "radm2.eqn {64:043} KET+OH=KETP+H2O. The fixed product H2O is omitted (KPP generates no tendency for a fixed species)."
      }
    },
    {
      "id": "R064",
      "name": "65:044",
      "substrates": [
        {
          "species": "GLY",
          "stoichiometry": 1
        },
        {
          "species": "OH",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HO2",
          "stoichiometry": 1.0
        },
        {
          "species": "CO",
          "stoichiometry": 2.0
        }
      ],
      "rate": "RADM2RateConstants.k_R064",
      "reference": {
        "notes": "radm2.eqn {65:044} GLY+OH=HO2+2.00 CO+H2O. The fixed product H2O is omitted (KPP generates no tendency for a fixed species)."
      }
    },
    {
      "id": "R065",
      "name": "66:045",
      "substrates": [
        {
          "species": "MGLY",
          "stoichiometry": 1
        },
        {
          "species": "OH",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "ACO3",
          "stoichiometry": 1.0
        },
        {
          "species": "CO",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R065",
      "reference": {
        "notes": "radm2.eqn {66:045} MGLY+OH=ACO3+CO+H2O. The fixed product H2O is omitted (KPP generates no tendency for a fixed species)."
      }
    },
    {
      "id": "R066",
      "name": "67:046",
      "substrates": [
        {
          "species": "DCB",
          "stoichiometry": 1
        },
        {
          "species": "OH",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "TCO3",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R066",
      "reference": {
        "notes": "radm2.eqn {67:046} DCB+OH=TCO3+H2O. The fixed product H2O is omitted (KPP generates no tendency for a fixed species)."
      }
    },
    {
      "id": "R067",
      "name": "68:047",
      "substrates": [
        {
          "species": "OP1",
          "stoichiometry": 1
        },
        {
          "species": "OH",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "MO2",
          "stoichiometry": 0.5
        },
        {
          "species": "HCHO",
          "stoichiometry": 0.5
        },
        {
          "species": "OH",
          "stoichiometry": 0.5
        }
      ],
      "rate": "RADM2RateConstants.k_R067",
      "reference": {
        "notes": "radm2.eqn {68:047} OP1+OH=0.50 MO2+0.50 HCHO +0.50 OH"
      }
    },
    {
      "id": "R068",
      "name": "69:048",
      "substrates": [
        {
          "species": "OP2",
          "stoichiometry": 1
        },
        {
          "species": "OH",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HC3P",
          "stoichiometry": 0.5
        },
        {
          "species": "ALD",
          "stoichiometry": 0.5
        },
        {
          "species": "OH",
          "stoichiometry": 0.5
        }
      ],
      "rate": "RADM2RateConstants.k_R068",
      "reference": {
        "notes": "radm2.eqn {69:048} OP2+OH=0.50 HC3P+0.50 ALD +0.50 OH"
      }
    },
    {
      "id": "R069",
      "name": "70:049",
      "substrates": [
        {
          "species": "PAA",
          "stoichiometry": 1
        },
        {
          "species": "OH",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "ACO3",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R069",
      "reference": {
        "notes": "radm2.eqn {70:049} PAA+OH=ACO3+H2O. The fixed product H2O is omitted (KPP generates no tendency for a fixed species)."
      }
    },
    {
      "id": "R070",
      "name": "71:050",
      "substrates": [
        {
          "species": "PAN",
          "stoichiometry": 1
        },
        {
          "species": "OH",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HCHO",
          "stoichiometry": 1.0
        },
        {
          "species": "NO3",
          "stoichiometry": 1.0
        },
        {
          "species": "XO2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R070",
      "reference": {
        "notes": "radm2.eqn {71:050} PAN+OH=HCHO+NO3+XO2"
      }
    },
    {
      "id": "R071",
      "name": "72:051",
      "substrates": [
        {
          "species": "ONIT",
          "stoichiometry": 1
        },
        {
          "species": "OH",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HC3P",
          "stoichiometry": 1.0
        },
        {
          "species": "NO2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R071",
      "reference": {
        "notes": "radm2.eqn {72:051} ONIT+OH=HC3P+NO2"
      }
    },
    {
      "id": "R072",
      "name": "73:052",
      "substrates": [
        {
          "species": "ISO",
          "stoichiometry": 1
        },
        {
          "species": "OH",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "OLTP",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R072",
      "reference": {
        "notes": "radm2.eqn {73:052} ISO+OH=OLTP"
      }
    },
    {
      "id": "R073",
      "name": "74:053",
      "substrates": [
        {
          "species": "ACO3",
          "stoichiometry": 1
        },
        {
          "species": "NO2",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "PAN",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R073",
      "reference": {
        "notes": "radm2.eqn {74:053} ACO3+NO2=PAN"
      }
    },
    {
      "id": "R074",
      "name": "75:054",
      "substrates": [
        {
          "species": "PAN",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "ACO3",
          "stoichiometry": 1.0
        },
        {
          "species": "NO2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R074",
      "reference": {
        "notes": "radm2.eqn {75:054} PAN=ACO3+NO2"
      }
    },
    {
      "id": "R075",
      "name": "76:055",
      "substrates": [
        {
          "species": "TCO3",
          "stoichiometry": 1
        },
        {
          "species": "NO2",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "TPAN",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R075",
      "reference": {
        "notes": "radm2.eqn {76:055} TCO3+NO2=TPAN"
      }
    },
    {
      "id": "R076",
      "name": "77:056",
      "substrates": [
        {
          "species": "TPAN",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "TCO3",
          "stoichiometry": 1.0
        },
        {
          "species": "NO2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R076",
      "reference": {
        "notes": "radm2.eqn {77:056} TPAN=TCO3+NO2"
      }
    },
    {
      "id": "R077",
      "name": "78:057",
      "substrates": [
        {
          "species": "MO2",
          "stoichiometry": 1
        },
        {
          "species": "NO",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HCHO",
          "stoichiometry": 1.0
        },
        {
          "species": "HO2",
          "stoichiometry": 1.0
        },
        {
          "species": "NO2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R077",
      "reference": {
        "notes": "radm2.eqn {78:057} MO2+NO=HCHO+HO2+NO2"
      }
    },
    {
      "id": "R078",
      "name": "79:058",
      "substrates": [
        {
          "species": "HC3P",
          "stoichiometry": 1
        },
        {
          "species": "NO",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "ALD",
          "stoichiometry": 0.75
        },
        {
          "species": "KET",
          "stoichiometry": 0.25
        },
        {
          "species": "HCHO",
          "stoichiometry": 0.09
        },
        {
          "species": "ONIT",
          "stoichiometry": 0.036
        },
        {
          "species": "NO2",
          "stoichiometry": 0.964
        },
        {
          "species": "HO2",
          "stoichiometry": 0.964
        }
      ],
      "rate": "RADM2RateConstants.k_R078",
      "reference": {
        "notes": "radm2.eqn {79:058} HC3P+NO=0.75 ALD+0.25 KET +0.09 HCHO+0.036 ONIT +0.964 NO2+0.964 HO2"
      }
    },
    {
      "id": "R079",
      "name": "80:060",
      "substrates": [
        {
          "species": "HC5P",
          "stoichiometry": 1
        },
        {
          "species": "NO",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "ALD",
          "stoichiometry": 0.38
        },
        {
          "species": "KET",
          "stoichiometry": 0.69
        },
        {
          "species": "ONIT",
          "stoichiometry": 0.08
        },
        {
          "species": "NO2",
          "stoichiometry": 0.92
        },
        {
          "species": "HO2",
          "stoichiometry": 0.92
        }
      ],
      "rate": "RADM2RateConstants.k_R079",
      "reference": {
        "notes": "radm2.eqn {80:060} HC5P+NO=0.38 ALD+0.69 KET +0.08 ONIT+0.92 NO2 +0.92 HO2"
      }
    },
    {
      "id": "R080",
      "name": "81:062",
      "substrates": [
        {
          "species": "HC8P",
          "stoichiometry": 1
        },
        {
          "species": "NO",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "ALD",
          "stoichiometry": 0.35
        },
        {
          "species": "KET",
          "stoichiometry": 1.06
        },
        {
          "species": "HCHO",
          "stoichiometry": 0.04
        },
        {
          "species": "ONIT",
          "stoichiometry": 0.24
        },
        {
          "species": "NO2",
          "stoichiometry": 0.76
        },
        {
          "species": "HO2",
          "stoichiometry": 0.76
        }
      ],
      "rate": "RADM2RateConstants.k_R080",
      "reference": {
        "notes": "radm2.eqn {81:062} HC8P+NO=0.35 ALD+1.06 KET +0.04 HCHO+0.24 ONIT +0.76 NO2+0.76 HO2"
      }
    },
    {
      "id": "R081",
      "name": "82:064",
      "substrates": [
        {
          "species": "OL2P",
          "stoichiometry": 1
        },
        {
          "species": "NO",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HCHO",
          "stoichiometry": 1.6
        },
        {
          "species": "HO2",
          "stoichiometry": 1.0
        },
        {
          "species": "NO2",
          "stoichiometry": 1.0
        },
        {
          "species": "ALD",
          "stoichiometry": 0.2
        }
      ],
      "rate": "RADM2RateConstants.k_R081",
      "reference": {
        "notes": "radm2.eqn {82:064} OL2P+NO=1.60 HCHO+HO2+NO2 +0.20 ALD"
      }
    },
    {
      "id": "R082",
      "name": "83:065",
      "substrates": [
        {
          "species": "OLTP",
          "stoichiometry": 1
        },
        {
          "species": "NO",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "ALD",
          "stoichiometry": 1.0
        },
        {
          "species": "HCHO",
          "stoichiometry": 1.0
        },
        {
          "species": "HO2",
          "stoichiometry": 1.0
        },
        {
          "species": "NO2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R082",
      "reference": {
        "notes": "radm2.eqn {83:065} OLTP+NO=ALD+HCHO+HO2+NO2"
      }
    },
    {
      "id": "R083",
      "name": "84:066",
      "substrates": [
        {
          "species": "OLIP",
          "stoichiometry": 1
        },
        {
          "species": "NO",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HO2",
          "stoichiometry": 1.0
        },
        {
          "species": "ALD",
          "stoichiometry": 1.45
        },
        {
          "species": "HCHO",
          "stoichiometry": 0.28
        },
        {
          "species": "KET",
          "stoichiometry": 0.1
        },
        {
          "species": "NO2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R083",
      "reference": {
        "notes": "radm2.eqn {84:066} OLIP+NO=HO2+1.45 ALD +0.28 HCHO+0.10 KET+NO2"
      }
    },
    {
      "id": "R084",
      "name": "85:067",
      "substrates": [
        {
          "species": "ACO3",
          "stoichiometry": 1
        },
        {
          "species": "NO",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "MO2",
          "stoichiometry": 1.0
        },
        {
          "species": "NO2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R084",
      "reference": {
        "notes": "radm2.eqn {85:067} ACO3+NO=MO2+NO2"
      }
    },
    {
      "id": "R085",
      "name": "86:068",
      "substrates": [
        {
          "species": "TCO3",
          "stoichiometry": 1
        },
        {
          "species": "NO",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "NO2",
          "stoichiometry": 1.0
        },
        {
          "species": "HO2",
          "stoichiometry": 0.92
        },
        {
          "species": "GLY",
          "stoichiometry": 0.89
        },
        {
          "species": "MGLY",
          "stoichiometry": 0.11
        },
        {
          "species": "ACO3",
          "stoichiometry": 0.05
        },
        {
          "species": "CO",
          "stoichiometry": 0.95
        },
        {
          "species": "XO2",
          "stoichiometry": 2.0
        }
      ],
      "rate": "RADM2RateConstants.k_R085",
      "reference": {
        "notes": "radm2.eqn {86:068} TCO3+NO=NO2+0.92 HO2 +0.89 GLY+0.11 MGLY +0.05 ACO3+0.95 CO +2.00 XO2"
      }
    },
    {
      "id": "R086",
      "name": "87:069",
      "substrates": [
        {
          "species": "TOLP",
          "stoichiometry": 1
        },
        {
          "species": "NO",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "NO2",
          "stoichiometry": 1.0
        },
        {
          "species": "HO2",
          "stoichiometry": 1.0
        },
        {
          "species": "MGLY",
          "stoichiometry": 0.17
        },
        {
          "species": "GLY",
          "stoichiometry": 0.16
        },
        {
          "species": "DCB",
          "stoichiometry": 0.7
        }
      ],
      "rate": "RADM2RateConstants.k_R086",
      "reference": {
        "notes": "radm2.eqn {87:069} TOLP+NO=NO2+HO2+0.17 MGLY +0.16 GLY+0.70 DCB"
      }
    },
    {
      "id": "R087",
      "name": "88:070",
      "substrates": [
        {
          "species": "XYLP",
          "stoichiometry": 1
        },
        {
          "species": "NO",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "NO2",
          "stoichiometry": 1.0
        },
        {
          "species": "HO2",
          "stoichiometry": 1.0
        },
        {
          "species": "MGLY",
          "stoichiometry": 0.45
        },
        {
          "species": "DCB",
          "stoichiometry": 0.806
        }
      ],
      "rate": "RADM2RateConstants.k_R087",
      "reference": {
        "notes": "radm2.eqn {88:070} XYLP+NO=NO2+HO2+0.45 MGLY +0.806 DCB"
      }
    },
    {
      "id": "R088",
      "name": "89:071",
      "substrates": [
        {
          "species": "ETHP",
          "stoichiometry": 1
        },
        {
          "species": "NO",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "ALD",
          "stoichiometry": 1.0
        },
        {
          "species": "HO2",
          "stoichiometry": 1.0
        },
        {
          "species": "NO2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R088",
      "reference": {
        "notes": "radm2.eqn {89:071} ETHP+NO=ALD+HO2+NO2"
      }
    },
    {
      "id": "R089",
      "name": "90:072",
      "substrates": [
        {
          "species": "KETP",
          "stoichiometry": 1
        },
        {
          "species": "NO",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "MGLY",
          "stoichiometry": 1.0
        },
        {
          "species": "NO2",
          "stoichiometry": 1.0
        },
        {
          "species": "HO2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R089",
      "reference": {
        "notes": "radm2.eqn {90:072} KETP+NO=MGLY+NO2+HO2"
      }
    },
    {
      "id": "R090",
      "name": "91:073",
      "substrates": [
        {
          "species": "OLN",
          "stoichiometry": 1
        },
        {
          "species": "NO",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HCHO",
          "stoichiometry": 1.0
        },
        {
          "species": "ALD",
          "stoichiometry": 1.0
        },
        {
          "species": "NO2",
          "stoichiometry": 2.0
        }
      ],
      "rate": "RADM2RateConstants.k_R090",
      "reference": {
        "notes": "radm2.eqn {91:073} OLN+NO=HCHO+ALD+2.00 NO2"
      }
    },
    {
      "id": "R091",
      "name": "92:074",
      "substrates": [
        {
          "species": "HCHO",
          "stoichiometry": 1
        },
        {
          "species": "NO3",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HO2",
          "stoichiometry": 1.0
        },
        {
          "species": "HNO3",
          "stoichiometry": 1.0
        },
        {
          "species": "CO",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R091",
      "reference": {
        "notes": "radm2.eqn {92:074} HCHO+NO3=HO2+HNO3+CO"
      }
    },
    {
      "id": "R092",
      "name": "93:075",
      "substrates": [
        {
          "species": "ALD",
          "stoichiometry": 1
        },
        {
          "species": "NO3",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "ACO3",
          "stoichiometry": 1.0
        },
        {
          "species": "HNO3",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R092",
      "reference": {
        "notes": "radm2.eqn {93:075} ALD+NO3=ACO3+HNO3"
      }
    },
    {
      "id": "R093",
      "name": "94:076",
      "substrates": [
        {
          "species": "GLY",
          "stoichiometry": 1
        },
        {
          "species": "NO3",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HNO3",
          "stoichiometry": 1.0
        },
        {
          "species": "HO2",
          "stoichiometry": 1.0
        },
        {
          "species": "CO",
          "stoichiometry": 2.0
        }
      ],
      "rate": "RADM2RateConstants.k_R093",
      "reference": {
        "notes": "radm2.eqn {94:076} GLY+NO3=HNO3+HO2+2.00 CO"
      }
    },
    {
      "id": "R094",
      "name": "95:077",
      "substrates": [
        {
          "species": "MGLY",
          "stoichiometry": 1
        },
        {
          "species": "NO3",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HNO3",
          "stoichiometry": 1.0
        },
        {
          "species": "ACO3",
          "stoichiometry": 1.0
        },
        {
          "species": "CO",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R094",
      "reference": {
        "notes": "radm2.eqn {95:077} MGLY+NO3=HNO3+ACO3+CO"
      }
    },
    {
      "id": "R095",
      "name": "96:078",
      "substrates": [
        {
          "species": "DCB",
          "stoichiometry": 1
        },
        {
          "species": "NO3",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HNO3",
          "stoichiometry": 1.0
        },
        {
          "species": "TCO3",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R095",
      "reference": {
        "notes": "radm2.eqn {96:078} DCB+NO3=HNO3+TCO3"
      }
    },
    {
      "id": "R096",
      "name": "97:079",
      "substrates": [
        {
          "species": "CSL",
          "stoichiometry": 1
        },
        {
          "species": "NO3",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HNO3",
          "stoichiometry": 1.0
        },
        {
          "species": "XNO2",
          "stoichiometry": 1.0
        },
        {
          "species": "CSL",
          "stoichiometry": 0.5
        }
      ],
      "rate": "RADM2RateConstants.k_R096",
      "reference": {
        "notes": "radm2.eqn {97:079} CSL+NO3=HNO3+XNO2+0.50 CSL"
      }
    },
    {
      "id": "R097",
      "name": "98:080",
      "substrates": [
        {
          "species": "OL2",
          "stoichiometry": 1
        },
        {
          "species": "NO3",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "OLN",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R097",
      "reference": {
        "notes": "radm2.eqn {98:080} OL2+NO3=OLN"
      }
    },
    {
      "id": "R098",
      "name": "99:081",
      "substrates": [
        {
          "species": "OLT",
          "stoichiometry": 1
        },
        {
          "species": "NO3",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "OLN",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R098",
      "reference": {
        "notes": "radm2.eqn {99:081} OLT+NO3=OLN"
      }
    },
    {
      "id": "R099",
      "name": "100:082",
      "substrates": [
        {
          "species": "OLI",
          "stoichiometry": 1
        },
        {
          "species": "NO3",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "OLN",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R099",
      "reference": {
        "notes": "radm2.eqn {100:082} OLI+NO3=OLN"
      }
    },
    {
      "id": "R100",
      "name": "101:083",
      "substrates": [
        {
          "species": "ISO",
          "stoichiometry": 1
        },
        {
          "species": "NO3",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "OLN",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R100",
      "reference": {
        "notes": "radm2.eqn {101:083} ISO+NO3=OLN"
      }
    },
    {
      "id": "R101",
      "name": "102:084",
      "substrates": [
        {
          "species": "OL2",
          "stoichiometry": 1
        },
        {
          "species": "O3",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HCHO",
          "stoichiometry": 1.0
        },
        {
          "species": "CO",
          "stoichiometry": 0.42
        },
        {
          "species": "ORA1",
          "stoichiometry": 0.4
        },
        {
          "species": "HO2",
          "stoichiometry": 0.12
        }
      ],
      "rate": "RADM2RateConstants.k_R101",
      "reference": {
        "notes": "radm2.eqn {102:084} OL2+O3=HCHO+0.42 CO+0.40 ORA1 +0.12 HO2"
      }
    },
    {
      "id": "R102",
      "name": "103:085",
      "substrates": [
        {
          "species": "OLT",
          "stoichiometry": 1
        },
        {
          "species": "O3",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HCHO",
          "stoichiometry": 0.53
        },
        {
          "species": "ALD",
          "stoichiometry": 0.5
        },
        {
          "species": "CO",
          "stoichiometry": 0.33
        },
        {
          "species": "ORA1",
          "stoichiometry": 0.2
        },
        {
          "species": "ORA2",
          "stoichiometry": 0.2
        },
        {
          "species": "HO2",
          "stoichiometry": 0.23
        },
        {
          "species": "MO2",
          "stoichiometry": 0.22
        },
        {
          "species": "OH",
          "stoichiometry": 0.1
        },
        {
          "species": "CH4",
          "stoichiometry": 0.06
        }
      ],
      "rate": "RADM2RateConstants.k_R102",
      "reference": {
        "notes": "radm2.eqn {103:085} OLT+O3=0.53 HCHO+0.50 ALD +0.33 CO+0.20 ORA1 +0.20 ORA2+0.23 HO2 +0.22 MO2+0.10 OH +0.06 CH4"
      }
    },
    {
      "id": "R103",
      "name": "104:086",
      "substrates": [
        {
          "species": "OLI",
          "stoichiometry": 1
        },
        {
          "species": "O3",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HCHO",
          "stoichiometry": 0.18
        },
        {
          "species": "ALD",
          "stoichiometry": 0.72
        },
        {
          "species": "KET",
          "stoichiometry": 0.1
        },
        {
          "species": "CO",
          "stoichiometry": 0.23
        },
        {
          "species": "ORA1",
          "stoichiometry": 0.06
        },
        {
          "species": "ORA2",
          "stoichiometry": 0.29
        },
        {
          "species": "CH4",
          "stoichiometry": 0.09
        },
        {
          "species": "HO2",
          "stoichiometry": 0.26
        },
        {
          "species": "MO2",
          "stoichiometry": 0.31
        },
        {
          "species": "OH",
          "stoichiometry": 0.14
        }
      ],
      "rate": "RADM2RateConstants.k_R103",
      "reference": {
        "notes": "radm2.eqn {104:086} OLI+O3=0.18 HCHO+0.72 ALD +0.10 KET+0.23 CO +0.06 ORA1+0.29 ORA2 +0.09 CH4+0.26 HO2 +0.31 MO2+0.14 OH"
      }
    },
    {
      "id": "R104",
      "name": "105:087",
      "substrates": [
        {
          "species": "ISO",
          "stoichiometry": 1
        },
        {
          "species": "O3",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HCHO",
          "stoichiometry": 0.53
        },
        {
          "species": "ALD",
          "stoichiometry": 0.5
        },
        {
          "species": "CO",
          "stoichiometry": 0.33
        },
        {
          "species": "ORA1",
          "stoichiometry": 0.2
        },
        {
          "species": "ORA2",
          "stoichiometry": 0.2
        },
        {
          "species": "HO2",
          "stoichiometry": 0.23
        },
        {
          "species": "MO2",
          "stoichiometry": 0.22
        },
        {
          "species": "OH",
          "stoichiometry": 0.1
        }
      ],
      "rate": "RADM2RateConstants.k_R104",
      "reference": {
        "notes": "radm2.eqn {105:087} ISO+O3=0.53 HCHO+0.50 ALD +0.33 CO+0.20 ORA1 +0.20 ORA2+0.23 HO2 +0.22 MO2+0.10 OH"
      }
    },
    {
      "id": "R105",
      "name": "106:088",
      "substrates": [
        {
          "species": "HO2",
          "stoichiometry": 1
        },
        {
          "species": "MO2",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "OP1",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R105",
      "reference": {
        "notes": "radm2.eqn {106:088} HO2+MO2=OP1"
      }
    },
    {
      "id": "R106",
      "name": "107:089",
      "substrates": [
        {
          "species": "HO2",
          "stoichiometry": 1
        },
        {
          "species": "ETHP",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "OP2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R106",
      "reference": {
        "notes": "radm2.eqn {107:089} HO2+ETHP=OP2"
      }
    },
    {
      "id": "R107",
      "name": "108:090",
      "substrates": [
        {
          "species": "HO2",
          "stoichiometry": 1
        },
        {
          "species": "HC3P",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "OP2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R107",
      "reference": {
        "notes": "radm2.eqn {108:090} HO2+HC3P=OP2"
      }
    },
    {
      "id": "R108",
      "name": "109:091",
      "substrates": [
        {
          "species": "HO2",
          "stoichiometry": 1
        },
        {
          "species": "HC5P",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "OP2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R108",
      "reference": {
        "notes": "radm2.eqn {109:091} HO2+HC5P=OP2"
      }
    },
    {
      "id": "R109",
      "name": "110:092",
      "substrates": [
        {
          "species": "HO2",
          "stoichiometry": 1
        },
        {
          "species": "HC8P",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "OP2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R109",
      "reference": {
        "notes": "radm2.eqn {110:092} HO2+HC8P=OP2"
      }
    },
    {
      "id": "R110",
      "name": "111:093",
      "substrates": [
        {
          "species": "HO2",
          "stoichiometry": 1
        },
        {
          "species": "OL2P",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "OP2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R110",
      "reference": {
        "notes": "radm2.eqn {111:093} HO2+OL2P=OP2"
      }
    },
    {
      "id": "R111",
      "name": "112:094",
      "substrates": [
        {
          "species": "HO2",
          "stoichiometry": 1
        },
        {
          "species": "OLTP",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "OP2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R111",
      "reference": {
        "notes": "radm2.eqn {112:094} HO2+OLTP=OP2"
      }
    },
    {
      "id": "R112",
      "name": "113:095",
      "substrates": [
        {
          "species": "HO2",
          "stoichiometry": 1
        },
        {
          "species": "OLIP",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "OP2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R112",
      "reference": {
        "notes": "radm2.eqn {113:095} HO2+OLIP=OP2"
      }
    },
    {
      "id": "R113",
      "name": "114:096",
      "substrates": [
        {
          "species": "HO2",
          "stoichiometry": 1
        },
        {
          "species": "KETP",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "OP2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R113",
      "reference": {
        "notes": "radm2.eqn {114:096} HO2+KETP=OP2"
      }
    },
    {
      "id": "R114",
      "name": "115:097",
      "substrates": [
        {
          "species": "HO2",
          "stoichiometry": 1
        },
        {
          "species": "ACO3",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "PAA",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R114",
      "reference": {
        "notes": "radm2.eqn {115:097} HO2+ACO3=PAA"
      }
    },
    {
      "id": "R115",
      "name": "116:098",
      "substrates": [
        {
          "species": "HO2",
          "stoichiometry": 1
        },
        {
          "species": "TOLP",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "OP2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R115",
      "reference": {
        "notes": "radm2.eqn {116:098} HO2+TOLP= OP2"
      }
    },
    {
      "id": "R116",
      "name": "117:099",
      "substrates": [
        {
          "species": "HO2",
          "stoichiometry": 1
        },
        {
          "species": "XYLP",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "OP2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R116",
      "reference": {
        "notes": "radm2.eqn {117:099} HO2+XYLP=OP2"
      }
    },
    {
      "id": "R117",
      "name": "118:100",
      "substrates": [
        {
          "species": "HO2",
          "stoichiometry": 1
        },
        {
          "species": "TCO3",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "OP2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R117",
      "reference": {
        "notes": "radm2.eqn {118:100} HO2+TCO3=OP2"
      }
    },
    {
      "id": "R118",
      "name": "119:101",
      "substrates": [
        {
          "species": "HO2",
          "stoichiometry": 1
        },
        {
          "species": "OLN",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "ONIT",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R118",
      "reference": {
        "notes": "radm2.eqn {119:101} HO2+OLN=ONIT"
      }
    },
    {
      "id": "R119",
      "name": "120:102",
      "substrates": [
        {
          "species": "MO2",
          "stoichiometry": 2
        }
      ],
      "products": [
        {
          "species": "HCHO",
          "stoichiometry": 1.5
        },
        {
          "species": "HO2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R119",
      "reference": {
        "notes": "radm2.eqn {120:102} MO2+MO2=1.50 HCHO+HO2"
      }
    },
    {
      "id": "R120",
      "name": "121:103",
      "substrates": [
        {
          "species": "MO2",
          "stoichiometry": 1
        },
        {
          "species": "ETHP",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HCHO",
          "stoichiometry": 0.75
        },
        {
          "species": "HO2",
          "stoichiometry": 1.0
        },
        {
          "species": "ALD",
          "stoichiometry": 0.75
        }
      ],
      "rate": "RADM2RateConstants.k_R120",
      "reference": {
        "notes": "radm2.eqn {121:103} MO2+ETHP=0.75 HCHO+HO2 +0.75 ALD"
      }
    },
    {
      "id": "R121",
      "name": "122:104",
      "substrates": [
        {
          "species": "MO2",
          "stoichiometry": 1
        },
        {
          "species": "HC3P",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HCHO",
          "stoichiometry": 0.75
        },
        {
          "species": "HO2",
          "stoichiometry": 1.0
        },
        {
          "species": "ALD",
          "stoichiometry": 0.15
        },
        {
          "species": "KET",
          "stoichiometry": 0.6
        }
      ],
      "rate": "RADM2RateConstants.k_R121",
      "reference": {
        "notes": "radm2.eqn {122:104} MO2+HC3P=0.75 HCHO+HO2 +0.15 ALD+0.6 KET"
      }
    },
    {
      "id": "R122",
      "name": "123:105",
      "substrates": [
        {
          "species": "MO2",
          "stoichiometry": 1
        },
        {
          "species": "HC5P",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HCHO",
          "stoichiometry": 0.77
        },
        {
          "species": "HO2",
          "stoichiometry": 1.0
        },
        {
          "species": "ALD",
          "stoichiometry": 0.41
        },
        {
          "species": "KET",
          "stoichiometry": 0.75
        }
      ],
      "rate": "RADM2RateConstants.k_R122",
      "reference": {
        "notes": "radm2.eqn {123:105} MO2+HC5P=0.77 HCHO+HO2 +0.41 ALD+0.75 KET"
      }
    },
    {
      "id": "R123",
      "name": "124:106",
      "substrates": [
        {
          "species": "MO2",
          "stoichiometry": 1
        },
        {
          "species": "HC8P",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HCHO",
          "stoichiometry": 0.8
        },
        {
          "species": "HO2",
          "stoichiometry": 1.0
        },
        {
          "species": "ALD",
          "stoichiometry": 0.46
        },
        {
          "species": "KET",
          "stoichiometry": 1.39
        }
      ],
      "rate": "RADM2RateConstants.k_R123",
      "reference": {
        "notes": "radm2.eqn {124:106} MO2+HC8P=0.80 HCHO+HO2 +0.46 ALD+1.39 KET"
      }
    },
    {
      "id": "R124",
      "name": "125:107",
      "substrates": [
        {
          "species": "MO2",
          "stoichiometry": 1
        },
        {
          "species": "OL2P",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HCHO",
          "stoichiometry": 1.55
        },
        {
          "species": "HO2",
          "stoichiometry": 1.0
        },
        {
          "species": "ALD",
          "stoichiometry": 0.35
        }
      ],
      "rate": "RADM2RateConstants.k_R124",
      "reference": {
        "notes": "radm2.eqn {125:107} MO2+OL2P=1.55 HCHO+HO2 +0.35 ALD"
      }
    },
    {
      "id": "R125",
      "name": "126:108",
      "substrates": [
        {
          "species": "MO2",
          "stoichiometry": 1
        },
        {
          "species": "OLTP",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HCHO",
          "stoichiometry": 1.25
        },
        {
          "species": "HO2",
          "stoichiometry": 1.0
        },
        {
          "species": "ALD",
          "stoichiometry": 0.75
        }
      ],
      "rate": "RADM2RateConstants.k_R125",
      "reference": {
        "notes": "radm2.eqn {126:108} MO2+OLTP=1.25 HCHO+HO2 +0.75 ALD"
      }
    },
    {
      "id": "R126",
      "name": "127:109",
      "substrates": [
        {
          "species": "MO2",
          "stoichiometry": 1
        },
        {
          "species": "OLIP",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HCHO",
          "stoichiometry": 0.89
        },
        {
          "species": "HO2",
          "stoichiometry": 1.0
        },
        {
          "species": "ALD",
          "stoichiometry": 0.725
        },
        {
          "species": "KET",
          "stoichiometry": 0.55
        }
      ],
      "rate": "RADM2RateConstants.k_R126",
      "reference": {
        "notes": "radm2.eqn {127:109} MO2+OLIP=0.89 HCHO+HO2 +0.725 ALD+0.55 KET"
      }
    },
    {
      "id": "R127",
      "name": "128:110",
      "substrates": [
        {
          "species": "MO2",
          "stoichiometry": 1
        },
        {
          "species": "KETP",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HCHO",
          "stoichiometry": 0.75
        },
        {
          "species": "HO2",
          "stoichiometry": 1.0
        },
        {
          "species": "MGLY",
          "stoichiometry": 0.75
        }
      ],
      "rate": "RADM2RateConstants.k_R127",
      "reference": {
        "notes": "radm2.eqn {128:110} MO2+KETP=0.75 HCHO+HO2 +0.75 MGLY"
      }
    },
    {
      "id": "R128",
      "name": "129:111",
      "substrates": [
        {
          "species": "MO2",
          "stoichiometry": 1
        },
        {
          "species": "ACO3",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HCHO",
          "stoichiometry": 1.0
        },
        {
          "species": "HO2",
          "stoichiometry": 0.5
        },
        {
          "species": "MO2",
          "stoichiometry": 0.5
        },
        {
          "species": "ORA2",
          "stoichiometry": 0.5
        }
      ],
      "rate": "RADM2RateConstants.k_R128",
      "reference": {
        "notes": "radm2.eqn {129:111} MO2+ACO3=HCHO+0.50 HO2 +0.50 MO2+0.50 ORA2"
      }
    },
    {
      "id": "R129",
      "name": "130:112",
      "substrates": [
        {
          "species": "MO2",
          "stoichiometry": 1
        },
        {
          "species": "TOLP",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HCHO",
          "stoichiometry": 1.0
        },
        {
          "species": "HO2",
          "stoichiometry": 2.0
        },
        {
          "species": "MGLY",
          "stoichiometry": 0.17
        },
        {
          "species": "GLY",
          "stoichiometry": 0.16
        },
        {
          "species": "DCB",
          "stoichiometry": 0.7
        }
      ],
      "rate": "RADM2RateConstants.k_R129",
      "reference": {
        "notes": "radm2.eqn {130:112} MO2+TOLP=HCHO+2.00 HO2 +0.17 MGLY+0.16 GLY +0.70 DCB"
      }
    },
    {
      "id": "R130",
      "name": "131:113",
      "substrates": [
        {
          "species": "MO2",
          "stoichiometry": 1
        },
        {
          "species": "XYLP",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HCHO",
          "stoichiometry": 1.0
        },
        {
          "species": "HO2",
          "stoichiometry": 2.0
        },
        {
          "species": "MGLY",
          "stoichiometry": 0.45
        },
        {
          "species": "DCB",
          "stoichiometry": 0.806
        }
      ],
      "rate": "RADM2RateConstants.k_R130",
      "reference": {
        "notes": "radm2.eqn {131:113} MO2+XYLP=HCHO+2.00 HO2 +0.45 MGLY+0.806 DCB"
      }
    },
    {
      "id": "R131",
      "name": "132:114",
      "substrates": [
        {
          "species": "MO2",
          "stoichiometry": 1
        },
        {
          "species": "TCO3",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HCHO",
          "stoichiometry": 0.5
        },
        {
          "species": "ORA2",
          "stoichiometry": 0.5
        },
        {
          "species": "GLY",
          "stoichiometry": 0.445
        },
        {
          "species": "MGLY",
          "stoichiometry": 0.055
        },
        {
          "species": "ACO3",
          "stoichiometry": 0.025
        },
        {
          "species": "CO",
          "stoichiometry": 0.475
        },
        {
          "species": "HO2",
          "stoichiometry": 0.46
        },
        {
          "species": "XO2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R131",
      "reference": {
        "notes": "radm2.eqn {132:114} MO2+TCO3=0.50 HCHO+0.50 ORA2 +0.445 GLY+0.055 MGLY +0.025 ACO3+0.475 CO +0.46 HO2+XO2"
      }
    },
    {
      "id": "R132",
      "name": "133:115",
      "substrates": [
        {
          "species": "ETHP",
          "stoichiometry": 1
        },
        {
          "species": "ACO3",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "ALD",
          "stoichiometry": 1.0
        },
        {
          "species": "HO2",
          "stoichiometry": 0.5
        },
        {
          "species": "MO2",
          "stoichiometry": 0.5
        },
        {
          "species": "ORA2",
          "stoichiometry": 0.5
        }
      ],
      "rate": "RADM2RateConstants.k_R132",
      "reference": {
        "notes": "radm2.eqn {133:115} ETHP+ACO3=ALD+0.50 HO2 +0.50 MO2+0.50 ORA2"
      }
    },
    {
      "id": "R133",
      "name": "134:116",
      "substrates": [
        {
          "species": "HC3P",
          "stoichiometry": 1
        },
        {
          "species": "ACO3",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "ALD",
          "stoichiometry": 0.2
        },
        {
          "species": "KET",
          "stoichiometry": 0.8
        },
        {
          "species": "HO2",
          "stoichiometry": 0.5
        },
        {
          "species": "ORA2",
          "stoichiometry": 0.5
        },
        {
          "species": "MO2",
          "stoichiometry": 0.5
        }
      ],
      "rate": "RADM2RateConstants.k_R133",
      "reference": {
        "notes": "radm2.eqn {134:116} HC3P+ACO3=0.2 ALD+0.8 KET +0.50 HO2+0.50 ORA2 +0.50 MO2"
      }
    },
    {
      "id": "R134",
      "name": "135:117",
      "substrates": [
        {
          "species": "HC5P",
          "stoichiometry": 1
        },
        {
          "species": "ACO3",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "ALD",
          "stoichiometry": 0.14
        },
        {
          "species": "KET",
          "stoichiometry": 0.86
        },
        {
          "species": "HO2",
          "stoichiometry": 0.5
        },
        {
          "species": "ORA2",
          "stoichiometry": 0.5
        },
        {
          "species": "MO2",
          "stoichiometry": 0.5
        }
      ],
      "rate": "RADM2RateConstants.k_R134",
      "reference": {
        "notes": "radm2.eqn {135:117} HC5P+ACO3=0.14 ALD+0.86 KET +0.50 HO2+0.50 ORA2 +0.50 MO2"
      }
    },
    {
      "id": "R135",
      "name": "136:118",
      "substrates": [
        {
          "species": "HC8P",
          "stoichiometry": 1
        },
        {
          "species": "ACO3",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "ALD",
          "stoichiometry": 0.1
        },
        {
          "species": "KET",
          "stoichiometry": 0.9
        },
        {
          "species": "HO2",
          "stoichiometry": 0.5
        },
        {
          "species": "ORA2",
          "stoichiometry": 0.5
        },
        {
          "species": "MO2",
          "stoichiometry": 0.5
        }
      ],
      "rate": "RADM2RateConstants.k_R135",
      "reference": {
        "notes": "radm2.eqn {136:118} HC8P+ACO3=0.1 ALD+0.9 KET +0.50 HO2+0.50 ORA2 +0.50 MO2"
      }
    },
    {
      "id": "R136",
      "name": "137:119",
      "substrates": [
        {
          "species": "OL2P",
          "stoichiometry": 1
        },
        {
          "species": "ACO3",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HCHO",
          "stoichiometry": 0.8
        },
        {
          "species": "ALD",
          "stoichiometry": 0.6
        },
        {
          "species": "HO2",
          "stoichiometry": 0.5
        },
        {
          "species": "ORA2",
          "stoichiometry": 0.5
        },
        {
          "species": "MO2",
          "stoichiometry": 0.5
        }
      ],
      "rate": "RADM2RateConstants.k_R136",
      "reference": {
        "notes": "radm2.eqn {137:119} OL2P+ACO3=0.80 HCHO+0.60 ALD +0.50 HO2+0.50 ORA2 +0.50 MO2"
      }
    },
    {
      "id": "R137",
      "name": "138:120",
      "substrates": [
        {
          "species": "OLTP",
          "stoichiometry": 1
        },
        {
          "species": "ACO3",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "ALD",
          "stoichiometry": 1.0
        },
        {
          "species": "HCHO",
          "stoichiometry": 0.5
        },
        {
          "species": "HO2",
          "stoichiometry": 0.5
        },
        {
          "species": "ORA2",
          "stoichiometry": 0.5
        },
        {
          "species": "MO2",
          "stoichiometry": 0.5
        }
      ],
      "rate": "RADM2RateConstants.k_R137",
      "reference": {
        "notes": "radm2.eqn {138:120} OLTP+ACO3=ALD+0.50 HCHO +0.50 HO2+0.50 ORA2 +0.50 MO2"
      }
    },
    {
      "id": "R138",
      "name": "139:121",
      "substrates": [
        {
          "species": "OLIP",
          "stoichiometry": 1
        },
        {
          "species": "ACO3",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "ALD",
          "stoichiometry": 0.725
        },
        {
          "species": "KET",
          "stoichiometry": 0.55
        },
        {
          "species": "HCHO",
          "stoichiometry": 0.14
        },
        {
          "species": "HO2",
          "stoichiometry": 0.5
        },
        {
          "species": "MO2",
          "stoichiometry": 0.5
        },
        {
          "species": "ORA2",
          "stoichiometry": 0.5
        }
      ],
      "rate": "RADM2RateConstants.k_R138",
      "reference": {
        "notes": "radm2.eqn {139:121} OLIP+ACO3=0.725 ALD+0.55 KET +0.14 HCHO+0.50 HO2 +0.50 MO2+0.50 ORA2"
      }
    },
    {
      "id": "R139",
      "name": "140:122",
      "substrates": [
        {
          "species": "KETP",
          "stoichiometry": 1
        },
        {
          "species": "ACO3",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "MGLY",
          "stoichiometry": 1.0
        },
        {
          "species": "HO2",
          "stoichiometry": 0.5
        },
        {
          "species": "ORA2",
          "stoichiometry": 0.5
        },
        {
          "species": "MO2",
          "stoichiometry": 0.5
        }
      ],
      "rate": "RADM2RateConstants.k_R139",
      "reference": {
        "notes": "radm2.eqn {140:122} KETP+ACO3=MGLY+0.50 HO2 +0.50 ORA2+0.50 MO2"
      }
    },
    {
      "id": "R140",
      "name": "141:123",
      "substrates": [
        {
          "species": "ACO3",
          "stoichiometry": 2
        }
      ],
      "products": [
        {
          "species": "MO2",
          "stoichiometry": 2.0
        }
      ],
      "rate": "RADM2RateConstants.k_R140",
      "reference": {
        "notes": "radm2.eqn {141:123} ACO3+ACO3=2.00 MO2"
      }
    },
    {
      "id": "R141",
      "name": "142:124",
      "substrates": [
        {
          "species": "ACO3",
          "stoichiometry": 1
        },
        {
          "species": "TOLP",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "MGLY",
          "stoichiometry": 0.8
        },
        {
          "species": "GLY",
          "stoichiometry": 0.2
        },
        {
          "species": "DCB",
          "stoichiometry": 1.0
        },
        {
          "species": "HO2",
          "stoichiometry": 1.0
        },
        {
          "species": "MO2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R141",
      "reference": {
        "notes": "radm2.eqn {142:124} ACO3+TOLP=0.8 MGLY+0.2 GLY +1.00 DCB+HO2+MO2"
      }
    },
    {
      "id": "R142",
      "name": "143:125",
      "substrates": [
        {
          "species": "ACO3",
          "stoichiometry": 1
        },
        {
          "species": "XYLP",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "MO2",
          "stoichiometry": 1.0
        },
        {
          "species": "MGLY",
          "stoichiometry": 1.0
        },
        {
          "species": "DCB",
          "stoichiometry": 1.0
        },
        {
          "species": "HO2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R142",
      "reference": {
        "notes": "radm2.eqn {143:125} ACO3+XYLP=MO2+1.00 MGLY +1.00 DCB+HO2"
      }
    },
    {
      "id": "R143",
      "name": "144:126",
      "substrates": [
        {
          "species": "ACO3",
          "stoichiometry": 1
        },
        {
          "species": "TCO3",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "MO2",
          "stoichiometry": 1.0
        },
        {
          "species": "HO2",
          "stoichiometry": 0.92
        },
        {
          "species": "GLY",
          "stoichiometry": 0.89
        },
        {
          "species": "MGLY",
          "stoichiometry": 0.11
        },
        {
          "species": "ACO3",
          "stoichiometry": 0.05
        },
        {
          "species": "CO",
          "stoichiometry": 0.95
        },
        {
          "species": "XO2",
          "stoichiometry": 2.0
        }
      ],
      "rate": "RADM2RateConstants.k_R143",
      "reference": {
        "notes": "radm2.eqn {144:126} ACO3+TCO3=MO2+0.92 HO2 +0.89 GLY+0.11 MGLY +0.05 ACO3+0.95 CO +2.00 XO2"
      }
    },
    {
      "id": "R144",
      "name": "145:127",
      "substrates": [
        {
          "species": "XO2",
          "stoichiometry": 1
        },
        {
          "species": "HO2",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "OP2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R144",
      "reference": {
        "notes": "radm2.eqn {145:127} XO2+HO2=OP2"
      }
    },
    {
      "id": "R145",
      "name": "146:128",
      "substrates": [
        {
          "species": "XO2",
          "stoichiometry": 1
        },
        {
          "species": "MO2",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HCHO",
          "stoichiometry": 1.0
        },
        {
          "species": "HO2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R145",
      "reference": {
        "notes": "radm2.eqn {146:128} XO2+MO2=HCHO+HO2"
      }
    },
    {
      "id": "R146",
      "name": "147:129",
      "substrates": [
        {
          "species": "XO2",
          "stoichiometry": 1
        },
        {
          "species": "ACO3",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "MO2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R146",
      "reference": {
        "notes": "radm2.eqn {147:129} XO2+ACO3=MO2"
      }
    },
    {
      "id": "R147",
      "name": "148:130",
      "substrates": [
        {
          "species": "XO2",
          "stoichiometry": 2
        }
      ],
      "products": null,
      "rate": "RADM2RateConstants.k_R147",
      "reference": {
        "notes": "radm2.eqn {148:130} XO2+XO2=H2O. The fixed product H2O is omitted (KPP generates no tendency for a fixed species)."
      }
    },
    {
      "id": "R148",
      "name": "149:131",
      "substrates": [
        {
          "species": "XO2",
          "stoichiometry": 1
        },
        {
          "species": "NO",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "NO2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R148",
      "reference": {
        "notes": "radm2.eqn {149:131} XO2+NO=NO2"
      }
    },
    {
      "id": "R149",
      "name": "150:132",
      "substrates": [
        {
          "species": "XNO2",
          "stoichiometry": 1
        },
        {
          "species": "NO2",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "ONIT",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R149",
      "reference": {
        "notes": "radm2.eqn {150:132} XNO2+NO2=ONIT"
      }
    },
    {
      "id": "R150",
      "name": "151:133",
      "substrates": [
        {
          "species": "XNO2",
          "stoichiometry": 1
        },
        {
          "species": "HO2",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "OP2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R150",
      "reference": {
        "notes": "radm2.eqn {151:133} XNO2+HO2=OP2"
      }
    },
    {
      "id": "R151",
      "name": "152:134",
      "substrates": [
        {
          "species": "XNO2",
          "stoichiometry": 1
        },
        {
          "species": "MO2",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HCHO",
          "stoichiometry": 1.0
        },
        {
          "species": "HO2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R151",
      "reference": {
        "notes": "radm2.eqn {152:134} XNO2+MO2=HCHO+HO2"
      }
    },
    {
      "id": "R152",
      "name": "153:135",
      "substrates": [
        {
          "species": "XNO2",
          "stoichiometry": 1
        },
        {
          "species": "ACO3",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "MO2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R152",
      "reference": {
        "notes": "radm2.eqn {153:135} XNO2+ACO3=MO2"
      }
    },
    {
      "id": "R153",
      "name": "154:136",
      "substrates": [
        {
          "species": "XNO2",
          "stoichiometry": 2
        }
      ],
      "products": null,
      "rate": "RADM2RateConstants.k_R153",
      "reference": {
        "notes": "radm2.eqn {154:136} XNO2+XNO2=H2O. The fixed product H2O is omitted (KPP generates no tendency for a fixed species)."
      }
    },
    {
      "id": "R154",
      "name": "155:138",
      "substrates": [
        {
          "species": "MO2",
          "stoichiometry": 1
        },
        {
          "species": "OLN",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HCHO",
          "stoichiometry": 1.75
        },
        {
          "species": "HO2",
          "stoichiometry": 0.5
        },
        {
          "species": "ALD",
          "stoichiometry": 1.0
        },
        {
          "species": "NO2",
          "stoichiometry": 1.0
        }
      ],
      "rate": "RADM2RateConstants.k_R154",
      "reference": {
        "notes": "radm2.eqn {155:138} MO2+OLN=1.75 HCHO+.5 HO2 +ALD+NO2"
      }
    },
    {
      "id": "R155",
      "name": "156:139",
      "substrates": [
        {
          "species": "ACO3",
          "stoichiometry": 1
        },
        {
          "species": "OLN",
          "stoichiometry": 1
        }
      ],
      "products": [
        {
          "species": "HCHO",
          "stoichiometry": 1.0
        },
        {
          "species": "ALD",
          "stoichiometry": 1.0
        },
        {
          "species": "ORA2",
          "stoichiometry": 0.5
        },
        {
          "species": "NO2",
          "stoichiometry": 1.0
        },
        {
          "species": "MO2",
          "stoichiometry": 0.5
        }
      ],
      "rate": "RADM2RateConstants.k_R155",
      "reference": {
        "notes": "radm2.eqn {156:139} ACO3+OLN=HCHO+ALD+0.50 ORA2 +NO2+0.50 MO2"
      }
    },
    {
      "id": "R156",
      "name": "157:140",
      "substrates": [
        {
          "species": "OLN",
          "stoichiometry": 2
        }
      ],
      "products": [
        {
          "species": "HCHO",
          "stoichiometry": 2.0
        },
        {
          "species": "ALD",
          "stoichiometry": 2.0
        },
        {
          "species": "NO2",
          "stoichiometry": 2.0
        }
      ],
      "rate": "RADM2RateConstants.k_R156",
      "reference": {
        "notes": "radm2.eqn {157:140} OLN+OLN=2.00 HCHO+2.00 ALD +2.00 NO2"
      }
    }
  ],
  "tests": [
    {
      "id": "box_urban_noon_trajectory",
      "description": "Trajectory of the urban noon box state (T 298 K, p 101325 Pa, M 2.462e19 and H2O 6.963e17 molec/cm3 (RH 0.550), clear-sky noon photolysis, dump box_urban_noon.json): the concentrations of 12 species after 60, 300 and 1800 s, from the KPP Rosenbrock (Rodas3, ICNTRL(3)=4 as WRF) solver of the standalone WRF-Chem RADM2 box driver (real64, KPP-generated code from chem/KPP/mechanisms/radm2 of WRF v4.8.0 with WRFUserRateLaws; RTOL 1e-9, ATOL 1e-3 molec/cm3). Tolerance rel 1e-5 is the solver-to-solver agreement expected between the KPP Rosenbrock at rtol 1e-9 and the binding integrator; the rate coefficients themselves are pinned to 1e-9 by the RADM2RateConstants tests. The environment (T, p, M, H2O and the photolysis frequencies) is set through scoped parameter_overrides into RADM2RateConstants, whose observeds every reaction rate references, and both it and the initial state are identical to the matching RADM2Tendencies test. Measured agreement with the KPP Rosenbrock reference (Rust CLI) is within rel 3e-8 on every one of the 12 species at all three output times in the three box regimes, and within 2.4e-7 in the WRF-Chem regime, where the largest residual is NO3, a species that sits at about 1e-3 of its night-time box value in that late-afternoon column. The document declares `solver.abstol` 1e-3 molec/cm^3 (the box driver's own ATOL): the runner default of 1e-6 is meaningless for a state carried in molec/cm^3 and collapses the step size to zero at t ~ 1e-14 s in both daylight regimes. There is NO WRF-Chem reference run behind this state; the initial state is a typical mixing-ratio profile (make_states.py).",
      "time_span": {
        "start": 0,
        "end": 1800
      },
      "initial_conditions": {
        "O3": 1477411357577.5947,
        "H2O2": 24623522626.293247,
        "NO": 492470452525.86487,
        "NO2": 984940905051.7297,
        "NO3": 49247045.2525865,
        "N2O5": 1231176131.3146625,
        "HONO": 12311761313.146624,
        "HNO3": 49247045252.586494,
        "HNO4": 1231176131.3146625,
        "SO2": 123117613131.46622,
        "SULF": 2462352262.629325,
        "CO": 12311761313146.623,
        "ETH": 246235226262.93243,
        "HC3": 492470452525.86487,
        "HC5": 246235226262.93243,
        "HC8": 123117613131.46622,
        "OL2": 123117613131.46622,
        "OLT": 49247045252.586494,
        "OLI": 24623522626.293247,
        "ISO": 24623522626.293247,
        "TOL": 123117613131.46622,
        "XYL": 73870567878.87975,
        "CSL": 4924704525.25865,
        "HCHO": 123117613131.46622,
        "ALD": 49247045252.586494,
        "ETHP": 24623522.62629325,
        "KET": 49247045252.586494,
        "GLY": 4924704525.25865,
        "MGLY": 7387056787.887973,
        "MO2": 123117613.13146622,
        "DCB": 2462352262.629325,
        "ONIT": 12311761313.146624,
        "PAN": 24623522626.293247,
        "TPAN": 1231176131.3146625,
        "OP1": 12311761313.146624,
        "OP2": 7387056787.887973,
        "PAA": 2462352262.629325,
        "ORA1": 12311761313.146624,
        "ORA2": 12311761313.146624,
        "OH": 4924704.525258649,
        "HO2": 492470452.5258649,
        "O3P": 2462.3522626293243,
        "O1D": 2.4623522626293246,
        "HC3P": 24623522.62629325,
        "HC5P": 12311761.313146625,
        "HC8P": 7387056.787887973,
        "OLTP": 7387056.787887973,
        "OLIP": 4924704.525258649,
        "TOLP": 4924704.525258649,
        "XYLP": 4924704.525258649,
        "ACO3": 49247045.2525865,
        "TCO3": 4924704.525258649,
        "KETP": 4924704.525258649,
        "OLN": 2462352.2626293246,
        "XO2": 24623522.62629325,
        "XNO2": 2462352.2626293246,
        "CH4": 44322340727327.84,
        "CO2": 9849409050517298.0,
        "OL2P": 7387056.787887973
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
          "variable": "O3",
          "time": 60.0,
          "expected": 1378033627747.4736,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "NO",
          "time": 60.0,
          "expected": 380064762803.44464,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "NO2",
          "time": 60.0,
          "expected": 1096692662485.5603,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "OH",
          "time": 60.0,
          "expected": 3611799.298709912,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "HO2",
          "time": 60.0,
          "expected": 27158296.65821768,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "HCHO",
          "time": 60.0,
          "expected": 125015150410.4064,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "HNO3",
          "time": 60.0,
          "expected": 53134277458.900505,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "PAN",
          "time": 60.0,
          "expected": 24691666832.837154,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "H2O2",
          "time": 60.0,
          "expected": 24601002724.564888,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "CO",
          "time": 60.0,
          "expected": 12312168126130.168,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "NO3",
          "time": 60.0,
          "expected": 4527193.137633351,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "N2O5",
          "time": 60.0,
          "expected": 149380988.94980866,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "O3",
          "time": 300.0,
          "expected": 1388613481150.5195,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "NO",
          "time": 300.0,
          "expected": 364992789741.9138,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "NO2",
          "time": 300.0,
          "expected": 1103673149159.0046,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "OH",
          "time": 300.0,
          "expected": 3151183.073403459,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "HO2",
          "time": 300.0,
          "expected": 24381751.65412995,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "HCHO",
          "time": 300.0,
          "expected": 128993237773.74113,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "HNO3",
          "time": 300.0,
          "expected": 63420475059.18359,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "PAN",
          "time": 300.0,
          "expected": 24755592244.999912,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "H2O2",
          "time": 300.0,
          "expected": 24526343590.066555,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "CO",
          "time": 300.0,
          "expected": 12314511104080.904,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "NO3",
          "time": 300.0,
          "expected": 4561742.267684117,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "N2O5",
          "time": 300.0,
          "expected": 110377343.24548937,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "O3",
          "time": 1800.0,
          "expected": 1498110359526.3162,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "NO",
          "time": 1800.0,
          "expected": 331901103685.95074,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "NO2",
          "time": 1800.0,
          "expected": 1082161286618.1239,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "OH",
          "time": 1800.0,
          "expected": 2682088.992589267,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "HO2",
          "time": 1800.0,
          "expected": 22685414.840452127,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "HCHO",
          "time": 1800.0,
          "expected": 144054280774.59448,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "HNO3",
          "time": 1800.0,
          "expected": 118206676922.95946,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "PAN",
          "time": 1800.0,
          "expected": 25824316704.331432,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "H2O2",
          "time": 1800.0,
          "expected": 24093101875.65752,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "CO",
          "time": 1800.0,
          "expected": 12332398207093.225,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "NO3",
          "time": 1800.0,
          "expected": 5288223.356997348,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "N2O5",
          "time": 1800.0,
          "expected": 125515203.36765033,
          "tolerance": {
            "rel": 1e-05
          }
        }
      ]
    },
    {
      "id": "box_rural_morning_trajectory",
      "description": "Trajectory of the rural morning box state (T 288 K, p 95000 Pa, M 2.389e19 and H2O 5.558e17 molec/cm3 (RH 0.800), 35 % of noon photolysis, dump box_rural_morning.json): the concentrations of 12 species after 60, 300 and 1800 s, from the KPP Rosenbrock (Rodas3, ICNTRL(3)=4 as WRF) solver of the standalone WRF-Chem RADM2 box driver (real64, KPP-generated code from chem/KPP/mechanisms/radm2 of WRF v4.8.0 with WRFUserRateLaws; RTOL 1e-9, ATOL 1e-3 molec/cm3). Tolerance rel 1e-5 is the solver-to-solver agreement expected between the KPP Rosenbrock at rtol 1e-9 and the binding integrator; the rate coefficients themselves are pinned to 1e-9 by the RADM2RateConstants tests. The environment (T, p, M, H2O and the photolysis frequencies) is set through scoped parameter_overrides into RADM2RateConstants, whose observeds every reaction rate references, and both it and the initial state are identical to the matching RADM2Tendencies test. Measured agreement with the KPP Rosenbrock reference (Rust CLI) is within rel 3e-8 on every one of the 12 species at all three output times in the three box regimes, and within 2.4e-7 in the WRF-Chem regime, where the largest residual is NO3, a species that sits at about 1e-3 of its night-time box value in that late-afternoon column. The document declares `solver.abstol` 1e-3 molec/cm^3 (the box driver's own ATOL): the runner default of 1e-6 is meaningless for a state carried in molec/cm^3 and collapses the step size to zero at t ~ 1e-14 s in both daylight regimes. There is NO WRF-Chem reference run behind this state; the initial state is a typical mixing-ratio profile (make_states.py).",
      "time_span": {
        "start": 0,
        "end": 1800
      },
      "initial_conditions": {
        "O3": 1074962875571.1233,
        "H2O2": 47776127803.161026,
        "NO": 2388806390.1580515,
        "NO2": 11944031950.790257,
        "NO3": 23888063.901580516,
        "N2O5": 119440319.50790258,
        "HONO": 238880639.01580516,
        "HNO3": 11944031950.790257,
        "HNO4": 238880639.01580516,
        "SO2": 11944031950.790257,
        "SULF": 1194403195.0790257,
        "CO": 2866567668189.662,
        "ETH": 23888063901.580513,
        "HC3": 47776127803.161026,
        "HC5": 23888063901.580513,
        "HC8": 11944031950.790257,
        "OL2": 7166419170.4741535,
        "OLT": 4777612780.316103,
        "OLI": 2388806390.1580515,
        "ISO": 47776127803.161026,
        "TOL": 4777612780.316103,
        "XYL": 2388806390.1580515,
        "CSL": 477761278.0316103,
        "HCHO": 23888063901.580513,
        "ALD": 11944031950.790257,
        "ETHP": 11944031.950790258,
        "KET": 11944031950.790257,
        "GLY": 1194403195.0790257,
        "MGLY": 2388806390.1580515,
        "MO2": 191104511.21264413,
        "DCB": 477761278.0316103,
        "ONIT": 2388806390.1580515,
        "PAN": 7166419170.4741535,
        "TPAN": 238880639.01580516,
        "OP1": 11944031950.790257,
        "OP2": 4777612780.316103,
        "PAA": 1194403195.0790257,
        "ORA1": 7166419170.4741535,
        "ORA2": 7166419170.4741535,
        "OH": 7166419.170474154,
        "HO2": 716641917.0474154,
        "O3P": 2388.8063901580513,
        "O1D": 2.3888063901580514,
        "HC3P": 11944031.950790258,
        "HC5P": 4777612.780316103,
        "HC8P": 2388806.3901580516,
        "OLTP": 4777612.780316103,
        "OLIP": 2388806.3901580516,
        "TOLP": 1194403.1950790258,
        "XYLP": 1194403.1950790258,
        "ACO3": 47776127.80316103,
        "TCO3": 1194403.1950790258,
        "KETP": 2388806.3901580516,
        "OLN": 1194403.1950790258,
        "XO2": 11944031.950790258,
        "XNO2": 477761.27803161036,
        "CH4": 42998515022844.93,
        "CO2": 9555225560632206.0,
        "OL2P": 2388806.3901580516
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
          "variable": "O3",
          "time": 60.0,
          "expected": 1074985283159.6597,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "NO",
          "time": 60.0,
          "expected": 1743378220.6576655,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "NO2",
          "time": 60.0,
          "expected": 12599178258.603727,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "OH",
          "time": 60.0,
          "expected": 1339613.0755707785,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "HO2",
          "time": 60.0,
          "expected": 371962932.7897664,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "HCHO",
          "time": 60.0,
          "expected": 24187052379.08568,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "HNO3",
          "time": 60.0,
          "expected": 11995443393.059206,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "PAN",
          "time": 60.0,
          "expected": 7211212536.066992,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "H2O2",
          "time": 60.0,
          "expected": 47866472673.50548,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "CO",
          "time": 60.0,
          "expected": 2866601298258.9307,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "NO3",
          "time": 60.0,
          "expected": 5868622.281014714,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "N2O5",
          "time": 60.0,
          "expected": 44161966.294101804,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "O3",
          "time": 300.0,
          "expected": 1076750955312.4758,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "NO",
          "time": 300.0,
          "expected": 1578375854.7703145,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "NO2",
          "time": 300.0,
          "expected": 12739835321.99853,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "OH",
          "time": 300.0,
          "expected": 1256443.3476526807,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "HO2",
          "time": 300.0,
          "expected": 352834464.8119104,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "HCHO",
          "time": 300.0,
          "expected": 25531597954.38395,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "HNO3",
          "time": 300.0,
          "expected": 12068526142.813519,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "PAN",
          "time": 300.0,
          "expected": 7279526636.813861,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "H2O2",
          "time": 300.0,
          "expected": 48060092341.44036,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "CO",
          "time": 300.0,
          "expected": 2866777680241.605,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "NO3",
          "time": 300.0,
          "expected": 2115660.3339721817,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "N2O5",
          "time": 300.0,
          "expected": 2541744.1476282105,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "O3",
          "time": 1800.0,
          "expected": 1088002297459.727,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "NO",
          "time": 1800.0,
          "expected": 1469278239.7742798,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "NO2",
          "time": 1800.0,
          "expected": 11898483993.013119,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "OH",
          "time": 1800.0,
          "expected": 1359995.732693168,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "HO2",
          "time": 1800.0,
          "expected": 353114401.0270677,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "HCHO",
          "time": 1800.0,
          "expected": 33157136269.843784,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "HNO3",
          "time": 1800.0,
          "expected": 12408063795.488466,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "PAN",
          "time": 1800.0,
          "expected": 7836140558.542414,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "H2O2",
          "time": 1800.0,
          "expected": 49254126436.179924,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "CO",
          "time": 1800.0,
          "expected": 2868060111028.319,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "NO3",
          "time": 1800.0,
          "expected": 2061381.8487134478,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "N2O5",
          "time": 1800.0,
          "expected": 1720322.5556821944,
          "tolerance": {
            "rel": 1e-05
          }
        }
      ]
    },
    {
      "id": "box_urban_night_trajectory",
      "description": "Trajectory of the urban night box state (T 283 K, p 101325 Pa, M 2.593e19 and H2O 4.554e17 molec/cm3 (RH 0.900), every photolysis rate zero, dump box_urban_night.json): the concentrations of 12 species after 60, 300 and 1800 s, from the KPP Rosenbrock (Rodas3, ICNTRL(3)=4 as WRF) solver of the standalone WRF-Chem RADM2 box driver (real64, KPP-generated code from chem/KPP/mechanisms/radm2 of WRF v4.8.0 with WRFUserRateLaws; RTOL 1e-9, ATOL 1e-3 molec/cm3). Tolerance rel 1e-5 is the solver-to-solver agreement expected between the KPP Rosenbrock at rtol 1e-9 and the binding integrator; the rate coefficients themselves are pinned to 1e-9 by the RADM2RateConstants tests. The environment (T, p, M, H2O and the photolysis frequencies) is set through scoped parameter_overrides into RADM2RateConstants, whose observeds every reaction rate references, and both it and the initial state are identical to the matching RADM2Tendencies test. Measured agreement with the KPP Rosenbrock reference (Rust CLI) is within rel 3e-8 on every one of the 12 species at all three output times in the three box regimes, and within 2.4e-7 in the WRF-Chem regime, where the largest residual is NO3, a species that sits at about 1e-3 of its night-time box value in that late-afternoon column. The document declares `solver.abstol` 1e-3 molec/cm^3 (the box driver's own ATOL): the runner default of 1e-6 is meaningless for a state carried in molec/cm^3 and collapses the step size to zero at t ~ 1e-14 s in both daylight regimes. There is NO WRF-Chem reference run behind this state; the initial state is a typical mixing-ratio profile (make_states.py).",
      "time_span": {
        "start": 0,
        "end": 1800
      },
      "initial_conditions": {
        "O3": 518573126688.0133,
        "H2O2": 25928656334.400665,
        "NO": 51857312668.80133,
        "NO2": 777859690032.02,
        "NO3": 1296432816.7200334,
        "N2O5": 25928656334.400665,
        "HONO": 25928656334.400665,
        "HNO3": 51857312668.80133,
        "HNO4": 1296432816.7200334,
        "SO2": 129643281672.00333,
        "SULF": 2592865633.440067,
        "CO": 12964328167200.334,
        "ETH": 259286563344.00665,
        "HC3": 518573126688.0133,
        "HC5": 259286563344.00665,
        "HC8": 129643281672.00333,
        "OL2": 129643281672.00333,
        "OLT": 51857312668.80133,
        "OLI": 25928656334.400665,
        "ISO": 25928656334.400665,
        "TOL": 129643281672.00333,
        "XYL": 77785969003.202,
        "CSL": 5185731266.880134,
        "HCHO": 129643281672.00333,
        "ALD": 51857312668.80133,
        "ETHP": 25928656.33440067,
        "KET": 51857312668.80133,
        "GLY": 5185731266.880134,
        "MGLY": 7778596900.320199,
        "MO2": 12964328.167200334,
        "DCB": 2592865633.440067,
        "ONIT": 12964328167.200333,
        "PAN": 25928656334.400665,
        "TPAN": 1296432816.7200334,
        "OP1": 12964328167.200333,
        "OP2": 7778596900.320199,
        "PAA": 2592865633.440067,
        "ORA1": 12964328167.200333,
        "ORA2": 12964328167.200333,
        "OH": 51857.31266880133,
        "HO2": 51857312.66880134,
        "O3P": 0.0,
        "O1D": 0.0,
        "HC3P": 25928656.33440067,
        "HC5P": 12964328.167200334,
        "HC8P": 7778596.900320198,
        "OLTP": 7778596.900320198,
        "OLIP": 5185731.266880133,
        "TOLP": 5185731.266880133,
        "XYLP": 5185731.266880133,
        "ACO3": 51857312.66880134,
        "TCO3": 5185731.266880133,
        "KETP": 5185731.266880133,
        "OLN": 51857312.66880134,
        "XO2": 25928656.33440067,
        "XNO2": 2592865.6334400666,
        "CH4": 46671581401921.195,
        "CO2": 1.0371462533760266e+16,
        "OL2P": 7778596.900320198
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
          "variable": "O3",
          "time": 60.0,
          "expected": 501209697173.7672,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "NO",
          "time": 60.0,
          "expected": 28450800244.462555,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "NO2",
          "time": 60.0,
          "expected": 810618595440.9172,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "OH",
          "time": 60.0,
          "expected": 126970.9588873039,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "HO2",
          "time": 60.0,
          "expected": 15148308.325070024,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "HCHO",
          "time": 60.0,
          "expected": 130073525394.4527,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "HNO3",
          "time": 60.0,
          "expected": 61006028861.563896,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "PAN",
          "time": 60.0,
          "expected": 25983994596.04835,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "H2O2",
          "time": 60.0,
          "expected": 25928327485.256157,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "CO",
          "time": 60.0,
          "expected": 12964341400299.016,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "NO3",
          "time": 60.0,
          "expected": 68867274.9942089,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "N2O5",
          "time": 60.0,
          "expected": 16952986041.450079,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "O3",
          "time": 300.0,
          "expected": 479349153693.47723,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "NO",
          "time": 300.0,
          "expected": 3387532202.245021,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "NO2",
          "time": 300.0,
          "expected": 841350947343.1088,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "OH",
          "time": 300.0,
          "expected": 23813.08694877994,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "HO2",
          "time": 300.0,
          "expected": 16699190.248900624,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "HCHO",
          "time": 300.0,
          "expected": 130881692643.19818,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "HNO3",
          "time": 300.0,
          "expected": 77341732152.26741,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "PAN",
          "time": 300.0,
          "expected": 25995319596.241882,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "H2O2",
          "time": 300.0,
          "expected": 25928255369.05614,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "CO",
          "time": 300.0,
          "expected": 12964440257321.545,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "NO3",
          "time": 300.0,
          "expected": 36652132.4234493,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "N2O5",
          "time": 300.0,
          "expected": 5261467696.672275,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "O3",
          "time": 1800.0,
          "expected": 462041642989.01984,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "NO",
          "time": 1800.0,
          "expected": 251847.0338751573,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "NO2",
          "time": 1800.0,
          "expected": 822126834884.472,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "OH",
          "time": 1800.0,
          "expected": 7648.976590691869,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "HO2",
          "time": 1800.0,
          "expected": 24008166.610116746,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "HCHO",
          "time": 1800.0,
          "expected": 132103523842.82626,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "HNO3",
          "time": 1800.0,
          "expected": 102783815105.5276,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "PAN",
          "time": 1800.0,
          "expected": 26012718683.16701,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "H2O2",
          "time": 1800.0,
          "expected": 25933367659.372944,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "CO",
          "time": 1800.0,
          "expected": 12965111087855.348,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "NO3",
          "time": 1800.0,
          "expected": 18043176.53748655,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "N2O5",
          "time": 1800.0,
          "expected": 1764973093.2064292,
          "tolerance": {
            "rel": 1e-05
          }
        }
      ]
    },
    {
      "id": "wrfchem_scm_midtrop_trajectory",
      "description": "Trajectory of a real WRF-Chem state, the mid-troposphere level k = 45 (T = 254.674 K, p = 490.1 hPa, M = 1.3939e19 and H2O = 1.027e16 molec/cm3, RH = 0.156, late-afternoon TUV/Madronich photolysis) of the first chemistry call of an idealized single-column WRF-Chem run: WRF v4.8.0 em_scm_xy ideal case, 1999-10-22 19:00 UTC, 59 levels, chem_opt = 101 (RADM2 KPP), phot_opt = 1 (Madronich TUV), emiss_opt = 0, chem_in_opt = 0 (species from the built-in idealized profiles of chem/module_input_chem_data.F), no dry deposition; ctessum-claude/WRF branch earthsciml-instrumented-chem, commit 2ce0388 (v4.8.0-6-g2ce03882), the same state as wrfchem_scm_midtrop_tendencies (dump dumps/radm2/box_wrfchem_k45.json): the concentrations of 12 species after 60, 300 and 1800 s, from the KPP Rosenbrock (Rodas3, ICNTRL(3)=4 as WRF) solver of the standalone WRF-Chem RADM2 box driver (real64, KPP-generated code from chem/KPP/mechanisms/radm2 of WRF v4.8.0 with WRFUserRateLaws; RTOL 1e-9, ATOL 1e-3 molec/cm3). Tolerance rel 1e-5 is the solver-to-solver agreement expected between the KPP Rosenbrock at rtol 1e-9 and the binding integrator; the rate coefficients themselves are pinned to 1e-9 by the RADM2RateConstants tests. The environment (T, p, M, H2O and the photolysis frequencies) is set through scoped parameter_overrides into RADM2RateConstants, whose observeds every reaction rate references, and both it and the initial state are identical to the matching RADM2Tendencies test. Measured agreement with the KPP Rosenbrock reference (Rust CLI) is within rel 3e-8 on every one of the 12 species at all three output times in the three box regimes, and within 2.4e-7 in the WRF-Chem regime, where the largest residual is NO3, a species that sits at about 1e-3 of its night-time box value in that late-afternoon column. The document declares `solver.abstol` 1e-3 molec/cm^3 (the box driver's own ATOL): the runner default of 1e-6 is meaningless for a state carried in molec/cm^3 and collapses the step size to zero at t ~ 1e-14 s in both daylight regimes. The reference is the box driver, not WRF-Chem's own 60 s chemistry step (var_out of the dump), because WRF integrates at RTOL 1e-3 and its result is not a reference at rel 1e-5.",
      "time_span": {
        "start": 0,
        "end": 1800
      },
      "initial_conditions": {
        "SULF": 696928722.0572433,
        "ORA1": 696928671.3490074,
        "ORA2": 836314405.6188089,
        "CO2": 427354071.527174,
        "SO2": 1393857444.1144867,
        "ETH": 8920687804.599072,
        "O1D": 0.0,
        "HC5": 6007525202.807504,
        "HC8": 2578636109.345445,
        "TOL": 0.13938573534499446,
        "XYL": 0.13938573534499446,
        "TPAN": 9589738.761161875,
        "HONO": 0.13938573534499446,
        "H2O2": 19235232241.980854,
        "N2O5": 172577.6695157276,
        "HC3": 345676650.3998845,
        "CH4": 23695576089109.83,
        "PAA": 801798881.3224971,
        "O3P": 0.0,
        "HNO4": 2245036.8312564474,
        "OP1": 21465403178.9659,
        "CSL": 0.13938573534499446,
        "PAN": 163081312.64524424,
        "OL2": 2578636109.345445,
        "HNO3": 975700190.5968463,
        "CO": 1115085877403.739,
        "ISO": 0.0013938574014135715,
        "OLT": 1360404815.153169,
        "OLI": 680202407.5765845,
        "DCB": 0.13938573534499446,
        "GLY": 0.13938573534499446,
        "XNO2": 0.0,
        "KET": 177019878.465989,
        "MGLY": 0.13938573534499446,
        "TOLP": 0.0,
        "XYLP": 0.0,
        "OLTP": 0.0,
        "OLN": 0.0,
        "XO2": 0.0,
        "OL2P": 0.0,
        "HC5P": 0.0,
        "OP2": 10732701589.48295,
        "HCHO": 7122611076.965915,
        "HC8P": 0.0,
        "TCO3": 0.0,
        "O3": 418157204026.4021,
        "ONIT": 0.13938573534499446,
        "ALD": 416763360.1720949,
        "OLIP": 0.0,
        "KETP": 0.0,
        "HO2": 0.0013938574014135715,
        "MO2": 0.0,
        "OH": 0.0013938574014135715,
        "NO3": 1553198.9142220845,
        "ACO3": 801798881.3224971,
        "HC3P": 0.0,
        "ETHP": 0.0,
        "NO": 75268294.73090453,
        "NO2": 225804890.53124312
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
          "variable": "O3",
          "time": 60.0,
          "expected": 418169454739.1641,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "NO",
          "time": 60.0,
          "expected": 61961621.950245716,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "NO2",
          "time": 60.0,
          "expected": 192414024.43204424,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "OH",
          "time": 60.0,
          "expected": 200818.14594394667,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "HO2",
          "time": 60.0,
          "expected": 15464392.834232276,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "HCHO",
          "time": 60.0,
          "expected": 7128813756.240589,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "HNO3",
          "time": 60.0,
          "expected": 975718317.9485192,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "PAN",
          "time": 60.0,
          "expected": 211072810.05131033,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "H2O2",
          "time": 60.0,
          "expected": 19232597839.28491,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "CO",
          "time": 60.0,
          "expected": 1115093205608.886,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "NO3",
          "time": 60.0,
          "expected": 96360.98187768755,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "N2O5",
          "time": 60.0,
          "expected": 180183.60904570692,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "O3",
          "time": 300.0,
          "expected": 418198792765.24207,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "NO",
          "time": 300.0,
          "expected": 40969821.38091815,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "NO2",
          "time": 300.0,
          "expected": 135752430.3001792,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "OH",
          "time": 300.0,
          "expected": 239964.28138924376,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "HO2",
          "time": 300.0,
          "expected": 48230562.75961836,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "HCHO",
          "time": 300.0,
          "expected": 7190941094.064608,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "HNO3",
          "time": 300.0,
          "expected": 975779692.2122573,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "PAN",
          "time": 300.0,
          "expected": 286858203.54647917,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "H2O2",
          "time": 300.0,
          "expected": 19222988977.58484,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "CO",
          "time": 300.0,
          "expected": 1115121097550.147,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "NO3",
          "time": 300.0,
          "expected": 10926.633210455682,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "N2O5",
          "time": 300.0,
          "expected": 175595.1598378096,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "O3",
          "time": 1800.0,
          "expected": 418221179889.9332,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "NO",
          "time": 1800.0,
          "expected": 34786092.19792038,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "NO2",
          "time": 1800.0,
          "expected": 83619108.09189194,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "OH",
          "time": 1800.0,
          "expected": 272495.26530514215,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "HO2",
          "time": 1800.0,
          "expected": 76927187.34032409,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "HCHO",
          "time": 1800.0,
          "expected": 7201338379.367484,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "HNO3",
          "time": 1800.0,
          "expected": 975953892.0956813,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "PAN",
          "time": 1800.0,
          "expected": 333135750.64270514,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "H2O2",
          "time": 1800.0,
          "expected": 19178243755.58107,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "CO",
          "time": 1800.0,
          "expected": 1115289738567.1455,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "NO3",
          "time": 1800.0,
          "expected": 7553.403630709095,
          "tolerance": {
            "rel": 1e-05
          }
        },
        {
          "variable": "N2O5",
          "time": 1800.0,
          "expected": 145492.917078408,
          "tolerance": {
            "rel": 1e-05
          }
        }
      ]
    }
  ]
}
```

</details>
