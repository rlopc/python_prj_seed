# Engineering Standards

This document is the single reference for how this repository is built, checked
and released. Each section covers one concern: the tools involved, what each of
them solves, and which gate it imposes. A new concern gets a new section.

Decisions that had a defensible alternative are recorded separately as ADRs under
[`docs/adr/`](adr/), written when the decision is taken. An accepted ADR is not
rewritten: a changed decision gets a new ADR, and the old one is kept with its
status pointing to its successor.

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

## 7. Command-line interface

**Concern:** how the application is invoked, and where its logic lives relative
to its input and output.

| Module | What it solves | Gate |
| --- | --- | --- |
| `python_prj_seed.domain` | Application logic, free of I/O. | Covered by the test suite like any other code. |
| `python_prj_seed.cli` | Parses arguments with `argparse`, calls the domain, prints, and returns the exit code. | The console script `python-prj-seed` and `python -m python_prj_seed` both run `cli.main`. |

### Rules

- The domain never reads arguments, prints, or exits; the CLI holds no logic
  beyond translating between the command line and the domain.
- `main(argv: Sequence[str] | None = None) -> int`. Tests pass `argv`
  explicitly. `main` returns the exit code; only argparse itself exits, for
  `--help`, `--version` and usage errors.
- CLI output is in English.

**Decisions:** [ADR-0012](adr/0012-build-the-cli-on-argparse.md)

## 8. Continuous integration

**Concern:** running the gate on every change, on a clean machine, and keeping
the tools it depends on up to date.

| File | What it solves | Gate |
| --- | --- | --- |
| `.github/workflows/ci.yml` | Runs `uv sync --locked` and `uv run just verify` on every push to `main` and every pull request. | A red `Verify` job blocks the merge. |
| `.github/dependabot.yml` | Opens weekly pull requests to update GitHub Actions and the uv lockfile. | Each update goes through the same CI as any other change. |

### Rules

- CI runs exactly `just verify`, nothing more: what passes locally passes in CI.
- `UV_LOCKED=1` is set for the whole workflow; see section 2.
- Third-party actions are pinned to a full commit SHA, with the version tag in a
  comment. A tag can be moved to point at different code; a SHA cannot.
- The workflow token is read-only (`permissions: contents: read`) and checkout
  does not persist credentials.
- Dependabot waits seven days before proposing a new release, so a broken or
  compromised one is likely to be yanked first.
- The uv version CI installs is pinned in the workflow. Dependabot does not
  track it, so it is bumped by hand.

## 9. Versioning and changelog

**Concern:** who sets the version, when, and where each release's changes are
recorded.

| Tool / file | What it solves | Gate |
| --- | --- | --- |
| `python-semantic-release` | Derives the next version from the Conventional Commits since the last tag, and writes `project.version`, `uv.lock` and `CHANGELOG.md`. | Runs in CI as the `Release` job, only after `Verify` passes on `main`. |
| `CHANGELOG.md` | The human-readable list of changes per release. | Generated; never edited by hand. Created by the first release. |

### Rules

- `project.version` is written only by the release job. It is never edited by
  hand.
- `feat:` bumps the minor version and `fix:` or `perf:` the patch. A breaking
  change (`!` or a `BREAKING CHANGE:` footer) bumps the minor while on 0.x.
- Releases are `v<version>` tags plus a changelog entry. Nothing is published,
  and no GitHub Release is created.
- To preview the next version locally, without changing anything:
  `uv run --group release semantic-release --noop version --print`.

**Decisions:** [ADR-0013](adr/0013-version-with-python-semantic-release.md)

## 10. Pre-commit hooks

**Concern:** catching the most common failures on the contributor's machine,
before a commit exists, instead of minutes later in CI.

| Tool / file | What it solves | Gate |
| --- | --- | --- |
| `pre-commit` (with `pre-commit-uv`) | Runs the hooks in `.pre-commit-config.yaml` on the staged files of every commit. `pre-commit-uv` makes it build hook environments with uv. | The commit is refused if a hook fails or changes a file. |
| `.pre-commit-config.yaml` | File hygiene (large files, merge markers, TOML/YAML syntax, private keys, final newlines, trailing whitespace), Ruff, and the Conventional Commits check on the commit message. | — |

### Rules

- Hooks are installed once per clone: `uv run pre-commit install`. The config
  installs both the `pre-commit` and `commit-msg` hooks.
- Hooks are a fast subset of `just verify`, never a replacement: mypy and the
  tests run only in `verify`. CI does not run pre-commit.
- Ruff runs as a local hook through `uv run`, so its version comes from
  `uv.lock`. Third-party hook repositories are pinned to a commit SHA
  (`pre-commit autoupdate --freeze`) and updated by Dependabot.
- Commit messages that are not Conventional Commits are rejected locally,
  because the release job (section 9) derives versions from them.
