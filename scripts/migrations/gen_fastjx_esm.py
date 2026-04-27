#!/usr/bin/env python3
"""Generate components/gaschem/fastjx.esm — full 13-J-rate version (mdl-09u).

Migrates GasChem.jl `FastJX_interpolation_troposphere` (interpolations_FastJX.jl)
using the v0.3 named tensor-interpolation primitives `interp.linear` and
`interp.bilinear` (esm-spec §9.2 / esm-94w / esm-q7a):

  - 18 actinic-flux observed F_i = interp.bilinear(Z_all[i], P_axis, cosSZA_axis,
    P, cos_sza). Replaces the upstream BSpline-Linear extrapolate(_, Flat()) flux
    interpolators. One symbolic node per F_i instead of ~30 inlined searchsorted+
    clamp+blend nodes — sized for MTK structural_simplify.
  - σ_X observed per (species, bin) = interp.linear(σ_table_per_T_at_bin, T_grid, T)
    Replaces the prior chained searchsorted+index AST. One symbolic node per σ.
  - ϕ_O31D observed per bin = interp.linear(...). Same shape.
  - 13 J-rates (j_H2O2, j_H2COa, j_H2COb, j_O3, j_O31D, j_o32OH, j_NO2, j_NO3a,
    j_NO3b, j_N2O5, j_CH3OOH, j_ActAld, j_PAN) as AST sum-products.
  - cos_sza accepted as an input parameter. (mdl-0u6 mounted lib/solar.esm via §4.7
    and read Solar.cos_zenith, but the ESS Julia binding's namespace_expr drops
    subsystem-scoped refs in parent expressions — see mdl-2aq. Until that bug
    is fixed, downstream callers feed cos_sza directly; this keeps numeric
    agreement testable end-to-end without dropping the bilinear flux pipeline.)
  - adjust_j_o31D inline (no carried state).

Inputs (read at gen time):
    /tmp/fastjx_data.json    — emitted by scripts/migrations/extract_fastjx_data.jl

Run:
    julia scripts/migrations/extract_fastjx_data.jl       # emits /tmp/fastjx_data.json
    python3 scripts/migrations/gen_fastjx_esm.py          # emits components/gaschem/fastjx.esm
"""
import json
from pathlib import Path

DATA_PATH = Path("/tmp/fastjx_data.json")


# ---------------------------------------------------------------------------
# AST helpers
# ---------------------------------------------------------------------------

def C(value):
    return {"op": "const", "args": [], "value": value}


def fn(name, *args):
    return {"op": "fn", "name": name, "args": list(args)}


def Op(o, *args):
    return {"op": o, "args": list(args)}


# ---------------------------------------------------------------------------
# Primitive-based interpolation expressions
# ---------------------------------------------------------------------------

def bilinear_F(z_const_2d, p_grid_const, c_grid_const):
    """interp.bilinear(table, axis_x, axis_y, x, y) for an actinic-flux bin.

    Single fn-op node — the binding handles searchsorted + corner blend +
    flat extrapolation in one closed-form primitive.

    NB: Julia JSON.jl serializes a 23×61 Matrix as 61 outer rows × 23 inner
    columns (column-major, the column ends up as the outer JSON dimension).
    Z_all[i] is Float64 indexed as (P, cosSZA) but its JSON is (cosSZA, P).
    So at the binding boundary axis_x = cosSZA (61) and axis_y = P (23), and
    the query is interp.bilinear(table, cosSZA_axis, P_axis, cos_sza, P).
    """
    return fn("interp.bilinear", z_const_2d, c_grid_const, p_grid_const, "cos_sza", "P")


def sigma_at_T(T_grid, sigmas_per_T, bin_idx):
    """interp.linear(table, axis, T) for σ_X[bin_idx](T).

    For T-independent species the caller passes sigma_const directly — this
    helper is only invoked when T_grid is non-empty. Returns a single fn-op.
    """
    n = len(T_grid)
    assert n >= 2, f"sigma_at_T expects ≥2-point T grid, got {T_grid}"
    table = [sigmas_per_T[k][bin_idx] for k in range(n)]
    return fn("interp.linear", C(table), C(T_grid), "T")


def phi_O31D_at_T(phi_T_grid, phi_per_T, bin_idx):
    """interp.linear(table, axis, T) for ϕ_O31D[bin_idx](T)."""
    n = len(phi_T_grid)
    table = [phi_per_T[k][bin_idx] for k in range(n)]
    return fn("interp.linear", C(table), C(phi_T_grid), "T")


# ---------------------------------------------------------------------------
# Build .esm
# ---------------------------------------------------------------------------

# Map .esm species name → upstream (sigma source, phi handling). For NO3a/NO3b
# the upstream applies a fixed branching ratio onto the shared σ_NO3 mean rate:
#   j_NO3a = j_mean(σ_NO3, ϕ=1.0) · 0.886
#   j_NO3b = j_mean(σ_NO3, ϕ=1.0) · 0.114
#
# Otherwise j_X = (Σ_i F_i · σ_X_i) · ϕ_X for constant ϕ, or
#           j_O31D = Σ_i F_i · σ_O3_i · ϕ_O31D_i(T).
J_RATE_SPECS = [
    # (j_var, sigma_species, phi_var | phi_const | None, branch_ratio)
    ("j_H2O2",   "H2O2",   None,        None),
    ("j_H2COa",  "H2COa",  None,        None),
    ("j_H2COb",  "H2COb",  None,        None),
    ("j_O3",     "O3",     None,        None),
    ("j_NO2",    "NO2",    None,        None),
    ("j_NO3a",   "NO3",    None,        0.886),
    ("j_NO3b",   "NO3",    None,        0.114),
    ("j_N2O5",   "N2O5",   None,        None),
    ("j_CH3OOH", "CH3OOH", None,        None),
    ("j_ActAld", "ActAld", None,        None),
    ("j_PAN",    "PAN",    None,        None),
]


def build():
    data = json.loads(DATA_PATH.read_text())
    P_grid = data["tropospheric_P"]
    C_grid = data["cosSZA_vals"]
    Z_all = data["Z_all"]              # list of 18 matrices [23][61]
    species = data["species"]
    phi_O31D = data["phi_O31D"]
    scenarios = data["scenarios"]
    P_n = len(P_grid)
    C_n = len(C_grid)
    assert P_n == 23 and C_n == 61, (P_n, C_n)

    p_grid_const = C(P_grid)
    c_grid_const = C(C_grid)

    # ---- Variables ----
    v = {}

    # Inputs
    v["T"] = {
        "type": "parameter", "units": "K", "default": 298.0,
        "description": "Air temperature (K). Drives σ_X(T) and ϕ_O31D(T) and adjust_j_o31D.",
    }
    v["P"] = {
        "type": "parameter", "units": "Pa", "default": 101325.0,
        "description": (
            "Air pressure (Pa). One axis of the bilinear actinic-flux interpolation; "
            "also feeds adjust_j_o31D."
        ),
    }
    v["H2O"] = {
        "type": "parameter", "units": "ppb", "default": 450.0,
        "description": "Water vapor mixing ratio (ppb). Feeds adjust_j_o31D.",
    }
    v["cos_sza"] = {
        "type": "parameter", "units": "1", "default": 0.0,
        "description": (
            "Cosine of the solar zenith angle. Input — provided by the caller "
            "(typically lib/solar.esm via Solar.cos_zenith once mdl-2aq fixes "
            "the §4.6 cross-subsystem ref handling in the ESS Julia binding)."
        ),
    }

    # 18 actinic-flux observed F_i — interp.bilinear over Z_all[i] table at (P, cos_sza).
    # Each F_i is a single fn-op node, replacing the upstream flux_interp_i
    # @register_symbolic call. The binding's @register_symbolic on
    # interp.bilinear keeps these from being expanded at structural_simplify time.
    for i in range(18):
        v[f"F_{i+1}"] = {
            "type": "observed", "units": "1/s",
            "description": (
                f"Actinic flux at wavelength bin {i+1} ({data['WL'][i]:.0f} nm), "
                f"bilinearly interpolated from the precomputed Z_all[{i+1}] table "
                f"({P_n}×{C_n}) on the (tropospheric_P, cosSZA) grid via interp.bilinear. "
                "Replaces the upstream BSpline-Linear extrapolate(_, Flat()) flux interpolator."
            ),
            "expression": bilinear_F(C(Z_all[i]), p_grid_const, c_grid_const),
        }

    # σ_X(T) per-bin variables — one observed σ per (species, bin), full 10-species set.
    SIGMA_SPECIES = sorted(species.keys())
    for sp_name in SIGMA_SPECIES:
        sp = species[sp_name]
        for bin_i in range(18):
            if "sigma_const" in sp:
                # T-independent (e.g. CH3OOH)
                expr = float(sp["sigma_const"][bin_i])
                desc_extra = " (T-independent JPL-10 cross section)"
            else:
                expr = sigma_at_T(sp["T_grid"], sp["sigma"], bin_i)
                desc_extra = (
                    f" Linearly interpolated in T over the {len(sp['T_grid'])}-point grid "
                    f"{sp['T_grid']} K with flat extrapolation (interp.linear)."
                )
            v[f"sigma_{sp_name}_{bin_i+1}"] = {
                "type": "observed", "units": "1",
                "description": (
                    f"σ_{sp_name} at wavelength bin {bin_i+1} "
                    f"({data['WL'][bin_i]:.0f} nm).{desc_extra}"
                ),
                "expression": expr,
            }

    # ϕ_O31D(T) per-bin — temperature-dependent quantum yield (3-T grid)
    for bin_i in range(18):
        v[f"phi_O31D_{bin_i+1}"] = {
            "type": "observed", "units": "1",
            "description": (
                f"ϕ_O31D quantum yield at wavelength bin {bin_i+1}, "
                "linearly interpolated in T over the 3-point grid "
                f"{phi_O31D['T_grid']} K (Burkholder/JPL-10) via interp.linear."
            ),
            "expression": phi_O31D_at_T(phi_O31D["T_grid"], phi_O31D["phi"], bin_i),
        }

    # j_X = (Σ_i F_i · σ_X_i) · ϕ_X (constant) or Σ_i F_i · σ_X_i · ϕ_O31D_i (T-dep)
    def sum_product_const_phi(sp_name, phi_const, branch=None):
        terms = [Op("*", f"F_{i}", f"sigma_{sp_name}_{i}") for i in range(1, 19)]
        s = Op("+", *terms)
        factor = phi_const if branch is None else (phi_const * branch)
        return Op("*", s, factor)

    def sum_product_phi_O31D(sp_name):
        terms = [
            Op("*", f"F_{i}", f"sigma_{sp_name}_{i}", f"phi_O31D_{i}")
            for i in range(1, 19)
        ]
        return Op("+", *terms)

    for j_var, sigma_sp, _phi_var, branch in J_RATE_SPECS:
        phi_const = species[sigma_sp]["phi"]
        if branch is None:
            desc = f"j_{sigma_sp} = (Σ_i F_i · σ_{sigma_sp}_i) · ϕ_{sigma_sp}."
        else:
            desc = (
                f"{j_var} = (Σ_i F_i · σ_NO3_i) · ϕ_NO3 · {branch} "
                f"(branching ratio for the {'(NO + O2)' if branch == 0.886 else '(NO2 + O)'} channel; "
                "upstream FastJX_interpolation_troposphere applies this fixed split to the shared "
                "j_NO3 mean rate)."
            )
        v[j_var] = {
            "type": "observed", "units": "1/s",
            "description": desc,
            "expression": sum_product_const_phi(sigma_sp, phi_const, branch),
        }

    # j_O31D — sigma_O3 with T-dependent phi_O31D (special case)
    v["j_O31D"] = {
        "type": "observed", "units": "1/s",
        "description": (
            "j_O31D = Σ_i F_i · σ_O3_i · ϕ_O31D_i(T). Uses σ_O3 with the temperature-"
            "dependent ϕ_O31D quantum yield (Burkholder/JPL-10)."
        ),
        "expression": sum_product_phi_O31D("O3"),
    }

    # adjust_j_o31D — inline AST (no carried state).
    # NB: A is factored as a product of factors each < Int64.max to avoid mdl-ntu —
    # the ESS Julia binding's NumExpr int-coercion overflows Int64 for any
    # integer-valued Float64 literal > Int64.max (~9.2e18). 6.02e23 is split as
    # 6.02 (fractional, not int-coerced) * 1e15 * 1e8 (each ≤ 2^53, Int64-safe).
    # R = 8.314e6 is left as a literal: 8.314 has fractional bits in Float64,
    # so the product has fractional bits and is not coerced.
    A_ast = Op("*", 6.02, 1.0e15, 1.0e8)  # Avogadro (molec/mol)
    v["num_density"] = {
        "type": "observed", "units": "1",
        "description": (
            "Air number density (molec/cm^3, expressed unitless to match the upstream "
            "adjust_j_o31D convention): A · P / (R · T)."
        ),
        "expression": Op("/", Op("*", A_ast, "P"), Op("*", 8.314e6, "T")),
    }
    v["C_H2O"] = {
        "type": "observed", "units": "1",
        "description": "H2O concentration (molec/cm^3 unitless): H2O[ppb] · 1e-9 · num_density.",
        "expression": Op("*", "H2O", 1.0e-9, "num_density"),
    }
    v["C_O2"] = {
        "type": "observed", "units": "1",
        "description": "O2 concentration: 0.2095 · num_density.",
        "expression": Op("*", 0.2095, "num_density"),
    }
    v["C_N2"] = {
        "type": "observed", "units": "1",
        "description": "N2 concentration: 0.7808 · num_density.",
        "expression": Op("*", 0.7808, "num_density"),
    }
    v["C_H2"] = {
        "type": "observed", "units": "1",
        "description": "H2 concentration: 0.5e-6 · num_density.",
        "expression": Op("*", 0.5e-6, "num_density"),
    }
    v["RO1DplH2O"] = {
        "type": "observed", "units": "1",
        "description": "Rate constant for O(1D) + H2O: 1.63e-10 · exp(60/T) · C_H2O.",
        "expression": Op("*", 1.63e-10, Op("exp", Op("/", 60.0, "T")), "C_H2O"),
    }
    v["RO1DplH2"] = {
        "type": "observed", "units": "1",
        "description": "Rate constant for O(1D) + H2: 1.2e-10 · C_H2.",
        "expression": Op("*", 1.2e-10, "C_H2"),
    }
    v["RO1DplN2"] = {
        "type": "observed", "units": "1",
        "description": "Rate constant for O(1D) + N2: 2.15e-11 · exp(110/T) · C_N2.",
        "expression": Op("*", 2.15e-11, Op("exp", Op("/", 110.0, "T")), "C_N2"),
    }
    v["RO1DplO2"] = {
        "type": "observed", "units": "1",
        "description": "Rate constant for O(1D) + O2: 3.3e-11 · exp(55/T) · C_O2.",
        "expression": Op("*", 3.3e-11, Op("exp", Op("/", 55.0, "T")), "C_O2"),
    }
    v["RO1D"] = {
        "type": "observed", "units": "1",
        "description": "Total O(1D) loss rate: sum of RO1DplH2O + RO1DplH2 + RO1DplN2 + RO1DplO2.",
        "expression": Op("+", "RO1DplH2O", "RO1DplH2", "RO1DplN2", "RO1DplO2"),
    }
    v["j_O31D_adj"] = {
        "type": "observed", "units": "1",
        "description": (
            "Fraction of O(1D) that reacts with H2O (producing 2 OH). j_o32OH = j_O31D · "
            "j_O31D_adj. Inlined from GasChem.jl `adjust_j_o31D(T, P, H2O)`."
        ),
        "expression": Op("/", "RO1DplH2O", "RO1D"),
    }
    v["j_o32OH"] = {
        "type": "observed", "units": "1/s",
        "description": "Effective rate for O3 → 2 OH: j_o32OH = j_O31D · j_O31D_adj.",
        "expression": Op("*", "j_O31D", "j_O31D_adj"),
    }

    # Trivial state — first-order decay so the component is a real ODE
    v["NO2"] = {
        "type": "state", "units": "mol/mol", "default": 1.0e-9,
        "description": "Trivial NO2 tracer decayed by j_NO2 — provides the ODE skeleton.",
    }

    # ---- Equations ----
    eqs = [
        {"lhs": {"op": "D", "args": ["NO2"], "wrt": "t"},
         "rhs": Op("-", Op("*", "j_NO2", "NO2"))},
    ]

    # ---- Tests ----
    tests = []
    for sc in scenarios:
        po = {
            "T": sc["T"], "P": sc["P"], "H2O": sc["H2O"],
            "cos_sza": sc["cosSZA"],
        }
        # Reference values — full 13 J-rates plus a few observed F_i spot-checks.
        # cos_sza is now an input parameter, pinned via parameter_overrides.
        asserts = [
            {"variable": "j_O3",     "time": 0.0, "expected": sc["j_O3"]},
            {"variable": "j_O31D",   "time": 0.0, "expected": sc["j_O31D"]},
            {"variable": "j_o32OH",  "time": 0.0, "expected": sc["j_o32OH"]},
            {"variable": "j_NO2",    "time": 0.0, "expected": sc["j_NO2"]},
            {"variable": "j_NO3a",   "time": 0.0, "expected": sc["j_NO3a"]},
            {"variable": "j_NO3b",   "time": 0.0, "expected": sc["j_NO3b"]},
            {"variable": "j_N2O5",   "time": 0.0, "expected": sc["j_N2O5"]},
            {"variable": "j_H2O2",   "time": 0.0, "expected": sc["j_H2O2"]},
            {"variable": "j_H2COa",  "time": 0.0, "expected": sc["j_H2COa"]},
            {"variable": "j_H2COb",  "time": 0.0, "expected": sc["j_H2COb"]},
            {"variable": "j_CH3OOH", "time": 0.0, "expected": sc["j_CH3OOH"]},
            {"variable": "j_ActAld", "time": 0.0, "expected": sc["j_ActAld"]},
            {"variable": "j_PAN",    "time": 0.0, "expected": sc["j_PAN"]},
            # Spot-check the bilinear flux pipeline by pinning a couple of F_i
            # to the reference values from the same upstream interpolators.
            {"variable": "F_12",     "time": 0.0, "expected": sc["F"][11]},  # 295 nm
            {"variable": "F_14",     "time": 0.0, "expected": sc["F"][13]},  # 310 nm
        ]
        tests.append({
            "id": sc["id"],
            "description": (
                f"Reference scenario: cos_sza={sc['cosSZA']:.4f} (pinned from "
                f"t_unix={sc['t_unix']:.0f} s, lat={sc['lat']}°, lon={sc['long']}°), "
                f"T={sc['T']} K, P={sc['P']:.0f} Pa, H2O={sc['H2O']} ppb. "
                "Compares the migrated component's 13 J-rates and 2 spot-checked F_i fluxes "
                "against the upstream GasChem.jl FastJX_interpolation_troposphere reference "
                "computed at the same conditions (see scripts/migrations/extract_fastjx_data.jl)."
            ),
            "parameter_overrides": po,
            "time_span": {"start": 0.0, "end": 1.0},
            "tolerance": {"rel": 5.0e-3, "abs": 1.0e-15},
            "assertions": asserts,
        })

    # ---- Examples ----
    sc0 = scenarios[0]
    examples = [{
        "id": "diurnal_decay_summer_eq",
        "description": (
            "Decay of NO2 under fixed-conditions photolysis at the noon-summer-equator "
            "scenario. Demonstrates that the migrated component runs as a real 0-D ODE "
            "driven by AST-composed j_NO2."
        ),
        "initial_state": {
            "type": "per_variable",
            "values": {"NO2": 1.0e-9},
        },
        "parameters": {
            "T": sc0["T"], "P": sc0["P"], "H2O": sc0["H2O"],
            "cos_sza": sc0["cosSZA"],
        },
        "time_span": {"start": 0.0, "end": 3600.0},
    }]

    notes = (
        "\n\n=== MIGRATION NOTES (mdl-09u) ===\n"
        "Migration scope: full 13-J-rate FastJX_interpolation_troposphere using the v0.3\n"
        "named tensor-interpolation primitives (esm-94w / esm-q7a). Follows mdl-0u6's\n"
        "trimmed soak test, which deferred the bilinear flux pipeline + 5 J-rates because\n"
        "the previous inlined-AST formulation (~10 nodes per lookup × 18 wavelengths\n"
        "+ 220 σ chains) blew MTK 11.x structural_simplify wall time past 5 minutes.\n"
        "\n"
        "Source: GasChem.jl/src/interpolations_FastJX.jl (FastJX_interpolation_troposphere).\n"
        "\n"
        "Mappings:\n"
        "  - flux_interp_1..18(P, csa)  →  18 observed F_i = interp.bilinear(Z_all[i],\n"
        "    P_axis, cosSZA_axis, P, cos_sza). Single fn-op per F_i, kept opaque to MTK\n"
        "    structural_simplify by the @register_symbolic on the binding side.\n"
        "  - σ_X interp(T)  →  σ_X_i = interp.linear(σ_per_T, T_grid, T) for each\n"
        "    (species, bin). T-independent species use a literal scalar.\n"
        "  - ϕ_O31D(T) interp  →  phi_O31D_i = interp.linear(...) — same shape.\n"
        "  - j_mean_X(T, fluxes)  →  observed j_X = (Σ_i F_i · σ_X_i [· phi_O31D_i]) · ϕ_X.\n"
        "  - j_NO3a / j_NO3b      →  shared j_NO3 mean rate scaled by 0.886 / 0.114\n"
        "    (NO3 → NO + O2 vs NO3 → NO2 + O branching ratio).\n"
        "  - adjust_j_o31D(T, P, H2O)  →  inline observed C_H2O / C_O2 / C_N2 / C_H2 +\n"
        "    rate-constant AST + j_O31D_adj = RO1DplH2O / RO1D. j_o32OH = j_O31D · j_O31D_adj.\n"
        "\n"
        "All upstream registered functions are recovered as AST compositions of the closed\n"
        "function registry (interp.linear + interp.bilinear) + AST ops. No registered\n"
        "functions remain in the migrated component.\n"
        "\n"
        "Note on cos_sza routing:\n"
        "  mdl-0u6 mounted lib/solar.esm via §4.7 inclusion and read Solar.cos_zenith\n"
        "  through a §4.6 scoped reference. The ESS Julia binding's namespace_expr\n"
        "  short-circuits on dotted names and never rewrites Sub.x → Parent.Sub.x for\n"
        "  parent-model expressions, so the prior file failed to load (see mdl-2aq).\n"
        "  Until that bug is fixed, cos_sza is exposed as a FastJX parameter and the\n"
        "  caller pins it (typically by mounting Solar at a higher level and forwarding\n"
        "  cos_sza ← Solar.cos_zenith there). Tests pin cos_sza to lib/solar.esm's\n"
        "  reference value computed in extract_fastjx_data.jl using the same NOAA\n"
        "  Spencer-Fourier formula.\n"
    )

    doc = {
        "esm": "0.3.0",
        "metadata": {
            "name": "FastJX",
            "description": (
                notes +
                "\n=== END MIGRATION NOTES ===\n\n"
                "Fast-JX UV photolysis rates (interpolation-based variant). "
                "0-D component computing 13 J-rates (j_H2O2, j_H2COa, j_H2COb, j_O3, "
                "j_O31D, j_o32OH, j_NO2, j_NO3a, j_NO3b, j_N2O5, j_CH3OOH, j_ActAld, "
                "j_PAN) from atmospheric (cos_sza, T, P, H2O). Uses the v0.3 named "
                "tensor-interpolation primitives interp.linear (σ_X(T) and ϕ_O31D(T)) "
                "and interp.bilinear (actinic flux F_i on a (P, cosSZA) grid) so MTK "
                "structural_simplify sees one symbolic node per interpolation rather "
                "than a deeply-nested chain."
            ),
            "authors": ["EarthSciML"],
            "created": "2026-04-26T00:00:00Z",
            "tags": [
                "chemistry", "photolysis", "fast-jx",
                "closed-function-registry", "interp-linear", "interp-bilinear",
                "subsystem-inclusion",
            ],
            "references": [
                {"citation":
                    "Neu, J.L., Prather, M.J., and Penner, J.E. (2007), Global atmospheric "
                    "chemistry: Integrating over fractional cloud cover, J. Geophys. Res., "
                    "112, D11306, doi:10.1029/2006JD008007."},
                {"citation":
                    "Wild, O., Zhu, X., and Prather, M.J. (2000), Fast-J: Accurate Simulation "
                    "of In- and Below-Cloud Photolysis in Tropospheric Chemical Models. "
                    "Journal of Atmospheric Chemistry, 37(3), 245–282."},
                {"citation":
                    "Burkholder, J.B. et al. (2015), Chemical Kinetics and Photochemical Data "
                    "for Use in Atmospheric Studies, Evaluation No. 18, JPL Publication 15-10."},
                {"citation":
                    "Source: GasChem.jl/src/interpolations_FastJX.jl + src/Fast-JX.jl + "
                    "src/tropospheric_interpolation_data.bson "
                    "(commit 8c12c048482b515fb8eb2110bf8ab4b4f4e71309)."},
            ],
        },
        "models": {
            "FastJX": {
                "coupletype": "FastJX",
                "variables": v,
                "equations": eqs,
                "tests": tests,
                "examples": examples,
            }
        },
    }
    return doc


def main():
    doc = build()
    out = Path(__file__).resolve().parents[2] / "components" / "gaschem" / "fastjx.esm"
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w") as f:
        json.dump(doc, f, indent=2)
        f.write("\n")
    size_kb = out.stat().st_size / 1024
    print(f"Wrote {out} ({size_kb:.1f} KB)")


if __name__ == "__main__":
    main()
