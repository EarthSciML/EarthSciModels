---
title: "MosaicHostParameters"
slug: "mosaichostparameters"
domains: ["aerosol"]
component_types: ["model"]
subdomains: ["mosaic"]
domain: "aerosol"
subdomain: "mosaic"
component_type: "model"
esm_version: "1.2.0"
esm_path: "components/aerosol/mosaic/mosaic_host_parameters.esm"
description: "Constants of MOSAIC's mapping between the WRF-Chem host arrays and its own column state (mapaer_tofrom_host, chem/module_mosaic_driver.F, WRF v4.8.0) and of the saturation-vapour-pressure table it forms relative humidity with (module_mosaic_csuesat.F)."
tags: ["aerosol", "mosaic", "model", "wrf-chem", "parameters"]
---

## Description

Constants of MOSAIC's mapping between the WRF-Chem host arrays and its own column state (mapaer_tofrom_host, chem/module_mosaic_driver.F, WRF v4.8.0) and of the saturation-vapour-pressure table it forms relative humidity with (module_mosaic_csuesat.F).

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `factdens` | `kg*cm^3/(m^3*mol)` | `28966.0` | factdens = 28.966e3: molar air density (mol/cm^3) -> mass density (kg/m^3), i.e. MOSAIC's molar mass of air in kg/mol times 1e6 cm^3/m^3 (module_mosaic_driver.F mapaer_tofrom_host :806). |
| `factpres` | `Pa*cm^2/dyn` | `0.1` | factpres = 0.1: dyn/cm^2 -> Pa (:807). |
| `dyncm2_per_atm_therm` | `dyn/(cm^2*atm)` | `1032000.0` | The 1.032d6 module_mosaic_therm converts ptotclm to atmospheres with (:254) for ASTEM's p_atm, not the standard 1.01325e6 its coagulation uses (FORTRAN_BUGS N129). |
| `eps` | `1` | `0.622` | eps = 0.622: water vapour mixing ratio, mol/mol -> kg/kg (factmoist, :808), and 1 - eps in the saturation mixing ratio. |
| `factgas` | `ppmv` | `1000000.0` | factgas = 1.0e6: gas mole fraction -> ppmv (:809). |
| `cm3_per_m3` | `cm^3/m^3` | `1000000.0` | The 1.e6 of cair_mol_m3 = cairclm*1.e6 (module_mosaic_therm.F map_mosaic_species :606): molar air density mol/cm^3 -> mol/m^3. A default-REAL literal, exact in binary32. |
| `nmol_per_mol` | `nmol/mol` | `1000000000.0` | The 1.d9 of conv1a = cair_mol_m3*1.d9 (map_mosaic_species :611): with cm3_per_m3, the factor that takes rsub's mole fractions (mol/mol(air)) to MOSAIC's box concentrations (nmol/m^3), and back (conv1b = 1/conv1a). |
| `factaernum` | `mol/kg` | `34.52323413657391` | factaernum = 1000/28.966: moles of air per kg of air (:815); number per kg <-> number per mole of air. |
| `ug_per_g` | `ug/g` | `1000000.0` | The 1.0e6 of dum = factaernum*1.0e6 (:817): g -> ug in the aerosol mass factors factaer<x> = dum*mw_<x>_aer. |
| `mw_water_aer` | `g/mol` | `18.016` | mw_water_aer (module_data_mosaic_asect.F:467), the factor of factaerwater and factaerhysw. |
| `min_temp` | `K` | `233.0` | aboxtest_min_temp (module_data_mosaic_other.F:200): MOSAIC's temperature is held at or above 233 K. The 'box testing' block that would set it to 0 is compiled out of WRF. |
| `min_relhum` | `1` | `0.05` | aboxtest_min_relhum (:201). |
| `max_relhum` | `1` | `0.98` | aboxtest_max_relhum (:202). |
| `relhum_cap` | `1` | `0.99` | The first clamp of the computed relative humidity, max(0, min(0.99, rh)) (mapaer_tofrom_host). |
| `rsat_floor` | `1` | `1e-20` | Floor on the saturation mixing ratio in rh = h2o / max(rsat, 1e-20). |
| `es_tmin` | `K` | `163.0` | tmin of module_mosaic_csuesat: the saturation-vapour-pressure table's node k is at tmin + k kelvin. |
| `es_nbins` | `1` | `149` | nebins: the table interval index is held to [1, 149] (nodes 164 to 313 K). |
| `one_K` | `K` | `1.0` | The table's node spacing, one kelvin. |
| `es_a0` | `dyn/cm^2` | `79535724200.0` | init_csuesat water coefficient a0 (dyn/cm^2 before the final 1e3) (module_mosaic_csuesat.F). |
| `es_ax` | `1` | `-18.1972839` | init_csuesat water coefficient ax (module_mosaic_csuesat.F). |
| `es_a2` | `1` | `5.02808` | init_csuesat water coefficient a2 (module_mosaic_csuesat.F). |
| `es_a3` | `1` | `-70242.1852` | init_csuesat water coefficient a3 (module_mosaic_csuesat.F). |
| `es_a4` | `1` | `-26.1205253` | init_csuesat water coefficient a4 (module_mosaic_csuesat.F). |
| `es_a5` | `1` | `58.0691913` | init_csuesat water coefficient a5 (module_mosaic_csuesat.F). |
| `es_a6` | `1` | `-8.03945282` | init_csuesat water coefficient a6 (module_mosaic_csuesat.F). |
| `es_tf` | `K` | `373.16` | init_csuesat's tf for the water table. |
| `es_scale` | `1` | `1000.0` | The trailing *1.e3 of estbar(jd) = a0 exp(arg) 1.e3. |

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "variables": {
    "factdens": {
      "type": "parameter",
      "units": "kg*cm^3/(m^3*mol)",
      "default": 28966.0,
      "description": "factdens = 28.966e3: molar air density (mol/cm^3) -> mass density (kg/m^3), i.e. MOSAIC's molar mass of air in kg/mol times 1e6 cm^3/m^3 (module_mosaic_driver.F mapaer_tofrom_host :806)."
    },
    "factpres": {
      "type": "parameter",
      "units": "Pa*cm^2/dyn",
      "default": 0.1,
      "description": "factpres = 0.1: dyn/cm^2 -> Pa (:807)."
    },
    "dyncm2_per_atm_therm": {
      "type": "parameter",
      "units": "dyn/(cm^2*atm)",
      "default": 1032000.0,
      "description": "The 1.032d6 module_mosaic_therm converts ptotclm to atmospheres with (:254) for ASTEM's p_atm, not the standard 1.01325e6 its coagulation uses (FORTRAN_BUGS N129)."
    },
    "eps": {
      "type": "parameter",
      "units": "1",
      "default": 0.622,
      "description": "eps = 0.622: water vapour mixing ratio, mol/mol -> kg/kg (factmoist, :808), and 1 - eps in the saturation mixing ratio."
    },
    "factgas": {
      "type": "parameter",
      "units": "ppmv",
      "default": 1000000.0,
      "description": "factgas = 1.0e6: gas mole fraction -> ppmv (:809)."
    },
    "cm3_per_m3": {
      "type": "parameter",
      "units": "cm^3/m^3",
      "default": 1000000.0,
      "description": "The 1.e6 of cair_mol_m3 = cairclm*1.e6 (module_mosaic_therm.F map_mosaic_species :606): molar air density mol/cm^3 -> mol/m^3. A default-REAL literal, exact in binary32."
    },
    "nmol_per_mol": {
      "type": "parameter",
      "units": "nmol/mol",
      "default": 1000000000.0,
      "description": "The 1.d9 of conv1a = cair_mol_m3*1.d9 (map_mosaic_species :611): with cm3_per_m3, the factor that takes rsub's mole fractions (mol/mol(air)) to MOSAIC's box concentrations (nmol/m^3), and back (conv1b = 1/conv1a)."
    },
    "factaernum": {
      "type": "parameter",
      "units": "mol/kg",
      "default": 34.52323413657391,
      "description": "factaernum = 1000/28.966: moles of air per kg of air (:815); number per kg <-> number per mole of air."
    },
    "ug_per_g": {
      "type": "parameter",
      "units": "ug/g",
      "default": 1000000.0,
      "description": "The 1.0e6 of dum = factaernum*1.0e6 (:817): g -> ug in the aerosol mass factors factaer<x> = dum*mw_<x>_aer."
    },
    "mw_water_aer": {
      "type": "parameter",
      "units": "g/mol",
      "default": 18.016,
      "description": "mw_water_aer (module_data_mosaic_asect.F:467), the factor of factaerwater and factaerhysw."
    },
    "min_temp": {
      "type": "parameter",
      "units": "K",
      "default": 233.0,
      "description": "aboxtest_min_temp (module_data_mosaic_other.F:200): MOSAIC's temperature is held at or above 233 K. The 'box testing' block that would set it to 0 is compiled out of WRF."
    },
    "min_relhum": {
      "type": "parameter",
      "units": "1",
      "default": 0.05,
      "description": "aboxtest_min_relhum (:201)."
    },
    "max_relhum": {
      "type": "parameter",
      "units": "1",
      "default": 0.98,
      "description": "aboxtest_max_relhum (:202)."
    },
    "relhum_cap": {
      "type": "parameter",
      "units": "1",
      "default": 0.99,
      "description": "The first clamp of the computed relative humidity, max(0, min(0.99, rh)) (mapaer_tofrom_host)."
    },
    "rsat_floor": {
      "type": "parameter",
      "units": "1",
      "default": 1e-20,
      "description": "Floor on the saturation mixing ratio in rh = h2o / max(rsat, 1e-20)."
    },
    "es_tmin": {
      "type": "parameter",
      "units": "K",
      "default": 163.0,
      "description": "tmin of module_mosaic_csuesat: the saturation-vapour-pressure table's node k is at tmin + k kelvin."
    },
    "es_nbins": {
      "type": "parameter",
      "units": "1",
      "default": 149,
      "description": "nebins: the table interval index is held to [1, 149] (nodes 164 to 313 K)."
    },
    "one_K": {
      "type": "parameter",
      "units": "K",
      "default": 1.0,
      "description": "The table's node spacing, one kelvin."
    },
    "es_a0": {
      "type": "parameter",
      "units": "dyn/cm^2",
      "default": 79535724200.0,
      "description": "init_csuesat water coefficient a0 (dyn/cm^2 before the final 1e3) (module_mosaic_csuesat.F)."
    },
    "es_ax": {
      "type": "parameter",
      "units": "1",
      "default": -18.1972839,
      "description": "init_csuesat water coefficient ax (module_mosaic_csuesat.F)."
    },
    "es_a2": {
      "type": "parameter",
      "units": "1",
      "default": 5.02808,
      "description": "init_csuesat water coefficient a2 (module_mosaic_csuesat.F)."
    },
    "es_a3": {
      "type": "parameter",
      "units": "1",
      "default": -70242.1852,
      "description": "init_csuesat water coefficient a3 (module_mosaic_csuesat.F)."
    },
    "es_a4": {
      "type": "parameter",
      "units": "1",
      "default": -26.1205253,
      "description": "init_csuesat water coefficient a4 (module_mosaic_csuesat.F)."
    },
    "es_a5": {
      "type": "parameter",
      "units": "1",
      "default": 58.0691913,
      "description": "init_csuesat water coefficient a5 (module_mosaic_csuesat.F)."
    },
    "es_a6": {
      "type": "parameter",
      "units": "1",
      "default": -8.03945282,
      "description": "init_csuesat water coefficient a6 (module_mosaic_csuesat.F)."
    },
    "es_tf": {
      "type": "parameter",
      "units": "K",
      "default": 373.16,
      "description": "init_csuesat's tf for the water table."
    },
    "es_scale": {
      "type": "parameter",
      "units": "1",
      "default": 1000.0,
      "description": "The trailing *1.e3 of estbar(jd) = a0 exp(arg) 1.e3."
    }
  },
  "equations": []
}
```

</details>
