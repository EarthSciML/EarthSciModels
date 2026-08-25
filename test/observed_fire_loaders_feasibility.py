#!/usr/bin/env python3
"""test/observed_fire_loaders_feasibility.py  (campfire-e2e E1, bead esm-1zj)

F-data-4 FEASIBILITY GATE for the three observed-fire pure-IO data loaders
(campfire-e2e plan, observed-fire-data-loaders-plan-2026-06-26.md): confirm
that the canonical ESS Python runner (``earthsci_ast``) can READ each new
loader END-TO-END — both the structural ``load_path()`` (the same path the
``tools/run_esm_inline_tests.py`` gate walks) AND the per-kind runtime
slice (``load_grid`` / ``load_static`` / ``load_points``) — across THREE
modalities the pure-IO loader framework has not previously exercised:

  * STATIC raster        -> mtbs_severity_loader.esm        (load_static)
  * GRID (rasterized     -> nifc_perimeters_loader.esm       (load_grid)
    vector, via the
    nifc rasterize leaf)
  * POINTS               -> viirs_active_fire_loader.esm      (load_points)

This DOUBLES as a generality test of the framework on data it has not seen.
NO NETWORK: each slice injects an ``opener`` / ``fetcher`` / ``parser`` that
returns small fixture data (the framework supports this by design — the
URL layer is pure string templating and the runtime takes injected I/O).
Framework gaps surfaced here are reported in
``docs/observed-fire-loaders-framework-gaps.md`` (declarative-or-fail —
they are documented, not hacked around).

Fixtures (committed, text):
  test/fixtures/earthsci_data/observed_fire/campfire_perimeters_sample.geojson
  test/fixtures/earthsci_data/observed_fire/viirs_active_fire_sample.csv
NetCDF fixtures (NIFC rasterized output + the MTBS static raster) are built at
runtime into a temp dir via the rasterize leaf / xarray, so no binary blobs
are committed.

Exit codes:  0 = every check passed   1 = at least one check failed
"""
from __future__ import annotations

import csv
import datetime as dt
import io
import os
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
_FIX = os.path.join(_HERE, "fixtures", "earthsci_data", "observed_fire")
_LEAF = os.path.join(_ROOT, "tools", "leaves", "nifc_perimeters_rasterize.py")

LOADER_DIR = os.path.join(_ROOT, "components", "earthsci_data")
LOADERS = {
    "mtbs_severity_loader.esm": "MTBS_severity",
    "nifc_perimeters_loader.esm": "NIFC_burned_fraction",
    "viirs_active_fire_loader.esm": "VIIRS_active_fire",
}

# The Camp-Fire-like analysis grid the fixture perimeters live on.
GRID = (-122.0, -121.2, 80, 39.6, 40.1, 50)  # lon0,lon1,n_lon,lat0,lat1,n_lat

# The loaders declare tz-aware temporal.start/end (ISO "…Z", matching the
# era5/openaq convention). The runtime compares the requested `time` against
# those bounds, so a consumer MUST pass a tz-AWARE datetime — a naive one
# raises "can't compare offset-naive and offset-aware datetimes" (framework
# finding F-3 in docs/observed-fire-loaders-framework-gaps.md).
_UTC = dt.timezone.utc


def _ok(msg: str) -> None:
    print(f"  [ OK ] {msg}")


def _fail(msg: str) -> None:
    print(f"  [FAIL] {msg}")


def _have(mod: str) -> bool:
    try:
        __import__(mod)
        return True
    except Exception:
        return False


def main() -> int:
    try:
        # phase-6 H-4: the data-loading tier is no longer re-exported at the
        # top level of `earthsci_ast` — it lives in `earthsci_ast.data_sources`
        # (the Python counterpart of Rust's `esio` feature and Julia's
        # EarthSciASTEarthSciIOExt). `load_path` is format-library surface and
        # stays where it was.
        from earthsci_ast import load_path
        from earthsci_ast.data_sources import (
            load_grid, load_points, load_static,
        )
    except Exception as e:  # pragma: no cover - environment guard
        print(f"FATAL: cannot import earthsci_ast ({e}). "
              f"Install the canonical ESS runner (see .github/workflows/test-esm.yml).")
        return 1

    import numpy as np

    failures = 0
    have_xr = _have("xarray") and _have("netCDF4")
    tmp = tempfile.mkdtemp(prefix="obsfire_feasibility_")

    # ------------------------------------------------------------------ #
    # [1] STRUCTURAL: every loader load_path()s through the canonical runner #
    #     (the same minimum-bar gate tools/run_esm_inline_tests.py runs). #
    # ------------------------------------------------------------------ #
    print("[1] structural load_path() — all three loaders resolve through the runner")
    parsed = {}
    for fname, dlname in LOADERS.items():
        path = os.path.join(LOADER_DIR, fname)
        try:
            m = load_path(path)
            dl = m.data_loaders[dlname]
            parsed[dlname] = dl
            _ok(f"{fname}: load_path() resolved (kind={dl.kind.value}, "
                f"vars={list(dl.variables)})")
        except Exception as e:
            failures += 1
            _fail(f"{fname}: load() raised {type(e).__name__}: {str(e).splitlines()[0][:160]}")

    # ------------------------------------------------------------------ #
    # [2] STATIC slice — mtbs_severity_loader via load_static             #
    # ------------------------------------------------------------------ #
    print("[2] STATIC modality — mtbs_severity_loader slices via load_static")
    dl = parsed.get("MTBS_severity")
    if dl is None:
        failures += 1
        _fail("MTBS loader did not parse; skipping slice")
    else:
        # Build a tiny static raster fixture (burn_severity + dnbr) and read it
        # back through the loader's declared file_variables.
        bs = np.array([[1, 2, 3], [4, 4, 2], [1, 0, 6]], dtype="float32")
        dn = bs * 100.0  # synthetic dNBR (×1000-scaled index in real MTBS)
        lon = np.array([-121.7, -121.6, -121.5], dtype="float32")
        lat = np.array([39.7, 39.8, 39.9], dtype="float32")
        if have_xr:
            import xarray as xr
            p = os.path.join(tmp, "mtbs_sample.nc")
            xr.Dataset(
                {"burn_severity": (("lat", "lon"), bs), "dnbr": (("lat", "lon"), dn)},
                coords={"lon": lon, "lat": lat},
            ).to_netcdf(p)
            opener = lambda url, _p=p: __import__("xarray").open_dataset(_p)
            backing = "xarray NetCDF read"
        else:
            opener = lambda url: {"burn_severity": bs, "dnbr": dn, "lon": lon, "lat": lat}
            backing = "in-memory mapping (xarray/netCDF4 absent)"
        try:
            res = load_static(dl, opener=opener, fire_id="sample",
                              bbox_west=-122.0, bbox_south=39.6, bbox_east=-121.2,
                              bbox_north=40.1, width=3, height=3)
            got = {k: np.asarray(v) for k, v in res.variables.items()}
            if "burn_severity_class" in got and "dnbr" in got:
                _ok(f"load_static returned burn_severity_class{tuple(got['burn_severity_class'].shape)} "
                    f"+ dnbr{tuple(got['dnbr'].shape)} via {backing}")
                if float(got["burn_severity_class"].max()) == 6.0:
                    _ok("burn_severity_class values mapped from file_variable 'burn_severity' (max class 6)")
                else:
                    failures += 1
                    _fail(f"burn_severity_class max {float(got['burn_severity_class'].max())} != 6")
            else:
                failures += 1
                _fail(f"load_static missing declared vars; got {list(got)}")
        except Exception as e:
            failures += 1
            _fail(f"load_static raised {type(e).__name__}: {str(e).splitlines()[0][:160]}")

    # ------------------------------------------------------------------ #
    # [3] GRID slice — nifc_perimeters_loader via load_grid               #
    #     (first run the rasterize leaf on the GeoJSON fixture)           #
    # ------------------------------------------------------------------ #
    print("[3] GRID modality — nifc rasterize leaf -> load_grid reads burned_fraction")
    dl = parsed.get("NIFC_burned_fraction")
    geojson = os.path.join(_FIX, "campfire_perimeters_sample.geojson")
    if dl is None:
        failures += 1
        _fail("NIFC loader did not parse; skipping slice")
    elif not have_xr:
        # No NetCDF stack: still exercise the grid slice contract in-memory.
        bf = np.linspace(0, 1, 12, dtype="float32").reshape(3, 4)
        lon = np.array([-121.7, -121.6, -121.5, -121.4], dtype="float32")
        lat = np.array([39.7, 39.8, 39.9], dtype="float32")
        opener = lambda url: {"burned_fraction": bf, "lon": lon, "lat": lat}
        try:
            res = load_grid(dl, time=dt.datetime(2018, 11, 10, tzinfo=_UTC), opener=opener,
                            fire_id="sample")
            bfo = np.asarray(res.variables["burned_fraction"])
            _ok(f"load_grid returned burned_fraction{tuple(bfo.shape)} "
                f"(in-memory; xarray/netCDF4 absent), url={res.urls_tried[0]}")
        except Exception as e:
            failures += 1
            _fail(f"load_grid raised {type(e).__name__}: {str(e).splitlines()[0][:160]}")
    else:
        import xarray as xr
        sys.path.insert(0, os.path.join(_ROOT, "tools", "leaves"))
        try:
            import nifc_perimeters_rasterize as leaf
            written = leaf.rasterize_all(geojson, os.path.join(tmp, "nifc"), GRID,
                                         mode="cumulative", supersample=8)
            _ok(f"rasterize leaf produced {len(written)} daily NetCDF(s)")
            # Read 2018-11-10 (the largest cumulative footprint) via the loader.
            day_file = os.path.join(tmp, "nifc", "burned_fraction_20181110.nc")
            opener = lambda url, _p=day_file: xr.open_dataset(_p)
            res = load_grid(dl, time=dt.datetime(2018, 11, 10, tzinfo=_UTC), opener=opener,
                            fire_id="sample")
            bf = np.asarray(res.variables["burned_fraction"])
            frac_burned = float((bf > 0).mean())
            if 0.0 < float(bf.max()) <= 1.0 and frac_burned > 0:
                _ok(f"load_grid sliced burned_fraction{tuple(bf.shape)} "
                    f"(max={float(bf.max()):.3f}, {frac_burned:.0%} cells>0) "
                    f"from url {res.urls_tried[0]}")
            else:
                failures += 1
                _fail(f"burned_fraction out of range or empty: max={float(bf.max())}")
        except Exception as e:
            failures += 1
            _fail(f"NIFC grid slice raised {type(e).__name__}: {str(e).splitlines()[0][:160]}")

    # ------------------------------------------------------------------ #
    # [4] POINTS slice — viirs_active_fire_loader via load_points         #
    # ------------------------------------------------------------------ #
    print("[4] POINTS modality — viirs_active_fire slices via load_points")
    dl = parsed.get("VIIRS_active_fire")
    csv_path = os.path.join(_FIX, "viirs_active_fire_sample.csv")
    if dl is None:
        failures += 1
        _fail("VIIRS loader did not parse; skipping slice")
    else:
        with open(csv_path, "rb") as f:
            csv_bytes = f.read()

        def fetcher(url, _b=csv_bytes):
            return _b

        def parser(body):
            text = body.decode() if isinstance(body, (bytes, bytearray)) else body
            rows = []
            for r in csv.DictReader(io.StringIO(text)):
                # Coerce numeric columns (the framework's column mapping does
                # NOT coerce string CSV cells — see framework-gaps report).
                for k in ("frp", "bright_ti4", "bright_ti5", "latitude", "longitude"):
                    if r.get(k):
                        r[k] = float(r[k])
                rows.append(r)
            return rows

        try:
            res = load_points(dl, time=dt.datetime(2018, 11, 8, tzinfo=_UTC),
                              fetcher=fetcher, parser=parser,
                              map_key="TEST_KEY", firms_source="VIIRS_SNPP_SP",
                              bbox_west=-122.0, bbox_south=39.6, bbox_east=-121.2,
                              bbox_north=40.1, day_range=1)
            v = res.variables
            if all(k in v for k in ("frp", "brightness", "confidence")):
                n = len(v["frp"])
                _ok(f"load_points returned {n} detections: "
                    f"frp={v['frp']}, brightness={v['brightness']}, confidence={v['confidence']}")
                # url carries the runtime-only MAP_KEY substitution.
                if "TEST_KEY" in res.urls_tried[0] and "VIIRS_SNPP_SP" in res.urls_tried[0]:
                    _ok(f"url_template resolved custom {{map_key}}/{{firms_source}}: {res.urls_tried[0]}")
                else:
                    failures += 1
                    _fail(f"url substitution drift: {res.urls_tried[0]}")
                # lon/lat/time available in raw records (not declared vars).
                if res.records and "latitude" in res.records[0] and "acq_time" in res.records[0]:
                    _ok("detection lon/lat/acq_date/acq_time present in raw records")
                else:
                    failures += 1
                    _fail("coordinate/time columns missing from records")
            else:
                failures += 1
                _fail(f"load_points missing declared vars; got {list(v)}")
        except Exception as e:
            failures += 1
            _fail(f"load_points raised {type(e).__name__}: {str(e).splitlines()[0][:160]}")

    print()
    if failures:
        print(f"RESULT: FAIL ({failures} check(s) failed)")
        return 1
    print("RESULT: PASS — all three observed-fire loaders load() + slice "
          "(static / grid / points) end-to-end through the canonical runner")
    return 0


if __name__ == "__main__":
    sys.exit(main())
