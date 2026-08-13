# 5. Commit the uv lockfile

- Status: accepted
- Date: 2026-08-13

## Context

`uv.lock` records the exact resolved dependency set for every supported platform.
Whether to track it depends on what the project is. A library must work against a
range of versions and its lockfile would be ignored by consumers anyway, so
libraries usually leave it untracked. An application is the opposite case: there
is exactly one dependency set that matters, and CI has to reproduce it.

## Decision

Track `uv.lock`. `.gitignore` deliberately does not list it, and `.gitattributes`
marks it `linguist-generated=true` so it does not drown human changes in reviews.

## Alternatives considered

- **Ignore the lockfile.** Rejected: CI would re-resolve dependencies on every run,
  so a bad upstream release turns an untouched branch red, and a failure that
  reproduces locally but not in CI becomes impossible to diagnose.
- **Export `requirements.txt` instead.** Rejected: a second artefact to keep in
  sync, with weaker support for platform markers, when uv already consumes the
  lockfile natively.

## Consequences

- Dependency changes show up as reviewable diffs instead of happening invisibly.
- Merge conflicts on the lockfile do occur. They are resolved by re-running
  `uv lock`, never by editing the file by hand.
- CI only gets the benefit if it installs with `uv sync --locked`, which fails
  when the lockfile is out of date with respect to `pyproject.toml`. The flag is
  easy to get wrong: `--frozen` looks like the stricter option but is the
  opposite, taking the lockfile as the source of truth and never checking it, so
  a dependency change committed without re-locking passes unnoticed. Applied in
  the CI step.
