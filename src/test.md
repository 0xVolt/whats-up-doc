# Function Documentation for `.\test.py`

## Function Name: `checkGPU`



### Arguments
* tensorflow (bool): Whether to use TensorFlow or PyTorch for checking GPU availability. Defaults to True.


### Return Values
None


### Explanation
The checkGPU function takes a boolean argument 'tensorflow' which specifies whether the function should use TensorFlow or PyTorch for checking GPU availability. If tensorflow is set to True, it imports the necessary modules from TensorFlow and prints out the number of GPUs available with TensorFlow using the len() function on the list returned by tf.config.list_physical_devices('GPU').
If tensorflow is set to False, it imports the necessary modules from PyTorch and checks if a GPU is available with PyTorch using torch.cuda.is_available(). The output of this check is printed out.
In both cases, no return value is returned as the function simply prints out information about the availability of GPUs.

---

## Function Name: `log_directory_structure`



### Arguments
* `directory_path` (str): The path of the directory to be logged. It is required.
* `ai_context` (dict): A dictionary containing information about the AI context. This parameter can be used for additional functionality, but it's not necessary for logging the directory structure.


### Return Values
None - this function does not return any value.

Explanation of Function Logic:
1. The function first checks if the given path is valid by using `os.path.exists()`. If the path is invalid, it prints an error message and returns without logging anything.
2. It then gets a list of items in the directory using `os.listdir()` and iterates through each item.
3. For each item, it checks if it's a directory by using `os.path.isdir()`. If it is, it logs the directory name using `print()`, adjusting the indentation level for subdirectories using string multiplication (`" " * indent`) and concatenating it with the current directory path.
4. It then recursively calls itself on the item path to log its subdirectory structure.
5. If the item is a file, it can be logged similarly by calling `print()` with the item name and path.
6. After logging all items in the directory, it prompts the user for the directory path using `input()` and logs the root directory using `print()`.
7. Finally, it calls itself on the given directory path to log its structure recursively.

