#pragma once
#include <iostream>
#include "Employee.h"

class Boss : public Employee {
public:
    Boss(int id = 0, int age = 0, int bonus = 0) : Employee(id, age, 40), bonus_(bonus) {}
    void setBonus(int bonus) { bonus_ = bonus; }
    int getBonus() const { return bonus_; }
    int calcSalary() const{ return 40000 + bonus_; } // Provide implementation
    void print() const {
        std::cout << "The Boss's age is: " << getAge() << std::endl;
        std::cout << "The Boss's ID is: " << getId() << std::endl;
        std::cout << "The Boss's step is: " << getStep() << std::endl;
        std::cout << "The Boss's salary is: " << calcSalary() << std::endl;
        std::cout << "The Boss's bonus is: " << getBonus() << std::endl;
    }

private:
    int bonus_;
};