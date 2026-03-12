# 参考文献引用方式

所有参考文献统一维护在 `mlsys.bib` 中。

## 添加文献条目

在 `mlsys.bib` 中添加 BibTeX 格式的条目，添加前请先检索是否已存在同名 key：

```bibtex
@inproceedings{cnn2015,
  title    = {CNN},
  author   = {xxx},
  year     = {2015},
  keywords = {xxx}
}
```

## 正文引用

引用时前面需要有一个空格：

1. 单篇参考文献
   ```
   这篇文章参考了论文 :cite:`cnn2015`
   ```

2. 多篇参考文献用逗号分隔
   ```
   这篇文章参考了论文 :cite:`cnn2015,rnn2015`
   ```
