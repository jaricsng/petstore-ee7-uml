# ADR-0008: Migrate to Jakarta EE 10, PostgreSQL and Flyway

| Status | Date | Deciders |
|---|---|---|
| Proposed | 2026-09-25 | Architecture review (PetStore EE7 UML project) |

## Context and problem statement

Java EE 7 (`javax.*`) is end of life; WildFly 27 and later do not support it. H2 in memory with `drop-and-create` loses all data on restart (OPS-01). jQuery 2.2.4 and Bootstrap 3.3.7 have known CVEs (DEP-01).

## Decision drivers

* Supported platform, security patches
* Durable data with repeatable schema migrations
* Minimal functional change

## Considered options

1. Jakarta EE 10 + Java 21 (OpenRewrite `javax`→`jakarta` recipes), PostgreSQL 16, Flyway migrations, Bootstrap 5.
2. Rewrite on Spring Boot.
3. Stay on Java EE 7.

## Decision outcome

Chosen option 1: the smallest change that restores support while keeping the teaching goal (standard APIs).

### Consequences

* Good: security updates, modern language features, production-grade persistence.
* Bad: the UI must move from Bootstrap 3 to 5; PrimeFaces must be upgraded to the Jakarta variant.

---
[Back to architecture description](../README.md#12-architecture-decision-records)
