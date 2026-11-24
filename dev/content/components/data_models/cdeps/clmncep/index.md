---
title: "Clmncep"
slug: "clmncep"
domains: ["data_models"]
component_types: ["model"]
subdomains: ["cdeps"]
domain: "data_models"
subdomain: "cdeps"
component_type: "model"
esm_version: "2.0.0"
esm_path: "components/data_models/cdeps/cdeps_datm_gswp3.esm"
reference: "https://github.com/ESCOMP/CDEPS"
description: "The CDEPS DATM data-atmosphere laws for the GSWP3v1 forcing with the CLMNCEP datamode (cdeps1.0.112), with no data access: (1) Streams - the stream layer of shr_strdata_advance for the four GSWP3 streams, with the time-interpolation factors computed from the model time t (coszen for Solar: cosz/tavCosz from the shr_orb_decl declination and the modeldt-sampled interval average, 0 at night; nearest for Precip; linear for TPQW; lower for the static topo), each 3-hourly field entering as its bracketing record pair [LB, UB] over the record axis rec (esm-spec 8.5.1); (2) Clmncep - the datamode transformation from the interpolated stream values to the export state Sa_* / Faxa_*. The shared pointwise laws are imported from ./cdeps_templates.esm. The tests pin CDEPS instrumentation dumps of a reference CESM I2000Clm60Sp_f19 run (cdeps_strdata_streams.csv for Streams, datm_gswp3_streams.csv + datm_gswp3_exports.csv for Clmncep; all traced points are at lat -90 on 2000-01-01, so polar day and all snow), plus closed-form recomputations for the branches no traced row reaches (README). The GSWP3 data sources and the reader -> Streams -> Clmncep wiring live in cdeps_datm_gswp3_data.esm, and the data-reading test in cdeps_datm_gswp3_synthetic.esm, so these law tests need no data."
tags: ["data_models", "cdeps", "model", "datm", "data-atmosphere", "expression-templates", "cesm", "gswp3", "forcing"]
---

## Description

The CDEPS DATM data-atmosphere laws for the GSWP3v1 forcing with the CLMNCEP datamode (cdeps1.0.112), with no data access: (1) Streams - the stream layer of shr_strdata_advance for the four GSWP3 streams, with the time-interpolation factors computed from the model time t (coszen for Solar: cosz/tavCosz from the shr_orb_decl declination and the modeldt-sampled interval average, 0 at night; nearest for Precip; linear for TPQW; lower for the static topo), each 3-hourly field entering as its bracketing record pair [LB, UB] over the record axis rec (esm-spec 8.5.1); (2) Clmncep - the datamode transformation from the interpolated stream values to the export state Sa_* / Faxa_*. The shared pointwise laws are imported from ./cdeps_templates.esm. The tests pin CDEPS instrumentation dumps of a reference CESM I2000Clm60Sp_f19 run (cdeps_strdata_streams.csv for Streams, datm_gswp3_streams.csv + datm_gswp3_exports.csv for Clmncep; all traced points are at lat -90 on 2000-01-01, so polar day and all snow), plus closed-form recomputations for the branches no traced row reaches (README). The GSWP3 data sources and the reader -> Streams -> Clmncep wiring live in cdeps_datm_gswp3_data.esm, and the data-reading test in cdeps_datm_gswp3_synthetic.esm, so these law tests need no data.

## Reference

- CESM (Community Earth System Model), ESCOMP/CDEPS: Common Data model EXchange Platform source (cdeps1.0.112) - datm/datm_datamode_clmncep_mod.F90, streams/dshr_strdata_mod.F90, streams/dshr_tinterp_mod.F90, share/shr_precip_mod.F90, share/shr_const_mod.F90 - the reference implementation these components are transcribed from.
- Kim, H. (2017). Global Soil Wetness Project Phase 3 Atmospheric Boundary Conditions (Experiment 1) [Data set]. Data Integration and Analysis System (DIAS). The GSWP3v1 0.5x0.5 deg, 3-hourly atmospheric forcing (Solar, Precip, TPHWL streams) and the USGS topography the datm consumes.
- EarthSciModels - the authoritative .esm corpus this component lives in.

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `strm_tbot` | `K` | `249.30924313863048` | interpolated TPQW Sa_tbot stream value, [K] |
| `strm_pbot` | `Pa` | `68134.13610026057` | interpolated TPQW Sa_pbot stream value, [Pa] |
| `strm_wind` | `m/s` | `4.88208296870192` | interpolated TPQW Sa_wind stream value, [m/s] |
| `strm_shum` | `kg/kg` | `0.0007554910110128631` | interpolated TPQW Sa_shum stream value, [kg/kg] |
| `strm_rh` | `1` | `0.0` | Relative-humidity stream value [percent, 0-100] (used when shum_source = 2; not provided by GSWP3). |
| `strm_tdew` | `K` | `0.0` | Dew-point stream value [K, or degC when tdewmax < 50] (used when shum_source = 3; not provided by GSWP3). |
| `strm_lwdn` | `W/m^2` | `147.6519253730771` | interpolated TPQW Faxa_lwdn stream value, [W/m2] |
| `strm_swdn` | `W/m^2` | `429.97176732088275` | interpolated Solar Faxa_swdn stream value, [W/m2] |
| `strm_precn` | `kg/m^2/s` | `5.22216069182629e-06` | interpolated Precip Faxa_precn stream value, [kg/m2/s] |
| `strm_topo` | `m` | `2824.921026576389` | interpolated topo Sa_topo stream value, [m] |
| `strm_z` | `m` | `1e+30` | interpolated z stream value (1e30 spval when no z stream, as in GSWP3), [m] |
| `tbotmax` | `K` | `310.35066065749163` | first-call global max of Sa_tbot before the tkfrz adjustment (units detector: <50 means the stream temperature is in degC), [K] |
| `tdewmax` | `K` | `300.0` | First-call global max of the dew-point stream (units detector: < 50 means degC), used when shum_source = 3. |
| `anidrmax` | `W/m^2` | `1e+30` | first-call global max of the Sx_anidr import (existence detector; 1e30 when the imports are absent), [W/m2] |
| `topo_present` | `1` | `1.0` | 1 when the topo stream is associated |
| `pbot_present` | `1` | `1.0` | 1 when the pbot stream is associated |
| `lwdn_present` | `1` | `1.0` | 1 when the lwdn stream is associated |
| `shum_source` | `1` | `1.0` | Which humidity stream the datamode has (F90:409-428): 1 = specific humidity (Sa_shum, GSWP3 QBOT; capped at qsat), 2 = relative humidity (Sa_rh), 3 = dew point (Sa_tdew). |
| `Sx_anidr` | `1` | `1e+30` | NIR direct albedo import (1e30 spval when absent), [-] |
| `Sx_avsdr` | `1` | `1e+30` | VIS direct albedo import (1e30 spval when absent), [-] |
| `Sx_anidf` | `1` | `1e+30` | NIR diffuse albedo import (1e30 spval when absent), [-] |
| `Sx_avsdf` | `1` | `1e+30` | VIS diffuse albedo import (1e30 spval when absent), [-] |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `e` | `Pa` |  | Vapor pressure of the humidity path [Pa]: esat(Sa_tbot) on the shum path (the qsat it caps at), rh*0.01*esat(Sa_tbot) on the rh path, esat(tdew) with the phase of Sa_tbot on the dew-point path (F90:409-428). |
| `tdew_k` | `K` |  | Dew point in K (tkfrz added when tdewmax < 50, F90:424). |
| `qsat_` | `kg/kg` |  | qsat(e, Sa_pbot) = 0.622 e / (Sa_pbot - 0.378 e): the cap on the shum path, the specific humidity itself on the rh and dew-point paths. |
| `vp` | `Pa` |  | vapor pressure q pbot / (0.622 + 0.378 q), [Pa] |
| `rainc0` | `kg/m^2/s` |  | convective-scale precipitation rate before the rain/snow split = 0.1 precn, [kg/m2/s] |
| `rainl0` | `kg/m^2/s` |  | large-scale precipitation rate before the rain/snow split = 0.9 precn, [kg/m2/s] |
| `frac` | `1` |  | rain fraction of the temperature ramp clamp((tbot - TKFRZ)*0.5, 0, 1), [-] |
| `swdn_half` | `W/m^2` |  | half of the incoming shortwave = 0.5 swdn, the argument s of the ratio_rvrf polynomials, [W/m2] |
| `ratio_nir` | `1` |  | NIR direct fraction from the cam3_5_55 polynomial, clamped to [0.01, 0.99], [-] |
| `ratio_vis` | `1` |  | VIS direct fraction from the cam3_5_55 polynomial, clamped to [0.01, 0.99], [-] |
| `e2` | `Pa` |  | vapor pressure for the lwdn fallback = pslv q / (0.622 + 0.378 q), [Pa] |
| `ea` | `1` |  | lwdn fallback emissivity 0.70 + 5.95e-5 * 0.01 e * exp(1500/tbot), [-] |
| `Sa_topo` | `m` |  | surface height export, [m] |
| `Sa_z` | `m` |  | bottom-layer height export (30 m when the z stream is absent), [m] |
| `Sa_u` | `m/s` |  | zonal wind export = wind/sqrt(2), [m/s] |
| `Sa_v` | `m/s` |  | meridional wind export = wind/sqrt(2), [m/s] |
| `Sa_tbot` | `K` |  | bottom-layer temperature export, [K] |
| `Sa_ptem` | `K` |  | potential temperature export = Sa_tbot, [K] |
| `Sa_shum` | `kg/kg` |  | specific humidity export = min(qsat, stream), [kg/kg] |
| `Sa_dens` | `kg/m^3` |  | density export, [kg/m3] |
| `Sa_pbot` | `Pa` |  | pressure export (pstd when 0 or stream absent), [Pa] |
| `Sa_pslv` | `Pa` |  | sea-level pressure export = Sa_pbot, [Pa] |
| `Faxa_rainc` | `kg/m^2/s` |  | convective-scale rain flux export, [kg/m2/s] |
| `Faxa_rainl` | `kg/m^2/s` |  | large-scale rain flux export, [kg/m2/s] |
| `Faxa_snowc` | `kg/m^2/s` |  | convective-scale snow flux export, [kg/m2/s] |
| `Faxa_snowl` | `kg/m^2/s` |  | large-scale snow flux export, [kg/m2/s] |
| `Faxa_swndr` | `W/m^2` |  | NIR direct shortwave export, [W/m2] |
| `Faxa_swndf` | `W/m^2` |  | NIR diffuse shortwave export, [W/m2] |
| `Faxa_swvdr` | `W/m^2` |  | VIS direct shortwave export, [W/m2] |
| `Faxa_swvdf` | `W/m^2` |  | VIS diffuse shortwave export, [W/m2] |
| `Faxa_swnet` | `W/m^2` |  | net shortwave export (albedo-weighted sum; 0 when the Sx imports are spval/tiny; plain sum when absent), [W/m2] |
| `Faxa_swdn` | `W/m^2` |  | incoming shortwave export = stream, [W/m2] |
| `Faxa_lwdn` | `W/m^2` |  | incoming longwave export = stream (or the ea sigma T^4 fallback), [W/m2] |

## Observed expressions

$$
e = \mathrm{ifelse}\left(shum_{source} = \mathrm{const}\left(\right), \mathrm{esat}\left(tK=tdew_{k}, tKbot=Sa_{tbot}\right), \mathrm{ifelse}\left(shum_{source} = \mathrm{const}\left(\right), strm_{rh} \cdot \mathrm{const}\left(\right) \cdot \mathrm{esat}\left(tK=Sa_{tbot}, tKbot=Sa_{tbot}\right), \mathrm{esat}\left(tK=Sa_{tbot}, tKbot=Sa_{tbot}\right)\right)\right)
$$
_Vapor pressure of the humidity path [Pa]: esat(Sa_tbot) on the shum path (the qsat it caps at), rh*0.01*esat(Sa_tbot) on the rh path, esat(tdew) with the phase of Sa_tbot on the dew-point path (F90:409-428)._

$$
tdew_{k} = strm_{tdew} + \mathrm{ifelse}\left(\mathrm{<}\left(tdewmax, \mathrm{const}\left(\right)\right), \mathrm{tkfrz}\left(\right), \mathrm{const}\left(\right)\right)
$$
_Dew point in K (tkfrz added when tdewmax < 50, F90:424)._

$$
qsat_{} = \mathrm{qsat}\left(e=e, pbot=Sa_{pbot}\right)
$$
_qsat(e, Sa_pbot) = 0.622 e / (Sa_pbot - 0.378 e): the cap on the shum path, the specific humidity itself on the rh and dew-point paths._

$$
vp = \mathrm{vapor_pressure}\left(q=Sa_{shum}, pbot=Sa_{pbot}\right)
$$
_vapor pressure q pbot / (0.622 + 0.378 q), [Pa]_

$$
rainc0 = \mathrm{const}\left(\right) \cdot strm_{precn}
$$
_convective-scale precipitation rate before the rain/snow split = 0.1 precn, [kg/m2/s]_

$$
rainl0 = \mathrm{const}\left(\right) \cdot strm_{precn}
$$
_large-scale precipitation rate before the rain/snow split = 0.9 precn, [kg/m2/s]_

$$
frac = \mathrm{rain_snow_frac}\left(tbot=Sa_{tbot}\right)
$$
_rain fraction of the temperature ramp clamp((tbot - TKFRZ)*0.5, 0, 1), [-]_

$$
swdn_{half} = \mathrm{const}\left(\right) \cdot strm_{swdn}
$$
_half of the incoming shortwave = 0.5 swdn, the argument s of the ratio_rvrf polynomials, [W/m2]_

$$
ratio_{nir} = \mathrm{ratio_rvrf_nir}\left(s=swdn_{half}\right)
$$
_NIR direct fraction from the cam3_5_55 polynomial, clamped to [0.01, 0.99], [-]_

$$
ratio_{vis} = \mathrm{ratio_rvrf_vis}\left(s=swdn_{half}\right)
$$
_VIS direct fraction from the cam3_5_55 polynomial, clamped to [0.01, 0.99], [-]_

$$
e2 = \mathrm{vapor_pressure}\left(q=Sa_{shum}, pbot=Sa_{pslv}\right)
$$
_vapor pressure for the lwdn fallback = pslv q / (0.622 + 0.378 q), [Pa]_

$$
ea = \mathrm{const}\left(\right) + \mathrm{const}\left(\right) \cdot \mathrm{const}\left(\right) \cdot e2 \cdot e^{\frac{\mathrm{const}\left(\right)}{Sa_{tbot}}}
$$
_lwdn fallback emissivity 0.70 + 5.95e-5 * 0.01 e * exp(1500/tbot), [-]_

$$
Sa_{topo} = \mathrm{ifelse}\left(topo_{present} = \mathrm{const}\left(\right), \mathrm{const}\left(\right), strm_{topo}\right)
$$
_surface height export, [m]_

$$
Sa_{z} = \mathrm{ifelse}\left(\mathrm{>=}\left(strm_{z}, \mathrm{const}\left(\right)\right), \mathrm{const}\left(\right), strm_{z}\right)
$$
_bottom-layer height export (30 m when the z stream is absent), [m]_

$$
Sa_{u} = \mathrm{wind_split}\left(wind=strm_{wind}\right)
$$
_zonal wind export = wind/sqrt(2), [m/s]_

$$
Sa_{v} = Sa_{u}
$$
_meridional wind export = wind/sqrt(2), [m/s]_

$$
Sa_{tbot} = \mathrm{max}\left(\mathrm{const}\left(\right), strm_{tbot} + \mathrm{ifelse}\left(\mathrm{<}\left(tbotmax, \mathrm{const}\left(\right)\right), \mathrm{const}\left(\right), \mathrm{const}\left(\right)\right)\right)
$$
_bottom-layer temperature export, [K]_

$$
Sa_{ptem} = Sa_{tbot}
$$
_potential temperature export = Sa_tbot, [K]_

$$
Sa_{shum} = \mathrm{ifelse}\left(shum_{source} = \mathrm{const}\left(\right), \mathrm{min}\left(qsat_{}, strm_{shum}\right), qsat_{}\right)
$$
_specific humidity export = min(qsat, stream), [kg/kg]_

$$
Sa_{dens} = \mathrm{density}\left(pbot=Sa_{pbot}, vp=vp, tbot=Sa_{tbot}\right)
$$
_density export, [kg/m3]_

$$
Sa_{pbot} = \mathrm{ifelse}\left(pbot_{present} = \mathrm{const}\left(\right), \mathrm{const}\left(\right), \mathrm{ifelse}\left(strm_{pbot} = \mathrm{const}\left(\right), \mathrm{const}\left(\right), strm_{pbot}\right)\right)
$$
_pressure export (pstd when 0 or stream absent), [Pa]_

$$
Sa_{pslv} = Sa_{pbot}
$$
_sea-level pressure export = Sa_pbot, [Pa]_

$$
Faxa_{rainc} = \mathrm{max}\left(\mathrm{const}\left(\right), rainc0 \cdot frac\right)
$$
_convective-scale rain flux export, [kg/m2/s]_

$$
Faxa_{rainl} = \mathrm{max}\left(\mathrm{const}\left(\right), rainl0 \cdot frac\right)
$$
_large-scale rain flux export, [kg/m2/s]_

$$
Faxa_{snowc} = \mathrm{max}\left(\mathrm{const}\left(\right), rainc0 \cdot \left(\mathrm{const}\left(\right) - frac\right)\right)
$$
_convective-scale snow flux export, [kg/m2/s]_

$$
Faxa_{snowl} = \mathrm{max}\left(\mathrm{const}\left(\right), rainl0 \cdot \left(\mathrm{const}\left(\right) - frac\right)\right)
$$
_large-scale snow flux export, [kg/m2/s]_

$$
Faxa_{swndr} = ratio_{nir} \cdot swdn_{half}
$$
_NIR direct shortwave export, [W/m2]_

$$
Faxa_{swndf} = \left(\mathrm{const}\left(\right) - ratio_{nir}\right) \cdot swdn_{half}
$$
_NIR diffuse shortwave export, [W/m2]_

$$
Faxa_{swvdr} = ratio_{vis} \cdot swdn_{half}
$$
_VIS direct shortwave export, [W/m2]_

$$
Faxa_{swvdf} = \left(\mathrm{const}\left(\right) - ratio_{vis}\right) \cdot swdn_{half}
$$
_VIS diffuse shortwave export, [W/m2]_

$$
Faxa_{swnet} = \mathrm{ifelse}\left(\mathrm{or}\left(\mathrm{<}\left(anidrmax, \mathrm{const}\left(\right)\right), \mathrm{>}\left(anidrmax, \mathrm{const}\left(\right)\right)\right), \mathrm{const}\left(\right), \mathrm{ifelse}\left(\mathrm{<}\left(Sx_{anidr}, \mathrm{const}\left(\right)\right), \left(\mathrm{const}\left(\right) - Sx_{anidr}\right) \cdot Faxa_{swndr} + \left(\mathrm{const}\left(\right) - Sx_{avsdr}\right) \cdot Faxa_{swvdr} + \left(\mathrm{const}\left(\right) - Sx_{anidf}\right) \cdot Faxa_{swndf} + \left(\mathrm{const}\left(\right) - Sx_{avsdf}\right) \cdot Faxa_{swvdf}, Faxa_{swndr} + Faxa_{swvdr} + Faxa_{swndf} + Faxa_{swvdf}\right)\right)
$$
_net shortwave export (albedo-weighted sum; 0 when the Sx imports are spval/tiny; plain sum when absent), [W/m2]_

$$
Faxa_{swdn} = strm_{swdn}
$$
_incoming shortwave export = stream, [W/m2]_

$$
Faxa_{lwdn} = \mathrm{ifelse}\left(lwdn_{present} = \mathrm{const}\left(\right), ea \cdot \mathrm{const}\left(\right) \cdot Sa_{tbot}^{4}, strm_{lwdn}\right)
$$
_incoming longwave export = stream (or the ea sigma T^4 fallback), [W/m2]_

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "expression_template_imports": [
    {
      "ref": "./cdeps_templates.esm"
    }
  ],
  "variables": {
    "strm_tbot": {
      "type": "parameter",
      "units": "K",
      "description": "interpolated TPQW Sa_tbot stream value, [K]",
      "default": 249.30924313863048
    },
    "strm_pbot": {
      "type": "parameter",
      "units": "Pa",
      "description": "interpolated TPQW Sa_pbot stream value, [Pa]",
      "default": 68134.13610026057
    },
    "strm_wind": {
      "type": "parameter",
      "units": "m/s",
      "description": "interpolated TPQW Sa_wind stream value, [m/s]",
      "default": 4.88208296870192
    },
    "strm_shum": {
      "type": "parameter",
      "units": "kg/kg",
      "description": "interpolated TPQW Sa_shum stream value, [kg/kg]",
      "default": 0.0007554910110128631
    },
    "strm_rh": {
      "type": "parameter",
      "units": "1",
      "default": 0.0,
      "description": "Relative-humidity stream value [percent, 0-100] (used when shum_source = 2; not provided by GSWP3)."
    },
    "strm_tdew": {
      "type": "parameter",
      "units": "K",
      "default": 0.0,
      "description": "Dew-point stream value [K, or degC when tdewmax < 50] (used when shum_source = 3; not provided by GSWP3)."
    },
    "strm_lwdn": {
      "type": "parameter",
      "units": "W/m^2",
      "description": "interpolated TPQW Faxa_lwdn stream value, [W/m2]",
      "default": 147.6519253730771
    },
    "strm_swdn": {
      "type": "parameter",
      "units": "W/m^2",
      "description": "interpolated Solar Faxa_swdn stream value, [W/m2]",
      "default": 429.97176732088275
    },
    "strm_precn": {
      "type": "parameter",
      "units": "kg/m^2/s",
      "description": "interpolated Precip Faxa_precn stream value, [kg/m2/s]",
      "default": 5.22216069182629e-06
    },
    "strm_topo": {
      "type": "parameter",
      "units": "m",
      "description": "interpolated topo Sa_topo stream value, [m]",
      "default": 2824.921026576389
    },
    "strm_z": {
      "type": "parameter",
      "units": "m",
      "default": 1e+30,
      "description": "interpolated z stream value (1e30 spval when no z stream, as in GSWP3), [m]"
    },
    "tbotmax": {
      "type": "parameter",
      "units": "K",
      "description": "first-call global max of Sa_tbot before the tkfrz adjustment (units detector: <50 means the stream temperature is in degC), [K]",
      "default": 310.35066065749163
    },
    "tdewmax": {
      "type": "parameter",
      "units": "K",
      "default": 300.0,
      "description": "First-call global max of the dew-point stream (units detector: < 50 means degC), used when shum_source = 3."
    },
    "anidrmax": {
      "type": "parameter",
      "units": "W/m^2",
      "default": 1e+30,
      "description": "first-call global max of the Sx_anidr import (existence detector; 1e30 when the imports are absent), [W/m2]"
    },
    "topo_present": {
      "type": "parameter",
      "units": "1",
      "default": 1.0,
      "description": "1 when the topo stream is associated"
    },
    "pbot_present": {
      "type": "parameter",
      "units": "1",
      "default": 1.0,
      "description": "1 when the pbot stream is associated"
    },
    "lwdn_present": {
      "type": "parameter",
      "units": "1",
      "default": 1.0,
      "description": "1 when the lwdn stream is associated"
    },
    "shum_source": {
      "type": "parameter",
      "units": "1",
      "default": 1.0,
      "description": "Which humidity stream the datamode has (F90:409-428): 1 = specific humidity (Sa_shum, GSWP3 QBOT; capped at qsat), 2 = relative humidity (Sa_rh), 3 = dew point (Sa_tdew)."
    },
    "Sx_anidr": {
      "type": "parameter",
      "units": "1",
      "default": 1e+30,
      "description": "NIR direct albedo import (1e30 spval when absent), [-]"
    },
    "Sx_avsdr": {
      "type": "parameter",
      "units": "1",
      "default": 1e+30,
      "description": "VIS direct albedo import (1e30 spval when absent), [-]"
    },
    "Sx_anidf": {
      "type": "parameter",
      "units": "1",
      "default": 1e+30,
      "description": "NIR diffuse albedo import (1e30 spval when absent), [-]"
    },
    "Sx_avsdf": {
      "type": "parameter",
      "units": "1",
      "default": 1e+30,
      "description": "VIS diffuse albedo import (1e30 spval when absent), [-]"
    },
    "e": {
      "type": "unknown",
      "units": "Pa",
      "description": "Vapor pressure of the humidity path [Pa]: esat(Sa_tbot) on the shum path (the qsat it caps at), rh*0.01*esat(Sa_tbot) on the rh path, esat(tdew) with the phase of Sa_tbot on the dew-point path (F90:409-428)."
    },
    "tdew_k": {
      "type": "unknown",
      "units": "K",
      "description": "Dew point in K (tkfrz added when tdewmax < 50, F90:424)."
    },
    "qsat_": {
      "type": "unknown",
      "units": "kg/kg",
      "description": "qsat(e, Sa_pbot) = 0.622 e / (Sa_pbot - 0.378 e): the cap on the shum path, the specific humidity itself on the rh and dew-point paths."
    },
    "vp": {
      "type": "unknown",
      "units": "Pa",
      "description": "vapor pressure q pbot / (0.622 + 0.378 q), [Pa]"
    },
    "rainc0": {
      "type": "unknown",
      "units": "kg/m^2/s",
      "description": "convective-scale precipitation rate before the rain/snow split = 0.1 precn, [kg/m2/s]"
    },
    "rainl0": {
      "type": "unknown",
      "units": "kg/m^2/s",
      "description": "large-scale precipitation rate before the rain/snow split = 0.9 precn, [kg/m2/s]"
    },
    "frac": {
      "type": "unknown",
      "units": "1",
      "description": "rain fraction of the temperature ramp clamp((tbot - TKFRZ)*0.5, 0, 1), [-]"
    },
    "swdn_half": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "half of the incoming shortwave = 0.5 swdn, the argument s of the ratio_rvrf polynomials, [W/m2]"
    },
    "ratio_nir": {
      "type": "unknown",
      "units": "1",
      "description": "NIR direct fraction from the cam3_5_55 polynomial, clamped to [0.01, 0.99], [-]"
    },
    "ratio_vis": {
      "type": "unknown",
      "units": "1",
      "description": "VIS direct fraction from the cam3_5_55 polynomial, clamped to [0.01, 0.99], [-]"
    },
    "e2": {
      "type": "unknown",
      "units": "Pa",
      "description": "vapor pressure for the lwdn fallback = pslv q / (0.622 + 0.378 q), [Pa]"
    },
    "ea": {
      "type": "unknown",
      "units": "1",
      "description": "lwdn fallback emissivity 0.70 + 5.95e-5 * 0.01 e * exp(1500/tbot), [-]"
    },
    "Sa_topo": {
      "type": "unknown",
      "units": "m",
      "description": "surface height export, [m]"
    },
    "Sa_z": {
      "type": "unknown",
      "units": "m",
      "description": "bottom-layer height export (30 m when the z stream is absent), [m]"
    },
    "Sa_u": {
      "type": "unknown",
      "units": "m/s",
      "description": "zonal wind export = wind/sqrt(2), [m/s]"
    },
    "Sa_v": {
      "type": "unknown",
      "units": "m/s",
      "description": "meridional wind export = wind/sqrt(2), [m/s]"
    },
    "Sa_tbot": {
      "type": "unknown",
      "units": "K",
      "description": "bottom-layer temperature export, [K]"
    },
    "Sa_ptem": {
      "type": "unknown",
      "units": "K",
      "description": "potential temperature export = Sa_tbot, [K]"
    },
    "Sa_shum": {
      "type": "unknown",
      "units": "kg/kg",
      "description": "specific humidity export = min(qsat, stream), [kg/kg]"
    },
    "Sa_dens": {
      "type": "unknown",
      "units": "kg/m^3",
      "description": "density export, [kg/m3]"
    },
    "Sa_pbot": {
      "type": "unknown",
      "units": "Pa",
      "description": "pressure export (pstd when 0 or stream absent), [Pa]"
    },
    "Sa_pslv": {
      "type": "unknown",
      "units": "Pa",
      "description": "sea-level pressure export = Sa_pbot, [Pa]"
    },
    "Faxa_rainc": {
      "type": "unknown",
      "units": "kg/m^2/s",
      "description": "convective-scale rain flux export, [kg/m2/s]"
    },
    "Faxa_rainl": {
      "type": "unknown",
      "units": "kg/m^2/s",
      "description": "large-scale rain flux export, [kg/m2/s]"
    },
    "Faxa_snowc": {
      "type": "unknown",
      "units": "kg/m^2/s",
      "description": "convective-scale snow flux export, [kg/m2/s]"
    },
    "Faxa_snowl": {
      "type": "unknown",
      "units": "kg/m^2/s",
      "description": "large-scale snow flux export, [kg/m2/s]"
    },
    "Faxa_swndr": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "NIR direct shortwave export, [W/m2]"
    },
    "Faxa_swndf": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "NIR diffuse shortwave export, [W/m2]"
    },
    "Faxa_swvdr": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "VIS direct shortwave export, [W/m2]"
    },
    "Faxa_swvdf": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "VIS diffuse shortwave export, [W/m2]"
    },
    "Faxa_swnet": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "net shortwave export (albedo-weighted sum; 0 when the Sx imports are spval/tiny; plain sum when absent), [W/m2]"
    },
    "Faxa_swdn": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "incoming shortwave export = stream, [W/m2]"
    },
    "Faxa_lwdn": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "incoming longwave export = stream (or the ea sigma T^4 fallback), [W/m2]"
    }
  },
  "equations": [
    {
      "lhs": "Sa_tbot",
      "rhs": {
        "op": "max",
        "args": [
          {
            "op": "const",
            "args": [],
            "value": 180.0,
            "units": "K"
          },
          {
            "op": "+",
            "args": [
              "strm_tbot",
              {
                "op": "ifelse",
                "args": [
                  {
                    "op": "<",
                    "args": [
                      "tbotmax",
                      {
                        "op": "const",
                        "args": [],
                        "value": 50.0,
                        "units": "K"
                      }
                    ]
                  },
                  {
                    "op": "const",
                    "args": [],
                    "value": 273.15,
                    "units": "K"
                  },
                  {
                    "op": "const",
                    "args": [],
                    "value": 0.0,
                    "units": "K"
                  }
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "Sa_ptem",
      "rhs": "Sa_tbot"
    },
    {
      "lhs": "Sa_pbot",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "==",
            "args": [
              "pbot_present",
              {
                "op": "const",
                "args": [],
                "value": 0.0,
                "units": "1"
              }
            ]
          },
          {
            "op": "const",
            "args": [],
            "value": 101325.0,
            "units": "Pa"
          },
          {
            "op": "ifelse",
            "args": [
              {
                "op": "==",
                "args": [
                  "strm_pbot",
                  {
                    "op": "const",
                    "args": [],
                    "value": 0.0,
                    "units": "Pa"
                  }
                ]
              },
              {
                "op": "const",
                "args": [],
                "value": 101325.0,
                "units": "Pa"
              },
              "strm_pbot"
            ]
          }
        ]
      }
    },
    {
      "lhs": "Sa_pslv",
      "rhs": "Sa_pbot"
    },
    {
      "lhs": "Sa_u",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "wind_split",
        "bindings": {
          "wind": "strm_wind"
        }
      }
    },
    {
      "lhs": "Sa_v",
      "rhs": "Sa_u"
    },
    {
      "lhs": "tdew_k",
      "rhs": {
        "op": "+",
        "args": [
          "strm_tdew",
          {
            "op": "ifelse",
            "args": [
              {
                "op": "<",
                "args": [
                  "tdewmax",
                  {
                    "op": "const",
                    "args": [],
                    "value": 50.0,
                    "units": "K"
                  }
                ]
              },
              {
                "op": "apply_expression_template",
                "args": [],
                "name": "tkfrz",
                "bindings": {}
              },
              {
                "op": "const",
                "args": [],
                "value": 0.0,
                "units": "K"
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "e",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "==",
            "args": [
              "shum_source",
              {
                "op": "const",
                "args": [],
                "value": 3.0,
                "units": "1"
              }
            ]
          },
          {
            "op": "apply_expression_template",
            "args": [],
            "name": "esat",
            "bindings": {
              "tK": "tdew_k",
              "tKbot": "Sa_tbot"
            }
          },
          {
            "op": "ifelse",
            "args": [
              {
                "op": "==",
                "args": [
                  "shum_source",
                  {
                    "op": "const",
                    "args": [],
                    "value": 2.0,
                    "units": "1"
                  }
                ]
              },
              {
                "op": "*",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      "strm_rh",
                      {
                        "op": "const",
                        "args": [],
                        "value": 0.01,
                        "units": "1"
                      }
                    ]
                  },
                  {
                    "op": "apply_expression_template",
                    "args": [],
                    "name": "esat",
                    "bindings": {
                      "tK": "Sa_tbot",
                      "tKbot": "Sa_tbot"
                    }
                  }
                ]
              },
              {
                "op": "apply_expression_template",
                "args": [],
                "name": "esat",
                "bindings": {
                  "tK": "Sa_tbot",
                  "tKbot": "Sa_tbot"
                }
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "qsat_",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "qsat",
        "bindings": {
          "e": "e",
          "pbot": "Sa_pbot"
        }
      }
    },
    {
      "lhs": "Sa_shum",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "==",
            "args": [
              "shum_source",
              {
                "op": "const",
                "args": [],
                "value": 1.0,
                "units": "1"
              }
            ]
          },
          {
            "op": "min",
            "args": [
              "qsat_",
              "strm_shum"
            ]
          },
          "qsat_"
        ]
      }
    },
    {
      "lhs": "vp",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "vapor_pressure",
        "bindings": {
          "q": "Sa_shum",
          "pbot": "Sa_pbot"
        }
      }
    },
    {
      "lhs": "Sa_dens",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "density",
        "bindings": {
          "pbot": "Sa_pbot",
          "vp": "vp",
          "tbot": "Sa_tbot"
        }
      }
    },
    {
      "lhs": "rainc0",
      "rhs": {
        "op": "*",
        "args": [
          {
            "op": "const",
            "args": [],
            "value": 0.1,
            "units": "1"
          },
          "strm_precn"
        ]
      }
    },
    {
      "lhs": "rainl0",
      "rhs": {
        "op": "*",
        "args": [
          {
            "op": "const",
            "args": [],
            "value": 0.9,
            "units": "1"
          },
          "strm_precn"
        ]
      }
    },
    {
      "lhs": "frac",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "rain_snow_frac",
        "bindings": {
          "tbot": "Sa_tbot"
        }
      }
    },
    {
      "lhs": "Faxa_rainc",
      "rhs": {
        "op": "max",
        "args": [
          {
            "op": "const",
            "args": [],
            "value": 0.0,
            "units": "kg/m^2/s"
          },
          {
            "op": "*",
            "args": [
              "rainc0",
              "frac"
            ]
          }
        ]
      }
    },
    {
      "lhs": "Faxa_rainl",
      "rhs": {
        "op": "max",
        "args": [
          {
            "op": "const",
            "args": [],
            "value": 0.0,
            "units": "kg/m^2/s"
          },
          {
            "op": "*",
            "args": [
              "rainl0",
              "frac"
            ]
          }
        ]
      }
    },
    {
      "lhs": "Faxa_snowc",
      "rhs": {
        "op": "max",
        "args": [
          {
            "op": "const",
            "args": [],
            "value": 0.0,
            "units": "kg/m^2/s"
          },
          {
            "op": "*",
            "args": [
              "rainc0",
              {
                "op": "-",
                "args": [
                  {
                    "op": "const",
                    "args": [],
                    "value": 1.0,
                    "units": "1"
                  },
                  "frac"
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "Faxa_snowl",
      "rhs": {
        "op": "max",
        "args": [
          {
            "op": "const",
            "args": [],
            "value": 0.0,
            "units": "kg/m^2/s"
          },
          {
            "op": "*",
            "args": [
              "rainl0",
              {
                "op": "-",
                "args": [
                  {
                    "op": "const",
                    "args": [],
                    "value": 1.0,
                    "units": "1"
                  },
                  "frac"
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "swdn_half",
      "rhs": {
        "op": "*",
        "args": [
          {
            "op": "const",
            "args": [],
            "value": 0.5,
            "units": "1"
          },
          "strm_swdn"
        ]
      }
    },
    {
      "lhs": "ratio_nir",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "ratio_rvrf_nir",
        "bindings": {
          "s": "swdn_half"
        }
      }
    },
    {
      "lhs": "ratio_vis",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "ratio_rvrf_vis",
        "bindings": {
          "s": "swdn_half"
        }
      }
    },
    {
      "lhs": "Faxa_swndr",
      "rhs": {
        "op": "*",
        "args": [
          "ratio_nir",
          "swdn_half"
        ]
      }
    },
    {
      "lhs": "Faxa_swndf",
      "rhs": {
        "op": "*",
        "args": [
          {
            "op": "-",
            "args": [
              {
                "op": "const",
                "args": [],
                "value": 1.0,
                "units": "1"
              },
              "ratio_nir"
            ]
          },
          "swdn_half"
        ]
      }
    },
    {
      "lhs": "Faxa_swvdr",
      "rhs": {
        "op": "*",
        "args": [
          "ratio_vis",
          "swdn_half"
        ]
      }
    },
    {
      "lhs": "Faxa_swvdf",
      "rhs": {
        "op": "*",
        "args": [
          {
            "op": "-",
            "args": [
              {
                "op": "const",
                "args": [],
                "value": 1.0,
                "units": "1"
              },
              "ratio_vis"
            ]
          },
          "swdn_half"
        ]
      }
    },
    {
      "lhs": "Faxa_swnet",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "or",
            "args": [
              {
                "op": "<",
                "args": [
                  "anidrmax",
                  {
                    "op": "const",
                    "args": [],
                    "value": 1e-08,
                    "units": "W/m^2"
                  }
                ]
              },
              {
                "op": ">",
                "args": [
                  "anidrmax",
                  {
                    "op": "const",
                    "args": [],
                    "value": 9e+29,
                    "units": "W/m^2"
                  }
                ]
              }
            ]
          },
          {
            "op": "const",
            "args": [],
            "value": 0.0,
            "units": "W/m^2"
          },
          {
            "op": "ifelse",
            "args": [
              {
                "op": "<",
                "args": [
                  "Sx_anidr",
                  {
                    "op": "const",
                    "args": [],
                    "value": 1e+30,
                    "units": "1"
                  }
                ]
              },
              {
                "op": "+",
                "args": [
                  {
                    "op": "+",
                    "args": [
                      {
                        "op": "*",
                        "args": [
                          {
                            "op": "-",
                            "args": [
                              {
                                "op": "const",
                                "args": [],
                                "value": 1.0,
                                "units": "1"
                              },
                              "Sx_anidr"
                            ]
                          },
                          "Faxa_swndr"
                        ]
                      },
                      {
                        "op": "*",
                        "args": [
                          {
                            "op": "-",
                            "args": [
                              {
                                "op": "const",
                                "args": [],
                                "value": 1.0,
                                "units": "1"
                              },
                              "Sx_avsdr"
                            ]
                          },
                          "Faxa_swvdr"
                        ]
                      }
                    ]
                  },
                  {
                    "op": "+",
                    "args": [
                      {
                        "op": "*",
                        "args": [
                          {
                            "op": "-",
                            "args": [
                              {
                                "op": "const",
                                "args": [],
                                "value": 1.0,
                                "units": "1"
                              },
                              "Sx_anidf"
                            ]
                          },
                          "Faxa_swndf"
                        ]
                      },
                      {
                        "op": "*",
                        "args": [
                          {
                            "op": "-",
                            "args": [
                              {
                                "op": "const",
                                "args": [],
                                "value": 1.0,
                                "units": "1"
                              },
                              "Sx_avsdf"
                            ]
                          },
                          "Faxa_swvdf"
                        ]
                      }
                    ]
                  }
                ]
              },
              {
                "op": "+",
                "args": [
                  {
                    "op": "+",
                    "args": [
                      "Faxa_swndr",
                      "Faxa_swvdr"
                    ]
                  },
                  {
                    "op": "+",
                    "args": [
                      "Faxa_swndf",
                      "Faxa_swvdf"
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "Faxa_swdn",
      "rhs": "strm_swdn"
    },
    {
      "lhs": "e2",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "vapor_pressure",
        "bindings": {
          "q": "Sa_shum",
          "pbot": "Sa_pslv"
        }
      }
    },
    {
      "lhs": "ea",
      "rhs": {
        "op": "+",
        "args": [
          {
            "op": "const",
            "args": [],
            "value": 0.7,
            "units": "1"
          },
          {
            "op": "*",
            "args": [
              {
                "op": "const",
                "args": [],
                "value": 5.95e-05,
                "units": "1/Pa"
              },
              {
                "op": "*",
                "args": [
                  {
                    "op": "const",
                    "args": [],
                    "value": 0.01,
                    "units": "1"
                  },
                  {
                    "op": "*",
                    "args": [
                      "e2",
                      {
                        "op": "exp",
                        "args": [
                          {
                            "op": "/",
                            "args": [
                              {
                                "op": "const",
                                "args": [],
                                "value": 1500.0,
                                "units": "K"
                              },
                              "Sa_tbot"
                            ]
                          }
                        ]
                      }
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "Faxa_lwdn",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "==",
            "args": [
              "lwdn_present",
              {
                "op": "const",
                "args": [],
                "value": 0.0,
                "units": "1"
              }
            ]
          },
          {
            "op": "*",
            "args": [
              "ea",
              {
                "op": "*",
                "args": [
                  {
                    "op": "const",
                    "args": [],
                    "value": 5.67e-08,
                    "units": "W/(m^2*K^4)"
                  },
                  {
                    "op": "^",
                    "args": [
                      "Sa_tbot",
                      4
                    ]
                  }
                ]
              }
            ]
          },
          "strm_lwdn"
        ]
      }
    },
    {
      "lhs": "Sa_topo",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "==",
            "args": [
              "topo_present",
              {
                "op": "const",
                "args": [],
                "value": 0.0,
                "units": "1"
              }
            ]
          },
          {
            "op": "const",
            "args": [],
            "value": 1e+30,
            "units": "m"
          },
          "strm_topo"
        ]
      }
    },
    {
      "lhs": "Sa_z",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": ">=",
            "args": [
              "strm_z",
              {
                "op": "const",
                "args": [],
                "value": 1e+30,
                "units": "m"
              }
            ]
          },
          {
            "op": "const",
            "args": [],
            "value": 30.0,
            "units": "m"
          },
          "strm_z"
        ]
      }
    }
  ],
  "tests": [
    {
      "id": "step0_p1",
      "description": "Traced datamode row step 0 point 1 (lon 0, lat -90): the full stream->export chain at the first coupling step. tbotmax = 310.35 K (no tkfrz adjustment), anidrmax = 1e30 (Sx imports absent -> swnet = 0), tbot = 249.309 K < 273.15 -> frac = 0 (all snow), shum = min(qsat, 7.5549e-4) = 6.4803e-4 (qsat caps), swdn split via the ratio_rvrf polynomials (datm_gswp3_streams.csv / datm_gswp3_exports.csv).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "strm_tbot": 249.30924313863048,
        "strm_pbot": 68134.13610026057,
        "strm_wind": 4.88208296870192,
        "strm_shum": 0.0007554910110128631,
        "strm_lwdn": 147.6519253730771,
        "strm_swdn": 429.97176732088275,
        "strm_precn": 5.22216069182629e-06,
        "strm_topo": 2824.921026576389,
        "strm_z": 1e+30,
        "tbotmax": 310.35066065749163,
        "anidrmax": 1e+30
      },
      "assertions": [
        {
          "variable": "Sa_topo",
          "time": 0.0,
          "expected": 2824.921026576389
        },
        {
          "variable": "Sa_z",
          "time": 0.0,
          "expected": 30.0
        },
        {
          "variable": "Sa_u",
          "time": 0.0,
          "expected": 3.452153973484479
        },
        {
          "variable": "Sa_v",
          "time": 0.0,
          "expected": 3.452153973484479
        },
        {
          "variable": "Sa_tbot",
          "time": 0.0,
          "expected": 249.30924313863048
        },
        {
          "variable": "Sa_ptem",
          "time": 0.0,
          "expected": 249.30924313863048
        },
        {
          "variable": "Sa_shum",
          "time": 0.0,
          "expected": 0.0006480331532619146,
          "tolerance": {
            "rel": 1e-11
          }
        },
        {
          "variable": "Sa_dens",
          "time": 0.0,
          "expected": 0.9517205665016577,
          "tolerance": {
            "rel": 1e-11
          }
        },
        {
          "variable": "Sa_pbot",
          "time": 0.0,
          "expected": 68134.13610026057
        },
        {
          "variable": "Sa_pslv",
          "time": 0.0,
          "expected": 68134.13610026057
        },
        {
          "variable": "Faxa_rainc",
          "time": 0.0,
          "expected": 0.0
        },
        {
          "variable": "Faxa_rainl",
          "time": 0.0,
          "expected": 0.0
        },
        {
          "variable": "Faxa_snowc",
          "time": 0.0,
          "expected": 5.222160691826291e-07
        },
        {
          "variable": "Faxa_snowl",
          "time": 0.0,
          "expected": 4.699944622643661e-06
        },
        {
          "variable": "Faxa_swndr",
          "time": 0.0,
          "expected": 179.6370757987365,
          "tolerance": {
            "rel": 1e-11
          }
        },
        {
          "variable": "Faxa_swndf",
          "time": 0.0,
          "expected": 35.348807861704884,
          "tolerance": {
            "rel": 1e-11
          }
        },
        {
          "variable": "Faxa_swvdr",
          "time": 0.0,
          "expected": 141.46489999577733,
          "tolerance": {
            "rel": 1e-11
          }
        },
        {
          "variable": "Faxa_swvdf",
          "time": 0.0,
          "expected": 73.52098366466403,
          "tolerance": {
            "rel": 1e-11
          }
        },
        {
          "variable": "Faxa_swnet",
          "time": 0.0,
          "expected": 0.0
        },
        {
          "variable": "Faxa_swdn",
          "time": 0.0,
          "expected": 429.97176732088275
        },
        {
          "variable": "Faxa_lwdn",
          "time": 0.0,
          "expected": 147.6519253730771
        }
      ],
      "tolerance": {
        "rel": 1e-12
      }
    },
    {
      "id": "step11_p1",
      "description": "Traced datamode row step 11 point 1 (05:30 UTC): weaker wind (1.79 m/s -> u = v = 1.2656), slightly different tbot/pbot/precn; still all-snow (tbot = 249.36 K).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "strm_tbot": 249.361815000464,
        "strm_pbot": 68124.74884620964,
        "strm_wind": 1.7898325886439403,
        "strm_shum": 0.0007548493967786151,
        "strm_lwdn": 145.79053868187884,
        "strm_swdn": 437.95537962233925,
        "strm_precn": 5.524998584307837e-06,
        "strm_topo": 2824.921026576389,
        "strm_z": 1e+30,
        "tbotmax": 310.35066065749163,
        "anidrmax": 1e+30
      },
      "assertions": [
        {
          "variable": "Sa_u",
          "time": 0.0,
          "expected": 1.2656027606188025
        },
        {
          "variable": "Sa_v",
          "time": 0.0,
          "expected": 1.2656027606188025
        },
        {
          "variable": "Sa_tbot",
          "time": 0.0,
          "expected": 249.361815000464
        },
        {
          "variable": "Sa_shum",
          "time": 0.0,
          "expected": 0.0006515049554584835,
          "tolerance": {
            "rel": 1e-11
          }
        },
        {
          "variable": "Sa_dens",
          "time": 0.0,
          "expected": 0.9513868162151617,
          "tolerance": {
            "rel": 1e-11
          }
        },
        {
          "variable": "Faxa_snowc",
          "time": 0.0,
          "expected": 5.524998584307837e-07
        },
        {
          "variable": "Faxa_snowl",
          "time": 0.0,
          "expected": 4.972498725877053e-06
        },
        {
          "variable": "Faxa_swndr",
          "time": 0.0,
          "expected": 183.5416775681492,
          "tolerance": {
            "rel": 1e-11
          }
        },
        {
          "variable": "Faxa_swndf",
          "time": 0.0,
          "expected": 35.43601224302044,
          "tolerance": {
            "rel": 1e-11
          }
        },
        {
          "variable": "Faxa_swvdr",
          "time": 0.0,
          "expected": 145.00214991294726,
          "tolerance": {
            "rel": 1e-11
          }
        },
        {
          "variable": "Faxa_swvdf",
          "time": 0.0,
          "expected": 73.97553989822235,
          "tolerance": {
            "rel": 1e-11
          }
        },
        {
          "variable": "Faxa_swnet",
          "time": 0.0,
          "expected": 0.0
        }
      ],
      "tolerance": {
        "rel": 1e-12
      }
    },
    {
      "id": "step0_p16",
      "description": "Traced datamode row step 0 point 16 (lon 37.5, lat -90): the swdn differs in the 8th significant digit from point 1 (4.29971767320882691e2 vs ...748e2), so the shortwave split pins the per-point values.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "parameter_overrides": {
        "strm_tbot": 249.30924313863048,
        "strm_pbot": 68134.13610026057,
        "strm_wind": 4.88208296870192,
        "strm_shum": 0.0007554910110128631,
        "strm_lwdn": 147.6519253730771,
        "strm_swdn": 429.9717673208827,
        "strm_precn": 5.22216069182629e-06,
        "strm_topo": 2824.921026576389,
        "strm_z": 1e+30,
        "tbotmax": 310.35066065749163,
        "anidrmax": 1e+30
      },
      "assertions": [
        {
          "variable": "Faxa_swndr",
          "time": 0.0,
          "expected": 179.6370757987365,
          "tolerance": {
            "rel": 1e-11
          }
        },
        {
          "variable": "Faxa_swndf",
          "time": 0.0,
          "expected": 35.348807861704856,
          "tolerance": {
            "rel": 1e-11
          }
        },
        {
          "variable": "Faxa_swvdr",
          "time": 0.0,
          "expected": 141.4648999957773,
          "tolerance": {
            "rel": 1e-11
          }
        },
        {
          "variable": "Faxa_swvdf",
          "time": 0.0,
          "expected": 73.52098366466404,
          "tolerance": {
            "rel": 1e-11
          }
        },
        {
          "variable": "Faxa_snowc",
          "time": 0.0,
          "expected": 5.222160691826291e-07
        },
        {
          "variable": "Faxa_snowl",
          "time": 0.0,
          "expected": 4.699944622643661e-06
        }
      ],
      "tolerance": {
        "rel": 1e-12
      }
    },
    {
      "id": "branch_tbot_degc",
      "description": "The tbot units detector (F90:384): tbotmax < 50 means degC, TKFRZ is added (strm_tbot = 10 degC -> 283.15 K). Expected values: closed-form recomputation with an independent Python transcription of datm_datamode_clmncep_advance (the same transcription reproduces all 192 traced export rows to <= 1e-15 relative); no traced dump row exercises this branch.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "tolerance": {
        "rel": 1e-12
      },
      "parameter_overrides": {
        "strm_tbot": 10.0,
        "strm_pbot": 95000.0,
        "strm_wind": 4.0,
        "strm_shum": 0.004,
        "strm_lwdn": 300.0,
        "strm_swdn": 400.0,
        "strm_precn": 1e-05,
        "strm_topo": 500.0,
        "strm_z": 1e+30,
        "tbotmax": 10.0,
        "anidrmax": 1e+30
      },
      "assertions": [
        {
          "variable": "Sa_tbot",
          "time": 0.0,
          "expected": 283.15
        },
        {
          "variable": "Sa_ptem",
          "time": 0.0,
          "expected": 283.15
        }
      ]
    },
    {
      "id": "branch_tbot_floor",
      "description": "The 180 K floor (F90:386): strm_tbot = -100 degC with tbotmax = -100 -> max(180, 173.15) = 180 K. Expected values: closed-form recomputation with an independent Python transcription of datm_datamode_clmncep_advance (the same transcription reproduces all 192 traced export rows to <= 1e-15 relative); no traced dump row exercises this branch.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "tolerance": {
        "rel": 1e-12
      },
      "parameter_overrides": {
        "strm_tbot": -100.0,
        "strm_pbot": 95000.0,
        "strm_wind": 4.0,
        "strm_shum": 0.004,
        "strm_lwdn": 300.0,
        "strm_swdn": 400.0,
        "strm_precn": 1e-05,
        "strm_topo": 500.0,
        "strm_z": 1e+30,
        "tbotmax": -100.0,
        "anidrmax": 1e+30
      },
      "assertions": [
        {
          "variable": "Sa_tbot",
          "time": 0.0,
          "expected": 180.0
        }
      ]
    },
    {
      "id": "branch_pbot_zero",
      "description": "The pbot zero-fill (F90:394-396): strm_pbot = 0 (masked ocean point) -> Sa_pbot = Sa_pslv = pstd. Expected values: closed-form recomputation with an independent Python transcription of datm_datamode_clmncep_advance (the same transcription reproduces all 192 traced export rows to <= 1e-15 relative); no traced dump row exercises this branch.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "tolerance": {
        "rel": 1e-12
      },
      "parameter_overrides": {
        "strm_tbot": 280.0,
        "strm_pbot": 0.0,
        "strm_wind": 4.0,
        "strm_shum": 0.004,
        "strm_lwdn": 300.0,
        "strm_swdn": 400.0,
        "strm_precn": 1e-05,
        "strm_topo": 500.0,
        "strm_z": 1e+30,
        "tbotmax": 300.0,
        "anidrmax": 1e+30
      },
      "assertions": [
        {
          "variable": "Sa_pbot",
          "time": 0.0,
          "expected": 101325.0
        },
        {
          "variable": "Sa_pslv",
          "time": 0.0,
          "expected": 101325.0
        },
        {
          "variable": "Sa_dens",
          "time": 0.0,
          "expected": 1.257645470601843
        }
      ]
    },
    {
      "id": "branch_pbot_absent",
      "description": "No pressure stream (pbot_present = 0, F90:390-391): Sa_pbot = pstd whatever strm_pbot holds. Expected values: closed-form recomputation with an independent Python transcription of datm_datamode_clmncep_advance (the same transcription reproduces all 192 traced export rows to <= 1e-15 relative); no traced dump row exercises this branch.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "tolerance": {
        "rel": 1e-12
      },
      "parameter_overrides": {
        "strm_tbot": 280.0,
        "strm_pbot": 12345.0,
        "strm_wind": 4.0,
        "strm_shum": 0.004,
        "strm_lwdn": 300.0,
        "strm_swdn": 400.0,
        "strm_precn": 1e-05,
        "strm_topo": 500.0,
        "strm_z": 1e+30,
        "tbotmax": 300.0,
        "anidrmax": 1e+30,
        "pbot_present": 0.0
      },
      "assertions": [
        {
          "variable": "Sa_pbot",
          "time": 0.0,
          "expected": 101325.0
        },
        {
          "variable": "Sa_shum",
          "time": 0.0,
          "expected": 0.004
        },
        {
          "variable": "Sa_dens",
          "time": 0.0,
          "expected": 1.257645470601843
        }
      ]
    },
    {
      "id": "branch_shum_qsat_cap",
      "description": "The qsat cap on the shum path (F90:411-417): tbot = 283.15 K (water phase, e = esat(10 C)), pbot = 101325 Pa; a stream shum of 9e-3 exceeds qsat and is capped to it. Expected values: closed-form recomputation with an independent Python transcription of datm_datamode_clmncep_advance (the same transcription reproduces all 192 traced export rows to <= 1e-15 relative); no traced dump row exercises this branch.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "tolerance": {
        "rel": 1e-12
      },
      "parameter_overrides": {
        "strm_tbot": 283.15,
        "strm_pbot": 101325.0,
        "strm_wind": 4.0,
        "strm_shum": 0.009,
        "strm_lwdn": 300.0,
        "strm_swdn": 400.0,
        "strm_precn": 1e-05,
        "strm_topo": 500.0,
        "strm_z": 1e+30,
        "tbotmax": 283.15,
        "anidrmax": 1e+30
      },
      "assertions": [
        {
          "variable": "Sa_shum",
          "time": 0.0,
          "expected": 0.0075672319664761
        },
        {
          "variable": "Sa_dens",
          "time": 0.0,
          "expected": 1.2409706227936699
        }
      ]
    },
    {
      "id": "branch_shum_rh",
      "description": "The relative-humidity path (F90:418-421; shum_source = 2, not used by GSWP3, which supplies QBOT): e = rh*0.01*esat(tbot), Sa_shum = qsat(e). Expected values: closed-form recomputation with an independent Python transcription of datm_datamode_clmncep_advance (the same transcription reproduces all 192 traced export rows to <= 1e-15 relative); no traced dump row exercises this branch.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "tolerance": {
        "rel": 1e-12
      },
      "parameter_overrides": {
        "strm_tbot": 280.0,
        "strm_pbot": 95000.0,
        "strm_wind": 4.0,
        "strm_shum": 0.0,
        "strm_lwdn": 300.0,
        "strm_swdn": 400.0,
        "strm_precn": 1e-05,
        "strm_topo": 500.0,
        "strm_z": 1e+30,
        "tbotmax": 300.0,
        "anidrmax": 1e+30,
        "shum_source": 2.0,
        "strm_rh": 65.0
      },
      "assertions": [
        {
          "variable": "Sa_shum",
          "time": 0.0,
          "expected": 0.004228109226224205
        },
        {
          "variable": "Sa_dens",
          "time": 0.0,
          "expected": 1.1789765570915693
        }
      ]
    },
    {
      "id": "branch_shum_tdew_degc",
      "description": "The dew-point path (F90:422-427; shum_source = 3, not used by GSWP3): tdewmax < 50 so the dew point is in degC and TKFRZ is added; e = esat(tdew) with the phase of tbot (water, 280 K), Sa_shum = qsat(e). Expected values: closed-form recomputation with an independent Python transcription of datm_datamode_clmncep_advance (the same transcription reproduces all 192 traced export rows to <= 1e-15 relative); no traced dump row exercises this branch.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "tolerance": {
        "rel": 1e-12
      },
      "parameter_overrides": {
        "strm_tbot": 280.0,
        "strm_pbot": 95000.0,
        "strm_wind": 4.0,
        "strm_shum": 0.0,
        "strm_lwdn": 300.0,
        "strm_swdn": 400.0,
        "strm_precn": 1e-05,
        "strm_topo": 500.0,
        "strm_z": 1e+30,
        "tbotmax": 300.0,
        "anidrmax": 1e+30,
        "shum_source": 3.0,
        "strm_tdew": 2.5,
        "tdewmax": 20.0
      },
      "assertions": [
        {
          "variable": "Sa_shum",
          "time": 0.0,
          "expected": 0.004800417678110948
        },
        {
          "variable": "Sa_dens",
          "time": 0.0,
          "expected": 1.1785676999166335
        }
      ]
    },
    {
      "id": "branch_shum_tdew_ice",
      "description": "The dew-point path with tbot below freezing (ice-phase esat polynomial selected by tbot, F90:424) and the dew point already in K (tdewmax >= 50). Expected values: closed-form recomputation with an independent Python transcription of datm_datamode_clmncep_advance (the same transcription reproduces all 192 traced export rows to <= 1e-15 relative); no traced dump row exercises this branch.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "tolerance": {
        "rel": 1e-12
      },
      "parameter_overrides": {
        "strm_tbot": 265.0,
        "strm_pbot": 95000.0,
        "strm_wind": 4.0,
        "strm_shum": 0.0,
        "strm_lwdn": 300.0,
        "strm_swdn": 400.0,
        "strm_precn": 1e-05,
        "strm_topo": 500.0,
        "strm_z": 1e+30,
        "tbotmax": 300.0,
        "anidrmax": 1e+30,
        "shum_source": 3.0,
        "strm_tdew": 260.0,
        "tdewmax": 290.0
      },
      "assertions": [
        {
          "variable": "Sa_shum",
          "time": 0.0,
          "expected": 0.0012818869031005298
        }
      ]
    },
    {
      "id": "branch_rain_full",
      "description": "All rain (tbot = 285 K >= tkfrz + 2, frac = 1, shr_precip_partition_rain_snow_ramp): rainc = 0.1 precn, rainl = 0.9 precn, no snow. Expected values: closed-form recomputation with an independent Python transcription of datm_datamode_clmncep_advance (the same transcription reproduces all 192 traced export rows to <= 1e-15 relative); no traced dump row exercises this branch.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "tolerance": {
        "rel": 1e-12
      },
      "parameter_overrides": {
        "strm_tbot": 285.0,
        "strm_pbot": 95000.0,
        "strm_wind": 4.0,
        "strm_shum": 0.004,
        "strm_lwdn": 300.0,
        "strm_swdn": 400.0,
        "strm_precn": 1e-05,
        "strm_topo": 500.0,
        "strm_z": 1e+30,
        "tbotmax": 300.0,
        "anidrmax": 1e+30
      },
      "assertions": [
        {
          "variable": "Faxa_rainc",
          "time": 0.0,
          "expected": 1.0000000000000002e-06
        },
        {
          "variable": "Faxa_rainl",
          "time": 0.0,
          "expected": 9e-06
        },
        {
          "variable": "Faxa_snowc",
          "time": 0.0,
          "expected": 0.0
        },
        {
          "variable": "Faxa_snowl",
          "time": 0.0,
          "expected": 0.0
        }
      ]
    },
    {
      "id": "branch_rain_snow_ramp",
      "description": "Mid-ramp (tbot = 274.4 K, frac = (tbot - tkfrz)*0.5 = 0.625): precipitation split between rain and snow. Expected values: closed-form recomputation with an independent Python transcription of datm_datamode_clmncep_advance (the same transcription reproduces all 192 traced export rows to <= 1e-15 relative); no traced dump row exercises this branch.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "tolerance": {
        "rel": 1e-12
      },
      "parameter_overrides": {
        "strm_tbot": 274.4,
        "strm_pbot": 95000.0,
        "strm_wind": 4.0,
        "strm_shum": 0.004,
        "strm_lwdn": 300.0,
        "strm_swdn": 400.0,
        "strm_precn": 1e-05,
        "strm_topo": 500.0,
        "strm_z": 1e+30,
        "tbotmax": 300.0,
        "anidrmax": 1e+30
      },
      "assertions": [
        {
          "variable": "Faxa_rainc",
          "time": 0.0,
          "expected": 6.250000000000002e-07
        },
        {
          "variable": "Faxa_rainl",
          "time": 0.0,
          "expected": 5.625e-06
        },
        {
          "variable": "Faxa_snowc",
          "time": 0.0,
          "expected": 3.7500000000000006e-07
        },
        {
          "variable": "Faxa_snowl",
          "time": 0.0,
          "expected": 3.375e-06
        }
      ]
    },
    {
      "id": "branch_lwdn_fallback",
      "description": "No longwave stream (lwdn_present = 0, F90:432-436): Faxa_lwdn = ea*stebol*tbot^4 with ea = 0.70 + 5.95e-5*0.01*e*exp(1500/tbot), e the vapor pressure at Sa_pslv. Expected values: closed-form recomputation with an independent Python transcription of datm_datamode_clmncep_advance (the same transcription reproduces all 192 traced export rows to <= 1e-15 relative); no traced dump row exercises this branch.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "tolerance": {
        "rel": 1e-12
      },
      "parameter_overrides": {
        "strm_tbot": 280.0,
        "strm_pbot": 95000.0,
        "strm_wind": 4.0,
        "strm_shum": 0.004,
        "strm_lwdn": 0.0,
        "strm_swdn": 400.0,
        "strm_precn": 1e-05,
        "strm_topo": 500.0,
        "strm_z": 1e+30,
        "tbotmax": 300.0,
        "anidrmax": 1e+30,
        "lwdn_present": 0.0
      },
      "assertions": [
        {
          "variable": "Faxa_lwdn",
          "time": 0.0,
          "expected": 270.76398477196267
        }
      ]
    },
    {
      "id": "branch_topo_absent",
      "description": "No topo stream (topo_present = 0, F90:337-340): Sa_topo = SHR_CONST_SPVAL = 1e30. Expected values: closed-form recomputation with an independent Python transcription of datm_datamode_clmncep_advance (the same transcription reproduces all 192 traced export rows to <= 1e-15 relative); no traced dump row exercises this branch.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "tolerance": {
        "rel": 1e-12
      },
      "parameter_overrides": {
        "strm_tbot": 280.0,
        "strm_pbot": 95000.0,
        "strm_wind": 4.0,
        "strm_shum": 0.004,
        "strm_lwdn": 300.0,
        "strm_swdn": 400.0,
        "strm_precn": 1e-05,
        "strm_topo": 500.0,
        "strm_z": 1e+30,
        "tbotmax": 300.0,
        "anidrmax": 1e+30,
        "topo_present": 0.0
      },
      "assertions": [
        {
          "variable": "Sa_topo",
          "time": 0.0,
          "expected": 1e+30
        }
      ]
    },
    {
      "id": "branch_z_stream",
      "description": "A bottom-height stream present (strm_z < spval): Sa_z = strm_z instead of the 30 m default (F90:376-380). Expected values: closed-form recomputation with an independent Python transcription of datm_datamode_clmncep_advance (the same transcription reproduces all 192 traced export rows to <= 1e-15 relative); no traced dump row exercises this branch.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "tolerance": {
        "rel": 1e-12
      },
      "parameter_overrides": {
        "strm_tbot": 280.0,
        "strm_pbot": 95000.0,
        "strm_wind": 4.0,
        "strm_shum": 0.004,
        "strm_lwdn": 300.0,
        "strm_swdn": 400.0,
        "strm_precn": 1e-05,
        "strm_topo": 500.0,
        "strm_z": 10.0,
        "tbotmax": 300.0,
        "anidrmax": 1e+30
      },
      "assertions": [
        {
          "variable": "Sa_z",
          "time": 0.0,
          "expected": 10.0
        }
      ]
    },
    {
      "id": "branch_swnet_albedo",
      "description": "Albedo-weighted net shortwave (F90:466-470; atm_prognostic albedos present, anidrmax within (1e-8, 0.9 spval)): swnet = sum (1 - albedo) * band flux over the four bands. Expected values: closed-form recomputation with an independent Python transcription of datm_datamode_clmncep_advance (the same transcription reproduces all 192 traced export rows to <= 1e-15 relative); no traced dump row exercises this branch.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "tolerance": {
        "rel": 1e-12
      },
      "parameter_overrides": {
        "strm_tbot": 280.0,
        "strm_pbot": 95000.0,
        "strm_wind": 4.0,
        "strm_shum": 0.004,
        "strm_lwdn": 300.0,
        "strm_swdn": 400.0,
        "strm_precn": 1e-05,
        "strm_topo": 500.0,
        "strm_z": 1e+30,
        "tbotmax": 300.0,
        "anidrmax": 0.35,
        "Sx_anidr": 0.3,
        "Sx_avsdr": 0.15,
        "Sx_anidf": 0.35,
        "Sx_avsdf": 0.2
      },
      "assertions": [
        {
          "variable": "Faxa_swndr",
          "time": 0.0,
          "expected": 164.8496
        },
        {
          "variable": "Faxa_swndf",
          "time": 0.0,
          "expected": 35.15039999999998
        },
        {
          "variable": "Faxa_swvdr",
          "time": 0.0,
          "expected": 128.26296000000002
        },
        {
          "variable": "Faxa_swvdf",
          "time": 0.0,
          "expected": 71.73703999999998
        },
        {
          "variable": "Faxa_swnet",
          "time": 0.0,
          "expected": 304.655628
        }
      ]
    },
    {
      "id": "branch_swnet_no_albedo",
      "description": "anidrmax valid but the albedo imports absent (Sx_anidr = spval, F90:471-472): swnet = the sum of the four band fluxes. Expected values: closed-form recomputation with an independent Python transcription of datm_datamode_clmncep_advance (the same transcription reproduces all 192 traced export rows to <= 1e-15 relative); no traced dump row exercises this branch.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "tolerance": {
        "rel": 1e-12
      },
      "parameter_overrides": {
        "strm_tbot": 280.0,
        "strm_pbot": 95000.0,
        "strm_wind": 4.0,
        "strm_shum": 0.004,
        "strm_lwdn": 300.0,
        "strm_swdn": 400.0,
        "strm_precn": 1e-05,
        "strm_topo": 500.0,
        "strm_z": 1e+30,
        "tbotmax": 300.0,
        "anidrmax": 0.35
      },
      "assertions": [
        {
          "variable": "Faxa_swnet",
          "time": 0.0,
          "expected": 400.0
        }
      ]
    },
    {
      "id": "branch_swnet_zero_anidrmax",
      "description": "anidrmax < 1e-8 (first-call albedos all zero, F90:464-465): swnet = 0. Expected values: closed-form recomputation with an independent Python transcription of datm_datamode_clmncep_advance (the same transcription reproduces all 192 traced export rows to <= 1e-15 relative); no traced dump row exercises this branch.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "tolerance": {
        "rel": 1e-12
      },
      "parameter_overrides": {
        "strm_tbot": 280.0,
        "strm_pbot": 95000.0,
        "strm_wind": 4.0,
        "strm_shum": 0.004,
        "strm_lwdn": 300.0,
        "strm_swdn": 400.0,
        "strm_precn": 1e-05,
        "strm_topo": 500.0,
        "strm_z": 1e+30,
        "tbotmax": 300.0,
        "anidrmax": 0.0,
        "Sx_anidr": 0.0,
        "Sx_avsdr": 0.0,
        "Sx_anidf": 0.0,
        "Sx_avsdf": 0.0
      },
      "assertions": [
        {
          "variable": "Faxa_swnet",
          "time": 0.0,
          "expected": 0.0
        }
      ]
    },
    {
      "id": "branch_swdn_ratio_clamp",
      "description": "A strong shortwave (swdn = 1300 W/m2, half = 650): both cubic ratio_rvrf polynomials exceed 1 there and are clamped to 0.99 (F90:450-456), a branch the traced (~430 W/m2) rows never reach. Expected values: closed-form recomputation with an independent Python transcription of datm_datamode_clmncep_advance (the same transcription reproduces all 192 traced export rows to <= 1e-15 relative); no traced dump row exercises this branch.",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "tolerance": {
        "rel": 1e-12
      },
      "parameter_overrides": {
        "strm_tbot": 280.0,
        "strm_pbot": 95000.0,
        "strm_wind": 4.0,
        "strm_shum": 0.004,
        "strm_lwdn": 300.0,
        "strm_swdn": 1300.0,
        "strm_precn": 1e-05,
        "strm_topo": 500.0,
        "strm_z": 1e+30,
        "tbotmax": 300.0,
        "anidrmax": 1e+30
      },
      "assertions": [
        {
          "variable": "Faxa_swndr",
          "time": 0.0,
          "expected": 643.5
        },
        {
          "variable": "Faxa_swndf",
          "time": 0.0,
          "expected": 6.500000000000005
        },
        {
          "variable": "Faxa_swvdr",
          "time": 0.0,
          "expected": 643.5
        },
        {
          "variable": "Faxa_swvdf",
          "time": 0.0,
          "expected": 6.500000000000005
        }
      ]
    }
  ]
}
```

</details>
