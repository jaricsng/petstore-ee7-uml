# ADR-0001: Record architecture decisions

| Status | Date | Deciders |
|---|---|---|
| Accepted | 2026-09-25 | Architecture review (PetStore EE7 UML project) |

## Context and problem statement

Decisions about PetStore were implicit in code and comments. Students and maintainers cannot see *why* the architecture looks the way it does.

## Decision drivers

* Traceable rationale for teaching and review
* Low ceremony; lives next to the code and is reviewed in pull requests

## Considered options

1. Use lightweight ADRs in MADR 3 format, stored in `docs/architecture/adr/`, one file per decision, numbered sequentially.
2. Wiki pages.
3. No records.

## Decision outcome

Chosen option 1: ADRs are Markdown, versioned with the code, and reviewed in the same pull request as the change.

### Consequences

* Good: history of decisions is diff-able and reviewable.
* Bad: must be maintained; the pull-request template gains a checklist item "ADR needed?".

---
[Back to architecture description](../README.md#12-architecture-decision-records)
