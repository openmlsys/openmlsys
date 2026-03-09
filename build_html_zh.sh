#!/bin/bash
# Build the Chinese (zh) version of the book from zh_chapters/.
# Output: zh_chapters/_build/html/
#
# Resources (img/, references/, static/, mlsys.bib) live at the repo root and
# are symlinked into zh_chapters/ so d2lbook can find them at relative paths.

set -e

ROOT="$(cd "$(dirname "$0")" && pwd)"

# ── Create resource symlinks ──────────────────────────────────────────────────
for target in img references static mlsys.bib; do
    link="$ROOT/zh_chapters/$target"
    if [ ! -e "$link" ]; then
        ln -sf "$ROOT/$target" "$link"
    fi
done

# ── Build ─────────────────────────────────────────────────────────────────────
cd "$ROOT/zh_chapters"

rm -rf _build/rst _build/html
d2lbook build rst
cp static/frontpage.html _build/rst/
d2lbook build html
cp -r static/image/* _build/html/_images/ 2>/dev/null || true
python3 "$ROOT/tools/format_tables.py"
