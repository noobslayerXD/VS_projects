import numpy as np
import scipy.stats as stats




### Opgave 4: Statistik
n = 10
x1 = np.array([11.3, 17.4, 12.4, 14.5, 23.5, 19.6, 10.5, 40.7, 35.6, 42.5])
x2 = np.array([12.0, 19.7, 14.8, 15.4, 28.2, 22.2, 13.5, 42.7, 38.6, 45.8])

## a: Hvilken statisk model og test-metode skal benyttes ved testen? Begrund svaret
# Test Catalog for PAIRED data
# di = X1i - X2i
d_i = x1-x2
d_hat = np.mean(d_i)
print(d_hat)

## b: Opskriv en nulhypotese og alternativ hypotese for testen
# H0: delta = delta_0
# H1: delta != delta_0

## c: Opstil udtryk for og beregn p-værdien. Kan vi afvise nulhypotesen på 5% signifikansniveau
varianse = np.var(d_i,ddof=1)
std_div = np.std(d_i, ddof=1)

print(f"Variansen er:{varianse}, og std_div er: {std_div}")

t = (d_hat - 0)/(std_div/(n**0.5))
print("t:",t)

p = 2*(1-stats.t.cdf(abs(t),n-1))
print("P value:", p)

if (p>0.05):
    print( "We fail to reject the null hypothesis")
else:
    print(" We reject the null hypothesis")
    
## d: Opstil udtryk for og beregn 99% konfidensintervallet for forskellen i genereret energi mellem nye og gamle vindmøller
t0 = stats.t.ppf(1-0.01/2,n-1)
delta_neg = d_hat-t0*std_div/(n) **0.5
delta_pos = d_hat+t0*std_div/(n) **0.5

print(f"the 99% confidence interval is from {delta_neg} to {delta_pos}")

## e: Er det  et krav for denne test, at den generede energi for de nye vindmøller følger en normalfordeling? Begrund svaret
# Nej, det er ikke et krav at energien fra de nye møller er normalfordelt, men derimod er det et krav at forskellene imellem ny og gammel møllers energi er normalfordelt.