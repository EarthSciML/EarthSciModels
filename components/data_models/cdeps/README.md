# CDEPS DATM stage 2 — `.esm` implementation

Stage-2 implementation of the CDEPS DATM data-atmosphere component for the
GSWP3v1 forcing with the CLMNCEP datamode (cdeps1.0.112, fork
`stage1/EqESM-cesm-cdeps` branch `instrument/cdeps-dumps`) as esm 1.3.0
files: the stream time-interpolation laws, the CLMNCEP forcing-derivation
laws, the four GSWP3 data sources read through the esm netcdf reader, and
the tests pinning the stage-1 instrumentation dumps
(`stage1/dumps/cdeps/`) — see [Testing](#testing).

All model logic lives in `.esm` files; this README is the human-readable
map. The `stage1/...` paths throughout refer to the EqESM project
repository (the CESM checkout instrumented to produce the dump tuples the
tests pin). Sources: `components/cdeps/datm/datm_datamode_clmncep_mod.F90`,
`components/cdeps/streams/dshr_strdata_mod.F90`,
`components/cdeps/streams/dshr_tinterp_mod.F90`,
`components/cdeps/share/shr_precip_mod.F90` (cdeps1.0.112); the stream
configuration of the reference I-class run
(`stage1/cime/cases/I2000Clm60Sp_f19/Buildconf/datmconf/datm.streams.xml`);
and the boundary/derivation tables in
`stage1/runs/CDEPS_LANE.md` + `stage1/runs/cdeps_instrument.json`.

## Files

| file | content |
|---|---|
| `cdeps_templates.esm` | expression-template library of the shared pointwise laws: the esat water/ice polynomials (`esat_poly_water`/`esat_poly_ice` + the phase-selecting `esat`, datm_datamode_clmncep_mod.F90:545-586), `qsat`, `vapor_pressure`, `density` (RDAIR = 287.0423113650487), the cam3_5_55 `ratio_rvrf_nir`/`ratio_rvrf_vis` shortwave polynomials, `rain_snow_frac`, `wind_split` |
| `cdeps_datm_gswp3.esm` | the component: `data_sources` (Solar/Precip/TPQW/topo on the public NCAR archive), the `Streams` interpolation model, the `Clmncep` datamode transformation model, and the `GSWP3Files` netcdf-reader wiring model; tests from the dump rows (51 assertions) |

## Model structure

```
GSWP3v1 netCDF on the NCAR inputdata server (0.5°, 3-hourly; topo 0.9x1.25°, static)
   │  esm netcdf reader (metadata.esio_format = "netcdf", https url_templates
   │  with {date:%Y-%m} placeholders, temporal blocks, time axis at "all",
   │  lat/lon fixed, extent -> N_REC metaparameter)
   ▼
GSWP3Files.*  (raw record values, shaped over index_sets.record)
   │  [the bilinear spatial map to the model grid is out of scope for
   │   this slice — the trace pins the post-map values (see Risks)]
   ▼
Streams.*     value = flb·lb + fub·ub   (coszen: lb·flb by day, 0 at night)
   │  per stream: Solar coszen, Precip nearest, TPQW linear, topo lower
   ▼
Clmncep.*     the datamode laws (below)
   ▼
Sa_*, Faxa_*  export state consumed by CLM via the mediator
```

`Streams` carries the time-interpolation law of `shr_strdata_advance`
(dshr_strdata_mod.F90:1292-1391): the interpolated value is the convex
combination of the lower/upper time-bound values with the
`shr_tInterp_getFactors` factors (linear: flb+fub=1; nearest/lower/upper:
unit vectors), and the coszen special case (value = lb·cosz/tavCosz by
day — the dumped flb IS cosz/tavCosz — and 0 when cosz ≤ 0.001, carried
here as the `day` flag). `Clmncep` carries the CLMNCEP datamode
derivations of `datm_datamode_clmncep_advance` (F90:328-487):
tbot units detector/clamp, wind split, qsat-capped specific humidity
(esat polynomials), density, pressure zero-fill, the shortwave
direct/diffuse split, the rain/snow ramp, the swnet albedo weighting, and
the topo/z/lwdn fallbacks. `GSWP3Files` declares the netcdf-reader field
wiring (source keys, file variables, shapes, selects).

## Data access (public NCAR archive)

All four `data_sources` point at the **public NCAR CESM inputdata server**
(`https://svn-ccsm-inputdata.cgd.ucar.edu/trunk/inputdata/atm/datm7/`), not
at cluster-local paths, so anyone can load and consume the component. The
three 3-hourly streams (Solar, Precip, TPQW) use the server's own monthly
file naming with a `{date:%Y-%m}` placeholder
(`atm_forcing.datm7.GSWP3.0.5d.v1.c170516/<Stream>/clmforc.GSWP3.c2011.0.5x0.5.<Solr|Prec|TPQWL>.{date:%Y-%m}.nc`),
with `temporal.start = 1901-01-01`, `temporal.end = 2014-12-31`,
`file_period = P1M`, `frequency = PT3H`, `records_per_file = 248` and
`time_variable = "time"` — the exact holdings verified with `curl -sI`
(HTTP 200 for every stream, 1901-01 through 2014-12; the topo file
`topo_forcing/topodata_0.9x1.25_USGS_070110_stream_c151201.nc` is a single
static file, `kind: static`, no `temporal` block). Each entry carries a
`reference` block: Kim (2017), doi:10.20783/DIAS.501, and the archive URL.
The 1991-01 files are the ones the reference run reads on 2000-01-01 via
`taxmode=cycle, year_align=1991`.

## The data_sources recipe (esm 0.7.0 CLI, esio enabled)

The netcdf reader is reached through `metadata.esio_format = "netcdf"`,
`select.axes` = `["all", {fixed: ilat}, {fixed: ilon}]` (0-based indices;
the time axis MUST stay "all" — record selection is the Provider's, a
`fixed` time axis is a reader error), and `extent.metaparameter` binding
the delivered record count to a document `metaparameters` entry so the
`index_sets.record` interval (size = the metaparameter) sizes the shaped
parameters. A model parameter then declares `shape: ["record"]` and
`update: {kind: "data", source: <key>, from: {file_variable: <var>}}`.
Each source needs its OWN extent metaparameter — the topo file delivers 1
record while the 3-hourly files deliver 248, and sources sharing one
metaparameter must agree on the count. The netcdf reader delivers the
file's native float32 values widened to float64.

**Runner caveat (Rust CLI):** the CLI materializes every data-fed parameter
at build — `esm test` runs extent discovery for `GSWP3Files.*` even though
no test reads those parameters, so with the https url_templates it needs
network access to the NCAR archive at test time (no network ⇒ every test
in the document errors at compile with the transport error). `esm validate`
is offline. This is a property of the CLI's build (all providers prepared
up front), not of the document: the previous `file://` form had the same
build path, it just read local files. `GSWP3Files` therefore carries no
inline tests — the raw-record assertions were dropped in the portability
change (see [Testing](#testing)) — and numeric reader checks are a
downstream consumer concern with data access.

## Testing

`esm validate components/data_models/cdeps/cdeps_templates.esm
components/data_models/cdeps/cdeps_datm_gswp3.esm` and
`esm test components/data_models/cdeps` (the CDEPS-only suite — the CDEPS
files import no `${ESD_ROOT}` templates, so no EarthSciDiscretizations
checkout is needed).

- **Streams tests** (7): coszen day rows (steps 0 and 11), the coszen
  night branch (synthetic — the traced points are all at lat −90 on
  Jan 1, i.e. polar day), linear rows with midpoint (flb = fub = 1/2) and
  off-midpoint (flb = 2/3) factors, nearest (1,0), lower (1,0). All
  expected values are the dumped `value` column to 1e-12 relative.
- **Clmncep tests** (7): three traced (step, point) rows exercising the
  full stream→export chain (step 0 point 1, step 11 point 1, step 0
  point 16 — the last pins the per-point shortwave split at the 8th
  significant digit), plus synthetic branch tuples for the tbot units
  detector (+273.15), the 180 K floor, the pbot zero→pstd fill, and the
  qsat cap (esat(10 °C) = 1227.073698721729 Pa → qsat = 7.5672320e-3).
- **GSWP3Files tests** (none): the raw-record reader test
  (`netcdf_records`, 7 assertions on records 1/248 of FSDS, PRECTmms, TBOT
  and the single TOPO record through the netcdf reader at the fixed cells)
  was dropped in the portability change so the component loads and tests
  without live external data — the same convention as the earthsci_data
  components (empty `tests`). The field wiring (source keys, file
  variables, shapes, selects) is unchanged and is exercised by consumers
  with data access.

Total: 51 assertions (Streams 7, Clmncep 44), all passing on the Rust CLI
when the data-fed `GSWP3Files` parameters can be materialized — locally
this means the `file://` form, or network access to the NCAR archive for
the https form (see [Data access](#data-access-public-ncar-archive)). The
dumps they pin were verified solution-neutral (bit-identical restart files
vs the reference `I2000Clm60Sp_f19` run) and law-exact on every row
(`stage1/analysis/check_datm_neutral.py`, `check_datm_laws.py`).

## Deferred / notes

- The **spatial map** (bilinear ESMF regrid from the 0.5° source mesh to
  the 1.9x2.5° model mesh) is applied before the traced layer; the trace
  pins post-map values, so the stage-2 model consumes the same values.
  The regrid itself is an EarthSciDiscretizations concern (PR later).
- The **temporal cadence**: the dumps pin the interpolated values and
  factors per step; the stream clock semantics (why step 0 sits at
  flb = fub = 1/2 and step 11 at flb = 2/3) follow from
  `shr_strdata_advance`'s interval bookkeeping and are not re-expressed
  here — a stage-3 integrator concern (EarthSciIntegrator).
- The presaero/presndep/preso3 streams (pure pass-throughs with unit
  scales) and the lwdn formula fallback / swdndr+swdndf stream branch of
  the datamode are documented but not traced (inactive in the GSWP3
  case); the fallback branches are implemented in `Clmncep` behind the
  `lwdn_present`/`pbot_present`/`topo_present` flags and the Sx_* spval
  convention. The lwdn-fallback vapor pressure `e2`
  (`datm_datamode_clmncep_mod.F90:440`, `e = Sa_pslv Sa_shum / (0.622 +
  0.378 Sa_shum)`) is the same law as the density-path `vp`
  (F90:435), so `Clmncep` computes it as
  `apply_expression_template("vapor_pressure", {q: Sa_shum, pbot:
  Sa_pslv})` — one law, one template, no copied formula.
- JRA55 datamode (same stream layer, different datamode laws) is the
  next slice if time permits.
- Factoring cleanup: the `s^2`/`s^3` terms of the ratio_rvrf_nir/vis
  polynomials are written with the `^` operator
  (`{"op": "^", "args": ["s", 2]}` / `["s", 3]`) instead of nested
  `s·s` / `(s·s)·s` multiplications; the repeated constants are factored
  as zero-parameter fragment templates — `tkfrz` = 273.15 K (the esat
  phase branch, both polynomial t-axis clamps, and the rain/snow ramp),
  `eps` = 0.622 and `eps1` = 1 − eps = 0.378 (the molecular-weight-ratio
  pair of the qsat/vapor-pressure/density laws, `eps1` derived from
  `eps` so the pair is defined once) — applied with `bindings: {}`. The
  laws and expected values are unchanged.

## Units hygiene

Every literal in `cdeps_templates.esm` and in the `Streams`/`Clmncep`
equations of `cdeps_datm_gswp3.esm` carries an explicit `units` field
(`{"op": "const", "args": [], "value": …, "units": …}`), so
`./esm units stage2/cdeps_templates.esm stage2/cdeps_datm_gswp3.esm`
reports every equation **consistent** — no
`units_dimensionless_literal_mismatch`, no `dimensional_mismatch`, no
undetermined operands. The dimensional readings: the esat polynomials
are Taylor expansions in °C (temperature axis) with coefficients in
Pa/K^n and the ×100 hPa→Pa scale dimensionless; the ratio_rvrf
polynomials expand in s = swdn/2 [W/m^2] with coefficients in (m^2/W)^n;
the ea formula's 5.95e-5 carries 1/Pa so the emissivity reads
dimensionless; the rain ramp 0.5 carries 1/K; stebol carries
W/(m^2 K^4). The 51 assertions are unchanged (same laws, same expected
values).
