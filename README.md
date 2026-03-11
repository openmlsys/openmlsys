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

本书分为基础篇、进阶篇和扩展篇三个部分：

### 基础篇

| 章节 | 内容 |
|------|------|
| [编程接口](chapter_programming_interface/) | 框架接口设计哲学、机器学习工作流、深度学习模型定义、C/C++ 框架开发 |
| [计算图](chapter_computational_graph/) | 计算图基本构成、生成方法、调度策略、自动微分 |

### 进阶篇

| 章节 | 内容 |
|------|------|
| [编译器前端和中间表示](chapter_frontend_and_ir/) | 类型推导、中间表示（IR）、自动微分、常见优化 Pass |
| [编译器后端和运行时](chapter_backend_and_runtime/) | 计算图优化、算子选择、内存分配、计算调度与执行 |
| [硬件加速器](chapter_accelerator/) | GPU/Ascend 架构原理、高性能编程接口（CUDA/CANN） |
| [数据处理框架](chapter_data_processing/) | 易用性、高效性、保序性、分布式数据处理 |
| [模型部署](chapter_model_deployment/) | 模型转换、模型压缩、模型推理、安全保护 |
| [分布式训练](chapter_distributed_training/) | 数据并行、模型并行、流水线并行、集合通讯、参数服务器 |

### 扩展篇

| 章节 | 内容 |
|------|------|
| [深度学习推荐系统](chapter_recommender_system/) | 推荐系统原理、大规模工业场景架构设计 |
| [联邦学习系统](chapter_federated_learning/) | 联邦学习方法、隐私保护、系统实现 |
| [强化学习系统](chapter_reinforcement_learning/) | 单智能体/多智能体强化学习系统 |
| [可解释性 AI 系统](chapter_explainable_AI/) | 可解释 AI 方法与落地实践 |
| [机器人学习系统](chapter_rl_sys/) | 机器人感知、规划、控制与系统安全 |

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
sh build_mdbook_zh.sh
# 生成结果位于 .mdbook-zh/book
```

更多细节请参考 [构建指南](info/info.md)。

## 贡献指南

我们欢迎任何形式的贡献，包括：

- **勘误**：发现文字或图片错误，请创建 Issue 并 @ [章节编辑](info/editors.md)，或直接提交 PR。
- **内容更新**：提交 PR 更新或添加 Markdown 文件。
- **新章节**：欢迎社区对元学习系统、自动并行、集群调度、绿色 AI、图学习等主题贡献章节。

提交前请阅读：
- [写作风格指南](info/style.md)
- [中英文术语对照](info/terminology.md)

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
