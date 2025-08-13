#include <vector>
#include <iostream>
#include <sstream>

class DataStorage {
private:
    std::vector<double> data;

public:
    // Constructor with the prototype: DataStorage(int size, double initValue)
    DataStorage(int size, double initValue) {
        // Initialize the vector with the specified size and initial value
        data.assign(size, initValue);
    }

    // Function to insert a double value into the vector
    DataStorage& insert(double value) {
        data.push_back(value);
        return *this;
    }

    // Function to get the number of elements in the vector
    int numberOfElements() const {
        return data.size();
    }

    // Function to calculate the mean value of the elements
    double meanValue() const {
        if (data.empty()) {
            // Handle the case where the vector is empty
            return 0.0; // You can modify this return value as needed
        }

        double sum = 0.0;
        for (double value : data) {
            sum += value;
        }

        return sum / static_cast<double>(data.size());
    }

    // Function to convert the data to a string
    std::string to_string() const {
        if (data.empty()) {
            return "DataStorage is empty.";
        }

        std::stringstream ss;
        ss << "DataStorage [ ";
        for (double value : data) {
            ss << value << " ";
        }
        ss << "]";
        return ss.str();
    }


        // Overload the << operator for DataStorage
    friend std::ostream& operator<<(std::ostream& os, const DataStorage& ds) {
        if (ds.data.empty()) {
            os << "DataStorage is empty.";
            return os;
        }

        // Iterate through the vector in reverse order using iterators
        for (auto it = ds.data.rbegin(); it != ds.data.rend(); ++it) {
            os << *it << "\n";
        }

        return os;
    }
};


int main()
{
    // Test the constructor with size 3 and initial value 1.5
    DataStorage ds(3, 1.5);

    // Test insert method with cascading calls
    ds.insert(2.0).insert(3.5).insert(4.2);

    // Test output operator<<
    std::cout << "DataStorage contents:\n" << ds << "\n";

    // Test numberOfElements method
    std::cout << "Number of elements: " << ds.numberOfElements() << "\n";

    // Test meanValue method
    std::cout << "Mean value: " << ds.meanValue() << "\n";

    return 0;
}