# PetStore EE7 — Design Documentation

Documentation for `agoncal-application-petstore-ee7`, kept as code: every diagram is text (PlantUML), every page is
Markdown, and one command renders and verifies the whole set.

| Area | What you will find | Standards |
|---|---|---|
| [UML model](uml/README.md) | All 14 UML 2.5.1 diagram kinds (37 diagrams), design-pattern catalogue including target-state patterns, a Markdown page per diagram with its PlantUML source | OMG UML 2.5.1 |
| [Architecture](architecture/README.md) | C4 context, container, component and deployment views (current and target); layering rules; architectural pattern review; quality scenarios; risks; 8 ADRs | arc42, C4, ISO/IEC/IEEE 42010, ISO/IEC 25010, MADR |
| [Interface design (UX)](ux/README.md) | Site map, screen flow, 13 as-built wireframes, 1 proposed checkout, UI review findings, interface design guidelines | WCAG 2.2 AA, ISO 9241-110, Nielsen heuristics |
| [REST interface (API)](api/README.md) | Review of `/rest` against conventions; proposed OpenAPI 3.1 contract for `/api/v1` | RFC 9110, RFC 9457, OWASP API Top 10 2023 |
| [Testing](testing/README.md) | Test strategy and architecture; 65 traceable test cases (unit, integration, API, E2E, accessibility, security, governance, audit, performance) plus CSV | ISO/IEC/IEEE 29119-3, OWASP WSTG/ASVS, WCAG |

## Traceability chain

```
Use case (UML 10a/10b, UC01..UC21)
  -> Screen (UX WF-xx)            -> Interaction (UML 13x/14/15)      -> Component (C4 L3)
  -> Finding (SEC/BUG/UX/ARCH)    -> Decision (ADR-000x)              -> Target pattern (UML 29)
  -> Test case (TC-xxx-nn)        -> CI gate (testing/README.md)
```

## Regenerate and verify

```bash
export PLANTUML_JAR=~/.local/lib/plantuml.jar   # PlantUML 1.2025.4 or later
./docs/render.sh           # render all diagrams, regenerate generated pages, verify
./docs/render.sh --check   # verify only (use in CI and pre-commit)
```

The check fails on any of the following:
- a PlantUML syntax error;
- a UML frame heading that does not follow Annex A;
- an unresolved cross-diagram reference;
- stale generated pages (UML pages or the test catalogue);
- a missing rendered image, or a rendered image that no page uses;
- a broken Markdown link or anchor;
- an invalid OpenAPI contract.

CI runs the same check on every pull request: see [`.github/workflows/docs.yml`](../.github/workflows/docs.yml). Locally, the
`docs-check` hook in [`.pre-commit-config.yaml`](../.pre-commit-config.yaml) runs it when files under `docs/` are staged.

## Licence

Derived from work by Antonio Goncalves licensed under CC BY-SA 3.0; this documentation is distributed under the same
licence. UML is a registered trademark of the Object Management Group. C4-PlantUML is MIT-licensed.
