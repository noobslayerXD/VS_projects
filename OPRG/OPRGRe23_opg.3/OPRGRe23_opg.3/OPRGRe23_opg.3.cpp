//del (e
#include <iostream>
#include"Header1.h"
using namespace std;


int main()
{
    MineralSample sample1(19.3, 1);
    MineralSample sample2(105.0, 10);
    MineralSample sample3(100.0, 100);
    cout << "sample 1: er det guld:" << MineralSample::is_gold() << "er det sølv:" << MineralSample::is_silver();;
    cout << "sample 2: er det guld:" << MineralSample::is_gold() << "er det sølv:" << MineralSample::is_silver();;
    cout << "sample 3: er det guld:" << MineralSample::is_gold() << "er det sølv:" << MineralSample::is_silver();;

}
