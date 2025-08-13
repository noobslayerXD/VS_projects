// januar2023.cpp : This file contains the 'main' function. Program execution begins and ends there.
#include <iostream>
#include "Periode.h"
#include "Vare.h"
#include "Service.h"
#include "FakturaLinje.h"
#include <vector>

int main()
{
	std::cout << "Opgave 1" << std::endl;

	Periode p1(1, 1, 650);
	Periode p2(3, 5, 1200);
	p1.print();
	p2.print();

	Periode q1(1, 3, 4000.0), q2(4, 6, 1800.0);
	Periode h2Total;
	h2Total = q1 + q2;
	h2Total.print();

	std::cout << "Opgave 2" << std::endl;

	Service s1("kram", 1, 10000, false);
	Vare v1("vand", 100, 20);
	s1.print();
	v1.print();


	std::vector<FakturaLinje*> faktura;
	faktura.push_back(&s1);
	faktura.push_back(&v1);

	for (std::vector<FakturaLinje*>::iterator it = faktura.begin(); it != faktura.end(); it++)
	{
		(*it)->print();
	}



	return 0;
}
