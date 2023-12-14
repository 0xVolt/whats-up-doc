import ast
import json
import re
import textwrap


def cleanString(inputString):
    # Remove characters that are not spaces, newlines, or tabs
    cleanedString = re.sub(r'\r', '', inputString)
    return cleanedString


def formatModelOutputToMarkdown(inputString):
    # Split the input string into lines
    lines = inputString.strip().split('\n')

    # Ensure that there are at least two lines
    if len(lines) < 2:
        raise ValueError("Input string does not contain enough lines")

    # Extract function name and description
    function_name = lines[0].split(":")[1].strip()

    # Initialize section start indices
    section_starts = []

    # Find the start indices for each section
    for section in ["Description:", "Arguments:", "Return Values:", "Explanation:"]:
        try:
            section_starts.append(lines.index(section) + 1)
        except ValueError:
            # Handle the case when a section is not found
            section_starts.append(None)

    # Extract content for each section
    description_start, args_start, return_vals_start, explanation_start = section_starts

    description = '\n'.join(lines[description_start:args_start - 1]) if description_start else ""
    arguments = '\n'.join(lines[args_start:return_vals_start - 1]) if args_start else ""
    return_values = '\n'.join(lines[return_vals_start:explanation_start - 1]) if return_vals_start else ""
    explanation = '\n'.join(lines[explanation_start:]) if explanation_start else ""

    # Format the output
    markdownFormattedOutput = f"## Function Name: `{function_name}`\n\n{description}\n\n"

    if args_start:
        markdownFormattedOutput += f"### Arguments\n{textwrap.indent(arguments.replace('- ', '* '), '')}\n\n"

    if return_vals_start:
        markdownFormattedOutput += f"### Return Values\n{textwrap.indent(return_values, '')}\n\n"

    if explanation_start:
        markdownFormattedOutput += f"### Explanation\n{textwrap.indent(explanation, '')}"

    return markdownFormattedOutput


def extractFunctionsAsList(path):
    listOfFunctions = []

    with open(path, 'r') as file:
        content = file.read()
        tree = ast.parse(content, filename=path)

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                body = ast.get_source_segment(content, node)

                function_data = {
                    'name': node.name,
                    'args': [arg.arg for arg in node.args.args],
                    'defaults': [ast.get_source_segment(content, arg) for arg in node.args.defaults],
                    'body': body,
                    'return': ast.get_source_segment(content, node.returns) if node.returns else None
                }

                # Collect functions' meta data
                listOfFunctions.append(function_data)

    listOfFunctionBodies = [function['body'] for function in listOfFunctions]

    return listOfFunctionBodies


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
    code=None,            # parseAssignment is the only function that could pass code
    targets=None          # Dictionary for parseAssignment if multiple targets exist
):
    blockBody = None
    # I don't think I wanna change this anytime soon. Indexing starts from 1.
    bodyCount = 0

    if typeName != 'Import' and typeName != 'Assignment':
        blockBody = []

        for statement in node.body:
            blockBody.append(ast.unparse(statement))
            bodyCount += 1
    else:
        # Signifies that import and assignment statements have one line of code
        bodyCount = 1

    blockMetaData = {
        'Type': typeName,
        'Name': name,
        'StartLine': startLine,
        'StartCol': startCol,
        'EndLine': endLine,
        'EndCol': endCol,
        # 'RelativePath': os.path.relpath(path),
        'Body': code if typeName == 'Assignment' else blockBody,
        'BodyCount': bodyCount
    }

    if targets:
        blockMetaData['Targets'] = targets

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
        result['Module'] = parseModule(node)

    elif isinstance(node, ast.Assign):
        result['Assignment'] = parseAssignment(node, lines)

    elif isinstance(node, ast.Expression):
        result['Expression'] = parseExpression(node, path)

    elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        result[node.name] = parseFunctionOrClass(node)

    elif isinstance(node, ast.If):
        result['If'] = parseIf(node)

    elif isinstance(node, ast.For):
        result['For'] = parseFor(node)

    elif isinstance(node, ast.While):
        result['While'] = parseWhile(node)

    elif isinstance(node, ast.Import):
        result['Import'] = parseImport(node)

    for child_node in ast.iter_child_nodes(node):
        child_result = parseNode(child_node, path, lines)
        result.update(child_result)

    return result


def parseModule(node):
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


def parseAssignment(node, lines):
    assignmentMetaData = {}

    startLine = node.lineno
    endLine = node.end_lineno if hasattr(node, 'end_lineno') else startLine
    startCol = 0
    endColumn = node.col_offset
    code = "".join(lines[startLine - 1:endLine])

    # Replace consecutive spaces with a single tab character
    code = code.replace('    ', '\t')

    targetsMetaData = {}
    for target in node.targets:
        targetMetaData = {
            'Target': target.id if isinstance(target, ast.Name) else ast.dump(target),
            'Value': ast.unparse(node.value).strip(),
            'Object': ast.dump(node.value)
        }

        # If there are multiple targets. Fuck, I really hope not ://
        targetsMetaData.update(targetMetaData)

    assignmentMetaData = generateBlockMetaData(
        node=node,
        name=None,
        typeName='Assignment',
        startLine=startLine,
        endLine=endLine,
        startCol=startCol,
        endCol=endColumn,
        code=code,
        targets=targetMetaData
    )

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


def parseFunctionOrClass(node):
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


def parseIf(node):
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


def parseFor(node):
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


def parseWhile(node):
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


def parseImport(node):
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