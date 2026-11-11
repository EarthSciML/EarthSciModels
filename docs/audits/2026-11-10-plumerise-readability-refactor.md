# PlumeRise (Freitas plume-rise model): parameter semantics and readability refactor

Date: 2026-11-10. Model: `components/environmental_transport/plume_rise/plumerise_freitas.esm`
(PlumeRise v0.10.10-dev2, SHA-256 `aa2d1ba57811590a70ba50c130f9fb69ebdd3a59d85f327b7534147fb8c3e7d1`).

This is a **readability refactor with no change to the physics or the numbers**. It responds to review comments by
Chris Tessum on the previous version (v0.10.10-dev1, SHA-256 `638ce589…0c55`):

1. Equations such as `cᵢ₀ = 1.6` are unnecessary: a constant should be a *parameter* (a value that does not change
   during the simulation), not an *unknown* (a quantity the solver solves for).
2. Descriptions such as "Rainwater mixing ratio after glaciation by freezing. Mass basis: kg water per kg dry air.
   Dimensionless." do not make clear why such a quantity belongs in a plume-rise model.

## Result

| Check | Result |
|---|---|
| Official EarthSciAST Rust runner (esm 0.3.1), inline tests | **57 PASS / 0 FAIL / 0 ERROR** |
| dev2 vs dev1, 300 s simulation, every shared output at every saved time (1,753,792 values) | **bit-identical** (max difference 0) |
| Adaptive time grid | identical (818 saved points in both) |
| Schema validation (`esm validate`) | passed |
| Dimensional check (`esm units --check`) | 0 mismatches |
| 57 assertions: variables, times, expected values, tolerances | identical to the immutable reference v0.10.9 |
| Remaining equations, expression templates, initial conditions, grid, solver block | unchanged (structural check) |

Validation run: Slurm job 12318807 (2026-11-10). The same job re-simulated dev1 and reproduced the archived dev1
validation run bit for bit, so the comparison is not affected by the compute node.

## A. Constants converted from unknowns to parameters

The candidates were derived from the source, not counted by hand: every unknown whose only equation is
`x = <number>` (no other variable and no time dependence). There were **68**. Each one is now
a `parameter` whose `default` is the exact literal from the removed equation (same JSON number, same units, same
symbol), and its equation is removed. Equations: 348 → 280. Variables: 270 unknowns and 85 parameters
(previously 338 and 17).

`q∅` is a 200-level profile. It uses the schema's scalar-broadcast default (`default: 0` on a shaped parameter,
esm-spec §6.3), which the Rust runner supports.

The schema (esm 1.2.0) defines `default` for a parameter as "its constant value", and solver behavior is derived from
the equations. For this reason the conversion cannot change any computed value. The simulation confirms this: in
the dev1 output, every converted constant equals its new default at every saved time.

### Not converted (deliberately)

| Equation(s) | Why kept |
|---|---|
| `a₀ = 5/(6α)`, `r₀ = √(A𝒻/π₀)`, `uₐ = χ𝑤 uₑ`, `Λᵥ = Lᵥ/cₚφ`, `Λₛ = Lₛ/cₚφ`, `Λ𝒻 = L𝒻/cₚφ`, `ν(k)`, `φₘ = 1/2 + ⌊m𝒻⌋/100` | Time-independent, but *computed from other parameters*. The equation documents the derivation. Replacing it with a literal would hide the derivation and change how the value is evaluated in floating point. |
| 10 initial-condition equations `ic(…)` | Initial conditions, not constant assignments. |
| Everything else (state-dependent quantities, e.g. `ℋ₀`, which depends on t + τₙ) | Changes during the simulation. |

### Remaining unknowns (270)

* 10 prognostic states: temperature, vapor, cloud water, rain, ice, horizontal speed, radius, tracer, vertical velocity
  and carried vertical velocity.
* 8 parameter-derived constants (table above).
* About 60 lower-boundary quantities from the buoyant-source similarity solution and the lower-boundary
  microphysics. They depend on the time-varying heat flux and the boundary state.
* About 120 interior intermediates on the 200-level grids. These are thermodynamic quantities, transport fluxes
  and tendencies, the staged microphysics and the momentum terms.
* 75 output diagnostics. These are plume-top height, maxima and minima, single-level values, budget residuals, and
  the scalar-level buoyancy values `ℬₜ_k` that the Fortran assertions compare. 70 of them feed no other equation.

## B. Readability changes (descriptions only)

All edits are in `description` and `_comment` text: 638 text edits in total. No expression was changed.

* **Converted constants**: each description now states the constant's role and where it is used. For example:
  `gᵦ` is g/(1 + γ) with virtual-mass coefficient γ = 0.5, numerically 9.8/1.5, as in the reference code
  (`umgamai = 1./(1.+gama)`); `cᵢ₀`/`cᵢ₁` are the terms of the ventilation coefficient
  cᵢ = cᵢ₀ + cᵢ₁|w + vᵢ|^1.5/cₘ; `Λᵥᴴ`/`Λ𝒻ᴴ` are marked as diagnostic-only.
* **Transport terms**: one-phrase descriptions such as "Temperature flux" or "Cloud diffusion" now say which
  operator each term is, and on which quantity (eddy-diffusion tendency, upward advective flux through
  velocity-level faces, advection tendency from the flux divergence, sedimentation at a fall speed). The scalar
  and momentum mass fluxes `fρ` and `f𝑤` are described by their formulas.
* **Unit boilerplate**: trailing "Units: …", "Dimensionless." and "Mass basis: kg water per kg dry air." are removed
  from variable descriptions, because the `units` field already carries them. The mass-mixing-ratio convention is
  now stated once in the model description. Expression templates have no `units` field, so they keep their unit
  notes.
* **Model description**: two paragraphs were added. One explains why the model carries water and ice (below). The
  other states the conventions: constants are parameters, and mixing ratios are kg water per kg dry air.
* **Typo**: `ρ_min` described the density as κρpₑ/t (time); corrected to κρpₑ/T (temperature).

## C. The microphysics question

Water processes are part of the plume dynamics, not a side calculation:

* The fire and the entrained air supply water vapor, which condenses as the plume rises and cools.
* Condensation, deposition onto ice and freezing of rain **release latent heat**. This warms the plume and adds
  buoyancy.
* Evaporation, sublimation and melting **absorb heat** and reduce buoyancy.
* Cloud water, rain and ice add **weight**. They enter the buoyancy ℬₜ directly as −(qₗ + qᵣ + qᵢ).
* These effects control the rise of large fire plumes that form pyrocumulus clouds.

What changed:

* The descriptions of all six phase-change stages now say which phase change occurs and its effect on plume
  temperature, and so on buoyancy. This covers vapor, liquid, ice and temperature after each stage, for both the
  interior and the lower boundary. The microphysical temperature tendency `Mₜ` is described as the path by which
  phase changes alter buoyancy.
* The quoted example `qᵣ⁽⁵⁾` now reads: "Rainwater mixing ratio after stage 5, in which part of the rain freezes to
  ice (glaciation) at or below T𝒻. Freezing matters for plume rise because it releases latent heat (see T⁽⁵⁾) that
  adds buoyancy to high, cold plumes."

The model description now says that in the default 0–300 s test the plume stays almost unsaturated. In the
validation run, the largest rain mixing ratio is about 7×10⁻⁹ and the largest cloud water about 10⁻¹⁶. So the
inline tests do not exercise the microphysics.

**Nothing was deleted.** No microphysics variable or equation is unused. Each feeds the temperature and water
tendencies.

### Possible later simplifications (flagged, not performed)

* Seventy output-only diagnostics are not used by any other equation. Twelve of them are assertion targets
  (`hₚ` and `ℬₜ_2`–`ℬₜ_11`, `ℬₜ_20`) and must stay. The other 58 are neither used nor asserted. They are mostly
  per-level buoyancy values `ℬₜ_k`, single-level values such as `T_11` and `w_51`, and profile maxima and minima.
  Removing them would not change the dynamics, but it would change the model's output set. That is a separate
  decision.
* The lower-boundary microphysics repeats the interior sequence with its own variables (`…₀`). Expressing both
  through the shared expression templates would shorten the file. That is a structural change, outside a
  description-only refactor.

## Conversion audit (all 68)

| # | Symbol | Value | Units | Role (new description) |
|---:|---|---:|---|---|
| 1 | `g` | 9.80796 | m/s^2 | Gravitational acceleration in the lower-boundary buoyancy flux f₀ and thermal factor β₀ (the reference code's 9.80796 m/s²). Interior buoyancy uses gᵦ and adiabatic cooling uses Γᴅ. |
| 2 | `Rᴅ` | 287.04 | J/kg/K | Specific gas constant of dry air, used in the lower-boundary buoyancy flux f₀. |
| 3 | `cₚᴅ` | 1004.6 | J/kg/K | Specific heat of dry air at constant pressure, used in the lower-boundary buoyancy flux f₀. |
| 4 | `κρ` | 3483.8 | g*K/m^3/kPa | Air-density coefficient 1/Rᴅ expressed for pressure in kPa and density in g/m³, so that ρ = κρ p/T. |
| 5 | `e₀` | 0.61078 | kPa | Saturation vapor pressure at Tᵣ in the Tetens formula eₛ = e₀ exp[aₑₛ(T − Tᵣ)/(T − Tₑₛ)]. |
| 6 | `Tᵣ` | 273.15 | K | Reference temperature (0 °C) in the Tetens formula eₛ = e₀ exp[aₑₛ(T − Tᵣ)/(T − Tₑₛ)]. |
| 7 | `Tₑₛ` | 35.85 | K | Temperature offset in the denominator of the Tetens formula eₛ = e₀ exp[aₑₛ(T − Tᵣ)/(T − Tₑₛ)]. |
| 8 | `κW` | 1000 | W/kW | Unit conversion from kW to W for the surface heat flux. |
| 9 | `κp` | 1000 | Pa/kPa | Unit conversion from kPa to Pa in the lower-boundary buoyancy flux. |
| 10 | `κg` | 1000 | g/kg | Unit conversion from kg to g in the fire water-vapor increment δq₀. |
| 11 | `κkg` | 0.001 | kg/g | Unit conversion from g to kg; converts air density from g/m³ to kg/m³ in the mass fluxes. |
| 12 | `h𝒻` | 19300000.0 | J/kg | Heat of combustion of the fuel. The surface heat flux divided by η h𝒻 is the fuel burning rate, which sets the fire's water-vapor source δq₀. |
| 13 | `tₘ` | 60 | s | One-minute forcing interval: the heat-flux ramp steps every tₘ, the velocity-filter weight ε changes at tₘ, and the Rayleigh timescale τᴅ is capped at tₘ. |
| 14 | `tᵣ` | 240 | s | End of the heat-flux ramp; the full fire heat flux applies from tᵣ. |
| 15 | `t𝒻` | 3180 | s | End (inclusive) of the full-intensity fire; the post-fire floor ℋₑₙd applies afterwards. |
| 16 | `ℋₘᵢₙ` | 0.1 | W/m^2 | Small surface heat flux applied during the first minute, before the ramp starts. |
| 17 | `ℋₑₙd` | 1e-06 | W/m^2 | Small surface heat flux applied after the fire ends. |
| 18 | `Δz` | 100 | m | Nominal vertical grid spacing, used in the transport timescale, plume-top height, damping onset, initial heights and face reconstruction. |
| 19 | `τₘₐₓ` | 5 | s | Upper bound of the transport timescale; equals the 5 s maximum time step of the reference scheme. |
| 20 | `wₘᵢₙ` | 1 | m/s | Vertical-velocity threshold that defines the plume top (first level with w ≤ wₘᵢₙ) and floor of the speed in the transport timescale. |
| 21 | `rₘᵢₙ` | 1 | m | Minimum plume radius in the entrainment and wind-exchange rates; prevents division by a vanishing radius. |
| 22 | `ℋᴅ` | 2000 | m | Depth scale of the Rayleigh damping layer above the active column. |
| 23 | `νₘᵢₙ` | 0.001 | m^2/s | Minimum eddy diffusivity. |
| 24 | `ν₀` | 500 | m^2/s | Eddy diffusivity at the surface; ν decreases linearly with level index down to νₘᵢₙ. |
| 25 | `vᵢ` | -3 | m/s | Fall speed of ice (negative is downward). Used for ice sedimentation and in the ventilation coefficient for ice sublimation and melting. |
| 26 | `vᵣ` | -4 | m/s | Fall speed of rain (negative is downward), used for rain sedimentation. |
| 27 | `gᵦ` | 6.533333333333334 | m/s^2 | Gravitational coefficient in the buoyancy acceleration, g/(1 + γ) with g = 9.8 m/s² and virtual-mass coefficient γ = 0.5 (numerically 9.8/1.5), as in the reference code. |
| 28 | `Γᴅ` | 0.009770916334661355 | K/m | Dry-adiabatic lapse rate g/cₚ, numerically 9.81/1004; rising plume air cools at the rate w̄Γᴅ. |
| 29 | `Λᵥᴴ` | 2490.03984063745 | K | Latent heat of condensation divided by cₚ (numerically 2.5×10⁶/1004). Used only in the enthalpy-budget diagnostic Rₕ; it does not affect the plume evolution. |
| 30 | `Λ𝒻ᴴ` | 332.66932270916334 | K | Latent heat of fusion divided by cₚ (numerically 3.34×10⁵/1004). Used only in the enthalpy-budget diagnostic Rₕ; it does not affect the plume evolution. |
| 31 | `π₀` | 3.14159 | 1 | Value of π (3.14159) for the source radius, the initial radius and the lower-boundary buoyancy flux, as in the reference code. |
| 32 | `πᵣ` | 3.1416 | 1 | Value of π (3.1416) in the wind-shear radius growth and in κλ and κE; it differs from π₀ as in the reference code. |
| 33 | `εᵥ` | 0.622 | 1 | Ratio of the molar masses of water vapor and dry air. |
| 34 | `aₑₛ` | 17.2693882 | 1 | Exponential coefficient in the Tetens formula eₛ = e₀ exp[aₑₛ(T − Tᵣ)/(T − Tₑₛ)]. |
| 35 | `η` | 0.55 | 1 | Convective fraction of the fire heat release: the part that heats the plume. It also converts the heat flux back to a fuel burning rate in δq₀. |
| 36 | `cᵦ` | 0.9 | 1 | Coefficient of the buoyancy-flux scale B₀ = cᵦ α f₀ in the lower-boundary similarity solution. |
| 37 | `Lᵥ` | 2500.0 | kJ/kg | Latent heat of condensation (vapor ↔ liquid). |
| 38 | `Lₛ` | 2834.0 | kJ/kg | Latent heat of sublimation (vapor ↔ ice). |
| 39 | `L𝒻` | 334.0 | kJ/kg | Latent heat of fusion (liquid ↔ ice). |
| 40 | `cₚφ` | 1.004 | kJ/kg/K | Specific heat that converts latent heat into a temperature change in phase-change heating (Λ = L/cₚφ). |
| 41 | `qε` | 1e-10 | 1 | Smallest condensed-water mixing ratio kept in the microphysics; smaller values are set to zero. |
| 42 | `T𝒻` | 269.3 | K | Temperature threshold for ice processes: deposition onto ice and rain freezing occur at or below T𝒻, and warm-rain conversion requires T > T𝒻. |
| 43 | `Tₘ` | 273.0 | K | Temperature at or above which ice melts to rain. |
| 44 | `aᵣ` | 0.000544 | m^1.95/g^0.65/s | Coefficient of the empirical rain-evaporation rate. |
| 45 | `aᵢ` | 700000.0 | 1 | Constant term in the normalized resistance to vapor transfer between air and ice. |
| 46 | `bᵢ` | 4100000.0 | 1 | Coefficient of the saturation-vapor-pressure term in the normalized ice-transfer resistance. |
| 47 | `κₑ` | 10.0 | 1 | Pressure normalization factor in the empirical ice-transfer resistance; saturation vapor pressure is scaled by 1 kPa. |
| 48 | `κρᵢ` | 1000000.0 | 1 | Reciprocal-density normalization factor in the empirical ice-transfer relation; air density is scaled by 1 g/m³. |
| 49 | `cᵢₛ` | 1.13 | 1 | Coefficient scaling the normalized vapor-transfer driving terms for ice sublimation and deposition. |
| 50 | `a𝒻` | 0.025 | 1/s | Rate coefficient for rain freezing to ice (glaciation): the fraction of rain frozen per second when freezing is possible. |
| 51 | `aₘ` | 2.27 | g/m^3*(cm^3/g)^0.525/s/K | Coefficient of the empirical ice-melting rate. |
| 52 | `κₘ` | 1e-06 | m^3/cm^3 | Unit conversion from g/m³ to g/cm³ for the ice mass concentration in the empirical melting relation. |
| 53 | `cₘ` | 0.75 | 1 | Normalization factor in the ventilation coefficient cᵢ = cᵢ₀ + cᵢ₁/w + vᵢ/^1.5/cₘ and in the melting rate. |
| 54 | `Λₘ` | 332.27 | K | Latent cooling per unit ice mixing ratio melted (latent heat of fusion over heat capacity), used in the melting stage. |
| 55 | `aₐ` | 0.0052 | m^2.625/g^0.875/s | Coefficient of the rate at which rain collects cloud water (accretion). |
| 56 | `cᵤ` | 0.146 | 1 | Coefficient of the autoconversion rate 𝒞ᵤ = cᵤ mₗ³/[tᵤ(aᵤ cᵤ mₗ + bᵤ nᵤ)], which turns cloud water into rain. |
| 57 | `tᵤ` | 60.0 | s | Time scale in the autoconversion rate 𝒞ᵤ = cᵤ mₗ³/[tᵤ(aᵤ cᵤ mₗ + bᵤ nᵤ)]. |
| 58 | `aᵤ` | 5.0 | g/m^3 | Concentration coefficient in the denominator of the autoconversion rate 𝒞ᵤ = cᵤ mₗ³/[tᵤ(aᵤ cᵤ mₗ + bᵤ nᵤ)]. |
| 59 | `bᵤ` | 0.0366 | (g/m^3)^2*cm^3 | Mass coefficient in the denominator of the autoconversion rate 𝒞ᵤ = cᵤ mₗ³/[tᵤ(aᵤ cᵤ mₗ + bᵤ nᵤ)]. |
| 60 | `nᵤ` | 100000.0 | 1/cm^3 | Cloud-droplet number concentration in the autoconversion rate 𝒞ᵤ = cᵤ mₗ³/[tᵤ(aᵤ cᵤ mₗ + bᵤ nᵤ)]. |
| 61 | `cᵢ₀` | 1.6 | 1 | Constant term of the ventilation coefficient cᵢ = cᵢ₀ + cᵢ₁/w + vᵢ/^1.5/cₘ, which increases ice sublimation and melting because air flows past falling ice. |
| 62 | `cᵢ₁` | 0.00057 | (s/m)^1.5 | Speed coefficient of the ventilation coefficient cᵢ = cᵢ₀ + cᵢ₁/w + vᵢ/^1.5/cₘ. |
| 63 | `ε₁` | 0.2 | 1 | Velocity-filter weight ε after the first minute (ε = 1/2 before then). |
| 64 | `aᵣ₀` | 1.2 | 1 | Coefficient of the initial radius profile r = r₀ + aᵣ₀ α z. |
| 65 | `κλ` | 0.6366182836771073 | 1 | Coefficient 2/πᵣ of the wind-driven exchange rate λ𝑤. |
| 66 | `κE` | 0.31830914183855363 | 1 | Coefficient 1/πᵣ of the wind-driven vertical-momentum loss in E𝑤. |
| 67 | `aᵣ₁` | 0.6 | 1 | Coefficient of radius growth by entrainment, aᵣ₁ λ r, in the radius tendency. |
| 68 | `q∅` | 0 | 1 (per level, zt) | Ambient mixing ratio of cloud water, rain, ice and tracer: zero, so exchange with ambient air only dilutes these quantities. |

## Reproduction

dev2 is generated deterministically from dev1 by a script that derives the conversion set from the source. A
rebuild reproduces the SHA-256 above. An independent structural checker confirms the following:

* the only differences are the 68 conversions and description text;
* every remaining equation, template, initial condition, test and solver field is byte-for-byte identical in JSON;
* the 57 assertions equal those of v0.10.9.

The checker was tested with three deliberate mutations (a parameter value, an equation, a tolerance) and rejected
all three. Validation commands, using the official runner: `esm validate`, `esm units --check`,
`esm test --verbose`, and `esm simulate --time 300 --format flat` for dev1 and dev2. The outputs were then compared
at every saved time with the pass rule |a − b| ≤ 1e‑12 + 1e‑6·max(|a|, |b|). The result was bit-identical.

## Scope and limitations

The 57 inline assertions screen early-time behavior (0–300 s) against the Freitas-derived Fortran. They do not
validate full-duration, variable-time-step or wet (precipitating/glaciating) behavior; see the model description.
This refactor inherits the scientific status of v0.10.10-dev1 unchanged. Only the Rust runner was used. The Python
and Julia runners were not run for this change.
