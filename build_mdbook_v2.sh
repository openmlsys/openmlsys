#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_BIN="$(command -v python3 || command -v python || true)"

if [[ -z "${PYTHON_BIN}" ]]; then
    echo "Python is required to prepare the mdBook staging tree." >&2
    exit 1
fi

if ! command -v mdbook >/dev/null 2>&1; then
    echo "mdbook is not installed. Install it first, for example with: cargo install mdbook" >&2
    exit 1
fi

# ── English v2 ────────────────────────────────────────────────────────────────
"${PYTHON_BIN}" "${ROOT}/tools/ensure_book_resources.py" --chapter-dir "${ROOT}/v2/en_chapters"
"${PYTHON_BIN}" "${ROOT}/tools/prepare_mdbook.py" \
    --source "${ROOT}/v2/en_chapters" \
    --summary-output "${ROOT}/v2/en_chapters/SUMMARY.md" \
    --placeholder-prefix "[TODO: src = zh_chapters/"

cd "${ROOT}/v2" && mdbook build .

# ── Chinese v2 ────────────────────────────────────────────────────────────────
"${PYTHON_BIN}" "${ROOT}/tools/ensure_book_resources.py" --chapter-dir "${ROOT}/v2/zh_chapters"
"${PYTHON_BIN}" "${ROOT}/tools/prepare_mdbook_zh.py" \
    --source "${ROOT}/v2/zh_chapters" \
    --summary-output "${ROOT}/v2/zh_chapters/SUMMARY.md"

cd "${ROOT}/v2/books/zh" && mdbook build .
