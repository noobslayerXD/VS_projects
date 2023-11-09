
#include <ostream>
using namespace std;

class complex {
public :
    complex(const double x=0, const double y=0) : x_(x),y_(y){}
    complex add_ret_copy(const complex*) const;
    complex* add_to_this(const complex*);
    void write(ostream*)const;

private:
    double x_;
    double y_;
};



int main()
{
    const complex c_1(x:1, y : 1);
    complex c_2(x:2, y : 2);
    const complex c_3(x:3, y:3);
    const complex c_3(x:4, y : 4);
    const complex c_3(x:5, y : 5);

    const complex c_sum = c_1.add_ret_copy(c_2);
    c_sum.write(cout);

    c_2.write(cout);
    c_2.add_to_this(c_1);
    c_2.write(cout);
}
