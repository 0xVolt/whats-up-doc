import ollama

stream = ollama.chat(
    model='llama2',
    messages=[
        {
            'role': 'user',
            'content': 'Write a code snippet implementing an ascii art generator in Rust.'
        }
    ],
    stream=True
)

# print(response['message']['content'])
for chunk in stream:
    print(chunk['message']['content'], end='', flush=True)