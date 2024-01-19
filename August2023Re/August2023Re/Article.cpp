#include "Article.h"
#include <iostream>

Article::Article(int id, std::string head_line)
	:NewsItem(id)
{
	this->head_line_ = head_line;
}

void Article::add_item(NewsItem* item)
{
	items_.push_back(item);
}


std::string Article::get_html() const
{
	std::string result;

	result = "Article\n";
	result = "id:" + get_id_string() + '\n';
	result = "Head line: " + head_line_+ "\n";

	for (auto it = items_.begin(); it != items_.end(); it++)
	{
		result += (*it)->get_html();
	}

	return result;
}