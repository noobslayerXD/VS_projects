//del (a

#include <iostream>
#include <cmath>
using namespace std;

void mid_value(const double* , const double* , double*);
void min_max_value(double , double , double*, double* );



void mid_value(const double* left, const double* right, double* middle)
{
	*middle = (*left + *right) / 2;
}

void min_max_value(double left, double right, double* min, double* max)
{
	if (left > right)
	{
		*min = right;
		*max = left;
	}
	else
	{
		*min = left;
		*max = right;
	}
}


//del (b
int main()
{
	double x, y;

	cout << "Skriv venligst det første decimaltal: ";
	cin >> x;
	cout << "\n Skriv venligst det andet decimaltal: ";
	cin >> y;

	
	cout << min_max_value(x,y)<<"\n";
	cout << mid_value(x, y);

}