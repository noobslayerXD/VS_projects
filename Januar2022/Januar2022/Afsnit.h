#pragma once
#include <ostream>

class Afsnit 
{
private:
	double x_;
	double y_;

public:
	Afsnit(double x = 0.0, double y = 0.0);

	void setX(double);
	void setY(double);
	double getX() const;
	double getY() const;
	void GetXY(double&, double&) const;

	friend Afsnit operator+(const Afsnit& a, const Afsnit& b);
	friend std::ostream& operator<< (std::ostream&, const Afsnit&);
};