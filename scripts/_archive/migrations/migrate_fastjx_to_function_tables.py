#!/usr/bin/env python3
"""One-shot migration: rewrite components/gaschem/fastjx.esm onto
function_tables + table_lookup (esm-spec §9.5, v0.4.0).

Replaces the per-binding interp.bilinear (18 actinic-flux F_i) and
interp.linear (18 phi_O31D + 9*18 sigma_X) fn-op chains with a small
set of multi-output function tables and table_lookup AST nodes. T-
independent species (sigma_CH3OOH_*) keep their literal-scalar form.

Run from the repo root:

    python3 scripts/_archive/migrations/migrate_fastjx_to_function_tables.py

Idempotent: refuses to run if function_tables is already populated.

Bead: mdl-jm8 (mdl-09u → mdl-jm8 lineage).
"""

from __future__ import annotations

import json
import re
import sys
from collections import OrderedDict
from pathlib import Path


REPO = Path(__file__).resolve().parents[3]
ESM = REPO / "components" / "gaschem" / "fastjx.esm"


def main() -> int:
    raw = ESM.read_text()
    data = json.loads(raw, object_pairs_hook=OrderedDict)

    if data.get("function_tables"):
        print(f"refusing: {ESM} already has function_tables — already migrated",
              file=sys.stderr)
        return 1

    data["esm"] = "0.4.0"

    vars_ = data["models"]["FastJX"]["variables"]

    # Group bindings by family. Each family becomes one multi-output table.
    # Family name = strip trailing _<digits>.
    fam_re = re.compile(r"_(\d+)$")
    families: "OrderedDict[str, list[tuple[int, str, dict]]]" = OrderedDict()
    for name, vdef in vars_.items():
        m = fam_re.search(name)
        if not m:
            continue
        expr = vdef.get("expression")
        if not isinstance(expr, dict) or expr.get("op") != "fn":
            continue
        fname = expr.get("name")
        if fname not in ("interp.linear", "interp.bilinear"):
            continue
        fam = name[: m.start()]
        idx = int(m.group(1))
        families.setdefault(fam, []).append((idx, name, vdef))

    # Sanity: every family is contiguous 1..N in idx order.
    for fam, entries in families.items():
        entries.sort(key=lambda t: t[0])
        idxs = [t[0] for t in entries]
        if idxs != list(range(1, len(idxs) + 1)):
            raise SystemExit(f"family {fam} has non-contiguous indices: {idxs}")

    # Build function_tables block.
    tables: "OrderedDict[str, OrderedDict]" = OrderedDict()

    # F (bilinear) — single bilinear table on (cos_sza, P)
    if "F" in families:
        entries = families["F"]
        ax0 = entries[0][2]["expression"]["args"][1]["value"]
        ax1 = entries[0][2]["expression"]["args"][2]["value"]
        q0 = entries[0][2]["expression"]["args"][3]
        q1 = entries[0][2]["expression"]["args"][4]
        if q0 != "cos_sza" or q1 != "P":
            raise SystemExit(f"F bilinear queries unexpected: {q0}, {q1}")
        # Verify shared axes
        for _, name, vdef in entries:
            args = vdef["expression"]["args"]
            if args[1]["value"] != ax0 or args[2]["value"] != ax1:
                raise SystemExit(f"{name}: bilinear axes diverge — cannot fold")
            if args[3] != q0 or args[4] != q1:
                raise SystemExit(f"{name}: bilinear queries diverge")
        tables["F_actinic"] = OrderedDict([
            ("description",
             "Actinic flux F_i on the (cos_sza, P) grid for 18 Fast-JX wavelength bins. "
             "Bit-equivalent to the prior interp.bilinear chains: bindings lower this "
             "table_lookup back to interp.bilinear (esm-lhm). Bin order: "
             "[187, 191, 193, 196, 202, 208, 211, 214, 261, 267, 277, 295, 303, 310, "
             "316, 333, 380, 574] nm."),
            ("axes", [
                OrderedDict([("name", "cos_sza"), ("units", "1"),
                             ("values", ax0)]),
                OrderedDict([("name", "P"), ("units", "Pa"),
                             ("values", ax1)]),
            ]),
            ("interpolation", "bilinear"),
            ("out_of_bounds", "clamp"),
            ("outputs", [name for _, name, _ in entries]),
            ("data", [vdef["expression"]["args"][0]["value"]
                      for _, _, vdef in entries]),
        ])
        del families["F"]

    # Linear families: one table per family on the family's T axis.
    for fam, entries in families.items():
        ax = entries[0][2]["expression"]["args"][1]["value"]
        q = entries[0][2]["expression"]["args"][2]
        if q != "T":
            raise SystemExit(f"family {fam} linear query unexpected: {q}")
        for _, name, vdef in entries:
            args = vdef["expression"]["args"]
            if args[1]["value"] != ax:
                raise SystemExit(f"{name}: T axis diverges from family {fam}")
            if args[2] != q:
                raise SystemExit(f"{name}: query diverges from {q}")

        # Description tag varies between sigma vs phi.
        if fam.startswith("sigma_"):
            species = fam[len("sigma_"):]
            desc = (f"Absorption cross-section sigma_{species}_i(T) for the "
                    f"18 Fast-JX wavelength bins. Bindings lower the "
                    f"table_lookup back to interp.linear on T (esm-lhm).")
        elif fam == "phi_O31D":
            desc = ("O(1D) quantum yield phi_O31D_i(T) for the 18 Fast-JX "
                    "wavelength bins. Bindings lower the table_lookup back "
                    "to interp.linear on T (esm-lhm).")
        else:
            desc = (f"{fam}_i(T) for the 18 Fast-JX wavelength bins. "
                    "Bindings lower the table_lookup back to interp.linear "
                    "on T (esm-lhm).")

        table_id = fam if fam == "phi_O31D" else fam  # keep family name
        tables[table_id] = OrderedDict([
            ("description", desc),
            ("axes", [
                OrderedDict([("name", "T"), ("units", "K"),
                             ("values", ax)]),
            ]),
            ("interpolation", "linear"),
            ("out_of_bounds", "clamp"),
            ("outputs", [name for _, name, _ in entries]),
            ("data", [vdef["expression"]["args"][0]["value"]
                      for _, _, vdef in entries]),
        ])

    # Inject function_tables block at top level (after metadata, before models).
    new_data: "OrderedDict[str, object]" = OrderedDict()
    for k, v in data.items():
        if k == "models":
            new_data["function_tables"] = tables
        new_data[k] = v
    data = new_data

    # Rewrite each binding's expression with table_lookup.
    F_outputs = set(tables["F_actinic"]["outputs"])
    linear_outputs: dict[str, str] = {}
    for tid, table in tables.items():
        if tid == "F_actinic":
            continue
        for out_name in table["outputs"]:
            linear_outputs[out_name] = tid

    for name, vdef in vars_.items():
        if name in F_outputs:
            vdef["expression"] = OrderedDict([
                ("op", "table_lookup"),
                ("args", []),
                ("table", "F_actinic"),
                ("axes", OrderedDict([("cos_sza", "cos_sza"), ("P", "P")])),
                ("output", name),
            ])
        elif name in linear_outputs:
            vdef["expression"] = OrderedDict([
                ("op", "table_lookup"),
                ("args", []),
                ("table", linear_outputs[name]),
                ("axes", OrderedDict([("T", "T")])),
                ("output", name),
            ])

    # Update migration notes header on metadata.description.
    desc = data["metadata"]["description"]
    note_marker = "=== END MIGRATION NOTES ==="
    if note_marker in desc and "(mdl-jm8)" not in desc:
        injected = (
            "\n\n=== MIGRATION NOTES (mdl-jm8) ===\n"
            "Migrated the 18 actinic-flux F_i bindings (interp.bilinear) and "
            "the 18*9 + 18 = 180 sigma_X / phi_O31D bindings (interp.linear) "
            "onto first-class sampled function tables (esm-spec §9.5, v0.4.0). "
            "ESS bindings (esm-hid + esm-lhm) lower table_lookup back to the "
            "underlying interp.bilinear / interp.linear ASTs, so all 13 J-rate "
            "outputs are bit-equivalent to the pre-migration values; the "
            "noon_summer_eq / morning_midlat / spot_check_F12 inline tests "
            "lock that in.\n\n"
            "Tables emitted (function_tables, top-level):\n"
            "  F_actinic           — bilinear on (cos_sza, P), 18 outputs F_1..F_18.\n"
            "  phi_O31D            — linear on T, 18 outputs phi_O31D_1..18.\n"
            "  sigma_<species>     — linear on T, 18 outputs each, for ActAld, "
            "H2COa, H2COb, H2O2, N2O5, NO2, NO3, O3, PAN.\n"
            "  (sigma_CH3OOH_i remain literal scalars — T-independent.)\n\n"
            "File-size win: was 37231 lines of repeated axis const blocks and "
            "fn-op chains; the migrated form folds the shared axes once per "
            "table family.\n\n"
            "=== END MIGRATION NOTES ==="
        )
        # Append the new section after the existing END marker, keeping the prior history intact.
        data["metadata"]["description"] = desc.replace(
            note_marker, note_marker + injected, 1)

    ESM.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {ESM}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
