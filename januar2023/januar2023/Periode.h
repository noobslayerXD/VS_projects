#pragma once
#include <algorithm>
#include <iostream>
class Periode
{
public:
	Periode(int startmåned = 1, int slutmaaned = 1, double forbrug = 0.0);

	void setPeriode(int, int);
	void setForbrug(double);

	int getStartMaaned() const;
	int getSlutMaaned() const;
	double getForbrug() const;

	void print() const;
	double beregnGennemsnitPerMaaned() const ;

	int min(int a, int b)
	{
		if (a >= b)
		{
			return b;
		}
		else
			return a;
	}

	int max(int a, int b)
	{
		if (a <= b)
		{
			return b;
		}
		else
			return a;
	}

	Periode operator+ (const Periode& p2)
	{
		return Periode(min(startMaaned_,p2.startMaaned_), max(slutMaaned_,p2.slutMaaned_), forbrug_+p2.forbrug_);
	}
private:
	int startMaaned_;
	int slutMaaned_;
	double forbrug_;
};