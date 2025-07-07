import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# File paths (update if needed)
file_paths = [
    "simdata/lqr/Init_angle_1.57_seed_1_Nactor_6/3wrobotNI_lqr_2025-06-05_16h30m59s__run01.csv",  # Run 1
    "simdata/lqr/Init_angle_1.57_seed_1_Nactor_6/3wrobotNI_lqr_2025-06-05_17h26m58s__run01.csv",  # Run 2
    "simdata/lqr/Init_angle_1.57_seed_1_Nactor_6/3wrobotNI_lqr_2025-06-05_17h57m04s__run01.csv"   # Run 3
]

def load_csv(path):
    with open(path, "r") as f:
        lines = f.readlines()
    for i, line in enumerate(lines):
        if line.startswith("t [s]"):
            start_idx = i
            break
    df = pd.read_csv(path, skiprows=start_idx)
    df.columns = df.columns.str.strip().str.replace('"', '')
    df = df.dropna()
    df = df.apply(pd.to_numeric, errors='coerce')
    df = df.dropna()
    return df

# Load all runs
dfs = [load_csv(path) for path in file_paths]

# Colors per run
colors = ['blue', 'green', 'red']
labels = ['Run 1', 'Run 2', 'Run 3']

# 📊 Plot 1: Trajectory (x vs y)
plt.figure(figsize=(6, 5))
for i, df in enumerate(dfs):
    plt.plot(df['x [m]'], df['y [m]'], label=labels[i], color=colors[i])
plt.xlabel("x [m]")
plt.ylabel("y [m]")
plt.title("Trajectory: x vs y (LQR)")
plt.grid()
plt.legend()
plt.tight_layout()
plt.savefig("lqr_trajectory.png")
plt.show()

# 📊 Plot 2: Tracking Error vs Time
plt.figure(figsize=(6, 5))
for i, df in enumerate(dfs):
    error = np.sqrt(df['x [m]']**2 + df['y [m]']**2)
    plt.plot(df['t [s]'], error, label=labels[i], color=colors[i])
plt.xlabel("Time [s]")
plt.ylabel("Tracking Error [m]")
plt.title("Tracking Error vs Time (LQR)")
plt.grid()
plt.legend()
plt.tight_layout()
plt.savefig("lqr_tracking_error.png")
plt.show()

# 📊 Plot 3: Linear Velocity vs Time
plt.figure(figsize=(6, 5))
for i, df in enumerate(dfs):
    plt.plot(df['t [s]'], df['v [m/s]'], label=labels[i], color=colors[i])
plt.xlabel("Time [s]")
plt.ylabel("Linear Velocity [m/s]")
plt.title("Linear Velocity vs Time (LQR)")
plt.grid()
plt.legend()
plt.tight_layout()
plt.savefig("lqr_velocity.png")
plt.show()

# 📊 Plot 4: Angular Velocity vs Time
plt.figure(figsize=(6, 5))
for i, df in enumerate(dfs):
    plt.plot(df['t [s]'], df['omega [rad/s]'], label=labels[i], color=colors[i])
plt.xlabel("Time [s]")
plt.ylabel("Angular Velocity [rad/s]")
plt.title("Angular Velocity vs Time (LQR)")
plt.grid()
plt.legend()
plt.tight_layout()
plt.savefig("lqr_omega.png")
plt.show()
