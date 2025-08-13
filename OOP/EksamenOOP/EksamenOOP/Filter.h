#pragma once
class Filter
{
public:
	virtual double transform(double value) const = 0;
};

