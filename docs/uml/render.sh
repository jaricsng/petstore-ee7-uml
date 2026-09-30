#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Render every PlantUML source under docs/uml/src to SVG (primary) and PNG.
# Usage:   ./docs/uml/render.sh            (render SVG/PNG + Markdown pages)
#          ./docs/uml/render.sh --check    (syntax + Markdown freshness check; CI / pre-commit)
# Requires: Java 11+, Python 3.8+, Graphviz 'dot', and plantuml.jar (PLANTUML_JAR env var or
#           ~/.local/lib/plantuml.jar). Tested with PlantUML 1.2025.4.
# ---------------------------------------------------------------------------
set -euo pipefail
cd "$(dirname "$0")"

JAR="${PLANTUML_JAR:-$HOME/.local/lib/plantuml.jar}"
if [[ ! -f "$JAR" ]]; then
  echo "plantuml.jar not found. Download it:" >&2
  echo "  curl -L -o $JAR https://github.com/plantuml/plantuml/releases/download/v1.2025.4/plantuml-1.2025.4.jar" >&2
  exit 1
fi
JAVA_OPTS="-DPLANTUML_LIMIT_SIZE=16384 -Djava.awt.headless=true"

if [[ "${1:-}" == "--check" ]]; then
  java $JAVA_OPTS -jar "$JAR" -checkonly src/*/*.puml
  echo "All PlantUML sources are syntactically valid."
  python3 gen_markdown.py --check || { echo "Markdown pages are stale: run ./docs/uml/render.sh" >&2; exit 1; }
  exit 0
fi

for d in structure behaviour patterns; do
  mkdir -p "rendered/$d"
  java $JAVA_OPTS -jar "$JAR" -tsvg -o "$PWD/rendered/$d" src/$d/*.puml
  java $JAVA_OPTS -jar "$JAR" -tpng -o "$PWD/rendered/$d" src/$d/*.puml
done
echo "Rendered $(find rendered -type f | wc -l | tr -d ' ') files into docs/uml/rendered/"
python3 gen_markdown.py
