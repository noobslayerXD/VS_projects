import numpy as np
import scipy.stats as stats

### Problem 1
n1 = 65
x_hat1 = 36.725
s1 = 0.699

n2 = 65
x_hat2 = 36.886
s2 = 0.743

# a: write down the null hypothesis that the mean body temperatur of men and women is the same
# mu1 = mu2

# b: test your null hypothesis vs. the alternative hypothesis that the mean body temperature of men and women is not the same. Use a significance level of 0.05
delta_hat = x_hat1 - x_hat2
variance_estimate = 1/(n1+n2-2) * ((n1-1)*(s1)**2+(n2-1)*(s2)**2)

s = variance_estimate ** 0.5
print("s:",s)

t = (x_hat1-x_hat2)/(s*(1/n1+1/n2)**0.5)
print("t:",t)

p_approx = 2*(1-stats.t.cdf(abs(t),n1+n2-2))
print("Approximated p-value:",p_approx)
print("Since p>0.05, then we fail to reject the null hypothesis")

# c: Compute a 95% confidence interval for the difference between the population means
t0 = stats.t.ppf(1-0.05/2,n1+n2-2)

delta_neg = round(float((x_hat1-x_hat2)-t0*s*(1/n1+1/n2) ** 0.5),4)
delta_pos = round(float((x_hat1-x_hat2)+t0*s*(1/n1+1/n2) ** 0.5),4)

print("95% confidence interval for the difference between the population means:", (delta_neg, delta_pos))

### Problem 4
n = 10
x1 = np.array([88, 92, 85, 80, 83, 84, 86, 78, 81, 95])
x2 = np.array([89, 90, 87, 84, 84, 86, 86, 84, 83, 92])

# a: test the null hypothesis H=:delta = 0 against the alternative H1 delta !=0
# d is the sum of x1i - x2i devided by n, do it with a for loop
# Calculate differences d_i = x1_i - x2_i
d_array = x1 - x2  # Vectorized operation - much more efficient than loop

d = sum(d_array) / n  # Calculate the mean of the differences   
print("d:", d)
delta = np.mean(d_array)
variance = np.var(d_array, ddof=1)
std_div = np.std(d_array, ddof=1)
print(delta)
print(variance)
print(std_div)
delta0 = 0
# test size
t = (d-delta0)/(std_div/(n)**0.5)
print("t value:",t)
p = 2*(1-stats.t.cdf(abs(t),n-1))
print("p value:", p)
print("Since p>0.05, we fail to rejct the null hypothesis")

# b: compute a 95% confidence interval for the effect, delta
t0 = stats.t.ppf(1-0.05/2,n-1)
delta_neg = d-t0*std_div/(n)**0.5

delta_pos = d+t0*std_div/(n)**0.5
# print result
print(f"the 95 percent confidence interval is from {delta_neg} to {delta_pos}")