#include <iostream>
using namespace std;

// Klasse for rektangel med invariant på areal
class RectangleByArea {
public:
    RectangleByArea(long double a) : area(a) { updateDimensions(); }

    long double getWidth() const { return width; }

    long double getHeight() const { return height; }

    void scaleWidth(double scaleFactor) { width *= scaleFactor; updateDimensions(); }

    void scaleHeight(double scaleFactor) { height *= scaleFactor; updateDimensions(); }

private:
    long double area,width,height;

    void updateDimensions() { width = sqrt(area * height); }
};

// Klasse for rektangel med invariant på omkreds
class RectangleByPerimeter {
public:
    RectangleByPerimeter(long double p) : perimeter(p) { updateDimensions(); }

    long double getWidth() const { return width; }

    long double getHeight() const { return height; }

    void scaleWidth(double scaleFactor) {
        width *= scaleFactor;
        perimeter = 2 * (width + height); // Update perimeter based on new width and height
    }

    void scaleHeight(double scaleFactor) {
        height *= scaleFactor;
        perimeter = 2 * (width + height); // Update perimeter based on new width and height
    }

private:
    long double perimeter, width, height;

    void updateDimensions() { width = perimeter / 2 - height; }
};


int main()
{
    // Test af RectangleByArea
    RectangleByArea rectByArea(12.0); // Areal på 12
    cout << "Width: " << rectByArea.getWidth() << endl; // Forventet output: Width: 2.44949
    cout << "Height: " << rectByArea.getHeight() << endl; // Forventet output: Height: 4.89898
    rectByArea.scaleWidth(2.0);
    cout << "Width: " << rectByArea.getWidth() << endl; // Forventet output: Width: 4.89898
    cout << "Height: " << rectByArea.getHeight() << endl; // Forventet output: Height: 2.44949
    rectByArea.scaleHeight(3.0);
    cout << "Width: " << rectByArea.getWidth() << endl; // Forventet output: Width: 2.87228
    cout << "Height: " << rectByArea.getHeight() << endl; // Forventet output: Height: 8.61784

    // Test af RectangleByPerimeter
    RectangleByPerimeter rectByPerimeter(14.0); // Omkreds på 14
    cout << "Width: " << rectByPerimeter.getWidth() << endl; // Forventet output: Width: 3
    cout << "Height: " << rectByPerimeter.getHeight() << endl; // Forventet output: Height: 4
    rectByPerimeter.scaleWidth(2.0);
    cout << "Width: " << rectByPerimeter.getWidth() << endl; // Forventet output: Width: 6
    cout << "Height: " << rectByPerimeter.getHeight() << endl; // Forventet output: Height: 1
    rectByPerimeter.scaleHeight(3.0);
    cout << "Width: " << rectByPerimeter.getWidth() << endl; // Forventet output: Width: 2.16667
    cout << "Height: " << rectByPerimeter.getHeight() << endl; // Forventet output: Height: 9.83333

    return 0;


}

