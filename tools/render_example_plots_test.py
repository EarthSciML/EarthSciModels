"""
Unit tests for tools/render_example_plots.py.

Run locally with: python3 -m unittest tools/render_example_plots_test.py
"""
from __future__ import annotations

import json
import math
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import render_example_plots as mod  # noqa: E402


class EvaluateTest(unittest.TestCase):
    def test_literal(self):
        self.assertEqual(mod.evaluate(3.5, {}), 3.5)
        self.assertEqual(mod.evaluate(7, {}), 7.0)

    def test_variable_lookup(self):
        self.assertEqual(mod.evaluate("x", {"x": 4.0}), 4.0)

    def test_unbound_variable_raises(self):
        with self.assertRaises(mod.UnsupportedExpression):
            mod.evaluate("missing", {})

    def test_arithmetic_ops(self):
        env = {"a": 2.0, "b": 3.0}
        self.assertAlmostEqual(mod.evaluate({"op": "+", "args": ["a", "b"]}, env), 5.0)
        self.assertAlmostEqual(mod.evaluate({"op": "-", "args": ["a", "b"]}, env), -1.0)
        self.assertAlmostEqual(mod.evaluate({"op": "*", "args": ["a", "b"]}, env), 6.0)
        self.assertAlmostEqual(
            mod.evaluate({"op": "/", "args": ["a", "b"]}, env), 2.0 / 3.0
        )
        self.assertAlmostEqual(mod.evaluate({"op": "^", "args": ["a", "b"]}, env), 8.0)

    def test_unary_minus(self):
        self.assertEqual(mod.evaluate({"op": "-", "args": ["a"]}, {"a": 5.0}), -5.0)

    def test_nary_plus_and_times(self):
        self.assertAlmostEqual(
            mod.evaluate({"op": "+", "args": [1, 2, 3, 4]}, {}), 10.0
        )
        self.assertAlmostEqual(
            mod.evaluate({"op": "*", "args": [2, 3, 4]}, {}), 24.0
        )

    def test_unary_funcs(self):
        self.assertAlmostEqual(
            mod.evaluate({"op": "exp", "args": [0]}, {}), 1.0
        )
        self.assertAlmostEqual(
            mod.evaluate({"op": "log10", "args": [100]}, {}), 2.0
        )
        self.assertAlmostEqual(
            mod.evaluate({"op": "sqrt", "args": [9]}, {}), 3.0
        )

    def test_unknown_op_raises(self):
        with self.assertRaises(mod.UnsupportedExpression):
            mod.evaluate({"op": "factorial", "args": [5]}, {})

    def test_evaluate_against_numpy_arrays(self):
        # Vectorized eval should broadcast naturally.
        env = {"x": np.array([1.0, 2.0, 4.0])}
        out = mod.evaluate({"op": "*", "args": ["x", 2]}, env)
        np.testing.assert_array_equal(out, np.array([2.0, 4.0, 8.0]))

    def test_cloud_albedo_gamma_matches_analytic(self):
        # γ = 2 / (√3 · (1 − g)) — at g=0.85 this is the Aerosol.jl pin.
        gamma_expr = {
            "op": "/",
            "args": [
                2,
                {
                    "op": "*",
                    "args": [
                        1.7320508075688772,
                        {
                            "op": "+",
                            "args": [
                                1,
                                {"op": "*", "args": [-1, "g"]},
                            ],
                        },
                    ],
                },
            ],
        }
        gamma = mod.evaluate(gamma_expr, {"g": 0.85})
        self.assertAlmostEqual(gamma, 7.698003589195009, places=10)


class IsAlgebraicOnlyTest(unittest.TestCase):
    def test_no_equations_with_observed_passes(self):
        component = {
            "variables": {
                "x": {"type": "parameter", "default": 1.0},
                "y": {"type": "observed", "expression": {"op": "*", "args": ["x", 2]}},
            },
            "equations": [],
        }
        self.assertTrue(mod._is_algebraic_only(component))

    def test_algebraic_equations_with_state_output_passes(self):
        # Mirrors water.esm: state outputs defined by algebraic equations
        # (no `D` op anywhere) — must be classified as algebraic-only so
        # the doc renderer evaluates the sweep.
        component = {
            "variables": {
                "T": {"type": "parameter", "default": 298.0},
                "K_w_298": {"type": "parameter", "default": 1e-8},
                "K_w": {"type": "state"},
            },
            "equations": [
                {
                    "lhs": "K_w",
                    "rhs": {"op": "*", "args": ["K_w_298", "T"]},
                }
            ],
        }
        self.assertTrue(mod._is_algebraic_only(component))

    def test_ode_equation_with_lhs_derivative_fails(self):
        # Mirrors diameter_growth.esm: D(D_p) ~ I_D — D op on the LHS
        # signals an ODE. Must be skipped (needs an integrator).
        component = {
            "variables": {
                "D_p": {"type": "state"},
                "I_D": {"type": "state"},
            },
            "equations": [
                {"lhs": {"op": "D", "wrt": "t", "args": ["D_p"]}, "rhs": "I_D"},
                {"lhs": "I_D", "rhs": {"op": "*", "args": [2, "D_p"]}},
            ],
        }
        self.assertFalse(mod._is_algebraic_only(component))

    def test_ode_equation_with_rhs_derivative_fails(self):
        # Defensive: a D op nested in the RHS also marks the system as
        # non-algebraic, even if no equation has D on the LHS.
        component = {
            "variables": {"y": {"type": "state"}},
            "equations": [
                {"lhs": "y", "rhs": {"op": "+", "args": [1, {"op": "D", "args": ["y"]}]}}
            ],
        }
        self.assertFalse(mod._is_algebraic_only(component))

    def test_non_empty_equations_without_observed_state_fails(self):
        # Algebraic equations are fine, but you still need at least one
        # observed/state variable to plot.
        component = {
            "variables": {"x": {"type": "parameter"}},
            "equations": [{"lhs": "y", "rhs": 1}],
        }
        self.assertFalse(mod._is_algebraic_only(component))

    def test_reaction_system_fails(self):
        component = {
            "species": {"O3": {"default": 40}},
            "reactions": [{"id": "R1"}],
        }
        self.assertFalse(mod._is_algebraic_only(component))

    def test_no_observed_or_state_fails(self):
        component = {
            "variables": {"x": {"type": "parameter", "default": 1.0}},
            "equations": [],
        }
        self.assertFalse(mod._is_algebraic_only(component))


class HasTimeDerivativeTest(unittest.TestCase):
    def test_direct_d_op(self):
        self.assertTrue(mod._has_time_derivative({"op": "D", "args": ["x"]}))

    def test_nested_d_op(self):
        node = {"op": "+", "args": [1, {"op": "*", "args": [2, {"op": "D", "args": ["y"]}]}]}
        self.assertTrue(mod._has_time_derivative(node))

    def test_no_d_op(self):
        self.assertFalse(mod._has_time_derivative({"op": "*", "args": ["x", 2]}))

    def test_scalar_or_string(self):
        self.assertFalse(mod._has_time_derivative(3.14))
        self.assertFalse(mod._has_time_derivative("x"))
        self.assertFalse(mod._has_time_derivative(None))


class BuildSweepGridTest(unittest.TestCase):
    def test_linear_1d(self):
        spec = {
            "type": "cartesian",
            "dimensions": [
                {"parameter": "x", "range": {"start": 0.0, "stop": 1.0, "count": 5}}
            ],
        }
        names, values = mod._build_sweep_grid(spec)
        self.assertEqual(names, ["x"])
        np.testing.assert_array_almost_equal(
            values[0], np.linspace(0.0, 1.0, 5)
        )

    def test_log_scale(self):
        spec = {
            "type": "cartesian",
            "dimensions": [
                {
                    "parameter": "x",
                    "range": {
                        "start": 0.01,
                        "stop": 100.0,
                        "count": 5,
                        "scale": "log",
                    },
                }
            ],
        }
        _, values = mod._build_sweep_grid(spec)
        np.testing.assert_array_almost_equal(
            values[0], np.logspace(math.log10(0.01), math.log10(100.0), 5)
        )

    def test_2d_cartesian(self):
        spec = {
            "type": "cartesian",
            "dimensions": [
                {"parameter": "x", "range": {"start": 0.0, "stop": 1.0, "count": 3}},
                {"parameter": "y", "range": {"start": 0.0, "stop": 2.0, "count": 4}},
            ],
        }
        names, values = mod._build_sweep_grid(spec)
        self.assertEqual(names, ["x", "y"])
        self.assertEqual(values[0].shape, (3,))
        self.assertEqual(values[1].shape, (4,))

    def test_unsupported_type_raises(self):
        with self.assertRaises(mod.UnsupportedExpression):
            mod._build_sweep_grid({"type": "latin_hypercube", "dimensions": []})


class IntegrationTest(unittest.TestCase):
    """Render plots from a tiny synthetic .esm and verify outputs."""

    def _write_esm(self, root: Path) -> Path:
        body = {
            "esm": "0.1.0",
            "metadata": {"name": "Toy"},
            "models": {
                "Toy": {
                    "description": "A toy algebraic model.",
                    "variables": {
                        "x": {"type": "parameter", "default": 1.0},
                        "y": {
                            "type": "observed",
                            "expression": {"op": "*", "args": ["x", 2]},
                        },
                    },
                    "equations": [],
                    "examples": [
                        {
                            "id": "y_vs_x",
                            "description": "y over x",
                            "parameter_sweep": {
                                "type": "cartesian",
                                "dimensions": [
                                    {
                                        "parameter": "x",
                                        "range": {
                                            "start": 0.0,
                                            "stop": 1.0,
                                            "count": 10,
                                        },
                                    }
                                ],
                            },
                            "plots": [
                                {
                                    "id": "line",
                                    "type": "line",
                                    "x": {"variable": "x", "label": "x"},
                                    "y": {"variable": "y", "label": "y"},
                                    "description": "y = 2x",
                                }
                            ],
                        }
                    ],
                }
            },
        }
        path = root / "components" / "toy" / "toy.esm"
        path.parent.mkdir(parents=True)
        path.write_text(json.dumps(body), encoding="utf-8")
        return path

    def test_run_emits_plot_in_expected_path(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            self._write_esm(root)
            rc = mod.run(root / "components")
            self.assertEqual(rc, 0)
            png = (
                root
                / "components"
                / "toy"
                / "toy.plots"
                / "y_vs_x-line.png"
            )
            self.assertTrue(png.is_file(), f"expected {png} to exist")
            # Sanity: PNG magic bytes.
            self.assertEqual(png.read_bytes()[:8], b"\x89PNG\r\n\x1a\n")

    def test_skips_examples_without_sweep(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            body = {
                "esm": "0.1.0",
                "models": {
                    "T": {
                        "variables": {
                            "x": {"type": "parameter", "default": 1.0},
                            "y": {
                                "type": "observed",
                                "expression": {"op": "*", "args": ["x", 2]},
                            },
                        },
                        "equations": [],
                        "examples": [
                            {
                                "id": "no_sweep",
                                "plots": [
                                    {
                                        "id": "p",
                                        "type": "line",
                                        "x": {"variable": "x"},
                                        "y": {"variable": "y"},
                                    }
                                ],
                            }
                        ],
                    }
                },
            }
            path = root / "components" / "t" / "t.esm"
            path.parent.mkdir(parents=True)
            path.write_text(json.dumps(body))
            rc = mod.run(root / "components")
            self.assertEqual(rc, 0)
            self.assertFalse((root / "components" / "t" / "t.plots").exists())


if __name__ == "__main__":
    unittest.main()
