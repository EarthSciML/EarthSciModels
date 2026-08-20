# Pure-I/O Data-Loader Migration — the loader + regridding-model split

> ## ⚠️ SUPERSEDED by esm 1.0.0 — historical record only
>
> This guide describes the 0.5.0 → 0.6.0 loader split and the 0.7.0 → 0.8.0
> grid-descriptor removal that followed it. **esm 1.0.0 retired the concept it
> is built on.** Do not follow its instructions for new work; read it only to
> understand how the existing `components/earthsci_data/*.esm` files got their
> present shape.
>
> What 1.0.0 changed (esm-spec §8):
>
> - The top-level key is **`data_sources`**, not `data_loaders`.
> - A source is **not a component**. It cannot be a coupling endpoint, a
>   subsystem, or a scoped-name path root, so the "declare the loader as the
>   subsystem `raw` via `{"ref": "./X_loader.esm"}`" pattern below no longer
>   exists.
> - A source **exposes no variables**. The `variables` map is gone from the
>   entry; each former loader variable becomes a **parameter on the model that
>   consumes it**, carrying
>   `update: {kind: "data", source: "<registry key>", from: {file_variable,
>   unit_conversion?, codes?, select?}}`. Units are declared once, on that
>   parameter, and a parameter with a `data` update MUST declare a `shape`.
> - `DataSource` is `additionalProperties: false` over `{kind, source,
>   temporal, determinism, reader_options, select, record_filter, extent,
>   reference, metadata}` — no `grid`, no `spatial`, no `regridding`.
>
> The version numbers in the tables below (`esm 0.5.0`, `0.6.0`, `0.7.0`,
> `0.8.0`) are the historical ones and are **not** what the corpus carries; the
> loader rejects every major-0 document outright.

This guide documents the **repeatable split pattern** for migrating the ten
`components/earthsci_data/*.esm` files from the old **co-located** format (one
file holding both a `models.X` coupler *and* a `data_loaders.X` block) into the
new **pure-I/O loader + regridding-model** pair required by the merged ESS RFC
[`pure-io-data-loaders`](https://github.com/EarthSciML/EarthSciAST/blob/main/docs/content/rfcs/pure-io-data-loaders.md)
(schema beads `ess-v9a.2`–`.8`; ESD rule beads `esd-47z.1`–`.5`).

It is written for the polecats picking up the remaining migration beads
(`esm-3nc.2`–`.5`). The two reference cases established by `esm-3nc.1` —
**`era5`** (geographic) and **`wrf`** (Lambert Conformal Conic) — are worked
examples you can copy from.

> **Hard break, no deprecation window (RFC §7).** The ESS schema change is
> already on `main`: a loader carrying the old `spatial` or `regridding`
> sub-blocks is now **rejected** at load (`SchemaValidationError: Additional
> properties ('spatial'|'regridding') are not allowed`). The CI gate installs
> `earthsci_ast @ EarthSciAST main`, so every unmigrated
> `earthsci_data` file fails the gate until it is split. Migrate in lockstep.

---

## 1. What changed

| Old (co-located, `esm` 0.5.0) | New (split, `esm` 0.6.0) |
|---|---|
| One file: `models.X` **and** `data_loaders.X` | Two files: `X.esm` (model) + `X_loader.esm` (loader) |
| `data_loaders.X.spatial` (proj4 `crs` string / `grid_type` / `staggering` / `resolution` / `extent`) | **Removed.** Native grid is a GDD `grid` block with a structured `crs` descriptor |
| `data_loaders.X.regridding` (`fill_value` / `extrapolation`) | **Removed.** Regridding is **per-variable on the model** (`Model.regrid`) |
| model subsystem re-implements each loader field with an `interp_unsafe` observed | model references the loader as a **subsystem** (`{"ref": "./X_loader.esm"}`) |

The loader becomes **pure I/O**: it declares *what to read* (`source`,
`variables`, optional `temporal`) and *its native grid* (`grid` with `crs`). It
performs **no** reprojection and **no** regridding — those are the regridding
model's job.

---

## 2. File-naming & placement convention

Both files stay in `components/earthsci_data/`:

| Role | Path | Top-level content |
|---|---|---|
| Pure loader | `components/earthsci_data/<name>_loader.esm` | `data_loaders.<NAME>` **only** (no `models`) |
| Regridding model | `components/earthsci_data/<name>.esm` | `models.<NAME>` (keeps the original filename, so existing consumers' `{"ref": "./<name>.esm"}` keep working) |

The model references the loader by **relative path**: `{"ref": "./<name>_loader.esm"}`.
The ref resolves relative to the model file's directory.

**Multi-loader components.** A component whose original co-located file held several
`data_loaders` blocks (e.g. `geosfp` with six GEOS-FP collections, `ncep_ncar` with a
pressure + a surface loader) splits into **one loader file per block** — §8's "one component
per loader file" rule — named `<name>_<block>_loader.esm` (e.g. `geosfp_a3dyn_loader.esm`,
`ncep_ncar_surface_loader.esm`). The single model file `<name>.esm` declares each as a
subsystem keyed by the **original loader name** (`GEOSFP_A3dyn`, `NCEPNCAR_Surface`, …) so
the pre-existing observed expressions `GEOSFP_A3dyn.U` / `NCEPNCAR_Surface.hgt_sfc` keep
resolving unchanged. A `kind: "lookup"` block (removed in 0.6.0) is **not** a loader — re-home
it as top-level `function_tables` (see `geosfp`'s `Ap`/`Bp` → `geosfp_Ap_pa`/`geosfp_Bp`).

---

## 3. The loader half (`<name>_loader.esm`)

A **loader-only** document is valid (the schema's top-level `anyOf` has a
`data_loaders` branch — `ess-v9a.4`). Minimal shape:

```jsonc
{
  "esm": "0.6.0",
  "metadata": { "name": "<NAME>_loader", "description": "...", "tags": [...] },
  "data_loaders": {
    "<NAME>": {
      "kind": "grid",                     // grid | points | static | mesh
      "source": { "url_template": "https://.../{date:%Y}_{date:%m}.nc" },
      "temporal": {                        // OMIT for non-time-varying data (→ CONST cadence)
        "start": "...", "end": "...",
        "file_period": "P1M", "frequency": "PT1H",
        "records_per_file": 744, "time_variable": "valid_time"
      },
      "grid": {
        "family": "cartesian",             // cartesian for gridded; unstructured for points
        "crs": { "projection": "longlat", "datum": "WGS84" },
        "dimensions": ["lon", "lat", "pressure_level"],
        "extents": {
          "lon": { "n": 1440, "spacing": "uniform" },
          "lat": { "n": 720,  "spacing": "uniform" },
          "pressure_level": { "n": "n_pressure_level", "spacing": "uniform" }
        },
        "parameters": {                    // for n-values resolved from the source at load time
          "n_pressure_level": { "description": "resolved from the source dataset at load time" }
        }
      },
      "variables": {
        "t": { "file_variable": "t", "units": "K", "description": "..." }
      },
      "reference": { ... },
      "metadata": { ... }                  // free-form: keep extent/resolution/staggering here for §8 parity
    }
  }
}
```

### 3.1 Encoding the native grid `crs`

`crs` is **orthogonal to `family`**: a `cartesian` grid can be geographic or
projected; only `crs` differs. The old proj4 string maps to a structured
descriptor (`GridCRS`):

- **Geographic (identity reprojection)** — `era5`, `geosfp`, `ncep_ncar`,
  `landfire`, `usgs3dep`, `ceds`, `edgar`, `openaq`:
  ```json
  "crs": { "projection": "longlat", "datum": "WGS84" }
  ```
- **Lambert Conformal Conic** — `wrf`, `nei2016_monthly`:
  ```json
  "crs": {
    "projection": "lambert_conformal",
    "datum": "sphere",
    "R": 6370000.0,
    "parameters": { "lat_1": 30.0, "lat_2": 60.0, "lat_0": 38.999996, "lon_0": -97.0 }
  }
  ```
  Map the proj4 keys directly: `+lat_1/+lat_2/+lat_0/+lon_0` → `crs.parameters`;
  `+a=+b=R` → `crs.R` with `datum: "sphere"`. **Do not** keep the proj4 string in
  `crs` (it is not a valid `crs` field); keep it in loader `metadata` for
  provenance if you like.

> **`GridExtent` only carries `n` (an int **or** a parameter-name string) +
> `spacing`** — it has no min/max/Δ fields. The real bounds/resolution resolve
> from the source dataset at load time; record the documented extent/resolution
> in the loader's free-form `metadata` (RFC §8 "GDD grid parity").

### 3.2 Cadence (`ess-v9a.5`)

Cadence is **derived**, not declared: a loader **with** a `temporal` block seeds
`DISCRETE` (refreshed on its update schedule); a loader **without** one seeds
`CONST` (folded once at bind). The only knob is whether you include `temporal`.
Time-varying met/emissions → include it; fixed climatology/static terrain
(`landfire`, `usgs3dep`) → omit it.

---

## 4. The model half (`<name>.esm`)

The regridding model is the **same coupler model that already exists**,
restructured to (RFC §6):

1. declare the loader as a **subsystem** (`{"ref": "./<name>_loader.esm"}`);
2. carry a per-variable **`regrid`** block; and
3. keep its parameters (`lon/lat/lev/t_ref`) and its derived observed variables
   (e.g. `P`, `P_total`, `z`, `δxδlon`, `δyδlat`).

```jsonc
"models": {
  "<NAME>": {
    "coupletype": "<NAME>Coupler",
    "variables": { /* parameters lon/lat/lev/t_ref + derived observed */ },
    "subsystems": { "<key>": { "ref": "./<name>_loader.esm" } },
    "regrid": {
      "u": { "method": "bspline",      "description": "..." },
      "t": { "method": "conservative", "description": "..." }
    },
    "equations": [],
    "tests": []
  }
}
```

The subsystem resolves to a `DataLoader` **named by the parent's subsystem key**
(not the loader file's internal name). Its fields are referenced by dot notation
`<NAME>.<key>.<var>`.

### 4.1 Two coupling sub-patterns — match the original's interface

How downstream consumers (and the runtime `couple2`) name the loader fields
dictates the subsystem key and whether you re-expose:

- **Pattern A — namespaced subsystem (`era5`).** The original model exposed
  loader fields under a sub-namespace (`ERA5.pl.u`). Bind the loader under that
  same key (`"pl"`) and reference fields directly via the dotpath; **no
  re-exposure** needed. `MeanWind.v_lon ~ ERA5.pl.u` keeps working.

- **Pattern B — re-exposed at model top level (`wrf`).** The original model
  exposed loader fields at the model top level (`WRF.U`). Bind the loader under
  an internal key (`"raw"`) and **re-expose** the needed fields as model
  `observed` variables whose expression is the dotpath:
  ```json
  "U": { "type": "observed", "units": "m/s", "expression": "raw.U" }
  ```
  This preserves `WRF.U` for `MeanWind.v_lon ~ WRF.U` and lets derived observeds
  (`P_total = raw.P + raw.PB`, `z = (raw.PH + raw.PHB)/9.80665`) reference loader
  fields.

Check the original model's `reference.notes` (the `couple2 with MeanWindCoupler`
line) and `couplings/*.esm` to see which symbol paths must survive.

### 4.2 Per-variable `regrid` method

`regrid` is keyed by the **loader-field variable name** → `RegridSpec`. `method`
is one of three (`RegridSpec.additionalProperties: false`):

| `method` | Use for | ESD kernel |
|---|---|---|
| `conservative` | cell-centered gridded scalars (T, q, emissions, geopotential) — mass-conserving | `regridding/conservative_regrid_overlap_join.esm` |
| `bspline` | edge/face-staggered gridded fields (C-grid winds U/V/W) — interpolating | `regridding/bspline_regrid.esm` (`esd-47z.3`) |
| `cell_average` | scattered points (`openaq`) — bin-average; add `"missing_value": <num>` for empty cells | `regridding/point_cell_average_regrid.esm` (`esd-47z.4`) |

`method` is technically optional (it defaults by the variable's staggering on the
native grid), **but declare it explicitly** in these reference migrations so the
intent is self-documenting. For `era5` the horizontal wind components `u`, `v`
take `bspline` (the vertical-velocity scalar `w` stays `conservative`); for `wrf`
all three C-grid winds `U`, `V`, `W` take `bspline`.

### 4.3 Reprojection is by convention — there is no `$ref` to the ESD rule

The reprojection rule is selected **by convention** from the loader's
`grid.crs.projection`: `longlat` → ESD `reprojection/longlat.esm` (identity,
`esd-47z.1`); `lambert_conformal` → ESD `reprojection/lambert_conformal.esm`
(`esd-47z.2`), parameterized by `crs.parameters`. The model does **not** name the
ESD file; it only needs the loader's `crs` to be correct. Document the selected
rule in the model's `reference.notes` for the reader.

---

## 5. Reference cases (copy from these)

| File | CRS | Pattern | Notes |
|---|---|---|---|
| `components/earthsci_data/era5.esm` + `era5_loader.esm` | geographic `longlat`/WGS84 | A (subsystem `pl`) | 16 pressure-level vars; `u`/`v`→bspline, rest→conservative; `P` via `function_tables` lookup |
| `components/earthsci_data/wrf.esm` + `wrf_loader.esm` | `lambert_conformal` (30/60/38.999996/-97/R=6370000) | B (re-expose, subsystem `raw`) | C-grid `U`/`V`/`W`→bspline, scalars→conservative; derived `P_total`, `z` |

---

## 6. Remaining files (RFC Appendix A) → beads

| File | Native CRS | `kind` | Reprojection | Regridding | Bead |
|---|---|---|---|---|---|
| `era5` | geographic | grid | identity | centered→conservative, wind→B-spline | **esm-3nc.1 ✓** |
| `wrf` | LCC (30/60/39/-97/6370000) | grid | LCC↔lonlat | centered→conservative, C-grid wind→B-spline | **esm-3nc.1 ✓** |
| `geosfp` | `longlat`/WGS84 (0.3125°×0.25°) | grid | identity | centered→conservative, staggered (A3dyn U/V/OMEGA)→B-spline | **esm-3nc.2 ✓** |
| `ncep_ncar` | geographic | grid | identity | centered→conservative, wind→B-spline | **esm-3nc.2 ✓** |
| `ceds` | geographic | grid | identity | emissions (centered)→conservative | esm-3nc.3 |
| `edgar_v81_monthly` | geographic | grid | identity | emissions→conservative | esm-3nc.3 |
| `nei2016_monthly` | **LCC** (33/45/40/-97/**R=6370997**) | grid | LCC↔lonlat | emissions (centered)→conservative | esm-3nc.3 |
| `landfire` | `longlat`/WGS84 (~30 m) | static | identity | static, centered→conservative (**omit `temporal`**) | esm-3nc.4 |
| `usgs3dep` | `EPSG:4326` (~10 m) | static | identity | static, centered→conservative (**omit `temporal`**) | esm-3nc.4 |
| `openaq` | `longlat`/WGS84 (point stations) | **points** | identity | **cell_average** + `missing_value` for empty cells | esm-3nc.5 |

Notes for the projected/special cases:
- **`nei2016_monthly`** is the second LCC dataset — same `crs` shape as `wrf`
  but **different parameters**: `{lat_1:33, lat_2:45, lat_0:40, lon_0:-97}`,
  `R:6370997.0`. One rule, two parameter sets (the declarative-or-fail proof).
- **`openaq`** uses `kind: "points"`, `grid.family: "unstructured"`, and
  `regrid.<var> = {"method": "cell_average", "missing_value": <num>}`.
- **`geosfp`** is the one geographic file with genuinely staggered variables
  (A3dyn `U`/`V`/`OMEGA` on lon/lat/lev edges) — those take `bspline`, the rest
  `conservative`.

---

## 7. Validate before you push

The CI gate (`tools/run_esm_inline_tests.py`) walks `components/**/*.esm` and,
for a file with no inline `tests` (all loaders/regridding models — they need real
NetCDF), runs a **load-only minimum-bar gate**: `earthsci_ast.load(file)`
must succeed. Both halves must load independently (the model load resolves the
`{"ref": ...}` to the loader file).

Run it on just your changed files:

```bash
python3 tools/run_esm_inline_tests.py \
  --files components/earthsci_data/<name>_loader.esm \
          components/earthsci_data/<name>.esm
```

Expect `2P / 0F / 0E`. A `SchemaValidationError` mentioning `spatial` or
`regridding` means a legacy block survived; a `SubsystemRefError` means the
model's `{"ref": ...}` path is wrong.

---

## 8. Gotchas

- **Keep the model filename `<name>.esm`** so existing `{"ref": "./<name>.esm"}`
  consumers and `couplings/*.esm` references (e.g. `ERA5.lon`/`.lat`/`.lev`)
  keep resolving. The model still owns `lon`/`lat`/`lev`/`t_ref` parameters.
- **`function_tables` is top-level**, not under the model (e.g. era5's
  `era5_pressure_levels_pa`, used by the `P` observed `table_lookup`). Keep it in
  the **model** file, not the loader.
- **One component per loader file.** A `{"ref": ...}` target must contain exactly
  one top-level model/loader. Don't put two `data_loaders` entries in one
  `_loader.esm`.
- **Preserve documented gaps.** Carry forward `reference.notes` gap markers
  (era5's `gt-6ohw` δPδlev omission; wrf's `gt-p3ep(lookup)` δzδlev omission) so
  they stay tracked.
