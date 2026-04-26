#!/usr/bin/env bash
# Bootstrap the scripts/migrations Julia environment so polecats can run
# GasChem-based migrations (e.g. migrate_geoschem_fullchem.jl) without
# re-discovering the upstream Catalyst/MTK compat patch every time.
#
# WHY this exists:
#   GasChem.jl 0.12.0 (the unreleased dev version polecats need for migrations
#   that target ESS 0.0.3+) declares `Catalyst = "15"` in [compat] but uses a
#   [sources] entry that pulls Catalyst master (which is v16+). EarthSciSerialization
#   0.0.3 requires `Catalyst = "16"`, so a naive `Pkg.develop("GasChem")` fails to
#   resolve — Pkg trusts the [compat] string, not what [sources] actually points at.
#   The published GasChem 0.11.0 is also unusable because it pins MTK 10 while ESS
#   wants MTK 11. Until upstream lands a release with bumped compat (Catalyst=16,
#   MTK=11), every polecat migrating a GasChem-based mechanism must apply this
#   patch. This script does it for them.
#
# What it does:
#   1. Pkg.develop the parent EarthSciModels project (this repo) into the
#      scripts/migrations env. Required because that env's Project.toml lists
#      EarthSciModels as a dep but it isn't registered.
#   2. Pkg.develop EarthSciSerialization from the workspace checkout (same
#      resolution rules as scripts/setup_polecat_env.sh) — required for the
#      same registry reason.
#   3. Locate the GasChem dev checkout, rewrite `Catalyst = "15"` →
#      `Catalyst = "16"` in its Project.toml (idempotent), then Pkg.develop
#      the patched checkout into the migrations env.
#   4. Pkg.instantiate.
#
# Resolution order for GasChem:
#   1. $GASCHEM_DEV_PATH (if set and a directory exists there)
#   2. ~/.julia/dev/GasChem (the standard `Pkg.develop("GasChem")` location)
#
# Resolution order for EarthSciSerialization:
#   1. $EARTHSCI_SERIALIZATION_PATH
#   2. ../../../../EarthSciSerialization/{refinery,mayor}/rig/packages/EarthSciSerialization.jl
#      (matches scripts/setup_polecat_env.sh)
#
# Usage (from the repo root):
#   scripts/migrations/setup_gaschem_env.sh
#
# Re-running is safe — every step is idempotent.

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
migrations_env="$repo_root/scripts/migrations"

# --- 1. GasChem dev checkout ------------------------------------------------

gaschem_path=""

if [[ -n "${GASCHEM_DEV_PATH:-}" ]]; then
  if [[ -d "$GASCHEM_DEV_PATH" ]]; then
    gaschem_path="$GASCHEM_DEV_PATH"
  else
    echo "warn: GASCHEM_DEV_PATH=$GASCHEM_DEV_PATH is not a directory; trying default" >&2
  fi
fi

if [[ -z "$gaschem_path" ]]; then
  default_path="$HOME/.julia/dev/GasChem"
  if [[ -f "$default_path/Project.toml" ]]; then
    gaschem_path="$default_path"
  fi
fi

if [[ -z "$gaschem_path" ]]; then
  cat >&2 <<EOF
error: could not find a GasChem dev checkout.

Tried:
  \$GASCHEM_DEV_PATH (unset or missing)
  ~/.julia/dev/GasChem (missing)

Fix: dev GasChem first so this script has something to patch:
  julia -e 'using Pkg; Pkg.develop("GasChem")'
Then re-run this script.
EOF
  exit 1
fi

gaschem_proj="$gaschem_path/Project.toml"
if [[ ! -f "$gaschem_proj" ]]; then
  echo "error: $gaschem_proj does not exist" >&2
  exit 1
fi

echo "GasChem dev checkout: $gaschem_path"

# Patch Catalyst compat: "15" -> "16". Idempotent — only acts when the old
# value is present. If the line shape ever drifts upstream, we leave it alone
# and warn so a human notices.
if grep -qE '^Catalyst = "15"$' "$gaschem_proj"; then
  echo "  patching Catalyst compat 15 -> 16 in $gaschem_proj"
  sed -i 's/^Catalyst = "15"$/Catalyst = "16"/' "$gaschem_proj"
elif grep -qE '^Catalyst = "16"$' "$gaschem_proj"; then
  echo "  Catalyst compat already at 16 — no patch needed"
else
  echo "warn: unexpected Catalyst compat line in $gaschem_proj — leaving alone:" >&2
  grep -nE '^Catalyst = ' "$gaschem_proj" >&2 || true
fi

# --- 2. EarthSciSerialization checkout --------------------------------------

ess_path=""

if [[ -n "${EARTHSCI_SERIALIZATION_PATH:-}" ]]; then
  if [[ -d "$EARTHSCI_SERIALIZATION_PATH" ]]; then
    ess_path="$EARTHSCI_SERIALIZATION_PATH"
  else
    echo "warn: EARTHSCI_SERIALIZATION_PATH=$EARTHSCI_SERIALIZATION_PATH is not a directory; trying workspace defaults" >&2
  fi
fi

if [[ -z "$ess_path" ]]; then
  for candidate in \
    "$repo_root/../../../../EarthSciSerialization/refinery/rig/packages/EarthSciSerialization.jl" \
    "$repo_root/../../../../EarthSciSerialization/mayor/rig/packages/EarthSciSerialization.jl"
  do
    if [[ -f "$candidate/Project.toml" ]]; then
      ess_path="$(cd "$candidate" && pwd)"
      break
    fi
  done
fi

if [[ -z "$ess_path" ]]; then
  cat >&2 <<EOF
error: could not find an EarthSciSerialization.jl checkout.

Tried:
  \$EARTHSCI_SERIALIZATION_PATH (unset or missing)
  ../../../../EarthSciSerialization/{refinery,mayor}/rig/packages/EarthSciSerialization.jl

Fix: run scripts/setup_polecat_env.sh first, or set EARTHSCI_SERIALIZATION_PATH.
EOF
  exit 1
fi

# --- 3. One Pkg call: develop all three local paths, then instantiate -------

echo "Pkg.develop into $migrations_env:"
echo "  EarthSciModels       <- $repo_root"
echo "  EarthSciSerialization <- $ess_path"
echo "  GasChem              <- $gaschem_path"

julia --project="$migrations_env" -e "
using Pkg
Pkg.develop([
    PackageSpec(path=\"$repo_root\"),
    PackageSpec(path=\"$ess_path\"),
    PackageSpec(path=\"$gaschem_path\"),
])
Pkg.instantiate()
"
