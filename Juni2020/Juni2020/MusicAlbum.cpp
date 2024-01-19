#include "MusicAlbum.h"
#include <iostream>

using namespace std;
MusicAlbum::MusicAlbum(const std::string& category, const std::string& title, const std::string& artist, double duration)
	:EMedia(category,title)
{
	duration_ = duration > 0 ? duration : 0;
	duration_ = duration > 1.5 ? duration : 1.5;
	artist_ = artist;

	
}

std::string MusicAlbum::getAuthorOrArtist() const
{
	return artist_;
}

double MusicAlbum::getDuration() const
{
	return duration_;
}

double MusicAlbum::calculatePrice() const
{
	return duration_*100.0;
}

void MusicAlbum::print() const
{
	int timer = (int)duration_;
	int minutter = ((int)(duration_ * 60)) % 60;

	EMedia::print();
	cout << "Kunstner:   " << artist_ << endl;
	cout << timer << " t " << minutter << " m" << endl;
	cout << "kr. " << calculatePrice() << endl << endl;;
}