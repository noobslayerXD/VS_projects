from pathlib import Path
import sys
import pandas as pd
import numpy as np

# Aflevering2.py
# Finds the first two CSV files in the script directory, loads them with pandas and
# plots the first two columns (or index vs single column) from each on the same plot.

import matplotlib.pyplot as plt

DIR = Path(__file__).parent
csv_files = sorted(DIR.glob("*.csv"))

if len(csv_files) < 2:
    print(f"Found {len(csv_files)} CSV file(s) in {DIR}. Need at least two.")
    sys.exit(1)

# Use the first two CSV files
csv_files = csv_files[:2]

plt.figure(figsize=(8, 5))
all_x_values = []
# Default axis labels
xlabel = "x"
ylabel = "y"
first_csv = True
converted_db_first = False

for csv_path in csv_files:
    df = pd.read_csv(csv_path)

    if df.shape[1] >= 2:
        x = df.iloc[:, 0]
        y = df.iloc[:, 1]
        if first_csv:
            # Use the first CSV's column headers if available
            try:
                cols = list(df.columns)
                if len(cols) >= 2:
                    xlabel = cols[0]
                    ylabel = cols[1]
            except Exception:
                pass
    elif df.shape[1] == 1:
        x = df.index
        y = df.iloc[:, 0]
        if first_csv:
            try:
                cols = list(df.columns)
                if len(cols) >= 1:
                    xlabel = "index"
                    ylabel = cols[0]
            except Exception:
                pass
    else:
        print(f"Skipping {csv_path.name}: no usable columns")
        continue

    # Attempt to convert y to numeric and, if successful, plot in dB.
    y_to_plot = y
    try:
        y_numeric = pd.to_numeric(y, errors="coerce")
        # Drop NaNs to see if any numeric data exist
        if not y_numeric.dropna().empty:
            # avoid log(0) by adding a tiny epsilon where values are zero
            eps = 1e-12
            y_safe = y_numeric.fillna(0)
            # compute 20*log10(abs(y)) safely
            with pd.option_context('mode.use_inf_as_na', True):
                y_db = 20 * np.log10(y_safe.abs() + eps)
            y_to_plot = y_db
            if first_csv:
                converted_db_first = True
        else:
            print(f"Note: y values in {csv_path.name} are non-numeric; plotting raw values.")
    except Exception:
        print(f"Warning: failed to convert y values in {csv_path.name} to numeric; plotting raw values.")

    plt.plot(x, y_to_plot, label=csv_path.name)

    # Try to collect numeric x values to decide if a log x-axis is safe.
    try:
        numeric_x = pd.to_numeric(x, errors="coerce").dropna()
        if not numeric_x.empty:
            all_x_values.append(numeric_x)
    except Exception:
        # If conversion fails for some reason, ignore this file for log-check
        pass

    # Mark that we've processed the first CSV so header-label extraction only runs once
    first_csv = False

plt.xlabel("x")
plt.ylabel("y")
plt.title("Combined plot of two CSV files")

# Apply labels extracted from CSV headers (if any)
plt.xlabel(xlabel)
if converted_db_first:
    plt.ylabel(f"{ylabel} (dB)")
else:
    plt.ylabel(ylabel)
plt.legend()
plt.grid(True)

# Determine whether to use a logarithmic x-axis.
use_log_x = False
if all_x_values:
    try:
        concatenated = pd.concat(all_x_values)
        # Use log scale only if all numeric x-values are strictly positive
        if (concatenated > 0).all():
            use_log_x = True
    except Exception:
        use_log_x = False

if use_log_x:
    plt.xscale("log")
else:
    if all_x_values:
        print("Note: x data contain non-positive or non-numeric values; using linear x-axis.")

out_path = DIR / "combined_plot.png"
plt.savefig(out_path, dpi=150)
print(f"Saved plot to: {out_path}")
plt.show()