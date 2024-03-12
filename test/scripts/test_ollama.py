from langchain_community.llms import Ollama

model = Ollama(model='codellama')

stream = model.stream("Write a sample chrome extension in Rust.")

# Initialize an empty string to store the output
output_string = ""

for chunk in stream:
    # Print each chunk to the terminal
    print(chunk, end='')
    
    # Concatenate each chunk to the output string
    output_string += chunk

# Now you can use the output_string variable wherever you need the complete output as a string
print("\n\nComplete Output as String:")
print(output_string)
