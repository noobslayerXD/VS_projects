#import scipy
import scipy as sp
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


my = 100
sigma = 5

## 1 Analytical Calculation (sigma =5)

print("5% tolerance interval")
slim =sp.stats.norm.cdf(105,my,sigma)-sp.stats.norm.cdf(95,my,sigma)
print(slim)

# sandsynligheden for at værdierne er mellem 90 og 95 og 105 og 110
wide = (sp.stats.norm.cdf(110,my,sigma)-sp.stats.norm.cdf(90,my,sigma))
print("10% tolerance interval")
print(wide-slim)

# out of spec below 90 above 110
out_of_spec_low = sp.stats.norm.cdf(90,my,sigma)
out_of_spec_high = 1 - sp.stats.norm.cdf(110,my,sigma)

print("Out of spec")
print(out_of_spec_low + out_of_spec_high)

## 2 Simulation (1000 samples)
samples = 1000
simulated_data = np.random.normal(my, sigma, samples)

sorted_simulated_data = np.sort(simulated_data)

print("5% tolerance interval (simulation)")
print(np.sum((sorted_simulated_data >= 95) & (sorted_simulated_data <= 105)) / samples)

print("10% tolerance interval (simulation)")
print((np.sum((sorted_simulated_data >= 90) & (sorted_simulated_data <= 110)) / samples)-(np.sum((sorted_simulated_data >= 95) & (sorted_simulated_data <= 105)) / samples))

print("Out of spec (simulation)")
print(np.sum(sorted_simulated_data < 90) / samples + np.sum(sorted_simulated_data > 110) / samples)

## 3 Tolerance to Standard Deviation
# Givet:
lower = 95         # nedre grænse for integralet
upper = 105        # øvre grænse
target_prob = 0.5  # ønsket sandsynlighed

# Funktion der repræsenterer forskellen mellem den ønskede og aktuelle sandsynlighed
def equation_to_solve(sigma):
    return sp.stats.norm.cdf(upper,my,sigma) - sp.stats.norm.cdf(lower,my,sigma) - target_prob

# Gæt et startpunkt for sigma
initial_guess = 5

# Brug fsolve til at finde sigma
sigma_solution = sp.optimize.fsolve(equation_to_solve, initial_guess)[0]

print("Løsning for sigma:", sigma_solution)

## 4 Plotting the distribution

# plot the PDF of simulated data
sns.set_theme(style="whitegrid")
plt.figure(figsize=(10, 6))
sns.histplot(sorted_simulated_data, bins=30, kde=True, stat="density", label="Simulated Data")
plt.title("Probability Density Function of Simulated Data")
plt.xlabel("Value")
plt.ylabel("Density")
plt.legend()
plt.show()

# plot the CDF of simulated data
plt.figure(figsize=(10, 6))
sns.histplot(sorted_simulated_data, bins=30, kde=True, stat="density", cumulative=True, label="Simulated Data")
plt.title("Cumulative Distribution Function of Simulated Data")
plt.xlabel("Value")
plt.ylabel("Density")
plt.legend()
plt.show()