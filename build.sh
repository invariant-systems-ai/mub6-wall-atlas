#!/usr/bin/env bash
# Render the MUB(6) Wall Atlas docs to a single, continuously paginated PDF.
# Portable: paths are relative to this script. Requires: pandoc and weasyprint.
# The PDF is a convenience artifact; the repository front doors remain README.md and START-HERE.md.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
CSS="$ROOT/assets/is-doc.css"
HEADER="$ROOT/assets/atlas-header.css"
BUILD="$ROOT/build"
TITLE="MUB(6) Wall Atlas"
ORDER=(
  START-HERE.md
  README.md
  LEAN-LANDING.md
  WOLFRAM-LANDING.md
  ATLAS.md
  POINTS.md
  SEED_ISSUES.md
  CONTRIBUTING.md
  DCO.md
  FAQ.md
  ACKNOWLEDGMENTS.md
  INTENT.md
)

mkdir -p "$BUILD"
cd "$ROOT"

echo ">> rendering ${#ORDER[@]} documents"
for f in "${ORDER[@]}"; do
  test -f "$f" || { echo "missing $f" >&2; exit 1; }
  echo "   - $f"
done

pandoc "${ORDER[@]}" \
  -f gfm \
  -t html5 \
  -s \
  --no-highlight \
  --toc \
  --toc-depth=1 \
  --metadata title="$TITLE" \
  -o "$BUILD/MUB6-Wall-Atlas.html"

weasyprint -q "$BUILD/MUB6-Wall-Atlas.html" "$BUILD/MUB6-Wall-Atlas.pdf" -s "$CSS" -s "$HEADER"
cp "$BUILD/MUB6-Wall-Atlas.pdf" "$ROOT/_MUB6-Wall-Atlas-preview.pdf"
echo ">> wrote $BUILD/MUB6-Wall-Atlas.pdf"
echo ">> refreshed _MUB6-Wall-Atlas-preview.pdf"
