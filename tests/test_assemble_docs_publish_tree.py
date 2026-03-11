from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

from tools.assemble_docs_publish_tree import assemble_publish_tree


class AssembleDocsPublishTreeTests(unittest.TestCase):
    def test_assemble_publish_tree_uses_legacy_docs_layout(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            pages_repo = root / "pages"
            en_source = root / "en-html"
            zh_source = root / "zh-html"

            pages_repo.mkdir()
            en_source.mkdir()
            zh_source.mkdir()

            (en_source / "index.html").write_text("english home", encoding="utf-8")
            (en_source / "guide.html").write_text("english guide", encoding="utf-8")
            (zh_source / "index.html").write_text("chinese home", encoding="utf-8")
            (zh_source / "searchindex.js").write_text("zh search", encoding="utf-8")

            assemble_publish_tree(
                destination_root=pages_repo,
                docs_subdir="docs",
                en_source=en_source,
                zh_source=zh_source,
            )

            self.assertEqual(
                (pages_repo / "docs" / "index.html").read_text(encoding="utf-8"),
                "english home",
            )
            self.assertEqual(
                (pages_repo / "docs" / "guide.html").read_text(encoding="utf-8"),
                "english guide",
            )
            self.assertEqual(
                (pages_repo / "docs" / "cn" / "index.html").read_text(encoding="utf-8"),
                "chinese home",
            )
            self.assertEqual(
                (pages_repo / "docs" / "cn" / "searchindex.js").read_text(encoding="utf-8"),
                "zh search",
            )

    def test_assemble_publish_tree_replaces_stale_docs_content(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            pages_repo = root / "pages"
            en_source = root / "en-html"
            zh_source = root / "zh-html"

            (pages_repo / "docs" / "cn").mkdir(parents=True)
            (pages_repo / "docs" / "old.html").write_text("stale en", encoding="utf-8")
            (pages_repo / "docs" / "cn" / "old.html").write_text("stale zh", encoding="utf-8")

            en_source.mkdir()
            zh_source.mkdir()
            (en_source / "index.html").write_text("fresh en", encoding="utf-8")
            (zh_source / "index.html").write_text("fresh zh", encoding="utf-8")

            assemble_publish_tree(
                destination_root=pages_repo,
                docs_subdir="docs",
                en_source=en_source,
                zh_source=zh_source,
            )

            self.assertFalse((pages_repo / "docs" / "old.html").exists())
            self.assertFalse((pages_repo / "docs" / "cn" / "old.html").exists())
            self.assertEqual(
                (pages_repo / "docs" / "index.html").read_text(encoding="utf-8"),
                "fresh en",
            )
            self.assertEqual(
                (pages_repo / "docs" / "cn" / "index.html").read_text(encoding="utf-8"),
                "fresh zh",
            )


if __name__ == "__main__":
    unittest.main()
