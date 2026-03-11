from __future__ import annotations

import argparse
from pathlib import Path

try:
    from tools.prepare_mdbook import (
        build_title_cache,
        extract_title,
        inline_raw_html,
        parse_bib,
        process_equation_labels,
        rewrite_markdown,
        write_summary,
    )
except ModuleNotFoundError:
    from prepare_mdbook import (
        build_title_cache,
        extract_title,
        inline_raw_html,
        parse_bib,
        process_equation_labels,
        rewrite_markdown,
        write_summary,
    )


FRONTPAGE_SWITCH_LABEL = "English"
FRONTPAGE_SWITCH_HREF = "../"


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


def rewrite_markdown(
    markdown: str,
    current_file: Path,
    title_cache: dict[Path, str],
    bib_db: dict[str, dict[str, str]] | None = None,
    bibliography_title: str = "参考文献",
) -> str:
    try:
        from tools.prepare_mdbook import rewrite_markdown as generic_rewrite_markdown
    except ModuleNotFoundError:
        from prepare_mdbook import rewrite_markdown as generic_rewrite_markdown

    return generic_rewrite_markdown(
        markdown,
        current_file,
        title_cache,
        bib_db=bib_db,
        bibliography_title=bibliography_title,
        frontpage_switch_label=FRONTPAGE_SWITCH_LABEL,
        frontpage_switch_href=FRONTPAGE_SWITCH_HREF,
    )


if __name__ == "__main__":
    raise SystemExit(main())
