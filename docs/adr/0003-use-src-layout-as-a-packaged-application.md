# 3. Use a src layout as a packaged application

- Status: accepted
- Date: 2026-08-13

## Context

This project is an application, not a library: it is never uploaded anywhere.
That raised a fair question — if nothing is distributed, why make the code an
installable package at all, rather than a few modules at the repository root?

Since uv 0.12 the src layout plus a `[build-system]` is the default for every
project type, applications included; the flat layout has to be requested with
`--no-package`. pytest's own guidance is stronger: it *strongly* suggests a src
layout. The PyPA guide is neutral but lists correctness advantages only on the
src side.

## Decision

Lay the code out as `src/python_prj_seed/`, declare a `[build-system]`, and let
`uv sync` install the project into the environment in editable mode.

## Alternatives considered

- **Flat layout (`uv init --no-package`).** Rejected. Code at the repository root
  is importable from the current working directory, so tests import files that
  were never installed and packaging mistakes only surface in deployment. It also
  gives no namespace, so module names compete with everything in `site-packages`,
  and `[project.scripts]` has no dotted path to point at.
- **src layout without a build system.** Rejected as not viable: nothing would put
  `src/` on `sys.path` except test-runner configuration, which reintroduces the
  working-directory import problem under another name.

## Consequences

- The code is not importable until installed. `uv sync` does that and `uv run`
  guarantees it, at the cost of one setup step for newcomers.
- Tests exercise the installed package, so what is tested is what runs.
- The domain/delivery boundary becomes expressible and checkable as
  `python_prj_seed.domain` versus `python_prj_seed.cli`.
- A build backend is now required. See ADR-0004.
