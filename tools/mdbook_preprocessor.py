from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from tools.prepare_mdbook import build_title_cache, parse_bib, rewrite_markdown
except ModuleNotFoundError:
    from prepare_mdbook import build_title_cache, parse_bib, rewrite_markdown


PLACEHOLDER_PREFIX = "[TODO: src = zh_chapters/"
BIBLIOGRAPHY_TITLE = "References"
FRONTPAGE_SWITCH_LABEL = "中文"
FRONTPAGE_SWITCH_HREF = "cn/"


def iter_chapters(items: list[dict]) -> list[dict]:
    chapters: list[dict] = []
    for item in items:
        chapter = item.get("Chapter")
        if not chapter:
            continue
        chapters.append(chapter)
        chapters.extend(iter_chapters(chapter.get("sub_items", [])))
    return chapters


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "supports":
        return 0

    context, book = json.load(sys.stdin)
    root = Path(context["root"]).resolve()
    source_dir = (root / context["config"]["book"]["src"]).resolve()
    title_cache = build_title_cache(source_dir, placeholder_prefix=PLACEHOLDER_PREFIX)
    bib_path = source_dir.parent / "mlsys.bib"
    bib_db = parse_bib(bib_path) if bib_path.exists() else {}
    refs_dir = source_dir.parent / "references"
    if refs_dir.is_dir():
        for extra_bib in sorted(refs_dir.glob("*.bib")):
            for key, fields in parse_bib(extra_bib).items():
                bib_db.setdefault(key, fields)

    for chapter in iter_chapters(book.get("items", [])):
        source_path = chapter.get("source_path") or chapter.get("path")
        if not source_path:
            continue
        current_file = (source_dir / source_path).resolve()
        chapter["content"] = rewrite_markdown(
            chapter["content"],
            current_file,
            title_cache,
            bib_db,
            bibliography_title=BIBLIOGRAPHY_TITLE,
            frontpage_switch_label=FRONTPAGE_SWITCH_LABEL,
            frontpage_switch_href=FRONTPAGE_SWITCH_HREF,
        )

    json.dump(book, sys.stdout, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
