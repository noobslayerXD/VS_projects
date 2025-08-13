#include "person.h"
#include "Employee.h"
#include "Boss.h"
#include <iostream>
#include <vector>
#include <list>

// Global funktion prototype
void calcTotalSalary(const Person&);

int main() {
	Person person(1234, 25);
	person.print();  // Output: ID: 1234, Age: 25
	std::cout << "\nSalary: " << person.calcSalary() << std::endl;

	Employee employee(1234, 25, 20);
	employee.print();  // Output: ID: 1234, Age: 25, Step: 20, Salary: 20000 kr.

	Boss boss(1200, 16, 20000);
	boss.print(); // Output: ID: 1200, Age: 16, Step: 40, Salary: 60000 kr., Bonus: 20000 kr.

	// Opret et array af Person-pointere
	const int arraySize = 5;
	Person* persons[arraySize];

	// Opret forskellige Employee og Boss objekter og tildel pointerne
	persons[0] = new Employee(1001, 30, 15);
	persons[1] = new Boss(2002, 40, 5000);
	persons[2] = new Employee(3003, 25, 20);
	persons[3] = new Boss(4004, 50, 10000);
	persons[4] = new Employee(5005, 35, 25);

	// Test metoder ved hjælp af for-løkker
	std::cout << "Testing methods via pointers:" << std::endl;
	for (int i = 0; i < arraySize; ++i) {
		persons[i]->print();
		std::cout << ", Salary: " << persons[i]->calcSalary() << " kr." << std::endl;
	}

	// Kald den globale funktion calcTotalSalary ved hjælp af pointerne
	std::cout << "\nCalculating total salary via global function:" << std::endl;
	for (int i = 0; i < arraySize; ++i) {
		calcTotalSalary(*persons[i]);
	}

	// Frigiv hukommelsen allokeret til objekterne
	for (int i = 0; i < arraySize; ++i) {
		delete persons[i];
	}

	return 0;
}

// Global funktion implementering
void calcTotalSalary(const Person& person) {
	std::cout << "ID: " << person.getId() << ", Annual Salary: " << person.calcSalary() * 12 << " kr." << std::endl;
}