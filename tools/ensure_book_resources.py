from __future__ import annotations

import argparse
import os
from pathlib import Path


RESOURCE_NAMES = ("img", "references", "static", "mlsys.bib")


def ensure_resource_views(
    chapter_dir: Path,
    repo_root: Path,
    resource_names: tuple[str, ...] = RESOURCE_NAMES,
    version: str = "v1"
) -> None:
    chapter_dir = chapter_dir.resolve()
    repo_root = repo_root.resolve()

    for name in resource_names:
        destination = chapter_dir / name
        source = repo_root / version / name
        if not source.exists():
            raise FileNotFoundError(f"Resource does not exist: {source}")

        if destination.is_symlink():
            destination.unlink()
        elif destination.exists():
            continue

        relative_source = os.path.relpath(source, start=chapter_dir)
        destination.symlink_to(relative_source)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Ensure chapter directories can see shared book resources."
    )
    parser.add_argument(
        "--chapter-dir",
        type=Path,
        required=True,
        help="Book source directory such as en_chapters or zh_chapters.",
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="Repository root that owns the shared resources.",
    )
    parser.add_argument(
        "--version",
        type=str,
        default="v1",
        help="Version subdirectory to place the resource links (default: v1).",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ensure_resource_views(args.chapter_dir, args.repo_root, version=args.version)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
