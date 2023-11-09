#pragma once

struct Time
{
	int hour;
	int minute;
	int second;
};

void printTime(Time t);
Time addTime(Time t1, Time t2);
