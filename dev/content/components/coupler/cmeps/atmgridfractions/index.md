---
title: "AtmGridFractions"
slug: "atmgridfractions"
domains: ["coupler"]
component_types: ["model"]
subdomains: ["cmeps"]
domain: "coupler"
subdomain: "cmeps"
component_type: "model"
esm_version: "1.3.0"
esm_path: "components/coupler/cmeps/cmeps_fractions.esm"
reference: "https://github.com/ESCOMP/CESM"
description: "The surface fractions of the CMEPS mediator (med_fraction_set of mediator/med_fraction_mod.F90:774-954 plus the init-time fields of med_fraction_init, called from med_phases_post_ice) as transcribed from the M8 stage-1 dump (cmeps_fractions_*.csv of the C_JRA_t62_inst run 12446243 and the F2000climo_f19_inst rerun of 2026-11-17, fork cmeps 5e41b8ee/b548fa7c/17545715).  The per-grid laws: on the ICE grid (F90:851-856) ifrac = Si_ifrac*Si_imask and ofrac = Si_imask - ifrac with Si_ifrac the time-evolving ice export and Si_imask the constant ice domain mask (the gx1v7 ocean mask mapped onto the f19 grid in the F2000climo case takes PARTIAL values on coastal cells, so the product law is exercised non-degenerately there); the OCN grid bundle is the mapfcopy redistribution of the ice-grid fractions (F90:866-881) - in the traced configurations the ice and ocean grids are the same mesh (tx2_3v2 in C_JRA, fv1.9x2.5 in F2000), so every same-mesh map is the identity at the same global element (verified grid-wide from the cpl restarts, 0 diffs), and the two fraction maps are modeled through the single EarthSciDiscretizations conservative_overlap_apply template imported by reference (${ESD_ROOT}/regridding/conservative_overlap.esm) with the identity weights carried as data - the same map law as the cmeps_map component, one template for every ESMF routehandle; the ATM grid bundle (F90:900-929) is the ice->atm mapped ifrac, the ice->atm mapped ofrac (gated on the ocn->atm coupling; the source is the ice-grid ofrac) and aofrac = Sa_ofrac of FBImp(compatm,compatm) (F90:928), plus the init-time lfrac (the truncated residual 1 - ofrac of F90:455-481 with the |x| < 1.0e-3 truncation - NOT dumped, so lfrac is carried as DATA from the dump column, a documented gap: the init-time ofrac is not traced) and lfrin (the lnd->atm mapped lfrin of F90:421-448, = the lnd-grid Sl_lfrin at the same gid in the traced configuration); the LND grid bundle is the pure copy lfrac = lfrin = Sl_lfrin of F90:294-309 (the land model's own mask export, pinned by the stage-1 validator only: a copy law admits no failable stage-2 pin).  The models: IceGridFractions evaluates the product laws pointwise; OcnGridFractions and AtmGridFractions evaluate the identity maps on the 1x1 traced subdomain (NSRC = NTGT = 1, the single traced cell of each test; the weights-as-data treatment is the cmeps_map precedent); LndGridFractions carries the copy equations.  The fail-able cross-check of the component is the partition of unity on the ATM grid, pou = lfrac + ifrac + ofrac == 1 (asserted in every atm test; it fails if the data lfrac, pinned from the dump, does not tile with the mapped fractions - the traced F2000 rows sum to 1.0 exactly).  Configuration facts (verified by stage1/analysis/check_cmeps_fractions.py and asserted by stage1/analysis/extract_cmeps_fraction_test_rows.py on ALL dumped rows): the C_JRA atm bundle is identically zero (DATM run sequence: no MED->ATM connector, the atm fraction maps of F90:900-921 are gated off by the med_coupling_active checks); the C_JRA ocn traced cells are fully masked (So_omask = 1, the SICE mask is 1 there, so ofrac + ifrac = 1 on every row) and the mapped ice export Si_ifrac(step k) == ifrac(step k-1) bit-exactly (the mapfcopy redist maps PET-0-local index n of the ice grid to the same n of the ocn grid; the mapped Si_imask column holds the bundle reset 0.0 because Si_imask is not in the ice->ocn packed map list of this configuration); the F2000 atm lfrac/lfrin/aofrac/Sa_ofrac are constant across steps (init-time) with lfrin == lfrac on every traced cell and aofrac == Sa_ofrac == 0 (CAM does not export Sa_ofrac here); the F2000 ice Si_imask takes 5 distinct values 0.114..1.0 on the traced window (the non-degenerate product law).  The pinned rows: the F2000 ice rows (5 tests, partial mask everywhere: ifrac = Si_ifrac*Si_imask is never a copy of an input, and the step-6/step-12 rows cover the cells that enter the traced set as the ice edge moves and the time evolution of Si_ifrac), the C_JRA ocn rows (7 tests: first/mid/last traced cells at steps 1, 2, 12, 24 plus the min/max ifrac rows; the identity-map pins fail on any wrong map law or weight), and the F2000 atm rows (4 tests: the partial-land AND partial-ice cell n = 6 at steps 1 and 6 - the only cell of the window where lfrac, ifrac and ofrac are all partial, so every pin can fail and the partition-of-unity pin cross-checks the data lfrac - plus the north-pole cell gid 13753 at step 12, whose ifrac 0.99875 the wrong 0edaae42 recorder read as 0 (the bug the recorder fix removed), and the smallest partial-ice ocean cell of step 12).  The lfrin pin is dropped on the pure-ocean rows (lfrin = Sl_lfrin = 0 there: a copy of a zero input cannot fail) and the aofrac pin is dropped everywhere (aofrac = Sa_ofrac = 0 in this configuration; the equation is the law, the pin would be unfailable).  All overrides and expected values are raw dump columns at rel 1e-12 (abs 0.0); the stage-1 replay is bit-exact and the engine's summation slack on the 1-term maps is zero, so the pins hold exactly."
tags: ["coupler", "cmeps", "model", "fractions", "cesm"]
---

## Description

The surface fractions of the CMEPS mediator (med_fraction_set of mediator/med_fraction_mod.F90:774-954 plus the init-time fields of med_fraction_init, called from med_phases_post_ice) as transcribed from the M8 stage-1 dump (cmeps_fractions_*.csv of the C_JRA_t62_inst run 12446243 and the F2000climo_f19_inst rerun of 2026-11-17, fork cmeps 5e41b8ee/b548fa7c/17545715).  The per-grid laws: on the ICE grid (F90:851-856) ifrac = Si_ifrac*Si_imask and ofrac = Si_imask - ifrac with Si_ifrac the time-evolving ice export and Si_imask the constant ice domain mask (the gx1v7 ocean mask mapped onto the f19 grid in the F2000climo case takes PARTIAL values on coastal cells, so the product law is exercised non-degenerately there); the OCN grid bundle is the mapfcopy redistribution of the ice-grid fractions (F90:866-881) - in the traced configurations the ice and ocean grids are the same mesh (tx2_3v2 in C_JRA, fv1.9x2.5 in F2000), so every same-mesh map is the identity at the same global element (verified grid-wide from the cpl restarts, 0 diffs), and the two fraction maps are modeled through the single EarthSciDiscretizations conservative_overlap_apply template imported by reference (${ESD_ROOT}/regridding/conservative_overlap.esm) with the identity weights carried as data - the same map law as the cmeps_map component, one template for every ESMF routehandle; the ATM grid bundle (F90:900-929) is the ice->atm mapped ifrac, the ice->atm mapped ofrac (gated on the ocn->atm coupling; the source is the ice-grid ofrac) and aofrac = Sa_ofrac of FBImp(compatm,compatm) (F90:928), plus the init-time lfrac (the truncated residual 1 - ofrac of F90:455-481 with the |x| < 1.0e-3 truncation - NOT dumped, so lfrac is carried as DATA from the dump column, a documented gap: the init-time ofrac is not traced) and lfrin (the lnd->atm mapped lfrin of F90:421-448, = the lnd-grid Sl_lfrin at the same gid in the traced configuration); the LND grid bundle is the pure copy lfrac = lfrin = Sl_lfrin of F90:294-309 (the land model's own mask export, pinned by the stage-1 validator only: a copy law admits no failable stage-2 pin).  The models: IceGridFractions evaluates the product laws pointwise; OcnGridFractions and AtmGridFractions evaluate the identity maps on the 1x1 traced subdomain (NSRC = NTGT = 1, the single traced cell of each test; the weights-as-data treatment is the cmeps_map precedent); LndGridFractions carries the copy equations.  The fail-able cross-check of the component is the partition of unity on the ATM grid, pou = lfrac + ifrac + ofrac == 1 (asserted in every atm test; it fails if the data lfrac, pinned from the dump, does not tile with the mapped fractions - the traced F2000 rows sum to 1.0 exactly).  Configuration facts (verified by stage1/analysis/check_cmeps_fractions.py and asserted by stage1/analysis/extract_cmeps_fraction_test_rows.py on ALL dumped rows): the C_JRA atm bundle is identically zero (DATM run sequence: no MED->ATM connector, the atm fraction maps of F90:900-921 are gated off by the med_coupling_active checks); the C_JRA ocn traced cells are fully masked (So_omask = 1, the SICE mask is 1 there, so ofrac + ifrac = 1 on every row) and the mapped ice export Si_ifrac(step k) == ifrac(step k-1) bit-exactly (the mapfcopy redist maps PET-0-local index n of the ice grid to the same n of the ocn grid; the mapped Si_imask column holds the bundle reset 0.0 because Si_imask is not in the ice->ocn packed map list of this configuration); the F2000 atm lfrac/lfrin/aofrac/Sa_ofrac are constant across steps (init-time) with lfrin == lfrac on every traced cell and aofrac == Sa_ofrac == 0 (CAM does not export Sa_ofrac here); the F2000 ice Si_imask takes 5 distinct values 0.114..1.0 on the traced window (the non-degenerate product law).  The pinned rows: the F2000 ice rows (5 tests, partial mask everywhere: ifrac = Si_ifrac*Si_imask is never a copy of an input, and the step-6/step-12 rows cover the cells that enter the traced set as the ice edge moves and the time evolution of Si_ifrac), the C_JRA ocn rows (7 tests: first/mid/last traced cells at steps 1, 2, 12, 24 plus the min/max ifrac rows; the identity-map pins fail on any wrong map law or weight), and the F2000 atm rows (4 tests: the partial-land AND partial-ice cell n = 6 at steps 1 and 6 - the only cell of the window where lfrac, ifrac and ofrac are all partial, so every pin can fail and the partition-of-unity pin cross-checks the data lfrac - plus the north-pole cell gid 13753 at step 12, whose ifrac 0.99875 the wrong 0edaae42 recorder read as 0 (the bug the recorder fix removed), and the smallest partial-ice ocean cell of step 12).  The lfrin pin is dropped on the pure-ocean rows (lfrin = Sl_lfrin = 0 there: a copy of a zero input cannot fail) and the aofrac pin is dropped everywhere (aofrac = Sa_ofrac = 0 in this configuration; the equation is the law, the pin would be unfailable).  All overrides and expected values are raw dump columns at rel 1e-12 (abs 0.0); the stage-1 replay is bit-exact and the engine's summation slack on the 1-term maps is zero, so the pins hold exactly.

## Reference

- CESM (Community Earth System Model), ESCOMP/CESM: CMEPS (Coupled Mediator for Earth System Prediction) source (cesm3.0-alphabranch) - flux_atmocn/flux_atmocn_Large.F90, share/src/shr_wv_sat_mod.F90, share/src/shr_orb_mod.F90, mediator/med_phases_aofluxes_mod.F90, mediator/med_phases_ocnalb_mod.F90, mediator/med_phases_prep_ocn_mod.F90, mediator/med_phases_prep_atm_mod.F90, mediator/med_merge_mod.F90, mediator/esmFldsExchange_cesm_mod.F90 - the reference implementation these components are transcribed from.
- EarthSciModels - the authoritative .esm corpus this component lives in.

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `w_ij` | `1` | `[[1.0]]` | the routehandle weights of the traced subdomain (the ice->atm maps of F90:900-921 and the lnd->atm map of F90:421-448; the atm, ice, ocn and lnd grids share the fv1.9x2.5 mesh in the traced F2000 configuration, so every same-mesh map is the identity at the same global element - verified grid-wide from the cpl restart: atmFrac_ifrac/ofrac == iceFrac_ifrac/ofrac at 0 diffs over all 13824 cells - and the three maps' weight data coincide; the shared identity matrix is carried as data exactly like the cmeps_map weights), [1] |
| `A_j` | `1` | `[1.0]` | the row-sum normalization of the same routehandles (field_normOne = 1.0 for the same-mesh redist), [1] |
| `atol` | `1` | `0.0` | sliver filter of conservative_overlap_apply (w_ij > atol); 0 keeps the diagonal weight 1.0 and drops nothing else on the 1x1 subdomain, [1] |
| `ifrac_ice` | `1` | `[0.6206143427717847]` | the ice-grid ice-covered fraction at the traced cell (FBFrac(compice) ifrac; the F2000 atm dump does not carry the ice-grid columns, so the test overrides are the dump's atm-grid ifrac values - bit-identical to the ice-grid values at the same gid through the same-mesh redist identity, verified grid-wide), [1] |
| `ofrac_ice` | `1` | `[0.3040764458030172]` | the ice-grid open-ocean fraction at the traced cell (FBFrac(compice) ofrac, the source of the atm-grid ofrac of F90:913-921; overrides are the dump's atm-grid ofrac values as for ifrac_ice), [1] |
| `Sl_lfrin` | `1` | `[0.07530921142519809]` | the land-grid land fraction export (FBImp(complnd,complnd) Sl_lfrin, the source of the atm-grid lfrin through the lnd->atm map of F90:421-448; overrides are the dump's atm-grid lfrin values - bit-identical to the lnd-grid values at the same gid), [1] |
| `lfrac` | `1` | `[0.07530921142519809]` | the atm-grid land fraction (FBFrac(compatm) lfrac): the init-time residual 1 - ofrac of F90:455-481 with the \|x\| < 1.0e-3 truncation to 0 (eps_fraclim).  The init-time ofrac is NOT traced (no init-time dump), so the truncation law is a documented gap and lfrac is carried AS DATA from the dump column - the partition-of-unity pin pou == 1 is the fail-able cross-check that this data tiles with the mapped fractions, [1] |
| `Sa_ofrac` | `1` | `[0.0]` | the atm model's open-ocean fraction export (FBImp(compatm,compatm) Sa_ofrac; the CAM model of the traced F2000 configuration does not export it, so the column holds 0.0 on every traced row), [1] |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `ifrac` | `1` | `[0.0]` | the ice-covered fraction of the atm grid (FBFrac(compatm) ifrac): the ice->atm mapped ice-grid ifrac (F90:900-912) - the identity map in the traced configuration, [1] |
| `ofrac` | `1` | `[0.0]` | the open-ocean fraction of the atm grid (FBFrac(compatm) ofrac): the ice->atm mapped ice-grid ofrac (F90:913-921, gated on the ocn->atm coupling; the source is the ice-grid ofrac) - the identity map in the traced configuration, [1] |
| `lfrin` | `1` | `[0.0]` | the atm-grid land fraction of the lnd->atm map (FBFrac(compatm) lfrin, F90:421-448): the mapped lnd-grid lfrin = Sl_lfrin - the identity map in the traced configuration, where lfrin == lfrac on every traced cell (the f19 lnd mask and the gx1v7-derived ocean mask agree cell by cell), [1] |
| `aofrac` | `1` | `[0.0]` | the atm-grid open-ocean fraction export (FBFrac(compatm) aofrac, F90:928): aofrac = Sa_ofrac of FBImp(compatm,compatm).  NOT pinned: in the traced configuration Sa_ofrac = 0 on every row, so any pin over it would be an unfailable copy of a zero input (the equation is the law; the stage-1 validator asserts the aofrac == Sa_ofrac == 0 fact), [1] |
| `pou` | `1` | `[0.0]` | the partition of unity of the atm grid: pou = lfrac + ifrac + ofrac.  The fail-able cross-check of the component: it holds (== 1 on every traced row, exactly on the pinned rows) only when the data lfrac tiles with the mapped fractions - a wrong lfrac datum (e.g. from a configuration whose init-time ofrac differs), a broken map or a broken mask law all fail it, [1] |

## Observed expressions

$$
ifrac = \mathrm{conservative_overlap_apply}\left(A_{ij}=w_{ij}, A_{j}=A_{j}, F_{src}=ifrac_{ice}, atol=atol\right)
$$
_the ice-covered fraction of the atm grid (FBFrac(compatm) ifrac): the ice->atm mapped ice-grid ifrac (F90:900-912) - the identity map in the traced configuration, [1]_

$$
ofrac = \mathrm{conservative_overlap_apply}\left(A_{ij}=w_{ij}, A_{j}=A_{j}, F_{src}=ofrac_{ice}, atol=atol\right)
$$
_the open-ocean fraction of the atm grid (FBFrac(compatm) ofrac): the ice->atm mapped ice-grid ofrac (F90:913-921, gated on the ocn->atm coupling; the source is the ice-grid ofrac) - the identity map in the traced configuration, [1]_

$$
lfrin = \mathrm{conservative_overlap_apply}\left(A_{ij}=w_{ij}, A_{j}=A_{j}, F_{src}=Sl_{lfrin}, atol=atol\right)
$$
_the atm-grid land fraction of the lnd->atm map (FBFrac(compatm) lfrin, F90:421-448): the mapped lnd-grid lfrin = Sl_lfrin - the identity map in the traced configuration, where lfrin == lfrac on every traced cell (the f19 lnd mask and the gx1v7-derived ocean mask agree cell by cell), [1]_

$$
aofrac = Sa_{ofrac}
$$
_the atm-grid open-ocean fraction export (FBFrac(compatm) aofrac, F90:928): aofrac = Sa_ofrac of FBImp(compatm,compatm).  NOT pinned: in the traced configuration Sa_ofrac = 0 on every row, so any pin over it would be an unfailable copy of a zero input (the equation is the law; the stage-1 validator asserts the aofrac == Sa_ofrac == 0 fact), [1]_

$$
pou = lfrac + ifrac + ofrac
$$
_the partition of unity of the atm grid: pou = lfrac + ifrac + ofrac.  The fail-able cross-check of the component: it holds (== 1 on every traced row, exactly on the pinned rows) only when the data lfrac tiles with the mapped fractions - a wrong lfrac datum (e.g. from a configuration whose init-time ofrac differs), a broken map or a broken mask law all fail it, [1]_

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "expression_template_imports": [
    {
      "ref": "${ESD_ROOT}/regridding/conservative_overlap.esm",
      "only": [
        "conservative_overlap_apply"
      ],
      "bindings": {
        "NSRC": "NSRC",
        "NTGT": "NTGT",
        "NVERT": "NVERT"
      }
    }
  ],
  "variables": {
    "w_ij": {
      "type": "parameter",
      "units": "1",
      "default": [
        [
          1.0
        ]
      ],
      "description": "the routehandle weights of the traced subdomain (the ice->atm maps of F90:900-921 and the lnd->atm map of F90:421-448; the atm, ice, ocn and lnd grids share the fv1.9x2.5 mesh in the traced F2000 configuration, so every same-mesh map is the identity at the same global element - verified grid-wide from the cpl restart: atmFrac_ifrac/ofrac == iceFrac_ifrac/ofrac at 0 diffs over all 13824 cells - and the three maps' weight data coincide; the shared identity matrix is carried as data exactly like the cmeps_map weights), [1]",
      "shape": [
        "src_cells",
        "tgt_cells"
      ]
    },
    "A_j": {
      "type": "parameter",
      "units": "1",
      "default": [
        1.0
      ],
      "description": "the row-sum normalization of the same routehandles (field_normOne = 1.0 for the same-mesh redist), [1]",
      "shape": [
        "tgt_cells"
      ]
    },
    "atol": {
      "type": "parameter",
      "units": "1",
      "default": 0.0,
      "description": "sliver filter of conservative_overlap_apply (w_ij > atol); 0 keeps the diagonal weight 1.0 and drops nothing else on the 1x1 subdomain, [1]"
    },
    "ifrac_ice": {
      "type": "parameter",
      "units": "1",
      "default": [
        0.6206143427717847
      ],
      "description": "the ice-grid ice-covered fraction at the traced cell (FBFrac(compice) ifrac; the F2000 atm dump does not carry the ice-grid columns, so the test overrides are the dump's atm-grid ifrac values - bit-identical to the ice-grid values at the same gid through the same-mesh redist identity, verified grid-wide), [1]",
      "shape": [
        "src_cells"
      ]
    },
    "ofrac_ice": {
      "type": "parameter",
      "units": "1",
      "default": [
        0.3040764458030172
      ],
      "description": "the ice-grid open-ocean fraction at the traced cell (FBFrac(compice) ofrac, the source of the atm-grid ofrac of F90:913-921; overrides are the dump's atm-grid ofrac values as for ifrac_ice), [1]",
      "shape": [
        "src_cells"
      ]
    },
    "Sl_lfrin": {
      "type": "parameter",
      "units": "1",
      "default": [
        0.07530921142519809
      ],
      "description": "the land-grid land fraction export (FBImp(complnd,complnd) Sl_lfrin, the source of the atm-grid lfrin through the lnd->atm map of F90:421-448; overrides are the dump's atm-grid lfrin values - bit-identical to the lnd-grid values at the same gid), [1]",
      "shape": [
        "src_cells"
      ]
    },
    "lfrac": {
      "type": "parameter",
      "units": "1",
      "default": [
        0.07530921142519809
      ],
      "description": "the atm-grid land fraction (FBFrac(compatm) lfrac): the init-time residual 1 - ofrac of F90:455-481 with the |x| < 1.0e-3 truncation to 0 (eps_fraclim).  The init-time ofrac is NOT traced (no init-time dump), so the truncation law is a documented gap and lfrac is carried AS DATA from the dump column - the partition-of-unity pin pou == 1 is the fail-able cross-check that this data tiles with the mapped fractions, [1]",
      "shape": [
        "tgt_cells"
      ]
    },
    "Sa_ofrac": {
      "type": "parameter",
      "units": "1",
      "default": [
        0.0
      ],
      "description": "the atm model's open-ocean fraction export (FBImp(compatm,compatm) Sa_ofrac; the CAM model of the traced F2000 configuration does not export it, so the column holds 0.0 on every traced row), [1]",
      "shape": [
        "tgt_cells"
      ]
    },
    "ifrac": {
      "type": "unknown",
      "units": "1",
      "default": [
        0.0
      ],
      "description": "the ice-covered fraction of the atm grid (FBFrac(compatm) ifrac): the ice->atm mapped ice-grid ifrac (F90:900-912) - the identity map in the traced configuration, [1]",
      "shape": [
        "tgt_cells"
      ]
    },
    "ofrac": {
      "type": "unknown",
      "units": "1",
      "default": [
        0.0
      ],
      "description": "the open-ocean fraction of the atm grid (FBFrac(compatm) ofrac): the ice->atm mapped ice-grid ofrac (F90:913-921, gated on the ocn->atm coupling; the source is the ice-grid ofrac) - the identity map in the traced configuration, [1]",
      "shape": [
        "tgt_cells"
      ]
    },
    "lfrin": {
      "type": "unknown",
      "units": "1",
      "default": [
        0.0
      ],
      "description": "the atm-grid land fraction of the lnd->atm map (FBFrac(compatm) lfrin, F90:421-448): the mapped lnd-grid lfrin = Sl_lfrin - the identity map in the traced configuration, where lfrin == lfrac on every traced cell (the f19 lnd mask and the gx1v7-derived ocean mask agree cell by cell), [1]",
      "shape": [
        "tgt_cells"
      ]
    },
    "aofrac": {
      "type": "unknown",
      "units": "1",
      "default": [
        0.0
      ],
      "description": "the atm-grid open-ocean fraction export (FBFrac(compatm) aofrac, F90:928): aofrac = Sa_ofrac of FBImp(compatm,compatm).  NOT pinned: in the traced configuration Sa_ofrac = 0 on every row, so any pin over it would be an unfailable copy of a zero input (the equation is the law; the stage-1 validator asserts the aofrac == Sa_ofrac == 0 fact), [1]",
      "shape": [
        "tgt_cells"
      ]
    },
    "pou": {
      "type": "unknown",
      "units": "1",
      "default": [
        0.0
      ],
      "description": "the partition of unity of the atm grid: pou = lfrac + ifrac + ofrac.  The fail-able cross-check of the component: it holds (== 1 on every traced row, exactly on the pinned rows) only when the data lfrac tiles with the mapped fractions - a wrong lfrac datum (e.g. from a configuration whose init-time ofrac differs), a broken map or a broken mask law all fail it, [1]",
      "shape": [
        "tgt_cells"
      ]
    }
  },
  "equations": [
    {
      "lhs": "ifrac",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "conservative_overlap_apply",
        "bindings": {
          "A_ij": "w_ij",
          "A_j": "A_j",
          "F_src": "ifrac_ice",
          "atol": "atol"
        }
      }
    },
    {
      "lhs": "ofrac",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "conservative_overlap_apply",
        "bindings": {
          "A_ij": "w_ij",
          "A_j": "A_j",
          "F_src": "ofrac_ice",
          "atol": "atol"
        }
      }
    },
    {
      "lhs": "lfrin",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "conservative_overlap_apply",
        "bindings": {
          "A_ij": "w_ij",
          "A_j": "A_j",
          "F_src": "Sl_lfrin",
          "atol": "atol"
        }
      }
    },
    {
      "lhs": "aofrac",
      "rhs": "Sa_ofrac"
    },
    {
      "lhs": "pou",
      "rhs": {
        "op": "+",
        "args": [
          "lfrac",
          {
            "op": "+",
            "args": [
              "ifrac",
              "ofrac"
            ]
          }
        ]
      }
    }
  ],
  "tests": [
    {
      "id": "step1_first_cell",
      "description": "Instantaneous pin of the atm-grid fraction maps (the ice->atm maps of F90:900-921 and the lnd->atm map of F90:421-448) from stage1/dumps/cmeps/cmeps_fractions_f2000_atm.csv: row (step 1, gid 11737, atm cell n = 6, lat 63.474 deg, lon 180.0 deg).  The only cell of the window with lfrac, ifrac AND ofrac all partial (lfrac = 0.07531, ifrac = 0.62061, ofrac = 0.30408): every pin can fail, and the partition-of-unity pin pou = lfrac + ifrac + ofrac = 1.0 exactly cross-checks the data lfrac against the mapped fractions.  lfrin = lfrac = 0.07531 (the lnd->atm mapped Sl_lfrin).  time_span {0,0} evaluates the maps at the dumped inputs; the outputs are asserted at dump precision, rel 1e-12 (abs 0.0).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "ifrac_ice": [
          0.6206143427717847
        ],
        "ofrac_ice": [
          0.3040764458030172
        ],
        "Sl_lfrin": [
          0.07530921142519809
        ],
        "lfrac": [
          0.07530921142519809
        ],
        "Sa_ofrac": [
          0.0
        ]
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 0.0
      },
      "assertions": [
        {
          "variable": "ifrac",
          "time": 0.0,
          "coords": {
            "tgt_cells": 1
          },
          "expected": 0.6206143427717847
        },
        {
          "variable": "ofrac",
          "time": 0.0,
          "coords": {
            "tgt_cells": 1
          },
          "expected": 0.3040764458030172
        },
        {
          "variable": "lfrin",
          "time": 0.0,
          "coords": {
            "tgt_cells": 1
          },
          "expected": 0.07530921142519809
        },
        {
          "variable": "pou",
          "time": 0.0,
          "coords": {
            "tgt_cells": 1
          },
          "expected": 1.0
        }
      ]
    },
    {
      "id": "step6_mid_land",
      "description": "Instantaneous pin of the atm-grid fraction maps (the ice->atm maps of F90:900-921 and the lnd->atm map of F90:421-448) from stage1/dumps/cmeps/cmeps_fractions_f2000_atm.csv: row (step 6, gid 11737, atm cell n = 6).  The same cell at mid-window - the runtime update of the mapped fractions (ifrac 0.62061 -> 0.62160, ofrac 0.30408 -> 0.30309) against the init-constant lfrac/lfrin (0.07531 unchanged); pou = 1.0 exactly.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "ifrac_ice": [
          0.6216029408363338
        ],
        "ofrac_ice": [
          0.3030878477384681
        ],
        "Sl_lfrin": [
          0.07530921142519809
        ],
        "lfrac": [
          0.07530921142519809
        ],
        "Sa_ofrac": [
          0.0
        ]
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 0.0
      },
      "assertions": [
        {
          "variable": "ifrac",
          "time": 0.0,
          "coords": {
            "tgt_cells": 1
          },
          "expected": 0.6216029408363338
        },
        {
          "variable": "ofrac",
          "time": 0.0,
          "coords": {
            "tgt_cells": 1
          },
          "expected": 0.3030878477384681
        },
        {
          "variable": "lfrin",
          "time": 0.0,
          "coords": {
            "tgt_cells": 1
          },
          "expected": 0.07530921142519809
        },
        {
          "variable": "pou",
          "time": 0.0,
          "coords": {
            "tgt_cells": 1
          },
          "expected": 1.0
        }
      ]
    },
    {
      "id": "step12_north_pole",
      "description": "Instantaneous pin of the atm-grid fraction maps (the ice->atm maps of F90:900-921) from stage1/dumps/cmeps/cmeps_fractions_f2000_atm.csv: row (step 12, gid 13753, atm cell n = 2, lat 90.0 deg, lon 180.0 deg).  The north-pole cell, nearly fully iced: ifrac = 0.99875, ofrac = 0.00125, lfrac = 0 (the truncated residual: land-free ocean).  This is the cell whose ice-grid input the wrong 0edaae42 recorder read as 0 at this element (the cross-grid same-element bug the recorder fix of 2026-11-17 removed: the true value is 0.99875, verified against the cpl restart).  The lfrin pin is dropped here: Sl_lfrin = 0 at this cell, so lfrin = 0 is a copy of a zero input that cannot fail.  pou = 1.0 exactly (lfrac = 0 + ifrac + ofrac = the mask 1).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "ifrac_ice": [
          0.9987490205995498
        ],
        "ofrac_ice": [
          0.0012509794004501584
        ],
        "Sl_lfrin": [
          0.0
        ],
        "lfrac": [
          0.0
        ],
        "Sa_ofrac": [
          0.0
        ]
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 0.0
      },
      "assertions": [
        {
          "variable": "ifrac",
          "time": 0.0,
          "coords": {
            "tgt_cells": 1
          },
          "expected": 0.9987490205995498
        },
        {
          "variable": "ofrac",
          "time": 0.0,
          "coords": {
            "tgt_cells": 1
          },
          "expected": 0.0012509794004501584
        },
        {
          "variable": "pou",
          "time": 0.0,
          "coords": {
            "tgt_cells": 1
          },
          "expected": 1.0
        }
      ]
    },
    {
      "id": "step12_min_ice",
      "description": "Instantaneous pin of the atm-grid fraction maps (the ice->atm maps of F90:900-921) from stage1/dumps/cmeps/cmeps_fractions_f2000_atm.csv: row (step 12, gid 11738, atm cell n = 22, lat 63.474 deg, lon 182.5 deg).  The smallest nonzero partial-ice ocean cell of the last step: ifrac = 0.48385, ofrac = 0.51615, lfrac = 0.  The lfrin pin is dropped (Sl_lfrin = 0 at this cell, an unfailable copy).  pou = 1.0 exactly.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "ifrac_ice": [
          0.483847544077904
        ],
        "ofrac_ice": [
          0.516152455922096
        ],
        "Sl_lfrin": [
          0.0
        ],
        "lfrac": [
          0.0
        ],
        "Sa_ofrac": [
          0.0
        ]
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 0.0
      },
      "assertions": [
        {
          "variable": "ifrac",
          "time": 0.0,
          "coords": {
            "tgt_cells": 1
          },
          "expected": 0.483847544077904
        },
        {
          "variable": "ofrac",
          "time": 0.0,
          "coords": {
            "tgt_cells": 1
          },
          "expected": 0.516152455922096
        },
        {
          "variable": "pou",
          "time": 0.0,
          "coords": {
            "tgt_cells": 1
          },
          "expected": 1.0
        }
      ]
    }
  ]
}
```

</details>
