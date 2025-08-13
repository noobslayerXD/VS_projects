#pragma once
#include <iostream>
#include "Person.h"

class Employee : public Person {
public:
    Employee(int id = 0, int age = 0, int step = 10) : Person(id, age), step_(step) {}
    void setStep(const int step) { step_ = step; }
    int getStep() const { return step_; }
    int calcSalary() const { return step_ * 1000; }
    void print() const {
        std::cout << "The employees age is: " << getAge() << std::endl;
        std::cout << "The employees ID is: " << getId() << std::endl;
        std::cout << "The employees step is: " << getStep() << std::endl;
        std::cout << "The employees salary is: " << calcSalary() << std::endl;
    }

protected:
    int step_;
};