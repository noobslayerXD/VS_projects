// Sommereksamen2.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
using namespace std;

int main()
{
    string navn;
    int alder;
    
    cout << "skriv dit fornavn: ";
    cin >> navn;
    cout << "skriv din alder: ";
    cin >> alder;
    cout << "du hedder " << navn<<endl;
    cout << "Dit fornavn har " << navn.length()<< " bogstaver"<<endl;
    cout << "din alder er " << alder;
    
}
