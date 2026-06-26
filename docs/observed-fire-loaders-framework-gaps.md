# Observed-fire data loaders — framework-gaps report (declarative-or-fail)

**Bead:** `esm-1zj` (campfire-e2e **E1**). **Date:** 2026-06-26.
**Plan:** `.gc/agents/mayor/observed-fire-data-loaders-plan-2026-06-26.md`.

This is the **F-data-4 feasibility verdict** for the three observed-fire pure-IO
loaders. Per the acceptance contract, framework limitations are **reported
(declarative-or-fail), not hacked around**: each loader is authored in the
correct 0.7.0 pure-IO shape, and where the canonical runner
(`earthsci_toolkit`) cannot yet do something, it is documented here and in the
loader `access_note`s rather than worked around in the `.esm`.

## What was delivered

| Artifact | Path | Kind |
|---|---|---|
| MTBS burn-severity loader | `components/earthsci_data/mtbs_severity_loader.esm` | `static` |
| NIFC/GeoMAC perimeters loader | `components/earthsci_data/nifc_perimeters_loader.esm` | `grid` (daily) |
| VIIRS/MODIS active-fire loader | `components/earthsci_data/viirs_active_fire_loader.esm` | `points` |
| Perimeter→burned_fraction rasterize **leaf** | `tools/leaves/nifc_perimeters_rasterize.py` | offline preprocessing |
| Fixtures (text) | `test/fixtures/earthsci_data/observed_fire/{campfire_perimeters_sample.geojson, viirs_active_fire_sample.csv}` | sample data |
| Feasibility driver (F-data-4) | `test/observed_fire_loaders_feasibility.py` | load + slice gate |

## Feasibility verdict: PASS (all three modalities read end-to-end)

`python test/observed_fire_loaders_feasibility.py` → **PASS**. It exercises,
with **no network** (injected `opener`/`fetcher`/`parser` over small fixtures):

1. **Structural `load()`** of all three loaders through the canonical runner —
   the same minimum-bar path `tools/run_esm_inline_tests.py` walks over
   `components/**/*.esm`.
2. **STATIC** (`mtbs_severity_loader`) sliced via `load_static` — `burn_severity_class`
   + `dnbr` mapped from their `file_variable`s out of a NetCDF raster.
3. **GRID** (`nifc_perimeters_loader`) sliced via `load_grid` — the rasterize
   leaf turns the sample perimeters into daily `burned_fraction` NetCDFs, which
   the loader reads back (`burned_fraction(50,80)`, cumulative growth).
4. **POINTS** (`viirs_active_fire_loader`) sliced via `load_points` — `frp` /
   `brightness` / `confidence` mapped from a FIRMS-format CSV, with the custom
   `{map_key}` / `{firms_source}` / bbox / `{date}` substitutions resolving.

The pure-IO loader framework therefore **generalizes** to three modalities it
had not exercised (static raster, points, rasterized-vector grid). The points
path is sufficient for VIIRS — the plan's rasterize-to-`detection_count`
fallback is **not** needed.

## Framework gaps / findings

### F-1 — No local data-cache (`EARTHSCIDATADIR`) resolution in the loader URL layer  *(the plan's C2 gap; pre-existing, not introduced here)*
The toolkit's `url_template` layer is **pure string templating** — there is no
env-var / local-cache / `file://` fallback resolution anywhere under
`earthsci_toolkit/data_loaders/` (no `environ`/`getenv`/`EARTHSCIDATADIR`/`cache`
references). All three loaders document an `access_note` pointing at
`EARTHSCIDATADIR`, exactly as the existing `era5_loader`/`openaq_loader` do, but
the runner does not implement it.
- **Impact:** a consumer must inject an `opener`/`fetcher` that resolves a local
  path, or point `url_template` at a `file://` path by hand. Live fetching of
  NIFC/MTBS/FIRMS data is therefore a downstream/consumer concern (AGENTS.md §2),
  consistent with the other earthsci_data loaders.
- **Disposition (declarative):** unchanged loaders; the fix belongs in
  EarthSciSerialization's runtime loader layer (EARTHSCIDATADIR-aware URL
  resolution), tracked as a framework follow-up. **Not** hacked into the `.esm`.

### F-2 — `points` column mapping does not coerce string CSV cells; numeric `unit_conversion` on a string column raises
`apply_variable_mapping` for `kind:points` keeps raw parsed columns; the default
CSV parser yields **strings**. A declared numeric `unit_conversion` then hits a
NumPy `UFuncTypeError` (string × float).
- **Impact on VIIRS:** FRP and brightness are already native MW / K, so the
  loader declares **no** `unit_conversion` and the consumer/parser coerces types
  (the feasibility driver's parser casts `frp`/`bright_ti4` to float). Documented
  in the loader's variable descriptions.
- **Disposition (declarative):** no `unit_conversion` on the points loader; if a
  future points source needs scaling, the framework should coerce declared-numeric
  variables (or expose a dtype hint) — a framework enhancement, not a loader hack.

### F-3 — Naive vs tz-aware `time`: grid/points loaders with tz-aware `temporal.start/end` require a tz-aware requested `time`
The loaders declare `temporal.start/end` as ISO `"…Z"` (tz-aware), matching the
`era5`/`openaq` convention. The runtime compares the requested `time` against
those bounds, so passing a **naive** `datetime` raises
`TypeError: can't compare offset-naive and offset-aware datetimes` (the `static`
kind is unaffected — it has no `temporal`).
- **Disposition (declarative):** correct consumer behavior is to pass a tz-aware
  `time` (the feasibility driver uses `datetime(..., tzinfo=timezone.utc)`); kept
  the tz-aware bounds for cross-loader consistency. Recommended framework
  enhancement: normalize naive→UTC or raise a clearer message.

### F-4 — No vector/polygon loader `kind` (by design — shaped the NIFC approach)
The `DataLoader.kind` enum is `grid`/`points`/`static`/`mesh`; fire perimeters
are time-varying **polygons** with no kind. Per the plan's no-new-primitives
principle, perimeters are **rasterized OFFLINE** by `tools/leaves/nifc_perimeters_rasterize.py`
to a `burned_fraction` grid read by an ordinary `kind:grid` loader — **zero new
loader kinds / engine primitives**. Recorded as the framework boundary that
shaped the design, not a defect to fix.

### F-5 — Single `url_template` per loader (+ mirrors are same-content fallbacks)  *(minor)*
MTBS ships two products (thematic severity **and** continuous dNBR). They are
modeled as two `file_variable`s read from one per-fire **bundle** (the
`usgs3dep_loader` "two variables from one fetched product" pattern). `mirrors`
are fallbacks for the *same* content, so a source whose layers live at *different*
endpoints can't express both as primaries. The bundle framing sidesteps this for
MTBS; noted for future multi-endpoint sources.

### F-6 — Version skew note (not a gap)
The locally-installed ESS reports `_CURRENT_VERSION (0,4,0)` while these files
(and the 35 migrated earthsci_data loaders) declare `esm 0.7.0`, so `load()`
emits a `UserWarning: 0.7.0 is newer than the current library version 0.4.0` and
accepts via the lenient-downward check. This is the **same** behavior the
existing migrated loaders rely on; the esm-aha validation matrix confirms these
files also load under the bumped ESS (`ess-v9a.7`, schema 0.7.0). No action.

## User-action items (carried from the plan; do not block E1 authoring)
- **FIRMS `MAP_KEY`** (free) for VIIRS/MODIS — supplied at runtime via the
  `{map_key}` substitution; never committed.
- **Rasterization analysis grid** — default = the fire model's domain grid
  (2018 Camp Fire domain); set via the leaf's `--grid` and the loader's grid
  `extents`.
- **Citations / licenses** — NIFC, MTBS, FIRMS are public/open; cited per source
  in each loader's `references`.
- **`EARTHSCIDATADIR` cache** — see F-1 (framework follow-up).
