#include "HighPassFilter.h"

HighPassFilter::HighPassFilter(double threshold)
{
	threshhold_ = threshold < threshhold_ ? threshhold_ : threshold;
}

double HighPassFilter::transform(double threshold) const
{
	if (threshold > threshhold_)
	{
		return threshhold_;
	}
}