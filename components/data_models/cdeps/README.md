# CDEPS DATM — GSWP3 forcing, CLMNCEP datamode

The CESM CDEPS data atmosphere (DATM) for the GSWP3v1 forcing with the
CLMNCEP datamode (cdeps1.0.112), as esm 2.0.0 files: the stream
time-interpolation layer, the CLMNCEP forcing derivations, the GSWP3 data
sources and their wiring into the laws, and a data-reading test on synthetic
files.

All model logic lives in the `.esm` files; this README is the map. Fortran
line numbers refer to the cdeps1.0.112 sources
(`datm/datm_datamode_clmncep_mod.F90` = F90 below,
`streams/dshr_strdata_mod.F90`, `streams/dshr_tinterp_mod.F90`,
`share/shr_precip_mod.F90`) and to CESM share `share/src/shr_orb_mod.F90`.

## Files

| file | content | tests |
|---|---|---|
| `cdeps_templates.esm` | expression-template library: the esat water/ice polynomials (`esat_poly_water`/`esat_poly_ice`, phase-selecting `esat`, F90:545-586), `qsat`, `vapor_pressure`, `density`, the cam3_5_55 `ratio_rvrf_nir`/`ratio_rvrf_vis` shortwave polynomials, `rain_snow_frac`, `wind_split`; the orbital geometry of the coszen interpolation (`orb_lambm`, `orb_lamb`, `orb_decl` = shr_orb_decl; `orb_cosz` = shr_tInterp_getCosz) and `record_lower_time`; constant fragments `tkfrz`, `eps`, `eps1` | (through the component) |
| `cdeps_datm_gswp3.esm` | the laws, no data access: `Streams` (stream layer) and `Clmncep` (datamode) | 207 assertions, all pass |
| `cdeps_datm_gswp3_data.esm` | the four GSWP3 `data_sources` on the public NCAR archive, the `GSWP3Files` reader model, `Streams`/`Clmncep` mounted by ref from `cdeps_datm_gswp3.esm`, and the reader → Streams → Clmncep coupling | none (would read the real archive) |
| `cdeps_datm_gswp3_synthetic.esm` | the same reader declarations, mounts and coupling edges, pointed at synthetic files | 48 assertions (see [Status](#status-of-the-data-test)) |
| `../../../tools/gen_synthetic_gswp3.py` | writes the synthetic files | — |

## Model structure

```
GSWP3v1 netCDF (data_sources; netcdf reader)
   │  GSWP3Files.FSDS, PRECTmms, TBOT, PSRF, WIND, QBOT, FLDS   shape [rec]:
   │      the record at or before t (CDEPS LB) and the next one (UB)
   │  GSWP3Files.TOPO                                            scalar (static)
   ▼  variable_map param_to_var
Streams.*_rec / topo_in
   │  factors computed from t (coszen, nearest, linear, lower)
   ▼  variable_map param_to_var
Clmncep.strm_*
   │  CLMNCEP datamode laws
   ▼
Sa_*, Faxa_*   (export state, consumed by CLM through the mediator)
```

The spatial map (in CESM, a bilinear ESMF regrid from the 0.5° source mesh
to the model mesh) is not represented: the data sources select one source
cell, and the traced dumps are post-map values used as they are.

### Streams (shr_strdata_advance + shr_tInterp)

Every 3-hourly field enters as a record pair `[LB, UB]` over the record axis
`rec` (`"records": true`, esm-spec §8.5.1). The record times and the
interpolation factors are computed from the model time `t` — nothing is
supplied:

- **record times**: `t_lb = t0 + dt_rec·floor((t − t0)/dt_rec)` (template
  `record_lower_time`); the GSWP3 Solar records sit at 00, 03, … Z
  (`t0_solar = 0`), the TPQW and Precip records at 01:30, 04:30, … Z
  (`t0_tpqw = t0_precip = 5400 s`), `dt_rec = 10800 s`.
- **coszen** (Solar FSDS): `swdn = LB·cosz/tavCosz` when `cosz > 0.001`, else
  0 (dshr_strdata_mod.F90:1396-1397), with `cosz = max(0.001, cos z)` at `t`
  (dshr_tinterp_mod.F90:313-318) from the shr_orb_decl declination with the
  year-2000 orbital parameters of the reference run (`eccen`, `obliqr`,
  `lambm0`, `mvelpp`), and `tavCosz` the `modeldt`-weighted mean of the
  clipped cosz at the sub-steps `t_lb + k·modeldt`, k = 0…5, of `[LB, UB)`
  (shr_tInterp_getAvgCosz, dshr_tinterp_mod.F90:258-272). The calendar day is
  `calday0 + t/86400 s` (`calday0 = 1` at the time origin
  2000-01-01T00:00:00Z).
- **linear** (TPQW TBOT/PSRF/WIND/QBOT/FLDS): `flb = (t_UB − t)/(t_UB − t_LB)`,
  `fub = 1 − flb`, `value = LB·flb + UB·fub`.
- **nearest** (Precip PRECTmms): `flb = 1` when `|t_LB − t| ≤ |t_UB − t|`
  (ties go to LB), else 0.
- **lower** (topo.observed TOPO): the static file's single record.

The transcription reproduces all 192 traced coszen rows of the dump to the
last bit (checked off-line in Python); the esm tests pin 9 traced (step,
point) rows to `rel = 1e-12`.

Limits: the coszen average is written with 6 samples (`dt_rec/modeldt` for
the reference case, ATM_NCPL = 48, `modeldt = 1800 s`); a different coupling
step changes `modeldt` but not the sample count. The `upper` algorithm is not
implemented (no GSWP3 stream uses it). The calendar is noleap day-of-year
counted from `calday0`, exact while a run stays inside one year.

### Clmncep (datm_datamode_clmncep_advance, F90:328-487)

tbot units detector (+273.15 when `tbotmax < 50`) and 180 K floor; pressure
zero-fill and no-stream fallback to pstd; wind split; humidity on all three
CLMNCEP paths behind `shum_source` — 1 = specific humidity capped at qsat
(the GSWP3 path: QBOT), 2 = relative humidity (F90:418-421), 3 = dew point
(F90:422-427, degC detection by `tdewmax`, esat phase from tbot); density;
longwave fallback (`lwdn_present = 0`); shortwave direct/diffuse split; swnet
(zero when anidrmax is out of range, albedo-weighted when the `Sx_*` imports
are present, plain sum otherwise); rain/snow ramp; topo/z fallbacks
(`topo_present`, strm_z spval).

**Not represented:** the bias-correction / anomaly-forcing block
(F90:489-546). It is inactive unless bias or anomaly streams are configured,
and the GSWP3 case configures none. The presaero/presndep/preso3 streams are
not part of CLMNCEP (pass-throughs with unit scales elsewhere in DATM).

## Data sources (`cdeps_datm_gswp3_data.esm`)

The sources point at the **public NCAR CESM inputdata server**
(`https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/datm7/`): the
three 3-hourly streams (Solar, Precip, TPQW) as monthly files through a
`{date:%Y-%m}` placeholder (`file_period P1M`, `frequency PT3H`,
`records_per_file "auto"`, `time_variable "time"`, 1901-01 … 2014-12), and
the static topo file. esm 2.0.0 conventions:

- `select.axes` covers only the non-time dimensions of a time-varying source:
  `[{fixed: ilat}, {fixed: ilon}]` (§8.9.2); record selection is the
  provider's. The static topo source has no `temporal` block, so its select
  names every native dimension: `["all", {fixed}, {fixed}]` (the degenerate
  time axis stays `"all"`; the netcdf reader refuses a subset of a time
  dimension).
- The 3-hourly reader parameters declare `shape: ["rec"]` and so receive the
  pair of records bracketing `t`; TOPO declares `shape: []` (one record).
  There is no `extent` and no record-count metaparameter (the former
  `N_REC`/`N_TOPO`/`record`/`record_topo` are gone).
- `temporal.start` is each stream's first record time (00:00Z for Solar,
  01:30Z for TPQW and Precip): the Rust provider places records at
  `start + k·frequency` and does not consult the file's `time` coordinate.
- The time origin is `domain.temporal.reference_time = 2000-01-01T00:00:00Z`,
  which `Streams.calday0` and `t0_*` assume.

Differences from the reference CESM run: the reference cycles 1991-2010
(`taxmode cycle`, `year_align 1991`), so model year 2000 reads the 1991
files, while a data source here reads the file of the model date itself; and
the spatial map (above).

### Licensing and citation

GSWP3v1: Kim, H. (2017). *Global Soil Wetness Project Phase 3 Atmospheric
Boundary Conditions (Experiment 1)* [Data set]. Data Integration and Analysis
System (DIAS). doi:[10.20783/DIAS.501](https://doi.org/10.20783/DIAS.501).
Use of the data is subject to the provider's terms; cite Kim (2017). **No
GSWP3 data is redistributed here**: the documents reference the NCAR archive
by URL only, the tests embed only a handful of scalar values traced from a
CESM run, and CI reads synthetic files. The topography file is the
USGS-derived `topodata_0.9x1.25_USGS_070110_stream_c151201.nc` from the same
archive.

## Synthetic data

CI never downloads data. `tools/gen_synthetic_gswp3.py` writes small files
with the GSWP3 layout into `components/data_models/cdeps/synthetic/`
(git-ignored): `clmforc.GSWP3.synthetic.{Solr,Prec,TPQWL}.2000-01.nc`
(NETCDF3 classic, `(time, lat, lon)` float32 on a 4 × 5 grid, 248 records at
the GSWP3 record times) and `topodata.synthetic.nc` (static
`(time=1, lat, lon)` float64). Every value is closed-form and exactly
representable in float32 (k = record index, (i, j) = cell):

```
FSDS = 100 + 2k + 50i + 10j            PSRF = 90000 + 16k + 1000i + 100j
PRECTmms = (1 + k + 8i + 2j)·2^-20     QBOT = (2 + 0.0625k + i + 0.25j)·2^-9
TBOT = 270 + 0.25k + 2i + 0.5j         WIND = 3 + 0.125k + i + 0.5j
FLDS = 250 + 0.5k + 10i + j            TOPO = 1000 + 100i + 10j
```

`cdeps_datm_gswp3_synthetic.esm` reads cell (1, 2). Its two tests (05:30Z
and 21:00Z on 2000-01-01; the latter on the rain/snow ramp) assert the
reader → Streams → Clmncep chain — 11 Streams values/factors and 13 exports
each — against values computed from the generator formulas with the same
Python transcriptions the law tests use.

Run locally:

```
python3 tools/gen_synthetic_gswp3.py          # needs numpy + scipy
esm test components/data_models/cdeps         # esm built with --features esio
```

CI (`.github/workflows/test-esm.yml`) runs the generator before each
inline-test sweep (Rust, Julia, and the disabled Python gate) and builds the
`esm` CLI with `--features esio`. With `esio`, documents with data-fed
parameters but no tests (this directory's `_data` file, `earthsci_data/*`)
no longer report a "cannot ingest data_sources" ERROR row, and still read
nothing.

### Status of the data test

On the Rust CLI (EarthSciAST main, esm 0.14.0, built with `esio`) the 48
assertions currently **ERROR** with `E_TREEWALK_UNBOUND_NAME`: the Rust build
pipeline binds a *shaped* DISCRETE (time-varying) data-fed parameter for the
right-hand side but not in the scope where it materializes algebraic
observeds, so `Streams.swdn` cannot read `GSWP3FilesSynthetic.FSDS[1]`. A
one-model document with a scalar observed `y = Q[1]` over a data-fed
`Q[rec]` reproduces it, while a scalar (shapeless) data-fed parameter
feeding an observed works and returns the right record at or before `t`
from these same synthetic files. This is an upstream runner gap, not a
property of the documents. The expected values were checked by running the
same 48 assertions with the record pairs supplied as overrides through the
mounted Streams → Clmncep chain (48 pass on the Rust CLI). The Julia runner
has not been tried on this file.

## Testing

```
python3 tools/gen_synthetic_gswp3.py
esm validate components/data_models/cdeps/<file>.esm      # each of the four files
esm units    components/data_models/cdeps/<file>.esm      # every equation consistent
esm test     components/data_models/cdeps
```

`cdeps_datm_gswp3.esm` (no data, no esio feature needed):

- **Streams** (12 tests, 130 assertions): 9 traced rows of
  `cdeps_strdata_streams.csv` (steps 0, 1, 2, 3, 5, 6, 11 of point 1; steps
  0 and 11 of point 16). For each, the record pairs of all seven fields and
  the topo record go in; the seven interpolated values, topo, and the
  factors (`flb_solar`; linear `flb_tpqw`/`fub_tpqw`; nearest
  `flb_precip`/`fub_precip`) are asserted. The rows cover linear at the
  interval midpoint, at 2/3 and on a record time (flb = 1), nearest picking
  LB, UB and a tie, and coszen inside an interval and on a new interval.
  Plus three closed-form coszen tests: a mid-latitude daytime point (lat 40,
  lon 120, 05:30Z) where cosz varies strongly within the interval; the same
  point before sunrise (cosz clipped while tavCosz > 0.001 → night branch);
  and polar night.
- **Clmncep** (20 tests, 77 assertions): 3 traced (step, point) rows of
  `datm_gswp3_streams.csv` → `datm_gswp3_exports.csv` (now at `rel = 1e-12`),
  and 17 closed-form branch tests: tbot degC detector, 180 K floor, pbot
  zero-fill, no-pbot stream, qsat cap (now `rel = 1e-12` against the exact
  double, was 1e-5 against an 8-digit value), relative-humidity path,
  dew-point path (degC and ice phase), all rain, mid-ramp rain/snow split,
  longwave fallback, no topo stream, bottom-height stream present,
  albedo-weighted swnet, swnet without albedos, swnet with anidrmax = 0,
  and shortwave ratios at their 0.99 clamp.

All traced points are at lat −90 on 2000-01-01 (polar day, all snow), so no
traced row reaches the rain, mid-ramp, longwave-fallback, topo-absent,
albedo-weighted swnet, rh or dew-point branches. Their expected values are
**closed-form recomputations** with an independent Python transcription of
`datm_datamode_clmncep_advance` — the same transcription reproduces all 192
traced export rows to ≤ 1e-15 relative — not dump values; each test's
description says so.

## Provenance of the traced values

The `stage1/...` paths in descriptions refer to the EqESM project repository
(private): an instrumented CESM checkout (CDEPS fork
`stage1/EqESM-cesm-cdeps`, branch `instrument/cdeps-dumps`) and the dumps it
wrote for the reference case `I2000Clm60Sp_f19` (start 2000-01-01, 12
coupling steps of 1800 s, PET 0, first 16 mesh points: lat −90, lon 0 …
37.5°; stream configuration
`stage1/cime/cases/I2000Clm60Sp_f19/CaseDocs/datm.streams.xml`):

| dump | content | used by |
|---|---|---|
| `stage1/dumps/cdeps/cdeps_strdata_streams.csv` | per (step, stream, field, point): lb, ub, flb, fub, value of shr_strdata_advance | Streams tests |
| `stage1/dumps/cdeps/datm_gswp3_streams.csv` | the interpolated strm_* values entering the datamode (and tbotmax) | Clmncep tests (inputs) |
| `stage1/dumps/cdeps/datm_gswp3_exports.csv` | the export state after datm_datamode_clmncep_advance (and anidrmax) | Clmncep tests (expected) |

The orbital parameters (`eccen 0.0167036603927656034`, `obliqr
0.409101122579778931`, `lambm0 -0.0324724956615293284`, `mvelpp
4.93745779048815780`) are those of the same run's mediator dump
(`stage1/dumps/cmeps/cmeps_ocnalb.csv`, orb_iyear 2000). The dumps were
checked solution-neutral (bit-identical restart files vs the uninstrumented
run). The dump files are not public; the values the tests need are embedded
in the tests.

## Units hygiene

Every literal in `cdeps_templates.esm` and in the `Streams`/`Clmncep`
equations carries an explicit `units` field, and `esm units` reports every
equation **consistent**. Readings: the esat polynomials are Taylor
expansions in °C with coefficients in Pa/K^n; the ratio_rvrf polynomials
expand in s = swdn/2 [W/m²] with coefficients in (m²/W)^n; the ea formula's
5.95e-5 carries 1/Pa; the rain ramp slope 0.5 carries 1/K; stebol carries
W/(m² K⁴); angles are rad, lat/lon deg (converted by `π/180 rad/deg`), times
s, the calendar day dimensionless.
