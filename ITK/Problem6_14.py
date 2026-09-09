import matplotlib.pyplot as plt
import numpy as np

p1 = np.array([1,0,0,0,1,0,0,1,1,0,1,0,1,1,1])
p2 = np.array([1,0,0,0,1,1,1,1,0,1,0,1,1,0,0])

# map binary to bipolar: 0 → -1, 1 → +1
p1_bip = 2 * p1 - 1
p2_bip = 2 * p2 - 1

auto  = np.correlate(p1_bip, p1_bip, mode='full')
cross = np.correlate(p1_bip, p2_bip, mode='full')
lags  = np.arange(-(len(p1_bip)-1), len(p1_bip))

#plot the auto and cross correlation functions

plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.stem(lags, auto)
plt.title('Auto-correlation of p1')
plt.xlabel('Lag')
plt.ylabel('Correlation')
plt.subplot(2, 1, 2)
plt.stem(lags, cross)
plt.title('Cross-correlation of p1 and p2')
plt.xlabel('Lag')
plt.ylabel('Correlation')
plt.tight_layout()
plt.show()