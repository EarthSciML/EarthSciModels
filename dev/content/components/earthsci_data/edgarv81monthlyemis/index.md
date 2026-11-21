---
title: "EDGARv81MonthlyEmis"
slug: "edgarv81monthlyemis"
domains: ["earthsci_data"]
component_types: ["model"]
domain: "earthsci_data"
component_type: "model"
esm_version: "1.0.0"
esm_path: "components/earthsci_data/edgar_v81_monthly.esm"
reference: "https://edgar.jrc.ec.europa.eu/dataset_ap81"
description: "EDGAR v8.1 monthly global air pollutant emissions data loader. Provides surface-layer volumetric emission rate (kg m⁻³ s⁻¹) for lev < 2 (first vertical layer), and zero above. Configured per substance (species) and emission sector at instantiation time via {species} and {sector} URL template substitutions."
tags: ["earthsci_data", "model", "emissions", "anthropogenic", "edgar", "monthly", "data_loader", "surface_flux", "regridding_model"]
---

## Description

EDGAR v8.1 monthly global air pollutant emissions data loader. Provides surface-layer volumetric emission rate (kg m⁻³ s⁻¹) for lev < 2 (first vertical layer), and zero above. Configured per substance (species) and emission sector at instantiation time via {species} and {sector} URL template substitutions.

Supported substances: BC, CO, NH3, NMVOC, NOx, OC, PM10, PM2.5, SO2.
Data spans 2000–2022 at 0.1°×0.1° global resolution, with monthly temporal resolution.

The gt-p3ep (@register_symbolic interp_unsafe) blocking gap is resolved by the data_loaders §8 mechanism: the runtime handles file download, temporal interpolation, and spatial regridding to the model domain; the model equation references the loader variable directly via EDGAR_v81.flx. No registered functions remain in the migrated component.

Equation: emission = ifelse(lev < 2, EDGAR_v81.flx / Δz * scale, 0)
where EDGAR_v81.flx is the emission flux (kg m⁻² s⁻¹) regridded by the runtime from the 0.1°×0.1° EDGAR grid to the model domain, and Δz (default 60 m) is the first-layer height that converts the surface flux to a volumetric rate.

Migrated from EarthSciData.jl@830435a src/edgar_v81_monthly.jl:277 (EDGARv81MonthlyEmis, esm-yp9q).

[esm-3nc.3] Split at 0.7.0 into a pure-I/O loader (edgar_v81_monthly_loader.esm) + this regridding model per RFC pure-io-data-loaders §6/§7; at esm 1.0.0 that file is merged BACK into this one, which now holds both the model and the `EDGAR_v81` data source it consumes. The loader is referenced as the subsystem EDGAR_v81; the surface flux is regridded conservatively (cell-centered emissions).

## Reference

_source_ref: EarthSciData.jl@830435a065f27e99f10bba91107ca1730322cc6b:src/edgar_v81_monthly.jl:277

Upstream constructor EDGARv81MonthlyEmis(substance, sector, domaininfo; scale=1.0, ...) creates an MTK System with:
  - @parameters: lon (rad), lat (rad), lev (1), Δz=60.0 (m), t_ref=get_tref(domaininfo) (s)
  - One DataSetInterpolator per varnames(fileset): builds interp_unsafe equation for each NC variable
  - Equation template (from create_interp_equation with wrapper_f):
      var(t) ~ ifelse(lev < 2, interp_unsafe(data, fit, fi_lon, fi_lat, extrap) * unit_scale / Δz * scale, zero_var)
    where fit = 1 + (t_ref + t - tstart) / tstep
          fi_lon = 1 + (lon - s1start) / s1step
          fi_lat = 1 + (lat - s2start) / s2step
  - discrete_events: build_interp_event fires at monthly tstops to reload data buffers
  - metadata: Dict(CoupleType => EDGARv81MonthlyEmisCoupler, SysDomainInfo => domaininfo)

gt-p3ep resolution: the @register_symbolic interp_unsafe pattern is replaced by the data_loaders §8
mechanism. EDGAR_v81.flx is the loader variable that the runtime regridds from the 0.1°×0.1° EDGAR
grid to the model domain and interpolates in time to t. The runtime implicitly handles the
build_interp_event discrete callbacks based on data_loaders.temporal.frequency = P1M.

Parameter rename: upstream `t` (simulation time relative to t_ref) is implicit; the ESM model
has no independent variable in the variable map since it only contains observed equations.

The variable `emission` corresponds to the observed variable created by the for-loop over
varnames(fileset). For the typical single-variable EDGAR NC file (one flux variable per
substance/sector), there is one observed equation. The variable name in the NC file is 'flx'
(from the _flx_nc.zip filename convention; confirmed by ESS test fixture at
EarthSciAST/pkg/earthsci-ast-py/tests/fixtures/data_loaders/edgar_v81_monthly.esm).

--- esm-3nc.3 pure-IO split ---
This is the regridding-model half of the pure-IO loader migration (RFC pure-io-data-loaders §6/§7, bead esm-3nc.3). The pre-migration edgar_v81_monthly.esm carried both this coupler model AND a co-located data_loaders.EDGAR_v81 block (with the now-removed `spatial` and `regridding` sub-blocks). That loader became, at 0.7.0, the pure-I/O file components/earthsci_data/edgar_v81_monthly_loader.esm, referenced as the subsystem `EDGAR_v81`. At esm 1.0.0 it is the `EDGAR_v81` entry in THIS file's `data_sources`: a data source is not a component, so it neither needs nor may be a subsystem, and the standalone file is gone. The observed `emission` expression still names the field as EDGAR_v81.flx.
Reprojection (RFC §6 step 2): EDGAR's native grid.crs.projection is 'longlat' (geographic WGS84), so the reprojection rule selected by convention is ESD reprojection/longlat.esm (esd-47z.1) — the IDENTITY transform.
Regridding (RFC §6 step 3 / §5.2): the EDGAR flux is a cell-centered scalar → conservative area-weighted overlap join (ESD regridding/conservative_regrid_overlap_join.esm), declared in the model `regrid` block.

Coupler identity: this model was serialized with the model-level field `coupletype: "EDGARv81MonthlyEmisCoupler"`, the EarthSciMLBase `CoupleType` metadata tag naming the Julia coupler struct that `EarthSciMLBase.couple2` dispatches on to find this component's pairwise coupling rules. The esm schema defined `coupletype` only before 0.8.0 ("informational label identifying this system's role in coupling"); 0.8.0 removed it in favour of explicit coupling — `coupling` entries naming components directly, or `coupling_roles` + `coupling_import` in a coupling-library file (esm-spec §10.9–§10.11). esm 1.0.0 has no model-level coupler-identity field, so the tag is recorded here to keep it recoverable.

Regridding intent: this model was serialized with the model-level `regrid` map, one entry per variable naming the kernel that carries the loaded native-grid field onto the consuming model's grid. The esm schema defined `regrid` only before 0.8.0. esm 1.0.0 states (esm-spec §8.6) that a data source performs no regridding and that there is NO `Model.regrid` map: the carrier is the `variable_map` entry's `transform` field on the coupling edge that consumes the field (§10.4/§10.5) — an ordinary `aggregate` expression, typically an `apply_expression_template` invocation of an imported overlap-weight library. No such coupling edge exists in this document, so the map is recorded here VERBATIM to keep every field recoverable. This is a demotion from a structured field to prose, not an equivalent: the transform expression still has to be authored on whichever coupling edge consumes these fields.

`regrid` (verbatim):
{
  "flx": {
    "method": "conservative",
    "description": "EDGAR surface emission flux (kg m⁻² s⁻¹). Cell-centered emissions scalar → conservative area-weighted overlap-join regridder (ESD regridding/conservative_regrid_overlap_join.esm). Referenced by the `emission` observed as EDGAR_v81.flx."
  }
}_

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `lon` | `rad` | `0.0` | Longitude of the grid point (radians). Coupled to the simulation domain's longitude coordinate via param_to_var when composed into a CoupledSystem. |
| `lat` | `rad` | `0.0` | Latitude of the grid point (radians). Coupled to the simulation domain's latitude coordinate via param_to_var when composed into a CoupledSystem. |
| `lev` | `1` | `1.0` | Vertical level index (dimensionless, 1-based). Emissions are applied only at lev < 2 (surface layer). Coupled to the simulation domain's lev coordinate via param_to_var when composed into a CoupledSystem. |
| `Δz` | `m` | `60.0` | Height of the first vertical grid layer (m). Used to convert surface emission flux (kg m⁻² s⁻¹) to volumetric emission rate (kg m⁻³ s⁻¹) via division. |
| `scale` | `1` | `1.0` | Multiplicative scaling factor applied to the emission flux. Default 1.0 (no scaling). May be used to adjust emissions for sensitivity experiments or unit-system conversions. |
| `flx` | `kg/m^2/s` |  | Surface emission flux for the configured species and sector. Variable name 'flx' is derived from the _flx_nc.zip archive naming convention for EDGAR v8.1 AP datasets. |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `emission` | `kg/m^3/s` |  | Volumetric emission rate (kg m⁻³ s⁻¹) at the current grid point and time. Non-zero only in the surface layer (lev < 2): emission = EDGAR_v81.flx / Δz * scale. Zero for lev ≥ 2. Corresponds to the upstream observed variable created per varnames(fileset) by create_interp_equation with wrapper_f = eq -> ifelse(lev < 2, eq / Δz * scale, zero_emis). |

## Observed expressions

$$
emission = \mathrm{ifelse}\left(\mathrm{<}\left(lev, 2.0\right), \frac{flx}{Δz} \cdot scale, 0.0\right)
$$
_Volumetric emission rate (kg m⁻³ s⁻¹) at the current grid point and time. Non-zero only in the surface layer (lev < 2): emission = EDGAR_v81.flx / Δz * scale. Zero for lev ≥ 2. Corresponds to the upstream observed variable created per varnames(fileset) by create_interp_equation with wrapper_f = eq -> ifelse(lev < 2, eq / Δz * scale, zero_emis)._

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "reference": {
    "notes": "source_ref: EarthSciData.jl@830435a065f27e99f10bba91107ca1730322cc6b:src/edgar_v81_monthly.jl:277\n\nUpstream constructor EDGARv81MonthlyEmis(substance, sector, domaininfo; scale=1.0, ...) creates an MTK System with:\n  - @parameters: lon (rad), lat (rad), lev (1), Δz=60.0 (m), t_ref=get_tref(domaininfo) (s)\n  - One DataSetInterpolator per varnames(fileset): builds interp_unsafe equation for each NC variable\n  - Equation template (from create_interp_equation with wrapper_f):\n      var(t) ~ ifelse(lev < 2, interp_unsafe(data, fit, fi_lon, fi_lat, extrap) * unit_scale / Δz * scale, zero_var)\n    where fit = 1 + (t_ref + t - tstart) / tstep\n          fi_lon = 1 + (lon - s1start) / s1step\n          fi_lat = 1 + (lat - s2start) / s2step\n  - discrete_events: build_interp_event fires at monthly tstops to reload data buffers\n  - metadata: Dict(CoupleType => EDGARv81MonthlyEmisCoupler, SysDomainInfo => domaininfo)\n\ngt-p3ep resolution: the @register_symbolic interp_unsafe pattern is replaced by the data_loaders §8\nmechanism. EDGAR_v81.flx is the loader variable that the runtime regridds from the 0.1°×0.1° EDGAR\ngrid to the model domain and interpolates in time to t. The runtime implicitly handles the\nbuild_interp_event discrete callbacks based on data_loaders.temporal.frequency = P1M.\n\nParameter rename: upstream `t` (simulation time relative to t_ref) is implicit; the ESM model\nhas no independent variable in the variable map since it only contains observed equations.\n\nThe variable `emission` corresponds to the observed variable created by the for-loop over\nvarnames(fileset). For the typical single-variable EDGAR NC file (one flux variable per\nsubstance/sector), there is one observed equation. The variable name in the NC file is 'flx'\n(from the _flx_nc.zip filename convention; confirmed by ESS test fixture at\nEarthSciAST/pkg/earthsci-ast-py/tests/fixtures/data_loaders/edgar_v81_monthly.esm).\n\n--- esm-3nc.3 pure-IO split ---\nThis is the regridding-model half of the pure-IO loader migration (RFC pure-io-data-loaders §6/§7, bead esm-3nc.3). The pre-migration edgar_v81_monthly.esm carried both this coupler model AND a co-located data_loaders.EDGAR_v81 block (with the now-removed `spatial` and `regridding` sub-blocks). That loader became, at 0.7.0, the pure-I/O file components/earthsci_data/edgar_v81_monthly_loader.esm, referenced as the subsystem `EDGAR_v81`. At esm 1.0.0 it is the `EDGAR_v81` entry in THIS file's `data_sources`: a data source is not a component, so it neither needs nor may be a subsystem, and the standalone file is gone. The observed `emission` expression still names the field as EDGAR_v81.flx.\nReprojection (RFC §6 step 2): EDGAR's native grid.crs.projection is 'longlat' (geographic WGS84), so the reprojection rule selected by convention is ESD reprojection/longlat.esm (esd-47z.1) — the IDENTITY transform.\nRegridding (RFC §6 step 3 / §5.2): the EDGAR flux is a cell-centered scalar → conservative area-weighted overlap join (ESD regridding/conservative_regrid_overlap_join.esm), declared in the model `regrid` block.\n\nCoupler identity: this model was serialized with the model-level field `coupletype: \"EDGARv81MonthlyEmisCoupler\"`, the EarthSciMLBase `CoupleType` metadata tag naming the Julia coupler struct that `EarthSciMLBase.couple2` dispatches on to find this component's pairwise coupling rules. The esm schema defined `coupletype` only before 0.8.0 (\"informational label identifying this system's role in coupling\"); 0.8.0 removed it in favour of explicit coupling — `coupling` entries naming components directly, or `coupling_roles` + `coupling_import` in a coupling-library file (esm-spec §10.9–§10.11). esm 1.0.0 has no model-level coupler-identity field, so the tag is recorded here to keep it recoverable.\n\nRegridding intent: this model was serialized with the model-level `regrid` map, one entry per variable naming the kernel that carries the loaded native-grid field onto the consuming model's grid. The esm schema defined `regrid` only before 0.8.0. esm 1.0.0 states (esm-spec §8.6) that a data source performs no regridding and that there is NO `Model.regrid` map: the carrier is the `variable_map` entry's `transform` field on the coupling edge that consumes the field (§10.4/§10.5) — an ordinary `aggregate` expression, typically an `apply_expression_template` invocation of an imported overlap-weight library. No such coupling edge exists in this document, so the map is recorded here VERBATIM to keep every field recoverable. This is a demotion from a structured field to prose, not an equivalent: the transform expression still has to be authored on whichever coupling edge consumes these fields.\n\n`regrid` (verbatim):\n{\n  \"flx\": {\n    \"method\": \"conservative\",\n    \"description\": \"EDGAR surface emission flux (kg m⁻² s⁻¹). Cell-centered emissions scalar → conservative area-weighted overlap-join regridder (ESD regridding/conservative_regrid_overlap_join.esm). Referenced by the `emission` observed as EDGAR_v81.flx.\"\n  }\n}"
  },
  "tolerance": {
    "rel": 1e-06
  },
  "variables": {
    "lon": {
      "type": "parameter",
      "units": "rad",
      "default": 0.0,
      "description": "Longitude of the grid point (radians). Coupled to the simulation domain's longitude coordinate via param_to_var when composed into a CoupledSystem."
    },
    "lat": {
      "type": "parameter",
      "units": "rad",
      "default": 0.0,
      "description": "Latitude of the grid point (radians). Coupled to the simulation domain's latitude coordinate via param_to_var when composed into a CoupledSystem."
    },
    "lev": {
      "type": "parameter",
      "units": "1",
      "default": 1.0,
      "description": "Vertical level index (dimensionless, 1-based). Emissions are applied only at lev < 2 (surface layer). Coupled to the simulation domain's lev coordinate via param_to_var when composed into a CoupledSystem."
    },
    "Δz": {
      "type": "parameter",
      "units": "m",
      "default": 60.0,
      "description": "Height of the first vertical grid layer (m). Used to convert surface emission flux (kg m⁻² s⁻¹) to volumetric emission rate (kg m⁻³ s⁻¹) via division."
    },
    "scale": {
      "type": "parameter",
      "units": "1",
      "default": 1.0,
      "description": "Multiplicative scaling factor applied to the emission flux. Default 1.0 (no scaling). May be used to adjust emissions for sensitivity experiments or unit-system conversions."
    },
    "emission": {
      "type": "unknown",
      "units": "kg/m^3/s",
      "description": "Volumetric emission rate (kg m⁻³ s⁻¹) at the current grid point and time. Non-zero only in the surface layer (lev < 2): emission = EDGAR_v81.flx / Δz * scale. Zero for lev ≥ 2. Corresponds to the upstream observed variable created per varnames(fileset) by create_interp_equation with wrapper_f = eq -> ifelse(lev < 2, eq / Δz * scale, zero_emis)."
    },
    "flx": {
      "type": "parameter",
      "units": "kg/m^2/s",
      "description": "Surface emission flux for the configured species and sector. Variable name 'flx' is derived from the _flx_nc.zip archive naming convention for EDGAR v8.1 AP datasets.",
      "update": {
        "kind": "data",
        "source": "EDGAR_v81",
        "from": {
          "file_variable": "flx",
          "description": "Surface emission flux for the configured species and sector. Variable name 'flx' is derived from the _flx_nc.zip archive naming convention for EDGAR v8.1 AP datasets."
        }
      }
    }
  },
  "equations": [
    {
      "lhs": "emission",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "<",
            "args": [
              "lev",
              2.0
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "/",
                "args": [
                  "flx",
                  "Δz"
                ]
              },
              "scale"
            ]
          },
          0.0
        ]
      }
    }
  ],
  "tests": []
}
```

</details>
