from __future__ import annotations

import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]


class DarkModeImagesCssTests(unittest.TestCase):
    def test_both_theme_css_files_style_dark_mode_body_images_only(self) -> None:
        css_paths = [
            REPO_ROOT / "v1" / "theme" / "dark-mode-images.css",
            REPO_ROOT / "v1" / "books" / "zh" / "theme" / "dark-mode-images.css",
            REPO_ROOT / "v2" / "theme" / "dark-mode-images.css",
            REPO_ROOT / "v2" / "books" / "zh" / "theme" / "dark-mode-images.css",
        ]

        for css_path in css_paths:
            css = css_path.read_text(encoding="utf-8")

            self.assertIn(".navy .content main img", css, css_path.as_posix())
            self.assertIn(".coal .content main img", css, css_path.as_posix())
            self.assertIn(".ayu .content main img", css, css_path.as_posix())
            self.assertIn("background-color: #e8e8e8;", css, css_path.as_posix())
            self.assertIn(".openmlsys-frontpage img", css, css_path.as_posix())
            self.assertIn("background-color: transparent !important;", css, css_path.as_posix())
            self.assertIn("padding: 0 !important;", css, css_path.as_posix())


if __name__ == "__main__":
    unittest.main()
