from transformers import AutoTokenizer
import transformers
import torch

model = "mlabonne/NeuralBeagle14-7B"

function = """
def checkGPU(tensorflow):
    if tensorflow == True:
        import tensorflow as tf
        print("Number of GPUs available with tensorflow:", len(tf.config.list_physical_devices('GPU')))
    else:
        import torch
        print('Checking if the GPU is available with PyTorch:', torch.cuda.is_available())
"""

messages = [
    {
        "role": "system",
        "content": "You are an informative programming assistant that understands the working of a function and replies with it's documentation in markdown syntax."
    },
    {
        "role": "user",
        "content": f"{function}"
    }
]

tokenizer = AutoTokenizer.from_pretrained(model)
prompt = tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
pipeline = transformers.pipeline(
    "text-generation",
    model=model,
    torch_dtype=torch.float16, # Remember that float32 - CPU and float16 - GPU, keep this in mind if RuntimeError: "addmm_impl_cpu_" not implemented for 'Half'
    device_map="auto",
)