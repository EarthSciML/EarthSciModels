---
title: "Freitas2007FortranComparison"
slug: "freitas2007fortrancomparison"
domains: ["environmental_transport"]
component_types: ["model"]
subdomains: ["plume_rise"]
domain: "environmental_transport"
subdomain: "plume_rise"
component_type: "model"
esm_version: "2.0.0"
esm_path: "components/environmental_transport/plume_rise/freitas_2007_tests.esm"
description: "Time-dependent tests of the Freitas (2007) plume-rise model (freitas_2007.esm), mounted here on a shorter and coarser column so that they run in seconds: NLEV = 52 levels bound at the mount, Δz = 200 m (top at 10.25 km, enough for the plume top at 5.8 km plus the 4 km sponge). The ambient sounding is the model default (Williams Flats), interpolated to this grid. On the default 200-level, 100 m column the same 20-minute integration takes several minutes with the implicit solver (cost grows with the square of the number of states), which is why the comparison with the reference Fortran lives here; the Fortran was run on the same 200 m grid. freitas_2007.esm itself carries an instantaneous test of its default configuration. The one test covers the dry rise, cloud formation, rain and ice; see its description for the provenance of the expected values."
tags: ["environmental_transport", "plume_rise", "model", "plume-rise", "wildfire", "pyrocumulus", "cloud-microphysics", "freitas", "column-model", "tests"]
---

## Description

Time-dependent tests of the Freitas (2007) plume-rise model (freitas_2007.esm), mounted here on a shorter and coarser column so that they run in seconds: NLEV = 52 levels bound at the mount, Δz = 200 m (top at 10.25 km, enough for the plume top at 5.8 km plus the 4 km sponge). The ambient sounding is the model default (Williams Flats), interpolated to this grid. On the default 200-level, 100 m column the same 20-minute integration takes several minutes with the implicit solver (cost grows with the square of the number of states), which is why the comparison with the reference Fortran lives here; the Fortran was run on the same 200 m grid. freitas_2007.esm itself carries an instantaneous test of its default configuration. The one test covers the dry rise, cloud formation, rain and ice; see its description for the provenance of the expected values.

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "variables": {},
  "subsystems": {
    "plume": {
      "ref": "./freitas_2007.esm",
      "bindings": {
        "NLEV": 52
      }
    }
  },
  "equations": [],
  "tests": [
    {
      "id": "williams_flats_maritime_200m",
      "description": "Williams Flats fire (2.56 kW/m2, 750 ha) on a 52-level, 200 m column with the maritime Berry autoconversion of the Fortran (droplet number 50 per cm3, dispersion 0.366), so that within 20 minutes the plume rises dry, forms a pyrocumulus cloud, rains, and the rain partly freezes and grows ice. At 300 s: plume top, vertical velocity, temperature excess, vapor and tracer of the dry rise. At 1200 s (plume top 5.8 km): the same through the column, and cloud water, rain and ice through the cloud. Reference: the stand-alone Fortran (tartanrunner25/Plume-model_stand_alone at 9265514, GNU Fortran 11.5.0 -O3) with the Williams Flats inputs, built with the corrections listed as departures (1)-(4) and (7)-(10) of freitas_2007.esm (preprocessor flags FIX_PR FIX_SED FIX_SUBL FIX_LEAPFROG), the maritime Berry parameters (MARITIME), a 200 m grid (GRIDDZ=200), its maximum time step reduced from 5 s to 0.2 s (DTMAX) and its sponge time fixed at 15 s (FIXED_SPONGE), so that it approximates the continuous-time limit the model represents. Values are interpolated linearly in time between the two Fortran steps that bracket the assertion time and converted to the state units (temperature excess T - Te, water in g/kg, tracer as a fraction of the boundary value 1000). Tolerances are about twice the largest model-reference difference measured for each field over the asserted levels (one tolerance per field and time), with floors of 0.2 % (relative), 0.02 K and one grid level (200 m) for hp. Levels at the advancing plume head, where the reference itself changes by several per cent between 0.2 s and 0.1 s steps, are not asserted. Parameter overrides: Δz = 200 m with the Fortran sponge depth (20 levels, ℋᴅ = 4000 m) and eddy-diffusivity taper (ν₀/200 per level, ℓν = 40 km) of that grid; nᵤ and cᵤ maritime.",
      "time_span": {
        "start": 0,
        "end": 1200.0
      },
      "assertions": [
        {
          "variable": "plume.hₚ",
          "time": 300.0,
          "expected": 1400.0,
          "tolerance": {
            "abs": 200.0
          }
        },
        {
          "variable": "plume.hₚ",
          "time": 1200.0,
          "expected": 5800.0,
          "tolerance": {
            "abs": 200.0
          }
        },
        {
          "variable": "plume.velocity_state[2]",
          "time": 300.0,
          "expected": 9.44161,
          "tolerance": {
            "rel": 0.02
          }
        },
        {
          "variable": "plume.velocity_state[3]",
          "time": 300.0,
          "expected": 9.43586,
          "tolerance": {
            "rel": 0.02
          }
        },
        {
          "variable": "plume.velocity_state[4]",
          "time": 300.0,
          "expected": 9.06975,
          "tolerance": {
            "rel": 0.02
          }
        },
        {
          "variable": "plume.velocity_state[5]",
          "time": 300.0,
          "expected": 7.31544,
          "tolerance": {
            "rel": 0.02
          }
        },
        {
          "variable": "plume.temperature_state[2]",
          "time": 300.0,
          "expected": 0.9552,
          "tolerance": {
            "abs": 0.04
          }
        },
        {
          "variable": "plume.temperature_state[3]",
          "time": 300.0,
          "expected": 0.976593,
          "tolerance": {
            "abs": 0.04
          }
        },
        {
          "variable": "plume.temperature_state[4]",
          "time": 300.0,
          "expected": 1.00769,
          "tolerance": {
            "abs": 0.04
          }
        },
        {
          "variable": "plume.temperature_state[5]",
          "time": 300.0,
          "expected": 0.923157,
          "tolerance": {
            "abs": 0.04
          }
        },
        {
          "variable": "plume.vapor_state[3]",
          "time": 300.0,
          "expected": 7.67324,
          "tolerance": {
            "rel": 0.002
          }
        },
        {
          "variable": "plume.vapor_state[5]",
          "time": 300.0,
          "expected": 7.57553,
          "tolerance": {
            "rel": 0.002
          }
        },
        {
          "variable": "plume.tracer_state[3]",
          "time": 300.0,
          "expected": 0.92291,
          "tolerance": {
            "rel": 0.007
          }
        },
        {
          "variable": "plume.tracer_state[5]",
          "time": 300.0,
          "expected": 0.784289,
          "tolerance": {
            "rel": 0.007
          }
        },
        {
          "variable": "plume.velocity_state[6]",
          "time": 1200.0,
          "expected": 9.88712,
          "tolerance": {
            "rel": 0.008
          }
        },
        {
          "variable": "plume.velocity_state[10]",
          "time": 1200.0,
          "expected": 10.8729,
          "tolerance": {
            "rel": 0.008
          }
        },
        {
          "variable": "plume.velocity_state[14]",
          "time": 1200.0,
          "expected": 10.8896,
          "tolerance": {
            "rel": 0.008
          }
        },
        {
          "variable": "plume.velocity_state[18]",
          "time": 1200.0,
          "expected": 9.41969,
          "tolerance": {
            "rel": 0.008
          }
        },
        {
          "variable": "plume.velocity_state[22]",
          "time": 1200.0,
          "expected": 10.0077,
          "tolerance": {
            "rel": 0.008
          }
        },
        {
          "variable": "plume.temperature_state[6]",
          "time": 1200.0,
          "expected": 1.0159,
          "tolerance": {
            "abs": 0.06
          }
        },
        {
          "variable": "plume.temperature_state[10]",
          "time": 1200.0,
          "expected": 0.451874,
          "tolerance": {
            "abs": 0.06
          }
        },
        {
          "variable": "plume.temperature_state[14]",
          "time": 1200.0,
          "expected": -0.368713,
          "tolerance": {
            "abs": 0.06
          }
        },
        {
          "variable": "plume.temperature_state[20]",
          "time": 1200.0,
          "expected": 0.38557,
          "tolerance": {
            "abs": 0.06
          }
        },
        {
          "variable": "plume.temperature_state[22]",
          "time": 1200.0,
          "expected": 1.45007,
          "tolerance": {
            "abs": 0.06
          }
        },
        {
          "variable": "plume.vapor_state[10]",
          "time": 1200.0,
          "expected": 7.47812,
          "tolerance": {
            "rel": 0.003
          }
        },
        {
          "variable": "plume.vapor_state[20]",
          "time": 1200.0,
          "expected": 6.1119,
          "tolerance": {
            "rel": 0.003
          }
        },
        {
          "variable": "plume.vapor_state[24]",
          "time": 1200.0,
          "expected": 4.6526,
          "tolerance": {
            "rel": 0.003
          }
        },
        {
          "variable": "plume.tracer_state[10]",
          "time": 1200.0,
          "expected": 0.748552,
          "tolerance": {
            "rel": 0.02
          }
        },
        {
          "variable": "plume.tracer_state[20]",
          "time": 1200.0,
          "expected": 0.579495,
          "tolerance": {
            "rel": 0.02
          }
        },
        {
          "variable": "plume.tracer_state[26]",
          "time": 1200.0,
          "expected": 0.479058,
          "tolerance": {
            "rel": 0.02
          }
        },
        {
          "variable": "plume.cloud_state[20]",
          "time": 1200.0,
          "expected": 0.609843,
          "tolerance": {
            "rel": 0.03
          }
        },
        {
          "variable": "plume.cloud_state[22]",
          "time": 1200.0,
          "expected": 1.10119,
          "tolerance": {
            "rel": 0.03
          }
        },
        {
          "variable": "plume.cloud_state[24]",
          "time": 1200.0,
          "expected": 1.61341,
          "tolerance": {
            "rel": 0.03
          }
        },
        {
          "variable": "plume.cloud_state[26]",
          "time": 1200.0,
          "expected": 1.95135,
          "tolerance": {
            "rel": 0.03
          }
        },
        {
          "variable": "plume.rain_state[22]",
          "time": 1200.0,
          "expected": 0.0997241,
          "tolerance": {
            "rel": 0.2
          }
        },
        {
          "variable": "plume.rain_state[24]",
          "time": 1200.0,
          "expected": 0.0312703,
          "tolerance": {
            "rel": 0.2
          }
        },
        {
          "variable": "plume.rain_state[26]",
          "time": 1200.0,
          "expected": 0.0102704,
          "tolerance": {
            "rel": 0.2
          }
        },
        {
          "variable": "plume.ice_state[24]",
          "time": 1200.0,
          "expected": 0.0541616,
          "tolerance": {
            "rel": 0.2
          }
        },
        {
          "variable": "plume.ice_state[26]",
          "time": 1200.0,
          "expected": 0.062762,
          "tolerance": {
            "rel": 0.2
          }
        }
      ],
      "parameter_overrides": {
        "plume.Δz": 200.0,
        "plume.ℋᴅ": 4000.0,
        "plume.ℓν": 40000.0,
        "plume.nᵤ": 50.0,
        "plume.cᵤ": 0.366
      }
    }
  ]
}
```

</details>
