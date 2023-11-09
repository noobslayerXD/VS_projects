// Uge10_Opgave1.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include "Header.h"
#include<cmath>
int main()
{
    double v, r;
    std::cout << "This program calculates the power dissipated in a simple resistance circuit" << std::endl;
    std::cout << "Input the power source voltage [V]" << std::endl;
    std::cin >> v;
    std::cout << "Input resistance R[Ohm]" << std::endl;
    std::cin >> r;
    double power = pow(v, 2) / r;
    std::cout << "the power dissipated in R is " << power << " Watts";
    return 0;
}

// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
