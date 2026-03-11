#!/bin/bash
# Build the English (en) version of the book from en_chapters/.
# Output: en_chapters/_build/html/
#
# Resources (img/, references/, static/, mlsys.bib) live at the repo root and
# are symlinked into en_chapters/ so d2lbook can find them at relative paths.

set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"

# ── Create resource symlinks ──────────────────────────────────────────────────
python3 "$ROOT/tools/ensure_book_resources.py" --chapter-dir "$ROOT/en_chapters"

# ── Build ─────────────────────────────────────────────────────────────────────
cd "$ROOT/en_chapters"

rm -rf _build/rst _build/html
d2lbook build rst
cp static/frontpage.html _build/rst/
d2lbook build html
cp -r static/image/* _build/html/_images/ 2>/dev/null || true
python3 "$ROOT/tools/format_tables.py"
