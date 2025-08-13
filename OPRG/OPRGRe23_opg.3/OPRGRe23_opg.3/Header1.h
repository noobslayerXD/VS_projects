//del (a
#pragma once


class MineralSample{

private:
	double weight;
	double volume;

	//del (c
public:
	MineralSample(double x, double y) {
		weight = x;
		volume = y;
	}
	bool is_gold();
	bool is_silver();
};

//del (b
/*
siden vægten er en talværdi har jeg vagt at gå med double. og siden at vægten næsten aldrig er en heltals værdi, har jeg valgt double, det samme gælder for volumen
*/


