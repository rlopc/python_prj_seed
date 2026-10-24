# 13. Version and keep a changelog with python-semantic-release

- Status: accepted
- Date: 2026-10-24

## Context

Every commit already follows Conventional Commits, so the history states which
changes are fixes, features or breaking. Without a tool reading it, that
discipline has no payoff, and `version` in `pyproject.toml` has no owner: it
stays at whatever someone last typed.

Nothing built from this seed is published (see the README), so the tool only
has to set the version, tag the release and write the changelog.

## Decision

Run python-semantic-release in CI, on every push to `main` that passes
`verify`. It derives the next version from the commits since the last tag,
writes it to `project.version`, re-locks `uv.lock` for it, updates
`CHANGELOG.md`, and pushes a release commit and a `v<version>` tag. It creates
no GitHub Release and publishes nothing.

Versions stay below 1.0.0 until one is cut deliberately: while on 0.x, a
breaking change bumps the minor version.

It is installed in its own `release` dependency group, so the lockfile pins it
but it stays out of the default development environment.

## Alternatives considered

- **Manual versioning (with bump-my-version or by hand).** Rejected: it relies
  on someone deciding the bump and writing the changelog on every release, which
  the commit history already encodes.
- **release-please.** Opens a release pull request that is reviewed and merged,
  which is a real advantage. Rejected: its Python strategy updates
  `pyproject.toml` but has no updater for `uv.lock`, so keeping
  `uv sync --locked` passing would need a hand-written rule for the lockfile.
- **Commitizen (`cz bump`).** Comparable features. Rejected narrowly:
  python-semantic-release documents a uv integration, which is exactly the
  lockfile problem above.

## Consequences

- A release happens on every qualifying push to `main`; `docs:`, `test:`,
  `ci:`, `build:`, `chore:` and `style:` commits do not trigger one.
- The release commit is pushed with the workflow token, and GitHub does not run
  workflows for pushes made with it. That commit is therefore never verified by
  CI; it only touches the version, the lockfile and the changelog.
- If `main` is protected against direct pushes, the workflow token cannot push
  the release commit. Protecting `main` then requires an exception for the
  workflow, or a token with that permission stored as a secret.
- `CHANGELOG.md` does not exist until the first release creates it.
