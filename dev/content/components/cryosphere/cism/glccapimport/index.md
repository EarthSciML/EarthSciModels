---
title: "GlcCapImport"
slug: "glccapimport"
domains: ["cryosphere"]
component_types: ["model"]
subdomains: ["cism"]
domain: "cryosphere"
subdomain: "cism"
component_type: "model"
esm_version: "2.0.0"
esm_path: "components/cryosphere/cism/cism_cap.esm"
reference: "https://github.com/ESCOMP/CESM"
description: "Stage-2 implementation of the CISM GLC cap coupling boundary (stage 2 of the EqESM project; CISM = cismwrap_3_00_002 / cism_main_3.00.002 as built in CESM cesm3.0-alphabranch, reference run T1850Gg/f09_g17_gris20, CISM_LANE.md row 15): the mediator-to-CISM import transformations and the CISM-to-mediator export laws around glad_gcm. (a) GlcCapImport - the cap import_fields processing (drivers/cpl/nuopc/glc_import_export.F90:326-333): tsfc = tsfc_raw - tkfrz (the Sl_tsrf temperature, K, converted to degC by subtracting SHR_CONST_TKFRZ = 273.15 K, glc_constants.F90:22-23, shr_const_mod.F90:37) with the -250 degC sentinel clamp to 0 (the 'Jer hack' of F90:328-333: land points where CLM sees ocean send a raw 0 K, which the conversion would drop to -273.15 degC), and the qsmb pass-through (state_getimport, F90:679-714, applies no conversion; qsmb stays kg/m2/s). The halo conversion (vector_to_spatial / parallel_convert_nonhaloed_to_haloed) is a grid operation, deferred to the stage-3 assembly. The model-side continuation - the mbal averaging of qsmb/tsfc over the coupling interval and the qsmb -> acab SMB conversion (glad_main.F90:800-824, glad_timestep.F90:200, glide_set_acab; acab = qsmb * tstep_mbal * 3600/1000 * rhow/rhoi m/yr ice, pinned by the stage-1 smb_chain validator check) - belongs to the surface-forcing/transport lane, not the cap. (b) GlcCapExport - the export fields of glad_set_output_fields (glad_main.F90:971-1027) / set_output_states (glad_output_states.F90:48-105): the surface elevation topo = usrf gated by the active grid (usrf > 0, F90:110-133), the ice-covered flag ice_covered = (thck > min_thck = 0, F90:137-158, glad_constants.F90:63) AND (usrf > 0), and the three coupling-interval-averaged fluxes of glad_output_fluxes (F90:77-161): rofi = mean over the interval of rhoi*(calving_thck + removal_thck)/dt (F90:104-105), rofl = mean of rhoi*bmlt + rhoi*lateral_melt_thck/dt (F90:128-129), hflx = mean of -ucondflx (F90:138-139; ucondflx positive down, glissade_therm.F90:669; the sign flip makes hflx positive up per the F90:135-136 comment, which contradicts the 'positive down' labels of glad_main.F90:625 and the CMEPS field dictionary esmFldsExchange_cesm_mod.F90:816 - see bugs.md; unpinned by the dump because hflx = 0 everywhere in this window). The averages are written as storage ODEs D(S)/dt = f with the export S/T_coupling - the continuous limit of the Fortran's per-dynamics-step accumulation (reset at the interval start, glad_timestep.F90:149; one accumulation per glissade_tstep, F90:290; average = sum/av_count_output, F90:151-159). With piecewise-constant integrands over the n_icetstep = 2 dynamics steps of dt = 0.5 yr, the Fortran average sum_k f_k/count equals (1/T_coupling)*integral_0^T_coupling f dt with T_coupling = count*dt = 8760 h = 3.1536e7 s (tstep_mbal at GLC_NCPL = 1), so the ODE form is that integral exactly. The literal `integral` op is NOT used because the CLI cannot lower it (probed: unlowered_operator, esm-spec section 4.2 / 9.6.8 - a file using it validates but cannot simulate); the differential form is the same continuous limit the rest of stage 2 uses for storage (mosart_channel D(wr)/dt). The integrands (calving_thck, removal_thck, bmlt, lateral_melt_thck, ucondflx) are per-dynamics-step CISM state that cism_cap.csv does not carry, so they enter as parameters (the dump carries only the final interval averages, all zero in this window: a 2-year cold-base run with no calving, no basal melt and ucondflx = 0); the averages' zero rows are dump-pinned and the averaging law itself is pinned synthetically with constant integrands from the source formula. ice_sheet_grid_mask (= the same active-grid gate) is not dumped and is not modeled. Time convention: model time in seconds, matching the dump's thour column x 3600 (cap_step 1 at 0 h, cap_step 2 at 8760 h)."
tags: ["cryosphere", "cism", "model", "ice-sheet", "coupler", "cmeps", "unit-conversion", "cesm"]
---

## Description

Stage-2 implementation of the CISM GLC cap coupling boundary (stage 2 of the EqESM project; CISM = cismwrap_3_00_002 / cism_main_3.00.002 as built in CESM cesm3.0-alphabranch, reference run T1850Gg/f09_g17_gris20, CISM_LANE.md row 15): the mediator-to-CISM import transformations and the CISM-to-mediator export laws around glad_gcm. (a) GlcCapImport - the cap import_fields processing (drivers/cpl/nuopc/glc_import_export.F90:326-333): tsfc = tsfc_raw - tkfrz (the Sl_tsrf temperature, K, converted to degC by subtracting SHR_CONST_TKFRZ = 273.15 K, glc_constants.F90:22-23, shr_const_mod.F90:37) with the -250 degC sentinel clamp to 0 (the 'Jer hack' of F90:328-333: land points where CLM sees ocean send a raw 0 K, which the conversion would drop to -273.15 degC), and the qsmb pass-through (state_getimport, F90:679-714, applies no conversion; qsmb stays kg/m2/s). The halo conversion (vector_to_spatial / parallel_convert_nonhaloed_to_haloed) is a grid operation, deferred to the stage-3 assembly. The model-side continuation - the mbal averaging of qsmb/tsfc over the coupling interval and the qsmb -> acab SMB conversion (glad_main.F90:800-824, glad_timestep.F90:200, glide_set_acab; acab = qsmb * tstep_mbal * 3600/1000 * rhow/rhoi m/yr ice, pinned by the stage-1 smb_chain validator check) - belongs to the surface-forcing/transport lane, not the cap. (b) GlcCapExport - the export fields of glad_set_output_fields (glad_main.F90:971-1027) / set_output_states (glad_output_states.F90:48-105): the surface elevation topo = usrf gated by the active grid (usrf > 0, F90:110-133), the ice-covered flag ice_covered = (thck > min_thck = 0, F90:137-158, glad_constants.F90:63) AND (usrf > 0), and the three coupling-interval-averaged fluxes of glad_output_fluxes (F90:77-161): rofi = mean over the interval of rhoi*(calving_thck + removal_thck)/dt (F90:104-105), rofl = mean of rhoi*bmlt + rhoi*lateral_melt_thck/dt (F90:128-129), hflx = mean of -ucondflx (F90:138-139; ucondflx positive down, glissade_therm.F90:669; the sign flip makes hflx positive up per the F90:135-136 comment, which contradicts the 'positive down' labels of glad_main.F90:625 and the CMEPS field dictionary esmFldsExchange_cesm_mod.F90:816 - see bugs.md; unpinned by the dump because hflx = 0 everywhere in this window). The averages are written as storage ODEs D(S)/dt = f with the export S/T_coupling - the continuous limit of the Fortran's per-dynamics-step accumulation (reset at the interval start, glad_timestep.F90:149; one accumulation per glissade_tstep, F90:290; average = sum/av_count_output, F90:151-159). With piecewise-constant integrands over the n_icetstep = 2 dynamics steps of dt = 0.5 yr, the Fortran average sum_k f_k/count equals (1/T_coupling)*integral_0^T_coupling f dt with T_coupling = count*dt = 8760 h = 3.1536e7 s (tstep_mbal at GLC_NCPL = 1), so the ODE form is that integral exactly. The literal `integral` op is NOT used because the CLI cannot lower it (probed: unlowered_operator, esm-spec section 4.2 / 9.6.8 - a file using it validates but cannot simulate); the differential form is the same continuous limit the rest of stage 2 uses for storage (mosart_channel D(wr)/dt). The integrands (calving_thck, removal_thck, bmlt, lateral_melt_thck, ucondflx) are per-dynamics-step CISM state that cism_cap.csv does not carry, so they enter as parameters (the dump carries only the final interval averages, all zero in this window: a 2-year cold-base run with no calving, no basal melt and ucondflx = 0); the averages' zero rows are dump-pinned and the averaging law itself is pinned synthetically with constant integrands from the source formula. ice_sheet_grid_mask (= the same active-grid gate) is not dumped and is not modeled. Time convention: model time in seconds, matching the dump's thour column x 3600 (cap_step 1 at 0 h, cap_step 2 at 8760 h).

## Reference

- CISM (Community Ice Sheet Model) cismwrap_3_00_002 / cism_main_3.00.002, as built in CESM cesm3.0-alphabranch (checkout stage1/cesm/components/cism, reference run T1850Gg/f09_g17_gris20): libglissade/glissade_basal_traction.F90, libglissade/glissade_therm.F90, libglissade/glissade_grid_operators.F90, libglissade/glissade_velo_higher.F90, libglissade/glissade_mass_balance.F90, libglissade/glissade_calving.F90, libglissade/glissade_masks.F90, libglissade/glissade_utils.F90, libglimmer/glimmer_physcon.F90, libglimmer/glimmer_utils.F90, libglide/glide_types.F90, libglide/glide_setup.F90, libglad/glad_main.F90, libglad/glad_timestep.F90, libglad/glad_output_states.F90, libglad/glad_output_fluxes.F90, drivers/cpl/nuopc/glc_import_export.F90 - the reference implementation these components are transcribed from.
- EarthSciModels - the authoritative .esm corpus this component lives in.

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `tsfc_raw` | `K` | `273.15` | raw mediator surface temperature Sl_tsrf (K) at the cap input; the dump carries only the CONVERTED tsfc (degC), so the test inputs reconstruct the raw value as tsfc_dump + tkfrz (valid on every dump row: no traced cell hits the clamp, tsfc in [-9.68, -0.004] degC) |
| `qsmb_raw` | `kg/m^2/s` | `0.0` | raw mediator ice flux Flgl_qice (kg/m2/s); state_getimport applies no conversion, so qsmb passes through unchanged |
| `tkfrz` | `K` | `273.15` | freezing point of fresh water SHR_CONST_TKFRZ (glc_constants.F90:22-23, shr_const_mod.F90:37) |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `tsfc_c` | `degC` |  | Converted surface temperature (degC) before the sentinel clamp: tsfc_c = tsfc_raw - tkfrz, the cap import_fields conversion of glc_import_export.F90:326-333 (Sl_tsrf in K minus SHR_CONST_TKFRZ = 273.15 K, glc_constants.F90:22-23, shr_const_mod.F90:37). Named intermediate consumed once by cism_tsfc_import (the -250 degC sentinel clamp), so the conversion and the clamp stay separate templates. |
| `tsfc` | `degC` |  | surface temperature as consumed by CISM (degC): the sentinel clamp of the converted intermediate, tsfc = ifelse(tsfc_c < -250, 0, tsfc_c) with tsfc_c = tsfc_raw - tkfrz - the cap import_fields processing of glc_import_export.F90:326-333 |
| `qsmb` | `kg/m^2/s` |  | surface mass balance flux as consumed by CISM (kg/m2/s); identical to qsmb_raw (the cap applies no conversion) |

## Observed expressions

$$
tsfc_{c} = tsfc_{raw} - tkfrz
$$
_Converted surface temperature (degC) before the sentinel clamp: tsfc_c = tsfc_raw - tkfrz, the cap import_fields conversion of glc_import_export.F90:326-333 (Sl_tsrf in K minus SHR_CONST_TKFRZ = 273.15 K, glc_constants.F90:22-23, shr_const_mod.F90:37). Named intermediate consumed once by cism_tsfc_import (the -250 degC sentinel clamp), so the conversion and the clamp stay separate templates._

$$
tsfc = \mathrm{cism_tsfc_import}\left(tsfc_{c}=tsfc_{c}\right)
$$
_surface temperature as consumed by CISM (degC): the sentinel clamp of the converted intermediate, tsfc = ifelse(tsfc_c < -250, 0, tsfc_c) with tsfc_c = tsfc_raw - tkfrz - the cap import_fields processing of glc_import_export.F90:326-333_

$$
qsmb = qsmb_{raw}
$$
_surface mass balance flux as consumed by CISM (kg/m2/s); identical to qsmb_raw (the cap applies no conversion)_

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "expression_template_imports": [
    {
      "ref": "./cism_templates.esm"
    }
  ],
  "variables": {
    "tsfc_raw": {
      "type": "parameter",
      "units": "K",
      "default": 273.15,
      "description": "raw mediator surface temperature Sl_tsrf (K) at the cap input; the dump carries only the CONVERTED tsfc (degC), so the test inputs reconstruct the raw value as tsfc_dump + tkfrz (valid on every dump row: no traced cell hits the clamp, tsfc in [-9.68, -0.004] degC)"
    },
    "qsmb_raw": {
      "type": "parameter",
      "units": "kg/m^2/s",
      "default": 0.0,
      "description": "raw mediator ice flux Flgl_qice (kg/m2/s); state_getimport applies no conversion, so qsmb passes through unchanged"
    },
    "tkfrz": {
      "type": "parameter",
      "units": "K",
      "default": 273.15,
      "description": "freezing point of fresh water SHR_CONST_TKFRZ (glc_constants.F90:22-23, shr_const_mod.F90:37)"
    },
    "tsfc_c": {
      "type": "unknown",
      "units": "degC",
      "description": "Converted surface temperature (degC) before the sentinel clamp: tsfc_c = tsfc_raw - tkfrz, the cap import_fields conversion of glc_import_export.F90:326-333 (Sl_tsrf in K minus SHR_CONST_TKFRZ = 273.15 K, glc_constants.F90:22-23, shr_const_mod.F90:37). Named intermediate consumed once by cism_tsfc_import (the -250 degC sentinel clamp), so the conversion and the clamp stay separate templates."
    },
    "tsfc": {
      "type": "unknown",
      "units": "degC",
      "description": "surface temperature as consumed by CISM (degC): the sentinel clamp of the converted intermediate, tsfc = ifelse(tsfc_c < -250, 0, tsfc_c) with tsfc_c = tsfc_raw - tkfrz - the cap import_fields processing of glc_import_export.F90:326-333"
    },
    "qsmb": {
      "type": "unknown",
      "units": "kg/m^2/s",
      "description": "surface mass balance flux as consumed by CISM (kg/m2/s); identical to qsmb_raw (the cap applies no conversion)"
    }
  },
  "equations": [
    {
      "lhs": "tsfc_c",
      "rhs": {
        "op": "-",
        "args": [
          "tsfc_raw",
          "tkfrz"
        ]
      },
      "_comment": "The K -> degC conversion of the cap import (F90:326-333), named once and consumed by the clamp below"
    },
    {
      "lhs": "tsfc",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "cism_tsfc_import",
        "bindings": {
          "tsfc_c": "tsfc_c"
        }
      }
    },
    {
      "lhs": "qsmb",
      "rhs": "qsmb_raw"
    }
  ],
  "tests": [
    {
      "id": "import_step1_cell2511",
      "description": "Dump pin, cism_cap.csv import row (cap_step 1, cell 25,11): tsfc = -1.71672789484000532 degC and qsmb = 4.05302216536369290e-06 kg/m2/s as consumed by CISM. The raw mediator value is rebuilt from the dumped tsfc by inverting the conversion, tsfc_raw = tsfc_dump + tkfrz = -1.7167278948400053 + 273.15 = 271.43327210516 K, and the converted intermediate comes back as tsfc_c = tsfc_dump: the round-trip pins the named intermediate, and the reconstructed value sits far above the -250 degC clamp threshold, showing the sentinel clamp did not fire on any traced row (all 64 import rows have tsfc in [-9.68, -0.004] degC; the clamp itself is pinned by the synthetic import_clamp_* tests).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "tsfc_raw": 271.43327210516,
        "qsmb_raw": 4.053022165363693e-06
      },
      "assertions": [
        {
          "variable": "tsfc",
          "time": 0.0,
          "expected": -1.7167278948400053,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "tsfc_c",
          "time": 0.0,
          "expected": -1.7167278948400053,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "qsmb",
          "time": 0.0,
          "expected": 4.053022165363693e-06,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "import_step1_cell2811_negative_smb",
      "description": "Dump pin, cism_cap.csv import row (cap_step 1, cell 28,11): a negative-SMB cell (ablation): qsmb = -2.05729925935643034e-05 kg/m2/s passes through unchanged; tsfc = -2.38918507155790394 degC, rebuilt as tsfc_raw = tsfc_dump + tkfrz = 270.7608149284421 K and converted back to tsfc_c = tsfc_dump (again far above the -250 degC clamp threshold, which did not fire).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "tsfc_raw": 270.7608149284421,
        "qsmb_raw": -2.0572992593564303e-05
      },
      "assertions": [
        {
          "variable": "tsfc",
          "time": 0.0,
          "expected": -2.389185071557904,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "tsfc_c",
          "time": 0.0,
          "expected": -2.389185071557904,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "qsmb",
          "time": 0.0,
          "expected": -2.0572992593564303e-05,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "import_step2_cell2511",
      "description": "Dump pin, cism_cap.csv import row (cap_step 2, cell 25,11): the second coupling year's forcing: tsfc = -1.5278547818759307 degC (tsfc_raw = tsfc_dump + tkfrz = 271.62214521812405 K, round-tripping to tsfc_c = tsfc_dump - no clamp), qsmb = -1.69074734385491e-05 kg/m2/s (this cell's SMB turned negative in year 2).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "tsfc_raw": 271.62214521812405,
        "qsmb_raw": -1.69074734385491e-05
      },
      "assertions": [
        {
          "variable": "tsfc",
          "time": 0.0,
          "expected": -1.5278547818759307,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "tsfc_c",
          "time": 0.0,
          "expected": -1.5278547818759307,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "qsmb",
          "time": 0.0,
          "expected": -1.69074734385491e-05,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "import_step1_cell2714_coldest",
      "description": "Dump pin, cism_cap.csv import row (cap_step 1, cell 27,14): the coldest traced surface temperature, tsfc = -9.678254083449986 degC (tsfc_raw = tsfc_dump + tkfrz = 263.47174591655 K, round-tripping to tsfc_c = tsfc_dump - still ~240 degC above the clamp threshold, which did not fire; qsmb = 6.438260380534927e-05 kg/m2/s), exercising the conversion away from the clamp.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "tsfc_raw": 263.47174591655,
        "qsmb_raw": 6.438260380534927e-05
      },
      "assertions": [
        {
          "variable": "tsfc",
          "time": 0.0,
          "expected": -9.678254083449986,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "tsfc_c",
          "time": 0.0,
          "expected": -9.678254083449986,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "qsmb",
          "time": 0.0,
          "expected": 6.438260380534927e-05,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "import_step2_cell2812_warmest",
      "description": "Dump pin, cism_cap.csv import row (cap_step 2, cell 28,12): the warmest traced surface temperature, tsfc = -0.003957271002548168 degC (tsfc_raw = tsfc_dump + tkfrz = 273.14604272899743 K, barely below freezing; the round-trip tsfc_c = tsfc_dump is ~250 degC above the clamp threshold, which did not fire; qsmb = 1.2898195203542923e-05 kg/m2/s).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "tsfc_raw": 273.14604272899743,
        "qsmb_raw": 1.2898195203542923e-05
      },
      "assertions": [
        {
          "variable": "tsfc",
          "time": 0.0,
          "expected": -0.003957271002548168,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "tsfc_c",
          "time": 0.0,
          "expected": -0.003957271002548168,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "qsmb",
          "time": 0.0,
          "expected": 1.2898195203542923e-05,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "import_clamp_sentinel",
      "description": "The -250 degC sentinel clamp firing, from the SOURCE FORMULA (glc_import_export.F90:326-333; no dump row hits it - the traced cells are all CLM land/ice points): the 'Jer hack' case of F90:328-332 - a land point where CLM sees ocean sends raw 0 K, which the -tkfrz conversion drops to -273.15 degC; the where-clamp resets it to 0 degC.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "tsfc_raw": 0.0
      },
      "assertions": [
        {
          "variable": "tsfc",
          "time": 0.0,
          "expected": 0.0
        }
      ]
    },
    {
      "id": "import_clamp_boundary_open",
      "description": "The clamp boundary, from the SOURCE FORMULA: tsfc_raw = 23.15 K converts to exactly -250 degC, which does NOT fire the strict (<) where-condition of F90:333 - the converted value passes through unchanged (tsfc = -250 degC).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "tsfc_raw": 23.15
      },
      "assertions": [
        {
          "variable": "tsfc",
          "time": 0.0,
          "expected": -250.0
        }
      ]
    },
    {
      "id": "import_clamp_just_below",
      "description": "The clamp just below the boundary, from the SOURCE FORMULA: tsfc_raw = 23.1499 K converts to -250.0001 degC < -250, so the where-condition fires and tsfc = 0 degC (the strict-< boundary of F90:333 sits between this row and import_clamp_boundary_open).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "tsfc_raw": 23.1499
      },
      "assertions": [
        {
          "variable": "tsfc",
          "time": 0.0,
          "expected": 0.0
        }
      ]
    },
    {
      "id": "import_warm_branch",
      "description": "The unconverted linear branch, from the SOURCE FORMULA: tsfc_raw = 293.15 K (20 degC) converts to tsfc = 20 degC with no clamp (the dump window's tsfc are all below freezing; this pins the linear branch away from the traced range).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "tsfc_raw": 293.15
      },
      "assertions": [
        {
          "variable": "tsfc",
          "time": 0.0,
          "expected": 20.0
        }
      ]
    }
  ]
}
```

</details>
