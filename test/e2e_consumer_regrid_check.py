#!/usr/bin/env python3
"""test/e2e_consumer_regrid_check.py  (bead esm-3nc.6)

End-to-end consumer validation for the pure-IO data-loader migration
(RFC pure-io-data-loaders §6/§7; epic esm-3nc). Realises the esm-3nc.6
acceptance sentence:

    "Verify a consumer file that ref-includes a migrated single-component
     model resolves + regrids + produces fields identical (to tolerance)
     to the pre-migration inline pipeline."

Everything structural is read through the canonical ESS Python runner
(``earthsci_ast.load_path`` / ``flatten`` / ``classification``) — the single
resolution pathway per AGENTS.md §1. Nothing here re-derives variable
classification by walking equations; ``earthsci_ast.classification`` is the
single source of truth for what an unknown or a parameter *is*
(esm-spec §6.3.1).

What it checks
--------------

  [1] RESOLVES — ``load_path()`` the consumer fixture
      ``test/fixtures/earthsci_data/consumer_openaq.esm`` and the migrated
      model ``components/earthsci_data/openaq.esm``, then ``flatten()`` the
      consumer. The consumer ``{"ref"}``-includes the migrated model as the
      subsystem ``aq``; at esm 1.0.0 that one file holds BOTH the ``OpenAQ``
      model and the ``OpenAQ_obs`` entry of its ``data_sources`` registry
      (a data source is not a component, so there is no second
      ``openaq_loader.esm`` and no two-level ref chain any more). A
      successful flatten proves the ref mounts and namespaces the migrated
      model's fields into the consumer.

  [2] INGEST BINDING preserved — the machine-readable half of "regrids".
      Compared field-by-field against the frozen pre-migration reference
      ``test/fixtures/earthsci_data/openaq_pre_migration_reference.json``
      (esm 0.5.0, captured from origin/main before the split), translating
      the 0.5.0 vocabulary into the 1.0.0 one:

          0.5.0                                   1.0.0
          data_loaders.OpenAQ_obs             ->  data_sources.OpenAQ_obs
          …          .kind / .source / .temporal   (identical sub-blocks)
          …          .variables[v].file_variable-> models.OpenAQ.variables[v]
                                                     .update.from.file_variable
          …          .variables[v].units       ->  models.OpenAQ.variables[v].units
          models.OpenAQ.variables.pm25
              .type "observed" + .expression       models.OpenAQ.variables.pm25
              "OpenAQ_obs.pm25"               ->     .type "parameter" +
                                                     .update.source "OpenAQ_obs"

      i.e. the same registry key, the same source kind, the same URL
      template, the same temporal cadence, the same ten fields, the same
      per-field file variable and units, and the same named producer for
      the exposed ``pm25``.

  [3] EXPOSED FIELD INTERFACE identical — units of ``lon`` / ``lat`` /
      ``pm25`` against the pre-migration reference, plus the DERIVED roles
      taken from ``earthsci_ast.classification`` (never from a local walk
      of the equations): ``lon``/``lat`` are constant parameters, ``pm25``
      is a data-updated (discrete) parameter and NOT an observed unknown,
      and the consumer's ``pm25_consumed`` is an observed unknown whose
      defining RHS is ``aq.pm25``, with matching units. The flattened IR is
      cross-checked for the same two facts under their namespaced names.

  [4] REGRID INTENT — a PROVENANCE check, not a schema contract. Read this
      before trusting it:

      The per-variable ``Model.regrid`` map that esm 0.5.0–0.7.0 declared
      was REMOVED by esm 0.8.0 and does not exist at 1.0.0. esm-spec §8.6:
      a data source performs no regridding, and the carrier of a regrid
      kernel is the ``transform`` field of a ``variable_map`` entry on the
      COUPLING EDGE that consumes the field (§10.4/§10.5). Neither
      ``openaq.esm`` nor this consumer fixture declares such an edge, so
      there is no schema-validated regrid structure anywhere in this
      repository to assert against — the 0.x check's "load_path()
      schema-validates the regrid block" premise is simply gone.

      What the 1.0.0 migration promised instead is RECOVERABILITY: the
      demoted map was recorded verbatim under
      ``models.OpenAQ.reference.notes``. This check holds the migration to
      that promise — it recovers the recorded JSON out of the notes and
      asserts it still covers exactly the ten data-bound fields, still
      names a recognised ESD kernel per field, and still carries a
      ``missing_value`` equal (within ``REL_TOL``) to the pre-migration
      ``data_loaders.OpenAQ_obs.regridding.fill_value``. It fails if the
      record is deleted, truncated, made unparseable, loses a field, or
      drifts in kernel or fill value.

      It does NOT — and at 1.0.0 cannot — prove that any runtime will apply
      ``cell_average`` with ``missing_value`` 0.0 to these fields. Regaining
      that requires authoring the consuming coupling edge's ``transform``;
      see "Coverage lost at esm 1.0.0" in
      ``test/fixtures/earthsci_data/README.md``.

Numeric *field values* (regridded station concentrations) require external
OpenAQ station data and are a downstream consumer-repo concern (AGENTS.md
§2); this check validates the *interface + ingest binding + recorded regrid
intent* identity that the model-content rig is responsible for, which is
what survives the migration independent of data availability.

The frozen reference stays pinned at esm 0.5.0 on purpose: it is the
pre-migration snapshot the migration must be shown to have preserved.
Re-freezing it at 1.0.0 would turn every comparison below into the current
file compared against a copy of itself. It is stored as ``.json`` rather
than ``.esm`` because ``earthsci_ast`` rejects major-0 documents outright,
so it is read here as raw JSON — the only place in this script that does
not go through the runner, and only because no runner will load it.

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

# The one ingest registry key the migration must have carried across
# `data_loaders` -> `data_sources` (esm 1.0.0, AGENTS.md §2).
SOURCE_KEY = "OpenAQ_obs"

CONSUMER_MODEL = "OpenAQConsumerE2E"
MIGRATED_MODEL = "OpenAQ"
SUBSYSTEM = "aq"          # {"ref"} mount point in the consumer
EXPOSED_FIELD = "pm25"    # the representative re-exposed field
CONSUMED_FIELD = "pm25_consumed"

# Regrid kernels recognised by ESD (esd-47z.*). Point-observation sources
# (OpenAQ) use cell_average.
_KNOWN_KERNELS = {"conservative", "bspline", "cell_average"}

# Marker introducing the verbatim record of the `regrid` map that esm 0.8.0
# demoted out of the schema (see the module docstring, check [4]).
_REGRID_NOTE_MARKER = "`regrid` (verbatim):"


def _fail(msg: str) -> None:
    print(f"  [FAIL] {msg}")


def _ok(msg: str) -> None:
    print(f"  [ OK ] {msg}")


def _note(msg: str) -> None:
    print(f"  [note] {msg}")


def _approx_equal(a: float, b: float, rel: float = REL_TOL) -> bool:
    return abs(a - b) <= rel * max(1.0, abs(a), abs(b))


def _recover_demoted_regrid(model) -> "tuple[dict | None, str]":
    """Recover the esm-0.8.0-demoted `regrid` map from `reference.notes`.

    Returns ``(map, "")`` on success or ``(None, reason)``. This reads the
    RECORD of a retired schema field, not a live one — see check [4] in the
    module docstring for why that distinction matters.
    """
    reference = getattr(model, "reference", None)
    notes = getattr(reference, "notes", None) or ""
    idx = notes.find(_REGRID_NOTE_MARKER)
    if idx < 0:
        return None, f"reference.notes carries no {_REGRID_NOTE_MARKER!r} record"
    blob = notes[idx + len(_REGRID_NOTE_MARKER):]
    start = blob.find("{")
    if start < 0:
        return None, "the verbatim record marker is not followed by a JSON object"
    try:
        recovered, _ = json.JSONDecoder().raw_decode(blob[start:])
    except ValueError as e:
        return None, f"the recorded verbatim map does not parse as JSON: {e}"
    if not isinstance(recovered, dict):
        return None, f"the recorded verbatim map is a {type(recovered).__name__}, not an object"
    return recovered, ""


def _data_bound_fields(model) -> "dict[str, object]":
    """name -> ParameterUpdate for every variable fed by SOURCE_KEY.

    A consumed data field at esm 1.0.0 is a PARAMETER whose ``update`` is
    ``{kind: "data", source: <registry key>, from: {...}}`` (esm-spec §8;
    AGENTS.md §2). Declared shape only; no classification is derived here.
    """
    out = {}
    for name, var in model.variables.items():
        update = getattr(var, "update", None)
        if update is not None and getattr(update, "kind", None) == "data":
            out[name] = update
    return out


def main() -> int:
    try:
        import earthsci_ast
        from earthsci_ast import classification, flatten, load_path
    except Exception as e:  # pragma: no cover - environment guard
        print(f"FATAL: cannot import earthsci_ast ({e}). "
              f"Install the canonical ESS runner (see .github/workflows/test-esm.yml).")
        return 1

    failures = 0

    # ---- 1. RESOLVES: consumer ref-include chain loads + flattens ----------
    print("[1] consumer ref-include resolves through the canonical runner")
    loaded = {}
    for label, key, path in (
        ("consumer", "consumer", CONSUMER),
        ("migrated OpenAQ model", "migrated", MIGRATED),
    ):
        try:
            loaded[key] = load_path(path)
            _ok(f"{label} load_path() resolved: {os.path.relpath(path, _ROOT)}")
        except Exception as e:
            failures += 1
            _fail(f"{label} load_path() raised {type(e).__name__}: "
                  f"{(str(e).splitlines() or [''])[0][:200]}")

    if "consumer" not in loaded or "migrated" not in loaded:
        print()
        print(f"RESULT: FAIL ({failures} check(s) failed) — cannot continue "
              f"without both documents")
        return 1

    consumer_file = loaded["consumer"]
    migrated_file = loaded["migrated"]
    consumer_model = consumer_file.models[CONSUMER_MODEL]
    migrated_model = migrated_file.models[MIGRATED_MODEL]

    # The esm 1.0.0 shape: model + the data_sources it consumes in one
    # {"ref"}-mountable file (the standalone *_loader.esm split is gone).
    if SOURCE_KEY in migrated_file.data_sources:
        _ok(f"migrated file declares data_sources['{SOURCE_KEY}'] alongside its "
            f"model (esm 1.0.0 single-file shape)")
    else:
        failures += 1
        _fail(f"migrated file has no data_sources['{SOURCE_KEY}']: "
              f"{sorted(migrated_file.data_sources)}")

    flat = None
    try:
        flat = flatten(consumer_file, base_path=os.path.dirname(CONSUMER))
    except Exception as e:
        failures += 1
        _fail(f"flatten(consumer) raised {type(e).__name__}: "
              f"{(str(e).splitlines() or [''])[0][:200]}")

    mounted = f"{CONSUMER_MODEL}.{SUBSYSTEM}.{EXPOSED_FIELD}"
    consumed = f"{CONSUMER_MODEL}.{CONSUMED_FIELD}"
    if flat is not None:
        if mounted in flat.variables:
            _ok(f"flatten() mounted the migrated model at '{SUBSYSTEM}': "
                f"{mounted} present in the canonical IR")
        else:
            failures += 1
            _fail(f"flatten() produced no '{mounted}': the {{\"ref\"}} did not "
                  f"mount the migrated model")

    # Load the pre-migration reference as raw JSON: earthsci_ast rejects
    # major-0 documents outright, so no runner can read it (that rejection is
    # exactly why it is stored as .json and not .esm).
    with open(PRE_REF) as f:
        pre = json.load(f)
    pre_model = pre["models"][MIGRATED_MODEL]
    pre_source = pre.get("data_loaders", {}).get(SOURCE_KEY, {})

    # ---- 2. INGEST BINDING preserved across data_loaders -> data_sources ---
    print("[2] ingest binding preserved (0.5.0 `data_loaders` -> 1.0.0 `data_sources`)")
    if not pre_source:
        failures += 1
        _fail(f"pre-migration reference has no data_loaders['{SOURCE_KEY}']")
    post_source = migrated_file.data_sources.get(SOURCE_KEY)

    if pre_source and post_source is not None:
        post_kind = getattr(post_source.kind, "value", post_source.kind)
        if str(post_kind) == pre_source.get("kind"):
            _ok(f"source kind preserved: '{post_kind}'")
        else:
            failures += 1
            _fail(f"source kind drift: pre={pre_source.get('kind')!r} -> "
                  f"post={post_kind!r}")

        pre_url = pre_source.get("source", {}).get("url_template")
        post_url = getattr(post_source.source, "url_template", None)
        if pre_url and post_url == pre_url:
            _ok("source url_template preserved verbatim")
        else:
            failures += 1
            _fail(f"source url_template drift: pre={pre_url!r} -> post={post_url!r}")

        pre_temporal = pre_source.get("temporal", {})
        post_temporal = post_source.temporal
        temporal_drift = [
            (k, v, getattr(post_temporal, k, None))
            for k, v in pre_temporal.items()
            if getattr(post_temporal, k, None) != v
        ]
        if pre_temporal and not temporal_drift:
            _ok(f"temporal cadence preserved ({len(pre_temporal)} keys, "
                f"frequency {pre_temporal.get('frequency')})")
        else:
            failures += 1
            _fail(f"temporal cadence drift: {temporal_drift or 'reference has no temporal block'}")

    # Per-field: same field set, same file_variable, same units, all bound
    # back to the same registry key.
    pre_fields = pre_source.get("variables", {})
    post_fields = _data_bound_fields(migrated_model)
    if set(pre_fields) == set(post_fields):
        _ok(f"all {len(pre_fields)} loader fields still bound: "
            f"{', '.join(sorted(pre_fields))}")
    else:
        failures += 1
        _fail(f"loader field set drift: missing={sorted(set(pre_fields) - set(post_fields))} "
              f"added={sorted(set(post_fields) - set(pre_fields))}")

    binding_drift = []
    for name in sorted(set(pre_fields) & set(post_fields)):
        update = post_fields[name]
        from_source = getattr(update, "from_source", None)
        post_binding = (
            getattr(update, "source", None),
            getattr(from_source, "file_variable", None),
            migrated_model.variables[name].units,
        )
        pre_binding = (
            SOURCE_KEY,
            pre_fields[name].get("file_variable"),
            pre_fields[name].get("units"),
        )
        if post_binding != pre_binding:
            binding_drift.append((name, pre_binding, post_binding))
    if not binding_drift:
        _ok(f"every field's (source, file_variable, units) triple preserved "
            f"(e.g. {EXPOSED_FIELD}: {SOURCE_KEY}/"
            f"{pre_fields.get(EXPOSED_FIELD, {}).get('file_variable')}/"
            f"{pre_fields.get(EXPOSED_FIELD, {}).get('units')})")
    else:
        failures += len(binding_drift)
        for name, pre_b, post_b in binding_drift:
            _fail(f"field '{name}' ingest binding drift: pre={pre_b} -> post={post_b}")

    # ---- 3. EXPOSED FIELD INTERFACE identical to the pre-migration pipeline -
    print("[3] exposed field interface identical to the pre-migration inline pipeline")

    # 3a. units of the exposed fields (the one attribute both vocabularies
    #     spell the same way).
    for name in ("lon", "lat", EXPOSED_FIELD):
        pre_units = pre_model.get("variables", {}).get(name, {}).get("units")
        post_units = getattr(migrated_model.variables.get(name), "units", None)
        if pre_units is not None and pre_units == post_units:
            _ok(f"field '{name}' units preserved: {pre_units}")
        else:
            failures += 1
            _fail(f"field '{name}' units drift: pre={pre_units!r} -> post={post_units!r}")

    # 3b. DERIVED roles, straight from earthsci_ast.classification (AGENTS.md
    #     §1: never re-derive these locally). At 0.5.0 `pm25` was declared
    #     `type: "observed"` with `expression: "OpenAQ_obs.pm25"`; at 1.0.0
    #     `observed` is derived, not declarable, and a consumed data field is
    #     a data-updated parameter. Both spellings name the SAME producer,
    #     and that is what is compared.
    mig_parameters = classification.parameters(migrated_model)
    mig_discrete = classification.discrete_parameters(migrated_model)
    mig_constant = classification.constant_parameters(migrated_model)
    mig_observed = classification.observed_unknowns(migrated_model)

    if EXPOSED_FIELD in mig_parameters and EXPOSED_FIELD in mig_discrete:
        _ok(f"classification: '{EXPOSED_FIELD}' is a data-updated (discrete) "
            f"parameter — the esm 1.0.0 form of a consumed loader field")
    else:
        failures += 1
        _fail(f"classification: '{EXPOSED_FIELD}' is not a discrete parameter "
              f"(parameters={mig_parameters}, discrete={mig_discrete})")
    if EXPOSED_FIELD in mig_observed:
        failures += 1
        _fail(f"classification: '{EXPOSED_FIELD}' is an observed unknown on the "
              f"migrated model; at esm 1.0.0 a consumed data field must be a "
              f"parameter (esm-spec §8)")
    for name in ("lon", "lat"):
        if name in mig_constant:
            _ok(f"classification: '{name}' is a constant parameter (unchanged "
                f"from the pre-migration spatial parameter)")
        else:
            failures += 1
            _fail(f"classification: '{name}' is not a constant parameter "
                  f"(constant={mig_constant})")

    # Same producer, across the vocabulary change.
    pre_expression = pre_model.get("variables", {}).get(EXPOSED_FIELD, {}).get("expression")
    pre_producer = pre_expression.split(".", 1)[0] if pre_expression else None
    post_producer = getattr(post_fields.get(EXPOSED_FIELD), "source", None)
    if pre_producer and pre_producer == post_producer:
        _ok(f"producer of '{EXPOSED_FIELD}' preserved: 0.5.0 expression "
            f"'{pre_expression}' -> 1.0.0 update.source '{post_producer}'")
    else:
        failures += 1
        _fail(f"producer drift for '{EXPOSED_FIELD}': pre={pre_producer!r} "
              f"(from expression {pre_expression!r}) -> post={post_producer!r}")

    # 3c. the consumer re-exposes the field: an observed unknown defined by a
    #     bare-LHS pass-through of the mounted parameter, same units.
    cons_observed = classification.observed_definitions(consumer_model)
    expected_rhs = f"{SUBSYSTEM}.{EXPOSED_FIELD}"
    if cons_observed.get(CONSUMED_FIELD) == expected_rhs:
        _ok(f"consumer: '{CONSUMED_FIELD}' is an observed unknown defined as "
            f"'{expected_rhs}' (classification.observed_definitions)")
    else:
        failures += 1
        _fail(f"consumer: observed_definitions['{CONSUMED_FIELD}'] = "
              f"{cons_observed.get(CONSUMED_FIELD)!r}, expected {expected_rhs!r}")

    cons_units = getattr(consumer_model.variables.get(CONSUMED_FIELD), "units", None)
    mig_units = getattr(migrated_model.variables.get(EXPOSED_FIELD), "units", None)
    if cons_units is not None and cons_units == mig_units:
        _ok(f"consumer '{CONSUMED_FIELD}' units match migrated "
            f"'{EXPOSED_FIELD}' ({cons_units})")
    else:
        failures += 1
        _fail(f"consumer '{CONSUMED_FIELD}' units {cons_units!r} != migrated "
              f"'{EXPOSED_FIELD}' units {mig_units!r}")

    # 3d. the same two facts survive flattening under their namespaced names,
    #     i.e. the interface holds through the {"ref"}, not just in isolation.
    if flat is not None:
        if flat.variables.get(mounted) == "parameter" and mounted in flat.discrete_parameters:
            _ok(f"flattened IR: {mounted} is a data-updated parameter")
        else:
            failures += 1
            _fail(f"flattened IR: {mounted} is {flat.variables.get(mounted)!r}, "
                  f"expected a data-updated parameter")
        if consumed in flat.observed_variables:
            _ok(f"flattened IR: {consumed} is observed (pass-through of {mounted})")
        else:
            failures += 1
            _fail(f"flattened IR: {consumed} is not an observed variable "
                  f"({sorted(flat.observed_variables)})")

    # ---- 4. REGRID INTENT: demoted to prose at esm 0.8.0 -------------------
    print("[4] regrid intent recorded + recoverable (PROVENANCE, not a schema "
          "contract — see docstring)")
    _note("esm 0.8.0 removed `Model.regrid`; esm 1.0.0 (esm-spec §8.6) puts the "
          "kernel on a coupling edge's variable_map.transform, and no document "
          "here declares such an edge — so there is no live structure to assert.")

    recovered, reason = _recover_demoted_regrid(migrated_model)
    pre_fill = pre_source.get("regridding", {}).get("fill_value")
    if pre_fill is None:
        failures += 1
        _fail("pre-migration reference has no regridding.fill_value")

    if recovered is None:
        failures += 1
        _fail(f"the demoted `regrid` map is not recoverable: {reason}")
    else:
        _ok(f"recovered the verbatim `regrid` record from reference.notes "
            f"({len(recovered)} entries)")

        if set(recovered) == set(post_fields):
            _ok(f"the record still covers exactly the {len(post_fields)} "
                f"data-bound fields")
        else:
            failures += 1
            _fail(f"recorded regrid coverage drift: "
                  f"missing={sorted(set(post_fields) - set(recovered))} "
                  f"extra={sorted(set(recovered) - set(post_fields))}")

        bad_kernels = sorted(
            (name, entry.get("method"))
            for name, entry in recovered.items()
            if entry.get("method") not in _KNOWN_KERNELS
        )
        if not bad_kernels:
            methods = sorted({e.get("method") for e in recovered.values()})
            _ok(f"every recorded kernel is a recognised ESD kernel: {methods}")
        else:
            failures += 1
            _fail(f"unrecognised recorded kernels (known: "
                  f"{sorted(_KNOWN_KERNELS)}): {bad_kernels}")

        if pre_fill is not None:
            fill_drift = []
            for name, entry in sorted(recovered.items()):
                post_fill = entry.get("missing_value")
                if post_fill is None or not _approx_equal(float(post_fill), float(pre_fill)):
                    fill_drift.append((name, post_fill))
            if not fill_drift:
                _ok(f"every recorded missing_value matches the pre-migration "
                    f"fill_value {pre_fill} to tol {REL_TOL:g}")
            else:
                failures += len(fill_drift)
                for name, post_fill in fill_drift:
                    _fail(f"regrid fill drift for '{name}': pre fill_value "
                          f"{pre_fill} != recorded missing_value {post_fill!r}")

    print()
    print(f"(earthsci_ast {getattr(earthsci_ast, 'LIBRARY_VERSION', '?')}, "
          f"schema {getattr(earthsci_ast, 'SCHEMA_VERSION', '?')})")
    if failures:
        print(f"RESULT: FAIL ({failures} check(s) failed)")
        return 1
    print("RESULT: PASS — consumer ref-include resolves + flattens, the ingest "
          "binding and exposed field interface are identical to the "
          "pre-migration inline pipeline, and the demoted regrid intent is "
          "still recorded verbatim")
    return 0


if __name__ == "__main__":
    sys.exit(main())
