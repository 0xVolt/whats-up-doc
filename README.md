# Language-agnostic Code Documentation with LLMs & LangChain

A command-line tool leveraging LangChain and LLMs for language-agnostic code documentation.

## TODO
- [X] Setup parser
  - [X] Finish metadata logging
  - [X] Fix assignment statement parser
  - [X] Pre process code before passing it to the parser
  - [X] Code `BodyCount` attribute O.O
  - [X] Move assignment parser into `multi_parser`
  - [ ] Fix `relativePath` attribute when dealing with multiple files
- [ ] Fix `utils` package
  - [X] Move parser to `utils` package
  - [ ] Smooth over `utils` package functions
  - [ ] Rename modules with logical names
- [ ] Add docstrings to functions
- [ ] Setup CLI
  - [ ] Add ASCII art
  - [ ] Implement logic to check `BodyCount` attribute for block groups
  - [ ] Fix/circumvent `yaspin` spinner flicker
  - [ ] Setup multi-model select
  - [ ] Ensure models work for C++/JS (langchain dependency check)
    - [ ] May need to setup another model to work with another language by default
  - [ ] Setup markdown generator
    - [ ] Generate text file and then parse and add `md` syntax

## Resources
1. [Code Documentation Generation task on *paperswithcode.com*](https://paperswithcode.com/task/code-documentation-generation)
2. [CodeSearchNet corpus on *paperswithcode.com*](https://paperswithcode.com/dataset/codesearchnet)
3. [CodeTrans model GitHub page](https://github.com/agemagician/CodeTrans)
4. [CodeTrans Python models for ST, TF, MT & MT-TF through HuggingFace search](https://huggingface.co/search/full-text?q=codetrans+code+documentation+generation+python&type=model)
5. [Code Docstring Corpus on GitHub](https://github.com/EdinburghNLP/code-docstring-corpus)
6. [Parallel Corpus for docstrings on ArXiv](https://arxiv.org/abs/1707.02275)
7. [Transformers tokenizer error with hotfix](https://discuss.huggingface.co/t/error-with-new-tokenizers-urgent/2847/3)
8. [CodeTrans T5 FT Dataset](https://www.dropbox.com/sh/488bq2of10r4wvw/AACs5CGIQuwtsD7j_Ls_JAORa/finetuning_dataset?dl=0&subfolder_nav_tracking=1)

---
