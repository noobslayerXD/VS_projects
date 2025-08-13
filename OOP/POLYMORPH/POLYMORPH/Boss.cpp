#include "boss.h"
#include <iostream>

Boss::Boss(int id, int age, int bonus) : Employee(id, age, 40) {
	setBonus(bonus);
}

Boss::~Boss() {}

void Boss::setBonus(int bonus) {
	if (bonus >= 1000 && bonus <= 20000) {
		bonus_ = bonus;
	}
	else {
		std::cerr << "Ugyldig bonus-værdi. Skal være mellem 1000 og 20000." << std::endl;
	}
}

int Boss::getBonus() const {
	return bonus_;
}

int Boss::calcSalary() const {
	return Employee::calcSalary() + bonus_;
}

void Boss::print() const {
	Employee::print();
	std::cout << ", Bonus: " << bonus_ << " kr." << std::endl;
}