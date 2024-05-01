import js2xml

def extract_functions_from_js(path):
    functions = []

    with open(path, 'r') as file:
        content = file.read()
        tree = js2xml.parse(content)

        # Traverse the parsed XML tree to extract function definitions
        for node in tree.xpath('//FunctionDeclaration'):
            function_name = node.xpath('.//identifier')[0].text  # Use lowercase 'identifier'
            function_body = js2xml.pretty_print(node.xpath('.//block')[0])  # Use lowercase 'block'
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