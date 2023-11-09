#include <iostream>

using namespace std;

int sum(int arr[], int n) {
    int total = 0;
    for (int i = 0; i < n; i++) {
        total += arr[i];
    }
    return total;
}

int main() {
    int arr[10];
    int n = 0;

    // Indtast op til 10 tal og gem dem i arrayet
    while (n < 10) {
        int x;
        cout << "Indtast et tal (eller indtast '0' for at stoppe): ";
        cin >> x;
        if (x == 0) {
            break;
        }
        arr[n] = x;
        n++;
    }

    // Udskriv summen af tallene i arrayet
    cout << "Summen af tallene i arrayet er: " << sum(arr, n) << endl;

    return 0;
}