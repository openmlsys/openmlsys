# 贡献指南

> **注意：** 本项目的 v1 版本已归档（位于 `v1/` 目录），不再接受新的贡献。请将所有内容贡献提交至 v2（`v2/` 目录）。

---

## 仓库结构说明

```
openmlsys/
├── v2/                        # 第二版（当前活跃版本，接受贡献）
│   ├── zh_chapters/           # 中文章节源文件
│   │   ├── 00_chapter_preface/    # 各章目录（数字前缀 + 名称）
│   │   ├── 01_chapter_introduction/
│   │   ├── ...
│   │   ├── index.md           # 全书首页
│   │   └── SUMMARY.md         # 由脚本自动生成，勿手动编辑
│   ├── en_chapters/           # 英文章节源文件（结构与中文章节一致）
│   ├── books/zh/              # 中文 mdBook 配置（供构建使用）
│   ├── info/                  # 文档（本文件所在位置）
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

```bash
# 1. 安装 Rust 工具链
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# 2. 安装 mdBook
cargo install mdbook

# 3. 克隆仓库（需预先安装 Python 3）
git clone https://github.com/openmlsys/openmlsys.git
cd openmlsys
```

---

## 本地构建

### 构建 v2 中英文双版本

```bash
bash build_mdbook_v2.sh
```

构建产物输出至 `.mdbook-v2-zh/book`（中文）和 `.mdbook-v2/book`（英文）。

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

详细的自定义语法（公式、图片标签、文献引用、代码块等）及图片规范，请参阅 **[写作样式规范](style_zh.md)**。

---

## 提交流程

1. **Fork** 本仓库并创建功能分支：
   ```bash
   git checkout -b feat/chapter-xxx-section-yyy
   ```

2. **本地构建验证**：修改完成后运行 `bash build_mdbook_v2.sh`，确保无报错

3. **提交代码**：遵循语义化提交信息
   ```bash
   git commit -m "feat(zh): 新增第X章第Y节内容"
   git commit -m "feat(en): Add content for chapter X section Y"
   git commit -m "ci: update main.yml"
   ```
   常用前缀：`feat`（新内容）、`fix`（修正错误）、`refactor`（重组结构）、`style`（格式调整）、`ci`（构建流程更新）

4. **发起 Pull Request**：目标分支为 `main`，请使用 PR 模板：

   - [中文 PR 模板](.github/PULL_REQUEST_TEMPLATE/zh.md)
   - [英文 PR 模板](.github/PULL_REQUEST_TEMPLATE/en.md)

5. **代码审查**：PR要求至少有一位非本人Contributor进行检查，且github action将会自动验证新增内容是否可以编译通过

---

## 常见问题

**Q：如何添加新章节？**

- 在 `v2/zh_chapters/` 下新建 `chapter_<名称>/` 目录
- 创建 `index.md`，在其中使用 `toc` 块列出各节
- 在全书 `v2/zh_chapters/index.md` 的 `toc` 块中注册新章节
- 确保本地构建通过后再提交 PR

**Q：参考文献如何添加？**

在 `mlsys.bib` 中添加 BibTeX 格式的文献条目，然后在正文中使用 `:cite:\`key\`` 引用。

**Q：构建时提示找不到图片怎么处理？**

检查图片路径是否以 `../img/` 开头（相对于章节目录），以及图片文件是否已提交至 `img/` 目录。
