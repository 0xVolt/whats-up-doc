#include <iostream>
#include <vector>
#include <random>

// Generate random integer between min and max (inclusive)
int randomInt(int min, int max) {
    static std::random_device rd;
    static std::mt19937 gen(rd());
    std::uniform_int_distribution<int> dist(min, max);
    return dist(gen);
}

std::vector<int> randomIntVector(int size, int min, int max) {
    std::vector<int> result(size);
    for (int i = 0; i < size; ++i) {
        result[i] = randomInt(min, max);
    }
    return result;
}

int main() {
    // Example usage
    int size = 10;
    int min = 1;
    int max = 100;
    
    // Generate a random vector of integers
    std::vector<int> randomVec = randomIntVector(size, min, max);
    
    // Print the generated vector
    std::cout << "Random vector:" << std::endl;
    printVector(randomVec);
    
    return 0;
}