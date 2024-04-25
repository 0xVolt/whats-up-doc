import ast


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
                
                listOfFunctions.append(function_data)

    return listOfFunctions


# Example usage:
path = r'C:\Users\deshi\Code\whats-up-doc\src\test.py'
functions_list = extractFunctions(path)

# Print the extracted listOfFunctions
for function_data in functions_list:
    print(f"Function: {function_data['name']}")
    print(f"  Args: {function_data['args']}")
    print(f"  Defaults: {function_data['defaults']}")
    print(f"  Body:\n{function_data['body']}")
    print(f"  Return: {function_data['return']}")
    print("\n")
