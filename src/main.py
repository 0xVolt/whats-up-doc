from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, SummarizationPipeline
from utils import readFile, pythonTokenizer
import typer
import tokenize
import io

app = typer.Typer()


@app.command()
def generate(file: str, default: bool = True, gpu: bool = True):
    print(f"File: {file}")
    print(f"Use Default Model: {default}")
    
    # Change gpu flag
    device = 0 if gpu else 1

    checkpoint = r"SEBIS/code_trans_t5_base_source_code_summarization_python_transfer_learning_finetune" if default else -1
    
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

    code = readFile(file)
    tokenizedCode = pythonTokenizer(code)

    print(f"Code:\n\n{code}")
    print(f"\n\nCode after tokenization:\n\n{tokenizedCode}")
    print(f"\n\nModel Output through inference point:\n\n{pipeline([tokenizedCode])}")


@app.command()
def easter():
    print("This is a test command! If you're here, that means you've discovered something pretty cool in our code-base.\nCongrats and thanks for using our app!")


if __name__ == "__main__":
    app()