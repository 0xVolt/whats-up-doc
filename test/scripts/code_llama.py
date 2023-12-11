from transformers import AutoTokenizer
import transformers
import torch
from utils import test_utils


def get_llama_response(prompt: str) -> None:
    """
    Generate a response from the Llama model.

    Parameters:
        prompt (str): The user's input/question for the model.

    Returns:
        None: Prints the model's response.
    """
    sequences = llama_pipeline(
        prompt,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        max_length=1024,
    )
    
    print("Chatbot:", sequences[0]['generated_text'])
    

test_utils.checkGPU(tensorflow=False)

model = "meta-llama/Llama-2-7b-chat-hf" # meta-llama/Llama-2-7b-hf

tokenizer = AutoTokenizer.from_pretrained(model, token=True)

from transformers import pipeline

# Note: RuntimeError: "addmm_impl_cpu_" not implemented for 'Half' error means that GPU implementation is only supported for float16 and not float32
# If your program runs on the CPU, turn this to float32
llama_pipeline = pipeline(
    "text-generation",  # LLM task
    model=model,
    torch_dtype=torch.float32,
    device_map="auto",
)

testFunction = """
def get_llama_response(prompt: str) -> None:
    '''
    Generate a response from the Llama model.

    Parameters:
        prompt (str): The user's input/question for the model.

    Returns:
        None: Prints the model's response.
    '''
    sequences = llama_pipeline(
        prompt,
        do_sample=True,
        top_k=10,
        num_return_sequences=1,
        eos_token_id=tokenizer.eos_token_id,
        max_length=256,
    )
    print("Chatbot:", sequences[0]['generated_text'])
"""

prompt = f"""
Given the definition of a program in any programming language (particularly Python and C++), please generate it's stand-alone documentation in markdown form. I want it complete with fields like function name, function arguments and return values as well as a detailed explanation of how the function works. 

Do this for the following function in Python:\n
{testFunction}
"""

get_llama_response(prompt)