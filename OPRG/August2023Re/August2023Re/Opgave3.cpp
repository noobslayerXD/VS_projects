#include "Box.h"
#include "Resistor.h"

int main()
{
	Box b1(10);
	Resistor r1;
	Resistor r2(4.5);

	b1.addResistor(r1);
	b1.addResistor(r2);
	b1.addResistor(Resistor(47.5));

	b1.print();

	return 0;
}
