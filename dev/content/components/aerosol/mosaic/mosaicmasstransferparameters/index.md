---
title: "MosaicMassTransferParameters"
slug: "mosaicmasstransferparameters"
domains: ["aerosol"]
component_types: ["model"]
subdomains: ["mosaic"]
domain: "aerosol"
subdomain: "mosaic"
component_type: "model"
esm_version: "1.1.0"
esm_path: "components/aerosol/mosaic/mosaic_mass_transfer_parameters.esm"
reference: "Fuchs, N. A. and Sutugin, A. G. (1971). High-dispersed aerosols. In Topics in Current Aerosol Research, Pergamon (the transition-regime correction this kernel uses)."
description: "The per-gas and fixed numbers of MOSAIC's gas-particle mass-transfer coefficient: SUBROUTINE aerosolmtc and the functions gas_diffusivity, mean_molecular_speed and fuchs_sutugin of chem/module_mosaic_therm.F (WRF v4.8.0). The molecular weights, Fuller molar volumes and accommodation coefficients are the routine's own table; MOSAIC gives every condensing gas the same accommodation coefficient, 0.1."
tags: ["aerosol", "mosaic", "model", "condensation", "wrf-chem"]
---

## Description

The per-gas and fixed numbers of MOSAIC's gas-particle mass-transfer coefficient: SUBROUTINE aerosolmtc and the functions gas_diffusivity, mean_molecular_speed and fuchs_sutugin of chem/module_mosaic_therm.F (WRF v4.8.0). The molecular weights, Fuller molar volumes and accommodation coefficients are the routine's own table; MOSAIC gives every condensing gas the same accommodation coefficient, 0.1.

## Reference

- Fuchs, N. A. and Sutugin, A. G. (1971). High-dispersed aerosols. In Topics in Current Aerosol Research, Pergamon (the transition-regime correction this kernel uses).
- Zaveri, R. A., Easter, R. C., Fast, J. D. and Peters, L. K. (2008). Model for Simulating Aerosol Interactions and Chemistry (MOSAIC). J. Geophys. Res. 113, D13204.

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `speed_c0` | `cm/s*(g/mol/K)^(1/2)` | `14550.0` | Coefficient of the mean molecular speed, 1.455e4*sqrt(T/mw) (function mean_molecular_speed). |
| `dg_c0` | `cm^2/s*atm*(g/mol)^(1/2)` | `0.0010000000474974513` | Leading coefficient of the Fuller gas-diffusivity fit (function gas_diffusivity). The fit is empirical in K, g/mol, cm^3/mol and atm; temperature and molar volume enter it divided by t_unit and vm_unit (both exactly 1, so values are unchanged), which leaves this coefficient carrying the units that make dg come out in cm^2/s. Written 0.001 in default REAL, so held as binary32 0.0010000000474974513 (re-pinned 2026-11-12 against the real64 ASTEM tape; the decimal value was within the real32 tests' 5e-7 but not 1e-9). |
| `dg_texp` | `1` | `1.75` | Temperature exponent of that fit. |
| `dg_mw_add` | `mol/g` | `0.03500000014901161` | The 0.035 added to 1/mw under the square root; it stands for the reciprocal molecular weight of air. Written 0.035 in default REAL, so held as binary32 0.03500000014901161 (re-pinned 2026-11-12 against the real64 ASTEM tape; the decimal value was within the real32 tests' 5e-7 but not 1e-9). |
| `dg_vm_exp` | `1` | `0.33333298563957214` | Exponent applied to the molar volume. It is the routine's truncated 1/3 and reproducing it matters at single precision. Written 0.333333 in default REAL, so held as binary32 0.33333298563957214 (re-pinned 2026-11-12 against the real64 ASTEM tape; the decimal value was within the real32 tests' 5e-7 but not 1e-9). |
| `dg_vm_add` | `1` | `2.718899965286255` | The air term added to (v_molar/vm_unit)^dg_vm_exp before squaring; dimensionless because the molar volume is divided by vm_unit before the power. Written 2.7189 in default REAL, so held as binary32 2.718899965286255 (re-pinned 2026-11-12 against the real64 ASTEM tape; the decimal value was within the real32 tests' 5e-7 but not 1e-9). |
| `t_unit` | `K` | `1.0` | Unit temperature: the Fuller fit raises T in kelvin to dg_texp, so T is divided by this before the power (dimensional bookkeeping only; dividing by exactly 1 changes no value). |
| `vm_unit` | `cm^3/mol` | `1.0` | Unit molar volume: the Fuller fit raises the molar volume in cm^3/mol to the truncated 1/3 dg_vm_exp, so v_molar is divided by this before the power (dimensional bookkeeping only; dividing by exactly 1 changes no value). |
| `freepath_c0` | `1` | `3.0` | freepath = 3*dg/speed. |
| `two_pi` | `1` | `6.283185005187988` | 2*pi as aerosolmtc spells it in `cdum = 6.283185*dp_avg*num_a`. Written 6.283185 in default REAL, so held as binary32 6.283185005187988 (re-pinned 2026-11-12 against the real64 ASTEM tape; the decimal value was within the real32 tests' 5e-7 but not 1e-9). |
| `fs_c0` | `1` | `0.75` | Numerator and denominator coefficient of the Fuchs-Sutugin correction, 0.75*a*(1+Kn) over Kn^2 + Kn + 0.283*Kn*a + 0.75*a. |
| `fs_c1` | `1` | `0.28299999237060547` | The 0.283 in that denominator. Written 0.283 in default REAL, so held as binary32 0.28299999237060547 (re-pinned 2026-11-12 against the real64 ASTEM tape; the decimal value was within the real32 tests' 5e-7 but not 1e-9). |
| `mw_h2so4` | `g/mol` | `98.0` | Molecular weight of H2SO4 in the mass-transfer table. |
| `vm_h2so4` | `cm^3/mol` | `42.880001068115234` | Fuller molar volume of H2SO4. Written 42.88 in default REAL, so held as binary32 42.880001068115234 (re-pinned 2026-11-12 against the real64 ASTEM tape; the decimal value was within the real32 tests' 5e-7 but not 1e-9). |
| `mw_msa` | `g/mol` | `96.0` | Molecular weight of MSA. |
| `vm_msa` | `cm^3/mol` | `58.0` | Fuller molar volume of MSA. |
| `mw_hno3` | `g/mol` | `63.0` | Molecular weight of HNO3. |
| `vm_hno3` | `cm^3/mol` | `24.110000610351562` | Fuller molar volume of HNO3. Written 24.11 in default REAL, so held as binary32 24.110000610351562 (re-pinned 2026-11-12 against the real64 ASTEM tape; the decimal value was within the real32 tests' 5e-7 but not 1e-9). |
| `mw_hcl` | `g/mol` | `36.5` | Molecular weight of HCl. |
| `vm_hcl` | `cm^3/mol` | `21.479999542236328` | Fuller molar volume of HCl. Written 21.48 in default REAL, so held as binary32 21.479999542236328 (re-pinned 2026-11-12 against the real64 ASTEM tape; the decimal value was within the real32 tests' 5e-7 but not 1e-9). |
| `mw_nh3` | `g/mol` | `17.0` | Molecular weight of NH3. |
| `vm_nh3` | `cm^3/mol` | `14.899999618530273` | Fuller molar volume of NH3. Written 14.9 in default REAL, so held as binary32 14.899999618530273 (re-pinned 2026-11-12 against the real64 ASTEM tape; the decimal value was within the real32 tests' 5e-7 but not 1e-9). |
| `accom` | `1` | `0.10000000149011612` | Accommodation coefficient. MOSAIC gives every condensing gas the same value. Written 0.1 in default REAL, so held as binary32 0.10000000149011612 (re-pinned 2026-11-12 against the real64 ASTEM tape; the decimal value was within the real32 tests' 5e-7 but not 1e-9). |

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "variables": {
    "speed_c0": {
      "type": "parameter",
      "units": "cm/s*(g/mol/K)^(1/2)",
      "default": 14550.0,
      "description": "Coefficient of the mean molecular speed, 1.455e4*sqrt(T/mw) (function mean_molecular_speed)."
    },
    "dg_c0": {
      "type": "parameter",
      "units": "cm^2/s*atm*(g/mol)^(1/2)",
      "default": 0.0010000000474974513,
      "description": "Leading coefficient of the Fuller gas-diffusivity fit (function gas_diffusivity). The fit is empirical in K, g/mol, cm^3/mol and atm; temperature and molar volume enter it divided by t_unit and vm_unit (both exactly 1, so values are unchanged), which leaves this coefficient carrying the units that make dg come out in cm^2/s. Written 0.001 in default REAL, so held as binary32 0.0010000000474974513 (re-pinned 2026-11-12 against the real64 ASTEM tape; the decimal value was within the real32 tests' 5e-7 but not 1e-9)."
    },
    "dg_texp": {
      "type": "parameter",
      "units": "1",
      "default": 1.75,
      "description": "Temperature exponent of that fit."
    },
    "dg_mw_add": {
      "type": "parameter",
      "units": "mol/g",
      "default": 0.03500000014901161,
      "description": "The 0.035 added to 1/mw under the square root; it stands for the reciprocal molecular weight of air. Written 0.035 in default REAL, so held as binary32 0.03500000014901161 (re-pinned 2026-11-12 against the real64 ASTEM tape; the decimal value was within the real32 tests' 5e-7 but not 1e-9)."
    },
    "dg_vm_exp": {
      "type": "parameter",
      "units": "1",
      "default": 0.33333298563957214,
      "description": "Exponent applied to the molar volume. It is the routine's truncated 1/3 and reproducing it matters at single precision. Written 0.333333 in default REAL, so held as binary32 0.33333298563957214 (re-pinned 2026-11-12 against the real64 ASTEM tape; the decimal value was within the real32 tests' 5e-7 but not 1e-9)."
    },
    "dg_vm_add": {
      "type": "parameter",
      "units": "1",
      "default": 2.718899965286255,
      "description": "The air term added to (v_molar/vm_unit)^dg_vm_exp before squaring; dimensionless because the molar volume is divided by vm_unit before the power. Written 2.7189 in default REAL, so held as binary32 2.718899965286255 (re-pinned 2026-11-12 against the real64 ASTEM tape; the decimal value was within the real32 tests' 5e-7 but not 1e-9)."
    },
    "t_unit": {
      "type": "parameter",
      "units": "K",
      "default": 1.0,
      "description": "Unit temperature: the Fuller fit raises T in kelvin to dg_texp, so T is divided by this before the power (dimensional bookkeeping only; dividing by exactly 1 changes no value)."
    },
    "vm_unit": {
      "type": "parameter",
      "units": "cm^3/mol",
      "default": 1.0,
      "description": "Unit molar volume: the Fuller fit raises the molar volume in cm^3/mol to the truncated 1/3 dg_vm_exp, so v_molar is divided by this before the power (dimensional bookkeeping only; dividing by exactly 1 changes no value)."
    },
    "freepath_c0": {
      "type": "parameter",
      "units": "1",
      "default": 3.0,
      "description": "freepath = 3*dg/speed."
    },
    "two_pi": {
      "type": "parameter",
      "units": "1",
      "default": 6.283185005187988,
      "description": "2*pi as aerosolmtc spells it in `cdum = 6.283185*dp_avg*num_a`. Written 6.283185 in default REAL, so held as binary32 6.283185005187988 (re-pinned 2026-11-12 against the real64 ASTEM tape; the decimal value was within the real32 tests' 5e-7 but not 1e-9)."
    },
    "fs_c0": {
      "type": "parameter",
      "units": "1",
      "default": 0.75,
      "description": "Numerator and denominator coefficient of the Fuchs-Sutugin correction, 0.75*a*(1+Kn) over Kn^2 + Kn + 0.283*Kn*a + 0.75*a."
    },
    "fs_c1": {
      "type": "parameter",
      "units": "1",
      "default": 0.28299999237060547,
      "description": "The 0.283 in that denominator. Written 0.283 in default REAL, so held as binary32 0.28299999237060547 (re-pinned 2026-11-12 against the real64 ASTEM tape; the decimal value was within the real32 tests' 5e-7 but not 1e-9)."
    },
    "mw_h2so4": {
      "type": "parameter",
      "units": "g/mol",
      "default": 98.0,
      "description": "Molecular weight of H2SO4 in the mass-transfer table."
    },
    "vm_h2so4": {
      "type": "parameter",
      "units": "cm^3/mol",
      "default": 42.880001068115234,
      "description": "Fuller molar volume of H2SO4. Written 42.88 in default REAL, so held as binary32 42.880001068115234 (re-pinned 2026-11-12 against the real64 ASTEM tape; the decimal value was within the real32 tests' 5e-7 but not 1e-9)."
    },
    "mw_msa": {
      "type": "parameter",
      "units": "g/mol",
      "default": 96.0,
      "description": "Molecular weight of MSA."
    },
    "vm_msa": {
      "type": "parameter",
      "units": "cm^3/mol",
      "default": 58.0,
      "description": "Fuller molar volume of MSA."
    },
    "mw_hno3": {
      "type": "parameter",
      "units": "g/mol",
      "default": 63.0,
      "description": "Molecular weight of HNO3."
    },
    "vm_hno3": {
      "type": "parameter",
      "units": "cm^3/mol",
      "default": 24.110000610351562,
      "description": "Fuller molar volume of HNO3. Written 24.11 in default REAL, so held as binary32 24.110000610351562 (re-pinned 2026-11-12 against the real64 ASTEM tape; the decimal value was within the real32 tests' 5e-7 but not 1e-9)."
    },
    "mw_hcl": {
      "type": "parameter",
      "units": "g/mol",
      "default": 36.5,
      "description": "Molecular weight of HCl."
    },
    "vm_hcl": {
      "type": "parameter",
      "units": "cm^3/mol",
      "default": 21.479999542236328,
      "description": "Fuller molar volume of HCl. Written 21.48 in default REAL, so held as binary32 21.479999542236328 (re-pinned 2026-11-12 against the real64 ASTEM tape; the decimal value was within the real32 tests' 5e-7 but not 1e-9)."
    },
    "mw_nh3": {
      "type": "parameter",
      "units": "g/mol",
      "default": 17.0,
      "description": "Molecular weight of NH3."
    },
    "vm_nh3": {
      "type": "parameter",
      "units": "cm^3/mol",
      "default": 14.899999618530273,
      "description": "Fuller molar volume of NH3. Written 14.9 in default REAL, so held as binary32 14.899999618530273 (re-pinned 2026-11-12 against the real64 ASTEM tape; the decimal value was within the real32 tests' 5e-7 but not 1e-9)."
    },
    "accom": {
      "type": "parameter",
      "units": "1",
      "default": 0.10000000149011612,
      "description": "Accommodation coefficient. MOSAIC gives every condensing gas the same value. Written 0.1 in default REAL, so held as binary32 0.10000000149011612 (re-pinned 2026-11-12 against the real64 ASTEM tape; the decimal value was within the real32 tests' 5e-7 but not 1e-9)."
    }
  },
  "equations": []
}
```

</details>
