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

    modelOutputs = []

    functions = parserUtils.extractFunctionsAsList(path)

    llmChain = modelUtils.setupLangChain(model)

    for function in functions:
        output = llmChain.run({'function': function})
        modelOutputs.append(parserUtils.cleanString(output))

    string1 = """
Function Name: log_directory_structure

Description: This function logs the directory structure by recursively traversing through all subdirectories and files in the given directory path.

Arguments:
- `directory_path` (str): The path of the root directory to be logged. It should exist on the file system.
- `ai_context` (dict): A dictionary containing any additional context information that needs to be passed along with the log messages.
- `indent` (int, optional): An integer specifying how many spaces to indent each level of subdirectories in the output. Default is 0.

Return Values:
None - This function does not return a value.

Explanation:
1. The function first checks if the given directory path exists on the file system using `os.path.exists()` and prints an error message if it doesn't exist.
2. It then gets a list of all items in the directory using `os.listdir()`.
3. For each item, it constructs the full path to that item by joining the directory path with the item name using `os.path.join()` and checks if it's a directory or file using `os.path.isdir()`.
4. If the item is a directory, it logs the directory using the given `ai_context` dictionary and recursively calls itself on that subdirectory with an increased indentation level using `log_directory_structure(item_path, ai_context, indent + 1)`.
5. If the item is a file, it can log it similarly.
6. The function then prompts the user to enter the directory path and logs the root directory with that path.
7. Finally, it calls itself on the given `directory_path` using `log_directory_structure(directory_path, ai_context)`.
"""

    string2 = """
Function Name: checkGPU

Description: This function checks if GPU is available with TensorFlow or PyTorch.

Arguments:
- tensorflow (bool): Whether to use TensorFlow or PyTorch for checking GPU availability. Defaults to True.

Return Values:
None

Explanation:
The checkGPU function takes a boolean argument 'tensorflow' which specifies whether the function should use TensorFlow or PyTorch for checking GPU availability. If tensorflow is set to True, it imports the necessary modules from TensorFlow and prints out the number of GPUs available with TensorFlow using the len() function on the list returned by tf.config.list_physical_devices('GPU').
If tensorflow is set to False, it imports the necessary modules from PyTorch and checks if a GPU is available with PyTorch using torch.cuda.is_available(). The output of this check is printed out.
In both cases, no return value is returned as the function simply prints out information about the availability of GPUs.  
"""

    # modelOutputs.append(string1)
    # modelOutputs.append(string2)

    fileUtils.writeOutputToMarkdownFile(outputFile, modelOutputs, title=f"Function Documentation for `{path}`")


@app.command()
def easter():
    '''
    An easter egg for the keen eyed open-source contributor.
    '''
    print("This is a test command! If you're here, that means you've discovered something pretty cool in our code-base.\nCongrats and thanks for using our app!")


if __name__ == "__main__":
    app()