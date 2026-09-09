import numpy as np
from scipy import stats

### Problem 1
mean = 100
std_dev = 15


# a: probability of a value exceeding 125
p_value = 1 - stats.norm.cdf(125, loc=mean, scale=std_dev)
print("P-value for exceeding 125:", p_value)

# b: what is the probability that the demand will be less than 75
p_value_less_than_75 = stats.norm.cdf(75, loc=mean, scale=std_dev)
print("P-value for demand less than 75:", p_value_less_than_75)

p_value_less_than_70 = stats.norm.cdf(70, loc=mean, scale=std_dev)
print("P-value for demand less than 70:", p_value_less_than_70)

# c: How many should be stocked to ensure with 95% probability all demands will be met?
stocked_amount = stats.norm.ppf(0.95, loc=mean, scale=std_dev)
print("Stocked amount for 95% probability:", stocked_amount)

### Problem 4
sample_mean = 350000
sample_size = 40
sample_std_dev = 60000
# how significant is the evidence that the population mean is greater than 300000, give a p-value
z_score = (sample_mean - 300000) / (sample_std_dev / np.sqrt(sample_size))
print("Z-score for population mean greater than 300000:", z_score)
p_value_greater_than_300000 = stats.norm.cdf(z_score)

print("P-value for population mean greater than 300000:", p_value_greater_than_300000) 

### Problem 6
sample_size = 40
sample_mean = 350000
sample_std_dev = 60000
# find a 95% confidence interval for the population mean
confidence_level = 0.95
z_critical = stats.norm.ppf((1 + confidence_level) / 2)
margin_of_error = z_critical * (sample_std_dev / np.sqrt(sample_size))
confidence_interval = (float(sample_mean - margin_of_error), float(sample_mean + margin_of_error))
rounded_confidence_interval = (round(confidence_interval[0], 2), round(confidence_interval[1], 2))
print("95 percent confidence interval for the population mean:", rounded_confidence_interval)
print("95 percent confidence interval for the population mean:", confidence_interval)