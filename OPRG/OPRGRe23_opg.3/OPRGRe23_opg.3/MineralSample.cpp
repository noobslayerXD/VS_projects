//del (d

#include <iostream>
#include "Header1.h"
#include <cmath>
using namespace std;


double dens = wieght / volume;
double dens_gold = 19.30;
double dens_silver = 10.50;

MineralSample()
{
	if (weight < 0 || volume < 0)
	{
		cout << "der skete en fejl";
		weight = 0;
		volume = 1;
	}
	else if (volume == 0)
	{
		cout << "der skete en fejl";
		weight = 0;
		volume = 1;
	}
}

bool is_gold() {
	
	if (abs(dens-dens_gold)) {
		return true;
	}
	else {
		return false;
	}
}
bool is_silver()
{
	if (abs(dens - dens_silver)) {
		return true;
	}
	else {
		return false;
	}
}