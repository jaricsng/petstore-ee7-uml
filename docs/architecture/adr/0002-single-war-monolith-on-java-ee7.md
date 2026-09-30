# ADR-0002: Single WAR monolith on Java EE 7

| Status | Date | Deciders |
|---|---|---|
| Accepted (retrospective) | 2013 (original); recorded 2026-09-25 | Architecture review (PetStore EE7 UML project) |

## Context and problem statement

The application exists to demonstrate how the Java EE 7 specifications work together with no external frameworks.

## Decision drivers

* Simplicity for learners
* Only standard APIs
* Deploys to any Java EE 7 server

## Considered options

1. One WAR containing UI, REST, services and persistence.
2. Separate EAR modules (web, EJB, persistence).
3. Microservices.

## Decision outcome

Chosen option 1: a single WAR (EJB Lite in WAR) keeps the build to one Maven module and the deployment to one artifact.

### Consequences

* Good: simple to build, deploy and read.
* Bad: no enforced module boundaries, so layering violations appeared (ARCH-01/02); scaling is all-or-nothing; tied to end-of-life Java EE 7.
* Follow-up: enforce module boundaries with ArchUnit (modular monolith); see ADR-0008.

---
[Back to architecture description](../README.md#12-architecture-decision-records)
