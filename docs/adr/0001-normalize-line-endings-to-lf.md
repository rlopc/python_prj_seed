# 1. Normalize line endings to LF

- Status: accepted
- Date: 2026-08-13

## Context

Git can store a file's line endings verbatim or normalize them on commit. Left
unconfigured, the outcome depends on each contributor's `core.autocrlf`, so a
single-line edit made on Windows can rewrite a whole file as CRLF. Mixed endings
produce diffs in which every line appears changed, break formatter checks and
shell scripts, and are expensive to correct afterwards: the fix is one commit
touching every file, which invalidates `git blame`.

This repository is a seed meant to be copied, so the setting is inherited by
every project derived from it.

## Decision

Ship a `.gitattributes` with `* text=auto eol=lf` in the first setup commit, and
run `git add --renormalize .` so files committed earlier are brought in line.
Binary extensions are marked `binary` so Git never normalizes or text-diffs them.

## Alternatives considered

- **Rely on each contributor's `core.autocrlf`.** Rejected: it is per-machine
  configuration, invisible in the repository and impossible to review or enforce.
- **`* text=auto` without `eol=lf`.** Rejected: it normalizes the repository to
  LF but checks out CRLF on Windows, so tools that read the working tree
  (formatters, generated snapshots) can disagree with what Git stores.

## Consequences

- Diffs stay minimal and `git blame` stays meaningful.
- Windows contributors get LF in their working tree; editors handle this, and
  `.editorconfig` restates the same rule for tools that ignore Git config.
- The decision is effectively permanent: reverting it would require exactly the
  repository-wide rewrite it exists to avoid.
