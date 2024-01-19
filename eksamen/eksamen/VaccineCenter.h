#pragma once
#include<deque>
#include"Person.h"

class Vaccinecenter
{
public:
	void tilføjPersonTilKø(Person& nyPersonIKø);
	void fjernPersonFraKø();
	void print() const;
private:
	std::deque<Person*> kø_;
};