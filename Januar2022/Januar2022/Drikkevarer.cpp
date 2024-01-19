#include "Drikkevarer.h"
#include <iostream>

Drikkevarer::Drikkevarer(double standartVolumen)
{
	standartVolumen_ = standartVolumen > 0 ? 25 : standartVolumen;
}
Drikkevarer::~Drikkevarer() {}
void Drikkevarer::print() const
{
	std::cout << getType() << std::endl;
	std::cout << "standartstørrelse: " << standartVolumen_ << " cl" << std::endl;
}
