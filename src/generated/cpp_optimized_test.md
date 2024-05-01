# Documentation for `test_doc_scripts\test_functions_regular.cpp`



---


## Function Name: `main`

The main function is the entry point of the program. It is used to initialize and control the execution of the program. In this case, it is used to call other functions to generate a random vector of integers.

### Arguments
* None

### Return Values
* `int`: The return value of the main function is an integer that represents the exit status of the program. A value of 0 indicates that the program executed successfully, while any other value indicates an error.

### Explanation of Function Logic:
1. The size of the vector to generate is specified as a command-line argument using the `size` variable.
2. The minimum and maximum values of the generated integers are specified as command-line arguments using the `min` and `max` variables, respectively.
3. A random integer between the minimum and maximum values is generated using the `randomInt` function for each element in the vector.
4. The generated vector is printed to the console using the `printVector` function.
5. The program returns 0 to indicate that it executed successfully.

## Function Name: `randomInt`

The `randomInt` function is used to generate a random integer between a minimum and maximum value (inclusive). It uses the `std::uniform_int_distribution` class from the `<random>` header to generate random integers within the specified range.

### Arguments
* `min` (int): The minimum value of the generated integer.
* `max` (int): The maximum value of the generated integer.

### Return Values
* `int`: A random integer between the minimum and maximum values (inclusive).

### Explanation of Function Logic:
1. The function uses the `std::random_device` class to generate a seed for the random number generator.
2. It then creates an instance of the `std::mt19937` class using the generated seed and initializes it with the `std::uniform_int_distribution` class from the `<random>` header.
3. The function then uses the `std::uniform_int_distribution` object to generate a random integer between the minimum and maximum values (inclusive) for each call.
4. The generated integer is returned by the function.

## Function Name: `randomIntVector`

The `randomIntVector` function is used to generate a vector of random integers with a specified size, where each element in the vector has a random value between a minimum and maximum value (inclusive). It uses the `std::vector` class from the `<vector>` header to create and populate the vector.

### Arguments
* `size` (int): The number of elements in the generated vector.
* `min` (int): The minimum value of the generated integers.
* `max` (int): The maximum value of the generated integers.

### Return Values
* `std::vector<int>`: A vector of random integers with a specified size, where each element has a random value between the minimum and maximum values (inclusive).

### Explanation of Function Logic:
1. The function first creates an empty vector of the specified size using the `std::vector` class from the `<vector>` header.
2. It then uses a loop to generate a random integer between the minimum and maximum values (inclusive) for each element in the vector and stores it in the corresponding position in the vector.
3. The generated vector is returned by the function.