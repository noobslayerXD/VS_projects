#pragma once
#include <iostream>
#include <stdexcept >

class Modulo
{
private:
	int value_;
	int mod_;
public:
	Modulo(int value, int mod);

	int getMod();
	int getValue();

	friend std::ostream& operator<< (std::ostream&, const Modulo&);
	friend double operator+ (const Modulo&, const Modulo&);
	friend double operator* (const Modulo&, const Modulo&);
};

