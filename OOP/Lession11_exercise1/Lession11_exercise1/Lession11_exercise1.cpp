#include <iostream>

class Shape
{
private:
    std::string color_;
public:
    Shape(const std::string& color):color_(color){}

    void printColor()
    {
        std::cout <<"The color is: " << color_<< std::endl;
    }

};

class Circle
{
private:
    float radius_;
    Shape shape_;
public:
    Circle(const float radius, const std::string& color) : shape_(color), radius_(radius){}

    float area() 
    {
        return (radius_ * radius_) * 3.14159;
    }

    void printAllInfo()
    {
        std::cout << "Radius: " << radius_ << std::endl;
        std::cout << "Area: " << area() << std::endl;
        shape_.printColor();
    }
};

class Rectangle
{
private:
    float width_;
    float height_;
    Shape shape_;
public:
    Rectangle(const float width, const float height,const std::string& color) : shape_(color),height_(height), width_(width){}
    
    float area()
    {
        return width_ * height_;
    }
    void printAllInfo()
    {
        std::cout << "Height: " << height_ << std::endl;
        std::cout << "width: " << width_ << std::endl;
        std::cout << "Area: " << area() << std::endl;
        shape_.printColor();
    }
};

int main()
{
    // Example usage
    std::cout << "circle: " << std::endl;
    Circle myCircle(5.0, "Blue");
    myCircle.printAllInfo();

    std::cout << "Rectangle: " << std::endl;
    Rectangle myRectangle(10, 15.3, "GRØN");
    myRectangle.printAllInfo();

    return 0;
}