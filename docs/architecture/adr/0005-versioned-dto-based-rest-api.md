# ADR-0005: Versioned, DTO-based REST API

| Status | Date | Deciders |
|---|---|---|
| Proposed | 2026-09-25 | Architecture review (PetStore EE7 UML project) |

## Context and problem statement

The `/rest/*` endpoints serialise JPA entities directly, which leaks `Customer.password` (SEC-04). They have no versioning, pagination metadata, error model, or authentication. They also bypass the session facades (ARCH-02).

## Decision drivers

* Stable public contract, independent of the persistence model
* Industry conventions: RFC 9110 semantics, RFC 9457 problem details, OpenAPI 3.1
* Least-privilege data exposure (OWASP API3:2023 Broken Object Property Level Authorization)

## Considered options

1. Keep the entity-based API.
2. Introduce `/api/v1` with request/response DTOs mapped by MapStruct, delegating to the session facades.
3. GraphQL.

## Decision outcome

Chosen option 2. See the proposed contract [`../../api/openapi-v1.yaml`](../../api/openapi-v1.yaml) and the [API design review](../../api/README.md).

### Consequences

* Good: closes SEC-04 and ARCH-02; the contract can be tested (contract tests).
* Bad: mapping code to write and maintain; `/rest` must be deprecated with a `Sunset` header (RFC 8594).

---
[Back to architecture description](../README.md#12-architecture-decision-records)
