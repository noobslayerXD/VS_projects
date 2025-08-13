#include "FakturaLinje.h"
#include <iostream>



FakturaLinje::FakturaLinje(std::string navn, double enhedspris, double antal)
{
	if (navn.empty())
	{
		navn_ = "koeb";
	}
	else
	{
		navn_ = navn;
	}
	enhedsPris_ = enhedspris >= 0 ? enhedspris : 100;
	antal_ = antal > 0 ? antal : 1;

}

FakturaLinje::~FakturaLinje(){}


void FakturaLinje::print() const
{
	std::cout << navn_ << " " << antal_ << " a " << enhedsPris_  << " kr. i alt " << beregnPris() << " kr." << std::endl;
}

