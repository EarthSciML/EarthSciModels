#!/usr/bin/env python3
"""
esm_to_docs — turn `components/**/*.esm` files into Hugo markdown pages.

One `.esm` may contain multiple entries (models, reaction_systems, ...); each
top-level entry becomes one page under `docs/content/components/<path>/<name>/`.

The generator also writes `docs/data/components-index.json` for faceted search
feeds and other downstream consumers (SSG-agnostic).

Entry points:
    python tools/esm_to_docs.py                         # from repo root
    python tools/esm_to_docs.py --repo-root <path> --out <docs_content_dir>
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable


# ---------------------------------------------------------------------------
# AST → LaTeX renderer
# ---------------------------------------------------------------------------

# Operator precedence (higher binds tighter).
_PREC_ATOM = 100
_PREC_POW = 80
_PREC_MUL = 60
_PREC_ADD = 40
_PREC_LOW = 0


def _fmt_number(n: int | float) -> str:
    """Format a numeric literal as LaTeX. Scientific notation for very small/large."""
    if isinstance(n, bool):
        # Python's bool is a subclass of int; treat specially (unlikely in .esm but safe).
        return "1" if n else "0"
    if isinstance(n, int):
        if n < 0:
            return f"-{-n}"
        return str(n)
    # float
    if n != n:  # NaN
        return r"\mathrm{NaN}"
    if n == float("inf"):
        return r"\infty"
    if n == float("-inf"):
        return r"-\infty"
    # Use Python's repr, then convert to LaTeX sci notation if present.
    s = repr(n)
    if "e" in s or "E" in s:
        mantissa, _, exp = s.lower().partition("e")
        exp_i = int(exp)
        # Drop trailing ".0" on whole-number mantissas.
        if mantissa.endswith(".0"):
            mantissa = mantissa[:-2]
        return f"{mantissa} \\times 10^{{{exp_i}}}"
    return s


def _fmt_varname(name: str) -> str:
    """Render a variable name as LaTeX. First underscore becomes subscript.

    We avoid LaTeX ``\\_`` escapes for subsequent underscores because Goldmark
    (Hugo's Markdown renderer) treats ``\\_`` as a backslash-escape for the
    punctuation character ``_`` and silently strips the backslash, which would
    then let KaTeX re-parse the bare ``_`` as a nested subscript. We use a
    thin-space separator instead, which is safe through both Markdown and KaTeX.
    """
    if "_" not in name:
        return name
    head, _, tail = name.partition("_")
    tail = tail.replace("_", r"\,")
    return f"{head}_{{{tail}}}"


# NOTE: avoid ``\!`` (negative thin space) in these templates — Goldmark would
# strip the backslash because ``!`` is an ASCII-punctuation escape character,
# which leaves a literal ``!`` in the HTML that KaTeX cannot parse.
_UNARY_FUNCS = {
    "exp": lambda inner: f"e^{{{inner}}}",
    "log": lambda inner: f"\\ln\\left({inner}\\right)",
    "log10": lambda inner: f"\\log_{{10}}\\left({inner}\\right)",
    "log2": lambda inner: f"\\log_{{2}}\\left({inner}\\right)",
    "sqrt": lambda inner: f"\\sqrt{{{inner}}}",
    "sin": lambda inner: f"\\sin\\left({inner}\\right)",
    "cos": lambda inner: f"\\cos\\left({inner}\\right)",
    "tan": lambda inner: f"\\tan\\left({inner}\\right)",
    "abs": lambda inner: f"\\left|{inner}\\right|",
}


@dataclass
class _Rendered:
    text: str
    prec: int


def _render(node: Any, parent_prec: int = _PREC_LOW) -> str:
    r = _render_inner(node)
    if r.prec < parent_prec:
        return f"\\left({r.text}\\right)"
    return r.text


def _render_inner(node: Any) -> _Rendered:
    # Atoms.
    if node is None:
        return _Rendered(r"\varnothing", _PREC_ATOM)
    if isinstance(node, bool):
        return _Rendered("1" if node else "0", _PREC_ATOM)
    if isinstance(node, (int, float)):
        text = _fmt_number(node)
        # A negative atom has effectively unary-minus precedence for bracketing.
        prec = _PREC_ADD if text.startswith("-") or text.startswith("\\-") else _PREC_ATOM
        return _Rendered(text, prec)
    if isinstance(node, str):
        return _Rendered(_fmt_varname(node), _PREC_ATOM)

    if not isinstance(node, dict):
        # Defensive: render anything else as a fenced literal.
        return _Rendered(f"\\mathrm{{{json.dumps(node)}}}", _PREC_ATOM)

    op = node.get("op")
    args = node.get("args", [])
    if op is None:
        return _Rendered(r"\mathrm{?}", _PREC_ATOM)

    # Function-style unary ops.
    if op in _UNARY_FUNCS and len(args) == 1:
        inner = _render(args[0], _PREC_LOW)
        return _Rendered(_UNARY_FUNCS[op](inner), _PREC_ATOM)

    if op == "/":
        if len(args) == 2:
            num = _render(args[0], _PREC_LOW)
            den = _render(args[1], _PREC_LOW)
            return _Rendered(f"\\frac{{{num}}}{{{den}}}", _PREC_ATOM)
        # N-ary division folds left: a / b / c = (a/b)/c.
        if len(args) > 2:
            acc = _render(args[0], _PREC_LOW)
            for a in args[1:]:
                nxt = _render(a, _PREC_LOW)
                acc = f"\\frac{{{acc}}}{{{nxt}}}"
            return _Rendered(acc, _PREC_ATOM)

    if op == "*":
        if not args:
            return _Rendered("1", _PREC_ATOM)
        parts = [_render(a, _PREC_MUL) for a in args]
        return _Rendered(" \\cdot ".join(parts), _PREC_MUL)

    if op == "+":
        if not args:
            return _Rendered("0", _PREC_ATOM)
        if len(args) == 1:
            return _Rendered(_render(args[0], _PREC_ADD), _PREC_ADD)
        parts = [_render(a, _PREC_ADD) for a in args]
        return _Rendered(" + ".join(parts), _PREC_ADD)

    if op == "-":
        if len(args) == 1:
            inner = _render(args[0], _PREC_MUL)
            return _Rendered(f"-{inner}", _PREC_ADD)
        if len(args) >= 2:
            first = _render(args[0], _PREC_ADD)
            rest = [_render(a, _PREC_MUL) for a in args[1:]]
            return _Rendered(first + "".join(" - " + r for r in rest), _PREC_ADD)

    if op == "^":
        if len(args) == 2:
            base = _render(args[0], _PREC_POW + 1)  # right-assoc: tighten the base
            exp = _render(args[1], _PREC_LOW)
            return _Rendered(f"{base}^{{{exp}}}", _PREC_POW)

    if op == "==":
        if len(args) == 2:
            left = _render(args[0], _PREC_LOW)
            right = _render(args[1], _PREC_LOW)
            return _Rendered(f"{left} = {right}", _PREC_LOW)

    if op == "apply_expression_template":
        name = node.get("name", "?")
        bindings = node.get("bindings", {}) or {}
        parts = [f"{_fmt_varname(k)}={_render(v, _PREC_LOW)}" for k, v in bindings.items()]
        return _Rendered(f"\\mathrm{{{name}}}\\left({', '.join(parts)}\\right)", _PREC_ATOM)

    # Unknown op — emit as \op(args, ...).
    rendered_args = ", ".join(_render(a, _PREC_LOW) for a in args)
    return _Rendered(f"\\mathrm{{{op}}}\\left({rendered_args}\\right)", _PREC_ATOM)


def ast_to_latex(node: Any) -> str:
    """Public entry point: render an .esm expression AST as a LaTeX string."""
    return _render(node, _PREC_LOW)


# ---------------------------------------------------------------------------
# .esm file walking & page emission
# ---------------------------------------------------------------------------


# Top-level schema sections that describe a single component we render a page for.
_COMPONENT_SECTIONS = (
    "models",
    "reaction_systems",
    "operators",
    "data_loaders",
    "coupling",
    "interfaces",
)


@dataclass
class ComponentEntry:
    """One renderable component extracted from a .esm file."""

    section: str            # e.g. "models", "reaction_systems"
    name: str               # the dict key, e.g. "SuperFast"
    body: dict              # the dict value
    esm_path: Path          # path to the source .esm file, repo-relative
    esm_version: str        # the top-level "esm" field (often "0.1.0")
    file_metadata: dict     # top-level "metadata" block (may be empty)

    @property
    def domain(self) -> str:
        """First path segment below components/ (e.g. 'gaschem', 'aerosol')."""
        parts = self.esm_path.parts
        if parts and parts[0] == "components" and len(parts) >= 2:
            return parts[1]
        return "unknown"

    @property
    def subdomain(self) -> str:
        """Optional second segment (e.g. 'cloud_physics'). Empty if file is directly under the domain."""
        parts = self.esm_path.parts
        if len(parts) >= 4 and parts[0] == "components":
            return parts[2]
        return ""

    @property
    def slug(self) -> str:
        """Stable URL slug: domain/[subdomain/]name (lowercased)."""
        parts = [self.domain]
        if self.subdomain:
            parts.append(self.subdomain)
        parts.append(self.name.lower())
        return "/".join(parts)

    @property
    def title(self) -> str:
        return self.name

    @property
    def type_label(self) -> str:
        """Human-facing component type derived from the .esm section."""
        return {
            "models": "model",
            "reaction_systems": "reaction_system",
            "operators": "operator",
            "data_loaders": "data_loader",
            "coupling": "coupling",
            "interfaces": "interface",
        }.get(self.section, self.section)


def discover_esm_files(components_root: Path) -> list[Path]:
    """Walk a components/ directory and return all .esm files sorted for determinism."""
    return sorted(p for p in components_root.rglob("*.esm") if p.is_file())


def parse_esm(path: Path, repo_root: Path) -> list[ComponentEntry]:
    """Parse one .esm file and emit one ComponentEntry per top-level component."""
    with path.open("r", encoding="utf-8") as fp:
        data = json.load(fp)
    rel = path.relative_to(repo_root)
    esm_version = data.get("esm", "")
    file_metadata = data.get("metadata") or {}
    entries: list[ComponentEntry] = []
    for section in _COMPONENT_SECTIONS:
        block = data.get(section)
        if not isinstance(block, dict):
            continue
        for name, body in block.items():
            if not isinstance(body, dict):
                continue
            entries.append(
                ComponentEntry(
                    section=section,
                    name=name,
                    body=body,
                    esm_path=rel,
                    esm_version=esm_version,
                    file_metadata=file_metadata,
                )
            )
    return entries


# ---------------------------------------------------------------------------
# Frontmatter + body emission
# ---------------------------------------------------------------------------


def _yaml_scalar(value: Any) -> str:
    """Emit a safe YAML scalar. Never attempt complex structures here."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return repr(value)
    # Strings: always double-quote with JSON-style escapes (safe under YAML 1.2).
    return json.dumps(str(value), ensure_ascii=False)


def _yaml_list(values: Iterable[Any]) -> str:
    out = "[" + ", ".join(_yaml_scalar(v) for v in values) + "]"
    return out


def _collect_tags(entry: ComponentEntry) -> list[str]:
    """Tags for faceted search: domain, subdomain (if any), type, and any author-supplied tags."""
    tags: list[str] = []
    seen: set[str] = set()

    def add(t: str) -> None:
        if not t:
            return
        if t in seen:
            return
        seen.add(t)
        tags.append(t)

    add(entry.domain)
    if entry.subdomain:
        add(entry.subdomain)
    add(entry.type_label)
    meta_tags = entry.file_metadata.get("tags") or []
    if isinstance(meta_tags, list):
        for t in meta_tags:
            if isinstance(t, str):
                add(t)
    body_tags = entry.body.get("tags") or []
    if isinstance(body_tags, list):
        for t in body_tags:
            if isinstance(t, str):
                add(t)
    return tags


def _first_reference_url(entry: ComponentEntry) -> str:
    """Best-effort extraction of a DOI/URL for the reference frontmatter field."""
    ref = entry.body.get("reference") or {}
    if isinstance(ref, dict):
        for key in ("doi", "url", "citation"):
            v = ref.get(key)
            if isinstance(v, str) and v.strip():
                return v.strip()
    refs = entry.file_metadata.get("references") or []
    if isinstance(refs, list) and refs:
        first = refs[0]
        if isinstance(first, dict):
            for key in ("doi", "url", "citation"):
                v = first.get(key)
                if isinstance(v, str) and v.strip():
                    return v.strip()
    return ""


def _description(entry: ComponentEntry) -> str:
    desc = entry.body.get("description")
    if isinstance(desc, str) and desc.strip():
        return desc.strip()
    fd = entry.file_metadata.get("description")
    if isinstance(fd, str):
        return fd.strip()
    return ""


def _frontmatter(entry: ComponentEntry) -> str:
    tags = _collect_tags(entry)
    ref = _first_reference_url(entry)
    desc = _description(entry)
    # Keep one-line descriptions so YAML stays clean.
    desc_line = desc.splitlines()[0] if desc else ""

    lines = ["---"]
    lines.append(f"title: {_yaml_scalar(entry.title)}")
    lines.append(f"slug: {_yaml_scalar(entry.name.lower())}")
    # Plural-list forms so Hugo's taxonomy walker picks them up.
    lines.append(f"domains: {_yaml_list([entry.domain])}")
    lines.append(f"component_types: {_yaml_list([entry.type_label])}")
    if entry.subdomain:
        lines.append(f"subdomains: {_yaml_list([entry.subdomain])}")
    # Singular scalars for convenient layout access (sibling to the lists).
    lines.append(f"domain: {_yaml_scalar(entry.domain)}")
    if entry.subdomain:
        lines.append(f"subdomain: {_yaml_scalar(entry.subdomain)}")
    lines.append(f"component_type: {_yaml_scalar(entry.type_label)}")
    lines.append(f"esm_version: {_yaml_scalar(entry.esm_version)}")
    lines.append(f"esm_path: {_yaml_scalar(str(entry.esm_path))}")
    if ref:
        lines.append(f"reference: {_yaml_scalar(ref)}")
    if desc_line:
        lines.append(f"description: {_yaml_scalar(desc_line)}")
    lines.append(f"tags: {_yaml_list(tags)}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def _section(title: str, body: str) -> str:
    if not body.strip():
        return ""
    return f"\n## {title}\n\n{body.strip()}\n"


def _render_description_section(entry: ComponentEntry) -> str:
    desc = _description(entry)
    return _section("Description", desc) if desc else ""


def _render_reference_section(entry: ComponentEntry) -> str:
    ref = entry.body.get("reference") or {}
    if not isinstance(ref, dict) or not ref:
        # Fall back to file-level references list if present.
        refs = entry.file_metadata.get("references") or []
        if isinstance(refs, list) and refs:
            parts = []
            for r in refs:
                if isinstance(r, dict):
                    citation = r.get("citation") or r.get("url") or r.get("doi") or ""
                    if citation:
                        parts.append(f"- {citation}")
            if parts:
                return _section("Reference", "\n".join(parts))
        return ""
    parts = []
    citation = ref.get("citation")
    if citation:
        parts.append(f"{citation}")
    notes = ref.get("notes")
    if notes:
        parts.append("")
        parts.append(f"_{notes}_")
    for key in ("doi", "url"):
        v = ref.get(key)
        if v:
            parts.append(f"- **{key.upper()}**: {v}")
    return _section("Reference", "\n".join(parts))


def _render_variable_table(title: str, variables: dict, include_kinds: Iterable[str]) -> str:
    rows = []
    include = set(include_kinds)
    for name, spec in variables.items():
        if not isinstance(spec, dict):
            continue
        kind = spec.get("type", "variable")
        if kind not in include:
            continue
        units = spec.get("units", "")
        default = spec.get("default", "")
        desc = (spec.get("description") or "").replace("|", r"\|")
        name_fmt = f"`{name}`"
        units_fmt = f"`{units}`" if units else ""
        default_fmt = f"`{default}`" if default != "" else ""
        rows.append(f"| {name_fmt} | {units_fmt} | {default_fmt} | {desc} |")
    if not rows:
        return ""
    header = "| Name | Units | Default | Description |\n| --- | --- | --- | --- |\n"
    return _section(title, header + "\n".join(rows))


def _render_expression_list(title: str, variables: dict) -> str:
    lines = []
    for name, spec in variables.items():
        if not isinstance(spec, dict):
            continue
        if spec.get("type") != "observed":
            continue
        expr = spec.get("expression")
        if expr is None:
            continue
        latex = ast_to_latex(expr)
        name_latex = _fmt_varname(name)
        desc = spec.get("description") or ""
        lines.append(f"$$\n{name_latex} = {latex}\n$$")
        if desc:
            lines.append(f"_{desc}_")
        lines.append("")
    if not lines:
        return ""
    return _section(title, "\n".join(lines).rstrip())


def _render_variables_sections(entry: ComponentEntry) -> str:
    variables = entry.body.get("variables") or {}
    if not isinstance(variables, dict) or not variables:
        return ""
    out = []
    vars_tbl = _render_variable_table("Variables", variables, include_kinds={"variable", "state"})
    params_tbl = _render_variable_table("Parameters", variables, include_kinds={"parameter"})
    const_tbl = _render_variable_table("Constants", variables, include_kinds={"constant"})
    observed_tbl = _render_variable_table("Observed", variables, include_kinds={"observed"})
    observed_exprs = _render_expression_list("Observed expressions", variables)
    for s in (vars_tbl, params_tbl, const_tbl, observed_tbl, observed_exprs):
        if s:
            out.append(s)
    return "".join(out)


def _render_parameters_section(entry: ComponentEntry) -> str:
    """reaction_systems use a separate `parameters` dict (not `variables`)."""
    params = entry.body.get("parameters")
    if not isinstance(params, dict) or not params:
        return ""
    rows = []
    for name, spec in params.items():
        if not isinstance(spec, dict):
            continue
        units = spec.get("units", "")
        default = spec.get("default", "")
        desc = (spec.get("description") or "").replace("|", r"\|")
        units_fmt = f"`{units}`" if units else ""
        default_fmt = f"`{default}`" if default != "" else ""
        rows.append(f"| `{name}` | {units_fmt} | {default_fmt} | {desc} |")
    if not rows:
        return ""
    header = "| Name | Units | Default | Description |\n| --- | --- | --- | --- |\n"
    return _section("Parameters", header + "\n".join(rows))


def _render_species_section(entry: ComponentEntry) -> str:
    species = entry.body.get("species")
    if not isinstance(species, dict) or not species:
        return ""
    rows = []
    for name, spec in species.items():
        if not isinstance(spec, dict):
            continue
        units = spec.get("units", "")
        default = spec.get("default", "")
        constant = spec.get("constant", False)
        desc = (spec.get("description") or "").replace("|", r"\|")
        flag = "yes" if constant else ""
        units_fmt = f"`{units}`" if units else ""
        default_fmt = f"`{default}`" if default != "" else ""
        rows.append(f"| `{name}` | {units_fmt} | {default_fmt} | {flag} | {desc} |")
    if not rows:
        return ""
    header = (
        "| Species | Units | Default | Constant | Description |\n"
        "| --- | --- | --- | --- | --- |\n"
    )
    return _section("Species", header + "\n".join(rows))


def _render_equations_section(entry: ComponentEntry) -> str:
    equations = entry.body.get("equations")
    if not isinstance(equations, list) or not equations:
        return ""
    blocks = []
    for i, eq in enumerate(equations):
        if not isinstance(eq, dict):
            continue
        lhs = eq.get("lhs")
        rhs = eq.get("rhs")
        if lhs is None and rhs is None:
            continue
        lhs_tex = ast_to_latex(lhs) if lhs is not None else ""
        rhs_tex = ast_to_latex(rhs) if rhs is not None else ""
        blocks.append(f"$$\n{lhs_tex} = {rhs_tex}\n$$")
    if not blocks:
        return ""
    return _section("Equations", "\n\n".join(blocks))


def _render_expression_templates_section(entry: ComponentEntry) -> str:
    """Render declared expression_templates so reaction rates that
    `apply_expression_template(name, ...)` are self-documenting.

    Template schema (per .esm spec): ``{name: {"params": [..], "body": <AST>}}``.
    Body params appear as plain variable names in the AST and pass through the
    standard LaTeX renderer.
    """
    templates = entry.body.get("expression_templates")
    if not isinstance(templates, dict) or not templates:
        return ""
    blocks = []
    for name, spec in templates.items():
        if not isinstance(spec, dict):
            continue
        params = spec.get("params") or []
        body = spec.get("body")
        block = [f"### `{name}`"]
        if isinstance(params, list) and params:
            params_str = ", ".join(f"`{p}`" for p in params)
            block.append(f"**Parameters:** {params_str}")
        if body is not None:
            latex = ast_to_latex(body)
            block.append(f"$$\n{latex}\n$$")
        blocks.append("\n\n".join(block))
    if not blocks:
        return ""
    return _section("Expression Templates", "\n\n".join(blocks))


def _render_reactions_section(entry: ComponentEntry) -> str:
    reactions = entry.body.get("reactions")
    if not isinstance(reactions, list) or not reactions:
        return ""
    rows = []
    for r in reactions:
        if not isinstance(r, dict):
            continue
        rid = r.get("id", "")
        subs = _format_reaction_side(r.get("substrates") or [])
        prods = _format_reaction_side(r.get("products") or [])
        rate = ast_to_latex(r.get("rate")) if r.get("rate") is not None else ""
        rows.append(f"| `{rid}` | {subs} | → | {prods} | $${rate}$$ |")
    if not rows:
        return ""
    header = (
        "| ID | Substrates | | Products | Rate |\n"
        "| --- | --- | --- | --- | --- |\n"
    )
    return _section("Reactions", header + "\n".join(rows))


def _format_reaction_side(side: list) -> str:
    parts = []
    for item in side:
        if not isinstance(item, dict):
            continue
        sp = item.get("species", "")
        stoich = item.get("stoichiometry", 1)
        if stoich == 1:
            parts.append(f"`{sp}`")
        else:
            parts.append(f"{stoich} `{sp}`")
    return " + ".join(parts)


_PLOT_IMG_EXTS = (".png", ".svg", ".jpg", ".jpeg", ".webp")


def _find_plot_artifacts(entry: ComponentEntry, example: dict, repo_root: Path) -> list[tuple[str, str]]:
    """Return [(image_relpath, caption)] for any plot artifacts shipped alongside
    the .esm for the given example.

    Convention: an artifact for plot `<plot_id>` under example `<example_id>` of
    `foo.esm` lives at `<esm_dir>/foo.plots/<example_id>-<plot_id>.<ext>` where
    `<ext>` is png / svg / jpg / jpeg / webp. Artifacts get copied into the
    Hugo `static/plots/<slug>/` tree and linked below the example prose.

    Returns an empty list if no artifacts are present — today every .esm hits
    this path (see docs/README.md "Example plots — path forward").
    """
    example_id = example.get("id") or ""
    if not example_id:
        return []
    plots_meta = example.get("plots") or []
    if not isinstance(plots_meta, list) or not plots_meta:
        return []
    esm_abs = (repo_root / entry.esm_path).resolve()
    plots_dir = esm_abs.parent / (esm_abs.stem + ".plots")
    if not plots_dir.is_dir():
        return []
    found: list[tuple[str, str]] = []
    for plot in plots_meta:
        if not isinstance(plot, dict):
            continue
        plot_id = plot.get("id") or ""
        if not plot_id:
            continue
        caption = plot.get("description") or plot_id
        for ext in _PLOT_IMG_EXTS:
            candidate = plots_dir / f"{example_id}-{plot_id}{ext}"
            if candidate.is_file():
                found.append((str(candidate), caption))
                break
    return found


def _copy_and_link_plots(
    entry: ComponentEntry,
    example: dict,
    repo_root: Path,
    static_dir: Path,
) -> list[str]:
    """Copy plot artifacts into the Hugo static tree and return markdown image
    lines. Empty list when no artifacts exist for this example."""
    artifacts = _find_plot_artifacts(entry, example, repo_root)
    if not artifacts:
        return []
    dest_rel = Path("plots") / entry.slug
    dest_abs = static_dir / dest_rel
    dest_abs.mkdir(parents=True, exist_ok=True)
    lines: list[str] = []
    for src_path_str, caption in artifacts:
        src = Path(src_path_str)
        dest = dest_abs / src.name
        dest.write_bytes(src.read_bytes())
        url = "/" + str(dest_rel / src.name).replace(os.sep, "/")
        # Escape caption chars that break markdown image syntax.
        alt = caption.replace("[", "(").replace("]", ")")
        lines.append(f"![{alt}]({url})")
    return lines


def _render_examples_section(
    entry: ComponentEntry,
    repo_root: Path,
    static_dir: Path,
) -> str:
    examples = entry.body.get("examples")
    if not isinstance(examples, list) or not examples:
        return ""
    blocks = []
    for ex in examples:
        if not isinstance(ex, dict):
            continue
        title = ex.get("title") or ex.get("id") or "Example"
        desc = ex.get("description") or ""
        code = ex.get("code") or ""
        lang = ex.get("language") or "julia"
        parts = [f"### {title}"]
        if desc:
            parts.append(desc)
        if code:
            parts.append(f"```{lang}\n{code}\n```")
        plot_lines = _copy_and_link_plots(entry, ex, repo_root, static_dir)
        if plot_lines:
            parts.append("\n\n".join(plot_lines))
        blocks.append("\n\n".join(parts))
    return _section("Examples", "\n\n".join(blocks))


def _render_raw_section(entry: ComponentEntry) -> str:
    # Compact, collapsed raw JSON for reference.
    raw = json.dumps(entry.body, indent=2, ensure_ascii=False)
    body = (
        "<details><summary>Raw .esm JSON (this component)</summary>\n\n"
        f"```json\n{raw}\n```\n\n"
        "</details>"
    )
    return _section("Raw .esm", body)


def render_markdown(
    entry: ComponentEntry,
    repo_root: Path | None = None,
    static_dir: Path | None = None,
) -> str:
    """Render one component entry as a Hugo markdown page (frontmatter + body).

    `repo_root` and `static_dir` control where example plot artifacts are
    looked up and copied; when omitted, no plots are emitted (useful for
    pure-render unit tests).
    """
    parts = [_frontmatter(entry)]
    parts.append(_render_description_section(entry))
    parts.append(_render_reference_section(entry))
    # Models / operators use `variables`; reaction_systems use `parameters` + `species` + `reactions`.
    parts.append(_render_variables_sections(entry))
    parts.append(_render_parameters_section(entry))
    parts.append(_render_species_section(entry))
    parts.append(_render_equations_section(entry))
    parts.append(_render_expression_templates_section(entry))
    parts.append(_render_reactions_section(entry))
    if repo_root is not None and static_dir is not None:
        parts.append(_render_examples_section(entry, repo_root, static_dir))
    else:
        parts.append(_render_examples_section_no_plots(entry))
    parts.append(_render_raw_section(entry))
    return "".join(parts)


def _render_examples_section_no_plots(entry: ComponentEntry) -> str:
    """Variant of the examples renderer that skips plot-artifact lookup —
    used by tests that don't need filesystem access to the components tree."""
    examples = entry.body.get("examples")
    if not isinstance(examples, list) or not examples:
        return ""
    blocks = []
    for ex in examples:
        if not isinstance(ex, dict):
            continue
        title = ex.get("title") or ex.get("id") or "Example"
        desc = ex.get("description") or ""
        code = ex.get("code") or ""
        lang = ex.get("language") or "julia"
        parts = [f"### {title}"]
        if desc:
            parts.append(desc)
        if code:
            parts.append(f"```{lang}\n{code}\n```")
        blocks.append("\n\n".join(parts))
    return _section("Examples", "\n\n".join(blocks))


# ---------------------------------------------------------------------------
# Index (JSON) for faceted search / downstream tooling
# ---------------------------------------------------------------------------


def build_index(entries: list[ComponentEntry]) -> dict:
    """Build a compact faceted-search index: one record per component."""
    records = []
    for e in entries:
        records.append(
            {
                "name": e.name,
                "slug": e.slug,
                "domain": e.domain,
                "subdomain": e.subdomain,
                "type": e.type_label,
                "esm_version": e.esm_version,
                "esm_path": str(e.esm_path),
                "description": _description(e),
                "tags": _collect_tags(e),
                "reference": _first_reference_url(e),
            }
        )
    records.sort(key=lambda r: r["slug"])
    return {
        "generator": "esm_to_docs",
        "count": len(records),
        "components": records,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def run(repo_root: Path, content_dir: Path, data_dir: Path, static_dir: Path | None = None) -> int:
    components_root = repo_root / "components"
    if not components_root.exists():
        print(f"error: components/ not found at {components_root}", file=sys.stderr)
        return 2

    files = discover_esm_files(components_root)
    if not files:
        print(f"warning: no .esm files under {components_root}", file=sys.stderr)

    entries: list[ComponentEntry] = []
    for p in files:
        try:
            entries.extend(parse_esm(p, repo_root))
        except json.JSONDecodeError as exc:
            print(f"error: invalid JSON in {p}: {exc}", file=sys.stderr)
            return 2

    # Clean any prior generated pages so stale files never ship.
    components_out = content_dir / "components"
    if components_out.exists():
        _clean_generated(components_out)
    components_out.mkdir(parents=True, exist_ok=True)

    if static_dir is None:
        static_dir = (content_dir.parent / "static").resolve()

    for e in entries:
        target_dir = components_out / e.slug
        target_dir.mkdir(parents=True, exist_ok=True)
        md = render_markdown(e, repo_root=repo_root, static_dir=static_dir)
        (target_dir / "index.md").write_text(md, encoding="utf-8")

    # Write the faceted-search index.
    data_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / "components-index.json").write_text(
        json.dumps(build_index(entries), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    print(f"generated {len(entries)} component pages from {len(files)} .esm file(s)")
    return 0


def _clean_generated(components_out: Path) -> None:
    """Remove auto-generated component pages but preserve `_index.md` and any hand-written pages."""
    # We recognise generated dirs by the presence of an `index.md` with our marker.
    for root, dirs, files in os.walk(components_out, topdown=False):
        p = Path(root)
        # Skip the top-level components dir itself (preserve its _index.md).
        if p == components_out:
            continue
        idx = p / "index.md"
        if idx.exists():
            try:
                text = idx.read_text(encoding="utf-8")
            except OSError:
                continue
            if "esm_path:" in text[:500]:
                idx.unlink()
        # Remove now-empty dirs.
        try:
            p.rmdir()
        except OSError:
            pass


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate Hugo markdown from .esm files.")
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Repository root containing components/ (default: parent of tools/).",
    )
    parser.add_argument(
        "--content-dir",
        type=Path,
        default=None,
        help="Hugo content directory (default: <repo-root>/docs/content).",
    )
    parser.add_argument(
        "--data-dir",
        type=Path,
        default=None,
        help="Hugo data directory (default: <repo-root>/docs/data).",
    )
    parser.add_argument(
        "--static-dir",
        type=Path,
        default=None,
        help="Hugo static directory for plot artifacts (default: <repo-root>/docs/static).",
    )
    args = parser.parse_args(argv)
    repo_root = args.repo_root.resolve()
    content_dir = (args.content_dir or (repo_root / "docs" / "content")).resolve()
    data_dir = (args.data_dir or (repo_root / "docs" / "data")).resolve()
    static_dir = (args.static_dir or (repo_root / "docs" / "static")).resolve()
    return run(repo_root, content_dir, data_dir, static_dir)


if __name__ == "__main__":
    raise SystemExit(main())
