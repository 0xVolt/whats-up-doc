from plyj.parser import Parser

def extract_functions_from_js(path):
    functions = []

    with open(path, 'r') as file:
        content = file.read()

        # Parse the JavaScript code using plyj
        parser = Parser()
        compilation_unit = parser.parse_string(content)

        # Traverse the parsed AST to extract function definitions
        for declaration in compilation_unit.type_declarations:
            if declaration.type == 'MethodDeclaration':
                function_name = declaration.name
                function_body = ''.join([str(child) for child in declaration.body])
                function_data = {
                    'name': function_name,
                    'body': function_body
                }
                functions.append(function_data)

    return functions

# Example usage
file_path = r'C:\Users\deshi\Code\whats-up-doc\src\test_doc_scripts\test_functions.js'
extracted_functions = extract_functions_from_js(file_path)
print(extracted_functions)
for func in extracted_functions:
    print(func['name'])
    print(func['body'])
    print("-------------------")
