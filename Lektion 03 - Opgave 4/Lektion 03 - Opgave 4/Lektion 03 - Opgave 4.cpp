#include <iostream>
#include <vector>
using namespace std;


int main() {
    vector<int> numbers; // opret en tom vektor af heltal
    int num;

    cout << "Indtast positive heltal (indtast 0 for at afslutte): " << endl;

    while (cin >> num && num != 0) { // læs input fra brugeren, afslut hvis inputtet er 0
        numbers.push_back(num); // tilføj tallet til vektoren
    }

    cout << "Du indtastede følgende tal: ";

    int i = 0;
    while (i < numbers.size()) { // iterer gennem vektoren og udskriv hvert element
        cout << numbers[i] << " ";
        i++;
    }

    cout << endl;
    int sum = 0;
    int j = 0;
    while (j < numbers.size()) {
        sum += numbers[j];
        j++;
    }
    cout << sum / numbers.size();
    
}

