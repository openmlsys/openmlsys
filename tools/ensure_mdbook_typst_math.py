from __future__ import annotations

import argparse
import gzip
import hashlib
import os
import platform
import urllib.request
from pathlib import Path


VERSION = "v0.3.0"
RELEASE_BASE_URL = "https://github.com/duskmoon314/mdbook-typst-math/releases/download"
ASSET_SHA256 = {
    "mdbook-typst-math-aarch64-apple-darwin.gz": "9c7a94113e16a465edd1324010e2cc432be3c0794320c13d6a44d9523f069384",
    "mdbook-typst-math-aarch64-unknown-linux-gnu.gz": "bbcf4574e380663400af74dda76dd6ecafd36aff185d653a2e24e294c45321c3",
    "mdbook-typst-math-x86_64-apple-darwin.gz": "8bb36eb558fc438c55162b442975eca588a7654b8069860526e46cc08c2aee6a",
    "mdbook-typst-math-x86_64-pc-windows-msvc.exe": "b5d3e07108a7286007d153c66efe434d06ab6caf43fcd22f78b4e6af8a294314",
    "mdbook-typst-math-x86_64-unknown-linux-gnu.gz": "3b785a42fb3a93bcd3f80106e6ded5c55bb0bcd4cd0634edf8232d14444b6987",
}
SUPPORTED_ASSETS = {
    ("darwin", "aarch64"): "mdbook-typst-math-aarch64-apple-darwin.gz",
    ("darwin", "x86_64"): "mdbook-typst-math-x86_64-apple-darwin.gz",
    ("linux", "aarch64"): "mdbook-typst-math-aarch64-unknown-linux-gnu.gz",
    ("linux", "x86_64"): "mdbook-typst-math-x86_64-unknown-linux-gnu.gz",
    ("windows", "x86_64"): "mdbook-typst-math-x86_64-pc-windows-msvc.exe",
}


def normalize_machine(machine: str) -> str:
    normalized = machine.strip().lower()
    if normalized in {"arm64", "aarch64"}:
        return "aarch64"
    if normalized in {"amd64", "x86_64", "x64"}:
        return "x86_64"
    return normalized


def normalize_system(system: str) -> str:
    normalized = system.strip().lower()
    if normalized.startswith("mingw") or normalized.startswith("msys") or normalized.startswith("cygwin"):
        return "windows"
    return normalized


def resolve_asset_name(system: str | None = None, machine: str | None = None) -> str:
    resolved_system = normalize_system(system or platform.system())
    resolved_machine = normalize_machine(machine or platform.machine())
    asset_name = SUPPORTED_ASSETS.get((resolved_system, resolved_machine))
    if asset_name is None:
        raise ValueError(
            f"Unsupported platform for mdbook-typst-math: system={resolved_system!r}, machine={resolved_machine!r}"
        )
    return asset_name


def build_download_url(version: str, asset_name: str) -> str:
    return f"{RELEASE_BASE_URL}/{version}/{asset_name}"


def resolve_binary_path(output_dir: Path, version: str, asset_name: str) -> Path:
    binary_name = "mdbook-typst-math.exe" if asset_name.endswith(".exe") else "mdbook-typst-math"
    return output_dir / binary_name


def resolve_version_path(output_dir: Path) -> Path:
    return output_dir / ".mdbook-typst-math.version"


def download_bytes(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "openmlsys-mdbook-bootstrap/1.0"})
    with urllib.request.urlopen(request) as response:
        return response.read()


def ensure_binary(
    output_dir: Path,
    *,
    version: str = VERSION,
    system: str | None = None,
    machine: str | None = None,
    downloader=download_bytes,
) -> Path:
    asset_name = resolve_asset_name(system=system, machine=machine)
    binary_path = resolve_binary_path(output_dir, version, asset_name)
    version_path = resolve_version_path(output_dir)
    if binary_path.exists() and version_path.exists() and version_path.read_text(encoding="utf-8").strip() == version:
        if binary_path.suffix != ".exe":
            binary_path.chmod(binary_path.stat().st_mode | 0o111)
        return binary_path

    expected_sha256 = ASSET_SHA256[asset_name]
    download_url = build_download_url(version, asset_name)
    archive_bytes = downloader(download_url)
    digest = hashlib.sha256(archive_bytes).hexdigest()
    if digest != expected_sha256:
        raise ValueError(
            f"Checksum mismatch for {asset_name}: expected {expected_sha256}, got {digest}"
        )

    binary_path.parent.mkdir(parents=True, exist_ok=True)
    payload = gzip.decompress(archive_bytes) if asset_name.endswith(".gz") else archive_bytes
    output_dir.mkdir(parents=True, exist_ok=True)
    temporary_path = binary_path.with_suffix(f"{binary_path.suffix}.tmp")
    temporary_path.write_bytes(payload)
    if binary_path.suffix != ".exe":
        temporary_path.chmod(0o755)
    os.replace(temporary_path, binary_path)
    version_path.write_text(version, encoding="utf-8")
    return binary_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download a pinned mdbook-typst-math release binary.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(".mdbook-bin"),
        help="Directory used to cache the downloaded mdbook-typst-math binary.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    binary_path = ensure_binary(args.output_dir.resolve())
    print(binary_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
