#include "Person.h"
#include <iostream>

class person {
private:
    int id_;
    int age_;
public:
    void setId(const int id) { id_ = id; }
    int getId() const { return age_; }
    void setAge(const int age) { age_ = age; }
    int getAge()const const { return age_; }
    int calcSalary() {

    }
    void print() {
        std::cout << "The id is: " << getId() << std::endl;
        std::cout << "The age is: " << getAge() << std::endl;
    }
};