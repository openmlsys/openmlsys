from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.prepare_mdbook_zh import extract_title, process_equation_labels, rewrite_markdown, write_summary


class PrepareMdBookZhTests(unittest.TestCase):
    def test_extract_title_supports_atx_and_setext_headings(self) -> None:
        self.assertEqual(extract_title("# 导论\n"), "导论")
        self.assertEqual(extract_title("前言文字\n\n## 机器学习应用\n"), "机器学习应用")
        self.assertEqual(extract_title("机器学习系统：设计和实现\n=========================\n"), "机器学习系统：设计和实现")

    def test_write_summary_generates_nested_navigation(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source = root / "zh_chapters"
            source.mkdir()

            (source / "index.md").write_text(
                """机器学习系统：设计和实现
=========================

```eval_rst
.. raw:: html
   :file: frontpage.html
```

```toc
:maxdepth: 2

[前言](chapter_preface/index)

# 基础篇
chapter_introduction/index

# 附录
[机器学习基础附录](appendix_machine_learning_introduction/index)
```
""",
                encoding="utf-8",
            )

            chapter_preface = source / "chapter_preface"
            chapter_preface.mkdir()
            (chapter_preface / "index.md").write_text("# 前言\n", encoding="utf-8")
            static_dir = source / "static"
            static_dir.mkdir()
            (static_dir / "frontpage.html").write_text(
                "<div class=\"hero\">frontpage</div>\n",
                encoding="utf-8",
            )

            chapter_intro = source / "chapter_introduction"
            chapter_intro.mkdir()
            (chapter_intro / "index.md").write_text(
                """# 导论

```toc
:maxdepth: 2

applications
design
```
""",
                encoding="utf-8",
            )
            (chapter_intro / "applications.md").write_text("# 机器学习应用\n", encoding="utf-8")
            (chapter_intro / "design.md").write_text("# 设计目标\n", encoding="utf-8")

            appendix = source / "appendix_machine_learning_introduction"
            appendix.mkdir()
            (appendix / "index.md").write_text("# 机器学习基础附录\n", encoding="utf-8")

            for name in ("img", "static", "references"):
                (root / name).mkdir()
            (root / "mlsys.bib").write_text("% bibliography\n", encoding="utf-8")

            summary_path = write_summary(source)
            summary = summary_path.read_text(encoding="utf-8")
            self.assertEqual(
                summary,
                """# Summary

[机器学习系统：设计和实现](index.md)
[前言](chapter_preface/index.md)

# 基础篇

- [导论](chapter_introduction/index.md)
  - [机器学习应用](chapter_introduction/applications.md)
  - [设计目标](chapter_introduction/design.md)

# 附录

- [机器学习基础附录](appendix_machine_learning_introduction/index.md)
""",
            )

            title_cache = {
                (source / "chapter_preface" / "index.md").resolve(): "前言",
                (source / "chapter_introduction" / "index.md").resolve(): "导论",
                (source / "chapter_introduction" / "applications.md").resolve(): "机器学习应用",
                (source / "chapter_introduction" / "design.md").resolve(): "设计目标",
                (source / "appendix_machine_learning_introduction" / "index.md").resolve(): "机器学习基础附录",
            }
            root_index = rewrite_markdown((source / "index.md").read_text(encoding="utf-8"), (source / "index.md").resolve(), title_cache)
            self.assertNotIn("```eval_rst", root_index)
            self.assertNotIn("```toc", root_index)
            self.assertIn("- [前言](chapter_preface/index.md)", root_index)
            self.assertIn("- 基础篇", root_index)
            self.assertIn("  - [导论](chapter_introduction/index.md)", root_index)
            self.assertIn("- 附录", root_index)
            self.assertIn("  - [机器学习基础附录](appendix_machine_learning_introduction/index.md)", root_index)

            intro_index = rewrite_markdown(
                (source / "chapter_introduction" / "index.md").read_text(encoding="utf-8"),
                (source / "chapter_introduction" / "index.md").resolve(),
                title_cache,
            )
            self.assertNotIn("```toc", intro_index)
            self.assertIn("- [机器学习应用](applications.md)", intro_index)
            self.assertIn("- [设计目标](design.md)", intro_index)

    def test_write_summary_raises_for_missing_toc_entries(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source = root / "zh_chapters"
            source.mkdir()

            (source / "index.md").write_text(
                """# 首页

```toc
:maxdepth: 2

existing
missing
```
""",
                encoding="utf-8",
            )
            (source / "existing.md").write_text("# 现有章节\n", encoding="utf-8")

            summary_path = write_summary(source)
            summary = summary_path.read_text(encoding="utf-8")
            self.assertIn("existing", summary)
            self.assertNotIn("missing", summary)

    def test_rewrite_markdown_normalizes_common_d2l_directives(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source = root / "zh_chapters"
            source.mkdir()

            page = source / "chapter.md"
            page.write_text(
                """# 标题

![配图](../img/example.png)
:width:`800px`
:label:`fig_example`

参见 :numref:`fig_example` 和公式 :eqref:`eq_example`，引用 :cite:`foo2024`。
""",
                encoding="utf-8",
            )

            rewritten = rewrite_markdown(page.read_text(encoding="utf-8"), page.resolve(), {page.resolve(): "标题"})
            self.assertNotIn(":width:", rewritten)
            self.assertNotIn(":label:", rewritten)
            self.assertNotIn(":numref:", rewritten)
            self.assertNotIn(":eqref:", rewritten)
            self.assertNotIn(":cite:", rewritten)
            self.assertIn("`fig_example`", rewritten)
            self.assertIn("$\\eqref{eq_example}$", rewritten)
            self.assertIn("[foo2024]", rewritten)

    def test_rewrite_markdown_inlines_frontpage_html_include(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            source = root / "zh_chapters"
            static_dir = source / "static"
            static_dir.mkdir(parents=True)

            index = source / "index.md"
            index.write_text(
                """# 首页

```eval_rst
.. raw:: html
   :file: frontpage.html
```
""",
                encoding="utf-8",
            )
            (static_dir / "frontpage.html").write_text(
                """<head>
<style>
.hero { color: red; }

.other { color: blue; }
</style>
</head>
<p class="star-slot">STAR</p>
<!-- OPENMLSYS_LANGUAGE_SWITCH -->
<div class="hero">
  <img src="_images/logo.png" />
  <img src="./_images/jinxuefeng.png" />
</div>
<script>console.log('frontpage');</script>
""",
                encoding="utf-8",
            )

            rewritten = rewrite_markdown(index.read_text(encoding="utf-8"), index.resolve(), {index.resolve(): "首页"})
            self.assertNotIn("```eval_rst", rewritten)
            self.assertNotIn("<head>", rewritten)
            self.assertIn('class="openmlsys-frontpage"', rewritten)
            self.assertIn('<div class="hero">', rewritten)
            self.assertIn('<style>', rewritten)
            self.assertIn(".hero { color: red; } .other { color: blue; }", rewritten)
            self.assertIn("static/image/logo.png", rewritten)
            self.assertIn("static/image/jinxuefeng.png", rewritten)
            self.assertIn("console.log('frontpage')", rewritten)
            self.assertNotIn('class="openmlsys-frontpage-switch-row"', rewritten)


    def test_process_equation_labels_single_line(self) -> None:
        """Verify single-line equation gets \\tag and \\label injected."""
        md = "# Title\n\n$$a = f(z)$$\n:eqlabel:`sigmoid`\n\nSee :eqref:`sigmoid`.\n"
        result, label_map = process_equation_labels(md)
        self.assertIn("\\tag{1}\\label{sigmoid}$$", result)
        self.assertNotIn(":eqlabel:", result)
        self.assertEqual(label_map, {"sigmoid": 1})

    def test_process_equation_labels_multiline(self) -> None:
        """Verify multi-line equation (closing $$ on own line) gets \\tag and \\label."""
        md = "# Title\n\n$$\na = f(z)\n$$\n:eqlabel:`eq1`\n"
        result, label_map = process_equation_labels(md)
        lines = result.split("\n")
        # \\tag line should appear before the closing $$
        tag_idx = next(i for i, l in enumerate(lines) if "\\tag{1}\\label{eq1}" in l)
        close_idx = next(i for i, l in enumerate(lines) if l.strip() == "$$" and i > tag_idx)
        self.assertLess(tag_idx, close_idx)
        self.assertNotIn(":eqlabel:", result)
        self.assertEqual(label_map, {"eq1": 1})

    def test_process_equation_labels_sequential_numbering(self) -> None:
        """Verify multiple equations get sequential numbers."""
        md = "$$a$$\n:eqlabel:`eq1`\n\n$$b$$\n:eqlabel:`eq2`\n"
        result, label_map = process_equation_labels(md)
        self.assertIn("\\tag{1}\\label{eq1}", result)
        self.assertIn("\\tag{2}\\label{eq2}", result)
        self.assertEqual(label_map, {"eq1": 1, "eq2": 2})


if __name__ == "__main__":
    unittest.main()
