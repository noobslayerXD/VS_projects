#include "Modulo.h"

Modulo::Modulo(int value, int mod)
{
	value_ = value % mod;

	try
	{
		value_ = value > 0;
		mod_ = mod >= 1;
	}

	catch (std::invalid_argument& ia)
	{
		std::cerr << "Invalid argument: " << ia.what() << '\n';
	}
}

int Modulo::getMod()
{
	return mod_;
}
int Modulo::getValue()
{
	return value_;
}

std::ostream& operator<< (std::ostream& os, const Modulo& m)
{
	os << m.value_ << " mod " << m.mod_ << std::endl;

	return os;
}
double operator+ (const Modulo& m1, const Modulo& m2)
{
	return (m1.value_ + m2.value_) % m1.mod_;
	try
	{
		m1.mod_ != m2.mod_;
	}

	catch (std::invalid_argument& ia)
	{
		std::cerr << "Invalid argument: " << ia.what() << '\n';
	}
}
double operator* (const Modulo& m1, const Modulo& m2)
{
	return (m1.value_ * m2.value_) % m1.mod_;
	try
	{
		m1.mod_ != m2.mod_;
	}

	catch (std::invalid_argument& ia)
	{
		std::cerr << "Invalid argument: " << ia.what() << '\n';
	}
}
