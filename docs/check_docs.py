#!/usr/bin/env python3
"""
Documentation integrity check for docs/ (runs in docs/render.sh and CI).

Fails (exit 1) when:
  * a PlantUML source under docs/<area>/src has no rendered PNG and SVG;
  * a rendered diagram of an area is not referenced by any Markdown file (orphan);
  * a relative Markdown link or image points to a file that does not exist;
  * a link anchor (#section) does not match a heading in the target Markdown file (GitHub slug rules);
  * the proposed OpenAPI contract is invalid (when openapi-spec-validator is installed).
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

DOCS = Path(__file__).resolve().parent
AREAS = ["architecture", "ux", "api", "testing"]
LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)\)")
HEADING_RE = re.compile(r"^#{1,6}\s+(.*)$", re.M)


def slug(h: str) -> str:
    h = re.sub(r"<[^>]+>", "", h).strip().lower()
    h = re.sub(r"[`*_~]", "", h)
    h = re.sub(r"[^\w\- ]", "", h)          # GitHub drops punctuation, keeps letters, digits, - and space
    return h.replace(" ", "-")


def anchors(md: Path) -> set[str]:
    text = re.sub(r"```.*?```", "", md.read_text(encoding="utf-8"), flags=re.S)
    return {slug(h) for h in HEADING_RE.findall(text)}


def main() -> int:
    errors: list[str] = []
    mds = [p for p in DOCS.rglob("*.md")]
    referenced: set[Path] = set()

    for md in mds:
        text = re.sub(r"```.*?```", "", md.read_text(encoding="utf-8"), flags=re.S)
        for target in LINK_RE.findall(text):
            if re.match(r"^[a-z]+:", target):          # http:, https:, mailto:
                continue
            path, _, frag = target.partition("#")
            dest = (md.parent / path).resolve() if path else md
            if not dest.exists():
                errors.append(f"{md.relative_to(DOCS)}: broken link -> {target}")
                continue
            referenced.add(dest)
            if frag and dest.suffix == ".md" and frag not in anchors(dest):
                errors.append(f"{md.relative_to(DOCS)}: missing anchor -> {target}")

    for area in AREAS:
        for src in sorted((DOCS / area / "src").glob("*.puml")):
            if src.name.startswith("_"):
                continue
            for ext in ("png", "svg"):
                out = DOCS / area / "rendered" / f"{src.stem}.{ext}"
                if not out.exists():
                    errors.append(f"{area}/src/{src.name}: missing rendered/{out.name}")
            png = (DOCS / area / "rendered" / f"{src.stem}.png").resolve()
            if png.exists() and png not in referenced:
                errors.append(f"{area}/rendered/{png.name}: not referenced by any Markdown page (orphan)")

    try:
        from openapi_spec_validator import validate
        from openapi_spec_validator.readers import read_from_filename
        spec, _ = read_from_filename(str(DOCS / "api" / "openapi-v1.yaml"))
        validate(spec)
    except ImportError:
        print("note: openapi-spec-validator not installed; OpenAPI validation skipped")
    except Exception as e:  # noqa: BLE001
        errors.append(f"api/openapi-v1.yaml: invalid OpenAPI: {e}")

    for e in errors:
        print(f"DOC ERROR: {e}", file=sys.stderr)
    print(f"Checked {len(mds)} Markdown files; {len(errors)} error(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
