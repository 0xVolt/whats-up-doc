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

# def calculate_desired_noise_rms(clean_rms, snr): """ Given the Root Mean Square (RMS) of a clean sound and a desired signal-to-noise ratio (SNR), calculate the desired RMS of a noise sound to be mixed in. Based on https://github.com/Sato-Kunihiko/audio-SNR/blob/8d2c933b6c0afe6f1203251f4877e7a1068a6130/create_mixed_audio_file.py#L20 :param clean_rms: Root Mean Square (RMS) - a value between 0.0 and 1.0 :param snr: Signal-to-Noise (SNR) Ratio in dB - typically somewhere between -20 and 60 :return: """ a = float(snr) / 20 noise_rms = clean_rms / (10 ** a) return noise_rms

pipeline = SummarizationPipeline(
    model=AutoModelForSeq2SeqLM.from_pretrained("SEBIS/code_trans_t5_base_source_code_summarization_python_transfer_learning_finetune"),
    tokenizer=AutoTokenizer.from_pretrained("SEBIS/code_trans_t5_base_source_code_summarization_python_transfer_learning_finetune", skip_special_tokens=True, legacy=False),
    device=0    
)   

code = readFile(r"C:\Users\deshi\Code\whats-up-doc\src\testReadFile.py")

print(f"Code:\n\n{code}")

tokenizedCode = pythonTokenizer(code)
print(f"\n\nCode after tokenization:\n\n{tokenizedCode}")

print(f"\n\nModel Output through inference point:\n\n{pipeline([tokenizedCode])}")