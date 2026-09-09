from scipy import stats

### Opgave 4
n  = 1200
x = 1177
p = x/n
p0 = 0.988

z = (x-n*p0)/((n*p0*(1-p0))**0.5)
print("z værdien er:",z)
p2 = 1 - stats.norm.cdf(z)
print("p værdien er:",p)
if p2 > 0.05:
    print("We fail to reject the null hypothesis")
else:
    print("We reject the null hypothesis")
    
# e: Beregn 95% konfidens intervallet
p_lower = (x+(1.96**2/2)-1.96*((((x*(n-x))/n)+(1.96**2)/4)**0.5)) / (n + 1.96**2)
p_upper = (x+(1.96**2/2)+1.96*((((x*(n-x))/n)+(1.96**2)/4)**0.5)) / (n + 1.96**2)
print(f"95% konfidensintervallet for succesraten går fra {p_lower} til {p_upper}")
if p_lower <= p <= p_upper:
    print("We accept the null hypothesis")
else:
    print("We reject the null hypothesis")

