#pragma once
#include "Filter.h"

class HighPassFilter
{
private:
	double threshhold_;
public:
	HighPassFilter(double threshold);
	double transform(double threshold) const;
};

