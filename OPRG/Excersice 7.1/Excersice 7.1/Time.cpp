#include "Time.hpp"
#include "Time.hpp"
#include <iostream>
using namespace std;

void printTime(Time t)
{
	cout << t.hour << ":" << t.minute << ":" << t.second << endl;
}

Time addTime(Time t1, Time t2) {
	Time sum;
	sum.hour = t1.hour + t2.hour;
	sum.minute = t1.minute + t2.minute;
	sum.second = t1.second + t2.second;

	if (sum.second >= 60.0) {
		sum.second -= 60.0;
		sum.minute += 1;
	}

	if (sum.minute >= 60) {
		sum.minute -= 60;
		sum.hour += 1;
	}

	return sum;
}
