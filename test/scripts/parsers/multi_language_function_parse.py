import re
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

def extractFunctionsAsList(path, language):
    match language:
        case "Python":
            return extractFunctionsAsListPython(path)

        case _:
            print("Unsupported language...")

def main():
    path = r"C:\Users\deshi\Code\whats-up-doc\src\test\test_functions.cpp"
    
    lang = getScriptLanguage(path)
    listOfFunctions = extractFunctionsAsList(path, lang)
    
    print(*listOfFunctions, sep='\n')

if __name__ == "__main__":
    main()