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

MDBOOK_TYPST_MATH_BIN_DIR="${ROOT}/.mdbook-bin"
"${PYTHON_BIN}" "${ROOT}/tools/ensure_mdbook_typst_math.py" --output-dir "${MDBOOK_TYPST_MATH_BIN_DIR}" >/dev/null
export PATH="${MDBOOK_TYPST_MATH_BIN_DIR}:${PATH}"

# ── Create resource links ─────────────────────────────────────────────────────
"${PYTHON_BIN}" "${ROOT}/tools/ensure_book_resources.py" --chapter-dir "${ROOT}/zh_chapters"

# ── Build ─────────────────────────────────────────────────────────────────────
"${PYTHON_BIN}" "${ROOT}/tools/prepare_mdbook_zh.py" \
    --source "${ROOT}/zh_chapters" \
    --summary-output "${ROOT}/zh_chapters/SUMMARY.md"

mdbook build "${ROOT}/books/zh"
