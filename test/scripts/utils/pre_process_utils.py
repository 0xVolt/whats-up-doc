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
                result.append('CODE_STRING')
            elif tokenType == tokenize.NUMBER:
                result.append('CODE_INTEGER')
            elif (not token == '\n') and (not token == '    '):
                result.append(str(token))

    result = ' '.join(result)

    return result