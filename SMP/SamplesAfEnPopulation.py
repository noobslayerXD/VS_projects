import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

mean = 7
variance = 2
std_div = 2 ** 0.5
n = 100

# 1: Er Samples fra X statistisk uafhænginge
## Siden det er i.i.d så ja

# 2: generer og plot data fra et sample
X = np.random.normal(mean,std_div,n)

# plot the histogram
plt.hist(X, bins=20, density=True, alpha=0.6)
plt.show()

# 3: Hvad er populationen i dette tilfælde?


# 4: Beregn sample middelværdien v.hj.a. formlem for denne
sample_mean = np.mean(X)
print("Sample Mean:", sample_mean)

# 5: Beregn sample variansen v.hj.a. formlen for denne
sample_var = np.var(X)
print("Sample Variance:", sample_var)

# 6: find z-scoren for dataene i samplet. Hvad fortæller z scoren?
z = (sample_mean- mean)/(variance/(n ** 0.5))
print("Z-score:",z)
print("Z scoren er meget tæt på 0 så det bare dejlig")

# 7: find 95% confidens interval
mu_neg = mean - 1.96 * std_div/(n**0.5)
mu_pos = mean + 1.96 * std_div/(n**0.5)
print("95% Confidence Interval:", (mu_neg, mu_pos))

# 8: Indtegn kofidens intervallet på plottet i spørgsmål 2, hvad fortæller konfidens intervallet
# 95% samples middelværdi ligger indefor intervallet
plt.hist(X, bins=20, density=True, alpha=0.6)
plt.axvline(mu_neg, color='red', linestyle='dashed', linewidth=1)
plt.axvline(mu_pos, color='red', linestyle='dashed', linewidth=1)
plt.show()

# 9: hvor stor en sample-størrelse er nødvendig, hvis du vil have et konfidens-interval, der er mindre end 0.5 bred(B=0.25)
B = 0.25
needed_samples = round((1.96*std_div/B) ** 2,0)
print("minimum needed samples for small interval:", needed_samples)

# 10: lav 1000 samples af test data, beregn sample middelværdien for hver og lav et histogram af sample middelværdierne. Hvilken fordeling har sample middelværdierne
repeats = 1000
sample_means = []
for _ in range(repeats):
    X_ny = np.random.normal(mean,std_div,n)
    sample_means.append(np.mean(X_ny))
plt.hist(sample_means, bins=20, density=True, alpha=0.6)
plt.show()


# 11: Hvilken fordeling vil middelværdierne have hvis det var uniform fordelt

sample_means = []
for _ in range(repeats):
    X_ny = np.random.uniform(5, 9,n)
    sample_means.append(np.mean(X_ny))
plt.hist(sample_means, bins=20, density=True, alpha=0.6)
plt.show()
