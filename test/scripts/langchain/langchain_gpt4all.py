from langchain.llms import gpt4all

model = gpt4all(model=r"C:\Users\deshi\Code\gpt4all-models\orca-mini-3b-gguf2-q4_0.gguf")

with open(r"C:\Users\deshi\Code\whats-up-doc\assets\test_prompt.txt", "r") as file:
    prompt = file.read()

response = model(prompt)

print(response)