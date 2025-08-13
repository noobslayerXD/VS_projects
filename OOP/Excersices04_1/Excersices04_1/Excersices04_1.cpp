#include <iostream>
#include <cstdlib>
#include <ctime>
#include <vector>
using namespace std;


class Die {
private:
	static vector<int> results; // Static vector to store all results
	int value;
public:
	int roll()
	{
		value = rand() % 6 + 1;

		// Add the rolled value to the static vector
		results.push_back(value);

		return value;
	}
	int getValue()
	{
		return value;
	}

	// Static method to get all the results
	static const vector<int>& getAllResults() {
		return results;
	}

	// Static method to calculate and return the average of all results
	static double getAverage() {
		if (results.empty()) {
			return 0.0; // Handle the case where there are no results
		}

		int sum = 0;
		for (int num : results) {
			sum += num;
		}

		return static_cast<double>(sum) / results.size();
	}
	
};

vector<int> Die::results; // Initialize the static vector

int main()
{
	srand(static_cast<unsigned int>(time(nullptr)));

	Die die;

	for (int i = 0; i < 10000000000; ++i) {
		int result = die.roll();
		//cout << "Roll " << i + 1 << ": " << result << endl;
	}
	
	// Get and display all the results
	const vector<int>& allResults = Die::getAllResults();
	/*cout << "All results: ";
	for (int result : allResults) {
		cout << result << " ";
	}
	cout << endl;
	*/
	// Calculate and display the average
	double average = Die::getAverage();
	cout << "Average: " << average << endl;
	
	return 0;

}