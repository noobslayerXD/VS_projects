import numpy as np
import matplotlib.pyplot as plt

# %% Load line;
Rc = 2.2*10**3 
VCC = 1.5
VCE = np.arange(0, 1.5, 0.1)  # 0:0.1:15 in MATLAB becomes np.arange(0, 15.1, 0.1)
Ic = (-1/Rc) * VCE + (VCC/Rc)
plt.plot(VCE, Ic*10**3, linewidth=2)  # Ic*10^3 becomes Ic*10**3, linewidth instead of 'linewidth'
plt.grid(True)
plt.xlabel('VCE [V]')
plt.ylabel('Ic [mA]')
plt.title('Load Line')
plt.show()
# %%
