#pragma once
#include "Time.h"
#include "../../../../Downloads/Bilag/Time.h"
#include <iostream>

int convertBack(int secondOne)
{
	struct notTime {
		int seconds;
		int minutes;
		int hours;
	};
	notTime t3;
	t3.minutes = secondOne / 60;
	t3.seconds = secondOne % 60;

	t3.hours = t3.minutes / 60;
	t3.minutes %= 60;

	cout << t3.hours << ":" << t3.minutes << ":" << t3.seconds << endl;
	return t3;
}