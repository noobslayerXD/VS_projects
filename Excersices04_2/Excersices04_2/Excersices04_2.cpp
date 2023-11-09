#include <limits>
#include <iostream>
#include <stdexcept>
using namespace std;


double calculate(double first, char op, double second) {
    /*if (first < 0 || second < 0) {
        // Throw an exception for non-positive input values.
        throw invalid_argument("Input values must be positive.");
    }
    */
    double result;

    switch (op) {
    case '+':
        result = first + second;
        break;
    case '-':
        result = first - second;
        break;
    case '*':
        result = first * second;
        break;
    case '/':
        if (second == 0) {
            // Throw an exception for division by zero.
            throw invalid_argument("Division by zero is not allowed.");
        }
        result = first / second;
        break;
    default:
        // Throw an exception for an unknown operator.
        throw invalid_argument("Unknown operator.");
    }

    return result;
}

int main()
{
    double firstDouble, secondDouble;
    char op;

    // Prompt the user for input.
    cout << "Enter a double, an operator (+, -, *, /), and another double: ";

    // Use cin to read the user's input.
    try {
        cin >> firstDouble >> op >> secondDouble;

        // Check if the input was successful.
        if (cin.fail()) {
            throw invalid_argument("Invalid input. Please enter a valid format.");
        }

        double result = calculate(firstDouble, op, secondDouble);
        cout << "The result is: " << result << endl;
    }
    catch (const std::exception& e) {
        cout << "Error: " << e.what() << endl;
        return 1; // Exit with an error code.
    }

    return 0; // Exit successfully.
}
