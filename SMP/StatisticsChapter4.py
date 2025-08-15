import scipy.stats as stats

### Problem 1

gamma = 10 # Number of cars claim pr. hr.
t = 4
mu = gamma*t

# a: What is the probability that more than 45 cars will pass the traffic light

k = 45
PMoreThan45 = 1-stats.poisson.cdf(k,mu)
print("More than 45:",PMoreThan45)

# b: What is the probability that less than 38 cars will pass the traffic light
k = 38
PLessThan38 = stats.poisson.cdf(k,mu)
print("Less than 38:",PLessThan38)

# c: What is the probability that exactly 45 cars will pass the  traffic light
k = 45
PExactly45 = stats.poisson.pmf(k,mu)
print("Exactly 45:", PExactly45)

### Problem 2



### Problem 3
x = 45
t = 4

# a:
Elambda = x/t

# b: 
# H0 gamma = 10
# H1 gamma != 10
lambda_ = 10


# c:
z = (x-t*lambda_)/((lambda_*t) ** 0.5)
print("z value:" , z)

ApproxPValue = 2*(1-stats.norm.cdf(abs(z)))
print("approximate p value:", ApproxPValue)
print("We fail to reject the null hypothesis")

