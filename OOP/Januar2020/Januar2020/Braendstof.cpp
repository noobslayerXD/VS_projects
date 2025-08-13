#include "Braendstof.h"

Braendstof::Braendstof(double pris)
{
	setPrisPerLiter(pris);
}

Braendstof::~Braendstof(){}

double Braendstof::getPrisPerLiter() const
{
	return prisPerLiter_;
}
void Braendstof::setPrisPerLiter(double pris)
{
	prisPerLiter_ = pris > 0 ? pris : 10;
}
