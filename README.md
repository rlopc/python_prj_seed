# Python Project Seed

A starting point for Python applications with a production toolchain already
in place: uv, strict typing, full test coverage, linting, a single check
command, CI, automatic versioning and pre-commit hooks. Every choice is
documented, with the alternatives that were rejected.

## Scope

This seed is for Python **applications** (CLIs, services, scripts) — never
for libraries published to PyPI. It deliberately omits distribution concerns:
no wheel publishing, no multi-version support promises to consumers.

## What is included

| Concern | Tooling |
| --- | --- |
| Environment and dependencies | uv, a tracked `uv.lock`, Python 3.14 |
| Static typing | mypy in strict mode |
| Tests | pytest, 100% branch coverage |
| Lint and format | Ruff |
| Single check command | `just verify` |
| Continuous integration | GitHub Actions, Dependabot |
| Versioning and changelog | python-semantic-release, from Conventional Commits |
| Local checks | pre-commit hooks |

[`docs/engineering-standards.md`](docs/engineering-standards.md) describes each
of these: what it solves, which gate it imposes, and the rules that apply. The
decisions behind them are recorded as ADRs in [`docs/adr/`](docs/adr/).

## Requirements

[uv](https://docs.astral.sh/uv/) is the only prerequisite. It installs the
Python version in `.python-version` and every development tool, including
`just`, at the versions pinned in `uv.lock`.

## Getting started

```sh
uv sync                     # create the environment
uv run pre-commit install   # install the git hooks, once per clone
uv run just verify          # run every check, as CI does
uv run python-prj-seed Ada  # run the application
```

`uv run just` lists the available tasks; `uv run just fix` applies formatting
and safe lint fixes.

## Starting a new project from this seed

1. Copy the repository without its history, so the new project starts its own
   versioning from scratch: for example, download it as an archive, or create
   a fresh repository and copy the files in.
2. Rename the project. Every place the name appears is listed by:

   ```sh
   git grep -n -e python_prj_seed -e python-prj-seed -- ':!uv.lock'
   ```

   That covers the `src/python_prj_seed/` directory, `project.name` and the
   console script in `pyproject.toml`, `source_pkgs` for coverage, the imports
   in `src/` and `tests/`, and the references in the engineering standards.
   ADRs mention the name only as history; leave them as they are.
3. Update `description` and `authors` in `pyproject.toml`, and the copyright
   holder in `LICENSE` (or replace the licence; see ADR-0002).
4. Replace this README with one for the new project.
5. Run `uv lock` and `uv run just fix` (a name of a different length can change
   how the formatter wraps lines), then `uv run just verify`. It must pass
   before the first commit.

`version` stays at `0.1.0`: the release job owns it from the first push to
`main` onwards.

## Project layout

```text
src/python_prj_seed/
  domain.py       application logic, free of I/O
  cli.py          command-line entry point
  __main__.py     support for `python -m python_prj_seed`
tests/            pytest suite, run against the installed package
docs/
  engineering-standards.md
  adr/            architecture decision records
justfile          tasks: verify, fix
pyproject.toml    project metadata and all tool configuration
```

## License

[MIT](LICENSE)
