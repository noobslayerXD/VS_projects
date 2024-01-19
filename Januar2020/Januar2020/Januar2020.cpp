// Januar2020.cpp 
#include <iostream>
#include "Kasse.h"
#include <vector>
#include "Braendstof.h"
#include "Benzin.h"
#include "Optankning.h"

int main()
{
    std::cout << "milestone 1" <<std::endl;
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

    Optankning biljuice(  46, 18.4783, &Bens);
    biljuice.printBeskrivelse();






    return 0;
}
