#include <iostream>
using namespace std;

int main()
{
    //del (a
    char gender;
    cout << "Hvilket køn: ";
    cin >> gender;
  
    if (gender!=('f'&&'m'))
    {
        cout << "der blev skrevet noget forkert, kønnet er sat til hunkøn\n";
        gender = 'f';
    }
    

    //del (b
    double weight;
    double height;
    double age;


    cout<< "indtast venligst vægt,højde og alder\n";
    cout<< "vægt(kilogram): ";
    cin>>weight;
    cout << "\n højde(centimeter): ";
    cin >> height;
    cout << "\n alder(aar): ";
    cin >> age ;

    //del (c
    double BMR;
    if (gender == 'f')
    {
        BMR = 88.362 + 13.397 * weight + 4.799 * height - 5.677 * age;
    }
    else if (gender == 'm')
    {
        BMR = 447.593 + 9.247 * weight + 3.098 * height - 4.330 * age;
    }
    cout << "Din BMR er: " << BMR;
}
