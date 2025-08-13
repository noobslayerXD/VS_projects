#include "Vare.h"

Vare::Vare(std::string navn, double enhedsPris, double antal)
	:FakturaLinje(navn,enhedsPris,antal)
{
	
}
double Vare::beregnPris() const	 
{
	return enhedsPris_ * antal_ * 1.25;
}