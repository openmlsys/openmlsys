from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
BOOK_PATHS = (
    REPO_ROOT / "book.toml",
    REPO_ROOT / "books" / "zh" / "book.toml",
)
BUILD_SCRIPTS = (
    REPO_ROOT / "build_mdbook.sh",
    REPO_ROOT / "build_mdbook_zh.sh",
)


class MdBookTypstMathConfigTests(unittest.TestCase):
    def test_books_use_typst_math_without_mathjax(self) -> None:
        for path in BOOK_PATHS:
            config = path.read_text(encoding="utf-8")

            self.assertIn("[preprocessor.typst-math]", config, path.as_posix())
            self.assertIn("theme/typst.css", config, path.as_posix())
            self.assertNotIn("mathjax-support = true", config, path.as_posix())

    def test_build_scripts_bootstrap_prebuilt_typst_math_binary(self) -> None:
        for path in BUILD_SCRIPTS:
            script = path.read_text(encoding="utf-8")

            self.assertIn("ensure_mdbook_typst_math.py", script, path.as_posix())
            self.assertIn("MDBOOK_TYPST_MATH_BIN_DIR", script, path.as_posix())
            self.assertIn("export PATH=", script, path.as_posix())
            self.assertNotIn("cargo install mdbook-typst-math", script, path.as_posix())


if __name__ == "__main__":
    unittest.main()
