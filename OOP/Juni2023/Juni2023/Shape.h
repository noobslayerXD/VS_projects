#pragma once
class Shape
{
public:
	virtual ~Shape() = default;
	virtual void print() const = 0;
	virtual double area() const = 0;
	virtual double circumference() const = 0;
};

