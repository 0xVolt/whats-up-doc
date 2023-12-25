from utils import *

script_data = parser_utils.parseScript(r"C:\Users\deshi\Code\whats-up-doc\src\test.py")  # Your script data dictionary

# Initialize a dictionary to store functions
functions_dict = {}

# Flag to track whether the current statement is inside a function or not
inside_function = False

# Iterate through the script data
for key, statement_data in script_data.items():
    # Check if the statement is a function
    if "FunctionDef" in statement_data:
        # If we were previously inside a function, store its body in the dictionary
        if inside_function:
            functions_dict[function_name]["Body"] = function_body
        inside_function = True
        function_name = statement_data["Name"]
        function_body = []
    elif "Assignment" in statement_data or "Expression" in statement_data:
        # If it's an assignment/expression statement inside a function, add it to the body
        if inside_function:
            function_body.append(statement_data)

# If there is any remaining function, store its body in the dictionary
if inside_function:
    functions_dict[function_name]["Body"] = function_body

# Print the bodies of each function
for function_name, function_data in functions_dict.items():
    print(f"Function: {function_name}")
    for statement in function_data["Body"]:
        print(f"  {statement['Type']}: {statement.get('Name', '')}")
