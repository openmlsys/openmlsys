<p align="center">
  <img src="info/logo-with-text.png" alt="OpenMLSys Logo" width="400"/>
</p>

<p align="center">
  <a href="https://github.com/openmlsys/openmlsys-zh/actions/workflows/main.yml">
    <img src="https://github.com/openmlsys/openmlsys-zh/actions/workflows/main.yml/badge.svg" alt="CI"/>
  </a>
  <a href="https://openmlsys.github.io/">
    <img src="https://img.shields.io/badge/book-online-blue" alt="Book Online"/>
  </a>
  <a href="https://github.com/openmlsys/openmlsys-zh/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/openmlsys/openmlsys-zh" alt="License"/>
  </a>
  <a href="https://github.com/openmlsys/openmlsys-zh/stargazers">
    <img src="https://img.shields.io/github/stars/openmlsys/openmlsys-zh?style=social" alt="GitHub Stars"/>
  </a>
</p>

<p align="center">
  <a href="README.md">中文</a> | <b>English</b>
</p>

---

# Machine Learning Systems: Design and Implementation

An open-source book explaining the design principles and implementation experience of modern machine learning systems, covering the complete technology stack from programming interfaces and computational graphs to compilers and distributed training.

**English version 1 (stable):** [openmlsys.github.io/html-en/](https://openmlsys.github.io/html-en/)

**English version 2:** Under reconstruction.

## Table of Contents

- [Target Audience](#target-audience)
- [Content Overview](#content-overview)
- [Build Guide](#build-guide)
- [Contributing](#contributing)
- [Community](#community)
- [License](#license)

## Target Audience

- **Students**: Those who have mastered machine learning fundamentals and want to deeply understand the design and implementation of modern ML systems.
- **Researchers**: Those who need to develop custom operators or leverage distributed execution for large model development.
- **Engineers**: Those responsible for building ML infrastructure and need to tune system performance or customize ML systems for business needs.

## Content Overview

The book (2nd edition) consists of 9 chapters:

| Chapter | Content |
|---------|---------|
| [Chapter 1: Introduction](v2/en_chapters/01_chapter_introduction/) | Overview of ML system architecture and technology stack |
| [Chapter 2: Programming Interfaces and Computational Graphs](v2/en_chapters/02_chapter_programming_and_graph/) | Tensor abstraction, automatic differentiation, graph representation and execution |
| [Chapter 3: AI Accelerators and Programming](v2/en_chapters/03_chapter_accelerator/) | GPU architecture and CUDA/Triton/CUTLASS programming models |
| [Chapter 4: AI Compilers and Runtime Systems](v2/en_chapters/04_chapter_compiler_and_runtime/) | IR design, graph optimization, kernel generation, and runtime execution |
| [Chapter 5: Data Processing Systems](v2/en_chapters/05_chapter_data_processing/) | Data loading, data pipelines, and distributed data processing |
| [Chapter 6: Training Systems](v2/en_chapters/06_chapter_training_systems/) | Single-node and distributed training, parallelism strategies, and training optimization |
| [Chapter 7: Model Serving](v2/en_chapters/07_chapter_model_serving/) | Inference optimization, online serving, and model management |
| [Chapter 8: RL Systems](v2/en_chapters/08_chapter_rl_systems/) | Reinforcement learning pipelines, environment interaction, and RL system design |
| [Chapter 9: Large-scale GPU Cluster Management](v2/en_chapters/09_chapter_gpu_cluster/) | GPU scheduling, resource management, and large-scale training infrastructure |

## Changelog

| Date | Event |
|------|-------|
| 2022-01 | Project initialized; Chinese content writing begins |
| 2022-05 | Extension chapters released (Federated Learning, RL Systems, Explainable AI) |
| 2023-05 | Codebase adapted to MindSpore 2.0 |
| 2026-03 | Bilingual (CN/EN) build architecture refactored; English version launched |

## Build Guide

### Prerequisites

- curl
- git
- Python 3

### Installation

```bash
# Clone the repository
git clone https://github.com/openmlsys/openmlsys-zh.git
cd openmlsys-zh

# Install Rust toolchain (Linux/macOS)
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Install mdbook
cargo install mdbook
```

### Build HTML

```bash
sh build_mdbook_v2.sh
# English output: .mdbook-v2/book
# Chinese output: .mdbook-v2-zh/book
```

For more details, see the [Build Guide](v2/info/info.md).

## Contributing

We welcome all forms of contributions. For the full workflow, see the **[Contributing Guide](v2/info/CONTRIBUTING.md)**.

Before contributing, please read:
- [Writing Style Guide](v2/info/style.md)
- [Terminology Guide](v2/info/terminology.md)

## Community

<p align="center">
  <img src="info/mlsys_group.png" alt="微信群二维码" width="200"/>
  <br/>
  Join our WeChat group by scanning the QR code
</p>

## Citation

If this book has been helpful to your research or work, please cite it as:

**Plain text:**

> OpenMLSys Team. *Machine Learning Systems: Design and Implementation*. 2022. https://openmlsys.github.io/

**BibTeX:**

```bibtex
@book{openmlsys2022,
  title     = {Machine Learning Systems: Design and Implementation},
  author    = {OpenMLSys Team},
  year      = {2022},
  url       = {https://openmlsys.github.io/},
  note      = {Open-source textbook, \url{https://github.com/openmlsys/openmlsys-zh}}
}
```

## License

This project is licensed under the [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License](https://creativecommons.org/licenses/by-nc-sa/4.0/).
