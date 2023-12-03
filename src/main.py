from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, SummarizationPipeline
from utils import *
import typer
import tokenize
import io

app = typer.Typer()

def main():
    pipeline = SummarizationPipeline(
        model=AutoModelForSeq2SeqLM.from_pretrained("SEBIS/code_trans_t5_base_source_code_summarization_python_transfer_learning_finetune"),
        tokenizer=AutoTokenizer.from_pretrained("SEBIS/code_trans_t5_base_source_code_summarization_python_transfer_learning_finetune", skip_special_tokens=True, legacy=False),
        max_new_tokens=512,
        device=0
    )

    code = readFile(r"C:\Users\deshi\Code\whats-up-doc\src\testReadFile.py")
    
    print(f"Code:\n\n{code}")

    tokenizedCode = pythonTokenizer(code)
    print(f"\n\nCode after tokenization:\n\n{tokenizedCode}")

    print(f"\n\nModel Output through inference point:\n\n{pipeline([tokenizedCode])}")

if __name__ == '__main__':
    main()