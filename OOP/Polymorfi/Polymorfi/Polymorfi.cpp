#include "Person.h"
#include "Employee.h"
#include "Boss.h"

int main()
{
	
	Person mig(69,20);
	mig.print();

	Employee dig(6969, 87, 36);
	dig.print();

	Boss alle(1000, 15, 20000);
	alle.print();
	 
	return 0;
}