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
| `.editorconfig` | Gives every editor the same charset, indentation and final-newline rules before any formatter exists. Covers what Ruff does not format: YAML, JSON, and Markdown prose (Ruff formats only the Python code blocks inside Markdown). | None. Prevention only. Ruff enforces Python formatting from section 5 onwards. |
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
| `uv` | Resolves dependencies, provisions the interpreter, owns the virtual environment, and runs commands inside it via `uv run`. | `uv sync --locked` fails when `uv.lock` is out of date with respect to `pyproject.toml`. Not `--frozen`, which skips that check entirely. CI also sets `UV_LOCKED=1`, because a plain `uv run` re-locks a stale lockfile silently. |
| `pyproject.toml` | Single configuration file for the project and for every tool that can be configured there. | — |
| `.python-version` | Pins the interpreter uv provisions locally: 3.14, the single target version. | uv provisions it automatically on `uv run` and `uv sync`. |
| `uv.lock` | The exact resolved dependency set, tracked in git and reviewed as a diff. | Enforced in CI. |
| `hatchling` | PEP 517 backend that makes `src/python_prj_seed/` an installable package. | — |

### Rules

- One target version, Python 3.14, used for development, CI and deployment: the
  newest minor that has been out for at least a year. It moves up one minor
  every October. `requires-python = ">=3.14"` carries no upper bound.
- Layout is src-layout: `src/python_prj_seed/` for code, `tests/` for tests. The
  package is installed editable; nothing is importable from the repository root.
- Development tools are installed with `uv add --dev` whenever they are
  published on PyPI, whatever language they are written in, so they are pinned
  in the lockfile and CI runs the same versions. Only tools not on PyPI are
  installed outside the project.
- `uv.lock` is tracked: an application has exactly one dependency set, and CI
  must reproduce it. Lockfile conflicts are resolved by re-running `uv lock`,
  never by editing the file by hand.
- All tool configuration lives in `pyproject.toml`. A tool gets its own file only
  when it cannot read `pyproject.toml`.

**Decisions:** [ADR-0003](adr/0003-use-src-layout-as-a-packaged-application.md) ·
[ADR-0004](adr/0004-use-hatchling-as-build-backend.md) ·
[ADR-0007](adr/0007-target-a-single-python-version.md)

## 3. Static typing

**Concern:** catching type errors before the code runs, and keeping every
signature in the codebase annotated.

| Tool | What it solves | Gate |
| --- | --- | --- |
| `mypy` | Checks the annotations of `src/` against the code that uses them, in strict mode: every function annotated, no calls into untyped code. | `uv run mypy` exits non-zero on any error. |

### Rules

- mypy runs with `strict = true`. Individual checks are never relaxed globally;
  a justified exception is a line-level `# type: ignore[code]` with a comment.
- `python_version` is set explicitly and must match `.python-version`, because
  mypy does not read `requires-python`.
- The paths to check live in `[tool.mypy] files`, so a bare `uv run mypy` is the
  only command anyone needs.

**Decisions:** [ADR-0008](adr/0008-type-check-with-mypy-in-strict-mode.md)

## 4. Tests and coverage

**Concern:** proving the code behaves as intended, and making untested code
visible.

| Tool | What it solves | Gate |
| --- | --- | --- |
| `pytest` | Discovers and runs the tests under `tests/`, against the installed package. | Exits non-zero on any failing test, unregistered marker, invalid configuration, or warning. |
| `pytest-cov` (`coverage.py`) | Measures which lines and branches of `python_prj_seed` the tests executed. | `uv run pytest --cov` fails below 100% branch coverage. |

### Rules

- Tests live in `tests/`, outside the package, with no `__init__.py`. pytest
  runs in `importlib` import mode, so tests can only reach the installed code.
- `strict = true` turns every pytest strictness option on, and
  `filterwarnings = ["error"]` turns warnings into failures: a deprecation is
  fixed when it appears, not when it becomes a break.
- Tests are type-checked like the rest of the code.
- Code left untested on purpose is excluded explicitly, with a reason.
  Coverage is never lowered to make room for it.

**Decisions:** [ADR-0009](adr/0009-require-full-branch-coverage.md)

## 5. Lint and format

**Concern:** one formatting style for every Python file, and catching
bug-prone, insecure or outdated code before review.

| Tool | What it solves | Gate |
| --- | --- | --- |
| `ruff format` | Formats Python files, and Python code blocks in Markdown, in a single fixed style. | `uv run ruff format --check` fails on any file it would change. |
| `ruff check` | Lints against Ruff's default rule set plus the flake8-bandit security rules (`S`). | `uv run ruff check` fails on any violation. |

### Rules

- The formatter runs with its defaults. Style is not debated in review.
- Ruff's default rule set is extended, never replaced and never widened to
  `"ALL"`. Adding a family to `extend-select` is a deliberate change.
- A rule is ignored per file, in `per-file-ignores`, with a comment; a single
  line takes `# noqa: CODE`. Rules are never ignored globally.
- Ruff targets the version in `requires-python`, so `UP` rules modernize the
  code for 3.14 with no extra setting.

**Decisions:** [ADR-0010](adr/0010-lint-and-format-with-ruff.md)

## 6. Task runner

**Concern:** one command that runs every check, identical on a laptop and in CI.

| Tool / file | What it solves | Gate |
| --- | --- | --- |
| `just` (`rust-just`) | Runs the named recipes in `justfile`. Installed from PyPI as `rust-just`, the distribution just's own README lists, so the lockfile pins it. | — |
| `justfile` | Defines `verify`, the full check suite, and `fix`, which applies formatting and safe lint fixes. | `uv run just verify` fails if any check fails. |

### Rules

- `uv run just verify` is the gate before every commit, and the command CI runs.
  A check that is not in `verify` is not enforced.
- Recipes call tools through `uv run`, so they work without an activated
  environment.
- Locally, `uv run` re-locks a stale lockfile instead of failing; the change
  then shows up in `git status`. CI does not allow that: see section 2.

**Decisions:** [ADR-0011](adr/0011-run-tasks-with-just.md)
