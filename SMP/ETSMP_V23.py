import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy.special import comb

# region Opgave 1

P_F = 0.11
P_nF = 1 - P_F

P_T_givet_F = 0.7
P_nT_givet_F = 1 - P_T_givet_F

P_T_givet_nF = 0.31
P_nT_givet_nF = 1 - P_T_givet_nF

## a:
n = 50
P_AF_eq_0 = comb(n,0)*(P_F**0)*P_nF**50 
P_AF_eq_1 = comb(n,1)*(P_F**1)*P_nF**49

P_A = 1- (P_AF_eq_0+P_AF_eq_1)
print("Sandsynligheden for at finde 2 eller flere biler med fejl:",P_A)

## b: find P_T
P_T = P_T_givet_F * P_F + P_T_givet_nF * P_nF
print("Den totale sandsynlighed for at testen finder en fejl:", P_T)
P_nT = 1 - P_T
## c: Find den betingede sandsynlighed for, at der er en fejl på en bil, givet at software-testen ikke finder fejl
P_F_givet_nT = (P_nT_givet_F*P_F)/P_nT
print("Sandsynligheden for at testen siger der ikke er en fejl, men der er en:",P_F_givet_nT)
P_nF_givet_nT = 1- P_F_givet_nT

Antal_biler_med_fejl = P_F*n
print("Det estimerede antal biler med fejl:",Antal_biler_med_fejl)

# endregion

# region Opgave 2

# a:
def f_x(x):
    if x == 10:
        return 1/4
    elif x == 20:
        return 3/20
    elif x == 50:
        return 3/5
    else:
        return 0

x_vals = np.arange(0, 51, 1)
y_vals = [f_x(x) for x in x_vals]

plt.stem(x_vals, y_vals)
plt.xlabel('x')
plt.ylabel('$f_x(x)$')
plt.title('Plot af $f_x(x)$')
plt.show()

# b: Bestem middelværdien(EX) af X
EX = 10*(1/4)+20*(3/20)+50*(3/5)
print("Middelværdien af f_x er:",EX)

# c: Opstil udtryk og beregn korrelationen mellem X og Y
def f_y(y):
    if y == 0:
        return 13/20
    elif y == 1:
        return 7/20
    else:
        return 0


EXY = 10* 1 * 4/20 + 20 *1 * 1/20 + 50*1*2/20
print("Korrelation mellem X og Y:", EXY)

# d: 
f_XY_20_0 = 1/20 + 2/20
print("Fordelingsfunktionen for f_XY(20,0) er:",f_XY_20_0)
# endregion

# region Opgave 3

# a: Plot 3 realiseringer af X[n] hvor der medtages 10 samples af hver realisation.
n = 10
for i in range(3):
    y = np.random.normal(-50, 3, n)
    X = y + (-1)**n
    plt.plot(range(n), X, label=f'Realisering {i+1}')
plt.xlabel('n')
plt.ylabel('X[n]')
plt.title('3 realiseringer af X[n]')
plt.legend()
plt.show()

# b: Find, med visning af mellemregninger, ensemble mean og ensemble variansen
# X består af to led y og -1**n
# mean af y er givet
y_mean = 50
# siden -1**n, kun kan være -1 eller 1, så må mean afhænger af antallet af samples
if n % 2 == 0:
    neg1_mean = 1
elif n % 2 == 1:
    neg_1_mean = -1
x_mean = y_mean + neg1_mean
# x_mean er enten -49 eller -51

# Ensemble variansen
y_var = 9 # givet fra opgaven
neg1_var = neg1_mean**2
# dette giver altid 1, da -1^2=! og 1^2=1
neg1_var = 1
x_var = y_var + neg1_var
print("Ensemble variansen af x er:", x_var)

# c: angiv om X[n] er WSS og ergodisk, begrund svaret
# for at den er WSS kræves to ting
# ensemble middelværdien er konstant, dette er ikke sandt i vores tilfælde da den afhænger på om der er et lige eller ulige antal samples
# Det andet der skal gælde er at autokorrelationen kun skal afhænge af tidsforskydningen, dette er sandt i vores tilfælde da variansen er konstant
# Den er ikke WSS og kan derfor heller ikke være ergodisk

# endregion

# region Opgave 4
mu0 = 25
std_div = 1.5
t = [24.2, 27.47, 28.56, 26.67, 23.74, 23.68, 24.28, 26.85, 25.07, 27.06]
n = len(t)
# a:
# Den test statistik vi skal bruge er den for kendt varians, hvor man vil finde mean(z-test)

# b: opstil null hypotese og alternativ hypotese
# H0: mu = mu0
# H1: mu != mu0

# c: Beregn p værdien for testen, kan vi afvise nulhypotesen med et signifikansniveau på 5%
# først findes middelværdien
mu = sum(t)/n
x_hat = np.mean(t)
print("middelværdien er:",mu,"Med indbygget funktion:",x_hat) # to forskellige måder at finde mean på
# Så findes z
z = (x_hat-mu0)/(std_div/(n**0.5))
print("z value:",z)
# Nu kan p findes
p = 2*(1-stats.norm.cdf(abs(z)))

# kan vi afvise null hypotesen?
if p> 0.05:
    print("We fail to reject the null hypothesis")
elif p< 0.05:
    print("We can reject the NULL hypothesis")

print("The p value is:",p)

# d: beregn 90% konfidensintervallet
z_0 = stats.norm.ppf(1-0.05) # da det er 90% konfidens intervallet skal det være 0.05 i stedet for 0.025
mu_neg = x_hat - z_0 *std_div/(n**0.5)
mu_pos = x_hat + z_0 *std_div/(n**0.5)
print(f"the 90% confidence interval is from {mu_neg} to {mu_pos}")

# e: Hvor mange målinger skal til for at 95% konfidens intervallet er 0.1 fra 25
conf_pos = []
conf_neg = []

for i in range (10000):
    conf_pos.append(x_hat + z_0 *std_div/((i+1)**0.5))
    conf_neg.append(x_hat - z_0 *std_div/((i+1)**0.5))
    if conf_pos[i]-conf_neg[i]<0.2:
        print("Antal samples needed:",i-1,"Dette er åbenbart ikke rigtigt")
        break

B = 0.1
needed_samples = ((1.96*std_div)/B)**2
print("the minimum needed samples:",needed_samples)
    
# f: nu antager vi at middelværdien er rigtig på 25 
tid_cdf = stats.norm.cdf(26,scale=std_div,loc=25)
print("Sandsyligheden for at det tager 26 sekunder eller mere:",1-tid_cdf)




# endregion