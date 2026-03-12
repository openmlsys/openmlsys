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

# ── English v1 ────────────────────────────────────────────────────────────────
"${PYTHON_BIN}" "${ROOT}/tools/ensure_book_resources.py" --chapter-dir "${ROOT}/v1/en_chapters"
"${PYTHON_BIN}" "${ROOT}/tools/prepare_mdbook.py" \
    --source "${ROOT}/v1/en_chapters" \
    --summary-output "${ROOT}/v1/en_chapters/SUMMARY.md" \
    --placeholder-prefix "[TODO: src = zh_chapters/"

mdbook build "${ROOT}/v1"

# ── Chinese v1 ────────────────────────────────────────────────────────────────
"${PYTHON_BIN}" "${ROOT}/tools/ensure_book_resources.py" --chapter-dir "${ROOT}/v1/zh_chapters"
"${PYTHON_BIN}" "${ROOT}/tools/prepare_mdbook_zh.py" \
    --source "${ROOT}/v1/zh_chapters" \
    --summary-output "${ROOT}/v1/zh_chapters/SUMMARY.md"

mdbook build "${ROOT}/v1/books/zh"
