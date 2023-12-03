import io
import tokenize

def pythonTokenizer(line):
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

def readFile(path):
    with open(path) as fin:
        code = fin.read()
    
    return code