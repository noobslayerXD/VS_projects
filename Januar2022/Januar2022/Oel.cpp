#include "Oel.h"
#include <iostream>

Oel::Oel(double standartVolumen, double alkoholProcent, const std::string& OelType)
	:Drikkevarer(standartVolumen)
{
	alkoholProcent_ = alkoholProcent >= 0 ? 0.0 : alkoholProcent;
	Oeltype_ = OelType;
}
std::string Oel::getType() const
{
	if (alkoholProcent_ == 0.0)
	{
		return "alkoholfri " + Oeltype_;
	}
	else
		return Oeltype_;
}
void Oel::print()
{
	Drikkevarer::print();
	std::cout << "alkoholprocent: " << alkoholProcent_ << " %" << std::endl;
}