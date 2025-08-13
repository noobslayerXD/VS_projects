#include <iostream>

using namespace std;

int main()
{
	int i, j, k;
	string x;
	cout << "skriv et tal: ";
	cin >> i;
	cout << "skriv et tegn'+,-,*,/': ";
	cin >> x;
	cout << "skriv et tal mere: ";
	cin >> j;
	if (x == "/" )
	{
		k = i / j;
	}
	else if (x == "*")
	{
		k = i * j;
	}
	else if (x == "+")
	{
		k = i + j;
	}
	else if (x == "-")
	{
		k = i - j;
	}
	cout << k;
}