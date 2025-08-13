import numpy as np

# Problem 1: Calculate the sample mean, variance, and standard deviation

# sample data
X = np.array([165.5, 175.4, 144.1, 178.5, 168.0, 157.9, 170.1, 202.5, 145.5, 135.7])

# Calculate the sample mean
sample_mean = np.mean(X)

#calculate the sample variance  
sample_variance = np.var(X, ddof=1)  # Using numpy's var function with ddof=1 for sample variance

# Calculate the sample standard deviation
sample_std_dev = np.std(X, ddof=1)  # Using numpy's std function with ddof=1 for sample standard deviation

# print the results
print("Sample Mean:", sample_mean)
print("Sample Variance:", sample_variance)
print("Sample Standard Deviation:", sample_std_dev)

# Problem 13
sample_mean = 110.5
sample_variance = 45.6
sample_size = 100

# find a 95% confidence interval for theta = ex_i
confidence_level = 0.95
z_critical = 1.96  # For a 95% confidence interval, z-critical is approximately 1.96
margin_of_error = z_critical * (np.sqrt(sample_variance) / np.sqrt(sample_size))
confidence_interval = (float(sample_mean - margin_of_error), float(sample_mean + margin_of_error))
rounded_confidence_interval = (round(confidence_interval[0], 2), round(confidence_interval[1], 2))
print("95 percent confidence interval for theta = ex_i:", rounded_confidence_interval)
