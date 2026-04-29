"""Rewrite ``max(a, 0.0)`` rate clamps in geoschem_fullchem.esm to
``(a + abs(a)) / 2``.

EarthSciSerializationCatalystExt._esm_to_symbolic supports
{+, -, *, /, ^, exp, log, log10, sin, cos, tan, sqrt, abs} but NOT max/min.
The migration generated 64 ``max(expr, 0.0)`` calls (Arrhenius branches that
would otherwise go negative at very low T). The mathematical identity
``max(a, 0) = (a + abs(a)) / 2`` lets us land equivalent rate semantics
using only operators the Catalyst extension already understands.

We deliberately avoid touching the ESS Catalyst extension (cross-rig fix
deferred to a follow-on bead). This keeps mdl-ode self-contained and mirrors
the existing post_process_geoschem_fullchem.py stop-gap pattern.

The script idempotently rewrites max ops in the named .esm in place:

    python3 scripts/migrations/rewrite_max_in_esm.py components/gaschem/geoschem_fullchem.esm
"""
import json
import sys
from pathlib import Path


def rewrite_max(node):
    if isinstance(node, dict):
        op = node.get("op")
        args = node.get("args")
        if isinstance(args, list):
            node["args"] = [rewrite_max(a) for a in args]
        if "expr" in node:
            node["expr"] = rewrite_max(node["expr"])
        if "values" in node:
            node["values"] = [rewrite_max(v) for v in node["values"]]
        if op == "max" and isinstance(node["args"], list) and len(node["args"]) == 2:
            a, b = node["args"]
            # max(a, 0) -> (a + abs(a)) / 2
            if b == 0 or b == 0.0:
                return {
                    "op": "/",
                    "args": [
                        {"op": "+", "args": [a, {"op": "abs", "args": [a]}]},
                        2.0,
                    ],
                }
            # max(0, a) -> same
            if a == 0 or a == 0.0:
                return {
                    "op": "/",
                    "args": [
                        {"op": "+", "args": [b, {"op": "abs", "args": [b]}]},
                        2.0,
                    ],
                }
            # General max(a, b) = (a + b + abs(a - b)) / 2
            return {
                "op": "/",
                "args": [
                    {
                        "op": "+",
                        "args": [
                            a,
                            b,
                            {
                                "op": "abs",
                                "args": [{"op": "+", "args": [a, {"op": "*", "args": [-1.0, b]}]}],
                            },
                        ],
                    },
                    2.0,
                ],
            }
        return node
    if isinstance(node, list):
        return [rewrite_max(x) for x in node]
    return node


def main():
    if len(sys.argv) != 2:
        print(f"usage: {sys.argv[0]} <path-to-esm>", file=sys.stderr)
        sys.exit(2)
    path = Path(sys.argv[1])
    data = json.loads(path.read_text())
    rs_dict = data.get("reaction_systems", {})
    n_changed = 0
    for sys_name, rs in rs_dict.items():
        for r in rs.get("reactions", []):
            before = json.dumps(r["rate"], sort_keys=True)
            r["rate"] = rewrite_max(r["rate"])
            after = json.dumps(r["rate"], sort_keys=True)
            if before != after:
                n_changed += 1
    path.write_text(json.dumps(data, indent=4))
    print(f"reactions rewritten: {n_changed}")
    print(f"wrote {path} size={path.stat().st_size}")


if __name__ == "__main__":
    main()
