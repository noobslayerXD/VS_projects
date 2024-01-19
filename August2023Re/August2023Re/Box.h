#pragma once

#include "Resistor.h"

class Box
{
public:
	Box(int size = 5);
	~Box();

	void addResistor(const Resistor& r);
	void print() const;

	Box(const Box& copyMe);

	const Box& operator=(const Box& copyMe);

private:
	Resistor* resistors_;
	int size_;
	int noOfResistors_;
};

