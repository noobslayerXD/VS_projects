#include "EBook.h"
#include <iostream>

EBook::EBook(const std::string& category, const std::string& title, const std::string& author, int numberOfPages)
	:EMedia(category,title)
{
	if (numberOfPages < 0)
	{
		numberOfPages_ = 0;
	}
	else if (numberOfPages > 500)
	{
		numberOfPages_ = 500;
	}
	else
		numberOfPages_ = numberOfPages;
	author_ = author;
}

std::string EBook::getAuthorOrArtist() const
{
	return author_;
}

int EBook::getNumberOfPages() const
{
	return numberOfPages_;
}
double EBook::calculatePrice() const
{
	return numberOfPages_ * 0.5;
}
void EBook::print() const
{
	EMedia::print();
	std::cout << "Forfatter: \t" << author_ << std::endl;
	std::cout << numberOfPages_ << " sider" << std::endl;
	std::cout << "kr. " << calculatePrice() << std::endl<< std::endl;
}
