import ast
import os
import json


def testScriptParsing(path):
    parsedScriptDictionary = parseScript(path)

    print(json.dumps(parsedScriptDictionary, sort_keys=False, indent=2))
    

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
    parsedScriptDictionary = {}

    with open(path, 'r') as file:
        lines = file.readlines()
        
    # Do this to make sure the lines of code is displayed as a field in the attributes
    # Man, this is hella confusing...
    script = "".join(lines)

    # Parse the script using ast module
    parsedScript = ast.parse(script)

    for node in ast.walk(parsedScript):
        nodeMetaData = parseNode(node, path, lines)
        
        if nodeMetaData:
            parsedScriptDictionary[nodeMetaData.get('Name', str(len(parsedScriptDictionary)))] = nodeMetaData

    return parsedScriptDictionary


def parseNode(node, path, lines):
    result = {}

    if isinstance(node, ast.Module):
        result['Module'] = parseModule(node, path)

    elif isinstance(node, ast.Assign):
        result['Assignment'] = parseAssignment(node, path, lines)

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
        child_result = parseNode(child_node, path, lines)
        result.update(child_result)

    return result


def parseModule(node, path):
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


def parseAssignment(node, path, lines):
    assignmentMetaData = {}
    
    for target in node.targets:
        start_line = node.lineno
        end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line
        line_of_code = "".join(lines[start_line - 1:end_line])
        
        # Replace consecutive spaces with a single tab character
        line_of_code = line_of_code.replace('    ', '\t')
        
        targetMetaData = {
            'target': target.id if isinstance(target, ast.Name) else ast.dump(target),
            'value': ast.dump(node.value),
            'line': node.lineno,
            'line_of_code': line_of_code.strip()
        }
        
        # If there are multiple targets. Fuck, I really hope not ://
        assignmentMetaData.update(targetMetaData)
        
    return assignmentMetaData


def parseExpression(node, path):
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
    path = r"C:\Users\deshi\Code\whats-up-doc\test\scripts\test_response.py"
    testScriptParsing(path)