#include "NewsItem.h"
using namespace std;

// Denne kode blev givet med som bilag

// get_html() skal ikke implementeres (den må godt, men det giver ikke mening i dette tilfælde)
NewsItem::NewsItem(int id)
{
	this->id_ = id;
}

int NewsItem::get_id() const
{
	return id_;
}

std::string NewsItem::get_id_string() const
{
	return to_string(id_);
}
