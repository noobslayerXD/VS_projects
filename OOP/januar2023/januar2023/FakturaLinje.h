#pragma once
#include <string>

class FakturaLinje 
{
private:
	std::string navn_;

protected:
	double enhedsPris_ ;
	double antal_ ;

public:
	FakturaLinje(std::string navn, double enhedspris, double antal);
	virtual ~FakturaLinje();

	virtual double beregnPris() const =0;
	virtual void print() const;
};