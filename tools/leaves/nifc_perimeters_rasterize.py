#!/usr/bin/env python3
"""tools/leaves/nifc_perimeters_rasterize.py  (campfire-e2e E1, bead esm-1zj)

Preprocessing LEAF: rasterize daily NIFC / GeoMAC wildfire-perimeter polygons
to a ``burned_fraction(lon, lat)`` grid, ONE NetCDF per day, feeding the pure-IO
``components/earthsci_data/nifc_perimeters_loader.esm`` (kind: grid) loader.

WHY THIS LEAF EXISTS
--------------------
The ESM ``DataLoader`` ``kind`` enum is ``grid`` / ``points`` / ``static`` /
``mesh`` — there is NO vector/polygon kind. Fire perimeters are time-varying
POLYGONS. Rather than add a new vector/feature loader primitive (against the
no-new-primitives principle, campfire-e2e plan §"Key design constraint"), we
rasterize the daily perimeters OFFLINE here — a one-time preprocessing step,
not an engine capability — to a burned-fraction grid that an ordinary
``kind: grid`` loader reads. This keeps every loader pure-IO and reuses the
existing grid machinery.

OUTPUT CONTRACT (what nifc_perimeters_loader.esm reads)
-------------------------------------------------------
For each day D in the perimeter set, writes ``<out_dir>/burned_fraction_<YYYYMMDD>.nc``
with:
  * dims   : ``lat`` (n_lat), ``lon`` (n_lon)
  * coords : ``lon`` (cell centers, degrees east), ``lat`` (cell centers,
             degrees north), ``time`` (scalar, the day, CF-encoded)
  * var    : ``burned_fraction(lat, lon)`` in [0, 1], units "1" — the per-cell
             fraction of cell area inside the day's fire perimeter union.
The loader's ``temporal`` is daily (file_period P1D, frequency P1D); a fire's
``burned_fraction(lon, lat, time)`` series is the stack of these daily files
(mirrors the era5_loader period-file model).

MODE
----
  * ``--mode cumulative`` (default): each day's grid is the union of ALL
    perimeters dated <= D — the monotonic non-decreasing burned-area growth
    curve (the modeled fire's footprint through that day). This is what the
    validation metric usually wants.
  * ``--mode daily``: each day's grid is the union of only that day's
    perimeters (new-front snapshot).

RASTERIZATION
-------------
Dependency-light: pure-numpy point-in-polygon SUPERSAMPLING (no shapely /
rasterio / GDAL). Each output cell is sampled on an SxS sub-lattice
(``--supersample``, default 8) and burned_fraction = (sub-points inside the
perimeter union) / S^2. Polygon interiors use the even-odd rule across all
rings, so holes (interior rings) are honored. shapely would give exact
cell-coverage areas; the supersampling estimate is sufficient for a
burned-fraction validation reference and keeps this leaf runnable anywhere
numpy + netCDF4 are installed.

INPUT
-----
A GeoJSON ``FeatureCollection`` of perimeter features. Each feature:
  * ``geometry``: ``Polygon`` or ``MultiPolygon`` (lon/lat / EPSG:4326 rings).
  * ``properties``: a date under one of ``date`` / ``DATE_CUR`` / ``CREATE_DATE``
    / ``perimeterdatetime`` / ``acq_date`` (ISO ``YYYY-MM-DD`` or a parseable
    ``YYYY-MM-DD*`` prefix). ``--date-field`` overrides the auto-detection.
NIFC Open Data / GeoMAC perimeter exports already match this shape; reproject
to EPSG:4326 first if your export is in a projected CRS.

USAGE
-----
    python tools/leaves/nifc_perimeters_rasterize.py \
        --perimeters campfire_perimeters.geojson \
        --out-dir /data/nifc_perimeters/ca3995712175620181108/ \
        --grid -122.0,-121.2,80,39.6,40.1,50 \
        --mode cumulative

``--grid`` is ``lon0,lon1,n_lon,lat0,lat1,n_lat`` (the analysis grid; default
should be the fire model's own domain grid — campfire-e2e plan §User-action).

This is a LEAF (offline preprocessing utility), not part of the ESM inline-test
gate or the engine. It has no .esm and is not auto-walked.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import sys
from typing import Dict, List, Sequence, Tuple

import numpy as np

# Property keys NIFC/GeoMAC perimeter exports use for the perimeter date.
_DATE_FIELDS = ("date", "DATE_CUR", "CREATE_DATE", "perimeterdatetime", "acq_date")

Ring = np.ndarray            # shape (k, 2): lon, lat
Polygon = List[Ring]         # exterior ring + optional interior (hole) rings


def _parse_date(raw: object) -> _dt.date:
    """Parse a perimeter date from a GeoJSON property value."""
    if raw is None:
        raise ValueError("perimeter feature has no date property")
    s = str(raw).strip()
    # Accept full ISO timestamps and epoch-millis (NIFC sometimes ships millis).
    if s.isdigit() and len(s) >= 12:
        return _dt.datetime.utcfromtimestamp(int(s) / 1000.0).date()
    s = s.replace("/", "-")
    return _dt.date.fromisoformat(s[:10])


def _feature_date(props: Dict, date_field: str | None) -> _dt.date:
    if date_field:
        return _parse_date(props.get(date_field))
    for f in _DATE_FIELDS:
        if props.get(f) not in (None, ""):
            return _parse_date(props[f])
    raise ValueError(
        f"no date property found (looked for {date_field or list(_DATE_FIELDS)})"
    )


def _iter_polygons(geom: Dict) -> List[Polygon]:
    """Normalize Polygon / MultiPolygon GeoJSON geometry to a list of polygons.

    Each polygon is a list of rings (exterior first, then holes); each ring is
    an (k, 2) float array of lon/lat.
    """
    t = geom.get("type")
    if t == "Polygon":
        raw_polys = [geom["coordinates"]]
    elif t == "MultiPolygon":
        raw_polys = geom["coordinates"]
    else:
        raise ValueError(f"unsupported geometry type {t!r} (need Polygon/MultiPolygon)")
    polys: List[Polygon] = []
    for rings in raw_polys:
        polys.append([np.asarray(r, dtype=float) for r in rings if len(r) >= 4])
    return polys


def _points_in_ring(px: np.ndarray, py: np.ndarray, ring: Ring) -> np.ndarray:
    """Vectorized crossing-number ray cast: is each (px,py) inside `ring`?

    Returns a boolean array (True = an odd number of edge crossings to the
    right of the point). `ring` is closed or open; the wrap edge is included.
    """
    x = ring[:, 0]
    y = ring[:, 1]
    n = len(ring)
    inside = np.zeros(px.shape, dtype=bool)
    j = n - 1
    for i in range(n):
        yi, yj = y[i], y[j]
        xi, xj = x[i], x[j]
        # Edge straddles the horizontal ray through py?
        cond = (yi > py) != (yj > py)
        # x-coordinate of the edge at height py (guard against yj==yi via cond mask).
        denom = np.where(yj != yi, yj - yi, 1.0)
        x_cross = xi + (py - yi) * (xj - xi) / denom
        inside ^= cond & (px < x_cross)
        j = i
    return inside


def _points_in_polygon(px: np.ndarray, py: np.ndarray, poly: Polygon) -> np.ndarray:
    """Even-odd test across all rings of one polygon (honors holes)."""
    acc = np.zeros(px.shape, dtype=bool)
    for ring in poly:
        acc ^= _points_in_ring(px, py, ring)
    return acc


def _grid_edges(lo: float, hi: float, n: int) -> Tuple[np.ndarray, np.ndarray]:
    """Return (edges[n+1], centers[n]) for a uniform 1-D axis."""
    edges = np.linspace(lo, hi, n + 1)
    centers = 0.5 * (edges[:-1] + edges[1:])
    return edges, centers


def rasterize_day(
    polys: Sequence[Polygon],
    lon0: float, lon1: float, n_lon: int,
    lat0: float, lat1: float, n_lat: int,
    supersample: int,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Rasterize a day's polygon union to burned_fraction(lat, lon) in [0,1].

    Supersamples each cell on an SxS sub-lattice and returns the fraction of
    sub-points inside ANY polygon. Returns (burned_fraction[n_lat,n_lon],
    lon_centers[n_lon], lat_centers[n_lat]).
    """
    _, lon_c = _grid_edges(lon0, lon1, n_lon)
    _, lat_c = _grid_edges(lat0, lat1, n_lat)
    S = max(1, int(supersample))
    # Sub-cell center offsets within a cell, in [0,1) -> (k+0.5)/S.
    dlon = (lon1 - lon0) / n_lon
    dlat = (lat1 - lat0) / n_lat
    sub = (np.arange(S) + 0.5) / S
    # Full supersampled lattice of points (n_lat*S, n_lon*S).
    sub_lon = (np.repeat(np.arange(n_lon), S) * dlon
               + np.tile(sub, n_lon) * dlon + lon0)
    sub_lat = (np.repeat(np.arange(n_lat), S) * dlat
               + np.tile(sub, n_lat) * dlat + lat0)
    PX, PY = np.meshgrid(sub_lon, sub_lat)   # (n_lat*S, n_lon*S)
    union = np.zeros(PX.shape, dtype=bool)
    for poly in polys:
        if poly:
            union |= _points_in_polygon(PX.ravel(), PY.ravel(), poly).reshape(PX.shape)
    # Average each SxS block -> burned fraction per output cell.
    frac = union.reshape(n_lat, S, n_lon, S).mean(axis=(1, 3))
    return frac.astype("float32"), lon_c, lat_c


def write_netcdf(
    path: str, burned_fraction: np.ndarray,
    lon_c: np.ndarray, lat_c: np.ndarray, day: _dt.date,
) -> None:
    """Write one daily burned_fraction NetCDF the loader can read."""
    import xarray as xr

    da = xr.DataArray(
        burned_fraction,
        dims=("lat", "lon"),
        coords={"lon": lon_c, "lat": lat_c,
                "time": np.datetime64(day.isoformat())},
        name="burned_fraction",
    )
    da.attrs.update(units="1", long_name="per-cell burned area fraction",
                    valid_min=0.0, valid_max=1.0)
    da["lon"].attrs.update(units="degrees_east", standard_name="longitude")
    da["lat"].attrs.update(units="degrees_north", standard_name="latitude")
    ds = da.to_dataset()
    ds.attrs.update(
        title="NIFC/GeoMAC daily fire perimeter, rasterized to burned fraction",
        source="tools/leaves/nifc_perimeters_rasterize.py (campfire-e2e E1, esm-1zj)",
        Conventions="CF-1.8",
    )
    ds.to_netcdf(path)


def load_features(geojson_path: str, date_field: str | None
                  ) -> List[Tuple[_dt.date, List[Polygon]]]:
    with open(geojson_path) as f:
        gj = json.load(f)
    feats = gj["features"] if gj.get("type") == "FeatureCollection" else [gj]
    out: List[Tuple[_dt.date, List[Polygon]]] = []
    for ft in feats:
        geom = ft.get("geometry")
        if not geom:
            continue
        day = _feature_date(ft.get("properties", {}), date_field)
        out.append((day, _iter_polygons(geom)))
    if not out:
        raise ValueError(f"{geojson_path}: no usable perimeter features")
    return out


def rasterize_all(
    geojson_path: str, out_dir: str, grid: Tuple[float, float, int, float, float, int],
    mode: str = "cumulative", supersample: int = 8, date_field: str | None = None,
) -> List[str]:
    """Rasterize every day in the perimeter set; return written file paths."""
    lon0, lon1, n_lon, lat0, lat1, n_lat = grid
    feats = load_features(geojson_path, date_field)
    days = sorted({d for d, _ in feats})
    os.makedirs(out_dir, exist_ok=True)
    written: List[str] = []
    for day in days:
        if mode == "cumulative":
            polys = [p for d, polys in feats if d <= day for p in polys]
        elif mode == "daily":
            polys = [p for d, polys in feats if d == day for p in polys]
        else:
            raise ValueError(f"unknown --mode {mode!r} (cumulative|daily)")
        frac, lon_c, lat_c = rasterize_day(
            polys, lon0, lon1, n_lon, lat0, lat1, n_lat, supersample)
        path = os.path.join(out_dir, f"burned_fraction_{day:%Y%m%d}.nc")
        write_netcdf(path, frac, lon_c, lat_c, day)
        written.append(path)
        print(f"  wrote {path}  (burned_fraction max={frac.max():.3f}, "
              f"mean={frac.mean():.4f})")
    return written


def _parse_grid(s: str) -> Tuple[float, float, int, float, float, int]:
    parts = s.split(",")
    if len(parts) != 6:
        raise argparse.ArgumentTypeError(
            "--grid must be lon0,lon1,n_lon,lat0,lat1,n_lat")
    lon0, lon1 = float(parts[0]), float(parts[1])
    n_lon = int(parts[2])
    lat0, lat1 = float(parts[3]), float(parts[4])
    n_lat = int(parts[5])
    return (lon0, lon1, n_lon, lat0, lat1, n_lat)


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--perimeters", required=True, help="input GeoJSON of perimeters")
    ap.add_argument("--out-dir", required=True, help="output dir for daily NetCDFs")
    ap.add_argument("--grid", required=True, type=_parse_grid,
                    help="analysis grid lon0,lon1,n_lon,lat0,lat1,n_lat")
    ap.add_argument("--mode", default="cumulative", choices=("cumulative", "daily"))
    ap.add_argument("--supersample", type=int, default=8,
                    help="SxS sub-samples per cell (default 8)")
    ap.add_argument("--date-field", default=None,
                    help="GeoJSON property holding the perimeter date "
                         "(default: auto-detect)")
    args = ap.parse_args(argv)
    written = rasterize_all(
        args.perimeters, args.out_dir, args.grid, args.mode,
        args.supersample, args.date_field)
    print(f"rasterized {len(written)} day(s) -> {args.out_dir} (mode={args.mode})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
