#!/usr/bin/env python3
"""Lint Excalidraw sources and figure references for the openmlsys book.

Standard library only (Python 3.8+). No network access.

Usage:
    python3 check_figures.py PATH [PATH ...]

PATH may be:
  * a ``.excalidraw`` file or a directory (searched recursively) -- each scene
    is checked for structural problems and house-style violations, and for an
    exported ``.svg``/``.png`` sibling with the same stem;
  * a ``.md`` chapter file -- every image reference is checked: it must not
    point at a ``.pdf`` and the referenced file must exist.

Exit status is 1 if any ERROR was reported, otherwise 0 (WARNINGs only).
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ALLOWED_FONTS = {5, 3}  # 5 = Excalifont (body text), 3 = Cascadia (code)
MIN_FONT_SIZE = 16
IMAGE_REF = re.compile(r"!\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")

errors = 0
warnings = 0


def report(level: str, where: Path, msg: str) -> None:
    global errors, warnings
    if level == "ERROR":
        errors += 1
    else:
        warnings += 1
    print(f"{level}: {where}: {msg}")


def luminance(color: str) -> float | None:
    m = re.fullmatch(r"#([0-9a-fA-F]{6})", color or "")
    if not m:
        return None
    r, g, b = (int(m.group(1)[i : i + 2], 16) / 255 for i in (0, 2, 4))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def check_scene(path: Path) -> None:
    try:
        doc = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        report("ERROR", path, f"not valid JSON: {exc}")
        return
    if doc.get("type") != "excalidraw" or not isinstance(doc.get("elements"), list):
        report("ERROR", path, 'expected {"type": "excalidraw", "elements": [...]}')
        return

    elements = [e for e in doc["elements"] if not e.get("isDeleted")]
    by_id = {}
    for el in elements:
        eid = el.get("id")
        if not eid:
            report("ERROR", path, f"element without id: {el.get('type')}")
        elif eid in by_id:
            report("ERROR", path, f"duplicate id {eid!r}")
        by_id[eid] = el

    for el in elements:
        eid, etype = el.get("id"), el.get("type")
        tag = f"{etype} {eid!r}"
        if etype != "text" and "text" in el:
            report("ERROR", path, f"{tag} has a 'text' property; Excalidraw ignores it. "
                   "Use a separate text element with containerId (see references/openmlsys-conventions.md)")
        if etype == "text":
            if el.get("fontFamily") not in ALLOWED_FONTS:
                report("WARNING", path, f"{tag} uses fontFamily {el.get('fontFamily')}; house style is 5 (or 3 for code)")
            if (el.get("fontSize") or 0) < MIN_FONT_SIZE:
                report("WARNING", path, f"{tag} fontSize {el.get('fontSize')} < {MIN_FONT_SIZE}; may be illegible when scaled")
            lum = luminance(el.get("strokeColor", ""))
            if lum is not None and lum > 0.6:
                report("ERROR", path, f"{tag} text color {el['strokeColor']} is too light for the light page / #e8e8e8 dark-mode backdrop")
            cid = el.get("containerId")
            if cid:
                container = by_id.get(cid)
                if container is None:
                    report("ERROR", path, f"{tag} containerId {cid!r} does not exist")
                elif not any(b.get("id") == eid for b in container.get("boundElements") or []):
                    report("ERROR", path, f"container {cid!r} does not list text {eid!r} in boundElements")
        for b in el.get("boundElements") or []:
            if b.get("id") not in by_id:
                report("ERROR", path, f"{tag} boundElements references missing {b.get('id')!r}")
        for key in ("startBinding", "endBinding"):
            binding = el.get(key)
            if binding and binding.get("elementId") not in by_id:
                report("ERROR", path, f"{tag} {key} references missing {binding.get('elementId')!r}")
        if etype in ("arrow", "line") and len(el.get("points") or []) < 2:
            report("ERROR", path, f"{tag} needs at least two points")

    app = doc.get("appState") or {}
    if app.get("exportWithDarkMode"):
        report("WARNING", path, "exportWithDarkMode is on; export in light mode (the site handles dark mode)")

    stem = path.name[: -len(".excalidraw")]
    if not any((path.parent / f"{stem}{ext}").exists() for ext in (".svg", ".png")):
        report("WARNING", path, f"no exported {stem}.svg or {stem}.png next to the source")


def check_markdown(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for lineno, line in enumerate(text.splitlines(), 1):
        for target in IMAGE_REF.findall(line):
            if re.match(r"[a-z]+://", target):
                continue
            where = f"{path}:{lineno}"
            if target.lower().endswith(".pdf"):
                report("ERROR", Path(where), f"{target} is a PDF; browsers cannot show it in mdBook, export SVG/PNG instead")
            if target.endswith(".excalidraw"):
                report("ERROR", Path(where), f"{target} is an Excalidraw source; reference the exported SVG/PNG")
            if not (path.parent / target).exists():
                report("ERROR", Path(where), f"{target} does not resolve relative to the chapter file")


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0 if argv else 2
    for arg in argv:
        p = Path(arg)
        if p.is_dir():
            for scene in sorted(p.rglob("*.excalidraw")):
                check_scene(scene)
        elif p.suffix == ".excalidraw":
            check_scene(p)
        elif p.suffix == ".md":
            check_markdown(p)
        else:
            report("ERROR", p, "not a directory, .excalidraw or .md file")
    print(f"{errors} error(s), {warnings} warning(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
