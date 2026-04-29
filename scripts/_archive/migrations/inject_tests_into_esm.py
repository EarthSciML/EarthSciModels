"""Inject the inline tests block into components/gaschem/geoschem_fullchem.esm
from scripts/migrations/reference_values_geoschem_fullchem.json.

Reads the JSON file produced by reference_values_geoschem_fullchem.jl and
turns each pinned reference state into one ESM Test (per spec §6.6) with
initial_conditions, parameter_overrides, time_span, assertions, description,
and tolerance. Writes back to the .esm in place.

Tolerance: spec §6.6.4 default rel=1e-6 is too tight for cross-implementation
ODE solves at this scale (819 reactions, stiff system, mtkcompile path
divergence). We use rel=1e-3 for the integrated species values — three
significant figures of agreement is plenty to catch translation bugs while
absorbing solver-tolerance and finite-precision drift between Catalyst paths.
"""
import json
import sys
from pathlib import Path

ESM_PATH = Path("components/gaschem/geoschem_fullchem.esm")
REF_PATH = Path("scripts/migrations/reference_values_geoschem_fullchem.json")

DESCRIPTIONS = {
    "clean_troposphere": (
        "Clean troposphere reference state (mdl-ode): T=285 K, P=101325 Pa "
        "(num_density=42.76 mol/m^3), daytime photolysis (j_NO2≈0.005 1/s), "
        "low NOx ([NO]=50 ppt, [NO2]=200 ppt), low VOC ([ISOP]=200 ppt), "
        "background O3=30 ppb. Expected values from "
        "GasChem.jl/GEOSChemGasPhase via "
        "scripts/migrations/reference_values_geoschem_fullchem.jl."
    ),
    "polluted_urban": (
        "Polluted urban reference state (mdl-ode): T=298 K, P=101325 Pa "
        "(num_density=40.89 mol/m^3), daytime (j_NO2≈0.0149 1/s), high NOx "
        "([NO]=10 ppb, [NO2]=20 ppb), high VOC ([ISOP]=2 ppb), elevated "
        "O3=70 ppb. Expected values from GasChem.jl/GEOSChemGasPhase via "
        "scripts/migrations/reference_values_geoschem_fullchem.jl."
    ),
    "upper_troposphere": (
        "Upper-troposphere / lower-stratosphere reference state (mdl-ode): "
        "T=220 K, P=20000 Pa (num_density=10.94 mol/m^3, ~12 km), reduced "
        "photolysis (j_NO2≈0.002 1/s), low NOx, no VOCs, O3=100 ppb. "
        "Expected values from GasChem.jl/GEOSChemGasPhase via "
        "scripts/migrations/reference_values_geoschem_fullchem.jl."
    ),
}

# (T, P) per-state — used to compute num_density override = P/(R*T) (mol/m³).
STATE_TP = {
    "clean_troposphere":   (285.0, 101325.0),
    "polluted_urban":      (298.0, 101325.0),
    "upper_troposphere":   (220.0,  20000.0),
}
R_GAS = 8.314


def main():
    data = json.loads(ESM_PATH.read_text())
    refs = json.loads(REF_PATH.read_text())
    rs = data["reaction_systems"]["GEOSChemGasPhase"]
    tests = []
    # Stable test ordering matches the bead: clean / urban / UTLS.
    for state_id in ("clean_troposphere", "polluted_urban", "upper_troposphere"):
        state = refs[state_id]
        T, P = STATE_TP[state_id]
        ic = dict(state["initial_conditions"])
        params = dict(state["parameter_overrides"])
        params["T"] = T
        params["num_density"] = P / (R_GAS * T)
        tspan = state["tspan_seconds"]
        assertions = list(state["samples"])
        tests.append({
            "id": state_id,
            "description": DESCRIPTIONS[state_id],
            "initial_conditions": ic,
            "parameter_overrides": params,
            "time_span": {"start": float(tspan[0]), "end": float(tspan[1])},
            "tolerance": {"rel": 1.0e-3},
            "assertions": assertions,
        })
    rs["tests"] = tests
    ESM_PATH.write_text(json.dumps(data, indent=4))
    print(f"injected {len(tests)} tests, wrote {ESM_PATH} size={ESM_PATH.stat().st_size}")


if __name__ == "__main__":
    main()
