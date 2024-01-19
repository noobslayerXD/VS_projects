#pragma once
#include "Bog.h"

class BoerneBog:public Bog
{
private:
	int minimumsAlder_;
public:
	BoerneBog(const std::string& titel, const std::string& forfatter, int minimumsAlder);

	int getMinimumsAlder() const override;

	void setMinimumsAlder(int minimumsAlder);

};

