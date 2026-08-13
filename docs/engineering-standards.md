# Engineering Standards

This document is the single reference for how this repository is built, checked
and released. It grows by one section per setup step. Each section covers one
concern: the tools involved, what each of them solves, and which gate it imposes.

Decisions that had a defensible alternative are recorded separately as ADRs under
[`docs/adr/`](adr/), written in the step in which the decision was taken.

## Repository-wide rules

- All repository content is written in English: code, comments, documentation,
  CLI output and commit messages.
- Every commit follows [Conventional Commits](https://www.conventionalcommits.org/).
- Every non-obvious adjustment carries an adjacent comment stating its reason.
- A decision gets an ADR when all three hold: a competent person would defend the
  alternative, the choice constrains future work or is costly to reverse, and the
  reason is not evident from reading the file. Otherwise a comment is enough.

## 1. Repository foundations

**Concern:** the invariants every file in the repository must satisfy, and the
terms under which the repository is distributed.

| File | What it solves | Gate |
| --- | --- | --- |
| `.gitattributes` | Normalizes line endings to LF inside the repository regardless of the contributor's platform, and marks binary formats so Git never text-diffs them. | Enforced by Git itself on every `add` and `checkout`. |
| `.gitignore` | Keeps generated artefacts out of history: caches, the virtual environment, coverage reports. Deliberately does not ignore `uv.lock`. | None. Prevention only. |
| `.editorconfig` | Gives every editor the same charset, indentation and final-newline rules before any formatter exists. Covers the file types Ruff will never format: YAML, TOML, Markdown. | None. Prevention only. Ruff enforces Python formatting from section 5 onwards. |
| `LICENSE` | States the terms under which the project may be used and copied. | None. |

**Why this comes first:** line endings are the only irreversible setting in the
whole setup. Correcting them later takes a single commit that touches every file
and invalidates `git blame`, so it has to be in place before any other file
exists.

**Decisions:** [ADR-0001](adr/0001-normalize-line-endings-to-lf.md) ·
[ADR-0002](adr/0002-license-under-mit.md)
