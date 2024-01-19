// Matrix2.cpp
#include "Matrix2.h"
#include <iostream>

// Implementering af constructor
Matrix2::Matrix2(double k11, double k12, double k21, double k22)
    : k11(k11), k12(k12), k21(k21), k22(k22) {}

// Implementering af displayMatrix-metoden
void Matrix2::displayMatrix() 
{
    std::cout << "[" << k11 << ", " << k12 << "]" << std::endl;
    std::cout << "[" << k21 << ", " << k22 << "]" << std::endl;
}

Matrix2 Matrix2::operator*(const Matrix2& other) const 
{
    Matrix2 result;

    result.k11 = (k11 * other.k11) + (k12 * other.k21);
    result.k12 = (k11 * other.k12) + (k12 * other.k22);
    result.k21 = (k21 * other.k11) + (k22 * other.k21);
    result.k22 = (k21 * other.k12) + (k22 * other.k22);

    return result;
}