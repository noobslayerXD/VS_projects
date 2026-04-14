#include "Circle.hpp"
#include <iostream>

Circle::Circle(const Point& center, double radius)
	: center(center), radius(radius){}

void Circle::print() const
{
	std::cout << "Cirkel med center i " << center.x << ", " << center.y << std::endl;
    std::cout << "cirkel med radius " << radius << std::endl;
	std::cout << "cirkel med areal " << area() << std::endl;
	std::cout << "cirkel med omkreds " << circumference() << std::endl;
}

double Circle::area() const
{
	return 3.1415*radius*radius;
}
double Circle::circumference() const
{
	return 3.1415*radius;
}