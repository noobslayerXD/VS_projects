#include "Erotik.h"

Erotik::Erotik(const std::string& titel, const std::string& forfatter)
	:Bog(titel, forfatter)
	{
	
	}

int Erotik::getMinimumsAlder() const
{
	return 18;
}
