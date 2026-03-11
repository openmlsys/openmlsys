from __future__ import annotations

import gzip
import hashlib
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from tools.ensure_mdbook_typst_math import (
    ASSET_SHA256,
    VERSION,
    build_download_url,
    ensure_binary,
    resolve_asset_name,
    resolve_binary_path,
    resolve_version_path,
)


class ResolveAssetNameTests(unittest.TestCase):
    def test_resolve_asset_name_for_supported_targets(self) -> None:
        self.assertEqual(
            resolve_asset_name(system="Darwin", machine="arm64"),
            "mdbook-typst-math-aarch64-apple-darwin.gz",
        )
        self.assertEqual(
            resolve_asset_name(system="Darwin", machine="x86_64"),
            "mdbook-typst-math-x86_64-apple-darwin.gz",
        )
        self.assertEqual(
            resolve_asset_name(system="Linux", machine="aarch64"),
            "mdbook-typst-math-aarch64-unknown-linux-gnu.gz",
        )
        self.assertEqual(
            resolve_asset_name(system="Linux", machine="AMD64"),
            "mdbook-typst-math-x86_64-unknown-linux-gnu.gz",
        )
        self.assertEqual(
            resolve_asset_name(system="Windows", machine="AMD64"),
            "mdbook-typst-math-x86_64-pc-windows-msvc.exe",
        )

    def test_resolve_asset_name_rejects_unsupported_targets(self) -> None:
        with self.assertRaises(ValueError):
            resolve_asset_name(system="Linux", machine="riscv64")


class EnsureBinaryTests(unittest.TestCase):
    def test_ensure_binary_downloads_and_extracts_gzip_release(self) -> None:
        payload = b"linux-binary"
        asset_name = "mdbook-typst-math-x86_64-unknown-linux-gnu.gz"

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            urls: list[str] = []

            def fake_downloader(url: str) -> bytes:
                urls.append(url)
                return gzip.compress(payload)

            with patch.dict(ASSET_SHA256, {asset_name: hashlib.sha256(gzip.compress(payload)).hexdigest()}):
                binary_path = ensure_binary(
                    output_dir,
                    system="Linux",
                    machine="x86_64",
                    downloader=fake_downloader,
                )

            self.assertEqual(binary_path, resolve_binary_path(output_dir, VERSION, asset_name))
            self.assertEqual(binary_path.name, "mdbook-typst-math")
            self.assertEqual(binary_path.read_bytes(), payload)
            self.assertEqual(resolve_version_path(output_dir).read_text(encoding="utf-8"), VERSION)
            self.assertEqual(urls, [build_download_url(VERSION, asset_name)])
            self.assertTrue(os.access(binary_path, os.X_OK))

    def test_ensure_binary_uses_cached_file_without_downloading(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)
            asset_name = "mdbook-typst-math-x86_64-unknown-linux-gnu.gz"
            cached_binary = resolve_binary_path(output_dir, VERSION, asset_name)
            output_dir.mkdir(parents=True, exist_ok=True)
            cached_binary.write_bytes(b"cached")
            cached_binary.chmod(0o755)
            resolve_version_path(output_dir).write_text(VERSION, encoding="utf-8")

            def fail_downloader(_: str) -> bytes:
                raise AssertionError("downloader should not be called for cached binary")

            binary_path = ensure_binary(
                output_dir,
                system="Linux",
                machine="x86_64",
                downloader=fail_downloader,
            )

            self.assertEqual(binary_path, cached_binary)
            self.assertEqual(binary_path.read_bytes(), b"cached")

    def test_ensure_binary_keeps_windows_extension(self) -> None:
        payload = b"windows-binary"
        asset_name = "mdbook-typst-math-x86_64-pc-windows-msvc.exe"

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir)

            def fake_downloader(_: str) -> bytes:
                return payload

            with patch.dict(ASSET_SHA256, {asset_name: hashlib.sha256(payload).hexdigest()}):
                binary_path = ensure_binary(
                    output_dir,
                    system="Windows",
                    machine="AMD64",
                    downloader=fake_downloader,
                )

            self.assertEqual(binary_path.name, "mdbook-typst-math.exe")
            self.assertEqual(binary_path.read_bytes(), payload)

    def test_ensure_binary_rejects_checksum_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            with self.assertRaises(ValueError):
                ensure_binary(
                    Path(tmpdir),
                    system="Linux",
                    machine="x86_64",
                    downloader=lambda _: gzip.compress(b"bad-binary"),
                )


if __name__ == "__main__":
    unittest.main()
