# `scripts/_archive/`

Historical one-shot tools. **MUST NOT be invoked from CI or runtime.** Kept for
git-log archeology only.

## Contents

- `migrations/` — one-shot translation tools that converted upstream MTK /
  Catalyst components into the committed `.esm` files under `components/`.
  Reference values produced by these scripts are now baked into `.esm` test
  assertions; the scripts themselves are no longer on any execution path.
- `diagnostics/` — closed-bead memory/perf diagnostic scripts. Kept for the
  phase breakdowns documented at the top of each file; the scripts are not
  invoked by any runner.

## Policy

Anything moved here is inert. Do not add it to `Project.toml`, `runtests.jl`,
or any GitHub Actions workflow. If a script in this directory becomes useful
again, move it back out of `_archive/` rather than referencing it in place —
that way the archive stays a clean "no live code" boundary.
