// Januar2022.cpp : This file contains the 'main' function. Program execution begins and ends there.

#include <iostream>
#include "Afsnit.h"
#include "Tur.h"
#include "Sodavand.h"
#include "Oel.h"
#include "Drikkevarer.h"
#include <list>

int main()
{
    Afsnit a(9,12);
    Afsnit me(1, 2);

    double x, y;

    a.GetXY(x, y);

    std::cout << x << " og " << y << std::endl;

    me.GetXY(x, y);

    std::cout << x << " og " << y << std::endl;

    Afsnit saml;
    saml = a + me;

    saml.GetXY(x, y);

    std::cout << x << " og " << y << std::endl;


    Afsnit a1(1500, 200), a2(800, -350.5); 
    Afsnit atotal; atotal = a1 + a2;  
    std::cout << atotal << std::endl;

    Tur tur; 
    tur.tilfoejAfsnit(a1); 
    tur.tilfoejAfsnit(a2);
    Afsnit totaltur = tur.beregnFugleflugslinje();
    std::cout << totaltur << std::endl;


    std::cout << "opgave 2" << std::endl;

    Sodavand squash(33, "himlen");

    squash.print();

    Oel Green(1000, 5.4, "Green");

    Green.print();

    std::list<Drikkevarer*> bar;

    bar.push_back(&squash);
    bar.push_back(&Green);

    for ( auto it = bar.begin(); it != bar.end(); it++)
    {
        (*it)->print();
    }

    return 0;
}
