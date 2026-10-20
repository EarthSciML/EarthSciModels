"""The gridded meteorology models load, and all name temperature `T`.

ERA5's NetCDF short name for temperature is `t`, and a model regenerated from
upstream EarthSciData.jl declared a parameter by that name. `t` is the
document's independent variable, so esm-spec refused the file: era5.esm failed
to load on every gate run, and the error went unnoticed among the gate's other
failures. This test fails on its own, fast, if that comes back, and pins the
shared name that lets a coupling swap one met source for another.

Run: python -m unittest tools/met_data_names_test.py
"""

from __future__ import annotations

import unittest
from pathlib import Path

import earthsci_ast

DATA = Path(__file__).resolve().parent.parent / "components" / "earthsci_data"

MET_MODELS = {
    "era5.esm": "ERA5",
    "geosfp.esm": "GEOSFP",
    "ncep_ncar.esm": "NCEPNCARReanalysis",
    "wrf.esm": "WRF",
}


class MetDataNamesTest(unittest.TestCase):
    def test_met_models_load_and_expose_T(self):
        for file, model in MET_MODELS.items():
            with self.subTest(file=file):
                doc = earthsci_ast.load_path(str(DATA / file))
                variables = doc.models[model].variables
                self.assertIn("T", variables)
                self.assertNotIn("t", variables)


if __name__ == "__main__":
    unittest.main()
