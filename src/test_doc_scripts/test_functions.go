package main

import "fmt"

// Node represents a node in the linked list
type Node struct {
	data int
	next *Node
}

// LinkedList represents a linked list
type LinkedList struct {
	head *Node
}

// Append adds a new node with the given data to the end of the linked list
func (ll *LinkedList) Append(data int) {
	newNode := &Node{data: data, next: nil}
	if ll.head == nil {
		ll.head = newNode
		return
	}
	lastNode := ll.head
	for lastNode.next != nil {
		lastNode = lastNode.next
	}
	lastNode.next = newNode
}

// Display prints the elements of the linked list
func (ll *LinkedList) Display() {
	current := ll.head
	for current != nil {
		fmt.Printf("%d -> ", current.data)
		current = current.next
	}
	fmt.Println("nil")
}

// Function to calculate the factorial of a number
func factorial(n int) int {
	if n == 0 {
		return 1
	}
	return n * factorial(n-1)
}

// Function to check if a number is prime
func isPrime(n int) bool {
	if n <= 1 {
		return false
	}
	if n <= 3 {
		return true
	}
	if n%2 == 0 || n%3 == 0 {
		return false
	}
	i := 5
	for i*i <= n {
		if n%i == 0 || n%(i+2) == 0 {
			return false
		}
		i += 6
	}
	return true
}

func main() {
	// Test the square function
	fmt.Println("Square of 5:", square(5))

	// Test the factorial function
	fmt.Println("Factorial of 5:", factorial(5))

	// Test the isPrime function
	fmt.Println("Is 17 prime?", isPrime(17))
}