def readFile(path):
    with open(path) as fin:
        code = fin.read()
    
    return code


def checkGPU(tensorflow):
    if tensorflow == True:
        import tensorflow as tf
        print("Number of GPUs available with tensorflow:", len(tf.config.list_physical_devices('GPU')))
    else:
        import torch
        print('Checking if the GPU is available with PyTorch:', torch.cuda.is_available())


def pythonTokenizer(line):
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

    return ' '.join(result)