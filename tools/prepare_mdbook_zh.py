from __future__ import annotations

import argparse
from pathlib import Path

try:
    from tools.prepare_mdbook import (
        build_title_cache,
        extract_title,
        parse_bib,
        rewrite_markdown,
        write_summary,
    )
except ModuleNotFoundError:
    from prepare_mdbook import (
        build_title_cache,
        extract_title,
        parse_bib,
        rewrite_markdown,
        write_summary,
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate mdBook SUMMARY.md for zh_chapters.")
    parser.add_argument("--source", type=Path, default=Path("zh_chapters"), help="Source chapter directory")
    parser.add_argument(
        "--summary-output",
        type=Path,
        default=Path("zh_chapters/SUMMARY.md"),
        help="Where to write the generated SUMMARY.md",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    summary_path = write_summary(args.source, summary_path=args.summary_output)
    print(f"Wrote mdBook summary to {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
