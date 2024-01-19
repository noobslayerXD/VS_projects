#include <iostream>
#include "Kapacitor.h"
#include "Article.h"
#include "IdGenerator.h"
#include "Image.h"
#include "Text.h"
/*
int main()
{
    std::cout << "Opgave 1" << std::endl;

    Kapacitor k1(100e-6);
    Kapacitor k2(200e-6);
    Kapacitor parralel = k1 | k2;
    Kapacitor seriel = k1 & k2;

    std::cout << parralel << " og " << seriel<<std::endl;

    std::cout << "Opgave 2" << std::endl;

    
    int id = IdGenerator::new_id();
    Image im1(id, "link", "caption");
    
    IdGenerator g;
    Text t1(g.new_id(), "Article text");

    Article a1(IdGenerator::new_id(), "Head line");


    a1.add_item(&t1); 
    a1.add_item(&im1);

    std::cout << a1.get_html() << std::endl;



    return 0;
}
*/