
#include <iostream>
#include <cmath>
using namespace std;

int main()
{
    double a, b, c,d,x;
    cout << "skriv a: ";
    cin >> a;
    cout << "skriv b: ";
    cin >> b; 
    cout << "skriv c: ";
    cin >> c;
    d = pow(b, 2) - 4 * a * c;
    cout <<" d er: " << d<<endl;
    if (d < 0)
    {
        cout << "der er ingen roots";
    }
    else if (d == 0)
    {
        cout << "der er en rod\n";
        x = -b / (2 * a);
        cout << "og den er: " << x;
    }
    else if (d > 0)
    {
        cout << "der er to roots\n";
        x = (-b + sqrt(d)) / (2 * a);
        cout << "den første rod er: " << x;
        x = (-b - sqrt(d)) / (2 * a);
        cout << "den anden rod er: " << x;

    }
}
