import typer
# Import custom utils package
from utils import *

# Initialize Typer CLI app
app = typer.Typer()

# Typer command to generate the documentation when an input script is passed
@app.command()
def generate_script_documentation(
    path: str,
    model: str = typer.Argument(None),
    outputFile: str = 'output'
):
    '''
    Typer command to generate the documentation for an input script file.

    Args:
    - filePath (string) - path to the input file
    - model (string) - string to specify which model to use when generating documentation
    '''

    # Logic to handle model selection
    if model is None:
        model = modelUtils.getModelChoice()

    # Print out arguments thus far to debug
    print(f"Arguments specified:")
    print(f"File Path: {path}")
    print(f"Model: {model}\n")

    # Get the script's language by file extension
    language = fileUtils.getScriptLanguage(path)

    # Read script source code into a string
    with open(path, 'r') as file:
        code = file.read()

    # Setup LangChain with the user's choice of model
    chain = modelUtils.setupLangChain(model)

    print("Generating model outputs...")

    # Inference model as a stream
    stream = chain.stream({
            'code': code, 
            'language': language
        }
    )
    outputString = ''

    # Iterate over generated chunks in the stream
    for chunk in stream:
        # Print each chunk to the terminal
        print(chunk, end='')
        # Concatenate each chunk to the output string
        outputString += chunk

    # Write output string into a markdown file with the specified output file name (if exists)
    fileUtils.writeOutputToMarkdownFile(outputFile, outputString, title=f"Documentation for `{path}`")

# Run the app as a main function
# Typer forces this approach to build
if __name__ == "__main__":
    app()
