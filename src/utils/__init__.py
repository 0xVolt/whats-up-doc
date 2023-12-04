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


def checkGPU(tensorflow):
    '''
    Check if a GPU is recognized by Tensorflow or PyTorch 
    '''
    if tensorflow == True:
        import tensorflow as tf
        print("Number of GPUs available with tensorflow:", len(tf.config.list_physical_devices('GPU')))
    else:
        import torch
        print('Checking if the GPU is available with PyTorch:', torch.cuda.is_available())


def pythonTokenizer(line):
    '''
    Tokenize a python script file and replace code with abstracted syntax to then pass to a model inference point.
    
    Argument(s):
    line (string) - Python code passed to tokenize
    
    Output(s):
    result (string) - Result of the tokenized Python code
    '''
    import io
    import tokenize
    
    result = []
    line = io.StringIO(line)

    for tokenType, token, start, end, line in tokenize.generate_tokens(line.readline):
        if (not tokenType == tokenize.COMMENT):
            if tokenType == tokenize.STRING:
                result.append("CODE_STRING")
            elif tokenType == tokenize.NUMBER:
                result.append("CODE_INTEGER")
            elif (not token == "\n") and (not token == "    "):
                result.append(str(token))

    result = ' '.join(result)

    return result