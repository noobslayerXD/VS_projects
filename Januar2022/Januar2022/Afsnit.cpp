#include "Afsnit.h"

Afsnit::Afsnit(double x, double y)
{
	setX(x);
	setY(y);
}

void Afsnit::setX(double x)
{
	x_ = (x >= -200000 && x <= 200000) ? x : 0.0;
}

void Afsnit::setY(double y)
{
	y_ = (y >= -200000 && y <= 200000) ? y : 0.0;
}

double Afsnit::getX() const
{
	return x_;
}

double Afsnit::getY() const
{
	return y_;
}

void Afsnit::GetXY(double& x, double& y) const
{
	x = x_;
	y = y_;
}

Afsnit operator+(const Afsnit& a, const Afsnit& b)
{
	return Afsnit (a.x_+b.x_,a.y_+b.y_);
}

std::ostream& operator <<(std::ostream& os, const Afsnit& k)
{
	os << "( " << k.x_ << ",  " << k.y_ << " ) " << std::endl;

	return os;
}