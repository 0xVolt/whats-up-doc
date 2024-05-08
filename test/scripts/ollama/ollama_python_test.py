import ollama

response = ollama.chat(
    model='llama2',
    messages=[
        {
            'role': 'user',
            'content': 'Write a code snippet implementing an ascii art generator in Rust.'
        }
    ]
)

print(response['message']['content'])