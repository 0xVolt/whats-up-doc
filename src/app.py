import typer
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.llms import GPT4All
from langchain.prompts import PromptTemplate
from transformers import (AutoModelForSeq2SeqLM, AutoTokenizer,
                          SummarizationPipeline)
from yaspin import yaspin

from utils import *

app = typer.Typer()
spinner = yaspin()


@app.command()
def generate(
    path: str,
    model: str = typer.Argument(None),
    output: str = 'output.txt'
):
    '''
    Typer command to generate the documentation for an input script file.

    Arguments:
    filePath (string) - path to the input file
    model (string) - string to specify which model to use when generating documentation
    '''
    
    if model is None:
        model = model_utils.getModelChoice()
    
    print(f"Arguments specified:")
    print(f"File Path: {path}")
    print(f"Model: {model}\n")

    functionBodies = parser_utils.extractFunctionsAsList(path)
    
    # with open(output, 'w') as file:
    
    print(functionBodies[0])
    
    llmChain = model_utils.setupLangChain(model)
    response = model_utils.returnInferenceFromLangChain(llmChain, functionBodies[0])

    print(response)

@app.command()
def easter():
    '''
    An easter egg for the keen eyed open-source contributor.
    '''
    print("This is a test command! If you're here, that means you've discovered something pretty cool in our code-base.\nCongrats and thanks for using our app!")


if __name__ == "__main__":
    app()