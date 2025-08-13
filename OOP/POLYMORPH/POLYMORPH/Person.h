#pragma once

class Person {
public:
	Person(int id = 0, int age = 0);
	virtual ~Person();

	void setId(int id);
	int getId() const;

	void setAge(int age);
	int getAge() const;

	virtual int calcSalary() const;
	virtual void print() const;

private:
	int id_;
	int age_;
};