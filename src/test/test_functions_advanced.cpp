#include <iostream>
#include <vector>
#include <random>
#include <algorithm>

// Generate random integer between min and max (inclusive)
int randomInt(int min, int max) {
    static std::random_device rd;
    static std::mt19937 gen(rd());
    std::uniform_int_distribution<int> dist(min, max);
    return dist(gen);
}

// Generate random double between min and max (inclusive)
double randomDouble(double min, double max) {
    static std::random_device rd;
    static std::mt19937 gen(rd());
    std::uniform_real_distribution<double> dist(min, max);
    return dist(gen);
}

// Custom data structure representing a point in 2D space
struct Point {
    double x;
    double y;
    
    Point(double x, double y) : x(x), y(y) {}
};

// Random class representing a Person
class Person {
private:
    std::string name;
    int age;
public:
    Person(std::string name, int age) : name(name), age(age) {}
    
    void displayInfo() {
        std::cout << "Name: " << name << ", Age: " << age << std::endl;
    }
};

// Random class representing a Circle
class Circle {
private:
    double radius;
public:
    Circle(double radius) : radius(radius) {}
    
    double getArea() {
        return 3.14159 * radius * radius;
    }
};

// Custom data structure representing a stack (using vector)
template<typename T>
class Stack {
private:
    std::vector<T> elements;
public:
    void push(const T& element) {
        elements.push_back(element);
    }
    
    void pop() {
        if (!elements.empty()) {
            elements.pop_back();
        }
    }
    
    const T& top() const {
        if (!elements.empty()) {
            return elements.back();
        }
        throw std::out_of_range("Stack is empty");
    }
    
    bool empty() const {
        return elements.empty();
    }
};

int main() {
    // Example usage
    
    // Generate random vector of integers
    std::vector<int> randomVec(10);
    std::generate(randomVec.begin(), randomVec.end(), []() { return randomInt(1, 100); });
    
    // Print the generated vector
    std::cout << "Random vector:" << std::endl;
    for (int num : randomVec) {
        std::cout << num << " ";
    }
    std::cout << std::endl;
    
    // Create random Person objects
    Person person1("Alice", randomInt(20, 40));
    Person person2("Bob", randomInt(20, 40));
    
    // Display information about the persons
    std::cout << "\nPerson 1:\n";
    person1.displayInfo();
    std::cout << "Person 2:\n";
    person2.displayInfo();
    
    // Create a random Circle object
    Circle circle(randomDouble(1.0, 10.0));
    
    // Calculate and print the area of the circle
    std::cout << "\nArea of the circle: " << circle.getArea() << std::endl;
    
    // Create a stack of integers
    Stack<int> intStack;
    intStack.push(10);
    intStack.push(20);
    intStack.push(30);
    
    // Print the top element of the stack
    std::cout << "\nTop element of the stack: " << intStack.top() << std::endl;
    
    // Pop elements from the stack until it's empty
    std::cout << "Popping elements from the stack: ";
    while (!intStack.empty()) {
        std::cout << intStack.top() << " ";
        intStack.pop();
    }
    std::cout << std::endl;
    
    return 0;
}
