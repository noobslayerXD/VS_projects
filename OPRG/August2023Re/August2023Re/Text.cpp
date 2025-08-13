#include "Text.h"
#include <iostream>

Text::Text(int id, std::string text)
	:NewsItem(id)
{
	this->text_ = text;
}
std::string Text::get_html() const 
{
	std::string result;

	result = "Text\n";
	result = "id:" + get_id() + '\n';
	result = "text: " + text_ + "\n";

	return result;
}