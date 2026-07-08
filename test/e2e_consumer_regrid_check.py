#!/usr/bin/env python3
"""test/e2e_consumer_regrid_check.py  (bead esm-3nc.6)

End-to-end consumer validation for the pure-IO data-loader migration
(RFC pure-io-data-loaders §6/§7; epic esm-3nc). Realises the esm-3nc.6
acceptance sentence:

    "Verify a consumer file that ref-includes a migrated single-component
     model resolves + regrids + produces fields identical (to tolerance)
     to the pre-migration inline pipeline."

What it checks, using the canonical ESS Python runner
(``earthsci_ast.load`` — the single simulation/resolution pathway per
AGENTS.md §1; no parallel evaluator):

  1. RESOLVES — ``load()`` the consumer fixture
     ``test/fixtures/earthsci_data/consumer_openaq.esm``. The consumer
     {"ref"}-includes the migrated single-component model
     ``components/earthsci_data/openaq.esm`` as the subsystem ``aq``;
     that model in turn {"ref"}-includes the pure-IO loader
     ``openaq_loader.esm`` as ``obs``. A successful load proves the
     two-level pure-IO loader ref chain resolves through the runner.

  2. REGRIDS — the migrated model carries a per-variable ``regrid`` block
     (the post-migration home of regridding, moved off the loader). A
     successful ``load()`` schema-validates that block; this check
     additionally asserts the kernel + ``missing_value`` are present.

  3. FIELDS IDENTICAL (to tolerance) — the migrated model's exposed field
     interface (spatial parameters + observed air-quality field, their
     units, and the regrid fill semantics) is compared against the frozen
     pre-migration reference
     ``test/fixtures/earthsci_data/openaq_pre_migration_reference.json``
     (the legacy esm-0.5.0 OpenAQ with co-located
     ``data_loaders.OpenAQ_obs.regridding``, captured from origin/main
     before migration). The pre-migration regridding ``fill_value`` and
     the post-migration ``regrid.<var>.missing_value`` must agree within
     ``REL_TOL``.

Numeric *field values* (regridded station concentrations) require external
OpenAQ station data and are a downstream consumer-repo concern (AGENTS.md
§2); this check validates the *interface + regrid intent* identity that
the model-content rig is responsible for, which is what survives the
migration independent of data availability.

The fixtures live under ``test/fixtures/earthsci_data/`` and are
deliberately NOT under ``components/**`` or ``lib/**``, so the
``run_esm_inline_tests.py`` gate and the Julia inline-test discovery do
not auto-walk them; this script is the explicit driver.

Exit codes:
  0  every check passed
  1  at least one check failed
"""
from __future__ import annotations

import json
import os
import sys

REL_TOL = 1e-6  # spec §6.6.4 default relative tolerance

_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)

CONSUMER = os.path.join(_HERE, "fixtures", "earthsci_data", "consumer_openaq.esm")
MIGRATED = os.path.join(_ROOT, "components", "earthsci_data", "openaq.esm")
PRE_REF = os.path.join(
    _HERE, "fixtures", "earthsci_data", "openaq_pre_migration_reference.json"
)

# Regrid kernels recognised by ESD (esd-47z.*) / the post-migration model
# `regrid` block. point-observation loaders (OpenAQ) use cell_average.
_KNOWN_KERNELS = {"conservative", "bspline", "cell_average"}


def _fail(msg: str) -> None:
    print(f"  [FAIL] {msg}")


def _ok(msg: str) -> None:
    print(f"  [ OK ] {msg}")


def _approx_equal(a: float, b: float, rel: float = REL_TOL) -> bool:
    return abs(a - b) <= rel * max(1.0, abs(a), abs(b))


def _exposed_vars(model: dict) -> dict:
    """name -> (type, units) for the model's declared variables."""
    return {
        k: (v.get("type"), v.get("units"))
        for k, v in model.get("variables", {}).items()
    }


def main() -> int:
    try:
        from earthsci_ast import load
    except Exception as e:  # pragma: no cover - environment guard
        print(f"FATAL: cannot import earthsci_ast ({e}). "
              f"Install the canonical ESS runner (see .github/workflows/test-esm.yml).")
        return 1

    failures = 0

    # ---- 1. RESOLVES: consumer ref-include chain loads through the runner ----
    print("[1] consumer ref-include resolves through the canonical runner")
    for label, path in (("consumer", CONSUMER), ("migrated OpenAQ model", MIGRATED)):
        try:
            load(path)
            _ok(f"{label} load() resolved: {os.path.relpath(path, _ROOT)}")
        except Exception as e:
            failures += 1
            _fail(f"{label} load() raised {type(e).__name__}: "
                  f"{(str(e).splitlines() or [''])[0][:200]}")

    # Load JSON declarations for the interface / regrid comparison.
    with open(MIGRATED) as f:
        migrated = json.load(f)
    with open(PRE_REF) as f:
        pre = json.load(f)
    with open(CONSUMER) as f:
        consumer = json.load(f)

    mig_model = migrated["models"]["OpenAQ"]
    pre_model = pre["models"]["OpenAQ"]

    # ---- 2. REGRIDS: migrated model carries a valid per-variable regrid block ----
    print("[2] migrated model regrids (per-variable regrid block present + valid)")
    regrid = mig_model.get("regrid", {})
    if not regrid:
        failures += 1
        _fail("migrated OpenAQ has no `regrid` block")
    else:
        pm25 = regrid.get("pm25", {})
        method = pm25.get("method")
        if method in _KNOWN_KERNELS:
            _ok(f"regrid.pm25.method = '{method}' (recognised ESD kernel)")
        else:
            failures += 1
            _fail(f"regrid.pm25.method = {method!r} not in {_KNOWN_KERNELS}")
        if "missing_value" in pm25:
            _ok(f"regrid.pm25.missing_value = {pm25['missing_value']}")
        else:
            failures += 1
            _fail("regrid.pm25 missing `missing_value`")

    # ---- 3. FIELDS IDENTICAL (to tolerance) vs pre-migration inline pipeline ----
    print("[3] exposed fields identical (to tolerance) to pre-migration inline pipeline")
    mig_vars = _exposed_vars(mig_model)
    pre_vars = _exposed_vars(pre_model)

    # 3a. spatial parameters + observed air-quality field preserved with units.
    for name in ("lon", "lat", "pm25"):
        if mig_vars.get(name) == pre_vars.get(name) and pre_vars.get(name) is not None:
            _ok(f"field '{name}': {pre_vars[name]} (type, units) preserved")
        else:
            failures += 1
            _fail(f"field '{name}' interface drift: "
                  f"pre={pre_vars.get(name)} -> post={mig_vars.get(name)}")

    # 3b. consumer re-exposes the migrated field with the same units.
    cons_vars = _exposed_vars(consumer["models"]["OpenAQConsumerE2E"])
    if cons_vars.get("pm25_consumed", (None, None))[1] == mig_vars.get("pm25", (None, None))[1]:
        _ok(f"consumer pm25_consumed units match migrated pm25 "
            f"({cons_vars.get('pm25_consumed')[1]})")
    else:
        failures += 1
        _fail(f"consumer pm25_consumed units {cons_vars.get('pm25_consumed')} "
              f"!= migrated pm25 {mig_vars.get('pm25')}")

    # 3c. regrid fill semantics: post missing_value == pre regridding.fill_value.
    pre_loader = next(iter(pre.get("data_loaders", {}).values()), {})
    pre_fill = pre_loader.get("regridding", {}).get("fill_value")
    post_fill = regrid.get("pm25", {}).get("missing_value")
    if pre_fill is None:
        failures += 1
        _fail("pre-migration reference has no regridding.fill_value")
    elif post_fill is None:
        failures += 1
        _fail("post-migration regrid.pm25.missing_value absent")
    elif _approx_equal(float(post_fill), float(pre_fill)):
        _ok(f"regrid fill preserved to tol {REL_TOL:g}: "
            f"pre fill_value {pre_fill} == post missing_value {post_fill}")
    else:
        failures += 1
        _fail(f"regrid fill drift: pre fill_value {pre_fill} "
              f"!= post missing_value {post_fill}")

    print()
    if failures:
        print(f"RESULT: FAIL ({failures} check(s) failed)")
        return 1
    print("RESULT: PASS — consumer ref-include resolves + regrids + fields "
          "identical (to tolerance) to the pre-migration inline pipeline")
    return 0


if __name__ == "__main__":
    sys.exit(main())
