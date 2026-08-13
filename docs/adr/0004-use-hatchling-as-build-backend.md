# 4. Use Hatchling as the build backend

- Status: accepted
- Date: 2026-08-13

## Context

ADR-0003 requires a `[build-system]`. uv ships its own backend, `uv_build`, which
is what `uv init` selects by default: it is very fast, needs no configuration and
is tightly integrated with uv. Its documented limitations — pure Python only, no
build scripts, less layout flexibility — do not affect this project.

So on technical merit alone `uv_build` would win. The counterweight is what this
repository is for: it is a seed, copied into other projects, and those copies do
not inherit our toolchain assumptions.

## Decision

Use `hatchling` as the build backend.

## Alternatives considered

- **`uv_build` (the default).** Rejected, and it is a close call. It is faster and
  simpler, and for this application in isolation it would be the better choice.
  It was rejected because it makes building the project depend on uv specifically,
  and a project started from this seed may end up built by `pip`, `build`, or a
  pipeline where uv is not present. Hatchling costs a small amount of speed to
  remove that coupling.
- **setuptools.** Rejected: it works everywhere, but needs explicit configuration
  for a src layout and carries legacy behaviour hatchling does not.
- **flit-core, pdm-backend.** Rejected: no advantage here over hatchling, and a
  smaller share of the ecosystem, so less familiar to contributors.

## Consequences

- Any PEP 517 frontend can build the project without uv installed.
- Hatchling infers `src/python_prj_seed` from the normalized project name, so no
  `[tool.hatch]` configuration is needed.
- Builds are marginally slower than with `uv_build`. This is invisible here: the
  project is only ever built for the editable install.
- The decision is cheap to revert — it is three lines in `[build-system]`.
