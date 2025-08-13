#include "Resistor.h"

Resistor::Resistor(double resistance)
{
	setResisance(resistance);
	
}

double Resistor::getResistance() const
{
	return resistance_;
}
double Resistor::getConductance() const
{
	return 1 / resistance_;
}
void Resistor::setResisance(double resistance)
{
	resistance_ = resistance < 0 ? 1 : resistance;
	
}
void Resistor::setConductance(double conductance)
{
	resistance_ = 1 / conductance;
}

Resistor operator||(const Resistor& r1, const Resistor& r2)
{
	double denom = (1 / r1.resistance_) + (1 / r2.resistance_);

	return Resistor(1 / denom);
}
Resistor operator&&(const Resistor& r1, const Resistor& r2)
{
	return Resistor(r1.resistance_ + r2.resistance_);
}