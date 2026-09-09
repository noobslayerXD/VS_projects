# calculate the cosine integral of 2 pi
import numpy as np
from scipy.integrate import quad


def integrand(x):
    return (1-np.cos(x)) / x

# Use a small epsilon to avoid singularity at x=0
epsilon = 1e-30
result, error = quad(integrand, epsilon,  np.pi)
print("Cosine Integral of 2π:", result)
print("Error estimate:", error)