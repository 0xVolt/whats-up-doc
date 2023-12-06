import ast
import os


def testScriptParsing(path):
    blocksInfo = parseScript(path)

    for block_name, info in blocksInfo.items():
        print(f"Type: {info['Type']}")
        print(f"Name: {info['Name']}")
        print(f"Start Line: {info['StartLine']}, Start Col: {info['StartCol']}")
        print(f"End Line: {info['EndLine']}, End Col: {info['EndCol']}")
        print(f"Relative Path: {info['RelativePath']}")
        print("=" * 50)


def parseScript(path):
    blocksDictionary = {}

    with open(path, 'r') as file:
        script = file.read()

    # Parse the script using ast module
    parsedScript = ast.parse(script)

    for node in ast.walk(parsedScript):
        blockInfo = parseNode(node, path)
        if blockInfo:
            blocksDictionary[blockInfo.get('Name', str(len(blocksDictionary)))] = blockInfo

    return blocksDictionary


def parseNode(node, path):
    # Note: Python match-case statements are only supported in 3.10+
    if isinstance(node, ast.Module):
        return parseModule(node, path)
    elif isinstance(node, ast.Expression):
        return parseModule(node, path)
    elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        return parseFunctionOrClass(node, path)
    elif isinstance(node, ast.If):
        return parseIf(node, path)
    elif isinstance(node, ast.While):
        return parseWhile(node, path)
    elif isinstance(node, ast.Import):
        return parseImport(node, path)


def parseModule(node, path):
    moduleMetaData = {
        'Type': 'Module',
        'Name': None,
        'StartLine': 1,
        'StartCol': 0,
        'EndLine': len(node.body) if node.body else 1,
        'EndCol': 0,
        'RelativePath': os.path.relpath(path)
    }
    
    return moduleMetaData


def parseExpression(node, path):
    blockType = type(node).__name__
    blockName = node.name if hasattr(node, 'name') else None
    startLine, startColumn = node.lineno, node.col_offset
    endLine, endColumn = startLine + len(node.body) if node.body else startLine, 0

    blockMetaData = {
        'Type': blockType,
        'Name': blockName,
        'StartLine': startLine,
        'StartCol': startColumn,
        'EndLine': endLine,
        'EndCol': endColumn,
        'RelativePath': os.path.relpath(path)
    }

    return blockMetaData


def parseFunctionOrClass():
    pass


def parseIf():
    pass


def parseFor():
    pass


def parseWhile():
    pass


def parseImport():
    pass