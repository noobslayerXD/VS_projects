# Import CSV Files and Plot Data
# First row is name of data. first column is time, and second column is voltage data.

import matplotlib.pyplot as plt
import pandas as pd

# Read the CSV file (assuming it's in the same directory)
df = pd.read_csv('KomparatorTest.CSV', header=None)

# Check if the first row contains text (headers) or data
try:
    # Try to convert first cell to float; if it works, it's data, not header
    float(df.iloc[0, 0])
    # If no error, first row is data, so add headers
    df.columns = ['time', 'voltage']
    print("No headers found; added 'time' and 'voltage' as column names.")
except ValueError:
    # First row is text, so it's headers; set as columns
    df.columns = df.iloc[0]
    df = df[1:].reset_index(drop=True)
    print("Headers found in first row.")

print("First few rows of the data:")
print(df.head())

# Use column names
time = df['time'] if 'time' in df.columns else df.iloc[:, 0]
voltage = df['voltage'] if 'voltage' in df.columns else df.iloc[:, 1]

# Plot the data
plt.figure(dpi=300, figsize=(10, 6))
plt.plot(time, voltage)
plt.grid()
plt.xlabel('Tid (s)')
plt.ylabel('Spænding (V)')
plt.xlim(-0.000001, 0.000001)
plt.title('Voltage vs Time')
plt.savefig('plot.png', dpi=1000)  # Save the plot as a high-resolution image
print("Plot saved as plot.png")
