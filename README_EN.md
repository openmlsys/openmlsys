<p align="center">
  <img src="static/logo-with-text.png" alt="OpenMLSys Logo" width="400"/>
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

The book is organized into three parts: Fundamentals, Advanced Topics, and Extensions.

### Part I: Fundamentals

| Chapter | Content |
|---------|---------|
| [Programming Interface](chapter_programming_interface/) | Framework API design, ML workflows, deep learning model definition, C/C++ framework development |
| [Computational Graph](chapter_computational_graph/) | Graph components, generation methods, scheduling strategies, automatic differentiation |

### Part II: Advanced Topics

| Chapter | Content |
|---------|---------|
| [Compiler Frontend & IR](chapter_frontend_and_ir/) | Type inference, intermediate representation (IR), automatic differentiation, common optimization passes |
| [Compiler Backend & Runtime](chapter_backend_and_runtime/) | Graph optimization, operator selection, memory allocation, compute scheduling and execution |
| [Hardware Accelerators](chapter_accelerator/) | GPU/Ascend architecture, high-performance programming interfaces (CUDA/CANN) |
| [Data Processing](chapter_data_processing/) | Usability, efficiency, order preservation, distributed data processing |
| [Model Deployment](chapter_model_deployment/) | Model conversion, compression, inference, and security |
| [Distributed Training](chapter_distributed_training/) | Data parallelism, model parallelism, pipeline parallelism, collective communication, parameter servers |

### Part III: Extensions

| Chapter | Content |
|---------|---------|
| [Recommender Systems](chapter_recommender_system/) | Recommendation principles, large-scale industrial architecture |
| [Federated Learning](chapter_federated_learning/) | Federated learning methods, privacy protection, system implementation |
| [Reinforcement Learning Systems](chapter_reinforcement_learning/) | Single-agent and multi-agent RL systems |
| [Explainable AI Systems](chapter_explainable_AI/) | XAI methods and production practices |
| [Robot Learning Systems](chapter_rl_sys/) | Robot perception, planning, control, and system safety |

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
sh build_mdbook.sh
# Output is in .mdbook/book
```

For more details, see the [Build Guide](info/info.md).

## Contributing

We welcome all forms of contributions, including:

- **Errata**: If you find text or figure errors, please open an Issue and @ the [chapter editors](info/editors.md), or submit a PR directly.
- **Content updates**: Submit PRs to update or add Markdown files.
- **New chapters**: We welcome community contributions on topics such as meta-learning systems, automatic parallelism, cluster scheduling, green AI, and graph learning.

Before contributing, please read:
- [Writing Style Guide](info/style.md)
- [Terminology Guide](info/terminology.md)

## Community

Join our WeChat group by scanning the QR code in [info/mlsys_group.png](info/mlsys_group.png).

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
