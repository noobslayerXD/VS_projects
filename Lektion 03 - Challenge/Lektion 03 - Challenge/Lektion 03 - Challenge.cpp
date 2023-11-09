// Lektion 03 - Challenge.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
using namespace std;
#include <cmath>

int main()
{
    double x1=-1;
    double x2=3;
    double y1 = exp(x1);
    double y2 = exp(x2);
    double midt = y1 + y2;
    int i = 0;
    while (i < 10) {
        if (midt < 0) 
        {
            x1 = x1 + 0.2;
            double midt = y1 + y2;
        }
        else if (midt > 0) 
        {
            x2 = x2 - 0.5;
            double midt = y1 + y2;
        }
        i++;
    }
    cout << midt;

}

