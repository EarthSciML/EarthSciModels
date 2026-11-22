"""Write the synthetic GSWP3-shaped NetCDF files the CDEPS DATM data test reads.

CI never downloads forcing data. The data-reading test of
components/data_models/cdeps/cdeps_datm_gswp3_synthetic.esm instead reads small
files with the layout of the GSWP3v1 files on the NCAR CESM inputdata server
(NETCDF3 classic; FSDS / PRECTmms / TBOT,PSRF,QBOT,WIND,FLDS as
(time, lat, lon) float32; a `time` coordinate in days since the month start,
noleap calendar, 248 3-hourly records per month; the Solar records at
00,03,..,21Z and the Precip/TPQW records offset by 1.5 h; TOPO as a
(time=1, lat, lon) float64 static field). The values are closed-form functions
of the record index k and the cell indices (i, j), chosen exactly
representable in float32, so the test's expected values follow from the
formulas below with no file in git:

    FSDS     = 100 + 2 k + 50 i + 10 j                  [W/m2]
    PRECTmms = (1 + k + 8 i + 2 j) * 2**-20             [kg/m2/s]
    TBOT     = 270 + 0.25 k + 2 i + 0.5 j               [K]
    PSRF     = 90000 + 16 k + 1000 i + 100 j            [Pa]
    QBOT     = (2 + 0.0625 k + i + 0.25 j) * 2**-9      [kg/kg]
    WIND     = 3 + 0.125 k + i + 0.5 j                  [m/s]
    FLDS     = 250 + 0.5 k + 10 i + j                   [W/m2]
    TOPO     = 1000 + 100 i + 10 j                      [m]

k counts records from the first record of the month (0-based); every month
starts again at k = 0. The grid is NLAT x NLON = 4 x 5, so a reader that
selects the wrong cell or the wrong axis order returns a different number.

Run from the repository root (CI does this before the inline-test sweeps):

    python3 tools/gen_synthetic_gswp3.py

It writes components/data_models/cdeps/synthetic/ (git-ignored) and is
idempotent. Requires numpy and scipy.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from scipy.io import netcdf_file

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "components" / "data_models" / "cdeps" / "synthetic"

NLAT, NLON = 4, 5
RECORDS_PER_MONTH = 248  # 31 days x 8 records, as in the GSWP3 January files
MONTHS = ["2000-01"]  # the window the test runs in

FIELDS = {
    "FSDS": lambda k, i, j: 100 + 2 * k + 50 * i + 10 * j,
    "PRECTmms": lambda k, i, j: (1 + k + 8 * i + 2 * j) * 2.0**-20,
    "TBOT": lambda k, i, j: 270 + 0.25 * k + 2 * i + 0.5 * j,
    "PSRF": lambda k, i, j: 90000 + 16 * k + 1000 * i + 100 * j,
    "QBOT": lambda k, i, j: (2 + 0.0625 * k + i + 0.25 * j) * 2.0**-9,
    "WIND": lambda k, i, j: 3 + 0.125 * k + i + 0.5 * j,
    "FLDS": lambda k, i, j: 250 + 0.5 * k + 10 * i + j,
}

# file tag -> (first-record time [days after the month start], fields)
STREAMS = {
    "Solr": (0.0, ["FSDS"]),
    "Prec": (0.0625, ["PRECTmms"]),
    "TPQWL": (0.0625, ["PSRF", "TBOT", "WIND", "QBOT", "FLDS"]),
}


def field(fn, nrec):
    k, i, j = np.meshgrid(
        np.arange(nrec), np.arange(NLAT), np.arange(NLON), indexing="ij"
    )
    values = np.asarray(fn(k, i, j), dtype=np.float64)
    out = values.astype(np.float32)
    assert np.array_equal(out.astype(np.float64), values), "not float32-exact"
    return out


def write_stream(path: Path, month: str, offset: float, names: list[str]) -> None:
    with netcdf_file(path, "w", version=1) as f:
        f.createDimension("time", RECORDS_PER_MONTH)
        f.createDimension("lat", NLAT)
        f.createDimension("lon", NLON)
        t = f.createVariable("time", "f4", ("time",))
        t.units = f"days since {month}-01 00:00:00"
        t.calendar = "noleap"
        t[:] = offset + 0.125 * np.arange(RECORDS_PER_MONTH, dtype=np.float32)
        lat = f.createVariable("LATIXY", "f4", ("lat", "lon"))
        lat.units = "degrees_north"
        lat[:] = np.repeat(np.linspace(-45, 45, NLAT), NLON).reshape(NLAT, NLON)
        lon = f.createVariable("LONGXY", "f4", ("lat", "lon"))
        lon.units = "degrees_east"
        lon[:] = np.tile(np.linspace(0, 288, NLON), NLAT).reshape(NLAT, NLON)
        for name in names:
            v = f.createVariable(name, "f4", ("time", "lat", "lon"))
            v[:] = field(FIELDS[name], RECORDS_PER_MONTH)


def write_topo(path: Path) -> None:
    with netcdf_file(path, "w", version=1) as f:
        f.createDimension("time", 1)
        f.createDimension("lat", NLAT)
        f.createDimension("lon", NLON)
        t = f.createVariable("time", "f8", ("time",))
        t.units = "days since 0001-01-01 00:00:00"
        t.calendar = "noleap"
        t[:] = [0.0]
        v = f.createVariable("TOPO", "f8", ("time", "lat", "lon"))
        v.units = "m"
        i, j = np.meshgrid(np.arange(NLAT), np.arange(NLON), indexing="ij")
        v[:] = (1000.0 + 100.0 * i + 10.0 * j)[np.newaxis, :, :]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument("--out", type=Path, default=OUT, help="output directory")
    out = parser.parse_args().out
    out.mkdir(parents=True, exist_ok=True)
    for month in MONTHS:
        for tag, (offset, names) in STREAMS.items():
            write_stream(out / f"clmforc.GSWP3.synthetic.{tag}.{month}.nc", month, offset, names)
    write_topo(out / "topodata.synthetic.nc")
    print(f"wrote synthetic GSWP3 files to {out}")


if __name__ == "__main__":
    main()
