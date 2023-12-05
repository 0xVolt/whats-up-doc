from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, SummarizationPipeline
from utils import readFile, pythonTokenizer, splitFileIntoBlocks
import typer
import tokenize
import io
from yaspin import yaspin

app = typer.Typer()
spinner = yaspin()


def createPipeline(checkpoint, device):
    '''
    Create a transformers model summarization pipeline.

    Arguments:
    checkpoint - model checkpoint
    device (integer) - either 0 or 1, to specify if there exists a GPU
    '''
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

    return pipeline


@app.command()
def generate(
    file: str,
    default: bool = True,
    gpu: bool = True
):
    '''
    Typer command to generate the documentation for an input script file.

    Arguments:
    file (string) - path to the input file
    default (boolean) - flag to specify using the default model or a custom model
    gpu (boolean) - flag to specify whether a GPU is available
    '''
    print(f"Arguments specified:")
    print(f"File Path: {file}")
    print(f"Use Default Model Flag: {default}")
    print(f"Use GPU: {gpu}")

    # Change gpu flag
    device = 0 if gpu else 1

    checkpoint = r"SEBIS/code_trans_t5_base_source_code_summarization_python_transfer_learning_finetune" if default else -1

    print("\nCreating model summarization pipeline...\n")
    spinner.start()
    pipeline = createPipeline(checkpoint=checkpoint, device=device)
    spinner.stop()

    code = readFile(file)
    tokenizedCode = pythonTokenizer(code)

    print(f"Code:\n\n{code}")
    print(f"\n\nCode after tokenization:\n\n{tokenizedCode}")
    print(f"\n\nModel Output through inference point:\n\n{pipeline([tokenizedCode])}")


@app.command()
def easter():
    '''
    An easter egg for the keen eyed open-source contributor.
    '''
    print("This is a test command! If you're here, that means you've discovered something pretty cool in our code-base.\nCongrats and thanks for using our app!")


if __name__ == "__main__":
    # app()
    
    path = input('Enter the file path: ')
    
    codeBlocks = splitFileIntoBlocks(path)
    
    print(codeBlocks)