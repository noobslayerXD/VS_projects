// Opgave 3.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
using namespace std;
int SumUpTo(int i);
int main()
{
    int i;
    cout << "skriv et positivt heltal: ";
    cin >> i;
    int total = SumUpTo(i);
    cout <<total;
    return 0;
}
//finder summen af talle op og med i
int SumUpTo(int i)
{
    int total = i * (i + 1) / 2;
    return total;
}
