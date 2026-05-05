# docs/ — EarthSciModels component catalog

This directory is the source for the **auto-generated component documentation
site** published at `https://earthsciml.github.io/EarthSciModels/`. The source
of truth remains the `.esm` files under [`components/`](../components) — this
site is a view over them.

## Stack

| Piece | Purpose |
| --- | --- |
| [`tools/esm_to_docs.py`](../tools/esm_to_docs.py) | Walks `components/**/*.esm`, writes one Hugo page per component (plus `docs/data/components-index.json`). SSG-agnostic: only the output format is Hugo-specific. |
| [`tools/render_example_plots.py`](../tools/render_example_plots.py) | Walks `components/**/*.esm`, evaluates each example via the `parameter_sweep` path (algebraic models) or via the canonical Python ESS runner (`earthsci_toolkit.simulation.simulate`) (ODE models with `time_span` + `initial_state`), and writes a PNG per declared plot under `<esm_dir>/<stem>.plots/`. `esm_to_docs.py` then inlines the artifacts on the rendered page. |
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
walks `components/**/*.esm`, evaluates each example (cartesian
`parameter_sweep` for algebraic models, or via the canonical Python ESS
runner (`earthsci_toolkit.simulation.simulate`) of `time_span` +
`initial_state` for ODE models), and writes a PNG per declared plot under

```
components/<domain>/[<subdomain>/]<name>.plots/<example_id>-<plot_id>.png
```

`tools/esm_to_docs.py` then copies the artifact into `docs/static/plots/<slug>/`
and inlines it on the rendered page. The `.plots/` tree is gitignored — CI
regenerates it on every run. Custom hand-shipped artifacts for a specific
example are still supported by simply checking them into the same path
(but you'll need to remove the gitignore rule if you do).

### Coverage

The renderer handles two example shapes:

- **Algebraic models** (no `D` op in `equations`) drive the cartesian
  `parameter_sweep` path: each grid point is evaluated through ESS and
  fed to one PNG per declared plot. Covers `CloudAlbedo`,
  `WaterEquilibrium`, `DropletGrowth`, `AerosolScavenging`, etc.
- **ODE models** (one or more `D(state)/dt = rhs` equations) drive the
  time-series path when the example carries `time_span` + `initial_state`
  (`per_variable` form). Each example integrates via the canonical Python
  ESS runner (`earthsci_toolkit.simulation.simulate`) and emits one PNG
  per plot of state/algebraic trajectories vs `t`. A
  1-D `parameter_sweep` is allowed and produces a family of curves on
  one axes (one integration per grid point). Covers
  `DiameterGrowthRate`'s Fig. 13.2 reproductions (mdl-hxx).

Reaction systems (`reaction_systems`), DAE-only models (algebraics that
won't reduce to forward-defined targets), and examples missing both
`parameter_sweep` and `initial_state` are skipped with a diagnostic
line. Both supported paths run in pure Python (`matplotlib`, `numpy`,
`scipy`) and add ~1 s per .esm to the docs build.

### Build-time impact

For the current 6 components × ~25 example plots:

| Stage | Local time | Notes |
| --- | --- | --- |
| `pip install matplotlib numpy scipy` | ~10–15 s | Cached across CI runs once the wheels are in place. |
| `python tools/render_example_plots.py` | <20 s | Algebraic examples scale with sweep grid size; ODE examples scale with the canonical-runner integration cost. |
| `python tools/esm_to_docs.py` | <0.5 s | Unchanged. |

The `Render example plots` step grows roughly proportional to the total
sweep grid count plus the integration time of any ODE examples, but
stays well under 30 s in practice for the current component set.

### Follow-up — interactive embeds

Tracked separately:

- **Client-side interactive embeds** — render the plot spec as Vega-Lite /
  Plotly JSON and let the browser draw it from the integration result.
  Still needs a server-side evaluation step to produce the data.
- **`reaction_systems` + DAE-only rendering** — pure-Python ODE coverage
  landed in mdl-hxx, but `reaction_systems` and DAE models with
  irreducible algebraics still skip. Wiring `EarthSciModels.jl` (Julia +
  MTK + Catalyst + a solver stack) into the docs CI would close the
  remaining gap through the same `<esm_stem>.plots/` convention.

## Out of scope (tracked elsewhere)

- Connectors (not yet a distinct `.esm` section)
- Discretization rules (lives in ESD, not ESM)
- Versioned docs (history of a component across `.esm` versions)
- `reaction_systems` and DAE-only plot rendering (see "Example plots → Follow-up" above)
- Algolia DocSearch swap (revisit only if we outgrow Pagefind at >10k pages)
- PDF export
