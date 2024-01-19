#pragma once
#include <list>
#include <string>
#include "EMedia.h"

class EMediaShop
{
private:
	char* namePtr_;
	std::list<const EMedia*> mediaList;

public:
	EMediaShop(const char* name);
	~EMediaShop();

	void addEMedia(const EMedia &addMe);
	void SearchTitle(const std::string &name)const;
	void searchAuthorOrArtist(const std::string &name);
	void print() const;
	void operator+=(const EMedia& add);
};

