#include <iostream>

using namespace std;


double beregnKraft(double q1, double q2, double afstand)
{

	const double k = 8.98877e9;

	double f = k * q1 * q2 / (afstand * afstand);
	return f;
}

int main()
{
	
	double q1, q2, afstand;
	
	cout << "hvad er ladningen af den ene partikel: ";
	cin >> q1;
	cout << "hvad er ladningen af den anden partikel: ";
	cin >> q2;
	cout << "hvad er afstanden mellem de to partikler i meter: ";
	cin >> afstand;
	
	double f = beregnKraft(q1, q2, afstand);
	cout << f;
	return 0;
}

