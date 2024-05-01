import re

fileExtensionMap = {
    "py": "Python",
    "js": "JavaScript",
    "java": "Java",
    "cpp": "C++",
    "c": "C",
    "go": "Golang",
    "html": "HTML",
    "css": "CSS",
    "php": "PHP",
    "sh": "Bash",
    "sc": "Scala",
    "scala": "Scala",
    "md": "Markdown"
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


def writeOutputToMarkdownFile(fileName, outputList, title):
    # Join the formatted outputs into a single string
    markdownContent = f"# {title}\n\n" + "\n\n---\n\n".join(outputList)

    # Write the content to the file
    with open(f'{fileName}.md', 'w') as file:
        file.write(markdownContent)