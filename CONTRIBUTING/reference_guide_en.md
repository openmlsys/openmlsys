# Reference Citation Guide

All references are maintained in `mlsys.bib`.

## Adding Bibliography Entries

Add a BibTeX entry to `mlsys.bib`. Before adding, search for existing keys to avoid duplicates:

```bibtex
@inproceedings{cnn2015,
  title    = {CNN},
  author   = {xxx},
  year     = {2015},
  keywords = {xxx}
}
```

## In-text Citations

A space is required before the citation directive:

1. Single reference
   ```
   This article references the paper :cite:`cnn2015`
   ```

2. Multiple references separated by commas
   ```
   This article references the papers :cite:`cnn2015,rnn2015`
   ```
