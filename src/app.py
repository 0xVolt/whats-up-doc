import typer
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.chains import LLMChain
from langchain.llms import GPT4All
from langchain.prompts import PromptTemplate
from transformers import (AutoModelForSeq2SeqLM, AutoTokenizer,
                          SummarizationPipeline)
from yaspin import yaspin
import mdutils

from utils import *

app = typer.Typer()
spinner = yaspin()


@app.command()
def generate(
    path: str,
    model: str = typer.Argument(None),
    outputFile: str = 'output.txt'
):
    '''
    Typer command to generate the documentation for an input script file.

    Arguments:
    filePath (string) - path to the input file
    model (string) - string to specify which model to use when generating documentation
    '''

    if model is None:
        model = modelUtils.getModelChoice()

    print(f"Arguments specified:")
    print(f"File Path: {path}")
    print(f"Model: {model}\n")

    modelOutputs = []

    functions = parserUtils.extractFunctionsAsList(path)

    llmChain = modelUtils.setupLangChain(model)

    for function in functions:
        modelOutputs.append(llmChain.run({'function': function}))

    fileUtils.writeOutputToMarkdownFile(outputFile, modelOutputs, title="Test Output Markdown File", ordered=False)


@app.command()
def easter():
    '''
    An easter egg for the keen eyed open-source contributor.
    '''
    print("This is a test command! If you're here, that means you've discovered something pretty cool in our code-base.\nCongrats and thanks for using our app!")


if __name__ == "__main__":
    app()