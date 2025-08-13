#pragma once
#include "Person.h"

class Sundhedspersonale : public Person {
	private:
		int risikogruppe_;
	public:
		void setRisikogruppe(int);
		int getRisikogruppe();
		void print();

};

