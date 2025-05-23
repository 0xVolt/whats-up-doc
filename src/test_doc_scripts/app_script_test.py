import typer
from yaspin import yaspin

from utils import *

app = typer.Typer()
spinner = yaspin()


@app.command()
def generate(
    path: str,
    model: str = typer.Argument(None),
    outputFile: str = 'output'
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

    functions = parserUtils.extractFunctionsAsList(path)

    chain = modelUtils.setupLangChain(model)

    print("Generating model outputs...")
    # spinner.start()

    modelOutputs = []

    for function in functions:
        stream = chain.stream({'function': function})
        outputString = ''
        
        for chunk in stream:                
            # Print each chunk to the terminal
            print(chunk, end='')
            # Concatenate each chunk to the output string
            outputString+= chunk
        
        modelOutputs.append(outputString)

    # spinner.stop()

    fileUtils.writeOutputToMarkdownFile(outputFile, modelOutputs, title=f"Documentation for `{path}`")


@app.command()
def easter():
    '''
    An easter egg for the keen eyed open-source contributor.
    '''
    print("This is a test command! If you're here, that means you've discovered something pretty cool in our code-base.\nCongrats and thanks for using our app!")


if __name__ == "__main__":
    app()