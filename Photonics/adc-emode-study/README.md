# ADC tolerance study in EMode2D

Does a narrower access waveguide make a silicon asymmetric directional coupler (ADC)
more tolerant to width errors? These scripts answer that for two couplers,
TE0→TE1 and TE0→TE2, on 220 nm silicon-on-insulator with oxide cladding at 1550 nm
and a 200 nm gap. Everything is a 2D cross-section mode solve, so it runs in EMode2D.

## Files

| File | What it does |
| --- | --- |
| `adc_study.py` | The study: parameters at the top, one function per step. |
| `solver_emode.py` | Every EMode call lives here (settings, shape, reset, FDM, get). EMode2D functions only. |
| `solver_empy.py` | Open-source mode solver with the same interface, for cross-checks. |
| `plots.py` | The figures. |
| `tests/` | Test double of `emodeconnection` (documented arguments only) and `test_solver_emode.py`. |
| `crosscheck_empy_20nm/` | Results of a complete run with the open-source solver. |

## Run it

EMode must be installed and logged in (`pip install emodeconnection`, then
`emode-install`, then `emode login`). Python also needs `numpy`, `scipy`,
`matplotlib`. The solver asks for an EMode2D licence (`license_type='2d'`) and
saves `adc_study.eph` in the results folder.

```
python adc_study.py --backend emode --steps check    # one solve: tests the EMode link
python adc_study.py --backend emode --quick          # coarse first look
python adc_study.py --backend emode                  # full study (about 700 mode solves)
python adc_study.py --backend emode --steps plots    # redraw figures from saved results
```

Other options: `--access 300,340,400` (access widths in nm), `--couplers 1`,
`--resolution 5`, `--out folder`. Results go to `results_emode/`: figures,
`summary.csv`, `results.json` and `cache.json`. Solved cross-sections are cached, so
a rerun only solves what is new. Delete `cache.json` to force new solves.

The open-source cross-check needs no EMode:

```
pip install electromagneticpython
python adc_study.py --backend empy --resolution 20
```

## Status: what has been tested

- `solver_emode.py` was checked line by line against the EMode documentation
  (version 1.0.8): the Python interface, Simulation setup, Solver analysis, File
  management, Variables and Material pages, the release notes and troubleshooting,
  and the EMode2D examples. It has **not** been run against a licensed EMode, because
  that needs your licence. Run the `check` step first. It prints the EMode version and
  the boundary condition EMode actually used.
- A test double of `emodeconnection` that only accepts the documented keyword
  arguments and applies the documented conventions was used to run the whole study
  through the EMode code path. That tests the Python, not EMode's numbers.
- The analysis (`adc_study.py`, `plots.py`) was run end to end with the open-source
  solver. Those results are in `crosscheck_empy_20nm/`. They are not EMode results.

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
   has two supermodes. Their index difference dn_s is smallest when the strips are
   phase matched. Scanning the bus width and fitting

       dn_s(W)^2 = dn_min^2 + [c (W - W*)]^2

   gives the phase-matched bus width W*, the coupling coefficient
   kappa = pi dn_min / lambda and the coupling length L_c = lambda / (2 dn_min).
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

## Cross-check results (open-source solver, 20 nm grid, not EMode)

| Coupler | Access (nm) | Bus W* (nm) | L_c (um) | S_a - S_m (1e-3/nm) | Tolerance (nm) | First-order (nm) | Worst C-band (dB) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TE0→TE1 | 320 | 702 | 7.4 | 1.96 | ±8.25 | ±9.5 | -17.4 |
| TE0→TE1 | 360 | 772 | 12.2 | 1.69 | ±6.0 | ±6.5 | -16.8 |
| TE0→TE1 | 400 | 846 | 19.5 | 1.35 | ±5.0 | ±5.25 | -16.2 |
| TE0→TE1 | 440 | 922 | 29.8 | 1.07 | ±4.0 | ±4.25 | -16.7 |
| TE0→TE1 | 480 | 999 | 42.8 | 0.84 | ±3.5 | ±3.75 | -17.1 |
| TE0→TE2 | 320 | 1079 | 8.8 | 2.68 | ±5.5 | ±5.75 | -15.7 |
| TE0→TE2 | 360 | 1180 | 14.8 | 2.29 | ±3.75 | ±4.0 | -15.5 |
| TE0→TE2 | 400 | 1288 | 23.7 | 1.82 | ±3.0 | ±3.0 | -15.5 |
| TE0→TE2 | 440 | 1401 | 36.2 | 1.43 | ±2.5 | ±2.5 | -15.5 |
| TE0→TE2 | 480 | 1516 | 52.1 | 1.13 | ±2.0 | ±2.25 | -15.6 |

"Worst C-band" is the highest unconverted power between 1530 and 1565 nm.

Checks from the same run:

- Mesh convergence of the baseline TE0→TE1 coupler: L_c = 19.6, 19.5, 19.8 um at
  40, 20, 10 nm grid. W* = 849, 846, 844 nm.
- Wang et al. 2022 report 17.0 um for their conventional TE0→TE1 coupler with a
  400 nm access waveguide. This run gives 19.5 um.
- Dai et al. 2013 use a 1020 nm bus for TM0→TM1. Isolated phase matching in this run
  gives 1053 nm at 20 nm grid (1042 nm at 5 nm grid). Their 4.5 um coupler length
  comes from 3D FDTD with S-bends and is not comparable with the 11.9 um supermode
  coupling length.

## Limits of the method

- 2D cross-sections only. Coupling in the S-bends, the tapers between bus sections
  and reflections are not modelled. A real coupler needs a shorter straight section
  than L_c.
- Two-mode model. Power lost to other modes and to radiation is ignored.
- The unconverted power is a coupler-level number. Channel crosstalk in a complete
  multiplexer needs a propagation simulation (EME or FDTD).
- Only width errors are studied. Silicon thickness and sidewall angle also vary.
- The open-source solver has no sub-pixel averaging: its n_eff is about 0.01 too high
  at a 10 nm grid. EMode uses sub-pixel averaging by default (`subpixel_avg=True`)
  and should converge faster.
