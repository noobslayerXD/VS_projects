#include "person.h"
#include <iostream>

Person::Person(int id, int age) : id_(id), age_(age) { setId(id); setAge(age); }

Person::~Person() {}

void Person::setId(int id) {
	// Tilføj validering baseret på tilladte værdier
	if (id >= 1000 && id <= 9999) {
		id_ = id;
	}
	else {
		std::cerr << "Ugyldig id-værdi. Skal være mellem 1000 og 9999." << std::endl;
	}
}

int Person::getId() const {
	return id_;
}

void Person::setAge(int age) {
	// Tilføj validering baseret på tilladte værdier
	if (age >= 15 && age <= 67) {
		age_ = age;
	}
	else {
		std::cerr << "Ugyldig alder. Skal være mellem 15 og 67." << std::endl;
	}
}

int Person::getAge() const {
	return age_;
}

int Person::calcSalary() const {
	// Default implementation for Person
	return 0;
}

void Person::print() const {
	std::cout << "ID: " << id_ << ", Age: " << age_;
}