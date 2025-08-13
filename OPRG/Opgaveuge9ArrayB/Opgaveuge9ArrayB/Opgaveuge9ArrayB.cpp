#include <iostream>

using namespace std;

int main() {
    int arr[] = { 4, 7, 2, 9, 1, 5, 8, 3, 6 }; // opretter et array med forskellige tal
    int n = sizeof(arr) / sizeof(arr[0]); // beregner størrelsen af arrayet

    int smallest = arr[0]; // initialiserer variablen smallest med det første element i arrayet
    int largest = arr[n - 1]; // initialiserer variablen largest med det sidste element i arrayet

    // Itererer igennem arrayet og sammenligner hvert element med smallest og largest
    for (int i = 0; i < n; i++) {
        if (arr[i] < smallest) {
            smallest = arr[i]; // opdaterer smallest, hvis der findes et mindre tal
        }
        if (arr[i] > largest) {
            largest = arr[i]; // opdaterer largest, hvis der findes et større tal
        }
    }

    // Udskriver det mindste og største tal i arrayet
    cout << "Det mindste tal i arrayet er: " << smallest << endl;
    cout << "Det største tal i arrayet er: " << largest << endl;

    return 0;
}