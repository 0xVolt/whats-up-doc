import ast
import os


def parse_script(file_path):
    functions_dict = {}

    with open(file_path, 'r') as file:
        script_contents = file.read()

    # Parse the script using ast module
    parsed_script = ast.parse(script_contents)

    for node in ast.walk(parsed_script):
        if isinstance(node, ast.FunctionDef):
            function_name = node.name
            arguments = [arg.arg for arg in node.args.args]
            num_chars = len(ast.get_source_segment(script_contents, node))
            relative_path = os.path.relpath(file_path)

            function_info = {
                'Name': function_name,
                'Arguments': arguments,
                'NumChars': num_chars,
                'RelativePath': relative_path
            }

            functions_dict[function_name] = function_info

    return functions_dict

# Example usage:
file_path = r'C:\Users\deshi\Code\whats-up-doc\src\utils\__init__.py'
functions_info = parse_script(file_path)

for function_name, info in functions_info.items():
    print(f"Function: {function_name}")
    print(f"Arguments: {info['Arguments']}")
    print(f"NumChars: {info['NumChars']}")
    print(f"RelativePath: {info['RelativePath']}")
    print("=" * 50)
