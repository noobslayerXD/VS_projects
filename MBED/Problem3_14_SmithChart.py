import numpy as np
import matplotlib.pyplot as plt

from pysmithchart import S_PARAMETER





# Source circle
# center of source circle
C_S = -1.184 + 2.354j
# radius of source circle
R_S = 1.963

# Load circle
# center of load circle
C_L = 1.044 + 0.925j
# radius of load circle
R_L = 0.576

# plot load circle in smith chart
plt.figure(figsize=(6, 6))
params = {
    "grid_major_color": "blue",
    "grid_minor_color": "lightblue",
    "grid_major_linewidth": 0.8,
    "grid_minor_linewidth": 0.5,
    "grid_minor_linestyle": "--",
    "grid_minor_enable": True,
    "grid_minor_fancy": True,
    "grid_major_fancy": True,
}
plt.subplot(1, 1, 1, projection="smith", **params)
plt.gca().add_artist(plt.Circle((C_S.real, C_S.imag), R_S, color="red", fill=False, lw=2))
plt.gca().add_artist(plt.Circle((C_L.real, C_L.imag), R_L, color="green", fill=False, lw=2))
plt.text(C_S.real + R_S + 0.1, C_S.imag, "  Source Circle", color="red", fontsize=12)
plt.text(C_L.real + R_L + 0.1, C_L.imag, "  Load Circle", color="green", fontsize=12)
plt.show()