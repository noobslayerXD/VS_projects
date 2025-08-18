import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
# import seaborn as sns
# import pandas as pd

### Opgave 2
mu = 10
sigma = 2 ** 0.5
# a: plot normalfordeling
x = np.linspace(mu - 4*sigma, mu + 4*sigma, 100)
y = stats.norm.pdf(x, mu, sigma)
plt.plot(x, y)
plt.title("Normalfordeling")
plt.xlabel("x")
plt.xlim([6, 14])
plt.ylabel("Probability Density")
plt.grid()
plt.show()

# b: P(x<5)
y2 = stats.norm.cdf(x, mu, sigma)
P_x_less_5 = y2[5]
print("P(x<5):", P_x_less_5)

# c: Høj PDF
mu2= 5
varians = 0.1
std_div = varians ** 0.5


x = np.linspace(mu2 - 4*std_div, mu2 + 4*std_div, 100)
y = stats.norm.pdf(x, mu2, std_div)
plt.plot(x, y)
plt.title("Normalfordeling")
plt.xlabel("x")
plt.ylabel("Probability Density")
plt.grid()
plt.show()

### Opgave 3

# a: 
N = 11
n = np.arange(0, N)
MC = 3

for i in range(MC):
    y = np.random.randint(0,4+1,N)
    print(y)
    z = 6 * np.random.rand(N) - 3
    x = 4 * y - z **2
    plt.plot(n, x, label=f'x_{i+1}')
    
plt.grid(True)
plt.title('3 realisationer af X')
plt.xlabel('n')
plt.ylabel('x')
plt.legend()
plt.show()



### Opgave 4
n = 10
X = np.array([1, 2, 5, 10, 15, 20, 25, 30, 40, 50])
Y = np.array([1.55, 2.88, 6.82, 11.13, 17.42, 22.23, 28.11, 33.82, 44.54, 54.39])

## a: Opstil udtryk for og beregn sample middelværiden af de målte værdier
sum_Y = 0
for i in range(n):
    sum_Y += Y[i]

Sample_mean_Y = sum_Y / n
print("Mean of Y:", Sample_mean_Y)

## b: Calculate the variance without using built in functions
sum_squared_diffs = 0
for i in range(n):
    sum_squared_diffs += (Y[i] - Sample_mean_Y) ** 2

Sample_variance_Y = sum_squared_diffs / (n - 1)
print("Variance of Y:", Sample_variance_Y)

## c: beregn beta
res = stats.linregress(X, Y)
print("beregning af beta:", res.slope)

## d: beregn alfa
print("beregning af alfa:", res.intercept)

## e: Lav et residual plot
residuals = Y - (res.intercept + res.slope * X)
plt.scatter(X, residuals)
plt.axhline(0, color="red", linestyle="--")
plt.xlabel("x")
plt.ylabel("Residuals")
plt.title("Residual Plot")
plt.show()

## f: opstil udtryk for og beregn et unbiased estimat af residualernes varians
print("Unbiased varians:", np.var(residuals, ddof=2))
