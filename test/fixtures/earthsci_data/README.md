# earthsci_data consumer e2e fixtures (bead esm-3nc.6)

End-to-end validation fixtures for the pure-IO data-loader migration
(RFC pure-io-data-loaders §6/§7; epic `esm-3nc`). They back the `esm-3nc.6`
acceptance: *a consumer file that ref-includes a migrated single-component
model resolves + regrids + produces fields identical (to tolerance) to the
pre-migration inline pipeline.*

At esm 1.0.0 the "regrids" half of that sentence no longer has a
schema-validated home in these documents. Read
["Coverage lost at esm 1.0.0"](#coverage-lost-at-esm-100) before relying on
it: the driver still checks the ingest binding that feeds each field and the
verbatim record of the demoted regrid map, but it cannot check an enforced
regrid contract, because there is not one.

## Files

| File | Role |
|------|------|
| `consumer_openaq.esm` | A downstream **consumer** model that `{"ref"}`-includes the migrated single-component model `components/earthsci_data/openaq.esm` as the subsystem `aq`, re-exposing the regridded field as `pm25_consumed ~ aq.pm25`. Exercises a `{"ref"}` into a file that holds a model **and** the `data_sources` that model consumes (see the esm 1.0.0 note below). |
| `openaq_pre_migration_reference.json` | Frozen snapshot of the **pre-migration** OpenAQ (`esm 0.5.0`, co-located `data_loaders.OpenAQ_obs` with `regridding.fill_value = 0.0` + legacy `spatial`), captured from `origin/main` before the split. Stored as `.json` (not `.esm`) so no live `.esm` gate ever loads the legacy shape. The reference interface the migration must preserve. **Stays pinned at 0.5.0** — see "Why the reference stays at 0.5.0" below. |

Driver: [`test/e2e_consumer_regrid_check.py`](../../e2e_consumer_regrid_check.py).
Run it through the canonical ESS Python runner (single-pathway rule,
AGENTS.md §1):

```bash
python test/e2e_consumer_regrid_check.py    # exit 0 = green
```

These fixtures live outside `components/**` and `lib/**`, so the
`run_esm_inline_tests.py` gate (Python) and `discover_esm_files`
(`DEFAULT_ROOTS = ["components"]`, Julia) do **not** auto-walk them — the
driver script is the explicit entry point. In CI it is run by the
`consumer-e2e` job in `.github/workflows/test-esm.yml` (wired in by esm-aha;
before that the script existed but was gated by no CI job).

## Why structural (not numeric) field identity

OpenAQ and the other earthsci_data loaders read **external** station /
NetCDF data, so their migrated models carry no self-contained numeric
inline tests (the `tests` blocks are empty). Numeric regridded *values*
require that external data and are a downstream consumer-repo concern
(AGENTS.md §2). What the model-content rig owns — and what survives the
migration independent of data — is the **field interface + ingest
binding**: exposed variable names, units, derived roles, and the
`data_sources` wiring that feeds each field. That identity is what this
check asserts, to tolerance.

Up to esm 0.7.0 this section could also say "and the regrid kernel + fill
semantics", because the kernel lived in a schema-validated per-variable
`Model.regrid` map. It no longer does; see the next two sections.

## Why the reference stays at 0.5.0

`openaq_pre_migration_reference.json` is a **historical record**, not a
mirror of the current tree, and it is deliberately not re-frozen at esm
1.0.0. The gate's whole job is to show that the pure-IO migration preserved
an interface that existed *before* it; a reference re-frozen at 1.0.0 would
be a copy of the file under test, so every comparison would pass by
construction. Keeping it at 0.5.0 keeps each assertion falsifiable.

The cost is that the driver script owns the vocabulary translation between
the two format versions. That translation is:

| esm 0.5.0 (frozen reference) | esm 1.0.0 (current corpus) |
|------------------------------|----------------------------|
| `data_loaders.OpenAQ_obs` | `data_sources.OpenAQ_obs` (document-scoped ingest registry, esm-spec §8) |
| `data_loaders.*.kind` / `.source` / `.temporal` | identical sub-blocks on the `data_sources` entry |
| `data_loaders.*.variables[v].file_variable` | `models.OpenAQ.variables[v].update.from.file_variable` |
| `data_loaders.*.variables[v].units` | `models.OpenAQ.variables[v].units` (units live on the consuming parameter) |
| `models.OpenAQ.variables.pm25` = `type: "observed"` + `expression: "OpenAQ_obs.pm25"` | `type: "parameter"` + `update: {kind: "data", source: "OpenAQ_obs", from: {…}}` — a consumed data field is a **parameter** at 1.0.0 |
| `data_loaders.*.spatial` | dropped; the geographic CRS is preserved as prose in the source's `metadata.native_crs` |
| `data_loaders.*.regridding.fill_value` | no schema home; recorded verbatim in `models.OpenAQ.reference.notes` (next section) |

The `type` strings are **not** compared directly: esm 1.0.0 collapsed
declared variable types to `unknown` and `parameter`, and `observed` /
`state` / `discrete` became DERIVED (esm-spec §6.3.1). Per AGENTS.md §1 the
driver takes every role from `earthsci_ast.classification`
(`parameters`, `discrete_parameters`, `constant_parameters`,
`observed_unknowns`, `observed_definitions`) rather than re-deriving it by
walking equations, and cross-checks the same two facts in the flattened IR
returned by `earthsci_ast.flatten`.

The reference is read as raw JSON, not through the runner: `earthsci_ast`
rejects major-0 documents outright (`SchemaValidationError`), which is
exactly why it is stored with a `.json` extension. That is the only place in
the driver that bypasses the runner, and only because no runner will load
it.

## Coverage lost at esm 1.0.0

The 0.5.0-era check asserted a **schema-validated** regrid contract: the
migrated model carried a per-variable `Model.regrid` map, `load_path()`
validated it, and the driver asserted `regrid.pm25.method` was a recognised
ESD kernel and `regrid.pm25.missing_value` matched the pre-migration
`regridding.fill_value`.

esm 0.8.0 removed `Model.regrid`, and esm 1.0.0 has no replacement in this
document. Per esm-spec §8.6 a data source performs no regridding; the
carrier of a regrid kernel is the `transform` field of a `variable_map`
entry on the **coupling edge** that consumes the field (§10.4/§10.5).
Neither `components/earthsci_data/openaq.esm` nor `consumer_openaq.esm`
declares such an edge, so there is no live, schema-validated regrid
structure anywhere in this repository to assert against. The migration
commit recorded the demoted map verbatim under
`models.OpenAQ.reference.notes` "instead of being dropped" — as prose.

The driver therefore **downgrades** the regrid checks from an interface
assertion to a **provenance assertion**, and labels them as such in its
output (`[4] … PROVENANCE, not a schema contract`). It recovers the recorded
JSON out of the notes and fails if the record is deleted, truncated, made
unparseable, stops covering exactly the data-bound fields, names an
unrecognised kernel, or drifts from `fill_value = 0.0`.

Stated plainly, what is **lost** relative to the 0.5.0-era check:

1. **Enforcement.** The check can no longer prove that any runtime will
   apply `cell_average` with `missing_value 0.0` to these fields — only
   that the intent is still on record. Nothing consumes the record.
2. **Schema validation of the kernel.** At 0.5.0–0.7.0 a malformed kernel
   name or a missing `missing_value` failed `load_path()` itself. Now the
   record is free text; the driver's own parse and kernel allow-list are
   the only validation.
3. **A stable structural anchor.** The recovery keys off the literal
   `` `regrid` (verbatim): `` marker in the notes. Reword that marker and
   the check reports the record as unrecoverable (a loud failure, not a
   silent pass — which is the intended failure direction).

This is acceptable because the lost coverage guarded a schema field that no
longer exists, and the coverage that replaced it — the `data_sources`
ingest binding (registry key, source kind, URL template, temporal cadence,
and each field's `file_variable` + units) — is *stronger* than what 0.5.0
could check, since at 0.5.0 those lived in a block the model did not have to
reference at all. Regaining full regrid enforcement requires authoring the
consuming coupling edge's `variable_map.transform`; no consumer in this rig
couples these fields yet, and coupling-edge content is out of scope for
this fixture (application-level pipelines are a downstream concern,
AGENTS.md §2). When such an edge is authored, `[4]` should be promoted back
to a structural assertion against it.

## Validation matrix (esm-3nc.6, 2026-06-25)

Validated against both the current CI ESS (`EarthSciAST@main`,
`_CURRENT_VERSION (0,4,0)`, schema `0.6.0`) and the **bumped** ESS
(`ess-v9a.7`: `_CURRENT_VERSION (0,7,0)`, schema `0.7.0`,
`reject_legacy_data_loader_shapes` active):

| Check | ESS main | ESS bumped (v9a.7) |
|-------|----------|--------------------|
| 35 migrated `components/earthsci_data/*.esm` load + resolve (gate) | 35/35 PASS | 35/35 PASS |
| 10 pre-migration legacy-shape files **rejected** (`data_loader_regridding_removed`) | n/a (pre-bump loads w/ warning) | 10/10 REJECTED |
| Consumer ref-include resolves + regrids + fields identical (to tol) | PASS | PASS |

The hard-break is internally consistent: migrated files load under the
bumped version gate (declared `esm 0.7.0` == library `0.7.0` after the
esm-aha stamp correction — they were originally stamped `esm 0.6.0`, which
loaded only via the lenient-downward check; no legacy `regridding`/`spatial`
blocks), while legacy files are rejected with the named diagnostic.

> **Stamp correction (esm-aha, 2026-06-26).** The 35 migrated
> `components/earthsci_data/*.esm` and the `consumer_openaq.esm` fixture
> declared `esm 0.6.0` while already using the `0.7.0` pure-IO shape (a
> latent mis-stamp: RFC §7 step-1 / `SCHEMA_CHANGE_PROCEDURE.md` require the
> new shape to declare the new schema version). They are now stamped
> `0.7.0`. Loads stay green (the matrix results above are unchanged); under
> the bumped ESS the declared version is now an exact match rather than a
> lenient-downward accept.

> **esm 1.0.0 (2026-08-20).** The matrix above is a frozen record of the
> 0.7.0 hard break; it is not a description of the tree today. Two things
> changed under it. (1) `data_loaders` became `data_sources`: a data source
> is no longer a component, so it is not a subsystem, not a coupling
> endpoint and not a scoped-name path root, and each former loader variable
> is now a **parameter on the consuming model** carrying
> `update: {kind: "data", source: "<registry key>", from: {file_variable, …}}`.
> `aq.pm25` therefore resolves to a parameter, not to a subsystem observed.
> (2) The `X.esm` / `X_loader.esm` split is gone. It existed only because a
> loader was a component and a `{"ref"}` target had to contain exactly one
> component; `data_sources` no longer counts toward a file's top-level
> system count, so `openaq.esm` now holds the OpenAQ model **and** the
> `OpenAQ_obs` source it consumes, and is still mountable by `{"ref"}` —
> which is exactly what `consumer_openaq.esm` proves. The 26 standalone
> `*_loader.esm` files are deleted; each one's own metadata is preserved
> verbatim under its registry entry's `metadata.merged_file_metadata`.
> `components/earthsci_data` is 14 files, not 35 or 40.

> **Driver realigned to esm 1.0.0.** The matrix and the two notes above
> describe the corpus; the driver script itself was left on the 0.5.0-era
> assertions until now, and had been red in the `consumer-e2e` CI job ever
> since the 1.0.0 migration (it asserted a `regrid` block that 0.8.0
> removed, and compared declared `type` strings across a version boundary
> that made `observed` non-declarable). It now reads every derived role from
> `earthsci_ast.classification`, compares the ingest binding across the
> `data_loaders` → `data_sources` rename, and treats the regrid map as a
> provenance record — see "Why the reference stays at 0.5.0" and "Coverage
> lost at esm 1.0.0" above.
