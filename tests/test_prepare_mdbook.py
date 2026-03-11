from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.prepare_mdbook import (
    _relative_chapter_path,
    build_title_cache,
    collect_figure_labels,
    collect_labels,
    convert_math_to_mathjax,
    normalize_directives,
    process_figure_captions,
    rewrite_markdown,
    write_summary,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


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
                "<p class=\"star-slot\">STAR</p>\n<!-- OPENMLSYS_LANGUAGE_SWITCH -->\n<div class=\"hero\">frontpage</div>\n",
                encoding="utf-8",
            )

            rewritten = rewrite_markdown(
                index.read_text(encoding="utf-8"),
                index.resolve(),
                {index.resolve(): "Home"},
                frontpage_switch_label="中文",
                frontpage_switch_href="cn/",
            )

            self.assertIn('class="openmlsys-frontpage-switch-row"', rewritten)
            self.assertIn('class="openmlsys-frontpage-switch"', rewritten)
            self.assertIn('href="cn/"', rewritten)
            self.assertIn(">中文</a>", rewritten)
            self.assertLess(
                rewritten.index('class="star-slot"'),
                rewritten.index('class="openmlsys-frontpage-switch-row"'),
            )

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
            self.assertIn("border-radius: 6px;", rewritten)
            self.assertIn("background: #f6f8fa;", rewritten)
            self.assertIn(".content main {", rewritten)
            self.assertIn("max-width: min(100%, max(65%, var(--content-max-width)));", rewritten)
            self.assertIn(".openmlsys-frontpage {", rewritten)
            self.assertIn("width: 100%;", rewritten)
            self.assertIn("margin-inline: auto;", rewritten)

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

    def test_english_frontpage_author_grid_uses_top_aligned_spacing(self) -> None:
        frontpage = (REPO_ROOT / "en_chapters" / "frontpage.html").read_text(encoding="utf-8")

        self.assertIn(".authors.mdl-grid {", frontpage)
        self.assertIn("align-items: flex-start;", frontpage)
        self.assertIn("row-gap: calc(24px + 1.5em);", frontpage)
        self.assertIn("height: 120px;", frontpage)
        self.assertIn("object-fit: cover;", frontpage)

    def test_english_frontpage_footer_titles_are_stacked_not_flex_columns(self) -> None:
        frontpage = (REPO_ROOT / "en_chapters" / "frontpage.html").read_text(encoding="utf-8")

        self.assertIn(".authors .mdl-cell:not(.author-group-title) {", frontpage)
        self.assertIn(".author-group-title {", frontpage)
        self.assertIn("display: block;", frontpage)
        self.assertIn(".author-group-title h3,", frontpage)
        self.assertIn("width: 100%;", frontpage)


class CollectLabelsTests(unittest.TestCase):
    def test_standalone_label(self) -> None:
        md = ":label:`my_fig`\n"
        self.assertEqual(collect_labels(md), ["my_fig"])

    def test_inline_table_label(self) -> None:
        md = "|:label:`tbl`|||\n"
        self.assertEqual(collect_labels(md), ["tbl"])

    def test_escaped_underscores(self) -> None:
        md = ":label:`ros2\\_topics`\n"
        self.assertEqual(collect_labels(md), ["ros2\\_topics"])

    def test_empty(self) -> None:
        md = "No labels here.\n"
        self.assertEqual(collect_labels(md), [])

    def test_multiple_labels(self) -> None:
        md = ":label:`fig1`\nsome text\n:label:`fig2`\n"
        self.assertEqual(collect_labels(md), ["fig1", "fig2"])


class LabelToAnchorTests(unittest.TestCase):
    def test_standalone_label_becomes_anchor(self) -> None:
        result = normalize_directives(":label:`ROS2_arch`\n")
        self.assertIn('<a id="ROS2_arch"></a>', result)
        self.assertNotIn(":label:", result)

    def test_table_row_label_becomes_anchor(self) -> None:
        result = normalize_directives("|:label:`tbl`|||\n")
        self.assertIn('|<a id="tbl"></a>|||', result)

    def test_width_line_removed(self) -> None:
        result = normalize_directives(":width:`800px`\n")
        self.assertNotIn(":width:", result)
        self.assertNotIn("800px", result)


class NumrefToLinkTests(unittest.TestCase):
    def test_same_file_link(self) -> None:
        ref_map = {"my_fig": "chapter/page.md"}
        result = normalize_directives(
            "See :numref:`my_fig`.\n",
            ref_label_map=ref_map,
            current_source_path="chapter/page.md",
        )
        self.assertIn("[my_fig](#my_fig)", result)

    def test_cross_file_link(self) -> None:
        ref_map = {"my_fig": "other_ch/file.md"}
        result = normalize_directives(
            "See :numref:`my_fig`.\n",
            ref_label_map=ref_map,
            current_source_path="chapter/page.md",
        )
        self.assertIn("[my_fig](../other_ch/file.md#my_fig)", result)

    def test_unknown_label_fallback(self) -> None:
        result = normalize_directives(
            "See :numref:`unknown`.\n",
            ref_label_map={},
            current_source_path="chapter/page.md",
        )
        self.assertIn("`unknown`", result)
        self.assertNotIn("[unknown]", result)

    def test_no_ref_map_fallback(self) -> None:
        result = normalize_directives("See :numref:`foo`.\n")
        self.assertIn("`foo`", result)

    def test_escaped_underscores_in_numref(self) -> None:
        ref_map = {"ros2\\_topics": "chapter/ros.md"}
        result = normalize_directives(
            "See :numref:`ros2\\_topics`.\n",
            ref_label_map=ref_map,
            current_source_path="chapter/ros.md",
        )
        # _strip_latex_escapes_outside_math removes \_ → _, producing consistent IDs
        self.assertIn("[ros2_topics](#ros2_topics)", result)


class RelativeChapterPathTests(unittest.TestCase):
    def test_same_file(self) -> None:
        self.assertEqual(_relative_chapter_path("ch/page.md", "ch/page.md"), "")

    def test_same_dir(self) -> None:
        result = _relative_chapter_path("ch/a.md", "ch/b.md")
        self.assertEqual(result, "b.md")

    def test_different_dir(self) -> None:
        result = _relative_chapter_path("ch1/page.md", "ch2/other.md")
        self.assertEqual(result, "../ch2/other.md")


class CollectFigureLabelsTests(unittest.TestCase):
    def test_image_followed_by_label(self) -> None:
        md = "![cap](img.png)\n:label:`fig1`\n"
        self.assertEqual(collect_figure_labels(md), ["fig1"])

    def test_image_with_width_and_label(self) -> None:
        md = "![cap](img.png)\n:width:`800px`\n:label:`fig1`\n"
        self.assertEqual(collect_figure_labels(md), ["fig1"])

    def test_image_with_blank_lines(self) -> None:
        md = "![cap](img.png)\n\n:width:`800px`\n\n:label:`fig1`\n"
        self.assertEqual(collect_figure_labels(md), ["fig1"])

    def test_table_label_not_collected(self) -> None:
        md = "|:label:`tbl`|||\n"
        self.assertEqual(collect_figure_labels(md), [])

    def test_standalone_label_without_image(self) -> None:
        md = "# Heading\n:label:`sec1`\n"
        self.assertEqual(collect_figure_labels(md), [])

    def test_multiple_figures(self) -> None:
        md = "![a](a.png)\n:label:`f1`\n\n![b](b.png)\n:label:`f2`\n"
        self.assertEqual(collect_figure_labels(md), ["f1", "f2"])


class ProcessFigureCaptionsTests(unittest.TestCase):
    def test_figure_with_number_and_caption(self) -> None:
        md = "![量化原理](img.png)\n:width:`800px`\n:label:`fig1`\n"
        result = process_figure_captions(md, fig_number_map={"fig1": "8.1"})
        self.assertIn('<a id="fig1"></a>', result)
        self.assertIn("![量化原理](img.png)", result)
        self.assertIn('<p align="center">图8.1 量化原理</p>', result)
        self.assertNotIn(":width:", result)
        self.assertNotIn(":label:", result)

    def test_figure_without_number_map(self) -> None:
        md = "![caption](img.png)\n:label:`fig1`\n"
        result = process_figure_captions(md)
        self.assertIn('<a id="fig1"></a>', result)
        self.assertIn("![caption](img.png)", result)
        self.assertIn('<p align="center">caption</p>', result)

    def test_image_without_label_passthrough(self) -> None:
        md = "![caption](img.png)\nSome text\n"
        result = process_figure_captions(md)
        self.assertIn("![caption](img.png)", result)
        self.assertNotIn('<a id=', result)
        self.assertNotIn('<p align="center">', result)

    def test_figure_empty_caption(self) -> None:
        md = "![](img.png)\n:label:`fig1`\n"
        result = process_figure_captions(md, fig_number_map={"fig1": "1.1"})
        self.assertIn('<p align="center">图1.1</p>', result)


class NumrefWithFigureNumberTests(unittest.TestCase):
    def test_numref_shows_figure_number(self) -> None:
        result = normalize_directives(
            "See :numref:`my_fig`.\n",
            ref_label_map={"my_fig": "ch/page.md"},
            current_source_path="ch/page.md",
            fig_number_map={"my_fig": "8.1"},
        )
        self.assertIn("[图8.1](#my_fig)", result)

    def test_numref_cross_file_with_figure_number(self) -> None:
        result = normalize_directives(
            "See :numref:`my_fig`.\n",
            ref_label_map={"my_fig": "other/page.md"},
            current_source_path="ch/page.md",
            fig_number_map={"my_fig": "3.2"},
        )
        self.assertIn("[图3.2](../other/page.md#my_fig)", result)

    def test_numref_without_figure_number_shows_name(self) -> None:
        result = normalize_directives(
            "See :numref:`tbl`.\n",
            ref_label_map={"tbl": "ch/page.md"},
            current_source_path="ch/page.md",
            fig_number_map={},
        )
        self.assertIn("[tbl](#tbl)", result)


class LabelNumrefIntegrationTests(unittest.TestCase):
    def test_rewrite_markdown_with_label_map(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            page = Path(tmpdir) / "chapter" / "page.md"
            page.parent.mkdir()
            page.write_text(
                "# Title\n\n:label:`my_fig`\n\nSee :numref:`my_fig`.\n",
                encoding="utf-8",
            )
            rewritten = rewrite_markdown(
                page.read_text(encoding="utf-8"),
                page.resolve(),
                {page.resolve(): "Title"},
                ref_label_map={"my_fig": "chapter/page.md"},
                current_source_path="chapter/page.md",
            )
            self.assertIn('<a id="my_fig"></a>', rewritten)
            self.assertIn("[my_fig](#my_fig)", rewritten)

    def test_rewrite_markdown_cross_file_numref(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            page = Path(tmpdir) / "ch1" / "page.md"
            page.parent.mkdir()
            page.write_text(
                "# Title\n\nSee :numref:`other_fig`.\n",
                encoding="utf-8",
            )
            rewritten = rewrite_markdown(
                page.read_text(encoding="utf-8"),
                page.resolve(),
                {page.resolve(): "Title"},
                ref_label_map={"other_fig": "ch2/file.md"},
                current_source_path="ch1/page.md",
            )
            self.assertIn("[other_fig](../ch2/file.md#other_fig)", rewritten)

    def test_rewrite_markdown_figure_with_number_and_caption(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            page = Path(tmpdir) / "ch" / "page.md"
            page.parent.mkdir()
            page.write_text(
                "# Title\n\n![量化原理](img.png)\n:width:`800px`\n:label:`qfig`\n\nSee :numref:`qfig`.\n",
                encoding="utf-8",
            )
            rewritten = rewrite_markdown(
                page.read_text(encoding="utf-8"),
                page.resolve(),
                {page.resolve(): "Title"},
                ref_label_map={"qfig": "ch/page.md"},
                current_source_path="ch/page.md",
                fig_number_map={"qfig": "8.1"},
            )
            self.assertIn('<a id="qfig"></a>', rewritten)
            self.assertIn("![量化原理](img.png)", rewritten)
            self.assertIn('<p align="center">图8.1 量化原理</p>', rewritten)
            self.assertIn("[图8.1](#qfig)", rewritten)


class ConvertMathToMathjaxTests(unittest.TestCase):
    def test_display_math(self) -> None:
        result = convert_math_to_mathjax("before $$x^2$$ after")
        self.assertEqual(result, "before \\\\[x^2\\\\] after")

    def test_inline_math(self) -> None:
        result = convert_math_to_mathjax("before $x^2$ after")
        self.assertEqual(result, "before \\\\(x^2\\\\) after")

    def test_backslash_doubling_inside_math(self) -> None:
        result = convert_math_to_mathjax("$$a \\\\ b$$")
        self.assertEqual(result, "\\\\[a \\\\\\\\ b\\\\]")

    def test_math_inside_code_block_not_converted(self) -> None:
        text = "```\n$x^2$\n```"
        result = convert_math_to_mathjax(text)
        self.assertEqual(result, text)

    def test_math_inside_inline_code_not_converted(self) -> None:
        text = "use `$x$` for math"
        result = convert_math_to_mathjax(text)
        self.assertEqual(result, text)

    def test_cjk_dollar_spans_stripped(self) -> None:
        result = convert_math_to_mathjax("price $100美元$ done")
        self.assertEqual(result, "price 100美元 done")

    def test_no_math_passthrough(self) -> None:
        text = "No math here at all."
        self.assertEqual(convert_math_to_mathjax(text), text)

    def test_mixed_display_and_inline(self) -> None:
        text = "Inline $a$ and display $$b$$."
        result = convert_math_to_mathjax(text)
        self.assertEqual(result, "Inline \\\\(a\\\\) and display \\\\[b\\\\].")

    def test_asterisk_escaped_inside_math(self) -> None:
        result = convert_math_to_mathjax("$$n*CHW$$")
        self.assertEqual(result, "\\\\[n\\*CHW\\\\]")

    def test_underscore_escaped_inside_math(self) -> None:
        result = convert_math_to_mathjax("$x_i$")
        self.assertEqual(result, "\\\\(x\\_i\\\\)")


if __name__ == "__main__":
    unittest.main()
