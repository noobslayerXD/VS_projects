// C++ mby C.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include <cmath>
using namespace std;

int calculate(int, int);

int main()
{
   
    int number1 = calculate(1, 2);
    int number2 = calculate(4, 5);
    int resultat = calculate(number1, number2);  
    cout << "Resultatet af beregningen med " << number1 << " og " << number2; 
    cout << " er " << resultat << endl;

}

int calculate(int parameter1, int parameter2) {

    
    // indsæt din egen beregning i næste linie 
    return (exp(parameter1) * sqrt(parameter2));
}

