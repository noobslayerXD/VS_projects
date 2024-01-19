#include "IdGenerator.h"

// Denne kode blev givet med som bilag
// Husk global erklæring af en ikke const static member
int IdGenerator::id_ = 0;

int IdGenerator::new_id()
{
	// Værdien tælles op efter returværdien er fundet
	return id_++;
}
