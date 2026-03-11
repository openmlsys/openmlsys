from __future__ import annotations

import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
THEME_HEAD = REPO_ROOT / "theme" / "head.hbs"


class MdBookKatexTests(unittest.TestCase):
    def test_katex_prerender_outputs_katex_markup_without_mathjax(self) -> None:
        if shutil.which("mdbook") is None or shutil.which("mdbook-katex") is None:
            self.skipTest("mdbook or mdbook-katex is not installed")

        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            src = root / "src"
            theme = root / "theme"
            src.mkdir()
            theme.mkdir()

            (root / "book.toml").write_text(
                """[book]
title = "Test Book"
language = "en"
src = "src"

[build]
build-dir = "book"

[preprocessor.katex]
after = ["links"]
pre-render = true
""",
                encoding="utf-8",
            )
            (src / "SUMMARY.md").write_text("# Summary\n\n- [Chapter](chapter.md)\n", encoding="utf-8")
            (src / "chapter.md").write_text("# Chapter\n\nInline math $C$ and block:\n\n$$x^2$$\n", encoding="utf-8")
            (theme / "head.hbs").write_text(THEME_HEAD.read_text(encoding="utf-8"), encoding="utf-8")

            subprocess.run(["mdbook", "build", str(root)], check=True, capture_output=True, text=True)

            output = (root / "book" / "chapter.html").read_text(encoding="utf-8")
            self.assertIn("katex", output)
            self.assertNotIn("MathJax.Hub.Config", output)
            self.assertNotIn("MathJax.js", output)


if __name__ == "__main__":
    unittest.main()
