# ADC tolerance study in EMode2D

Does a narrower access waveguide make a silicon asymmetric directional coupler (ADC)
more tolerant to width errors? These scripts answer that for two couplers,
TE0→TE1 and TE0→TE2, on 220 nm silicon-on-insulator with oxide cladding at 1550 nm
and a 200 nm gap. Everything is a 2D cross-section mode solve, so it runs in EMode2D.

## Files

| File | What it does |
| --- | --- |
| `adc_study.py` | The study: parameters at the top, one function per step. |
| `solver_emode.py` | Every EMode call lives here (settings, shape, reset, FDM, get, get_grid, get_fields). EMode2D functions only; EMode2D is the only solver. |
| `modefields.py` | Mode fields: the checks done on them and the saved `modes/*.npz` files (`modefields.load`). |
| `plots.py` | The figures. |
| `report_figures.py` | Figures (PDF) and tables for the report in `../mdm-design-study/report.tex`, from `results_emode/`. |
| `../tests/` | In `Photonics/tests`: a test double of `emodeconnection` and two test scripts. The double accepts only the documented EMode arguments and answers with a made-up coupled-mode model; it is not a mode solver and none of the study's results come from it. Run the tests from `Photonics/`, for example `python tests/test_modes_step.py`. |
| `results_emode/` | The EMode2D run (10 nm grid). |
| `results_emode_quick/` | The coarse EMode2D run (`--quick`, 20 nm grid). |

## Run it

EMode must be installed and logged in (`pip install emodeconnection`, then
`emode-install`, then `emode login`). Python also needs `numpy`, `scipy`,
`matplotlib`. The solver asks for an EMode2D licence (`license_type='2d'`) and
saves `adc_study.eph` in the results folder.

```
python adc_study.py --backend emode --steps check    # one solve: tests the EMode link
python adc_study.py --backend emode --quick          # coarse first look
python adc_study.py --backend emode                  # full study (about 800 mode solves)
python adc_study.py --backend emode --steps modes,plots   # add the mode fields to a finished run (90 solves)
python adc_study.py --backend emode --steps matched,plots # couplers rebuilt at the phase-matched width (about 160 solves)
python adc_study.py --backend emode --steps plots    # redraw figures from saved results
```

Other options: `--access 300,340,400` (access widths in nm), `--couplers 1`,
`--resolution 5`, `--out folder`. Results go to `results_emode/` next to
`adc_study.py`, wherever the script is started from: figures, `summary.csv`,
`results.json`, `cache.json`, and from the `modes` step `modes/*.npz` and
`modes_summary.csv`. Solved cross-sections are cached, so a rerun only solves what is
new; saved mode fields are reused the same way. Delete `cache.json` (or `modes/`) to
force new solves.

## Status: what has been tested

- `solver_emode.py` was checked line by line against the EMode documentation
  (version 1.0.8): the Python interface, Simulation setup, Solver analysis, File
  management, Variables and Material pages, the release notes and troubleshooting,
  and the EMode2D examples. The full study has since been run with a licensed EMode
  (`results_emode/`).
- `mode_fields()`, the field reading of the `modes` and `matched` steps, produced
  `results_emode/modes/` with EMode's `get('x')`, `get('Ex')`, ... calls. Those are
  deprecated, so it now reads the grid with `get_grid()` and the fields with
  `get_fields(['Ex', 'Ey', 'Hx', 'Hy'])`, as the EMode documentation asks. This new
  version has not yet run against EMode: run the `check` step first. It does one field
  solve and prints the grid, the components EMode returned and where the TE0 field is
  centred (should be x = 0, y = 0). `get()` is still used for `effective_index`,
  `TE_fraction`, `loss_dB_per_m`, `BC`, `PML_indices` and `emode_version`, which are
  not deprecated.
- A test double of `emodeconnection` that only accepts the documented keyword
  arguments and applies the documented conventions was used to run the whole study,
  including the `modes` and `matched` steps, through the EMode code path. It refuses
  the deprecated `get('x')`, `get('Ex')`, ... calls. Its numbers come from a made-up
  coupled-mode model, so it tests the Python, not EMode's numbers.
- The `matched` step has not been run in EMode yet.

### Changes after reading the EMode documentation (18 Nov)

| What | Before | Now | Source in the docs |
| --- | --- | --- | --- |
| Bend loss reference | `loss_dB_per_m` used as if it were per metre along the core | Rescaled by (R + x_off)/R. EMode gives n_eff and loss per metre along the window centre. That reference alone made the old 90° loss 14 % too low at R = 3 um. | Ring Resonator Design example |
| Bend window | East PML 1.5 um from the core edge; the 1 um top and bottom PMLs started at the silicon surface (the PML lies inside the window) | Window reaches past the radiation caustic R(n_eff/n_clad - 1) plus 0.5 um before a 1.5 um PML (6 um at R = 10 um); 1 um of oxide between the silicon and the top and bottom PMLs | Ring Resonator Design and Bending: SiN examples; Variables (`pml_extent`) |
| Bend solver shift | `n_eff + 0.05` at the core radius | `(n_eff + 0.05)` referenced to the window centre; falls back to `pml_seed_bool=True` if no TE mode is found; PML modes (`PML_indices`) skipped | Ring Resonator Design; Simulation setup |
| Settings between solves | `reset(kind='shapes')`, so PML and bend settings stayed on the profile | `reset(kind='all')`, then every setting given again | Simulation setup: `reset` |
| Window size | Any length; EMode grows it to an even cell count and warns | Rounded to an even number of cells, core on the mirror plane, so the 'TE' fold of the bend solve is kept | Release notes 1.0.7; Troubleshooting |
| Licence | `EMode()` tries EMode3D first | `EMode(license_type='2d')` | Python interface |
| Dai TM benchmark | Constant indices ignored by EMode | `emc.MaterialProperties(n=...)` for core and cladding | Scattering loss: Laser example; Simulation setup |
| Output | EMode printed every solve | `FDM(verbose=False)` | Release notes 1.0.5 |

Conventions confirmed and kept: lengths in nm; origin at the centre of the bottom
wall with `position` = shape centre; `boundary_condition='00'` (metal walls, full
window) for straight solves, as in the Straight Waveguide Convergence example;
explicit grid steps instead of the 1.0.8 default `'auto'`; `get('effective_index')`,
`get('TE_fraction')` and `get('loss_dB_per_m')`; materials `'Si'` and `'SiO2'` from
the database (Si is valid from 1357 nm, so 1500–1600 nm is covered).

EMode2D also offers `converge()` (automatic resolution and window convergence) and
`perturb()` (first-order dn_eff/dW for tolerance analysis). The study does its own
convergence and sensitivity checks, but these are an independent check if wanted.

The bend step is still the least certain part. To look at a bend solve, run
`python adc_study.py --backend emode --steps bend` on its own (the straight solves
come from the cache, so the last solve in the file is a bend), then reopen the saved
file as in the 'Open a Simulation' example:

```python
import emodeconnection as emc
em = emc.EMode(simulation_name='adc_study', save_path='results_emode', open_existing=True)
em.plot(component='Ex', window_display=True)   # field, window and PMLs
em.close()
```

## Method

1. **Width sweep** (`step_sweep`). Single strips: n_eff of TE0, TE1, TE2 against
   width, and the slopes S = dn_eff/dW.
2. **Anticrossing scan** (`step_design`). The coupler cross-section (access | gap | bus)
   has two supermodes. Their index difference dn_s is smallest near phase matching.
   Scanning the bus width and fitting

       dn_s(W)^2 = dn_min^2 + [c (W - W*)]^2

   gives the bus width W*, the coupling coefficient kappa = pi dn_min / lambda and the
   coupling length L_c = lambda / (2 dn_min). The fit treats W* as the phase-matched
   width. The mode fields (step 7) show that this holds only when the coupling does
   not change with the bus width; for narrow access waveguides W* is several nm too
   wide (see the mode-field check below).
3. **Width error** (`step_tolerance`). Every waveguide is dW wider and the center lines
   stay fixed: access W_a + dW, bus W* + dW, gap g - dW. The scan is repeated for this
   geometry and the converted power at the nominal length L_c is

       eta = (dn_min / dn_s)^2 * sin^2(pi dn_s L_c / lambda)

   The first factor is the phase-matching penalty, the second the length penalty.
   **Tolerance** = largest |dW| for which the unconverted power 1 - eta stays below
   -15 dB.
4. **Wavelength** (`step_wavelength`). The same at 1500 to 1600 nm with fixed geometry.
5. **Bend loss** (`step_bend`). The access waveguide in a bend. This sets how narrow it
   can be.
6. **Validation** (`step_validate`). Mesh convergence; the published couplers of
   Wang et al. 2022 (TE) and Dai et al. 2013 (TM); re-solved tolerance against the
   first-order estimate that uses only kappa and the slopes S.
7. **Mode fields** (`step_modes`). For every design and every width error in
   `mode_errors` (default -10, 0, +10 nm, same geometry rule as step 3) three
   cross-sections are solved on one grid and saved: the coupler (two supermodes), the
   access strip alone (TE0) and the bus strip alone (TE1 or TE2). Each supermode is
   fitted with the two strip modes (least squares on the transverse electric field,
   all modes at unit power). From the fit:
   - **residual**: the share of the supermode the two strip modes do not explain. It
     stays small if the coupling is the intended two-mode coupling; a third mode
     taking part would raise it.
   - **access share s** of the upper supermode. Two-mode coupled-mode theory turns it
     into the detuning, dn_det = (1 - 2 s) dn_s, and the largest convertible power,
     4 s (1 - s). So the fields give their own unconverted power at the nominal length,

         eta = 4 s (1 - s) sin^2(pi dn_s L_c / lambda)

     which is compared with step 3. s = 0.5 means the coupler is phase matched.
   - **bus width for an even mixture**: W* moved by the detuning the fields show
     (dn_det / dn/dW of the bus mode).
   - also: dn_s solved at the exact geometry against the step 2 fit, the phase of the
     two strips in each supermode, TE fractions, the field within 300 nm of the window
     walls, and the access mode's tail at the bus edge (what sets the coupling).

   Results: console table, `modes_summary.csv`, `results.json` ('modes') and
   figures 8 to 12.
8. **Couplers at the phase-matched width** (`step_matched`). Each coupler is rebuilt
   with its bus at the even-mixture width W_pm from step 7 (checked with one solve and
   corrected until the access share is 0.50 +/- 0.02). For each width error in
   `matched_errors` (default -10, -5, 0, 5, 10 nm) the coupler and its strips are
   solved; the access share s gives dn_det = (1 - 2s) dn_s and
   dn_min = 2 sqrt(s(1 - s)) dn_s. With L_pm = lambda / (2 dn_s(0)) and quadratic fits of
   dn_min and dn_det over dW, eta follows from the formula of step 3 and gives the
   tolerance. Results: console table, `results.json` ('matched'), three extra columns in
   `summary.csv`, and figure 13. The checks are cached in `cache.json`; no fields are
   saved.

### Saved mode fields

Each `modes/TE0-TE<m>_wa<access>_dw<error>.npz` holds the four modes of one
geometry on one grid, real after a phase rotation, with 600 nm of cladding around
the strips (about 1 MB each at a 10 nm grid). Coordinates are in nm, with
the access strip centred on x = 0 and the silicon from y = -110 to +110 nm.

```python
import modefields
d = modefields.load("results_emode/modes/TE0-TE1_wa320_dw+0.npz")
d["x"], d["y"]                          # grid (nm)
d["modes"]["upper"]["Ex"]               # Re(Ex) on (x, y); also "Ey", "neff", "te"
d["meta"]["cores"], d["meta"]["checks"] # strip positions and widths; share, residual
```

The names are `access`, `bus`, `upper`, `lower`. The access mode has Ex > 0 at the
centre of its strip, the bus mode in its lobe next to the gap, and each supermode's
access part is in phase with the access mode. So in the saved Re(Ex), a positive bus
lobe next to the gap means the two strips oscillate in phase. The figures draw |Ex|
instead, where a sign change shows as a dark line: an anti-phase supermode has one in
the gap.

## Figures

| Figure | Shows |
| --- | --- |
| `fig1_phase_matching` | n_eff against width and how the bus widths follow. |
| `fig2_anticrossing` | The scan and fit for the baseline coupler. |
| `fig3_design` | Coupling length, sensitivity mismatch and their ratio against access width. |
| `fig4_tolerance_curves` | Unconverted power against width error. |
| `fig5_tolerance_summary` | Tolerance against access width: the main result. |
| `fig6_wavelength` | Conversion loss against wavelength. |
| `fig7_bend_loss` | Loss per 90 degree bend against access width (EMode only). |
| `fig8_modes_TE0-TE1`, `fig9_modes_TE0-TE2` | Every nominal coupler: access mode alone, bus mode alone, upper and lower supermode, with the access share. |
| `fig10_supermodes_width_error` | Upper supermode of the narrowest and widest couplers at each saved width error. |
| `fig11_mode_checks` | Access-mode tail at the bus, two-mode residual, and how far W* is from the phase-matched bus width. |
| `fig12_tolerance_fields` | Unconverted power against width error: the model of step 3 (lines) and the fields (dots). |
| `fig13_tolerance_matched` | Tolerance with the bus at W* (model) and at the phase-matched width (fields). |

The mode maps (figures 8 to 10 and the report's mode figure) use EMode's own colour
scale, matplotlib's `plasma` as in EMode's `plot()`: |Ex| with each mode scaled to its
own peak, dark where there is no field, and the silicon outlined in white.

## Results (EMode2D, 10 nm grid, `results_emode/`)

| Coupler | Access (nm) | Bus W* (nm) | L_c (um) | kappa (1/um) | S_a - S_m (1e-3/nm) | Tolerance (nm) | First-order (nm) | Worst C-band (dB) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| TE0→TE1 | 320 | 697.2 | 7.1 | 0.222 | 2.02 | ±8 | ±9.5 | -17.1 |
| TE0→TE1 | 360 | 766.7 | 12.0 | 0.130 | 1.77 | ±5.75 | ±6.5 | -16.2 |
| TE0→TE1 | 400 | 840.8 | 19.8 | 0.079 | 1.42 | ±4.5 | ±4.75 | -16.5 |
| TE0→TE1 | 440 | 917.0 | 30.3 | 0.052 | 1.12 | ±3.75 | ±4 | -16.4 |
| TE0→TE1 | 480 | 994.5 | 45.2 | 0.035 | 0.87 | ±3 | ±3.5 | -16.6 |
| TE0→TE2 | 320 | 1069.4 | 8.5 | 0.185 | 2.80 | ±5.25 | ±5.75 | -15.5 |
| TE0→TE2 | 360 | 1169.9 | 14.6 | 0.108 | 2.40 | ±3.5 | ±3.75 | -15.3 |
| TE0→TE2 | 400 | 1278.6 | 24.0 | 0.065 | 1.90 | ±2.75 | ±3 | -15.4 |
| TE0→TE2 | 440 | 1391.7 | 37.3 | 0.042 | 1.48 | ±2 | ±2.5 | -15.7 |
| TE0→TE2 | 480 | 1507.0 | 54.2 | 0.029 | 1.17 | ±1.75 | ±2 | -15.8 |

"Worst C-band" is the highest unconverted power between 1530 and 1565 nm. The
tolerance is the largest |dW| with at most -15 dB unconverted power at the nominal
coupler length.

Checks from the same run:

- Mesh convergence of the 400 nm TE0→TE1 coupler: L_c = 19.17, 19.74 and 19.82 um and
  W* = 844.6, 841.7 and 840.8 nm at 40, 20 and 10 nm grid.
- Wang et al. 2022 report 17.0 um for their conventional TE0→TE1 coupler with a
  400 nm access waveguide. This run gives L_c = 19.8 um.
- Dai et al. 2013 use a 1020 nm bus for TM0→TM1 (400 nm access, 1500 nm, constant
  indices 3.455 and 1.445). Isolated phase matching in this run gives 1035.5 nm.

### Mode-field check (`--steps modes`)

The coupling is the intended two-mode coupling, and it is stronger for narrow access
waveguides for the expected reason:

- The two strip modes explain every supermode to within 2.8 % of its field (largest
  for 320 nm access, at most 0.35 % at 480 nm). The upper supermode has the strips in
  phase and the lower in anti-phase in every case. TE fraction at least 0.93; at most
  0.02 % of a field lies within 300 nm of the window walls.
- The supermode splitting solved at each exact geometry agrees with the anticrossing
  fits to within 2.9 %.
- The access mode alone has |Ex|^2 at the bus edge of -12.4 dB (320 nm), -14.8,
  -17.3, -19.4 and -21.0 dB (480 nm) relative to its peak.

But W*, the anticrossing minimum, is not where the supermodes are an even mixture:

| Coupler | Access (nm) | W* (nm) | W_iso (nm) | Even mixture W_pm (nm) | Access share at W* | Unconverted at W*, dW = 0 (dB) |
| --- | --- | --- | --- | --- | --- | --- |
| TE0→TE1 | 320 | 697.2 | 686.3 | 686.1 | 0.37 | -11.6 |
| TE0→TE1 | 360 | 766.7 | 760.6 | 761.1 | 0.41 | -15.0 |
| TE0→TE1 | 400 | 840.8 | 837.0 | 837.2 | 0.43 | -17.2 |
| TE0→TE1 | 440 | 917.0 | 914.3 | 914.7 | 0.45 | -19.4 |
| TE0→TE1 | 480 | 994.5 | 992.2 | 992.7 | 0.45 | -20.5 |
| TE0→TE2 | 320 | 1069.4 | 1055.3 | 1057.6 | 0.38 | -12.6 |
| TE0→TE2 | 360 | 1169.9 | 1161.8 | 1164.3 | 0.43 | -16.6 |
| TE0→TE2 | 400 | 1278.6 | 1273.6 | 1275.6 | 0.45 | -20.0 |
| TE0→TE2 | 440 | 1391.7 | 1387.8 | 1389.6 | 0.46 | -22.0 |
| TE0→TE2 | 480 | 1507.0 | 1503.6 | 1505.6 | 0.47 | -24.3 |

W_iso is the bus width at which the isolated strips have equal n_eff (step 2's
"isolated" column). The even-mixture width from the fields lies within 0.5 nm of it
for TE0→TE1 and within 2.5 nm for TE0→TE2, while W* is 1.4 to 12 nm wider. The
coupling weakens as the bus widens, and that moves the minimum of dn_s away from
phase matching; the narrower the access waveguide, the stronger the coupling and the
larger the shift. A coupler built at W* is therefore detuned before any fabrication
error, by most for the narrowest access widths. The tolerances in the table above
assume full conversion at dW = 0, that is, a coupler at the phase-matched width, not
at W*. The `matched` step solves those couplers directly; it has not been run yet.

## Limits of the method

- 2D cross-sections only. Coupling in the S-bends, the tapers between bus sections
  and reflections are not modelled. A real coupler needs a shorter straight section
  than L_c.
- Two-mode model. Power lost to other modes and to radiation is ignored.
- The nominal bus width is the anticrossing minimum W*. The mode fields show it is
  wider than the phase-matched width, by 1.4 to 12 nm in the EMode run (most for
  narrow access), so the bus widths in the first columns of the summary table are too
  wide by that much. Use W_pm (`bus_width_phase_matched_nm` after the `matched` step),
  the even-mixture width from the `modes` step, or W_iso for a layout.
- The unconverted power is a coupler-level number. Channel crosstalk in a complete
  multiplexer needs a propagation simulation (EME or FDTD).
- Only width errors are studied. Silicon thickness and sidewall angle also vary.
