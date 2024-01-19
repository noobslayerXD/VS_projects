#include "Sodavand.h"

Sodavand::Sodavand(double standartVolumen, const std::string& smag)
	:Drikkevarer(standartVolumen)
{
	smag_ = smag;
}

std::string Sodavand::getType() const
{
	return smag_ + "sodavand";
}
