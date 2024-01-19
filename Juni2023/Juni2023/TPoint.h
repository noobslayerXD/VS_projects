#pragma once
#include <iostream>

class TPoint
{
public:
    TPoint(double x, double y);

    void print() const;

    int beregnKvadrant() const;
private:
    double x;
    double y;
};

TPoint::TPoint(double x, double y)
{
    this->x = x;
    this->y = y;
}

void TPoint::print() const
{
    std::cout << "(" << x << ", " << y << ")";
}

int TPoint::beregnKvadrant() const
{
    if (x >= 0 && y >= 0)
        return 1;
    else if (x < 0 && y >= 0)
        return 2;
    else if (x < 0 && y < 0)
        return 3;
    else
        return 4;
}
