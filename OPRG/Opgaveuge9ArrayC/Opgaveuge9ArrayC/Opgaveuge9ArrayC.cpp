#include <iostream>

using namespace std;

float beregnGennemsnit(int arr[], int n) {
    int sum = 0; // initialiserer summen til 0
    for (int i = 0; i < n; i++) {
        sum += arr[i]; // adderer hvert element til summen
    }
    float gennemsnit = (float)sum / n; // dividerer summen med antallet af elementer for at få gennemsnittet
    return gennemsnit; // returnerer gennemsnittet
}


float beregnGennemsnit(int arr[], int n);

int main() {
    int arr[10];
    int n;
    cout << "Indtast op til 10 tal i arrayet:" << endl;
    for (int i = 0; i < 10; i++) {
        cin >> arr[i];
        if (arr[i] == 0) {
            n = i;
            break;
        }
    }

    float gennemsnit = beregnGennemsnit(arr, n); // kalder funktionen beregnGennemsnit for at beregne gennemsnittet af elementerne i arrayet

    cout << "Gennemsnittet af elementerne i arrayet er: " << gennemsnit << endl;

    return 0;
}