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
| `.editorconfig` | Gives every editor the same charset, indentation and final-newline rules before any formatter exists. Covers the file types Ruff will never format: YAML, JSON, Markdown. | None. Prevention only. Ruff enforces Python formatting from section 5 onwards. |
| `LICENSE` | States the terms under which the project may be used and copied. | None. |

**Why this comes first:** line endings are the only irreversible setting in the
whole setup. Correcting them later takes a single commit that touches every file
and invalidates `git blame`, so it has to be in place before any other file
exists.

**Decisions:** [ADR-0001](adr/0001-normalize-line-endings-to-lf.md) ·
[ADR-0002](adr/0002-license-under-mit.md)

## 2. Environment and packaging

**Concern:** which interpreter runs the code, which dependencies are installed,
and how the source tree becomes importable.

| Tool / file | What it solves | Gate |
| --- | --- | --- |
| `uv` | Resolves dependencies, provisions the interpreter, owns the virtual environment, and runs commands inside it via `uv run`. | `uv sync --locked` fails when `uv.lock` is out of date with respect to `pyproject.toml`. Not `--frozen`, which skips that check entirely. |
| `pyproject.toml` | Single configuration file for the project and for every tool that can be configured there. | — |
| `.python-version` | Pins the interpreter uv provisions locally: 3.12, the lowest supported version. | uv provisions it automatically on `uv run` and `uv sync`. |
| `uv.lock` | The exact resolved dependency set, tracked in git and reviewed as a diff. | Enforced in CI. |
| `hatchling` | PEP 517 backend that makes `src/python_prj_seed/` an installable package. | — |

### Rules

- Supported versions: Python 3.12 and above, per SPEC 0. The CI matrix covers
  3.12, 3.13 and 3.14. `requires-python` carries no upper bound.
- Development happens on the floor version, so incompatibilities fail locally
  rather than in CI.
- Layout is src-layout: `src/python_prj_seed/` for code, `tests/` for tests. The
  package is installed editable; nothing is importable from the repository root.
- Python development tools are installed with `uv add --dev`, so they are pinned
  in the lockfile and CI runs the same versions. Only non-Python binaries are
  installed outside the project.
- All tool configuration lives in `pyproject.toml`. A tool gets its own file only
  when it cannot read `pyproject.toml`.

**Decisions:** [ADR-0003](adr/0003-use-src-layout-as-a-packaged-application.md) ·
[ADR-0004](adr/0004-use-hatchling-as-build-backend.md) ·
[ADR-0005](adr/0005-commit-the-uv-lockfile.md) ·
[ADR-0006](adr/0006-python-version-policy.md)
