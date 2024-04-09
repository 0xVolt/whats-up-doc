def writeOutputToMarkdownFile(fileName, outputList, title):
    # Join the formatted outputs into a single string
    markdownContent = f"# {title}\n\n" + "\n\n---\n\n".join(outputList)

    # Write the content to the file
    with open(f'{fileName}.md', 'w') as file:
        file.write(markdownContent)