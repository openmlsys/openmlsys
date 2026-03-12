from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
        return
    if path.is_dir():
        shutil.rmtree(path)


def copy_site(source: Path, destination: Path) -> None:
    source = source.resolve()
    if not source.is_dir():
        raise FileNotFoundError(f"Site source does not exist or is not a directory: {source}")

    remove_path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, destination)


def assemble_publish_tree(
    destination_root: Path,
    docs_subdir: str = "docs",
    en_source: Path | None = None,
    zh_source: Path | None = None,
    v1_en_source: Path | None = None,
    v1_zh_source: Path | None = None,
    v2_en_source: Path | None = None,
    v2_zh_source: Path | None = None,
) -> tuple[Path, Path | None]:
    if en_source is None and zh_source is None and v2_en_source is None:
        raise ValueError("At least one site source must be provided.")

    destination_root = destination_root.resolve()
    docs_root = (destination_root / docs_subdir).resolve()

    remove_path(docs_root)
    docs_root.parent.mkdir(parents=True, exist_ok=True)

    # v2 (latest) is deployed at the root — /docs/
    effective_en = v2_en_source or en_source
    if effective_en is not None:
        copy_site(effective_en, docs_root)
    else:
        docs_root.mkdir(parents=True, exist_ok=True)

    zh_destination: Path | None = None
    effective_zh = v2_zh_source or zh_source
    if effective_zh is not None:
        zh_destination = docs_root / "cn"
        copy_site(effective_zh, zh_destination)

    # v1 is deployed under /docs/v1/
    if v1_en_source is not None:
        v1_root = docs_root / "v1"
        copy_site(v1_en_source, v1_root)
        if v1_zh_source is not None:
            copy_site(v1_zh_source, v1_root / "cn")

    return docs_root, zh_destination


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Assemble the publish tree expected by openmlsys.github.io."
    )
    parser.add_argument(
        "--destination-root",
        type=Path,
        required=True,
        help="Root of the checked-out deployment repository.",
    )
    parser.add_argument(
        "--docs-subdir",
        default="docs",
        help="Subdirectory inside the destination root that hosts the site.",
    )
    parser.add_argument(
        "--en-source",
        type=Path,
        help="Built site to publish at docs/ (legacy, use --v2-en-source instead).",
    )
    parser.add_argument(
        "--zh-source",
        type=Path,
        help="Built site to publish at docs/cn/ (legacy, use --v2-zh-source instead).",
    )
    parser.add_argument(
        "--v1-en-source",
        type=Path,
        help="Built v1 English site to publish at docs/v1/.",
    )
    parser.add_argument(
        "--v1-zh-source",
        type=Path,
        help="Built v1 Chinese site to publish at docs/v1/cn/.",
    )
    parser.add_argument(
        "--v2-en-source",
        type=Path,
        help="Built v2 English site to publish at docs/.",
    )
    parser.add_argument(
        "--v2-zh-source",
        type=Path,
        help="Built v2 Chinese site to publish at docs/cn/.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    docs_root, zh_root = assemble_publish_tree(
        destination_root=args.destination_root,
        docs_subdir=args.docs_subdir,
        en_source=args.en_source,
        zh_source=args.zh_source,
        v1_en_source=args.v1_en_source,
        v1_zh_source=args.v1_zh_source,
        v2_en_source=args.v2_en_source,
        v2_zh_source=args.v2_zh_source,
    )
    print(f"Assembled root site at {docs_root}")
    if zh_root is not None:
        print(f"Assembled Chinese site at {zh_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
