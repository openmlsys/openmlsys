# 贡献指南

> 首先，感谢所有参与到本教材写作的贡献者们，你们的贡献让本教材可以持续蓬勃地发展。

> **注意：** 本项目的 v1 版本已归档（位于 `v1/` 目录），不再接受新的贡献。请将所有内容贡献提交至 v2（`v2/` 目录）。

---

## 目录

- [贡献类型](#贡献类型)
- [仓库结构说明](#仓库结构说明)
- [环境准备](#环境准备)
- [本地构建](#本地构建)
- [写作规范](#写作规范)
- [提交流程](#提交流程)
- [常见问题](#常见问题)

---

## 贡献类型

欢迎以下几类贡献：

- **内容修订**：修正已有章节的笔误、表述错误或过时内容
- **新章节撰写**：认领并撰写 v2 中尚未完成的章节
- **译文同步**：将中文内容同步翻译为英文（或反向），保持 `zh_chapters/` 与 `en_chapters/` 一致
- **图片与代码**：补充示意图、代码示例、实验结果
- **工具与构建**：改进 `tools/` 下的预处理脚本或构建流程

> **建议：** 对于**新增内容**（如新章节、新小节）或**结构调整**（如章节重组、目录变更），建议在动手之前先[提交一个 Issue](https://github.com/openmlsys/openmlsys-zh/issues/new/choose) 与维护者讨论，确认方向和范围后再开始工作，避免无效劳动。

---

## 仓库结构说明

```
openmlsys/
├── v2/                        # 第二版（当前活跃版本，接受贡献）
│   ├── zh_chapters/           # 中文章节源文件
│   │   ├── chapter_xxx/       # 各章目录，包含 index.md 及各节 .md 文件
│   │   ├── index.md           # 全书首页
│   │   └── SUMMARY.md         # 由脚本自动生成，勿手动编辑
│   ├── en_chapters/           # 英文章节源文件（结构与中文章节一致）
│   ├── books/zh/              # 中文 mdBook 配置（供构建使用）
│   ├── docs/                  # 文档（本文件所在位置）
│   └── book.toml              # 英文版 mdBook 配置
├── v1/                        # 第一版（已归档）
├── img/                       # 全书共享图片资源
├── references/                # 参考文献目录
├── tools/                     # 构建与预处理脚本
│   ├── prepare_mdbook.py      # 核心预处理：解析自定义语法、生成 SUMMARY
│   └── mdbook_preprocessor.py # mdBook 预处理器入口
└── build_mdbook_v2.sh         # v2 一键构建脚本
```

**重要**：`SUMMARY.md` 由 `tools/prepare_mdbook_zh.py` 根据 `index.md` 中的 `toc` 块自动生成，**请勿手动修改**。

---

## 环境准备

本项目使用 [mdBook](https://rust-lang.github.io/mdBook/index.html) 驱动，构建前请确保安装以下依赖：

| 工具 | 用途 | 最低版本 |
|------|------|----------|
| git | 版本管理 | - |
| Python 3 | 运行预处理脚本 | 3.8+ |
| Rust 工具链 | 提供 `cargo` 以安装 mdBook | stable |
| mdBook | 构建 HTML 电子书 | 0.5.x |

### 安装步骤

```bash
# 1. 安装 Rust 工具链
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source "$HOME/.cargo/env"

# 2. 安装 mdBook
cargo install mdbook

# 3. 克隆仓库
git clone https://github.com/openmlsys/openmlsys-zh.git
cd openmlsys-zh
```

---

## 本地构建

### 构建 v2 中英文双版本

```bash
bash build_mdbook_v2.sh
```

构建产物输出至 `.mdbook-v2/book/cn/`（中文）和 `.mdbook-v2/book/`（英文）。

### 实时预览

```bash
# 中文版实时预览
cd v2/books/zh && mdbook serve --open
# 英文版实时预览
cd v2/ && mdbook serve --open
```

修改 `zh_chapters/` 或 `en_chapters/` 下的源文件后，浏览器将自动刷新。

> **注意**：预处理脚本会在每次构建时重新生成 `SUMMARY.md`，如遇构建报错请先检查 `index.md` 中 `toc` 块的格式是否正确。

---

## 写作规范

### 目录与文件组织

- 每章对应 `v2/<zh/en>_chapters/chapter_<名称>/` 目录
- 章节入口为 `index.md`，各节内容放在同目录下的独立 `.md` 文件中
- 在 `index.md` 中使用 `toc` 块声明本章的节结构（自动生成 SUMMARY）

```markdown
​```toc
:maxdepth: 2

section_one
section_two
​```
```

### 自定义语法

本项目的预处理器支持以下扩展语法，**请严格遵守**以确保构建正确：

**行内公式**

```markdown
模型学习映射 $f: \mathcal{X} \rightarrow \mathcal{Y}$。
```

**行间公式与标签**

```markdown
$$
\mathcal{L}_{CE} = -\sum_{i=1}^{N} y_i \log(\hat{y}_i)
$$
:eqlabel:`eq-cross-entropy-zh`
```

引用公式：`:eqref:\`eq-cross-entropy-zh\``

**图片与标签**

```markdown
![图片描述](../img/ch01/figure.png)
:width:`600px`
:label:`figure-label-zh`
```

引用图片：`:numref:\`figure-label-zh\``

**文献引用**

```markdown
感知机 :cite:`rosenblatt1958perceptron` 是最早期的神经网络模型之一。
```

参考文献条目统一维护在 `mlsys.bib` 中。

**代码块**

使用标准 Markdown 围栏代码块，标注语言类型：

````markdown
```python
import torch
```
````

### 图片规范

- 图片存放于 `img/ch<章节编号>/` 目录下，如 `img/ch01/`
- 文件名使用英文小写加连字符，如 `framework-architecture.png`
- 推荐格式：PNG、SVG
- 分辨率建议：≥ 150 dpi，宽度不超过 1200px


---

## 提交流程

> **提示：** 若你计划新增内容或调整文档结构，请先完成第 0 步——提 Issue 讨论，获得确认后再进行后续步骤。

0. **（新增内容 / 结构调整时必做）提 Issue 讨论**：在 [GitHub Issues](https://github.com/openmlsys/openmlsys-zh/issues/new/choose) 中简要描述你的计划（涉及章节、改动原因、预期效果），待维护者确认可行后再开始动手，以确保工作方向与项目规划一致。

1. **Fork** 本仓库并创建功能分支：
   ```bash
   git checkout -b feat/chapter-xxx-section-yyy
   ```

2. **本地构建验证**：修改完成后运行 `bash build_mdbook_v2.sh`，确保无报错

3. **提交代码**：遵循语义化提交信息
   ```bash
   git commit -m "feat(zh): 新增第X章第Y节内容"
   git commit -m "feat(en): Add content for chapter X section Y"
   ```
   常用前缀：`feat`（新内容）、`fix`（修正错误）、`refactor`（重组结构）、`style`（格式调整）、`ci`（构建流程更新）

4. **发起 Pull Request**：目标分支为 `main`，请使用我们提供的 PR 模板：

   - [中文 PR 模板](https://github.com/openmlsys/openmlsys-zh/compare/main...your-branch?template=zh.md)（将 `your-branch` 替换为你的分支名）
   - [英文 PR 模板](https://github.com/openmlsys/openmlsys-zh/compare/main...your-branch?template=en.md)

   模板中包含变更说明、涉及章节、关联 Issue 及提交前检查清单，请如实填写。

   > **提示：** 如果你发现了笔误或内容问题但暂时没有时间修改，欢迎直接[提交 Issue](https://github.com/openmlsys/openmlsys-zh/issues/new/choose) 告知我们，这同样是宝贵的贡献！

5. **代码审查**：维护者将对内容的准确性、格式规范性进行审查，请耐心等待并响应反馈
   - 提交后请关注PR中github action状态，只有自动检查通过的PR才会被正式合并到本仓库内

---

## 常见问题

**Q：我可以为 v1 提交修改吗？**

不可以。v1 已归档，仅保留历史记录，不再接受任何形式的贡献。请将所有贡献提交至 `v2/zh_chapters/`。

**Q：`SUMMARY.md` 构建后被覆盖了怎么办？**

这是正常行为。`SUMMARY.md` 由脚本自动生成，不应手动编辑。若需调整章节顺序或结构，请修改对应章节 `index.md` 中的 `toc` 块。

**Q：如何添加新章节？**

- 在 `v2/zh_chapters/` 下新建 `chapter_<名称>/` 目录
- 创建 `index.md`，在其中使用 `toc` 块列出各节
- 在全书 `v2/zh_chapters/index.md` 的 `toc` 块中注册新章节
- 确保本地构建通过后再提交 PR

**Q：参考文献如何添加？**

在 `mlsys.bib` 中添加 BibTeX 格式的文献条目，然后在正文中使用 `:cite:\`key\`` 引用。

**Q：构建时提示找不到图片怎么处理？**

检查图片路径是否以 `../img/` 开头（相对于章节目录），以及图片文件是否已提交至 `img/` 目录。

---

*如有其他问题，欢迎在 [GitHub Issues](https://github.com/openmlsys/openmlsys-zh/issues) 中提出。*
