---
name: excalidraw-diagram
description: Draw figures for the openmlsys "Machine Learning Systems" book with Excalidraw. Use when a chapter needs a new or redrawn diagram (architecture, pipeline, flowchart, data flow, sequence, mind map), or when asked to "draw", "diagram", "make a figure" or "create an Excalidraw file" for this repo. Produces an editable .excalidraw source plus an exported SVG/PNG under v1/img/chXX/, with EN/ZH variants when the figure contains text.
---

# Excalidraw figures for openmlsys

Every figure in the book has two files side by side: the editable `.excalidraw`
source and the exported `.svg` (preferred) or `.png` that the Markdown
references. Read [references/openmlsys-conventions.md](references/openmlsys-conventions.md)
before drawing. It covers paths, house style, dark mode and bilingual variants.

## Workflow

1. **Plan the figure.** Pick the diagram type and list the nodes, edges and
   labels. Keep it to about 20 elements. If it needs more, split it into
   several figures.
2. **Choose the paths.** Images live in `v1/img/ch<NN>/`, which every chapter
   tree reaches through its `img` symlink. Name files in lowercase with
   hyphens, e.g. `v1/img/ch03/tensor-core-dataflow.excalidraw`. v1 and v2
   share this folder, so check that the name is not taken.
3. **Write the scene.** Start from a file in [templates/](templates/) or write
   the JSON yourself. The schema is in
   [references/excalidraw-schema.md](references/excalidraw-schema.md) and the
   element specs are in [references/element-types.md](references/element-types.md).
   House rules:
   - Text uses `fontFamily: 5` (Excalifont), or `3` for code. Use `fontSize`
     16 or more and the dark stroke `#1e1e1e`.
   - A label inside a shape is a **separate `text` element** with
     `containerId` set to the shape. The shape must list it in
     `boundElements`. A `text` property on a rectangle is silently ignored.
   - Use pastel fills, dark strokes and no white or light-colored text (see
     the palette in the conventions file).
   - To add a connector to an existing file, run
     `python3 .claude/skills/excalidraw-diagram/scripts/add-arrow.py <file> x1 y1 x2 y2 [--label T] [--style dashed]`.
4. **Make the ZH variant** if the figure contains words. Copy the scene to
   `<name>-zh.excalidraw` and translate only the text. Then widen any boxes
   that the Chinese labels overflow. Figures without text use one shared file.
5. **Lint.** Run `python3 .claude/skills/excalidraw-diagram/scripts/check_figures.py <files or dirs>`.
   It needs only the standard library. Fix every ERROR.
6. **Export** each scene to `<name>.svg` (or `<name>.png` at 2x) next to its
   source: background off, dark mode off, light theme. You can export with the
   Excalidraw MCP, excalidraw.com or the VS Code Excalidraw extension (steps in
   the conventions file). If you have no tool that can render, stop here. Tell
   the contributor which files still need exporting. Do not hand-write an SVG.
   **Never export or reference a PDF.** mdBook pages cannot display PDF images.
7. **Reference** the image from the chapter with a relative path:

   ```markdown
   ![Data flow of a training step](../img/ch06/training-step-dataflow.svg)
   :width:`700px`
   :label:`fig-training-step-dataflow`
   ```

   Use the `-zh.svg` variant in `v2/zh_chapters/...`. Re-run `check_figures.py`
   on the edited `.md` files to confirm that the paths resolve.

## Deliverables checklist

- [ ] `<name>.excalidraw` + exported `<name>.svg|png` (and `-zh` pair if the figure has text)
- [ ] `check_figures.py` reports 0 errors for the scenes and the edited chapter files
- [ ] Markdown references the SVG/PNG, never `.pdf` or `.excalidraw`
- [ ] Commit the source and the export together

## Attribution

Adapted from the `excalidraw-diagram-generator` skill in
[github/awesome-copilot](https://github.com/github/awesome-copilot/tree/main/skills/excalidraw-diagram-generator)
(MIT, see [LICENSE.txt](LICENSE.txt)).
