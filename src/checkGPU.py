import torch
import tensorflow as tf

# PyTorch
# print('Checking for GPU...')
# print(f'{torch.cuda.is_available()}')

# Tensorflow
print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))