#!/usr/bin/env bash
# Resolve a local checkout of the GasChem.jl *source tree* so a migration
# polecat can read a component's source from the path recorded in its bead's
# `source_path` metadata (e.g. src/methane_oxidation.jl:213) WITHOUT running an
# unbounded `bfs /` / `find /` filesystem search.
#
# WHY this exists (esm-gp47):
#   Migration beads carry a `source_path` relative to the upstream repo root.
#   With no known GasChem.jl checkout on disk, polecats fell back to walking
#   the whole filesystem from `/` to locate the file. Each walk traversed tens
#   of GB of unrelated worktrees and Dolt data, ran for *hours*, ballooned to
#   GB-scale RSS, and orphaned (PPID=1) when the launching session ended. This
#   script gives polecats a bounded, cached checkout instead — no search.
#
# Prints the absolute path of the resolved checkout to STDOUT (and nothing
# else to stdout, so a caller can capture it):
#
#   GASCHEM_SRC=$(scripts/resolve_gaschem_src.sh)
#   cat "$GASCHEM_SRC/src/methane_oxidation.jl"
#
# Resolution order (first hit wins; mirrors scripts/setup_polecat_env.sh):
#   1. $GASCHEM_SRC          — explicit override; an existing checkout, used as-is.
#   2. ~/.julia/dev/GasChem  — a `Pkg.develop("GasChem")` checkout, if present.
#   3. Clone fallback        — git clone EarthSciML/GasChem.jl at the commit
#      pinned in docs/migration-tracker.md into a per-user cache
#      ($XDG_CACHE_HOME/earthsci-migration-src/GasChem.jl), checked out detached
#      at that SHA. The clone is cached: the first polecat pays for it, the
#      rest reuse it. Idempotent — re-runs reuse the cached checkout.
#
# Usage:
#   scripts/resolve_gaschem_src.sh                       # resolve, print path
#   GASCHEM_SRC=/path/to/GasChem.jl scripts/resolve_gaschem_src.sh
#   GASCHEM_SRC_REV=<sha> scripts/resolve_gaschem_src.sh  # pin a different rev
#
# Runnable from any directory — the clone fallback caches under $HOME, so the
# script does not depend on the current working directory.

set -euo pipefail

# Commit GasChem.jl is pinned at in docs/migration-tracker.md ("Pinned commit
# SHAs"). Keep this in sync with that table — it is what makes the tracker's
# `source_path:LINE` numbers correct.
PINNED_SHA="8c12c048482b515fb8eb2110bf8ab4b4f4e71309"
GASCHEM_URL="https://github.com/EarthSciML/GasChem.jl.git"

# Diagnostics go to stderr; stdout carries only the resolved path.
log() { echo "$@" >&2; }

# A plausible GasChem.jl checkout has a src/ tree and a Project.toml naming it.
is_gaschem_checkout() {
  [[ -d "$1/src" && -f "$1/Project.toml" ]] && \
    grep -q '^name *= *"GasChem"' "$1/Project.toml"
}

resolved=""

# --- 1. Explicit override ---------------------------------------------------
if [[ -n "${GASCHEM_SRC:-}" ]]; then
  if is_gaschem_checkout "$GASCHEM_SRC"; then
    resolved="$(cd "$GASCHEM_SRC" && pwd)"
    log "resolve_gaschem_src: using \$GASCHEM_SRC=$resolved"
  else
    log "warn: \$GASCHEM_SRC=$GASCHEM_SRC is not a GasChem.jl checkout" \
        "(no src/ + Project.toml naming GasChem); trying other sources"
  fi
fi

# --- 2. Julia dev checkout --------------------------------------------------
if [[ -z "$resolved" ]]; then
  julia_depot="${JULIA_DEPOT_PATH:-}"
  julia_depot="${julia_depot%%:*}"          # first entry of a colon-list, if set
  dev_path="${julia_depot:-$HOME/.julia}/dev/GasChem"
  if is_gaschem_checkout "$dev_path"; then
    resolved="$(cd "$dev_path" && pwd)"
    log "resolve_gaschem_src: using Julia dev checkout $resolved"
  fi
fi

# --- 3. Clone fallback (pinned SHA, cached) ---------------------------------
if [[ -z "$resolved" ]]; then
  cache_root="${XDG_CACHE_HOME:-$HOME/.cache}/earthsci-migration-src"
  cache_dir="$cache_root/GasChem.jl"
  rev="${GASCHEM_SRC_REV:-$PINNED_SHA}"
  mkdir -p "$cache_root"

  # A directory left behind by an aborted clone has no .git — clear it.
  if [[ -e "$cache_dir" && ! -d "$cache_dir/.git" ]]; then
    log "resolve_gaschem_src: $cache_dir is not a git checkout; clearing stale cache"
    rm -rf "$cache_dir"
  fi

  # Populate the cache once. The clone + checkout happen in a private temp
  # dir, then publish atomically with `mv -T` — so concurrent migration
  # polecats never race on a shared .git (esm-gp47 saw up to ~9 at once).
  if [[ ! -d "$cache_dir/.git" ]]; then
    log "resolve_gaschem_src: cloning $GASCHEM_URL -> $cache_dir"
    tmp_clone="$(mktemp -d "$cache_root/.clone.XXXXXX")"
    if git clone --quiet "$GASCHEM_URL" "$tmp_clone" \
       && git -C "$tmp_clone" checkout --quiet --detach "$rev"; then
      # mv -T renames onto cache_dir, or fails if a rival run published first.
      mv -T "$tmp_clone" "$cache_dir" 2>/dev/null \
        || log "resolve_gaschem_src: $cache_dir already populated by a concurrent run; using it"
      rm -rf "$tmp_clone"   # no-op when mv -T succeeded
    else
      rm -rf "$tmp_clone"
      log "error: could not clone $GASCHEM_URL at $rev (network, auth, or bad rev?)."
      log "  Set \$GASCHEM_SRC to an existing GasChem.jl checkout and re-run."
      exit 1
    fi
  fi

  # Cache exists. Re-checkout only if it has drifted off the requested rev
  # (e.g. a custom $GASCHEM_SRC_REV against an older cache). Steady state —
  # cache already at rev — is a pure read: no fetch, no checkout, no lock.
  cache_head="$(git -C "$cache_dir" rev-parse HEAD 2>/dev/null || true)"
  if [[ "$cache_head" != "$rev" ]]; then
    if ! git -C "$cache_dir" cat-file -e "${rev}^{commit}" 2>/dev/null; then
      log "resolve_gaschem_src: fetching $rev from origin"
      git -C "$cache_dir" fetch --quiet origin
    fi
    log "resolve_gaschem_src: checking out $rev in $cache_dir"
    git -C "$cache_dir" checkout --quiet --detach "$rev"
  fi

  if is_gaschem_checkout "$cache_dir"; then
    resolved="$cache_dir"
    log "resolve_gaschem_src: using cached clone $resolved (at $rev)"
  fi
fi

if [[ -z "$resolved" ]]; then
  log "error: could not resolve a GasChem.jl source checkout."
  log "  Set \$GASCHEM_SRC to a checkout, or check network access for the clone fallback."
  exit 1
fi

# Soft check: the tracker's `source_path:LINE` numbers are relative to the
# pinned SHA. Warn (don't fail) if a resolved checkout has drifted off it.
if git -C "$resolved" rev-parse --git-dir >/dev/null 2>&1; then
  head_sha="$(git -C "$resolved" rev-parse HEAD 2>/dev/null || true)"
  if [[ -n "$head_sha" && "$head_sha" != "$PINNED_SHA" && -z "${GASCHEM_SRC_REV:-}" ]]; then
    log "warn: $resolved is at $head_sha,"
    log "      not the tracker-pinned $PINNED_SHA."
    log "      \`source_path\` line numbers may be off — verify against docs/migration-tracker.md."
  fi
fi

echo "$resolved"
