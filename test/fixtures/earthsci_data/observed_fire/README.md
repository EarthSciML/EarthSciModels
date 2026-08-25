# observed-fire loader fixtures (bead esm-1zj, campfire-e2e E1)

Small, text-only fixtures backing the three observed-fire pure-IO data loaders
and their F-data-4 feasibility driver
([`test/observed_fire_loaders_feasibility.py`](../../../observed_fire_loaders_feasibility.py)).

| File | Role |
|------|------|
| `campfire_perimeters_sample.geojson` | Tiny **synthetic** 3-day growing fire-perimeter set (NIFC/GeoMAC-shaped `FeatureCollection`, EPSG:4326, square polygons) over a Camp-Fire-like domain. Input to `tools/leaves/nifc_perimeters_rasterize.py`, which rasterizes it to daily `burned_fraction` NetCDFs that `nifc_perimeters_loader.esm` reads. **Not** real Camp Fire geometry. |
| `viirs_active_fire_sample.csv` | Tiny FIRMS VIIRS area-CSV (real column layout: `latitude,longitude,bright_ti4,…,confidence,…,frp,daynight`) with 5 synthetic detections over the same domain. Read by `viirs_active_fire_loader.esm` via `load_points`. |

The NetCDF inputs the `grid`/`static` loaders read (the rasterized perimeters and
the MTBS static raster) are **generated at runtime** by the feasibility driver
into a temp dir (via the rasterize leaf / xarray), so no binary blobs are
committed here.

These fixtures live under `test/fixtures/**`, so neither the Python inline-test
gate (`tools/run_esm_inline_tests.py`) nor the Julia discovery auto-walks them —
the feasibility driver is the explicit entry point:

```bash
python test/observed_fire_loaders_feasibility.py   # exit 0 = green
```

See [`docs/observed-fire-loaders-framework-gaps.md`](../../../../docs/observed-fire-loaders-framework-gaps.md)
for the F-data-4 verdict and the declarative-or-fail framework findings.

## esm 1.0.0 (2026-08-20)

The three loader files are now `data_sources` catalogs, not `data_loaders`.
They are the only data sources in the corpus with **no consuming `.esm`**, so
they stay standalone rather than being merged into a consumer the way the other
26 sources were. Two consequences for the driver:

- `EsmFile.data_loaders` and `DataSource.variables` are gone. A data source is
  no longer a component and carries no variable map; each former loader
  variable becomes a **parameter on the consuming model** with
  `update: {kind: "data", source: "<registry key>", from: {file_variable, …}}`,
  and `earthsci_ast.data_sources.load_data` / `load_grid` / `load_points` /
  `load_static` take `bindings = {consuming parameter name -> DataSourceBinding}`
  (phase-6 H-4 moved the data-loading tier out of the top-level namespace; the
  xarray-backed `grid` / `static` openers now need the `data` extra:
  `pip install "earthsci-ast[data]"`).
- These catalogs have no consumer, so they cannot supply those bindings. Their
  six `file_variable` / `units` / `description` declarations are parked
  verbatim in each source's `metadata.unconsumed_file_variables`, with the
  reasoning in `metadata.unconsumed_file_variables_note`. A shared catalog is
  not self-describing at 1.0.0 — that is an open format gap, recorded, not
  worked around.

`test/observed_fire_loaders_feasibility.py` still uses the 0.x
`m.data_loaders[...]` / `dl.variables` API and has not been ported.
