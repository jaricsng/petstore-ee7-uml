# ADR-0003: Server-side UI with JSF Facelets

| Status | Date | Deciders |
|---|---|---|
| Accepted (retrospective) | 2013 (original); recorded 2026-09-25 | Architecture review (PetStore EE7 UML project) |

## Context and problem statement

A UI technology had to be chosen that is part of Java EE 7.

## Decision drivers

* Must be a standard API
* Component model and i18n support
* Low JavaScript skill requirement for students

## Considered options

1. JSF 2.2 Facelets with PrimeFaces and Bootstrap.
2. JAX-RS with a JavaScript SPA (Angular or React).
3. MVC 1.0 (JSR 371, not final in EE 7).

## Decision outcome

Chosen option 1: JSF is the standard component framework in Java EE 7.

### Consequences

* Good: server-side validation and i18n are built in; ViewState gives some CSRF protection on postbacks.
* Bad: stateful views; accessibility depends on hand-written markup; the image-map home page and tables need work (see the UX review).

---
[Back to architecture description](../README.md#12-architecture-decision-records)
