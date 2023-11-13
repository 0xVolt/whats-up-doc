#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/0xVolt/whats-up-doc/blob/main/src/experimental-notebooks/code-t5-code-documentation.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# In[15]:


get_ipython().run_line_magic('pip', 'install -q --no-cache transformers datasets nltk sentencepiece')


# In[16]:


from transformers import RobertaTokenizer, T5Tokenizer, T5ForConditionalGeneration
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from datasets import load_dataset


# In[17]:


def calculateSmoothedBLEU(reference, candidate):
    """
    Calculate the Smoothed BLEU-4 score between a reference string and a candidate string.

    Args:
    reference (str): The reference (ground truth) string.
    candidate (str): The candidate (generated) string.

    Returns:
    float: The Smoothed BLEU-4 score.
    """
    reference_tokens = reference.split()
    candidate_tokens = candidate.split()

    smoother = SmoothingFunction()
    bleu_score = sentence_bleu([reference_tokens], candidate_tokens, smoothing_function=smoother.method1)

    return bleu_score


# In[25]:


tokenizer = RobertaTokenizer.from_pretrained('Salesforce/codet5-base-multi-sum')
model = T5ForConditionalGeneration.from_pretrained('Salesforce/codet5-base-multi-sum')

# tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-small")
# model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-small")


# In[26]:


data = load_dataset("code_search_net", "python")['test']
data


# In[37]:


testFunction = '''
def calculateSmoothedBLEU(reference, candidate):
    reference_tokens = reference.split()
    candidate_tokens = candidate.split()

    smoother = SmoothingFunction()
    bleu_score = sentence_bleu([reference_tokens], candidate_tokens, smoothing_function=smoother.method1)

    return bleu_score
'''


# In[32]:


idx = 1600

text = data['func_code_string'][idx]
label = data['func_documentation_string'][idx]

labelFirstLine = label.split("\n")[0]

print(f"Text:\n{text}\n\nLabel:\n{label}\n\nLabel's First Line:\n{labelFirstLine}")


# In[38]:


input_ids = tokenizer(testFunction, return_tensors="pt").input_ids
generated_ids = model.generate(input_ids, max_length=20)


# In[39]:


predicted = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
predicted


# In[35]:


calculateSmoothedBLEU(label, predicted)


# In[36]:


calculateSmoothedBLEU(labelFirstLine, predicted)

