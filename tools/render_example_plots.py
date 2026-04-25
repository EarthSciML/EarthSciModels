#!/usr/bin/env python3
"""
render_example_plots — evaluate `.esm` examples and emit PNG plots.

Walks `components/**/*.esm`, and for each top-level component with examples
carrying a `parameter_sweep` + `plots`, evaluates the sweep and writes one
PNG per plot under

    <esm_dir>/<esm_stem>.plots/<example_id>-<plot_id>.png

`tools/esm_to_docs.py` already understands this convention and will inline
the artifacts on the rendered Hugo page (mdl-f42).

Coverage today: algebraic-only components — i.e. models whose `equations`
list is empty and whose `observed` expressions are pure functions of
parameters and other observed values. CloudAlbedo (Seinfeld & Pandis Fig
24.16) is the canonical case. Components with non-trivial ODE / DAE
dynamics (e.g. SuperFast's 24-hour integration) are skipped with a
diagnostic line and tracked as a follow-up — driving them through MTK
would require Julia in the docs CI image.

Entry points:
    python3 tools/render_example_plots.py                   # from repo root
    python3 tools/render_example_plots.py --components-dir <path>
"""
from __future__ import annotations

import argparse
import json
import math
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

# Headless backend so this works in CI without a display.
import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402


# ---------------------------------------------------------------------------
# AST evaluator (mirrors esm_to_docs.ast_to_latex but produces numeric values)
# ---------------------------------------------------------------------------


_BINARY_FUNCS = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "/": lambda a, b: a / b,
    "^": lambda a, b: a ** b,
}

_UNARY_FUNCS = {
    "exp": np.exp,
    "log": np.log,
    "log10": np.log10,
    "log2": np.log2,
    "sqrt": np.sqrt,
    "sin": np.sin,
    "cos": np.cos,
    "tan": np.tan,
    "abs": np.abs,
}


class UnsupportedExpression(Exception):
    """Raised when the evaluator hits an op or pattern it cannot handle."""


def evaluate(node: Any, env: dict[str, Any]) -> Any:
    """Evaluate an .esm expression AST against a numeric environment.

    `env` maps variable names (parameters and previously-evaluated observed
    values) to scalars or numpy arrays. Returns a numpy-broadcastable value.
    """
    if isinstance(node, bool):
        return 1.0 if node else 0.0
    if isinstance(node, (int, float)):
        return float(node)
    if isinstance(node, str):
        if node not in env:
            raise UnsupportedExpression(f"unbound variable: {node!r}")
        return env[node]
    if not isinstance(node, dict):
        raise UnsupportedExpression(f"unsupported AST node type: {type(node).__name__}")

    op = node.get("op")
    args = node.get("args") or []
    if op is None:
        raise UnsupportedExpression("AST node missing 'op'")

    if op in _UNARY_FUNCS and len(args) == 1:
        return _UNARY_FUNCS[op](evaluate(args[0], env))

    if op == "+":
        if not args:
            return 0.0
        out = evaluate(args[0], env)
        for a in args[1:]:
            out = out + evaluate(a, env)
        return out
    if op == "-":
        if len(args) == 1:
            return -evaluate(args[0], env)
        out = evaluate(args[0], env)
        for a in args[1:]:
            out = out - evaluate(a, env)
        return out
    if op == "*":
        if not args:
            return 1.0
        out = evaluate(args[0], env)
        for a in args[1:]:
            out = out * evaluate(a, env)
        return out
    if op == "/":
        if len(args) < 2:
            raise UnsupportedExpression("'/' requires at least 2 args")
        out = evaluate(args[0], env)
        for a in args[1:]:
            out = out / evaluate(a, env)
        return out
    if op == "^":
        if len(args) != 2:
            raise UnsupportedExpression("'^' requires exactly 2 args")
        return evaluate(args[0], env) ** evaluate(args[1], env)

    raise UnsupportedExpression(f"unsupported op: {op!r}")


# ---------------------------------------------------------------------------
# Sweep + plot evaluation
# ---------------------------------------------------------------------------


@dataclass
class _Variable:
    name: str
    kind: str
    default: Any
    expression: Any


def _collect_variables(component: dict) -> dict[str, _Variable]:
    out: dict[str, _Variable] = {}
    raw = component.get("variables") or {}
    if not isinstance(raw, dict):
        return out
    for name, spec in raw.items():
        if not isinstance(spec, dict):
            continue
        out[name] = _Variable(
            name=name,
            kind=spec.get("type", "variable"),
            default=spec.get("default"),
            expression=spec.get("expression"),
        )
    return out


def _is_algebraic_only(component: dict) -> bool:
    """A component is renderable here when it has no time-evolving state.

    Concretely: an empty `equations` list (or none) and at least one
    observed variable to plot. ReactionSystems are excluded — their state
    is the species concentration vector, which needs an ODE solve.
    """
    eqs = component.get("equations")
    if isinstance(eqs, list) and eqs:
        return False
    if "reactions" in component or "species" in component:
        return False
    vars_ = component.get("variables") or {}
    if not isinstance(vars_, dict) or not vars_:
        return False
    return any(
        isinstance(v, dict) and v.get("type") == "observed" for v in vars_.values()
    )


def _build_sweep_grid(parameter_sweep: dict) -> tuple[list[str], list[np.ndarray]]:
    """Return (names, values) for a 1D or 2D cartesian sweep."""
    if not isinstance(parameter_sweep, dict):
        raise UnsupportedExpression("parameter_sweep is not a dict")
    if parameter_sweep.get("type") != "cartesian":
        raise UnsupportedExpression(
            f"unsupported sweep type: {parameter_sweep.get('type')!r}"
        )
    dims = parameter_sweep.get("dimensions") or []
    if not isinstance(dims, list) or not dims:
        raise UnsupportedExpression("parameter_sweep has no dimensions")
    names: list[str] = []
    values: list[np.ndarray] = []
    for d in dims:
        if not isinstance(d, dict):
            raise UnsupportedExpression("dimension is not a dict")
        param = d.get("parameter")
        rng = d.get("range") or {}
        if not isinstance(param, str) or not isinstance(rng, dict):
            raise UnsupportedExpression("dimension missing parameter or range")
        start = float(rng.get("start"))
        stop = float(rng.get("stop"))
        count = int(rng.get("count", 50))
        scale = rng.get("scale", "linear")
        if scale == "log":
            arr = np.logspace(math.log10(start), math.log10(stop), count)
        else:
            arr = np.linspace(start, stop, count)
        names.append(param)
        values.append(arr)
    return names, values


def _evaluate_observed(
    variables: dict[str, _Variable], env: dict[str, Any]
) -> dict[str, Any]:
    """Evaluate every observed variable into `env` (which already contains
    parameters + constants). Loops up to N passes to resolve dependency order.
    """
    pending = {
        name: v
        for name, v in variables.items()
        if v.kind == "observed" and v.expression is not None
    }
    max_passes = len(pending) + 1
    for _ in range(max_passes):
        if not pending:
            break
        progress = False
        for name in list(pending.keys()):
            try:
                env[name] = evaluate(pending[name].expression, env)
            except UnsupportedExpression:
                continue
            pending.pop(name)
            progress = True
        if not progress:
            break
    if pending:
        names = sorted(pending.keys())
        raise UnsupportedExpression(
            f"could not resolve observed variables: {names}"
        )
    return env


def _baseline_env(
    variables: dict[str, _Variable], example: dict
) -> dict[str, float]:
    """Initial environment: parameter / constant defaults, optionally
    overridden by the example's `parameters` map."""
    env: dict[str, float] = {}
    for name, v in variables.items():
        if v.kind in ("parameter", "constant") and v.default is not None:
            env[name] = float(v.default)
    overrides = example.get("parameters") or {}
    if isinstance(overrides, dict):
        for name, val in overrides.items():
            env[name] = float(val)
    return env


def _grid_envs(
    base_env: dict[str, float],
    sweep_names: list[str],
    sweep_values: list[np.ndarray],
) -> dict[str, np.ndarray]:
    """Broadcast the sweep onto base_env. Returns env where every value is
    a numpy array of shape `tuple(len(v) for v in sweep_values)` (or scalar
    for non-sweep parameters)."""
    grids = np.meshgrid(*sweep_values, indexing="ij")
    env: dict[str, Any] = dict(base_env)
    for name, grid in zip(sweep_names, grids):
        env[name] = grid
    return env


# ---------------------------------------------------------------------------
# Plotting
# ---------------------------------------------------------------------------


def _render_line_plot(
    plot: dict,
    sweep_names: list[str],
    sweep_values: list[np.ndarray],
    env: dict[str, Any],
    out_path: Path,
) -> None:
    if len(sweep_values) != 1:
        raise UnsupportedExpression(
            f"line plot needs 1D sweep, got {len(sweep_values)}D"
        )
    x_spec = plot.get("x") or {}
    y_spec = plot.get("y") or {}
    x_name = x_spec.get("variable")
    y_name = y_spec.get("variable")
    if x_name not in env or y_name not in env:
        raise UnsupportedExpression(
            f"line plot references unbound variables: x={x_name!r} y={y_name!r}"
        )
    x_vals = np.asarray(env[x_name])
    y_vals = np.asarray(env[y_name])
    # Broadcast a scalar y onto the sweep axis (rare but safe).
    if y_vals.ndim == 0:
        y_vals = np.full_like(x_vals, float(y_vals))

    fig, ax = plt.subplots(figsize=(6.0, 4.0))
    ax.plot(x_vals, y_vals, color="#1f4d8a", linewidth=2)
    ax.set_xlabel(x_spec.get("label") or x_name)
    ax.set_ylabel(y_spec.get("label") or y_name)
    # Detect log axis from the sweep dimension's scale (heuristic via spread).
    if x_vals.size > 1 and x_vals[0] > 0:
        ratio = x_vals[-1] / x_vals[0]
        if ratio > 50.0:
            ax.set_xscale("log")
    ax.grid(True, which="both", alpha=0.3)
    title = plot.get("description") or plot.get("id") or ""
    if title:
        ax.set_title(title, fontsize=10)
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=120)
    plt.close(fig)


def _render_heatmap_plot(
    plot: dict,
    sweep_names: list[str],
    sweep_values: list[np.ndarray],
    env: dict[str, Any],
    out_path: Path,
) -> None:
    if len(sweep_values) != 2:
        raise UnsupportedExpression(
            f"heatmap plot needs 2D sweep, got {len(sweep_values)}D"
        )
    x_spec = plot.get("x") or {}
    y_spec = plot.get("y") or {}
    v_spec = plot.get("value") or {}
    x_name = x_spec.get("variable")
    y_name = y_spec.get("variable")
    v_name = v_spec.get("variable")
    if x_name not in env or y_name not in env or v_name not in env:
        raise UnsupportedExpression(
            f"heatmap references unbound: x={x_name} y={y_name} value={v_name}"
        )
    x_vals = sweep_values[sweep_names.index(x_name)]
    y_vals = sweep_values[sweep_names.index(y_name)]
    z = np.asarray(env[v_name])
    # Orient: rows = y, cols = x. Our meshgrid uses indexing="ij" so
    # env[v_name] is shaped (len(sweep[0]), len(sweep[1])). Transpose to
    # match the conventional (y, x) imshow orientation.
    if sweep_names.index(x_name) == 0:
        z_yx = z.T
    else:
        z_yx = z

    fig, ax = plt.subplots(figsize=(6.0, 4.5))
    extent = (float(x_vals[0]), float(x_vals[-1]), float(y_vals[0]), float(y_vals[-1]))
    im = ax.imshow(
        z_yx,
        origin="lower",
        aspect="auto",
        extent=extent,
        cmap="viridis",
    )
    ax.set_xlabel(x_spec.get("label") or x_name)
    ax.set_ylabel(y_spec.get("label") or y_name)
    if x_vals.size > 1 and x_vals[0] > 0 and x_vals[-1] / x_vals[0] > 50.0:
        ax.set_xscale("log")
    if y_vals.size > 1 and y_vals[0] > 0 and y_vals[-1] / y_vals[0] > 50.0:
        ax.set_yscale("log")
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label(v_spec.get("label") or v_name)
    title = plot.get("description") or plot.get("id") or ""
    if title:
        ax.set_title(title, fontsize=10)
    fig.tight_layout()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=120)
    plt.close(fig)


_PLOT_RENDERERS = {
    "line": _render_line_plot,
    "heatmap": _render_heatmap_plot,
}


# ---------------------------------------------------------------------------
# Per-file driver
# ---------------------------------------------------------------------------


_COMPONENT_SECTIONS = (
    "models",
    "reaction_systems",
    "operators",
    "data_loaders",
    "coupling",
    "interfaces",
)


@dataclass
class _RenderStats:
    files_seen: int = 0
    examples_seen: int = 0
    plots_rendered: int = 0
    plots_skipped: int = 0
    elapsed_s: float = 0.0


def render_examples_for_file(
    esm_path: Path, stats: _RenderStats, log: Iterable | None = None
) -> None:
    with esm_path.open("r", encoding="utf-8") as fp:
        data = json.load(fp)
    plots_dir = esm_path.parent / (esm_path.stem + ".plots")

    for section in _COMPONENT_SECTIONS:
        block = data.get(section)
        if not isinstance(block, dict):
            continue
        for cname, body in block.items():
            if not isinstance(body, dict):
                continue
            examples = body.get("examples")
            if not isinstance(examples, list) or not examples:
                continue
            for example in examples:
                if not isinstance(example, dict):
                    continue
                _render_one_example(
                    esm_path, cname, body, example, plots_dir, stats
                )


def _render_one_example(
    esm_path: Path,
    component_name: str,
    component_body: dict,
    example: dict,
    plots_dir: Path,
    stats: _RenderStats,
) -> None:
    plots = example.get("plots")
    if not isinstance(plots, list) or not plots:
        return
    if "parameter_sweep" not in example:
        # Examples without a sweep cannot be rendered into a plot here.
        # (e.g. SuperFast's `default_run_24h` is a time-series ODE run.)
        for plot in plots:
            stats.plots_skipped += 1
            print(
                f"[skip] {esm_path.name}::{component_name} example "
                f"{example.get('id')!r}: no parameter_sweep "
                f"(time-series examples need an ODE solver — see docs/README.md)"
            )
        return

    if not _is_algebraic_only(component_body):
        for plot in plots:
            stats.plots_skipped += 1
            print(
                f"[skip] {esm_path.name}::{component_name} example "
                f"{example.get('id')!r}: component has non-algebraic dynamics"
            )
        return

    stats.examples_seen += 1
    variables = _collect_variables(component_body)
    base_env = _baseline_env(variables, example)

    try:
        sweep_names, sweep_values = _build_sweep_grid(example["parameter_sweep"])
        env = _grid_envs(base_env, sweep_names, sweep_values)
        env = _evaluate_observed(variables, env)
    except UnsupportedExpression as exc:
        for plot in plots:
            stats.plots_skipped += 1
            print(
                f"[skip] {esm_path.name}::{component_name} example "
                f"{example.get('id')!r}: {exc}"
            )
        return

    example_id = example.get("id") or "example"
    for plot in plots:
        if not isinstance(plot, dict):
            continue
        plot_id = plot.get("id") or "plot"
        plot_type = plot.get("type") or "line"
        renderer = _PLOT_RENDERERS.get(plot_type)
        if renderer is None:
            stats.plots_skipped += 1
            print(
                f"[skip] {esm_path.name}::{component_name} example "
                f"{example_id} plot {plot_id}: unsupported plot type {plot_type!r}"
            )
            continue
        out_path = plots_dir / f"{example_id}-{plot_id}.png"
        try:
            renderer(plot, sweep_names, sweep_values, env, out_path)
        except UnsupportedExpression as exc:
            stats.plots_skipped += 1
            print(
                f"[skip] {esm_path.name}::{component_name} example "
                f"{example_id} plot {plot_id}: {exc}"
            )
            continue
        stats.plots_rendered += 1
        rel = out_path.relative_to(esm_path.parent.parent.parent.parent) \
            if str(out_path).startswith(str(esm_path.parent.parent.parent.parent)) \
            else out_path
        print(f"[ok]   {rel}")


# ---------------------------------------------------------------------------
# Discovery + CLI
# ---------------------------------------------------------------------------


def discover_esm_files(components_root: Path) -> list[Path]:
    return sorted(p for p in components_root.rglob("*.esm") if p.is_file())


def run(components_root: Path) -> int:
    if not components_root.exists():
        print(
            f"error: components/ not found at {components_root}", file=sys.stderr
        )
        return 2
    files = discover_esm_files(components_root)
    if not files:
        print(f"warning: no .esm files under {components_root}", file=sys.stderr)
        return 0
    stats = _RenderStats()
    t0 = time.time()
    for f in files:
        stats.files_seen += 1
        try:
            render_examples_for_file(f, stats)
        except json.JSONDecodeError as exc:
            print(f"error: invalid JSON in {f}: {exc}", file=sys.stderr)
            return 2
    stats.elapsed_s = time.time() - t0
    print()
    print(
        f"render_example_plots: {stats.plots_rendered} plot(s) rendered, "
        f"{stats.plots_skipped} skipped, {stats.examples_seen} examples seen "
        f"across {stats.files_seen} .esm file(s) in {stats.elapsed_s:.2f}s"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render example plots from .esm files.")
    parser.add_argument(
        "--components-dir",
        type=Path,
        default=None,
        help="Components root (default: <repo-root>/components).",
    )
    args = parser.parse_args(argv)
    repo_root = Path(__file__).resolve().parent.parent
    components_root = (args.components_dir or (repo_root / "components")).resolve()
    return run(components_root)


if __name__ == "__main__":
    raise SystemExit(main())
