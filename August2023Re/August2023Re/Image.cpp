#include "Image.h"
#include <iostream>

Image::Image(int id, std::string image_link, std::string caption)
	:NewsItem(id)
{
	this->image_link_ = image_link;
	this->caption_ = caption;
}
std::string Image::get_html() const
{
	std::string result;

	result = "image\n";
	result = "id:" + get_id() + '\n';
	result = "link: " + image_link_ + "\n";
	result = "Caption: " + caption_ + "\n";

	return result;
}

