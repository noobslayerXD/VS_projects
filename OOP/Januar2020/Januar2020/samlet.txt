#pragma once

class Braendstof
{
public:
	Braendstof(double);

	virtual ~Braendstof();

	double getPrisPerLiter() const;
	void setPrisPerLiter(double);

	virtual void printBeskrivelse() const = 0;

protected:
	double prisPerLiter_;
};

#include "Braendstof.h"

Braendstof::Braendstof(double pris)
{
	setPrisPerLiter(pris);
}

Braendstof::~Braendstof() {}

double Braendstof::getPrisPerLiter() const
{
	return prisPerLiter_;
}
void Braendstof::setPrisPerLiter(double pris)
{
	prisPerLiter_ = pris > 0 ? pris : 10;
}

#pragma once
#include "Braendstof.h"

// Denne fil skal du tilrette for at svare på opgave 2.D

class Benzin :public Braendstof
{
public:
	Benzin(double, int);
	int getOktan() const;
	void setOktan(int oktan);
	void printBeskrivelse() const override;

private:
	int oktan_;
};


#include "Benzin.h"
#include <iostream>


// I denne fil skal du indsætte koden fra opgave 2.E
Benzin::Benzin(double pris, int oktan)
	:Braendstof(pris)
{
	setOktan(oktan);
	//setPrisPerLiter(pris);
}

int Benzin::getOktan() const
{
	return oktan_;
}

void Benzin::setOktan(int oktan)
{
	oktan_ = (88 <= oktan && oktan <= 101) ? oktan : 95;
}

void Benzin::printBeskrivelse() const
{
	std::cout << "Benzin med oktantal " << oktan_ << std::endl;
	std::cout << "Pris pr. Liter: " << getPrisPerLiter() << " kr. " << std::endl;
}

#pragma once

#include "Braendstof.h"

// Denne fil skal du tilrette for at svare på Opgave 2.G

class Optankning : public Braendstof
{
public:
	void printInformation() const;
	Optankning(double liter, double meter, Braendstof* braendstofptr);

private:
	Braendstof* braendstofPtr_;
	double antalLiter_;
	double antalKilometer_;
};

#include "Optankning.h"
#include <iostream>
using namespace std;

// I denne fil skal du tilføje kode for at svare på Opgave 2.G
Optankning::Optankning(double liter, double meter, Braendstof* braendstofptr)
{
	antalLiter_ = liter <= 0 ? liter : 0;
	antalKilometer_ = meter <= 0 ? meter : 0;
	braendstofPtr_ = braendstofptr;
}


void Optankning::printInformation() const
{
	double okonomi;
	if (antalLiter_ > 0)
		okonomi = antalKilometer_ / antalLiter_;
	else
		okonomi = -1;

	cout << "Optankning paa " << antalLiter_ << " liter" << endl;
	if (braendstofPtr_ != nullptr)
		braendstofPtr_->printBeskrivelse();
	cout << "Der blev koert " << okonomi << " km/liter" << endl;
}

// Januar2020.cpp 
#include <iostream>
#include "Kasse.h"
#include <vector>
#include "Braendstof.h"
#include "Benzin.h"
#include "Optankning.h"

int main()
{
	std::cout << "milestone 1" << std::endl;
	Kasse k1(50, 25, 10);
	std::cout << k1 << std::endl;

	std::cout << "milestone 2" << std::endl;

	Kasse k2(510, 29, 1000);
	Kasse k3(5, 25, 1);
	Kasse k4(523, 215, 101);
	Kasse k5(590, 24445, 11230);

	std::vector<Kasse> katalog;
	katalog.push_back(k1);
	katalog.push_back(k2);
	katalog.push_back(k3);
	katalog.push_back(k4);
	katalog.push_back(k5);

	for (std::vector<Kasse>::iterator it = katalog.begin(); it != katalog.end(); it++)
	{
		std::cout << *it << std::endl;
	}

	std::cout << "milestone 3" << std::endl;

	Kasse maxKasse(1, 1, 1);
	maxKasse = *katalog.begin();
	for (std::vector<Kasse>::const_iterator it = katalog.begin(); it != katalog.end(); it++)
	{
		if (*it > maxKasse)
			maxKasse = *it;
	}
	std::cout << "Den stoerste kasse er:" << std::endl;
	std::cout << maxKasse << std::endl;


	std::cout << "milestone 4" << std::endl;

	//Braendstof urin(12);
	//urin.printBeskrivelse();


	std::cout << "milestone 5" << std::endl;

	Benzin Bens(12.21343, 19);
	Bens.printBeskrivelse();


	std::cout << "milestone 6" << std::endl;

	Optankning biljuice(46, 18.4783, &Bens);
	biljuice.printBeskrivelse();






	return 0;
}
