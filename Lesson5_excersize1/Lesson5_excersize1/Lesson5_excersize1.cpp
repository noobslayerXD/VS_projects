#include <iostream>
#include "IntArray.h" 
using namespace std;

int main() {
    // Create an IntArray with an initial size of 5 and reallocation size of 5.
    IntArray dyn_array(5, 5);

    // Push some values into the array.
    for (int i = 1; i <= 10; i++) 
    {
        dyn_array.push_back(i);
    }

    // Convert the array to a string and print it.
    string array_str = dyn_array.to_string();
    cout << "Array: " << array_str << endl;

    IntArray array1(5,5);
    array1.push_back(1);
    array1.push_back(2);
    array1.push_back(3);

    IntArray array2(10,10);
    array2 = array1; // Use the assignment operator to copy array1 into array2

    // Now, array2 is a deep copy of array1, and modifying one won't affect the other
}