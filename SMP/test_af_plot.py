import matplotlib.pyplot as plt
import numpy as np

N = 11
n = np.arange(0, N-1)   # svarer til 0:N-2 i MATLAB
MC = 3

for nn in range(MC):
    y = np.random.randint(1, 4, size=N) - 2   # giver -1,0,1
    x = y[:-1] + 2 * y[1:]                   # længde N-1
    plt.plot(n, x, 'x-', label=f'x_{nn+1}')

plt.grid(True)
plt.title("3 realisationer af X'")
plt.xlabel('n')
plt.ylabel('x')
plt.legend()
plt.show()
