import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt

# region Opgave 3

# a:

N = 9  # antal tidspunkter (n=0,...,10)
MC = 3  # antal realiseringer
n = np.arange(0, N+1)

for i in range(MC):
    X = np.zeros(N+1)
    Z = np.random.normal(-1, 1**0.5, N+1)
    W = np.random.normal(3, 2**0.5 ,N+1)
    for k in range(1, N+1):
        X[k] = Z[k-1] + Z[k] + W[k]
    plt.plot(n, X, label=f'Realisering {i+1}')
plt.xlabel('n')
plt.ylabel('X[n]')
plt.title('3 realiseringer af X[n]')
plt.legend()
plt.grid(True, which="both", ls="--")
plt.show()

# b: Med visning af mellemregning, bestem ensemble middelværdi og varians

# endregion

# region Opgave 4

weight = [50.58, 50.47, 50.48, 50.56, 50.60, 50.28, 50.44, 50.37, 50.46, 50.58]
n = len(weight)

# a: bestem sample middelværdi og varians
sample_mean = sum(weight)/n
sample_mean_tjek = np.mean(weight)
print("Sample mean:",sample_mean)
print("Sample mean tjek:", sample_mean_tjek)

sample_varians_arr = []

for i in range(n):
    sample_varians_arr.append((weight[i]-sample_mean)**2)

sample_var = sum(sample_varians_arr)/(n-1)
sample_var_check = np.var(weight,ddof=1)
print("Sample varians:",sample_var)
print("Sample varians tjek:",sample_var_check)

mu0 = 50

# Opstil nul hypotese og alternativ hypotese
# H0:mu=mu0
# H1:mu !=mu0

# c: Hvilken test-statisk benyttes?
# Der skal bruges den test statisk for hvor man skal finde mean og variansen er ukendt

# d: Er det nødvendigt at lave et QQ-plot for at benytte testen=
# det er ikke nødvendigt, den kan bruges til at bekræfte at dataen normal fordelt, men da vi ved at det er sandt er det ikke nødvendigt

# e: beregn p værdi, kan nulhypotesen afvises på et 5% signifikans niveau
sample_std_div = sample_var**0.5
t = (sample_mean-mu0)/(sample_std_div/(n)**0.5)
p = 2 * (1-stats.t.cdf(abs(t),n-1))

if p>0.05:
    print("We fail to reject the null hypothesis")
else:
    print("We can reject the null hypothesis")

print("P værdien er:",p)

# beregn 99% konfidens intervallet
alfa = 0.01
t0 = stats.t.ppf(1-alfa/2,n-1)

mu_lower = sample_mean - t0 * sample_std_div/(n**0.5)
mu_upper = sample_mean + t0 * sample_std_div/(n**0.5)
print(f"99% konfidensintervallet går fra {mu_lower} til {mu_upper}")