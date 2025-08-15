import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
# import seaborn as sns
# import pandas as pd

## Problem 2
x = np.array([ 1, 2, 3, 4, 5, 6, 7, 8, 9 ])
y = np.array([ 2, 1, 6, 14, 15, 30, 40, 74, 75 ])

# a: Make a scatterplot x vs y
plt.scatter(x,y)
plt.show()

# b: 
res = stats.linregress(x,y)
print(res)
plt.plot(x, y, 'o', label='original data')
plt.plot(x, res.intercept + res.slope * x, 'r', label='fitted line')
plt.legend()
plt.show()

# c: make a residual plot
residuals = y - (res.intercept + res.slope * x)
plt.scatter(x, residuals)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('x')
plt.ylabel('Residuals')
plt.title('Residual Plot')
plt.show()
# The assumption of linearity does not hold

# d: transform y by taking the square root
y_trans = y ** 0.5
print(y_trans)

# e: find the regression line for dredicing sqrt(y) from x
res = stats.linregress(x,y_trans)
plt.plot(x, y_trans, 'o', label='original data')
plt.plot(x, res.intercept + res.slope * x, 'r', label='fitted line')
plt.legend()
plt.show()

# f: make a residual plot, does the assumption of linearity seem to hold
residuals = y_trans - (res.intercept + res.slope * x)
plt.scatter(x, residuals)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('x')
plt.ylabel('Residuals')
plt.title('Residual Plot')
plt.show()