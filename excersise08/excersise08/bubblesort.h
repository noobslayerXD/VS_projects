#pragma once

#include <vector>

template <typename T>
void bubbleSort(std::vector<T>& data) {
    for (size_t i = 0; i < data.size(); i++) {
        for (size_t j = data.size() - 1; j > i; --j) {
            if (data[j - 1] > data[j]) { 
                T temp = data[j - 1];
                data[j - 1] = data[j];
                data[j] = temp;
            }
        }
    }
}
