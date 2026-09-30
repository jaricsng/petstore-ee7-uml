# ADR-0006: Jakarta Security with OIDC and role-based access

| Status | Date | Deciders |
|---|---|---|
| Proposed | 2026-09-25 | Architecture review (PetStore EE7 UML project) |

## Context and problem statement

Authentication is bypassed (SEC-01), admin and REST are unprotected (SEC-02), password hashing is weak (SEC-03), logout keeps the session (SEC-07), and default credentials are shown on the sign-in page (SEC-08).

## Decision drivers

* OWASP ASVS 5.0 Level 2 (authentication, session management, access control)
* Standard API; no custom crypto
* SSO-ready for staff (administrators)

## Considered options

1. Jakarta Security 3 `@OpenIdAuthenticationMechanismDefinition` against an external IdP (Keycloak / Entra ID), with roles `CUSTOMER` and `ADMIN`.
2. Jakarta Security `@FormAuthenticationMechanismDefinition` plus a custom `IdentityStore` using `Pbkdf2PasswordHash`.
3. Fix the JAAS module.

## Decision outcome

Chosen: option 1 for administrators (MFA enforced at the IdP) and option 2 for customers until they are migrated to the IdP. Protect `/admin/*` and `/api/v1/*` (write operations) with `@RolesAllowed` and web.xml constraints. Call `HttpServletRequest.logout()` and `session.invalidate()` at sign-out, and change the session ID at sign-in.

### Consequences

* Good: closes SEC-01/02/03/07/08; rehashes passwords at next login.
* Bad: requires migrating to Jakarta EE 10 (ADR-0008); an IdP to operate.

---
[Back to architecture description](../README.md#12-architecture-decision-records)
