# 6. Support Python 3.12+ and develop on the floor version

- Status: accepted
- Date: 2026-08-13

## Context

Two related questions: which Python versions the project claims to support, and
which one is used for local development.

For the first, SPEC 0 recommends supporting the minor versions released in the
last three years, with a floor of the last two. As of 2026-08-13 that window
starts in August 2023: Python 3.12 (October 2023) is inside it, 3.11 (October
2022) is not. The latest stable release is 3.14.

The second question is independent, and the two are often conflated.

## Decision

- `requires-python = ">=3.12"`, with no upper bound.
- `.python-version = 3.12` — local development happens on the floor version.
- The CI matrix covers every supported minor: 3.12, 3.13 and 3.14.

## Alternatives considered

- **Develop on the latest stable (3.14), let CI cover the floor.** Rejected:
  syntax and standard-library APIs added after 3.12 would work on the developer's
  machine and fail only in CI, late and out of context. Developing on the floor
  makes incompatibilities fail where they are written. Ruff and mypy also target
  3.12, but static checks do not cover runtime behaviour.
- **Add an upper bound such as `<3.15`.** Rejected: it breaks users on a version
  that would have worked, to protect against a hypothetical incompatibility, and
  requires a manual edit every October.
- **Also support 3.11.** Rejected: outside the SPEC 0 window. Each extra minor is
  another CI job and another constraint on the code, paid for indefinitely.

## Consequences

- Nothing verifies Python versions outside the matrix. Supporting a new release
  means adding a row to the matrix, not editing `requires-python`.
- Post-3.12 features are unavailable locally. That is the intended effect.
- `.python-version` pins the minor, not the patch: CPython patch releases are
  compatible, and pinning them would create churn with no benefit.
- This policy expires. Around October 2026, 3.15 ships and 3.12 leaves the
  three-year window, so the floor moves to 3.13. Revisit annually.
