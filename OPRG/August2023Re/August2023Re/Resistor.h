#pragma once
class Resistor
{
public:
	Resistor(double resistance = 1.0)
	{
		setResistance(resistance);
	}

	double getResistance() const
	{
		return resistance_;
	}

	void setResistance(double resistance)
	{
		resistance_ = resistance < 0 ? 1.0 : resistance;
	}

private:
	double resistance_;
};

