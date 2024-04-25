import re

def keep_alphanumeric_and_whitespace(input_string):
    # Keep only alphanumeric characters (A-Z, a-z, 0-9), spaces, tabs, and newlines
    cleaned_string = re.sub(r'[^A-Za-z0-9 \t\n]', '', input_string)
    return cleaned_string

# Example usage
model_output = "This is\na\r\r\r\r\r\rmodel output with\t special characters!\n\nLet's clean it."
cleaned_output = keep_alphanumeric_and_whitespace(model_output)

print(cleaned_output)
