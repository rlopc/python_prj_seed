# 10. Lint and format with Ruff, extending its default rule set

- Status: accepted
- Date: 2026-10-24

## Context

Linting and formatting used to take several tools: Black for formatting, isort
for imports, and Flake8 with a set of plugins for linting. Ruff reimplements
all of them in one tool, configured in `pyproject.toml`.

The open question is which lint rules to enable. Until 0.15, Ruff's default set
was 59 rules, so any serious configuration replaced it with its own `select`
list. Ruff 0.16 (July 2026) turned the default into a curated selection of
several hundred rules drawn from more than thirty linters, chosen to flag code
that is wrong, suspicious, needlessly complex, slow or unidiomatic. Security
rules stay off by default because they favour false positives.
`select = ["ALL"]` enables every rule, including each new one an upgrade adds.

## Decision

Use Ruff as both linter and formatter, with the formatter's defaults. Keep
Ruff's default rule set and add the flake8-bandit security rules with
`extend-select = ["S"]`. Ignore individual rules only per file, with a reason.

## Alternatives considered

- **Black, isort and Flake8.** Rejected: three tools and three configurations to
  keep consistent, for the same checks Ruff provides.
- **An explicit `select` list of rule families.** Ruff's documentation prefers
  `select` for explicitness, and it was the norm while the default was small.
  Rejected: it replaces a curated set with whole families, which drops the
  default rules of every family not listed and enables every noisy rule of
  those that are. Keeping it equivalent would mean maintaining hundreds of
  rule codes by hand.
- **`select = ["ALL"]` with ignores.** Rejected: every Ruff upgrade can enable
  rules no one chose, and the ignore list grows with rules that conflict with
  each other or with the formatter.

## Consequences

- The enabled set is whatever the pinned Ruff version defines as default, plus
  `S`. `ruff check --show-settings` lists it in full.
- A Ruff upgrade can change the default set, as 0.16 and 0.17 did. The lockfile
  pins Ruff, so that happens only when Ruff is bumped on purpose, and the
  bump's lint failures are reviewed in the same change.
- Docstring rules (pydocstyle) are not enabled beyond the default: mypy-checked
  signatures carry most of what they would enforce.
