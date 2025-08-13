#pragma once
#include <string>
#include "Drikkevarer.h"

class Oel: public Drikkevarer
{
private:
	std::string Oeltype_;
	double alkoholProcent_;
public:
	Oel(double standartVolumen, double alkoholProcent, const std::string& OelType);
	std::string getType() const override;
	void print() ;
};

