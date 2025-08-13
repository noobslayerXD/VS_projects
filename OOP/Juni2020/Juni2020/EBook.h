#pragma once
#include <string>
#include "EMedia.h"

class EBook: public EMedia 
{
private:
	std::string author_;
	int numberOfPages_;

public:
	EBook(const std::string& category, const std::string& title, const std::string& author, int numberOfPages);
	std::string getAuthorOrArtist() const;
	int getNumberOfPages() const;
	double calculatePrice() const;
	void print() const;

};

