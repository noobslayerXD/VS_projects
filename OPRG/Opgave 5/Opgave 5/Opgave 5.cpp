// Opgave 5.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
using namespace std;

int main()
{
    int n;
    cout << "please skriv et tal <3: ";
    cin >>n;
    int fib1 = 0, fib2 = 1, fib3;
    cout << fib1<<endl;
    while (fib2 <= n)
    {
        fib3 = fib1 + fib2;
        if (fib3 <= n)
        {
            cout << fib3<<endl;
        }
        fib1 = fib2;
        fib2 = fib3;
    }
}