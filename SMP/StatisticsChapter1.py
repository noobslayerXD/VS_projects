import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

### Problem 1
Sample_mean = 260
mean = 250
std_dev = 2.5
sample_size = 25

z = (Sample_mean - mean) / (std_dev/sample_size**0.5)
print("Z-score:", z)

# p-value calculation
p_value = 1 - stats.norm.cdf(z)
print("P-value:", p_value)

# den er under 0.05, så vi kan afvise hypotesen om at sample mean er lig med population mean

### Problem 2 at what sample_mean can we reject the null hypothesis
p = 0.05
critical_value = stats.norm.ppf(1 - p)
print("Critical value for p =", p, ":", critical_value)
# Calculate the minimum sample mean to reject the null hypothesis
min_sample_mean = mean + critical_value * (std_dev / sample_size**0.5)
print("Minimum sample mean to reject null hypothesis:", min_sample_mean)

### problem 3 calculate the two sided p-value when sample mean is 250.2
sample_mean = 250.2
z = (sample_mean - mean) / (std_dev / sample_size**0.5)
p = 2*(1 - stats.norm.cdf(z))
print("Two-sided p-value for sample mean", sample_mean, ":", p)

### Problem 4 using the two sided p-value, what range of values of sample would give rise to a p-value larger than 0.05
lower_bound = round(float(mean - critical_value * (std_dev / sample_size**0.5)), 2)
upper_bound = round(float(mean + critical_value * (std_dev / sample_size**0.5)), 2)
print("Range of values for sample mean with p-value > 0.05:", (lower_bound, upper_bound))
