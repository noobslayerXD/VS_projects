#include "Periode.h"
#include <iostream>

using namespace std;

Periode::Periode(int startMaaned, int slutMaaned, double forbrug)
{
	this->startMaaned_ = startMaaned;
	this->slutMaaned_ = slutMaaned;
	this->forbrug_ = forbrug;
}

void Periode::setPeriode(int startMaaned, int slutMaaned)
{
	startMaaned_ = startMaaned >= 1 && startMaaned <= 12 ? startMaaned : 1;
	slutMaaned_ = slutMaaned >= 1 && slutMaaned <= 12 && slutMaaned >= startMaaned ? slutMaaned : startMaaned;
}

int Periode::getStartMaaned() const
{
	return startMaaned_;
}

int Periode::getSlutMaaned() const
{
	return slutMaaned_;
}

void Periode::setForbrug(double forbrug)
{
	forbrug_ = forbrug >= 0 ? forbrug : 0;
}

double Periode::getForbrug() const
{
	return forbrug_;
}

double Periode::beregnGennemsnitPerMaaned() const 
{
	return forbrug_ / (slutMaaned_ - startMaaned_);
}

void Periode::print() const
{
	cout << "Forbrug fra " << startMaaned_ << ". maaned til og med " 
		<< slutMaaned_ << ". maaned er " 
		<< forbrug_ << " m3" << endl;
}


