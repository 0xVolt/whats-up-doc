#!/usr/bin/env python
# coding: utf-8

# <a href="https://colab.research.google.com/github/0xVolt/whats-up-doc/blob/main/src/experimental-notebooks/compare-models.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# # Compare Various HuggingFace Models for CDG by `SmoothedBLEU` Score
# 
# ## Purpose
# 
# The purpose of this notebook is to figure out which models will work best for our CLI app. We will calculate and compare these select models by their smoothed BLEU scores and possibly look into fine-tuning them with [this dataset](https://www.dropbox.com/sh/488bq2of10r4wvw/AACs5CGIQuwtsD7j_Ls_JAORa/finetuning_dataset?dl=0&subfolder_nav_tracking=1).
# 
# ## Models
# 
# These are the models we'll create inference points for and load in this notebook.
# 1. [SEBIS/code_trans_t5_base_code_documentation_generation_python](https://huggingface.co/SEBIS/code_trans_t5_base_code_documentation_generation_python)
# 2. [Salesforce/codet5-base-multi-sum](https://huggingface.co/Salesforce/codet5-base-multi-sum)
# 3. [google/flan-t5-small](https://huggingface.co/google/flan-t5-small)
# 
# The models listed above have been fine-tuned on the CodeSearchNet dataset across various programming languages for PL-NL sequence-to-sequence tasks.

# ## Install Dependencies

# In[1]:


get_ipython().run_line_magic('pip', 'install -q transformers sentencepiece datasets nltk accelerate')


# In[2]:


from transformers import AutoTokenizer, AutoModelWithLMHead, RobertaTokenizer, T5Tokenizer, T5ForConditionalGeneration, SummarizationPipeline
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from datasets import load_dataset
import tokenize
import io


# ## Define Evaluation Metric

# In[3]:


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


# ## Define Python Tokenizer

# In[4]:


def pythonTokenizer(line):
    result = []
    line = io.StringIO(line)

    for tokenType, token, start, end, line in tokenize.generate_tokens(line.readline):
        if (not tokenType == tokenize.COMMENT):
            if tokenType == tokenize.STRING:
                result.append("CODE_STRING")
            elif tokenType == tokenize.NUMBER:
                result.append("CODE_INTEGER")
            elif (not token == "\n") and (not token == "    "):
                result.append(str(token))
                
    return ' '.join(result)


# ## Define Models

# ### CodeTransT5

# In[5]:


codeTransModel = AutoModelWithLMHead.from_pretrained("SEBIS/code_trans_t5_base_source_code_summarization_python_transfer_learning_finetune")
codeTransTokenizer = AutoTokenizer.from_pretrained("SEBIS/code_trans_t5_base_source_code_summarization_python_transfer_learning_finetune", skip_special_tokens=True)


# ### CodeT5

# In[6]:


codeT5Model = T5ForConditionalGeneration.from_pretrained('Salesforce/codet5-base-multi-sum')
codeT5Tokenizer = RobertaTokenizer.from_pretrained('Salesforce/codet5-base-multi-sum', skip_special_tokens=True)


# ### FlanT5 

# In[7]:


flanT5Model = T5ForConditionalGeneration.from_pretrained("google/flan-t5-small", device_map="auto")
flanT5Tokenizer = T5Tokenizer.from_pretrained("google/flan-t5-small", skip_special_tokens=True)


# ## Create Pipelines

# In[8]:


codeTransPipeline = SummarizationPipeline(
    model=codeTransModel,
    tokenizer=codeTransTokenizer,
    device=0
)


# In[9]:


codeT5Pipeline = SummarizationPipeline(
    model=codeT5Model,
    tokenizer=codeT5Tokenizer,
    device=0
)


# In[11]:


flanPipeline = SummarizationPipeline(
    model=flanT5Model,
    tokenizer=flanT5Tokenizer,
)


# ## Sample Code

# In[12]:


code = '''

def is_prime(number):
    if number <= 1:
        return False
    elif number <= 3:
        return True
    elif number % 2 == 0 or number % 3 == 0:
        return False
    i = 5
    while i * i <= number:
        if number % i == 0 or number % (i + 2) == 0:
            return False
        i += 6
    return True
        
''' #@param {type:"raw"}

tokenizedCode = pythonTokenizer(code)
label = "A code block in Python to check whether a number is prime or not."


# ## Prompt Models

# In[22]:


codeTransOutput = codeTransPipeline([tokenizedCode])[0]['summary_text']
codeT5Output = codeT5Pipeline([tokenizedCode])[0]['summary_text']
flanOutput = flanPipeline([tokenizedCode])[0]['summary_text']


# ## Create Dictionary of Predictions

# In[23]:


calculateSmoothedBLEU(codeTransOutput, label)


# In[24]:


predictions = {
    'codeTrans': {
        'output': codeTransOutput,
        'score': calculateSmoothedBLEU(codeTransOutput, label)
    },
    'codeT5': {
        'output': codeT5Output,
        'score': calculateSmoothedBLEU(codeT5Output, label)
    },
    'flanT5': {
        'output': flanOutput,
        'score': calculateSmoothedBLEU(flanOutput, label)
    }
}


# In[25]:


predictions


# ---
