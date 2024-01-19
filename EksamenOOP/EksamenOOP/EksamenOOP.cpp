// EksamenOOP.cpp : This file contains the 'main' function. Program execution begins and ends there.
#include <iostream>
#include "Modulo.h"
#include "LowPassFilter.h"
#include "DataSequence.h"

int main()
{
    std::cout << "Opgave 1"<<std::endl;

    Modulo m(2,4);

    std::cout << m << std::endl;

    LowPassFilter lp1(8);


    //std::cout << lp1.transform(10) << std::endl;
}