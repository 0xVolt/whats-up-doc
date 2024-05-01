from slimit.parser import Parser
from slimit.visitors import nodevisitor
from slimit import ast as js_ast

def extract_functions_from_js(path):
    # List to store function bodies
    function_bodies = []

    with open(path, 'r') as file:
        content = file.read()

        # Parse the JavaScript file
        parser = Parser()
        tree = parser.parse(content)

        # Visit each node in the AST
        for node in nodevisitor.visit(tree):
            if isinstance(node, js_ast.FunctionDeclaration):
                # Extract function body
                function_body = node.to_ecma()

                # Add function body to the list
                function_bodies.append(function_body)

    return function_bodies

def main():
    # Path to the JavaScript file
    js_file_path = r"C:\Users\deshi\Code\whats-up-doc\src\test_doc_scripts\test_functions.js"

    # Extract functions from the JavaScript file
    functions = extract_functions_from_js(js_file_path)

    # Print the extracted function bodies
    for idx, func_body in enumerate(functions):
        print(f"Function {idx + 1}:\n{func_body}")
        print("-" * 20)

if __name__ == "__main__":
    main()
