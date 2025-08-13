#pragma once
#include "Shape.h"
#include "Point.h"

class Circle :public Shape
{
public:
	Circle(const Point& center, double radius);
	void print() const override;
	double area() const override;
	double circumference() const override;

private:
	Point center;
	double radius;
};


