// Lection 02, opgave 3.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
using namespace std;
#include <math.h>
int main()
{
    /* we solve the linear system
    * ax+by=e
    * cx+dy=f
    */
    double a;
    double b;
    double c;
    double d;
    double e;
    double f;
    cout << "input the matrix values in order a b c d\n";
    cout << "a :";
    cin >> a;
    cout << "b :";
    cin >> b; 
    cout << "c :";
    cin >> c; 
    cout << "d :";
    cin >> d; 
    cout << "e :";
    cin >> e;
    cout << "f :";
    cin >> f;
    double determinant = a * d - b * c;
    if (determinant != 0) {
        double x = (e * d - b * f) / determinant;
        double y = (a * f - e * c) / determinant;
        printf("Cramer equations system: result, x = %f, y = %f\n", x, y);
    }
    else {
        printf("Cramer equations system: determinant is zero\n"
            "there are either no solutions or many solutions exist.\n");
    }
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
