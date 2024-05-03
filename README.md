# Language-agnostic Code Documentation Generation with LLMs & LangChain

A command-line tool leveraging LangChain and LLMs for language-agnostic code documentation.

# Problem Statement

- Fine-tune an LLM on a dataset of code snippets in different languages
	- Refer to this [link](https://www.mdpi.com/2073-8994/14/3/471) for datasets to explore
	- Codellama-7b, [StarCoder2-7b](https://huggingface.co/bigcode/starcoder2-7b), [StarCoderbase-3b](https://huggingface.co/bigcode/starcoderbase-3b)
- Record a score higher than the average for the different datasets using the above models in a mixture of experts (or depths?) model that can run on consumer h/w
- Showcase findings in fine-tuning and results on different benchmarks for languages
	- Evaluation metrics include: METEOR, BLEU-4
	- Benchmarks: [HumanEval](https://huggingface.co/datasets/openai_humaneval), [MultiPL-E](https://huggingface.co/datasets/nuprl/MultiPL-E)

# To-do 

- Get access to these papers
	- [Automatic Code Documentation Generation Using GPT-3](https://dl.acm.org/doi/10.1145/3551349.3559548)
- Structure content and findings in paper format
	- [x] Confirm Problem Statement
	- [x] Find more relevant papers and structure Literature Survey accordingly
	- [ ] Re-write abstract and introduction
- Explore
	- [ ] Dataset augmentation
	- [ ] Mergekit
	- [ ] [LLMAutoEval](https://github.com/mlabonne/llm-autoeval)
	- [ ] Claude 3
	- [ ] Quantization and model layer dropping
- Code
	- [ ] Update template to produce consistent responses
	- [ ] Test for language-agnostic generation
	- [ ] Clean code and add docstrings
    - [ ] Add ASCII art
    - [ ] Better status messages (probably use logs instead of prints in some places)
    - [ ] Clean up what's displayed to the user
	- [ ] Make sure it runs for directories

# References

1. [Code Documentation Generation task on *paperswithcode.com*](https://paperswithcode.com/task/code-documentation-generation)
2. [CodeSearchNet corpus on *paperswithcode.com*](https://paperswithcode.com/dataset/codesearchnet)
3. [CodeTrans model GitHub page](https://github.com/agemagician/CodeTrans)
4. [CodeTrans Python models for ST, TF, MT & MT-TF through HuggingFace search](https://huggingface.co/search/full-text?q=codetrans+code+documentation+generation+python&type=model)
5. [Code Docstring Corpus on GitHub](https://github.com/EdinburghNLP/code-docstring-corpus)
6. [Parallel Corpus for docstrings on ArXiv](https://arxiv.org/abs/1707.02275)
7. [Transformers tokenizer error with hotfix](https://discuss.huggingface.co/t/error-with-new-tokenizers-urgent/2847/3)
8. [CodeTrans T5 FT Dataset](https://www.dropbox.com/sh/488bq2of10r4wvw/AACs5CGIQuwtsD7j_Ls_JAORa/finetuning_dataset?dl=0&subfolder_nav_tracking=1)
9. Liu, X., Wang, D., Wang, A., Hou, Y., & Wu, L. (2021, March 31). HAConvGNN: Hierarchical Attention Based Convolutional Graph Neural Network for Code Documentation Generation in Jupyter Notebooks. arXiv.org. [https://arxiv.org/abs/2104.01002v2](https://arxiv.org/abs/2104.01002v2) 
10. Feng, Z., Guo, D., Tang, D., Duan, N., Feng, X., Gong, M., Shou, L., Qin, B., Liu, T., Jiang, D., & Zhou, M. (2020, February 19). CodeBERT: A Pre-Trained Model for Programming and Natural Languages. arXiv.org. [https://arxiv.org/abs/2002.08155v4](https://arxiv.org/abs/2002.08155v4) 
11. Elnaggar, A., Ding, W., Jones, L., Gibbs, T., Feher, T., Angerer, C., Severini, S., Matthes, F., & Rost, B. (2021, April 6). CodeTrans: Towards Cracking the Language of Silicon’s Code Through Self-Supervised Deep Learning and High Performance Computing. arXiv.org. [https://arxiv.org/abs/2104.02443v2](https://arxiv.org/abs/2104.02443v2) 
12. Luo, Q., Ye, Y., Liang, S., Zhang, Z., Qin, Y., Lu, Y., ... & Sun, M. (2024). RepoAgent: An LLM-Powered Open-Source Framework for Repository-level Code Documentation Generation. arXiv preprint arXiv:2402.16667.
13. Gromov, A., Tirumala, K., Shapourian, H., Glorioso, P., & Roberts, D. A. (2024). The Unreasonable Ineffectiveness of the Deeper Layers. arXiv preprint arXiv:2403.17887.
14. https://arxiv.org/pdf/2402.16667.pdf#page=9&zoom=100,401,853
15. [Summarizing Source Code using a Neural Attention Model](https://aclanthology.org/P16-1195.pdf)
16. [Huggingface LLM Leaderboards](https://huggingface.co/collections/open-llm-leaderboard/the-big-benchmarks-collection-64faca6335a7fc7d4ffe974a)
17. [HF BigCode Leaderboard](https://huggingface.co/spaces/bigcode/bigcode-models-leaderboard)
18. [IEEE Paper Template](https://www.ieee.org/conferences/publishing/templates.html)
19. [Purdue OWL's Guidelines for IEEE Papers](https://owl.purdue.edu/owl/research_and_citation/ieee_style/ieee_general_format.html)
---
