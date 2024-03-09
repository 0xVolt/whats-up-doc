# Language-agnostic Code Documentation with LLMs & LangChain

A command-line tool leveraging LangChain and LLMs for language-agnostic code documentation.

## Usage

_Under maintenance._

Run `install.sh`. If you have a GPU on your machine, use the `-g` flag to install the correct dependencies for `llama-cpp`. When in doubt, always create a new Python virtual environment, like so:
1. `python3 -m venv <path_to_venv>`
2. `source venv/bin/activate` for Linux. The command differs with OS.
3. `chmod +x ./install.sh`
4. `./install.sh`

## TODO

- [ ] Remove GPT4All dependency
  - [ ] Check out Claude 3
- [ ] Eliminate need for `llama-cpp` due to dependency issues
- [ ] Clean code and add docstrings
- [ ] Pretty up CLI
  - [ ] Add ASCII art
  - [ ] Better status messages (probably use logs instead of prints in some places)
  - [ ] Clean up what's displayed to the user

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
