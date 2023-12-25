import json


def stringToDictionary(string):
    pass 


def prettyPrintDictionary(dict):
    print(json.dumps(dict, sort_keys=False, indent=2))


def checkGPU(tensorflow):
    '''
    Check if a GPU is recognized by Tensorflow or PyTorch
    
    Argument(s):
    tensorflow (bool) - Toggle a check for a GPU through either TensorFlow or PyTorch
    '''
    if tensorflow == True:
        import tensorflow as tf
        print('Number of GPUs available with tensorflow', len(tf.config.list_physical_devices('GPU')))
    else:
        import torch
        print('Checking if the GPU is available with PyTorch:', torch.cuda.is_available())