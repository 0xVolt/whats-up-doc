import typer
from transformers import pipeline
import ast

app = typer.Typer()

# Load the mistral-7b-instruct model
instruct_model = pipeline("text2text-generation", model="salesforce/instruct-mistral-7.0", tokenizer="salesforce/instruct-mistral-7.0")

def generate_function_docstring(function_name, source_code):
    # Extract the docstring of a function using AST
    tree = ast.parse(source_code)
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Str):
                return node.body[0].value.s
    return ""

@app.command()
def generate_docs(file_path: str, output_file: str = "documentation.md"):
    """
    Generate documentation for functions in a Python script.

    Args:
    - file_path (str): Path to the Python script file.
    - output_file (str): Path to the output markdown file. Default is "documentation.md".
    """
    with open(file_path, "r") as file:
        source_code = file.read()

    # Parse the source code using AST
    tree = ast.parse(source_code)

    documentation = []

    # Iterate through the AST to find functions
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            function_name = node.name
            docstring = generate_function_docstring(function_name, source_code)

            # Generate documentation using mistral-7b-instruct model
            if docstring:
                instruction = f"Document the function {function_name}."
                generated_doc = instruct_model(instruction)[0]['generated_text']
                documentation.append(f"## {function_name}\n\n{docstring}\n\nGenerated Documentation:\n\n{generated_doc}\n\n---\n")

    # Write documentation to the output file
    with open(output_file, "w") as output:
        output.write("# Function Documentation\n\n")
        output.write("This document contains the documentation for functions in the provided Python script.\n\n")
        output.write("Note: The generated documentation is based on mistral-7b-instruct model.\n\n")
        output.writelines(documentation)

if __name__ == "__main__":
    app()