#pragma once
class Resistor
{
private:
	double resistance_;
public:

	Resistor(double resistance=1);

	double getResistance() const;
	double getConductance() const;
	void setResisance(double);
	void setConductance(double);

	friend Resistor operator||(const Resistor&, const Resistor&);
	friend Resistor operator&&(const Resistor&, const Resistor&);

};

