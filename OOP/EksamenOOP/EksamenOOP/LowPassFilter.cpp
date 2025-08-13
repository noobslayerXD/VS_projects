#include "LowPassFilter.h"

LowPassFilter::LowPassFilter(double threshold)
{
	threshhold_ = threshold > threshhold_ ? threshhold_ : threshold;
}

double LowPassFilter::transform(double threshold) const
{
	if (threshold < threshhold_)
	{
		return threshhold_;
	}
}