get_ipython().run_line_magic('pip', 'install -q transformers sentencepiece datasets nltk accelerate')

# In[2]:

from transformers import AutoTokenizer, AutoModelForCausalLM, RobertaTokenizer, T5Tokenizer, T5ForConditionalGeneration, SummarizationPipeline
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from datasets import load_dataset
import tokenize
import io

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

# In[5]:

codeTransModel = AutoModelWithLMHead.from_pretrained("SEBIS/code_trans_t5_base_source_code_summarization_python_transfer_learning_finetune")
codeTransTokenizer = AutoTokenizer.from_pretrained("SEBIS/code_trans_t5_base_source_code_summarization_python_transfer_learning_finetune", skip_special_tokens=True)

# In[6]:

codeT5Model = T5ForConditionalGeneration.from_pretrained('Salesforce/codet5-base-multi-sum')
codeT5Tokenizer = RobertaTokenizer.from_pretrained('Salesforce/codet5-base-multi-sum', skip_special_tokens=True)

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
