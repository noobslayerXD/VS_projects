// Lektion08Opgave3.cpp : This file contains the 'main' function. Program execution begins and ends there.

#include <iostream>
#include <cmath>
using namespace std;

class Vektor
{
    private:
        double x, y;
    public:
        // Constructor
        Vektor(double x_, double y_) : x(x_), y(y_) {}

        //getters
        double getX() const { return x; }
        double getY() const { return y; }
    
        // Setters
        void setX(double x_) { x = x_; }
        void setY(double y_) { y = y_; }
    
        //længde
        double length() const {return sqrt(x*x + y*y); }

        //prikprodukt
        double prikprodukt(const Vektor&anden) const{ 
            return x * anden.getX() + y * anden.getY();
        }

        //vinkel
        double vinkel(const Vektor& anden) const {
            double prik = prikprodukt(anden);
            double l1 = length();
            double l2 = anden.length();
            return prik / (l1 * l2);
        }
};


int main()
{
    Vektor v1(3,1);
    Vektor v2(9,10);
    //skriver længderne
    cout << "længden af vektor 1 er: " << v1.length() << endl;
    cout << "længden af vektor 2 er: " << v2.length() << endl;

    //skriver prikproduktet
    cout << "prikproduktet af de to vektorer er: " << v1.prikprodukt(v2) << endl;

    //skriver vinklen mellem 
    cout << "vinklen mellem de to vektorer er: " << v1.vinkel(v2) << endl;

}