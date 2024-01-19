#pragma once
#include "Braendstof.h"

// Denne fil skal du tilrette for at svare på opgave 2.D

class Benzin:public Braendstof
{
public:
	Benzin(double, int);
	int getOktan() const;
	void setOktan(int oktan);
	void printBeskrivelse() const override;

private:
	int oktan_;
};

