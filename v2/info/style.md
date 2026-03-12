# Writing Style Guide

This document defines the formatting and style requirements for v2 chapter content. All contributors must follow these guidelines when writing or modifying content.

> **Note:** The LaTeX-to-Markdown conversion workflow has been **deprecated**. All v2 content is written directly in Markdown — no Pandoc or similar tools are needed.

---

## Table of Contents

- [File Structure](#file-structure)
- [Custom Syntax](#custom-syntax)
- [Figure Guidelines](#figure-guidelines)
- [Table Guidelines](#table-guidelines)
- [Code Block Guidelines](#code-block-guidelines)
- [References](#references)

---

## File Structure

- Each chapter corresponds to a `v2/en_chapters/<nn>_chapter_<name>/` directory (e.g., `02_chapter_programming_and_graph/`)
- The chapter entry file is `index.md`; section content goes in separate `.md` files in the same directory
- Declare the section structure in `index.md` using a `toc` block (used to auto-generate `SUMMARY.md`):

```markdown
​```toc
:maxdepth: 2

section_one
section_two
​```
```

---

## Custom Syntax

The project preprocessor supports the following extended Markdown syntax. **Follow it strictly** to ensure a correct build.

### Inline Math

```markdown
The model learns the mapping $f: \mathcal{X} \rightarrow \mathcal{Y}$.
```

### Display Math with Label

Label names should include a language suffix (e.g., `-en`) to avoid conflicts with Chinese labels:

```markdown
$$
\mathcal{L}_{CE} = -\sum_{i=1}^{N} y_i \log(\hat{y}_i)
$$
:eqlabel:`eq-cross-entropy-en`
```

Reference an equation: `:eqref:\`eq-cross-entropy-en\``

### Figures with Labels

```markdown
![Figure description](../img/ch01/figure.png)
:width:`600px`
:label:`figure-label-en`
```

Reference a figure: `:numref:\`figure-label-en\``

### Section References

Add a label after a section heading:

```markdown
### Section Title
:label:`my-section-en`
```

Reference the section: `:ref:\`my-section-en\``

### Citations

```markdown
The perceptron :cite:`rosenblatt1958perceptron` is one of the earliest neural network models.
```

Multiple citations separated by commas: `:cite:\`paper1,paper2\``

All bibliography entries are maintained in `mlsys.bib` (see [References](#references)).

---

## Figure Guidelines

### Storage Location

Store figures under `img/ch<chapter-number>/`, e.g., `img/ch01/`. Image files must be committed together with the PR.

### Naming

Use lowercase English with hyphens, e.g., `framework-architecture.png`.

### Format

| Format | Use case |
|--------|---------|
| SVG    | Hand-drawn diagrams and flowcharts (vector, lossless scaling); remove white background |
| PNG    | Screenshots, photos, or images with complex gradients |

Recommended tools: PPT, draw.io. **Do not use images from the internet** (copyright risk).

### Resolution and Size

- Recommended resolution: ≥ 150 dpi
- Maximum width: 1200 px
- Set display width in Markdown via `:width:` (600–800 px recommended)

### Layout

Include sufficient explanatory text between adjacent figures. Do not place figures immediately next to each other.

---

## Table Guidelines

Use standard Markdown table syntax. Add a label to any table that needs to be referenced:

```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Value 1  | Value 2  | Value 3  |
:label:`table-label-en`
```

Reference a table: `:numref:\`table-label-en\``

---

## Code Block Guidelines

Use standard Markdown fenced code blocks and always specify the language:

````markdown
```python
import torch
import torch.nn as nn
```
````

Common language identifiers: `python`, `bash`, `cpp`, `markdown`, `text`.

---

## References

Add BibTeX entries to `mlsys.bib`:

```bibtex
@inproceedings{key2015,
  title  = {Title of the Paper},
  author = {Author, A. and Author, B.},
  year   = {2015}
}
```

**Note:** Duplicate keys in `mlsys.bib` are not allowed. Search for existing entries before adding a new one.

Example citations in body text:

```markdown
This chapter references the paper :cite:`cnn2015`.
Multiple citations: :cite:`cnn2015,rnn2015`.
```
