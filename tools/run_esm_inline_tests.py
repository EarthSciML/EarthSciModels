#!/usr/bin/env python3
"""tools/run_esm_inline_tests.py

Python inline-test gate for the EarthSciModels rig.

Walks ``components/``, ``lib/`` and ``registered_functions/`` and runs every
inline test (``Model.tests`` / ``ReactionSystem.tests``, esm-spec §6.6,
including the §6.6.5 field assertions) through the **public** EarthSciAST
Python runner :func:`earthsci_ast.inline_tests.run_inline_tests`.

What this file owns, and nothing else:

  * discovery of this repo's ``.esm`` corpus,
  * one SUBPROCESS PER FILE — several at a time (``--jobs``), each optionally
    under a wall-clock cap (``--timeout-seconds``) — so a runaway build cannot
    take the whole CI job with it (Python's per-process GC is the OOM
    guardrail; each worker caps its own address space at
    ``WORKER_RLIMIT_BYTES``, and a worker past the cap is killed and reported
    as an ERROR row for its file),
  * the junit report CI uploads, and the summary a human reads.

Everything about what an inline test MEANS — tolerance resolution (§6.6.4),
the pass predicate (§6.6.3), variable lookup on the built system, §6.6.5
``reduce`` / ``coords`` field collapse, the integrator and its tolerances —
belongs to the toolkit and is not restated here. This driver previously
carried its own copy of all of that, reaching into private upstream modules
(``earthsci_ast.pde_inline_tests``, ``earthsci_ast.simulation.observed_at_state``)
to do it. When upstream renamed that module the private import raised inside
the worker, the worker died before emitting a row, and the parent read "no
rows" as "no inline tests": the gate reported 22 assertions over a corpus
that declares 8,176, and went green on models it never ran. A gate that
can only fail by breaking loudly is the point of the rewrite.

Solver policy lives in the DOCUMENT, not here. A stiff document says so itself
with ``solver.stiffness: "high"`` (esm-spec §2.2); a basename table in this
gate could not travel to the Julia or Rust runners, which is exactly why the
spec grew the block. Two of the three bindings act on it today — Python picks
BDF and Julia picks Rosenbrock23 — while the Rust runner parses and
version-checks the block but maps it to no integrator choice, so a document
that declares it is unchanged there. The field is advisory by specification,
so that conforms; it is recorded here because "every binding maps it to its
own integrator" is what this comment used to claim, and it is not true yet.

``cse`` is the one exception, and it is deliberately ONE line rather than a
table — see ``CSE_FALSE_FILENAMES``.

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

# The documents this gate asks to be built WITHOUT common-subexpression
# elimination. `cse` is a SymPy-lowering knob, not a fact about the model
# (esm-spec §2.2 keeps it out of the document on purpose), so it can only be
# said here — and it has to be said, because the corpus contains one document
# the library's default cannot build in any usable time.
#
# Measured on this corpus (Python runner, per-file subprocess):
#
#   geoschem_fullchem.esm   cse=True  did not finish in 50 min
#                           cse=False 506 s (8.4 min), 81/81 assertions pass
#   urban_canopy_model.esm  cse=True  2.3 min, passes
#                           cse=False did not finish in 50 min
#
# The two want OPPOSITE settings, so neither a global `cse=False` nor the
# default serves the whole corpus, and the NumPy (non-SymPy) engine finishes
# neither document — it was measured too. In CI the cost is not subtle: the
# walk cleared 195 files in 19 minutes and then spent 26 minutes on
# geoschem_fullchem alone before the job cap.
#
# Exit criterion: this set disappears the moment the toolkit picks CSE from
# the system's own size rather than from the caller. The two documents sit far
# apart on exactly that axis (819 reactions against 78 algebraic states), so
# the choice is the library's to make; until it does, the gate states it for
# the one document that needs it.
CSE_FALSE_FILENAMES: frozenset = frozenset({"geoschem_fullchem.esm"})

# Per-subprocess hard address-space ceiling. It is a PER-WORKER guard, not a
# budget for the run: with `--jobs N` there are N of them, so N * 6 GiB can
# exceed the 16 GiB ubuntu-latest runner on paper. What keeps that theoretical
# is that the documents in this corpus build far below the ceiling — the
# ceiling exists so that ONE runaway build dies as a worker (an ERROR row for
# its file) instead of taking the whole job down with an OOM kill, and a
# smaller number would refuse documents that legitimately need the room.
WORKER_RLIMIT_BYTES = 6 * 1024 * 1024 * 1024

# CPython's default 1000-frame limit is below what the deepest documents in
# this corpus need: the toolkit's AST walks are recursive and
# geoschem_fullchem.esm (819 reactions, deepest RHS ~322 levels) peaks near
# 1,300 frames in flatten() alone — measured when the limit was still the
# default, where every one of its 81 assertions errored as
# "flatten failed: RecursionError". 20,000 is ~15x that measured peak: enough
# headroom for a deeper mechanism than any in the corpus today.
#
# It is raised on the worker's own (main) thread, so the C stack is whatever
# the process was given. A walk deep enough to exhaust that stack segfaults
# the worker rather than raising RecursionError — which is reported, not
# swallowed: the worker dies without its `__DONE__` marker and the parent
# turns that into an ERROR row for the file (see `rows_from_worker`).
WORKER_RECURSION_LIMIT = 20_000

# The exit code the driver reports for a worker it killed at the per-file cap.
# 124 is what `timeout(1)` uses, and it is outside the worker's own 0/1, so it
# takes the `rows_from_worker` / `verdict_for_file` path every other worker
# that could not report takes.
TIMEOUT_RC = 124


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

    from earthsci_ast.inline_tests import InlineTestOptions, run_inline_tests

    def options_for(document):
        """The toolkit's per-document policy hook (it exists so a corpus gate's
        site policy stays at the site instead of being re-implemented around
        the runner). Everything this gate could say here, it says in the
        DOCUMENT instead — except `cse`, which the spec keeps out of the
        document because it is a binding's lowering knob."""
        if isinstance(document, str) and Path(document).name in CSE_FALSE_FILENAMES:
            return InlineTestOptions(cse=False)
        return None

    t0 = time.time()
    rows: List[AssertionRow] = []
    try:
        # A LIST input selects the runner's batch semantics: a document that
        # fails to load contributes an ERROR row naming the path instead of
        # raising, so a load failure is reported like every other failure.
        results = run_inline_tests([file_path], options_for=options_for)
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


def rows_from_worker(
    file_path: Path, stdout: str, returncode: int, stderr: str
) -> List[AssertionRow]:
    """Parse one worker's output into rows, turning a worker that did not
    finish into an ERROR row.

    The ``__DONE__`` marker is what separates "this file has no inline tests"
    from "the worker died before it could say anything" — an OOM kill, the
    address-space rlimit, a segfault, an import that raised. Those look
    identical in the row stream (both are empty), and reading the second as
    the first is exactly how this gate came to report 22 assertions over a
    corpus of 8,176 and call it green.
    """
    rows: List[AssertionRow] = []
    done = False
    for line in stdout.splitlines():
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
        rows.append(_spawn_row(
            file_path,
            f"worker exited rc={returncode} without emitting __DONE__; "
            f"stderr_tail={stderr[-500:]!r}",
        ))
    elif returncode not in (0, 1):
        rows.append(_spawn_row(
            file_path,
            f"worker exited rc={returncode}; stderr_tail={stderr[-500:]!r}",
        ))
    return rows


def verdict_for_file(rows: List[AssertionRow], returncode: int) -> int:
    """This file's contribution to the driver's exit code: 0 clean, 1 an
    assertion failed or errored, 2 the driver could not test the file at all.

    A file that produced NO row is a 2, not a 0. Every path that reaches here
    should have left at least one row — a finished worker with no inline tests
    still emits its ``<load>`` row, and a worker that did not finish is given a
    spawn row by `rows_from_worker` — so an empty list means the driver lost
    the file somewhere, and the one thing this gate must never do is call that
    a pass."""
    if returncode not in (0, 1):
        return 2
    if not rows:
        return 2
    return 1 if any(r.status in ("FAIL", "ERROR") for r in rows) else 0


def run_one_file(
    file_path: Path, timeout_s: float = 0.0
) -> Tuple[List[AssertionRow], int, str]:
    """Spawn the worker subprocess for one .esm file. Returns
    (rows, exit_code, raw_stderr).

    ``timeout_s`` (0 = no cap) is the wall-clock a single document may take
    before its worker is killed and the file reported as an ERROR row. A
    document that never finishes is otherwise indistinguishable to CI from a
    slow one: the job hits its own cap, and the log says nothing about which
    file it was sitting on, whether the rest of the corpus passed, or what the
    junit report would have said — none of which is ever written. A cap turns
    that into a named row and lets the walk finish."""
    cmd = [
        sys.executable, "-X", "faulthandler",
        str(Path(__file__).resolve()), "--worker", str(file_path),
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False,
                              timeout=timeout_s if timeout_s > 0 else None)
    except subprocess.TimeoutExpired as expired:
        # The partial streams come back undecoded even in text mode.
        out = _as_text(expired.stdout)
        err = (f"worker killed after the {timeout_s:g}s per-file cap "
               f"(--timeout-seconds)\n" + _as_text(expired.stderr))
        return rows_from_worker(file_path, out, TIMEOUT_RC, err), TIMEOUT_RC, err
    rows = rows_from_worker(file_path, proc.stdout, proc.returncode, proc.stderr)
    return rows, proc.returncode, proc.stderr


def _as_text(stream) -> str:
    if stream is None:
        return ""
    if isinstance(stream, bytes):
        return stream.decode("utf-8", "replace")
    return str(stream)


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
        "--timeout-seconds", type=float, default=0.0,
        help="Wall-clock a single .esm may take before its worker is killed "
             "and the file reported as an ERROR row. 0 (the default) is no "
             "cap, which is what a local run of one document wants; CI passes "
             "a value sized against its own job timeout, so that a document "
             "that does not finish is named in the report instead of taking "
             "the job down with nothing written.",
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
    cap = (f", {args.timeout_seconds:g}s cap per file"
           if args.timeout_seconds > 0 else "")
    print(f"Walking {len(files)} .esm file(s), {jobs} at a time{cap} ...")
    all_rows: List[AssertionRow] = []
    overall_rc = 0
    t_total = time.time()

    def _one(f: Path):
        t0 = time.time()
        rows, rc, stderr = run_one_file(f, timeout_s=args.timeout_seconds)
        return f, rows, rc, stderr, time.time() - t0

    # Results are reported in discovery order however the workers finish, so a
    # log diffed between two runs lines up file for file.
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        for f, rows, rc, stderr, wall in pool.map(_one, files):
            all_rows.extend(rows)
            verdict = verdict_for_file(rows, rc)
            tag = "OK " if verdict == 0 else "FAIL"
            print(f"  [{tag}] {f}  ({len(rows)} assertions, {wall:.1f}s)",
                  flush=True)
            if rc not in (0, 1):
                print(f"    worker stderr tail:\n{stderr[-400:]}", file=sys.stderr)
            overall_rc = max(overall_rc, verdict)

    _print_summary(all_rows, files)
    print(f"Total wall: {time.time() - t_total:.1f}s")

    if args.junit_xml:
        _write_junit_xml(all_rows, args.junit_xml)

    return overall_rc


if __name__ == "__main__":
    sys.exit(main())
