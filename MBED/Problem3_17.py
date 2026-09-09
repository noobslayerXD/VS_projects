import matplotlib.pyplot as plt

S = [[-1.626-1.626j, 0], 
     [2+3.464j, 0.4-0.693j]]
print(S)

# Source circle
# center of source circle
C_S = 0.286 - 0.286j
# radius of source circle
R_S = 0.24

Gamma_S = 0.307+0.307j


# plot load circle in smith chart
plt.figure(figsize=(6, 6))
params = {
    "grid_minor_enable": True,
    "grid_minor_fancy": True,
    "grid_major_fancy": True,
}
plt.subplot(1, 1, 1, projection="smith", **params)
plt.gca().add_artist(plt.Circle((C_S.real, C_S.imag), R_S, color="red", fill=False, lw=2))
plt.plot(Gamma_S, "b-o", markersize=10) 
plt.text(C_S.real + R_S + 0.1, C_S.imag, "  Source Circle", color="red", fontsize=12)
plt.show()