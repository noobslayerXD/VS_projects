// main.cpp
#include "Matrix2.h"
#include "Tpoint2.h"
#include "Rectangle.h"
#include "Circle.h"
#include "Drawing.h"
#include <iostream>

int main() {
    std::cout << "Opgave 1" << std::endl;

    Matrix2 m1(1, 2, 3, 4);
    Matrix2 m2(5, 6, 7, 8);

    // Udfører matrixmultiplikation
    Matrix2 result = m1 * m2;

    // Viser resultatematricen
    std::cout << "Result Matrix:" << std::endl;
    result.displayMatrix();

    std::cout << "Opgave 2" << std::endl;

    Rectangle r1(Point(4, 5), 6, 7);
    r1.print();

    Circle c1(Point(0, 0), 1);
    c1.print();

    Drawing d1(1);
    d1.add(&c1);
    d1.add(&r1);

    d1.print();

    std::cout << "Opgave 3"<<std::endl;

    TPoint<double> d(1.2, -3.9);
    std::cout << d.beregnKvadrant();
    d.print();

    TPoint<int> i(1, 3);
    std::cout<<i.beregnKvadrant();
    i.print();

    TPoint<float> f(6.8, -17);
    std::cout << f.beregnKvadrant();
    f.print();

    return 0;
}
