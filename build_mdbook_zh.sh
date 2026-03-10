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

# ── Create resource symlinks ──────────────────────────────────────────────────
# Resources (img/, references/, static/, mlsys.bib) live at the repo root and
# are symlinked into zh_chapters/ so mdbook can find them at relative paths.
for target in img references static mlsys.bib; do
    link="${ROOT}/zh_chapters/${target}"
    rel_target="../${target}"
    if [[ -e "${link}" ]] && [[ ! -L "${link}" ]]; then
        echo "Refusing to replace non-symlink path: ${link}" >&2
        exit 1
    fi
    ln -sfn "${rel_target}" "${link}"
done

# ── Build ─────────────────────────────────────────────────────────────────────
"${PYTHON_BIN}" "${ROOT}/tools/prepare_mdbook_zh.py" \
    --source "${ROOT}/zh_chapters" \
    --summary-output "${ROOT}/zh_chapters/SUMMARY.md"

mdbook build "${ROOT}"
