import numpy as np
import scipy.stats as stats
import seaborn as sns
import matplotlib.pyplot as plt
import random

### Problem 1 : sandsynlighedsteori
# En software udvikler  tester et spamfilter til filtrering af uønskede mails



### Problem 2



### Problem 3
n = 10
T = 22 # er en konstant temperatur
p = 0.8
# generate samples
# Fejlfinding W = np.random.normal(0, 1, n)
# Fejlfinding print("W:",W)
# Fejlfinding A = stats.bernoulli.rvs(p,0,n) 
# Fejlfinding print("A:",A)
# X er WSS, X[n] og X[n+tau] er uafhængige
# Fejlfinding X = A * (T + W)
# Fejlfinding print("X:",X)


## a: Plot 3 realiseringer af X[n] hvor der medtages 10 samples af hver realisation.
for i in range(3):
    W = np.random.normal(0, 1, n)
    A = stats.bernoulli.rvs(p, 0, n)
    X = A * (T + W)
    plt.plot(range(n), X, label=f'Realisering {i+1}')
plt.xlabel('n')
plt.ylabel('X[n]')
plt.title('3 realiseringer af X[n]')
plt.legend()
plt.show()

## b: beregn ensemble midedlværdi E[X[N]] af processen X[n]
# mathcad


### Problem 4

x = np.array([0, 2, 4, 6, 8, 10, 12, 14, 16, 18]) # antal timer
y = np.array([210, 220, 230, 245, 250, 270, 275, 290 , 310, 330]) # reaktionstid

## a: lav et plot af målingerne
plt.scatter(x,y)
plt.show()

## b: angiv den lineære regressionsmodel til beskrivelse af målepunkterne. Forklar betydningen af parametrene i modellen
res = stats.linregress(x,y)
# print(res)

# alfa + beta*x + epsilon er den lineære regressions model der bliver brugt, epsilon er residualerne og de antages at være normalfordelt

## c: estimer alfa og beta, samt plot den
print("alfa:",res.intercept)
print("beta:",res.slope)

plt.plot(x, y, 'o', label='original data')
plt.plot(x, res.intercept + res.slope * x, 'r', label='fitted line')
plt.legend()
plt.show()

## d: Brug modellen til at forudsige reaktionstiden ved 15 timers søvnmangel. Kan modellen også brugtes til at forudsige reaktisntiden ved 24 timers søvnmangel
# den kan ikke bruges til 24 timers søvn da der så kan opstå extrapolation
y_pred = res.intercept + res.slope * 15
print("Forudsigelser:", y_pred)

## e: formuler hypotesetest for hældningen beta til test af sammenhængen mellem søvn og reaktionstid, og forklar valget af hyportese
# nulhypotesen vil vise om der er en lineær sammenhæng mellem søvnmangel og reaktionstid
# nulhypotesen bliver det modsatte: H0:beta_0=0

## f: undersøg om hypotesen kan afvises ved 5% signifikans niveau, og forklar hvad testen fortæller om den lineære model
beta0 = 0

t = (res.slope-beta0)/ (res.stderr*(1/sum((x - np.mean(x))**2)**0.5))
print("t:",t)
# Find test size
alpha = 0.05
df = len(x) - 2
t_0 = stats.t.ppf(1-alpha/2, df)

# approximate p value
p = 2*(1-stats.t.cdf(abs(t),n-2))
if (p>alpha):
    print("We fail to reject the null hypothesis")
else:
    print("We reject the null hypothesis")

print("the p value:",p)
print("the test shows that beta isnt close to zero, which means that there is a linear correlation between driving hours and reactiontime")