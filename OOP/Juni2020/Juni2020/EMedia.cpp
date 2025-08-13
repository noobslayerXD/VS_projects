#include "EMedia.h"
#include <iostream>


EMedia::EMedia(const std::string &catagory, const std::string &title)
{
	catagory_ = catagory;
	title_ = title;
}
std::string EMedia::getCatagory() const
{
	return catagory_;
}
std::string EMedia::getTitle() const
{
	return title_;
}

void EMedia::print() const
{
	std::cout << "Genre: \t" << catagory_ << std::endl;
	std::cout << "title: \t" << title_ << std::endl;
}
EMedia::~EMedia(){}