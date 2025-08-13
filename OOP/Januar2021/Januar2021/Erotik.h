#pragma once
#include "Bog.h"
#include <string>

class Erotik: public Bog
{
private:
	

public:
	Erotik(const std::string& titel, const std::string& forfatter);
	

	int getMinimumsAlder() const override;
	
};

