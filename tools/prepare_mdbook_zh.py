from __future__ import annotations

import argparse
import re
from pathlib import Path


TOC_FENCE = "toc"
EVAL_RST_FENCE = "eval_rst"
OPTION_LINE_RE = re.compile(r"^:(width|label):`[^`]+`\s*$", re.MULTILINE)
NUMREF_RE = re.compile(r":numref:`([^`]+)`")
EQREF_RE = re.compile(r":eqref:`([^`]+)`")
CITE_RE = re.compile(r":cite:`([^`]+)`")


def extract_title(markdown: str, fallback: str = "Untitled") -> str:
    lines = markdown.splitlines()

    for index, line in enumerate(lines):
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            heading = stripped.lstrip("#").strip()
            if heading:
                return heading

        next_index = index + 1
        if next_index < len(lines):
            underline = lines[next_index].strip()
            if underline and set(underline) <= {"=", "-"}:
                return stripped

    return fallback


def parse_toc_blocks(markdown: str) -> list[list[str]]:
    blocks: list[list[str]] = []
    lines = markdown.splitlines()
    index = 0

    while index < len(lines):
        if lines[index].strip() == f"```{TOC_FENCE}":
            index += 1
            entries: list[str] = []
            while index < len(lines) and lines[index].strip() != "```":
                stripped = lines[index].strip()
                if stripped and not stripped.startswith(":"):
                    entries.append(stripped)
                index += 1
            blocks.append(entries)
        index += 1

    return blocks


def resolve_toc_target(current_file: Path, entry: str) -> Path:
    target = (current_file.parent / f"{entry}.md").resolve()
    if not target.exists():
        raise FileNotFoundError(f"TOC entry '{entry}' from '{current_file}' does not exist")
    return target


def relative_link(from_file: Path, target_file: Path) -> str:
    return target_file.relative_to(from_file.parent).as_posix()


def normalize_directives(markdown: str) -> str:
    normalized = OPTION_LINE_RE.sub("", markdown)
    normalized = NUMREF_RE.sub(lambda match: f"`{match.group(1)}`", normalized)
    normalized = EQREF_RE.sub(lambda match: f"`{match.group(1)}`", normalized)
    normalized = CITE_RE.sub(lambda match: f"[{match.group(1)}]", normalized)

    lines = [line.rstrip() for line in normalized.splitlines()]
    collapsed: list[str] = []
    previous_blank = False
    for line in lines:
        is_blank = line == ""
        if is_blank and previous_blank:
            continue
        collapsed.append(line)
        previous_blank = is_blank

    while collapsed and collapsed[-1] == "":
        collapsed.pop()

    return "\n".join(collapsed) + "\n"


def render_toc_list(entries: list[str], current_file: Path, title_cache: dict[Path, str]) -> list[str]:
    rendered: list[str] = []
    for entry in entries:
        target = resolve_toc_target(current_file, entry)
        rendered.append(f"- [{title_cache[target]}]({relative_link(current_file, target)})")
    return rendered


def rewrite_markdown(markdown: str, current_file: Path, title_cache: dict[Path, str]) -> str:
    output: list[str] = []
    lines = markdown.splitlines()
    index = 0

    while index < len(lines):
        stripped = lines[index].strip()
        if stripped in (f"```{TOC_FENCE}", f"```{EVAL_RST_FENCE}"):
            fence = stripped[3:]
            index += 1
            block_lines: list[str] = []
            while index < len(lines) and lines[index].strip() != "```":
                block_lines.append(lines[index])
                index += 1

            if fence == TOC_FENCE:
                entries = [line.strip() for line in block_lines if line.strip() and not line.strip().startswith(":")]
                if entries:
                    if output and output[-1] != "":
                        output.append("")
                    output.extend(render_toc_list(entries, current_file, title_cache))
                    if output and output[-1] != "":
                        output.append("")
            index += 1
            continue

        output.append(lines[index])
        index += 1

    while output and output[-1] == "":
        output.pop()

    return normalize_directives("\n".join(output) + "\n")


def build_title_cache(source_dir: Path) -> dict[Path, str]:
    cache: dict[Path, str] = {}
    for markdown_file in sorted(source_dir.rglob("*.md")):
        if "_build" in markdown_file.parts or markdown_file.name == "SUMMARY.md":
            continue
        cache[markdown_file.resolve()] = extract_title(markdown_file.read_text(encoding="utf-8"), fallback=markdown_file.stem)
    return cache


def build_summary(source_dir: Path, title_cache: dict[Path, str]) -> str:
    root_index = (source_dir / "index.md").resolve()
    root_markdown = root_index.read_text(encoding="utf-8")

    lines = ["# Summary", "", f"- [{title_cache[root_index]}](index.md)"]
    seen: set[Path] = {root_index}

    def append_entry(target: Path, indent: int) -> None:
        target = target.resolve()
        if target in seen:
            return
        seen.add(target)
        rel = target.relative_to(source_dir.resolve()).as_posix()
        lines.append(f"{'  ' * indent}- [{title_cache[target]}]({rel})")

        child_markdown = target.read_text(encoding="utf-8")
        for block in parse_toc_blocks(child_markdown):
            for entry in block:
                append_entry(resolve_toc_target(target, entry), indent + 1)

    for block in parse_toc_blocks(root_markdown):
        for entry in block:
            append_entry(resolve_toc_target(root_index, entry), 0)

    return "\n".join(lines) + "\n"


def write_summary(source_dir: Path, summary_path: Path | None = None) -> Path:
    source_dir = source_dir.resolve()
    summary_path = summary_path.resolve() if summary_path else (source_dir / "SUMMARY.md")
    title_cache = build_title_cache(source_dir)
    summary_path.write_text(build_summary(source_dir, title_cache), encoding="utf-8")
    return summary_path


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
    summary_path = write_summary(args.source, args.summary_output)
    print(f"Wrote mdBook summary to {summary_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
