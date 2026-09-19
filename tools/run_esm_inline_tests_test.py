"""Unit tests for the Python inline-test gate (tools/run_esm_inline_tests.py).

The gate is thin — the toolkit owns §6.6 — so what is worth testing here is
the one thing the gate itself can get wrong: reading a worker that DIED as a
file with nothing to say. That is not a hypothetical. The gate imported a
private upstream module, the import raised inside every worker, each worker
died before emitting a row, and the parent printed ``[OK] (0 assertions)`` for
all 347 files: 22 assertions run over a corpus that declares 8,176, reported as
a pass.

Run: python -m unittest tools/run_esm_inline_tests_test.py
"""

from __future__ import annotations

import json
import sys
import unittest
from dataclasses import asdict
from pathlib import Path

# Importable both as `python -m unittest tools/..._test.py` from the repo root
# and as `python -m unittest ..._test` from `tools/` (mirrors the other tool
# test modules).
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import run_esm_inline_tests as gate  # noqa: E402

FIXTURES = HERE.parent / "test" / "fixtures" / "inline_tests"


def _line(**kw) -> str:
    row = gate.AssertionRow(
        file="f.esm", container_name="M", test_id="t", assertion_idx=1,
        variable="x", time=0.0, expected=1.0, actual=1.0, status="PASS",
        message="", duration_s=0.0,
    )
    return json.dumps({**asdict(row), **kw})


class WorkerOutputTest(unittest.TestCase):
    def test_rows_and_marker_are_taken_at_face_value(self):
        out = _line() + "\n" + _line(status="FAIL", message="off by one") + "\n__DONE__\n"
        rows = gate.rows_from_worker(Path("f.esm"), out, 1, "")
        self.assertEqual([r.status for r in rows], ["PASS", "FAIL"])

    def test_a_worker_that_never_finished_is_an_error_row(self):
        """No ``__DONE__``: whatever killed it is reported, not swallowed."""
        rows = gate.rows_from_worker(
            Path("f.esm"), "", 1, "ModuleNotFoundError: no module named ...")
        self.assertEqual([r.status for r in rows], ["ERROR"])
        self.assertIn("without emitting __DONE__", rows[0].message)
        self.assertIn("ModuleNotFoundError", rows[0].message)

    def test_rows_before_a_crash_are_kept_alongside_the_error_row(self):
        rows = gate.rows_from_worker(Path("f.esm"), _line() + "\n", -9, "Killed")
        self.assertEqual([r.status for r in rows], ["PASS", "ERROR"])

    def test_a_finished_worker_with_no_rows_is_not_an_error(self):
        """The marker is the difference: this worker ran and had nothing to
        report (the gate's own `<load>` row covers that case)."""
        rows = gate.rows_from_worker(Path("f.esm"), "__DONE__\n", 0, "")
        self.assertEqual(rows, [])

    def test_an_unexpected_exit_code_is_an_error_row_even_with_the_marker(self):
        rows = gate.rows_from_worker(Path("f.esm"), "__DONE__\n", -11, "SIGSEGV")
        self.assertEqual([r.status for r in rows], ["ERROR"])

    def test_noise_on_stdout_is_ignored(self):
        out = "RuntimeWarning: overflow\n" + _line() + "\n__DONE__\n"
        rows = gate.rows_from_worker(Path("f.esm"), out, 0, "")
        self.assertEqual([r.status for r in rows], ["PASS"])


class EndToEndFixtureTest(unittest.TestCase):
    """The gate against the two inline-test fixtures, through the real runner —
    the wiring the unit tests above deliberately do not touch."""

    def test_passing_fixture_passes(self):
        rows, rc, _ = gate.run_one_file(FIXTURES / "passing_decay.esm")
        self.assertTrue(rows, "no rows reported for a file with inline tests")
        self.assertTrue(all(r.status == "PASS" for r in rows), [r.message for r in rows])
        self.assertEqual(rc, 0)

    def test_failing_fixture_fails(self):
        rows, rc, _ = gate.run_one_file(FIXTURES / "failing_decay.esm")
        self.assertIn("FAIL", [r.status for r in rows])
        self.assertEqual(rc, 1)


if __name__ == "__main__":
    unittest.main()
