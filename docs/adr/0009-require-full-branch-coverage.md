# 9. Require 100% branch coverage

- Status: accepted
- Date: 2026-10-24

## Context

A coverage threshold only works as a gate if it is set before the code exists.
Raised later, it meets a backlog of untested code; set below 100%, it lets any
new line go untested as long as the total stays above the bar, so the gap it
tolerates is never the same code twice.

This seed starts with almost no code, which makes the strictest setting cheap
to adopt now and expensive to adopt at any later point.

## Decision

Measure branch coverage over the installed `python_prj_seed` package and fail
the test run below 100% (`fail_under = 100`). Code that is deliberately left
untested is excluded explicitly, with a `# pragma: no cover` and a reason, or
with an `exclude_also` pattern for a recurring idiom.

## Alternatives considered

- **A lower threshold, such as 80% or 90%.** The common choice, and a fair
  one for a codebase that already exists. Rejected here: it decides nothing
  about which code is tested, and it leaves no record of what was skipped.
- **No threshold, coverage as a report only.** Rejected: a number no gate
  enforces erodes without anyone deciding it should.

## Consequences

- Every untested line or branch is either a failing build or a visible,
  reviewable exclusion.
- 100% coverage proves every line ran, not that the assertions are good. It is
  a floor for test quality, not a measure of it.
- Exclusions can be abused to reach the number. They show up in review as
  diffs, which is where they are kept honest.
