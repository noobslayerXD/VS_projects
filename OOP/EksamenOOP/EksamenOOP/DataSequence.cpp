#include "DataSequence.h"

void DataSequence::add(double data)
{
	sequence.push_back(data);
}

DataSequence& apply_filter(const Filter& filter)
{
	(*filter) = Filter::transform(sequence);
	
}


std::ostream& operator<<(std::ostream& os, const DataSequence& seq)
{
	std::vector<const DataSequence*>::const_iterator iter;

	for (iter = sequence.begin(); iter != sequence.end(); iter++)
	{
		os << (*iter)<<" , ";
	}
		return os;
}
