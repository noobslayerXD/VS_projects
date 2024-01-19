#pragma once
#include <vector>
#include <iostream>

#include "Filter.h"

class DataSequence:public Filter
{
	friend std::ostream& operator<<(std::ostream& os, const DataSequence& seq);
public:
	void add(double data);
	DataSequence& apply_filter(const Filter& filter);
private:
	std::vector<double> sequence;
};

// Ikke strengt nødvendig, da friend erklæringen også virker som prototype
std::ostream& operator<<(std::ostream& os, const DataSequence& seq);

