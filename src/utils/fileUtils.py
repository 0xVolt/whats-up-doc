from .parserUtils import formatModelOutputToMarkdown


def readFile(path):
    '''
    Open a specified script file in read mode and return it's contents as a string.

    Argument(s):
    path (string) - path to the file to be read

    Output(s):
    code (string) - contents of the script file
    '''
    with open(path, 'r') as fin:
        code = fin.read()

    return code

    
def returnModelLocalPath(model):
    modelPath = {
        'mistral-7b-instruct': r"C:\Users\deshi\Code\gpt4all-models\mistral-7b-instruct-v0.1.Q4_0.gguf",
        'orca-mini-3b': r"C:\Users\deshi\Code\gpt4all-models\orca-mini-3b-gguf2-q4_0.gguf"
    }
    
    return modelPath[model]


def writeOutputToMarkdownFile(fileName, outputList, title):
    formattedOutputs = []
    
    for output in outputList:
        formattedOutputs.append(formatModelOutputToMarkdown(output))

    with open(f'{fileName}.md', 'a') as file:
        file.write(f'# {title}\n\n')
        
        for output in formattedOutputs:
            file.write(output)
            file.write(f'\n\n---\n\n')