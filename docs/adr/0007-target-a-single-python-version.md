# 7. Target a single Python version, one year behind the newest

- Status: accepted
- Date: 2026-10-24
- Supersedes: [ADR-0006](0006-python-version-policy.md)

## Context

ADR-0006 took its version policy from SPEC 0 and committed to a CI matrix over
every supported minor. Both answer a library's question: how far back must the
code keep working so that whoever installs it is not left out. This seed only
produces applications (see the README), and an application has no installers to
accommodate: it runs on one interpreter, chosen by whoever deploys it.

As of 2026-10-24, 3.15.0 has been out for two weeks (released 2026-10-09) and
3.14 for a year. PEP 745 gives 3.14 bugfix releases until October 2027 and
source-only security releases until October 2030.

## Decision

- One target version, used everywhere: `.python-version`, CI and deployment.
  It is the newest minor that has been out for at least a year — 3.14 today.
- `requires-python = ">=3.14"`, with no upper bound.
- Move up one minor every October, when the next one ships.

## Alternatives considered

- **Keep the floor-plus-matrix policy of ADR-0006, floor moved to 3.13.**
  Rejected: every extra minor is another CI job and another constraint on the
  code, paid for a compatibility promise no one is owed.
- **Target the newest release, 3.15.** Rejected for now: a fresh x.0 commonly
  lacks wheels for compiled dependencies and support in tooling for months. The
  one-year rule gives the ecosystem that time.
- **Pin `requires-python = "==3.14.*"`.** Rejected: it adds an edit to every
  yearly upgrade and blocks trying the next version locally, while
  `.python-version` and CI already fix the version that is actually run.

## Consequences

- Nothing verifies any version other than 3.14. `requires-python` only states
  the lowest version the code is written for; it is not a support promise.
- Ruff infers its target from `requires-python`. mypy does not: it targets
  whichever interpreter runs it, so `[tool.mypy] python_version` must be set
  explicitly.
- 3.14 leaves bugfix support in October 2027, the same month this policy moves
  the target to 3.15, so the target is always within bugfix support.
- The yearly upgrade applies this rule, so it needs no new ADR: it changes
  `.python-version` and `requires-python`, re-runs `uv lock`, and updates the
  standards document.
