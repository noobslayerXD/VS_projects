#include <iostream>
#include <ctime>
using namespace std;

int terning()
{
    srand(time(0));
    int x = rand() % 6 + 1;
    return x;
}

int main()
{
    terning();
    cout << terning() << endl;
}

