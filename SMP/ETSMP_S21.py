import numpy as np
import scipy.stats as stats

### Opgave 1



### Opgave 2



### Opgave 3



### Opgave 4


# a: 
# poisson fordeling fordi det er et antal over tid
lambda_ = 25
# b: Hvad er den estimerede rate for antal biler pr. minut ved tællingen
antal_biler = np.array([160, 142, 118, 155, 100 ,127, 93, 163, 136, 169, 102, 109])
antal_minutter = 60
måletid = 5
sum_af_biler = sum(antal_biler)
estimate_biler_pr_minut = sum_af_biler/antal_minutter
print("Estimat af antal biler pr minut ved tællingen:",estimate_biler_pr_minut)

# c: Opstil en hypotese
# H0 estimate_biler_pr_minut = lambda_ 
# H1 estimate_biler_pr_minut != lambda_ 

# d: Beregn p-værdien for testen, begrund den anvente test-statistik til beregningen
gamma = måletid* lambda_
print("gamma:",gamma) 
z = (estimate_biler_pr_minut*5 - lambda_*5)/((lambda_*5) ** 0.5)
print("z:",z)

p = 2*abs(1-stats.norm.cdf(abs(z)))
print("approximate p value:", p)
print("jeg har valgt two tailed fordi der kan både være flere og færre biler end dette")
# e: bestem 95% konfidens intervallet for det forventede antal biler pr. minut på baggrund af tællingerne
t = 5
x = estimate_biler_pr_minut*t
lambdaPos = 1/t * (((x + ((1.96 ** 2))/2))+1.96*(x + (1.96**2)/4)**0.5)
print("lambda Positiv:",lambdaPos)

lambdaNeg = 1/t * (((x + ((1.96 ** 2))/2))-1.96*(x + (1.96**2)/4)**0.5)
print("lambda Negativ:",lambdaNeg)

# f: Er der ifølge testen statistisk evidens for med 5% signifikansniveau at indstille trafiklyset til 25 biler pr. minut?
if p > 0.05:
    print("Der er statistisk evidens for at indstille trafiklyset til 25 biler pr. minut.")
else:
    print("Der er ikke statistisk evidens for at indstille trafiklyset til 25 biler pr. minut.")
    
print("Konfidensintervallet for det forventede antal biler pr. minut er fra", lambdaNeg, "til", lambdaPos, "og den forventede værdi er derimellem")