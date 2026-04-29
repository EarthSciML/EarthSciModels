"""Post-process /tmp/geoschem_fullchem.esm:
1. Fix species refs in rate ASTs: {op:X, args:["t"]} where X is species name -> bare "X"
2. Rename reaction ids to R1..RN
3. Convert string-encoded numbers (e.g., "300.0") back to actual numbers — these are
   MTK Constants that lost their numeric type during Catalyst's mtk2esm walk
"""
import json
import re
from pathlib import Path

NUM_RE = re.compile(r"^-?(\d+\.?\d*|\.\d+)([eE][+-]?\d+)?$")
RATIONAL_RE = re.compile(r"^\(?(-?\d+)//(-?\d+)\)?$")

src = Path("/tmp/geoschem_fullchem.esm")
data = json.loads(src.read_text())
rs = data["reaction_systems"]["GEOSChemGasPhase"]
species_names = set()
if isinstance(rs.get("species"), dict):
    species_names |= set(rs["species"].keys())
elif isinstance(rs.get("species"), list):
    species_names |= {s.get("name", s) if isinstance(s, dict) else s for s in rs["species"]}
for r in rs["reactions"]:
    for s in r.get("substrates", []) or []:
        species_names.add(s["species"])
    for s in r.get("products", []) or []:
        species_names.add(s["species"])
parameter_names = set()
params = rs.get("parameters", {})
if isinstance(params, dict):
    parameter_names |= set(params.keys())
elif isinstance(params, list):
    parameter_names |= {p.get("name", p) if isinstance(p, dict) else p for p in params}
print(f"species: {len(species_names)}, parameters: {len(parameter_names)}")

# Built-in scalar variable refs that are NOT numeric:
KNOWN_VARS = species_names | parameter_names | {"t"}

def fix_expr(node):
    if isinstance(node, dict):
        op = node.get("op")
        args = node.get("args")
        # species call as op
        if op in species_names and isinstance(args, list) and len(args) == 1 and args[0] == "t":
            return op
        if isinstance(args, list):
            node["args"] = [fix_expr(a) for a in args]
        if "expr" in node:
            node["expr"] = fix_expr(node["expr"])
        if "values" in node:
            node["values"] = [fix_expr(v) for v in node["values"]]
        return node
    elif isinstance(node, list):
        return [fix_expr(x) for x in node]
    elif isinstance(node, str):
        # If it looks like a number AND isn't a known variable name, convert to number
        if node not in KNOWN_VARS and NUM_RE.match(node):
            try:
                f = float(node)
                if f.is_integer() and "." not in node and "e" not in node.lower():
                    return int(f)
                return f
            except Exception:
                pass
        m = RATIONAL_RE.match(node)
        if m and node not in KNOWN_VARS:
            try:
                num, den = int(m.group(1)), int(m.group(2))
                return num / den
            except Exception:
                pass
        return node
    return node

n_fixed = 0
for i, r in enumerate(rs["reactions"]):
    before = json.dumps(r["rate"])
    r["rate"] = fix_expr(r["rate"])
    after = json.dumps(r["rate"])
    if before != after:
        n_fixed += 1
    r["id"] = f"R{i+1}"
print(f"reactions fixed: {n_fixed}/{len(rs['reactions'])}")

# Sanity scan: any remaining string args that look like numbers?
suspect_strings = set()
def scan(n):
    if isinstance(n, dict):
        for v in n.get("args", []) or []:
            scan(v)
        for k in ("expr","values"):
            if k in n: scan(n[k])
    elif isinstance(n, list):
        for v in n: scan(v)
    elif isinstance(n, str):
        if n not in KNOWN_VARS and NUM_RE.match(n):
            suspect_strings.add(n)
for r in rs["reactions"]:
    scan(r["rate"])
print(f"remaining string-numeric refs: {len(suspect_strings)}")
for s in list(suspect_strings)[:5]:
    print(f"  {s!r}")

# Also scan for unknown bare-string refs (potential undeclared params)
suspect_vars = set()
def scan2(n):
    if isinstance(n, dict):
        for v in n.get("args", []) or []:
            scan2(v)
        for k in ("expr","values"):
            if k in n: scan2(n[k])
    elif isinstance(n, list):
        for v in n: scan2(v)
    elif isinstance(n, str):
        if n not in KNOWN_VARS and not NUM_RE.match(n):
            suspect_vars.add(n)
for r in rs["reactions"]:
    scan2(r["rate"])
print(f"undeclared-name refs: {len(suspect_vars)}")
for s in list(suspect_vars)[:10]:
    print(f"  {s!r}")

out = Path("/home/ctessum/esmlgt/EarthSciModels/polecats/furiosa/EarthSciModels/components/gaschem/geoschem_fullchem.esm")
out.write_text(json.dumps(data, indent=4))
print(f"wrote {out} size={out.stat().st_size}")
