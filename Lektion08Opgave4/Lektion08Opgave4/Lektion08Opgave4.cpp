// Lektion08Opgave4.cpp : This file contains the 'main' function. Program execution begins and ends there.
#include<cmath>
#include <iostream>
using namespace std;

class Beholder {
private:
    double tryk, volumen, temperatur;
    int molekyler;
    const double R = 0.0831;
public:
    //getters
    double getTryk() const { return tryk; }
    double getVolumen() const { return volumen; }
    double getTemperatur() const { return temperatur; }
    int getMolekyler() const { return molekyler; }

    //setters
    void setTryk(double tryk_) { tryk = tryk_; }
    void setVolumen(double volumen_) { volumen = volumen_; }
    void setTemperatur(double temperatur_) { temperatur = temperatur_; }
    void setMolekyler(int molekyler_) { molekyler = molekyler_; }

    //tryk og vol beregning
    double setTrykVedFastVolumen() const { return (molekyler * R * temperatur) / volumen; }
    double setVolumenVedFastTryk() const { return (molekyler * R * temperatur) / tryk; }

};

int main()
{
    Beholder b1;
    b1.setTryk(1);
    b1.setTemperatur(100);
    b1.setMolekyler(100000);
    cout << b1.setVolumenVedFastTryk()<<endl;

    Beholder b2;
    b2.setMolekyler(100000);
    b2.setTemperatur(10000);
    b2.setVolumen(12341);
    cout << b2.setTrykVedFastVolumen();
}