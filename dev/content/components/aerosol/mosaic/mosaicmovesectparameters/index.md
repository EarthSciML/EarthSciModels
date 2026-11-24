---
title: "MosaicMovesectParameters"
slug: "mosaicmovesectparameters"
domains: ["aerosol"]
component_types: ["model"]
subdomains: ["mosaic"]
domain: "aerosol"
subdomain: "mosaic"
component_type: "model"
esm_version: "1.2.0"
esm_path: "components/aerosol/mosaic/mosaic_movesect_parameters.esm"
description: "The fixed numbers MOSAIC's section-moving routine carries (chem/module_mosaic_movesect.F, subroutine move_sections, WRF v4.8.0, msectional = 20). smallmassaa is the dry mass below which a section is treated as empty and does not move; the two density bounds mark a section whose dry density is unphysical -- below 0.1 g/cm3 is the -1 MOSAIC writes for a section in its no_aerosol state -- which also does not move. The reconstruction tolerances (1.0001, 0.9999, the 1 % edge band) are part of the size-space discretization and live in the EarthSciDiscretizations rules (grids/sectional_volume_1d), not here."
tags: ["aerosol", "mosaic", "model", "section moving", "wrf-chem"]
---

## Description

The fixed numbers MOSAIC's section-moving routine carries (chem/module_mosaic_movesect.F, subroutine move_sections, WRF v4.8.0, msectional = 20). smallmassaa is the dry mass below which a section is treated as empty and does not move; the two density bounds mark a section whose dry density is unphysical -- below 0.1 g/cm3 is the -1 MOSAIC writes for a section in its no_aerosol state -- which also does not move. The reconstruction tolerances (1.0001, 0.9999, the 1 % edge band) are part of the size-space discretization and live in the EarthSciDiscretizations rules (grids/sectional_volume_1d), not here.

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `smallmassaa` | `g/mol` | `1e-20` | move_sections' smallmassaa: a section whose dry mass (g per mol of air) is at or below this neither moves nor is reconstructed (iforce_movecenter 1 and 11). |
| `dens_min` | `g/cm^3` | `0.1` | Lower bound of a usable section dry density; MOSAIC writes -1 for a section in its no_aerosol state, so a density below this marks one (move_sections_initial_conform, iforce_movecenter 11). |
| `dens_max` | `g/cm^3` | `20.0` | Upper bound of a usable section dry density (move_sections_initial_conform: 'which is unreal'). |

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "variables": {
    "smallmassaa": {
      "type": "parameter",
      "units": "g/mol",
      "default": 1e-20,
      "description": "move_sections' smallmassaa: a section whose dry mass (g per mol of air) is at or below this neither moves nor is reconstructed (iforce_movecenter 1 and 11)."
    },
    "dens_min": {
      "type": "parameter",
      "units": "g/cm^3",
      "default": 0.1,
      "description": "Lower bound of a usable section dry density; MOSAIC writes -1 for a section in its no_aerosol state, so a density below this marks one (move_sections_initial_conform, iforce_movecenter 11)."
    },
    "dens_max": {
      "type": "parameter",
      "units": "g/cm^3",
      "default": 20.0,
      "description": "Upper bound of a usable section dry density (move_sections_initial_conform: 'which is unreal')."
    }
  },
  "equations": []
}
```

</details>
