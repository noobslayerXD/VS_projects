#pragma once
#include "person.h"

class Employee : public Person {
public:
	Employee(int id = 0, int age = 0, int step = 10);
	~Employee();

	void setStep(int step);
	int getStep() const;

	int calcSalary() const override;
	void print() const override;

private:
	int step_; // Tilladt værdi: 10-40, Default værdi: 10
};