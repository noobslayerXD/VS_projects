#include <iostream>
using namespace std;

void writeArray(const int* const a, const size_t& size)
{
    
    for (size_t i = 0; i < size; ++i) 
    {
        cout << a[i] << " ";
    }
    cout << "\nSize of array: " << size<<endl;
}
inline void swap(int* a, int* b)
{
    
    int temp = *a;
    *a = *b;
    *b = temp;
}
void increment(int* const a, const int& incr, const size_t& size)
{
    for (size_t i = 0; i < size; i++)
    {
        a[i] += incr;
        cout << a[i] << " ";
    }
}
inline void swapref(int& a, int& b)
{

    int temp = a;
    a = b;
    b = temp;
}
int main()
{
    //mit cute array
    int MitArray[] = { 9,9,9,9,6,9,69,420 };
    //størrelsen af MitArray
    size_t ArraySize = sizeof(MitArray) / sizeof(MitArray[0]);
    //kalder funktionen
    writeArray(MitArray, ArraySize);


    int x = 2;
    int y = 4;
    cout << "Before swap: x = " << x << ", y = " << y << endl;
    
    swap(&x,&y);

    cout << "After swap: x = " << x << ", y = " << y << endl;
 
    //alt bliver større med bigger
    int bigger = 2;
    increment(MitArray,bigger, ArraySize);

    cout << "\nBefore swap: x = " << x << ", y = " << y << endl;

    swapref(x, y);

    cout << "After swap: x = " << x << ", y = " << y << endl;
}
