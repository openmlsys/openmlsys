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
  <b>中文</b> | <a href="README_EN.md">English</a>
</p>

---

# 机器学习系统：设计和实现

本开源项目讲解现代机器学习系统的设计原理和实现经验，涵盖从编程接口、计算图、编译器到分布式训练的完整技术栈。

**在线阅读：** [openmlsys.github.io](https://openmlsys.github.io/)

## 目录

- [适用读者](#适用读者)
- [内容介绍](#内容介绍)
- [构建指南](#构建指南)
- [贡献指南](#贡献指南)
- [社区](#社区)
- [许可证](#许可证)

## 适用读者

- **学生**：掌握机器学习基础理论后，希望深入了解现代机器学习系统设计与实现的同学。
- **科研人员**：需要开发自定义算子（Custom Operators）或利用分布式执行实现大模型的研究者。
- **开发人员**：负责机器学习基础设施建设，需要对系统性能调优和深度定制的工程师。

## 内容介绍

本书（第二版）共分9章：

| 章节 | 内容 |
|------|------|
| [第1章 导论](v2/zh_chapters/01_chapter_introduction/) | 机器学习系统架构和技术栈概述 |
| [第2章 编程接口与计算图](v2/zh_chapters/02_chapter_programming_and_graph/) | 张量抽象、自动微分、图表示与执行 |
| [第3章 AI加速器与编程](v2/zh_chapters/03_chapter_accelerator/) | GPU 架构与 CUDA/Triton/CUTLASS 编程模型 |
| [第4章 AI编译器与运行时系统](v2/zh_chapters/04_chapter_compiler_and_runtime/) | IR 设计、图优化、算子生成与运行时执行 |
| [第5章 数据处理系统](v2/zh_chapters/05_chapter_data_processing/) | 数据加载、数据管道和分布式数据处理 |
| [第6章 训练系统](v2/zh_chapters/06_chapter_training_systems/) | 单节点与分布式训练、并行策略与训练优化 |
| [第7章 模型服务](v2/zh_chapters/07_chapter_model_serving/) | 推理优化、在线服务与模型管理 |
| [第8章 强化学习系统](v2/zh_chapters/08_chapter_rl_systems/) | 强化学习管道、环境交互与 RL 系统设计 |
| [第9章 大规模GPU集群管理](v2/zh_chapters/09_chapter_gpu_cluster/) | GPU 调度、资源管理与大规模训练基础设施 |

## 更新日志

| 日期 | 事件 |
|------|------|
| 2022-01 | 项目初始化，开始中文内容编写 |
| 2022-05 | 完成扩展篇各章节（联邦学习、强化学习、可解释 AI） |
| 2023-05 | 适配 MindSpore 2.0 |
| 2026-03 | 中英文双语构建架构重构；启动英文版 |

## 构建指南

### 环境依赖

- curl
- git
- Python 3

### 安装步骤

```bash
# 克隆仓库
git clone https://github.com/openmlsys/openmlsys-zh.git
cd openmlsys-zh

# 安装rust toolchain 
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# 安装mdbook
cargo install mdbook
```

### 编译HTML

```bash
sh build_mdbook_v2.sh
# 英文版生成结果位于 .mdbook-v2/book
# 中文版生成结果位于 .mdbook-v2-zh/book
```

更多细节请参考 [构建指南](v2/info/info.md)。

## 贡献指南

我们欢迎任何形式的贡献，详细流程请参阅 **[贡献指南](v2/info/CONTRIBUTING_zh.md)**。

提交前请阅读：
- [写作样式规范](v2/info/style_zh.md)
- [中英文术语对照](v2/info/terminology.md)

## 社区

<p align="center">
  <img src="info/mlsys_group.png" alt="微信群二维码" width="200"/>
  <br/>
  扫码加入微信交流群
</p>

## 引用

如果本书对您的研究或工作有所帮助，请使用以下格式引用：

**文本格式：**

> OpenMLSys Team. *机器学习系统：设计和实现*. 2022. https://openmlsys.github.io/

**BibTeX：**

```bibtex
@book{openmlsys2022,
  title     = {机器学习系统：设计和实现},
  author    = {OpenMLSys Team},
  year      = {2022},
  url       = {https://openmlsys.github.io/},
  note      = {开源教材，\url{https://github.com/openmlsys/openmlsys-zh}}
}
```

## 许可证

本项目采用 [知识共享 署名-非商业性使用-相同方式共享 4.0 国际许可协议](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh) 授权。
