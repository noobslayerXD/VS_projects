#include "employee.h"
#include <iostream>

Employee::Employee(int id, int age, int step) : Person(id, age) {
	setStep(step);
}

Employee::~Employee() {}

void Employee::setStep(int step) {
	if (step >= 10 && step <= 40) {
		step_ = step;
	}
	else {
		std::cerr << "Ugyldig step-værdi. Skal være mellem 10 og 40." << std::endl;
	}
}

int Employee::getStep() const {
	return step_;
}

int Employee::calcSalary() const {
	return step_ * 1000; // Hvert step udløser 1000 kr. pr. måned
}

void Employee::print() const {
	Person::print();
	std::cout << ", Step: " << step_ << ", Salary: " << calcSalary() << " kr." << std::endl;
}