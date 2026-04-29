# run_geoschem_fullchem_tests.jl
#
# Verification harness: runs run_esm_tests on the geoschem_fullchem .esm only.
# Prints summary and exits with the test runner's exit code.
using Pkg
Pkg.activate("scripts/migrations")
using EarthSciModels
using ModelingToolkit
using Catalyst
using OrdinaryDiffEqRosenbrock

# Walk only the geoschem_fullchem.esm file to keep CI iteration fast — the
# main test target (`test/runtests.jl`) walks `components/` for full coverage.
results, exit_code = EarthSciModels.run_esm_tests(["components/gaschem"];
    verbose=true)
println("\nexit_code=$(exit_code)")
exit(exit_code)
