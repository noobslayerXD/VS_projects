import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

# Opgave 3
# X[n] = Y[n]+W
# Y[n] er i.i.d, discret uniformt fodelt
# W er kontinuert uniformt fordelt 

N = 11
n = np.arange(0, N)
MC = 3

for i in range(MC):
    y = n * np.random.rand(N)
    w = -np.random.rand(1)
    x = y + w
    plt.plot(n, x, label=f'x_{i+1}')
    
plt.grid(True)
plt.title('3 realisationer af X')
plt.xlabel('n')
plt.ylabel('x')
plt.legend()
plt.show()


### Opgave 4
T = np.array([32.3, 31.4, 29.8, 34.2, 30.5, 30.8, 32.5, 31.9, 33.1, 32.4])
n = len(T)
# a: Betem den estimerede middeltemperatur og varians under proccesen
mean_est1 = np.mean(T)
mean_est2 = np.sum(T)/n
var = np.var(T,ddof=1) # ddof er delta degree of freedom

diff = []

for i in range(n):
    diff.append((T[i]-mean_est1)**2)
var2 = sum(diff)/(n-1)
print("Estimerede middelværdi, med mean funktion:",mean_est1)
print("Estimerede middelværdi, med summen dividerede med antal samples:",mean_est2)
print("Estimerede varians med var funktion:",var)
print("Estimerede varians med for løkke:",var2)


# b: Lav QQ plot
stats.probplot(T, plot=plt)
plt.show()

# d: 
mu_0 = 32
s = var ** 0.5
t = (mean_est1-mu_0)/(s/(n) ** 0.5)
p = 2 * (1 - stats.t.cdf(abs(t),n-1))

print("p værdien er:", p)

if (p> 0.05):
    print("Vi kan ikke afvise nul hypotesen")
else:
    print("Vi kan godt afvise nul hypotesen")


# e: bestem 95% konfidens intervallet
t_0 = stats.t.ppf(1-0.05/2,n-1)

delta_neg = mean_est1 - t_0 * s/n **0.5
delta_pos = mean_est1 + t_0 * s/n **0.5

print(f"95% konfidens intervallet går fra {delta_neg} til {delta_pos}")