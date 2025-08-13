#pragma once
#include <string>

class Person
{
public:
	Person(const std::string&, int);
	std::string toString() const;

	friend bool operator<(const Person& left, const Person& right);

private:
	std::string name_;
	int age_;
};
