#pragma once
#include <string>

// Denne klasse gives med som bilag
class NewsItem
{
public:
	NewsItem(int id);
	virtual ~NewsItem() = default;
	virtual std::string get_html() const = 0;
	int get_id() const;
	std::string get_id_string() const;

private:
	int id_;
};

