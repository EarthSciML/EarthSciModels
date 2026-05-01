# Substrate-in-rate audit (2026-05-01)

- **Tracking bead:** `mdl-79g`
- **Cross-rig dependency:** ESS-rig is dropping the substrate-detection heuristic from
  the Python / Julia / Rust bindings (`reactions.py`, `reactions.jl`, the Rust
  crate). This audit clears EarthSciModels for that drop.
- **Spec reference:** `esm-spec.md §7.4` — the `rate` field on a reaction is the
  rate **coefficient**; the runner ALWAYS multiplies by `∏ Sᵢ^nᵢ` over substrates.
  No exception, no detection, no skip.

## Method

Walked every `.esm` under this rig with the OFFICIAL Python ESS parser
(`earthsci_toolkit.parse.load`) and the OFFICIAL free-variable extractor
(`earthsci_toolkit.expression.free_variables`). For each `Reaction`, flagged
substrates whose name appears in the rate's free variables. No regex, no
custom JSON walker.

Pattern classification on the rate AST:
- **P1 (numerator):** substrate appears outside any `/` denominator → mechanical
  rewrite: drop the substrate from the rate expression.
- **P2 (denominator):** substrate appears under `/` (cancellation form, KPP
  "consumed but not in rate" trick) → case-by-case decision.

## Coverage

| Files audited | Reactions audited | Findings |
|---:|---:|---:|
| 12 | 846 | **3** (all P2, all in `components/gaschem/geoschem_fullchem.esm`) |

`lib/solar.esm` failed structural validation on a units check (in `models/Solar/variables/true_solar_time`,
unrelated to this audit). The file declares no `reaction_systems`, so it is
vacuously clean for substrate-in-rate. The unit-validation failure is filed
separately.

## Findings

All three findings are **Pattern 2** in `components/gaschem/geoschem_fullchem.esm`,
reaction system `GEOSChemGasPhase`:

| idx | name | substrates | products | rate | substrate-in-rate |
|---:|:---|:---|:---|:---|:---|
| 0 | R1 | `{SALAAL, O3, SO2}` | `{SO4}` | `k_mt1 / SALAAL` | `SALAAL` (denom) |
| 3 | R4 | `{O3, SO2, SALCAL}` | `{SO4s}` | `k_mt4 / SALCAL` | `SALCAL` (denom) |
| 11 | R12 | `{SO2, HMS, OH}` | `{2 SO4, CH2O}` | `k_cld6 / SO2` | `SO2` (denom) |

## Decision: kept-as-is (all three)

### Author intent (from upstream `GasChem.jl/src/geoschem_fullchem.jl`)

The reactions were ported from KPP-format GEOS-Chem chemistry. The KPP source
uses minus signs to mark species that are consumed but do not appear in the
rate expression, e.g.:

```
SO2 + SALAAL + O3 = SO4 - SALAAL : K_MT(1);   # KPP: SALAAL consumed but not in rate
```

The Catalyst-based port encodes this as a `rate / substrate` cancellation:

```
k_mt1 / SALAAL, SO2 + SALAAL + O3 --> SO4
```

Catalyst applies mass action straight: `v = (k_mt1/SALAAL) · SALAAL · O3 · SO2 = k_mt1 · O3 · SO2`.
The cancellation is mathematical, and `k_mt1` is therefore numerically equal to
`K_MT(1)` in the original KPP. Same trick for R4 (`k_mt4 / SALCAL`) and R12
(`k_cld6 / SO2`).

### Behavior under the heuristic (today's bindings — buggy)

`v_heuristic = k / S`, with substrate multiplication suppressed.
This does NOT match the KPP intent and produces a pathological rate that scales
inversely with the catalytic species' concentration.

### Behavior after the heuristic drop — kept-as-is form

`v_spec = (k / S) · S · X · Y = k · X · Y`, by mathematical cancellation, where
`X · Y` are the non-catalytic substrates. **This matches the original KPP intent.**
For R12, the cancellation cleanly removes SO2 from the rate while preserving
its stoichiometric consumption — exactly the "rate-limited by HMS+OH oxidation,
SO2 consumed by net stoichiometry" reading from `Moch et al. 2020`.

### Why not rewrite to `rate = k_eff` with the catalytic species removed from substrates?

Two reasons:

1. **Loses chemical meaning.** SALAAL / SALCAL are sea-salt-aerosol alkalinities;
   they ARE consumed (titrated) by the reaction. Dropping them from substrates
   would silently remove their consumption from the model, changing alkalinity
   dynamics. The same holds for SO2 in R12, which is the major sulfur source
   for the SO4 product — dropping it would unbalance sulfur stoichiometry.
2. **The spec has no "non-rate substrate" feature.** ESS §7.4 is mass-action
   only. Encoding "consumed but not in rate" requires either a spec extension
   (filed separately if needed) or the cancellation form. Among the available
   options, the cancellation form is the one that preserves both (a) the
   author's kinetic intent and (b) the stoichiometric mass balance.

The cancellation form is **spec-conformant**: §7.4 places no restriction on
what symbols the `rate` Expr may reference, and the runner's mass-action
multiplication produces the correct `v` regardless of internal cancellations.
The audit pattern flags it because it is unusual and was historically tied to
the now-removed heuristic; it is not a spec violation.

### Net effect of the ESS heuristic drop on geoschem_fullchem dynamics

The heuristic drop is a **bug fix**, not a behavior break. Three reactions
move from a buggy `k/S` rate to the intended `k · (non-catalytic substrates)`
rate. No further changes to this fixture are required for the heuristic drop
to land safely.

## Pattern 1 cases

**None.** No reaction in this rig writes its rate with a substrate symbol in
the numerator. All 846 reactions across `geoschem_fullchem.esm` (819) and
`superfast.esm` (27) parse cleanly and are spec-conformant under either
heuristic regime, except for the three P2 cases above which produce the
correct dynamics under the spec-conformant regime.

## Discovered work (out of scope)

- `lib/solar.esm` fails structural validation on
  `models/Solar/variables/true_solar_time` due to an addition/subtraction with
  incompatible units. Not a substrate-in-rate concern (no reactions). Filed
  separately.
