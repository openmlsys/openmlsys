from __future__ import annotations

import json
import sys
from pathlib import Path

from prepare_mdbook_zh import build_title_cache, parse_bib, rewrite_markdown


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
    source_dir = root / context["config"]["book"]["src"]
    title_cache = build_title_cache(source_dir)
    bib_path = root / "mlsys.bib"
    bib_db = parse_bib(bib_path) if bib_path.exists() else {}

    for chapter in iter_chapters(book.get("items", [])):
        source_path = chapter.get("source_path") or chapter.get("path")
        if not source_path:
            continue
        current_file = (source_dir / source_path).resolve()
        chapter["content"] = rewrite_markdown(chapter["content"], current_file, title_cache, bib_db)

    json.dump(book, sys.stdout, ensure_ascii=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
