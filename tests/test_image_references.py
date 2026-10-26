from __future__ import annotations

import os
import re
import unittest
from pathlib import Path

from tools.ensure_book_resources import RESOURCE_NAMES

REPO_ROOT = Path(__file__).resolve().parent.parent
CHAPTER_DIRS = (
    REPO_ROOT / "v1" / "en_chapters",
    REPO_ROOT / "v1" / "zh_chapters",
)
SHARED_RESOURCES = REPO_ROOT / "v1"
MARKDOWN_IMAGE_RE = re.compile(r"!\[[^\]]*\]\(\s*([^)\s]+)")
HTML_IMAGE_RE = re.compile(r"<img[^>]*?\ssrc=\"([^\"]+)\"")
# Browsers cannot display these inline, so mdBook renders a broken image.
UNRENDERABLE_SUFFIXES = {".pdf", ".eps", ".tif", ".tiff"}


def iter_markdown_files(chapter_dir: Path):
    for path in sorted(chapter_dir.rglob("*.md")):
        relative = path.relative_to(chapter_dir)
        if relative.parts[0] in RESOURCE_NAMES:
            continue
        yield path


def resolve_reference(chapter_dir: Path, markdown_file: Path, reference: str) -> Path:
    # Resource dirs are symlinks created at build time, so resolve them manually.
    target = Path(os.path.normpath(markdown_file.parent / reference))
    relative = target.relative_to(chapter_dir) if target.is_relative_to(chapter_dir) else None
    if relative is not None and relative.parts and relative.parts[0] in RESOURCE_NAMES:
        return SHARED_RESOURCES / relative
    return target


class ImageReferenceTests(unittest.TestCase):
    def test_chapter_images_exist_and_are_renderable(self) -> None:
        problems: list[str] = []
        for chapter_dir in CHAPTER_DIRS:
            for markdown_file in iter_markdown_files(chapter_dir):
                text = markdown_file.read_text(encoding="utf-8")
                references = MARKDOWN_IMAGE_RE.findall(text) + HTML_IMAGE_RE.findall(text)
                for reference in references:
                    if reference.startswith(("http://", "https://", "data:")):
                        continue
                    location = f"{markdown_file.relative_to(REPO_ROOT)}: {reference}"
                    if Path(reference).suffix.lower() in UNRENDERABLE_SUFFIXES:
                        problems.append(f"unrenderable format {location}")
                    elif not resolve_reference(chapter_dir, markdown_file, reference).is_file():
                        problems.append(f"missing file {location}")

        self.assertEqual(problems, [], "\n".join(problems))


if __name__ == "__main__":
    unittest.main()
