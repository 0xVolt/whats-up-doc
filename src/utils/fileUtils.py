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


def writeOutputToMarkdownFile(filename, strings, title=None, ordered=False):
    """
    Writes a list of strings to a markdown file with appropriate formatting.

    Args:
        filename: The path to the markdown file to write to.
        strings: A list of strings to write to the file.
        title (optional): The title for the markdown file (default: None).
        ordered (optional): Whether to format the list as ordered (numbered) or unordered (bullet points) (default: False).

    Returns:
        None
    """
    import mdutils
    
    mdFile = mdutils.MdUtils(filename, title=title)

    # Choose formatting based on ordered flag
    if ordered:
        mdFile.new_list(strings, ul_style=True)
    else:
        mdFile.new_list(strings)

    mdFile.create_md_file()