// Opgave 2.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include <iostream>
using namespace std;


int main()
{
	int i;
	cout << "skriv lige et eller andet positivt heltal: ";
	cin >> i;
	for (int j = 1; j <= i; j++) 
	{
		if (j % 2==0)
		{
			cout << j<<endl;
		}
	}
}


