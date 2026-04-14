#include <"functions1.hpp">
#include <"excersise1.3/functions1.hpp">
#include <iostream>
#include <cmath>
using namespace std;


float circleArea(float r)
{
	return (3.14 * r * r);
}


int rectangleArea(int a, int b)
{
	return (a * b);
}


float triangleArea(int a, int b, int c)
{
	if (a + b < c || a + c < b || b + c < a)
	{
		printf("\nDette er IKKE en trekant!\n");
		return 0;
	}
	else
	{
		float s = 0.5 * (a + b + c);
		return (sqrt(s * (s - a) * (s - b) * (s - c)));
	}
}


int isEqual(char c1, char c2)
{
	return (c1 == c2);
}


void charToASCII(char c)
{
	cout << "Tegnet " << c << " har ASCII vaerdien " << (int)c << endl;
}