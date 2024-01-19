#pragma once
#include <string>
class EMedia
{
private:
	std::string catagory_;
	std::string title_;
public:
	EMedia(const std::string& catagory, const std::string& title);
	std::string getCatagory() const;
	std::string getTitle() const;	
	virtual std::string getAuthorOrArtist() const=0;
	virtual double calculatePrice() const=0;
	virtual void print() const;
	virtual ~EMedia();

};

