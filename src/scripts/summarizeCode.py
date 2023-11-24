from transformers import AutoTokenizer, AutoModelWithLMHead, SummarizationPipeline
import tokenize
import io

def pythonTokenizer(line):
    result = []
    line = io.StringIO(line)

    for tokenType, tok, start, end, line in tokenize.generate_tokens(line.readline):
        if (not tokenType == tokenize.COMMENT):
            if tokenType == tokenize.STRING:
                result.append("CODE_STRING")
            elif tokenType == tokenize.NUMBER:
                result.append("CODE_INTEGER")
            elif (not tok=="\n") and (not tok=="    "):
                result.append(str(tok))

    return ' '.join(result)

def main():
    pipeline = SummarizationPipeline(
        model=AutoModelWithLMHead.from_pretrained("SEBIS/code_trans_t5_base_source_code_summarization_python_transfer_learning_finetune"),
        tokenizer=AutoTokenizer.from_pretrained("SEBIS/code_trans_t5_base_source_code_summarization_python_transfer_learning_finetune", skip_special_tokens=True),
        device=0
    )

    code = '''

    def is_prime(number):
        if number <= 1:
            return False
        elif number <= 3:
            return True
        elif number % 2 == 0 or number % 3 == 0:
            return False
        i = 5
        while i * i <= number:
            if number % i == 0 or number % (i + 2) == 0:
                return False
            i += 6
        return True
            
    ''' #@param {type:"raw"}

    tokenized_code = pythonTokenizer(code)
    # print("Code after tokenization: " + tokenized_code)

    print(pipeline([tokenized_code]))

if __name__ == '__main__':
    main()