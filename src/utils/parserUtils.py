import ast

fileExtensionMap = {
    "py": "Python",
    "js": "JavaScript",
    "java": "Java",
    "cpp": "C++",
    "c": "C",
    "go": "Golang",
    "html": "HTML",
    "css": "CSS",
    "php": "PHP",
    "sh": "Bash",
    "sc": "Scala",
    "scala": "Scala",
    "md": "Markdown"
}

def extractFunctionsAsListPython(path):
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

def extractFunctionsAsList(path, language):
    match language:
        case "Python":
            return extractFunctionsAsListPython(path)

        case _:
            print("Unsupported language...")
            return -1