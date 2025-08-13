#pragma once

#include "Braendstof.h"

// Denne fil skal du tilrette for at svare på Opgave 2.G

class Optankning: public Braendstof
{
public:
	void printInformation() const;
	Optankning( double liter, double meter, Braendstof* braendstofptr);

private:
	Braendstof* braendstofPtr_;
	double antalLiter_;
	double antalKilometer_;
};

