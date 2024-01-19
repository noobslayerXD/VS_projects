//rectangle.cpp
#include "Rectangle.h"
#include <iostream>

Rectangle::Rectangle(const Point& corner, double height, double width)
	:upperleftcorner(corner), height(height), width(width) {}


void Rectangle::print() const 
{
	std::cout << "Rectangle med upper left corner " <<upperleftcorner.x<<", " << upperleftcorner.y << std::endl;
	std::cout << "hoejde " << height << std::endl;
	std::cout << "bredde " << width << std::endl;
	std::cout << "areal " << area() << std::endl;
	std::cout << "omkreds " << circumference() << std::endl;
}

double Rectangle::area() const 
{
	return height * width;
}
double Rectangle::circumference() const
{
	return 2 * (height + width);
}