#pragma once 
#include <vector>


template <typename T>
class Stack {
private:
	std::vector<T> elements;
public:
	// Default constructor
	Stack() {} // Initialize the elements vector

	
	// Get a copy of the top element of the stack
	T peek() const 
	{	
		return elements.back();
	}
	

	// Push an element onto the stack
	void push(const T& t) 
	{
		elements.push_back(t);
	}

	// Pop and remove the top element from the stack
	void pop() 
	{
		elements.pop_back();
	}

};