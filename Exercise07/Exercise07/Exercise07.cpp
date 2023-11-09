#include <iostream>
#include <vector>
#include <stdexcept>

class Matrix {
private:
    int rows;
    int cols;
    std::vector<std::vector<double>> data;

public:
    Matrix(int rows, int cols) : rows(rows), cols(cols), data(rows, std::vector<double>(cols, 0.0)) {}

    // To string method
    std::string toString() const {
        std::string result;
        for (int i = 0; i < rows; ++i) {
            for (int j = 0; j < cols; ++j) {
                result += std::to_string(data[i][j]);
                if (j < cols - 1)
                    result += "\t";
            }
            result += "\n";
        }
        return result;
    }

    // Overload the + operator as a member function
    Matrix operator+(const Matrix& other) const {
        if (rows != other.rows || cols != other.cols) {
            throw std::runtime_error("Matrix dimensions do not match for addition");
        }
        Matrix result(rows, cols);
        for (int i = 0; i < rows; ++i) {
            for (int j = 0; j < cols; ++j) {
                result.data[i][j] = data[i][j] + other.data[i][j];
            }
        }
        return result;
    }

    // Overload multiplication by a scalar double as a member function
    Matrix operator*(double scalar) const {
        Matrix result(rows, cols);
        for (int i = 0; i < rows; ++i) {
            for (int j = 0; j < cols; ++j) {
                result.data[i][j] = data[i][j] * scalar;
            }
        }
        return result;
    }

    // Overload the * operator for matrix multiplication as a member function
    Matrix operator*(const Matrix& other) const {
        if (cols != other.rows) {
            throw std::runtime_error("Matrix dimensions do not allow multiplication");
        }
        Matrix result(rows, other.cols);
        for (int i = 0; i < rows; ++i) {
            for (int j = 0; j < other.cols; ++j) {
                for (int k = 0; k < cols; ++k) {
                    result.data[i][j] += data[i][k] * other.data[k][j];
                }
            }
        }
        return result;
    }

    // Overload the == operator as a member function
    bool operator==(const Matrix& other) const {
        if (rows != other.rows || cols != other.cols) {
            return false;
        }
        for (int i = 0; i < rows; ++i) {
            for (int j = 0; j < cols; ++j) {
                if (data[i][j] != other.data[i][j]) {
                    return false;
                }
            }
        }
        return true;
    }
};

// Test function
void testMatrixOperations() {
    Matrix mat1(2, 3);
    Matrix mat2(2, 3);

    // Initialize mat1 and mat2 with some values
    for (int i = 0; i < mat1.rows; ++i) {
        for (int j = 0; j < mat1.cols; ++j) {
            mat1.data[i][j] = i + j;
            mat2.data[i][j] = i - j;
        }
    }

    // Test the to string method
    std::cout << "Matrix 1:\n" << mat1.toString() << std::endl;
    std::cout << "Matrix 2:\n" << mat2.toString() << std::endl;

    // Test matrix addition
    Matrix sum = mat1 + mat2;
    std::cout << "Matrix 1 + Matrix 2:\n" << sum.toString() << std::endl;

    // Test scalar multiplication
    Matrix scaled = mat1 * 2.0;
    std::cout << "Matrix 1 * 2.0:\n" << scaled.toString() << std::endl;

    // Test matrix multiplication
    Matrix mat3(3, 2);
    for (int i = 0; i < mat3.rows; ++i) {
        for (int j = 0; j < mat3.cols; ++j) {
            mat3.data[i][j] = i * j;
        }
    }
    Matrix product = mat1 * mat3;
    std::cout << "Matrix 1 * Matrix 3:\n" << product.toString() << std::endl;

    // Test equality operator
    std::cout << "Matrix 1 == Matrix 2: " << (mat1 == mat2) << std::endl;
    std::cout << "Matrix 1 == Matrix 1: " << (mat1 == mat1) << std::endl;
}

int main() {
    testMatrixOperations();
    return 0;
}
