#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# Render and verify ALL design documentation under docs/.
#   docs/uml            UML 2.5.1 model (delegates to docs/uml/render.sh)
#   docs/architecture   C4 views, layer rules, ADRs
#   docs/ux             wireframes (Salt), screen flow, site map
#   docs/api            REST resource model, OpenAPI 3.1 contract
#   docs/testing        test architecture, generated test catalogue
# Usage:  ./docs/render.sh          render everything, regenerate generated docs, then verify
#         ./docs/render.sh --check  verify only (CI / pre-commit): syntax, freshness, links, anchors
# Requires: Java 11+, Graphviz, Python 3.8+, plantuml.jar (PLANTUML_JAR or ~/.local/lib/plantuml.jar)
# ---------------------------------------------------------------------------
set -euo pipefail
cd "$(dirname "$0")"
JAR="${PLANTUML_JAR:-$HOME/.local/lib/plantuml.jar}"
export PLANTUML_JAR="$JAR"
[[ -f "$JAR" ]] || { echo "plantuml.jar not found at $JAR" >&2; exit 1; }
JAVA_OPTS="-DPLANTUML_LIMIT_SIZE=16384 -Djava.awt.headless=true"
AREAS=(architecture ux api testing)

if [[ "${1:-}" == "--check" ]]; then
  ./uml/render.sh --check
  for a in "${AREAS[@]}"; do java $JAVA_OPTS -jar "$JAR" -checkonly $(ls $a/src/*.puml | grep -v '/_'); done
  python3 testing/gen_test_cases.py --check
  python3 check_docs.py
  exit 0
fi

./uml/render.sh
for a in "${AREAS[@]}"; do
  mkdir -p "$a/rendered"
  files=$(ls $a/src/*.puml | grep -v '/_')
  java $JAVA_OPTS -jar "$JAR" -tsvg -o "$PWD/$a/rendered" $files
  java $JAVA_OPTS -jar "$JAR" -tpng -o "$PWD/$a/rendered" $files
done
python3 testing/gen_test_cases.py
python3 check_docs.py
