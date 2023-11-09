// Lektion08opgave2.cpp : This file contains the 'main' function. Program execution begins and ends there.

#include <iostream>
struct Vektor
{
    double x, y;
    double angle;
    
    double rotate(double angle)
    {
        x = cos(angle)*x - sin(angle)*y;
        y = sin(angle) * x + cos(angle) * y;
        return x, y;
    }
};
int main()
{
    Vektor haps;
    std::cout << "hvad er vektorens x koordinat: ";
    std::cin >> haps.x ;
    std::cout << "hvad er vektorens y koordinat: ";
    std::cin >> haps.y;
    std::cout << "hvor mange radianer skal vektoren drejes mod urets retning: ";
    std::cin >> haps.angle;
    std::cout<<"Vektorens nye koordinater er: " << haps.rotate(haps.x)<<", "<<haps.rotate(haps.y);
        

}

