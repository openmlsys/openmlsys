# Build & Environment Guide

## Environment Setup

The book is deployed on GitHub using mdbook. We recommend installing mdbook via Rust's native package manager cargo.

```bash
# Install Rust toolchain to get cargo
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
cargo install mdbook
```

## Building HTML

Clone the [openmlsys-zh](https://github.com/openmlsys/openmlsys-zh) repository first. All build commands should be run from the repository root.

```bash
git clone https://github.com/openmlsys/openmlsys-zh.git
cd openmlsys-zh
```

Build HTML using mdbook. Please use the build scripts to ensure the homepage is correctly merged into the book.

```bash
sh build_mdbook_v1.sh
sh build_mdbook_v2.sh
```

Build outputs are placed in `.mdbook-v2/book` (English) and `.mdbook-v2-zh/book` (Chinese). The `tools/assemble_docs_publish_tree.py` script assembles the final bilingual publication tree, which is then copied to openmlsys.github.io for deployment.

For the detailed deployment workflow, see `.github/workflows/update_docs.yml`.

## Style Guide

Please follow the project [style guide](style_en.md) when contributing.

## Terminology

Please refer to the [terminology guide](terminology.md) for translations.
