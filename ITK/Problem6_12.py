import matplotlib.pyplot as plt
import numpy as np

W3 = np.array([0, 1, 1, 0, 0, 1, 1, 0])
W7 = np.array([0, 1, 1, 0, 1, 0, 0, 1])

# Map binary to bipolar: 0 → -1, 1 → +1
W3_bip = 2 * W3 - 1
W7_bip = 2 * W7 - 1

cross = np.correlate(W3_bip, W7_bip, mode='full')
lags = np.arange(-(len(W3) - 1), len(W3))

plt.stem(lags, cross)
plt.title('Cross-correlation of W3 and W7 (bipolar)')
plt.xlabel('tau')
plt.ylabel('Correlation')
plt.axhline(0, color='gray', linewidth=0.8)
plt.show()