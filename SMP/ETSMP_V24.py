import matplotlib.pyplot as plt
import numpy as np
from scipy import stats

## Opgave 1
N = 48 # antal kort
N1 = 36
N2 = 9
N3 = 3

# a
P_1 = 1/(N1+N2*1/2+N3*1/3)
P_2 = P_1/2
P_3 = P_1/3

# print sandsynligheder for et kort med 1 stjerne, 2 stjerner og 3 stjerner
print("P(1 stjerne):", P_1)
print("P(2 stjerner):", P_2)
print("P(3 stjerner):", P_3)


# b
P_z2 = N2*P_2
P_z3 = N3*P_3
P_z3_given_zleast2 = P_z3/(P_z3+P_z2) # bayes regel
print("sandsynligheden for at trække et 3 stjernet kort givet kortet har mindst 2 stjerner:",P_z3_given_zleast2)

# c
# De er ikke uafhængige da man fjerner alle 1 stjernet kort så bliver sandsynligheden større for at trække et 3 stjernet
print(P_z2 + P_z3 == 1)
print(P_z3 ==(P_z2+P_z3)*P_z3)
# da sandsynlighederne ikke er ens betyder det at de ikke er uafhængige

 

## Opgave 2

# Define the function values
# a
a = 0.2
x = np.arange(-3, 4)  # covers x = -3, -2, -1, 0, 1, 2, 3

def f_X(x):
    if x == 0:
        return a * 2
    elif abs(x) == 1:
        return a * 1
    elif abs(x) == 2:
        return a * 0.5
    else:
        return 0

y = [f_X(val) for val in x]

plt.stem(x, y)
plt.xlabel('x')
plt.ylabel('$f_X(x)$')
plt.title('Plot of $f_X(x)$ with $a=0.2$')
plt.show()

# b
cdf = np.cumsum(y)
print(cdf)

plt.step(x, cdf,where='post')
plt.xlabel('x')
plt.ylabel('CDF')
plt.title('CDF of $f_X(x)$ with $a=0.2$')
plt.show()

# c: Beregn forventningsværdien (mean) og varians
mean = np.sum(x * y)
variance = np.sum((x - mean)**2 * y)
print("Forventningsværdi (mean) af X:", mean)
print("Varians af X:", variance)

## Opgave 3
# a:
N = 11
n = np.arange(0, N)
MC = 3

for i in range(MC):
    z = np.random.rand(N)*2+3
    print(z)
    w = stats.norm.rvs(1,2**0.5,size=N)
    print(w)
    y = z + 3 * w
    plt.plot(n, y, label=f'y_{i+1}')

plt.grid(True)
plt.title("3 realisationer af Y'")
plt.xlabel('n')
plt.ylabel('y')
plt.legend()
plt.show()

## Opgave 4
first = [6.4, 9.9, 7.5, 8.6, 1.2, 5.6, 9.3, 7.0, 8.8, 2.9]
second = [8.7, 9.4, 9.1, 6.3, 6.1, 8.4, 9.2, 8.6, 8.4, 4.7]
n = len(first)

# c: 

diff = []
for i in range(n):
    diff.append(second[i] - first[i]) 
diff_est = np.mean(diff)

print("den gennemsnitlige forskel er:",diff_est)


# d: 
var_arr = []

for i in range(n):
    var_arr.append((diff[i]-diff_est)**2)
var = sum(var_arr)/(n-1)
print("Den estimerede varians af den observerede forskel:",var)

# e:
# null hypotesen er at delta0 er 0

t = diff_est/(var**0.5/n**0.5)
print("t-value is:",t)

p = 2 * (1 - stats.t.cdf(abs(t),n-1))
print("P value is:",p)

if p>0.05:
    print("We fail to reject the null hypothesis")
else:
    print("We reject the null hypothesis")

# f: bestem 95% konfidens intervallet
t_0 = stats.t.ppf(1-0.05/2,n-1)

delta_neg = diff_est - t_0 * var**0.5/n **0.5
delta_pos = diff_est + t_0 * var**0.5/n **0.5

print(f"95% konfidens intervallet går fra {delta_neg} til {delta_pos}")