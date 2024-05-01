import typer
# from yaspin import yaspin
from utils import *

app = typer.Typer()
# spinner = yaspin()

@app.command()
def generate_script_documentation(
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

    language = fileUtils.getScriptLanguage(path)
    with open(path, 'r') as file:
        code = file.read()

    chain = modelUtils.setupLangChain(model)

    print("Generating model outputs...")

    stream = chain.stream({'code': code, 'language': language})
    outputString = ''

    for chunk in stream:
        # Print each chunk to the terminal
        print(chunk, end='')
        # Concatenate each chunk to the output string
        outputString += chunk

    fileUtils.writeOutputToMarkdownFile(outputFile, outputString, title=f"Documentation for `{path}`")

if __name__ == "__main__":
    app()