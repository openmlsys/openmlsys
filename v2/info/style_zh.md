# 写作样式规范

本文档规定了 v2 章节内容的写作格式与样式要求。所有贡献者在撰写或修改内容时请遵循以下规范。

> **注意：** LaTeX 转 Markdown 的工作流已**废弃**。v2 中所有内容直接使用 Markdown 书写，无需通过 Pandoc 等工具转换。

---

## 目录

- [文件结构](#文件结构)
- [自定义语法](#自定义语法)
- [图片规范](#图片规范)
- [表格规范](#表格规范)
- [代码块规范](#代码块规范)
- [参考文献](#参考文献)

---

## 文件结构

- 每章对应 `v2/zh_chapters/chapter_<名称>/` 目录
- 章节入口为 `index.md`，各节内容放在同目录下的独立 `.md` 文件中
- 在 `index.md` 中使用 `toc` 块声明本章的节结构（脚本据此自动生成 `SUMMARY.md`）：

```markdown
​```toc
:maxdepth: 2

section_one
section_two
​```
```

---

## 自定义语法

本项目的预处理器支持以下扩展 Markdown 语法，**请严格遵守**以确保构建正确。

### 行内公式

```markdown
模型学习映射 $f: \mathcal{X} \rightarrow \mathcal{Y}$。
```

### 行间公式与标签

公式标签格式为 `:eqlabel:\`<标签名>\``，标签名建议以语言后缀结尾（如 `-zh`）以避免中英文冲突：

```markdown
$$
\mathcal{L}_{CE} = -\sum_{i=1}^{N} y_i \log(\hat{y}_i)
$$
:eqlabel:`eq-cross-entropy-zh`
```

引用公式：`:eqref:\`eq-cross-entropy-zh\``

### 图片与标签

```markdown
![图片描述](../img/ch01/figure.png)
:width:`600px`
:label:`figure-label-zh`
```

引用图片：`:numref:\`figure-label-zh\``

### 章节引用

在节标题后添加标签：

```markdown
### 节标题
:label:`my-section-zh`
```

引用该节：`:ref:\`my-section-zh\``

### 文献引用

```markdown
感知机 :cite:`rosenblatt1958perceptron` 是最早期的神经网络模型之一。
```

多篇文献用逗号分隔：`:cite:\`paper1,paper2\``

参考文献条目统一维护在 `mlsys.bib` 中（详见[参考文献](#参考文献)一节）。

---

## 图片规范

### 存放位置

图片存放于 `img/ch<章节编号>/` 目录下，如 `img/ch01/`。图片文件须随 PR 一起提交。

### 文件命名

使用英文小写加连字符，如 `framework-architecture.png`。

### 格式

| 格式 | 适用场景 |
|------|---------|
| SVG  | 自行绘制的流程图、示意图（矢量，缩放不失真），需去除白色背景 |
| PNG  | 截图、照片、含复杂渐变的图片 |

推荐使用 PPT、draw.io 等工具绘制后导出。**不得使用网络图片**（版权风险）。

### 分辨率与尺寸

- 推荐分辨率：≥ 150 dpi
- 宽度不超过 1200 px
- Markdown 中通过 `:width:` 指定显示宽度（建议 600–800 px）

### 排版

相邻两张图之间须有足够的文字说明，避免图片紧邻。

---

## 表格规范

使用标准 Markdown 表格语法，并为需要引用的表格打标签：

```markdown
| 列名 1 | 列名 2 | 列名 3 |
|--------|--------|--------|
| 值 1   | 值 2   | 值 3   |
:label:`table-label-zh`
```

引用表格：`:numref:\`table-label-zh\``

---

## 代码块规范

使用标准 Markdown 围栏代码块，必须标注语言类型：

````markdown
```python
import torch
import torch.nn as nn
```
````

常用语言标识：`python`、`bash`、`cpp`、`markdown`、`text`。

---

## 参考文献

在 `mlsys.bib` 中添加 BibTeX 格式的文献条目：

```bibtex
@inproceedings{key2015,
  title  = {Title of the Paper},
  author = {Author, A. and Author, B.},
  year   = {2015}
}
```

**注意**：`mlsys.bib` 中不可出现重复的 key，添加前请先检索是否已存在。

正文引用示例：

```markdown
这篇文章参考了论文 :cite:`cnn2015`。
多篇文献引用：:cite:`cnn2015,rnn2015`。
```
