#pragma once
#include <string>

class Drikkevarer
{
private:
	double standartVolumen_;
public:
	Drikkevarer(double standartVolumen);
	~Drikkevarer();
	void print() const;
	virtual std::string getType() const=0;
};

