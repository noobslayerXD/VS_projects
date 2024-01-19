#include "Tur.h"

Tur::Tur() {}

void Tur::tilfoejAfsnit(const Afsnit& nytAfsnit) 
{
	delAfsnit_.push_back(nytAfsnit);
}

Afsnit Tur::beregnFugleflugslinje() 
{
	Afsnit samlet;

	for (std::vector<Afsnit>::iterator it = delAfsnit_.begin(); it != delAfsnit_.end(); it++)
	{
		
		samlet =samlet + *it;
	}

	return samlet;
}