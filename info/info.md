## 环境安装
机器学习系统书籍部署在GitHub是依赖于mdbook工具实现的。我们推荐使用rust的原生包管理器cargo安装mdbook。
```bash
# 安装rust工具链，获取cargo
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
cargo install mdbook
```

## 编译HTML版本
在编译前先下载[openmlsys-zh](https://github.com/openmlsys/openmlsys-zh) ， 所有的编译命令都在这个文件目录内执行。
```bash
 git clone https://github.com/openmlsys/openmlsys-zh.git
 cd openmlsys-zh
```
使用mdbook工具编译HTML。 请尽量使用build_mdbook.sh脚本进行编译，保证首页正确合并到书籍中去。
```bash
sh build_mdbook.sh
# 中文版本
sh build_mdbook_zh.sh
```

生成的html会在`.mdbook/book`或者`.mdbook-zh/book`下。此时我们可以使用`tools/assemble_docs_publish_tree.py`组装最终的双语发布版本，然后将其拷贝至openmlsys.github.io的docs发布。

具体工作流可以参考`.github/workflows/update_docs.yml`

## 样式规范

贡献请遵照本教程的[样式规范](style.md)。

## 中英文术语对照

翻译请参照[中英文术语对照](terminology.md)。
