#include <iostream>
using namespace std;

struct testKarakter
{
    int karakter;
    string fag;
};

void printKarakter(testKarakter e1)
{
    cout << "I " << e1.fag << " fik du: " << e1.karakter << endl;
}

int main()
{
    
 
    testKarakter e1{};

    cout << "hvilket fag er det: ";
    cin >> e1.fag;
    cout << "Hvilken karakter: ";
    cin >> e1.karakter;
    printKarakter(e1);
    return 0;

}

