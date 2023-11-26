from transformers import AutoTokenizer, AutoModelForSeq2SeqLM, SummarizationPipeline
import tokenize
import io

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
        device=0
    )

    code = readFile(r"C:\Users\deshi\Code\whats-up-doc\src\scripts\testReadFile.py")
    
    print(f"Code:\n\n{code}")
    
    # code = '''

    # def is_prime(number):
    #     if number <= 1:
    #         return False
    #     elif number <= 3:
    #         return True
    #     elif number % 2 == 0 or number % 3 == 0:
    #         return False
    #     i = 5
    #     while i * i <= number:
    #         if number % i == 0 or number % (i + 2) == 0:
    #             return False
    #         i += 6
    #     return True
            
    # ''' #@param {type:"raw"}

    tokenizedCode = pythonTokenizer(code)
    print(f"\n\nCode after tokenization:\n\n{tokenizedCode}")

    print(f"\n\nModel Output through inference point:\n\n{pipeline([tokenizedCode])}")

if __name__ == '__main__':
    main()