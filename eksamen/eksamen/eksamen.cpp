#include <iostream>
#include "Person.h"

int main()
{
	Person p("Hanne Ibsen", "222222-2222", 0);
	p.print();
	p.operator++();
	p.print();
	p++;
	p.print();
}
