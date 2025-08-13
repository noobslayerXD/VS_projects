#include <iostream>
using namespace std;

class IceCream 
{
private :
    double volume, price;
    
public:   
    string name;
    void setVolume() 
    {
        cout << "hvad er volumen: ";
        cin >> volume;
        if (volume < 0)
        {
            cout << "volume skal være positiv: ";
            cin >> volume;
        }
    }
    void setPrice()
    {
        cout << "hvad er prisen: ";
        cin >> price;
        if (price < 0)
        {
            cout << "prisen skal være positiv: ";
            cin >> price;
        }
    }
    double getPricePrVolume()
    {
        double x = price / volume;
        return x;
    }
    void toString()
    {
        cout << "prisen pr. volumen er: " << getPricePrVolume() << endl;
    }
};



int main()
{
    IceCream ice;
    ice.setVolume();
    ice.setPrice();
    ice.toString();
    cin >> ice.name;
    return 0;
}

