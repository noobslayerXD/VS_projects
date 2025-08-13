#pragma once
#include "Shape.h"
#include <list>

class Drawing : public Shape
{
public:
	Drawing(int id);
	~Drawing() override;
	void print() const override;
	double area() const override;
	double circumference() const override;
	void add(Shape* shape);

private:
	int id; 
	std::list<Shape*> shapes;
};
