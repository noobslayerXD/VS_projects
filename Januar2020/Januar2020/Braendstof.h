#pragma once

class Braendstof
{
public:
	Braendstof(double);

	virtual ~Braendstof();
	
	double getPrisPerLiter() const ;
	void setPrisPerLiter(double);
	
	virtual void printBeskrivelse() const = 0;

protected:
	double prisPerLiter_;
};
