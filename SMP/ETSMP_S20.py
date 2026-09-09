from scipy import stats

### Opgave 4: Statistik
n = 10000
n_fejl = 178
n_rigtig = n - n_fejl
p_success_spec = 0.985

## a:
p_success = n_rigtig/n
print("Estimeret successrate:",p_success)

## b:
# Det er en binoial fordeling fordi der kun er to forskellige udkom

## c: Hvad er det forventede antal korrekt modtagne bits og standard afvigelsen af disse
forventede_antal_korrekte_bits = p_success_spec*n
var = n*p_success_spec*(1-p_success_spec)
print(var)

std_div = var ** 0.5
print(std_div)

## d: Opstil en nulhypotese og en alternativ hypotese for testen
# H0: p_success = p_success_spec
# H1: p_success != p_success_spec

## e: Beregn p-værdien. Kan nul-hypotesen afvises med et signifikansniveau på 5%
z = (n_rigtig-n*p_success_spec)/(n * p_success_spec * (1-p_success_spec)) ** 0.5
print("z:",z)
p = 2* abs(1-stats.norm.cdf(abs(z)))
print("p:",p)

if (p>0.05):
    print("We cannot reject the null hypothesis")
else:
    print("We can reject the null hypothesis")
    
## f: Bestem 95% konfidensintervallet for transmissionsledningens succesrate. hvad fortæller det beregnede konfidensinterval

p_neg = 1/(n+1.96 ** 2)*(n_rigtig + 1.96 ** 2 / 2 - 1.96 * (n_rigtig * ((1 - p_success_spec) / n)+(1.96**2)/4) ** 0.5)
p_pos = 1/(n+1.96 ** 2)*(n_rigtig + 1.96 ** 2 / 2 + 1.96 * (n_rigtig * ((1 - p_success_spec) / n)+(1.96**2)/4) ** 0.5)
# confidensinterval
print(f"95% konfidensinterval: ({p_neg}, {p_pos})")