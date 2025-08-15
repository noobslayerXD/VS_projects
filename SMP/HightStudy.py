import numpy as np
import scipy.stats as stats

m = np.array([1.76, 1.79, 1.60, 1.90, 1.78, 1.74, 1.75, 1.80, 1.82, 1.77, 1.79, 1.78, 1.38, 1.87, 1.59])

mean = 1.78
std_div = 0.2
n = len(m)
# 1: Estimate the mean of the population sample
sample_mean = np.mean(m)
print("Estimate of the mean",mean)

# 2: Formulate the NULL hypothesis to test whether the sample has the same sample mean as the rest of the population
# mean = sample_mean

# 3: Formulate the alternative hypothesis to the NULL hypothesis
# mean != sample_mean

# 4: Calculate the test statistics z
z = (sample_mean-mean)/(std_div/(n** 0.5))
print("The Z value is: ", z)

# 5: find the p-value basted on a Gaussian pdf
p = 2*abs(1-stats.norm.cdf(z))
print("The p value is: ", p)

# 6: With a significance level of alpha = 0.05, can we reject the NULL hypothesis
# since p > alpha then the NULL hypothesis cannot be rejected

# 7: With a significance level of alpha = 0.05, can we reject the NULL hypothesis
# since p > alpha then the NULL hypothesis cannot be rejected

# 8: repeat the experiment 100 times
repeats = 1000
p_values = []
for _ in range(repeats):
    m = np.random.normal(mean,std_div,n)
    sample_mean = np.mean(m)
    z = (sample_mean-mean)/(std_div/(n** 0.5))
    p = 2*abs(1-stats.norm.cdf(z))
    p_values.append(p)

# with a significance level of alpha = 0.05, how often can we reject the NULL hypothesis
alpha = 0.05
rejections = sum(p < alpha for p in p_values)
print(f"Reject the NULL hypothesis {rejections} out of {repeats} times")

# if we change the mean to 1.88, how often do we falsely fail to reject the NULL hypothesis
new_mean = 1.88
n = 30
p_values2 = []
for _ in range(repeats):
    m = np.random.normal(new_mean,std_div,n)
    sample_mean = np.mean(m)
    z2 = (sample_mean-mean)/(std_div/(n** 0.5))
    p2 = 2*min(1-stats.norm.cdf(z2), stats.norm.cdf(z2))
    p_values2.append(p2)

falsely_failed_rejections = sum(p2 > alpha for p2 in p_values2)
print(f"Falsely failed to reject the NULL hypothesis {falsely_failed_rejections} out of {repeats} times")
print(falsely_failed_rejections/repeats)


# 9: repeat part 8 with alpha 0.10
alpha = 0.10

rejections = sum(p < alpha for p in p_values)
print(f"Reject the NULL hypothesis {rejections} out of {repeats} times")
print(rejections/repeats)


falsely_failed_rejections = sum(p2 > alpha for p2 in p_values2)
print(f"Falsely failed to reject the NULL hypothesis {falsely_failed_rejections} out of {repeats} times")
print(falsely_failed_rejections/repeats)