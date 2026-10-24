# 12. Build the CLI on argparse, behind a domain/delivery boundary

- Status: accepted
- Date: 2026-10-24

## Context

The seed needs an entry point that shows the intended structure: where the
application logic lives, where input and output happen, and how both are
tested. The command itself is a placeholder each project replaces, so the
choices that matter are the structure and the library it is built on.

## Decision

- `python_prj_seed.domain` holds application logic. It never parses arguments,
  prints or exits.
- `python_prj_seed.cli` is the delivery layer: `main(argv) -> int` parses
  arguments with the standard library's `argparse`, calls the domain, prints,
  and returns the exit code. `argv` is injectable so tests call `main` directly.
- The console script and `python -m python_prj_seed` both go through
  `cli.main`.

## Alternatives considered

- **Typer or Click.** The common choice for larger CLIs: less boilerplate for
  subcommands, typed options and richer help. Rejected for the seed: they add a
  runtime dependency to every project built from it, including those that need
  no CLI beyond a single command. A project that outgrows argparse adopts one
  of them inside `cli`, without touching the domain.
- **Logic directly in `main`.** Simpler for one function. Rejected: the seed's
  point is the shape that scales, and logic tangled with I/O can only be tested
  by capturing output.

## Consequences

- The package has no runtime dependencies.
- The domain is tested with plain function calls; only the CLI tests capture
  output or exit codes.
- The boundary is a convention, not an enforced rule: nothing yet stops
  `domain` from importing `cli`. A tool such as import-linter can enforce it if
  the code base grows enough to need it.
