---
title: "Streams"
slug: "streams"
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
| `swdn_rec` | `W/m^2` | `0.0` | The two stream records bracketing t on the model grid after the spatial map: [1] = the record at or before t (CDEPS LB), [2] = the next record (UB), as a data-fed parameter shaped over the record axis receives them (esm-spec 8.5.1) - Solar FSDS (coszen; the upper record is read but unused by the coszen law). |
| `precn_rec` | `kg/m^2/s` | `0.0` | The two stream records bracketing t on the model grid after the spatial map: [1] = the record at or before t (CDEPS LB), [2] = the next record (UB), as a data-fed parameter shaped over the record axis receives them (esm-spec 8.5.1) - Precip PRECTmms (nearest). |
| `tbot_rec` | `K` | `0.0` | The two stream records bracketing t on the model grid after the spatial map: [1] = the record at or before t (CDEPS LB), [2] = the next record (UB), as a data-fed parameter shaped over the record axis receives them (esm-spec 8.5.1) - TPQW TBOT (linear). |
| `pbot_rec` | `Pa` | `0.0` | The two stream records bracketing t on the model grid after the spatial map: [1] = the record at or before t (CDEPS LB), [2] = the next record (UB), as a data-fed parameter shaped over the record axis receives them (esm-spec 8.5.1) - TPQW PSRF (linear). |
| `wind_rec` | `m/s` | `0.0` | The two stream records bracketing t on the model grid after the spatial map: [1] = the record at or before t (CDEPS LB), [2] = the next record (UB), as a data-fed parameter shaped over the record axis receives them (esm-spec 8.5.1) - TPQW WIND (linear). |
| `shum_rec` | `kg/kg` | `0.0` | The two stream records bracketing t on the model grid after the spatial map: [1] = the record at or before t (CDEPS LB), [2] = the next record (UB), as a data-fed parameter shaped over the record axis receives them (esm-spec 8.5.1) - TPQW QBOT (linear). |
| `lwdn_rec` | `W/m^2` | `0.0` | The two stream records bracketing t on the model grid after the spatial map: [1] = the record at or before t (CDEPS LB), [2] = the next record (UB), as a data-fed parameter shaped over the record axis receives them (esm-spec 8.5.1) - TPQW FLDS (linear). |
| `topo_in` | `m` | `0.0` | The topo.observed stream value (lower; the static topo file holds one record, which a shapeless data-fed parameter receives). |
| `lat` | `deg` | `-90.0` | Latitude of the model-grid point [deg] (the traced points are all at -90). |
| `lon` | `deg` | `0.0` | Longitude of the model-grid point [deg]. |
| `calday0` | `1` | `1.0` | Calendar day (1-based julian day of year including its fraction, noleap calendar) at t = 0; 1.0 = Jan 1 00Z, the reference run's start (2000-01-01T00:00:00Z). |
| `eccen` | `1` | `0.016703660392765603` | Orbital eccentricity (shr_orb_params, orb_iyear 2000; as dumped by the reference run's mediator, cmeps_ocnalb.csv). |
| `obliqr` | `rad` | `0.40910112257977893` | Obliquity [rad] (orb_iyear 2000). |
| `lambm0` | `rad` | `-0.03247249566152933` | Mean longitude of perihelion at the vernal equinox [rad] (orb_iyear 2000). |
| `mvelpp` | `rad` | `4.937457790488158` | Moving vernal equinox longitude of perihelion plus pi [rad] (orb_iyear 2000). |
| `dt_rec` | `s` | `10800.0` | Record spacing of the GSWP3 3-hourly streams [s]. |
| `t0_solar` | `s` | `0.0` | Time of a Solar stream record relative to t = 0 [s] (Solar records at 00,03,..,21Z: time = 0, 0.125, .. days in the file). |
| `t0_tpqw` | `s` | `5400.0` | Time of a TPQW stream record relative to t = 0 [s] (records at 01:30, 04:30, ..Z: time = 0.0625 + 0.125 n days). |
| `t0_precip` | `s` | `5400.0` | Time of a Precip stream record relative to t = 0 [s] (same record times as TPQW). |
| `modeldt` | `s` | `1800.0` | Model (coupling) time step [s] = the sub-step of the coszen time average (ATM_NCPL = 48 in the reference case). The average is written with dt_rec/modeldt = 6 samples; the sample count is structural (see README). |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `calday` | `1` |  | Calendar day at t: calday0 + t/86400 s. |
| `t_lb_solar` | `s` |  | Solar LB time: the record at or before t. |
| `calday_lb` | `1` |  | Calendar day of the Solar LB record. |
| `cosz` | `1` |  | max(0.001, cos solar zenith angle) at t (shr_tInterp_getCosz). |
| `tavcosz` | `1` |  | Time average of the clipped cosz over [LB, UB) on modeldt sub-steps starting at LB (shr_tInterp_getAvgCosz, dshr_tinterp_mod.F90:258-272). |
| `flb_solar` | `1` |  | Coszen factor on the Solar LB record: cosz/tavCosz (unused at night). |
| `day` | `1` |  | 1 when cosz > solZenMin = 0.001 (the coszen law applies), 0 at night (value = 0). |
| `t_lb_tpqw` | `s` |  | TPQW LB time. |
| `flb_tpqw` | `1` |  | Linear factor on the TPQW LB record: (t_UB - t)/(t_UB - t_LB) (shr_tInterp_getFactors 'linear'). |
| `fub_tpqw` | `1` |  | Linear factor on the TPQW UB record: 1 - flb. |
| `t_lb_precip` | `s` |  | Precip LB time. |
| `flb_precip` | `1` |  | Nearest factor on the Precip LB record: 1 when \|t_LB - t\| <= \|t_UB - t\| else 0 (shr_tInterp_getFactors 'nearest'; ties go to LB). |
| `fub_precip` | `1` |  | Nearest factor on the Precip UB record: 1 - flb. |
| `swdn` | `W/m^2` |  | Interpolated stream value of swdn on the model grid (fldbun_model), consumed by the datamode as strm_swdn. |
| `precn` | `kg/m^2/s` |  | Interpolated stream value of precn on the model grid (fldbun_model), consumed by the datamode as strm_precn. |
| `tbot` | `K` |  | Interpolated stream value of tbot on the model grid (fldbun_model), consumed by the datamode as strm_tbot. |
| `pbot` | `Pa` |  | Interpolated stream value of pbot on the model grid (fldbun_model), consumed by the datamode as strm_pbot. |
| `wind` | `m/s` |  | Interpolated stream value of wind on the model grid (fldbun_model), consumed by the datamode as strm_wind. |
| `shum` | `kg/kg` |  | Interpolated stream value of shum on the model grid (fldbun_model), consumed by the datamode as strm_shum. |
| `lwdn` | `W/m^2` |  | Interpolated stream value of lwdn on the model grid (fldbun_model), consumed by the datamode as strm_lwdn. |
| `topo` | `m` |  | Interpolated stream value of topo on the model grid (fldbun_model), consumed by the datamode as strm_topo. |

## Observed expressions

$$
calday = calday0 + \frac{t}{\mathrm{const}\left(\right)}
$$
_Calendar day at t: calday0 + t/86400 s._

$$
t_{lb\,solar} = \mathrm{record_lower_time}\left(t=t, t0=t0_{solar}, dt=dt_{rec}\right)
$$
_Solar LB time: the record at or before t._

$$
calday_{lb} = calday0 + \frac{t_{lb\,solar}}{\mathrm{const}\left(\right)}
$$
_Calendar day of the Solar LB record._

$$
cosz = \mathrm{orb_cosz}\left(calday=calday, lat=lat, lon=lon, eccen=eccen, obliqr=obliqr, lambm0=lambm0, mvelpp=mvelpp\right)
$$
_max(0.001, cos solar zenith angle) at t (shr_tInterp_getCosz)._

$$
tavcosz = \frac{\mathrm{orb_cosz}\left(calday=calday0 + \frac{t_{lb\,solar} + \mathrm{const}\left(\right) \cdot modeldt}{\mathrm{const}\left(\right)}, lat=lat, lon=lon, eccen=eccen, obliqr=obliqr, lambm0=lambm0, mvelpp=mvelpp\right) \cdot modeldt + \mathrm{orb_cosz}\left(calday=calday0 + \frac{t_{lb\,solar} + \mathrm{const}\left(\right) \cdot modeldt}{\mathrm{const}\left(\right)}, lat=lat, lon=lon, eccen=eccen, obliqr=obliqr, lambm0=lambm0, mvelpp=mvelpp\right) \cdot modeldt + \mathrm{orb_cosz}\left(calday=calday0 + \frac{t_{lb\,solar} + \mathrm{const}\left(\right) \cdot modeldt}{\mathrm{const}\left(\right)}, lat=lat, lon=lon, eccen=eccen, obliqr=obliqr, lambm0=lambm0, mvelpp=mvelpp\right) \cdot modeldt + \mathrm{orb_cosz}\left(calday=calday0 + \frac{t_{lb\,solar} + \mathrm{const}\left(\right) \cdot modeldt}{\mathrm{const}\left(\right)}, lat=lat, lon=lon, eccen=eccen, obliqr=obliqr, lambm0=lambm0, mvelpp=mvelpp\right) \cdot modeldt + \mathrm{orb_cosz}\left(calday=calday0 + \frac{t_{lb\,solar} + \mathrm{const}\left(\right) \cdot modeldt}{\mathrm{const}\left(\right)}, lat=lat, lon=lon, eccen=eccen, obliqr=obliqr, lambm0=lambm0, mvelpp=mvelpp\right) \cdot modeldt + \mathrm{orb_cosz}\left(calday=calday0 + \frac{t_{lb\,solar} + \mathrm{const}\left(\right) \cdot modeldt}{\mathrm{const}\left(\right)}, lat=lat, lon=lon, eccen=eccen, obliqr=obliqr, lambm0=lambm0, mvelpp=mvelpp\right) \cdot modeldt}{\mathrm{const}\left(\right) \cdot modeldt}
$$
_Time average of the clipped cosz over [LB, UB) on modeldt sub-steps starting at LB (shr_tInterp_getAvgCosz, dshr_tinterp_mod.F90:258-272)._

$$
flb_{solar} = \frac{cosz}{tavcosz}
$$
_Coszen factor on the Solar LB record: cosz/tavCosz (unused at night)._

$$
day = \mathrm{ifelse}\left(\mathrm{>}\left(cosz, \mathrm{const}\left(\right)\right), \mathrm{const}\left(\right), \mathrm{const}\left(\right)\right)
$$
_1 when cosz > solZenMin = 0.001 (the coszen law applies), 0 at night (value = 0)._

$$
t_{lb\,tpqw} = \mathrm{record_lower_time}\left(t=t, t0=t0_{tpqw}, dt=dt_{rec}\right)
$$
_TPQW LB time._

$$
flb_{tpqw} = \frac{t_{lb\,tpqw} + dt_{rec} - t}{dt_{rec}}
$$
_Linear factor on the TPQW LB record: (t_UB - t)/(t_UB - t_LB) (shr_tInterp_getFactors 'linear')._

$$
fub_{tpqw} = \mathrm{const}\left(\right) - flb_{tpqw}
$$
_Linear factor on the TPQW UB record: 1 - flb._

$$
t_{lb\,precip} = \mathrm{record_lower_time}\left(t=t, t0=t0_{precip}, dt=dt_{rec}\right)
$$
_Precip LB time._

$$
flb_{precip} = \mathrm{ifelse}\left(\mathrm{<=}\left(\left|t_{lb\,precip} - t\right|, \left|t_{lb\,precip} + dt_{rec} - t\right|\right), \mathrm{const}\left(\right), \mathrm{const}\left(\right)\right)
$$
_Nearest factor on the Precip LB record: 1 when |t_LB - t| <= |t_UB - t| else 0 (shr_tInterp_getFactors 'nearest'; ties go to LB)._

$$
fub_{precip} = \mathrm{const}\left(\right) - flb_{precip}
$$
_Nearest factor on the Precip UB record: 1 - flb._

$$
swdn = \mathrm{ifelse}\left(\mathrm{>}\left(cosz, \mathrm{const}\left(\right)\right), \frac{\mathrm{index}\left(swdn_{rec}, 1\right) \cdot cosz}{tavcosz}, \mathrm{const}\left(\right)\right)
$$
_Interpolated stream value of swdn on the model grid (fldbun_model), consumed by the datamode as strm_swdn._

$$
precn = \mathrm{index}\left(precn_{rec}, 1\right) \cdot flb_{precip} + \mathrm{index}\left(precn_{rec}, 2\right) \cdot fub_{precip}
$$
_Interpolated stream value of precn on the model grid (fldbun_model), consumed by the datamode as strm_precn._

$$
tbot = \mathrm{index}\left(tbot_{rec}, 1\right) \cdot flb_{tpqw} + \mathrm{index}\left(tbot_{rec}, 2\right) \cdot fub_{tpqw}
$$
_Interpolated stream value of tbot on the model grid (fldbun_model), consumed by the datamode as strm_tbot._

$$
pbot = \mathrm{index}\left(pbot_{rec}, 1\right) \cdot flb_{tpqw} + \mathrm{index}\left(pbot_{rec}, 2\right) \cdot fub_{tpqw}
$$
_Interpolated stream value of pbot on the model grid (fldbun_model), consumed by the datamode as strm_pbot._

$$
wind = \mathrm{index}\left(wind_{rec}, 1\right) \cdot flb_{tpqw} + \mathrm{index}\left(wind_{rec}, 2\right) \cdot fub_{tpqw}
$$
_Interpolated stream value of wind on the model grid (fldbun_model), consumed by the datamode as strm_wind._

$$
shum = \mathrm{index}\left(shum_{rec}, 1\right) \cdot flb_{tpqw} + \mathrm{index}\left(shum_{rec}, 2\right) \cdot fub_{tpqw}
$$
_Interpolated stream value of shum on the model grid (fldbun_model), consumed by the datamode as strm_shum._

$$
lwdn = \mathrm{index}\left(lwdn_{rec}, 1\right) \cdot flb_{tpqw} + \mathrm{index}\left(lwdn_{rec}, 2\right) \cdot fub_{tpqw}
$$
_Interpolated stream value of lwdn on the model grid (fldbun_model), consumed by the datamode as strm_lwdn._

$$
topo = topo_{in}
$$
_Interpolated stream value of topo on the model grid (fldbun_model), consumed by the datamode as strm_topo._

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
    "swdn_rec": {
      "type": "parameter",
      "units": "W/m^2",
      "default": 0.0,
      "description": "The two stream records bracketing t on the model grid after the spatial map: [1] = the record at or before t (CDEPS LB), [2] = the next record (UB), as a data-fed parameter shaped over the record axis receives them (esm-spec 8.5.1) - Solar FSDS (coszen; the upper record is read but unused by the coszen law).",
      "shape": [
        "rec"
      ]
    },
    "precn_rec": {
      "type": "parameter",
      "units": "kg/m^2/s",
      "default": 0.0,
      "description": "The two stream records bracketing t on the model grid after the spatial map: [1] = the record at or before t (CDEPS LB), [2] = the next record (UB), as a data-fed parameter shaped over the record axis receives them (esm-spec 8.5.1) - Precip PRECTmms (nearest).",
      "shape": [
        "rec"
      ]
    },
    "tbot_rec": {
      "type": "parameter",
      "units": "K",
      "default": 0.0,
      "description": "The two stream records bracketing t on the model grid after the spatial map: [1] = the record at or before t (CDEPS LB), [2] = the next record (UB), as a data-fed parameter shaped over the record axis receives them (esm-spec 8.5.1) - TPQW TBOT (linear).",
      "shape": [
        "rec"
      ]
    },
    "pbot_rec": {
      "type": "parameter",
      "units": "Pa",
      "default": 0.0,
      "description": "The two stream records bracketing t on the model grid after the spatial map: [1] = the record at or before t (CDEPS LB), [2] = the next record (UB), as a data-fed parameter shaped over the record axis receives them (esm-spec 8.5.1) - TPQW PSRF (linear).",
      "shape": [
        "rec"
      ]
    },
    "wind_rec": {
      "type": "parameter",
      "units": "m/s",
      "default": 0.0,
      "description": "The two stream records bracketing t on the model grid after the spatial map: [1] = the record at or before t (CDEPS LB), [2] = the next record (UB), as a data-fed parameter shaped over the record axis receives them (esm-spec 8.5.1) - TPQW WIND (linear).",
      "shape": [
        "rec"
      ]
    },
    "shum_rec": {
      "type": "parameter",
      "units": "kg/kg",
      "default": 0.0,
      "description": "The two stream records bracketing t on the model grid after the spatial map: [1] = the record at or before t (CDEPS LB), [2] = the next record (UB), as a data-fed parameter shaped over the record axis receives them (esm-spec 8.5.1) - TPQW QBOT (linear).",
      "shape": [
        "rec"
      ]
    },
    "lwdn_rec": {
      "type": "parameter",
      "units": "W/m^2",
      "default": 0.0,
      "description": "The two stream records bracketing t on the model grid after the spatial map: [1] = the record at or before t (CDEPS LB), [2] = the next record (UB), as a data-fed parameter shaped over the record axis receives them (esm-spec 8.5.1) - TPQW FLDS (linear).",
      "shape": [
        "rec"
      ]
    },
    "topo_in": {
      "type": "parameter",
      "units": "m",
      "default": 0.0,
      "description": "The topo.observed stream value (lower; the static topo file holds one record, which a shapeless data-fed parameter receives)."
    },
    "lat": {
      "type": "parameter",
      "units": "deg",
      "default": -90.0,
      "description": "Latitude of the model-grid point [deg] (the traced points are all at -90)."
    },
    "lon": {
      "type": "parameter",
      "units": "deg",
      "default": 0.0,
      "description": "Longitude of the model-grid point [deg]."
    },
    "calday0": {
      "type": "parameter",
      "units": "1",
      "default": 1.0,
      "description": "Calendar day (1-based julian day of year including its fraction, noleap calendar) at t = 0; 1.0 = Jan 1 00Z, the reference run's start (2000-01-01T00:00:00Z)."
    },
    "eccen": {
      "type": "parameter",
      "units": "1",
      "default": 0.016703660392765603,
      "description": "Orbital eccentricity (shr_orb_params, orb_iyear 2000; as dumped by the reference run's mediator, cmeps_ocnalb.csv)."
    },
    "obliqr": {
      "type": "parameter",
      "units": "rad",
      "default": 0.40910112257977893,
      "description": "Obliquity [rad] (orb_iyear 2000)."
    },
    "lambm0": {
      "type": "parameter",
      "units": "rad",
      "default": -0.03247249566152933,
      "description": "Mean longitude of perihelion at the vernal equinox [rad] (orb_iyear 2000)."
    },
    "mvelpp": {
      "type": "parameter",
      "units": "rad",
      "default": 4.937457790488158,
      "description": "Moving vernal equinox longitude of perihelion plus pi [rad] (orb_iyear 2000)."
    },
    "dt_rec": {
      "type": "parameter",
      "units": "s",
      "default": 10800.0,
      "description": "Record spacing of the GSWP3 3-hourly streams [s]."
    },
    "t0_solar": {
      "type": "parameter",
      "units": "s",
      "default": 0.0,
      "description": "Time of a Solar stream record relative to t = 0 [s] (Solar records at 00,03,..,21Z: time = 0, 0.125, .. days in the file)."
    },
    "t0_tpqw": {
      "type": "parameter",
      "units": "s",
      "default": 5400.0,
      "description": "Time of a TPQW stream record relative to t = 0 [s] (records at 01:30, 04:30, ..Z: time = 0.0625 + 0.125 n days)."
    },
    "t0_precip": {
      "type": "parameter",
      "units": "s",
      "default": 5400.0,
      "description": "Time of a Precip stream record relative to t = 0 [s] (same record times as TPQW)."
    },
    "modeldt": {
      "type": "parameter",
      "units": "s",
      "default": 1800.0,
      "description": "Model (coupling) time step [s] = the sub-step of the coszen time average (ATM_NCPL = 48 in the reference case). The average is written with dt_rec/modeldt = 6 samples; the sample count is structural (see README)."
    },
    "calday": {
      "type": "unknown",
      "units": "1",
      "description": "Calendar day at t: calday0 + t/86400 s."
    },
    "t_lb_solar": {
      "type": "unknown",
      "units": "s",
      "description": "Solar LB time: the record at or before t."
    },
    "calday_lb": {
      "type": "unknown",
      "units": "1",
      "description": "Calendar day of the Solar LB record."
    },
    "cosz": {
      "type": "unknown",
      "units": "1",
      "description": "max(0.001, cos solar zenith angle) at t (shr_tInterp_getCosz)."
    },
    "tavcosz": {
      "type": "unknown",
      "units": "1",
      "description": "Time average of the clipped cosz over [LB, UB) on modeldt sub-steps starting at LB (shr_tInterp_getAvgCosz, dshr_tinterp_mod.F90:258-272)."
    },
    "flb_solar": {
      "type": "unknown",
      "units": "1",
      "description": "Coszen factor on the Solar LB record: cosz/tavCosz (unused at night)."
    },
    "day": {
      "type": "unknown",
      "units": "1",
      "description": "1 when cosz > solZenMin = 0.001 (the coszen law applies), 0 at night (value = 0)."
    },
    "t_lb_tpqw": {
      "type": "unknown",
      "units": "s",
      "description": "TPQW LB time."
    },
    "flb_tpqw": {
      "type": "unknown",
      "units": "1",
      "description": "Linear factor on the TPQW LB record: (t_UB - t)/(t_UB - t_LB) (shr_tInterp_getFactors 'linear')."
    },
    "fub_tpqw": {
      "type": "unknown",
      "units": "1",
      "description": "Linear factor on the TPQW UB record: 1 - flb."
    },
    "t_lb_precip": {
      "type": "unknown",
      "units": "s",
      "description": "Precip LB time."
    },
    "flb_precip": {
      "type": "unknown",
      "units": "1",
      "description": "Nearest factor on the Precip LB record: 1 when |t_LB - t| <= |t_UB - t| else 0 (shr_tInterp_getFactors 'nearest'; ties go to LB)."
    },
    "fub_precip": {
      "type": "unknown",
      "units": "1",
      "description": "Nearest factor on the Precip UB record: 1 - flb."
    },
    "swdn": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Interpolated stream value of swdn on the model grid (fldbun_model), consumed by the datamode as strm_swdn."
    },
    "precn": {
      "type": "unknown",
      "units": "kg/m^2/s",
      "description": "Interpolated stream value of precn on the model grid (fldbun_model), consumed by the datamode as strm_precn."
    },
    "tbot": {
      "type": "unknown",
      "units": "K",
      "description": "Interpolated stream value of tbot on the model grid (fldbun_model), consumed by the datamode as strm_tbot."
    },
    "pbot": {
      "type": "unknown",
      "units": "Pa",
      "description": "Interpolated stream value of pbot on the model grid (fldbun_model), consumed by the datamode as strm_pbot."
    },
    "wind": {
      "type": "unknown",
      "units": "m/s",
      "description": "Interpolated stream value of wind on the model grid (fldbun_model), consumed by the datamode as strm_wind."
    },
    "shum": {
      "type": "unknown",
      "units": "kg/kg",
      "description": "Interpolated stream value of shum on the model grid (fldbun_model), consumed by the datamode as strm_shum."
    },
    "lwdn": {
      "type": "unknown",
      "units": "W/m^2",
      "description": "Interpolated stream value of lwdn on the model grid (fldbun_model), consumed by the datamode as strm_lwdn."
    },
    "topo": {
      "type": "unknown",
      "units": "m",
      "description": "Interpolated stream value of topo on the model grid (fldbun_model), consumed by the datamode as strm_topo."
    }
  },
  "equations": [
    {
      "lhs": "calday",
      "rhs": {
        "op": "+",
        "args": [
          "calday0",
          {
            "op": "/",
            "args": [
              "t",
              {
                "op": "const",
                "args": [],
                "value": 86400.0,
                "units": "s"
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "t_lb_solar",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "record_lower_time",
        "bindings": {
          "t": "t",
          "t0": "t0_solar",
          "dt": "dt_rec"
        }
      }
    },
    {
      "lhs": "calday_lb",
      "rhs": {
        "op": "+",
        "args": [
          "calday0",
          {
            "op": "/",
            "args": [
              "t_lb_solar",
              {
                "op": "const",
                "args": [],
                "value": 86400.0,
                "units": "s"
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "cosz",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "orb_cosz",
        "bindings": {
          "calday": "calday",
          "lat": "lat",
          "lon": "lon",
          "eccen": "eccen",
          "obliqr": "obliqr",
          "lambm0": "lambm0",
          "mvelpp": "mvelpp"
        }
      }
    },
    {
      "lhs": "tavcosz",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "+",
            "args": [
              {
                "op": "+",
                "args": [
                  {
                    "op": "+",
                    "args": [
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
                                    "op": "apply_expression_template",
                                    "args": [],
                                    "name": "orb_cosz",
                                    "bindings": {
                                      "calday": {
                                        "op": "+",
                                        "args": [
                                          "calday0",
                                          {
                                            "op": "/",
                                            "args": [
                                              {
                                                "op": "+",
                                                "args": [
                                                  "t_lb_solar",
                                                  {
                                                    "op": "*",
                                                    "args": [
                                                      {
                                                        "op": "const",
                                                        "args": [],
                                                        "value": 0.0,
                                                        "units": "1"
                                                      },
                                                      "modeldt"
                                                    ]
                                                  }
                                                ]
                                              },
                                              {
                                                "op": "const",
                                                "args": [],
                                                "value": 86400.0,
                                                "units": "s"
                                              }
                                            ]
                                          }
                                        ]
                                      },
                                      "lat": "lat",
                                      "lon": "lon",
                                      "eccen": "eccen",
                                      "obliqr": "obliqr",
                                      "lambm0": "lambm0",
                                      "mvelpp": "mvelpp"
                                    }
                                  },
                                  "modeldt"
                                ]
                              },
                              {
                                "op": "*",
                                "args": [
                                  {
                                    "op": "apply_expression_template",
                                    "args": [],
                                    "name": "orb_cosz",
                                    "bindings": {
                                      "calday": {
                                        "op": "+",
                                        "args": [
                                          "calday0",
                                          {
                                            "op": "/",
                                            "args": [
                                              {
                                                "op": "+",
                                                "args": [
                                                  "t_lb_solar",
                                                  {
                                                    "op": "*",
                                                    "args": [
                                                      {
                                                        "op": "const",
                                                        "args": [],
                                                        "value": 1.0,
                                                        "units": "1"
                                                      },
                                                      "modeldt"
                                                    ]
                                                  }
                                                ]
                                              },
                                              {
                                                "op": "const",
                                                "args": [],
                                                "value": 86400.0,
                                                "units": "s"
                                              }
                                            ]
                                          }
                                        ]
                                      },
                                      "lat": "lat",
                                      "lon": "lon",
                                      "eccen": "eccen",
                                      "obliqr": "obliqr",
                                      "lambm0": "lambm0",
                                      "mvelpp": "mvelpp"
                                    }
                                  },
                                  "modeldt"
                                ]
                              }
                            ]
                          },
                          {
                            "op": "*",
                            "args": [
                              {
                                "op": "apply_expression_template",
                                "args": [],
                                "name": "orb_cosz",
                                "bindings": {
                                  "calday": {
                                    "op": "+",
                                    "args": [
                                      "calday0",
                                      {
                                        "op": "/",
                                        "args": [
                                          {
                                            "op": "+",
                                            "args": [
                                              "t_lb_solar",
                                              {
                                                "op": "*",
                                                "args": [
                                                  {
                                                    "op": "const",
                                                    "args": [],
                                                    "value": 2.0,
                                                    "units": "1"
                                                  },
                                                  "modeldt"
                                                ]
                                              }
                                            ]
                                          },
                                          {
                                            "op": "const",
                                            "args": [],
                                            "value": 86400.0,
                                            "units": "s"
                                          }
                                        ]
                                      }
                                    ]
                                  },
                                  "lat": "lat",
                                  "lon": "lon",
                                  "eccen": "eccen",
                                  "obliqr": "obliqr",
                                  "lambm0": "lambm0",
                                  "mvelpp": "mvelpp"
                                }
                              },
                              "modeldt"
                            ]
                          }
                        ]
                      },
                      {
                        "op": "*",
                        "args": [
                          {
                            "op": "apply_expression_template",
                            "args": [],
                            "name": "orb_cosz",
                            "bindings": {
                              "calday": {
                                "op": "+",
                                "args": [
                                  "calday0",
                                  {
                                    "op": "/",
                                    "args": [
                                      {
                                        "op": "+",
                                        "args": [
                                          "t_lb_solar",
                                          {
                                            "op": "*",
                                            "args": [
                                              {
                                                "op": "const",
                                                "args": [],
                                                "value": 3.0,
                                                "units": "1"
                                              },
                                              "modeldt"
                                            ]
                                          }
                                        ]
                                      },
                                      {
                                        "op": "const",
                                        "args": [],
                                        "value": 86400.0,
                                        "units": "s"
                                      }
                                    ]
                                  }
                                ]
                              },
                              "lat": "lat",
                              "lon": "lon",
                              "eccen": "eccen",
                              "obliqr": "obliqr",
                              "lambm0": "lambm0",
                              "mvelpp": "mvelpp"
                            }
                          },
                          "modeldt"
                        ]
                      }
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      {
                        "op": "apply_expression_template",
                        "args": [],
                        "name": "orb_cosz",
                        "bindings": {
                          "calday": {
                            "op": "+",
                            "args": [
                              "calday0",
                              {
                                "op": "/",
                                "args": [
                                  {
                                    "op": "+",
                                    "args": [
                                      "t_lb_solar",
                                      {
                                        "op": "*",
                                        "args": [
                                          {
                                            "op": "const",
                                            "args": [],
                                            "value": 4.0,
                                            "units": "1"
                                          },
                                          "modeldt"
                                        ]
                                      }
                                    ]
                                  },
                                  {
                                    "op": "const",
                                    "args": [],
                                    "value": 86400.0,
                                    "units": "s"
                                  }
                                ]
                              }
                            ]
                          },
                          "lat": "lat",
                          "lon": "lon",
                          "eccen": "eccen",
                          "obliqr": "obliqr",
                          "lambm0": "lambm0",
                          "mvelpp": "mvelpp"
                        }
                      },
                      "modeldt"
                    ]
                  }
                ]
              },
              {
                "op": "*",
                "args": [
                  {
                    "op": "apply_expression_template",
                    "args": [],
                    "name": "orb_cosz",
                    "bindings": {
                      "calday": {
                        "op": "+",
                        "args": [
                          "calday0",
                          {
                            "op": "/",
                            "args": [
                              {
                                "op": "+",
                                "args": [
                                  "t_lb_solar",
                                  {
                                    "op": "*",
                                    "args": [
                                      {
                                        "op": "const",
                                        "args": [],
                                        "value": 5.0,
                                        "units": "1"
                                      },
                                      "modeldt"
                                    ]
                                  }
                                ]
                              },
                              {
                                "op": "const",
                                "args": [],
                                "value": 86400.0,
                                "units": "s"
                              }
                            ]
                          }
                        ]
                      },
                      "lat": "lat",
                      "lon": "lon",
                      "eccen": "eccen",
                      "obliqr": "obliqr",
                      "lambm0": "lambm0",
                      "mvelpp": "mvelpp"
                    }
                  },
                  "modeldt"
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "const",
                "args": [],
                "value": 6.0,
                "units": "1"
              },
              "modeldt"
            ]
          }
        ]
      }
    },
    {
      "lhs": "flb_solar",
      "rhs": {
        "op": "/",
        "args": [
          "cosz",
          "tavcosz"
        ]
      }
    },
    {
      "lhs": "day",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": ">",
            "args": [
              "cosz",
              {
                "op": "const",
                "args": [],
                "value": 0.001,
                "units": "1"
              }
            ]
          },
          {
            "op": "const",
            "args": [],
            "value": 1.0,
            "units": "1"
          },
          {
            "op": "const",
            "args": [],
            "value": 0.0,
            "units": "1"
          }
        ]
      }
    },
    {
      "lhs": "swdn",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": ">",
            "args": [
              "cosz",
              {
                "op": "const",
                "args": [],
                "value": 0.001,
                "units": "1"
              }
            ]
          },
          {
            "op": "/",
            "args": [
              {
                "op": "*",
                "args": [
                  {
                    "op": "index",
                    "args": [
                      "swdn_rec",
                      1
                    ]
                  },
                  "cosz"
                ]
              },
              "tavcosz"
            ]
          },
          {
            "op": "const",
            "args": [],
            "value": 0.0,
            "units": "W/m^2"
          }
        ]
      }
    },
    {
      "lhs": "t_lb_tpqw",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "record_lower_time",
        "bindings": {
          "t": "t",
          "t0": "t0_tpqw",
          "dt": "dt_rec"
        }
      }
    },
    {
      "lhs": "flb_tpqw",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "-",
            "args": [
              {
                "op": "+",
                "args": [
                  "t_lb_tpqw",
                  "dt_rec"
                ]
              },
              "t"
            ]
          },
          "dt_rec"
        ]
      }
    },
    {
      "lhs": "fub_tpqw",
      "rhs": {
        "op": "-",
        "args": [
          {
            "op": "const",
            "args": [],
            "value": 1.0,
            "units": "1"
          },
          "flb_tpqw"
        ]
      }
    },
    {
      "lhs": "t_lb_precip",
      "rhs": {
        "op": "apply_expression_template",
        "args": [],
        "name": "record_lower_time",
        "bindings": {
          "t": "t",
          "t0": "t0_precip",
          "dt": "dt_rec"
        }
      }
    },
    {
      "lhs": "flb_precip",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "<=",
            "args": [
              {
                "op": "abs",
                "args": [
                  {
                    "op": "-",
                    "args": [
                      "t_lb_precip",
                      "t"
                    ]
                  }
                ]
              },
              {
                "op": "abs",
                "args": [
                  {
                    "op": "-",
                    "args": [
                      {
                        "op": "+",
                        "args": [
                          "t_lb_precip",
                          "dt_rec"
                        ]
                      },
                      "t"
                    ]
                  }
                ]
              }
            ]
          },
          {
            "op": "const",
            "args": [],
            "value": 1.0,
            "units": "1"
          },
          {
            "op": "const",
            "args": [],
            "value": 0.0,
            "units": "1"
          }
        ]
      }
    },
    {
      "lhs": "fub_precip",
      "rhs": {
        "op": "-",
        "args": [
          {
            "op": "const",
            "args": [],
            "value": 1.0,
            "units": "1"
          },
          "flb_precip"
        ]
      }
    },
    {
      "lhs": "precn",
      "rhs": {
        "op": "+",
        "args": [
          {
            "op": "*",
            "args": [
              {
                "op": "index",
                "args": [
                  "precn_rec",
                  1
                ]
              },
              "flb_precip"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "index",
                "args": [
                  "precn_rec",
                  2
                ]
              },
              "fub_precip"
            ]
          }
        ]
      }
    },
    {
      "lhs": "tbot",
      "rhs": {
        "op": "+",
        "args": [
          {
            "op": "*",
            "args": [
              {
                "op": "index",
                "args": [
                  "tbot_rec",
                  1
                ]
              },
              "flb_tpqw"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "index",
                "args": [
                  "tbot_rec",
                  2
                ]
              },
              "fub_tpqw"
            ]
          }
        ]
      }
    },
    {
      "lhs": "pbot",
      "rhs": {
        "op": "+",
        "args": [
          {
            "op": "*",
            "args": [
              {
                "op": "index",
                "args": [
                  "pbot_rec",
                  1
                ]
              },
              "flb_tpqw"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "index",
                "args": [
                  "pbot_rec",
                  2
                ]
              },
              "fub_tpqw"
            ]
          }
        ]
      }
    },
    {
      "lhs": "wind",
      "rhs": {
        "op": "+",
        "args": [
          {
            "op": "*",
            "args": [
              {
                "op": "index",
                "args": [
                  "wind_rec",
                  1
                ]
              },
              "flb_tpqw"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "index",
                "args": [
                  "wind_rec",
                  2
                ]
              },
              "fub_tpqw"
            ]
          }
        ]
      }
    },
    {
      "lhs": "shum",
      "rhs": {
        "op": "+",
        "args": [
          {
            "op": "*",
            "args": [
              {
                "op": "index",
                "args": [
                  "shum_rec",
                  1
                ]
              },
              "flb_tpqw"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "index",
                "args": [
                  "shum_rec",
                  2
                ]
              },
              "fub_tpqw"
            ]
          }
        ]
      }
    },
    {
      "lhs": "lwdn",
      "rhs": {
        "op": "+",
        "args": [
          {
            "op": "*",
            "args": [
              {
                "op": "index",
                "args": [
                  "lwdn_rec",
                  1
                ]
              },
              "flb_tpqw"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "index",
                "args": [
                  "lwdn_rec",
                  2
                ]
              },
              "fub_tpqw"
            ]
          }
        ]
      }
    },
    {
      "lhs": "topo",
      "rhs": "topo_in"
    }
  ],
  "tests": [
    {
      "id": "dump_step0_p1",
      "description": "Traced row step 0 (2000-01-01 tod 0 s) point 1 (lat -90, lon 0) of cdeps_strdata_streams.csv: the record pairs [lb, ub] of every GSWP3 stream field go in; the factors are computed from t and the orbit, not supplied, and the factors and interpolated values must equal the dumped flb/fub/value columns (coszen Solar, nearest Precip, linear TPQW, lower topo).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 1e-15
      },
      "parameter_overrides": {
        "lat": -90.0,
        "lon": 0.0,
        "swdn_rec": [
          429.9039257897292,
          438.02563417222825
        ],
        "precn_rec": [
          5.22216069182629e-06,
          7.058281049252279e-06
        ],
        "tbot_rec": [
          249.1546637852978,
          249.46382249196316
        ],
        "pbot_rec": [
          68139.58841145803,
          68128.68378906311
        ],
        "wind_rec": [
          7.986586749553681,
          1.7775791878501583
        ],
        "shum_rec": [
          0.0007427445054215958,
          0.0007682375166041304
        ],
        "lwdn_rec": [
          146.63188468085335,
          148.67196606530084
        ],
        "topo_in": 2824.921026576389
      },
      "assertions": [
        {
          "variable": "swdn",
          "time": 0.0,
          "expected": 429.97176732088275
        },
        {
          "variable": "precn",
          "time": 0.0,
          "expected": 5.22216069182629e-06
        },
        {
          "variable": "tbot",
          "time": 0.0,
          "expected": 249.30924313863048
        },
        {
          "variable": "pbot",
          "time": 0.0,
          "expected": 68134.13610026057
        },
        {
          "variable": "wind",
          "time": 0.0,
          "expected": 4.88208296870192
        },
        {
          "variable": "shum",
          "time": 0.0,
          "expected": 0.0007554910110128631
        },
        {
          "variable": "lwdn",
          "time": 0.0,
          "expected": 147.6519253730771
        },
        {
          "variable": "topo",
          "time": 0.0,
          "expected": 2824.921026576389
        },
        {
          "variable": "flb_solar",
          "time": 0.0,
          "expected": 1.0001578062610825
        },
        {
          "variable": "flb_tpqw",
          "time": 0.0,
          "expected": 0.5
        },
        {
          "variable": "fub_tpqw",
          "time": 0.0,
          "expected": 0.5
        },
        {
          "variable": "flb_precip",
          "time": 0.0,
          "expected": 1.0
        },
        {
          "variable": "fub_precip",
          "time": 0.0,
          "expected": 0.0
        }
      ]
    },
    {
      "id": "dump_step1_p1",
      "description": "Traced row step 1 (2000-01-01 tod 1800 s) point 1 (lat -90, lon 0) of cdeps_strdata_streams.csv: the record pairs [lb, ub] of every GSWP3 stream field go in; the factors are computed from t and the orbit, not supplied, and the factors and interpolated values must equal the dumped flb/fub/value columns (coszen Solar, nearest Precip, linear TPQW, lower topo).",
      "time_span": {
        "start": 1800.0,
        "end": 1800.0
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 1e-15
      },
      "parameter_overrides": {
        "lat": -90.0,
        "lon": 0.0,
        "swdn_rec": [
          429.9039257897292,
          438.02563417222825
        ],
        "precn_rec": [
          5.22216069182629e-06,
          7.058281049252279e-06
        ],
        "tbot_rec": [
          249.1546637852978,
          249.46382249196316
        ],
        "pbot_rec": [
          68139.58841145803,
          68128.68378906311
        ],
        "wind_rec": [
          7.986586749553681,
          1.7775791878501583
        ],
        "shum_rec": [
          0.0007427445054215958,
          0.0007682375166041304
        ],
        "lwdn_rec": [
          146.63188468085335,
          148.67196606530084
        ],
        "topo_in": 2824.921026576389
      },
      "assertions": [
        {
          "variable": "swdn",
          "time": 1800.0,
          "expected": 429.9447095680577
        },
        {
          "variable": "precn",
          "time": 1800.0,
          "expected": 7.058281049252279e-06
        },
        {
          "variable": "tbot",
          "time": 1800.0,
          "expected": 249.36076958974138
        },
        {
          "variable": "pbot",
          "time": 1800.0,
          "expected": 68132.31866319476
        },
        {
          "variable": "wind",
          "time": 1800.0,
          "expected": 3.847248375084666
        },
        {
          "variable": "shum",
          "time": 1800.0,
          "expected": 0.0007597398462099523
        },
        {
          "variable": "lwdn",
          "time": 1800.0,
          "expected": 147.99193893715167
        },
        {
          "variable": "topo",
          "time": 1800.0,
          "expected": 2824.921026576389
        },
        {
          "variable": "flb_solar",
          "time": 1800.0,
          "expected": 1.0000948671921375
        },
        {
          "variable": "flb_tpqw",
          "time": 1800.0,
          "expected": 0.3333333333333333
        },
        {
          "variable": "fub_tpqw",
          "time": 1800.0,
          "expected": 0.6666666666666667
        },
        {
          "variable": "flb_precip",
          "time": 1800.0,
          "expected": 0.0
        },
        {
          "variable": "fub_precip",
          "time": 1800.0,
          "expected": 1.0
        }
      ]
    },
    {
      "id": "dump_step2_p1",
      "description": "Traced row step 2 (2000-01-01 tod 3600 s) point 1 (lat -90, lon 0) of cdeps_strdata_streams.csv: the record pairs [lb, ub] of every GSWP3 stream field go in; the factors are computed from t and the orbit, not supplied, and the factors and interpolated values must equal the dumped flb/fub/value columns (coszen Solar, nearest Precip, linear TPQW, lower topo).",
      "time_span": {
        "start": 3600.0,
        "end": 3600.0
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 1e-15
      },
      "parameter_overrides": {
        "lat": -90.0,
        "lon": 0.0,
        "swdn_rec": [
          429.9039257897292,
          438.02563417222825
        ],
        "precn_rec": [
          5.22216069182629e-06,
          7.058281049252279e-06
        ],
        "tbot_rec": [
          249.1546637852978,
          249.46382249196316
        ],
        "pbot_rec": [
          68139.58841145803,
          68128.68378906311
        ],
        "wind_rec": [
          7.986586749553681,
          1.7775791878501583
        ],
        "shum_rec": [
          0.0007427445054215958,
          0.0007682375166041304
        ],
        "lwdn_rec": [
          146.63188468085335,
          148.67196606530084
        ],
        "topo_in": 2824.921026576389
      },
      "assertions": [
        {
          "variable": "swdn",
          "time": 3600.0,
          "expected": 429.91759266770555
        },
        {
          "variable": "precn",
          "time": 3600.0,
          "expected": 7.058281049252279e-06
        },
        {
          "variable": "tbot",
          "time": 3600.0,
          "expected": 249.41229604085228
        },
        {
          "variable": "pbot",
          "time": 3600.0,
          "expected": 68130.50122612894
        },
        {
          "variable": "wind",
          "time": 3600.0,
          "expected": 2.812413781467412
        },
        {
          "variable": "shum",
          "time": 3600.0,
          "expected": 0.0007639886814070413
        },
        {
          "variable": "lwdn",
          "time": 3600.0,
          "expected": 148.33195250122625
        },
        {
          "variable": "topo",
          "time": 3600.0,
          "expected": 2824.921026576389
        },
        {
          "variable": "flb_solar",
          "time": 3600.0,
          "expected": 1.0000317905400637
        },
        {
          "variable": "flb_tpqw",
          "time": 3600.0,
          "expected": 0.16666666666666666
        },
        {
          "variable": "fub_tpqw",
          "time": 3600.0,
          "expected": 0.8333333333333334
        },
        {
          "variable": "flb_precip",
          "time": 3600.0,
          "expected": 0.0
        },
        {
          "variable": "fub_precip",
          "time": 3600.0,
          "expected": 1.0
        }
      ]
    },
    {
      "id": "dump_step3_p1",
      "description": "Traced row step 3 (2000-01-01 tod 5400 s) point 1 (lat -90, lon 0) of cdeps_strdata_streams.csv: the record pairs [lb, ub] of every GSWP3 stream field go in; the factors are computed from t and the orbit, not supplied, and the factors and interpolated values must equal the dumped flb/fub/value columns (coszen Solar, nearest Precip, linear TPQW, lower topo).",
      "time_span": {
        "start": 5400.0,
        "end": 5400.0
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 1e-15
      },
      "parameter_overrides": {
        "lat": -90.0,
        "lon": 0.0,
        "swdn_rec": [
          429.9039257897292,
          438.02563417222825
        ],
        "precn_rec": [
          7.058281049252279e-06,
          5.524998584307837e-06
        ],
        "tbot_rec": [
          249.46382249196316,
          249.49590365091888
        ],
        "pbot_rec": [
          68128.68378906311,
          68125.48240017409
        ],
        "wind_rec": [
          1.7775791878501583,
          1.7775791878501583
        ],
        "shum_rec": [
          0.0007682375166041304,
          0.0007593141400624021
        ],
        "lwdn_rec": [
          148.67196606530084,
          145.6960742102741
        ],
        "topo_in": 2824.921026576389
      },
      "assertions": [
        {
          "variable": "swdn",
          "time": 5400.0,
          "expected": 429.89041662355584
        },
        {
          "variable": "precn",
          "time": 5400.0,
          "expected": 7.058281049252279e-06
        },
        {
          "variable": "tbot",
          "time": 5400.0,
          "expected": 249.46382249196316
        },
        {
          "variable": "pbot",
          "time": 5400.0,
          "expected": 68128.68378906311
        },
        {
          "variable": "wind",
          "time": 5400.0,
          "expected": 1.7775791878501583
        },
        {
          "variable": "shum",
          "time": 5400.0,
          "expected": 0.0007682375166041304
        },
        {
          "variable": "lwdn",
          "time": 5400.0,
          "expected": 148.67196606530084
        },
        {
          "variable": "topo",
          "time": 5400.0,
          "expected": 2824.921026576389
        },
        {
          "variable": "flb_solar",
          "time": 5400.0,
          "expected": 0.9999685763135366
        },
        {
          "variable": "flb_tpqw",
          "time": 5400.0,
          "expected": 1.0
        },
        {
          "variable": "fub_tpqw",
          "time": 5400.0,
          "expected": 0.0
        },
        {
          "variable": "flb_precip",
          "time": 5400.0,
          "expected": 1.0
        },
        {
          "variable": "fub_precip",
          "time": 5400.0,
          "expected": 0.0
        }
      ]
    },
    {
      "id": "dump_step5_p1",
      "description": "Traced row step 5 (2000-01-01 tod 9000 s) point 1 (lat -90, lon 0) of cdeps_strdata_streams.csv: the record pairs [lb, ub] of every GSWP3 stream field go in; the factors are computed from t and the orbit, not supplied, and the factors and interpolated values must equal the dumped flb/fub/value columns (coszen Solar, nearest Precip, linear TPQW, lower topo).",
      "time_span": {
        "start": 9000.0,
        "end": 9000.0
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 1e-15
      },
      "parameter_overrides": {
        "lat": -90.0,
        "lon": 0.0,
        "swdn_rec": [
          429.9039257897292,
          438.02563417222825
        ],
        "precn_rec": [
          7.058281049252279e-06,
          5.524998584307837e-06
        ],
        "tbot_rec": [
          249.46382249196316,
          249.49590365091888
        ],
        "pbot_rec": [
          68128.68378906311,
          68125.48240017409
        ],
        "wind_rec": [
          1.7775791878501583,
          1.7775791878501583
        ],
        "shum_rec": [
          0.0007682375166041304,
          0.0007593141400624021
        ],
        "lwdn_rec": [
          148.67196606530084,
          145.6960742102741
        ],
        "topo_in": 2824.921026576389
      },
      "assertions": [
        {
          "variable": "swdn",
          "time": 9000.0,
          "expected": 429.83588711882646
        },
        {
          "variable": "precn",
          "time": 9000.0,
          "expected": 7.058281049252279e-06
        },
        {
          "variable": "tbot",
          "time": 9000.0,
          "expected": 249.47451621161508
        },
        {
          "variable": "pbot",
          "time": 9000.0,
          "expected": 68127.61665943344
        },
        {
          "variable": "wind",
          "time": 9000.0,
          "expected": 1.7775791878501583
        },
        {
          "variable": "shum",
          "time": 9000.0,
          "expected": 0.0007652630577568876
        },
        {
          "variable": "lwdn",
          "time": 9000.0,
          "expected": 147.68000211362525
        },
        {
          "variable": "topo",
          "time": 9000.0,
          "expected": 2824.921026576389
        },
        {
          "variable": "flb_solar",
          "time": 9000.0,
          "expected": 0.9998417351719275
        },
        {
          "variable": "flb_tpqw",
          "time": 9000.0,
          "expected": 0.6666666666666666
        },
        {
          "variable": "fub_tpqw",
          "time": 9000.0,
          "expected": 0.33333333333333337
        },
        {
          "variable": "flb_precip",
          "time": 9000.0,
          "expected": 1.0
        },
        {
          "variable": "fub_precip",
          "time": 9000.0,
          "expected": 0.0
        }
      ]
    },
    {
      "id": "dump_step6_p1",
      "description": "Traced row step 6 (2000-01-01 tod 10800 s) point 1 (lat -90, lon 0) of cdeps_strdata_streams.csv: the record pairs [lb, ub] of every GSWP3 stream field go in; the factors are computed from t and the orbit, not supplied, and the factors and interpolated values must equal the dumped flb/fub/value columns (coszen Solar, nearest Precip, linear TPQW, lower topo).",
      "time_span": {
        "start": 10800.0,
        "end": 10800.0
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 1e-15
      },
      "parameter_overrides": {
        "lat": -90.0,
        "lon": 0.0,
        "swdn_rec": [
          438.02563417222825,
          435.1825587802471
        ],
        "precn_rec": [
          7.058281049252279e-06,
          5.524998584307837e-06
        ],
        "tbot_rec": [
          249.46382249196316,
          249.49590365091888
        ],
        "pbot_rec": [
          68128.68378906311,
          68125.48240017409
        ],
        "wind_rec": [
          1.7775791878501583,
          1.7775791878501583
        ],
        "shum_rec": [
          0.0007682375166041304,
          0.0007593141400624021
        ],
        "lwdn_rec": [
          148.67196606530084,
          145.6960742102741
        ],
        "topo_in": 2824.921026576389
      },
      "assertions": [
        {
          "variable": "swdn",
          "time": 10800.0,
          "expected": 438.09568785808557
        },
        {
          "variable": "precn",
          "time": 10800.0,
          "expected": 7.058281049252279e-06
        },
        {
          "variable": "tbot",
          "time": 10800.0,
          "expected": 249.479863071441
        },
        {
          "variable": "pbot",
          "time": 10800.0,
          "expected": 68127.0830946186
        },
        {
          "variable": "wind",
          "time": 10800.0,
          "expected": 1.7775791878501583
        },
        {
          "variable": "shum",
          "time": 10800.0,
          "expected": 0.0007637758283332663
        },
        {
          "variable": "lwdn",
          "time": 10800.0,
          "expected": 147.18402013778746
        },
        {
          "variable": "topo",
          "time": 10800.0,
          "expected": 2824.921026576389
        },
        {
          "variable": "flb_solar",
          "time": 10800.0,
          "expected": 1.0001599305620315
        },
        {
          "variable": "flb_tpqw",
          "time": 10800.0,
          "expected": 0.5
        },
        {
          "variable": "fub_tpqw",
          "time": 10800.0,
          "expected": 0.5
        },
        {
          "variable": "flb_precip",
          "time": 10800.0,
          "expected": 1.0
        },
        {
          "variable": "fub_precip",
          "time": 10800.0,
          "expected": 0.0
        }
      ]
    },
    {
      "id": "dump_step11_p1",
      "description": "Traced row step 11 (2000-01-01 tod 19800 s) point 1 (lat -90, lon 0) of cdeps_strdata_streams.csv: the record pairs [lb, ub] of every GSWP3 stream field go in; the factors are computed from t and the orbit, not supplied, and the factors and interpolated values must equal the dumped flb/fub/value columns (coszen Solar, nearest Precip, linear TPQW, lower topo).",
      "time_span": {
        "start": 19800.0,
        "end": 19800.0
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 1e-15
      },
      "parameter_overrides": {
        "lat": -90.0,
        "lon": 0.0,
        "swdn_rec": [
          438.02563417222825,
          435.1825587802471
        ],
        "precn_rec": [
          5.524998584307837e-06,
          6.574792198548606e-06
        ],
        "tbot_rec": [
          249.49590365091888,
          249.09363769955428
        ],
        "pbot_rec": [
          68125.48240017409,
          68123.28173828071
        ],
        "wind_rec": [
          1.7775791878501583,
          1.8143393902315041
        ],
        "shum_rec": [
          0.0007593141400624021,
          0.000745919910211041
        ],
        "lwdn_rec": [
          145.6960742102741,
          145.97946762508832
        ],
        "topo_in": 2824.921026576389
      },
      "assertions": [
        {
          "variable": "swdn",
          "time": 19800.0,
          "expected": 437.95537962233925
        },
        {
          "variable": "precn",
          "time": 19800.0,
          "expected": 5.524998584307837e-06
        },
        {
          "variable": "tbot",
          "time": 19800.0,
          "expected": 249.361815000464
        },
        {
          "variable": "pbot",
          "time": 19800.0,
          "expected": 68124.74884620964
        },
        {
          "variable": "wind",
          "time": 19800.0,
          "expected": 1.7898325886439403
        },
        {
          "variable": "shum",
          "time": 19800.0,
          "expected": 0.0007548493967786151
        },
        {
          "variable": "lwdn",
          "time": 19800.0,
          "expected": 145.79053868187884
        },
        {
          "variable": "topo",
          "time": 19800.0,
          "expected": 2824.921026576389
        },
        {
          "variable": "flb_solar",
          "time": 19800.0,
          "expected": 0.9998396108711267
        },
        {
          "variable": "flb_tpqw",
          "time": 19800.0,
          "expected": 0.6666666666666666
        },
        {
          "variable": "fub_tpqw",
          "time": 19800.0,
          "expected": 0.33333333333333337
        },
        {
          "variable": "flb_precip",
          "time": 19800.0,
          "expected": 1.0
        },
        {
          "variable": "fub_precip",
          "time": 19800.0,
          "expected": 0.0
        }
      ]
    },
    {
      "id": "dump_step0_p16",
      "description": "Traced row step 0 (2000-01-01 tod 0 s) point 16 (lat -90, lon 37.5) of cdeps_strdata_streams.csv: the record pairs [lb, ub] of every GSWP3 stream field go in; the factors are computed from t and the orbit, not supplied, and the factors and interpolated values must equal the dumped flb/fub/value columns (coszen Solar, nearest Precip, linear TPQW, lower topo).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 1e-15
      },
      "parameter_overrides": {
        "lat": -90.0,
        "lon": 37.5,
        "swdn_rec": [
          429.9039257897292,
          438.02563417222825
        ],
        "precn_rec": [
          5.22216069182629e-06,
          7.058281049252279e-06
        ],
        "tbot_rec": [
          249.1546637852978,
          249.46382249196316
        ],
        "pbot_rec": [
          68139.58841145803,
          68128.68378906311
        ],
        "wind_rec": [
          7.986586749553681,
          1.7775791878501583
        ],
        "shum_rec": [
          0.0007427445054215958,
          0.0007682375166041304
        ],
        "lwdn_rec": [
          146.63188468085335,
          148.67196606530084
        ],
        "topo_in": 2824.921026576389
      },
      "assertions": [
        {
          "variable": "swdn",
          "time": 0.0,
          "expected": 429.9717673208827
        },
        {
          "variable": "precn",
          "time": 0.0,
          "expected": 5.22216069182629e-06
        },
        {
          "variable": "tbot",
          "time": 0.0,
          "expected": 249.30924313863048
        },
        {
          "variable": "pbot",
          "time": 0.0,
          "expected": 68134.13610026057
        },
        {
          "variable": "wind",
          "time": 0.0,
          "expected": 4.88208296870192
        },
        {
          "variable": "shum",
          "time": 0.0,
          "expected": 0.0007554910110128631
        },
        {
          "variable": "lwdn",
          "time": 0.0,
          "expected": 147.6519253730771
        },
        {
          "variable": "topo",
          "time": 0.0,
          "expected": 2824.921026576389
        },
        {
          "variable": "flb_solar",
          "time": 0.0,
          "expected": 1.0001578062610823
        },
        {
          "variable": "flb_tpqw",
          "time": 0.0,
          "expected": 0.5
        },
        {
          "variable": "fub_tpqw",
          "time": 0.0,
          "expected": 0.5
        },
        {
          "variable": "flb_precip",
          "time": 0.0,
          "expected": 1.0
        },
        {
          "variable": "fub_precip",
          "time": 0.0,
          "expected": 0.0
        }
      ]
    },
    {
      "id": "dump_step11_p16",
      "description": "Traced row step 11 (2000-01-01 tod 19800 s) point 16 (lat -90, lon 37.5) of cdeps_strdata_streams.csv: the record pairs [lb, ub] of every GSWP3 stream field go in; the factors are computed from t and the orbit, not supplied, and the factors and interpolated values must equal the dumped flb/fub/value columns (coszen Solar, nearest Precip, linear TPQW, lower topo).",
      "time_span": {
        "start": 19800.0,
        "end": 19800.0
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 1e-15
      },
      "parameter_overrides": {
        "lat": -90.0,
        "lon": 37.5,
        "swdn_rec": [
          438.02563417222825,
          435.1825587802471
        ],
        "precn_rec": [
          5.524998584307837e-06,
          6.574792198548606e-06
        ],
        "tbot_rec": [
          249.49590365091888,
          249.09363769955428
        ],
        "pbot_rec": [
          68125.48240017409,
          68123.28173828071
        ],
        "wind_rec": [
          1.7775791878501583,
          1.8143393902315041
        ],
        "shum_rec": [
          0.0007593141400624021,
          0.000745919910211041
        ],
        "lwdn_rec": [
          145.6960742102741,
          145.97946762508832
        ],
        "topo_in": 2824.921026576389
      },
      "assertions": [
        {
          "variable": "swdn",
          "time": 19800.0,
          "expected": 437.9553796223393
        },
        {
          "variable": "precn",
          "time": 19800.0,
          "expected": 5.524998584307837e-06
        },
        {
          "variable": "tbot",
          "time": 19800.0,
          "expected": 249.361815000464
        },
        {
          "variable": "pbot",
          "time": 19800.0,
          "expected": 68124.74884620964
        },
        {
          "variable": "wind",
          "time": 19800.0,
          "expected": 1.7898325886439403
        },
        {
          "variable": "shum",
          "time": 19800.0,
          "expected": 0.0007548493967786151
        },
        {
          "variable": "lwdn",
          "time": 19800.0,
          "expected": 145.79053868187884
        },
        {
          "variable": "topo",
          "time": 19800.0,
          "expected": 2824.921026576389
        },
        {
          "variable": "flb_solar",
          "time": 19800.0,
          "expected": 0.9998396108711268
        },
        {
          "variable": "flb_tpqw",
          "time": 19800.0,
          "expected": 0.6666666666666666
        },
        {
          "variable": "fub_tpqw",
          "time": 19800.0,
          "expected": 0.33333333333333337
        },
        {
          "variable": "flb_precip",
          "time": 19800.0,
          "expected": 1.0
        },
        {
          "variable": "fub_precip",
          "time": 19800.0,
          "expected": 0.0
        }
      ]
    },
    {
      "id": "coszen_midlat_day",
      "description": "Closed-form recomputation (not a dump row): lat 40, lon 120 at 05:30Z on Jan 1 (local solar time ~13:30, sun up), where cosz varies strongly within the 3-hour interval; expected flb = cosz(t)/tavCosz and swdn = lb*flb from an independent Python transcription of shr_orb_decl / shr_orb_cosz / shr_tInterp_getAvgCosz (the same transcription reproduces all 192 coszen dump rows to the last bit).",
      "time_span": {
        "start": 19800.0,
        "end": 19800.0
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 1e-15
      },
      "parameter_overrides": {
        "lat": 40.0,
        "lon": 120.0,
        "swdn_rec": [
          437.5,
          400.25
        ]
      },
      "assertions": [
        {
          "variable": "cosz",
          "time": 19800.0,
          "expected": 0.3991961171206615
        },
        {
          "variable": "tavcosz",
          "time": 19800.0,
          "expected": 0.43382669031694543
        },
        {
          "variable": "day",
          "time": 19800.0,
          "expected": 1.0
        },
        {
          "variable": "swdn",
          "time": 19800.0,
          "expected": 402.576201830032
        },
        {
          "variable": "flb_solar",
          "time": 19800.0,
          "expected": 0.9201741756115017
        }
      ]
    },
    {
      "id": "coszen_sunrise_interval",
      "description": "Closed-form recomputation: lat 40, lon 120 at 22:30Z (local ~06:30, before sunrise): cosz is clipped to 0.001 so the night branch applies (swdn = 0) although the interval average tavCosz > 0.001 because the sun rises inside [21Z, 24Z).",
      "time_span": {
        "start": 81000.0,
        "end": 81000.0
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 1e-15
      },
      "parameter_overrides": {
        "lat": 40.0,
        "lon": 120.0,
        "swdn_rec": [
          437.5,
          400.25
        ]
      },
      "assertions": [
        {
          "variable": "cosz",
          "time": 81000.0,
          "expected": 0.001
        },
        {
          "variable": "tavcosz",
          "time": 81000.0,
          "expected": 0.003917700669065724
        },
        {
          "variable": "day",
          "time": 81000.0,
          "expected": 0.0
        },
        {
          "variable": "swdn",
          "time": 81000.0,
          "expected": 0.0
        }
      ]
    },
    {
      "id": "coszen_polar_night",
      "description": "Polar night (lat +90 on Jan 1): cosz = max(0.001, sin(delta)) = 0.001 at every sample, so the night branch zeroes swdn even though lb > 0 (dshr_strdata_mod.F90:1396-1397).",
      "time_span": {
        "start": 0.0,
        "end": 0.0
      },
      "tolerance": {
        "rel": 1e-12,
        "abs": 1e-15
      },
      "parameter_overrides": {
        "lat": 90.0,
        "lon": 0.0,
        "swdn_rec": [
          437.5,
          400.25
        ]
      },
      "assertions": [
        {
          "variable": "cosz",
          "time": 0.0,
          "expected": 0.001
        },
        {
          "variable": "tavcosz",
          "time": 0.0,
          "expected": 0.001
        },
        {
          "variable": "day",
          "time": 0.0,
          "expected": 0.0
        },
        {
          "variable": "swdn",
          "time": 0.0,
          "expected": 0.0
        }
      ]
    }
  ]
}
```

</details>
