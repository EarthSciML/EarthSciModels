# EarthSciModels Migration Tracker

Inventory of MTK-based components across 14 earthsciml repositories, classified by
schema-gap blockers. This manifest drives per-component Phase-2 migration beads.

- **Inventory date:** 2026-04-19
- **Audit reference:** `EarthSciSerialization/mayor/rig/docs/audits/mtk-gap-audit-2026-04-19.md`
- **Source bead:** `mdl-pws` (Phase 0)

## Pinned commit SHAs

| Repo | SHA |
|---|---|
| Aerosol.jl | `c8c640bb636b22f2425460e9ed5cba50793bfee1` |
| AtmosphericDeposition.jl | `e4468c79c8dd4aae88646cd16d6bcf290874742c` |
| AtmosphericDynamics.jl | `816cc3918e1eef2c2ee6d8fa8dd73c8f13a85a47` |
| EarthSciData.jl | `830435a065f27e99f10bba91107ca1730322cc6b` |
| EarthSciDiscretizations.jl | `e3dae642e990a3414991154bcf63bfebae654c34` |
| EarthSciMLBase.jl | `d5e7c71e3f7c09626171030985f6bff0fa1047ff` |
| Emissions.jl | `85a6ac2573035c8a0993ab580462491db59e3178` |
| EnvironmentalTransport.jl | `a48559c4114eb9f06668ecf9f06235aad20f63f0` |
| GasChem.jl | `8c12c048482b515fb8eb2110bf8ab4b4f4e71309` |
| Geodynamics.jl | `d680af419676cc576d60b16af0d3dd40c0b23eea` |
| OceanDynamics.jl | `6fdcc74222e137565d5d19dfcced6dc3013108d2` |
| UrbanCanopy.jl | `9200edd4f15609f20339d3a7d104de8064544310` |
| Vegetation.jl | `010c3774dc5646d81806c6119c8a029a70f6c9a0` |
| WildlandFire.jl | `126976f2508ceacca6c486b21ae6da5b168c6f46` |

## Summary: counts by blocking-gap bucket

| Bucket | Components | Notes |
|---|---:|---|
| **Migrate today** (`none`) | **215** | Clean ODE/algebraic `@component` models. No schema gaps. |
| Blocked on `gt-p3ep` (lookup / @register_symbolic) | 26 | AtmDep lookup tables, GasChem Fast-JX, EarthSciData interpolators, WildlandFire fuel tables, Aerosol ISORROPIA-II helpers |
| Blocked on `gt-kuxo` (brownian / SDE) | 2 | StagePrognosis (Vegetation), BoundaryLayerMixingKC (EnvTransport) |
| Blocked on `gt-ebuq` (init_eqs / system_kind for nonlinear/algebraic) | 5 | Mogi/McTigue (Geodynamics), Sofiev2012PlumeRise (EnvTransport), Isorropia (Aerosol), IsorropiaEquilibrium, StagePrognosisHCB |
| Blocked on `gt-vzwk` (PDE-tests) | 7 | LevelSetFireSpread (WildlandFire), SurfaceRunoff (EnvTransport), plus in-component discretized PDE helpers in UrbanCanopy (roof/wall/hydrology) |
| Blocked on `gt-6ohw` (DataInterpolations.derivative) | 2 | ERA5, GEOSFP register get_unit for DataInterpolations.derivative |
| `other:P3-A-metric-tensor-coord-transforms` | 3 | WildlandFire level-set uses `partialderivative_transforms`; EarthSciDiscretizations metric tensors |
| `other:P3-B-BC-symbolic-offset` | 1 | Puff lateral stop references `grid_spacing * buffer_cells` in BC |
| `other:P2-C-terminate-in-FunctionalAffect` | 1 | Puff uses `terminate!(integrator)` in a closure |
| `other:discretization-plan` | ~1 per PDE | MOLFiniteDifference discretization plan not in ESM Domain; tracked by `gt-dq0f` (v2.1) |
| `other:framework-only` | — | EarthSciMLBase.jl, EarthSciDiscretizations.jl — framework primitives, not migratable as .esm files |
| `other:empty-no-mtk` | — | Emissions.jl (data-processing, non-MTK), OceanDynamics.jl (no `src/`) |

Total discovered MTK components: ~262 (excluding EarthSciMLBase framework primitives and EarthSciDiscretizations operator library).

**Notes on the numbers:**

- Framework repos (EarthSciMLBase, EarthSciDiscretizations) are listed for completeness but their contents are *schema enablers* (Operator, DomainInfo, param_to_var, MOLFiniteDifference, etc.) — they don't become `.esm` files; they make `.esm` files parseable/runnable. They gate P2+ migration of models that use them.
- Aerosol.jl ISORROPIA components individually compile into parameter/observed eqs, but the full `Isorropia`/`IsorropiaEquilibrium` top-level systems require `gt-ebuq` (init_eqs + system_kind=nonlinear) to solve. Sub-components (`Ion`, `Salt`, `Gas`, etc.) are marked `none` because they produce equation fragments only.
- Emissions.jl contains non-MTK data-processing modules (CSV, NetCDF, shapefile I/O). No MTK components discovered. Not a migration target for Phase 2.
- OceanDynamics.jl has no `src/` directory on the pinned commit. Not a migration target yet.

---

## 1. Aerosol.jl (116 components)

Repo purpose: aerosol microphysics, inorganic/organic aqueous chemistry, ISORROPIA equilibria, TOMAS size bins, radiative forcing.

### 1.1 aerosol_radiative_forcing.jl (6 components, all `none`)

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| AerosolLayerRadiativeForcing | `src/aerosol_radiative_forcing.jl:36` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/radiative_forcing/aerosol_layer.esm` | — |
| CriticalSingleScatteringAlbedo | `src/aerosol_radiative_forcing.jl:106` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/radiative_forcing/critical_ssa.esm` | — |
| CloudOpticalDepth | `src/aerosol_radiative_forcing.jl:154` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/radiative_forcing/cloud_optical_depth.esm` | — |
| CloudAlbedo | `src/aerosol_radiative_forcing.jl:205` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/radiative_forcing/cloud_albedo.esm` | — |
| CloudAlbedoSensitivity | `src/aerosol_radiative_forcing.jl:254` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/radiative_forcing/cloud_albedo_sensitivity.esm` | — |
| IndirectAerosolForcing | `src/aerosol_radiative_forcing.jl:306` | Model | variables, parameters, observed, coupling.couple | none | M | Y | Y | `components/aerosol/radiative_forcing/indirect_aerosol.esm` | CloudAlbedo, CriticalSingleScatteringAlbedo |

### 1.2 aqueous_equilibria.jl (9 components, all `none`)

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| WaterEquilibrium | `src/aqueous_equilibria.jl:76` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/aq_eq/water.esm` | — |
| CO2Equilibria | `src/aqueous_equilibria.jl:140` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/aq_eq/co2.esm` | — |
| SO2Equilibria | `src/aqueous_equilibria.jl:240` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/aq_eq/so2.esm` | — |
| NH3Equilibria | `src/aqueous_equilibria.jl:345` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/aq_eq/nh3.esm` | — |
| HNO3Equilibria | `src/aqueous_equilibria.jl:438` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/aq_eq/hno3.esm` | — |
| H2O2Equilibria | `src/aqueous_equilibria.jl:519` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/aq_eq/h2o2.esm` | — |
| O3Equilibria | `src/aqueous_equilibria.jl:589` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/aq_eq/o3.esm` | — |
| AqueousEquilibria | `src/aqueous_equilibria.jl:642` | Model | variables, parameters, observed, coupling.couple | none | L | Y | Y | `components/aerosol/aq_eq/all.esm` | WaterEquilibrium, CO2/SO2/NH3/HNO3/H2O2/O3 Equilibria |

### 1.3 aqueous_transport.jl (3 components, all `none`)

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| AqueousDiffusionReaction | `src/aqueous_transport.jl:14` | Model | variables, parameters, equations | none | S | Y | Y | `components/aerosol/transport/aqueous_diffusion_reaction.esm` | — |
| MassTransportLimitation | `src/aqueous_transport.jl:53` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/transport/mass_transport_limitation.esm` | — |
| DropletMassBalance | `src/aqueous_transport.jl:112` | Model | variables, parameters, equations | none | S | Y | Y | `components/aerosol/transport/droplet_mass_balance.esm` | — |

### 1.4 cloud_chemistry.jl (3), cloud_physics.jl (9)

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| CloudChemistry | `src/cloud_chemistry.jl:73` | Model | variables, parameters, equations, coupling.couple | none | L | Y | Y | `components/aerosol/cloud_chemistry/cloud_chemistry.esm` | AqueousEquilibria, SulfateFormation |
| CloudChemistryFixedpH | `src/cloud_chemistry.jl:269` | Model | variables, parameters, equations | none | M | Y | Y | `components/aerosol/cloud_chemistry/cloud_chemistry_fixed_ph.esm` | — |
| CloudChemistryODE | `src/cloud_chemistry.jl:422` | Model | variables, parameters, equations | none | M | Y | Y | `components/aerosol/cloud_chemistry/cloud_chemistry_ode.esm` | — |
| CloudWaterProperties | `src/cloud_physics.jl:15` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/cloud_physics/cloud_water_properties.esm` | — |
| CloudKelvinEffect | `src/cloud_physics.jl:181` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/cloud_physics/cloud_kelvin.esm` | — |
| KohlerTheory | `src/cloud_physics.jl:232` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/cloud_physics/kohler.esm` | — |
| DropletGrowth | `src/cloud_physics.jl:322` | Model | variables, parameters, equations | none | M | Y | Y | `components/aerosol/cloud_physics/droplet_growth.esm` | — | **status: complete, sha: c8c640bb636b22f2425460e9ed5cba50793bfee1** (mdl-43a; mtk2esm-scaffolded, round-trip passes, 7 tests / 38 assertions, 4 Köhler-style examples) |
| CloudDynamics | `src/cloud_physics.jl:455` | Model | variables, parameters, equations, coupling.couple | none | L | Y | Y | `components/aerosol/cloud_physics/cloud_dynamics.esm` | DropletGrowth, CloudKelvinEffect |
| IcePhysics | `src/cloud_physics.jl:525` | Model | variables, parameters, equations | none | M | Y | Y | `components/aerosol/cloud_physics/ice_physics.esm` | — |
| RainFormation | `src/cloud_physics.jl:604` | Model | variables, parameters, equations | none | M | Y | Y | `components/aerosol/cloud_physics/rain_formation.esm` | — |
| AerosolScavenging | `src/cloud_physics.jl:693` | Model | variables, parameters, equations | none | M | Y | Y | `components/aerosol/cloud_physics/aerosol_scavenging.esm` | — |
| CloudPhysics | `src/cloud_physics.jl:735` | Model | variables, parameters, coupling.couple | none | L | Y | Y | `components/aerosol/cloud_physics/cloud_physics.esm` | CloudDynamics, IcePhysics, RainFormation, AerosolScavenging |

### 1.5 dahneke_brownian_diffusion.jl (5), dynamics.jl (5)

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| DahnekeMassTransportCorrection | `src/dahneke_brownian_diffusion.jl:33` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/dahneke/mass_transport.esm` | — |
| DahnekeHeatTransportCorrection | `src/dahneke_brownian_diffusion.jl:93` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/dahneke/heat_transport.esm` | — |
| DahnekeCondensationEvaporation | `src/dahneke_brownian_diffusion.jl:157` | Model | variables, parameters, equations | none | M | Y | Y | `components/aerosol/dahneke/condensation_evaporation.esm` | — |
| DahnekeCoagulationRate | `src/dahneke_brownian_diffusion.jl:235` | Model | variables, parameters, equations | none | M | Y | Y | `components/aerosol/dahneke/coagulation_rate.esm` | — |
| DahnekeCapillaryPenetration | `src/dahneke_brownian_diffusion.jl:372` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/dahneke/capillary_penetration.esm` | — |
| DiameterGrowthRate | `src/dynamics.jl:22` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/dynamics/diameter_growth.esm` | — |
| BrownianCoagulationCoefficient | `src/dynamics.jl:75` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/dynamics/brownian_coag_coeff.esm` | — |
| MonodisperseCoagulation | `src/dynamics.jl:178` | Model | variables, parameters, equations | none | S | Y | Y | `components/aerosol/dynamics/monodisperse_coag.esm` | — |
| DiscreteCoagulation | `src/dynamics.jl:221` | Model | variables, parameters, equations (parameterized `n_bins`) | none | M | Y | Y | `components/aerosol/dynamics/discrete_coag.esm` | — |
| AerosolDynamics | `src/dynamics.jl:279` | Model | variables, parameters, equations, coupling.couple | none | L | Y | Y | `components/aerosol/dynamics/aerosol_dynamics.esm` | DiameterGrowthRate, BrownianCoagulationCoefficient |

### 1.6 elemental_carbon.jl (1, `none`), henrys_law.jl (3, `none`)

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| ElementalCarbon | `src/elemental_carbon.jl:13` | Model | variables, parameters, equations (with `DataInterpolations.LinearInterpolation`) | none (data is constants in-place) | S | Y | Y | `components/aerosol/elemental_carbon.esm` | — |
| HenrysLaw | `src/henrys_law.jl:101` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/henrys_law/henrys_law.esm` | — |
| HenrysLawTemperature | `src/henrys_law.jl:155` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/henrys_law/henrys_law_temperature.esm` | — |
| EffectiveHenrysLaw | `src/henrys_law.jl:240` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/henrys_law/effective_henrys_law.esm` | — |

### 1.7 ISORROPIA (v1, directory `src/isorropia/`) — 13 components

All sub-components compile to equation fragments; the TOP-LEVEL `Isorropia` system is `gt-ebuq`-blocked because nonlinear equilibrium solver needs `initialization_equations`/`guesses`/`system_kind=nonlinear`.

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| Gas | `src/isorropia/gas.jl:5` | Model | variables, parameters, guesses | gt-ebuq(init_eq/system_kind) | S | Y | Y | `components/aerosol/isorropia/gas.esm` | — |
| Gases | `src/isorropia/gas.jl:28` | Model | variables, coupling.couple | none | S | Y | Y | `components/aerosol/isorropia/gases.esm` | Gas |
| Ion | `src/isorropia/aqueous.jl:2` | Model | variables, parameters, guesses | gt-ebuq(init_eq/system_kind) | S | Y | Y | `components/aerosol/isorropia/ion.esm` | — |
| Salt | `src/isorropia/aqueous.jl:26` | Model | variables, parameters, equations | none | M | Y | Y | `components/aerosol/isorropia/salt.esm` | Ion |
| BinaryMolality | `src/isorropia/aqueous.jl:179` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/isorropia/binary_molality.esm` | — |
| Aqueous | `src/isorropia/aqueous.jl:201` | Model | variables, parameters, equations, coupling.couple | gt-ebuq(init_eq/system_kind) | L | Y | Y | `components/aerosol/isorropia/aqueous.esm` | Ion, Salt, BinaryMolality |
| EqConst | `src/isorropia/equilibria.jl:5` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/isorropia/eq_const.esm` | — |
| EquilibriumConstants | `src/isorropia/equilibria.jl:22` | Model | variables, coupling.couple | none | S | Y | Y | `components/aerosol/isorropia/equilibrium_constants.esm` | EqConst |
| Solid | `src/isorropia/solid.jl:6` | Model | variables, parameters | none | S | Y | Y | `components/aerosol/isorropia/solid.esm` | — |
| Solids | `src/isorropia/solid.jl:22` | Model | variables, coupling.couple | none | S | Y | Y | `components/aerosol/isorropia/solids.esm` | Solid |
| Species | `src/isorropia/isorropia.jl:100` | Model | variables, parameters | none | S | Y | Y | `components/aerosol/isorropia/species.esm` | — |
| Isorropia | `src/isorropia/isorropia.jl:110` | Model | variables, parameters, equations, initialization_equations, guesses, coupling.couple | **gt-ebuq(init_eq/system_kind)** | **XL** | Y | Y | `components/aerosol/isorropia/isorropia.esm` | Gases, Aqueous, Solids, EquilibriumConstants |

### 1.8 ISORROPIA-II (isorropia_ii_fn2007.jl) — 1 component + 8 @register_symbolic helpers

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| IsorropiaEquilibrium | `src/isorropia_ii_fn2007.jl:832` | Model | variables, parameters, equations, initialization_equations, guesses, registered_function calls (`_iso2_*`) | **gt-ebuq(init_eq/system_kind); gt-p3ep(lookup)** | XL | Y | Y | `components/aerosol/isorropia_ii/isorropia_ii.esm` | — |
| _iso2_eq_const | `src/isorropia_ii_fn2007.jl:421` | Interface | @register_symbolic | gt-p3ep(lookup) | S | Y | Y | `registered_functions/iso2_eq_const` | — |
| _iso2_km_gamma | `src/isorropia_ii_fn2007.jl:441` | Interface | @register_symbolic | gt-p3ep(lookup) | S | Y | Y | `registered_functions/iso2_km_gamma` | — |
| _iso2_gamma_T | `src/isorropia_ii_fn2007.jl:460` | Interface | @register_symbolic | gt-p3ep(lookup) | S | Y | Y | `registered_functions/iso2_gamma_T` | — |
| _iso2_zsr_m0 | `src/isorropia_ii_fn2007.jl:477` | Interface | @register_symbolic | gt-p3ep(lookup) | S | Y | Y | `registered_functions/iso2_zsr_m0` | — |
| _iso2_zsr_water | `src/isorropia_ii_fn2007.jl:646` | Interface | @register_symbolic | gt-p3ep(lookup) | S | Y | Y | `registered_functions/iso2_zsr_water` | — |
| _iso2_fb_ncp | `src/isorropia_ii_fn2007.jl:658` | Interface | @register_symbolic | gt-p3ep(lookup) | S | Y | Y | `registered_functions/iso2_fb_ncp` | — |
| _iso2_smooth_min | `src/isorropia_ii_fn2007.jl:669` | Interface | @register_symbolic | gt-p3ep(lookup) | S | Y | Y | `registered_functions/iso2_smooth_min` | — |
| _iso2_drh_T | `src/isorropia_ii_fn2007.jl:681` | Interface | @register_symbolic | gt-p3ep(lookup) | S | Y | Y | `registered_functions/iso2_drh_T` | — |
| _iso2_smooth_step | `src/isorropia_ii_fn2007.jl:693` | Interface | @register_symbolic | gt-p3ep(lookup) | S | Y | Y | `registered_functions/iso2_smooth_step` | — |
| _iso2_compute_mdrh | `src/isorropia_ii_fn2007.jl:730` | Interface | @register_symbolic | gt-p3ep(lookup) | S | Y | Y | `registered_functions/iso2_compute_mdrh` | — |

### 1.9 mass_transfer.jl (11 components, all `none`)

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| MeanMolecularSpeed | `src/mass_transfer.jl:12` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/mass_transfer/mean_molecular_speed.esm` | — |
| MeanFreePathMassTransfer | `src/mass_transfer.jl:45` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/mass_transfer/mean_free_path.esm` | — |
| KnudsenNumber | `src/mass_transfer.jl:87` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/mass_transfer/knudsen.esm` | — |
| FuchsSutugin | `src/mass_transfer.jl:117` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/mass_transfer/fuchs_sutugin.esm` | — |
| Dahneke | `src/mass_transfer.jl:145` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/mass_transfer/dahneke.esm` | — |
| MaxwellianFlux | `src/mass_transfer.jl:173` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/mass_transfer/maxwellian_flux.esm` | — |
| ParticleGrowthRate | `src/mass_transfer.jl:200` | Model | variables, parameters, equations | none | S | Y | Y | `components/aerosol/mass_transfer/particle_growth.esm` | — |
| MassTransferCoefficient | `src/mass_transfer.jl:231` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/mass_transfer/mass_transfer_coeff.esm` | — |
| UptakeCoefficient | `src/mass_transfer.jl:272` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/mass_transfer/uptake_coeff.esm` | — |
| MassTransfer | `src/mass_transfer.jl:319` | Model | variables, parameters, coupling.couple | none | M | Y | Y | `components/aerosol/mass_transfer/mass_transfer.esm` | MeanMolecularSpeed, Knudsen, FuchsSutugin |

### 1.10 mie_scattering.jl (5, `gt-p3ep` for Mie/Rayleigh helpers)

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| MieScattering | `src/mie_scattering.jl:36` | Model | variables, parameters, observed, registered_function calls (`mie_Q_ext`, `mie_Q_scat`) | gt-p3ep(lookup) | M | Y | Y | `components/aerosol/mie/mie_scattering.esm` | — |
| RayleighScattering | `src/mie_scattering.jl:111` | Model | variables, parameters, observed, registered_function calls (`_rayleigh_Q_*`) | gt-p3ep(lookup) | M | Y | Y | `components/aerosol/mie/rayleigh_scattering.esm` | — |
| AerosolExtinction | `src/mie_scattering.jl:206` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/mie/aerosol_extinction.esm` | — |
| Visibility | `src/mie_scattering.jl:273` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/mie/visibility.esm` | — |
| RayleighAtmosphere | `src/mie_scattering.jl:329` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/mie/rayleigh_atmosphere.esm` | — |

### 1.11 nucleation.jl (4, `none`), organic_aerosol.jl (7, `none`)

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| Nucleation | `src/nucleation.jl:35` | Model | variables, parameters, equations | none | M | Y | Y | `components/aerosol/nucleation/nucleation.esm` | — |
| WaterProperties | `src/nucleation.jl:117` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/nucleation/water_properties.esm` | — |
| CriticalCluster | `src/nucleation.jl:200` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/nucleation/critical_cluster.esm` | — |
| ClassicalNucleationRate | `src/nucleation.jl:257` | Model | variables, parameters, observed | none | M | Y | Y | `components/aerosol/nucleation/classical_rate.esm` | — |
| ECTracerMethod | `src/organic_aerosol.jl:18` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/organic/ec_tracer.esm` | — |
| NoninteractingSOA | `src/organic_aerosol.jl:64` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/organic/noninteracting_soa.esm` | — |
| AbsorptivePartitioning | `src/organic_aerosol.jl:125` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/organic/absorptive_partitioning.esm` | — |
| TwoProductSOA | `src/organic_aerosol.jl:197` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/organic/two_product_soa.esm` | — |
| LangmuirAdsorption | `src/organic_aerosol.jl:249` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/organic/langmuir.esm` | — |
| BETAdsorption | `src/organic_aerosol.jl:279` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/organic/bet.esm` | — |
| FHHAdsorption | `src/organic_aerosol.jl:314` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/organic/fhh.esm` | — |

### 1.12 single_particle_dynamics.jl (9), size_distribution.jl (7), stochastic_collection.jl (1)

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| MeanFreePath | `src/single_particle_dynamics.jl:22` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/particle_dyn/mean_free_path.esm` | — |
| SlipCorrection | `src/single_particle_dynamics.jl:64` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/particle_dyn/slip.esm` | — |
| SettlingVelocity | `src/single_particle_dynamics.jl:113` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/particle_dyn/settling.esm` | — |
| BrownianDiffusion | `src/single_particle_dynamics.jl:172` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/particle_dyn/brownian_diffusion.esm` | — |
| ParticleMobility | `src/single_particle_dynamics.jl:230` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/particle_dyn/mobility.esm` | — |
| ElectricalMobility | `src/single_particle_dynamics.jl:273` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/particle_dyn/electrical_mobility.esm` | — |
| StokesNumber | `src/single_particle_dynamics.jl:329` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/particle_dyn/stokes.esm` | — |
| AerodynamicDiameter | `src/single_particle_dynamics.jl:390` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/particle_dyn/aerodynamic_diameter.esm` | — |
| SingleParticleDynamics | `src/single_particle_dynamics.jl:440` | Model | variables, parameters, coupling.couple | none | M | Y | Y | `components/aerosol/particle_dyn/single_particle.esm` | MeanFreePath, SlipCorrection, SettlingVelocity |
| AerosolDistribution | `src/size_distribution.jl:25` | Model | variables, parameters (lognormal modes) | none | M | Y | Y | `components/aerosol/size/aerosol_distribution.esm` | — |
| UrbanAerosol | `src/size_distribution.jl:162` | Model | preset parameters for AerosolDistribution | none | S | Y | Y | `components/aerosol/size/urban.esm` | AerosolDistribution |
| MarineAerosol | `src/size_distribution.jl:182` | Model | preset parameters | none | S | Y | Y | `components/aerosol/size/marine.esm` | AerosolDistribution |
| RuralAerosol | `src/size_distribution.jl:202` | Model | preset parameters | none | S | Y | Y | `components/aerosol/size/rural.esm` | AerosolDistribution |
| RemoteContinentalAerosol | `src/size_distribution.jl:222` | Model | preset parameters | none | S | Y | Y | `components/aerosol/size/remote_continental.esm` | AerosolDistribution |
| FreeTroposphereAerosol | `src/size_distribution.jl:242` | Model | preset parameters | none | S | Y | Y | `components/aerosol/size/free_troposphere.esm` | AerosolDistribution |
| PolarAerosol | `src/size_distribution.jl:262` | Model | preset parameters | none | S | Y | Y | `components/aerosol/size/polar.esm` | AerosolDistribution |
| DesertAerosol | `src/size_distribution.jl:282` | Model | preset parameters | none | S | Y | Y | `components/aerosol/size/desert.esm` | AerosolDistribution |
| StochasticCollectionCoalescence | `src/stochastic_collection.jl:87` | Model | variables, parameters, equations (array-ops) | none | L | Y | Y | `components/aerosol/stochastic_collection.esm` | — |

### 1.13 sulfate_formation.jl (6), timescales.jl (6)

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| SulfateFormationO3 | `src/sulfate_formation.jl:78` | Model | variables, parameters, equations | none | S | Y | Y | `components/aerosol/sulfate/o3.esm` | — |
| SulfateFormationH2O2 | `src/sulfate_formation.jl:132` | Model | variables, parameters, equations | none | S | Y | Y | `components/aerosol/sulfate/h2o2.esm` | — |
| SulfateFormationFe | `src/sulfate_formation.jl:189` | Model | variables, parameters, equations | none | S | Y | Y | `components/aerosol/sulfate/fe.esm` | — |
| SulfateFormationMn | `src/sulfate_formation.jl:237` | Model | variables, parameters, equations | none | S | Y | Y | `components/aerosol/sulfate/mn.esm` | — |
| SulfateFormationFeMn | `src/sulfate_formation.jl:284` | Model | variables, parameters, equations | none | S | Y | Y | `components/aerosol/sulfate/femn.esm` | — |
| SulfateFormation | `src/sulfate_formation.jl:349` | Model | variables, parameters, coupling.couple | none | M | Y | Y | `components/aerosol/sulfate/total.esm` | SulfateFormationO3, H2O2, Fe, Mn, FeMn |
| GasDiffusionTimescale | `src/timescales.jl:14` | Model | variables, parameters, observed | none | S | N | Y | `components/aerosol/timescales/gas_diffusion.esm` | — |
| AqueousDiffusionTimescale | `src/timescales.jl:42` | Model | variables, parameters, observed | none | S | N | Y | `components/aerosol/timescales/aqueous_diffusion.esm` | — |
| InterfacialTimescale | `src/timescales.jl:70` | Model | variables, parameters, observed | none | S | N | Y | `components/aerosol/timescales/interfacial.esm` | — |
| ReactionTimescale | `src/timescales.jl:110` | Model | variables, parameters, observed | none | S | N | Y | `components/aerosol/timescales/reaction.esm` | — |
| SolidEquilibrationTimescale | `src/timescales.jl:145` | Model | variables, parameters, observed | none | S | N | Y | `components/aerosol/timescales/solid_eq.esm` | — |
| AqueousEquilibrationTimescale | `src/timescales.jl:183` | Model | variables, parameters, observed | none | S | N | Y | `components/aerosol/timescales/aqueous_eq.esm` | — |

### 1.14 seinfeld_pandis_ch10/ (4)

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| DRHTemperature | `src/seinfeld_pandis_ch10/drh.jl:76` | Model | variables, parameters, observed (parameterized `salt`) | none | S | Y | Y | `components/aerosol/sp_ch10/drh_temperature.esm` | — |
| KelvinEffect | `src/seinfeld_pandis_ch10/kelvin_effect.jl:51` | Model | variables, parameters, observed | none | S | Y | Y | `components/aerosol/sp_ch10/kelvin.esm` | — |
| NH4NO3Equilibrium | `src/seinfeld_pandis_ch10/nh4no3_equilibrium.jl:68` | Model | variables, parameters, equations | none | S | Y | Y | `components/aerosol/sp_ch10/nh4no3_eq.esm` | — |
| ZSRWaterContent | `src/seinfeld_pandis_ch10/zsr.jl:45` | Model | variables, parameters, observed (parameterized `n_species`) | none | S | Y | Y | `components/aerosol/sp_ch10/zsr.esm` | — |

### 1.15 TOMAS.jl (module-level script)

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| tomas (ODESystem) | `src/TOMAS.jl:258` | Model | @named ODESystem with 5-bin mass distribution; module-level | none (but script-style, needs refactor to library-form first) | L | N | N | `components/aerosol/tomas.esm` (TBD) | — |

---

## 2. AtmosphericDeposition.jl (20 components)

Repo purpose: dry and wet deposition velocity/resistance schemes (Wesley 1989, Seinfeld-Pandis Ch. 19, SP-2006 Ch. 20, Luo 2023).

### 2.1 dry_deposition.jl — 2 builders, 3 lookup tables

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| DryDepositionGas (Wesley) | `src/dry_deposition.jl:323` | Model | variables, parameters, equations, registered_function calls (A_table/α_table/γ_table) | gt-p3ep(lookup) | L | Y | Y | `components/atmospheric_deposition/wesley_dry_gas.esm` | — |
| DryDepositionAerosol | `src/dry_deposition.jl:1040` | Model | variables, parameters, equations | none | M | Y | Y | `components/atmospheric_deposition/dry_aerosol.esm` | — |
| A_table | `src/dry_deposition.jl:180` | Interface | @register_symbolic (season × land use) | gt-p3ep(lookup) | S | Y | Y | `registered_functions/wesley_A_table` | — |
| α_table | `src/dry_deposition.jl:185` | Interface | @register_symbolic (land use) | gt-p3ep(lookup) | S | Y | Y | `registered_functions/wesley_alpha_table` | — |
| γ_table | `src/dry_deposition.jl:190` | Interface | @register_symbolic (land use) | gt-p3ep(lookup) | S | Y | Y | `registered_functions/wesley_gamma_table` | — |

### 2.2 wet_deposition.jl — 1 builder, 1 lookup

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| WetDeposition | `src/wet_deposition.jl:147` | Model | variables, parameters, equations, registered_function calls (get_lev_depth) | gt-p3ep(lookup) | M | Y | Y | `components/atmospheric_deposition/wet_deposition.esm` | — |
| get_lev_depth | `src/wet_deposition.jl:90` | Interface | @register_symbolic | gt-p3ep(lookup) | S | Y | Y | `registered_functions/get_lev_depth` | — |

### 2.3 seinfeld_pandis_ch19.jl (7, `none`)

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| AerodynamicResistance | `src/seinfeld_pandis_ch19.jl:106` | Model | variables, parameters, observed | none | S | Y | Y | `components/atmospheric_deposition/sp_ch19/aerodynamic_resistance.esm` | — |
| QuasiLaminarResistanceGas | `src/seinfeld_pandis_ch19.jl:143` | Model | variables, parameters, observed | none | S | Y | Y | `components/atmospheric_deposition/sp_ch19/quasi_laminar_gas.esm` | — |
| ParticleSettling | `src/seinfeld_pandis_ch19.jl:182` | Model | variables, parameters, observed | none | S | Y | Y | `components/atmospheric_deposition/sp_ch19/particle_settling.esm` | — |
| QuasiLaminarResistanceParticle | `src/seinfeld_pandis_ch19.jl:234` | Model | variables, parameters, observed | none | S | Y | Y | `components/atmospheric_deposition/sp_ch19/quasi_laminar_particle.esm` | — |
| SurfaceResistance | `src/seinfeld_pandis_ch19.jl:311` | Model | variables, parameters, observed | none | M | Y | Y | `components/atmospheric_deposition/sp_ch19/surface_resistance.esm` | — |
| DryDepositionGas (SP) | `src/seinfeld_pandis_ch19.jl:416` | Model | variables, parameters, coupling.couple | none | M | Y | Y | `components/atmospheric_deposition/sp_ch19/dry_dep_gas.esm` | AerodynamicResistance, QuasiLaminarResistanceGas, SurfaceResistance |
| DryDepositionParticle | `src/seinfeld_pandis_ch19.jl:479` | Model | variables, parameters, coupling.couple | none | M | Y | Y | `components/atmospheric_deposition/sp_ch19/dry_dep_particle.esm` | AerodynamicResistance, QuasiLaminarResistanceParticle, ParticleSettling |

### 2.4 seinfeld_pandis_2006_ch20.jl (7, `none`)

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| MassTransferCoeff | `src/seinfeld_pandis_2006_ch20.jl:60` | Model | variables, parameters, observed | none | S | Y | Y | `components/atmospheric_deposition/sp06_ch20/mass_transfer_coeff.esm` | — |
| GasScavengingCoeff | `src/seinfeld_pandis_2006_ch20.jl:116` | Model | variables, parameters, observed | none | S | Y | Y | `components/atmospheric_deposition/sp06_ch20/gas_scavenging_coeff.esm` | — |
| ReversibleGasScavenging | `src/seinfeld_pandis_2006_ch20.jl:194` | Model | variables, parameters, equations | none | S | Y | Y | `components/atmospheric_deposition/sp06_ch20/reversible_gas_scavenging.esm` | — |
| BelowCloudGasScavenging | `src/seinfeld_pandis_2006_ch20.jl:234` | Model | variables, parameters, equations | none | M | Y | Y | `components/atmospheric_deposition/sp06_ch20/below_cloud_gas_scavenging.esm` | — |
| ParticleCollectionEfficiency | `src/seinfeld_pandis_2006_ch20.jl:365` | Model | variables, parameters, observed | none | S | Y | Y | `components/atmospheric_deposition/sp06_ch20/particle_collection_eff.esm` | — |
| ParticleScavengingCoeff | `src/seinfeld_pandis_2006_ch20.jl:414` | Model | variables, parameters, observed | none | S | Y | Y | `components/atmospheric_deposition/sp06_ch20/particle_scavenging_coeff.esm` | — |
| WetDepositionFlux | `src/seinfeld_pandis_2006_ch20.jl:451` | Model | variables, parameters, coupling.couple | none | M | Y | Y | `components/atmospheric_deposition/sp06_ch20/wet_deposition_flux.esm` | ParticleScavengingCoeff, GasScavengingCoeff |

### 2.5 luo2023.jl (3, `none`)

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| AirRefreshingLimitation | `src/luo2023.jl:210` | Model | variables, parameters, observed | none | S | Y | Y | `components/atmospheric_deposition/luo2023/air_refreshing.esm` | — |
| CloudIceUptakeLimitation | `src/luo2023.jl:260` | Model | variables, parameters, observed | none | S | Y | Y | `components/atmospheric_deposition/luo2023/cloud_ice_uptake.esm` | — |
| WetScavengingLimitations | `src/luo2023.jl:326` | Model | variables, parameters, coupling.couple | none | M | Y | Y | `components/atmospheric_deposition/luo2023/wet_scavenging.esm` | AirRefreshingLimitation, CloudIceUptakeLimitation |

### 2.6 wesley1989.jl — builder for EMEP-Wesley systems

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| WesleySurfaceResistance | `src/wesley1989.jl:360` | Model | variables, parameters, equations (builder) | none | M | Y | Y | `components/atmospheric_deposition/wesley1989/surface_resistance.esm` | — |

---

## 3. AtmosphericDynamics.jl (31 components, all `none`)

Repo purpose: atmospheric thermodynamics, stability, turbulence, global circulation, Clark 1977 anelastic system.

### 3.1 seinfeld_pandis_ch1.jl (11)

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| IdealGasLaw | `src/seinfeld_pandis_ch1.jl:68` | Model | variables, parameters, observed | none | S | Y | Y | `components/atmospheric_dynamics/sp_ch1/ideal_gas.esm` | — |
| ScaleHeight | `src/seinfeld_pandis_ch1.jl:109` | Model | variables, parameters, observed | none | S | Y | Y | `components/atmospheric_dynamics/sp_ch1/scale_height.esm` | — |
| AtmosphericPressureProfile | `src/seinfeld_pandis_ch1.jl:151` | Model | variables, parameters, observed | none | S | Y | Y | `components/atmospheric_dynamics/sp_ch1/pressure_profile.esm` | — |
| BarometricFormula | `src/seinfeld_pandis_ch1.jl:201` | Model | variables, parameters, observed | none | S | Y | Y | `components/atmospheric_dynamics/sp_ch1/barometric.esm` | — |
| TotalMolarConcentration | `src/seinfeld_pandis_ch1.jl:244` | Model | variables, parameters, observed | none | S | Y | Y | `components/atmospheric_dynamics/sp_ch1/total_molar_conc.esm` | — |
| MixingRatio | `src/seinfeld_pandis_ch1.jl:278` | Model | variables, parameters, observed | none | S | Y | Y | `components/atmospheric_dynamics/sp_ch1/mixing_ratio.esm` | — |
| PartialPressureMixingRatio | `src/seinfeld_pandis_ch1.jl:308` | Model | variables, parameters, observed | none | S | Y | Y | `components/atmospheric_dynamics/sp_ch1/partial_pressure.esm` | — |
| SaturationVaporPressure | `src/seinfeld_pandis_ch1.jl:351` | Model | variables, parameters, observed | none | S | Y | Y | `components/atmospheric_dynamics/sp_ch1/sat_vapor_pressure.esm` | — |
| RelativeHumidity | `src/seinfeld_pandis_ch1.jl:397` | Model | variables, parameters, observed | none | S | Y | Y | `components/atmospheric_dynamics/sp_ch1/relative_humidity.esm` | — |
| WaterVaporThermodynamics | `src/seinfeld_pandis_ch1.jl:433` | Model | variables, parameters, coupling.couple | none | M | Y | Y | `components/atmospheric_dynamics/sp_ch1/water_vapor_thermo.esm` | SaturationVaporPressure, RelativeHumidity |
| AtmosphericThermodynamics | `src/seinfeld_pandis_ch1.jl:479` | Model | variables, parameters, coupling.couple | none | L | Y | Y | `components/atmospheric_dynamics/sp_ch1/atmospheric_thermo.esm` | IdealGasLaw, WaterVaporThermodynamics, AtmosphericPressureProfile |

### 3.2 clark1977.jl (9)

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| IsentropicBaseState | `src/clark1977.jl:49` | Model | variables, parameters, observed | none | S | Y | Y | `components/atmospheric_dynamics/clark1977/isentropic_base_state.esm` | — |
| WitchOfAgnesi | `src/clark1977.jl:107` | Model | variables, parameters, observed | none | S | Y | Y | `components/atmospheric_dynamics/clark1977/witch_of_agnesi.esm` | — |
| TerrainFollowingTransform | `src/clark1977.jl:157` | CoordinateTransform | coordinate_transforms (scalar algebra; not metric-tensor) | none | S | Y | Y | `components/atmospheric_dynamics/clark1977/terrain_following.esm` | — |
| SmagorinskyTurbulence | `src/clark1977.jl:214` | Model | variables, parameters, observed | none | M | Y | Y | `components/atmospheric_dynamics/clark1977/smagorinsky.esm` | — |
| AnelasticMomentum | `src/clark1977.jl:282` | Model | variables, parameters, equations | none | M | Y | Y | `components/atmospheric_dynamics/clark1977/anelastic_momentum.esm` | — |
| AnelasticMassContinuity | `src/clark1977.jl:369` | Model | variables, parameters, equations | none | S | Y | Y | `components/atmospheric_dynamics/clark1977/anelastic_mass.esm` | — |
| AnelasticThermodynamics | `src/clark1977.jl:426` | Model | variables, parameters, equations | none | M | Y | Y | `components/atmospheric_dynamics/clark1977/anelastic_thermo.esm` | — |
| DiagnosticPressure | `src/clark1977.jl:499` | Model | variables, parameters, observed | none | M | Y | Y | `components/atmospheric_dynamics/clark1977/diagnostic_pressure.esm` | — |
| Clark1977AnelasticSystem | `src/clark1977.jl:582` | Model | variables, parameters, coupling.couple | none | L | Y | Y | `components/atmospheric_dynamics/clark1977/full_anelastic.esm` | AnelasticMomentum, AnelasticMassContinuity, AnelasticThermodynamics, DiagnosticPressure |

### 3.3 holtslag_boville_1993.jl (3), local_scale_meteorology.jl (3), global_cycles.jl (3), general_circulation.jl (1), atmospheric_diffusion.jl (1)

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| HoltslagBovilleSurfaceFlux | `src/holtslag_boville_1993.jl:35` | Model | variables, parameters, equations | none | M | Y | Y | `components/atmospheric_dynamics/holtslag_boville/surface_flux.esm` | — |
| HoltslagBovilleLocalDiffusion | `src/holtslag_boville_1993.jl:184` | Model | variables, parameters, equations | none | M | Y | Y | `components/atmospheric_dynamics/holtslag_boville/local_diffusion.esm` | — |
| HoltslagBovilleNonlocalABL | `src/holtslag_boville_1993.jl:290` | Model | variables, parameters, equations | none | L | Y | Y | `components/atmospheric_dynamics/holtslag_boville/nonlocal_abl.esm` | — |
| AtmosphericStability | `src/local_scale_meteorology.jl:32` | Model | variables, parameters, observed | none | S | Y | Y | `components/atmospheric_dynamics/local_scale/stability.esm` | — |
| SurfaceLayerProfile | `src/local_scale_meteorology.jl:107` | Model | variables, parameters, observed | none | M | Y | Y | `components/atmospheric_dynamics/local_scale/surface_layer_profile.esm` | — |
| LocalScaleMeteorology | `src/local_scale_meteorology.jl:234` | Model | variables, parameters, coupling.couple | none | M | Y | Y | `components/atmospheric_dynamics/local_scale/local_scale_met.esm` | AtmosphericStability, SurfaceLayerProfile |
| SulfurCycle | `src/global_cycles.jl:23` | Model | variables, parameters, equations | none | M | Y | Y | `components/atmospheric_dynamics/global_cycles/sulfur.esm` | — |
| CarbonCycle | `src/global_cycles.jl:115` | Model | variables, parameters, equations | none | M | Y | Y | `components/atmospheric_dynamics/global_cycles/carbon.esm` | — |
| FourCompartmentAtmosphere | `src/global_cycles.jl:280` | Model | variables, parameters, equations | none | L | Y | Y | `components/atmospheric_dynamics/global_cycles/four_compartment.esm` | — |
| GeneralCirculation | `src/general_circulation.jl:60` | Model | variables, parameters, equations | none | L | Y | Y | `components/atmospheric_dynamics/general_circulation.esm` | — |
| AtmosphericDiffusion | `src/atmospheric_diffusion.jl:30` | Model | variables, parameters, equations | none | M | Y | Y | `components/atmospheric_dynamics/atmospheric_diffusion.esm` | — |

---

## 4. EarthSciData.jl (10 DataLoaders + 12 registered interpolators)

Repo purpose: data-backed MTK systems (reanalysis/emissions/topography). Every system registers `interp_unsafe` family via `@register_symbolic` → `gt-p3ep`. ERA5 and GEOSFP additionally register `get_unit` for `DataInterpolations.derivative` → `gt-6ohw`.

### 4.1 DataLoaders (all use `gt-p3ep`)

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| ERA5 | `src/era5.jl:385` | DataLoader | variables, parameters, equations, discrete_events (build_interp_event), registered_function calls (`interp_unsafe`, `DataInterpolations.derivative`) | **gt-p3ep; gt-6ohw** | L | Y | Y | `components/earthsci_data/era5.esm` | — |
| GEOSFP | `src/geosfp.jl:410` | DataLoader | variables, parameters, equations, discrete_events, registered_function calls | **gt-p3ep; gt-6ohw** | L | Y | Y | `components/earthsci_data/geosfp.esm` | — |
| CEDS | `src/ceds.jl:313` | DataLoader | variables, parameters, equations, discrete_events, registered_function calls | gt-p3ep(lookup) | M | Y | Y | `components/earthsci_data/ceds.esm` | — |
| LANDFIRE | `src/landfire.jl:246` | DataLoader | variables, parameters, equations, discrete_events, registered_function calls | gt-p3ep(lookup) | M | Y | Y | `components/earthsci_data/landfire.esm` | — |
| USGS3DEP | `src/usgs3dep.jl:326` | DataLoader | variables, parameters, equations, discrete_events, registered_function calls | gt-p3ep(lookup) | M | Y | Y | `components/earthsci_data/usgs3dep.esm` | — |
| WRF | `src/wrf.jl:169` | DataLoader | variables, parameters, equations, discrete_events, registered_function calls | gt-p3ep(lookup) | L | Y | Y | `components/earthsci_data/wrf.esm` | — |
| OpenAQ | `src/openaq.jl:595` | DataLoader | variables, parameters, equations, discrete_events, registered_function calls | gt-p3ep(lookup) | M | Y | Y | `components/earthsci_data/openaq.esm` | — |
| NCEPNCARReanalysis | `src/NCEP-NCAR_Reanalysis.jl:224` | DataLoader | variables, parameters, equations, discrete_events, registered_function calls | gt-p3ep(lookup) | M | Y | N | `components/earthsci_data/ncep_ncar.esm` | — |
| NEI2016MonthlyEmis | `src/nei2016monthly.jl:358` | DataLoader | variables, parameters, equations, discrete_events, registered_function calls (diurnal/dayofweek/delp_dry_surface) | gt-p3ep(lookup) | L | Y | Y | `components/earthsci_data/nei2016_monthly.esm` | — |
| EDGARv81MonthlyEmis | `src/edgar_v81_monthly.jl:277` | DataLoader | variables, parameters, equations, discrete_events, registered_function calls | gt-p3ep(lookup) | M | Y | Y | `components/earthsci_data/edgar_v81_monthly.esm` | — |

### 4.2 Registered functions (all `gt-p3ep`)

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| interp_unsafe (3-arg/4-arg/5-arg overloads) | `src/mtk_integration.jl:55-64` | Interface | @register_symbolic (data-buffer typed) | gt-p3ep(lookup) | M | Y | N | `registered_functions/interp_unsafe` | — |
| interp_time_only (overloads) | `src/mtk_integration.jl:62-64` | Interface | @register_symbolic | gt-p3ep(lookup) | M | Y | N | `registered_functions/interp_time_only` | — |
| diurnal_itp | `src/nei2016monthly.jl:126` | Interface | @register_symbolic | gt-p3ep(lookup) | S | Y | Y | `registered_functions/nei_diurnal_itp` | — |
| diurnal_itp_NOx | `src/nei2016monthly.jl:127` | Interface | @register_symbolic | gt-p3ep(lookup) | S | Y | Y | `registered_functions/nei_diurnal_itp_nox` | — |
| diurnal_itp_ISOP | `src/nei2016monthly.jl:128` | Interface | @register_symbolic | gt-p3ep(lookup) | S | Y | Y | `registered_functions/nei_diurnal_itp_isop` | — |
| dayofweek_itp_CO | `src/nei2016monthly.jl:129` | Interface | @register_symbolic | gt-p3ep(lookup) | S | Y | Y | `registered_functions/nei_dayofweek_itp_co` | — |
| dayofweek_itp_NOx | `src/nei2016monthly.jl:130` | Interface | @register_symbolic | gt-p3ep(lookup) | S | Y | Y | `registered_functions/nei_dayofweek_itp_nox` | — |
| delp_dry_surface_itp | `src/nei2016monthly.jl:131` | Interface | @register_symbolic | gt-p3ep(lookup) | S | Y | Y | `registered_functions/nei_delp_dry_surface_itp` | — |
| DataInterpolations.derivative (get_unit) | `src/era5.jl:454,516`, `src/geosfp.jl:279` | Interface | registered `get_unit` hook | gt-6ohw | S | Y | N | `registered_functions/data_interpolations_derivative` | — |

### 4.3 Couplings (`src/coupling.jl`)

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| EarthSciData ↔ CoupledSystem couplings (ERA5/GEOSFP/CEDS/EDGAR/NEI adjoint couples via `param_to_var`) | `src/coupling.jl:24,31,...` | Coupling | coupling.param_to_var (`lat`, `lon`, `lev`) | none | S | Y | Y | `couplings/earthscidata_spatial_params.esm` | ERA5, GEOSFP, CEDS, EDGARv81MonthlyEmis, NEI2016MonthlyEmis |

---

## 5. EarthSciDiscretizations.jl (framework — 0 migratable models)

Repo purpose: finite-volume PDE discretization library (cubed sphere, metric tensors, divergence/gradient/laplacian operators).

**Classification:** Framework only. These are the discretization operators that MOLFiniteDifference-free PDE migration will need. They do not become `.esm` files themselves but they define the operator semantics that `Domain.coordinate_transforms` and array-op `ExpressionNode`s need to represent.

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| CubedSphereGrid | `src/grids/cubed_sphere.jl` | Interface | metric-tensor coordinate_transforms | other:P3-A-metric-tensor-coord-transforms | XL | Y | Y | framework-only; feeds into `Domain.coordinate_transforms` spec | — |
| MetricTensors | `src/grids/metric_tensors.jl` | CoordinateTransform | metric-tensor coord transform (Julia fn) | other:P3-A-metric-tensor-coord-transforms | L | Y | N | framework-only; schema extension via `CoordinateTransform.forward_expression` | — |
| PanelConnectivity | `src/grids/panel_connectivity.jl` | Interface | panel-indexing array-ops | other:discretization-plan | L | Y | N | framework-only | — |
| Divergence / Gradient / Laplacian ops | `src/operators/*.jl` | Operator | array-ops | other:discretization-plan (`gt-dq0f`) | L | Y | Y | framework-only; `ExpressionNode` array-op mapping already schema-ready | — |
| FV stencil ops (ppm_edge, reconstruction, transport_2d, vertical_remap, wind_ops, vorticity, flux_1d, kinetic_energy) | `src/operators/` | Operator | array-ops | other:discretization-plan | M-L | Y | Y | framework-only | — |
| BCHandler / GhostCells / Staggering | `src/{bc_handler,ghost_cells,staggering}.jl` | Interface | BC scheme | other:discretization-plan | M | Y | N | framework-only | — |

---

## 6. EarthSciMLBase.jl (framework — 0 migratable models)

Repo purpose: core coupling & composition machinery (`couple`, `operator_compose`, `param_to_var`, `DomainInfo`, `Operator`, `Advection`, coordinate transforms).

**Classification:** Framework only. These primitives ARE the schema features (§5 coupling, §6 operators, §7 domain). They do not become `.esm` files.

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| CoupledSystem | `src/coupled_system.jl` | Interface | system container holding models+operators+pdesystems | n/a — framework | XL | Y | Y | framework-only | — |
| Advection | `src/advection.jl` | Operator | advective-flux operator template | n/a — framework | L | Y | Y | framework-only; instances become Operator entries in model files | — |
| DomainInfo | `src/domaininfo.jl` | Interface | `Domain` schema schema — Interval/BC/coord_transforms | n/a — framework | L | Y | Y | framework-only | — |
| operator_compose | `src/operator_compose.jl` | Coupling | `coupling.operator_compose` schema | n/a — framework | L | Y | Y | framework-only | — |
| param_to_var | `src/param_to_var.jl` | Coupling | `coupling.param_to_var` transform | n/a — framework | M | Y | Y | framework-only | — |
| pdesystem_coupling / merge_pdesystems | `src/pdesystem_coupling.jl` | Coupling | PDE-PDE coupling via ConnectorSystem | n/a — framework | XL | Y | Y | framework-only | — |
| coord_trans (partialderivative_transforms) | `src/coord_trans.jl` | CoordinateTransform | scalar coord transforms | other:P3-A if metric-tensor variant used | L | Y | Y | framework-only | — |
| mtk_grid_func | `src/mtk_grid_func.jl` | Interface | `@register_symbolic` coupler-temp-file callable | gt-p3ep (P2-D subsumed) | M | Y | N | framework-only | — |
| Operator (base type) | `src/operator.jl` | Interface | `Operator` abstract type | n/a — framework | S | Y | Y | framework-only | — |
| add_dims / blockdiagonal / graph / jacobian / map_algorithm / solver_strategies | `src/*.jl` | Interface | internals | n/a — framework | M | Y | N | framework-only | — |

---

## 7. Emissions.jl (0 MTK components)

Repo purpose: emissions preprocessing (CSV/NetCDF/shapefile I/O, plume rise geometric calc, speciation, surrogates, spatial allocation).

**Classification:** Not an MTK-using library. Zero `@component`, `@mtkmodel`, `@reaction_network`, or `ReactionSystem`/`ODESystem` definitions discovered. Deferred from Phase 2 migration. Note: the 2026-04-19 audit marked this repo "empty" — it now has content (since 2026-04-19), but it is still not MTK-based.

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| (none) | — | — | — | other:non-MTK-data-processing | — | — | — | — | — |

---

## 8. EnvironmentalTransport.jl (8 user-facing components, 1 Operator, 1 Callback)

Repo purpose: advection, PBL mixing, puff dispersion, Saint-Venant overland flow, plume rise, Gaussian dispersion.

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| SurfaceRunoff | `src/surface_runoff.jl:35` | Model | variables, parameters, observed | none | M | Y | Y | `components/environmental_transport/surface_runoff/surface_runoff_component.esm` | — |
| Saint-Venant PDE (anonymous fn at `surface_runoff.jl:86`) | `src/surface_runoff.jl:193` | Model | PDESystem (`h(t,x,y)`, `q_x`, `q_y`), boundary_conditions, domain | **gt-vzwk(PDE-tests); other:discretization-plan** | XL | Y | Y | `components/environmental_transport/surface_runoff/saint_venant.esm` | SurfaceRunoff |
| HeavisideBoundaryCondition | `src/surface_runoff.jl:232` | Model | variables, parameters, observed | none | S | Y | N | `components/environmental_transport/surface_runoff/heaviside_bc.esm` | — |
| Puff | `src/puff.jl:24` | Model | variables, parameters, equations, continuous_events (vertical_boundary, lateral_boundary), FunctionalAffect (terminate!), BC referencing `di.grid_spacing*buffer_cells` | **other:P2-C-terminate-in-FunctionalAffect; other:P3-B-BC-symbolic-offset** | L | Y | Y | `components/environmental_transport/puff.esm` | — |
| Sofiev2012PlumeRise | `src/plume_rise/sofiev_2012.jl:14` | Model | variables, parameters, equations, initialization_equations, guesses | **gt-ebuq(init_eq/system_kind)** | L | Y | Y | `components/environmental_transport/plume_rise/sofiev_2012.esm` | — |
| BoundaryLayerMixingKC | `src/BoundaryLayerMixingKC.jl:15` | Model | variables, parameters, equations, **@brownians Bw** | **gt-kuxo(brownian)** | L | Y | Y | `components/environmental_transport/boundary_layer_mixing_kc.esm` | — |
| GaussianPGB | `src/GaussianDispersion.jl:83` | Model | variables, parameters, coupling.couple | none | M | Y | Y | `components/environmental_transport/gaussian/pgb.esm` | Puff |
| GaussianKC | `src/GaussianDispersion.jl:378` | Model | variables, parameters, coupling.couple | none | M | Y | Y | `components/environmental_transport/gaussian/kc.esm` | Puff, BoundaryLayerMixingKC |
| AdvectionOperator | `src/advection.jl:186` | Operator | EarthSciMLBase.Operator (stencil+BC) | none (Operator schema supported) | M | Y | Y | `components/environmental_transport/advection.esm` (Operator entry in model files) | — |
| PBLMixingCallback | `src/PBL_mixing.jl:183` | Coupling | `init_callback` returning PeriodicCallback; operates on ODEIntegrator state directly | other:P2-C (handler_id-based PeriodicCallback with imperative mutation — needs FunctionalAffect extension) | L | Y | Y | `couplings/pbl_mixing_callback.esm` | — |

---

## 9. GasChem.jl (36 components + 2 ReactionSystem-based models + 21 registered interpolators)

Repo purpose: gas-phase chemistry (SuperFast, GEOS-Chem full-chem, Pollu, Fast-JX photolysis, tropospheric/stratospheric chemistry, radiation fundamentals).

### 9.1 @reaction_network / ReactionSystem builders

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| SuperFast | `src/SuperFast.jl:205` | ReactionSystem | reaction_systems.species/reactions, ReactionSystem rate-law wrappers (constant_k/arrh/arr_3rd/rate_2HO2/rate_OH_CO) | none | L | Y | Y | `components/gaschem/superfast.esm` | — | **status: complete, sha: 8c12c048482b515fb8eb2110bf8ab4b4f4e71309** (mdl-dkw; friction: mdl-adq fractional stoich, mdl-kez isconstantspecies, mdl-uao no scaffolder) |
| SuperFast rate-law helpers (constant_k, arrh, arr_3rd, rate_2HO2, rate_OH_CO, rate_toppb) | `src/SuperFast.jl:6,33,64,102,142` | Interface | builder fns producing sub-ReactionSystems | none | S | Y | Y | `components/gaschem/superfast_ratelaws.esm` | — |
| GEOSChemGasPhase | `src/geoschem_fullchem.jl:62` | ReactionSystem | reaction_systems (~hundreds of reactions), ReactionSystem rate-law wrappers | none | XL | Y | Y | `components/gaschem/geoschem_fullchem.esm` | — |
| geoschem_ratelaws (constant_k, regress_T, ...) | `src/geoschem_ratelaws.jl:11,27,35,...` | Interface | builder fns producing sub-ReactionSystems | none | M | Y | Y | `components/gaschem/geoschem_ratelaws.esm` | — |
| Pollu | `src/Pollu.jl:27` | ReactionSystem | `@reaction_network` (classic 25-species chem benchmark) | none | M | Y | Y | `components/gaschem/pollu.esm` | — |

### 9.2 Fast-JX & interpolations (all `gt-p3ep`)

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| FastJX | `src/Fast-JX.jl:1276` | Model | variables, parameters, equations, registered_function calls (cos_solar_zenith_angle, calc_direct_flux, calc_direct_fluxes, flux_interp_1..18) | **gt-p3ep(lookup)** | XL | Y | Y | `components/gaschem/fastjx/fastjx.esm` | flux_interp_1..18, cos_solar_zenith_angle, calc_direct_flux, calc_direct_fluxes |
| FastJX_interpolation_troposphere | `src/interpolations_FastJX.jl:98` | Model | variables, parameters, equations, registered_function calls (flux_interp_1..18) | **gt-p3ep(lookup)** | L | Y | Y | `components/gaschem/fastjx/fastjx_interp_troposphere.esm` | flux_interp_1..18 |
| cos_solar_zenith_angle | `src/Fast-JX.jl:1049` | Interface | @register_symbolic | gt-p3ep(lookup) | S | Y | Y | `registered_functions/cos_solar_zenith_angle` | — |
| calc_direct_flux | `src/Fast-JX.jl:1065` | Interface | @register_symbolic | gt-p3ep(lookup) | S | Y | Y | `registered_functions/calc_direct_flux` | — |
| calc_direct_fluxes | `src/Fast-JX.jl:1082` | Interface | @register_symbolic | gt-p3ep(lookup) | S | Y | Y | `registered_functions/calc_direct_fluxes` | — |
| flux_interp_1..18 | `src/interpolations_FastJX.jl:36-53` | Interface | @register_symbolic (one per reaction channel) | gt-p3ep(lookup) | S each | Y | Y | `registered_functions/flux_interp_{1..18}` | — |

### 9.3 Fast-JX couplings

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| FastJX ↔ SuperFast coupling | `src/fastjx_couplings.jl:3` | Coupling | `param_to_var` of photolysis rate params into chemistry | gt-p3ep (inherits from FastJX) | M | Y | Y | `couplings/fastjx_superfast.esm` | FastJX, SuperFast |
| FastJX ↔ GEOSChemGasPhase coupling | `src/fastjx_couplings.jl:88` | Coupling | `param_to_var` of photolysis rate params | gt-p3ep (inherits) | M | Y | Y | `couplings/fastjx_geoschem.esm` | FastJX, GEOSChemGasPhase |
| FastJX ↔ (third system) coupling | `src/fastjx_couplings.jl:113` | Coupling | `param_to_var` | gt-p3ep (inherits) | M | Y | Y | `couplings/fastjx_other.esm` | FastJX |

### 9.4 @component models (all `none`)

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| NOxPhotochemistry | `src/nox_photochemistry.jl:88` | Model | variables, parameters, equations | none | M | Y | Y | `components/gaschem/nox_photochemistry/photochemistry.esm` | — |
| PhotostationaryState | `src/nox_photochemistry.jl:145` | Model | variables, parameters, observed | none | S | Y | Y | `components/gaschem/nox_photochemistry/photostationary.esm` | — |
| AtmosphericBudget | `src/AtmosphericLifetime.jl:64` | Model | variables, parameters, equations | none | S | Y | Y | `components/gaschem/lifetime/atmospheric_budget.esm` | — |
| SpeciesLifetime | `src/AtmosphericLifetime.jl:132` | Model | variables, parameters, observed | none | S | Y | Y | `components/gaschem/lifetime/species_lifetime.esm` | — |
| MultipleRemovalLifetime | `src/AtmosphericLifetime.jl:204` | Model | variables, parameters, observed | none | S | Y | Y | `components/gaschem/lifetime/multiple_removal.esm` | — |
| OHReactionLifetime | `src/AtmosphericLifetime.jl:264` | Model | variables, parameters, observed | none | S | Y | Y | `components/gaschem/lifetime/oh_reaction.esm` | — |
| TroposphericBudget | `src/AtmosphericLifetime.jl:336` | Model | variables, parameters, equations | none | M | Y | Y | `components/gaschem/lifetime/tropospheric_budget.esm` | — |
| COOxidation | `src/co_oxidation.jl:88` | Model | variables, parameters, equations | none | S | Y | Y | `components/gaschem/co_oxidation/co_oxidation.esm` | — |
| OzoneProductionEfficiency | `src/co_oxidation.jl:183` | Model | variables, parameters, observed | none | S | Y | Y | `components/gaschem/co_oxidation/ope.esm` | — |
| MethaneOxidation | `src/methane_oxidation.jl:77` | Model | variables, parameters, equations | none | M | Y | Y | `components/gaschem/methane/methane_oxidation.esm` | — |
| MethaneOxidationODE | `src/methane_oxidation.jl:213` | Model | variables, parameters, equations | none | M | Y | Y | `components/gaschem/methane/methane_ode.esm` | — |
| OHProduction | `src/oh_production.jl:88` | Model | variables, parameters, equations | none | M | Y | Y | `components/gaschem/oh_production.esm` | — |
| ClimateFeedback | `src/climate_forcing.jl:32` | Model | variables, parameters, observed | none | S | Y | N | `components/gaschem/climate/feedback.esm` | — |
| GHGForcing | `src/climate_forcing.jl:104` | Model | variables, parameters, observed | none | S | Y | N | `components/gaschem/climate/ghg_forcing.esm` | — |
| GlobalWarmingPotential | `src/climate_forcing.jl:182` | Model | variables, parameters, observed | none | S | Y | N | `components/gaschem/climate/gwp.esm` | — |
| PhotonEnergy | `src/radiation_fundamentals.jl:25` | Model | variables, parameters, observed | none | S | Y | Y | `components/gaschem/radiation/photon_energy.esm` | — |
| BlackbodyRadiation | `src/radiation_fundamentals.jl:73` | Model | variables, parameters, observed | none | S | Y | Y | `components/gaschem/radiation/blackbody.esm` | — |
| WienDisplacement | `src/radiation_fundamentals.jl:121` | Model | variables, parameters, observed | none | S | Y | Y | `components/gaschem/radiation/wien.esm` | — |
| StefanBoltzmann | `src/radiation_fundamentals.jl:164` | Model | variables, parameters, observed | none | S | Y | Y | `components/gaschem/radiation/stefan_boltzmann.esm` | — |
| PlanetaryEnergyBalance | `src/radiation_fundamentals.jl:211` | Model | variables, parameters, equations | none | M | Y | Y | `components/gaschem/radiation/planetary_energy_balance.esm` | — |
| ClimateSensitivity | `src/radiation_fundamentals.jl:268` | Model | variables, parameters, observed | none | S | Y | Y | `components/gaschem/radiation/climate_sensitivity.esm` | — |
| TOARadiativeForcing | `src/radiation_fundamentals.jl:327` | Model | variables, parameters, observed | none | S | Y | Y | `components/gaschem/radiation/toa_radiative_forcing.esm` | — |
| RadiationFundamentals | `src/radiation_fundamentals.jl:367` | Model | variables, parameters, coupling.couple | none | M | Y | Y | `components/gaschem/radiation/radiation_fundamentals.esm` | PhotonEnergy, BlackbodyRadiation, WienDisplacement, StefanBoltzmann, PlanetaryEnergyBalance |
| ChapmanMechanism | `src/StratosphericChemistry.jl:51` | Model | variables, parameters, equations | none | M | Y | Y | `components/gaschem/stratospheric/chapman.esm` | — |
| NOxCycle | `src/StratosphericChemistry.jl:118` | Model | variables, parameters, equations | none | M | Y | Y | `components/gaschem/stratospheric/nox_cycle.esm` | — |
| HOxCycle | `src/StratosphericChemistry.jl:187` | Model | variables, parameters, equations | none | M | Y | Y | `components/gaschem/stratospheric/hox_cycle.esm` | — |
| ClOxCycle | `src/StratosphericChemistry.jl:272` | Model | variables, parameters, equations | none | M | Y | Y | `components/gaschem/stratospheric/clox_cycle.esm` | — |
| BrOxCycle | `src/StratosphericChemistry.jl:390` | Model | variables, parameters, equations | none | M | Y | Y | `components/gaschem/stratospheric/brox_cycle.esm` | — |
| StratosphericOzoneSystem | `src/StratosphericChemistry.jl:497` | Model | variables, parameters, coupling.couple | none | L | Y | Y | `components/gaschem/stratospheric/stratospheric_ozone_system.esm` | ChapmanMechanism, NOxCycle, HOxCycle, ClOxCycle, BrOxCycle |
| TroposphericChemistrySystem | `src/combined_system.jl:54` | Model | variables, parameters, coupling.couple | none | L | Y | Y | `components/gaschem/combined/tropospheric_chemistry.esm` | NOxPhotochemistry, MethaneOxidation, OHProduction, COOxidation |
| TypicalConditions | `src/combined_system.jl:177` | Model | parameters preset | none | S | Y | Y | `components/gaschem/combined/typical.esm` | — |
| UrbanConditions | `src/combined_system.jl:219` | Model | parameters preset | none | S | Y | Y | `components/gaschem/combined/urban.esm` | — |
| RemoteConditions | `src/combined_system.jl:261` | Model | parameters preset | none | S | Y | Y | `components/gaschem/combined/remote.esm` | — |

---

## 10. Geodynamics.jl (2 components)

Repo purpose: volcanic source models (Mogi / McTigue) — algebraic elastic halfspace solutions.

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| MogiModel | `src/mogi_mctigue.jl:48` | Model | variables, parameters, equations (algebraic only — no D(x)) | **gt-ebuq(init_eq/system_kind=nonlinear)** | S | Y | Y | `components/geodynamics/mogi.esm` | — |
| McTigueModel | `src/mogi_mctigue.jl:107` | Model | variables, parameters, equations (algebraic only) | **gt-ebuq(init_eq/system_kind=nonlinear)** | S | Y | Y | `components/geodynamics/mctigue.esm` | — |

---

## 11. OceanDynamics.jl (0 components)

Repo purpose: ocean dynamics (placeholder — no `src/` on the pinned commit).

**Classification:** Empty. Deferred. No migration target.

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| (none) | — | — | — | other:empty-no-src | — | — | — | — | — |

---

## 12. UrbanCanopy.jl (45 components)

Repo purpose: CLMU-style urban canopy (roof/wall/road thermal conduction, snow, hydrology, radiation fluxes, waste heat).

**Notes:** Several components (`BuildingTemperature`, `PhaseChangeAdjustment`, `SoilWaterFlux`) internally call `PDESystem` + `MOLFiniteDifference` + `discretize` at MTK-build time and return an ODE-ified system. ESM `Domain` schema doesn't encode the MOL discretization plan — classified as `other:discretization-plan` (gt-dq0f). The pdesys lines are at `src/roof_wall_road_snow_temperatures.jl:1152,1227` and `src/hydrology.jl:674`.

### 12.1 urban_canopy_model.jl / clmu_introduction.jl / offline_mode.jl / heat_momentum_fluxes.jl / albedos_radiative_fluxes.jl (5)

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| UrbanCanopyModel | `src/urban_canopy_model.jl:41` | Model | variables, parameters, coupling.couple, coupling.param_to_var | none | XL | Y | Y | `components/urban_canopy/urban_canopy_model.esm` | ~30 sub-components |
| CLMUAtmosphere | `src/clmu_introduction.jl:22` | Model | variables, parameters, observed | none | M | Y | Y | `components/urban_canopy/clmu_atmosphere.esm` | — |
| OfflineModeForcing | `src/offline_mode.jl:33` | Model | variables, parameters, observed | none | M | Y | Y | `components/urban_canopy/offline_mode_forcing.esm` | — |
| HeatMomentumFluxes | `src/heat_momentum_fluxes.jl:26` | Model | variables, parameters, equations | none | L | Y | Y | `components/urban_canopy/heat_momentum_fluxes.esm` | — |
| UrbanRadiation | `src/albedos_radiative_fluxes.jl:27` | Model | variables, parameters, equations | none | L | Y | Y | `components/urban_canopy/urban_radiation.esm` | — |

### 12.2 roof_wall_road_snow_temperatures.jl (21 components; 2 use in-fn PDESystem)

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| SnowLayerGeometry | `src/roof_wall_road_snow_temperatures.jl:33` | Model | variables, parameters, observed | none | S | Y | Y | `components/urban_canopy/temps/snow_layer_geometry.esm` | — |
| SoilThermalProperties | `:75` | Model | variables, parameters, observed | none | S | Y | Y | `components/urban_canopy/temps/soil_thermal.esm` | — |
| SnowThermalProperties | `:190` | Model | variables, parameters, observed | none | S | Y | Y | `components/urban_canopy/temps/snow_thermal.esm` | — |
| UrbanSurfaceThermalProperties | `:245` | Model | variables, parameters, observed | none | S | Y | Y | `components/urban_canopy/temps/urban_surface_thermal.esm` | — |
| InterfaceThermalConductivity | `:278` | Model | variables, parameters, observed | none | S | Y | Y | `components/urban_canopy/temps/interface_thermal_conductivity.esm` | — |
| HeatFlux | `:312` | Model | variables, parameters, observed | none | S | Y | Y | `components/urban_canopy/temps/heat_flux.esm` | — |
| SurfaceEnergyFlux | `:347` | Model | variables, parameters, equations | none | M | Y | Y | `components/urban_canopy/temps/surface_energy_flux.esm` | — |
| BuildingTemperature | `:401` | Model | variables, parameters, equations; internally builds a 1D PDE (`@named pdesys` at `:1152`) via MOLFiniteDifference | **other:discretization-plan** | L | Y | Y | `components/urban_canopy/temps/building_temperature.esm` | — |
| WasteHeatAirConditioning | `:440` | Model | variables, parameters, equations | none | M | Y | Y | `components/urban_canopy/temps/waste_heat_ac.esm` | — |
| PhaseChangeEnergy | `:496` | Model | variables, parameters, equations (parameterized `layer_type`) | none | M | Y | Y | `components/urban_canopy/temps/phase_change_energy.esm` | — |
| WasteHeatAllocation | `:561` | Model | variables, parameters, equations | none | M | Y | Y | `components/urban_canopy/temps/waste_heat_allocation.esm` | — |
| AdjustedLayerThickness | `:601` | Model | variables, parameters, observed | none | S | Y | Y | `components/urban_canopy/temps/adjusted_layer_thickness.esm` | — |
| HeatingCoolingFlux | `:638` | Model | variables, parameters, observed | none | S | Y | Y | `components/urban_canopy/temps/heating_cooling_flux.esm` | — |
| PhaseChangeAdjustment | `:686` | Model | variables, parameters, equations; internally builds PDE (`:1227`) via MOLFiniteDifference | **other:discretization-plan** | L | Y | Y | `components/urban_canopy/temps/phase_change_adjustment.esm` | — |
| SnowMeltNoLayers | `:773` | Model | variables, parameters, equations | none | M | Y | Y | `components/urban_canopy/temps/snow_melt_no_layers.esm` | — |
| UniformGrid | `:830` | Model | variables, parameters (parameterized `N`) | none | S | Y | Y | `components/urban_canopy/temps/uniform_grid.esm` | — |
| ExponentialGrid | `:890` | Model | variables, parameters (parameterized `N`) | none | S | Y | Y | `components/urban_canopy/temps/exponential_grid.esm` | — |
| FreezingPointDepression | `:949` | Model | variables, parameters, observed | none | S | Y | Y | `components/urban_canopy/temps/freezing_point_depression.esm` | — |
| SnowSoilBlendedHeatCapacity | `:1003` | Model | variables, parameters, observed | none | S | Y | Y | `components/urban_canopy/temps/snow_soil_blended_heat_capacity.esm` | — |
| LayerPhaseChangeEnergy | `:1037` | Model | variables, parameters, observed | none | S | Y | Y | `components/urban_canopy/temps/layer_phase_change_energy.esm` | — | **status: complete, sha: 1c3d5fe6af317c23ad14b3deaacdd50bf324672f** (mdl-sqzs; observed-only single-equation algebraic component implementing Oleson (2010) CLM Tech Note Ch. 4 Eq. 4.73 per-layer phase-change energy E_p = L_f · (w_ice_n − w_ice_np1) / Δt — 4 parameters (w_ice_n, w_ice_np1, Δt, L_f = 3.337e5 J/kg from Oleson Table 1.4) and 1 algebraic state output (E_p), tolerance rel=1e-9 with abs=1e-12 on exact-zero outputs; 7 inline tests / 7 assertions reproducing the two upstream `roof_wall_road_snow_temperatures_test.jl` Julia tests (`:1200` Melting at w_ice_n=10, w_ice_np1=8, Δt=3600 → 185.389 W/m²; `:1224` No Change at w_ice_n=w_ice_np1=10 → 0) plus 5 regime cases (freezing_branch sign check at w_ice_np1>w_ice_n, complete_melt_short_dt at Δt=1800, small_mass_short_dt at thin-film/sub-cycling Δt=60, daily_step at Δt=86400, all_zero divide-by-zero/NaN guard at default Δt=1) exercising Eq. 4.73 across the physical range; 2 parameter-sweep examples (E_p_curve_vs_w_ice_np1 line over w_ice_np1 ∈ [0, 20] at fixed w_ice_n=10/Δt=3600 surfacing the linear zero-crossing at w_ice_np1=w_ice_n, and two_d_sweep_dw_dt heatmap over (w_ice_np1, Δt) surfacing the inverse-Δt scaling); column-summed output of this component feeds `TotalPhaseChangeEnergy` (Eq. 4.72); tracker-sync esm-4881 — work landed under mdl-sqzs but the row had no completion marker) |
| TotalPhaseChangeEnergy | `:1071` | Model | variables, parameters, observed | none | S | Y | Y | `components/urban_canopy/temps/total_phase_change_energy.esm` | — | **status: complete, sha: 84464eb885c96580327bd27f5449cecdbe4bec8b** (mdl-qzxo; observed-only single-equation algebraic component implementing Oleson (2010) CLM Tech Note Eq. 4.72 column-total phase change energy E_p_total = E_p1S + E_p_layers — additive identity aggregating surface snow melt energy (Eq. 4.71, from SnowMeltNoLayers) and column-summed per-layer phase change energies (Eq. 4.73, from LayerPhaseChangeEnergy column-sum); 2 parameters (E_p1S, E_p_layers in W/m^2), 1 algebraic state (E_p_total in W/m^2), 7 inline tests / 7 assertions reproducing the upstream `roof_wall_road_snow_temperatures_test.jl:1254` Equation-Verification testitem (upstream_equation_verification at E_p1S=50, E_p_layers=30 → 80) plus 6 boundary/qualitative cases (all_zero_inputs, surface_only, layers_only, freezing_branch with negative inputs, mixed_sign_cancellation crossing zero, high_magnitude peak-melt regime), 2 parameter-sweep examples (total_vs_surface_with_layer_offset line over E_p1S ∈ [-200, 1500] W/m^2 at fixed E_p_layers=50 and two_d_sweep_surface_layers heatmap over (E_p1S, E_p_layers) ∈ [-500, 1500] × [-500, 1000] W/m^2); tracker-sync esm-ej47 — work landed under mdl-qzxo but the row had no completion marker) |

### 12.3 hydrology.jl (19 components; 1 uses in-fn PDESystem)

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| SnowDensity | `src/hydrology.jl:25` | Model | variables, parameters, observed | none | S | Y | Y | `components/urban_canopy/hydro/snow_density.esm` | — | **status: complete, sha: 7b6e6343c4f2fad14d35cb71953c82bda4d680f3** (mdl-7htw; observed-only single-equation algebraic component implementing Anderson (1976) / Oleson (2010) CLM Tech Note Eq. 5.10 piecewise new-snow bulk density — 9 parameters (T_atm input, T_f = 273.15 K, one_K unit-balancer, rho_base = 50 kg/m^3, rho_coeff = 1.7 kg/m^3, rho_warm = 169.158 kg/m^3 precomputed warm-side plateau, T_offset = 15 K, T_thresh_high = 2 K, T_thresh_low = -15 K), 1 algebraic state (rho_sno), 9 inline tests / 9 assertions reproducing the upstream `SnowDensity - Equation Verification` testitem (hydrology_test.jl:351) — five canonical cases (warm-branch at upper threshold T_f+2, cold-branch well below, intermediate mid-range T_f-5, cold-branch at lower threshold T_f-15, warm-branch just-above) plus four boundary/qualitative cases (intermediate at exactly T_f, intermediate just above lower threshold, warm extreme 310 K, cold extreme 200 K), 1 parameter-sweep example (rho_sno_vs_T_atm_full_curve line sweep 240-280 K, 41 points, surfacing the three-regime cold-floor → (...)^1.5 ramp → warm-plateau structure); tracker-sync esm-hzmn — work landed under mdl-7htw but the row had no completion marker) |
| SnowIceContent | `:79` | Model | variables, parameters, equations | none | S | Y | Y | `components/urban_canopy/hydro/snow_ice_content.esm` | — | **status: complete, sha: 7681a447dd28d53525bbb1c831d327b2e0275c78** (mdl-hbhf; observed-only algebraic ice-mass-conservation component implementing Oleson (2010) CLM4 Tech Note Ch. 5 §5.1.1 Eqs. 5.7 and 5.9 — 4 parameters (q_grnd_ice, q_frost, q_subl, rho_sno) and 2 algebraic state outputs (dz_sno_dt = q_grnd_ice/rho_sno; q_ice_top = q_grnd_ice + (q_frost − q_subl)), tolerance rel=1e-9; 5 inline tests / 10 assertions reproducing the upstream `hydrology_test.jl:387` Equation-Verification testitem (default_canonical_rates) plus 4 regime cases (heavy_snowfall_dense_snow, sublimation_dominates, frost_only, light_snow_low_density) exercising both equations across the physical range; tracker-sync esm-4mv2 — work landed under mdl-hbhf but the row had no completion marker) |
| SnowWaterContent | `:119` | Model | variables, parameters, equations | none | S | Y | Y | `components/urban_canopy/hydro/snow_water_content.esm` | — |
| SnowCompaction | `:174` | Model | variables, parameters, equations | none | M | Y | Y | `components/urban_canopy/hydro/snow_compaction.esm` | — |
| SnowLayerCombination | `:253` | Model | variables, parameters, equations | none | M | Y | Y | `components/urban_canopy/hydro/snow_layer_combination.esm` | — |
| SoilHydraulicProperties | `:322` | Model | variables, parameters, observed | none | S | Y | Y | `components/urban_canopy/hydro/soil_hydraulic_properties.esm` | — |
| SurfaceRunoffInfiltration | `:384` | Model | variables, parameters, equations | none | M | Y | Y | `components/urban_canopy/hydro/surface_runoff_infiltration.esm` | — |
| SoilWaterFlux | `:471` | Model | variables, parameters, observed | none | S | Y | Y | `components/urban_canopy/hydro/soil_water_flux.esm` | — |
| SoilWaterEquilibrium | `:509` | Model | variables, parameters, equations; internally builds Richards-eq PDE (`:674`) via MOLFiniteDifference | **other:discretization-plan** | L | Y | Y | `components/urban_canopy/hydro/soil_water_equilibrium.esm` | — |
| GroundwaterDrainage | `:698` | Model | variables, parameters, observed | none | S | Y | Y | `components/urban_canopy/hydro/groundwater_drainage.esm` | — | **status: complete, sha: 76d9b5d1d8d8f63c1a4f8d93a9c1dd8ec280add8** (mdl-0sq3; observed-only two-equation algebraic component implementing Oleson (2010) CLM Tech Note Eqs. 5.140 (sub-surface drainage q_drai = (1 − f_imp)·q_drai_max·exp(−f_drai·z_v)) and 5.141 (impermeable fraction f_imp = max((exp(−α(1 − f_ice_weighted)) − exp(−α))/(1 − exp(−α)), 0)) — 5 parameters (z_v, f_ice_weighted, f_drai = 2.5 m⁻¹, q_drai_max = 5.5e-3 kg/(m²·s), α = 3.0), 2 algebraic states (f_imp, q_drai), 11 inline tests / 22 assertions reproducing the upstream `hydrology_test.jl:519` Equation-Verification testitem (shallow_unfrozen, fully_frozen, surface_unfrozen) plus 8 boundary/qualitative cases (deep_unfrozen, half_frozen, moderate_depth_unfrozen, quarter_frozen_shallow, three_quarter_frozen, shallow_partial_frozen, very_deep_unfrozen, typical_clmu_state), 3 parameter-sweep examples (q_drai_vs_z_v line over z_v ∈ [0, 5] m, f_imp_vs_f_ice line over f_ice_weighted ∈ [0, 1], and q_drai_2d heatmap over (z_v, f_ice_weighted)); tracker-sync esm-87ku — work landed under mdl-0sq3 but the row had no completion marker) |
| WaterTableDepth | `:743` | Model | variables, parameters, observed | none | S | Y | Y | `components/urban_canopy/hydro/water_table_depth.esm` | — | **status: complete, sha: 957d414386449a23f30d7d39316a08a0df7e290f** (mdl-frzb; observed-only single-equation Oleson (2010) CLM Tech Note Eq. 5.146 water-table depth z_v = max(z_v_min, min(z_v_max, z_h_bottom + z_offset − W_a/(ρ_liq·S_y))) with hard clamps at z_v_min = 0.05 m and z_v_max = 80 m — 7 parameters (S_y, z_v_min, z_v_max, z_offset, ρ_liq, z_h_bottom, W_a), 1 algebraic state (z_v), 7 inline tests / 7 assertions reproducing the upstream `hydrology_test.jl:486` Equation-Verification testitem (canonical_unclamped, min_clamp_active, no_aquifer_water) plus 4 boundary/qualitative cases (max_clamp_active, shallow_column_partial_aquifer, monotone_W_a_decreases_z_v, exact_min_clamp_boundary), 2 parameter-sweep examples (z_v_vs_W_a line over W_a ∈ [0, 6000] kg/m² and z_v_vs_W_a_and_z_h_bottom heatmap over (W_a, z_h_bottom)); tracker-sync esm-dqqd — work landed under mdl-frzb but the row had no completion marker) |
| AquiferWaterBalance | `:791` | Model | variables, parameters, equations | none | S | Y | Y | `components/urban_canopy/hydro/aquifer_water_balance.esm` | — | **status: complete, sha: d2297b09a4c56970cf668b7392bc2fb69a22bb8c** (mdl-jocz; 8 tests, 2 examples) |
| SnowCappingRunoff | `:823` | Model | variables, parameters, observed | none | S | Y | Y | `components/urban_canopy/hydro/snow_capping_runoff.esm` | — | **status: complete, sha: 004db417096053b35b732ad67306d551799f3344** (mdl-rhiv; 10 tests / 20 assertions, 2 examples) |
| SurfaceLayerUpdate | `:860` | Model | variables, parameters, equations | none | S | Y | Y | `components/urban_canopy/hydro/surface_layer_update.esm` | — | **status: complete, sha: 16d384c34455ecef629aabcdfc2b78696be6a0e4** (mdl-bylo; 9 tests / 27 assertions, 2 examples) |
| PerviousRoadWaterBalance | `:900` | Model | variables, parameters, equations | none | S | Y | Y | `components/urban_canopy/hydro/pervious_road_water_balance.esm` | — | **status: complete, sha: 37f674f9ff071983779ce7d1f13b4692b24220db** (mdl-c9nr; observed-only single-equation Oleson (2010) Eq. 5.1 pervious-road column water balance — 7 parameters (q_rain, q_sno, E_prvrd, q_over, q_drai, q_rgwl, q_snwcp_ice), 1 algebraic state (water_input = (q_rain + q_sno) − (E_prvrd + q_over + q_drai + q_rgwl + q_snwcp_ice)), 11 inline tests / 11 assertions reproducing the upstream `hydrology_test.jl:765` equation-verification testitem plus 10 boundary cases (all-zero, pure-rain, pure-snow, pure-evaporation, drainage-dominant-dry, snow-capping-loss-only, gains-balance-losses, heavy-storm-no-losses, all-loss-channels-active, mixed-storm-with-losses), 2 parameter-sweep examples (water_input-vs-q_rain line and water_input heatmap over (q_rain, q_over)); tracker-sync esm-m61n — work landed under mdl-c9nr but the row had no completion marker) |
| ImperviousWaterBalance | `:937` | Model | variables, parameters, equations | none | S | Y | Y | `components/urban_canopy/hydro/impervious_water_balance.esm` | — | **status: complete, sha: 56de56619ab6c379bd8963ea2153abc19a42330f** (mdl-fa2p; 10 tests / 30 assertions, 2 examples) |
| ImperviousRunoff | `:991` | Model | variables, parameters, observed | none | S | Y | Y | `components/urban_canopy/hydro/impervious_runoff.esm` | — | **status: complete, sha: e06699287b8d190bff4d814e5634be3e770d7361** (mdl-eggn; observed-only Oleson (2010) Eqs. 5.47-5.48 impervious-surface runoff and surface-water update with no-snow ponding logic and snow-present pass-through — 8 parameters (w_liq_1, q_liq_0, q_seva, has_snow flag, w_pond_max = 1.0 kg/m^2, and three unit-balancing literals zero_kgpm2s/zero_kgpm2/one_s), 3 algebraic states (q_over_nosnow, q_over, w_liq_1_new), 11 inline tests / 29 assertions reproducing the three upstream `hydrology_test.jl` cases plus 8 boundary cases (dry/idle, evaporation-only/overshoots, exactly-at and just-above the ponding limit, heavy rain with and without snow, snow-no-input), 2 parameter-sweep examples (q_over-vs-q_liq_0 line and w_liq_1_new heatmap over (w_liq_1, q_liq_0)); tracker-sync esm-10av — work landed under mdl-eggn but the row had no completion marker) |
| InterfaceHydraulicConductivity | `:1053` | Model | variables, parameters, observed | none | S | Y | Y | `components/urban_canopy/hydro/interface_hydraulic_conductivity.esm` | — | **status: complete, sha: 7e3c92e5fe83b32cdaac3d01757cfe6e0b3d3398** (mdl-u7xc; observed-only Oleson (2010) Eq. 5.69 interface hydraulic conductivity with Eq. 5.70 frozen-fraction reduction — 8 parameters, 1 algebraic state k_h, 10 inline assertions covering saturation/half-sat/fully-frozen/asymmetric layers/CLMU mid-column scenario, 2 parameter-sweep examples; tracker-sync esm-erg8 — work landed under mdl-u7xc but the row had no completion marker) |
| SoilWaterContentCalc | `:1091` | Model | variables, parameters, observed | none | S | Y | Y | `components/urban_canopy/hydro/soil_water_content_calc.esm` | — | **status: complete, sha: 36ed4052bae0915f4ed872a575c5a9dc347aea91** (mdl-mw6c; 10 tests / 10 assertions, 2 examples) |

---

## 13. Vegetation.jl (3 components)

Repo purpose: forest growth models (LANDIS biomass, Stage 1973 stochastic growth).

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| StagePrognosis | `src/stage_prognosis.jl:29` | Model | variables, parameters, equations, **@brownians B_growth** | **gt-kuxo(brownian)** | L | Y | Y | `components/vegetation/stage_prognosis.esm` | — |
| StagePrognosisHCB | `src/stage_prognosis.jl:257` | Model | variables, parameters, equations (pure algebraic; no D(x)) | **gt-ebuq(init_eq/system_kind=nonlinear)** | S | Y | Y | `components/vegetation/stage_prognosis_hcb.esm` | — |
| LANDISBiomass | `src/landis_biomass.jl:28` | Model | variables, parameters, equations | none | M | Y | Y | `components/vegetation/landis_biomass.esm` | — |

---

## 14. WildlandFire.jl (36 components + 1 PDE + 6 fuel-table registered fns)

Repo purpose: fire spread (Rothermel, Clark 1996 coupling, elliptical), NFDRS fuel moisture/fire-danger indices, FSIM fire-occurrence statistics, level-set fire spread PDE.

### 14.1 Fuel model lookup tables (all `gt-p3ep`)

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| fuel_savr | `src/coupling.jl:123` | Interface | @register_symbolic | gt-p3ep(lookup) | S | Y | Y | `registered_functions/fuel_savr` | — |
| fuel_load | `src/coupling.jl:124` | Interface | @register_symbolic | gt-p3ep(lookup) | S | Y | Y | `registered_functions/fuel_load` | — |
| fuel_depth | `src/coupling.jl:125` | Interface | @register_symbolic | gt-p3ep(lookup) | S | Y | Y | `registered_functions/fuel_depth` | — |
| fuel_mce | `src/coupling.jl:126` | Interface | @register_symbolic | gt-p3ep(lookup) | S | Y | Y | `registered_functions/fuel_mce` | — |
| fuel_heat | `src/coupling.jl:127` | Interface | @register_symbolic | gt-p3ep(lookup) | S | Y | Y | `registered_functions/fuel_heat` | — |
| fuel_weight | `src/coupling.jl:128` | Interface | @register_symbolic | gt-p3ep(lookup) | S | Y | Y | `registered_functions/fuel_weight` | — |
| FuelModelLookup | `src/coupling.jl:155` | Model | variables, parameters, observed, registered_function calls (fuel_*) | gt-p3ep(lookup) | M | Y | Y | `components/wildland_fire/fuel_model_lookup.esm` | fuel_savr, fuel_load, fuel_depth, fuel_mce, fuel_heat, fuel_weight |
| TerrainSlope | `src/coupling.jl:205` | Model | variables, parameters, observed | none | S | Y | Y | `components/wildland_fire/terrain_slope.esm` | — | **status: complete, sha: 944d4abbb79c142e809168fbd8ef2398d6148f1d** (mdl-kh9; 11 tests / 44 assertions, 2 examples) |
| MidflameWind | `src/coupling.jl:249` | Model | variables, parameters, observed | none | S | Y | Y | `components/wildland_fire/midflame_wind.esm` | — | **status: complete, sha: f13a61c1e87b001c7ad4cd9c52ec6bf886260106** (mdl-017v; observed-only 10 m → midflame-height wind conversion (U, omega, u_mf_x, u_mf_y) with default 0.4 Baughman & Albini (1980) timber-fuel reduction factor, 9 tests / 35 assertions, 2 examples; tracker-sync esm-igut — work landed under mdl-017v but the row had no completion marker) |

### 14.2 PDE: level set fire spread

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| LevelSetFireSpread | `src/level_set_fire_spread.jl:73` | Model | PDESystem, partialderivative_transforms (metric-tensor coord transforms), boundary_conditions | **gt-vzwk(PDE-tests); other:P3-A-metric-tensor-coord-transforms** | XL | Y | Y | `components/wildland_fire/level_set_fire_spread.esm` | — |
| FuelConsumption | `src/level_set_fire_spread.jl:243` | Model | variables, parameters, equations | none | S | Y | Y | `components/wildland_fire/level_set/fuel_consumption.esm` | — | **status: complete, sha: f817edbc9d9945003a446197c5ba5c6f3bf7ac02** (mdl-r2s6; Mandel et al. 2011 Eq. 3 fuel-fraction decay D(F) = -is_burning*F/T_f + algebraic w0_effective = F*w0_initial, 5 tests / 24 assertions, 2 examples; tracker-sync esm-arm7 — work landed under mdl-r2s6 but the row had no completion marker) |
| FireHeatFlux | `src/level_set_fire_spread.jl:295` | Model | variables, parameters, equations | none | S | Y | Y | `components/wildland_fire/level_set/fire_heat_flux.esm` | — | **status: complete, sha: b1d5dfa60ff412f6010aa73a8c221ed93f5a2cf7** (mdl-gwf7; observed-only Mandel et al. (2011) Eqs. 4–5 sensible/latent heat flux, 7 tests / 14 assertions, 2 examples; tracker-sync esm-d4ed — work landed under mdl-gwf7 but the row had no completion marker) |

### 14.3 Clark 1996 (4, `none`)

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| Clark1996FireSpread | `src/clark1996.jl:81` | Model | variables, parameters, equations | none | L | Y | Y | `components/wildland_fire/clark1996/fire_spread.esm` | — |
| Clark1996HeatFluxProfile | `src/clark1996.jl:206` | Model | variables, parameters, observed | none | S | Y | Y | `components/wildland_fire/clark1996/heat_flux_profile.esm` | — | **status: complete, sha: d577ebec344c123a171e28304909e6c82442fafe** (mdl-y7ew; observed-only F_s/F_l = F_sfc · exp(−z/alpha_ext), 9 tests / 18 assertions, 2 examples; tracker-sync esm-if7u — work landed under mdl-y7ew but the row had no completion marker) |
| Clark1996ConvectiveFroudeNumber | `src/clark1996.jl:253` | Model | variables, parameters, observed | none | S | Y | Y | `components/wildland_fire/clark1996/froude.esm` | — |
| Clark1996WindProfile | `src/clark1996.jl:299` | Model | variables, parameters, observed | none | S | Y | Y | `components/wildland_fire/clark1996/wind_profile.esm` | — |

### 14.4 Rothermel (5, `none`)

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| RothermelFireSpread | `src/rothermel.jl:70` | Model | variables, parameters, equations, coupling.couple | none | XL | Y | Y | `components/wildland_fire/rothermel/fire_spread.esm` | FuelModelLookup, TerrainSlope, MidflameWind |
| DynamicFuelLoadTransfer | `src/rothermel.jl:320` | Model | variables, parameters, equations | none | S | Y | Y | `components/wildland_fire/rothermel/dynamic_fuel_load_transfer.esm` | — |
| LiveFuelMoistureExtinction | `src/rothermel.jl:367` | Model | variables, parameters, observed | none | S | Y | Y | `components/wildland_fire/rothermel/live_fuel_moisture_extinction.esm` | — |
| EffectiveMidflameWindSpeed | `src/rothermel.jl:410` | Model | variables, parameters, observed | none | S | Y | Y | `components/wildland_fire/rothermel/effective_midflame_wind.esm` | — |
| WindLimit | `src/rothermel.jl:465` | Model | variables, parameters, observed (parameterized `use_corrected`) | none | S | Y | Y | `components/wildland_fire/rothermel/wind_limit.esm` | — |

### 14.5 NFDRS (14, `none`)

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| EquilibriumMoistureContent | `src/nfdrs.jl:79` | Model | variables, parameters, observed | none | S | Y | Y | `components/wildland_fire/nfdrs/emc.esm` | — |
| OneHourFuelMoisture | `src/nfdrs.jl:149` | Model | variables, parameters, equations | none | S | Y | Y | `components/wildland_fire/nfdrs/moisture_1h.esm` | — |
| TenHourFuelMoisture | `src/nfdrs.jl:207` | Model | variables, parameters, equations | none | S | Y | Y | `components/wildland_fire/nfdrs/moisture_10h.esm` | — |
| HundredHourFuelMoisture | `src/nfdrs.jl:279` | Model | variables, parameters, equations | none | S | Y | Y | `components/wildland_fire/nfdrs/moisture_100h.esm` | — |
| ThousandHourFuelMoisture | `src/nfdrs.jl:354` | Model | variables, parameters, equations | none | S | Y | Y | `components/wildland_fire/nfdrs/moisture_1000h.esm` | — |
| HerbaceousFuelMoisture | `src/nfdrs.jl:426` | Model | variables, parameters, equations | none | M | Y | Y | `components/wildland_fire/nfdrs/herbaceous_moisture.esm` | — |
| WoodyFuelMoisture | `src/nfdrs.jl:562` | Model | variables, parameters, equations | none | M | Y | Y | `components/wildland_fire/nfdrs/woody_moisture.esm` | — |
| FuelLoadingTransfer | `src/nfdrs.jl:655` | Model | variables, parameters, equations | none | M | Y | Y | `components/wildland_fire/nfdrs/fuel_loading_transfer.esm` | — |
| SpreadComponent | `src/nfdrs.jl:731` | Model | variables, parameters, equations | none | L | Y | Y | `components/wildland_fire/nfdrs/spread_component.esm` | — |
| EnergyReleaseComponent | `src/nfdrs.jl:1017` | Model | variables, parameters, equations | none | L | Y | Y | `components/wildland_fire/nfdrs/energy_release_component.esm` | — |
| BurningIndex | `src/nfdrs.jl:1231` | Model | variables, parameters, observed | none | S | Y | Y | `components/wildland_fire/nfdrs/burning_index.esm` | — |
| IgnitionComponent | `src/nfdrs.jl:1291` | Model | variables, parameters, equations | none | S | Y | Y | `components/wildland_fire/nfdrs/ignition_component.esm` | — |
| HumanFireOccurrenceIndex | `src/nfdrs.jl:1375` | Model | variables, parameters, equations | none | S | Y | Y | `components/wildland_fire/nfdrs/human_fire_occurrence.esm` | — |
| LightningFireOccurrenceIndex | `src/nfdrs.jl:1422` | Model | variables, parameters, equations | none | S | Y | Y | `components/wildland_fire/nfdrs/lightning_fire_occurrence.esm` | — |
| FireLoadIndex | `src/nfdrs.jl:1605` | Model | variables, parameters, observed | none | S | Y | Y | `components/wildland_fire/nfdrs/fire_load_index.esm` | — |

### 14.6 FSIM (5, `none`) + fire_spread_direction (3, `none`)

| component_name | source_path | kind | features | blocking_gap | complexity | tests | docs | target_path | depends_on |
|---|---|---|---|---|---|---|---|---|---|
| FireOccurrenceLogistic | `src/fsim.jl:53` | Model | variables, parameters, observed | none | S | Y | Y | `components/wildland_fire/fsim/fire_occurrence_logistic.esm` | — |
| FireContainment | `src/fsim.jl:139` | Model | variables, parameters, equations | none | M | Y | Y | `components/wildland_fire/fsim/fire_containment.esm` | — |
| BurnProbability | `src/fsim.jl:231` | Model | variables, parameters, equations | none | L | Y | Y | `components/wildland_fire/fsim/burn_probability.esm` | — |
| ERCTimeSeries | `src/fsim.jl:333` | Model | variables, parameters, equations | none | M | Y | Y | `components/wildland_fire/fsim/erc_time_series.esm` | — |
| FlameLengthCategory | `src/fsim.jl:418` | Model | variables, parameters, observed | none | S | Y | Y | `components/wildland_fire/fsim/flame_length_category.esm` | — |
| FireSpreadDirection | `src/fire_spread_direction.jl:59` | Model | variables, parameters, equations | none | M | Y | Y | `components/wildland_fire/spread_direction/fire_spread_direction.esm` | — |
| EllipticalFireSpread | `src/fire_spread_direction.jl:174` | Model | variables, parameters, equations | none | M | Y | Y | `components/wildland_fire/spread_direction/elliptical_fire_spread.esm` | — |
| FirePerimeterSpread | `src/fire_spread_direction.jl:264` | Model | variables, parameters, equations | none | M | Y | Y | `components/wildland_fire/spread_direction/fire_perimeter_spread.esm` | — |

---

## Recommendations / next steps

1. **Start Phase 2 with the "migrate today" set (215 components)** — these are `none`-blocked `@component` ODE/algebraic models with clean MTK patterns. Suggest prioritizing:
   - AtmosphericDynamics.jl (31 clean) — no dependencies; self-contained textbook physics.
   - AtmosphericDeposition.jl (17 clean SP-ch19/ch20 + 3 Luo2023) — no dependencies on unblocked gaps.
   - GasChem @component models (28 clean) — all radiation/lifetime/stratosphere/methane/NOx/CO paths.
   - Aerosol.jl mass_transfer/single_particle_dynamics/nucleation/organic/sulfate/timescales/cloud chains (65 clean).
   - WildlandFire.jl NFDRS + FSIM + Clark1996 + Rothermel (26 clean, minus FuelModelLookup which depends on fuel_* registered fns).

2. **Queue `gt-p3ep` work** (26 components + all DataLoaders + FastJX + Mie). This single schema addition unblocks EarthSciData entirely + FastJX + Wesley dry dep + fuel lookup + ISORROPIA-II helpers.

3. **Queue `gt-kuxo` + `gt-ebuq`** (7 components total) before attempting Vegetation StagePrognosis, EnvTransport BoundaryLayerMixingKC/Sofiev2012PlumeRise, Geodynamics, and top-level Isorropia.

4. **Defer PDE models to Phase 3** (`gt-vzwk`): LevelSetFireSpread, SurfaceRunoff Saint-Venant, and UrbanCanopy in-function PDE discretizations. These also need `other:discretization-plan` (MOLFiniteDifference spec) resolved.

5. **Spawn follow-up beads (not yet filed)**:
   - `other:P3-A-metric-tensor-coord-transforms` — CoordinateTransform needs optional `forward_expression`/`inverse_expression`/`metric` AST fields.
   - `other:P3-B-BC-symbolic-offset` — `BoundaryCondition.value` should accept Expression, not just number (Puff lateral BC).
   - `other:P2-C-terminate-in-FunctionalAffect` — reserve built-in `handler_id` set (`terminate`, `save`, `reset`) in the spec.
   - `other:discretization-plan` — MOLFiniteDifference / discretization stanza on `Domain` (related to `gt-dq0f`).

6. **Framework bootstrap (not a Phase-2 model migration)**: EarthSciMLBase and EarthSciDiscretizations are not migrated as `.esm` files. They must remain code-form, but their `Operator`/`CoupledSystem`/`DomainInfo`/`MOLFiniteDifference` semantics are the schema's evaluation contract. Any `.esm` file that references an `Operator` by `handler_id` relies on an EarthSciMLBase-registered implementation.

7. **Non-MTK repos** (Emissions.jl, OceanDynamics.jl): not Phase-2 candidates. Emissions.jl migrates only if it adds MTK wrappers later. OceanDynamics.jl has no content.

## Appendix: methodology + repo-level file:line citations

- All SHAs captured from `origin/HEAD` on 2026-04-19 via `git clone --depth=50`.
- Component discovery pattern: `grep -rE "^@component function|^function [A-Z]\w+\([^)]*name\s*=|^@mtkmodel"` in each repo's `src/`.
- Gap-pattern markers per file: `@brownians`, `@register_symbolic`, `PDESystem`, `initialization_eqs|guesses\s*=`, `continuous_events|discrete_events`.
- Each repo's `test/` was spot-checked for `@test`/`isapprox` density to set `has_tests=Y`; `docs/src/` presence drives `has_docs=Y`.
- Where a single file contains a schema-gap pattern, all `@component`s in that file were individually checked against the pattern to decide whether the gap applies to each.
- `target_path` is a *suggestion*, not a fixed path — migrators may reorganize.
