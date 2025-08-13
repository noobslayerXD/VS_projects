#pragma once
#include <iostream>

template <class T> class TPoint
{
public:
    TPoint(T x, T y);

    void print() const;

    int beregnKvadrant() const;
private:
    T x;
    T y;
};

template <typename T>TPoint<T>::TPoint(T x, T y)
{
    this->x = x;
    this->y = y;
}

template <typename T>void TPoint<T>::print() const
{
    std::cout << "(" << x << ", " << y << ")"<<std::endl;
}

template <typename T>int TPoint<T>::beregnKvadrant() const
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
