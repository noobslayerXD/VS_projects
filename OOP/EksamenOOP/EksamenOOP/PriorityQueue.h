#pragma once
#include <list>

template <class T> class PriorityQueue
{
public:
	void push(const T value)
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
