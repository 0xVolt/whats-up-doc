import re

# Function to parse a C++ file and extract functions, classes, and structs with their bodies
def parse_cpp_file(file_path):
    # Regular expressions to match functions, classes, and structs
    function_pattern = r'(?:\b(?:void|int|float|double|char|long|short)\s+)(\w+)\s*\((.*?)\)\s*{([^}]*)\}'
    class_pattern = r'class\s+(\w+)\s*{([^}]*)};'
    struct_pattern = r'struct\s+(\w+)\s*{([^}]*)};'

    # Read the content of the C++ file
    with open(file_path, 'r') as file:
        content = file.read()

    # Extract functions
    functions = re.findall(function_pattern, content, re.DOTALL)

    # Extract classes
    classes = re.findall(class_pattern, content, re.DOTALL)

    # Extract structs
    structs = re.findall(struct_pattern, content, re.DOTALL)

    return functions, classes, structs

# Main function to test the script
def main():
    file_path = r"C:\Users\deshi\Code\whats-up-doc\src\test\test_functions.cpp"  # Provide the path to your C++ file
    functions, classes, structs = parse_cpp_file(file_path)
    
    print("Functions:")
    for name, args, body in functions:
        print(f"Name: {name}")
        print(f"Arguments: {args}")
        print(f"Body: {body.strip()}\n")
    
    print("\nClasses:")
    for name, body in classes:
        print(f"Name: {name}")
        print(f"Body: {body.strip()}\n")
    
    print("\nStructs:")
    for name, body in structs:
        print(f"Name: {name}")
        print(f"Body: {body.strip()}\n")

if __name__ == "__main__":
    main()
