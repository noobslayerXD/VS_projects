// Juni2020.cpp : This file contains the 'main' function. Program execution begins and ends there.
#include <iostream>
#include "EBook.h"
#include "MusicAlbum.h"
#include "EMediaShop.h"

int main()
{
    EBook bog1("uhyggeligheder", "monsteret under sengen", "Mig",350);
    bog1.print();
    MusicAlbum fav("hiphop", "College Dropout", "ye", 1);
    fav.print();

    EMediaShop musikhuset("musikhuset");
    musikhuset.addEMedia(fav);
    musikhuset.addEMedia(bog1);
    musikhuset.print();


    musikhuset += bog1;
    musikhuset.print();
}
