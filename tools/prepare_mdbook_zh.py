from __future__ import annotations

import argparse
import os
import re
from dataclasses import dataclass
from pathlib import Path


TOC_FENCE = "toc"
EVAL_RST_FENCE = "eval_rst"
OPTION_LINE_RE = re.compile(r"^:(width|label):`[^`]+`\s*$", re.MULTILINE)
NUMREF_RE = re.compile(r":numref:`([^`]+)`")
EQREF_RE = re.compile(r":eqref:`([^`]+)`")
CITE_RE = re.compile(r":cite:`([^`]+)`")
BIB_ENTRY_RE = re.compile(r"@(\w+)\{([^,]+),")
LATEX_ESCAPE_RE = re.compile(r"\\([_%#&])")
RAW_HTML_FILE_RE = re.compile(r"^\s*:file:\s*([^\s]+)\s*$")
TOC_LINK_RE = re.compile(r"^\[([^\]]+)\]\(([^)]+)\)\s*$")
TOC_PART_RE = re.compile(r"^#+\s+(.+?)\s*$")
HEAD_TAG_RE = re.compile(r"</?head>", re.IGNORECASE)
STYLE_BLOCK_RE = re.compile(r"<style>(.*?)</style>", re.IGNORECASE | re.DOTALL)
FRONTPAGE_LAYOUT_CSS = """
<style>
.openmlsys-frontpage {
  width: 100%;
  margin: 0 auto 3rem;
}
.openmlsys-frontpage .mdl-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 24px;
  width: 100%;
  box-sizing: border-box;
}
.openmlsys-frontpage .mdl-cell {
  box-sizing: border-box;
  flex: 1 1 220px;
  min-width: 0;
}
.openmlsys-frontpage .mdl-cell--1-col {
  flex: 0 0 48px;
}
.openmlsys-frontpage .mdl-cell--3-col {
  flex: 0 1 calc(16.666% - 20px);
  max-width: calc(16.666% - 20px);
}
.openmlsys-frontpage .authors.mdl-grid {
  justify-content: center;
}
.openmlsys-frontpage .mdl-cell--5-col {
  flex: 1 1 calc(41.666% - 24px);
  max-width: calc(41.666% - 18px);
}
.openmlsys-frontpage .mdl-cell--12-col {
  flex: 1 1 100%;
  max-width: 100%;
}
.openmlsys-frontpage .mdl-cell--middle {
  align-self: center;
}
.openmlsys-frontpage .mdl-color-text--primary {
  color: var(--links, #0b6bcb);
}
.openmlsys-frontpage img {
  max-width: 100%;
  height: auto;
}
#content,
.content {
  max-width: min(1440px, calc(100vw - 48px));
}
.content main {
  max-width: 75%;
}
.openmlsys-frontpage + ul,
.openmlsys-frontpage + ul ul {
  max-width: 960px;
}
@media (max-width: 1000px) {
  .openmlsys-frontpage .mdl-cell,
  .openmlsys-frontpage .mdl-cell--1-col,
  .openmlsys-frontpage .mdl-cell--3-col,
  .openmlsys-frontpage .mdl-cell--5-col {
    flex: 1 1 100%;
    max-width: 100%;
  }
}
</style>
""".strip()


@dataclass(frozen=True)
class TocItem:
    kind: str
    label: str
    target: str | None = None


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


def parse_toc_entries(block_lines: list[str]) -> list[TocItem]:
    entries: list[TocItem] = []
    for line in block_lines:
        stripped = line.strip()
        if not stripped or stripped.startswith(":"):
            continue
        part_match = TOC_PART_RE.match(stripped)
        if part_match:
            entries.append(TocItem(kind="part", label=part_match.group(1).strip()))
            continue
        link_match = TOC_LINK_RE.match(stripped)
        if link_match:
            entries.append(TocItem(kind="chapter", label=link_match.group(1).strip(), target=link_match.group(2).strip()))
            continue
        entries.append(TocItem(kind="chapter", label="", target=stripped))
    return entries


def parse_toc_blocks(markdown: str) -> list[list[TocItem]]:
    blocks: list[list[TocItem]] = []
    lines = markdown.splitlines()
    index = 0

    while index < len(lines):
        if lines[index].strip() == f"```{TOC_FENCE}":
            index += 1
            block_lines: list[str] = []
            while index < len(lines) and lines[index].strip() != "```":
                block_lines.append(lines[index])
                index += 1
            entries = parse_toc_entries(block_lines)
            blocks.append(entries)
        index += 1

    return blocks


def resolve_toc_target(current_file: Path, entry: str) -> Path:
    target_name = entry if entry.endswith(".md") else f"{entry}.md"
    target = (current_file.parent / target_name).resolve()
    if not target.exists():
        raise FileNotFoundError(f"TOC entry '{entry}' from '{current_file}' does not exist")
    return target


def relative_link(from_file: Path, target_file: Path) -> str:
    return Path(os.path.relpath(target_file, start=from_file.parent)).as_posix()


def _strip_latex_escapes_outside_math(line: str) -> str:
    """Remove LaTeX escapes (\\_, \\%, \\#, \\&) from text outside $...$ math spans."""
    parts = line.split("$")
    for i in range(0, len(parts), 2):  # even indices are outside math
        parts[i] = LATEX_ESCAPE_RE.sub(r"\1", parts[i])
    return "$".join(parts)


def normalize_directives(markdown: str) -> str:
    normalized = OPTION_LINE_RE.sub("", markdown)
    normalized = NUMREF_RE.sub(lambda match: f"`{match.group(1)}`", normalized)
    normalized = EQREF_RE.sub(lambda match: f"`{match.group(1)}`", normalized)

    lines = [_strip_latex_escapes_outside_math(line.rstrip()) for line in normalized.splitlines()]
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


# ── BibTeX parsing ────────────────────────────────────────────────────────────


def clean_bibtex(value: str) -> str:
    """Remove BibTeX formatting (braces, LaTeX accents) from a string."""
    value = re.sub(r"\{\\[`'^\"~=.](\w)\}", r"\1", value)
    value = re.sub(r"\\[`'^\"~=.](\w)", r"\1", value)
    value = value.replace("{", "").replace("}", "")
    return value.strip()


def _parse_bib_fields(body: str) -> dict[str, str]:
    """Parse field=value pairs inside a BibTeX entry body."""
    fields: dict[str, str] = {}
    i = 0
    while i < len(body):
        while i < len(body) and body[i] in " \t\n\r,":
            i += 1
        if i >= len(body):
            break
        start = i
        while i < len(body) and body[i] not in "= \t\n\r":
            i += 1
        name = body[start:i].strip().lower()
        while i < len(body) and body[i] != "=":
            i += 1
        if i >= len(body):
            break
        i += 1
        while i < len(body) and body[i] in " \t\n\r":
            i += 1
        if i >= len(body):
            break
        if body[i] == "{":
            depth = 1
            i += 1
            vstart = i
            while i < len(body) and depth > 0:
                if body[i] == "{":
                    depth += 1
                elif body[i] == "}":
                    depth -= 1
                i += 1
            value = body[vstart : i - 1]
        elif body[i] == '"':
            i += 1
            vstart = i
            while i < len(body) and body[i] != '"':
                i += 1
            value = body[vstart:i]
            i += 1
        else:
            vstart = i
            while i < len(body) and body[i] not in ", \t\n\r}":
                i += 1
            value = body[vstart:i]
        if name:
            fields[name] = value.strip()
    return fields


def parse_bib(bib_path: Path) -> dict[str, dict[str, str]]:
    """Parse a BibTeX file and return a dict keyed by citation key."""
    text = bib_path.read_text(encoding="utf-8")
    entries: dict[str, dict[str, str]] = {}
    for match in BIB_ENTRY_RE.finditer(text):
        key = match.group(2).strip()
        start = match.end()
        depth = 1
        pos = start
        while pos < len(text) and depth > 0:
            if text[pos] == "{":
                depth += 1
            elif text[pos] == "}":
                depth -= 1
            pos += 1
        fields = _parse_bib_fields(text[start : pos - 1])
        fields["_type"] = match.group(1).lower()
        entries[key] = fields
    return entries


# ── Citation formatting ───────────────────────────────────────────────────────


def _first_author_surname(author_str: str) -> str:
    """Extract the first author's surname from a BibTeX author string."""
    author_str = clean_bibtex(author_str)
    authors = [a.strip() for a in author_str.split(" and ")]
    if not authors or not authors[0]:
        return ""
    first = authors[0]
    if "," in first:
        return first.split(",")[0].strip()
    parts = first.split()
    return parts[-1] if parts else first


def _format_cite_label(author: str, year: str) -> str:
    """Format an inline citation label like 'Surname et al., Year'."""
    surname = _first_author_surname(author)
    if not surname:
        return year or "?"
    authors = [a.strip() for a in clean_bibtex(author).split(" and ")]
    if len(authors) > 2:
        name_part = f"{surname} et al."
    elif len(authors) == 2:
        second = authors[1]
        if second.lower() == "others":
            name_part = f"{surname} et al."
        else:
            if "," in second:
                surname2 = second.split(",")[0].strip()
            else:
                parts = second.split()
                surname2 = parts[-1] if parts else second
            name_part = f"{surname} and {surname2}"
    else:
        name_part = surname
    if year:
        return f"{name_part}, {year}"
    return name_part


def _render_bibliography(
    cited_keys: list[str], bib_db: dict[str, dict[str, str]]
) -> list[str]:
    """Render a footnote-style bibliography section for the cited keys."""
    lines: list[str] = ["---", "", "## 参考文献", "", "<ol>"]
    for idx, key in enumerate(cited_keys, 1):
        entry = bib_db.get(key)
        if not entry:
            lines.append(f'<li id="ref-{key}">{key}. <a href="#cite-{key}">↩</a></li>')
            continue
        author = clean_bibtex(entry.get("author", ""))
        title = clean_bibtex(entry.get("title", ""))
        year = entry.get("year", "")
        venue = clean_bibtex(entry.get("journal", "") or entry.get("booktitle", ""))
        parts: list[str] = []
        if author:
            parts.append(author)
        if title:
            parts.append(f"<em>{title}</em>")
        if venue:
            parts.append(venue)
        if year:
            parts.append(year)
        text = ". ".join(parts) + "." if parts else f"{key}."
        lines.append(f'<li id="ref-{key}">{text} <a href="#cite-{key}">↩</a></li>')
    lines.append("</ol>")
    return lines


def process_citations(
    markdown: str, bib_db: dict[str, dict[str, str]]
) -> str:
    """Replace :cite: references with footnote-style numbered citations."""
    cited_keys: list[str] = []

    def _replace_cite(match: re.Match[str]) -> str:
        keys = [k.strip() for k in match.group(1).split(",")]
        for key in keys:
            if key not in cited_keys:
                cited_keys.append(key)
        if not bib_db:
            return "[" + ", ".join(keys) + "]"
        nums: list[str] = []
        for key in keys:
            idx = cited_keys.index(key) + 1
            nums.append(
                f'<sup id="cite-{key}"><a href="#ref-{key}">[{idx}]</a></sup>'
            )
        return "".join(nums)

    processed = CITE_RE.sub(_replace_cite, markdown)
    if cited_keys and bib_db:
        bib_lines = _render_bibliography(cited_keys, bib_db)
        processed = processed.rstrip("\n") + "\n\n" + "\n".join(bib_lines) + "\n"
    return processed


def resolve_raw_html_file(current_file: Path, filename: str) -> Path:
    direct = (current_file.parent / filename).resolve()
    if direct.exists():
        return direct

    static_fallback = (current_file.parent / "static" / filename).resolve()
    if static_fallback.exists():
        return static_fallback

    repo_static = (Path(__file__).resolve().parent.parent / "static" / filename)
    if repo_static.exists():
        return repo_static

    raise FileNotFoundError(f"Raw HTML include '{filename}' from '{current_file}' does not exist")


def rewrite_frontpage_assets(html: str) -> str:
    rewritten = html.replace('./_images/', 'static/image/')
    rewritten = rewritten.replace('_images/', 'static/image/')
    rewritten = HEAD_TAG_RE.sub("", rewritten)
    rewritten = STYLE_BLOCK_RE.sub(_minify_style_block, rewritten)
    return rewritten


def _minify_style_block(match: re.Match[str]) -> str:
    content = match.group(1)
    parts = [line.strip() for line in content.splitlines() if line.strip()]
    return f"<style>{' '.join(parts)}</style>"


def wrap_frontpage_html(html: str) -> str:
    return "\n".join([FRONTPAGE_LAYOUT_CSS, '<div class="openmlsys-frontpage">', html.strip(), '</div>'])


def inline_raw_html(block_lines: list[str], current_file: Path) -> str | None:
    stripped = [line.strip() for line in block_lines if line.strip()]
    if not stripped or stripped[0] != ".. raw:: html":
        return None

    filename: str | None = None
    for line in stripped[1:]:
        match = RAW_HTML_FILE_RE.match(line)
        if match:
            filename = match.group(1)
            break

    if filename is None:
        return None

    html_path = resolve_raw_html_file(current_file, filename)
    html = rewrite_frontpage_assets(html_path.read_text(encoding="utf-8")).strip()
    if Path(filename).name == "frontpage.html":
        return wrap_frontpage_html(html)
    return html


def chapter_label(item: TocItem, target: Path, title_cache: dict[Path, str]) -> str:
    return item.label or title_cache[target]


def render_toc_list(entries: list[TocItem], current_file: Path, title_cache: dict[Path, str]) -> list[str]:
    rendered: list[str] = []
    current_indent = 0
    for entry in entries:
        if entry.kind == "part":
            rendered.append(f"- {entry.label}")
            current_indent = 1
            continue

        if entry.target is None:
            continue

        target = resolve_toc_target(current_file, entry.target)
        label = chapter_label(entry, target, title_cache)
        rendered.append(f"{'  ' * current_indent}- [{label}]({relative_link(current_file, target)})")
    return rendered


def rewrite_markdown(
    markdown: str,
    current_file: Path,
    title_cache: dict[Path, str],
    bib_db: dict[str, dict[str, str]] | None = None,
) -> str:
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
                entries = parse_toc_entries(block_lines)
                if entries:
                    if output and output[-1] != "":
                        output.append("")
                    output.extend(render_toc_list(entries, current_file, title_cache))
                    if output and output[-1] != "":
                        output.append("")
            elif fence == EVAL_RST_FENCE:
                raw_html = inline_raw_html(block_lines, current_file)
                if raw_html:
                    if output and output[-1] != "":
                        output.append("")
                    output.extend(raw_html.splitlines())
                    if output and output[-1] != "":
                        output.append("")
            index += 1
            continue

        output.append(lines[index])
        index += 1

    while output and output[-1] == "":
        output.pop()

    result = normalize_directives("\n".join(output) + "\n")
    result = process_citations(result, bib_db or {})
    return result


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

    lines = ["# Summary", "", f"[{title_cache[root_index]}](index.md)"]
    seen: set[Path] = {root_index}

    def append_entry(target: Path, indent: int, label: str | None = None) -> None:
        target = target.resolve()
        if target in seen:
            return
        seen.add(target)
        rel = target.relative_to(source_dir.resolve()).as_posix()
        title = label or title_cache[target]
        lines.append(f"{'  ' * indent}- [{title}]({rel})")

        child_markdown = target.read_text(encoding="utf-8")
        for block in parse_toc_blocks(child_markdown):
            for entry in block:
                if entry.kind != "chapter" or entry.target is None:
                    continue
                append_entry(resolve_toc_target(target, entry.target), indent + 1, entry.label or None)

    def append_prefix_chapter(target: Path, label: str | None = None) -> None:
        target = target.resolve()
        if target in seen:
            return
        seen.add(target)
        rel = target.relative_to(source_dir.resolve()).as_posix()
        title = label or title_cache[target]
        lines.append(f"[{title}]({rel})")

    numbered_started = False
    for block in parse_toc_blocks(root_markdown):
        for entry in block:
            if entry.kind == "part":
                if lines and lines[-1] != "":
                    lines.append("")
                lines.append(f"# {entry.label}")
                lines.append("")
                numbered_started = True
                continue

            if entry.target is None:
                continue

            target = resolve_toc_target(root_index, entry.target)
            if numbered_started:
                append_entry(target, 0, entry.label or None)
            else:
                append_prefix_chapter(target, entry.label or None)

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
