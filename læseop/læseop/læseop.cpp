
#include <iostream>
using namespace std;

int main()
{
    for (int i = 0; i < 100; i ++)
    {
        while (i % 2)
        {
            cout << i << "  " << sqrt(i)<<"\n";
            i++;
        }
       
    }
}
