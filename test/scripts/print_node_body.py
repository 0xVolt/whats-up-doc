import ast


def print_statements_in_function(code):
    # Parse the code into an Abstract Syntax Tree (AST)
    parsed_code = ast.parse(code)

    # Find all function definitions in the AST
    for node in ast.walk(parsed_code):
        if isinstance(node, ast.FunctionDef):
            print(f"Function: {node.name}")
            print("Statements in the function:")
            
            # Print all statements in the function's body
            for statement in node.body:
                print(ast.unparse(statement))
                

            print("=" * 30)

# Example code with a function definition
example_code = """
print("Hello!")

def example_function():
    print("This is the first statement in the function.")
    print("This is the second statement.")
    x = 10
    y = 20
    result = x + y
    print("The result is:", result)
    
print("Hello!")
"""

# Call the function to print statements in the function body
print_statements_in_function(example_code)