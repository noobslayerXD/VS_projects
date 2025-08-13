//rectangle.h
#pragma once
#include "Shape.h"
#include "Point.h"

class Rectangle :public Shape 
{
public:
	Rectangle(const Point& corner, double height, double width);
	void print() const override;
	double area() const override;
	double circumference() const override;

private:
	Point upperleftcorner; 
	double height, width;
};


