// Lektion 03 - Opgave 2.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
using namespace std;

int main() {
    // Få input fra brugeren
    int n;
    cout << "Indtast et positivt heltal: ";
    cin >> n;

    // Tjek om n er positivt og lige
    if (n < 0) {
        cout << "Tallet skal være positivt!" << endl;
    }
    else if (n % 2 == 1) {
        cout << "Tallet skal være lige!" << endl;
    }
    else {
        // Iterér gennem de lige tal op til n ved hjælp af en while-løkke
        int i = 0;
        while (i <= n) {
            cout << i << " ";
            i += 2;
        }
        cout << endl;
    }
    return 0;
}