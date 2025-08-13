#pragma once
#include <string>
#include <ostream>
class Kapacitor
{
private:
	double kapacitans_;
	static double lower_bound_;
public:

	//konstructor
	Kapacitor(double kapacitans);
	
	// Operatoroverbelastning for <<
	friend std::ostream& operator<<(std::ostream& os, const Kapacitor&);
	

	// Operatoroverbelastning for |
	friend Kapacitor operator|(const Kapacitor&, const Kapacitor&);

	// Operatoroverbelastning for &
	friend Kapacitor operator&(const Kapacitor&, const Kapacitor&);
};

