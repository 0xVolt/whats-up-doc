from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, SummarizationPipeline
from utils import *
import typer
import tokenize
import io

app = typer.Typer()

@app.command
def generate(filePath: str, defaultModel: bool, gpu: bool):
    device = 0
    if not gpu:
        device = 1
    
    if defaultModel:
        checkpoint = r"SEBIS/code_trans_t5_base_source_code_summarization_python_transfer_learning_finetune"
        pipeline = SummarizationPipeline(
            model=AutoModelForSeq2SeqLM.from_pretrained(checkpoint),
            tokenizer=AutoTokenizer.from_pretrained(
                checkpoint, 
                skip_special_tokens=True, 
                legacy=False
            ),
            max_new_tokens=1024,
            device=device
        )
    
    code = readFile(filePath)
    tokenizedCode = pythonTokenizer(code)
    
    print(f"Code:\n\n{code}")
    print(f"\n\nCode after tokenization:\n\n{tokenizedCode}")
    print(f"\n\nModel Output through inference point:\n\n{pipeline([tokenizedCode])}")

if __name__ == '__main__':
    app()