"""
    EarthSciModels

Thin Julia shim over `EarthSciSerialization.jl` for loading `.esm` files from
this repo as ready-to-simulate `ModelingToolkit.System` / `PDESystem` objects.

This package intentionally contains no model content — the authoritative models
live in the `.esm` files under `models/`, `reaction_systems/`, `operators/`,
`data_loaders/`, `coupling/`, and `interfaces/` at the repo root. See
`docs/REPO_LAYOUT.md` for the directory convention and
`docs/migration-tracker.md` for the migration inventory.

## Quickstart

```julia
using EarthSciModels
using ModelingToolkit   # required to materialize System; ESS MTK extension loads

sys = load_esm(joinpath(pkgdir(EarthSciModels), "models/gaschem/superfast.esm"))
```

For multi-component files, or to choose which model in a file to materialize,
use `EarthSciSerialization.load(path)` directly and then construct the desired
`System`/`PDESystem`/`ReactionSystem` from the returned `EsmFile`.
"""
module EarthSciModels

import EarthSciSerialization

export load_esm, esm_root, esm_path

"""
    load_esm(path::AbstractString)

Load an ESM file and return a ModelingToolkit `System` built from its single
top-level model.

Requires `ModelingToolkit` (and optionally `Catalyst` / `DomainSets`) to be
loaded at the call site so `EarthSciSerialization`'s MTK extension is active.

Raises an `ArgumentError` when the file contains zero or multiple models — in
that case use `EarthSciSerialization.load(path)` directly and pick the model
you want.
"""
function load_esm(path::AbstractString)
    esm_file = EarthSciSerialization.load(String(path))
    models = esm_file.models
    if models === nothing || isempty(models)
        throw(ArgumentError("ESM file has no models: $(path). Use EarthSciSerialization.load() for non-Model entries (reaction_systems, operators, data_loaders)."))
    elseif length(models) == 1
        return _to_system(first(values(models)))
    else
        names = collect(keys(models))
        throw(ArgumentError("ESM file has multiple models $(names); call EarthSciSerialization.load() and materialize the one you want."))
    end
end

# Resolved at runtime so the MTK extension (which defines
# `ModelingToolkit.System(::Model)`) is already loaded by the caller.
function _to_system(model)
    mtk_mod = get(Base.loaded_modules,
        Base.PkgId(Base.UUID("961ee093-0014-501f-94e3-6117800e7a78"), "ModelingToolkit"),
        nothing)
    if mtk_mod === nothing
        throw(ArgumentError("load_esm requires ModelingToolkit to be loaded. Call `using ModelingToolkit` first."))
    end
    return mtk_mod.System(model)
end

"""
    esm_root() -> String

Absolute path to the root of this repo's `.esm` tree (the package directory).
"""
esm_root() = pkgdir(@__MODULE__)

"""
    esm_path(parts...) -> String

Join `parts` onto the repo root. Example: `esm_path("models", "gaschem", "superfast.esm")`.
"""
esm_path(parts::AbstractString...) = joinpath(esm_root(), parts...)

end # module
