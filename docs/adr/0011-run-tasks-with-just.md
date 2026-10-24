# 11. Run tasks with just

- Status: accepted
- Date: 2026-10-24

## Context

The checks from the previous steps are four separate commands. Contributors and
CI must run the same set, in the same way, or CI becomes the first place a
failure shows up. That needs one entry point that lists and runs project tasks.

## Decision

Use just, with a `justfile` at the repository root. Install it as a development
dependency from PyPI (`rust-just`), so the lockfile pins its version and
`uv sync` provides it with everything else.

## Alternatives considered

- **Make.** Available almost everywhere, and the traditional answer. Rejected:
  it is a build system used as a task runner, so every task needs `.PHONY`,
  recipes are sensitive to tabs, and the version differs across platforms (GNU
  versus BSD make on macOS).
- **poethepoet (tasks in `pyproject.toml`).** Keeps everything in one file and
  installs from PyPI. Rejected narrowly: its task syntax is TOML strings, which
  get awkward as soon as a task needs more than one command or an argument.
- **nox or tox.** Rejected: built to run checks across several interpreters in
  separate environments. ADR-0007 fixes one interpreter and uv already owns the
  environment, so their main feature has nothing to do here.
- **Install just outside the project (Homebrew, `uv tool install`).** Rejected:
  every contributor and CI would install it separately, at whatever version is
  current there.

## Consequences

- `uv run just verify` is the single command for the full check suite.
- The `rust-just` wheel is published by a third party (`gnpaone/rust-just`),
  not by just's author. just's README lists it as the PyPI distribution, which
  is the trust this decision relies on.
- Contributors who want `just` without the `uv run` prefix can activate the
  virtual environment or install just globally.
