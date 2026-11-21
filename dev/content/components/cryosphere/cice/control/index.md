---
title: "Control"
slug: "control"
domains: ["cryosphere"]
component_types: ["model"]
subdomains: ["cice"]
domain: "cryosphere"
subdomain: "cice"
component_type: "model"
esm_version: "2.0.0"
esm_path: "components/cryosphere/cice/cice.esm"
reference: "Hunke, E. C., Allard, R., Bailey, D. A., Blain, P., Craig, A., Dupont, F., ... & Roberts, A. F. (2023). CICE-Consortium Icepack v1.2.4 and CICE v6.3.22: documentation and user's guide. Los Alamos National Laboratory (LA-UR-23-31851)."
description: "CICE sea-ice top-level component (stage 2 of the EqESM project): the cesm3_cice6_6_3_22 ice component as an esm 2.0.0 assembly, per the stage1/boundaries.md 1.3 boundary table. Five systems: IceCap (mounted from ./cice_coupling.esm, the med<->ice cap renames, the med2mod/mod2med areacor scaling, and the merge_fluxes export aggregation of ice_import_export.F90), Thermodynamics (./cice_thermodynamics.esm, the BL99 column physics: prep_radiation shortwave/albedo, step_therm1 vertical conduction and surface energy balance, step_therm2 growth/melt/ponds and the ocean heat/fresh/salt fluxes), Dynamics (./cice_dynamics.esm, the EVP momentum balance and stress relaxation of step_dyn_horiz), Transport (./cice_transport.esm, the per-category conservative advection of the area/volume/enthalpy/Tsfc states as a centered B-grid flux divergence -- the continuous flux form of the conservation law CICE integrates with incremental remapping, not the remap scheme itself), and the inline Control model, which is the ice_step orchestration (CICE_RunMod.F90:109-369 via ice_step_mod.F90) written as algebraic rate rules over one coupling period: the subcycling dt_dyn = dt/ndtd of the dynamics loop (CICE_RunMod.F90:271-281, ice_calendar dt_dyn), and the atmosphere boundary layer of the constant scheme (atmo_boundary_const, icepack_atmo.F90:398-496): wind = sqrt(uatm^2 + vatm^2) (prepare_forcing, ice_forcing.F90:1796), tau = rhoa*0.0012*wind with the components strairx = tau*uatm, strairy = tau*vatm (F90:460-464), shcoef = senscoef*cp_air*rhoa*wind (F90:493) and lhcoef = latncoef*Lsub*rhoa*wind (F90:494, Lheat = Lsub for ice F90:472-476). The coupling array wires the data flow with variable_map param_to_var entries in the ice_step order: the cap state fields (potT, Qa, rhoa, the four shortwave bands, flw, sst, sss, frzmlt, frain, fsnow, uocn, vocn, ss_tltx, ss_tlty) into Thermodynamics and Dynamics; the transport-owned mass states aicen/vicen/vsnon into Thermodynamics, Dynamics, and the cap aggregation; (the thermodynamics -> transport enthalpy hand-off, state_to_tracers, is an operator-splitting step the single-period assembly does not wire: Transport carries its own enthalpy-product states vqicen/vsqsnon); the dynamics-owned velocity uvel/vvel into Transport and the full ocean stress taux/tauy into the cap's Fioi_taux/tauy sign flip and the thermodynamics' ustar; and the per-category thermodynamics fluxes and albedos into the cap's export aggregation. Deferred to stage 3 (documented in the subcomponent descriptions and README.md): the Tsfc implicit surface-energy-balance solve (carried as a free parameter), the incremental-remap discretization of the transport PDEs (the lowered transport is a centered flux divergence without CICE's positivity/monotonicity guarantees), the ridge redistribution (the kstrength = 1 Rothrock strength itself is evaluated in Dynamics) and the kdyn/ktherm alternates, the similarity atmbndy scheme, the per-band Fioi_swpen_* fields, and the wave/aerosol/isotope exports. The shape-mismatched variable_map edges (3x5 dynamics/transport to the single-cell Thermodynamics/IceCap) carry faq full-map broadcast and single-cell select transforms (index of the traced cell (2,2) = global (3,5) inside a faq over ncat; the native compiler requires the full-rank index form), and the tests block pins the coupled assembly at the step-1 export-time state (17 assertions: the export-state chain through the coupling, the constant-scheme Control chain, and the broadcast ocean/tilt stress). The whole-coupling-period trace over [0, 3600] from the cold start remains a stage-3 concern. See README.md 'Testing'. Reference: stage1/cesm/components/cice/src/cicecore/drivers/nuopc/cmeps/."
tags: ["cryosphere", "cice", "model", "sea-ice", "cesm", "assembly", "coupling"]
---

## Description

CICE sea-ice top-level component (stage 2 of the EqESM project): the cesm3_cice6_6_3_22 ice component as an esm 2.0.0 assembly, per the stage1/boundaries.md 1.3 boundary table. Five systems: IceCap (mounted from ./cice_coupling.esm, the med<->ice cap renames, the med2mod/mod2med areacor scaling, and the merge_fluxes export aggregation of ice_import_export.F90), Thermodynamics (./cice_thermodynamics.esm, the BL99 column physics: prep_radiation shortwave/albedo, step_therm1 vertical conduction and surface energy balance, step_therm2 growth/melt/ponds and the ocean heat/fresh/salt fluxes), Dynamics (./cice_dynamics.esm, the EVP momentum balance and stress relaxation of step_dyn_horiz), Transport (./cice_transport.esm, the per-category conservative advection of the area/volume/enthalpy/Tsfc states as a centered B-grid flux divergence -- the continuous flux form of the conservation law CICE integrates with incremental remapping, not the remap scheme itself), and the inline Control model, which is the ice_step orchestration (CICE_RunMod.F90:109-369 via ice_step_mod.F90) written as algebraic rate rules over one coupling period: the subcycling dt_dyn = dt/ndtd of the dynamics loop (CICE_RunMod.F90:271-281, ice_calendar dt_dyn), and the atmosphere boundary layer of the constant scheme (atmo_boundary_const, icepack_atmo.F90:398-496): wind = sqrt(uatm^2 + vatm^2) (prepare_forcing, ice_forcing.F90:1796), tau = rhoa*0.0012*wind with the components strairx = tau*uatm, strairy = tau*vatm (F90:460-464), shcoef = senscoef*cp_air*rhoa*wind (F90:493) and lhcoef = latncoef*Lsub*rhoa*wind (F90:494, Lheat = Lsub for ice F90:472-476). The coupling array wires the data flow with variable_map param_to_var entries in the ice_step order: the cap state fields (potT, Qa, rhoa, the four shortwave bands, flw, sst, sss, frzmlt, frain, fsnow, uocn, vocn, ss_tltx, ss_tlty) into Thermodynamics and Dynamics; the transport-owned mass states aicen/vicen/vsnon into Thermodynamics, Dynamics, and the cap aggregation; (the thermodynamics -> transport enthalpy hand-off, state_to_tracers, is an operator-splitting step the single-period assembly does not wire: Transport carries its own enthalpy-product states vqicen/vsqsnon); the dynamics-owned velocity uvel/vvel into Transport and the full ocean stress taux/tauy into the cap's Fioi_taux/tauy sign flip and the thermodynamics' ustar; and the per-category thermodynamics fluxes and albedos into the cap's export aggregation. Deferred to stage 3 (documented in the subcomponent descriptions and README.md): the Tsfc implicit surface-energy-balance solve (carried as a free parameter), the incremental-remap discretization of the transport PDEs (the lowered transport is a centered flux divergence without CICE's positivity/monotonicity guarantees), the ridge redistribution (the kstrength = 1 Rothrock strength itself is evaluated in Dynamics) and the kdyn/ktherm alternates, the similarity atmbndy scheme, the per-band Fioi_swpen_* fields, and the wave/aerosol/isotope exports. The shape-mismatched variable_map edges (3x5 dynamics/transport to the single-cell Thermodynamics/IceCap) carry faq full-map broadcast and single-cell select transforms (index of the traced cell (2,2) = global (3,5) inside a faq over ncat; the native compiler requires the full-rank index form), and the tests block pins the coupled assembly at the step-1 export-time state (17 assertions: the export-state chain through the coupling, the constant-scheme Control chain, and the broadcast ocean/tilt stress). The whole-coupling-period trace over [0, 3600] from the cold start remains a stage-3 concern. See README.md 'Testing'. Reference: stage1/cesm/components/cice/src/cicecore/drivers/nuopc/cmeps/.

## Reference

- Hunke, E. C., Allard, R., Bailey, D. A., Blain, P., Craig, A., Dupont, F., ... & Roberts, A. F. (2023). CICE-Consortium Icepack v1.2.4 and CICE v6.3.22: documentation and user's guide. Los Alamos National Laboratory (LA-UR-23-31851).
- CESM (Community Earth System Model), ESCOMP/CESM: CICE sea-ice source (cesm3_cice6_6_3_22) - CICE_RunMod.F90, ice_step_mod.F90, ice_forcing.F90, icepack_atmo.F90 - the reference implementation these components are transcribed from.
- EarthSciModels - the authoritative .esm corpus this component lives in.

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `dt` | `s` | `3600.0` | coupling/thermodynamics timestep (namelist dt = 3600 s; the step_therm1/2 column physics runs once per step), [s] |
| `ndtd` | `1` | `1.0` | number of dynamics subcycles per step (namelist ndtd = 1), [-] |
| `uatm` | `m/s` | `0.0` | x wind velocity at zlvl (wired from the cap import Sa_u), [m/s] |
| `vatm` | `m/s` | `0.0` | y wind velocity at zlvl (wired from the cap import Sa_v), [m/s] |
| `rhoa` | `kg/m^3` | `1.2` | air density (wired from the cap import Sa_dens or the Sa_pbot branch), [kg/m3] |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `dt_dyn` | `s` |  | dynamics timestep of the ndtd subcycle loop: dt_dyn = dt/ndtd (ice_calendar dt_dyn, passed to step_dyn_horiz, CICE_RunMod.F90:271-281), [s] |
| `wind` | `m/s` |  | wind speed at the lowest model level: wind = sqrt(uatm^2 + vatm^2) (prepare_forcing, ice_forcing.F90:1796, 1819), [m/s] |
| `tau` | `N/m^2` |  | atmosphere-ice momentum stress magnitude of the constant boundary-layer scheme: tau = rhoa*0.0012*wind (atmo_boundary_const, icepack_atmo.F90:460), [N/m2] |
| `strairx` | `kg/s^3` |  | x air-ice stress at T points: strairx = tau*uatm (atmo_boundary_const, icepack_atmo.F90:463; the per-category strairxn of step_therm1 is identical across categories - no Tsfc dependence - so the merge_fluxes aggregation of icepack_flux.F90:187-189 collapses to this single value). The Fortran omits the /wind direction-cosine normalization (the vmag division is commented out, F90:328-329), so the transcription carries the dimension kg/s^3 of the active code; the quirk is logged in README.md, [kg/s3] |
| `strairy` | `kg/s^3` |  | y air-ice stress at T points: strairy = tau*vatm (F90:464; see strairx for the missing /wind normalization), [kg/s3] |
| `shcoef` | `W/m^2/K` |  | sensible-heat transfer coefficient: shcoef = senscoef*cp_air*rhoa*wind (atmo_boundary_const, icepack_atmo.F90:493; senscoef = 0.0012, cp_air = 1005), [W/m2/K] |
| `lhcoef` | `W/m^2` |  | latent-heat transfer coefficient: lhcoef = latncoef*Lsub*rhoa*wind (atmo_boundary_const, icepack_atmo.F90:494 with Lheat = Lsub = 2.8347e6 for ice -- the nuopc-cap value, ice_comp_nuopc.F90:415-450, bugs.md #11 -- vs 2.835e6, F90:472-476; latncoef = 0.0015), [W/m2] |

## Observed expressions

$$
dt_{dyn} = \frac{dt}{ndtd}
$$
_dynamics timestep of the ndtd subcycle loop: dt_dyn = dt/ndtd (ice_calendar dt_dyn, passed to step_dyn_horiz, CICE_RunMod.F90:271-281), [s]_

$$
wind = \sqrt{uatm^{2} + vatm^{2}}
$$
_wind speed at the lowest model level: wind = sqrt(uatm^2 + vatm^2) (prepare_forcing, ice_forcing.F90:1796, 1819), [m/s]_

$$
tau = \mathrm{atmo_constant_tau}\left(rhoa=rhoa, wind=wind\right)
$$
_atmosphere-ice momentum stress magnitude of the constant boundary-layer scheme: tau = rhoa*0.0012*wind (atmo_boundary_const, icepack_atmo.F90:460), [N/m2]_

$$
strairx = tau \cdot uatm
$$
_x air-ice stress at T points: strairx = tau*uatm (atmo_boundary_const, icepack_atmo.F90:463; the per-category strairxn of step_therm1 is identical across categories - no Tsfc dependence - so the merge_fluxes aggregation of icepack_flux.F90:187-189 collapses to this single value). The Fortran omits the /wind direction-cosine normalization (the vmag division is commented out, F90:328-329), so the transcription carries the dimension kg/s^3 of the active code; the quirk is logged in README.md, [kg/s3]_

$$
strairy = tau \cdot vatm
$$
_y air-ice stress at T points: strairy = tau*vatm (F90:464; see strairx for the missing /wind normalization), [kg/s3]_

$$
shcoef = \mathrm{atmo_constant_shcoef}\left(rhoa=rhoa, wind=wind\right)
$$
_sensible-heat transfer coefficient: shcoef = senscoef*cp_air*rhoa*wind (atmo_boundary_const, icepack_atmo.F90:493; senscoef = 0.0012, cp_air = 1005), [W/m2/K]_

$$
lhcoef = \mathrm{atmo_constant_lhcoef}\left(rhoa=rhoa, wind=wind, Lheat=\mathrm{const}\left(\right)\right)
$$
_latent-heat transfer coefficient: lhcoef = latncoef*Lsub*rhoa*wind (atmo_boundary_const, icepack_atmo.F90:494 with Lheat = Lsub = 2.8347e6 for ice -- the nuopc-cap value, ice_comp_nuopc.F90:415-450, bugs.md #11 -- vs 2.835e6, F90:472-476; latncoef = 0.0015), [W/m2]_

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "expression_template_imports": [
    {
      "ref": "./cice_templates.esm"
    }
  ],
  "variables": {
    "dt_dyn": {
      "type": "unknown",
      "units": "s",
      "description": "dynamics timestep of the ndtd subcycle loop: dt_dyn = dt/ndtd (ice_calendar dt_dyn, passed to step_dyn_horiz, CICE_RunMod.F90:271-281), [s]"
    },
    "wind": {
      "type": "unknown",
      "units": "m/s",
      "description": "wind speed at the lowest model level: wind = sqrt(uatm^2 + vatm^2) (prepare_forcing, ice_forcing.F90:1796, 1819), [m/s]"
    },
    "tau": {
      "type": "unknown",
      "units": "N/m^2",
      "description": "atmosphere-ice momentum stress magnitude of the constant boundary-layer scheme: tau = rhoa*0.0012*wind (atmo_boundary_const, icepack_atmo.F90:460), [N/m2]"
    },
    "strairx": {
      "type": "unknown",
      "units": "kg/s^3",
      "description": "x air-ice stress at T points: strairx = tau*uatm (atmo_boundary_const, icepack_atmo.F90:463; the per-category strairxn of step_therm1 is identical across categories - no Tsfc dependence - so the merge_fluxes aggregation of icepack_flux.F90:187-189 collapses to this single value). The Fortran omits the /wind direction-cosine normalization (the vmag division is commented out, F90:328-329), so the transcription carries the dimension kg/s^3 of the active code; the quirk is logged in README.md, [kg/s3]"
    },
    "strairy": {
      "type": "unknown",
      "units": "kg/s^3",
      "description": "y air-ice stress at T points: strairy = tau*vatm (F90:464; see strairx for the missing /wind normalization), [kg/s3]"
    },
    "shcoef": {
      "type": "unknown",
      "units": "W/m^2/K",
      "description": "sensible-heat transfer coefficient: shcoef = senscoef*cp_air*rhoa*wind (atmo_boundary_const, icepack_atmo.F90:493; senscoef = 0.0012, cp_air = 1005), [W/m2/K]"
    },
    "lhcoef": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "latent-heat transfer coefficient: lhcoef = latncoef*Lsub*rhoa*wind (atmo_boundary_const, icepack_atmo.F90:494 with Lheat = Lsub = 2.8347e6 for ice -- the nuopc-cap value, ice_comp_nuopc.F90:415-450, bugs.md #11 -- vs 2.835e6, F90:472-476; latncoef = 0.0015), [W/m2]"
    },
    "dt": {
      "type": "parameter",
      "units": "s",
      "default": 3600.0,
      "description": "coupling/thermodynamics timestep (namelist dt = 3600 s; the step_therm1/2 column physics runs once per step), [s]"
    },
    "ndtd": {
      "type": "parameter",
      "units": "1",
      "default": 1.0,
      "description": "number of dynamics subcycles per step (namelist ndtd = 1), [-]"
    },
    "uatm": {
      "type": "parameter",
      "units": "m/s",
      "default": 0.0,
      "description": "x wind velocity at zlvl (wired from the cap import Sa_u), [m/s]"
    },
    "vatm": {
      "type": "parameter",
      "units": "m/s",
      "default": 0.0,
      "description": "y wind velocity at zlvl (wired from the cap import Sa_v), [m/s]"
    },
    "rhoa": {
      "type": "parameter",
      "units": "kg/m^3",
      "default": 1.2,
      "description": "air density (wired from the cap import Sa_dens or the Sa_pbot branch), [kg/m3]"
    }
  },
  "equations": [
    {
      "lhs": "dt_dyn",
      "rhs": {
        "op": "/",
        "args": [
          "dt",
          "ndtd"
        ]
      }
    },
    {
      "lhs": "wind",
      "rhs": {
        "op": "sqrt",
        "args": [
          {
            "op": "+",
            "args": [
              {
                "op": "^",
                "args": [
                  "uatm",
                  2
                ]
              },
              {
                "op": "^",
                "args": [
                  "vatm",
                  2
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "tau",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "atmo_constant_tau",
        "bindings": {
          "rhoa": "rhoa",
          "wind": "wind"
        }
      }
    },
    {
      "lhs": "strairx",
      "rhs": {
        "op": "*",
        "args": [
          "tau",
          "uatm"
        ]
      }
    },
    {
      "lhs": "strairy",
      "rhs": {
        "op": "*",
        "args": [
          "tau",
          "vatm"
        ]
      }
    },
    {
      "lhs": "shcoef",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "atmo_constant_shcoef",
        "bindings": {
          "rhoa": "rhoa",
          "wind": "wind"
        }
      }
    },
    {
      "lhs": "lhcoef",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "atmo_constant_lhcoef",
        "bindings": {
          "rhoa": "rhoa",
          "wind": "wind",
          "Lheat": {
            "op": "const",
            "args": [],
            "value": 2834700.0,
            "units": "J/kg"
          }
        }
      }
    }
  ],
  "tests": [
    {
      "id": "assembly_exports_dynamics_step1_cell3_5",
      "description": "Instantaneous assembly pins of the step-1 export-time state (the end of the first coupling period; the run's step-1 exports aggregate the entry(2) state to round-off, so the export pins are exact): the traced cell local (2,2) = global (3,5). Initial conditions: Transport aicen/vicen/vsnon = the post-step-1 advected field, cice_thermo_state.csv step-2 entry rows at the 15 cells; Dynamics uvel/vvel = the export-time velocity field, cice_transport_state.csv step-1 t_entr uvel/vvel at the 15 U points (the advection uses the post-dynamics velocity; the U(4,4) = (0,0) convention cell local (3,1) is zero in the dump); Thermodynamics qicen/qsnon = the step-2 entry column state at (3,5). Parameter overrides: Thermodynamics Tsfc = the entry(2) Tsfc tracer (the surface temperature the Si_t export aggregates; the converged-solve Tsfcn is a different quantity, 0.7 K warmer, so the flux exports are not pinned here), albedos = the step-1 cice_albedo.csv rows at (3,5) (export-time albedos); the B-grid geometry dxT/dyT/cxp/cyp/cxm/cym/dxhy/dyhx (cice_evp_stress.csv step-2 ksub1 corner-1 rows) with HTE/HTN = (3cyp-cym)/4, (3cxp-cxm)/4 and the momentum-dump aiX/uarear (cice_evp_momentum.csv step-2 ksub1; U(4,4) missing from the dump, zeroed by the (0,0) convention); IceCap raw CMEPS fields = the step-1 (3,5) cice_run_imports.csv values inverted through the import equations (Sa_u = uatm, Sa_v = vatm, Sa_dens = rhoa, So_u = uocn, So_v = vocn, So_dhdx = ss_tltx, So_dhdy = ss_tlty) with med2mod_areacor = the row's areacor and mod2med_areacor = 1/areacor (the step-1 (3,5) export rows carry the inverse). Pins against cice_run_exports.csv step-1 (3,5): the export chain through the coupling (Transport->Thermodynamics/IceCap single-cell selects and the Thermodynamics->IceCap Tsfc/albedo edges) Si_ifrac/Si_vice/Si_vsno/Si_snowh/Si_t and the albedo aggregation Si_avsdr/Si_anidr/Si_avsdf/Si_anidf. Formulation pins (transcribed from the same inputs; no dump column is directly comparable): Faii_taux/Faii_tauy = strairxT/aice*areacor with the constant-scheme Control chain strairx = tau*uatm, tau = rhoa*0.0012*wind (icepack_atmo.F90:460-461; the run's similarity-scheme export differs, a stage-3 concern); the ocean-ice stress Dynamics.taux/tauy at U(1,1) and U(2,2) (the traced cell's NE corner), vrel = aiX*rhow*Cw*sqrt((uocn-uvel)^2+(vocn-vvel)^2) with rhow = 1026, Cw = 0.00536 and the broadcast step-1 (3,5) uocn/vocn; and the tilt stress strtltx/strtlty at T(2,2) as wiring pins of the ss_tltx/ss_tlty broadcast (the traced-cell So_dhdx/So_dhdy imports are identically zero in this run).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 0.0
      },
      "parameter_overrides": {
        "Thermodynamics.Tsfc": [
          -3.992162719228986,
          -3.992162719228986,
          -3.992162719228986,
          -3.992162719228986,
          -3.992162719228986
        ],
        "Thermodynamics.alvdrn": [
          0.8012425142819971,
          0.9746582279641268,
          0.9760305748565534,
          0.9765002562339028,
          0.9765440798804994
        ],
        "Thermodynamics.alidrn": [
          0.6223107683813334,
          0.6767922519895798,
          0.6767903895434615,
          0.6767902342356835,
          0.6767902682755257
        ],
        "Thermodynamics.alvdfn": [
          0.7031456254426053,
          0.9613931086200608,
          0.9634970346676461,
          0.9642170957905419,
          0.9642842813645289
        ],
        "Thermodynamics.alidfn": [
          0.5105101748076409,
          0.5888751644670052,
          0.5888722846514182,
          0.5888720442041272,
          0.588872096889385
        ],
        "Dynamics.aiX": [
          [
            0.8864372661049056,
            0.7919662066536575,
            0.8077055334869097,
            0.8159818452074996,
            0.8182679973964321
          ],
          [
            0.8846778445343791,
            0.7923124136324644,
            0.8038357038651518,
            0.8007595526771868,
            0.8023657323503273
          ],
          [
            0.0,
            0.7950656699846108,
            0.7941886908765261,
            0.7807671380302491,
            0.7826019104024559
          ]
        ],
        "Dynamics.uarear": [
          [
            6.413528696759567e-10,
            6.146806591704998e-10,
            5.901875919798776e-10,
            5.676191263820463e-10,
            5.467588875253487e-10
          ],
          [
            6.413528696759567e-10,
            6.146806591704998e-10,
            5.901875919798776e-10,
            5.676191263820463e-10,
            5.467588875253487e-10
          ],
          [
            0.0,
            6.146806591704998e-10,
            5.901875919798776e-10,
            5.676191263820463e-10,
            5.467588875253487e-10
          ]
        ],
        "Dynamics.dxT": [
          [
            25680.547570607527,
            26820.781783958108,
            27958.68417287352,
            29094.15580703113,
            30227.097967440433
          ],
          [
            25680.547570607527,
            26820.781783958108,
            27958.68417287352,
            29094.15580703113,
            30227.097967440433
          ],
          [
            25680.547570607527,
            26820.781783958108,
            27958.68417287352,
            29094.15580703113,
            30227.097967440433
          ]
        ],
        "Dynamics.dyT": [
          [
            59395.45501642161,
            59395.45501642161,
            59395.45501642161,
            59395.45501642161,
            59395.45501642161
          ],
          [
            59395.45501642161,
            59395.45501642161,
            59395.45501642161,
            59395.45501642161,
            59395.45501642161
          ],
          [
            59395.45501642161,
            59395.45501642161,
            59395.45501642161,
            59395.45501642161,
            59395.45501642161
          ]
        ],
        "Dynamics.cxp": [
          [
            26821.922937715524,
            27959.874843551268,
            29095.39589111118,
            30228.38735710868,
            31358.750738181487
          ],
          [
            26821.922937715524,
            27959.874843551268,
            29095.39589111118,
            30228.38735710868,
            31358.750738181487
          ],
          [
            26821.922937715524,
            27959.874843551268,
            29095.39589111118,
            30228.38735710868,
            31358.750738181487
          ]
        ],
        "Dynamics.cyp": [
          [
            59395.455016421605,
            59395.455016421605,
            59395.455016421605,
            59395.455016421605,
            59395.455016421605
          ],
          [
            59395.455016421605,
            59395.455016421605,
            59395.455016421605,
            59395.455016421605,
            59395.455016421605
          ],
          [
            59395.455016421605,
            59395.455016421605,
            59395.455016421605,
            59395.455016421605,
            59395.455016421605
          ]
        ],
        "Dynamics.cxm": [
          [
            -24539.172203499533,
            -25681.688724364943,
            -26821.972454635856,
            -27959.92425695357,
            -29095.445196699373
          ],
          [
            -24539.172203499533,
            -25681.688724364943,
            -26821.972454635856,
            -27959.92425695357,
            -29095.445196699373
          ],
          [
            -24539.172203499533,
            -25681.688724364943,
            -26821.972454635856,
            -27959.92425695357,
            -29095.445196699373
          ]
        ],
        "Dynamics.cym": [
          [
            -59395.455016421605,
            -59395.455016421605,
            -59395.455016421605,
            -59395.455016421605,
            -59395.455016421605
          ],
          [
            -59395.455016421605,
            -59395.455016421605,
            -59395.455016421605,
            -59395.455016421605,
            -59395.455016421605
          ],
          [
            -59395.455016421605,
            -59395.455016421605,
            -59395.455016421605,
            -59395.455016421605,
            -59395.455016421605
          ]
        ],
        "Dynamics.dxhy": [
          [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0
          ],
          [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0
          ],
          [
            0.0,
            0.0,
            0.0,
            0.0,
            0.0
          ]
        ],
        "Dynamics.dyhx": [
          [
            570.6876835539988,
            569.546529796582,
            568.3558591188303,
            567.1157750387774,
            565.8263853705284
          ],
          [
            570.6876835539988,
            569.546529796582,
            568.3558591188303,
            567.1157750387774,
            565.8263853705284
          ],
          [
            570.6876835539988,
            569.546529796582,
            568.3558591188303,
            567.1157750387774,
            565.8263853705284
          ]
        ],
        "Dynamics.HTE": [
          [
            59395.455016421605,
            59395.455016421605,
            59395.455016421605,
            59395.455016421605,
            59395.455016421605
          ],
          [
            59395.455016421605,
            59395.455016421605,
            59395.455016421605,
            59395.455016421605,
            59395.455016421605
          ],
          [
            59395.455016421605,
            59395.455016421605,
            59395.455016421605,
            59395.455016421605,
            59395.455016421605
          ]
        ],
        "Dynamics.HTN": [
          [
            26251.235254161526,
            27390.328313754686,
            28527.04003199235,
            29661.271582069905,
            30792.92435281096
          ],
          [
            26251.235254161526,
            27390.328313754686,
            28527.04003199235,
            29661.271582069905,
            30792.92435281096
          ],
          [
            26251.235254161526,
            27390.328313754686,
            28527.04003199235,
            29661.271582069905,
            30792.92435281096
          ]
        ],
        "IceCap.Sa_u": 0.16233199134639076,
        "IceCap.Sa_v": 1.7327887040729173,
        "IceCap.Sa_dens": 1.2698312342884206,
        "IceCap.So_u": 7.407083176076412e-05,
        "IceCap.So_v": -0.0018844332390775284,
        "IceCap.So_dhdx": 0.0,
        "IceCap.So_dhdy": 0.0,
        "IceCap.med2mod_areacor": 1.0003304865245655,
        "IceCap.mod2med_areacor": 0.9996696226606931
      },
      "initial_conditions": {
        "Transport.aicen": [
          [
            [
              0.009852850608356705,
              0.012855529713203084,
              0.02967522239569254,
              0.16810878906591015,
              0.7737677729487741
            ],
            [
              0.19517072496325305,
              0.1751699959445424,
              0.20299608331332739,
              0.0925064216149051,
              0.1216558550800837
            ],
            [
              0.2400766653663879,
              0.2634254615164032,
              0.17909871909393293,
              0.06249002808294717,
              0.05508345318458766
            ],
            [
              0.2426919186506009,
              0.3004531702096642,
              0.16427604885302102,
              0.05917420533990415,
              0.05122228568500235
            ],
            [
              0.21451075412464132,
              0.3379989394191858,
              0.16112464237950028,
              0.06074169961893066,
              0.05272389186144788
            ]
          ],
          [
            [
              0.019998693835139206,
              0.018689741990952156,
              0.021232919112523535,
              0.2325707828522124,
              0.7062446404306936
            ],
            [
              0.19509920997698144,
              0.19102973190363176,
              0.19874352490657504,
              0.08527745905757382,
              0.10446119777225216
            ],
            [
              0.2665298255694812,
              0.2729006570477799,
              0.16778864231529517,
              0.05189257221180012,
              0.04558044632846786
            ],
            [
              0.27103888359345235,
              0.30545283008105073,
              0.14120833461467586,
              0.049371543416734685,
              0.04065491374870835
            ],
            [
              0.2505253846079861,
              0.3313992567197806,
              0.1347485950838977,
              0.051994107144722954,
              0.042375364226296966
            ]
          ],
          [
            [
              0.014546987533488643,
              0.01437960674157303,
              0.02220442303290164,
              0.1984641673481961,
              0.7493161481210983
            ],
            [
              0.19333932043753435,
              0.21621557270682965,
              0.20867510730854066,
              0.07229338771572755,
              0.08563417081152437
            ],
            [
              0.2936476965493385,
              0.27663678612600096,
              0.15417825363337812,
              0.04715026122523659,
              0.04079790528181482
            ],
            [
              0.29897249929682534,
              0.2972514558583821,
              0.11590817072822045,
              0.04343285529264439,
              0.035316375642820606
            ],
            [
              0.2969767469479995,
              0.3099130350920145,
              0.10536018111674159,
              0.04494354825801149,
              0.03608501290682929
            ]
          ]
        ],
        "Transport.vicen": [
          [
            [
              0.003367779812266007,
              0.01554109629578779,
              0.06637380864748238,
              0.5907909709038863,
              21.611477507853053
            ],
            [
              0.03491946025185333,
              0.18814639271223785,
              0.38033637662938874,
              0.3246554490612238,
              1.4503495281475627
            ],
            [
              0.043477700357756895,
              0.27346944321742317,
              0.31914578046197933,
              0.2170465257476389,
              0.4266181762050393
            ],
            [
              0.047425102701226636,
              0.3090959875522784,
              0.288350670979356,
              0.20467440652634913,
              0.38238750791847226
            ],
            [
              0.05151028998780184,
              0.34622448934561495,
              0.277254649932636,
              0.208908156368402,
              0.38682674902647435
            ]
          ],
          [
            [
              0.005397850213129078,
              0.023942140179348897,
              0.0399397078635164,
              0.9741575968869286,
              19.81721380475162
            ],
            [
              0.034088386566977734,
              0.20815767151363995,
              0.35599114941687404,
              0.3057965536376442,
              1.16761539928305
            ],
            [
              0.04903782434030179,
              0.2793888801133831,
              0.2937598042356065,
              0.1784789205962492,
              0.34514955458031565
            ],
            [
              0.05585454615812537,
              0.304542063396575,
              0.244903908142195,
              0.16873640672255447,
              0.29602051740744867
            ],
            [
              0.06560256128663951,
              0.32605815989667336,
              0.23101073278912002,
              0.1772147938588419,
              0.306575838211402
            ]
          ],
          [
            [
              0.0035009181434715966,
              0.01786339513832903,
              0.04490632324489385,
              0.72865381404801,
              18.890818548001892
            ],
            [
              0.03649328146221779,
              0.23308233517458105,
              0.36955180944062754,
              0.25386734439471803,
              0.8305763143679897
            ],
            [
              0.05634645838924221,
              0.27798653967298403,
              0.2676293029172479,
              0.16162479045002112,
              0.30798566757939755
            ],
            [
              0.06849435654093011,
              0.28666165091875834,
              0.20065034643770607,
              0.14761639927580525,
              0.25636991886702826
            ],
            [
              0.08542000309789063,
              0.29181575997788195,
              0.1820959899616643,
              0.15249234122882746,
              0.26033223338002337
            ]
          ]
        ],
        "Transport.vsnon": [
          [
            [
              0.0,
              0.0019751743022568325,
              0.02041996777347029,
              0.18230923273106475,
              3.4177127644477934
            ],
            [
              0.002558356414974736,
              0.04642576613403754,
              0.08453248286313512,
              0.053012962507745155,
              0.1605960490536185
            ],
            [
              0.00553598157465553,
              0.07728705324754334,
              0.06980509698675395,
              0.036068005322586666,
              0.05585367606992837
            ],
            [
              0.007353967025129856,
              0.09274582612967944,
              0.06849663028892658,
              0.03713058599776843,
              0.05309667884903127
            ],
            [
              0.014124431456488227,
              0.10679293196387488,
              0.07205204828275692,
              0.04204083889759989,
              0.05727704593061239
            ]
          ],
          [
            [
              0.0,
              0.002794718458647137,
              0.007228721893417195,
              0.28218578938214034,
              3.004742960880409
            ],
            [
              0.00214517760028279,
              0.05120298134744836,
              0.07438735896096987,
              0.04898132510697397,
              0.13861653386722464
            ],
            [
              0.006340468223430725,
              0.07946324998047163,
              0.06586036950499848,
              0.03021851368098695,
              0.045054634606847464
            ],
            [
              0.009785562302312392,
              0.09062862360583843,
              0.05974037355438814,
              0.031027370420451242,
              0.04116342782161753
            ],
            [
              0.018981912797212026,
              0.09717172432401758,
              0.060931163985563794,
              0.0354460377803012,
              0.04492604738499721
            ]
          ],
          [
            [
              0.0,
              0.002899236964468358,
              0.01394477152813959,
              0.2273555088341527,
              3.5161499945474426
            ],
            [
              0.003218285658443744,
              0.05975237736986469,
              0.08166282501213593,
              0.04051420325329327,
              0.10498356329369356
            ],
            [
              0.008165464538160408,
              0.07717990701755018,
              0.058871124493702284,
              0.027103019740494994,
              0.03940362547334395
            ],
            [
              0.013555664833365838,
              0.08037619308780151,
              0.048655868863786554,
              0.0265439737208536,
              0.03462717095865928
            ],
            [
              0.023912868305829872,
              0.07888423600446277,
              0.047916895060079664,
              0.02943443630689699,
              0.03689197610152237
            ]
          ]
        ],
        "Dynamics.uvel": [
          [
            0.00012200831259922484,
            -0.00430503734325033,
            -0.006404552971129575,
            -0.0029079564379971357,
            -0.0037366886985347827
          ],
          [
            1.349728123413932e-05,
            -0.0049893802525858445,
            -0.006556908183432414,
            -0.004013004944111566,
            -0.0042590499452267415
          ],
          [
            0.0,
            -0.006049027918925767,
            -0.0058923320164812176,
            -0.0045391275967812655,
            -0.004738980872614332
          ]
        ],
        "Dynamics.vvel": [
          [
            0.0007204892821085377,
            0.0007865942006418693,
            0.0037168927343423233,
            0.013900356415145056,
            0.015928611364519916
          ],
          [
            0.0009977387642852074,
            0.001620845665338858,
            0.00661497866621736,
            0.011651221033965178,
            0.012191539845748306
          ],
          [
            0.0,
            0.003975027437344815,
            0.009118244672511678,
            0.01094051866825294,
            0.010805999470988786
          ]
        ],
        "Thermodynamics.qicen": [
          [
            -299745570.55563176,
            -298729215.3734631,
            -297784537.8242855,
            -296521779.2307301,
            -293954215.2851075,
            -288569024.12406754,
            -271530709.23044425,
            -214338206.79563126
          ],
          [
            -295867814.07185423,
            -294956506.8840964,
            -294154293.11888206,
            -293620457.76648116,
            -293369020.0450227,
            -293092878.05803216,
            -292520167.6976286,
            -287034635.01228637
          ],
          [
            -295425634.7961048,
            -294492386.3103499,
            -294028871.87121654,
            -294084684.3971227,
            -294727808.3367829,
            -294579802.6180682,
            -293192497.59631324,
            -285742794.39152205
          ],
          [
            -295830121.1648516,
            -295500925.71526706,
            -295407817.6053068,
            -295303574.99141634,
            -295544496.66183215,
            -297469692.4776547,
            -298744465.534943,
            -291872746.99332786
          ],
          [
            -297451926.7221619,
            -285340619.3968445,
            -269645718.1760381,
            -257487554.7701041,
            -248400334.46339342,
            -237951452.21243778,
            -209380141.79298782,
            -173195697.94371974
          ]
        ],
        "Thermodynamics.qsnon": [
          [
            -112391836.04929295,
            -112318823.05957381,
            -112264688.14831108
          ],
          [
            -115022655.1186357,
            -113892544.09169255,
            -112966462.42543253
          ],
          [
            -115152261.60677192,
            -114192712.78580083,
            -113370140.06140642
          ],
          [
            -115367131.97608271,
            -114831240.84226657,
            -114056410.92514798
          ],
          [
            -114830251.97507223,
            -114248384.96547455,
            -113796535.70086242
          ]
        ]
      },
      "assertions": [
        {
          "variable": "IceCap.Si_ifrac",
          "time": 0.0,
          "expected": 0.7746111236170142
        },
        {
          "variable": "IceCap.Si_vice",
          "time": 0.0,
          "expected": 2.071649160418186
        },
        {
          "variable": "IceCap.Si_vsno",
          "time": 0.0,
          "expected": 0.31533337688289964
        },
        {
          "variable": "IceCap.Si_snowh",
          "time": 0.0,
          "expected": 0.40708604262028103
        },
        {
          "variable": "IceCap.Si_t",
          "time": 0.0,
          "expected": 269.157837280771
        },
        {
          "variable": "IceCap.Si_avsdr",
          "time": 0.0,
          "expected": 0.9317896958382746
        },
        {
          "variable": "IceCap.Si_anidr",
          "time": 0.0,
          "expected": 0.6630691804696613
        },
        {
          "variable": "IceCap.Si_avsdf",
          "time": 0.0,
          "expected": 0.8975896091057705
        },
        {
          "variable": "IceCap.Si_anidf",
          "time": 0.0,
          "expected": 0.5691360902633934
        },
        {
          "variable": "IceCap.Faii_taux",
          "time": 0.0,
          "expected": 0.0005555807645563837
        },
        {
          "variable": "IceCap.Faii_tauy",
          "time": 0.0,
          "expected": 0.005930464260548856
        },
        {
          "variable": "Dynamics.taux",
          "time": 0.0,
          "expected": -6.088407333962123e-07,
          "coords": {
            "i": 1,
            "j": 1
          }
        },
        {
          "variable": "Dynamics.tauy",
          "time": 0.0,
          "expected": -3.30844030704005e-05,
          "coords": {
            "i": 1,
            "j": 1
          }
        },
        {
          "variable": "Dynamics.taux",
          "time": 0.0,
          "expected": 0.00013586918958307404,
          "coords": {
            "i": 2,
            "j": 2
          }
        },
        {
          "variable": "Dynamics.tauy",
          "time": 0.0,
          "expected": -9.405826106981281e-05,
          "coords": {
            "i": 2,
            "j": 2
          }
        },
        {
          "variable": "Dynamics.strtltx",
          "time": 0.0,
          "expected": 0.0,
          "coords": {
            "i": 2,
            "j": 2
          }
        },
        {
          "variable": "Dynamics.strtlty",
          "time": 0.0,
          "expected": 0.0,
          "coords": {
            "i": 2,
            "j": 2
          }
        }
      ]
    }
  ]
}
```

</details>
