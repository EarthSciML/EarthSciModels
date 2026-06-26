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
