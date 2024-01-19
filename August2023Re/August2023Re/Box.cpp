#include "Box.h"
#include "Resistor.h"
#include <iostream>
using namespace std;

Box::Box(int size)
{
	size_ = size > 0 ? size : 5;
	noOfResistors_ = 0;
	
	// Her mangler kode
	
	resistors_ = new Resistor[size_];
	
}

Box::~Box()
{
	// Her mangler kode
	delete[] resistors_;
}

void Box::addResistor(const Resistor& r)
{
	if (noOfResistors_ < size_)
	{
		resistors_[noOfResistors_] = r;
		noOfResistors_++;
	}
}

void Box::print() const
{
	cout << "Der er " << noOfResistors_ << " i en Box med plads til " << size_ << endl;
	for (int i = 0; i < noOfResistors_; i++)
	{
		cout << "Resistor nr. " << i + 1 << ": har modstanden " << resistors_[i].getResistance() << endl;
	}
}
