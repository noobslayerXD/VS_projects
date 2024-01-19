#pragma once
#include <vector>
#include "Afsnit.h"

class Tur:public Afsnit
{
private:
	std::vector<Afsnit> delAfsnit_;

public:
	Tur();
	void tilfoejAfsnit(const Afsnit&) ;
	Afsnit beregnFugleflugslinje() ;
};

