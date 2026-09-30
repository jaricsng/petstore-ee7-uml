# ADR-0004: Authentication with a custom JAAS LoginModule

| Status | Date | Deciders |
|---|---|---|
| Superseded by ADR-0006 | 2013 (original); recorded 2026-09-25 | Architecture review (PetStore EE7 UML project) |

## Context and problem statement

Customers must sign in before they can check out.

## Decision drivers

* Standard API available in Java SE / EE 7
* Reuse CustomerService for credential lookup

## Considered options

1. Custom JAAS `LoginModule` driven by a CDI-produced `LoginContext`.
2. Container-managed security (web.xml security-constraint + server realm).
3. Home-grown session flag only.

## Decision outcome

Option 1 was designed, but the call to `loginContext.login()` is commented out. In practice the system runs option 3, a session flag set without checking the password (SEC-01).

### Consequences

* Bad: authentication bypass (SEC-01), no authorisation (SEC-02), JNDI lookup inside the LoginModule (Service Locator), password comparison can never match the stored digest.
* Superseded by ADR-0006.

---
[Back to architecture description](../README.md#12-architecture-decision-records)
