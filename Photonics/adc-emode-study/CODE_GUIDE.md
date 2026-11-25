# How the ADC study code works

This guide explains every function in the five Python files of the design study and
every design decision behind them. It describes the code as it is in this folder.

| File | Role |
| --- | --- |
| `adc_study.py` | The study itself: parameters, physics formulas, and one method per step. |
| `solver_emode.py` | The only file that talks to EMode. Builds each cross-section and runs the mode solver. |
| `modefields.py` | Pure-numpy maths on mode fields (power, overlap, two-mode fit) and the saved field files. |
| `plots.py` | The 13 study figures in `results_emode/`. |
| `report_figures.py` | The four report figures and the rows of Table 1, and the numbers quoted in the report text. |

Lengths are in nm everywhere unless a name says otherwise (`_um`, `_per_um`, `_dB`).
The scripts pass ruff and Pylance's type checks; section 9 says how to run them.

---

## 1. How the pieces fit together

```
adc_study.py  ──calls──▶  solver_emode.py  ──▶  EMode2D (FDM mode solver)
     │                          │
     │ every solve is cached    └─ returns n_eff, TE fraction, and (for the mode
     ▼                             steps) the fields Ex, Ey, Hx, Hy
results_emode/
   cache.json        every solved cross-section (keyed by geometry and settings)
   results.json      the results of every step
   modes/*.npz       saved mode fields (written with modefields.save)
   summary.csv, modes_summary.csv
     │
     ├──▶ plots.py           → results_emode/fig1 … fig13 (PNG)
     └──▶ report_figures.py  → ../mdm-design-study/figures/report_*.pdf
                               ../mdm-design-study/generated/table_designs.tex
```

Design decisions in this layout:

- **EMode is isolated in one file.** Only `solver_emode.py` imports `emodeconnection`.
  The rest of the study sees a small interface (`modes`, `mode_fields`, `bend_loss`),
  which is what lets the tests run the whole study through a test double of
  `emodeconnection` without a licence.
- **Every solve is cached.** A rerun only solves cross-sections it has not solved before,
  and an interrupted run loses little work.
- **Figures never need EMode.** `python adc_study.py --steps plots` and
  `python report_figures.py` read only `results.json` and `modes/*.npz`.
- **The field maths is pure numpy** (`modefields.py`), so every check on the fields can be
  redone later from the saved files.

---

## 2. Every design decision at a glance

### 2.1 The physical design

| Decision | Value | Why | Where |
| --- | --- | --- | --- |
| Platform | 220 nm silicon, SiO2 above and below, λ = 1550 nm, TE | Standard silicon photonics. Oxide on both sides makes the cross-section symmetric top to bottom, which prevents TE–TM hybridisation. | `EModeSolver(h_si=220, core="Si", clad="SiO2")`, `CFG["wavelength"]` |
| Couplers | TE0→TE1 and TE0→TE2 | The first two stages of a cascaded ADC mode multiplexer (Dai et al. 2013 layout). | `CFG["couplers"]` |
| Gap | 200 nm, fixed | A conventional gap, and the smallest feature allowed in the study. Fixing it means any gain comes from the access width alone. | `CFG["gap"]` |
| Access widths | 320, 360, 400, 440, 480 nm | The design variable. 480 nm is near the single-mode limit: the access TE1 mode becomes guided between 460 and 480 nm. The lower end was expected to be set by confinement and bend loss. | `CFG["access_widths"]` |
| Baseline access width | 400 nm | The conventional value used by Dai et al. 2013 and Wang et al. 2022, so the benchmarks and the mesh check use it. | `CFG["baseline"]` |
| Bus width | W*, the bus width of minimum supermode splitting | Found by scanning the bus width through the anticrossing. Isolated phase matching (W_iso) is only the starting guess. The mode fields later show W* sits 1.4 to 12 nm wider than true phase matching (W_pm). | `Study.anticrossing`, `step_design` |
| Fabrication error | Every waveguide ΔW wider, centre lines fixed, so the gap shrinks by ΔW | A lithography or etch bias moves every sidewall by ΔW/2. | `step_tolerance`, `step_modes`, `step_matched` |
| Coupler length under error | Kept at the nominal L_c | A fabricated coupler cannot change its length. | `conversion(..., d["Lc"], ...)` |
| Tolerance criterion | Largest \|ΔW\| with unconverted power 1 − η ≤ −15 dB, for both signs | −15 dB means about 97 % of the light reaches the intended mode. | `CFG["residual_limit_dB"]`, `symmetric_tolerance` |
| Width errors solved | ±10 and ±20 nm (plus 0) | About 4 and 8 times the 2.6 nm wafer-scale non-uniformity, so the range also covers a systematic process bias. | `CFG["width_errors"]` |
| Wavelengths | 1500, 1530, 1550, 1565, 1600 nm; C-band 1530–1565 nm | The C-band edges, the design wavelength, and 50 nm beyond on each side. | `CFG["wavelengths"]`, `CFG["c_band"]` |
| Bend radii | 3, 5, 10 µm | A tight, a typical and a relaxed S-bend radius for the access waveguide. | `CFG["bend_radii"]` |

### 2.2 The numerical method

| Decision | Value | Why | Where |
| --- | --- | --- | --- |
| Solver | EMode2D finite-difference mode solver (FDM), 2D cross-sections only | Runs on an EMode2D licence; the study needs only effective indices and fields of cross-sections. | `solver_emode.py` |
| Grid | 10 nm in x and y | Checked by mesh convergence at 40, 20 and 10 nm: L_c changes by 0.4 % from 20 to 10 nm. | `CFG["resolution"]`, `CFG["convergence_resolutions"]` |
| Window | 1.5 µm of oxide beside the outermost strips, 1 µm above and below the silicon | Far enough that the walls do not distort the modes: less than 0.02 % of any mode's field lies within 300 nm of the walls. | `side_margin`, `vert_margin`, `modefields.edge_fraction` |
| Window size | Rounded up to an even number of 10 nm cells | EMode would grow the window itself (extra cells at the top), moving the structure off centre. Rounding first keeps the geometry exactly as asked. | `EModeSolver._even` |
| Boundaries | `"00"`: plain walls on all four sides, no symmetry fold | The asymmetric coupler has no vertical mirror plane, and the TM benchmark needs TM modes, which a fold would remove. Setting it also turns off EMode's `'auto'` default. | `_straight` |
| Modes per solve | 10 (single strips and couplers) | Enough to include the bus's lower-order modes, the TM modes and the supermode pair. The TM benchmark uses 12 and 14. | `CFG["modes_single"]`, `CFG["modes_coupled"]` |
| Guided-mode rule | n_eff > 1.46 and TE fraction > 0.5 (TE) or ≤ 0.5 (TM) | Oxide is 1.444 at 1550 nm; 1.46 keeps a small margin so cladding-like and near-cutoff modes are dropped. | `N_GUIDED`, `Study.guided` |
| Which two supermodes | The neighbouring pair of guided modes whose mean index is closest to the isolated access index | That pair is the one formed by the access TE0 and the bus mode it is matched to, not by other bus modes. | `Study.splitting`, `_solve_mode_set` |
| Anticrossing fit | Δn_s² = Δn_min² + c²(W − W*)², fitted as a parabola in Δn_s² | This is the exact two-mode form, so a quadratic fit in Δn_s² gives Δn_min, W* and c directly. | `Study.anticrossing` |
| Scan | ±30 nm around the guess in 10 nm steps, re-centred until W* is in the middle | The scan points sit on a 10 nm grid, so different scans reuse each other's cached solves. | `CFG["scan_half_range"]`, `CFG["scan_step"]` |
| Smooth curves n_eff(W) | PCHIP interpolation through the width sweep | Shape-preserving: no overshoot between points, and smooth derivatives for the slopes S = dn_eff/dW. The phase-matching width W_iso is also found on this curve. | `Study._curves`, `width_at_index` |
| Fits over ΔW and λ | Quadratic fits of Δn_min and Δn_det through the solved points; tolerance searched on a 0.25 nm grid | Five solved points per curve; a quadratic captures the curvature (negative errors detune faster) without overfitting. | `step_tolerance`, `step_wavelength`, `step_matched` |
| First-order estimate | Constant coupling, detuning (S_a − S_m)ΔW: ΔW_tol ≈ 0.18 Δn_min/\|S_a − S_m\| | An analytic check on the re-solved tolerance; it always overestimates. | `step_design` |
| Materials | EMode's database Si and SiO2 (dispersive); constant 3.455 and 1.445 for the Dai benchmark | The database gives the real dispersion for the wavelength sweep. Dai et al. used constant indices, so the benchmark does too. | `_materials`, `DAI_2013` |
| Bends | Cylindrical bend solver, PML on the outer, top and bottom walls, horizontal mirror fold | Follows EMode's bend examples. The window reaches 0.5 µm past the radiation caustic. | `bend_loss` |

### 2.3 The mode-field analysis

| Decision | Value | Why | Where |
| --- | --- | --- | --- |
| Same grid | The coupler and each strip alone are solved in the coupler's window | Their fields can then be compared point by point. | `frame=` in `modes`, `mode_fields` |
| Normalisation | Each mode scaled to 1 W from the Poynting vector (to unit field norm if EMode gives no H) | So the fitted amplitudes squared are powers. | `modefields.normalised` |
| Two-mode fit | Least squares of each supermode on the two strip modes, using their overlap (Gram) matrix | The strip modes overlap, so they are not orthogonal; projecting on each separately would count the overlap twice. | `modefields.decompose` |
| Checks | Access share s, residual, Δn_s, phase signs, TE fraction, edge fraction, tail at the bus | Each one tests an assumption of the two-mode model or of the window. | `_solve_mode_set`, `_mode_row` |
| Width errors with fields | ΔW = 0, ±10 nm | Brackets every tolerance found (at most 8 nm) and shows how the mixture shifts. | `CFG["mode_errors"]` |
| Saved fields | Ex and Ey only, cropped to 600 nm of cladding around the strips, float32 | About 1 MB per set at 10 nm; E is all the figures and later checks need. | `CFG["mode_crop"]`, `modefields.save` |
| Phase convention | Access mode: Ex > 0 at the centre of its strip. Bus mode: Ex > 0 in the lobe next to the gap. Supermodes: access part in phase with the access mode | Fixes the arbitrary sign of each eigenmode, so the sign of the bus lobe shows in-phase (+) or anti-phase (−). | `_solve_mode_set` |
| W_pm estimate | W* minus the detuning seen in the fields over the bus slope: W_pm = W* − Δn_det/S_m | Moving only the bus width by δ changes the detuning by S_m δ. | `_mode_row` |
| Matched rebuild | Bus at W_pm, checked to give s = 0.5 ± 0.02 (corrected at most twice); solved at ΔW = 0, ±5, ±10 nm | A direct test that the index-based tolerances hold for a phase-matched coupler. ±10 nm covers every tolerance found. | `step_matched`, `CFG["matched_errors"]` |

### 2.4 The figures

| Decision | Value | Why | Where |
| --- | --- | --- | --- |
| Colours | matplotlib's defaults. C0 for TE0→TE1, C1 for TE0→TE2, C<i> for the i-th access width, black for reference lines | No colour definitions to maintain. Where two plots must match, they name the same default colour. | `plots.py`, `report_figures.py` |
| Mode maps | \|Ex\| on `plasma`, each mode scaled to its own peak, silicon outlined in white | `plasma` is EMode's own colour scale; it matched the colour bar of an EMode plot exactly. A sign change shows as a dark line (a zero of the field). | `plots._field_panel` |
| Map framing | Equal aspect, every row of a figure at the same scale, each row centred on its coupler and kept inside its saved window | Outside the saved window there is no field, and the edge would show on the dark background. | `plots._views` |
| Report fonts | DejaVu Sans, TrueType embedded in the PDF | DejaVu ships with matplotlib, so the figures look the same on any machine; embedded TrueType keeps the text as text. | `report_figures.py` |

---

## 3. `solver_emode.py`

The only file that imports `emodeconnection`. Its module docstring records the EMode
conventions it relies on (checked against the EMode 1.0.8 documentation):

- the origin is at the horizontal centre of the bottom wall: x runs from −W/2 to +W/2,
  y from 0 to the window height; a shape's `position` is its centre;
- giving the shape's y explicitly stops EMode stacking it as a substrate, so each
  silicon strip floats in the oxide background;
- since EMode 1.0.8 the boundary condition and resolution default to `'auto'`; both
  are set explicitly so the study's own convergence checks control them;
- settings stay on the EMode profile between solves, so every solve starts with
  `reset(kind='all')` and gives every setting again;
- in a bend, `bend_radius` is measured at the window centre, and EMode's n_eff and loss
  refer to that radius.

### `class EModeSolver`

Class attribute `name = "emode"`. It goes into the cache keys of the mode-field steps
and into the saved metadata, so results from different solvers are never mixed.

#### `__init__(resolution=10, h_si=220, side_margin=1500, vert_margin=1000, core="Si", clad="SiO2", simulation_name="adc_study", save_path=".", verbose=False)`
Stores the grid step, silicon thickness, window margins and material names, sets
`fixed_indices` to `None` (database materials), and stores three bend settings taken from
EMode's bend examples: `pml_side = 1500` (outer-wall PML), `pml_vertical = 1000` (top and
bottom PML) and `caustic_clearance = 500` (oxide between the radiation caustic and the
PML). `fixed_indices` is declared `tuple[float, float] | None`. The Dai benchmark sets the
tuple from `adc_study.py`; without the declaration Pylance sees only the `None` set here,
finds no possible value inside `if self.fixed_indices:` in `_materials`, and reports
that "Never" is not iterable. `last` holds details of the last solve for checking.
Finally it opens the EMode session with `license_type='2d'`, written in the call rather
than taken as a parameter, because the study only ever uses EMode2D functions. `'2d'`
checks out the EMode2D licence directly; `'3d'` would fail on an account without an
EMode3D licence, and `'default'` takes a 3D licence first when one is available.

#### `_even(length)`
Rounds a window length up to a whole, even number of grid cells:
`cells = 2·ceil(length / (2·resolution) − 1e-9)`. The `− 1e-9` stops an exact multiple
being rounded up by floating-point error. Even, because EMode itself grows the window to
an even number of cells by adding them at the top, which would move the structure off
the window's mirror plane.

#### `_snap(length)`
Rounds a length up to a whole number of cells. Used for the margins, so walls fall on
grid lines.

#### `_materials()`
Returns the core and cladding materials: the database names `"Si"` and `"SiO2"`, or
`emc.MaterialProperties(n=...)` with constant indices when `fixed_indices` is set (the
Dai benchmark).

#### `_clad_index(wavelength)`
The cladding index, used only to place the bend window past the radiation caustic: the
fixed value, EMode's `refractive_index(material=clad, wavelength=...)`, or 1.444 (SiO2
near 1550 nm) if that call fails. EMode's answer goes through `np.asarray` before numpy
reads it, as in `_read`: the EMode package declares that its calls can also return a
dict, text or a plot, and numpy's type hints accept only array-like values.

#### `_read(key)`
Reads a per-mode result with `em.get(key)` and returns it as a 1D real float array.

#### `_read_optional(key, default=None)`
`em.get(key)`, or `default` if EMode raises. Used for diagnostics (`BC`, `PML_indices`,
`emode_version`) that must not stop a run. It returns EMode's answer unchanged, so
`bend_loss` passes the `PML_indices` through `np.asarray` before numpy reads them.

#### `_te_fraction()`
Reads `TE_fraction`. It is documented as 0 to 1; if the values exceed 1.5 they are taken
as percent and divided by 100, so a change of units in EMode cannot break the TE/TM
sorting.

#### `_axis(values)` (static)
Turns a grid axis from EMode into a 1D float array. If EMode returns a 2D meshgrid, it
keeps the distinct values.

#### `_stack(raw, n_modes, nx, ny)` (static)
Brings one field component of every mode into the layout (mode, x, y). EMode may return
(mode, x, y) or (mode, y, x), and a single mode may come without the mode axis. The mode
axis is moved to the front if needed, and the x and y lengths tell the two layouts apart
(the window is never square here). Any other shape raises an error rather than guessing.

#### `modes(cores, wavelength, num_modes=8, frame=None)`
Solves one straight cross-section and returns `(n_eff, TE_fraction)`, sorted by
decreasing n_eff. `cores` is a list of `(x_centre, width)` strips. `frame` (default: the
cores) sets the window: giving a coupler's two strips as the frame while solving only one
of them puts that strip on the coupler's grid.

#### `mode_fields(cores, wavelength, num_modes=8, frame=None)`
The same solve, plus the fields. It reads the grid with `get_grid()` and the fields with
`get_fields(['Ex', 'Ey', 'Hx', 'Hy'])` (retrying with `['Ex', 'Ey']` if that fails),
because reading x, y or fields through `get()` is deprecated in EMode. Coordinates are
returned in the caller's frame: x shifted back by the centring shift, y shifted so the
silicon runs from −h_si/2 to +h_si/2. Each component is stacked to (mode, x, y) and
sorted like the indices. Missing Ex or Ey raises an error; missing H is recorded in
`last["fields_missing"]` and the analysis then falls back to the field norm. EMode
normalises each mode to 1 W.

#### `_member(obj, name)` (static)
Reads `name` from an EMode result object (`Grid`, `Field`) or from a dict, so the code
works with both.

#### `_straight(cores, wavelength, num_modes, frame=None)`
Builds and solves a straight cross-section:

1. Finds the left and right edges of the frame strips and shifts the structure so it is
   centred on x = 0. The shift is a whole number of cells, so walls on the grid stay on
   the grid.
2. Window width = twice (the larger half-extent + `side_margin`), rounded up to an even
   number of cells. Window height = silicon thickness + twice `vert_margin`, also even.
3. `reset(kind='all')`, then `settings(...)` with the wavelength, the x and y resolution,
   the window size, the number of modes, `boundary_condition='00'`, oxide as the
   background material, and `max_effective_index=0` (EMode then starts its search from
   the highest index in the window).
4. One `shape` per strip, centred at mid-height of the window, then `FDM()`.
5. Reads `effective_index` and the TE fraction, and records the window and the boundary
   condition EMode reports back in `last`.

Returns the raw indices, TE fractions, the sort order, the shift and the window height.

#### `bend_loss(width, radius, wavelength, n_guess=None)`
The fundamental TE mode of one strip bent to `radius` (measured at the core centre), set
up as in EMode's 'Ring Resonator Design' and 'Bend Mode Solvers' examples:

- If no `n_guess` is given, the straight TE0 index is solved first.
- The centre of curvature is to the west, so the bend radiates east. The radiation
  caustic lies about `radius·(n_eff/n_clad − 1)` outside the core. The east side of the
  window reaches 0.5 µm past it (or the normal margin, if that is larger) before a
  1.5 µm PML. The west side gets the normal margin. Top and bottom get 1 µm of oxide plus
  a 1 µm PML.
- The core sits `x_off` west of the window centre, and EMode's `bend_radius` is set to
  `radius + x_off`, because EMode measures it at x = 0. A bend radius smaller than half
  the window raises an error.
- The nested `solve(seed)` resets EMode and sets the cylindrical bend solver,
  `boundary_condition='TE'` (fold about the horizontal mirror plane), PMLs on the north,
  south and east walls with `pml_kappa_max=1`, and 2 modes. The first try aims the
  eigen-solver just above the guided mode: `(n_guess + 0.05)/scale`, referenced to the
  window centre; the margin is 0.05 rather than the example's 0.01 because the mode
  moves outward in tight bends. Modes flagged in `PML_indices` and modes with TE
  fraction ≤ 0.5 are dropped.
- If the first try raises an error or finds no guided TE mode, a second try uses
  `pml_seed_bool=True`: EMode takes the shift from the same structure solved without
  PML, so no guess is needed. `last["pml_seeded"]` records which try gave the result.
- The highest-index remaining mode is taken. A negative loss (PML truncation error) is
  reported as a warning.
- n_eff and loss (dB/m) are multiplied by `scale = (radius + x_off)/radius`, which moves
  their reference from the window centre to the core. The loss of a 90° bend is then
  `loss_dB_per_m·(π/2)·radius`.

#### `describe()`
One line with EMode's version and the details of the last solve, printed by the
`check` step.

#### `close()`
Closes the EMode session, which saves `adc_study.eph` in `save_path`.

---

## 4. `modefields.py`

Everything here is plain numpy on arrays of shape (x, y). A mode is a dict with `Ex`,
`Ey` and, when available, `Hx`, `Hy`. `NAMES = ("access", "bus", "upper", "lower")` are
the four modes saved per geometry.

#### `cell_sizes(v)`
The width of the grid cell around each point of a 1D axis. Cell edges lie halfway
between points; the two outer edges are half a cell beyond the end points. Works for
non-uniform grids.

#### `weights(x, y)`
The area of the cell around each grid point, `outer(cell_sizes(x), cell_sizes(y))`. Every
integral below is a sum of values times these weights.

#### `power(f, w)`
The power carried along z, ½ Re ∫ (E × H*)·z dA = ½ Re ∫ (Ex Hy* − Ey Hx*) dA, in solver
units. Without H fields it returns the field norm ∫ (|Ex|² + |Ey|²) dA instead.

#### `normalised(f, w)`
The mode divided by √|power|, so it carries unit power (or unit field norm). A mode with
zero power raises an error.

#### `inner(f, g, w)`
The overlap ⟨f, g⟩ = ∫ (Ex_f* Ex_g + Ey_f* Ey_g) dA of the transverse electric fields.

#### `decompose(s, a, b, w)`
Fits a supermode `s` as `α·a + β·b` with the two strip modes `a`, `b` (at unit power) by
least squares on the transverse electric field. It solves the 2×2 normal equations with
the Gram matrix [[⟨a,a⟩, ⟨a,b⟩], [⟨b,a⟩, ⟨b,b⟩]], because `a` and `b` overlap. Returns:

- `share = |α|² / (|α|² + |β|²)`, the supermode's share of power in mode `a`
  (0.5 is an even mixture, as at phase matching);
- `residual = ⟨d, d⟩ / ⟨s, s⟩` with `d = s − αa − βb`, the part of the field the two
  modes do not explain (a third mode taking part would show up here).

#### `phase_at(f, x, y, point)`
The phase factor `conj(v)/|v|` that makes Ex real and positive at the grid point nearest
`point` (1 if the field is zero there).

#### `rotated(f, phase)`
Multiplies every component of a mode by `phase`.

#### `imaginary_fraction(f, w)`
The share of the transverse field in its imaginary part. A lossless mode is real up to
one overall phase, so after alignment this should be about 0.

#### `mid_cut(f, y, comp="Ex")`
\|comp\|² along x through the middle of the silicon (the y nearest 0), scaled to a peak
of 1.

#### `level_dB(f, x, y, x0)`
\|Ex\|² at position `x0` on that line (linear interpolation), in dB relative to the line's
peak; floored at 10⁻³⁰. Used for the access mode's tail at the bus wall.

#### `edge_fraction(f, x, y, w, depth=300.0)`
The share of \|E_t\|² within `depth` nm of the window walls. It should be tiny; otherwise
the walls are distorting the mode.

#### `save(path, x, y, modes, meta, xlim, ylim)`
Saves the four modes of one geometry, cropped to `xlim` × `ylim`. x and y are stored as
float32. Each Ex and Ey is stored as float32 if its imaginary part is at most 10⁻³ of its
largest value, otherwise as complex64. `meta` (the checks and settings) is stored as a
JSON string, and the file is compressed (`np.savez_compressed`).

#### `load(path)`
Reads a saved set and returns `dict(x, y, meta, modes)`, where
`modes[name] = dict(Ex, Ey, neff, te)`.

---

## 5. `adc_study.py`

### Module-level settings

- **`CFG`**: every study parameter (see section 2): wavelength, gap, access widths,
  baseline, the isolated-strip sweeps (access 280–520 nm in 20 nm steps, bus 600–1700 nm
  in 50 nm steps), the anticrossing scan (±30 nm, 10 nm steps), width errors,
  wavelengths, C-band, the −15 dB limit, bend radii, grid and convergence grids, modes
  per solve, couplers, mode-field errors, field crop and matched errors. The sweeps
  extend beyond the access widths and the bus widths used (686 to 1507 nm), so slopes
  and phase matching are never read off at the end of a curve.
- **`QUICK`**: coarse settings for a first look (three access widths, ±10 nm errors,
  three wavelengths, coarser sweeps, ±20 nm scans, 20 nm grid).
- Both are declared `dict[str, Any]`. Their values mix numbers, lists and tuples. Without
  the declaration Pylance gives every value one combined type, and then rejects
  `cfg["resolution"]` as the solver's grid step and the list of floats that `--access`
  stores in `cfg["access_widths"]`.
- **`N_GUIDED = 1.46`**: modes with lower n_eff are not counted as guided (oxide is 1.444).
- **`WANG_2022`**: the conventional TE0→TE1 coupler of Wang et al. (400 nm access, 200 nm
  gap, L_c 17.0 µm; 820 nm is the bus of their corrugated coupler).
- **`DAI_2013`**: the TM0→TM1 coupler of Dai et al. (400 nm access, 300 nm gap, 1020 nm
  bus, 4.5 µm straight section, 1500 nm, constant indices 3.455 and 1.445).

### Physics helpers

#### `conversion(dn_min, dn_det, length, wavelength)`
Two-mode coupled-mode theory: the converted power after `length` is
η = (Δn_min/Δn_s)² sin²(π Δn_s L/λ), with Δn_s = √(Δn_min² + Δn_det²). The first factor
is the phase-matching penalty, the second the length penalty. Works on arrays.

#### `to_dB(x)`
10·log10(x), with x floored at 10⁻⁶, so a perfect value reads −60 dB instead of −∞.

#### `width_at_index(w, n, n_target)`
The width at which a sweep n(w), rising with w, reaches `n_target`, found by root-finding
(`brentq`) on the PCHIP curve between the two sweep points that bracket it. A straight
line between sweep points 50 nm apart would put the width up to about 1 nm too high:
n_eff(W) is concave, so the chord lies below the curve. Checked against EMode solves of
each bus strip at W_pm and W*, the PCHIP value is within 0.3 nm. Raises an error if
`n_target` is outside the sweep. The root goes through `cast(float, ...)` for the type
checker: scipy declares that `brentq` may return a tuple, which it does only when asked
for `full_output`.

#### `read_json(path)`
The contents of a JSON file, or an empty dict if the file does not exist yet. The file is
opened in a `with` block, so it is closed as soon as it has been read.

#### `symmetric_tolerance(dw, residual_dB, limit_dB)`
Steps through |ΔW| in increasing order and returns the largest value for which every
point with |ΔW| at most that value, negative and positive, is within the limit. So the
tolerance is ±ΔW: the whole interval passes, not just its ends.

### `class Study`

#### `__init__(solver, cfg, outdir)`
Stores the solver, configuration and results folder, and loads `cache.json` and
`results.json` with `read_json` (empty if they do not exist yet), so a run continues from
earlier results. `n_new` counts new solves.

#### `solve(cores, wavelength, num_modes)`
The cached straight solve. The key contains the grid, both margins, the silicon
thickness, wavelength, number of modes, fixed indices and every strip (centre and width
to 0.01 nm), so any change of settings makes a new key. The cache is also saved every 10
new solves, so a hard crash loses little work.

#### `save()`
Writes `cache.json` and `results.json` (the results indented, so they can be read), each
in a `with` block, so the file is complete and closed before the run goes on.

#### `guided(cores, wavelength, pol, num_modes)`
The guided modes of one polarisation, highest index first: n_eff > 1.46 and TE fraction
> 0.5 for TE, ≤ 0.5 for TM.

#### `n_iso(width, wavelength, order=0, pol="TE")`
The effective index of mode number `order` of a single strip (NaN if that mode is not
guided).

#### `splitting(wa, gap, wb, wavelength, pol="TE")`
The supermode splitting Δn_s of a coupler (access strip centred at x = 0, bus centred at
wa/2 + gap + wb/2). Of the guided modes, it takes the neighbouring pair whose mean is
closest to the isolated access index, which is the pair formed by the access mode and
the bus mode it is matched to. Fewer than two guided modes raises an error.

#### `anticrossing(wa, gap, wavelength, wb_guess, pol="TE")`
Scans the bus width and fits the anticrossing. The nested helper `scan(guess)` does one
scan:

1. It centres ±`scan_half_range` in `scan_step` steps on the guess, rounded to the step
   (so the points lie on a 10 nm grid and different scans share cached solves), and
   solves the splitting at each point.
2. It fits Δn_s² with a quadratic in (W − centre); the centred variable keeps the fit
   well conditioned. A non-positive curvature means there is no anticrossing and raises
   an error.
3. It returns the centre, the scan, the fit and W*, the parabola's minimum.

The first scan is centred on `wb_guess`. While W* lies more than half a step (+0.5 nm)
from the scan's centre, the scan is repeated centred on W* (each move limited to ±2 × the
half range), at most four more times: five scans in all. If W* has not settled by then,
the last fit is used. In the EMode run every design scan settled (W* within 4.5 nm of
its centre). Finally Δn_min² is the parabola's minimum value; a non-positive value raises
an error.

Returns a dict with W*, Δn_min, the slope c = √(curvature) (the detuning per nm of bus
width), the scan points and the RMS fit error. The return type is declared
`dict[str, Any]`: the dict holds numbers and lists, and the callers calculate with the
numbers (κ, the figure of merit, L_c).

#### `step_check()`
One solve of the 400 nm access strip, printed with the expected values (TE0 near 2.2
with TE fraction near 1, then TM0 near 1.7), EMode's version and boundary condition, and
one field read: grid size, field components, and where the TE0 field is centred
(expected x = 0, y = 0). Its purpose is to test the link to EMode quickly. (The `+ 0` in
the centring line turns −0 into 0 for the printout.)

#### `step_sweep()`
Solves isolated strips over the union of the access sweep, the bus sweep and the access
widths, and stores n_eff of TE0, TE1 and TE2 at each width.

#### `_curves()`
Builds a PCHIP interpolator n_eff(W) for TE0, TE1 and TE2 from the sweep (running the
sweep first if needed), skipping widths where the mode is not guided.

#### `_phase_matched_width(n_target, m)`
The bus width at which the isolated TEm mode has index `n_target` (isolated phase
matching), via `width_at_index` on the PCHIP curve. An index outside the sweep raises an
error that says to widen `bus_sweep`.

#### `step_design()`
For each coupler and access width:

1. n_a, the index of the isolated access TE0.
2. W_iso, the isolated phase-matching bus width.
3. S_a and S_m, the slopes dn_eff/dW of the access TE0 at W_a and of the bus TEm at
   W_iso, from the PCHIP derivative.
4. The anticrossing scan, started at W_iso, giving W*, Δn_min and c.
5. L_c = λ/(2Δn_min) and κ = πΔn_min/λ (stored per µm).
6. The first-order tolerance: η at L_c with constant Δn_min and detuning
   (S_a − S_m)ΔW, for ΔW from 0 to 40 nm in 0.25 nm steps.
7. The figure of merit Δn_min/|S_a − S_m| in nm.

#### `_designs()`
The design rows, running `step_design` first if needed.

#### `step_tolerance()`
For each design and each width error ΔW: at ΔW = 0 the design's own anticrossing is used;
otherwise the anticrossing is re-scanned for access W_a + ΔW and gap g − ΔW, starting at
W* + ΔW·S_a/S_m, where the perturbed coupler is expected to be phase matched (the access
index moves by S_a ΔW, which a bus change of S_a ΔW/S_m matches). The detuning of the
real coupler, whose bus is W* + ΔW, is Δn_det = c·((W* + ΔW) − W*(ΔW)). Δn_min and Δn_det
are fitted quadratically in ΔW, η is evaluated at the nominal L_c on a 0.25 nm grid, and
`symmetric_tolerance` gives the tolerance. It is flagged as a lower bound if it reaches
the edge of the solved range.

#### `step_wavelength()`
For each design and wavelength: the anticrossing at that wavelength (the design's own at
1550 nm), the detuning c·(W* − W*(λ)) of the nominal bus, η at the nominal L_c, quadratic
fits in λ and a 1 nm grid. Stores the conversion loss −10·log10 η and the highest
unconverted power in the C-band.

#### `step_bend()`
For each access width and radius, the bend solve (cached under `bend2|...`, the 2 marking
the loss referenced to the core radius). A failed solve is stored as NaN, so one bad
bend does not stop the study. Loss per 90° = loss (dB/m) × (π/2)·R.

#### `step_validate()`
Checks that the numbers can be trusted:

1. **Mesh convergence**: the 400 nm TE0→TE1 coupler at 40, 20 and 10 nm grids (the grid
   is restored afterwards).
2. **Wang et al. 2022**: W_iso, W* and L_c of the 400 nm TE0→TE1 coupler next to their
   17.0 µm.
3. **Dai et al. 2013** (TM0→TM1, 1500 nm, 300 nm gap): constant indices 3.455 and 1.445
   as in the paper, larger margins (2 µm, 1.5 µm) because TM modes reach further, and 12
   and 14 modes per solve. A TM1 sweep of the bus from 900 to 1150 nm gives W_iso, then the
   TM anticrossing gives W* and L_c. The paper's lengths are straight sections from 3D
   FDTD, where the S-bends add coupling, so they are shorter than the supermode L_c.
   If the benchmark fails, the error is printed and the other checks go on; every
   changed setting is restored in a `finally` block either way.
4. Prints the re-solved against the first-order tolerance.

#### `step_modes()`
For each design and each ΔW in `mode_errors`, the coupler is built with the same rule as
the tolerance step (bus at W* + ΔW, centre lines fixed). If a saved file for that
geometry exists and its stored key matches (same solver, grid, margins, thickness,
wavelength, fixed indices, crop and strips), its checks are reused; otherwise, or if the
file cannot be read, `_solve_mode_set` solves and saves it. `_mode_row` then compares the
fields with the two-mode model, and `_modes_report` prints the summary.

#### `_guided_te(neff, te)`
Indices of the guided TE modes (n_eff > 1.46, TE fraction > 0.5), highest first.

#### `_solve_mode_set(d, dw, cores, key, path, tag)`
The core of the mode-field analysis:

1. Solves the coupler, the access strip alone and the bus strip alone, all three in the
   coupler's window (`frame=cores`), and checks the three grids are identical.
2. Picks the access TE0, the bus TEm (guided TE mode number m, counting from 0) and the
   supermode pair (as in `splitting`). Missing modes raise an error.
3. Normalises each mode to unit power, using H when all three solves returned it (else
   the field norm). The nested helper `mode(f, i)` takes mode i of a solve and does this.
4. Fixes the phases: the access mode positive at its centre; the bus mode positive at the
   centre of its lobe next to the gap, at `w_bus/(2(m+1))` from the bus's gap-side wall
   (TEm has m+1 lobes).
5. Fits each supermode with `decompose`, then rotates it so its access part is in phase
   with the access mode. Records the share, the residual and the sign of the bus part
   relative to the access part (+1 in phase, −1 anti-phase).
6. Stores in `meta`: the cores, the normalisation used, n_eff and TE fraction of the four
   modes, the checks, Δn_s = n_upper − n_lower, the access mode's tail at the bus wall
   (`level_dB`), the largest edge fraction and the largest imaginary fraction.
7. If `path` is given, saves the four modes cropped to `mode_crop` around the strips.

#### `_matched_set(d, wb, dw)`
The same set of solves for a coupler with its bus at `wb` (nominal) under error `dw`,
cached in `cache.json` under a `set|...` key, without saving fields.

#### `step_matched()`
Rebuilds each coupler with its bus at the phase-matched width W_pm and takes its
tolerance from the fields:

1. Starts from the `modes` step's W_pm (running that step first if needed). One solve
   at ΔW = 0 checks the upper supermode's access share; if it is outside 0.5 ± 0.02, W_pm
   is moved by −(1 − 2s)Δn_s/S_m and checked again, at most twice; a warning is printed
   if it still fails. In the EMode run no correction was needed.
2. For each ΔW in `matched_errors` the coupler and strips are solved with the same error
   rule. The share s gives Δn_det = (1 − 2s)Δn_s and Δn_min = 2√(s(1 − s))Δn_s.
3. The coupler length is L_pm = λ/(2Δn_s) at ΔW = 0; Δn_min and Δn_det are fitted
   quadratically in ΔW, η uses `conversion` at L_pm, and `symmetric_tolerance` gives the
   tolerance on a 0.25 nm grid.
4. Saves after every coupler, so a later failure keeps the solved sets.

#### `_model_at(t, dw)`
The tolerance step's Δn_min and Δn_det at width error `dw`: the solved point if `dw` was
solved, otherwise the quadratic fit within the solved range, otherwise NaN.

#### `_mode_row(d, dw, meta, t)`
One row of the field checks, next to the model:

- from the fields: the access share s, Δn_s, Δn_det = (1 − 2s)Δn_s, and
  η = 4s(1 − s)·sin²(πΔn_s L_c/λ) at the nominal L_c, with the unconverted power in dB;
- the bus width of an even mixture, W_pm = W* − Δn_det/S_m (only at ΔW = 0);
- from the model at the same ΔW: Δn_min, Δn_det, Δn_s, the predicted share
  ½(1 − Δn_det/Δn_s) and η.

The row holds text and numbers, so its type is declared `dict[str, Any]`; `step_modes`
prints the numbers scaled (for example 10³·Δn_s).

#### `_modes_report(rows)`
Prints whether the coupling is the intended two-mode coupling (largest residual,
splitting against the fit, phase signs, TE fraction, edge fraction), the access-mode
tails, the phase-matching table at ΔW = 0 (share, unconverted power, W*, W_iso, W_pm),
and the largest share difference between fields and model. Writes `modes_summary.csv`.

#### `step_plots()`
Draws all figures with `plots.make_all`. `plots` is imported only here, so the study
itself does not need matplotlib until figures are wanted.

#### `write_summary()`
Writes `summary.csv`: one line per coupler with W*, L_c, κ, the sensitivity mismatch,
the tolerance and its lower-bound flag, the first-order tolerance and the worst C-band
value, plus W_pm, L_pm and the tolerance at W_pm once the `matched` step has run.

### `STEPS` and `main()`
`STEPS` is the default order: sweep, design, tolerance, wavelength, bend, validate,
modes, matched, plots. `check` can be added by name.

`main()` parses the command line: `--backend` (only `emode`; kept so earlier command
lines still work), `--quick`, `--steps`, `--resolution`, `--couplers`, `--access` and
`--out`. A whole-number `--resolution` is stored as an int, because the cache keys
contain the grid step as text and `10.0` would not match `10`. The results go to
`results_emode` (or `results_emode_quick`) next to the script, wherever it is started
from, so a run always finds its earlier results and cache. If the only step is `plots`,
it redraws from `results.json` without opening EMode. Otherwise it opens the EMode
session, runs the steps, writes `summary.csv`, and in a `finally` block saves the cache
and closes EMode, so an error mid-run keeps what was solved.

---

## 6. `plots.py`

Right after its imports it switches pyplot to the non-interactive `Agg` backend
(`plt.switch_backend("Agg")`): figures go to files only, no windows open, and it works
on a machine without a display. One `rcParams` block sets sizes, line widths and grid.
It defines no colours.
`COUPLER = {1: "TE0→TE1", 2: "TE0→TE2"}` gives the labels.

#### `_save(fig, outdir, name, note)`
Writes the note "Solver: EMode2D · grid 10 nm" in the bottom-right corner, saves the PNG
with a tight bounding box and closes the figure.

#### `fig_phase_matching(...)` → `fig1_phase_matching.png`
Isolated n_eff of TE0, TE1 and TE2 against strip width, each labelled at its end. A black
dashed line with dots marks the index of the 400 nm access TE0 and the bus widths W1 and
W2 where TE1 and TE2 match it (isolated phase matching).

#### `fig_anticrossing(...)` → `fig2_anticrossing.png`
For the 400 nm couplers: the solved splittings (black dots), the fitted hyperbola (the
coupler's colour) and a dashed line at W*. Titles give W* and L_c.

#### `fig_design(...)` → `fig3_design.png`
L_c, S_a − S_m, and Δn_min/(S_a − S_m) against access width for both couplers: shorter
couplers, but a larger mismatch, and their ratio.

#### `fig_tolerance_curves(...)` → `fig4_tolerance_curves.png`
Unconverted power against ΔW, one colour per access width: the fitted curve and the
solved points, with the −15 dB limit. The legend goes on the last panel that has data.

#### `fig_tolerance_summary(...)` → `fig5_tolerance_summary.png`
Tolerance against access width: re-solved (solid line) and first-order estimate (hollow
squares, dashed), both in the coupler's colour. A "≥" marks a tolerance that reached the
edge of the solved range.

#### `fig_wavelength(...)` → `fig6_wavelength.png`
Conversion loss against wavelength per access width, with the C-band shaded and one
legend below both panels.

#### `fig_bend(...)` → `fig7_bend_loss.png`
Loss per 90° bend against access width, one line per radius, on a log axis. Only finite,
positive values are drawn: the log axis cannot show the tiny negative values (PML
truncation error) that occur at 10 µm radius.

#### `_mode_sets(res, outdir)`
Loads the saved mode files that exist, keyed (coupler, access width, width error).

#### `_mode_rows(res)`
The `modes` result rows, keyed the same way.

#### `_views(rows, margin=450, ymargin=380)`
The x and y limits for each row of a mode-map figure. All rows get the same span, so
every panel has the same scale. The span is the widest coupler plus the margin on each
side, cut to what every saved window holds, but never less than the widest coupler plus
100 nm. The nested helper `box(sets)` gives a row's strip extent and the part of x that
all its saved windows cover. Each row is centred on its own coupler and shifted, if
needed, to stay inside its saved windows. The vertical limits are the silicon plus
`ymargin`, also kept inside the windows.

#### `_field_panel(ax, data, name, xlim, ylim)`
Draws one mode: \|Ex\| scaled to its own peak, on `plasma` from 0 to 1, with bilinear
smoothing; the silicon strips outlined in white; equal aspect, no ticks, no frame. It
returns nothing: the colour bar takes its scale from the panel images afterwards.

#### `_scale_bar(ax, xlim, ylim, length=500)`
A white 500 nm bar with its label in the lower-left corner of a panel.

#### `_field_grid(nrows, ncols, pw, ph, ...)`
A grid of panels sized in inches, so equal-aspect maps fill their panels exactly, plus a
thin colour-bar axis in the right margin, centred on the panels.

#### `_field_colorbar(fig, im, cax)`
The colour bar: ticks at 0, 0.5 and 1, the label "|Ex|, each mode scaled to its peak", no
outline and no grid line across it. The figures pass the first panel's image,
`axes[0, 0].images[0]`; every panel uses the same scale (`plasma`, 0 to 1), so any of
them gives the same bar. The outline is hidden through `cb.ax.spines["outline"]`, which
is the same object as `cb.outline`. matplotlib 3.10's type hints wrongly call
`cb.outline` a `Spines` (the collection of an axes' spines; fixed in 3.11), so Pylance
rejected `cb.outline.set_visible(False)`.

#### `fig_mode_gallery(res, cfg, outdir, note, m)` → `fig8_…`, `fig9_…`
For one coupler type, every access width at ΔW = 0: the access strip alone, the bus strip
alone, and the upper and lower supermodes. Each panel shows n_eff (and for the supermodes
the access share); each row shows W_a and the bus width.

#### `fig_supermodes_error(...)` → `fig10_supermodes_width_error.png`
The upper supermode of the narrowest and widest access width of each coupler at every
saved ΔW, with its access share: how a width error moves the mixture away from 50 %.

#### `fig_mode_checks(...)` → `fig11_mode_checks.png`
(a) \|Ex\|² of the access mode alone along the middle of the silicon, from its gap-side
wall, with the bus region shaded: narrower access waveguides reach the bus with a
stronger tail. (b) The largest two-mode residual per access width. (c) W* minus the
phase-matched width, from the fields (solid) and from equal isolated indices (dashed).

#### `fig_tolerance_fields(...)` → `fig12_tolerance_fields.png`
The tolerance step's model curves (lines) next to the unconverted power from the fields
(dots) for the couplers as designed. Dots below −45 dB are drawn at −45 dB so they stay on
the axis.

#### `fig_tolerance_matched(...)` → `fig13_tolerance_matched.png`
Tolerance against access width: the model with the bus at W* (solid) and the fields with
the bus at W_pm (hollow, dashed).

#### `make_all(res, cfg, outdir)`
Draws every figure whose input exists in `res`: figures 1–7 from the index-based steps,
8–12 once the `modes` step has run, 13 once `matched` has run.

---

## 7. `report_figures.py`

Writes the report's figures and Table 1 from `results_emode/`. Paths are relative to the
script, so it works from any folder. `TEXTWIDTH = 6.5` inches is the drawing width;
LaTeX scales the figures to the report's 17 cm text width. The `rcParams` block sets
DejaVu Sans (it ships with matplotlib, so the figures look the same everywhere), small
report font sizes, 300 dpi for the raster mode maps inside the PDFs, and
`pdf.fonttype = 42` (embedded TrueType fonts, so the text stays text). Like `plots.py`, it
switches pyplot to the `Agg` backend after its imports.

#### `load(folder)`
Reads `results.json`, in a `with` block.

#### `save(fig, name)`
Saves a PDF into `../mdm-design-study/figures/` with a tight bounding box and closes it.

#### `panel_label(ax, text)`
A bold, left-aligned panel title such as "(a) Coupling coefficient".

#### `fig_tradeoff(res)` → Fig. 2, `report_tradeoff.pdf`
(a) κ, (b) S_a − S_m and (c) Δn_min/(S_a − S_m) against access width, for both couplers.

#### `fig_tolerance(res)` → Fig. 3, `report_tolerance.pdf`
(a, b) unconverted power against ΔW for every access width, with the solved points and
the −15 dB line; (c) the tolerance, re-solved (solid) and first order (hollow squares,
dashed).

#### `fig_modes(res)` → Fig. 4, `report_modes.pdf`
Three couplers: TE0→TE1 at 320 and 480 nm (the narrowest and widest access) and TE0→TE2
at 320 nm. Each row shows the access strip alone, the bus strip alone and the two
supermodes, using the same panel, view and scale-bar functions as `plots.py`. The
vertical window is the silicon ± 300 nm, and the colour bar takes its scale from the
first panel's image and hides its outline as `_field_colorbar` does.

#### `fig_fieldchecks(res)` → Fig. 5, `report_fieldchecks.pdf`
(a) the access mode's evanescent tail (from the TE0→TE1 files; the bus starts 200 nm from
the access wall), (b) W* − W_pm from the fields (solid) and W* − W_iso (dashed),
(c) the unconverted power of the couplers built at W* at ΔW = 0, with the −15 dB line.

#### `table_designs(res)` → `generated/table_designs.tex`
The rows of Table 1: W_a, W*, W_pm (from the `modes` step), L_c, κ, S_a − S_m, the
tolerance re-solved, first order and at W_pm (`--` until the `matched` step has run), the
unconverted power at W* from the fields, and the worst C-band value. Negative numbers go
through `\num{}`, so LaTeX prints a proper minus sign.

#### `write(name, lines)`
Writes a generated LaTeX file with a "do not edit by hand" header.

#### `summary(res)`
Prints every number quoted in the report text, so each one can be traced: the 320 against
480 nm ratios (κ, mismatch, figure of merit, L_c, tolerance), the first-order minus
re-solved differences, the field checks (residual, splitting, TE fraction, edge fraction,
tails, shares, W*, W_pm, W_iso), the convergence and benchmark values, bend losses, and
the matched results (shares, unconverted power at ΔW = 0, L_pm against L_c, tolerance
differences, W_pm − W_iso).

#### `main()`
Runs all of the above in order.

Fixed choices that belong to this report and not to `CFG`: the −15 dB line, the 200 nm
gap in Fig. 5a, the three couplers of Fig. 4, and the 320 and 480 nm widths that
`summary` compares. They match the study as run; change them here if the study changes.

---

## 8. Changes since the guide was first written

### 23 Nov

- **W_iso is now found on the PCHIP curve** (`width_at_index`). Before, straight lines
  between sweep points 50 nm apart put it 0.1 to 0.9 nm too wide. The `design`, `modes`
  and `validate` steps were rerun from the cached EMode solves, with no new solve. W_pm
  now lies 0.4 to 1.2 nm (TE0→TE1) and 2.1 to 3.0 nm (TE0→TE2) above W_iso, and the
  report says "within 1.5 nm" and "within 3.2 nm", bounds that also hold for the exact
  values from EMode's bus solves. S_m, taken at W_iso, moved by 0.04 to 0.31 %, which
  changes the last digit of S_a − S_m in four rows of Table 1. No tolerance and no
  fold-change quoted in the report changed. The `tolerance`, `validate`, `modes` and
  `matched` steps were then rerun in EMode, so every result now comes from the corrected
  code. That changed one tolerance-step point (TE0→TE1, 320 nm, ΔW = +10 nm: Δn_min
  0.56 % lower after a scan from a new start) and re-solved the matched couplers at the
  corrected W_pm (at most 0.023 nm away); no tolerance and no number in the report text
  changed. The Dai benchmark's W_iso is now 1034.95 nm.
- `--resolution 10` is now stored as the int 10, so it keeps matching the cache.
- Fig. 7's title no longer states the hypothesis as a result ("Bend loss sets the lower
  limit on the access width"); it now reads "Bend loss of the access waveguide". The
  results show bend loss does not limit the access width for radii of 5 µm or more.
- `solver_emode.py` no longer says it has not been run with EMode, the `plots.py`
  docstring now names the figures that read saved fields (8 to 11), and the
  `TEXTWIDTH` comment now says LaTeX scales the figures to the 17 cm text width.

### 25 Nov: every Pylance and ruff finding fixed

No result changed. Every study step rerun from the EMode cache gives byte for byte the
same `results.json`, `summary.csv` and `modes_summary.csv` with the new code as with the
old; the 13 study figures are pixel for pixel the same, the four report figures differ
only in their creation date, and Table 1 is the same. The changed lines in `bend_loss`
and `_clad_index` run only in a new bend solve: the test double runs them, both tries
included, and both test scripts pass.

- **Types** (Pylance): `fixed_indices` is declared `tuple[float, float] | None`; `CFG`,
  `QUICK` and the dicts that `anticrossing` and `_mode_row` return are declared
  `dict[str, Any]`; `brentq`'s root goes through `cast(float, ...)`; `add_axes` gets a
  tuple; and EMode's answers go through `np.asarray` before numpy reads them
  (`_clad_index`, the `PML_indices` in `bend_loss`), as `_read` already did. Pylance
  shows the last two only on a machine where EMode's package is installed.
- **The colour-bar outline** is hidden through `cb.ax.spines["outline"]` instead of
  `cb.outline`, in `_field_colorbar` and `fig_modes`: with matplotlib 3.10, whose type
  hints call `cb.outline` a `Spines`, Pylance reported "Object of type "Spine" is not
  callable" in `report_figures.py`. Same object, same figures.
- **Variables set before they are used** (Pylance's "possibly unbound"): `anticrossing`
  does its first scan before the re-centring loop, `step_matched` its first check before
  the correction loop, and `bend_loss` keeps the first try's outcome in `result`. The
  mode-map colour bars take the first panel's image instead of a variable left over from
  the drawing loop, so `_field_panel` no longer returns one.
- **Files** (ruff SIM115): every file is opened in a `with` block (`read_json`,
  `Study.save`, `report_figures.load`, the plots-only path of `main`).
- **Style** (ruff): `dict(...)` calls became `{...}` literals (C408), the imports are
  sorted (I001) with the `Agg` backend switched after them, the `%` formats in
  `summary` became f-strings (UP031), and the shebang line went (EXE001: the script is
  run with `python`).
- **Deliberate broad catches** (ruff BLE001): seven `except Exception` blocks stay,
  marked `# noqa: BLE001` with their reason (see section 9).
- **Tests**: they load the study modules with `importlib` after setting their paths
  (no import below code, and no `noqa`), and the test double builds its fields in a
  loop Pylance can follow.

The tests in `../tests/` (a test double of `emodeconnection` and two test scripts) are
not part of the five scripts. They run the whole study through the EMode code path on a
made-up coupled-mode model, so they check the Python, not EMode's numbers.

---

## 9. Checking the code

**Ruff** (linter). `ruff.toml` in this folder keeps ruff's default rules and sets one
thing: the 120-character lines the scripts use. Where it sits matters too: ruff takes
the folder that holds it as the project root, so it counts the study's own modules
(`plots`, `modefields`, ...) as local imports and sorts the imports the same way
whichever folder it is started from. From `Photonics/`:

```
ruff check adc-emode-study tests
```

The five scripts and the tests pass ruff's default rules (the command above), the
smaller rule set older ruff versions used by default, and all of pycodestyle and
pyflakes at 120 characters:

```
ruff check --select E4,E7,E9,F adc-emode-study tests
ruff check --select E,W,F --line-length 120 adc-emode-study tests
```

`ruff.toml` covers only this folder, so the last check needs `--line-length 120` for the
tests; without it ruff measures their lines against its default of 88 characters. The
default rules do not check line length.

Seven `except Exception` blocks are deliberate, and ruff's rule against broad catches
(BLE001) is switched off on exactly those lines with `# noqa: BLE001` and a reason:

| Where | Why any error is caught |
| --- | --- |
| `EModeSolver._clad_index` | No cladding index from EMode: use 1.444 (SiO2) to place the bend window. |
| `EModeSolver._read_optional` | A missing diagnostic must not stop a run. |
| `EModeSolver.mode_fields` | Retry without the H fields. |
| `EModeSolver.bend_loss` | The first try failed: fall back to the seeded solve. |
| `Study.step_bend` | One failed bend is stored as NaN and the study goes on. |
| `Study.step_validate` | A failed TM benchmark is reported and the other checks go on. |
| `Study.step_modes` | A saved field file that cannot be read is solved again. |

**Pylance** (type checker, `"python.analysis.typeCheckingMode": "standard"` in this
repository's VS Code settings) reports nothing in the five scripts or the tests. This was
checked with EMode's package (`emodeconnection` 1.1.25) installed, both with matplotlib
3.10.8 and with 3.11.2. On a machine without EMode's package, the only report is that
`emodeconnection` cannot be imported. The same checks can be run outside VS Code with
Pyright, the checker inside Pylance, from `Photonics/` in the Python environment where
EMode is installed:

```
pip install pyright
pyright adc-emode-study tests
```
