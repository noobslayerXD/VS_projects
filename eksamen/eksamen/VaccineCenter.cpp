#include "VaccineCenter.h"
#include <iterator>

using namespace std;

void Vaccinecenter::tilføjPersonTilKø(Person& nyPersonIKø)
{
	if (nyPersonIKø.getVaccineStatus() < 2)
		kø_.push_back(&nyPersonIKø);
}
void Vaccinecenter::fjernPersonFraKø()
{
	(*(kø_.front()))++;

	cout << "\nDenne person er nu vaccineret og er ikke i køen mere";

	(kø_.front())->print();

	kø_.pop_front();
}
void Vaccinecenter::print() const 
{
	deque<Person*>::const_iterator iter;

	std::cout << "personer i kø" << std::endl;

	for (iter = kø_.begin(); iter != kø_.end(); iter++)
	{
		(*iter)->print();
	}
}
