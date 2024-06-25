import ast

# Map (dict) that maps popular script file extensions to their associated language
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

# Function to parse Python scripts and store all functions into a list of strings using an Abstract Syntax Tree
def extractFunctionsAsListPython(path):
    # Create list of functions
    listOfFunctions = []

    with open(path, 'r') as file:
        content = file.read()
        # Initialize AST
        tree = ast.parse(content, filename=path)

        # Traverse tree starting with root node
        for node in ast.walk(tree):
            # If found an instance of a function definition
            if isinstance(node, ast.FunctionDef):
                # Get function's body
                body = ast.get_source_segment(content, node)

                # Store all function metadata into a dictionary
                function_data = {
                    'name': node.name,
                    'args': [arg.arg for arg in node.args.args],
                    'defaults': [ast.get_source_segment(content, arg) for arg in node.args.defaults],
                    'body': body,
                    'return': ast.get_source_segment(content, node.returns) if node.returns else None
                }

                # Collect functions' meta data
                listOfFunctions.append(function_data)

    # Only add function bodies when returning the list of functions as strings
    listOfFunctionBodies = [function['body'] for function in listOfFunctions]

    return listOfFunctionBodies

# Test code to eventually add support for multiple parsers spanning languages using a match-case statement
def extractFunctionsAsList(path, language):
    match language:
        case "Python":
            return extractFunctionsAsListPython(path)

        case _:
            print("Unsupported language...")
            return -1
