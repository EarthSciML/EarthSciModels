#!/usr/bin/env python3
"""tools/run_esm_inline_tests.py  (mdl-w1j, lib/ extension mdl-14s)

Python inline-test gate for the EarthSciModels rig.

Walks ``components/**/*.esm`` and ``lib/**/*.esm`` (both default roots) and
runs every inline test (``Model.tests`` / ``ReactionSystem.tests`` per ESM
spec §6.6) through the canonical ESS Python runner
``earthsci_toolkit.simulation.simulate``. For each ``(time, variable,
expected[, tolerance])`` assertion, samples the ``SimulationResult``
trajectory at the requested time and compares to the declared expected
value with the spec §6.6.4 tolerance precedence (assertion > test >
container > default rel=1e-6).

Minimum-bar gate (mdl-14s): a discovered .esm with no inline tests still
counts as a checked file — the worker calls ``earthsci_toolkit.load`` on
it and emits a synthetic ``<load>`` PASS row. A load failure emits an
ERROR row and fails the gate. This catches structural-validation drift
on lib/ files (e.g. lib/solar.esm) at PR time, which is the class of bug
that motivated the extension (see closed beads mdl-pk3, mdl-97r).

Single-pathway rule (CLAUDE.md "Simulation Pathway — ABSOLUTE Rule"):
this driver invokes ``earthsci_toolkit.simulation.simulate`` as the
**official ESS Python runner** — no homebrew lambdify+solve_ivp, no
parallel evaluator. The cse=False knob is requested via the public
``cse: bool`` kwarg on ``simulate`` (esm-5gk, ESS audit follow-up
mdl-167); the runner handles compile-cache population internally.

CSE per-file override (esm-wqy1): cse=False is the default — the
original audit concern (mdl-167, mirrored in
``tools/render_example_plots.py`` near ``_RSS_HARD_ABORT_GB``) was
defensive against ``sympy.lambdify(..., cse=True)``'s memory cliff
on very large reaction systems. The cse=False path runs through
``earthsci_toolkit.sympy_bridge._flat_to_sympy_rhs``'s topological
algebraic-state substitution loop, which has the opposite cliff:
models with many cross-referenced algebraic states explode in
compile time (>30 min on a single file vs <30s under cse=True).
``CSE_TRUE_OVERRIDE_FILENAMES`` below names .esm basenames that
opt into cse=True to dodge the substitution-loop cliff. Numerical
equivalence cse=True ↔ cse=False at IEEE-754 ULP scale was verified
in esm-wqy1 across a sample of stratospheric / radical-pool .esm
files (mismatches confined to numerically-zero values below the
``atol=1e-12`` integrator floor; non-zero values match within the
spec §6.6.4 default ``rel=1e-6`` tolerance). esm-kpo6 (upstream ESS
sympy_bridge perf fix) is the long-term path that would let the
override allowlist stay empty.

OOM guardrails (per bead mdl-w1j scope):
  * Each .esm is processed in its own subprocess via
    ``--worker <path>`` so Python's per-process GC structurally
    prevents cross-file accumulation, even if a future runner change
    reintroduces growth across simulate() calls.
  * Each subprocess sets ``RLIMIT_AS = 6 GiB`` (hard) so a runaway
    compile aborts cleanly instead of OOM-killing the CI runner.
  * Worker count = 1 (no parallel test execution); the parent walker
    spawns one subprocess at a time.

Cross-rig dependency (mdl-79g substrate-detection heuristic, ESS):
  Until the heuristic-removal series lands on EarthSciSerialization
  main, the geoschem_fullchem mechanism's RHS divides by SO2/SALAAL/
  SALCAL whose default initial values are 0 (denominators of 0 →
  non-finite RHS). Workaround: seed those species to a small positive
  ppb-scale value via the ``initial_conditions`` kwarg of simulate().
  Remove the seed (the ``_DENOM_SEED_PPB`` block below) once
  EarthSciSerialization main contains a commit referencing the
  substrate-detection heuristic drop.

Exit codes:
  0  every assertion passed
  1  at least one assertion failed or errored
  2  internal driver failure (parse error, etc.)
"""

from __future__ import annotations

import argparse
import json
import resource
import subprocess
import sys
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DEFAULT_ROOTS = ["components", "lib"]
DEFAULT_REL_TOL = 1e-6

# Per-subprocess hard memory ceiling. 6 GiB leaves headroom on the 16 GiB
# ubuntu-latest CI runner even if multiple processes are alive (parent +
# worker), and matches the budget called out in the bead mdl-w1j scope.
WORKER_RLIMIT_BYTES = 6 * 1024 * 1024 * 1024

# Initial-condition seed for SO2/SALAAL/SALCAL (mdl-79g workaround).
# A few ppb is far below any plausible boundary value and large enough
# to keep the heuristic-introduced denominators away from 0 during the
# integrator's first RHS evaluation. Remove this block once mdl-79g
# (substrate-detection heuristic drop) has landed on ESS main.
DENOM_SEED_PPB: Dict[str, float] = {
    "SO2": 1.0e-3,
    "SALAAL": 1.0e-3,
    "SALCAL": 1.0e-3,
}

# Per-file CSE override (esm-wqy1). .esm basenames listed here will be
# simulated with cse=True instead of the cse=False default. Entry
# criteria: cse=False compile time exceeds ~10 min wall on a single
# file (CI's 25-min walk-cap leaves no slack for one file to consume
# the whole budget), AND cse=True correctness has been verified
# against either a parallel forward evaluator or the file's existing
# reference data within the spec §6.6.4 declared tolerances. See the
# module docstring for the audit decision and esm-kpo6 for the
# long-term substitution-loop perf fix.
CSE_TRUE_OVERRIDE_FILENAMES: frozenset = frozenset({
    # heat_momentum_fluxes.esm (esm-0ro4): 78 algebraic states with
    # cross-referenced ψ_m/ψ_h piecewise calls feeding through
    # r_ah/r_aw/T_ac/q_ac/dH_*_dT produce ~419K substituted ops
    # post-flatten; cse=False compile >30 min, cse=True ~29s. ULP
    # correctness verified against a parallel Python forward
    # evaluator (rel ≤ 5e-15) before listing here.
    "heat_momentum_fluxes.esm",
})


def _cse_for_file(file_path: str) -> bool:
    """Return the ``cse`` kwarg value for ``simulate()`` on the given
    .esm. cse=False is the default; basenames listed in
    ``CSE_TRUE_OVERRIDE_FILENAMES`` opt into cse=True (see esm-wqy1)."""
    return Path(file_path).name in CSE_TRUE_OVERRIDE_FILENAMES

# Variables we may need to identify by their bare name in the simulate()
# output where ``vars`` is dot-namespaced (e.g. ``"SuperFast.O3"``).


# ---------------------------------------------------------------------------
# Result types (parent-side)
# ---------------------------------------------------------------------------


@dataclass
class AssertionRow:
    file: str
    container_kind: str  # "model" | "reaction_system"
    container_name: str
    test_id: str
    assertion_idx: int
    variable: str
    time: float
    expected: float
    actual: Optional[float]
    status: str          # "PASS" | "FAIL" | "ERROR"
    message: str
    duration_s: float


# ---------------------------------------------------------------------------
# Worker
# ---------------------------------------------------------------------------


def _set_memory_limit(nbytes: int) -> None:
    soft, _hard = resource.getrlimit(resource.RLIMIT_AS)
    target = nbytes
    if soft != resource.RLIM_INFINITY and soft < target:
        target = soft
    try:
        resource.setrlimit(resource.RLIMIT_AS, (target, target))
    except (ValueError, OSError):
        # Non-Linux or restricted; skip rather than abort the driver.
        pass


def _resolve_var_index(
    var_spec: str, sim_vars: List[str], container_name: str
) -> Optional[int]:
    """Map an ESM variable spec ("O3", "Sub.x", etc.) to a sim_vars index."""
    if var_spec in sim_vars:
        return sim_vars.index(var_spec)
    qualified = f"{container_name}.{var_spec}"
    if qualified in sim_vars:
        return sim_vars.index(qualified)
    bare = var_spec.rsplit(".", 1)[-1]
    matches = [
        i for i, v in enumerate(sim_vars)
        if v == bare or v.endswith("." + bare)
    ]
    if len(matches) == 1:
        return matches[0]
    return None


def _resolve_tolerance(
    container_tol, test_tol, assertion_tol
) -> Tuple[float, float]:
    """ESM spec §6.6.4: most-specific declared tolerance wins."""
    for cand in (assertion_tol, test_tol, container_tol):
        if cand is None:
            continue
        rel = cand.rel if cand.rel is not None else 0.0
        atol = cand.abs if cand.abs is not None else 0.0
        return float(rel), float(atol)
    return DEFAULT_REL_TOL, 0.0


def _check(actual: float, expected: float, rtol: float, atol: float) -> bool:
    if rtol == 0.0 and atol == 0.0:
        return actual == expected
    return abs(actual - expected) <= atol + rtol * abs(expected)


def _seed_denom_ic(
    initial_conditions: Dict[str, float],
    flat,
    container_name: str,
) -> Dict[str, float]:
    """Apply the mdl-79g denominator-seed workaround.

    Adds ``DENOM_SEED_PPB`` entries for any state variable whose bare
    name matches and that is not already overridden by the test. Uses
    the dot-namespaced state name from ``flat`` so simulate() resolves
    it deterministically.
    """
    out = dict(initial_conditions)
    state_names = list(flat.state_variables.keys()) if hasattr(
        flat, "state_variables"
    ) else [n for n in getattr(flat, "_state_names", [])]
    if not state_names:
        # Best-effort: pull from the compile cache we just built.
        cache = getattr(flat, "_simulate_compile_cache", None)
        if cache is not None:
            state_names = list(cache.state_names)
    for state_name in state_names:
        bare = state_name.rsplit(".", 1)[-1]
        if bare not in DENOM_SEED_PPB:
            continue
        # Don't clobber a test-supplied IC.
        if state_name in out or bare in out:
            continue
        out[state_name] = DENOM_SEED_PPB[bare]
    return out


def _run_tests_for_container(
    file_path: str,
    container_kind: str,
    container_name: str,
    container_tolerance,
    tests,
    flat,
    rows: List[AssertionRow],
) -> None:
    if not tests:
        return
    from earthsci_toolkit import simulate
    import numpy as np

    sim_vars: List[str] = []
    cse_flag = _cse_for_file(file_path)
    for t in tests:
        t_start = time.time()
        try:
            ic = dict(t.initial_conditions or {})
            ic = _seed_denom_ic(ic, flat, container_name)
            params = dict(t.parameter_overrides or {})
            res = simulate(
                flat,
                tspan=(t.time_span.start, t.time_span.end),
                parameters=params,
                initial_conditions=ic,
                rtol=1e-10,
                atol=1e-12,
                cse=cse_flag,
            )
        except Exception as err:  # noqa: BLE001
            for i, a in enumerate(t.assertions):
                rows.append(AssertionRow(
                    file=file_path,
                    container_kind=container_kind,
                    container_name=container_name,
                    test_id=t.id,
                    assertion_idx=i,
                    variable=a.variable,
                    time=a.time,
                    expected=a.expected,
                    actual=None,
                    status="ERROR",
                    message=f"simulate() raised: {type(err).__name__}: {err}",
                    duration_s=time.time() - t_start,
                ))
            continue

        if not res.success:
            for i, a in enumerate(t.assertions):
                rows.append(AssertionRow(
                    file=file_path,
                    container_kind=container_kind,
                    container_name=container_name,
                    test_id=t.id,
                    assertion_idx=i,
                    variable=a.variable,
                    time=a.time,
                    expected=a.expected,
                    actual=None,
                    status="ERROR",
                    message=f"integrator failed: {res.message}",
                    duration_s=time.time() - t_start,
                ))
            continue

        sim_vars = res.vars
        for i, a in enumerate(t.assertions):
            rtol, atol = _resolve_tolerance(
                container_tolerance, t.tolerance, a.tolerance
            )
            idx = _resolve_var_index(a.variable, sim_vars, container_name)
            if idx is None:
                rows.append(AssertionRow(
                    file=file_path,
                    container_kind=container_kind,
                    container_name=container_name,
                    test_id=t.id,
                    assertion_idx=i,
                    variable=a.variable,
                    time=a.time,
                    expected=a.expected,
                    actual=None,
                    status="ERROR",
                    message=(
                        f"variable not found in simulate() output "
                        f"(have {len(sim_vars)} vars; sample: "
                        f"{sim_vars[:3]})"
                    ),
                    duration_s=time.time() - t_start,
                ))
                continue
            try:
                actual = float(np.interp(a.time, res.t, res.y[idx]))
            except Exception as err:  # noqa: BLE001
                rows.append(AssertionRow(
                    file=file_path,
                    container_kind=container_kind,
                    container_name=container_name,
                    test_id=t.id,
                    assertion_idx=i,
                    variable=a.variable,
                    time=a.time,
                    expected=a.expected,
                    actual=None,
                    status="ERROR",
                    message=f"sample failed: {err}",
                    duration_s=time.time() - t_start,
                ))
                continue
            ok = _check(actual, a.expected, rtol, atol)
            rows.append(AssertionRow(
                file=file_path,
                container_kind=container_kind,
                container_name=container_name,
                test_id=t.id,
                assertion_idx=i,
                variable=a.variable,
                time=a.time,
                expected=a.expected,
                actual=actual,
                status="PASS" if ok else "FAIL",
                message="" if ok else (
                    f"actual={actual!r} expected={a.expected!r} "
                    f"(rtol={rtol}, atol={atol})"
                ),
                duration_s=time.time() - t_start,
            ))


def run_worker(file_path: str) -> int:
    _set_memory_limit(WORKER_RLIMIT_BYTES)

    from earthsci_toolkit import flatten, load

    rows: List[AssertionRow] = []
    try:
        ef = load(file_path)
    except Exception as err:  # noqa: BLE001
        rows.append(AssertionRow(
            file=file_path, container_kind="file", container_name="<load>",
            test_id="<load>", assertion_idx=0, variable="", time=0.0,
            expected=0.0, actual=None, status="ERROR",
            message=f"load failed: {type(err).__name__}: {err}",
            duration_s=0.0,
        ))
        _emit_worker_results(rows)
        return 1

    # Containers worth processing.
    containers: List[Tuple[str, str, object, list]] = []
    if ef.models:
        for mname, m in ef.models.items():
            if m.tests:
                containers.append(("model", mname, m.tolerance, m.tests))
    if ef.reaction_systems:
        for rname, rs in ef.reaction_systems.items():
            if rs.tests:
                containers.append((
                    "reaction_system", rname, rs.tolerance, rs.tests,
                ))

    if not containers:
        # mdl-14s: minimum-bar gate. With no inline tests, the load() call
        # above is the only structural check. Emit a synthetic PASS row so
        # the parent summary shows the file was actually verified, not
        # silently skipped.
        rows.append(AssertionRow(
            file=file_path, container_kind="file", container_name="<load>",
            test_id="<load>", assertion_idx=0, variable="", time=0.0,
            expected=0.0, actual=None, status="PASS",
            message="load() succeeded (no inline tests declared)",
            duration_s=0.0,
        ))
        _emit_worker_results(rows)
        return 0

    try:
        flat = flatten(ef)
    except Exception as err:  # noqa: BLE001
        for kind, name, _tol, tests in containers:
            for t in tests:
                for i, a in enumerate(t.assertions):
                    rows.append(AssertionRow(
                        file=file_path, container_kind=kind,
                        container_name=name, test_id=t.id,
                        assertion_idx=i, variable=a.variable, time=a.time,
                        expected=a.expected, actual=None, status="ERROR",
                        message=f"flatten failed: {type(err).__name__}: {err}",
                        duration_s=0.0,
                    ))
        _emit_worker_results(rows)
        return 1

    for kind, name, tol, tests in containers:
        _run_tests_for_container(
            file_path, kind, name, tol, tests, flat, rows,
        )

    _emit_worker_results(rows)
    n_bad = sum(1 for r in rows if r.status in ("FAIL", "ERROR"))
    return 1 if n_bad else 0


def _emit_worker_results(rows: List[AssertionRow]) -> None:
    """Worker writes one JSON object per assertion to stdout, then a final
    ``__DONE__`` marker. Parent reads only lines starting with ``{`` so
    incidental Python warnings on stderr don't pollute the parser."""
    for r in rows:
        sys.stdout.write(json.dumps(asdict(r)) + "\n")
    sys.stdout.write("__DONE__\n")
    sys.stdout.flush()


# ---------------------------------------------------------------------------
# Parent (driver)
# ---------------------------------------------------------------------------


def discover_esm_files(roots: List[str]) -> List[Path]:
    found: List[Path] = []
    repo_root = Path(__file__).resolve().parent.parent
    for r in roots:
        p = Path(r)
        if not p.is_absolute():
            p = repo_root / p
        if not p.is_dir():
            continue
        for path in sorted(p.rglob("*.esm")):
            found.append(path)
    return sorted(found)


def run_one_file(file_path: Path) -> Tuple[List[AssertionRow], int, str]:
    """Spawn the worker subprocess for one .esm file. Returns
    (rows, exit_code, raw_stderr)."""
    cmd = [
        sys.executable,
        "-X", "faulthandler",
        str(Path(__file__).resolve()),
        "--worker", str(file_path),
    ]
    proc = subprocess.run(
        cmd, capture_output=True, text=True, check=False,
    )
    rows: List[AssertionRow] = []
    for line in proc.stdout.splitlines():
        line = line.strip()
        if not line or not line.startswith("{"):
            continue
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        rows.append(AssertionRow(**d))
    if proc.returncode == 0 and not any(
        line.strip() == "__DONE__" for line in proc.stdout.splitlines()
    ):
        # Worker exited 0 but did not emit the done marker → treat as
        # internal failure (likely OOM kill or rlimit).
        rows.append(AssertionRow(
            file=str(file_path), container_kind="file",
            container_name="<worker>", test_id="<spawn>",
            assertion_idx=0, variable="", time=0.0, expected=0.0,
            actual=None, status="ERROR",
            message="worker exited without emitting __DONE__",
            duration_s=0.0,
        ))
    if proc.returncode not in (0, 1):
        # Crash, OOM kill, rlimit, etc.
        rows.append(AssertionRow(
            file=str(file_path), container_kind="file",
            container_name="<worker>", test_id="<spawn>",
            assertion_idx=0, variable="", time=0.0, expected=0.0,
            actual=None, status="ERROR",
            message=(
                f"worker exited rc={proc.returncode}; "
                f"stderr_tail={proc.stderr[-500:]!r}"
            ),
            duration_s=0.0,
        ))
    return rows, proc.returncode, proc.stderr


def _print_summary(all_rows: List[AssertionRow], files: List[Path]) -> None:
    by_file: Dict[str, List[AssertionRow]] = {}
    for r in all_rows:
        by_file.setdefault(r.file, []).append(r)

    print("\n=========== ESM Python inline-test summary ===========")
    print(f"Files discovered: {len(files)}")
    print(f"Assertions:       {len(all_rows)}")

    pass_n = sum(1 for r in all_rows if r.status == "PASS")
    fail_n = sum(1 for r in all_rows if r.status == "FAIL")
    err_n = sum(1 for r in all_rows if r.status == "ERROR")
    print(f"  PASS:  {pass_n}")
    print(f"  FAIL:  {fail_n}")
    print(f"  ERROR: {err_n}")

    print("\nPer-file:")
    for f in files:
        rs = by_file.get(str(f), [])
        if not rs:
            print(f"  {f}: (no inline tests)")
            continue
        p = sum(1 for r in rs if r.status == "PASS")
        fa = sum(1 for r in rs if r.status == "FAIL")
        e = sum(1 for r in rs if r.status == "ERROR")
        ok = "OK " if (fa == 0 and e == 0) else "FAIL"
        print(f"  [{ok}] {f}: {p}P / {fa}F / {e}E")

    if fail_n or err_n:
        print("\nFailures / errors (first 50):")
        shown = 0
        for r in all_rows:
            if r.status == "PASS" or shown >= 50:
                continue
            print(
                f"  - [{r.status}] {r.file}::{r.container_name}::"
                f"{r.test_id}#{r.assertion_idx} "
                f"({r.variable}@{r.time}): {r.message}"
            )
            shown += 1


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--worker",
        help="Internal: run a single .esm file in worker mode "
             "(emits JSON results to stdout).",
    )
    ap.add_argument(
        "--root", action="append", default=None,
        help="Root directory to search for .esm files. May be passed "
             "multiple times. Defaults to ./components and ./lib "
             "(mdl-14s: lib/ included so structural-validation drift in "
             "lib/*.esm is caught at PR time). Mutually exclusive with --files.",
    )
    ap.add_argument(
        "--files", nargs="+", default=None,
        help="Explicit list of .esm files to test (instead of walking --root "
             "directories). Useful for pre-merge gates that only want to test "
             "files changed in the diff. Mutually exclusive with --root.",
    )
    ap.add_argument(
        "--junit-xml", default=None,
        help="If set, also emit a junit-compatible XML report at this path.",
    )
    args = ap.parse_args(argv)

    if args.worker:
        return run_worker(args.worker)

    if args.files and args.root:
        ap.error("--files and --root are mutually exclusive")

    if args.files:
        repo_root = Path(__file__).resolve().parent.parent
        files: List[Path] = []
        for f in args.files:
            p = Path(f)
            if not p.is_absolute():
                p = repo_root / p
            if not p.exists():
                print(f"ERROR: --files: not found: {p}", file=sys.stderr)
                return 2
            if p.suffix != ".esm":
                print(f"ERROR: --files: not a .esm file: {p}", file=sys.stderr)
                return 2
            files.append(p.resolve())
        files = sorted(set(files))
        if not files:
            print("No .esm files passed via --files.", file=sys.stderr)
            return 0
    else:
        roots = args.root or DEFAULT_ROOTS
        files = discover_esm_files(roots)
        if not files:
            print(
                f"No .esm files discovered under: {', '.join(roots)}",
                file=sys.stderr,
            )
            return 0

    print(f"Walking {len(files)} .esm file(s) ...")
    all_rows: List[AssertionRow] = []
    overall_rc = 0
    t_total = time.time()
    for f in files:
        t0 = time.time()
        rows, rc, stderr = run_one_file(f)
        all_rows.extend(rows)
        bad = sum(1 for r in rows if r.status in ("FAIL", "ERROR"))
        tag = "OK " if bad == 0 else "FAIL"
        print(
            f"  [{tag}] {f}  ({len(rows)} assertions, "
            f"{time.time() - t0:.1f}s)"
        )
        if rc not in (0, 1):
            overall_rc = max(overall_rc, 2)
            print(f"    worker stderr tail:\n{stderr[-400:]}", file=sys.stderr)
        elif rc == 1 and overall_rc == 0:
            overall_rc = 1
        elif bad and overall_rc == 0:
            overall_rc = 1

    _print_summary(all_rows, files)
    print(f"Total wall: {time.time() - t_total:.1f}s")

    if args.junit_xml:
        _write_junit_xml(all_rows, args.junit_xml)

    return overall_rc


def _write_junit_xml(rows: List[AssertionRow], path: str) -> None:
    """Minimal junit XML — one <testsuite> per file, one <testcase> per
    assertion. Keeps the CI-side artifact symmetric with the existing
    Julia junit emitter (mdl-08t)."""
    from xml.sax.saxutils import escape
    by_file: Dict[str, List[AssertionRow]] = {}
    for r in rows:
        by_file.setdefault(r.file, []).append(r)
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', "<testsuites>"]
    for f, rs in by_file.items():
        n = len(rs)
        nf = sum(1 for r in rs if r.status == "FAIL")
        ne = sum(1 for r in rs if r.status == "ERROR")
        lines.append(
            f'  <testsuite name="{escape(f)}" tests="{n}" '
            f'failures="{nf}" errors="{ne}">'
        )
        for r in rs:
            tname = (
                f"{r.container_name}::{r.test_id}#{r.assertion_idx}"
                f"::{r.variable}@{r.time}"
            )
            lines.append(
                f'    <testcase classname="{escape(f)}" '
                f'name="{escape(tname)}" time="{r.duration_s:.4f}">'
            )
            if r.status == "FAIL":
                lines.append(
                    f'      <failure message="{escape(r.message)}"/>'
                )
            elif r.status == "ERROR":
                lines.append(
                    f'      <error message="{escape(r.message)}"/>'
                )
            lines.append("    </testcase>")
        lines.append("  </testsuite>")
    lines.append("</testsuites>\n")
    with open(path, "w") as fh:
        fh.write("\n".join(lines))


if __name__ == "__main__":
    sys.exit(main())
