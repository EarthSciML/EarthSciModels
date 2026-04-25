# docs/ — EarthSciModels component catalog

This directory is the source for the **auto-generated component documentation
site** published at `https://earthsciml.github.io/EarthSciModels/`. The source
of truth remains the `.esm` files under [`components/`](../components) — this
site is a view over them.

## Stack

| Piece | Purpose |
| --- | --- |
| [`tools/esm_to_docs.py`](../tools/esm_to_docs.py) | Walks `components/**/*.esm`, writes one Hugo page per component (plus `docs/data/components-index.json`). SSG-agnostic: only the output format is Hugo-specific. |
| [Hugo](https://gohugo.io) | Static site generator; renders taxonomies and markdown. |
| [KaTeX](https://katex.org) | Client-side math rendering for rate laws / equations (loaded via CDN in `layouts/partials/head.html`). |
| [Pagefind](https://pagefind.app) | Client-side chunked search index built post-`hugo` in CI. Lazy-loads, no server required. |
| `.github/workflows/docs.yml` | Generate → build → index → deploy on every push to `main`. |

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
# Generate pages from .esm files.
python tools/esm_to_docs.py

# Run the generator's unit tests (AST → LaTeX renderer coverage).
python -m unittest tools/esm_to_docs_test.py

# Build the site (requires Hugo extended ≥ 0.131).
hugo --source docs --minify --destination public

# Serve locally with live reload.
hugo server --source docs

# Build Pagefind index (optional; the UI silently degrades without it).
npx pagefind@1 --site docs/public
```

Generated content (`docs/content/components/**/index.md`, `docs/data/components-index.json`,
`docs/public/`, `docs/resources/`) is gitignored; CI regenerates on every run.

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

## Example plots — path forward

Examples in the `.esm` schema carry declarative plot specs (`type: line` /
`heatmap`, axis labels, variable bindings — see
[ESS §5.4.11](https://github.com/EarthSciML/EarthSciSerialization)). The doc
generator will render static images alongside each example if artifacts are
shipped under the convention:

```
components/<domain>/[<subdomain>/]<name>.plots/<example_id>-<plot_id>.{png,svg,jpg,webp}
```

Artifacts are copied into `docs/static/plots/<slug>/` at generate time and
referenced from the rendered page. If no artifact exists for a given plot, the
example renders without a figure (no placeholder).

**Today, no `.esm` ships plot artifacts**, so examples render description-only.
Two follow-up options are tracked separately:

- **Runtime plot generation** — execute each example at CI time, integrate the
  model with the declared `parameter_sweep`, and emit a PNG. Requires wiring
  the Julia component back through `EarthSciModels.jl` at doc-build time.
- **Client-side interactive embeds** — render the plot spec as Vega-Lite /
  Plotly JSON and let the browser draw it from the integration result. Still
  needs a server-side evaluation step to produce the data.

Either option is a larger lift than this POC.

## Out of scope (tracked elsewhere)

- Connectors (not yet a distinct `.esm` section)
- Discretization rules (lives in ESD, not ESM)
- Versioned docs (history of a component across `.esm` versions)
- Runtime plot generation (see "Example plots — path forward" above)
- Algolia DocSearch swap (revisit only if we outgrow Pagefind at >10k pages)
- PDF export
