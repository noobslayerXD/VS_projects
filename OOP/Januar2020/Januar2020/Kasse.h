#pragma once
#include <iostream>

class Kasse 
{
private:
	double lengde_;
	double bredde_;
	double hojde_;
public:
	Kasse(double lengde, double bredde, double hojde);
	double getLengde() const;
	double getBredde() const;
	double getHojde() const;
	void setLengde(double);
	void setBredde(double);
	void setHojde(double);
	double beregnVolumen() const;

	friend std::ostream& operator<< (std::ostream&, const Kasse&);
	friend bool operator< (const Kasse&, const Kasse&);
	friend bool operator> (const Kasse&, const Kasse&);

};