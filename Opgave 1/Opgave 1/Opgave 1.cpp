// Opgave 1.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
using namespace std;
int main()
{
    int n;
    int total = 0;
    cout << "skriv et positivt heltal: ";
    cin >> n;
    for (int i=1; i <= n; i++)
    {
        total += i;
    }
    cout << total;
}

