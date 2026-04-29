# Extract σ tables from Fast-JX.jl and compute reference j_X values for fastjx.esm.
# Avoids loading the GasChem package (its deps don't resolve under Julia 1.12); we
# transcribe just the constants and helpers we need.

using Pkg
Pkg.activate(temp=true)
Pkg.add(["StaticArrays", "BSON", "JSON", "Interpolations"])

using StaticArrays, BSON, JSON, Interpolations

const WL = SA_F32[187, 191, 193, 196, 202, 208, 211, 214,
                  261, 267, 277, 295, 303, 310, 316, 333, 380, 574]

# create_fjx_interp helpers (verbatim from fastjx_interp.jl)
function interp2_func(x1, x2, T1, T2)
    x1 ≈ x2 && return T -> Float64(x1)
    return T -> begin
        Tc = clamp(T, Float64(T1), Float64(T2))
        Float64(x1) + (Tc - Float64(T1)) * (Float64(x2) - Float64(x1)) / (Float64(T2) - Float64(T1))
    end
end
function interp3_func(x1, x2, x3, T1, T2, T3)
    (x1 ≈ x2 && x2 ≈ x3) && return T -> Float64(x1)
    return T -> begin
        Tc = clamp(T, Float64(T1), Float64(T3))
        if Tc < Float64(T2)
            Float64(x1) + (Tc - Float64(T1)) * (Float64(x2) - Float64(x1)) / (Float64(T2) - Float64(T1))
        else
            Float64(x2) + (Tc - Float64(T2)) * (Float64(x3) - Float64(x2)) / (Float64(T3) - Float64(T2))
        end
    end
end
function interp_func(temperatures, cross_sections)
    n = length(temperatures)
    n == 2 && return interp2_func(cross_sections[1], cross_sections[2],
                                  temperatures[1], temperatures[2])
    n == 3 && return interp3_func(cross_sections[1], cross_sections[2], cross_sections[3],
                                  temperatures[1], temperatures[2], temperatures[3])
    error("unexpected n=$n")
end
function create_fjx_interp(temperatures::Vector{Float32}, cross_sections::Vector{<:AbstractVector{Float32}})
    return [interp_func(temperatures, [x[i] for x in cross_sections]) for i in 1:length(cross_sections[1])]
end

# ---- σ tables (transcribed verbatim from Fast-JX.jl) ----

# H2COb (Fast-JX.jl:60)
const ϕ_H2COb_jx = 1.0f0
const σ_H2COb_T = Float32[223.0, 298.0]
const σ_H2COb_data = [
    Float32[0,0,0,0,0,0,0,0, 3.642e-21, 5.787e-21, 5.316e-21, 8.181e-21, 7.917e-21, 4.011e-21, 1.081e-20, 1.082e-20, 6.842e-23, 0],
    Float32[0,0,0,0,0,0,0,0, 3.649e-21, 5.768e-21, 5.305e-21, 8.154e-21, 7.914e-21, 4.002e-21, 1.085e-20, 1.085e-20, 6.819e-23, 0],
]
const σ_H2COb_interp = create_fjx_interp(σ_H2COb_T, σ_H2COb_data)

# N2O5 (Fast-JX.jl:84)
const ϕ_N2O5_jx = 1.0f0
const σ_N2O5_T = Float32[233.0, 300.0]
const σ_N2O5_data = [
    Float32[0,0, 8.922e-19, 1.183e-18, 5.868e-18, 4.682e-18, 3.395e-18, 2.613e-18, 2.138e-19, 2.155e-19, 1.988e-19, 3.772e-20, 2.182e-20, 1.334e-20, 8.419e-21, 2.621e-21, 4.355e-23, 0],
    Float32[0,0, 1.078e-18, 1.429e-18, 7.088e-18, 5.655e-18, 4.101e-18, 3.156e-18, 2.606e-19, 2.645e-19, 2.454e-19, 5.154e-20, 3.21e-20, 2.135e-20, 1.468e-20, 5.902e-21, 2.025e-22, 0],
]
const σ_N2O5_interp = create_fjx_interp(σ_N2O5_T, σ_N2O5_data)

# PAN (Fast-JX.jl:310)
const ϕ_PAN_jx = 1.0f0
const σ_PAN_T = Float32[250.0, 298.0]
const σ_PAN_data = [
    Float32[0, 5.8e-19, 4.36e-19, 3.7e-19, 2.456e-19, 1.766e-19, 1.515e-19, 1.302e-19, 1.659e-20, 1.039e-20, 4.282e-21, 5.401e-22, 2.493e-22, 1.184e-22, 5.444e-23, 7.412e-24, 8.046e-26, 0],
    Float32[0, 6.21e-19, 4.79e-19, 4.05e-19, 2.679e-19, 2.083e-19, 1.879e-19, 1.677e-19, 3.396e-20, 2.196e-20, 9.526e-21, 1.485e-21, 7.491e-22, 3.881e-22, 1.927e-22, 3.087e-23, 4.918e-25, 0],
]
const σ_PAN_interp = create_fjx_interp(σ_PAN_T, σ_PAN_data)

# H2O2 (Fast-JX.jl:425)
const ϕ_H2O2_jx = 1.0f0
const σ_H2O2_T = Float32[200.0, 300.0]
const σ_H2O2_data = [
    Float32[2.325e-19, 4.629e-19, 5.394e-19, 5.429e-19, 4.447e-19, 3.755e-19, 3.457e-19, 3.197e-19, 5.346e-20, 4.855e-20, 3.423e-20, 8.407e-21, 5.029e-21, 3.308e-21, 2.221e-21, 8.598e-22, 5.921e-24, 0],
    Float32[2.325e-19, 4.629e-19, 5.394e-19, 5.429e-19, 4.447e-19, 3.755e-19, 3.457e-19, 3.197e-19, 5.465e-20, 4.966e-20, 3.524e-20, 9.354e-21, 5.763e-21, 3.911e-21, 2.718e-21, 1.138e-21, 7.927e-24, 0],
]
const σ_H2O2_interp = create_fjx_interp(σ_H2O2_T, σ_H2O2_data)

# O31D quantum yield (Fast-JX.jl:501) — T-dependent, 3 T grid (200,260,300)
const ϕ_O31D_T = Float32[200.0, 260.0, 300.0]
const ϕ_O31D_data = [
    Float32[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.9094, 0.9094, 0.901, 0.7424, 0.5733, 0.0827, 0.0314, 0.087, 0.078, 0.078],
    Float32[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.9094, 0.9094, 0.9013, 0.7479, 0.5867, 0.1305, 0.0359, 0.087, 0.078, 0.078],
    Float32[1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 0.9094, 0.9094, 0.9026, 0.7799, 0.6657, 0.4083, 0.0728, 0.087, 0.078, 0.078],
]
const ϕ_O31D_interp = create_fjx_interp(ϕ_O31D_T, ϕ_O31D_data)

# O3 (Fast-JX.jl:757) — 3-T grid (218,258,298)
const ϕ_O3_jx = 1.0f0
const σ_O3_T = Float32[218.0, 258.0, 298.0]
const σ_O3_data = [
    Float32[5.988e-19, 4.859e-19, 4.307e-19, 3.654e-19, 3.41e-19, 4.849e-19, 6.534e-19, 9.32e-19, 8.757e-18, 3.513e-18, 1.508e-18, 7.925e-19, 2.456e-19, 8.904e-20, 3.661e-20, 4.539e-21, 6.167e-23, 1.666e-21],
    Float32[5.989e-19, 4.862e-19, 4.314e-19, 3.666e-19, 3.421e-19, 4.845e-19, 6.519e-19, 9.299e-19, 8.826e-18, 3.566e-18, 1.547e-18, 8.26e-19, 2.617e-19, 9.739e-20, 4.139e-20, 5.515e-21, 6.167e-23, 1.666e-21],
    Float32[5.99e-19, 4.866e-19, 4.32e-19, 3.678e-19, 3.432e-19, 4.84e-19, 6.504e-19, 9.278e-19, 8.896e-18, 3.618e-18, 1.586e-18, 8.595e-19, 2.778e-19, 1.058e-19, 4.617e-20, 6.493e-21, 6.167e-23, 1.666e-21],
]
const σ_O3_interp = create_fjx_interp(σ_O3_T, σ_O3_data)

# ActAld (Fast-JX.jl:798) — 2-T grid (235, 298)
const ϕ_ActAld_jx = 1.0f0
const σ_ActAld_T = Float32[235.0, 298.0]
const σ_ActAld_data = [
    Float32[0,0,0,0,0,0,0,0, 6.844e-22, 5.713e-21, 1.339e-20, 4.234e-20, 4.531e-20, 3.052e-20, 8.867e-21, 0, 0, 0],
    Float32[0,0,0,0,0,0,0,0, 7.282e-22, 6.121e-21, 1.43e-20, 4.508e-20, 4.853e-20, 3.246e-20, 9.443e-21, 0, 0, 0],
]
const σ_ActAld_interp = create_fjx_interp(σ_ActAld_T, σ_ActAld_data)

# NO3 (Fast-JX.jl:951) — 3-T grid (190, 230, 298)
const ϕ_NO3_jx = 1.0f0
const σ_NO3_T = Float32[190.0, 230.0, 298.0]
const σ_NO3_data = [
    Float32[0,0,0,0,0,0,0,0, 0,0,0,0, 1.42e-23, 4.16e-22, 1.74e-21, 1.74e-19, 1.911e-17, 0],
    Float32[0,0,0,0,0,0,0,0, 0,0,0,0, 1.42e-23, 4.16e-22, 1.74e-21, 1.74e-19, 1.911e-17, 0],
    Float32[0,0,0,0,0,0,0,0, 0,0,0,0, 1.42e-23, 4.16e-22, 1.74e-21, 1.74e-19, 1.911e-17, 0],
]
const σ_NO3_interp = create_fjx_interp(σ_NO3_T, σ_NO3_data)

# NO2 (Fast-JX.jl:875)
const ϕ_NO2_jx = 1.0f0
const σ_NO2_T = Float32[200.0, 300.0]
const σ_NO2_data = [
    Float32[0,0,0,0,0,0,0,0, 1.834e-20, 4.696e-20, 7.707e-20, 1.078e-19, 1.47e-19, 1.832e-19, 2.181e-19, 3.138e-19, 1.422e-19, 0],
    Float32[0,0,0,0,0,0,0,0, 2.354e-20, 4.697e-20, 7.546e-20, 1.063e-19, 1.477e-19, 1.872e-19, 2.303e-19, 3.469e-19, 1.546e-19, 0],
]
const σ_NO2_interp = create_fjx_interp(σ_NO2_T, σ_NO2_data)

# CH3OOH (Fast-JX.jl:890) — single SA, T-independent
const ϕ_CH3OOH_jx = 1.0f0
const σ_CH3OOH_data = Float32[0,0,0,0,0, 3.12e-19, 2.882e-19, 2.25e-19, 2.716e-20, 2.74e-20, 2.143e-20, 5.624e-21, 3.52e-21, 2.403e-21, 1.697e-21, 7.23e-22, 2.285e-23, 0]
const σ_CH3OOH_interp = [(T) -> Float64(σ_CH3OOH_data[i]) for i in 1:18]

# H2COa (Fast-JX.jl:907) — 2-T grid (223, 298)
const ϕ_H2COa_jx = 1.0f0
const σ_H2COa_T = Float32[223.0, 298.0]
const σ_H2COa_data = [
    Float32[0,0,0,0,0,0,0,0, 3.143e-21, 1.021e-20, 1.269e-20, 2.323e-20, 2.498e-20, 1.133e-20, 2.183e-20, 4.746e-21, 0, 0],
    Float32[0,0,0,0,0,0,0,0, 3.147e-21, 1.018e-20, 1.266e-20, 2.315e-20, 2.497e-20, 1.131e-20, 2.189e-20, 4.751e-21, 0, 0],
]
const σ_H2COa_interp = create_fjx_interp(σ_H2COa_T, σ_H2COa_data)

# ----- Flux interpolation tables -----
BSON.@load "/home/ctessum/.julia/dev/GasChem/src/tropospheric_interpolation_data.bson" Z_all tropospheric_P cosSZA_vals

# Build BSpline-Linear interpolators (matching upstream)
flux_itps = [extrapolate(Interpolations.scale(interpolate(Z_all[i], BSpline(Linear()), OnGrid()),
                                              tropospheric_P, cosSZA_vals), Flat()) for i in 1:18]

using Dates

# ----- cos_zenith via lib/solar.esm's exact NOAA Spencer-Fourier formula -----
# The migrated .esm sources cos_sza from Solar.cos_zenith via §4.7 inclusion, so
# reference j_X values must use the same formula (not GasChem's cos_solar_zenith_angle).
# This way the test compares apples to apples; tolerance can stay tight.
function lib_solar_cos_zenith(t_utc, lat_deg, lon_deg)
    dt = unix2datetime(t_utc)
    DOY = Dates.dayofyear(dt)
    H = Dates.hour(dt); Mn = Dates.minute(dt); S = Dates.second(dt)
    γ = 0.01721420632103996 * ((DOY - 1) + (H - 12)/24.0)
    δ = 0.006918 - 0.399912*cos(γ) + 0.070257*sin(γ) - 0.006758*cos(2γ) +
        0.000907*sin(2γ) - 0.002697*cos(3γ) + 0.00148*sin(3γ)
    EoT = 229.18 * (0.000075 + 0.001868*cos(γ) - 0.032077*sin(γ) -
                    0.014615*cos(2γ) - 0.040849*sin(2γ))
    TST = H*60.0 + Mn + S/60.0 + EoT + 4.0*lon_deg
    ω = 0.017453292519943295 * (TST/4.0 - 180.0)
    φ = 0.017453292519943295 * lat_deg
    return clamp(sin(φ)*sin(δ) + cos(φ)*cos(δ)*cos(ω), -1.0, 1.0)
end

# ----- Simulate j_X for reference values -----
function j_mean(σ_interp, ϕ, T, fluxes)
    j = 0.0
    for i in 1:18
        ϕ_val = (ϕ isa Vector && (ϕ[i] isa Function)) ? ϕ[i](T) : Float64(ϕ)
        j += fluxes[i] * σ_interp[i](T) * ϕ_val
    end
    return j
end

function reference_jX(t_unix, lat, long, T, P, H2O)
    CSZA = lib_solar_cos_zenith(t_unix, lat, long)

    fluxes = [flux_itps[i](P, CSZA) for i in 1:18]

    j_O3 = j_mean(σ_O3_interp, ϕ_O3_jx, T, fluxes)
    j_O31D = j_mean(σ_O3_interp, ϕ_O31D_interp, T, fluxes)
    j_NO2 = j_mean(σ_NO2_interp, ϕ_NO2_jx, T, fluxes)
    j_H2O2 = j_mean(σ_H2O2_interp, ϕ_H2O2_jx, T, fluxes)
    j_H2COa = j_mean(σ_H2COa_interp, ϕ_H2COa_jx, T, fluxes)
    j_H2COb = j_mean(σ_H2COb_interp, ϕ_H2COb_jx, T, fluxes)
    j_CH3OOH = j_mean(σ_CH3OOH_interp, ϕ_CH3OOH_jx, T, fluxes)
    j_NO3 = j_mean(σ_NO3_interp, ϕ_NO3_jx, T, fluxes)
    j_NO3a = j_NO3 * 0.886
    j_NO3b = j_NO3 * 0.114
    j_N2O5 = j_mean(σ_N2O5_interp, ϕ_N2O5_jx, T, fluxes)
    j_ActAld = j_mean(σ_ActAld_interp, ϕ_ActAld_jx, T, fluxes)
    j_PAN = j_mean(σ_PAN_interp, ϕ_PAN_jx, T, fluxes)

    # adjust_j_o31D
    A = 6.02e23; R = 8.314e6
    nd = A * P / (R * T)
    C_H2O = H2O * 1.0e-9 * nd
    C_O2 = 0.2095 * nd; C_N2 = 0.7808 * nd; C_H2 = 0.5e-6 * nd
    RO1DplH2O = 1.63e-10 * exp(60.0 / T) * C_H2O
    RO1DplH2 = 1.2e-10 * C_H2
    RO1DplN2 = 2.15e-11 * exp(110.0 / T) * C_N2
    RO1DplO2 = 3.3e-11 * exp(55.0 / T) * C_O2
    RO1D = RO1DplH2O + RO1DplH2 + RO1DplN2 + RO1DplO2
    j_O31D_adj = RO1DplH2O / RO1D
    j_o32OH = j_O31D * j_O31D_adj

    return Dict(
        "cosSZA" => CSZA,
        "F" => Float64.(fluxes),
        "j_O3" => j_O3, "j_O31D" => j_O31D, "j_o32OH" => j_o32OH,
        "j_NO2" => j_NO2, "j_H2O2" => j_H2O2,
        "j_H2COa" => j_H2COa, "j_H2COb" => j_H2COb,
        "j_CH3OOH" => j_CH3OOH,
        "j_NO3a" => j_NO3a, "j_NO3b" => j_NO3b,
        "j_N2O5" => j_N2O5, "j_ActAld" => j_ActAld, "j_PAN" => j_PAN,
        "j_O31D_adj" => j_O31D_adj,
    )
end

# Multiple test scenarios
scenarios = [
    Dict("id" => "noon_summer_eq", "t_unix" => datetime2unix(DateTime(2026, 6, 21, 12, 0, 0)),
         "lat" => 0.0, "long" => 0.0, "T" => 298.0, "P" => 101325.0, "H2O" => 450.0),
    Dict("id" => "morning_midlat", "t_unix" => datetime2unix(DateTime(2026, 6, 21, 9, 0, 0)),
         "lat" => 40.0, "long" => -97.0, "T" => 298.0, "P" => 101325.0, "H2O" => 450.0),
    Dict("id" => "noon_winter_midlat", "t_unix" => datetime2unix(DateTime(2026, 12, 21, 12, 0, 0)),
         "lat" => 40.0, "long" => -97.0, "T" => 273.0, "P" => 95000.0, "H2O" => 100.0),
]
results = Dict[]
for sc in scenarios
    r = reference_jX(sc["t_unix"], sc["lat"], sc["long"], sc["T"], sc["P"], sc["H2O"])
    push!(results, merge(sc, r))
end

# Output JSON
out = Dict(
    "tropospheric_P" => collect(tropospheric_P),
    "cosSZA_vals" => collect(cosSZA_vals),
    "Z_all" => [Float64.(collect(Z_all[i])) for i in 1:18],
    "WL" => Float64.(collect(WL)),
    # Cross sections per species — list of T grid + per-bin tables (or scalar)
    "species" => Dict(
        "H2O2" => Dict("T_grid" => Float64.(σ_H2O2_T),
                       "sigma" => [Float64.(σ_H2O2_data[k]) for k in 1:length(σ_H2O2_T)],
                       "phi" => Float64(ϕ_H2O2_jx)),
        "H2COa" => Dict("T_grid" => Float64.(σ_H2COa_T),
                        "sigma" => [Float64.(σ_H2COa_data[k]) for k in 1:length(σ_H2COa_T)],
                        "phi" => Float64(ϕ_H2COa_jx)),
        "H2COb" => Dict("T_grid" => Float64.(σ_H2COb_T),
                        "sigma" => [Float64.(σ_H2COb_data[k]) for k in 1:length(σ_H2COb_T)],
                        "phi" => Float64(ϕ_H2COb_jx)),
        "O3" => Dict("T_grid" => Float64.(σ_O3_T),
                     "sigma" => [Float64.(σ_O3_data[k]) for k in 1:length(σ_O3_T)],
                     "phi" => Float64(ϕ_O3_jx)),
        "NO3" => Dict("T_grid" => Float64.(σ_NO3_T),
                      "sigma" => [Float64.(σ_NO3_data[k]) for k in 1:length(σ_NO3_T)],
                      "phi" => Float64(ϕ_NO3_jx)),
        "N2O5" => Dict("T_grid" => Float64.(σ_N2O5_T),
                       "sigma" => [Float64.(σ_N2O5_data[k]) for k in 1:length(σ_N2O5_T)],
                       "phi" => Float64(ϕ_N2O5_jx)),
        "NO2" => Dict("T_grid" => Float64.(σ_NO2_T),
                      "sigma" => [Float64.(σ_NO2_data[k]) for k in 1:length(σ_NO2_T)],
                      "phi" => Float64(ϕ_NO2_jx)),
        "CH3OOH" => Dict("T_grid" => Float64[],
                         "sigma_const" => Float64.(σ_CH3OOH_data),
                         "phi" => Float64(ϕ_CH3OOH_jx)),
        "ActAld" => Dict("T_grid" => Float64.(σ_ActAld_T),
                         "sigma" => [Float64.(σ_ActAld_data[k]) for k in 1:length(σ_ActAld_T)],
                         "phi" => Float64(ϕ_ActAld_jx)),
        "PAN" => Dict("T_grid" => Float64.(σ_PAN_T),
                      "sigma" => [Float64.(σ_PAN_data[k]) for k in 1:length(σ_PAN_T)],
                      "phi" => Float64(ϕ_PAN_jx)),
    ),
    "phi_O31D" => Dict("T_grid" => Float64.(ϕ_O31D_T),
                       "phi" => [Float64.(ϕ_O31D_data[k]) for k in 1:length(ϕ_O31D_T)]),
    "scenarios" => results,
)
open("/tmp/fastjx_data.json", "w") do io
    JSON.print(io, out)
end
println("wrote /tmp/fastjx_data.json (", round(filesize("/tmp/fastjx_data.json")/1024, digits=1), " KB)")
println()
println("Reference values (scenario 1: noon summer equator):")
for (k, v) in results[1]
    if k in ("F","cosSZA","j_O3","j_O31D","j_o32OH","j_NO2","j_H2O2","j_H2COa","j_H2COb","j_CH3OOH","j_NO3a","j_NO3b","j_N2O5","j_ActAld","j_PAN")
        println("  $k = $v")
    end
end
