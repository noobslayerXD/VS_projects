#pragma once
#include "NewsItem.h"

class Image :public NewsItem
{
public:
	Image(int id, std::string image_link, std::string caption);
	std::string get_html() const override;

private:
	std::string image_link_;
	std::string caption_;
};

