# Contributing

Thank you for helping improve this repository. It is used for teaching software design, so changes to the code and
to the design documentation go together.

## Workflow

1. Open or pick an issue, then create a branch from `main`:
   `feat/<topic>`, `fix/<topic>`, `docs/<topic>`, `chore/<topic>` or `ci/<topic>`.
2. Keep `main` protected: every change goes through a pull request, and CI must pass.
3. Pull and rebase before opening or updating a PR: `git fetch origin && git rebase origin/main`.
4. Merge with **Rebase and merge** (or **Squash and merge** for noisy branches). History on `main` stays linear.

## Commits

- Follow [Conventional Commits](https://www.conventionalcommits.org/): `feat:`, `fix:`, `docs:`, `test:`,
  `build:`, `ci:`, `chore:`, `refactor:`. Add `!` or a `BREAKING CHANGE:` footer for breaking changes.
- Sign off every commit (`git commit -s`) to certify the [Developer Certificate of Origin](https://developercertificate.org/).
- One logical change per commit.

## Local setup

```bash
# Hooks: formatting checks, secret scanning, docs check on staged docs
pipx install pre-commit          # or: pip install pre-commit
pre-commit install --hook-type pre-commit --hook-type commit-msg

# Documentation tooling (see docs/README.md)
export PLANTUML_JAR=~/.local/lib/plantuml.jar   # PlantUML 1.2025.4, plus Graphviz and Java 11+
./docs/render.sh           # render diagrams and regenerate generated pages
./docs/render.sh --check   # verify only

# Application
mvn -B verify              # build and unit tests (JDK 8)
```

## Definition of done

- Tests cover the change at the right level (see [`docs/testing/README.md`](docs/testing/README.md)). A fix for a
  known finding starts with a failing test tagged with the finding ID.
- UML diagrams, ADRs, API contract and test catalogue are updated in the same PR when behaviour or structure changes.
  Generated pages are never edited by hand.
- `./docs/render.sh --check` passes; CI is green.
- No secrets or personal data. Test data uses obviously fake values.

## Versioning and releases

- [Semantic Versioning](https://semver.org/). Tags are `vMAJOR.MINOR.PATCH` and are protected.
- Record user-visible changes in [`CHANGELOG.md`](CHANGELOG.md) under *Unreleased*.
- Release: move *Unreleased* entries to a new version heading, merge, then tag `main`
  (`git tag -a v0.2.0 -m "v0.2.0" && git push origin v0.2.0`) and create a GitHub release.

## Licence

By contributing you agree that your contribution is licensed under CC BY-SA 3.0, the licence of this repository
(see [`LICENSE`](LICENSE) and [`NOTICE`](NOTICE)). Only add third-party code or assets whose licence is compatible
with that, and record their attribution in `NOTICE`.

## Security

Report vulnerabilities privately as described in [`SECURITY.md`](SECURITY.md).
