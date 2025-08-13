#include "Kapacitor.h"
#include <iostream>



Kapacitor::Kapacitor(double kapacitans)
{
	if (kapacitans < lower_bound_)
	{
		this->kapacitans_ = lower_bound_;
		std::cerr << "Det er for small :(" << std::endl;
	}
	else
		this->kapacitans_ = kapacitans;
}

double Kapacitor::lower_bound_ = 1.0e-10;

Kapacitor operator|(const Kapacitor& k1, const Kapacitor& k2)
{
	return Kapacitor(k1.kapacitans_+k2.kapacitans_);
}

Kapacitor operator&(const Kapacitor& k1, const Kapacitor& k2)
{
	double nederdel= (1/k1.kapacitans_) + (1/k2.kapacitans_);

	return 1 / nederdel;
}

std::ostream& operator<<(std::ostream& os, const Kapacitor& k)
{
	os << k.kapacitans_ << " F";

	return os;
}