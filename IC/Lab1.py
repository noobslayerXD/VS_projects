import matplotlib.pyplot as plt
import numpy as np

# import csv file
data = np.genfromtxt('Testmålinger_Lab1.csv', delimiter=',', skip_header=1)

# PLot coloum 1 vs coloum 2, as ic vs VCE
plt.plot(data[:, 0], (data[:, 1]/100)*1000)
plt.xlabel('VCE (V)')
plt.ylabel('IC (mA)')
plt.title('IC vs VCE')
plt.grid()


# Nu for en PNP istedet for ncp
data2 = np.genfromtxt('TestPNP.csv', delimiter=',', skip_header=1)

# PLot coloum 1 vs coloum 2, as ic vs VCE
plt.plot(abs(data2[:, 0]), abs((data2[:, 1]/100)*1000))
plt.xlabel('VCE (V)')
plt.ylabel('IC (mA)')
plt.title('IC vs VCE for PNP')
plt.grid()
plt.show()