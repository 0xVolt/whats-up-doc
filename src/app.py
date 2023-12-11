import typer
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.llms import GPT4All
from langchain.prompts import PromptTemplate
from transformers import (AutoModelForSeq2SeqLM, AutoTokenizer,
                          SummarizationPipeline)
from yaspin import yaspin
import gc

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
    
    llmChain = model_utils.setupLangChain(model)

    functionBodies = parser_utils.extractFunctionsAsList(path)
    print(functionBodies)
    
    code = file_utils.readFile(path)
    with open(output, 'w') as file:
        file.write(llmChain.run({'functions': code}))


    # with open(output, 'w') as file:
    #     response1 = llmChain.run({'function': functionBodies[0]})
    #     file.write(response1)
        
    #     print('\n\n')
    #     gc.collect()
        
    #     response2 = llmChain.run({'function': functionBodies[1]})
    #     file.write(response2)
        
    #     print('\n\n')
    #     gc.collect()


@app.command()
def easter():
    '''
    An easter egg for the keen eyed open-source contributor.
    '''
    print("This is a test command! If you're here, that means you've discovered something pretty cool in our code-base.\nCongrats and thanks for using our app!")


if __name__ == "__main__":
    app()