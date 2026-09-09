import matplotlib.pyplot as plt
import numpy as np

# Load line;
Rc = 2.2*10**3 
VCC = 1.5
VCE = np.arange(0, 1.5, 0.1) 
Ic = (-1/Rc) * VCE + (VCC/Rc)


plt.plot(VCE, Ic*10**3, linewidth=2)  
plt.grid(True)
plt.xlabel('VCE [V]')
plt.ylabel('Ic [mA]')
plt.title('Load Line')
plt.show()

