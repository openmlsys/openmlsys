from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class MdBookKatexConfigTests(unittest.TestCase):
    def test_books_use_katex_prerender_and_no_mathjax_head(self) -> None:
        book_tomls = [
            REPO_ROOT / "book.toml",
            REPO_ROOT / "books" / "zh" / "book.toml",
        ]
        head_templates = [
            REPO_ROOT / "theme" / "head.hbs",
            REPO_ROOT / "books" / "zh" / "theme" / "head.hbs",
        ]

        for book_toml in book_tomls:
            content = book_toml.read_text(encoding="utf-8")
            self.assertIn("[preprocessor.katex]", content, book_toml.as_posix())
            self.assertIn('pre-render = true', content, book_toml.as_posix())
            self.assertIn('after = [', content, book_toml.as_posix())
            self.assertNotIn("mathjax-support = true", content, book_toml.as_posix())

        for head_template in head_templates:
            content = head_template.read_text(encoding="utf-8")
            self.assertNotIn("MathJax.Hub.Config", content, head_template.as_posix())
            self.assertNotIn("MathJax.js", content, head_template.as_posix())


if __name__ == "__main__":
    unittest.main()
