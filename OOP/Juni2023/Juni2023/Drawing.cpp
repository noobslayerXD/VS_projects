#include "Drawing.h"
#include <iostream>
#include <list>

Drawing::Drawing(int id)
{
	this->id = id;
}

Drawing::~Drawing(){}

void Drawing::print() const
{
	std::cout << "Drawing med id " << id << std::endl;
	std::cout << "har følgende elementer " << std::endl << std::endl;

	// For løkker med iteratorer evt. med brug af auto er også OK 
	for (Shape* p : shapes) 
		p->print();

	std::cout << std::endl; 
	std::cout << "Totalt Areal: " << area() << std::endl; 
	std::cout << "Total Omkreds: " << circumference() << std::endl;
}

double Drawing::area() const
{
	double sum=0;
	for (auto it = shapes.begin(); it != shapes.end(); it++)
		sum += (*it)->area();

	return sum;
}

double Drawing::circumference() const
{
	double sum = 0;
	for (Shape* p : shapes)
		sum += p->circumference();
	
	return sum;
}

void Drawing::add(Shape* shape)
{
	shapes.push_back(shape);
}