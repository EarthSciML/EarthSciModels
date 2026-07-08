# earthsci_data consumer e2e fixtures (bead esm-3nc.6)

End-to-end validation fixtures for the pure-IO data-loader migration
(RFC pure-io-data-loaders §6/§7; epic `esm-3nc`). They back the `esm-3nc.6`
acceptance: *a consumer file that ref-includes a migrated single-component
model resolves + regrids + produces fields identical (to tolerance) to the
pre-migration inline pipeline.*

## Files

| File | Role |
|------|------|
| `consumer_openaq.esm` | A downstream **consumer** model that `{"ref"}`-includes the migrated single-component model `components/earthsci_data/openaq.esm` as the subsystem `aq`, re-exposing the regridded field as `pm25_consumed ~ aq.pm25`. Exercises a two-level pure-IO loader ref chain (consumer → model → `openaq_loader.esm`). |
| `openaq_pre_migration_reference.json` | Frozen snapshot of the **pre-migration** OpenAQ (`esm 0.5.0`, co-located `data_loaders.OpenAQ_obs` with `regridding.fill_value = 0.0` + legacy `spatial`), captured from `origin/main` before the split. Stored as `.json` (not `.esm`) so no live `.esm` gate ever loads the legacy shape. The reference interface the migration must preserve. |

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
migration independent of data — is the **field interface + regrid intent**:
exposed variable names, types, units, and the regrid kernel + fill
semantics. That identity is what this check asserts, to tolerance.

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
