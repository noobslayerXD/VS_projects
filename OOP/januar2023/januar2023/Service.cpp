#include "Service.h"
#include <iostream>

Service::Service(std::string navn, double enhedsPris, double antal, bool momsPligtig) 
	:FakturaLinje(navn, enhedsPris, antal)
{
	momsPligtig_ = momsPligtig;
}

double Service::beregnPris() const
{
	if (momsPligtig_ == true)
	{
		return enhedsPris_* antal_ * 1.25;
	}
	else
	{
		return enhedsPris_* antal_;
	}
}
void Service::print() const
{
	FakturaLinje::print(); 
	if (momsPligtig_) 
		std::cout << " (momspligtig) " << std::endl; 
	else 
		std::cout << " (ikke momspligtig) " << std::endl;
}