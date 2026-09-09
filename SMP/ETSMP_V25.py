import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

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


### Problem 4

billedserie = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
model1 = np.array([37, 48, 43, 35, 49, 41, 45, 39, 46, 47])
model2 = np.array([41, 47, 47, 44, 47, 44, 45, 47, 49, 45])
n = len(billedserie)
## a: Opstil en nulhypotese for at bestemme om model 1 eller model 2 er lige gode til at kategorisere bilerne korrekt 
# NULL hypothesis H0: begge middel værdier er ens mu_1 = mu_2
# alternativ H1: mu_1 != mu_2

## b: Hvilken type test skal benyttes: en z-test eller en t-test? En parret eller uparret test?
# Siden variansen ikke er kendt for datene så bliver det nød til at være en t-test
# Da begge modeller testes på samme billede serie så er det parrede data

## c: Bestem middelforskellen i antal korrekte hits af model 1 og model 2

difference = []

for i in range(n):
    difference.append(model1[i]-model2[i])

d_hat = sum(difference)/n
print("middelværdi af difference:",d_hat)

## d: Bestem variansen af forskllen i korrekte hits mellem model 1 og model 2
difference_of_difference = []
for i in range(n):
    difference_of_difference.append((difference[i]-d_hat) ** 2)

varians = (sum(difference_of_difference))/(n-1)
print("Variansen bliver:", varians)
s_d = varians ** 0.5 # estimat af standard afvigelsen

## e: beregn p-værdien for NULL hypotesen med 5% signifikansniveau. Kan den afvises
alpha = 0.05 # Signifikans niveau på 5%

t = (d_hat-0)/(s_d/((n)**0.5))
print("t-value:",t)

p = 2 * (1- stats.t.cdf(abs(t),n-1))
print("P-value:", p)

if (p>alpha):
    print("We fail to reject the null hypothesis")
else:
    print("We reject the null hypothesis")

## f: Opstil og bestem 95% confidence interval:
t_0 = stats.t.ppf(1-alpha/2,n-1)

delta_neg = d_hat - t_0 * s_d/n **0.5
delta_pos = d_hat + t_0 * s_d/n **0.5

print(f"Den nedre grænse bliver:{delta_neg}, og den øvre grænse bliver {delta_pos}")
print("Da intervallet indeholder 0 kan vi ikke sige at der er en signifikant forskel mellem de 2 modeller")