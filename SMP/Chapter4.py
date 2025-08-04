import math
# Chapter 4.4
# Problem 2

# a: 
c=4
def g(x):
    if x >= 0:
        return c*math.e**(-c*x)
    else:
        return 0
    
# b:
def u(x):
    if x < 0:
        return 0
    else:
        return 1

def f(x):
    return (1-math.e**(-c*x)) *u(x)

# print cdf
for i in range(-2, 5):
    print(f"F({i}) = {f(i)}")
    
# c:
#integral


print("Sandsynlighed for at få 3 eller 4")
print(g(3)+g(4))