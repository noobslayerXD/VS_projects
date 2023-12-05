#pragma once
#include "employee.h"

class Boss : public Employee {
public:
	Boss(int id = 0, int age = 0, int bonus = 0);
	~Boss();

	void setBonus(int bonus);
	int getBonus() const;

	int calcSalary() const override;
	void print() const override;

private:
	int bonus_; // Tilladt værdi: 1000-20000, Default værdi: 0
};
