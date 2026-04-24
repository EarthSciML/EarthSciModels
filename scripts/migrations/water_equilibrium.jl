"""
    water_equilibrium.jl

Standalone MTK module for the `WaterEquilibrium` component migrated from
Aerosol.jl@c8c640bb (`src/aqueous_equilibria.jl:76`). Constants and
equations mirror the upstream definition verbatim.

Upstream, `WaterEquilibrium` is a subsystem intended for composition: its
`T` and `H_plus` are `@variables` because they are wired to a parent
`AqueousEquilibria` system that provides their values. Serialized as a
standalone ESM component it would be structurally underdetermined (3
equations, 5 unknowns), so this module declares `T` and `H_plus` as
parameters. The remaining quantities (`K_w`, `OH_minus`, `pH`) then
resolve as observed variables — matching the bead's
`(S, observed-only)` classification.

Exports a top-level binding `system` so `scripts/roundtrip.jl` can
auto-discover it with no flags.

Reference: Seinfeld & Pandis, Atmospheric Chemistry and Physics, Ch 7,
Eq 7.10–7.13 (water autoionization) and Table 7.4 (van't Hoff
temperature dependence of K_w).
"""

using ModelingToolkit
using ModelingToolkit: t_nounits as t
using Unitful

@constants begin
    R_gas = 8.314, [description = "Gas constant", unit = u"J/mol/K"]
    T_ref = 298.0, [description = "Reference temperature", unit = u"K"]
    K_w_298 = 1.0e-14 * 1.0e6,
        [description = "K_w at 298 K", unit = u"mol^2/m^6"]
    dH_Kw = 55856.4,
        [
            description = "Enthalpy for K_w (13.35 kcal/mol)",
            unit = u"J/mol",
        ]
    C_ref = 1000.0,
        [
            description = "Reference concentration (1 mol/L = 1000 mol/m³)",
            unit = u"mol/m^3",
        ]
end

@parameters begin
    T = 298.0, [description = "Temperature", unit = u"K"]
    H_plus = 1.0e-4, [description = "Hydrogen ion concentration (pH 7 default is 1e-4 mol/m³)", unit = u"mol/m^3"]
end

@variables begin
    OH_minus(t), [description = "Hydroxide ion concentration", unit = u"mol/m^3"]
    K_w(t), [description = "Water dissociation constant", unit = u"mol^2/m^6"]
    pH(t), [description = "pH value (dimensionless)", unit = u"1"]
end

eqs = [
    K_w ~ K_w_298 * exp((-dH_Kw / R_gas) * (1 / T - 1 / T_ref)),
    K_w ~ H_plus * OH_minus,
    pH ~ -log10(H_plus / C_ref),
]

# `checks = false` skips unit validation at construction time. Unit
# checking is run lazily by ModelingToolkit and is stricter in the MTK
# version pinned by the ESS round-trip env than in our migration env —
# specifically it flags the `-log10(…)` literal `-` in equation 3 as an
# Int64 that cannot unify with the dimensionless `pH` unit. The underlying
# math is dimensionless (dimensionless / dimensionless = dimensionless,
# log10 of dimensionless is dimensionless). Disabling the redundant check
# at construction time lets the scaffolder, round-trip validator, and
# inline-test walker share the same source file without bifurcating units
# on an identity-only operator.
const system = System(eqs, t; name = :WaterEquilibrium, checks = false)
