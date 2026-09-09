"""Modes of a buried 1000 nm x 800 nm SiN waveguide at 930 and 1550 nm."""

import csv
import time
from pathlib import Path

import emodeconnection as emc
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

# Waveguide and solver settings
wavelengths_nm = [930.0, 1550.0]

core_width_nm = 1000.0
core_height_nm = 800.0

side_cladding_nm = 2500.0
top_cladding_nm = 2500.0
bottom_cladding_nm = 2500.0

mesh_nm = 10.0
number_of_modes = {930: 10, 1550: 10}
boundary_condition = "00"

output_folder = Path("SiN_modes_1000x800")
output_folder.mkdir(exist_ok=True)


# Refractive-index models #Sellmeier equations
#  
def n_sin_luke(wavelength_um):
    n_squared = (
        1.0
        + 3.0249 / (1.0 - (0.135341 / wavelength_um) ** 2)
        + 40314.0 / (1.0 - (1239.84 / wavelength_um) ** 2)
    )
    return float(np.sqrt(n_squared))


def n_sio2_malitson(wavelength_um):
    n_squared = (
        1.0
        + 0.696166 / (1.0 - (0.0684043 / wavelength_um) ** 2)
        + 0.407943 / (1.0 - (0.116241 / wavelength_um) ** 2)
        + 0.897479 / (1.0 - (9.89616 / wavelength_um) ** 2)
    )
    return float(np.sqrt(n_squared))


def as_1d(values):
    return np.asarray(values, dtype=float).ravel() 


def normalise_te_fraction(te_fraction):
    """Return TE fraction on a scale from 0 to 1."""

    te_fraction = as_1d(te_fraction)
    if np.max(te_fraction) > 1.5:
        te_fraction = te_fraction / 100.0
    return te_fraction


def select_mode(field_array, mode_index, modes_found):
    """Extract one mode from the array returned by EMode."""

    field_array = np.asarray(field_array) #field_array.shape = (10, 400, 500)

    if field_array.ndim == 2:
        return field_array

    if field_array.ndim == 3:
        if field_array.shape[0] == modes_found:
            return field_array[mode_index, :, :]
        if field_array.shape[-1] == modes_found:
            return field_array[:, :, mode_index]

    if field_array.ndim == 4:
        if field_array.shape[0] == 1 and field_array.shape[1] == modes_found:
            return field_array[0, mode_index, :, :]
        if field_array.shape[0] == modes_found and field_array.shape[1] == 1:
            return field_array[mode_index, 0, :, :]
        if field_array.shape[0] == 1 and field_array.shape[-1] == modes_found:
            return field_array[0, :, :, mode_index]

    raise ValueError(f"Unexpected field-array shape: {field_array.shape}")


def solve_at_wavelength(wavelength_nm):
    """Build the waveguide and calculate its modes at one wavelength."""

    wavelength_um = wavelength_nm / 1000.0
    n_sin = n_sin_luke(wavelength_um)
    n_sio2 = n_sio2_malitson(wavelength_um)

    window_width_nm = core_width_nm + 2.0 * side_cladding_nm
    window_height_nm = bottom_cladding_nm + core_height_nm + top_cladding_nm
    core_centre_y_nm = bottom_cladding_nm + core_height_nm / 2.0

    wavelength_label = str(int(wavelength_nm))
    modes_requested = number_of_modes[int(wavelength_nm)]
    run_folder = output_folder / f"{wavelength_label}nm"
    run_folder.mkdir(exist_ok=True)

    simulation_name = f"SiN_1000x800_{wavelength_label}nm"
    sin_material = f"SiN_{wavelength_label}"
    sio2_material = f"SiO2_{wavelength_label}"

    print(f"\nSolving at {wavelength_nm:.0f} nm")
    print(f"n(SiN) = {n_sin:.6f}, n(SiO2) = {n_sio2:.6f}")

    em = emc.EMode(simulation_name=simulation_name, save_path=str(run_folder))

    em.add_material(
        name=sin_material,
        refractive_index_equation=f"{n_sin:.10f}",
        wavelength_unit="um",
    )
    em.add_material(
        name=sio2_material,
        refractive_index_equation=f"{n_sio2:.10f}",
        wavelength_unit="um",
    )

    em.settings(
        wavelength=wavelength_nm,
        x_resolution=mesh_nm,
        y_resolution=mesh_nm,
        window_width=window_width_nm,
        window_height=window_height_nm,
        num_modes=modes_requested,
        background_material=sio2_material,
        boundary_condition=boundary_condition,
        max_effective_index=n_sin + 0.05,
    )

    em.shape(
        name="SiN_core",
        material=sin_material,
        width=core_width_nm,
        height=core_height_nm,
        position=[0.0, core_centre_y_nm],
    )

    em.FDM()
    em.effective_area()
    em.plot(component="Ex", mode=0)
    effective_index = as_1d(em.get("effective_index"))
    te_fraction = normalise_te_fraction(em.get("TE_fraction"))
    effective_area = as_1d(em.get("effective_area"))

    x_nm = np.real(np.asarray(em.get("x"))).ravel()
    y_nm = np.real(np.asarray(em.get("y"))).ravel() - bottom_cladding_nm

    ex_all = em.get("Ex")
    ey_all = em.get("Ey")
    ez_all = em.get("Ez")

    modes_found = len(effective_index)
    guided_modes = np.where(effective_index > n_sio2 + 1e-3)[0]

    if len(guided_modes) == 0:
        raise RuntimeError(f"No guided modes were found at {wavelength_nm:.0f} nm.")

    mode_intensities = []
    rows = []

    for mode_index in guided_modes: #loops over and solves all the modes
        ex = select_mode(ex_all, mode_index, modes_found)
        ey = select_mode(ey_all, mode_index, modes_found)
        ez = select_mode(ez_all, mode_index, modes_found)
        intensity = np.abs(ex) ** 2 + np.abs(ey) ** 2 + np.abs(ez) ** 2
        mode_intensities.append(intensity)

        te_percent = 100.0 * te_fraction[mode_index]
        polarization = "TE-like" if te_percent >= 50.0 else "TM-like"

        rows.append(
            {
                "wavelength_nm": wavelength_nm,
                "solver_mode_index": int(mode_index),
                "polarization": polarization,
                "n_eff": effective_index[mode_index],
                "TE_percent": te_percent,
                "TM_percent": 100.0 - te_percent,
                "A_eff_um2": effective_area[mode_index],
            }
        )

    try:
        em.close(save=True, save_all_fields=False)
    except (OSError, RuntimeError) as error:
        print(f"EMode close warning: {error}")
        try:
            em.close()
        except (OSError, RuntimeError) as error:
            print(f"Fallback EMode close warning: {error}")

    # Give Windows time to release the EMode port file before the next run.
    time.sleep(1.5)

    return rows, x_nm, y_nm, mode_intensities


def print_mode_table(rows):
    print("\nMode  Polarization       n_eff     TE [%]   TM [%]  A_eff [um^2]")
    print("----  ------------  ----------  --------  -------  ------------")

    for row in rows:
        print(
            f"{row['solver_mode_index']:>4d}  "
            f"{row['polarization']:<12s}  "
            f"{row['n_eff']:>10.7f}  "
            f"{row['TE_percent']:>8.2f}  "
            f"{row['TM_percent']:>7.2f}  "
            f"{row['A_eff_um2']:>12.4f}"
        )


def plot_guided_modes(wavelength_nm, rows, x_nm, y_nm, intensities):
    columns = 3
    rows_of_plots = int(np.ceil(len(rows) / columns)) #for the subplots
    figure, axes = plt.subplots(
        rows_of_plots,
        columns,
        figsize=(12, 3.8 * rows_of_plots),
        constrained_layout=True,
        squeeze=False,
    )
    axes = axes.ravel()
    extent = [x_nm[0], x_nm[-1], y_nm[0], y_nm[-1]] #entire simulation span

    for plot_index, axis in enumerate(axes):
        if plot_index >= len(rows):
            axis.set_visible(False)
            continue

        row = rows[plot_index]
        intensity = intensities[plot_index]
        colour_limit = np.nanpercentile(intensity, 99.7)

        image = axis.imshow(
            intensity.T,
            origin="lower",
            extent=extent,
            aspect="auto",
            cmap="turbo",
            vmin=0.0,
            vmax=colour_limit,
        )

        axis.add_patch(
            Rectangle(
                (-core_width_nm / 2.0, 0.0),
                core_width_nm,
                core_height_nm,
                fill=False,
                edgecolor="white",
                linewidth=1.2,
            )
        )

        axis.set_xlim(-1500.0, 1500.0) #visual span
        axis.set_ylim(-1000.0, 1800.0)
        axis.set_xlabel("x [nm]")
        axis.set_ylabel("y [nm]")
        axis.set_title(
            f"Mode {row['solver_mode_index']}: {row['polarization']}\n"
            f"n_eff={row['n_eff']:.4f}, TE={row['TE_percent']:.1f}%"
        )
        figure.colorbar(image, ax=axis, fraction=0.046, pad=0.03)

    figure.suptitle(
        f"Guided modes at {wavelength_nm:.0f} nm: $|E|^2$",
        fontsize=15,
    )
    figure_path = output_folder / f"guided_modes_{int(wavelength_nm)}nm.png"
    figure.savefig(figure_path, dpi=250)
    plt.show()


all_rows = []

for wavelength_nm in wavelengths_nm:
    rows, x_nm, y_nm, intensities = solve_at_wavelength(wavelength_nm)
    print_mode_table(rows)
    plot_guided_modes(wavelength_nm, rows, x_nm, y_nm, intensities)
    all_rows.extend(rows)


csv_path = output_folder / "guided_mode_properties_930_1550.csv"
with csv_path.open("w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=all_rows[0].keys())
    writer.writeheader()
    writer.writerows(all_rows)

print(f"\nResults saved in: {output_folder.resolve()}")
