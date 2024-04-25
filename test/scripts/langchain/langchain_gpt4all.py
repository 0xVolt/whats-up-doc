from langchain.llms import GPT4All

model = GPT4All(
            model=r"C:\Users\deshi\Code\gpt4all-models\orca-mini-3b-gguf2-q4_0.gguf",
            n_threads=8
        )

with open(r"C:\Users\deshi\Code\whats-up-doc\assets\test_prompt.txt", "r") as file:
    prompt = file.read()

response = model(prompt)

print(response)