# ADR-0007: Delegate card handling to a payment service provider

| Status | Date | Deciders |
|---|---|---|
| Proposed | 2026-09-25 | Architecture review (PetStore EE7 UML project) |

## Context and problem statement

The application stores the full card number, type and expiry date in `purchase_order` (SEC-05). It never authorises a payment.

## Decision drivers

* PCI DSS v4.0.1 scope reduction (Requirements 3 and 4)
* Real payment authorisation

## Considered options

1. Hosted payment fields / checkout from a PSP; store only the PSP token and the last 4 digits.
2. Encrypt the PAN in the database (still full PCI DSS scope).
3. Keep as is.

## Decision outcome

Chosen option 1, behind a `PaymentGateway` port with a PSP adapter and a fake adapter for tests (Ports and Adapters; see UML pattern 29).

### Consequences

* Good: the card number never reaches PetStore servers (SAQ A eligibility).
* Bad: external dependency and fees; the checkout flow must handle asynchronous payment results.

---
[Back to architecture description](../README.md#12-architecture-decision-records)
