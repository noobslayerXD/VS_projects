import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
# import seaborn as sns
# import pandas as pd
from scipy.integrate import quad

# region Opgave 1


# endregion


# region Opgave 2
def f_x(x):
    if 0 <= x < 2:
        return 1/4
    elif 2 <= x <= 3:
        return 1/2
    else:
        return 0

x_vals2 = np.arange(-1, 5, 0.01)
y_vals2 = [f_x(x) for x in x_vals2]
# a: Bestem og skitser fordelingsfunktionen CDF F_X(x) for x i intervallet -1 til 4

# Hvis den er continuert
def F_x(x):
    if x < 0:
        return 0
    elif 0 <= x <2:
        return x/4
    elif 2 <= x <= 3: 
        return (x/2)-1/2
    elif x >= 3:
        return 1


x_vals = np.arange(-1, 5, 0.01)
y_vals = [F_x(x) for x in x_vals]

plt.plot(x_vals, y_vals)
plt.xlabel('x')
plt.ylabel('$F_x(x)$')
plt.title('Plot af $F_x(x)$')
plt.show()

# b: 
result, error = quad(lambda x: f_x(x)*x, -np.inf, np.inf)
print("Integral of f_x(x)*x from -inf to inf (forventningsværdi):", result)

# c:
result, error = quad(lambda x: f_x(x)*x**2, -np.inf, np.inf)
print("Integral of f_x(x)*x from -inf to inf (forventningsværdi):", result)

# endregion


# region Opgave 3
n_vals = np.arange(0, 10)           # n = 0 to 9
x_1 = (1/2)*n_vals + 4         
x_2 = -(1/2)*n_vals + 4
x_3 = 2

# a:
plt.plot(n_vals, x_1) 
plt.plot(n_vals, x_2) 
plt.axhline(y=x_3)
plt.xlabel('n')
plt.grid(True)
plt.show()

# b: beregn ensemble mean
# x1 og x2 går ud med hinaden 
# x_3 mean er konstant
X_mean = (2 + 4 + 4)/3
print("ensemble mean af X:",X_mean)

# c: processen er ikke WSS og derfor også ikke ergodisk
# Dette er fordi variansen afhænger af samplen


# endregion


# region Opgave 4

x = np.array([1,2,3,4,5,6,7,8,9,10])
y = np.array([18.65,23.02,20.72,19.93,20.71,19.79,19.87,21.48,21.40,21.41])

## a: Beregn sample middelværdi og varians af vindhastighed målingerne
Sample_mean_y = np.mean(y)
variance_y = np.var(y,ddof=1)
print("Sample mean af vindhastighederne:", Sample_mean_y)
print("Variancen af vindhastigheds målingerne:", variance_y)

## Vi ønsker at teste nulhypotesen H0: mu=20
## b: Hvilken test og test statestik benyttes
print("Den statistiske model vi bruger er den fra side 62 i statistik noten, da det er normalfordelt data og vi kender ikke variansen")

## c: beregn p-værdien, kan nulhypotesen afvises med et 5% signifikansniveau
mu_0 = 20
mu_hat = Sample_mean_y
s = variance_y ** 0.5
1
t = (mu_hat-mu_0)/(s*(len(y))**0.5)
print("t:",t)
# approximate p-value
p = 2*(1-stats.t.cdf(abs(t),len(y)))
print("P værdien er:", p)

if(p>0.05):
    print("We fail to reject the null hypothesis")
else:
    print("We can reject the null hypothesis")
    
output_voltage = np.array([40.17,49.2,44.4,43.03,44.26,42.29,42.45,46.05,45.76,45.78])
## d: lav et scatter plot af sammenhæng mellem X og Y
X = y
Y = output_voltage
plt.scatter(X,Y)
plt.show()


## e: lav et residual plot
res = stats.linregress(X,Y)
residuals = Y - (res.intercept + res.slope * X)
plt.scatter(X, residuals)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel('x')
plt.ylabel('Residuals')
plt.title('Residual Plot')
plt.show()

## f: Beregn sample korrelationskoefficienten mellem X og Y
print(res.rvalue)
#eller
print(np.corrcoef(X,Y))

# endregion