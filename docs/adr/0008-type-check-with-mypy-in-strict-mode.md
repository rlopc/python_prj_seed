# 8. Type-check with mypy in strict mode

- Status: accepted
- Date: 2026-10-24

## Context

Every application built from this seed is fully annotated from its first line,
so the type checker can start at its strictest setting and never has to be
tightened later. As of 2026-10-24 four checkers are credible, with versions as
published on PyPI:

- mypy 2.4.0: the reference implementation, maintained under the `python`
  GitHub organization, and the only one with a plugin interface.
- pyright 1.1.414 and its fork basedpyright 1.40.2: high conformance to the
  typing specification and fast, but run on Node.js.
- Pyrefly 1.4.0 (Meta): stable since 1.0.0 in May 2026, fast, with a `strict`
  preset.
- ty 0.0.91 (Astral): still marked beta.

## Decision

Use mypy with `strict = true`, configured in `pyproject.toml` and installed as a
development dependency.

## Alternatives considered

- **basedpyright in strict mode.** The strongest alternative: higher conformance
  to the typing specification, faster, and a fork of pyright, the engine behind
  VS Code's Pylance. Rejected because it has no plugin interface: Django's type support depends on
  the django-stubs mypy plugin, and Pydantic also ships one. Its conformance
  advantage matters most for library-style typing, less for application code.
- **Pyrefly.** Rejected for now: five months of stable releases is a short
  record to build every future project on, and its Django support is partial.
  Worth re-evaluating once it has a longer track record.
- **ty.** Rejected: pre-1.0 and marked beta.

## Consequences

- Every function needs full annotations, calls into untyped code are errors,
  and generics must be parameterized. That is the intended effect.
- mypy is the slowest of the four. Parallel checking (`--num-workers`) is
  available if check time ever becomes a problem.
- Conformance is mypy's weak point: some valid typing constructs may be rejected
  or need a workaround. If that happens often, revisit this decision.
- mypy does not read `requires-python`, so `python_version` is set explicitly.
  See ADR-0007.
