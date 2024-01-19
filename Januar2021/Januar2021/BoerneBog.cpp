#include "BoerneBog.h"



BoerneBog::BoerneBog(const std::string& titel, const std::string& forfatter, int minimumsAlder)
	:Bog(titel,forfatter)
{
	setMinimumsAlder(minimumsAlder);
}

int BoerneBog::getMinimumsAlder() const
{
	return minimumsAlder_;
}

void BoerneBog::setMinimumsAlder(int minimumsAlder)
{
	minimumsAlder_ = minimumsAlder <= 0 ? 0 : minimumsAlder;
}