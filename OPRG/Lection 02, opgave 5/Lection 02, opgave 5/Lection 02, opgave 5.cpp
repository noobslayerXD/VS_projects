// Lection 02, opgave 5.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
using namespace std;

int main()
{
    double x;
    double y;
    cin >> x;
    cin >> y;
    if (x > y)
    {
        cout << "the first number is biggest"<<endl;
    }
    else if (x < y)
    {
        cout << "the second number is biggest" << endl;
    }
    else
    {
        cout << "they are the same number" << endl;
    }
    cout << "summen af tallene er: " << x + y <<endl ;
    cout << "produktet af tallene er: " << x * y << endl;
}


