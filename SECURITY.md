# Security Policy

## Status of this code base

This repository is a **teaching and documentation** adaptation of a Java EE 7 sample application. It is **not
intended for production use**. The design documentation records known, unfixed vulnerabilities on purpose so they can
be studied and remediated test-first. See [`docs/uml/README.md`, section 3](docs/uml/README.md#3-findings-raised-while-reverse-engineering-the-code)
and [`docs/architecture/README.md`, section 11](docs/architecture/README.md#11-risks-and-technical-debt).

Known findings (SEC-01 to SEC-08, DEP-01) are tracked there and do not need to be reported again.

## Supported versions

| Version | Supported |
|---|---|
| `main` (latest) | Yes |
| Tagged releases | Latest release only |
| `upstream-725839c` baseline | No (reference only) |

## Reporting a vulnerability

Report **new** vulnerabilities privately through
[GitHub private vulnerability reporting](https://github.com/jaricsng/petstore-ee7-uml/security/advisories/new).
Do not open a public issue or pull request.

Please include:
- a description of the issue and its impact;
- steps to reproduce, or a proof of concept;
- the affected commit or version.

You can expect an acknowledgement within **5 working days** and a triage decision within **10 working days**.
Accepted issues are fixed on `main` and credited in the advisory unless you ask to stay anonymous.

## Scope

In scope: the application source, build configuration, CI workflows and documentation tooling in this repository.
Out of scope: vulnerabilities in WildFly, the JDK, browsers or third-party libraries themselves. Report those to the
respective projects. Dependabot and dependency review track known CVEs in dependencies.
