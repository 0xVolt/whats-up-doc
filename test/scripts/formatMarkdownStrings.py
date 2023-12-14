import textwrap

def formatModelOutputToMarkdown(inputString):
    # Split the input string into lines
    lines = inputString.strip().split('\n')

    # Ensure that there are at least two lines
    if len(lines) < 2:
        raise ValueError("Input string does not contain enough lines")

    # Extract function name and description
    function_name = lines[0].split(":")[1].strip()
    
    # Initialize section start indices
    section_starts = []

    # Find the start indices for each section
    for section in ["Description:", "Arguments:", "Return Values:", "Explanation:"]:
        try:
            section_starts.append(lines.index(section) + 1)
        except ValueError:
            # Handle the case when a section is not found
            section_starts.append(None)

    # Extract content for each section
    description_start, args_start, return_vals_start, explanation_start = section_starts

    description = '\n'.join(lines[description_start:args_start - 1]) if description_start else ""
    arguments = '\n'.join(lines[args_start:return_vals_start - 1]) if args_start else ""
    return_values = '\n'.join(lines[return_vals_start:explanation_start - 1]) if return_vals_start else ""
    explanation = '\n'.join(lines[explanation_start:]) if explanation_start else ""

    # Format the output
    markdownFormattedOutput = f"## Function Name: `{function_name}`\n\n{description}\n\n"

    if args_start:
        markdownFormattedOutput += f"### Arguments\n{textwrap.indent(arguments.replace('- ', '* '), '')}\n\n"

    if return_vals_start:
        markdownFormattedOutput += f"### Return Values\n{textwrap.indent(return_values, '')}\n\n"

    if explanation_start:
        markdownFormattedOutput += f"### Explanation\n{textwrap.indent(explanation, '')}"

    return markdownFormattedOutput

# Example usage
# input_string = """
# Function Name: log_directory_structure

# Description: This function logs the directory structure by recursively traversing through all subdirectories and files in the given directory path.

# Arguments:
# - `directory_path` (str): The path of the root directory to be logged. It should exist on the file system.
# - `ai_context` (dict): A dictionary containing any additional context information that needs to be passed along with the log messages.
# - `indent` (int, optional): An integer specifying how many spaces to indent each level of subdirectories in the output. Default is 0.

# Return Values:
# None - This function does not return a value.

# Explanation:
# 1. The function first checks if the given directory path exists on the file system using `os.path.exists()` and prints an error message if it doesn't exist.
# 2. It then gets a list of all items in the directory using `os.listdir()`.
# 3. For each item, it constructs the full path to that item by joining the directory path with the item name using `os.path.join()` and checks if it's a directory or file using `os.path.isdir()`.
# 4. If the item is a directory, it logs the directory using the given `ai_context` dictionary and recursively calls itself on that subdirectory with an increased indentation level using `log_directory_structure(item_path, ai_context, indent + 1)`.
# 5. If the item is a file, it can log it similarly.
# 6. The function then prompts the user to enter the directory path and logs the root directory with that path.
# 7. Finally, it calls itself on the given `directory_path` using `log_directory_structure(directory_path, ai_context)`.
# """

input_string = """
Function Name: checkGPU

Description: This function checks if GPU is available with TensorFlow or PyTorch.

Arguments:
- tensorflow (bool): Whether to use TensorFlow or PyTorch for checking GPU availability. Defaults to True.

Return Values:
None

Explanation:
The checkGPU function takes a boolean argument 'tensorflow' which specifies whether the function should use TensorFlow or PyTorch for checking GPU availability. If tensorflow is set to True, it imports the necessary modules from TensorFlow and prints out the number of GPUs available with TensorFlow using the len() function on the list returned by tf.config.list_physical_devices('GPU').
If tensorflow is set to False, it imports the necessary modules from PyTorch and checks if a GPU is available with PyTorch using torch.cuda.is_available(). The output of this check is printed out.
In both cases, no return value is returned as the function simply prints out information about the availability of GPUs.
"""

formatted_output = formatModelOutputToMarkdown(input_string)
print(formatted_output)
