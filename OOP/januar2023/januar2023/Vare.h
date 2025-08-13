#pragma once
#include <string>
#include "FakturaLinje.h"

class Vare:public FakturaLinje
{
private:

public:
	Vare(std::string navn, double enhedsPris, double Antal);
	double beregnPris() const override;

};

