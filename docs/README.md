# docs/ — EarthSciModels component catalog

This directory is the source for the **auto-generated component documentation
site** published as part of [earthsci.dev](https://earthsci.dev/models/). The source
of truth remains the `.esm` files under [`components/`](../components) — this
site is a view over them.

## Stack

| Piece | Purpose |
| --- | --- |
| [`tools/esm_to_docs.py`](../tools/esm_to_docs.py) | Walks `components/**/*.esm`, writes one Hugo page per component (plus `docs/data/components-index.json`). SSG-agnostic: only the output format is Hugo-specific. |
| [`tools/render_example_plots.jl`](../tools/render_example_plots.jl) | Walks `components/**/*.esm`, evaluates each analysis through the canonical Julia runner (`EarthSciAST.esm_problem` + SciML `solve`; a `parameter_sweep` grid for algebraic components, integrations over `time_span` for ODE components), and writes a PNG per declared plot under `<esm_dir>/<stem>.plots/`. `esm_to_docs.py` then inlines the artifacts on the rendered page. Its environment is [`tools/plots/`](../tools/plots/Project.toml). |
| [Hugo](https://gohugo.io) | Static site generator. The Hugo config, layouts and CSS live in [EarthSciML/earthsci.dev](https://github.com/EarthSciML/earthsci.dev), not here. |
| [KaTeX](https://katex.org) | Client-side math rendering for rate laws / equations (loaded by the earthsci.dev layouts). |
| [Pagefind](https://pagefind.app) | Client-side chunked search index built post-`hugo` by the earthsci.dev build. Lazy-loads, no server required. |
| `.github/workflows/docs.yml` | Generate plots → generate pages → publish the `docs-bundle` branch → notify earthsci.dev, which builds, indexes and deploys the full site. |

## Adding a new component

1. Drop the `.esm` file into `components/<domain>/[<subdomain>/]<name>.esm`.
2. Commit it. CI rebuilds and redeploys the catalog automatically — you do
   **not** touch the `docs/` tree for new components. `tools/esm_to_docs.py`
   discovers the file and generates the page.

The generator reads each top-level component (`models.*`, `reaction_systems.*`,
`data_sources.*`) and emits sections for: description, reference, variables,
parameters, observed + observed expressions, equations, reactions (if any),
the data-source I/O descriptor (if any), analyses, and a collapsed raw JSON
block. (Tests live in the `.esm` source for CI validation but are
intentionally not rendered on user-facing pages.)

The Variables / Observed split is **derived**, not declared: from esm 1.0.0
the only declared variable types are `unknown` and `parameter`, and
`earthsci_ast.classification` (esm-spec §6.3.1) is what tells the generator
which unknowns are ODE states, which are observed, and which are algebraic.
"Variables" is the ODE states plus the algebraic unknowns; "Observed" is the
unknowns some equation defines with a bare-variable LHS, and "Observed
expressions" renders those defining right-hand sides.

Frontmatter fields set from the `.esm`:

- `title` — component name (dict key)
- `domain` / `subdomain` — derived from the file path under `components/`
- `component_type` — inferred from the schema section (`model`, `reaction_system`, …)
- `esm_version` — top-level `"esm"` field
- `esm_path` — repo-relative path back to the source
- `reference` — DOI / URL / citation (best match from the component reference)
- `tags` — domain + subdomain + type + any author-supplied tags

Taxonomies configured in earthsci.dev's `hugo.toml` (`domain`, `component_type`, `subdomain`,
`tag`) auto-generate faceted landing pages such as
`/domains/gaschem/` and `/component_types/model/`.

## Local development

```bash
# Render example plots from .esm files (Julia 1.12+; the first run
# instantiates and precompiles tools/plots, which takes several minutes).
julia --project=tools/plots -e 'using Pkg; Pkg.instantiate()'
julia --project=tools/plots tools/render_example_plots.jl
# ...or just some files:
julia --project=tools/plots tools/render_example_plots.jl --files components/gaschem/superfast.esm

# Generate pages from .esm files.
python tools/esm_to_docs.py

# Run the generators' unit tests.
python -m unittest tools/esm_to_docs_test.py
julia --project=tools/plots tools/render_example_plots_test.jl

# Preview: the site is built by earthsci.dev (Python 3.11+, Hugo extended >= 0.131).
git clone https://github.com/EarthSciML/earthsci.dev ../earthsci.dev
python ../earthsci.dev/tools/bundle.py --repo-root . --out ../earthsci.dev/build/bundles/models
python ../earthsci.dev/tools/assemble.py --local models=../earthsci.dev/build/bundles/models --only models
hugo server --source ../earthsci.dev

```

Generated content (`docs/content/components/**/index.md`, `docs/data/components-index.json`,
`docs/public/`, `docs/resources/`, `components/**/*.plots/`) is gitignored; CI regenerates on
every run.

## Layout overview

```
docs/
├── site.toml                             # project metadata for earthsci.dev
├── content/
│   ├── _index.md                          # landing page (hand-written)
│   ├── components/
│   │   ├── _index.md                      # catalog index (hand-written)
│   │   └── <domain>/<subdomain>/<name>/   # GENERATED
│   │       └── index.md
│   └── ...
├── static/                               # (plots land in static/plots, generated)
└── data/
    └── components-index.json              # GENERATED — faceted search feed
```

## Analysis plots

Analyses in the `.esm` schema (esm-spec §6.7 — the 1.0.0 spelling of what 0.x
called `examples`) carry declarative plot specs (`type: line` /
`heatmap`, axis labels, variable bindings — see
[ESS §5.4.11](https://github.com/EarthSciML/EarthSciAST)). At
build time, [`tools/render_example_plots.jl`](../tools/render_example_plots.jl)
walks `components/**/*.esm`, evaluates each analysis through the canonical
Julia runner (`EarthSciAST.esm_problem` + SciML `solve`), and writes a PNG
per declared plot under

```
components/<domain>/[<subdomain>/]<name>.plots/<analysis_id>-<plot_id>.png
```

`tools/esm_to_docs.py` then copies the artifact into `docs/static/plots/<slug>/`
and inlines it on the rendered page. The `.plots/` tree is gitignored — CI
regenerates it on every run. Custom hand-shipped artifacts for a specific
analysis are still supported by simply checking them into the same path
(but you'll need to remove the gitignore rule if you do).

### Coverage

Each component (model or reaction system) is built once with
`esm_problem`; every analysis on it reuses that build, and `remake` swaps
parameter values between sweep points without recompiling. The renderer
handles two analysis shapes:

- **Algebraic components** (the built problem has no state) drive the
  cartesian `parameter_sweep` path: each grid point's observed values are
  read with `observed_field` and fed to one PNG per declared plot (`line`
  and `scatter` for a 1-D sweep, `heatmap` for a 2-D one).
- **ODE components** drive the time-series path: one integration over
  `time_span` (or one per point of a 1-D `parameter_sweep`), starting from
  the states' declared defaults overridden by `initial_state` (either the
  flat scalar map or the esm-spec §11.4 `{type, values}` union). A `line`
  plot with `x = t` draws the trajectories; one whose `x` is the swept
  parameter draws each trajectory's final value against the sweep. The
  integrator is FBDF (Rodas5P as a fallback) at `reltol = 1e-8`,
  `abstol = 1e-12`.

Analyses missing both `parameter_sweep` and `initial_state` on an algebraic
component, 2-D sweeps of ODE components, `field_snapshot` / `field_slice`
plots, and anything the runner refuses to build or evaluate are skipped
with a `[skip]` line naming the reason.

### Build-time impact

Measured on the full corpus (497 `.esm` files, 817 plots), one process on a
shared workstation:

| Stage | Time | Notes |
| --- | --- | --- |
| `Pkg.instantiate()` + precompile of `tools/plots` | ~5 min cold | Cached across CI runs by `julia-actions/cache`; only EarthSciAST recompiles when its `main` moves. |
| `julia --project=tools/plots tools/render_example_plots.jl` | ~22 min | Mostly per-component compilation (a few seconds per document). `geoschem_fullchem.esm`, which took ~5 h under the old Python/LSODA renderer, is ~80 s including its build. |
| `python tools/esm_to_docs.py` | <0.5 s | Unchanged. |

### Follow-up — interactive embeds

Tracked separately:

- **Client-side interactive embeds** — render the plot spec as Vega-Lite /
  Plotly JSON and let the browser draw it from the integration result.
  Still needs a server-side evaluation step to produce the data.
- **PDE / field plots** — `field_snapshot` and `field_slice` plots, and
  documents whose spatial operators need an EarthSciDiscretizations stencil
  (`${ESD_ROOT}`, which the docs job does not clone), are still skipped.

## Out of scope (tracked elsewhere)

- Connectors (not yet a distinct `.esm` section)
- Discretization rules (lives in ESD, not ESM)
- Versioned docs (history of a component across `.esm` versions)
- PDE / field plot rendering (see "Analysis plots → Follow-up" above)
- Algolia DocSearch swap (revisit only if we outgrow Pagefind at >10k pages)
- PDF export
