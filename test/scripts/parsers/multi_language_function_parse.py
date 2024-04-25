import re
import ast
import clang.cindex

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

def getFileExtension(file_path):
    # Regular expression pattern to match file extension
    pattern = r'\.(?!\.)[a-zA-Z0-9+]+$'

    # Use regex expression to get file extension
    match = re.search(pattern, file_path)

    if match:
        # Remove leading period
        return match.group(0)[1:]
    else:
        return None

def getScriptLanguage(path):

    """
    Determine the programming language based on the file extension.

    Args:
    - file_extension (str): The file extension of the script file.

    Returns:
    - str: The programming language corresponding to the file extension.
    """
    extension = getFileExtension(path)
    language = fileExtensionMap.get(extension.lower(), "Unknown")

    return language

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

def extractFunctionsAsListCpp(path):
    listOfFunctions = []

    # Create an index for the translation unit
    index = clang.cindex.Index.create()

    # Parse the translation unit
    tu = index.parse(path)

    # Traverse the AST and extract function bodies
    for node in tu.cursor.walk_preorder():
        if node.kind == clang.cindex.CursorKind.FUNCTION_DECL:
            function_name = node.spelling
            function_body = node.extent.contents
            
            # Get the function body as a string
            function_body_str = function_body and function_body.as_string()

            function_data = {
                'name': function_name,
                'body': function_body_str,
                'return': node.result_type.spelling  # Extract return type if needed
            }

            # Collect functions' meta data
            listOfFunctions.append(function_data)

    listOfFunctionBodies = [function['body'] for function in listOfFunctions]

    return listOfFunctionBodies

def extractFunctionsAsList(path, language):
    match language:
        case "Python":
            return extractFunctionsAsListPython(path)
        
        case "C++":
            return extractFunctionsAsListCpp(path)

        case _:
            print("Unsupported language...")

def main():
    path = r"C:\Users\deshi\Code\whats-up-doc\src\test\test_functions.cpp"
    
    lang = getScriptLanguage(path)
    listOfFunctions = extractFunctionsAsList(path, lang)
    
    print(*listOfFunctions, sep='\n')

if __name__ == "__main__":
    main()