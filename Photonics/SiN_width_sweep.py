"""Standalone EMode width sweep for an 800-nm-thick SiN waveguide.

Mode labels are assigned from polarization and field shape, not from the raw
EMode mode number.  For example, TE10 means a TE-like mode with one sign change
along x and no sign change along y in its dominant transverse field Ex.
"""

import csv
import traceback
from datetime import UTC, datetime
from pathlib import Path

import emodeconnection as emc
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

# =============================================================================
# STUDENT SETTINGS
# =============================================================================

# Change this value to 1550.0 to run the second wavelength.
WAVELENGTH_NM = 930.0

CORE_HEIGHT_NM = 800.0
WIDTHS_NM = np.arange(100.0, 1400.0 + 1e-9, 100.0)

# The shorter wavelength can support more modes, so the solver must search for
# more candidate solutions. Students normally only change WAVELENGTH_NM above.
NUMBER_OF_MODES = 16 if WAVELENGTH_NM <= 1000.0 else 8

SIDE_CLADDING_NM = 2500.0
TOP_CLADDING_NM = 2500.0
BOTTOM_CLADDING_NM = 2500.0
WINDOW_WIDTH_NM = 6500.0
WINDOW_HEIGHT_NM = BOTTOM_CLADDING_NM + CORE_HEIGHT_NM + TOP_CLADDING_NM
CORE_CENTRE_Y_NM = BOTTOM_CLADDING_NM + CORE_HEIGHT_NM / 2.0

MESH_NM = 10.0
BOUNDARY_CONDITION = "00"
GUIDED_MARGIN = 1e-3
POLARIZATION_LIMIT = 0.65
MAX_NEFF_STEP = 0.15


def n_sin_luke(wavelength_um):
    """Refractive index of stoichiometric Si3N4."""
    lam = wavelength_um
    n_squared = (
        1.0
        + 3.0249 / (1.0 - (0.135341 / lam) ** 2)
        + 40314.0 / (1.0 - (1239.84 / lam) ** 2)
    )
    return float(np.sqrt(n_squared))


def n_sio2_malitson(wavelength_um):
    """Refractive index of fused silica."""
    lam = wavelength_um
    n_squared = (
        1.0
        + 0.696166 / (1.0 - (0.0684043 / lam) ** 2)
        + 0.407943 / (1.0 - (0.116241 / lam) ** 2)
        + 0.897479 / (1.0 - (9.89616 / lam) ** 2)
    )
    return float(np.sqrt(n_squared))


def as_1d(values):
    return np.asarray(values, dtype=float).ravel()


def normalise_te_fraction(values):
    values = as_1d(values)
    if values.size and np.nanmax(values) > 1.5:
        values = values / 100.0
    return values


def select_mode(field_array, mode_index, modes_found):
    """Extract one two-dimensional mode from common EMode array layouts."""
    field_array = np.asarray(field_array)

    if field_array.ndim == 2:
        return field_array
    if field_array.ndim == 3:
        if field_array.shape[0] == modes_found:
            return field_array[mode_index, :, :]
        if field_array.shape[-1] == modes_found:
            return field_array[:, :, mode_index]
    if field_array.ndim == 4:
        if field_array.shape[:2] == (1, modes_found):
            return field_array[0, mode_index, :, :]
        if field_array.shape[:2] == (modes_found, 1):
            return field_array[mode_index, 0, :, :]
        if field_array.shape[0] == 1 and field_array.shape[-1] == modes_found:
            return field_array[0, :, :, mode_index]

    raise ValueError(f"Unexpected field-array shape: {field_array.shape}")


def orient_field(field, x_nm, y_nm):
    """Return a field array ordered as [x, y]."""
    field = np.asarray(field)
    if field.shape == (len(x_nm), len(y_nm)):
        return field
    if field.shape == (len(y_nm), len(x_nm)):
        return field.T
    raise ValueError(
        f"Field shape {field.shape} does not match x/y grid "
        f"({len(x_nm)}, {len(y_nm)})."
    )


def phase_align(field):
    """Rotate one complex field so its largest point is real and positive."""
    index = np.unravel_index(np.argmax(np.abs(field)), field.shape)
    return field * np.exp(-1j * np.angle(field[index]))


def count_sign_changes(line, threshold=0.08, smoothing_points=5):
    """Count robust sign changes in a one-dimensional real field lineout."""
    line = np.real(np.asarray(line, dtype=complex))
    if line.size < 3 or np.max(np.abs(line)) == 0:
        return 0

    kernel = np.ones(smoothing_points) / smoothing_points
    line = np.convolve(line, kernel, mode="same")
    keep = np.abs(line) >= threshold * np.max(np.abs(line))
    signs = np.sign(line[keep])

    if signs.size == 0:
        return 0

    # Compress consecutive equal signs. Points near a node were removed above.
    sign_regions = signs[np.r_[True, signs[1:] != signs[:-1]]]
    return max(0, len(sign_regions) - 1)


def lobe_order(field, x_nm, y_nm, width_nm):
    """Return (number of x nodes, number of y nodes) inside the SiN core."""
    field = phase_align(field)
    x_core = np.where(np.abs(x_nm) <= width_nm / 2.0)[0]
    y_core = np.where(
        (y_nm >= BOTTOM_CLADDING_NM)
        & (y_nm <= BOTTOM_CLADDING_NM + CORE_HEIGHT_NM)
    )[0]

    core_field = field[np.ix_(x_core, y_core)]
    real_field = np.real(core_field)

    # Use the strongest horizontal and vertical lineouts, avoiding a line that
    # accidentally lies on a node of the other coordinate.
    y_line_index = int(np.argmax(np.sum(np.abs(core_field) ** 2, axis=0)))
    x_line_index = int(np.argmax(np.sum(np.abs(core_field) ** 2, axis=1)))
    nodes_x = count_sign_changes(real_field[:, y_line_index])
    nodes_y = count_sign_changes(real_field[x_line_index, :])
    return nodes_x, nodes_y


def polarization_name(te_fraction):
    """Return TE, TM, or HYB without forcing a strongly hybrid mode."""
    if te_fraction >= POLARIZATION_LIMIT:
        return "TE"
    if te_fraction <= 1.0 - POLARIZATION_LIMIT:
        return "TM"
    return "HYB"


def label_candidates(candidates, previous_neff):
    """Resolve labels using lobe shape first and n_eff continuity second."""
    groups = {}
    for mode in candidates:
        base = f"{mode['polarization']}{mode['nodes_x']}{mode['nodes_y']}"
        mode["shape_label"] = base
        groups.setdefault(base, []).append(mode)

    for base, group in groups.items():
        if len(group) == 1:
            chosen = group[0]
        elif base in previous_neff:
            chosen = min(group, key=lambda item: abs(item["neff"] - previous_neff[base]))
        else:
            chosen = max(group, key=lambda item: item["neff"])

        for mode in group:
            if mode is chosen:
                mode["mode_label"] = base
                jump = abs(mode["neff"] - previous_neff[base]) if base in previous_neff else 0.0
                mode["label_confident"] = (
                    mode["polarization"] != "HYB" and jump <= MAX_NEFF_STEP
                )
                mode["neff_step"] = jump
                previous_neff[base] = mode["neff"]
            else:
                # Do not silently give two different fields the same physical label.
                mode["mode_label"] = f"UNRESOLVED_mode{mode['emode_index']}"
                mode["label_confident"] = False
                mode["neff_step"] = np.nan

    return candidates


def save_mode_profile(mode, wavelength_nm, width_nm, x_nm, y_nm, output_folder):
    field = phase_align(mode["label_field"])
    real_field = np.real(field)
    vmax = np.nanpercentile(np.abs(real_field), 99.7)
    if not np.isfinite(vmax) or vmax == 0:
        vmax = 1.0

    fig, ax = plt.subplots(figsize=(6.2, 4.8), constrained_layout=True)
    image = ax.imshow(
        real_field.T,
        origin="lower",
        extent=[x_nm[0], x_nm[-1], y_nm[0] - BOTTOM_CLADDING_NM,
                y_nm[-1] - BOTTOM_CLADDING_NM],
        cmap="turbo",
        vmin=-vmax,
        vmax=vmax,
        aspect="equal",
    )
    ax.add_patch(
        Rectangle(
            (-width_nm / 2.0, 0.0), width_nm, CORE_HEIGHT_NM,
            fill=False, edgecolor="white", linewidth=1.4,
        )
    )
    component = mode["label_component"]
    ax.set_xlim(-1600, 1600)
    ax.set_ylim(-800, 1700)
    ax.set_xlabel("x [nm]")
    ax.set_ylabel("y [nm]")
    ax.set_title(
        f"{wavelength_nm:.0f} nm, w={width_nm:.0f} nm: "
        f"{mode['mode_label']}  Re({component})"
    )
    fig.colorbar(image, ax=ax, label=f"Re({component}) [solver units]")
    filename = (
        f"w{int(width_nm):04d}nm_{mode['mode_label']}_"
        f"emode{mode['emode_index']}.png"
    )
    fig.savefig(output_folder / filename, dpi=220, bbox_inches="tight")
    plt.close(fig)


def make_overview_plot(rows, wavelength_nm, quantity, ylabel, filename, output_folder):
    confident = [row for row in rows if row["label_confident"]]
    labels = sorted({row["mode_label"] for row in confident})

    fig, ax = plt.subplots(figsize=(8.0, 5.4), constrained_layout=True)
    for label in labels:
        selected = sorted(
            [row for row in confident if row["mode_label"] == label],
            key=lambda row: row["width_nm"],
        )
        linestyle = "-" if label.startswith("TE") else "--"
        ax.plot(
            [row["width_nm"] for row in selected],
            [row[quantity] for row in selected],
            marker="o", linestyle=linestyle, linewidth=1.6,
            markersize=4, label=label,
        )

    ax.set_xlabel("SiN core width [nm]")
    ax.set_ylabel(ylabel)
    ax.set_title(f"{wavelength_nm:.0f} nm")
    ax.grid(alpha=0.3)
    ax.legend(ncol=2)
    fig.savefig(output_folder / filename, dpi=300, bbox_inches="tight")
    plt.close(fig)


def run_width_sweep():
    """Run one complete width sweep and save tables, profiles, and plots."""
    wavelength_nm = WAVELENGTH_NM
    number_of_modes = NUMBER_OF_MODES
    wavelength_um = wavelength_nm / 1000.0
    n_sin = n_sin_luke(wavelength_um)
    n_sio2 = n_sio2_malitson(wavelength_um)

    script_folder = Path(__file__).resolve().parent
    timestamp = datetime.now(tz=UTC).strftime("%Y-%m-%d_%H-%M-%S")
    output_folder = script_folder / f"SiN_{wavelength_nm:.0f}nm_width_sweep_{timestamp}"
    profile_folder = output_folder / "mode_profiles"
    project_folder = output_folder / "emode_projects"
    profile_folder.mkdir(parents=True, exist_ok=True)
    project_folder.mkdir(exist_ok=True)

    rows = []
    previous_neff = {}
    error_log = output_folder / "errors.txt"

    print(f"\nSiN width sweep at {wavelength_nm:.0f} nm")
    print(f"n(SiN) = {n_sin:.6f}, n(SiO2) = {n_sio2:.6f}")

    for width_nm in WIDTHS_NM:
        print(f"\nSolving width {width_nm:.0f} nm")
        em = None
        try:
            width_tag = f"w{int(width_nm):04d}"
            width_project_folder = project_folder / width_tag
            width_project_folder.mkdir(exist_ok=True)
            em = emc.EMode(
                simulation_name=f"SiN_{wavelength_nm:.0f}nm_{width_tag}",
                save_path=str(width_project_folder),
            )

            sin_name = f"SiN_{wavelength_nm:.0f}"
            sio2_name = f"SiO2_{wavelength_nm:.0f}"
            em.add_material(
                name=sin_name,
                refractive_index_equation=f"{n_sin:.10f}",
                wavelength_unit="um",
            )
            em.add_material(
                name=sio2_name,
                refractive_index_equation=f"{n_sio2:.10f}",
                wavelength_unit="um",
            )
            em.settings(
                wavelength=wavelength_nm,
                x_resolution=MESH_NM,
                y_resolution=MESH_NM,
                window_width=WINDOW_WIDTH_NM,
                window_height=WINDOW_HEIGHT_NM,
                num_modes=number_of_modes,
                background_material=sio2_name,
                boundary_condition=BOUNDARY_CONDITION,
                max_effective_index=n_sin + 0.05,
            )
            em.shape(
                name="SiN_core", material=sin_name,
                width=float(width_nm), height=CORE_HEIGHT_NM,
                position=[0.0, CORE_CENTRE_Y_NM],
            )

            em.FDM()
            em.effective_area()

            neff = as_1d(em.get("effective_index"))
            te_fraction = normalise_te_fraction(em.get("TE_fraction"))
            effective_area = as_1d(em.get("effective_area"))
            x_nm = np.real(as_1d(em.get("x")))
            y_nm = np.real(as_1d(em.get("y")))
            ex_all = em.get("Ex")
            ey_all = em.get("Ey")
            modes_found = len(neff)

            candidates = []
            for mode_index in range(modes_found):
                if neff[mode_index] <= n_sio2 + GUIDED_MARGIN:
                    continue

                polarization = polarization_name(te_fraction[mode_index])
                ex = orient_field(
                    select_mode(ex_all, mode_index, modes_found), x_nm, y_nm
                )
                ey = orient_field(
                    select_mode(ey_all, mode_index, modes_found), x_nm, y_nm
                )
                if polarization == "TE":
                    label_field = ex
                    label_component = "Ex"
                elif polarization == "TM":
                    label_field = ey
                    label_component = "Ey"
                else:
                    # For a hybrid mode, inspect whichever transverse component
                    # actually carries the clearer spatial pattern.
                    if np.max(np.abs(ex)) >= np.max(np.abs(ey)):
                        label_field = ex
                        label_component = "Ex"
                    else:
                        label_field = ey
                        label_component = "Ey"
                nodes_x, nodes_y = lobe_order(label_field, x_nm, y_nm, width_nm)

                candidates.append(
                    {
                        "wavelength_nm": wavelength_nm,
                        "width_nm": float(width_nm),
                        "emode_index": mode_index,
                        "polarization": polarization,
                        "neff": float(neff[mode_index]),
                        "te_fraction": float(te_fraction[mode_index]),
                        "effective_area_um2": float(effective_area[mode_index]),
                        "nodes_x": nodes_x,
                        "nodes_y": nodes_y,
                        "label_field": label_field,
                        "label_component": label_component,
                    }
                )

            candidates = label_candidates(candidates, previous_neff)
            for mode in candidates:
                print(
                    f"  EMode {mode['emode_index']:2d} -> {mode['mode_label']:18s} "
                    f"neff={mode['neff']:.7f}, TE={100*mode['te_fraction']:.1f}%, "
                    f"confident={mode['label_confident']}"
                )
                save_mode_profile(
                    mode, wavelength_nm, width_nm, x_nm, y_nm, profile_folder
                )
                row = {key: value for key, value in mode.items() if key != "label_field"}
                rows.append(row)

        except (OSError, RuntimeError, ValueError, TypeError, KeyError, IndexError):
            message = f"FAILED at width {width_nm} nm\n{traceback.format_exc()}\n"
            print(message)
            with open(error_log, "a", encoding="utf-8") as file:
                file.write(message)
        finally:
            if em is not None:
                try:
                    em.close(save=False, save_all_fields=False)
                except (OSError, RuntimeError) as exc:
                    print(f"Warning: failed to close EMode connection: {exc}")

    csv_fields = [
        "wavelength_nm", "width_nm", "emode_index", "polarization",
        "mode_label", "shape_label", "label_component", "nodes_x", "nodes_y", "neff",
        "neff_step", "te_fraction", "effective_area_um2", "label_confident",
    ]
    csv_path = output_folder / f"modal_sweep_{wavelength_nm:.0f}nm.csv"
    with open(csv_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=csv_fields)
        writer.writeheader()
        writer.writerows(rows)

    make_overview_plot(
        rows, wavelength_nm, "neff", r"$n_{\mathrm{eff}}$",
        f"{wavelength_nm:.0f}nm_neff_vs_width.png", output_folder,
    )
    make_overview_plot(
        rows, wavelength_nm, "effective_area_um2",
        r"$A_{\mathrm{eff}}$ [$\mu$m$^2$]",
        f"{wavelength_nm:.0f}nm_Aeff_vs_width.png", output_folder,
    )

    print(f"\nResults saved in: {output_folder.resolve()}")
    print("Rows with label_confident=False must be inspected manually.")


if __name__ == "__main__":
    run_width_sweep()
