import inquirer
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from transformers import (AutoModelForSeq2SeqLM, AutoTokenizer,
                          SummarizationPipeline)

def getModelChoice():
    models = ["llama3", "llama2", "codellama", "mistral", "phi3"]

    questions = [
        inquirer.List(
            "model",
            message="Please select a model:",
            choices=models,
        ),
    ]

    answer = inquirer.prompt(questions)

    return answer["model"]

def returnTemplate():
    template = """
Given a script file in {language}, generate its documentation for each function. For each function in the script, document its name, arguments, return values, and a brief explanation of its logic.

Strictly use the following format for each function:

## Function Name: `function_name`

### Arguments
* `arg1` (type): Description of argument 1.
* `arg2` (type): Description of argument 2.
* ...

### Return Values
* `return_value1` (type): Description of return value 1.
* `return_value2` (type): Description of return value 2.
* ...

### Explanation of Function Logic:
1. Brief explanation of the function logic step by step.
2. ...
3. ...

Ensure that code within comments is not parsed and documented.

{code}
    """
    
    return template

def setupLangChain(model):
    llm = Ollama(model=model)

    template = returnTemplate()

    prompt = PromptTemplate(
        template=template,
        input_variables=["code", "language"]
    )

    chain = prompt | llm

    return chain

def createPipeline(checkpoint, device):
    '''
    Create a transformers model summarization pipeline.

    Arguments:
    checkpoint - model checkpoint
    device (integer) - either 0 or 1, to specify if there exists a GPU
    '''
    pipeline = SummarizationPipeline(
        model=AutoModelForSeq2SeqLM.from_pretrained(checkpoint),
        tokenizer=AutoTokenizer.from_pretrained(
            checkpoint,
            skip_special_tokens=True,
            legacy=False
        ),
        max_new_tokens=1024,
        device=device
    )

    return pipeline