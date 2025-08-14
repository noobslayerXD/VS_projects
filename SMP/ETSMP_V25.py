import numpy as np
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
import random as rd

### Problem 3

# u er IID og u er uniformt fordelt mellem -2 og 2 (discrete)
n = 8
u = stats.uniform.rvs(-2, 4, n)
print("u:", u)
# z er normalt fordelt (kontinuert)
z = stats.norm.rvs(0,1,n)
print("z:", z)

# x er summen af u og z
x = u + z

## a:

plt.stem(x)
plt.xlabel('Sample Index')
plt.ylabel('Value')
plt.title('Realization of X[n]')
plt.show()


## b:
