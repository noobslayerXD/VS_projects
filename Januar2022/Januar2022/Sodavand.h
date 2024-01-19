#pragma once
#include <string>
#include "Drikkevarer.h"

class Sodavand : public Drikkevarer
{
private:
	std::string smag_;
public:
	Sodavand(double standartVolumen, const std::string& smag);
	std::string getType()  const override;

};

