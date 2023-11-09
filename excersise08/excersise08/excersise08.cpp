#include <iostream>
#include <string>
#include "bubblesort.h" // Include the header file with your bubbleSort function
#include "person.h"
//#include "reverse.h"
#include "Stack.h"

bool compareByAge(const Person& a, const Person& b) {
    return a.getAge() < b.getAge();
}


int main() {
    // Create an unsorted vector of integers
    std::vector<int> data = { 5, 2, 9, 3, 1 };

    // Call your bubbleSort function to sort the vector
    bubbleSort(data);

    // Print the sorted elements
    for (const int& value : data) {
        std::cout << value << " ";
    }

    std::vector<Person> people;
    people.push_back(Person("Alice", 25));
    people.push_back(Person("Bob", 30));
    people.push_back(Person("Charlie", 20));
    
    // Sort the vector of Person objects by age
    std::sort(people.begin(), people.end(), compareByAge);
    std::cout << "\nsorted by age:\n";
    
    // Print the sorted list
    for (const Person& person : people) {
        std::cout << "Name: " << person.getName() << ", Age: " << person.getAge() << std::endl;
    }

    // Reverse the vector using std::reverse
    std::reverse(data.begin(), data.end());

    // Print the reversed vector
    for (const int& number : data) {
        std::cout << number << " ";
    }
    
    Stack<int> intStack;

    intStack.push(10);
    intStack.push(20);
    intStack.push(30);

    std::cout << "Top of the stack: " << intStack.peek() << std::endl;

    intStack.pop();

    std::cout << "Top of the stack after popping: " << intStack.peek() << std::endl;

    return 0;
}
