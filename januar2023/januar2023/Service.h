#pragma once
#include "FakturaLinje.h"
#include <string>

class Service:public FakturaLinje
{
private:
	bool momsPligtig_;
public:
	Service(std::string navn, double enhedspris, double antal, bool momspligt);
	double beregnPris() const override;
	void print() const;
};

