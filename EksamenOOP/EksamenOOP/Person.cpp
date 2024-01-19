#include "Person.h"
#include "PriorityQueue.h"

Person::Person(const std::string& name, int age): name_(name), age_(age)
{
}

std::string Person::toString() const
{
	return "Name:" + name_ + " Age:" + std::to_string(age_);
}


bool operator<(const Person& left, const Person& right)
{
	return true;
	//for( PriorityQueue peek())
}