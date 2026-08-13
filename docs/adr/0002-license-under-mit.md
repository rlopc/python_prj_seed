# 2. License the project under MIT

- Status: accepted
- Date: 2026-08-13

## Context

The repository will be public on GitHub and is intended to be copied as the
starting point of other projects. Whoever copies it must be able to tell, without
asking, that they may use, modify and relicense the result. A repository with no
licence defaults to "all rights reserved", which would make the seed unusable for
its stated purpose.

## Decision

License the repository under the MIT License.

## Alternatives considered

- **Apache-2.0.** Rejected: its explicit patent grant and NOTICE obligations earn
  their weight in projects shipping patentable implementations. This repository
  ships scaffolding, so those obligations would be inherited by every derived
  project for no corresponding benefit.
- **GPL-3.0.** Rejected: copyleft would propagate into every project started from
  the seed, and that is a choice each derived project must remain free to make.
- **No licence at all.** Rejected: defaults to all rights reserved, contradicting
  the purpose of a seed.

## Consequences

- Anyone may copy the seed, including into closed-source projects.
- Derived projects pick their own licence; nothing here forces MIT downstream.
- The copyright line must be kept accurate as contributors are added.
