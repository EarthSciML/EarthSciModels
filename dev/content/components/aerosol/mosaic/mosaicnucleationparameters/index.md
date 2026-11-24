---
title: "MosaicNucleationParameters"
slug: "mosaicnucleationparameters"
domains: ["aerosol"]
component_types: ["model"]
subdomains: ["mosaic"]
domain: "aerosol"
subdomain: "mosaic"
component_type: "model"
esm_version: "1.2.0"
esm_path: "components/aerosol/mosaic/mosaic_nucleation_parameters.esm"
reference: "Wexler, A. S., Lurmann, F. W. and Seinfeld, J. H. (1994). Modelling urban and regional aerosols -- I. model development. Atmospheric Environment 28(3), 531-546."
description: "The fixed numbers of MOSAIC's binary H2SO4-H2O nucleation, SUBROUTINE wexler_nuc_mosaic_1box of chem/module_mosaic_newnuc.F (WRF v4.8.0), kept apart from the physics so the physics file reads as the paper does. Molecular weights and densities are the routine's own local parameters, not the WRF constants of lib/wrf_constants.esm, and MOSAIC's molecular weight of sulfate (96 g/mol) is the SO4 ion, not sulfuric acid (98 g/mol), which the routine uses separately when it converts the critical concentration."
tags: ["aerosol", "mosaic", "model", "nucleation", "wrf-chem"]
---

## Description

The fixed numbers of MOSAIC's binary H2SO4-H2O nucleation, SUBROUTINE wexler_nuc_mosaic_1box of chem/module_mosaic_newnuc.F (WRF v4.8.0), kept apart from the physics so the physics file reads as the paper does. Molecular weights and densities are the routine's own local parameters, not the WRF constants of lib/wrf_constants.esm, and MOSAIC's molecular weight of sulfate (96 g/mol) is the SO4 ion, not sulfuric acid (98 g/mol), which the routine uses separately when it converts the critical concentration.

## Reference

- Wexler, A. S., Lurmann, F. W. and Seinfeld, J. H. (1994). Modelling urban and regional aerosols -- I. model development. Atmospheric Environment 28(3), 531-546.
- Zaveri, R. A., Easter, R. C., Fast, J. D. and Peters, L. K. (2008). Model for Simulating Aerosol Interactions and Chemistry (MOSAIC). J. Geophys. Res. 113, D13204.

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `crit_c0` | `ug/m^3` | `0.16` | Leading coefficient of the critical H2SO4 concentration, `ch2so4_crit = 0.16*exp(0.1*T - 3.5*RH - 27.7)` (module_mosaic_newnuc.F:1002). |
| `crit_ct` | `1/K` | `0.1` | Temperature coefficient in that exponent. |
| `crit_crh` | `1` | `3.5` | Relative-humidity coefficient in that exponent (RH as a fraction). |
| `crit_c1` | `1` | `27.7` | Constant term in that exponent. |
| `mw_h2so4` | `g/mol` | `98.0` | Molecular weight of sulfuric acid, used to turn the critical concentration into a mixing ratio (:1006). |
| `ugm3_to_gcm3` | `g*m^3/(ug*cm^3)` | `1e-12` | Unit conversion in the same line: 1 ug/m^3 = 1e-12 g/cm^3. |
| `q_avail_min` | `mol/mol` | `4e-18` | Guard: with less available vapour than this (~1e2 molecules/cm3) the routine returns with no new particles (:1011). |
| `mw_ammsulf` | `g/mol` | `132.0` | Molecular weight of ammonium sulfate, (NH4)2SO4 (:1010 of the parameter block). |
| `mw_ammbisulf` | `g/mol` | `114.0` | Molecular weight of ammonium bisulfate, NH4HSO4. |
| `mw_sulfacid` | `g/mol` | `96.0` | Molecular weight MOSAIC uses for sulfuric acid in the particle-composition block. It is the SO4 mass, not 98. |
| `dens_ammsulf` | `g/cm^3` | `1.769` | Density of ammonium sulfate. |
| `dens_ammbisulf` | `g/cm^3` | `1.78` | Density of ammonium bisulfate. |
| `dens_sulfacid` | `g/cm^3` | `1.841` | Density of sulfuric acid. |
| `mw_so4a` | `g/mol` | `96.0` | Molecular weight of aerosol sulfate, used for the mass of the new particles (:1053). |
| `mw_nh4a` | `g/mol` | `18.0` | Molecular weight of aerosol ammonium. |
| `frac_max` | `1` | `0.9999` | The routine will not remove more than this fraction of either gas in one call (`duma` at :1046). |
| `dens_in_lo` | `g/cm^3` | `1.6` | Lower end of the band in which the caller's incoming particle density is reused instead of the composition-derived one (:1040, `abs(dens_nh4so4a - 1.8) <= 0.2`). |
| `dens_in_hi` | `g/cm^3` | `2.0` | Upper end of that band. |

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "variables": {
    "crit_c0": {
      "type": "parameter",
      "units": "ug/m^3",
      "default": 0.16,
      "description": "Leading coefficient of the critical H2SO4 concentration, `ch2so4_crit = 0.16*exp(0.1*T - 3.5*RH - 27.7)` (module_mosaic_newnuc.F:1002)."
    },
    "crit_ct": {
      "type": "parameter",
      "units": "1/K",
      "default": 0.1,
      "description": "Temperature coefficient in that exponent."
    },
    "crit_crh": {
      "type": "parameter",
      "units": "1",
      "default": 3.5,
      "description": "Relative-humidity coefficient in that exponent (RH as a fraction)."
    },
    "crit_c1": {
      "type": "parameter",
      "units": "1",
      "default": 27.7,
      "description": "Constant term in that exponent."
    },
    "mw_h2so4": {
      "type": "parameter",
      "units": "g/mol",
      "default": 98.0,
      "description": "Molecular weight of sulfuric acid, used to turn the critical concentration into a mixing ratio (:1006)."
    },
    "ugm3_to_gcm3": {
      "type": "parameter",
      "units": "g*m^3/(ug*cm^3)",
      "default": 1e-12,
      "description": "Unit conversion in the same line: 1 ug/m^3 = 1e-12 g/cm^3."
    },
    "q_avail_min": {
      "type": "parameter",
      "units": "mol/mol",
      "default": 4e-18,
      "description": "Guard: with less available vapour than this (~1e2 molecules/cm3) the routine returns with no new particles (:1011)."
    },
    "mw_ammsulf": {
      "type": "parameter",
      "units": "g/mol",
      "default": 132.0,
      "description": "Molecular weight of ammonium sulfate, (NH4)2SO4 (:1010 of the parameter block)."
    },
    "mw_ammbisulf": {
      "type": "parameter",
      "units": "g/mol",
      "default": 114.0,
      "description": "Molecular weight of ammonium bisulfate, NH4HSO4."
    },
    "mw_sulfacid": {
      "type": "parameter",
      "units": "g/mol",
      "default": 96.0,
      "description": "Molecular weight MOSAIC uses for sulfuric acid in the particle-composition block. It is the SO4 mass, not 98."
    },
    "dens_ammsulf": {
      "type": "parameter",
      "units": "g/cm^3",
      "default": 1.769,
      "description": "Density of ammonium sulfate."
    },
    "dens_ammbisulf": {
      "type": "parameter",
      "units": "g/cm^3",
      "default": 1.78,
      "description": "Density of ammonium bisulfate."
    },
    "dens_sulfacid": {
      "type": "parameter",
      "units": "g/cm^3",
      "default": 1.841,
      "description": "Density of sulfuric acid."
    },
    "mw_so4a": {
      "type": "parameter",
      "units": "g/mol",
      "default": 96.0,
      "description": "Molecular weight of aerosol sulfate, used for the mass of the new particles (:1053)."
    },
    "mw_nh4a": {
      "type": "parameter",
      "units": "g/mol",
      "default": 18.0,
      "description": "Molecular weight of aerosol ammonium."
    },
    "frac_max": {
      "type": "parameter",
      "units": "1",
      "default": 0.9999,
      "description": "The routine will not remove more than this fraction of either gas in one call (`duma` at :1046)."
    },
    "dens_in_lo": {
      "type": "parameter",
      "units": "g/cm^3",
      "default": 1.6,
      "description": "Lower end of the band in which the caller's incoming particle density is reused instead of the composition-derived one (:1040, `abs(dens_nh4so4a - 1.8) <= 0.2`)."
    },
    "dens_in_hi": {
      "type": "parameter",
      "units": "g/cm^3",
      "default": 2.0,
      "description": "Upper end of that band."
    }
  },
  "equations": []
}
```

</details>
