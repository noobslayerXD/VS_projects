#pragma once
#include <iostream>

class Person
{
public:
	Person(const int id, const int age) :id_(id), age_(age) {}
	virtual ~Person();
	void setId(const int id) { id_ = id; }
	int getId() const { return id_; }
	void setAge(const int age) { age_ = age; }
	int getAge()const { return age_; }
	int calcSalary() {}
	void print() {
		std::cout << "The id is: " << getId() << std::endl;
		std::cout << "The age is: " << getAge() << std::endl;
	}
protected:
	int id_;
	int age_;
};