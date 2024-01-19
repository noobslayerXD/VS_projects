#include "Kasse.h"

// I denne fil skal du tilføje kode for at svare på Opgave 1.B, 1.C og 1.F
double Kasse::getLengde() const
{
	return lengde_;
}

double Kasse::getBredde() const
{
	return bredde_;
}

double Kasse::getHojde() const
{
	return hojde_;
}

void Kasse::setLengde(double l)
{
	lengde_ = (l > 0) ? l : 10;
}

void Kasse::setBredde(double b)
{
	bredde_ = (b > 0) ? b : 10;
}

void Kasse::setHojde(double h)
{
	hojde_ = (h > 0) ? h : 10;
}

Kasse::Kasse(double lengde, double bredde, double hojde)
{
	lengde_ = lengde > 0 ? lengde: 10;
	bredde_ = bredde > 0 ? bredde: 10;
	hojde_ = hojde > 0 ?  hojde : 10;
}
double Kasse::beregnVolumen() const
{
	return (lengde_ * bredde_ * hojde_)/1000;
}

std::ostream& operator <<(std::ostream& os, const Kasse& k) 
{  
	os << "kasse med laengde " << k.getLengde() << " cm, bredde " << k.getBredde() << " cm, hoejde "<< k.getHojde()<< " cm, og volumen "<< k.beregnVolumen()<<" Liter" << std::endl;
	
	return os;
}

bool operator< (const Kasse& k1, const Kasse& k2)
{
	return k1.beregnVolumen() < k2.beregnVolumen();
}

bool operator> (const Kasse& k1, const Kasse& k2)
{
	return k1.beregnVolumen() > k2.beregnVolumen();
}