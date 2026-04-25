# docs/ — EarthSciModels component catalog

This directory is the source for the **auto-generated component documentation
site** published at `https://earthsciml.github.io/EarthSciModels/`. The source
of truth remains the `.esm` files under [`components/`](../components) — this
site is a view over them.

## Stack

| Piece | Purpose |
| --- | --- |
| [`tools/esm_to_docs.py`](../tools/esm_to_docs.py) | Walks `components/**/*.esm`, writes one Hugo page per component (plus `docs/data/components-index.json`). SSG-agnostic: only the output format is Hugo-specific. |
| [`tools/render_example_plots.py`](../tools/render_example_plots.py) | Walks `components/**/*.esm`, evaluates each example's `parameter_sweep`, and writes a PNG per declared plot under `<esm_dir>/<stem>.plots/`. `esm_to_docs.py` then inlines the artifacts on the rendered page. |
| [Hugo](https://gohugo.io) | Static site generator; renders taxonomies and markdown. |
| [KaTeX](https://katex.org) | Client-side math rendering for rate laws / equations (loaded via CDN in `layouts/partials/head.html`). |
| [Pagefind](https://pagefind.app) | Client-side chunked search index built post-`hugo` in CI. Lazy-loads, no server required. |
| `.github/workflows/docs.yml` | Generate plots → generate pages → build → index → deploy on every push to `main`. |

## Adding a new component

1. Drop the `.esm` file into `components/<domain>/[<subdomain>/]<name>.esm`.
2. Commit it. CI rebuilds and redeploys the catalog automatically — you do
   **not** touch the `docs/` tree for new components. `tools/esm_to_docs.py`
   discovers the file and generates the page.

The generator reads each top-level component (`models.*`, `reaction_systems.*`,
etc.) and emits sections for: description, reference, variables, parameters,
constants, observed expressions, equations, reactions (if any), examples,
and a collapsed raw JSON block. (Tests live in the `.esm` source for CI
validation but are intentionally not rendered on user-facing pages.)

Frontmatter fields set from the `.esm`:

- `title` — component name (dict key)
- `domain` / `subdomain` — derived from the file path under `components/`
- `component_type` — inferred from the schema section (`model`, `reaction_system`, …)
- `esm_version` — top-level `"esm"` field
- `esm_path` — repo-relative path back to the source
- `reference` — DOI / URL / citation (best match from the component reference)
- `tags` — domain + subdomain + type + any author-supplied tags

Taxonomies configured in `hugo.toml` (`domain`, `component_type`, `subdomain`,
`tag`) auto-generate faceted landing pages such as
`/domains/gaschem/` and `/component_types/model/`.

## Local development

```bash
# Render example plots from .esm files (requires matplotlib + numpy).
python tools/render_example_plots.py

# Generate pages from .esm files.
python tools/esm_to_docs.py

# Run the generators' unit tests.
python -m unittest tools/esm_to_docs_test.py
python -m unittest tools/render_example_plots_test.py

# Build the site (requires Hugo extended ≥ 0.131).
hugo --source docs --minify --destination public

# Serve locally with live reload.
hugo server --source docs

# Build Pagefind index (optional; the UI silently degrades without it).
npx pagefind@1 --site docs/public
```

Generated content (`docs/content/components/**/index.md`, `docs/data/components-index.json`,
`docs/public/`, `docs/resources/`, `components/**/*.plots/`) is gitignored; CI regenerates on
every run.

## Layout overview

```
docs/
├── hugo.toml                             # Hugo config + taxonomies
├── content/
│   ├── _index.md                          # landing page (hand-written)
│   ├── components/
│   │   ├── _index.md                      # catalog index (hand-written)
│   │   └── <domain>/<subdomain>/<name>/   # GENERATED
│   │       └── index.md
│   └── ...
├── layouts/
│   ├── _default/{baseof,list,single,terms}.html
│   └── partials/{head,header,footer}.html
├── static/
│   └── css/site.css                       # site styling
└── data/
    └── components-index.json              # GENERATED — faceted search feed
```

## Example plots

Examples in the `.esm` schema carry declarative plot specs (`type: line` /
`heatmap`, axis labels, variable bindings — see
[ESS §5.4.11](https://github.com/EarthSciML/EarthSciSerialization)). At
build time, [`tools/render_example_plots.py`](../tools/render_example_plots.py)
walks `components/**/*.esm`, evaluates each example's `parameter_sweep`,
and writes a PNG per declared plot under

```
components/<domain>/[<subdomain>/]<name>.plots/<example_id>-<plot_id>.png
```

`tools/esm_to_docs.py` then copies the artifact into `docs/static/plots/<slug>/`
and inlines it on the rendered page. The `.plots/` tree is gitignored — CI
regenerates it on every run. Custom hand-shipped artifacts for a specific
example are still supported by simply checking them into the same path
(but you'll need to remove the gitignore rule if you do).

### Coverage

Today the renderer handles **algebraic-only components**: a `model` whose
`equations` list is empty and whose state variables are computed entirely
from `observed` expressions over parameters. That covers the
`CloudAlbedo` Seinfeld & Pandis Fig 24.16 reproduction (mdl-icq) and any
future model in the same shape.

Examples that need an ODE/DAE integration (`reaction_systems`, models
with non-trivial `equations`, or examples without a `parameter_sweep` —
e.g. `SuperFast`'s 24-hour run, `DiameterGrowthRate`'s trajectory tests)
are skipped with a diagnostic line and tracked as a follow-up. Driving
them through MTK requires Julia + `EarthSciModels.jl` in the docs CI
image; the algebraic-only path runs in pure Python (`matplotlib +
numpy`) and adds ~1 s to the docs build per .esm.

### Build-time impact

For the current 6 components × ~25 example plots:

| Stage | Local time | Notes |
| --- | --- | --- |
| `pip install matplotlib numpy` | ~10–15 s | Cached across CI runs once the wheel is in place. |
| `python tools/render_example_plots.py` | ~1 s | Scales linearly in the number of algebraic examples × sweep grid size. |
| `python tools/esm_to_docs.py` | <0.5 s | Unchanged. |

The `Render example plots` step grows roughly proportional to the total
sweep grid count across all examples, but stays well under 10 s in
practice. If a future ODE-driven path lands, expect that step to dwarf
this one.

### Follow-up — interactive embeds

Tracked separately:

- **Client-side interactive embeds** — render the plot spec as Vega-Lite /
  Plotly JSON and let the browser draw it from the integration result.
  Still needs a server-side evaluation step to produce the data.
- **ODE/DAE plot rendering** — wire `EarthSciModels.jl` (Julia + MTK +
  Catalyst + a solver stack) into the docs CI to integrate
  `reaction_systems` and DAE models, then emit PNGs through the same
  `<esm_stem>.plots/` convention.

## Out of scope (tracked elsewhere)

- Connectors (not yet a distinct `.esm` section)
- Discretization rules (lives in ESD, not ESM)
- Versioned docs (history of a component across `.esm` versions)
- ODE/DAE plot rendering (see "Example plots → Follow-up" above)
- Algolia DocSearch swap (revisit only if we outgrow Pagefind at >10k pages)
- PDF export
