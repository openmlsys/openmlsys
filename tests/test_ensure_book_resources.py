from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.ensure_book_resources import ensure_resource_views


class EnsureBookResourcesTests(unittest.TestCase):
    def test_ensure_resource_views_creates_missing_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            chapter_dir = root / "en_chapters"
            chapter_dir.mkdir()

            for directory in ("img", "references", "static"):
                (root / directory).mkdir()
            (root / "mlsys.bib").write_text("bib", encoding="utf-8")

            ensure_resource_views(chapter_dir, root)

            for name in ("img", "references", "static", "mlsys.bib"):
                path = chapter_dir / name
                self.assertTrue(path.is_symlink(), f"{name} should be a symlink")
                self.assertEqual(path.resolve(), (root / name).resolve())

    def test_ensure_resource_views_keeps_existing_non_symlink_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            chapter_dir = root / "en_chapters"
            chapter_dir.mkdir()

            for directory in ("img", "references", "static"):
                (root / directory).mkdir()
            (root / "mlsys.bib").write_text("root bib", encoding="utf-8")

            local_bib = chapter_dir / "mlsys.bib"
            local_bib.write_text("local bib", encoding="utf-8")
            local_static = chapter_dir / "static"
            local_static.mkdir()
            (local_static / "frontpage.html").write_text("local static", encoding="utf-8")

            ensure_resource_views(chapter_dir, root)

            self.assertFalse(local_bib.is_symlink())
            self.assertEqual(local_bib.read_text(encoding="utf-8"), "local bib")
            self.assertFalse(local_static.is_symlink())
            self.assertTrue((local_static / "frontpage.html").exists())
            self.assertTrue((chapter_dir / "img").is_symlink())
            self.assertTrue((chapter_dir / "references").is_symlink())


if __name__ == "__main__":
    unittest.main()
