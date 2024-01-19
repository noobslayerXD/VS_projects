#pragma once
#include "Filter.h"

class LowPassFilter
{
private:
	double threshhold_;
public:
	LowPassFilter(double threshold);
	double transform(double threshold) const;
};

