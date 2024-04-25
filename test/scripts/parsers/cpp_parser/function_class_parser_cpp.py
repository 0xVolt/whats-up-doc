# This script is able to parse all the functions in a C++ script
# However, this won't distinguish methods in a class/struct from other functions
import re

def extractFunctions(path):
    functions = []

    with open(path, 'r') as file:
        content = file.read()

        function_pattern = r'((?:\w+\s+)*\w+\s+\w+\s*\([^)]*\)\s*\{(?:[^{}]*|\{(?:[^{}]*|\{(?:[^{}]*|\{(?:[^{}]*|\{[^{}]*\})*\})*\})*\})*\})'

        functions = re.findall(function_pattern, content, re.DOTALL)

    return functions

# Function to print a separator line
def print_separator():
    print("-------------------")

# Main function to extract and print functions
def main():
    file_path = r'C:\Users\deshi\Code\whats-up-doc\src\test_doc_scripts\test_functions_advanced.cpp'
    extracted_functions = extractFunctions(file_path)

    if extracted_functions:
        for func in extracted_functions:
            print(func)
            print_separator()
    else:
        print("No functions found in the file.")

if __name__ == "__main__":
    main()
