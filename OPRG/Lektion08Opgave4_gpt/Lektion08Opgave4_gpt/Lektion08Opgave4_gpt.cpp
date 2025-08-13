#include <iostream>
using namespace std;
class Container {
private:
    double tryk;
    double volumen;
    double n;
    double temperatur;
    const double R = 0.0831; // L*bar/(mol*K)

public:
    // Constructor
    Container(double n_, double v_, double t_)
        : n(n_), volumen(v_), temperatur(t_)
    {
        tryk = n * R * temperatur / volumen;
    }

    // Getter methods
    double getPressure() const { return tryk; }
    double getVolume() const { return volumen; }
    double getMoles() const { return n; }
    double getTemperature() const { return temperatur; }

    // Set pressure at fixed volume
    void setPressureAtFixedVolume(double pressure)
    {
        if (pressure <= 0) {
            cout << "Error: pressure must be positive\n";
            return;
        }
        tryk = pressure;
        n = tryk * volumen / (R * temperatur);
    }

    // Set temperature at fixed volume
    void setTemperatureAtFixedVolume(double temperature)
    {
        if (temperature <= 0) {
            cout << "Error: temperature must be positive\n";
            return;
        }
        temperatur = temperature;
        tryk = n * R * temperatur / volumen;
    }
};
int main()
{
    double n = 5;  // antal molekyler
    double V = 2;  // volumen i liter
    double T = 298;  // temperatur i Kelvin
    Container Beholder1(n, V, T);
    
    // Udskriv værdierne i beholderen inden ændring
    cout << "Før ændring:" << endl;
    cout << "Antal molekyler: " << Beholder1.getMoles() << endl;
    cout << "Volumen: " << Beholder1.getVolume() << endl;
    cout << "Temperatur: " << Beholder1.getTemperature() << endl;
    cout << "Tryk: " << Beholder1.getPressure() << endl;

    // Ændr trykket i beholderen
    double newPressure = 2.5;  // nyt tryk i bar
    Beholder1.setPressureAtFixedVolume(newPressure);

    // Udskriv værdierne i beholderen efter ændring af trykket
    cout << endl << "Efter ændring af tryk:" << endl;
    cout << "Antal molekyler: " << Beholder1.getMoles() << endl;
    cout << "Volumen: " << Beholder1.getVolume() << endl;
    cout << "Temperatur: " << Beholder1.getTemperature() << endl;
    cout << "Tryk: " << Beholder1.getPressure() << endl;

    // Ændr temperaturen i beholderen
    double newTemperature = 350;  // ny temperatur i Kelvin
    Beholder1.setTemperatureAtFixedVolume(newTemperature);

    // Udskriv værdierne i beholderen efter ændring af temperaturen
    cout << endl << "Efter ændring af temperatur:" << endl;
    cout << "Antal molekyler: " << Beholder1.getMoles() << endl;
    cout << "Volumen: " << Beholder1.getVolume() << endl;
    cout << "Temperatur: " << Beholder1.getTemperature() << endl;
    cout << "Tryk: " << Beholder1.getPressure() << endl;

    return 0;
}