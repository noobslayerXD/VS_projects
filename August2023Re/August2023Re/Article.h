#pragma once
#include "NewsItem.h"
#include <list>

class Article: public NewsItem
{
public:
	Article(int id, std::string head_line);
	void add_item(NewsItem* item);
	std::string get_html() const override;

private:
	std::string head_line_;
	std::list<NewsItem*> items_;
};

