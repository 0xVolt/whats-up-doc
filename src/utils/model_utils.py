import inquirer
from .file_utils import returnModelLocalPath
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.llms import GPT4All
from langchain.prompts import PromptTemplate
from transformers import (AutoModelForSeq2SeqLM, AutoTokenizer,
                          SummarizationPipeline)


def getModelChoice():
    models = ["mistral-7b-instruct", "orca-mini-3b"]
    
    questions = [
        inquirer.List(
            "model",
            message="Select a model:",
            choices=models,
        ),
    ]
    
    answer = inquirer.prompt(questions)
    
    return answer["model"]


def setupLangChain(model, batches=4, threads=8, nPredict=1024):
    path = returnModelLocalPath(model)
    
    # Callbacks support token-wise streaming
    callbacks = [StreamingStdOutCallbackHandler()]

    # Verbose is required to pass to the callback manager
    llm = GPT4All(
        model=path, 
        callbacks=callbacks, 
        verbose=True,
        n_batch=batches,
        n_threads=threads,
        n_predict=nPredict,
    )
    
    template = """
Here's my function in Python:

{function}

Given the definition of a function in Python, generate it's documentation. I want it complete with fields like function name, function arguments and return values as well as a detailed explanation of how the function logic works line-by-line. Make it concise and informative to put the documentation into a project.
    """
    
    prompt = PromptTemplate(
        template=template,
        input_variables=["function"],
    )
    
    llmChain = LLMChain(
        prompt=prompt, 
        llm=llm,
    )
    
    return llmChain



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