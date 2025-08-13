// Januar2021.cpp : This file contains the 'main' function. Program execution begins and ends there.

#include <iostream>
#include "Resistor.h"
#include "Erotik.h"
#include "BoerneBog.h"

int main()
{
    Resistor r1(100);
    Resistor r2(1);
    r1.setResisance(5);
    r2.setConductance(10);
    std::cout << r1.getResistance() << " og " << r1.getConductance()<< std::endl;
    std::cout << r2.getResistance() << " og " << r2.getConductance() << std::endl;

    Resistor r3= r1 && r2;

    Resistor a(5), b(15); 
    Resistor c, d; 
    c = a && b; 
    d = a || b;

    std::cout << c.getResistance() << std::endl;
    std::cout << d.getResistance() << std::endl;

    std::cout << r3.getResistance() << std::endl;


    std::cout << "Opgave 2" << std::endl;

    Erotik kink("50 shades of grey", "E.L.James");
    kink.print();

    BoerneBog hygge("Hodja fra Pjort", "Ole Lund Kirkegaard", 8);
    hygge.print();


}
