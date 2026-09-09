import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

## Opgave 3

# a: 
N = 11
n = np.arange(0, N-1)
MC = 3

for i in range(MC):
    y = np.random.randint(-1, 2, size=N)   # giver -1,0,1
    # print(y) # fejlfinding
    x = y[:-1] + 2 * y[1:]                  
    # print(x) # fejlfinding
    plt.plot(n, x, label=f'x_{i+1}')

plt.grid(True)
plt.title("3 realisationer af X'")
plt.xlabel('n')
plt.ylabel('x')
plt.legend()
plt.show()


## Opgave 4
f = np.array([4.53, 5.12, 5.43, 6.09, 6.35, 7.29, 7.88, 8.65])
K_e = [0.18, 0.33, 0.55, 0.71, 0.98, 1.38, 1.46, 1.80]
n = len(f)
# a:
plt.scatter(f, K_e)
plt.show()

# b: lineær regression
res = stats.linregress(f,K_e)


plt.plot(f, K_e, 'o', label='original data')
plt.plot(f, res.intercept + res.slope * f, 'r', label='fitted line')
plt.legend()
plt.show()

print("alfa:",res.intercept)
print("beta:",res.slope)


# c: residual
# Beregn residualerne
residuals = K_e - (res.intercept + res.slope * f)
print("Residuals:", residuals)

# Plot residualerne
plt.scatter(f, residuals)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel("Head Size")
plt.ylabel("Residuals")
plt.show()


# e:
alfa = -res.intercept
print("alfa:", alfa)
alfa_0 = 1.5

# Calculate s_xx
s_xx = np.sum((f - np.mean(f)) ** 2)
print("s_xx:", s_xx)


# Calculate residual variance (mean squared error)
residuals = K_e - (res.intercept + res.slope * f)
s_squared = np.sum(residuals ** 2) / (n - 2)
print("Residual variance (s^2):", s_squared)
s = np.sqrt(s_squared)


# Calculate t-statistic for intercept
t = (alfa - alfa_0) / (np.sqrt(s_squared * (1/n + (np.mean(f) ** 2) / s_xx)))
print("t-statistic for intercept:", t)

p = 2* (1-stats.t.cdf(abs(t),n-1))
print("P value:", p)
print("Siden p er større end 0.05 så kan vi ikke afvise nul hypotesen")

# f: R^2

covarians_arr = []
var_f_arr = []
var_Ke_arr = []

for i in range(n):
     covarians_arr.append(f[i]*K_e[i]-np.mean(f)*np.mean(K_e))
     var_f_arr.append((f[i]-np.mean(f))**2)
     var_Ke_arr.append((K_e[i]-np.mean(K_e))**2)
covarians = sum(covarians_arr)
var_f = sum(var_f_arr)
var_Ke = sum(var_Ke_arr)

r = covarians/(var_f*var_Ke)**0.5


Coefdetermin = r**2
print(Coefdetermin)
print(res.rvalue)

