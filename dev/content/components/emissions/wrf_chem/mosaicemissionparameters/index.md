---
title: "MosaicEmissionParameters"
slug: "mosaicemissionparameters"
domains: ["emissions"]
component_types: ["model"]
subdomains: ["wrf_chem"]
domain: "emissions"
subdomain: "wrf_chem"
component_type: "model"
esm_version: "1.2.0"
esm_path: "components/emissions/wrf_chem/mosaic_emission_parameters.esm"
description: "The size apportioning of WRF-Chem's anthropogenic aerosol emissions onto MOSAIC's 8 size sections, and the component densities that turn the emitted mass into a particle number, from chem/module_mosaic_addemiss.F and chem/module_data_mosaic_asect.F (WRF v4.8.0). The fractions are the `fr8b_*` arrays of mosaic_addemiss, specific to the 8-bin structure with dlo_sect(1) = 0.039 um and dhi_sect(8) = 10 um: `sorgam_i/j/c` apportion a RADM2-variety input's MADE/SORGAM Aitken, accumulation and coarse modes (lognormals with the dgvem_i/j/c of module_data_sorgam), `mosaic_f/c` a CBM-Z-variety input's fine (< 2.5 um) and coarse (2.5-10 um) mass under the size distribution PNNL assumed for primary emissions (\"10-may-2005\" in the source). Each array sums to 1 apart from sorgam_c, whose last bin carries 0.592 and the remaining 0.000 above 10 um is dropped. The densities are module_data_mosaic_asect's `dens_<x>_aer` parameters."
tags: ["emissions", "wrf_chem", "model", "wrf-chem", "mosaic", "parameters"]
---

## Description

The size apportioning of WRF-Chem's anthropogenic aerosol emissions onto MOSAIC's 8 size sections, and the component densities that turn the emitted mass into a particle number, from chem/module_mosaic_addemiss.F and chem/module_data_mosaic_asect.F (WRF v4.8.0). The fractions are the `fr8b_*` arrays of mosaic_addemiss, specific to the 8-bin structure with dlo_sect(1) = 0.039 um and dhi_sect(8) = 10 um: `sorgam_i/j/c` apportion a RADM2-variety input's MADE/SORGAM Aitken, accumulation and coarse modes (lognormals with the dgvem_i/j/c of module_data_sorgam), `mosaic_f/c` a CBM-Z-variety input's fine (< 2.5 um) and coarse (2.5-10 um) mass under the size distribution PNNL assumed for primary emissions ("10-may-2005" in the source). Each array sums to 1 apart from sorgam_c, whose last bin carries 0.592 and the remaining 0.000 above 10 um is dropped. The densities are module_data_mosaic_asect's `dens_<x>_aer` parameters.

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `fr_sorgam_i` | `1` | `[0.965, 0.035, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]` | fr8b_aem_sorgam_i: Aitken-mode (i) fraction in each section. |
| `fr_sorgam_j` | `1` | `[0.026, 0.147, 0.35, 0.332, 0.125, 0.019, 0.001, 0.0]` | fr8b_aem_sorgam_j: accumulation-mode (j) fraction in each section. |
| `fr_sorgam_c` | `1` | `[0.0, 0.0, 0.0, 0.002, 0.021, 0.11, 0.275, 0.592]` | fr8b_aem_sorgam_c: coarse-mode fraction in each section (applied to E_PM_10 only). |
| `fr_mosaic_f` | `1` | `[0.06, 0.045, 0.245, 0.4, 0.1, 0.15, 0.0, 0.0]` | fr8b_aem_mosaic_f: fine (< 2.5 um) fraction in each section. |
| `fr_mosaic_c` | `1` | `[0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.3, 0.7]` | fr8b_aem_mosaic_c: coarse (2.5-10 um) fraction in each section. |
| `dens_so4` | `g/cm^3` | `1.8` | dens_so4_aer. |
| `dens_no3` | `g/cm^3` | `1.8` | dens_no3_aer. |
| `dens_oin` | `g/cm^3` | `2.6` | dens_oin_aer (other inorganic). |
| `dens_oc` | `g/cm^3` | `1.0` | dens_oc_aer. |
| `dens_bc` | `g/cm^3` | `1.7` | dens_bc_aer. |

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "variables": {
    "fr_sorgam_i": {
      "type": "parameter",
      "units": "1",
      "shape": [
        "bin"
      ],
      "default": [
        0.965,
        0.035,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0
      ],
      "description": "fr8b_aem_sorgam_i: Aitken-mode (i) fraction in each section."
    },
    "fr_sorgam_j": {
      "type": "parameter",
      "units": "1",
      "shape": [
        "bin"
      ],
      "default": [
        0.026,
        0.147,
        0.35,
        0.332,
        0.125,
        0.019,
        0.001,
        0.0
      ],
      "description": "fr8b_aem_sorgam_j: accumulation-mode (j) fraction in each section."
    },
    "fr_sorgam_c": {
      "type": "parameter",
      "units": "1",
      "shape": [
        "bin"
      ],
      "default": [
        0.0,
        0.0,
        0.0,
        0.002,
        0.021,
        0.11,
        0.275,
        0.592
      ],
      "description": "fr8b_aem_sorgam_c: coarse-mode fraction in each section (applied to E_PM_10 only)."
    },
    "fr_mosaic_f": {
      "type": "parameter",
      "units": "1",
      "shape": [
        "bin"
      ],
      "default": [
        0.06,
        0.045,
        0.245,
        0.4,
        0.1,
        0.15,
        0.0,
        0.0
      ],
      "description": "fr8b_aem_mosaic_f: fine (< 2.5 um) fraction in each section."
    },
    "fr_mosaic_c": {
      "type": "parameter",
      "units": "1",
      "shape": [
        "bin"
      ],
      "default": [
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.0,
        0.3,
        0.7
      ],
      "description": "fr8b_aem_mosaic_c: coarse (2.5-10 um) fraction in each section."
    },
    "dens_so4": {
      "type": "parameter",
      "units": "g/cm^3",
      "default": 1.8,
      "description": "dens_so4_aer."
    },
    "dens_no3": {
      "type": "parameter",
      "units": "g/cm^3",
      "default": 1.8,
      "description": "dens_no3_aer."
    },
    "dens_oin": {
      "type": "parameter",
      "units": "g/cm^3",
      "default": 2.6,
      "description": "dens_oin_aer (other inorganic)."
    },
    "dens_oc": {
      "type": "parameter",
      "units": "g/cm^3",
      "default": 1.0,
      "description": "dens_oc_aer."
    },
    "dens_bc": {
      "type": "parameter",
      "units": "g/cm^3",
      "default": 1.7,
      "description": "dens_bc_aer."
    }
  },
  "equations": []
}
```

</details>
