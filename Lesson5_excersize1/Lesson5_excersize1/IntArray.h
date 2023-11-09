#pragma once
#include <string>
using namespace std;

class IntArray {
private:
    int* array_;          // Pointer to the dynamic array
    size_t size_;         // Size of the dynamic array
    size_t current_size_; // Current number of elements in the array
    size_t re_alloc_size_;// The amount by which the array size increases when it needs to be reallocated 

public:
   
    // Constructor: Initializes the array with the given initial_size and re_alloc_size_
    IntArray(int initial_size, int re_alloc_size_)
        : size_(initial_size),
        current_size_(0),
        re_alloc_size_(re_alloc_size_) {
        array_ = new int[size_];
    }
    

    // Copy Constructor: Creates a deep copy of another IntArray object
    IntArray(const IntArray& other)
        : size_(other.size_),
        current_size_(other.current_size_),
        re_alloc_size_(other.re_alloc_size_) {
        array_ = new int[size_];
        for (int i = 0; i < current_size_; i++) {
            array_[i] = other.array_[i];
        }
    }

    // Destructor: Deallocates the dynamic array
    ~IntArray() {
        delete[] array_;
    }

    // Add an integer value to the end of the array
    void push_back(int value)
    {
        if (current_size_ == size_)
        {
            // The array is full, so we need to reallocate more space.
            int* new_array = new int[size_ + re_alloc_size_];
            for (int i = 0; i < size_; i++)
            {
                new_array[i] = array_[i];
            }
            delete[] array_;
            array_ = new_array;
            size_ += re_alloc_size_;
        }
        array_[current_size_] = value;
        current_size_++;
    }

    // Convert the array to a string for printing
    string to_string() const
    {
        string result = "[";
        for (int i = 0; i < current_size_; i++)
        {
            result += std::to_string(array_[i]);
            if (i < current_size_ - 1)
            {
                result += ", ";
            }
        }
        result += "]";
        return result;
    }

    // Assignment Operator: Performs a deep copy of another IntArray object
    IntArray& operator=(const IntArray& other) {
        if (this == &other) {
            // Self-assignment, no action needed
            return *this;
        }

        // Deallocate the current dynamic array
        delete[] array_;

        // Copy the size and re_alloc_size_ from the other object
        size_ = other.size_;
        re_alloc_size_ = other.re_alloc_size_;

        // Allocate a new dynamic array and copy the elements
        array_ = new int[size_];
        for (int i = 0; i < other.current_size_; i++) {
            array_[i] = other.array_[i];
        }

        // Update the current size
        current_size_ = other.current_size_;

        return *this;
    }

};
