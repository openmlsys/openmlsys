from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.prepare_mdbook import build_title_cache, rewrite_markdown, write_summary


class PrepareMdBookTests(unittest.TestCase):
    def test_write_summary_skips_placeholder_pages(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source = root / "en_chapters"
            source.mkdir()

            (source / "index.md").write_text(
                """Machine Learning Systems
========================

```toc
:maxdepth: 2

chapter_preface/index
chapter_introduction/index
```

```toc
:maxdepth: 1

appendix/index
```
""",
                encoding="utf-8",
            )

            chapter_preface = source / "chapter_preface"
            chapter_preface.mkdir()
            (chapter_preface / "index.md").write_text(
                "[TODO: src = zh_chapters/chapter_preface/index.md]\n",
                encoding="utf-8",
            )

            chapter_intro = source / "chapter_introduction"
            chapter_intro.mkdir()
            (chapter_intro / "index.md").write_text("# Introduction\n", encoding="utf-8")

            appendix = source / "appendix"
            appendix.mkdir()
            (appendix / "index.md").write_text("# Appendix\n", encoding="utf-8")

            summary_path = write_summary(
                source,
                placeholder_prefix="[TODO: src = zh_chapters/",
            )
            summary = summary_path.read_text(encoding="utf-8")

            self.assertEqual(
                summary,
                """# Summary

[Machine Learning Systems](index.md)
[Introduction](chapter_introduction/index.md)
[Appendix](appendix/index.md)
""",
            )

            title_cache = build_title_cache(
                source,
                placeholder_prefix="[TODO: src = zh_chapters/",
            )
            rewritten = rewrite_markdown(
                (source / "index.md").read_text(encoding="utf-8"),
                (source / "index.md").resolve(),
                title_cache,
            )

            self.assertIn("- [Introduction](chapter_introduction/index.md)", rewritten)
            self.assertIn("- [Appendix](appendix/index.md)", rewritten)
            self.assertNotIn("chapter_preface/index.md", rewritten)

    def test_rewrite_markdown_uses_configured_bibliography_title(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            page = root / "chapter.md"
            page.write_text(
                """# Introduction

Reference :cite:`smith2024`.
""",
                encoding="utf-8",
            )

            rewritten = rewrite_markdown(
                page.read_text(encoding="utf-8"),
                page.resolve(),
                {page.resolve(): "Introduction"},
                bib_db={
                    "smith2024": {
                        "author": "Smith, Alice and Doe, Bob",
                        "title": "Systems Paper",
                        "year": "2024",
                        "journal": "ML Systems Journal",
                    }
                },
                bibliography_title="References",
            )

            self.assertIn("## References", rewritten)
            self.assertNotIn("## 参考文献", rewritten)

    def test_rewrite_markdown_inlines_frontpage_with_language_switch(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source = root / "en_chapters"
            static_dir = source / "static"
            static_dir.mkdir(parents=True)

            index = source / "index.md"
            index.write_text(
                """# Home

```eval_rst
.. raw:: html
   :file: frontpage.html
```
""",
                encoding="utf-8",
            )
            (static_dir / "frontpage.html").write_text(
                "<div class=\"hero\">frontpage</div>\n",
                encoding="utf-8",
            )

            rewritten = rewrite_markdown(
                index.read_text(encoding="utf-8"),
                index.resolve(),
                {index.resolve(): "Home"},
                frontpage_switch_label="中文",
                frontpage_switch_href="cn/",
            )

            self.assertIn('class="openmlsys-frontpage-switch"', rewritten)
            self.assertIn('href="cn/"', rewritten)
            self.assertIn(">中文</a>", rewritten)

    def test_rewrite_markdown_prefers_book_local_frontpage_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source = root / "en_chapters"
            static_dir = source / "static"
            source.mkdir()
            static_dir.mkdir()

            index = source / "index.md"
            index.write_text(
                """# Home

```eval_rst
.. raw:: html
   :file: frontpage.html
```
""",
                encoding="utf-8",
            )
            (source / "frontpage.html").write_text(
                "<div class=\"hero\">English frontpage</div>\n",
                encoding="utf-8",
            )
            (static_dir / "frontpage.html").write_text(
                "<div class=\"hero\">Chinese fallback</div>\n",
                encoding="utf-8",
            )

            rewritten = rewrite_markdown(
                index.read_text(encoding="utf-8"),
                index.resolve(),
                {index.resolve(): "Home"},
            )

            self.assertIn("English frontpage", rewritten)
            self.assertNotIn("Chinese fallback", rewritten)
            self.assertIn("background: transparent !important;", rewritten)
            self.assertIn("padding: 0 !important;", rewritten)

    def test_regular_page_does_not_render_frontpage_switch(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            page = root / "chapter.md"
            page.write_text("# Chapter\n\nRegular body.\n", encoding="utf-8")

            rewritten = rewrite_markdown(
                page.read_text(encoding="utf-8"),
                page.resolve(),
                {page.resolve(): "Chapter"},
                frontpage_switch_label="中文",
                frontpage_switch_href="cn/",
            )

            self.assertNotIn('openmlsys-frontpage-switch', rewritten)


if __name__ == "__main__":
    unittest.main()
