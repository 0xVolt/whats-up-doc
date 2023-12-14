import textwrap

def format_function_description(input_string):
    # Split the input string into lines
    lines = input_string.strip().split('\n')

    # Extract function name and description
    function_name = lines[0].split(":")[1].strip()
    description = lines[1].split(":")[1].strip()

    # Extract arguments, return values, and explanation
    arguments_start = lines.index("Arguments:") + 1
    return_values_start = lines.index("Return Values:") + 1
    explanation_start = lines.index("Explanation:") + 1

    arguments = '\n'.join(lines[arguments_start:return_values_start-1])
    return_values = '\n'.join(lines[return_values_start:explanation_start-1])
    explanation = '\n'.join(lines[explanation_start:])

    # Format the output
    formatted_output = f"## Function Name: `{function_name}`\n\n{description}\n\n" \
                       f"### Description\n\n{textwrap.indent(description, '* ')}\n\n" \
                       f"### Arguments\n\n{textwrap.indent(arguments.replace('- ', '* '), '')}\n\n" \
                       f"### Return Values\n\n{return_values}\n\n" \
                       f"### Explanation\n{textwrap.indent(explanation, '')}"

    return formatted_output

# Example usage
input_string = """
Function Name: functionxyz
Description: This function logs the directory structure by recursively traversing through all subdirectories and files in the given directory path.
Arguments:
- directory_path (str): The path of the root directory to be logged. It should exist on the file system.
- ai_context (dict, optional): A dictionary containing any additional context information that needs to be passed along with the log messages.
- indent (int, optional): An integer specifying how many spaces to indent each level of subdirectories in the output. Default is 0.
Return Values:
None - This function does not return a value.
Explanation:
1. The function first checks if the given directory path exists using os.path.exists() and prints an error message if it doesn't exist.
"""

formatted_output = format_function_description(input_string)

# Write the formatted string to a markdown file
with open('formatted_function.md', 'w') as file:
    file.write(formatted_output)

print("Formatted string has been written to 'formatted_function.md'")