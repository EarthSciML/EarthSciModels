---
title: "StochasticCollectionConstant"
slug: "stochasticcollectionconstant"
domains: ["aerosol"]
component_types: ["model"]
domain: "aerosol"
component_type: "model"
esm_version: "1.0.0"
esm_path: "components/aerosol/stochastic_collection.esm"
reference: "10.1175/1520-0469(1989)046<3312:TEORSP>2.0.CO;2"
description: "Two-moment stochastic collection equation (SCE) for cloud-droplet coalescence (Tzivion, Feingold & Levin 1989), scalarized to I=5 mass-doubling categories. Two models, one per collection kernel: StochasticCollectionConstant (K=K0) and StochasticCollectionGolovin (K=C(x+y)). Each tracks number concentration N_k and mass concentration M_k in every category and closes the higher moments with the non-dimensional parameter xi_p. Migrated from the array-variable @component in Aerosol.jl src/stochastic_collection.jl @ c8c640bb636b22f2425460e9ed5cba50793bfee1 (esm-ar1e); the upstream @arrayop/@makearray array operations were scalarized to flat scalar states and equations."
tags: ["aerosol", "model", "cloud-microphysics", "coalescence", "stochastic-collection-equation", "two-moment", "size-distribution"]
---

## Description

Two-moment stochastic collection equation (SCE) for cloud-droplet coalescence (Tzivion, Feingold & Levin 1989), scalarized to I=5 mass-doubling categories. Two models, one per collection kernel: StochasticCollectionConstant (K=K0) and StochasticCollectionGolovin (K=C(x+y)). Each tracks number concentration N_k and mass concentration M_k in every category and closes the higher moments with the non-dimensional parameter xi_p. Migrated from the array-variable @component in Aerosol.jl src/stochastic_collection.jl @ c8c640bb636b22f2425460e9ed5cba50793bfee1 (esm-ar1e); the upstream @arrayop/@makearray array operations were scalarized to flat scalar states and equations.

## Reference

Tzivion, S., Feingold, G., and Levin, Z.: The Evolution of Raindrop Spectra. Part II: Collisional Collection/Breakup and Evaporation in a Rainshaft, J. Atmos. Sci., 46(21), 3312-3327, 1989.

_Source: Aerosol.jl src/stochastic_collection.jl @ c8c640bb636b22f2425460e9ed5cba50793bfee1 (migration bead esm-ar1e); the upstream @component StochasticCollectionCoalescence with kernel_type=constant. The upstream model solves the two-moment stochastic collection equation (SCE) for cloud-droplet coalescence (Tzivion et al. 1989) over I mass-doubling categories, tracking number N_k and mass M_k per category. It is built with symbolic array operations (SymbolicUtils @arrayop/@makearray over array variables Nk(t)[1:I], Mk(t)[1:I]); the array ops are not in the .esm closed AST and the ESS Python runner does not evaluate them, so the model is scalarized to I=5 categories and 10 scalar differential states N1..N5, M1..M5. The scalarization evaluates the upstream @arrayop ifelse masks (i==1, i<=k-2, i<=k-1, i>=k+1) at concrete (k,i), so the flat equations are the source semantics, not a hand-derived rewrite. The five (six for Golovin) closure families are carried as algebraic states with explicit equations (rig convention; cf. components/aerosol/tomas.esm): xb_k (mean mass M_k/N_k), Z_k/Q_k/R_k (higher moments xi_p*M^2/N, xi_p^2*M^3/N^2, xi_p^3*M^4/N^3), and f_k/psi_k/alpha_k (linear within-category reconstruction coefficients, Eq. 13+15). The upstream closures guard m/n divisions with ifelse(n>0,...); the .esm replaces each by the algebraically equivalent floored form m*n/(n^2+1e-300) etc. — bit-identical to m/n for every n>0 that occurs (n>=1e-20 makes the 1e-300 floor ~260 orders below rounding), finite at n=0, and free of the ifelse-guarded divide-by-zero that the runner's eager Piecewise lowering would otherwise hit. Kernel: constant kernel K(x,y)=K0. Verification: the scalarized RHS was checked (1) by a line-by-line transcription audit against the upstream @arrayop bodies; (2) against an independent literal double-sum implementation of the same @arrayop semantics (agreement < 1e-9 relative over random states); and (3) against first-principles no-overflow analytic identities — with the top category empty, no collision product exceeds the grid, so collection conserves number per collision and conserves mass exactly: dN_tot/dt = -(K0/2)*N_tot^2 (constant kernel) and dN_tot/dt = -C*M_tot*N_tot (Golovin kernel), with dM_tot/dt = 0. The scalarized RHS reproduces all three identities to machine precision (relative error 0). Inline-test expected values are a SciPy LSODA reference integration (rtol=1e-10, abstol=1e-14) of this verified RHS; the gate re-integrates the .esm with SciPy LSODA, and the model-level rel=2e-3 tolerance (as for tomas.esm) covers integrator-detail differences. This migration covers only collisional collection; the breakup, evaporation and sedimentation processes of the full 1989 paper are not implemented upstream either._
- **DOI**: 10.1175/1520-0469(1989)046<3312:TEORSP>2.0.CO;2
- **URL**: https://doi.org/10.1175/1520-0469(1989)046%3C3312:TEORSP%3E2.0.CO;2

## Variables

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `N1` | `m^-3` | `1429670.6078643417` | Number concentration of cloud droplets in mass category 1 (of 5); lower mass boundary x_1 = 1.600000e-14 kg. |
| `N2` | `m^-3` | `2838836.0713738734` | Number concentration of cloud droplets in mass category 2 (of 5); lower mass boundary x_2 = 3.200000e-14 kg. |
| `N3` | `m^-3` | `5596563.981307812` | Number concentration of cloud droplets in mass category 3 (of 5); lower mass boundary x_3 = 6.400000e-14 kg. |
| `N4` | `m^-3` | `10875864.787608625` | Number concentration of cloud droplets in mass category 4 (of 5); lower mass boundary x_4 = 1.280000e-13 kg. |
| `N5` | `m^-3` | `20538015.50564386` | Number concentration of cloud droplets in mass category 5 (of 5); lower mass boundary x_5 = 2.560000e-13 kg. |
| `M1` | `kg*m^-3` | `3.430294470019302e-08` | Mass concentration of cloud droplets in mass category 1 (of 5). |
| `M2` | `kg*m^-3` | `1.3619145733423377e-07` | Mass concentration of cloud droplets in mass category 2 (of 5). |
| `M3` | `kg*m^-3` | `5.366970575748642e-07` | Mass concentration of cloud droplets in mass category 3 (of 5). |
| `M4` | `kg*m^-3` | `2.083711394480048e-06` | Mass concentration of cloud droplets in mass category 4 (of 5). |
| `M5` | `kg*m^-3` | `7.852951776977424e-06` | Mass concentration of cloud droplets in mass category 5 (of 5). |

## Parameters

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `XI_P` | `1` | `1.0625` | Closure parameter xi_p (= 17/16) relating the higher-order moments Z_k, Q_k, R_k to N_k and M_k (Tzivion et al. 1989, Eq. 8a,b). |
| `K0` | `m^3/s` | `1e-10` | Constant collection-kernel coefficient: K(x,y) = K0. |

## Observed

| Name | Units | Default | Description |
| --- | --- | --- | --- |
| `xb1` | `kg` |  | Mean droplet mass M_1/N_1 in category 1; algebraic. Denominator floored by 1e-300 so the closure stays finite for an empty category. |
| `xb2` | `kg` |  | Mean droplet mass M_2/N_2 in category 2; algebraic. Denominator floored by 1e-300 so the closure stays finite for an empty category. |
| `xb3` | `kg` |  | Mean droplet mass M_3/N_3 in category 3; algebraic. Denominator floored by 1e-300 so the closure stays finite for an empty category. |
| `xb4` | `kg` |  | Mean droplet mass M_4/N_4 in category 4; algebraic. Denominator floored by 1e-300 so the closure stays finite for an empty category. |
| `xb5` | `kg` |  | Mean droplet mass M_5/N_5 in category 5; algebraic. Denominator floored by 1e-300 so the closure stays finite for an empty category. |
| `Z1` | `kg^2*m^-3` |  | Second-moment closure quantity xi_p*M_1^2/N_1 for category 1; algebraic. |
| `Z2` | `kg^2*m^-3` |  | Second-moment closure quantity xi_p*M_2^2/N_2 for category 2; algebraic. |
| `Z3` | `kg^2*m^-3` |  | Second-moment closure quantity xi_p*M_3^2/N_3 for category 3; algebraic. |
| `Z4` | `kg^2*m^-3` |  | Second-moment closure quantity xi_p*M_4^2/N_4 for category 4; algebraic. |
| `Z5` | `kg^2*m^-3` |  | Second-moment closure quantity xi_p*M_5^2/N_5 for category 5; algebraic. |
| `Q1` | `kg^3*m^-3` |  | Third-moment closure quantity xi_p^2*M_1^3/N_1^2 for category 1; algebraic. |
| `Q2` | `kg^3*m^-3` |  | Third-moment closure quantity xi_p^2*M_2^3/N_2^2 for category 2; algebraic. |
| `Q3` | `kg^3*m^-3` |  | Third-moment closure quantity xi_p^2*M_3^3/N_3^2 for category 3; algebraic. |
| `Q4` | `kg^3*m^-3` |  | Third-moment closure quantity xi_p^2*M_4^3/N_4^2 for category 4; algebraic. |
| `Q5` | `kg^3*m^-3` |  | Third-moment closure quantity xi_p^2*M_5^3/N_5^2 for category 5; algebraic. |
| `f1` | `kg^-1*m^-3` |  | Linear within-category number-distribution coefficient f_1 (Eq. 13a) with the positivity constraint Eq. 15 applied; algebraic. |
| `f2` | `kg^-1*m^-3` |  | Linear within-category number-distribution coefficient f_2 (Eq. 13a) with the positivity constraint Eq. 15 applied; algebraic. |
| `f3` | `kg^-1*m^-3` |  | Linear within-category number-distribution coefficient f_3 (Eq. 13a) with the positivity constraint Eq. 15 applied; algebraic. |
| `f4` | `kg^-1*m^-3` |  | Linear within-category number-distribution coefficient f_4 (Eq. 13a) with the positivity constraint Eq. 15 applied; algebraic. |
| `f5` | `kg^-1*m^-3` |  | Linear within-category number-distribution coefficient f_5 (Eq. 13a) with the positivity constraint Eq. 15 applied; algebraic. |
| `psi1` | `kg^-1*m^-3` |  | Linear within-category number-distribution coefficient psi_1 (Eq. 13b) with the positivity constraint Eq. 15 applied; algebraic. |
| `psi2` | `kg^-1*m^-3` |  | Linear within-category number-distribution coefficient psi_2 (Eq. 13b) with the positivity constraint Eq. 15 applied; algebraic. |
| `psi3` | `kg^-1*m^-3` |  | Linear within-category number-distribution coefficient psi_3 (Eq. 13b) with the positivity constraint Eq. 15 applied; algebraic. |
| `psi4` | `kg^-1*m^-3` |  | Linear within-category number-distribution coefficient psi_4 (Eq. 13b) with the positivity constraint Eq. 15 applied; algebraic. |
| `psi5` | `kg^-1*m^-3` |  | Linear within-category number-distribution coefficient psi_5 (Eq. 13b) with the positivity constraint Eq. 15 applied; algebraic. |
| `alpha1` | `kg^-2*m^-3` |  | Within-category distribution slope (f_1 - psi_1)/(2 x_1) for category 1; algebraic. |
| `alpha2` | `kg^-2*m^-3` |  | Within-category distribution slope (f_2 - psi_2)/(2 x_2) for category 2; algebraic. |
| `alpha3` | `kg^-2*m^-3` |  | Within-category distribution slope (f_3 - psi_3)/(2 x_3) for category 3; algebraic. |
| `alpha4` | `kg^-2*m^-3` |  | Within-category distribution slope (f_4 - psi_4)/(2 x_4) for category 4; algebraic. |
| `alpha5` | `kg^-2*m^-3` |  | Within-category distribution slope (f_5 - psi_5)/(2 x_5) for category 5; algebraic. |

## Observed expressions

$$
xb1 = \frac{M1 \cdot N1}{N1^{2} + 1 \times 10^{-300}}
$$
_Mean droplet mass M_1/N_1 in category 1; algebraic. Denominator floored by 1e-300 so the closure stays finite for an empty category._

$$
xb2 = \frac{M2 \cdot N2}{N2^{2} + 1 \times 10^{-300}}
$$
_Mean droplet mass M_2/N_2 in category 2; algebraic. Denominator floored by 1e-300 so the closure stays finite for an empty category._

$$
xb3 = \frac{M3 \cdot N3}{N3^{2} + 1 \times 10^{-300}}
$$
_Mean droplet mass M_3/N_3 in category 3; algebraic. Denominator floored by 1e-300 so the closure stays finite for an empty category._

$$
xb4 = \frac{M4 \cdot N4}{N4^{2} + 1 \times 10^{-300}}
$$
_Mean droplet mass M_4/N_4 in category 4; algebraic. Denominator floored by 1e-300 so the closure stays finite for an empty category._

$$
xb5 = \frac{M5 \cdot N5}{N5^{2} + 1 \times 10^{-300}}
$$
_Mean droplet mass M_5/N_5 in category 5; algebraic. Denominator floored by 1e-300 so the closure stays finite for an empty category._

$$
Z1 = \frac{XI_{P} \cdot M1^{2} \cdot N1}{N1^{2} + 1 \times 10^{-300}}
$$
_Second-moment closure quantity xi_p*M_1^2/N_1 for category 1; algebraic._

$$
Z2 = \frac{XI_{P} \cdot M2^{2} \cdot N2}{N2^{2} + 1 \times 10^{-300}}
$$
_Second-moment closure quantity xi_p*M_2^2/N_2 for category 2; algebraic._

$$
Z3 = \frac{XI_{P} \cdot M3^{2} \cdot N3}{N3^{2} + 1 \times 10^{-300}}
$$
_Second-moment closure quantity xi_p*M_3^2/N_3 for category 3; algebraic._

$$
Z4 = \frac{XI_{P} \cdot M4^{2} \cdot N4}{N4^{2} + 1 \times 10^{-300}}
$$
_Second-moment closure quantity xi_p*M_4^2/N_4 for category 4; algebraic._

$$
Z5 = \frac{XI_{P} \cdot M5^{2} \cdot N5}{N5^{2} + 1 \times 10^{-300}}
$$
_Second-moment closure quantity xi_p*M_5^2/N_5 for category 5; algebraic._

$$
Q1 = \frac{XI_{P}^{2} \cdot M1^{3} \cdot N1^{2}}{N1^{4} + 1 \times 10^{-300}}
$$
_Third-moment closure quantity xi_p^2*M_1^3/N_1^2 for category 1; algebraic._

$$
Q2 = \frac{XI_{P}^{2} \cdot M2^{3} \cdot N2^{2}}{N2^{4} + 1 \times 10^{-300}}
$$
_Third-moment closure quantity xi_p^2*M_2^3/N_2^2 for category 2; algebraic._

$$
Q3 = \frac{XI_{P}^{2} \cdot M3^{3} \cdot N3^{2}}{N3^{4} + 1 \times 10^{-300}}
$$
_Third-moment closure quantity xi_p^2*M_3^3/N_3^2 for category 3; algebraic._

$$
Q4 = \frac{XI_{P}^{2} \cdot M4^{3} \cdot N4^{2}}{N4^{4} + 1 \times 10^{-300}}
$$
_Third-moment closure quantity xi_p^2*M_4^3/N_4^2 for category 4; algebraic._

$$
Q5 = \frac{XI_{P}^{2} \cdot M5^{3} \cdot N5^{2}}{N5^{4} + 1 \times 10^{-300}}
$$
_Third-moment closure quantity xi_p^2*M_5^3/N_5^2 for category 5; algebraic._

$$
f1 = \mathrm{ifelse}\left(\mathrm{<}\left(xb1, 1.6 \times 10^{-14}\right), 0.0, \mathrm{ifelse}\left(\mathrm{>}\left(xb1, 3.2 \times 10^{-14}\right), \frac{2.0 \cdot N1}{1.6 \times 10^{-14}}, \frac{4.0 \cdot N1}{1.6 \times 10^{-14}} - \frac{2.0 \cdot M1}{2.56 \times 10^{-28}}\right)\right)
$$
_Linear within-category number-distribution coefficient f_1 (Eq. 13a) with the positivity constraint Eq. 15 applied; algebraic._

$$
f2 = \mathrm{ifelse}\left(\mathrm{<}\left(xb2, 3.2 \times 10^{-14}\right), 0.0, \mathrm{ifelse}\left(\mathrm{>}\left(xb2, 6.4 \times 10^{-14}\right), \frac{2.0 \cdot N2}{3.2 \times 10^{-14}}, \frac{4.0 \cdot N2}{3.2 \times 10^{-14}} - \frac{2.0 \cdot M2}{1.024 \times 10^{-27}}\right)\right)
$$
_Linear within-category number-distribution coefficient f_2 (Eq. 13a) with the positivity constraint Eq. 15 applied; algebraic._

$$
f3 = \mathrm{ifelse}\left(\mathrm{<}\left(xb3, 6.4 \times 10^{-14}\right), 0.0, \mathrm{ifelse}\left(\mathrm{>}\left(xb3, 1.28 \times 10^{-13}\right), \frac{2.0 \cdot N3}{6.4 \times 10^{-14}}, \frac{4.0 \cdot N3}{6.4 \times 10^{-14}} - \frac{2.0 \cdot M3}{4.096 \times 10^{-27}}\right)\right)
$$
_Linear within-category number-distribution coefficient f_3 (Eq. 13a) with the positivity constraint Eq. 15 applied; algebraic._

$$
f4 = \mathrm{ifelse}\left(\mathrm{<}\left(xb4, 1.28 \times 10^{-13}\right), 0.0, \mathrm{ifelse}\left(\mathrm{>}\left(xb4, 2.56 \times 10^{-13}\right), \frac{2.0 \cdot N4}{1.28 \times 10^{-13}}, \frac{4.0 \cdot N4}{1.28 \times 10^{-13}} - \frac{2.0 \cdot M4}{1.6384 \times 10^{-26}}\right)\right)
$$
_Linear within-category number-distribution coefficient f_4 (Eq. 13a) with the positivity constraint Eq. 15 applied; algebraic._

$$
f5 = \mathrm{ifelse}\left(\mathrm{<}\left(xb5, 2.56 \times 10^{-13}\right), 0.0, \mathrm{ifelse}\left(\mathrm{>}\left(xb5, 5.12 \times 10^{-13}\right), \frac{2.0 \cdot N5}{2.56 \times 10^{-13}}, \frac{4.0 \cdot N5}{2.56 \times 10^{-13}} - \frac{2.0 \cdot M5}{6.5536 \times 10^{-26}}\right)\right)
$$
_Linear within-category number-distribution coefficient f_5 (Eq. 13a) with the positivity constraint Eq. 15 applied; algebraic._

$$
psi1 = \mathrm{ifelse}\left(\mathrm{<}\left(xb1, 1.6 \times 10^{-14}\right), \frac{2.0 \cdot N1}{1.6 \times 10^{-14}}, \mathrm{ifelse}\left(\mathrm{>}\left(xb1, 3.2 \times 10^{-14}\right), 0.0, \frac{2.0 \cdot M1}{2.56 \times 10^{-28}} - \frac{2.0 \cdot N1}{1.6 \times 10^{-14}}\right)\right)
$$
_Linear within-category number-distribution coefficient psi_1 (Eq. 13b) with the positivity constraint Eq. 15 applied; algebraic._

$$
psi2 = \mathrm{ifelse}\left(\mathrm{<}\left(xb2, 3.2 \times 10^{-14}\right), \frac{2.0 \cdot N2}{3.2 \times 10^{-14}}, \mathrm{ifelse}\left(\mathrm{>}\left(xb2, 6.4 \times 10^{-14}\right), 0.0, \frac{2.0 \cdot M2}{1.024 \times 10^{-27}} - \frac{2.0 \cdot N2}{3.2 \times 10^{-14}}\right)\right)
$$
_Linear within-category number-distribution coefficient psi_2 (Eq. 13b) with the positivity constraint Eq. 15 applied; algebraic._

$$
psi3 = \mathrm{ifelse}\left(\mathrm{<}\left(xb3, 6.4 \times 10^{-14}\right), \frac{2.0 \cdot N3}{6.4 \times 10^{-14}}, \mathrm{ifelse}\left(\mathrm{>}\left(xb3, 1.28 \times 10^{-13}\right), 0.0, \frac{2.0 \cdot M3}{4.096 \times 10^{-27}} - \frac{2.0 \cdot N3}{6.4 \times 10^{-14}}\right)\right)
$$
_Linear within-category number-distribution coefficient psi_3 (Eq. 13b) with the positivity constraint Eq. 15 applied; algebraic._

$$
psi4 = \mathrm{ifelse}\left(\mathrm{<}\left(xb4, 1.28 \times 10^{-13}\right), \frac{2.0 \cdot N4}{1.28 \times 10^{-13}}, \mathrm{ifelse}\left(\mathrm{>}\left(xb4, 2.56 \times 10^{-13}\right), 0.0, \frac{2.0 \cdot M4}{1.6384 \times 10^{-26}} - \frac{2.0 \cdot N4}{1.28 \times 10^{-13}}\right)\right)
$$
_Linear within-category number-distribution coefficient psi_4 (Eq. 13b) with the positivity constraint Eq. 15 applied; algebraic._

$$
psi5 = \mathrm{ifelse}\left(\mathrm{<}\left(xb5, 2.56 \times 10^{-13}\right), \frac{2.0 \cdot N5}{2.56 \times 10^{-13}}, \mathrm{ifelse}\left(\mathrm{>}\left(xb5, 5.12 \times 10^{-13}\right), 0.0, \frac{2.0 \cdot M5}{6.5536 \times 10^{-26}} - \frac{2.0 \cdot N5}{2.56 \times 10^{-13}}\right)\right)
$$
_Linear within-category number-distribution coefficient psi_5 (Eq. 13b) with the positivity constraint Eq. 15 applied; algebraic._

$$
alpha1 = \frac{f1 - psi1}{3.2 \times 10^{-14}}
$$
_Within-category distribution slope (f_1 - psi_1)/(2 x_1) for category 1; algebraic._

$$
alpha2 = \frac{f2 - psi2}{6.4 \times 10^{-14}}
$$
_Within-category distribution slope (f_2 - psi_2)/(2 x_2) for category 2; algebraic._

$$
alpha3 = \frac{f3 - psi3}{1.28 \times 10^{-13}}
$$
_Within-category distribution slope (f_3 - psi_3)/(2 x_3) for category 3; algebraic._

$$
alpha4 = \frac{f4 - psi4}{2.56 \times 10^{-13}}
$$
_Within-category distribution slope (f_4 - psi_4)/(2 x_4) for category 4; algebraic._

$$
alpha5 = \frac{f5 - psi5}{5.12 \times 10^{-13}}
$$
_Within-category distribution slope (f_5 - psi_5)/(2 x_5) for category 5; algebraic._

## Equations

$$
\mathrm{D}\left(N1\right) = \left(-K0\right) \cdot N1^{2} + \left(-K0\right) \cdot N1 \cdot N2 + \left(-K0\right) \cdot N1 \cdot N3 + \left(-K0\right) \cdot N1 \cdot N4 + \left(-K0\right) \cdot N1 \cdot N5
$$

$$
\mathrm{D}\left(N2\right) = K0 \cdot 0.5 \cdot N1^{2} + \left(-K0\right) \cdot N2^{2} + \left(-K0\right) \cdot \left(psi2 \cdot M1 + alpha2 \cdot Z1\right) + \left(-K0\right) \cdot N2 \cdot N3 + \left(-K0\right) \cdot N2 \cdot N4 + \left(-K0\right) \cdot N2 \cdot N5
$$

$$
\mathrm{D}\left(N3\right) = K0 \cdot 0.5 \cdot N2^{2} + \left(-K0\right) \cdot N3^{2} + K0 \cdot \left(psi2 \cdot M1 + alpha2 \cdot Z1\right) + \left(-K0\right) \cdot \left(psi3 \cdot M1 + alpha3 \cdot Z1\right) + \left(-K0\right) \cdot \left(psi3 \cdot M2 + alpha3 \cdot Z2\right) + \left(-K0\right) \cdot N3 \cdot N4 + \left(-K0\right) \cdot N3 \cdot N5
$$

$$
\mathrm{D}\left(N4\right) = K0 \cdot 0.5 \cdot N3^{2} + \left(-K0\right) \cdot N4^{2} + K0 \cdot \left(psi3 \cdot M1 + alpha3 \cdot Z1\right) + K0 \cdot \left(psi3 \cdot M2 + alpha3 \cdot Z2\right) + \left(-K0\right) \cdot \left(psi4 \cdot M1 + alpha4 \cdot Z1\right) + \left(-K0\right) \cdot \left(psi4 \cdot M2 + alpha4 \cdot Z2\right) + \left(-K0\right) \cdot \left(psi4 \cdot M3 + alpha4 \cdot Z3\right) + \left(-K0\right) \cdot N4 \cdot N5
$$

$$
\mathrm{D}\left(N5\right) = K0 \cdot 0.5 \cdot N4^{2} + \left(-K0\right) \cdot N5^{2} + K0 \cdot \left(psi4 \cdot M1 + alpha4 \cdot Z1\right) + K0 \cdot \left(psi4 \cdot M2 + alpha4 \cdot Z2\right) + K0 \cdot \left(psi4 \cdot M3 + alpha4 \cdot Z3\right) + \left(-K0\right) \cdot \left(psi5 \cdot M1 + alpha5 \cdot Z1\right) + \left(-K0\right) \cdot \left(psi5 \cdot M2 + alpha5 \cdot Z2\right) + \left(-K0\right) \cdot \left(psi5 \cdot M3 + alpha5 \cdot Z3\right) + \left(-K0\right) \cdot \left(psi5 \cdot M4 + alpha5 \cdot Z4\right)
$$

$$
\mathrm{D}\left(M1\right) = \left(-K0\right) \cdot N1 \cdot M1 + \left(-K0\right) \cdot M1 \cdot N2 + \left(-K0\right) \cdot M1 \cdot N3 + \left(-K0\right) \cdot M1 \cdot N4 + \left(-K0\right) \cdot M1 \cdot N5
$$

$$
\mathrm{D}\left(M2\right) = K0 \cdot N1 \cdot M1 + \left(-K0\right) \cdot N2 \cdot M2 + \left(-K0\right) \cdot \left(6.4 \times 10^{-14} \cdot psi2 \cdot M1 + 0.5 \cdot f2 \cdot Z1 + alpha2 \cdot Q1\right) + K0 \cdot N2 \cdot M1 + \left(-K0\right) \cdot M2 \cdot N3 + \left(-K0\right) \cdot M2 \cdot N4 + \left(-K0\right) \cdot M2 \cdot N5
$$

$$
\mathrm{D}\left(M3\right) = K0 \cdot N2 \cdot M2 + \left(-K0\right) \cdot N3 \cdot M3 + K0 \cdot \left(6.4 \times 10^{-14} \cdot psi2 \cdot M1 + 0.5 \cdot f2 \cdot Z1 + alpha2 \cdot Q1\right) + \left(-K0\right) \cdot \left(1.28 \times 10^{-13} \cdot psi3 \cdot M1 + 0.5 \cdot f3 \cdot Z1 + alpha3 \cdot Q1\right) + K0 \cdot N3 \cdot M1 + \left(-K0\right) \cdot \left(1.28 \times 10^{-13} \cdot psi3 \cdot M2 + 0.5 \cdot f3 \cdot Z2 + alpha3 \cdot Q2\right) + K0 \cdot N3 \cdot M2 + \left(-K0\right) \cdot M3 \cdot N4 + \left(-K0\right) \cdot M3 \cdot N5
$$

$$
\mathrm{D}\left(M4\right) = K0 \cdot N3 \cdot M3 + \left(-K0\right) \cdot N4 \cdot M4 + K0 \cdot \left(1.28 \times 10^{-13} \cdot psi3 \cdot M1 + 0.5 \cdot f3 \cdot Z1 + alpha3 \cdot Q1\right) + K0 \cdot \left(1.28 \times 10^{-13} \cdot psi3 \cdot M2 + 0.5 \cdot f3 \cdot Z2 + alpha3 \cdot Q2\right) + \left(-K0\right) \cdot \left(2.56 \times 10^{-13} \cdot psi4 \cdot M1 + 0.5 \cdot f4 \cdot Z1 + alpha4 \cdot Q1\right) + K0 \cdot N4 \cdot M1 + \left(-K0\right) \cdot \left(2.56 \times 10^{-13} \cdot psi4 \cdot M2 + 0.5 \cdot f4 \cdot Z2 + alpha4 \cdot Q2\right) + K0 \cdot N4 \cdot M2 + \left(-K0\right) \cdot \left(2.56 \times 10^{-13} \cdot psi4 \cdot M3 + 0.5 \cdot f4 \cdot Z3 + alpha4 \cdot Q3\right) + K0 \cdot N4 \cdot M3 + \left(-K0\right) \cdot M4 \cdot N5
$$

$$
\mathrm{D}\left(M5\right) = K0 \cdot N4 \cdot M4 + \left(-K0\right) \cdot N5 \cdot M5 + K0 \cdot \left(2.56 \times 10^{-13} \cdot psi4 \cdot M1 + 0.5 \cdot f4 \cdot Z1 + alpha4 \cdot Q1\right) + K0 \cdot \left(2.56 \times 10^{-13} \cdot psi4 \cdot M2 + 0.5 \cdot f4 \cdot Z2 + alpha4 \cdot Q2\right) + K0 \cdot \left(2.56 \times 10^{-13} \cdot psi4 \cdot M3 + 0.5 \cdot f4 \cdot Z3 + alpha4 \cdot Q3\right) + \left(-K0\right) \cdot \left(5.12 \times 10^{-13} \cdot psi5 \cdot M1 + 0.5 \cdot f5 \cdot Z1 + alpha5 \cdot Q1\right) + K0 \cdot N5 \cdot M1 + \left(-K0\right) \cdot \left(5.12 \times 10^{-13} \cdot psi5 \cdot M2 + 0.5 \cdot f5 \cdot Z2 + alpha5 \cdot Q2\right) + K0 \cdot N5 \cdot M2 + \left(-K0\right) \cdot \left(5.12 \times 10^{-13} \cdot psi5 \cdot M3 + 0.5 \cdot f5 \cdot Z3 + alpha5 \cdot Q3\right) + K0 \cdot N5 \cdot M3 + \left(-K0\right) \cdot \left(5.12 \times 10^{-13} \cdot psi5 \cdot M4 + 0.5 \cdot f5 \cdot Z4 + alpha5 \cdot Q4\right) + K0 \cdot N5 \cdot M4
$$

## Analyses

### exponential_ic_evolution_constant

Evolution of the droplet number and mass spectra under the constant collection kernel, started from an exponential initial distribution. Number concentration decreases as droplets coalesce; mass shifts toward larger categories.

**Time span:** 0.0 → 1000.0

![Number concentration N_k(t) for each of the 5 mass categories.](/plots/aerosol/stochasticcollectionconstant/exponential_ic_evolution_constant-number_concentration.png)

![Mass concentration M_k(t) for each of the 5 mass categories.](/plots/aerosol/stochasticcollectionconstant/exponential_ic_evolution_constant-mass_concentration.png)

## Raw .esm

<details><summary>Raw .esm JSON (this component)</summary>

```json
{
  "reference": {
    "doi": "10.1175/1520-0469(1989)046<3312:TEORSP>2.0.CO;2",
    "citation": "Tzivion, S., Feingold, G., and Levin, Z.: The Evolution of Raindrop Spectra. Part II: Collisional Collection/Breakup and Evaporation in a Rainshaft, J. Atmos. Sci., 46(21), 3312-3327, 1989.",
    "url": "https://doi.org/10.1175/1520-0469(1989)046%3C3312:TEORSP%3E2.0.CO;2",
    "notes": "Source: Aerosol.jl src/stochastic_collection.jl @ c8c640bb636b22f2425460e9ed5cba50793bfee1 (migration bead esm-ar1e); the upstream @component StochasticCollectionCoalescence with kernel_type=constant. The upstream model solves the two-moment stochastic collection equation (SCE) for cloud-droplet coalescence (Tzivion et al. 1989) over I mass-doubling categories, tracking number N_k and mass M_k per category. It is built with symbolic array operations (SymbolicUtils @arrayop/@makearray over array variables Nk(t)[1:I], Mk(t)[1:I]); the array ops are not in the .esm closed AST and the ESS Python runner does not evaluate them, so the model is scalarized to I=5 categories and 10 scalar differential states N1..N5, M1..M5. The scalarization evaluates the upstream @arrayop ifelse masks (i==1, i<=k-2, i<=k-1, i>=k+1) at concrete (k,i), so the flat equations are the source semantics, not a hand-derived rewrite. The five (six for Golovin) closure families are carried as algebraic states with explicit equations (rig convention; cf. components/aerosol/tomas.esm): xb_k (mean mass M_k/N_k), Z_k/Q_k/R_k (higher moments xi_p*M^2/N, xi_p^2*M^3/N^2, xi_p^3*M^4/N^3), and f_k/psi_k/alpha_k (linear within-category reconstruction coefficients, Eq. 13+15). The upstream closures guard m/n divisions with ifelse(n>0,...); the .esm replaces each by the algebraically equivalent floored form m*n/(n^2+1e-300) etc. — bit-identical to m/n for every n>0 that occurs (n>=1e-20 makes the 1e-300 floor ~260 orders below rounding), finite at n=0, and free of the ifelse-guarded divide-by-zero that the runner's eager Piecewise lowering would otherwise hit. Kernel: constant kernel K(x,y)=K0. Verification: the scalarized RHS was checked (1) by a line-by-line transcription audit against the upstream @arrayop bodies; (2) against an independent literal double-sum implementation of the same @arrayop semantics (agreement < 1e-9 relative over random states); and (3) against first-principles no-overflow analytic identities — with the top category empty, no collision product exceeds the grid, so collection conserves number per collision and conserves mass exactly: dN_tot/dt = -(K0/2)*N_tot^2 (constant kernel) and dN_tot/dt = -C*M_tot*N_tot (Golovin kernel), with dM_tot/dt = 0. The scalarized RHS reproduces all three identities to machine precision (relative error 0). Inline-test expected values are a SciPy LSODA reference integration (rtol=1e-10, abstol=1e-14) of this verified RHS; the gate re-integrates the .esm with SciPy LSODA, and the model-level rel=2e-3 tolerance (as for tomas.esm) covers integrator-detail differences. This migration covers only collisional collection; the breakup, evaporation and sedimentation processes of the full 1989 paper are not implemented upstream either."
  },
  "tolerance": {
    "rel": 0.002
  },
  "variables": {
    "N1": {
      "type": "unknown",
      "units": "m^-3",
      "default": 1429670.6078643417,
      "description": "Number concentration of cloud droplets in mass category 1 (of 5); lower mass boundary x_1 = 1.600000e-14 kg."
    },
    "N2": {
      "type": "unknown",
      "units": "m^-3",
      "default": 2838836.0713738734,
      "description": "Number concentration of cloud droplets in mass category 2 (of 5); lower mass boundary x_2 = 3.200000e-14 kg."
    },
    "N3": {
      "type": "unknown",
      "units": "m^-3",
      "default": 5596563.981307812,
      "description": "Number concentration of cloud droplets in mass category 3 (of 5); lower mass boundary x_3 = 6.400000e-14 kg."
    },
    "N4": {
      "type": "unknown",
      "units": "m^-3",
      "default": 10875864.787608625,
      "description": "Number concentration of cloud droplets in mass category 4 (of 5); lower mass boundary x_4 = 1.280000e-13 kg."
    },
    "N5": {
      "type": "unknown",
      "units": "m^-3",
      "default": 20538015.50564386,
      "description": "Number concentration of cloud droplets in mass category 5 (of 5); lower mass boundary x_5 = 2.560000e-13 kg."
    },
    "M1": {
      "type": "unknown",
      "units": "kg*m^-3",
      "default": 3.430294470019302e-08,
      "description": "Mass concentration of cloud droplets in mass category 1 (of 5)."
    },
    "M2": {
      "type": "unknown",
      "units": "kg*m^-3",
      "default": 1.3619145733423377e-07,
      "description": "Mass concentration of cloud droplets in mass category 2 (of 5)."
    },
    "M3": {
      "type": "unknown",
      "units": "kg*m^-3",
      "default": 5.366970575748642e-07,
      "description": "Mass concentration of cloud droplets in mass category 3 (of 5)."
    },
    "M4": {
      "type": "unknown",
      "units": "kg*m^-3",
      "default": 2.083711394480048e-06,
      "description": "Mass concentration of cloud droplets in mass category 4 (of 5)."
    },
    "M5": {
      "type": "unknown",
      "units": "kg*m^-3",
      "default": 7.852951776977424e-06,
      "description": "Mass concentration of cloud droplets in mass category 5 (of 5)."
    },
    "XI_P": {
      "type": "parameter",
      "units": "1",
      "default": 1.0625,
      "description": "Closure parameter xi_p (= 17/16) relating the higher-order moments Z_k, Q_k, R_k to N_k and M_k (Tzivion et al. 1989, Eq. 8a,b)."
    },
    "K0": {
      "type": "parameter",
      "units": "m^3/s",
      "default": 1e-10,
      "description": "Constant collection-kernel coefficient: K(x,y) = K0."
    },
    "xb1": {
      "type": "unknown",
      "units": "kg",
      "description": "Mean droplet mass M_1/N_1 in category 1; algebraic. Denominator floored by 1e-300 so the closure stays finite for an empty category."
    },
    "xb2": {
      "type": "unknown",
      "units": "kg",
      "description": "Mean droplet mass M_2/N_2 in category 2; algebraic. Denominator floored by 1e-300 so the closure stays finite for an empty category."
    },
    "xb3": {
      "type": "unknown",
      "units": "kg",
      "description": "Mean droplet mass M_3/N_3 in category 3; algebraic. Denominator floored by 1e-300 so the closure stays finite for an empty category."
    },
    "xb4": {
      "type": "unknown",
      "units": "kg",
      "description": "Mean droplet mass M_4/N_4 in category 4; algebraic. Denominator floored by 1e-300 so the closure stays finite for an empty category."
    },
    "xb5": {
      "type": "unknown",
      "units": "kg",
      "description": "Mean droplet mass M_5/N_5 in category 5; algebraic. Denominator floored by 1e-300 so the closure stays finite for an empty category."
    },
    "Z1": {
      "type": "unknown",
      "units": "kg^2*m^-3",
      "description": "Second-moment closure quantity xi_p*M_1^2/N_1 for category 1; algebraic."
    },
    "Z2": {
      "type": "unknown",
      "units": "kg^2*m^-3",
      "description": "Second-moment closure quantity xi_p*M_2^2/N_2 for category 2; algebraic."
    },
    "Z3": {
      "type": "unknown",
      "units": "kg^2*m^-3",
      "description": "Second-moment closure quantity xi_p*M_3^2/N_3 for category 3; algebraic."
    },
    "Z4": {
      "type": "unknown",
      "units": "kg^2*m^-3",
      "description": "Second-moment closure quantity xi_p*M_4^2/N_4 for category 4; algebraic."
    },
    "Z5": {
      "type": "unknown",
      "units": "kg^2*m^-3",
      "description": "Second-moment closure quantity xi_p*M_5^2/N_5 for category 5; algebraic."
    },
    "Q1": {
      "type": "unknown",
      "units": "kg^3*m^-3",
      "description": "Third-moment closure quantity xi_p^2*M_1^3/N_1^2 for category 1; algebraic."
    },
    "Q2": {
      "type": "unknown",
      "units": "kg^3*m^-3",
      "description": "Third-moment closure quantity xi_p^2*M_2^3/N_2^2 for category 2; algebraic."
    },
    "Q3": {
      "type": "unknown",
      "units": "kg^3*m^-3",
      "description": "Third-moment closure quantity xi_p^2*M_3^3/N_3^2 for category 3; algebraic."
    },
    "Q4": {
      "type": "unknown",
      "units": "kg^3*m^-3",
      "description": "Third-moment closure quantity xi_p^2*M_4^3/N_4^2 for category 4; algebraic."
    },
    "Q5": {
      "type": "unknown",
      "units": "kg^3*m^-3",
      "description": "Third-moment closure quantity xi_p^2*M_5^3/N_5^2 for category 5; algebraic."
    },
    "f1": {
      "type": "unknown",
      "units": "kg^-1*m^-3",
      "description": "Linear within-category number-distribution coefficient f_1 (Eq. 13a) with the positivity constraint Eq. 15 applied; algebraic."
    },
    "f2": {
      "type": "unknown",
      "units": "kg^-1*m^-3",
      "description": "Linear within-category number-distribution coefficient f_2 (Eq. 13a) with the positivity constraint Eq. 15 applied; algebraic."
    },
    "f3": {
      "type": "unknown",
      "units": "kg^-1*m^-3",
      "description": "Linear within-category number-distribution coefficient f_3 (Eq. 13a) with the positivity constraint Eq. 15 applied; algebraic."
    },
    "f4": {
      "type": "unknown",
      "units": "kg^-1*m^-3",
      "description": "Linear within-category number-distribution coefficient f_4 (Eq. 13a) with the positivity constraint Eq. 15 applied; algebraic."
    },
    "f5": {
      "type": "unknown",
      "units": "kg^-1*m^-3",
      "description": "Linear within-category number-distribution coefficient f_5 (Eq. 13a) with the positivity constraint Eq. 15 applied; algebraic."
    },
    "psi1": {
      "type": "unknown",
      "units": "kg^-1*m^-3",
      "description": "Linear within-category number-distribution coefficient psi_1 (Eq. 13b) with the positivity constraint Eq. 15 applied; algebraic."
    },
    "psi2": {
      "type": "unknown",
      "units": "kg^-1*m^-3",
      "description": "Linear within-category number-distribution coefficient psi_2 (Eq. 13b) with the positivity constraint Eq. 15 applied; algebraic."
    },
    "psi3": {
      "type": "unknown",
      "units": "kg^-1*m^-3",
      "description": "Linear within-category number-distribution coefficient psi_3 (Eq. 13b) with the positivity constraint Eq. 15 applied; algebraic."
    },
    "psi4": {
      "type": "unknown",
      "units": "kg^-1*m^-3",
      "description": "Linear within-category number-distribution coefficient psi_4 (Eq. 13b) with the positivity constraint Eq. 15 applied; algebraic."
    },
    "psi5": {
      "type": "unknown",
      "units": "kg^-1*m^-3",
      "description": "Linear within-category number-distribution coefficient psi_5 (Eq. 13b) with the positivity constraint Eq. 15 applied; algebraic."
    },
    "alpha1": {
      "type": "unknown",
      "units": "kg^-2*m^-3",
      "description": "Within-category distribution slope (f_1 - psi_1)/(2 x_1) for category 1; algebraic."
    },
    "alpha2": {
      "type": "unknown",
      "units": "kg^-2*m^-3",
      "description": "Within-category distribution slope (f_2 - psi_2)/(2 x_2) for category 2; algebraic."
    },
    "alpha3": {
      "type": "unknown",
      "units": "kg^-2*m^-3",
      "description": "Within-category distribution slope (f_3 - psi_3)/(2 x_3) for category 3; algebraic."
    },
    "alpha4": {
      "type": "unknown",
      "units": "kg^-2*m^-3",
      "description": "Within-category distribution slope (f_4 - psi_4)/(2 x_4) for category 4; algebraic."
    },
    "alpha5": {
      "type": "unknown",
      "units": "kg^-2*m^-3",
      "description": "Within-category distribution slope (f_5 - psi_5)/(2 x_5) for category 5; algebraic."
    }
  },
  "equations": [
    {
      "lhs": {
        "op": "D",
        "args": [
          "N1"
        ],
        "wrt": "t"
      },
      "rhs": {
        "op": "+",
        "args": [
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              {
                "op": "^",
                "args": [
                  "N1",
                  2
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              "N1",
              "N2"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              "N1",
              "N3"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              "N1",
              "N4"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              "N1",
              "N5"
            ]
          }
        ]
      }
    },
    {
      "lhs": {
        "op": "D",
        "args": [
          "N2"
        ],
        "wrt": "t"
      },
      "rhs": {
        "op": "+",
        "args": [
          {
            "op": "*",
            "args": [
              "K0",
              0.5,
              {
                "op": "^",
                "args": [
                  "N1",
                  2
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              {
                "op": "^",
                "args": [
                  "N2",
                  2
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              {
                "op": "+",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      "psi2",
                      "M1"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "alpha2",
                      "Z1"
                    ]
                  }
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              "N2",
              "N3"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              "N2",
              "N4"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              "N2",
              "N5"
            ]
          }
        ]
      }
    },
    {
      "lhs": {
        "op": "D",
        "args": [
          "N3"
        ],
        "wrt": "t"
      },
      "rhs": {
        "op": "+",
        "args": [
          {
            "op": "*",
            "args": [
              "K0",
              0.5,
              {
                "op": "^",
                "args": [
                  "N2",
                  2
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              {
                "op": "^",
                "args": [
                  "N3",
                  2
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              "K0",
              {
                "op": "+",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      "psi2",
                      "M1"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "alpha2",
                      "Z1"
                    ]
                  }
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              {
                "op": "+",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      "psi3",
                      "M1"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "alpha3",
                      "Z1"
                    ]
                  }
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              {
                "op": "+",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      "psi3",
                      "M2"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "alpha3",
                      "Z2"
                    ]
                  }
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              "N3",
              "N4"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              "N3",
              "N5"
            ]
          }
        ]
      }
    },
    {
      "lhs": {
        "op": "D",
        "args": [
          "N4"
        ],
        "wrt": "t"
      },
      "rhs": {
        "op": "+",
        "args": [
          {
            "op": "*",
            "args": [
              "K0",
              0.5,
              {
                "op": "^",
                "args": [
                  "N3",
                  2
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              {
                "op": "^",
                "args": [
                  "N4",
                  2
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              "K0",
              {
                "op": "+",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      "psi3",
                      "M1"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "alpha3",
                      "Z1"
                    ]
                  }
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              "K0",
              {
                "op": "+",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      "psi3",
                      "M2"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "alpha3",
                      "Z2"
                    ]
                  }
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              {
                "op": "+",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      "psi4",
                      "M1"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "alpha4",
                      "Z1"
                    ]
                  }
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              {
                "op": "+",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      "psi4",
                      "M2"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "alpha4",
                      "Z2"
                    ]
                  }
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              {
                "op": "+",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      "psi4",
                      "M3"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "alpha4",
                      "Z3"
                    ]
                  }
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              "N4",
              "N5"
            ]
          }
        ]
      }
    },
    {
      "lhs": {
        "op": "D",
        "args": [
          "N5"
        ],
        "wrt": "t"
      },
      "rhs": {
        "op": "+",
        "args": [
          {
            "op": "*",
            "args": [
              "K0",
              0.5,
              {
                "op": "^",
                "args": [
                  "N4",
                  2
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              {
                "op": "^",
                "args": [
                  "N5",
                  2
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              "K0",
              {
                "op": "+",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      "psi4",
                      "M1"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "alpha4",
                      "Z1"
                    ]
                  }
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              "K0",
              {
                "op": "+",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      "psi4",
                      "M2"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "alpha4",
                      "Z2"
                    ]
                  }
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              "K0",
              {
                "op": "+",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      "psi4",
                      "M3"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "alpha4",
                      "Z3"
                    ]
                  }
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              {
                "op": "+",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      "psi5",
                      "M1"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "alpha5",
                      "Z1"
                    ]
                  }
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              {
                "op": "+",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      "psi5",
                      "M2"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "alpha5",
                      "Z2"
                    ]
                  }
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              {
                "op": "+",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      "psi5",
                      "M3"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "alpha5",
                      "Z3"
                    ]
                  }
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              {
                "op": "+",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      "psi5",
                      "M4"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "alpha5",
                      "Z4"
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": {
        "op": "D",
        "args": [
          "M1"
        ],
        "wrt": "t"
      },
      "rhs": {
        "op": "+",
        "args": [
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              "N1",
              "M1"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              "M1",
              "N2"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              "M1",
              "N3"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              "M1",
              "N4"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              "M1",
              "N5"
            ]
          }
        ]
      }
    },
    {
      "lhs": {
        "op": "D",
        "args": [
          "M2"
        ],
        "wrt": "t"
      },
      "rhs": {
        "op": "+",
        "args": [
          {
            "op": "*",
            "args": [
              "K0",
              "N1",
              "M1"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              "N2",
              "M2"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              {
                "op": "+",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      6.4e-14,
                      "psi2",
                      "M1"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      0.5,
                      "f2",
                      "Z1"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "alpha2",
                      "Q1"
                    ]
                  }
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              "K0",
              "N2",
              "M1"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              "M2",
              "N3"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              "M2",
              "N4"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              "M2",
              "N5"
            ]
          }
        ]
      }
    },
    {
      "lhs": {
        "op": "D",
        "args": [
          "M3"
        ],
        "wrt": "t"
      },
      "rhs": {
        "op": "+",
        "args": [
          {
            "op": "*",
            "args": [
              "K0",
              "N2",
              "M2"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              "N3",
              "M3"
            ]
          },
          {
            "op": "*",
            "args": [
              "K0",
              {
                "op": "+",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      6.4e-14,
                      "psi2",
                      "M1"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      0.5,
                      "f2",
                      "Z1"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "alpha2",
                      "Q1"
                    ]
                  }
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              {
                "op": "+",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      1.28e-13,
                      "psi3",
                      "M1"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      0.5,
                      "f3",
                      "Z1"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "alpha3",
                      "Q1"
                    ]
                  }
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              "K0",
              "N3",
              "M1"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              {
                "op": "+",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      1.28e-13,
                      "psi3",
                      "M2"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      0.5,
                      "f3",
                      "Z2"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "alpha3",
                      "Q2"
                    ]
                  }
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              "K0",
              "N3",
              "M2"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              "M3",
              "N4"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              "M3",
              "N5"
            ]
          }
        ]
      }
    },
    {
      "lhs": {
        "op": "D",
        "args": [
          "M4"
        ],
        "wrt": "t"
      },
      "rhs": {
        "op": "+",
        "args": [
          {
            "op": "*",
            "args": [
              "K0",
              "N3",
              "M3"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              "N4",
              "M4"
            ]
          },
          {
            "op": "*",
            "args": [
              "K0",
              {
                "op": "+",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      1.28e-13,
                      "psi3",
                      "M1"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      0.5,
                      "f3",
                      "Z1"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "alpha3",
                      "Q1"
                    ]
                  }
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              "K0",
              {
                "op": "+",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      1.28e-13,
                      "psi3",
                      "M2"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      0.5,
                      "f3",
                      "Z2"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "alpha3",
                      "Q2"
                    ]
                  }
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              {
                "op": "+",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      2.56e-13,
                      "psi4",
                      "M1"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      0.5,
                      "f4",
                      "Z1"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "alpha4",
                      "Q1"
                    ]
                  }
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              "K0",
              "N4",
              "M1"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              {
                "op": "+",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      2.56e-13,
                      "psi4",
                      "M2"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      0.5,
                      "f4",
                      "Z2"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "alpha4",
                      "Q2"
                    ]
                  }
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              "K0",
              "N4",
              "M2"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              {
                "op": "+",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      2.56e-13,
                      "psi4",
                      "M3"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      0.5,
                      "f4",
                      "Z3"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "alpha4",
                      "Q3"
                    ]
                  }
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              "K0",
              "N4",
              "M3"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              "M4",
              "N5"
            ]
          }
        ]
      }
    },
    {
      "lhs": {
        "op": "D",
        "args": [
          "M5"
        ],
        "wrt": "t"
      },
      "rhs": {
        "op": "+",
        "args": [
          {
            "op": "*",
            "args": [
              "K0",
              "N4",
              "M4"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              "N5",
              "M5"
            ]
          },
          {
            "op": "*",
            "args": [
              "K0",
              {
                "op": "+",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      2.56e-13,
                      "psi4",
                      "M1"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      0.5,
                      "f4",
                      "Z1"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "alpha4",
                      "Q1"
                    ]
                  }
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              "K0",
              {
                "op": "+",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      2.56e-13,
                      "psi4",
                      "M2"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      0.5,
                      "f4",
                      "Z2"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "alpha4",
                      "Q2"
                    ]
                  }
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              "K0",
              {
                "op": "+",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      2.56e-13,
                      "psi4",
                      "M3"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      0.5,
                      "f4",
                      "Z3"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "alpha4",
                      "Q3"
                    ]
                  }
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              {
                "op": "+",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      5.12e-13,
                      "psi5",
                      "M1"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      0.5,
                      "f5",
                      "Z1"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "alpha5",
                      "Q1"
                    ]
                  }
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              "K0",
              "N5",
              "M1"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              {
                "op": "+",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      5.12e-13,
                      "psi5",
                      "M2"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      0.5,
                      "f5",
                      "Z2"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "alpha5",
                      "Q2"
                    ]
                  }
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              "K0",
              "N5",
              "M2"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              {
                "op": "+",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      5.12e-13,
                      "psi5",
                      "M3"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      0.5,
                      "f5",
                      "Z3"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "alpha5",
                      "Q3"
                    ]
                  }
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              "K0",
              "N5",
              "M3"
            ]
          },
          {
            "op": "*",
            "args": [
              {
                "op": "-",
                "args": [
                  "K0"
                ]
              },
              {
                "op": "+",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      5.12e-13,
                      "psi5",
                      "M4"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      0.5,
                      "f5",
                      "Z4"
                    ]
                  },
                  {
                    "op": "*",
                    "args": [
                      "alpha5",
                      "Q4"
                    ]
                  }
                ]
              }
            ]
          },
          {
            "op": "*",
            "args": [
              "K0",
              "N5",
              "M4"
            ]
          }
        ]
      }
    },
    {
      "lhs": "xb1",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "*",
            "args": [
              "M1",
              "N1"
            ]
          },
          {
            "op": "+",
            "args": [
              {
                "op": "^",
                "args": [
                  "N1",
                  2
                ]
              },
              1e-300
            ]
          }
        ]
      }
    },
    {
      "lhs": "xb2",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "*",
            "args": [
              "M2",
              "N2"
            ]
          },
          {
            "op": "+",
            "args": [
              {
                "op": "^",
                "args": [
                  "N2",
                  2
                ]
              },
              1e-300
            ]
          }
        ]
      }
    },
    {
      "lhs": "xb3",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "*",
            "args": [
              "M3",
              "N3"
            ]
          },
          {
            "op": "+",
            "args": [
              {
                "op": "^",
                "args": [
                  "N3",
                  2
                ]
              },
              1e-300
            ]
          }
        ]
      }
    },
    {
      "lhs": "xb4",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "*",
            "args": [
              "M4",
              "N4"
            ]
          },
          {
            "op": "+",
            "args": [
              {
                "op": "^",
                "args": [
                  "N4",
                  2
                ]
              },
              1e-300
            ]
          }
        ]
      }
    },
    {
      "lhs": "xb5",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "*",
            "args": [
              "M5",
              "N5"
            ]
          },
          {
            "op": "+",
            "args": [
              {
                "op": "^",
                "args": [
                  "N5",
                  2
                ]
              },
              1e-300
            ]
          }
        ]
      }
    },
    {
      "lhs": "Z1",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "*",
            "args": [
              "XI_P",
              {
                "op": "^",
                "args": [
                  "M1",
                  2
                ]
              },
              "N1"
            ]
          },
          {
            "op": "+",
            "args": [
              {
                "op": "^",
                "args": [
                  "N1",
                  2
                ]
              },
              1e-300
            ]
          }
        ]
      }
    },
    {
      "lhs": "Z2",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "*",
            "args": [
              "XI_P",
              {
                "op": "^",
                "args": [
                  "M2",
                  2
                ]
              },
              "N2"
            ]
          },
          {
            "op": "+",
            "args": [
              {
                "op": "^",
                "args": [
                  "N2",
                  2
                ]
              },
              1e-300
            ]
          }
        ]
      }
    },
    {
      "lhs": "Z3",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "*",
            "args": [
              "XI_P",
              {
                "op": "^",
                "args": [
                  "M3",
                  2
                ]
              },
              "N3"
            ]
          },
          {
            "op": "+",
            "args": [
              {
                "op": "^",
                "args": [
                  "N3",
                  2
                ]
              },
              1e-300
            ]
          }
        ]
      }
    },
    {
      "lhs": "Z4",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "*",
            "args": [
              "XI_P",
              {
                "op": "^",
                "args": [
                  "M4",
                  2
                ]
              },
              "N4"
            ]
          },
          {
            "op": "+",
            "args": [
              {
                "op": "^",
                "args": [
                  "N4",
                  2
                ]
              },
              1e-300
            ]
          }
        ]
      }
    },
    {
      "lhs": "Z5",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "*",
            "args": [
              "XI_P",
              {
                "op": "^",
                "args": [
                  "M5",
                  2
                ]
              },
              "N5"
            ]
          },
          {
            "op": "+",
            "args": [
              {
                "op": "^",
                "args": [
                  "N5",
                  2
                ]
              },
              1e-300
            ]
          }
        ]
      }
    },
    {
      "lhs": "Q1",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "*",
            "args": [
              {
                "op": "^",
                "args": [
                  "XI_P",
                  2
                ]
              },
              {
                "op": "^",
                "args": [
                  "M1",
                  3
                ]
              },
              {
                "op": "^",
                "args": [
                  "N1",
                  2
                ]
              }
            ]
          },
          {
            "op": "+",
            "args": [
              {
                "op": "^",
                "args": [
                  "N1",
                  4
                ]
              },
              1e-300
            ]
          }
        ]
      }
    },
    {
      "lhs": "Q2",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "*",
            "args": [
              {
                "op": "^",
                "args": [
                  "XI_P",
                  2
                ]
              },
              {
                "op": "^",
                "args": [
                  "M2",
                  3
                ]
              },
              {
                "op": "^",
                "args": [
                  "N2",
                  2
                ]
              }
            ]
          },
          {
            "op": "+",
            "args": [
              {
                "op": "^",
                "args": [
                  "N2",
                  4
                ]
              },
              1e-300
            ]
          }
        ]
      }
    },
    {
      "lhs": "Q3",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "*",
            "args": [
              {
                "op": "^",
                "args": [
                  "XI_P",
                  2
                ]
              },
              {
                "op": "^",
                "args": [
                  "M3",
                  3
                ]
              },
              {
                "op": "^",
                "args": [
                  "N3",
                  2
                ]
              }
            ]
          },
          {
            "op": "+",
            "args": [
              {
                "op": "^",
                "args": [
                  "N3",
                  4
                ]
              },
              1e-300
            ]
          }
        ]
      }
    },
    {
      "lhs": "Q4",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "*",
            "args": [
              {
                "op": "^",
                "args": [
                  "XI_P",
                  2
                ]
              },
              {
                "op": "^",
                "args": [
                  "M4",
                  3
                ]
              },
              {
                "op": "^",
                "args": [
                  "N4",
                  2
                ]
              }
            ]
          },
          {
            "op": "+",
            "args": [
              {
                "op": "^",
                "args": [
                  "N4",
                  4
                ]
              },
              1e-300
            ]
          }
        ]
      }
    },
    {
      "lhs": "Q5",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "*",
            "args": [
              {
                "op": "^",
                "args": [
                  "XI_P",
                  2
                ]
              },
              {
                "op": "^",
                "args": [
                  "M5",
                  3
                ]
              },
              {
                "op": "^",
                "args": [
                  "N5",
                  2
                ]
              }
            ]
          },
          {
            "op": "+",
            "args": [
              {
                "op": "^",
                "args": [
                  "N5",
                  4
                ]
              },
              1e-300
            ]
          }
        ]
      }
    },
    {
      "lhs": "f1",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "<",
            "args": [
              "xb1",
              1.6e-14
            ]
          },
          0.0,
          {
            "op": "ifelse",
            "args": [
              {
                "op": ">",
                "args": [
                  "xb1",
                  3.2e-14
                ]
              },
              {
                "op": "/",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      2.0,
                      "N1"
                    ]
                  },
                  1.6e-14
                ]
              },
              {
                "op": "-",
                "args": [
                  {
                    "op": "/",
                    "args": [
                      {
                        "op": "*",
                        "args": [
                          4.0,
                          "N1"
                        ]
                      },
                      1.6e-14
                    ]
                  },
                  {
                    "op": "/",
                    "args": [
                      {
                        "op": "*",
                        "args": [
                          2.0,
                          "M1"
                        ]
                      },
                      2.56e-28
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "f2",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "<",
            "args": [
              "xb2",
              3.2e-14
            ]
          },
          0.0,
          {
            "op": "ifelse",
            "args": [
              {
                "op": ">",
                "args": [
                  "xb2",
                  6.4e-14
                ]
              },
              {
                "op": "/",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      2.0,
                      "N2"
                    ]
                  },
                  3.2e-14
                ]
              },
              {
                "op": "-",
                "args": [
                  {
                    "op": "/",
                    "args": [
                      {
                        "op": "*",
                        "args": [
                          4.0,
                          "N2"
                        ]
                      },
                      3.2e-14
                    ]
                  },
                  {
                    "op": "/",
                    "args": [
                      {
                        "op": "*",
                        "args": [
                          2.0,
                          "M2"
                        ]
                      },
                      1.024e-27
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "f3",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "<",
            "args": [
              "xb3",
              6.4e-14
            ]
          },
          0.0,
          {
            "op": "ifelse",
            "args": [
              {
                "op": ">",
                "args": [
                  "xb3",
                  1.28e-13
                ]
              },
              {
                "op": "/",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      2.0,
                      "N3"
                    ]
                  },
                  6.4e-14
                ]
              },
              {
                "op": "-",
                "args": [
                  {
                    "op": "/",
                    "args": [
                      {
                        "op": "*",
                        "args": [
                          4.0,
                          "N3"
                        ]
                      },
                      6.4e-14
                    ]
                  },
                  {
                    "op": "/",
                    "args": [
                      {
                        "op": "*",
                        "args": [
                          2.0,
                          "M3"
                        ]
                      },
                      4.096e-27
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "f4",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "<",
            "args": [
              "xb4",
              1.28e-13
            ]
          },
          0.0,
          {
            "op": "ifelse",
            "args": [
              {
                "op": ">",
                "args": [
                  "xb4",
                  2.56e-13
                ]
              },
              {
                "op": "/",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      2.0,
                      "N4"
                    ]
                  },
                  1.28e-13
                ]
              },
              {
                "op": "-",
                "args": [
                  {
                    "op": "/",
                    "args": [
                      {
                        "op": "*",
                        "args": [
                          4.0,
                          "N4"
                        ]
                      },
                      1.28e-13
                    ]
                  },
                  {
                    "op": "/",
                    "args": [
                      {
                        "op": "*",
                        "args": [
                          2.0,
                          "M4"
                        ]
                      },
                      1.6384e-26
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "f5",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "<",
            "args": [
              "xb5",
              2.56e-13
            ]
          },
          0.0,
          {
            "op": "ifelse",
            "args": [
              {
                "op": ">",
                "args": [
                  "xb5",
                  5.12e-13
                ]
              },
              {
                "op": "/",
                "args": [
                  {
                    "op": "*",
                    "args": [
                      2.0,
                      "N5"
                    ]
                  },
                  2.56e-13
                ]
              },
              {
                "op": "-",
                "args": [
                  {
                    "op": "/",
                    "args": [
                      {
                        "op": "*",
                        "args": [
                          4.0,
                          "N5"
                        ]
                      },
                      2.56e-13
                    ]
                  },
                  {
                    "op": "/",
                    "args": [
                      {
                        "op": "*",
                        "args": [
                          2.0,
                          "M5"
                        ]
                      },
                      6.5536e-26
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "psi1",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "<",
            "args": [
              "xb1",
              1.6e-14
            ]
          },
          {
            "op": "/",
            "args": [
              {
                "op": "*",
                "args": [
                  2.0,
                  "N1"
                ]
              },
              1.6e-14
            ]
          },
          {
            "op": "ifelse",
            "args": [
              {
                "op": ">",
                "args": [
                  "xb1",
                  3.2e-14
                ]
              },
              0.0,
              {
                "op": "-",
                "args": [
                  {
                    "op": "/",
                    "args": [
                      {
                        "op": "*",
                        "args": [
                          2.0,
                          "M1"
                        ]
                      },
                      2.56e-28
                    ]
                  },
                  {
                    "op": "/",
                    "args": [
                      {
                        "op": "*",
                        "args": [
                          2.0,
                          "N1"
                        ]
                      },
                      1.6e-14
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "psi2",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "<",
            "args": [
              "xb2",
              3.2e-14
            ]
          },
          {
            "op": "/",
            "args": [
              {
                "op": "*",
                "args": [
                  2.0,
                  "N2"
                ]
              },
              3.2e-14
            ]
          },
          {
            "op": "ifelse",
            "args": [
              {
                "op": ">",
                "args": [
                  "xb2",
                  6.4e-14
                ]
              },
              0.0,
              {
                "op": "-",
                "args": [
                  {
                    "op": "/",
                    "args": [
                      {
                        "op": "*",
                        "args": [
                          2.0,
                          "M2"
                        ]
                      },
                      1.024e-27
                    ]
                  },
                  {
                    "op": "/",
                    "args": [
                      {
                        "op": "*",
                        "args": [
                          2.0,
                          "N2"
                        ]
                      },
                      3.2e-14
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "psi3",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "<",
            "args": [
              "xb3",
              6.4e-14
            ]
          },
          {
            "op": "/",
            "args": [
              {
                "op": "*",
                "args": [
                  2.0,
                  "N3"
                ]
              },
              6.4e-14
            ]
          },
          {
            "op": "ifelse",
            "args": [
              {
                "op": ">",
                "args": [
                  "xb3",
                  1.28e-13
                ]
              },
              0.0,
              {
                "op": "-",
                "args": [
                  {
                    "op": "/",
                    "args": [
                      {
                        "op": "*",
                        "args": [
                          2.0,
                          "M3"
                        ]
                      },
                      4.096e-27
                    ]
                  },
                  {
                    "op": "/",
                    "args": [
                      {
                        "op": "*",
                        "args": [
                          2.0,
                          "N3"
                        ]
                      },
                      6.4e-14
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "psi4",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "<",
            "args": [
              "xb4",
              1.28e-13
            ]
          },
          {
            "op": "/",
            "args": [
              {
                "op": "*",
                "args": [
                  2.0,
                  "N4"
                ]
              },
              1.28e-13
            ]
          },
          {
            "op": "ifelse",
            "args": [
              {
                "op": ">",
                "args": [
                  "xb4",
                  2.56e-13
                ]
              },
              0.0,
              {
                "op": "-",
                "args": [
                  {
                    "op": "/",
                    "args": [
                      {
                        "op": "*",
                        "args": [
                          2.0,
                          "M4"
                        ]
                      },
                      1.6384e-26
                    ]
                  },
                  {
                    "op": "/",
                    "args": [
                      {
                        "op": "*",
                        "args": [
                          2.0,
                          "N4"
                        ]
                      },
                      1.28e-13
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "psi5",
      "rhs": {
        "op": "ifelse",
        "args": [
          {
            "op": "<",
            "args": [
              "xb5",
              2.56e-13
            ]
          },
          {
            "op": "/",
            "args": [
              {
                "op": "*",
                "args": [
                  2.0,
                  "N5"
                ]
              },
              2.56e-13
            ]
          },
          {
            "op": "ifelse",
            "args": [
              {
                "op": ">",
                "args": [
                  "xb5",
                  5.12e-13
                ]
              },
              0.0,
              {
                "op": "-",
                "args": [
                  {
                    "op": "/",
                    "args": [
                      {
                        "op": "*",
                        "args": [
                          2.0,
                          "M5"
                        ]
                      },
                      6.5536e-26
                    ]
                  },
                  {
                    "op": "/",
                    "args": [
                      {
                        "op": "*",
                        "args": [
                          2.0,
                          "N5"
                        ]
                      },
                      2.56e-13
                    ]
                  }
                ]
              }
            ]
          }
        ]
      }
    },
    {
      "lhs": "alpha1",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "-",
            "args": [
              "f1",
              "psi1"
            ]
          },
          3.2e-14
        ]
      }
    },
    {
      "lhs": "alpha2",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "-",
            "args": [
              "f2",
              "psi2"
            ]
          },
          6.4e-14
        ]
      }
    },
    {
      "lhs": "alpha3",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "-",
            "args": [
              "f3",
              "psi3"
            ]
          },
          1.28e-13
        ]
      }
    },
    {
      "lhs": "alpha4",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "-",
            "args": [
              "f4",
              "psi4"
            ]
          },
          2.56e-13
        ]
      }
    },
    {
      "lhs": "alpha5",
      "rhs": {
        "op": "/",
        "args": [
          {
            "op": "-",
            "args": [
              "f5",
              "psi5"
            ]
          },
          5.12e-13
        ]
      }
    }
  ],
  "tests": [
    {
      "id": "exponential_ic_constant",
      "description": "Upstream Aerosol.jl stochastic_collection_test.jl scenario, constant K(x,y)=K0 kernel, I=5 mass categories. Exponential initial droplet spectrum (N0=3e8 m^-3, LWC=1e-3 kg m^-3). Expected values are a SciPy LSODA reference integration (rtol=1e-10, abstol=1e-14) of the scalarized RHS; that RHS is verified against the upstream @arrayop model in the model reference notes (transcription audit, double-sum cross-check, and machine-precision no-overflow analytic identities).",
      "initial_conditions": {
        "N1": 1429670.6078643417,
        "M1": 3.430294470019302e-08,
        "N2": 2838836.0713738734,
        "M2": 1.3619145733423377e-07,
        "N3": 5596563.981307812,
        "M3": 5.366970575748642e-07,
        "N4": 10875864.787608625,
        "M4": 2.083711394480048e-06,
        "N5": 20538015.50564386,
        "M5": 7.852951776977424e-06
      },
      "time_span": {
        "start": 0.0,
        "end": 1000.0
      },
      "assertions": [
        {
          "variable": "N1",
          "time": 0.0,
          "expected": 1429670.6078643417
        },
        {
          "variable": "M5",
          "time": 0.0,
          "expected": 7.852951776977426e-06
        },
        {
          "variable": "N1",
          "time": 300.0,
          "expected": 598472.3040261099
        },
        {
          "variable": "N3",
          "time": 300.0,
          "expected": 2473717.8540761326
        },
        {
          "variable": "N5",
          "time": 300.0,
          "expected": 11602085.572298514
        },
        {
          "variable": "M3",
          "time": 300.0,
          "expected": 2.3788145085993707e-07
        },
        {
          "variable": "M5",
          "time": 300.0,
          "expected": 4.486753980882196e-06
        },
        {
          "variable": "N1",
          "time": 1000.0,
          "expected": 225470.2294585667
        },
        {
          "variable": "N3",
          "time": 1000.0,
          "expected": 979151.9833256787
        },
        {
          "variable": "N5",
          "time": 1000.0,
          "expected": 5765937.180969444
        },
        {
          "variable": "M3",
          "time": 1000.0,
          "expected": 9.439973524188377e-08
        },
        {
          "variable": "M5",
          "time": 1000.0,
          "expected": 2.255690898020376e-06
        }
      ]
    }
  ],
  "analyses": [
    {
      "id": "exponential_ic_evolution_constant",
      "description": "Evolution of the droplet number and mass spectra under the constant collection kernel, started from an exponential initial distribution. Number concentration decreases as droplets coalesce; mass shifts toward larger categories.",
      "initial_state": {
        "N1": 1429670.6078643417,
        "M1": 3.430294470019302e-08,
        "N2": 2838836.0713738734,
        "M2": 1.3619145733423377e-07,
        "N3": 5596563.981307812,
        "M3": 5.366970575748642e-07,
        "N4": 10875864.787608625,
        "M4": 2.083711394480048e-06,
        "N5": 20538015.50564386,
        "M5": 7.852951776977424e-06
      },
      "time_span": {
        "start": 0.0,
        "end": 1000.0
      },
      "plots": [
        {
          "id": "number_concentration",
          "type": "line",
          "description": "Number concentration N_k(t) for each of the 5 mass categories.",
          "x": {
            "variable": "t",
            "label": "time (s)"
          },
          "y": {
            "variable": "N1",
            "label": "number concentration (m^-3)"
          },
          "series": [
            {
              "name": "N1",
              "variable": "N1"
            },
            {
              "name": "N2",
              "variable": "N2"
            },
            {
              "name": "N3",
              "variable": "N3"
            },
            {
              "name": "N4",
              "variable": "N4"
            },
            {
              "name": "N5",
              "variable": "N5"
            }
          ]
        },
        {
          "id": "mass_concentration",
          "type": "line",
          "description": "Mass concentration M_k(t) for each of the 5 mass categories.",
          "x": {
            "variable": "t",
            "label": "time (s)"
          },
          "y": {
            "variable": "M1",
            "label": "mass concentration (kg*m^-3)"
          },
          "series": [
            {
              "name": "M1",
              "variable": "M1"
            },
            {
              "name": "M2",
              "variable": "M2"
            },
            {
              "name": "M3",
              "variable": "M3"
            },
            {
              "name": "M4",
              "variable": "M4"
            },
            {
              "name": "M5",
              "variable": "M5"
            }
          ]
        }
      ]
    }
  ]
}
```

</details>
