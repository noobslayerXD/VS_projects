#include <iostream>
#include <map>
#include <string>
#include <Windows.h> 
#include <utilapiset.h>

int main()
{
	while (true)
	{
		std::string ToneIn;
		std::cout << "Skriv en tone: ";
		std::cin >> ToneIn;

		std::map<std::string, double> Tones;

		Tones["C"] = 261.6;
		Tones["C#"] = 277.3;
		Tones["D"] = 293.8;
		Tones["D#"] = 311.3;
		Tones["E"] = 329.8;
		Tones["F"] = 349.3;
		Tones["F#"] = 370;
		Tones["G"] = 392;
		Tones["G#"] = 415.3;
		Tones["A"] = 440;
		Tones["A#"] = 466.3;
		Tones["B"] = 494;

		if (Tones.find(ToneIn) != Tones.end())
		{
			// Valid tone name, display corresponding value
			std::cout << "The corresponding musical note is: " << Tones[ToneIn] << std::endl;

			unsigned int duration = 500;
			Beep(Tones[ToneIn], duration);
		}
		else
		{
			// Invalid tone name, display error message
			std::cout << "Error: Invalid tone name. Please enter a valid tone name." << std::endl;
		}
	}
}
