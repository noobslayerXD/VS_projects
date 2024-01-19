#pragma once
class Matrix2
{
private:
	double k11, k12, k21, k22;
public:
	
	//default constructor
	Matrix2(double k11 = 1, double k12 = 0, double k21 = 0, double k22 = 1);

	//display
	void displayMatrix();
		
	// Operatoroverbelastning for matrixmultiplikation
	Matrix2 operator*(const Matrix2& other) const;

};

