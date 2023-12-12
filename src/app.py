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
    
    # model = 'mistral-7b-instruct'

    print(f"Arguments specified:")
    print(f"File Path: {path}")
    print(f"Model: {model}\n")
    
    # modelPath = file_utils.returnModelLocalPath(model)
    functions = parser_utils.extractFunctionsAsList(path)
    
    # modelPath = r"C:\Users\deshi\Code\gpt4all-models\mistral-7b-instruct-v0.1.Q4_0.gguf"
    
    # Callbacks support token-wise streaming
#     callbacks = [StreamingStdOutCallbackHandler()]

#     # Verbose is required to pass to the callback manager
#     llm = GPT4All(
#         model=modelPath, 
#         callbacks=callbacks, 
#         verbose=True,
#         n_batch=4,
#         n_threads=8,
#         # n_predict=512
#         # seed=-1
#     )
    
#     template = """
# Here's my function in Python:

# {function}

# Given the definition of a function in Python, generate it's documentation. I want it complete with fields like function name, function arguments and return values as well as a detailed explanation of how the function logic works line-by-line. Make it concise and informative to put the documentation into a project.
#     """
    
#     prompt = PromptTemplate(
#         template=template,
#         input_variables=["function"],
#     )
    
#     llmChain = LLMChain(
#         prompt=prompt, 
#         llm=llm,
#     )

    llmChain = model_utils.setupLangChain(model)
    
    for function in functions:
        llmChain.run({'function': function})


@app.command()
def easter():
    '''
    An easter egg for the keen eyed open-source contributor.
    '''
    print("This is a test command! If you're here, that means you've discovered something pretty cool in our code-base.\nCongrats and thanks for using our app!")


if __name__ == "__main__":
    app()