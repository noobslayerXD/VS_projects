import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


### Opgave 4

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