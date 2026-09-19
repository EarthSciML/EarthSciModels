#!/usr/bin/env python3
"""tools/run_esm_inline_tests.py

Python inline-test gate for the EarthSciModels rig.

Walks ``components/``, ``lib/`` and ``registered_functions/`` and runs every
inline test (``Model.tests`` / ``ReactionSystem.tests``, esm-spec §6.6,
including the §6.6.5 field assertions) through the **public** EarthSciAST
Python runner :func:`earthsci_ast.inline_tests.run_inline_tests`.

What this file owns, and nothing else:

  * discovery of this repo's ``.esm`` corpus,
  * one SUBPROCESS PER FILE — several at a time (``--jobs``) — so a runaway
    build cannot take the whole CI job with it (Python's per-process GC is the
    OOM guardrail; each worker caps its own address space at
    ``WORKER_RLIMIT_BYTES``),
  * the junit report CI uploads, and the summary a human reads.

Everything about what an inline test MEANS — tolerance resolution (§6.6.4),
the pass predicate (§6.6.3), variable lookup on the built system, §6.6.5
``reduce`` / ``coords`` field collapse, the integrator and its tolerances —
belongs to the toolkit and is not restated here. This driver previously
carried its own copy of all of that, reaching into private upstream modules
(``earthsci_ast.pde_inline_tests``, ``earthsci_ast.simulation.observed_at_state``)
to do it. When upstream renamed that module the private import raised inside
the worker, the worker died before emitting a row, and the parent read "no
rows" as "no inline tests": the gate reported 22 assertions over a
2,500-assertion corpus and went green on models it never ran. A gate that
can only fail by breaking loudly is the point of the rewrite.

Solver / CSE policy lives in the DOCUMENT, not here. A stiff document says so
itself with ``solver.stiffness: "high"`` (esm-spec §2.2), which every binding
maps to its own integrator; a basename table in this gate could not travel to
the Julia or Rust runners, which is exactly why the spec grew the block. The
``cse`` knob is likewise gone: the runner's default is the supported path.

Exit codes:
  0  every assertion passed
  1  at least one assertion failed or errored
  2  internal driver failure (a worker that could not report at all)
"""

from __future__ import annotations

import argparse
import json
import os
import resource
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Tuple

# Sweep roots. `components/` holds the per-science-domain corpus; `lib/` and
# `registered_functions/` hold the shared leaves the components `ref`-include.
# Kept in parity with the Julia gate's roots — two runners walking different
# corpora is how a cross-runner divergence hides.
DEFAULT_ROOTS = ["components", "lib", "registered_functions"]

REPO_ROOT = Path(__file__).resolve().parent.parent

# Per-subprocess hard memory ceiling. 6 GiB leaves headroom on the 16 GiB
# ubuntu-latest CI runner even with parent + worker alive.
WORKER_RLIMIT_BYTES = 6 * 1024 * 1024 * 1024

# CPython's default 1000-frame limit is below what the deepest documents in
# this corpus need: the toolkit's AST walks are recursive and
# geoschem_fullchem.esm (819 reactions, deepest RHS ~322 levels) peaks near
# 1,300 frames in flatten() alone. 20,000 is ~15x that, while still low enough
# that runaway recursion trips a clean RecursionError (an ERROR row) rather
# than blowing the C stack.
WORKER_RECURSION_LIMIT = 20_000


# ---------------------------------------------------------------------------
# Result rows (the parent/worker wire format)
# ---------------------------------------------------------------------------


@dataclass
class AssertionRow:
    file: str
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
# Worker: one .esm file, one process
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


def run_worker(file_path: str) -> int:
    _set_memory_limit(WORKER_RLIMIT_BYTES)
    sys.setrecursionlimit(WORKER_RECURSION_LIMIT)

    from earthsci_ast.inline_tests import run_inline_tests

    t0 = time.time()
    rows: List[AssertionRow] = []
    try:
        # A LIST input selects the runner's batch semantics: a document that
        # fails to load contributes an ERROR row naming the path instead of
        # raising, so a load failure is reported like every other failure.
        results = run_inline_tests([file_path])
    except Exception as err:  # noqa: BLE001 — the row IS the report
        rows.append(AssertionRow(
            file=file_path, container_name="<runner>", test_id="<run>",
            assertion_idx=0, variable="", time=0.0, expected=0.0, actual=None,
            status="ERROR",
            message=f"run_inline_tests failed: {type(err).__name__}: {err}",
            duration_s=time.time() - t0,
        ))
        _emit_worker_results(rows)
        return 1

    # One wall-clock measurement per file, shared evenly across its
    # assertions: junit sums <testcase> times, so stamping each assertion with
    # the cumulative figure would overcount the file N-fold.
    share = (time.time() - t0) / max(len(results), 1)
    for r in results:
        # `actual is None` is how the runner reports "never evaluated" (the
        # simulate/build/load failed) as opposed to "evaluated and wrong".
        status = "PASS" if r.passed else ("ERROR" if r.actual is None else "FAIL")
        rows.append(AssertionRow(
            file=file_path, container_name=str(r.model), test_id=str(r.test_id),
            assertion_idx=int(r.assertion_idx), variable=str(r.variable),
            time=float(r.time), expected=float(r.expected), actual=r.actual,
            status=status, message=r.message, duration_s=share,
        ))

    if not results:
        # Minimum-bar gate: a document with no inline tests still had to LOAD
        # (the runner loads before it can find no tests), so structural drift
        # in a leaf is caught here at PR time. Recorded as a row so the file
        # is visibly checked rather than silently absent.
        rows.append(AssertionRow(
            file=file_path, container_name="<load>", test_id="<load>",
            assertion_idx=0, variable="", time=0.0, expected=0.0, actual=None,
            status="PASS", message="loaded; no inline tests declared",
            duration_s=time.time() - t0,
        ))

    _emit_worker_results(rows)
    return 1 if any(r.status in ("FAIL", "ERROR") for r in rows) else 0


def _emit_worker_results(rows: List[AssertionRow]) -> None:
    """Worker writes one JSON object per assertion to stdout, then a final
    ``__DONE__`` marker. The parent reads only lines starting with ``{`` so
    incidental warnings do not pollute the parser, and treats a missing
    marker as a worker that died mid-file."""
    for r in rows:
        sys.stdout.write(json.dumps(asdict(r)) + "\n")
    sys.stdout.write("__DONE__\n")
    sys.stdout.flush()


# ---------------------------------------------------------------------------
# Parent (driver)
# ---------------------------------------------------------------------------


def discover_esm_files(roots: Sequence[str]) -> List[Path]:
    found: List[Path] = []
    for r in roots:
        p = Path(r)
        if not p.is_absolute():
            p = REPO_ROOT / p
        if not p.is_dir():
            continue
        found.extend(sorted(p.rglob("*.esm")))
    return sorted(set(found))


def _spawn_row(file_path: Path, message: str) -> AssertionRow:
    return AssertionRow(
        file=str(file_path), container_name="<worker>", test_id="<spawn>",
        assertion_idx=0, variable="", time=0.0, expected=0.0, actual=None,
        status="ERROR", message=message, duration_s=0.0,
    )


def run_one_file(file_path: Path) -> Tuple[List[AssertionRow], int, str]:
    """Spawn the worker subprocess for one .esm file. Returns
    (rows, exit_code, raw_stderr)."""
    cmd = [
        sys.executable, "-X", "faulthandler",
        str(Path(__file__).resolve()), "--worker", str(file_path),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)

    rows: List[AssertionRow] = []
    done = False
    for line in proc.stdout.splitlines():
        line = line.strip()
        if line == "__DONE__":
            done = True
            continue
        if not line.startswith("{"):
            continue
        try:
            rows.append(AssertionRow(**json.loads(line)))
        except (json.JSONDecodeError, TypeError):
            continue

    if not done:
        # No marker: the worker died before it could report (OOM kill, rlimit,
        # segfault, an import that raised). Whatever it had said so far is
        # kept, and the death itself becomes a row — the failure mode this
        # gate previously swallowed as "no inline tests".
        rows.append(_spawn_row(
            file_path,
            f"worker exited rc={proc.returncode} without emitting __DONE__; "
            f"stderr_tail={proc.stderr[-500:]!r}",
        ))
    elif proc.returncode not in (0, 1):
        rows.append(_spawn_row(
            file_path,
            f"worker exited rc={proc.returncode}; "
            f"stderr_tail={proc.stderr[-500:]!r}",
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
            print(f"  [??? ] {f}: no rows reported")
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


def _write_junit_xml(rows: List[AssertionRow], path: str) -> None:
    """Minimal junit XML — one <testsuite> per file, one <testcase> per
    assertion. Symmetric with the Julia gate's report."""
    from xml.sax.saxutils import quoteattr

    by_file: Dict[str, List[AssertionRow]] = {}
    for r in rows:
        by_file.setdefault(r.file, []).append(r)
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', "<testsuites>"]
    for f, rs in by_file.items():
        nf = sum(1 for r in rs if r.status == "FAIL")
        ne = sum(1 for r in rs if r.status == "ERROR")
        lines.append(
            f'  <testsuite name={quoteattr(f)} tests="{len(rs)}" '
            f'failures="{nf}" errors="{ne}">'
        )
        for r in rs:
            tname = (
                f"{r.container_name}::{r.test_id}#{r.assertion_idx}"
                f"::{r.variable}@{r.time}"
            )
            lines.append(
                f'    <testcase classname={quoteattr(f)} '
                f'name={quoteattr(tname)} time="{r.duration_s:.4f}">'
            )
            if r.status == "FAIL":
                lines.append(f'      <failure message={quoteattr(r.message)}/>')
            elif r.status == "ERROR":
                lines.append(f'      <error message={quoteattr(r.message)}/>')
            lines.append("    </testcase>")
        lines.append("  </testsuite>")
    lines.append("</testsuites>\n")
    with open(path, "w") as fh:
        fh.write("\n".join(lines))


def _resolve_files(args, ap) -> List[Path]:
    if args.files:
        files: List[Path] = []
        for f in args.files:
            p = Path(f)
            if not p.is_absolute():
                p = REPO_ROOT / p
            if not p.exists():
                ap.error(f"--files: not found: {p}")
            if p.suffix != ".esm":
                ap.error(f"--files: not a .esm file: {p}")
            files.append(p.resolve())
        return sorted(set(files))
    return discover_esm_files(args.root or DEFAULT_ROOTS)


def main(argv: Optional[List[str]] = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--worker",
        help="Internal: run a single .esm file in worker mode "
             "(emits JSON results to stdout).",
    )
    ap.add_argument(
        "--root", action="append", default=None,
        help="Root directory to search for .esm files. May be passed multiple "
             "times. Defaults to ./components, ./lib and "
             "./registered_functions. Mutually exclusive with --files.",
    )
    ap.add_argument(
        "--files", nargs="+", default=None,
        help="Explicit list of .esm files to test (instead of walking --root "
             "directories). Mutually exclusive with --root.",
    )
    ap.add_argument(
        "--jobs", type=int, default=0,
        help="Number of .esm files to test concurrently (one subprocess each). "
             "0 (the default) picks os.cpu_count() capped at 8; 1 is serial. "
             "Files are independent — the workers share nothing but the CPU.",
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

    files = _resolve_files(args, ap)
    if not files:
        print("No .esm files discovered.", file=sys.stderr)
        return 2

    jobs = args.jobs or min(os.cpu_count() or 1, 8)
    print(f"Walking {len(files)} .esm file(s), {jobs} at a time ...")
    all_rows: List[AssertionRow] = []
    overall_rc = 0
    t_total = time.time()

    def _one(f: Path):
        t0 = time.time()
        rows, rc, stderr = run_one_file(f)
        return f, rows, rc, stderr, time.time() - t0

    # Results are reported in discovery order however the workers finish, so a
    # log diffed between two runs lines up file for file.
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        for f, rows, rc, stderr, wall in pool.map(_one, files):
            all_rows.extend(rows)
            bad = sum(1 for r in rows if r.status in ("FAIL", "ERROR"))
            tag = "OK " if bad == 0 else "FAIL"
            print(f"  [{tag}] {f}  ({len(rows)} assertions, {wall:.1f}s)",
                  flush=True)
            if rc not in (0, 1):
                overall_rc = max(overall_rc, 2)
                print(f"    worker stderr tail:\n{stderr[-400:]}", file=sys.stderr)
            elif bad:
                overall_rc = max(overall_rc, 1)

    _print_summary(all_rows, files)
    print(f"Total wall: {time.time() - t_total:.1f}s")

    if args.junit_xml:
        _write_junit_xml(all_rows, args.junit_xml)

    return overall_rc


if __name__ == "__main__":
    sys.exit(main())
