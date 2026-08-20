#!/usr/bin/env python3
"""
esm_to_docs — turn `components/**/*.esm` files into Hugo markdown pages.

One `.esm` may contain multiple entries (models, reaction_systems, ...); each
top-level entry becomes one page under `docs/content/components/<path>/<name>/`.

The generator also writes `docs/data/components-index.json` for faceted search
feeds and other downstream consumers (SSG-agnostic).

Variable classification (esm 1.0.0)
-----------------------------------
From esm 1.0.0 a `.esm` declares exactly TWO variable types, `unknown` and
`parameter`. Whether an unknown is an ODE state, an observed quantity or an
algebraic one is DERIVED from the model's `equations`, and whether a parameter
is Brownian / discrete / sampled / constant is derived from its `distribution`
and `update` (esm-spec §6.3.1). This generator therefore asks the binding —
`earthsci_ast.classification` — rather than reading a declared type. That module
is the single sanctioned home for the derivation across all five language
bindings; re-deriving it here from the equations would be shadow logic that can
drift from the spec and from the other four bindings (AGENTS.md §1).

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

from earthsci_ast.classification import (
    algebraic_unknowns,
    observed_definitions,
    ode_states,
    parameters as declared_parameters,
)


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


# Top-level schema sections we render a page for.
#
# `data_sources` is the esm 1.0.0 spelling of what 0.x called `data_loaders`.
# It is NOT a component in 1.0.0 (a source cannot be a coupling endpoint, a
# subsystem, or a scoped-name path root — esm-spec §8); it is a document-scoped
# ingest registry. We still emit a page per entry because the dataset behind it
# is what a reader is looking for, but the page carries the source's I/O
# descriptor rather than a variables table: from 1.0.0 a source exposes no
# variables, and each former loader variable lives on the CONSUMING model as a
# parameter with `update: {kind: "data", source: ...}`.
_COMPONENT_SECTIONS = (
    "models",
    "reaction_systems",
    "operators",
    "data_sources",
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
            "data_sources": "data_source",
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


def _render_variable_table(title: str, variables: dict, include_names: Iterable[str]) -> str:
    """Render the named subset of `variables` as a table.

    The subset is chosen by the CALLER from `earthsci_ast.classification`, not
    by reading a declared type here: from esm 1.0.0 the only declared types are
    `unknown` and `parameter` (esm-spec §6.3.1). Declaration order is preserved
    so a table reads the way the author wrote the file.
    """
    rows = []
    include = set(include_names)
    for name, spec in variables.items():
        if not isinstance(spec, dict):
            continue
        if name not in include:
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


def _render_expression_list(title: str, variables: dict, definitions: dict) -> str:
    """Render each observed unknown as `name = <its defining RHS>`.

    Before 1.0.0 the defining expression sat on the variable itself
    (`variables[v].expression`); it now lives in the model's `equations` as a
    bare-variable-LHS row, and `classification.observed_definitions` is what
    recovers the map. `definitions` is that map (name → RHS AST); we walk the
    `variables` dict so the page keeps declaration order and can pick up each
    variable's `description`.
    """
    lines = []
    for name, spec in variables.items():
        if not isinstance(spec, dict):
            continue
        if name not in definitions:
            continue
        expr = definitions[name]
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
    """Variables / Parameters / Observed tables for one model node.

    The split is DERIVED, per esm-spec §6.3.1, by `earthsci_ast.classification`:

    - **Variables** — the unknowns the solver actually solves for: the ODE
      states plus the algebraic unknowns. (Those two together are exactly what
      0.x spelled `type: "state"`.)
    - **Parameters** — everything declared `type: "parameter"`.
    - **Observed** — the unknowns some equation defines with a bare-variable
      LHS, listed with their defining right-hand sides.

    A model with no `equations` (a pure interface declaration) classifies every
    unknown as algebraic, so its unknowns all land in **Variables** and none is
    silently dropped.

    The 0.x "Constants" table is gone: `constant` was never a member of any
    version's variable-type enum, so that table could only ever be empty. A
    constant is now DERIVED — a parameter with neither `distribution` nor
    `update` (`classification.constant_parameters`) — and every such parameter
    is already in the Parameters table.
    """
    variables = entry.body.get("variables") or {}
    if not isinstance(variables, dict) or not variables:
        return ""
    model = entry.body
    solved = set(ode_states(model)) | set(algebraic_unknowns(model))
    definitions = observed_definitions(model)
    parameter_names = set(declared_parameters(model))
    # Classification only accounts for variables declared `unknown` or
    # `parameter` — the two types 1.0.0 defines. A variable declared anything
    # else (a stale `state` / `observed`, or a spelling like `"variable"` that
    # is in no version's enum) belongs to no set, and filtering the tables by
    # those sets alone would drop it from the page without a word. Show it
    # under Variables and say so on stderr: a page that quietly omits a
    # declared quantity is worse than one that shows an unclassifiable one.
    unclassified = set(variables) - solved - parameter_names - set(definitions)
    if unclassified:
        for name in sorted(unclassified):
            declared = variables[name].get("type") if isinstance(variables[name], dict) else None
            print(
                f"warning: {entry.esm_path}:{entry.section}.{entry.name}: variable "
                f"{name!r} declares type {declared!r}, which esm 1.0.0 does not "
                f"define (only 'unknown' and 'parameter'); rendering it under "
                f"Variables",
                file=sys.stderr,
            )
    out = []
    vars_tbl = _render_variable_table("Variables", variables, solved | unclassified)
    params_tbl = _render_variable_table("Parameters", variables, parameter_names)
    observed_tbl = _render_variable_table("Observed", variables, set(definitions))
    observed_exprs = _render_expression_list("Observed expressions", variables, definitions)
    for s in (vars_tbl, params_tbl, observed_tbl, observed_exprs):
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
    """Render the model's equations, minus the observed definitions.

    From 1.0.0 an observed unknown is defined by a bare-variable-LHS EQUATION
    rather than by a `variables[v].expression` field, so `equations` now carries
    rows that the "Observed expressions" section already renders. Rendering both
    would print every observed quantity twice. We drop exactly one row per name
    in `classification.observed_definitions` — the FIRST bare-LHS row, which is
    the one the classifier credits — so a variable defined twice still shows its
    remaining rows here rather than having them silently disappear.
    """
    equations = entry.body.get("equations")
    if not isinstance(equations, list) or not equations:
        return ""
    pending_definitions = set(observed_definitions(entry.body))
    blocks = []
    for i, eq in enumerate(equations):
        if not isinstance(eq, dict):
            continue
        lhs = eq.get("lhs")
        rhs = eq.get("rhs")
        if lhs is None and rhs is None:
            continue
        if isinstance(lhs, str) and lhs in pending_definitions:
            pending_definitions.discard(lhs)
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


def _render_data_source_section(entry: ComponentEntry) -> str:
    """Render a `data_sources` entry's I/O descriptor (esm-spec §8).

    A source is pure I/O from 1.0.0: it locates, reads, decodes, slices and
    filters bytes, and exposes NO variables. What the model gets out of it is
    documented on the CONSUMING model, as a parameter whose
    `update: {kind: "data", source: "<this key>", from: {...}}` names it — so
    there is deliberately no variables table here.
    """
    if entry.section != "data_sources":
        return ""
    body = entry.body
    rows = []

    def add(label: str, value: Any) -> None:
        if value in (None, "", [], {}):
            return
        rows.append(f"| {label} | {value} |")

    add("Kind", f"`{body.get('kind')}`" if body.get("kind") else "")
    source = body.get("source")
    if isinstance(source, dict):
        add("URL template", f"`{source.get('url_template')}`" if source.get("url_template") else "")
        mirrors = source.get("mirrors") or []
        if isinstance(mirrors, list) and mirrors:
            add("Mirrors", ", ".join(f"`{m}`" for m in mirrors))
    temporal = body.get("temporal")
    if isinstance(temporal, dict):
        add("Coverage", " → ".join(str(temporal[k]) for k in ("start", "end") if temporal.get(k)))
        add("File period", f"`{temporal.get('file_period')}`" if temporal.get("file_period") else "")
        add("Sample frequency", f"`{temporal.get('frequency')}`" if temporal.get("frequency") else "")
        add("Records per file", temporal.get("records_per_file"))
    if not rows:
        return ""
    header = "| | |\n| --- | --- |\n"
    return _section("Data source", header + "\n".join(rows))


_PLOT_IMG_EXTS = (".png", ".svg", ".jpg", ".jpeg", ".webp")


def _find_plot_artifacts(entry: ComponentEntry, analysis: dict, repo_root: Path) -> list[tuple[str, str]]:
    """Return [(image_relpath, caption)] for any plot artifacts shipped alongside
    the .esm for the given analysis.

    Convention: an artifact for plot `<plot_id>` under analysis `<analysis_id>`
    of `foo.esm` lives at `<esm_dir>/foo.plots/<analysis_id>-<plot_id>.<ext>`
    where `<ext>` is png / svg / jpg / jpeg / webp. Artifacts get copied into
    the Hugo `static/plots/<slug>/` tree and linked below the analysis prose.

    Returns an empty list if no artifacts are present — today every .esm hits
    this path (see docs/README.md "Analysis plots — path forward").
    """
    analysis_id = analysis.get("id") or ""
    if not analysis_id:
        return []
    plots_meta = analysis.get("plots") or []
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
            candidate = plots_dir / f"{analysis_id}-{plot_id}{ext}"
            if candidate.is_file():
                found.append((str(candidate), caption))
                break
    return found


def _copy_and_link_plots(
    entry: ComponentEntry,
    analysis: dict,
    repo_root: Path,
    static_dir: Path,
) -> list[str]:
    """Copy plot artifacts into the Hugo static tree and return markdown image
    lines. Empty list when no artifacts exist for this analysis."""
    artifacts = _find_plot_artifacts(entry, analysis, repo_root)
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


def _render_analysis_body(analysis: dict) -> list[str]:
    """The prose parts of one analysis: heading, description, run window.

    esm-spec §6.7 fixes the Analysis object to `id`, `description`,
    `initial_state`, `parameters`, `time_span`, `parameter_sweep`, `plots` and
    `expression_template_imports` — the `$def` is `additionalProperties: false`.
    The 0.4-era `title` / `code` / `language` keys the 0.x `examples` block
    carried are therefore unrepresentable and no longer read here; the `id` is
    the heading and the run configuration below it is what a reader needs to
    reproduce the figure.
    """
    parts = [f"### {analysis.get('id') or 'Analysis'}"]
    desc = analysis.get("description") or ""
    if desc:
        parts.append(desc)
    span = analysis.get("time_span")
    if isinstance(span, dict):
        # TimeSpan is {start, end} in the component's own time units — the
        # schema carries no units field of its own.
        start, end = span.get("start"), span.get("end")
        if start is not None and end is not None:
            parts.append(f"**Time span:** {start} → {end}")
    sweep = analysis.get("parameter_sweep")
    if isinstance(sweep, dict):
        dims = sweep.get("dimensions") or []
        swept = [d.get("parameter") for d in dims if isinstance(d, dict) and d.get("parameter")]
        if swept:
            parts.append("**Swept over:** " + ", ".join(f"`{p}`" for p in swept))
    return parts


def _render_analyses_section(
    entry: ComponentEntry,
    repo_root: Path,
    static_dir: Path,
) -> str:
    analyses = entry.body.get("analyses")
    if not isinstance(analyses, list) or not analyses:
        return ""
    blocks = []
    for analysis in analyses:
        if not isinstance(analysis, dict):
            continue
        parts = _render_analysis_body(analysis)
        plot_lines = _copy_and_link_plots(entry, analysis, repo_root, static_dir)
        if plot_lines:
            parts.append("\n\n".join(plot_lines))
        blocks.append("\n\n".join(parts))
    return _section("Analyses", "\n\n".join(blocks))


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

    `repo_root` and `static_dir` control where analysis plot artifacts are
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
    parts.append(_render_data_source_section(entry))
    if repo_root is not None and static_dir is not None:
        parts.append(_render_analyses_section(entry, repo_root, static_dir))
    else:
        parts.append(_render_analyses_section_no_plots(entry))
    parts.append(_render_raw_section(entry))
    return "".join(parts)


def _render_analyses_section_no_plots(entry: ComponentEntry) -> str:
    """Variant of the analyses renderer that skips plot-artifact lookup —
    used by tests that don't need filesystem access to the components tree."""
    analyses = entry.body.get("analyses")
    if not isinstance(analyses, list) or not analyses:
        return ""
    blocks = []
    for analysis in analyses:
        if not isinstance(analysis, dict):
            continue
        blocks.append("\n\n".join(_render_analysis_body(analysis)))
    return _section("Analyses", "\n\n".join(blocks))


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


def _warn_slug_collisions(entries: list[ComponentEntry]) -> list[str]:
    """Report every slug two or more components share, and return those slugs.

    A slug is `domain/[subdomain/]name`, and it is the page's URL. When two
    components land on the same one, the second `index.md` overwrites the
    first, so a page disappears from the site while `components-index.json`
    goes on advertising both — a silent hole rather than a build failure. The
    usual cause is the SAME registry key declared in two `.esm` files (e.g. a
    `data_sources` entry inlined in a model file and also left behind in a
    standalone `*_loader.esm`), which is a corpus problem, not a docs one.

    This is a warning, not an error: the fix belongs in `components/`, and
    failing the docs build would gate the whole catalog on it. But it must be
    visible in the CI log rather than swallowed.
    """
    by_slug: dict[str, list[ComponentEntry]] = {}
    for e in entries:
        by_slug.setdefault(e.slug, []).append(e)
    collisions = sorted(slug for slug, group in by_slug.items() if len(group) > 1)
    for slug in collisions:
        sources = ", ".join(
            f"{e.section}.{e.name} in {e.esm_path}" for e in by_slug[slug]
        )
        print(
            f"warning: slug {slug!r} is claimed by {len(by_slug[slug])} components "
            f"({sources}); all but the last will be overwritten",
            file=sys.stderr,
        )
    return collisions


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

    _warn_slug_collisions(entries)

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
