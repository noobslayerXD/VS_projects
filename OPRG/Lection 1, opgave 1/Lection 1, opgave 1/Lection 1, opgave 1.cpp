// Lection 1, opgave 1.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
#include <string>
using namespace std;

int main()
{
    cout << "Skriv strømmen i mA\n";
    int current;
    cin >> current;
    cout << "skriv modstanden i ohm\n";
    int resistance;
    cin >> resistance;
    cout << "Spændingen er:"; 
    int voltage = (current * 0.001) * resistance;
    cout << voltage;cout << " V\n";
    int power = voltage * current;
    cout << "effekten er: "; cout << power; cout << "W";

}


