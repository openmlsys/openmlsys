# openmlsys figure conventions

These rules apply to every Excalidraw figure in the book. They extend
`CONTRIBUTING/style_en.md`, section "Figure Guidelines".

## Where files go

| What | Path |
|------|------|
| Image folder (physical) | `v1/img/ch<NN>/` |
| Same folder seen from a chapter | `v1/{en,zh}_chapters/img` → `../img`, `v2/{en,zh}_chapters/img` → `../../v1/img` (symlinks) |
| Chapter file (v2) | `v2/en_chapters/<NN>_chapter_<topic>/<section>.md` |
| Reference from a chapter | `../img/ch<NN>/<name>.svg` |

- `NN` is the chapter number of the chapter that uses the figure, for example
  `v2/en_chapters/03_chapter_accelerator/` → `img/ch03/`. v1 and v2 share this
  folder, so run `ls v1/img/ch<NN>/` first to avoid name clashes.
- Use lowercase names with hyphens: `pipeline-parallel-schedule`.
- The source and the export share a stem. Commit both:

  ```
  v1/img/ch06/pipeline-parallel-schedule.excalidraw     # editable source (EN)
  v1/img/ch06/pipeline-parallel-schedule.svg            # exported, used by en_chapters
  v1/img/ch06/pipeline-parallel-schedule-zh.excalidraw  # editable source (ZH)
  v1/img/ch06/pipeline-parallel-schedule-zh.svg         # exported, used by zh_chapters
  ```
- Do not save a source as `.json`. The repo `.gitignore` ignores `*.json`.

## Export formats

- **SVG** is the default for diagrams. Use **PNG** at 2x scale, at most
  1200 px wide, only if the SVG renders badly (very large scenes, embedded
  bitmaps).
- **Never use PDF.** mdBook output is HTML, and browsers do not render
  `![](x.pdf)` as an image. Some old v1 pages still point at `.pdf` files.
  Replace those references when you redraw the figures. Do not copy the pattern.
- Do not reference the `.excalidraw` file from Markdown.

### How to export

Use one of the following:

1. **Excalidraw MCP.** The style guide recommends the official server at
   `https://mcp.excalidraw.com` or the self-hosted `interactive-drawer`. Load
   the scene and export it to SVG or PNG with the settings below.
2. **excalidraw.com** (no install). Open the `.excalidraw` file, then
   *Menu → Export image*. Set *Background* off, *Dark mode* off and scale 2x
   for PNG, then save as SVG or PNG. Use *Menu → Save to…* to write the
   `.excalidraw` file back after you edit it.
3. **VS Code "Excalidraw" extension** (`pomdtr.excalidraw-editor`). It edits
   `.excalidraw` files in the editor and exports through the same dialog.

Export settings are the same for every method: light theme, no background
(the style guide asks for figures without a white background), and
`appState.exportWithDarkMode` false.

## Dark mode

The book's themes include `theme/dark-mode-images.css` (see
`tests/test_dark_mode_images_css.py`). In the dark themes `navy`, `coal` and
`ayu`, every body image gets a light gray `#e8e8e8` backdrop with 8 px
padding. Images are never inverted. A transparent figure therefore sits on
white in light mode and on `#e8e8e8` in dark mode. Consequences:

- Text and strokes must be dark. Use `#1e1e1e` by default. White or pastel
  text disappears, and `check_figures.py` reports it as an error.
- Every shape needs a visible dark stroke. A very light fill (`#e9ecef`,
  `#f8f9fa`) blends into the dark-mode backdrop, so do not rely on fill alone.
- Do not export with Excalidraw's "dark mode" option.
- Do not encode meaning by color alone. Add a label or a dashed/solid style
  difference so the figure also works in grayscale print.

## Palette

These are Excalidraw's built-in swatches, so the figures stay editable from
the stock UI.

| Role | Fill (`backgroundColor`) | Stroke / text |
|------|--------------------------|---------------|
| Default component | `#a5d8ff` (blue) | `#1e1e1e` |
| Data / tensors | `#b2f2bb` (green) | `#1e1e1e` |
| Highlight / focus | `#ffec99` (yellow) | `#1e1e1e` |
| Hardware / device | `#d0bfff` (violet) | `#1e1e1e` |
| Error / bottleneck | `#ffc9c9` (red) | `#1e1e1e` |
| Group / region frame | `transparent`, dashed stroke | `#495057` |
| Accent arrows (optional) | – | `#1971c2`, `#2f9e44`, `#e03131`, `#f08c00` |

Keep `fillStyle: "solid"`, `strokeWidth: 2`, `roughness: 1` and
`roundness: {"type": 3}` for boxes. Use the same values across one chapter.

## Text and fonts

- Use `fontFamily: 5` (Excalifont) for all labels and `3` (Cascadia) for code
  or identifiers. `1` (Virgil) is the legacy hand-drawn font and `2`
  (Helvetica) depends on the reader's system fonts. Do not use either.
- Excalidraw falls back to its bundled CJK hand-drawn font (Xiaolai) for
  Chinese automatically, and SVG export embeds the glyphs it uses. You do not
  need a different `fontFamily` for ZH variants.
- Use `fontSize` 20 for box labels, 16 for edge labels and annotations, and
  28 for an optional in-figure title. Most figures should have no title,
  because the Markdown caption serves that purpose.
- For math, write plain Unicode such as `W·x + b` or `∇L`. LaTeX is not
  rendered inside Excalidraw.

### Labels inside shapes (bound text)

```json
{ "id": "box1", "type": "rectangle", "...": "...",
  "boundElements": [{ "type": "text", "id": "box1-label" }] },
{ "id": "box1-label", "type": "text", "containerId": "box1",
  "text": "Parameter Server", "originalText": "Parameter Server",
  "fontSize": 20, "fontFamily": 5, "textAlign": "center",
  "verticalAlign": "middle", "lineHeight": 1.25, "autoResize": true,
  "strokeColor": "#1e1e1e", "...": "..." }
```

Center the text element in its container. Estimate the width as about
0.6 × fontSize per Latin character and 1.0 × fontSize per CJK character.
Excalidraw re-measures the text when the file is opened. Arrows that connect
shapes should set `startBinding`/`endBinding` (`{"elementId": ..., "focus": 0, "gap": 4}`).
The bound shapes must list the arrow in their `boundElements`.

## Bilingual figures

- If a figure contains words, make two variants: `<name>` (English, used by
  `en_chapters`) and `<name>-zh` (Chinese, used by `zh_chapters`).
- Build the ZH scene from the EN scene. Keep the ids and the geometry, and
  translate only `text`/`originalText`. Chinese labels are often wider, so
  widen the boxes and move neighbors symmetrically if needed.
- Keep established English acronyms (GPU, NCCL, AllReduce, KV cache) in the ZH
  variant. Follow `CONTRIBUTING/terminology.md` for the translated terms.
- A figure with no words, or only symbols and math, uses one file shared by
  both languages.
- Captions belong in the Markdown in each language, not in the image.

## Layout tips

- Draw main flows left to right, or top to bottom for stacks and layers.
- Leave a 40–80 px gap between boxes and use one box size per role.
- Use about 20 elements per figure at most. Split a dense figure and refer
  to both parts in the text.
- Leave a margin of about 20 px around the content so the exported image
  is not cropped tight.
