from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate

llm = Ollama(model='codellama')

template = """
Write the documentation for this function in markdown:

def sum():
    sum = 0
    for i in range(10):
        sum += i

    return sum
"""

prompt = PromptTemplate(input_variables=[], template=template)

chain = prompt | llm 

# Initialize an empty string to store the output
output_string = ""

for chunk in chain.stream({}):
    # Print each chunk to the terminal
    print(chunk, end='')
    
    # Concatenate each chunk to the output string
    output_string += chunk

# Now you can use the output_string variable wherever you need the complete output as a string
print("\n\nComplete Output as String:")
print(output_string)
