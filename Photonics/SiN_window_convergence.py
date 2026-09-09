"""Window convergence of a 200 nm x 800 nm SiN waveguide at 1550 nm."""

import csv
from pathlib import Path

import emodeconnection as emc
import matplotlib.pyplot as plt
import numpy as np

# Simulation settings
wavelength_nm = 1550.0
core_width_nm = 200.0
core_height_nm = 800.0
mesh_nm = 10.0
padding_values_nm = [1500.0, 2500.0, 3500.0, 5000.0, 7000.0]
number_of_modes = 4

output_folder = Path("window_convergence_200nm_1550nm")
output_folder.mkdir(exist_ok=True)


# Refractive-index models
def n_sin_luke(wavelength_um):
    n_squared = (
        1.0
        + 3.0249 / (1.0 - (0.135341 / wavelength_um) ** 2)
        + 40314.0 / (1.0 - (1239.84 / wavelength_um) ** 2)
    )
    return np.sqrt(n_squared)


def n_sio2_malitson(wavelength_um):
    n_squared = (
        1.0
        + 0.696166 / (1.0 - (0.0684043 / wavelength_um) ** 2)
        + 0.407943 / (1.0 - (0.116241 / wavelength_um) ** 2)
        + 0.897479 / (1.0 - (9.89616 / wavelength_um) ** 2)
    )
    return np.sqrt(n_squared)


wavelength_um = wavelength_nm / 1000.0
n_sin = float(n_sin_luke(wavelength_um))
n_sio2 = float(n_sio2_malitson(wavelength_um))

print(f"n(SiN)  = {n_sin:.6f}")
print(f"n(SiO2) = {n_sio2:.6f}")


def select_fundamental_te_mode(effective_index, te_fraction):
    """Return the highest-index mode with TE fraction above 50%."""

    effective_index = np.asarray(effective_index, dtype=float).ravel()
    te_fraction = np.asarray(te_fraction, dtype=float).ravel()

    # EMode versions may report TE fraction either from 0 to 1 or from 0 to 100.
    if np.max(te_fraction) > 1.5:
        te_fraction = te_fraction / 100.0

    te_modes = np.where(te_fraction > 0.5)[0]
    if len(te_modes) == 0:
        raise RuntimeError("No TE-like mode was found.")

    return int(te_modes[np.argmax(effective_index[te_modes])])


def solve_waveguide(padding_nm):
    """Solve the same waveguide using one value of SiO2 padding."""

    window_width_nm = core_width_nm + 2.0 * padding_nm
    window_height_nm = core_height_nm + 2.0 * padding_nm

    run_name = f"padding_{int(padding_nm)}nm"
    run_folder = output_folder / run_name
    run_folder.mkdir(exist_ok=True)

    em = emc.EMode(simulation_name=run_name, save_path=str(run_folder))

    em.add_material(
        name="SiN",
        refractive_index_equation=f"{n_sin:.10f}",
        wavelength_unit="um",
    )
    em.add_material(
        name="SiO2",
        refractive_index_equation=f"{n_sio2:.10f}",
        wavelength_unit="um",
    )

    em.settings(
        wavelength=wavelength_nm,
        x_resolution=mesh_nm,
        y_resolution=mesh_nm,
        window_width=window_width_nm,
        window_height=window_height_nm,
        num_modes=number_of_modes,
        background_material="SiO2",
        boundary_condition="00",
        max_effective_index=n_sin + 0.05,
    )

    # The lower-left corner of the simulation window is y = 0.
    core_centre_y_nm = padding_nm + core_height_nm / 2.0

    em.shape(
        name="SiN_core",
        material="SiN",
        width=core_width_nm,
        height=core_height_nm,
        position=[0.0, core_centre_y_nm],
    )

    em.FDM()
    em.effective_area()

    effective_index = np.asarray(em.get("effective_index"), dtype=float).ravel()
    te_fraction = np.asarray(em.get("TE_fraction"), dtype=float).ravel()
    effective_area = np.asarray(em.get("effective_area"), dtype=float).ravel()

    mode_index = select_fundamental_te_mode(effective_index, te_fraction)

    result = {
        "padding_nm": padding_nm,
        "window_width_nm": window_width_nm,
        "window_height_nm": window_height_nm,
        "mode_index": mode_index,
        "n_eff": effective_index[mode_index],
        "n_eff_minus_n_clad": effective_index[mode_index] - n_sio2,
        "TE_fraction": te_fraction[mode_index],
        "A_eff_um2": effective_area[mode_index],
    }

    try:
        em.close(save=True, save_all_fields=False)
    except TypeError:
        em.close()

    return result


# Repeat the calculation while increasing the surrounding SiO2 region.
results = []

for padding_nm in padding_values_nm:
    print(f"\nRunning padding = {padding_nm:.0f} nm")
    result = solve_waveguide(padding_nm)
    results.append(result)
    print(
        f"n_eff = {result['n_eff']:.9f}, "
        f"A_eff = {result['A_eff_um2']:.4f} um^2"
    )


# Save the numerical results.
csv_path = output_folder / "window_convergence.csv"
with csv_path.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=results[0].keys())
    writer.writeheader()
    writer.writerows(results)


# Compare each calculation with the largest simulated window.
padding = np.array([row["padding_nm"] for row in results])
n_eff = np.array([row["n_eff"] for row in results])
a_eff = np.array([row["A_eff_um2"] for row in results])

n_eff_reference = n_eff[-1]
n_eff_error = np.abs(n_eff - n_eff_reference)

fig, axes = plt.subplots(1, 3, figsize=(15, 4.2), constrained_layout=True)

axes[0].plot(padding, n_eff, "o-")
axes[0].set_xlabel("SiO2 padding on each side [nm]")
axes[0].set_ylabel(r"$n_\mathrm{eff}$")
axes[0].set_title("Effective index")

nonzero_error = n_eff_error > 0
axes[1].plot(padding[nonzero_error], n_eff_error[nonzero_error], "o-")
axes[1].set_yscale("log")
axes[1].set_xlabel("SiO2 padding on each side [nm]")
axes[1].set_ylabel(r"$|n_\mathrm{eff}-n_\mathrm{eff,ref}|$")
axes[1].set_title("Error relative to largest window")

axes[2].plot(padding, a_eff, "o-")
axes[2].set_xlabel("SiO2 padding on each side [nm]")
axes[2].set_ylabel(r"$A_\mathrm{eff}$ [$\mu$m$^2$]")
axes[2].set_title("Effective area")

for axis in axes:
    axis.grid(True, alpha=0.3)

figure_path = output_folder / "window_convergence.png"
fig.savefig(figure_path, dpi=250)
plt.show()

print(f"\nResults saved in: {output_folder.resolve()}")

