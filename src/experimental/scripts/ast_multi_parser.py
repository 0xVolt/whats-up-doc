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
    result = []

    if isinstance(node, ast.Module):
        result.append(parseModule(node, path))
    
    elif isinstance(node, ast.Expression):
        result.append(parseExpression(node, path))
    
    elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        result.append(parseFunctionOrClass(node, path))
    
    elif isinstance(node, ast.If):
        result.append(parseIf(node, path))
    
    elif isinstance(node, ast.While):
        result.append(parseWhile(node, path))
    
    elif isinstance(node, ast.Import):
        result.append(parseImport(node, path))
    
    for child_node in ast.iter_child_nodes(node):
        result.extend(parseNode(child_node, path))

    return result


# def parseNode(node, path):
#     # Note: Python match-case statements are only supported in 3.10+
#     if isinstance(node, ast.Module):
#         return parseModule(node, path)
    
#     elif isinstance(node, ast.Expression):
#         return parseModule(node, path)
    
#     elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
#         return parseFunctionOrClass(node, path)
    
#     elif isinstance(node, ast.If):
#         return parseIf(node, path)
    
#     elif isinstance(node, ast.While):
#         return parseWhile(node, path)
    
#     elif isinstance(node, ast.Import):
#         return parseImport(node, path)


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
    expressionMetaData = {
        'Type': 'Expression',
        'Name': None,
        'StartLine': node.lineno,
        'StartCol': node.col_offset,
        'EndLine': node.end_lineno,
        'EndCol': node.end_col_offset,
        'RelativePath': os.path.relpath(path)
    }

    if isinstance(node, ast.BinOp):
        expressionMetaData['Name'] = 'Binary Operation'
        expressionMetaData['Left'] = parseExpression(node.left, path)
        expressionMetaData['Operator'] = ast.get_op_symbol(node.op)
        expressionMetaData['Right'] = parseExpression(node.right, path)

    elif isinstance(node, ast.Call):
        expressionMetaData['Name'] = 'Function Call'
        expressionMetaData['Function'] = parseExpression(node.func, path)
        expressionMetaData['Arguments'] = [parseExpression(arg, path) for arg in node.args]

    elif isinstance(node, ast.Attribute):
        expressionMetaData['Name'] = 'Attribute'
        expressionMetaData['Value'] = parseExpression(node.value, path)
        expressionMetaData['Attr'] = node.attr

    elif isinstance(node, ast.Name):
        expressionMetaData['Name'] = 'Variable'
        expressionMetaData['Value'] = node.id

    elif isinstance(node, ast.Constant):
        expressionMetaData['Name'] = 'Constant'
        expressionMetaData['Value'] = node.value

    return expressionMetaData


def parseFunctionOrClass(node, path):
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


def parseIf(node, path):
    ifMetaData = {
        'Type': 'If',
        'Name': None,
        'StartLine': node.lineno,
        'StartCol': node.col_offset,
        'EndLine': node.orelse[0].lineno if node.orelse else node.lineno,
        'EndCol': node.orelse[0].col_offset if node.orelse else 0,
        'RelativePath': os.path.relpath(path)
    }
    
    return ifMetaData


def parseFor(node, path):
    forMetaData = {
        'Type': 'For',
        'Name': None,
        'StartLine': node.lineno,
        'StartCol': node.col_offset,
        'EndLine': node.body[0].lineno if node.body else node.lineno,
        'EndCol': node.body[0].col_offset if node.body else 0,
        'RelativePath': os.path.relpath(path)
    }
    
    return forMetaData


def parseWhile(node, path):
    whileMetaData = {
        'Type': 'While',
        'Name': None,
        'StartLine': node.lineno,
        'StartCol': node.col_offset,
        'EndLine': node.body[0].lineno if node.body else node.lineno,
        'EndCol': node.body[0].col_offset if node.body else 0,
        'RelativePath': os.path.relpath(path)
    }
    
    return whileMetaData


def parseImport(node, path):
    importMetaData = {
        'Type': 'Import',
        'Name': None,
        'StartLine': node.lineno,
        'StartCol': node.col_offset,
        'EndLine': node.lineno,
        'EndCol': node.col_offset + len('import'),
        'RelativePath': os.path.relpath(path)
    }
    
    return importMetaData


if __name__ == "__main__":
    path = r"C:\Users\deshi\Code\whats-up-doc\src\experimental\scripts\testResponse.py"
    testScriptParsing(path)