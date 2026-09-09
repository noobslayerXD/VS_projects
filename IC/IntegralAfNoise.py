# Import csv file and integrate noise
import csv

import numpy as np

# import csv and define
# Column 0 = time (s) or frequency (Hz)
# Column 1 = RMS noise (V)
file_path = '40uANoise.csv'

# Read time/frequency and noise values
time_values = []
noise_values = []

with open(file_path, 'r') as csvfile:
    csvreader = csv.reader(csvfile)
    next(csvreader)  # Skip header row if present
    
    for row in csvreader:
        time_values.append(float(row[0]))  # Time or frequency
        noise_values.append(float(row[1]))  # Noise values

# Convert to numpy arrays
time_array = np.array(time_values)
noise_array = np.array(noise_values)

# Calculate the definite integral using the trapezoidal rule
integrated_noise = np.trapezoid(noise_array, time_array)

print(f"Definite integral of noise: {integrated_noise}")
print(np.sqrt(integrated_noise))


