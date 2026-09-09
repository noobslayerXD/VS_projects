import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

### Problem 1
n = 100
p = 0.35

# a: probability that more than 40 costumers
probAbove40 = 1-stats.binom.cdf(40, n, p)
print(probAbove40)

# b: probability that less than 30 constumers
probBelow30 = stats.binom.cdf(29,n,p)
print(probBelow30)

# c: probability that exactly 45 costumers
probExact45 = stats.binom.pmf(45,n,p)
print(probExact45)

### problem 2
n = 10
p1 = 0.1
p2 = 0.5
p3 = 0.9

# a: 
#print results
mean1 = n*p1
std_div1 = (n*p1*(1-p1)) ** 0.5
print(f"Mean: {mean1}, Standard Deviation: {std_div1}")

mean2 = n*p2
std_div2 = (n*p2*(1-p2)) ** 0.5
print(f"Mean: {mean2}, Standard Deviation: {std_div2}")

mean3 = n*p3
std_div3 = (n*p3*(1-p3)) ** 0.5
print(f"Mean: {mean3}, Standard Deviation: {std_div3}")

# b: plot the three PDF
x = np.arange(0, n+1)
pdf1 = stats.binom.pmf(x, n, p1)
pdf2 = stats.binom.pmf(x, n, p2)
pdf3 = stats.binom.pmf(x, n, p3)

plt.plot(x, pdf1, label='p=0.1')
plt.plot(x, pdf2, label='p=0.5')
plt.plot(x, pdf3, label='p=0.9')
plt.xlabel('Number of Successes')
plt.ylabel('Probability')
plt.title('Binomial Distribution PMF')
plt.legend()
plt.show()

# c: 


### problem 3
p = 0.35
x = 30
n = 100

# a: Write down a statistical model describing the survey

# b: Write down a null hypothesis and an alternative hypothesis for the company's belief
# H0: p = 0.35 (The true proportion of customers who prefer the new product is 35%)
# H1: p != 0.35 (The true proportion of customers who prefer the new product is not equal to 35%)

# c: Test your null hypothesis using the exact p-value
p_value = 2*min(1-stats.binom.cdf(40,n,p),stats.binom.cdf(30,n,p))
print("Real p value",p_value)
# p= 0.25, siden det er større end 0,05 så kan vi ikke afslå null hypothesen

# d: Test your null hypothesis using the normal approximation to the p-value
z = (x - n*p)/(n*p*(1-p)) ** 0.5
print("z value:", z)

p_value_approx = 2*min(1-stats.norm.cdf(z),stats.norm.cdf(z))
print("P value approximaion:", p_value_approx)