// Lektion 03 - Opgave 3.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
using namespace std;

int main()
{
    int i;
    int x=0;
    cin >> i;
    while (x <= i) {
        int j=1;
        while (j <= 2 * x - 1) {
            cout << "*";
            j++;
        }
        
        cout << endl;;
        x++;
       
    }
    return 0;

}


