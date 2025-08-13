#include "/Users/Jacob/source/repos\Couloumb.h"


double beregnKraft(double q1,double q2,double afstand)
{
	
	const double k = 8.98877e9;

	double f = k * q1 * q2 / (afstand * afstand);
	return f;
}