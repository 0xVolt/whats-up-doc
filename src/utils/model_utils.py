from transformers import (AutoModelForSeq2SeqLM, AutoTokenizer,
                          SummarizationPipeline)


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