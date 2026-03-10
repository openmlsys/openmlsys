from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
THEME_HEAD = REPO_ROOT / "theme" / "head.hbs"


class MdBookMathJaxTests(unittest.TestCase):
    def test_custom_head_enables_inline_dollar_math_before_mathjax_script(self) -> None:
        if shutil.which("mdbook") is None:
            self.skipTest("mdbook is not installed")

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            src = root / "src"
            theme = root / "theme"
            src.mkdir()
            theme.mkdir()

            (root / "book.toml").write_text(
                """[book]
title = "Test Book"
language = "zh-CN"
src = "src"

[build]
build-dir = "book"

[output.html]
mathjax-support = true
""",
                encoding="utf-8",
            )
            (src / "SUMMARY.md").write_text("# Summary\n\n- [Chapter](chapter.md)\n", encoding="utf-8")
            (src / "chapter.md").write_text("# Chapter\n\nInline math $C$.\n", encoding="utf-8")
            theme_head = THEME_HEAD.read_text(encoding="utf-8")
            (theme / "head.hbs").write_text(theme_head, encoding="utf-8")

            subprocess.run(["mdbook", "build", str(root)], check=True, capture_output=True, text=True)

            output = (root / "book" / "chapter.html").read_text(encoding="utf-8")
            config_index = output.index("MathJax.Hub.Config")
            script_index = output.index("MathJax.js?config=TeX-AMS-MML_HTMLorMML")

            self.assertIn("inlineMath: [['$', '$'], ['\\\\(', '\\\\)']]", output)
            self.assertLess(config_index, script_index)


if __name__ == "__main__":
    unittest.main()
