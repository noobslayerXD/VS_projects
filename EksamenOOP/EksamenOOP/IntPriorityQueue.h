#pragma once
#include <list>

class IntPriorityQueue
{
public:
	void push(const int value)
	{
		queue_.push_front(value);
		queue_.sort();
	}

	void pop()
	{
		queue_.pop_back();
	}

	int peek() const
	{
		return queue_.back();
	}

private:
	std::list<int> queue_;
};
