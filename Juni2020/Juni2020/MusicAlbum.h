#pragma once
#include "EMedia.h"
#include <string>


class MusicAlbum : public EMedia
{
public:
	MusicAlbum(const std::string &category, const std::string& title, const std::string &artist, double duration);
	std::string getAuthorOrArtist() const;
	double getDuration() const;
	double calculatePrice() const;
	void print() const;
private:
	std::string artist_;
	double duration_;
};