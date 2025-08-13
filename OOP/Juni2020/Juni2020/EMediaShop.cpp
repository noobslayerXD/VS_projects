#include "EMediaShop.h"
#include <list>
#include <iostream>
#include <iterator>

EMediaShop::EMediaShop(const char* name)
{
	int length = strlen(name) + 1;
	namePtr_ = new char[length];
	strcpy_s(namePtr_, length, name);

}
EMediaShop::~EMediaShop()
{
	delete[] namePtr_;
}

void EMediaShop::addEMedia(const EMedia& addMe)
{
	mediaList.push_back(&addMe);
}

void EMediaShop::searchAuthorOrArtist(const std::string& name)
{
	std::list<const EMedia*>::const_iterator it;
	bool found = false;
	
	for (it =mediaList.begin();it!=mediaList.end();it++)
	{
		if ((*it)->getAuthorOrArtist() == name)
		{
			system("cls");
			(*it)->print();    
			found = true;
		}
	}
	if (found == false) 
	{
		std::cout << "Der blev ikke fundet en bog eller album med den ";
		std::cout << "ønskede forfatter eller kunstner" << std::endl << std::endl; 
	}
		
}
void EMediaShop::print() const
{
	std::list<const EMedia*>::const_iterator iter;

	std::cout << namePtr_ << std::endl << std::endl;
	
	for (iter = mediaList.begin(); iter != mediaList.end(); iter++)
	{
		(*iter)->print();
	}

	
}
void EMediaShop::operator+=(const EMedia &add)
{
	mediaList.push_back(&add)
}