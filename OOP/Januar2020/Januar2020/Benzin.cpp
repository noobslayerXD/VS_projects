#include "Benzin.h"
#include <iostream>


// I denne fil skal du indsætte koden fra opgave 2.E
Benzin::Benzin(double pris, int oktan)
	:Braendstof(pris)
{
	setOktan(oktan);
	//setPrisPerLiter(pris);
}

int Benzin::getOktan() const
{
	return oktan_;
}

void Benzin::setOktan(int oktan)
{
	oktan_ = (88 <= oktan && oktan <= 101) ? oktan : 95;
}

void Benzin::printBeskrivelse() const
{
	std::cout << "Benzin med oktantal " << oktan_ << std::endl;
	std::cout << "Pris pr. Liter: " << getPrisPerLiter() <<" kr. " << std::endl;
}