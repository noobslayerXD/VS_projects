#include "Person.h"


Person::Person(const std::string& navn, const char* personnummer, int vaccineStatus)
{
    navn_ = navn;
    strcpy_s(personnummer_, 12, personnummer);
    vaccineStatus_ = (0 <= vaccineStatus && vaccineStatus <= 2) ? vaccineStatus : 0;
}

//Person::~Person(){}

std::string Person::getNavn() const
{
    return navn_;
}

const char* Person::getPersonnummer() const
{
    return personnummer_;
}

int Person::getVaccineStatus() const
{
    return vaccineStatus_;
}

void Person::print() const
{
    std::cout << getNavn() << std::endl << getPersonnummer() << std::endl;
    if (vaccineStatus_ < 1)
    {
        std::cout << "ikke vaccineret" << std::endl;
    }
    else
    {
        std::cout << "Vaccineret " << getVaccineStatus() << " gang" << std::endl;
    }
}

Person& Person::operator++() {
    if (vaccineStatus_ < 2)
        vaccineStatus_++;
    return *this;
}
Person Person::operator++(int) {
    Person temp = *this;

    if (vaccineStatus_ < 2)
        vaccineStatus_++;
    return temp;
}
