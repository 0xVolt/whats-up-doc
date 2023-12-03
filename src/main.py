from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, SummarizationPipeline
import typer
import tokenize
import io

app = typer.Typer()

def pythonTokenizer(line):
    result = []
    line = io.StringIO(line)

    for tokenType, token, start, end, line in tokenize.generate_tokens(line.readline):
        if (not tokenType == tokenize.COMMENT):
            if tokenType == tokenize.STRING:
                result.append("CODE_STRING")
            elif tokenType == tokenize.NUMBER:
                result.append("CODE_INTEGER")
            elif (not token == "\n") and (not token == "    "):
                result.append(str(token))

    return ' '.join(result)

def readFile(path):
    with open(path) as fin:
        code = fin.read()
    
    return code

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