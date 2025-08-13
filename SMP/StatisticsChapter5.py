import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

### Problem 1
n = 10
# Mean is unknown, and variance is unknown
sample_mean = 48
sample_std_dev = 16

# a: test H0: mu = 50 versus H1: mu != 50 at the 5% level
mu = 50
test_size = (sample_mean - mu) / (sample_std_dev / np.sqrt(n))
approx_p_value = 2 * (1 - stats.t.cdf(np.abs(test_size), df=n-1))

print("the approximate p value:", approx_p_value)
# Does is fail H0 or H1
print("We fail to reject H0")


# b: find the 95% confidence interval
# find t0 (critical value for 95% confidence interval)
t0 = stats.t.ppf(1-0.05/2, n-1)  # Use ppf for inverse CDF, and 0.05/2 for two-tailed
print("t0:", t0)
# Calculate the confidence interval bounds
mu_neg = round(sample_mean-t0*(sample_std_dev**0.5)/np.sqrt(n),2)
mu_pos = round(sample_mean+t0*(sample_std_dev**0.5)/np.sqrt(n),2)
print("Lower bound:", mu_neg,"Upper bound:",mu_pos)

### problem 2
pop_std_div = 2.5

mu_neg = -0.25
mu_pos = 0.25

B = 0.5

samples = (1.96*pop_std_div/B) ** 2
print("Needed samples to ensure 95 percent confidence interval of 0.5:", samples)


### Problem 3
# Sample data
x = np.array([54.0748, 56.6827, 54.7552, 44.1039, 50.2046, 53.6727, 63.9488, 50.5385, 50.0734, 52.0398])
# Calculate the length of the sample
n = len(x)

# a: verify that the samples are normally distributed

## qq-plot
stats.probplot(x, dist="norm", plot=plt)
plt.title("Q-Q Plot")
plt.show()
print("Q-Q plot shows that the sample is approximately normally distributed.")

# b: give an estimate of the mean and variance of the population
sample_mean = np.mean(x)
print("Sample mean:", sample_mean)

unbiased_estimate_of_var = np.var(x)
print("Unbiased estimate of variance:", unbiased_estimate_of_var)

# c: Find a 95% conficende interval for the population mean, mu
t0 = stats.t.ppf(1-0.05/2, n-1)
mu_neg = sample_mean - t0 * (unbiased_estimate_of_var ** 0.5)/(n ** 0.5)
mu_pos = sample_mean + t0 * (unbiased_estimate_of_var ** 0.5)/(n ** 0.5)
print("mu_neg:", mu_neg, "mu_pos:", mu_pos)
