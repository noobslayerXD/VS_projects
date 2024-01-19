#pragma once
#include <string>
#include<iostream>

class Person
{
public:
	Person(const std::string &navn, const char *personnummer, int vaccineStatus);
	std::string getNavn() const;
	const char* getPersonnummer() const;
	int getVaccineStatus() const;
	virtual void print() const;
	Person& operator++();
	Person operator++(int);

	virtual ~Person() = default;
protected:
	std::string navn_;					// Ingen restriktioner
	char personnummer_[12];				// Ingen restriktioner
	int vaccineStatus_;					// gyldige værdier 0, 1, 2 - default 0
};