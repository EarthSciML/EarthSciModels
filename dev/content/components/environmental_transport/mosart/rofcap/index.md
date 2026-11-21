---
title: "RofCap"
slug: "rofcap"
domains: ["environmental_transport"]
component_types: ["model"]
subdomains: ["mosart"]
domain: "environmental_transport"
subdomain: "mosart"
component_type: "model"
esm_version: "2.0.0"
esm_path: "components/environmental_transport/mosart/mosart_coupling.esm"
reference: "10.1175/JHM-D-12-015.1"
description: "MOSART cap-boundary component (stage 2 of the EqESM project): the med<->rof field conversions of rof_comp_nuopc/rof_import_export.F90 (mosart1.1.13) as algebraic equations, per the stage1/boundaries.md 1.5 boundary table. Imports (med -> rof): Flrl_rofsur, Flrl_rofsub, Flrl_rofgwl, Flrl_rofi, Flrl_irrig (lnd runoff, CMEPS kg/m^2/s which for water equals mm/s), and Fgrg_rofl, Fgrg_rofi (glc runoff, active when rof_from_glc). Exports (rof -> med): Forr_rofl, Forr_rofi, Forr_rofl_glc, Forr_rofi_glc, Flrr_flood, Flrr_volr, Flrr_volrmch, Sr_tdepth, Sr_tdepth_max. Import conversion, exactly state_getimport (rof_import_export.F90:589-595): q [m3/s] = field [mm/s] * med2mod_areacor * area [m2] * 0.001 [m/mm], where med2mod_areacor is the mesh-area correction factor (F90:209-210, ~1 for the rof mesh on the model grid) and 0.001 is spelled as the parameter mm_to_m [m/mm] for dimensional honesty. Export conversion, exactly state_setexport (F90:636-643): field [mm/s] = q [m3/s] * mod2med_areacor / (area [m2] * 0.001 [m/mm]); Flrr_flood carries the sign flip flood = -ctl%flood/(area*0.001) (F90:395, the land->rof positive convention); Flrr_volr = volr/area and Flrr_volrmch = wr/area are depths [m] with no mm scaling (F90:396-397); Sr_tdepth/Sr_tdepth_max are stream depths exported only when flds_r2l_stream_channel_depths (F90:398-402, tdepth_max = max(twidth0,0)*(rdepth/rwidth)). The direct-transfer, irrigation, flood and subcycling orchestration of mosart_run lives in the assembly mosart_routing.esm (its Control model) because the qgwl threshold option and the flood threshold need the channel storage wr; this file keeps the pure unit conversions, per the boundaries.md 2.6 mapping (cap boundary row). The tests block pins the med<->rof import/export unit conversions pointwise (instantaneous tests, time_span {0,0}) from the step-1 boundary values of cell 100312 (EqESM instrumented-CESM dumps stage1/dumps/mosart/mosart_run_imports.csv, mosart_run_exports.csv, and the area/areacor columns of mosart_run_imports_wide.csv); see README.md (Testing). Reference: stage1/cesm/components/mosart/src/cpl/nuopc/rof_import_export.F90 (mosart1.1.13)."
tags: ["environmental_transport", "mosart", "model", "river-routing", "coupler", "cmesp", "unit-conversion", "cesm"]
---

## Description

MOSART cap-boundary component (stage 2 of the EqESM project): the med<->rof field conversions of rof_comp_nuopc/rof_import_export.F90 (mosart1.1.13) as algebraic equations, per the stage1/boundaries.md 1.5 boundary table. Imports (med -> rof): Flrl_rofsur, Flrl_rofsub, Flrl_rofgwl, Flrl_rofi, Flrl_irrig (lnd runoff, CMEPS kg/m^2/s which for water equals mm/s), and Fgrg_rofl, Fgrg_rofi (glc runoff, active when rof_from_glc). Exports (rof -> med): Forr_rofl, Forr_rofi, Forr_rofl_glc, Forr_rofi_glc, Flrr_flood, Flrr_volr, Flrr_volrmch, Sr_tdepth, Sr_tdepth_max. Import conversion, exactly state_getimport (rof_import_export.F90:589-595): q [m3/s] = field [mm/s] * med2mod_areacor * area [m2] * 0.001 [m/mm], where med2mod_areacor is the mesh-area correction factor (F90:209-210, ~1 for the rof mesh on the model grid) and 0.001 is spelled as the parameter mm_to_m [m/mm] for dimensional honesty. Export conversion, exactly state_setexport (F90:636-643): field [mm/s] = q [m3/s] * mod2med_areacor / (area [m2] * 0.001 [m/mm]); Flrr_flood carries the sign flip flood = -ctl%flood/(area*0.001) (F90:395, the land->rof positive convention); Flrr_volr = volr/area and Flrr_volrmch = wr/area are depths [m] with no mm scaling (F90:396-397); Sr_tdepth/Sr_tdepth_max are stream depths exported only when flds_r2l_stream_channel_depths (F90:398-402, tdepth_max = max(twidth0,0)*(rdepth/rwidth)). The direct-transfer, irrigation, flood and subcycling orchestration of mosart_run lives in the assembly mosart_routing.esm (its Control model) because the qgwl threshold option and the flood threshold need the channel storage wr; this file keeps the pure unit conversions, per the boundaries.md 2.6 mapping (cap boundary row). The tests block pins the med<->rof import/export unit conversions pointwise (instantaneous tests, time_span {0,0}) from the step-1 boundary values of cell 100312 (EqESM instrumented-CESM dumps stage1/dumps/mosart/mosart_run_imports.csv, mosart_run_exports.csv, and the area/areacor columns of mosart_run_imports_wide.csv); see README.md (Testing). Reference: stage1/cesm/components/mosart/src/cpl/nuopc/rof_import_export.F90 (mosart1.1.13).

## Reference

- Li, H., Wigmosta, M. S., Wu, H., Huang, M., Ke, Y., Coleman, A. M., and Leung, L. R. (2013). A physically based runoff routing model for land surface and earth system models. Journal of Hydrometeorology, 14(3), 808-828. The MOSART (Model for Scale Adaptive River Transport) routing scheme these components transcribe.
- CESM (Community Earth System Model), ESCOMP/CESM, cesm3.0-alphabranch: MOSART river-routing source (mosart1.1.13) - mosart_physics.F90, mosart_driver.F90, mosart_tstatusflux_type.F90, mosart_tspatialunit_type.F90, rof_comp_nuopc/rof_import_export.F90 - the reference implementation these components are transcribed from.
- EarthSciModels - the authoritative .esm corpus this component lives in.

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `Flrl_rofsur` | `mm/s` | `0.0` | lnd surface runoff to rof (CMEPS field name; kg/m^2/s of water = mm/s), [mm/s] |
| `Flrl_rofsub` | `mm/s` | `0.0` | lnd subsurface runoff to rof (CMEPS field name; kg/m^2/s of water = mm/s), [mm/s] |
| `Flrl_rofgwl` | `mm/s` | `0.0` | lnd gwl (glacier/wetland/lake) runoff to rof (CMEPS field name; kg/m^2/s of water = mm/s), [mm/s] |
| `Flrl_rofi` | `mm/s` | `0.0` | lnd frozen runoff to rof (CMEPS field name; kg/m^2/s of water = mm/s), routed directly to the outlet, [mm/s] |
| `Flrl_irrig` | `mm/s` | `-0.0001` | lnd irrigation demand to rof (CMEPS field name; kg/m^2/s of water = mm/s; negative, a demand), [mm/s] |
| `Fgrg_rofl` | `mm/s` | `0.0` | glc liquid runoff via rof (CMEPS field name; kg/m^2/s of water = mm/s), active when rof_from_glc, [mm/s] |
| `Fgrg_rofi` | `mm/s` | `0.0` | glc frozen runoff via rof (CMEPS field name; kg/m^2/s of water = mm/s), active when rof_from_glc, [mm/s] |
| `area` | `m^2` | `10000000.0` | area of the local cell (ctl%area), [m2] |
| `mm_to_m` | `m/mm` | `0.001` | millimeters to meters conversion, the 0.001 of state_getimport (rof_import_export.F90:594), spelled with units for dimensional honesty, [m/mm] |
| `med2mod_areacor` | `1` | `1.0` | mesh-to-model area correction factor for fields received from the mediator (rof_import_export.F90:210), ~1 on the rof mesh, [-] |
| `mod2med_areacor` | `1` | `1.0` | model-to-mesh area correction factor for fields sent to the mediator (rof_import_export.F90:209), ~1 on the rof mesh, [-] |
| `rof_from_glc` | `1` | `0.0` | 1 when glc runoff is routed through rof (ctl%rof_from_glc), [-]; 0/1 stands in for the Fortran logical |
| `flds_r2l_stream_channel_depths` | `1` | `0.0` | 1 when the rof->lnd stream channel depth fields are active (rof_import_export.F90:398), [-]; 0/1 stands in for the Fortran logical |
| `rofl_m3s` | `m^3/s` | `0.0` | liquid runoff to the ocean in m3/s, computed by the assembly Control model (runofftot_liq, ice_runoff branch of F90:362-382), [m3/s] |
| `rofi_m3s` | `m^3/s` | `0.0` | frozen runoff to the ocean in m3/s, computed by the assembly Control model, [m3/s] |
| `rofl_glc_m3s` | `m^3/s` | `0.0` | liquid glc runoff in m3/s, computed by the assembly Control model (direct_glc_liq, F90:385), [m3/s] |
| `rofi_glc_m3s` | `m^3/s` | `0.0` | frozen glc runoff in m3/s, computed by the assembly Control model (direct_glc_ice, F90:386), [m3/s] |
| `flood_m3s` | `m^3/s` | `0.0` | flood flux in m3/s, computed by the assembly Control model (ctl%flood, F90:516), [m3/s] |
| `volr_m3` | `m^3` | `0.0` | total water storage in m3, computed by the assembly Control model (ctl%volr = wt + wr + wh*area, F90:854), [m3] |
| `volrmch_m3` | `m^3` | `0.0` | main-channel storage in m3, computed by the assembly Control model (TRunoff%wr), [m3] |
| `tdepth_m` | `m` | `0.0` | stream depth (tributary depth yt) in m, computed by the assembly Control model, [m] |
| `tdepth_max_m` | `m` | `0.0` | maximum stream depth in m, computed by the assembly Control model, [m] |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `qsur_m3s` | `m^3/s` |  | liquid surface runoff stream (ctl%qsur, m3/s) after the cap unit conversion, [m3/s] |
| `qsub_m3s` | `m^3/s` |  | liquid subsurface runoff stream (ctl%qsub, m3/s) after the cap unit conversion, [m3/s] |
| `qgwl_m3s` | `m^3/s` |  | gwl runoff stream (ctl%qgwl, m3/s) after the cap unit conversion, [m3/s] |
| `qirrig_m3s` | `m^3/s` |  | irrigation demand stream (ctl%qirrig, m3/s; negative, a demand) after the cap unit conversion, [m3/s] |
| `qsur_ice_m3s` | `m^3/s` |  | frozen runoff stream (the Flrl_rofi field is loaded into qsur(:,nt_ice), rof_import_export.F90:286-287), always routed directly to the outlet, [m3/s] |
| `qglc_liq_m3s` | `m^3/s` |  | liquid glc runoff stream (ctl%qglc_liq, F90:298-299), active only when rof_from_glc, [m3/s] |
| `qglc_ice_m3s` | `m^3/s` |  | frozen glc runoff stream (ctl%qglc_ice, F90:301-302), active only when rof_from_glc, [m3/s] |
| `Forr_rofl` | `mm/s` |  | liquid river runoff to the ocean (CMEPS kg/m^2/s equivalent), [mm/s] |
| `Forr_rofi` | `mm/s` |  | frozen river runoff to the ocean (CMEPS kg/m^2/s equivalent), [mm/s] |
| `Forr_rofl_glc` | `mm/s` |  | liquid glc runoff to the ocean (CMEPS kg/m^2/s equivalent), [mm/s] |
| `Forr_rofi_glc` | `mm/s` |  | frozen glc runoff to the ocean (CMEPS kg/m^2/s equivalent), [mm/s] |
| `Flrr_flood` | `mm/s` |  | flood water sent back to the land, negative in the land->rof flux convention (F90:389-395), [mm/s] |
| `Flrr_volr` | `m` |  | gridcell-average total water storage sent back to the land (F90:396), [m] |
| `Flrr_volrmch` | `m` |  | gridcell-average main-channel storage sent back to the land (F90:397), [m] |
| `Sr_tdepth` | `m` |  | stream depth (tributary depth yt) for lnd, exported only when flds_r2l_stream_channel_depths (F90:398-399), [m] |
| `Sr_tdepth_max` | `m` |  | maximum stream depth = max(twidth0, 0)*(rdepth/rwidth) (F90:401), exported only when flds_r2l_stream_channel_depths, [m] |

## Observed expressions

$$
qsur_{m3s} = Flrl_{rofsur} \cdot med2mod_{areacor} \cdot area \cdot mm_{to\,m}
$$
_liquid surface runoff stream (ctl%qsur, m3/s) after the cap unit conversion, [m3/s]_

$$
qsub_{m3s} = Flrl_{rofsub} \cdot med2mod_{areacor} \cdot area \cdot mm_{to\,m}
$$
_liquid subsurface runoff stream (ctl%qsub, m3/s) after the cap unit conversion, [m3/s]_

$$
qgwl_{m3s} = Flrl_{rofgwl} \cdot med2mod_{areacor} \cdot area \cdot mm_{to\,m}
$$
_gwl runoff stream (ctl%qgwl, m3/s) after the cap unit conversion, [m3/s]_

$$
qirrig_{m3s} = Flrl_{irrig} \cdot med2mod_{areacor} \cdot area \cdot mm_{to\,m}
$$
_irrigation demand stream (ctl%qirrig, m3/s; negative, a demand) after the cap unit conversion, [m3/s]_

$$
qsur_{ice\,m3s} = Flrl_{rofi} \cdot med2mod_{areacor} \cdot area \cdot mm_{to\,m}
$$
_frozen runoff stream (the Flrl_rofi field is loaded into qsur(:,nt_ice), rof_import_export.F90:286-287), always routed directly to the outlet, [m3/s]_

$$
qglc_{liq\,m3s} = \mathrm{ifelse}\left(rof_{from\,glc} = 1.0, Fgrg_{rofl} \cdot med2mod_{areacor} \cdot area \cdot mm_{to\,m}, 0.0\right)
$$
_liquid glc runoff stream (ctl%qglc_liq, F90:298-299), active only when rof_from_glc, [m3/s]_

$$
qglc_{ice\,m3s} = \mathrm{ifelse}\left(rof_{from\,glc} = 1.0, Fgrg_{rofi} \cdot med2mod_{areacor} \cdot area \cdot mm_{to\,m}, 0.0\right)
$$
_frozen glc runoff stream (ctl%qglc_ice, F90:301-302), active only when rof_from_glc, [m3/s]_

$$
Forr_{rofl} = \frac{rofl_{m3s} \cdot mod2med_{areacor}}{area \cdot mm_{to\,m}}
$$
_liquid river runoff to the ocean (CMEPS kg/m^2/s equivalent), [mm/s]_

$$
Forr_{rofi} = \frac{rofi_{m3s} \cdot mod2med_{areacor}}{area \cdot mm_{to\,m}}
$$
_frozen river runoff to the ocean (CMEPS kg/m^2/s equivalent), [mm/s]_

$$
Forr_{rofl\,glc} = \frac{rofl_{glc\,m3s} \cdot mod2med_{areacor}}{area \cdot mm_{to\,m}}
$$
_liquid glc runoff to the ocean (CMEPS kg/m^2/s equivalent), [mm/s]_

$$
Forr_{rofi\,glc} = \frac{rofi_{glc\,m3s} \cdot mod2med_{areacor}}{area \cdot mm_{to\,m}}
$$
_frozen glc runoff to the ocean (CMEPS kg/m^2/s equivalent), [mm/s]_

$$
Flrr_{flood} = -\frac{flood_{m3s} \cdot mod2med_{areacor}}{area \cdot mm_{to\,m}}
$$
_flood water sent back to the land, negative in the land->rof flux convention (F90:389-395), [mm/s]_

$$
Flrr_{volr} = \frac{volr_{m3}}{area} \cdot mod2med_{areacor}
$$
_gridcell-average total water storage sent back to the land (F90:396), [m]_

$$
Flrr_{volrmch} = \frac{volrmch_{m3}}{area} \cdot mod2med_{areacor}
$$
_gridcell-average main-channel storage sent back to the land (F90:397), [m]_

$$
Sr_{tdepth} = \mathrm{ifelse}\left(flds_{r2l\,stream\,channel\,depths} = 1.0, tdepth_{m} \cdot mod2med_{areacor}, 0.0\right)
$$
_stream depth (tributary depth yt) for lnd, exported only when flds_r2l_stream_channel_depths (F90:398-399), [m]_

$$
Sr_{tdepth\,max} = \mathrm{ifelse}\left(flds_{r2l\,stream\,channel\,depths} = 1.0, tdepth_{max\,m} \cdot mod2med_{areacor}, 0.0\right)
$$
_maximum stream depth = max(twidth0, 0)*(rdepth/rwidth) (F90:401), exported only when flds_r2l_stream_channel_depths, [m]_

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "variables": {
    "qsur_m3s": {
      "type": "unknown",
      "units": "m^3/s",
      "description": "liquid surface runoff stream (ctl%qsur, m3/s) after the cap unit conversion, [m3/s]"
    },
    "qsub_m3s": {
      "type": "unknown",
      "units": "m^3/s",
      "description": "liquid subsurface runoff stream (ctl%qsub, m3/s) after the cap unit conversion, [m3/s]"
    },
    "qgwl_m3s": {
      "type": "unknown",
      "units": "m^3/s",
      "description": "gwl runoff stream (ctl%qgwl, m3/s) after the cap unit conversion, [m3/s]"
    },
    "qirrig_m3s": {
      "type": "unknown",
      "units": "m^3/s",
      "description": "irrigation demand stream (ctl%qirrig, m3/s; negative, a demand) after the cap unit conversion, [m3/s]"
    },
    "qsur_ice_m3s": {
      "type": "unknown",
      "units": "m^3/s",
      "description": "frozen runoff stream (the Flrl_rofi field is loaded into qsur(:,nt_ice), rof_import_export.F90:286-287), always routed directly to the outlet, [m3/s]"
    },
    "qglc_liq_m3s": {
      "type": "unknown",
      "units": "m^3/s",
      "description": "liquid glc runoff stream (ctl%qglc_liq, F90:298-299), active only when rof_from_glc, [m3/s]"
    },
    "qglc_ice_m3s": {
      "type": "unknown",
      "units": "m^3/s",
      "description": "frozen glc runoff stream (ctl%qglc_ice, F90:301-302), active only when rof_from_glc, [m3/s]"
    },
    "Forr_rofl": {
      "type": "unknown",
      "units": "mm/s",
      "description": "liquid river runoff to the ocean (CMEPS kg/m^2/s equivalent), [mm/s]"
    },
    "Forr_rofi": {
      "type": "unknown",
      "units": "mm/s",
      "description": "frozen river runoff to the ocean (CMEPS kg/m^2/s equivalent), [mm/s]"
    },
    "Forr_rofl_glc": {
      "type": "unknown",
      "units": "mm/s",
      "description": "liquid glc runoff to the ocean (CMEPS kg/m^2/s equivalent), [mm/s]"
    },
    "Forr_rofi_glc": {
      "type": "unknown",
      "units": "mm/s",
      "description": "frozen glc runoff to the ocean (CMEPS kg/m^2/s equivalent), [mm/s]"
    },
    "Flrr_flood": {
      "type": "unknown",
      "units": "mm/s",
      "description": "flood water sent back to the land, negative in the land->rof flux convention (F90:389-395), [mm/s]"
    },
    "Flrr_volr": {
      "type": "unknown",
      "units": "m",
      "description": "gridcell-average total water storage sent back to the land (F90:396), [m]"
    },
    "Flrr_volrmch": {
      "type": "unknown",
      "units": "m",
      "description": "gridcell-average main-channel storage sent back to the land (F90:397), [m]"
    },
    "Sr_tdepth": {
      "type": "unknown",
      "units": "m",
      "description": "stream depth (tributary depth yt) for lnd, exported only when flds_r2l_stream_channel_depths (F90:398-399), [m]"
    },
    "Sr_tdepth_max": {
      "type": "unknown",
      "units": "m",
      "description": "maximum stream depth = max(twidth0, 0)*(rdepth/rwidth) (F90:401), exported only when flds_r2l_stream_channel_depths, [m]"
    },
    "Flrl_rofsur": {
      "type": "parameter",
      "units": "mm/s",
      "default": 0.0,
      "description": "lnd surface runoff to rof (CMEPS field name; kg/m^2/s of water = mm/s), [mm/s]"
    },
    "Flrl_rofsub": {
      "type": "parameter",
      "units": "mm/s",
      "default": 0.0,
      "description": "lnd subsurface runoff to rof (CMEPS field name; kg/m^2/s of water = mm/s), [mm/s]"
    },
    "Flrl_rofgwl": {
      "type": "parameter",
      "units": "mm/s",
      "default": 0.0,
      "description": "lnd gwl (glacier/wetland/lake) runoff to rof (CMEPS field name; kg/m^2/s of water = mm/s), [mm/s]"
    },
    "Flrl_rofi": {
      "type": "parameter",
      "units": "mm/s",
      "default": 0.0,
      "description": "lnd frozen runoff to rof (CMEPS field name; kg/m^2/s of water = mm/s), routed directly to the outlet, [mm/s]"
    },
    "Flrl_irrig": {
      "type": "parameter",
      "units": "mm/s",
      "default": -0.0001,
      "description": "lnd irrigation demand to rof (CMEPS field name; kg/m^2/s of water = mm/s; negative, a demand), [mm/s]"
    },
    "Fgrg_rofl": {
      "type": "parameter",
      "units": "mm/s",
      "default": 0.0,
      "description": "glc liquid runoff via rof (CMEPS field name; kg/m^2/s of water = mm/s), active when rof_from_glc, [mm/s]"
    },
    "Fgrg_rofi": {
      "type": "parameter",
      "units": "mm/s",
      "default": 0.0,
      "description": "glc frozen runoff via rof (CMEPS field name; kg/m^2/s of water = mm/s), active when rof_from_glc, [mm/s]"
    },
    "area": {
      "type": "parameter",
      "units": "m^2",
      "default": 10000000.0,
      "description": "area of the local cell (ctl%area), [m2]"
    },
    "mm_to_m": {
      "type": "parameter",
      "units": "m/mm",
      "default": 0.001,
      "description": "millimeters to meters conversion, the 0.001 of state_getimport (rof_import_export.F90:594), spelled with units for dimensional honesty, [m/mm]"
    },
    "med2mod_areacor": {
      "type": "parameter",
      "units": "1",
      "default": 1.0,
      "description": "mesh-to-model area correction factor for fields received from the mediator (rof_import_export.F90:210), ~1 on the rof mesh, [-]"
    },
    "mod2med_areacor": {
      "type": "parameter",
      "units": "1",
      "default": 1.0,
      "description": "model-to-mesh area correction factor for fields sent to the mediator (rof_import_export.F90:209), ~1 on the rof mesh, [-]"
    },
    "rof_from_glc": {
      "type": "parameter",
      "units": "1",
      "default": 0.0,
      "description": "1 when glc runoff is routed through rof (ctl%rof_from_glc), [-]; 0/1 stands in for the Fortran logical"
    },
    "flds_r2l_stream_channel_depths": {
      "type": "parameter",
      "units": "1",
      "default": 0.0,
      "description": "1 when the rof->lnd stream channel depth fields are active (rof_import_export.F90:398), [-]; 0/1 stands in for the Fortran logical"
    },
    "rofl_m3s": {
      "type": "parameter",
      "units": "m^3/s",
      "default": 0.0,
      "description": "liquid runoff to the ocean in m3/s, computed by the assembly Control model (runofftot_liq, ice_runoff branch of F90:362-382), [m3/s]"
    },
    "rofi_m3s": {
      "type": "parameter",
      "units": "m^3/s",
      "default": 0.0,
      "description": "frozen runoff to the ocean in m3/s, computed by the assembly Control model, [m3/s]"
    },
    "rofl_glc_m3s": {
      "type": "parameter",
      "units": "m^3/s",
      "default": 0.0,
      "description": "liquid glc runoff in m3/s, computed by the assembly Control model (direct_glc_liq, F90:385), [m3/s]"
    },
    "rofi_glc_m3s": {
      "type": "parameter",
      "units": "m^3/s",
      "default": 0.0,
      "description": "frozen glc runoff in m3/s, computed by the assembly Control model (direct_glc_ice, F90:386), [m3/s]"
    },
    "flood_m3s": {
      "type": "parameter",
      "units": "m^3/s",
      "default": 0.0,
      "description": "flood flux in m3/s, computed by the assembly Control model (ctl%flood, F90:516), [m3/s]"
    },
    "volr_m3": {
      "type": "parameter",
      "units": "m^3",
      "default": 0.0,
      "description": "total water storage in m3, computed by the assembly Control model (ctl%volr = wt + wr + wh*area, F90:854), [m3]"
    },
    "volrmch_m3": {
      "type": "parameter",
      "units": "m^3",
      "default": 0.0,
      "description": "main-channel storage in m3, computed by the assembly Control model (TRunoff%wr), [m3]"
    },
    "tdepth_m": {
      "type": "parameter",
      "units": "m",
      "default": 0.0,
      "description": "stream depth (tributary depth yt) in m, computed by the assembly Control model, [m]"
    },
    "tdepth_max_m": {
      "type": "parameter",
      "units": "m",
      "default": 0.0,
      "description": "maximum stream depth in m, computed by the assembly Control model, [m]"
    }
  },
  "equations": [
    {
      "lhs": "qsur_m3s",
      "rhs": {
        "op": "*",
        "args": [
          "Flrl_rofsur",
          "med2mod_areacor",
          "area",
          "mm_to_m"
        ]
      }
    },
    {
      "lhs": "qsub_m3s",
      "rhs": {
        "op": "*",
        "args": [
          "Flrl_rofsub",
          "med2mod_areacor",
          "area",
          "mm_to_m"
        ]
      }
    },
    {
      "lhs": "qgwl_m3s",
      "rhs": {
        "op": "*",
        "args": [
          "Flrl_rofgwl",
          "med2mod_areacor",
          "area",
          "mm_to_m"
        ]
      }
    },
    {
      "lhs": "qirrig_m3s",
      "rhs": {
        "op": "*",
        "args": [
          "Flrl_irrig",
          "med2mod_areacor",
          "area",
          "mm_to_m"
        ]
      }
    },
    {
      "lhs": "qsur_ice_m3s",
      "rhs": {
        "op": "*",
        "args": [
          "Flrl_rofi",
          "med2mod_areacor",
          "area",
          "mm_to_m"
        ]
      }
    },
    {
      "lhs": "qglc_liq_m3s",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "==",
            "args": [
              "rof_from_glc",
              1.0
            ]
          },
          {
            "op": "*",
            "args": [
              "Fgrg_rofl",
              "med2mod_areacor",
              "area",
              "mm_to_m"
            ]
          },
          0.0
        ]
      }
    },
    {
      "lhs": "qglc_ice_m3s",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "==",
            "args": [
              "rof_from_glc",
              1.0
            ]
          },
          {
            "op": "*",
            "args": [
              "Fgrg_rofi",
              "med2mod_areacor",
              "area",
              "mm_to_m"
            ]
          },
          0.0
        ]
      }
    },
    {
      "lhs": "Forr_rofl",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "*",
            "args": [
              "rofl_m3s",
              "mod2med_areacor"
            ]
          },
          {
            "op": "*",
            "args": [
              "area",
              "mm_to_m"
            ]
          }
        ]
      }
    },
    {
      "lhs": "Forr_rofi",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "*",
            "args": [
              "rofi_m3s",
              "mod2med_areacor"
            ]
          },
          {
            "op": "*",
            "args": [
              "area",
              "mm_to_m"
            ]
          }
        ]
      }
    },
    {
      "lhs": "Forr_rofl_glc",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "*",
            "args": [
              "rofl_glc_m3s",
              "mod2med_areacor"
            ]
          },
          {
            "op": "*",
            "args": [
              "area",
              "mm_to_m"
            ]
          }
        ]
      }
    },
    {
      "lhs": "Forr_rofi_glc",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "*",
            "args": [
              "rofi_glc_m3s",
              "mod2med_areacor"
            ]
          },
          {
            "op": "*",
            "args": [
              "area",
              "mm_to_m"
            ]
          }
        ]
      }
    },
    {
      "lhs": "Flrr_flood",
      "rhs": {
        "op": "-",
        "args": [
          {
            "op": "/",
            "args": [
              {
                "op": "*",
                "args": [
                  "flood_m3s",
                  "mod2med_areacor"
                ]
              },
              {
                "op": "*",
                "args": [
                  "area",
                  "mm_to_m"
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "Flrr_volr",
      "rhs": {
        "op": "*",
        "args": [
          {
            "op": "/",
            "args": [
              "volr_m3",
              "area"
            ]
          },
          "mod2med_areacor"
        ]
      }
    },
    {
      "lhs": "Flrr_volrmch",
      "rhs": {
        "op": "*",
        "args": [
          {
            "op": "/",
            "args": [
              "volrmch_m3",
              "area"
            ]
          },
          "mod2med_areacor"
        ]
      }
    },
    {
      "lhs": "Sr_tdepth",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "==",
            "args": [
              "flds_r2l_stream_channel_depths",
              1.0
            ]
          },
          {
            "op": "*",
            "args": [
              "tdepth_m",
              "mod2med_areacor"
            ]
          },
          0.0
        ]
      }
    },
    {
      "lhs": "Sr_tdepth_max",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "==",
            "args": [
              "flds_r2l_stream_channel_depths",
              1.0
            ]
          },
          {
            "op": "*",
            "args": [
              "tdepth_max_m",
              "mod2med_areacor"
            ]
          },
          0.0
        ]
      }
    }
  ],
  "tests": [
    {
      "id": "cap_conversions_step1_cell100312",
      "description": "Instantaneous pin of the med<->rof unit conversions (rof_comp_nuopc/rof_import_export.F90:589-595 state_getimport, 636-643 state_setexport) at cell 100312 of the EqESM instrumented-CESM dry window (stage1/dumps/mosart/). The mesh-area correction factors are the run's own: med2mod_areacor = 1.00000405527865333 (areacor column of mosart_run_imports_wide.csv, row step 1, nt 1, gindex 100312, which also gives area = 2.90021364474052906e9 m2) and mod2med_areacor = 1/med2mod_areacor (F90:209-210). Import side: the Flrl_rofsur field itself is not dumped, so it is set to the value that state_getimport maps onto the dumped cap stream qsur = 7.51365591037279353e-05 m3/s (mosart_run_imports.csv row step 1, nt 1, gindex 100312): Flrl_rofsur = qsur/(med2mod_areacor*area*0.001) = 2.590714464830452e-11 mm/s; the qsur_m3s assertion therefore checks the forward conversion with the run's areacor (a conversion that ignored areacor would miss by 4e-6 rel, far outside the rel 1e-12 tolerance). The other import streams are zero in that row (qsub = qgwl = qirrig = qglc_liq = qglc_ice = 0). Export side: mosart_run_exports.csv row (step 1, nt 1, gindex 100312) gives volr = 8.11474838320261793e-01 m3, the final channel storage wr = 2.61999638886733984e-16 m3 (wr column) and its depth volrmch = wr/area = 9.03380478061898422e-26 m (volrmch column, already divided by area in mosart_run); the cap receives the storages in m3 (volr_m3, volrmch_m3 = wr) and exports Flrr_volr = volr/area*mod2med_areacor = 2.7979716220168887e-10 m and Flrr_volrmch = wr/area*mod2med_areacor = volrmch*mod2med_areacor = 9.033768146171862e-26 m (F90:396-397, 420-423: depths with no mm scaling, area-corrected on export). With runofftot = 0 and flood = 0 in that row, Forr_rofl = Forr_rofi = Forr_rofl_glc = Forr_rofi_glc = Flrr_flood = 0. time_span {0,0} evaluates the conversions pointwise (rel 1e-12).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "Flrl_rofsur": 2.590714464830452e-11,
        "Flrl_rofsub": 0.0,
        "Flrl_rofgwl": 0.0,
        "Flrl_irrig": 0.0,
        "Flrl_rofi": 0.0,
        "Fgrg_rofl": 0.0,
        "Fgrg_rofi": 0.0,
        "area": 2900213644.740529,
        "med2mod_areacor": 1.0000040552786533,
        "mod2med_areacor": 0.9999959447377919,
        "rofl_m3s": 0.0,
        "rofi_m3s": 0.0,
        "rofl_glc_m3s": 0.0,
        "rofi_glc_m3s": 0.0,
        "flood_m3s": 0.0,
        "volr_m3": 0.8114748383202618,
        "volrmch_m3": 2.61999638886734e-16,
        "tdepth_m": 0.0,
        "tdepth_max_m": 0.0
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 1e-40
      },
      "assertions": [
        {
          "variable": "qsur_m3s",
          "time": 0.0,
          "expected": 7.513655910372794e-05
        },
        {
          "variable": "qsub_m3s",
          "time": 0.0,
          "expected": 0.0
        },
        {
          "variable": "qgwl_m3s",
          "time": 0.0,
          "expected": 0.0
        },
        {
          "variable": "qirrig_m3s",
          "time": 0.0,
          "expected": 0.0
        },
        {
          "variable": "qsur_ice_m3s",
          "time": 0.0,
          "expected": 0.0
        },
        {
          "variable": "qglc_liq_m3s",
          "time": 0.0,
          "expected": 0.0
        },
        {
          "variable": "qglc_ice_m3s",
          "time": 0.0,
          "expected": 0.0
        },
        {
          "variable": "Forr_rofl",
          "time": 0.0,
          "expected": 0.0
        },
        {
          "variable": "Forr_rofi",
          "time": 0.0,
          "expected": 0.0
        },
        {
          "variable": "Forr_rofl_glc",
          "time": 0.0,
          "expected": 0.0
        },
        {
          "variable": "Forr_rofi_glc",
          "time": 0.0,
          "expected": 0.0
        },
        {
          "variable": "Flrr_flood",
          "time": 0.0,
          "expected": 0.0
        },
        {
          "variable": "Flrr_volr",
          "time": 0.0,
          "expected": 2.7979716220168887e-10
        },
        {
          "variable": "Flrr_volrmch",
          "time": 0.0,
          "expected": 9.033768146171862e-26
        },
        {
          "variable": "Sr_tdepth",
          "time": 0.0,
          "expected": 0.0
        },
        {
          "variable": "Sr_tdepth_max",
          "time": 0.0,
          "expected": 0.0
        }
      ]
    }
  ]
}
```

</details>
