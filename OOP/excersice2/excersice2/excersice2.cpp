#include <iostream>
#include <vector>
using namespace std;

int main()
{
    int grade=0;
    int sum = 0;
    int g = 0 ;
    bool isvalidgrade=false;
    vector<int> grades;
    while (grade!=-99)
    {
        int validGrades[] = { -3, 0, 2, 4, 7, 10, 12 };
        cout << "enter a grade:";
        cin >> grade;
        for (auto validgrade : validGrades)
        {
            cout << validgrade;
            if (grade == validgrade)
            {
                isvalidgrade = true;
                break;
            }
        }
        if (isvalidgrade = true)
        {
            cout << "valid grade\n";
            grades.push_back(grade);
            isvalidgrade = false;
            break;
        }
        else
        {
            cout << "invalid grade";
        }
    }
    for (auto g : grades)
    {
        cout << g<< "  ";
    }
    
}
