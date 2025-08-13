#include "Optankning.h"
#include <iostream>
using namespace std;

// I denne fil skal du tilføje kode for at svare på Opgave 2.G
Optankning::Optankning( double liter, double meter, Braendstof* braendstofptr)
{
	antalLiter_ = liter <= 0 ? liter : 0;
	antalKilometer_ = meter <= 0 ? meter : 0;
	braendstofPtr_ = braendstofptr;
}


void Optankning::printInformation() const 
{
	double okonomi;
	if (antalLiter_ > 0)
		okonomi = antalKilometer_ / antalLiter_;
	else
		okonomi = -1;

	cout << "Optankning paa " << antalLiter_ << " liter" << endl;
	if (braendstofPtr_ != nullptr)
		braendstofPtr_->printBeskrivelse();
	cout << "Der blev koert " << okonomi << " km/liter" << endl;
}
