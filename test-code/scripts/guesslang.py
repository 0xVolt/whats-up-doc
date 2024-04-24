# A script file to determine the programming language of a script file by checking it against a dictionary of file extensions
import re

fileExtensionMap = {
    "py": "Python",
    "js": "JavaScript",
    "java": "Java",
    "cpp": "C++",
    "c": "C",
    "html": "HTML",
    "css": "CSS",
    "php": "PHP",
    "sh": "Bash",
    "sc": "Scala",
    "scala": "Scala"
}

def getFileExtension(file_path):
    # Regular expression pattern to match file extension
    pattern = r'\.(?!\.)[a-zA-Z0-9+]+$'
    
    # Use regex expression to get file extension
    match = re.search(pattern, file_path)
    
    if match:
        # Remove leading period
        return match.group(0)[1:]
    else:
        return None
    
def getScriptLanguage(path):
    
    """
    Determine the programming language based on the file extension.

    Args:
    - file_extension (str): The file extension of the script file.

    Returns:
    - str: The programming language corresponding to the file extension.
    """
    extension = getFileExtension(path)
    language = fileExtensionMap.get(extension.lower(), "Unknown")
    
    return language

def main():
    path = "/path/to/your/file/script.cpp"
    print(getScriptLanguage(path))

if __name__ == "__main__":
    main()