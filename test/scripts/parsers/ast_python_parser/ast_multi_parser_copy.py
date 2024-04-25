import ast
import os
import json


def testScriptParsing(path):
    blocksInfo = parseScript(path)

    print(json.dumps(blocksInfo, sort_keys=False, indent=2))

    # for block_name, info in blocksInfo.items():
    #     # print(f"Type: {info['Type']}")
    #     print(f"Name: {info['Name']}")
    #     print(f"Start Line: {info['StartLine']}, Start Col: {info['StartCol']}")
    #     print(f"End Line: {info['EndLine']}, End Col: {info['EndCol']}")
    #     print(f"Relative Path: {info['RelativePath']}")
    #     print("=" * 50)


def generateBlockMetaData(
    node,
    typeName,
    name,
    startLine,
    endLine,
    startCol,
    endCol,
):
    blockBody = None

    if typeName is not 'Import':
        blockBody = []

        for statement in node.body:
            blockBody.append(ast.unparse(statement))

    blockMetaData = {
        'Type': typeName,
        'Name': name,
        'StartLine': startLine,
        'StartCol': startCol,
        'EndLine': endLine,
        'EndCol': endCol,
        'RelativePath': os.path.relpath(path),
        'Body': blockBody
    }

    return blockMetaData


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
    result = {}

    if isinstance(node, ast.Module):
        result['Module'] = parseModule(node, path)

    # elif isinstance(node, ast.Assign):
    #     for target in node.targets:
    #         if isinstance(target, ast.Name):
    #             result[target.id] = parseAssignment(node.value, path)

    elif isinstance(node, ast.Expression):
        result['Expression'] = parseExpression(node, path)

    elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        result[node.name] = parseFunctionOrClass(node, path)

    elif isinstance(node, ast.If):
        result['If'] = parseIf(node, path)

    elif isinstance(node, ast.For):
        result['For'] = parseFor(node, path)

    elif isinstance(node, ast.While):
        result['While'] = parseWhile(node, path)

    elif isinstance(node, ast.Import):
        result['Import'] = parseImport(node, path)

    for child_node in ast.iter_child_nodes(node):
        child_result = parseNode(child_node, path)
        result.update(child_result)

    return result


def parseModule(node, path):
    # moduleMetaData = {
    #     'Type': 'Module',
    #     'Name': None,
    #     'StartLine': 1,
    #     'StartCol': 0,
    #     'EndLine': len(node.body) if node.body else 1,
    #     'EndCol': 0,
    #     'RelativePath': os.path.relpath(path)
    # }

    moduleMetaData = generateBlockMetaData(
        node=node,
        typeName='Module',
        name=None,
        startLine=1,
        endLine=len(node.body) if node.body else 1,
        startCol=0,
        endCol=0
    )

    return moduleMetaData


# def parseAssignment(value_node, path):
#     try:
#         assigned_value = ast.literal_eval(value_node)
#         assignment_info = {
#             'AssignedValue': assigned_value,
#             'ValueType': type(assigned_value).__name__,
#             'RelativePath': os.path.relpath(path)
#         }
#         return assignment_info
#     except SyntaxError:
#         print(f"Error parsing assignment value in path: {path}")
#         return None


def parseExpression(node, path):
    # expressionMetaData = {
    #     'Type': 'Expression',
    #     'Name': None,
    #     'StartLine': node.lineno,
    #     'StartCol': node.col_offset,
    #     'EndLine': node.end_lineno,
    #     'EndCol': node.end_col_offset,
    #     'RelativePath': os.path.relpath(path)
    # }

    expressionMetaData = generateBlockMetaData(
        node,
        typeName='Expression',
        name=None,
        startLine=node.lineno,
        endLine=node.end_lineno,
        startCol=node.col_offset,
        endCol=node.end_col_offset,
    )

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

    # blockMetaData = {
    #     'Type': blockType,
    #     'Name': blockName,
    #     'StartLine': startLine,
    #     'StartCol': startColumn,
    #     'EndLine': endLine,
    #     'EndCol': endColumn,
    #     'RelativePath': os.path.relpath(path)
    # }

    functionOrClassMetaData = generateBlockMetaData(
        node,
        typeName=blockType,
        name=blockName,
        startLine=startLine,
        endLine=endLine,
        startCol=startColumn,
        endCol=endColumn
    )

    return functionOrClassMetaData


def parseIf(node, path):
    # ifMetaData = {
    #     'Type': 'If',
    #     'Name': None,
    #     'StartLine': node.lineno,
    #     'StartCol': node.col_offset,
    #     'EndLine': node.orelse[0].lineno if node.orelse else node.lineno,
    #     'EndCol': node.orelse[0].col_offset if node.orelse else 0,
    #     'RelativePath': os.path.relpath(path)
    # }

    ifMetaData = generateBlockMetaData(
        node,
        typeName='If',
        name=None,
        startLine=node.lineno,
        endLine=node.orelse[0].lineno if node.orelse else node.lineno,
        startCol=node.col_offset,
        endCol=node.orelse[0].col_offset if node.orelse else 0
    )

    return ifMetaData


def parseFor(node, path):
    # forMetaData = {
    #     'Type': 'For',
    #     'Name': None,
    #     'StartLine': node.lineno,
    #     'StartCol': node.col_offset,
    #     'EndLine': node.body[0].lineno if node.body else node.lineno,
    #     'EndCol': node.body[0].col_offset if node.body else 0,
    #     'RelativePath': os.path.relpath(path)
    # }

    forMetaData = generateBlockMetaData(
        node,
        typeName='For',
        name=None,
        startLine=node.lineno,
        endLine=node.body[0].lineno if node.body else node.lineno,
        startCol=node.col_offset,
        endCol=node.body[0].col_offset if node.body else 0
    )

    return forMetaData


def parseWhile(node, path):
    # whileMetaData = {
    #     'Type': 'While',
    #     'Name': None,
    #     'StartLine': node.lineno,
    #     'StartCol': node.col_offset,
    #     'EndLine': node.body[0].lineno if node.body else node.lineno,
    #     'EndCol': node.body[0].col_offset if node.body else 0,
    #     'RelativePath': os.path.relpath(path)
    # }

    whileMetaData = generateBlockMetaData(
        node,
        typeName='While',
        name=None,
        startLine=node.lineno,
        endLine=node.body[0].lineno if node.body else node.lineno,
        startCol=node.col_offset,
        endCol=node.body[0].col_offset if node.body else 0
    )

    return whileMetaData


def parseImport(node, path):
    # importMetaData = {
    #     'Type': 'Import',
    #     'Name': None,
    #     'StartLine': node.lineno,
    #     'StartCol': node.col_offset,
    #     'EndLine': node.lineno,
    #     'EndCol': node.col_offset + len('import'),
    #     'RelativePath': os.path.relpath(path)
    # }

    importMetaData = generateBlockMetaData(
        node,
        typeName='Import',
        name=None,
        startLine=node.lineno,
        endLine=node.lineno,
        startCol=node.col_offset,
        endCol=node.col_offset + len('import')
    )

    return importMetaData


if __name__ == "__main__":
    path = r"C:\Users\deshi\Code\whats-up-doc\test\scripts\testResponse.py"
    testScriptParsing(path)