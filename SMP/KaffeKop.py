import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm


# create 100 normal distributed random numbers
mean = 250
std_dev = 2.5
X = np.random.normal(loc=mean, scale=std_dev, size=100)

# create a histogram of the data
# plt.hist(X)
# plt.show()

# calculated mean and standard deviation
calculated_mean = np.mean(X)
calculated_std_dev = np.std(X)

print("Calculated mean:", calculated_mean)
print("Calculated standard deviation:", calculated_std_dev)

# norm cdf
print("Norm CDF at mean:", norm.cdf(0.4))