#pragma once
#include "NewsItem.h"

class Text : public NewsItem
{
public:
	Text(int id, std::string Text);
	std::string get_html() const override;

private:
	std::string text_;
};

