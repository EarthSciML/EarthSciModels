---
title: "Species"
slug: "species"
domains: ["aerosol"]
component_types: ["model"]
subdomains: ["isorropia"]
domain: "aerosol"
subdomain: "isorropia"
component_type: "model"
esm_version: "1.0.0"
esm_path: "components/aerosol/isorropia/species.esm"
reference: "Fountoukis, C. and Nenes, A. (2007) ISORROPIA II, Atmos. Chem. Phys. 7(17), 4639–4659 — total-species mass-balance constraint. Migrated from Aerosol.jl src/isorropia/isorropia.jl `Species` (esm-bvu)."
description: "Conserved total concentration of a single inorganic aerosol species (e.g. NH, Na, Ca, K, Mg, Cl, NO3, SO4) in the ISORROPIA v1 thermodynamic equilibrium model. The total concentration `total` is held constant over time (D(total)/dt = 0), representing the user-supplied input constraint: the total moles per unit air volume of that ionic group across all phases (gas + aqueous + solid). This component is instantiated once per tracked ion group inside the top-level Isorropia system. Migrated from Aerosol.jl src/isorropia/isorropia.jl `Species`."
tags: ["aerosol", "isorropia", "model", "thermodynamic-equilibrium", "inorganic-chemistry", "mass-balance", "fountoukis-nenes"]
---

## Description

Conserved total concentration of a single inorganic aerosol species (e.g. NH, Na, Ca, K, Mg, Cl, NO3, SO4) in the ISORROPIA v1 thermodynamic equilibrium model. The total concentration `total` is held constant over time (D(total)/dt = 0), representing the user-supplied input constraint: the total moles per unit air volume of that ionic group across all phases (gas + aqueous + solid). This component is instantiated once per tracked ion group inside the top-level Isorropia system. Migrated from Aerosol.jl src/isorropia/isorropia.jl `Species`.

## Reference

Fountoukis, C. and Nenes, A. (2007) ISORROPIA II, Atmos. Chem. Phys. 7(17), 4639–4659 — total-species mass-balance constraint. Migrated from Aerosol.jl src/isorropia/isorropia.jl `Species` (esm-bvu).

_source_ref: Aerosol.jl@c8c640bb:src/isorropia/isorropia.jl:100

Upstream `Species` is an MTK @component that takes a single constructor keyword argument `M_total` (default: nothing) used as the default initial condition for the state variable `total(t)`. The single equation D(total) ~ 0 makes `total` a conserved quantity — it retains whatever initial value it is given for the entire simulation.

In the full Isorropia component, eight Species instances are created:
  NH = Species(name=:NH, M_total=2.0e-7)   — ammonium total [mol/m³]
  Na = Species(name=:Na, M_total=4.0e-10)  — sodium
  Ca = Species(name=:Ca, M_total=1.0e-8)   — calcium
  K  = Species(name=:K,  M_total=8.4e-9)   — potassium
  Mg = Species(name=:Mg, M_total=4.1e-10)  — magnesium
  Cl = Species(name=:Cl, M_total=2.7e-10)  — chloride
  NO3= Species(name=:NO3,M_total=3.2e-8)   — nitrate
  SO4= Species(name=:SO4,M_total=1.0e-7)   — sulfate

Each instance supplies its `total` variable as a source term for the mass-balance equations inside Isorropia. The `total` value is pinned by the user-specified initial condition; D(total)=0 prevents the ODE solver from drifting it.

ESM design notes:
  - `M_total` is represented as an ESM parameter (the user-configured total concentration). Its default 1.0e-7 mol/m³ matches the NH usage in Isorropia. Users should set both `M_total` and the initial condition of `total` to the same value.
  - `total` is a state variable (it is declared in @variables in the Julia source). The equation D(total)=0 is encoded as an ODE equation in the `equations` block.
  - Because D(total)=0 holds for all t, total is trivially constant; tests verify it equals its initial value at multiple time points.

Tolerance rationale (model-level rel=1e-12): the system is a single ODE with zero RHS. The solver integrates a trivial zero derivative; floating-point round-off in the integrator step is bounded by the machine epsilon (~1e-15 relative). rel=1e-12 leaves three orders of margin while catching any regression._

## Variables

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `total` | `mol/m^3` |  | Total molar concentration of the ion group (mol m⁻³), conserved over time by D(total)/dt = 0. Initialize to M_total before solving. Linked to the Isorropia mass-balance equations: e.g. NH.total = g.NH3.M + aq.NH3.M + aq.NH3_dissociated.M. |

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `M_total` | `mol/m^3` | `1e-07` | User-specified total molar concentration of this ionic species across all phases (gas + aqueous + solid). Sets the initial condition for `total` and constrains it to remain constant throughout the simulation. Default 1.0e-7 mol/m³ matches the SO4 and NH usage in Isorropia. Units: mol m⁻³. |

## Equations

$$
\mathrm{D}\left(total\right) = 0.0
$$

## Analyses

### total_concentration_over_time

Evolution of the total species concentration over 100 s starting from M_total = 2.0e-7 mol/m³ (NH conditions). The D(total)/dt = 0 equation produces a flat trajectory at the initial value, illustrating that Species is a pure mass-balance constraint component.

**Time span:** 0.0 → 100.0

![Total concentration `total` (mol m⁻³) versus time. Flat at 2.0×10⁻⁷ mol/m³ for all t, confirming exact conservation.](/plots/aerosol/isorropia/species/total_concentration_over_time-total_vs_time.png)

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "reference": {
    "citation": "Fountoukis, C. and Nenes, A. (2007) ISORROPIA II, Atmos. Chem. Phys. 7(17), 4639–4659 — total-species mass-balance constraint. Migrated from Aerosol.jl src/isorropia/isorropia.jl `Species` (esm-bvu).",
    "notes": "source_ref: Aerosol.jl@c8c640bb:src/isorropia/isorropia.jl:100\n\nUpstream `Species` is an MTK @component that takes a single constructor keyword argument `M_total` (default: nothing) used as the default initial condition for the state variable `total(t)`. The single equation D(total) ~ 0 makes `total` a conserved quantity — it retains whatever initial value it is given for the entire simulation.\n\nIn the full Isorropia component, eight Species instances are created:\n  NH = Species(name=:NH, M_total=2.0e-7)   — ammonium total [mol/m³]\n  Na = Species(name=:Na, M_total=4.0e-10)  — sodium\n  Ca = Species(name=:Ca, M_total=1.0e-8)   — calcium\n  K  = Species(name=:K,  M_total=8.4e-9)   — potassium\n  Mg = Species(name=:Mg, M_total=4.1e-10)  — magnesium\n  Cl = Species(name=:Cl, M_total=2.7e-10)  — chloride\n  NO3= Species(name=:NO3,M_total=3.2e-8)   — nitrate\n  SO4= Species(name=:SO4,M_total=1.0e-7)   — sulfate\n\nEach instance supplies its `total` variable as a source term for the mass-balance equations inside Isorropia. The `total` value is pinned by the user-specified initial condition; D(total)=0 prevents the ODE solver from drifting it.\n\nESM design notes:\n  - `M_total` is represented as an ESM parameter (the user-configured total concentration). Its default 1.0e-7 mol/m³ matches the NH usage in Isorropia. Users should set both `M_total` and the initial condition of `total` to the same value.\n  - `total` is a state variable (it is declared in @variables in the Julia source). The equation D(total)=0 is encoded as an ODE equation in the `equations` block.\n  - Because D(total)=0 holds for all t, total is trivially constant; tests verify it equals its initial value at multiple time points.\n\nTolerance rationale (model-level rel=1e-12): the system is a single ODE with zero RHS. The solver integrates a trivial zero derivative; floating-point round-off in the integrator step is bounded by the machine epsilon (~1e-15 relative). rel=1e-12 leaves three orders of margin while catching any regression."
  },
  "tolerance": {
    "rel": 1e-12
  },
  "variables": {
    "M_total": {
      "type": "parameter",
      "units": "mol/m^3",
      "default": 1e-07,
      "description": "User-specified total molar concentration of this ionic species across all phases (gas + aqueous + solid). Sets the initial condition for `total` and constrains it to remain constant throughout the simulation. Default 1.0e-7 mol/m³ matches the SO4 and NH usage in Isorropia. Units: mol m⁻³."
    },
    "total": {
      "type": "unknown",
      "units": "mol/m^3",
      "description": "Total molar concentration of the ion group (mol m⁻³), conserved over time by D(total)/dt = 0. Initialize to M_total before solving. Linked to the Isorropia mass-balance equations: e.g. NH.total = g.NH3.M + aq.NH3.M + aq.NH3_dissociated.M."
    }
  },
  "equations": [
    {
      "_comment": "D(total)/dt = 0 — total concentration is conserved; the initial condition (= M_total) is never altered by the ODE solver.",
      "lhs": {
        "op": "D",
        "wrt": "t",
        "args": [
          "total"
        ]
      },
      "rhs": 0.0
    }
  ],
  "tests": [
    {
      "id": "nh_total_concentration_conserved",
      "description": "NH species with M_total = 2.0e-7 mol/m³ (typical ammonium total in Isorropia, matching Aerosol.jl default). D(total)/dt = 0 keeps total constant at its initial value 2.0e-7 mol/m³ for all t. Sampled at t=0, 1 s, and 100 s to confirm no drift.",
      "time_span": {
        "start": 0.0,
        "end": 100.0
      },
      "parameter_overrides": {
        "M_total": 2e-07
      },
      "initial_conditions": {
        "total": 2e-07
      },
      "assertions": [
        {
          "variable": "total",
          "time": 0.0,
          "expected": 2e-07,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "total",
          "time": 1.0,
          "expected": 2e-07,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "total",
          "time": 100.0,
          "expected": 2e-07,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "so4_total_concentration_conserved",
      "description": "SO4 species with M_total = 1.0e-7 mol/m³ (default value, typical sulfate total in Isorropia). D(total)/dt = 0 keeps total constant at 1.0e-7 mol/m³. Verifies the default parametrisation is self-consistent.",
      "time_span": {
        "start": 0.0,
        "end": 100.0
      },
      "initial_conditions": {
        "total": 1e-07
      },
      "assertions": [
        {
          "variable": "total",
          "time": 0.0,
          "expected": 1e-07,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "total",
          "time": 50.0,
          "expected": 1e-07,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "total",
          "time": 100.0,
          "expected": 1e-07,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "ca_total_concentration_conserved",
      "description": "Ca species with M_total = 1.0e-8 mol/m³ (typical calcium total in Isorropia). Tests a lower-concentration trace species; total must remain at 1.0e-8 mol/m³ for all t.",
      "time_span": {
        "start": 0.0,
        "end": 1000.0
      },
      "parameter_overrides": {
        "M_total": 1e-08
      },
      "initial_conditions": {
        "total": 1e-08
      },
      "assertions": [
        {
          "variable": "total",
          "time": 0.0,
          "expected": 1e-08,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "total",
          "time": 500.0,
          "expected": 1e-08,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "total",
          "time": 1000.0,
          "expected": 1e-08,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    },
    {
      "id": "na_trace_species_conserved",
      "description": "Na species with M_total = 4.0e-10 mol/m³ (sub-ppb trace species). Verifies that very small concentrations are conserved without numerical underflow or drift over 1000 s.",
      "time_span": {
        "start": 0.0,
        "end": 1000.0
      },
      "parameter_overrides": {
        "M_total": 4e-10
      },
      "initial_conditions": {
        "total": 4e-10
      },
      "assertions": [
        {
          "variable": "total",
          "time": 0.0,
          "expected": 4e-10,
          "tolerance": {
            "rel": 1e-12
          }
        },
        {
          "variable": "total",
          "time": 1000.0,
          "expected": 4e-10,
          "tolerance": {
            "rel": 1e-12
          }
        }
      ]
    }
  ],
  "analyses": [
    {
      "id": "total_concentration_over_time",
      "description": "Evolution of the total species concentration over 100 s starting from M_total = 2.0e-7 mol/m³ (NH conditions). The D(total)/dt = 0 equation produces a flat trajectory at the initial value, illustrating that Species is a pure mass-balance constraint component.",
      "initial_state": {
        "total": 2e-07
      },
      "parameters": {
        "M_total": 2e-07
      },
      "time_span": {
        "start": 0.0,
        "end": 100.0
      },
      "plots": [
        {
          "id": "total_vs_time",
          "type": "line",
          "description": "Total concentration `total` (mol m⁻³) versus time. Flat at 2.0×10⁻⁷ mol/m³ for all t, confirming exact conservation.",
          "x": {
            "variable": "t",
            "label": "Time (s)"
          },
          "y": {
            "variable": "total",
            "label": "Total concentration (mol/m³)"
          }
        }
      ]
    }
  ]
}
```

</details>
